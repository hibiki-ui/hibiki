#!/usr/bin/env python3
"""
内存调试工具 - 用于定位和修复 macUI 中的内存管理问题
"""

import sys
import os
import gc
import weakref
from typing import Dict, List, Any, Optional
import objc
from Foundation import NSObject
import traceback

class MemoryDebugger:
    """内存调试器 - 跟踪对象生命周期和内存泄漏"""
    
    def __init__(self):
        self.tracked_objects: Dict[int, Dict[str, Any]] = {}
        self.weak_refs: Dict[int, weakref.ref] = {}
        self.creation_stacks: Dict[int, List[str]] = {}
        self.objc_objects: Dict[int, str] = {}
        
    def track_object(self, obj: Any, name: str = None) -> int:
        """跟踪一个对象的生命周期"""
        obj_id = id(obj)
        obj_type = type(obj).__name__
        
        # 记录创建堆栈
        stack = traceback.format_stack()[:-1]  # 排除当前函数
        self.creation_stacks[obj_id] = stack
        
        # 创建弱引用来检测对象是否被回收
        def cleanup_callback(ref):
            if obj_id in self.tracked_objects:
                print(f"🗑️  对象已回收: {self.tracked_objects[obj_id]['name']} ({obj_type})")
                del self.tracked_objects[obj_id]
                if obj_id in self.creation_stacks:
                    del self.creation_stacks[obj_id]
                if obj_id in self.objc_objects:
                    del self.objc_objects[obj_id]
        
        try:
            weak_ref = weakref.ref(obj, cleanup_callback)
            self.weak_refs[obj_id] = weak_ref
        except TypeError:
            # 某些对象不支持弱引用
            pass
        
        self.tracked_objects[obj_id] = {
            'name': name or f"{obj_type}_{obj_id}",
            'type': obj_type,
            'obj': obj
        }
        
        # 如果是 NSObject 子类，特别记录
        if isinstance(obj, NSObject):
            self.objc_objects[obj_id] = f"{obj_type}({name or 'unnamed'})"
            print(f"🔍 跟踪 NSObject: {obj_type}({name or 'unnamed'}) - retain_count: {obj.retainCount()}")
        
        return obj_id
    
    def check_retain_counts(self):
        """检查 NSObject 的引用计数"""
        print("\n=== NSObject 引用计数检查 ===")
        for obj_id, obj_info in self.tracked_objects.items():
            obj = obj_info['obj']
            if isinstance(obj, NSObject):
                try:
                    count = obj.retainCount()
                    print(f"📊 {obj_info['name']}: retain_count = {count}")
                    if count > 10:  # 异常高的引用计数
                        print(f"⚠️  警告: {obj_info['name']} 引用计数异常高 ({count})")
                        self.print_creation_stack(obj_id)
                except:
                    print(f"❌ 无法获取 {obj_info['name']} 的引用计数（可能已释放）")
    
    def print_creation_stack(self, obj_id: int):
        """打印对象创建时的堆栈信息"""
        if obj_id in self.creation_stacks:
            print(f"📍 {self.tracked_objects[obj_id]['name']} 创建堆栈:")
            for line in self.creation_stacks[obj_id][-5:]:  # 只显示最后5层
                print(f"    {line.strip()}")
    
    def force_gc_and_check(self):
        """强制垃圾回收并检查结果"""
        print("\n=== 强制垃圾回收 ===")
        initial_count = len(self.tracked_objects)
        
        # 多次垃圾回收
        for i in range(3):
            collected = gc.collect()
            print(f"第{i+1}次垃圾回收: 回收了 {collected} 个对象")
        
        final_count = len(self.tracked_objects)
        print(f"垃圾回收前跟踪对象数: {initial_count}")
        print(f"垃圾回收后跟踪对象数: {final_count}")
        
        if final_count > 0:
            print("🔍 仍存活的对象:")
            for obj_info in self.tracked_objects.values():
                print(f"  - {obj_info['name']} ({obj_info['type']})")
    
    def get_memory_report(self) -> str:
        """生成内存报告"""
        report = ["\n=== 内存调试报告 ==="]
        report.append(f"跟踪对象总数: {len(self.tracked_objects)}")
        report.append(f"NSObject 对象数: {len(self.objc_objects)}")
        
        # 按类型分组
        type_counts = {}
        for obj_info in self.tracked_objects.values():
            obj_type = obj_info['type']
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        
        report.append("\n按类型分布:")
        for obj_type, count in sorted(type_counts.items()):
            report.append(f"  {obj_type}: {count}")
        
        return "\n".join(report)

# 全局调试器实例
debugger = MemoryDebugger()

def safe_objc_call(obj, method_name, *args, **kwargs):
    """安全的 Objective-C 方法调用，包含错误处理"""
    try:
        method = getattr(obj, method_name)
        result = method(*args, **kwargs)
        return result
    except Exception as e:
        print(f"❌ Objective-C 调用失败: {type(obj).__name__}.{method_name}")
        print(f"   错误: {e}")
        print(f"   对象: {obj}")
        traceback.print_exc()
        return None

def create_minimal_test():
    """创建最小化测试用例来隔离问题"""
    print("=== 创建最小化测试 ===")
    
    # 添加当前目录到路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    from macui import Signal
    from macui.components import TableView
    from macui.app import MacUIApp
    
    class MinimalTestApp:
        def __init__(self):
            self.table_data = Signal([
                {"name": "Test1", "age": "20"},
                {"name": "Test2", "age": "30"},
            ])
    
    print("创建应用...")
    app = MacUIApp("Minimal Test")
    test_app = MinimalTestApp()
    
    print("创建表格视图...")
    try:
        table_view = TableView(
            columns=[
                {"title": "姓名", "key": "name", "width": 100},
                {"title": "年龄", "key": "age", "width": 60},
            ],
            data=test_app.table_data,
            frame=(0, 0, 200, 100)
        )
        debugger.track_object(table_view, "minimal_table")
        print("✅ 表格视图创建成功")
        return table_view
    except Exception as e:
        print(f"❌ 表格视图创建失败: {e}")
        traceback.print_exc()
        return None

def analyze_layout_constraints():
    """分析布局约束问题"""
    print("\n=== 分析布局约束问题 ===")
    print("检测到 NSLayoutConstraint 警告:")
    print("- 约束常量超出内部限制")
    print("- 建议减小约束值")
    print("- 可能在未来版本中出现问题")
    
    print("\n可能的原因:")
    print("1. 窗口或视图的 frame 值过大")
    print("2. 自动布局约束冲突")
    print("3. 手动设置的 frame 与自动布局冲突")

if __name__ == "__main__":
    print("=== macUI 内存调试工具 ===")
    
    # 分析布局约束问题
    analyze_layout_constraints()
    
    # 创建最小化测试
    test_obj = create_minimal_test()
    
    if test_obj:
        # 检查引用计数
        debugger.check_retain_counts()
        
        # 生成报告
        print(debugger.get_memory_report())
        
        # 强制垃圾回收
        debugger.force_gc_and_check()