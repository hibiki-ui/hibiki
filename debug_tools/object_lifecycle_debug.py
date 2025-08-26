#!/usr/bin/env python3
"""
对象生命周期调试器 - 专门调试对象过早释放问题
"""

import sys
import os
import weakref
import gc
import objc
from typing import Dict, List, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

class ObjectLifecycleTracker:
    """对象生命周期跟踪器"""
    
    def __init__(self):
        self.tracked_objects: Dict[int, Dict[str, Any]] = {}
        self.strong_references: List[Any] = []  # 强引用列表防止垃圾回收
        
    def track_object(self, obj, name: str, keep_strong_ref: bool = True):
        """跟踪对象生命周期"""
        obj_id = id(obj)
        
        print(f"🔍 开始跟踪对象: {name} (id: {obj_id}, type: {type(obj).__name__})")
        
        # 记录对象信息
        self.tracked_objects[obj_id] = {
            'name': name,
            'type': type(obj).__name__,
            'obj': obj,
            'retained': keep_strong_ref
        }
        
        # 如果需要，保持强引用
        if keep_strong_ref:
            self.strong_references.append(obj)
            print(f"  ✅ 保持强引用: {name}")
        
        # 如果是 NSObject，输出引用计数
        if hasattr(obj, 'retainCount'):
            try:
                count = obj.retainCount()
                print(f"  📊 引用计数: {count}")
            except:
                print(f"  ⚠️ 无法获取引用计数")
        
        # 设置弱引用监控
        try:
            def cleanup_callback(ref):
                print(f"🗑️ 对象已被回收: {name} (id: {obj_id})")
                if obj_id in self.tracked_objects:
                    del self.tracked_objects[obj_id]
            
            weakref.ref(obj, cleanup_callback)
        except TypeError:
            print(f"  ⚠️ 对象不支持弱引用: {name}")
        
        return obj_id
    
    def check_all_objects(self):
        """检查所有跟踪对象的状态"""
        print("\n=== 对象生命周期检查 ===")
        
        for obj_id, info in self.tracked_objects.items():
            name = info['name']
            obj = info['obj']
            
            print(f"🔍 检查对象: {name}")
            
            # 检查对象是否仍然有效
            try:
                obj_type = type(obj).__name__
                print(f"  ✅ 对象有效: {obj_type}")
                
                # 如果是 NSObject，检查引用计数
                if hasattr(obj, 'retainCount'):
                    try:
                        count = obj.retainCount()
                        print(f"  📊 当前引用计数: {count}")
                        
                        if count <= 0:
                            print(f"  ⚠️ 警告: 引用计数异常 ({count})")
                    except Exception as e:
                        print(f"  ❌ 无法获取引用计数: {e}")
                
            except Exception as e:
                print(f"  💥 对象已失效: {e}")
    
    def force_retain_all(self):
        """强制保持所有对象的引用"""
        print("\n=== 强制保持所有对象引用 ===")
        
        for obj_id, info in self.tracked_objects.items():
            name = info['name']
            obj = info['obj']
            
            if not info['retained']:
                self.strong_references.append(obj)
                info['retained'] = True
                print(f"✅ 强制保持引用: {name}")

# 全局跟踪器
lifecycle_tracker = ObjectLifecycleTracker()

def create_safe_table_test():
    """创建安全的表格测试，重点关注对象生命周期"""
    print("=== 创建安全的表格测试（对象生命周期版本） ===")
    
    from macui.app import MacUIApp
    from macui import Signal
    from AppKit import NSScrollView, NSTableView, NSTableColumn
    from Foundation import NSMakeRect
    
    # 创建应用
    app = MacUIApp("Object Lifecycle Test")
    lifecycle_tracker.track_object(app, "MacUIApp", True)
    
    # 创建测试数据 - 使用 Signal
    test_data = Signal([
        {"name": "对象1", "value": "值1"},
        {"name": "对象2", "value": "值2"},
        {"name": "对象3", "value": "值3"}
    ])
    lifecycle_tracker.track_object(test_data, "test_data_signal", True)
    
    print("1. 创建 NSScrollView...")
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setFrame_(NSMakeRect(0, 0, 400, 200))
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)
    lifecycle_tracker.track_object(scroll_view, "NSScrollView", True)
    
    print("2. 创建 NSTableView...")
    table_view = NSTableView.alloc().init()
    lifecycle_tracker.track_object(table_view, "NSTableView", True)
    
    print("3. 创建表格列...")
    name_column = NSTableColumn.alloc().init()
    name_column.setIdentifier_("name")
    name_column.setWidth_(150)
    name_column.headerCell().setStringValue_("姓名")
    table_view.addTableColumn_(name_column)
    lifecycle_tracker.track_object(name_column, "name_column", True)
    
    value_column = NSTableColumn.alloc().init()
    value_column.setIdentifier_("value")
    value_column.setWidth_(200)
    value_column.headerCell().setStringValue_("值")
    table_view.addTableColumn_(value_column)
    lifecycle_tracker.track_object(value_column, "value_column", True)
    
    print("4. 设置文档视图...")
    scroll_view.setDocumentView_(table_view)
    
    print("5. 创建数据源...")
    from macui.core.binding import EnhancedTableViewDataSource
    
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.data = test_data.value  # 设置初始数据
    data_source.columns = ["name", "value"]
    
    # 这是关键 - 强制保持数据源引用！
    lifecycle_tracker.track_object(data_source, "TableViewDataSource", True)
    
    print("6. 设置数据源到表格...")
    table_view.setDataSource_(data_source)
    
    print("7. 创建数据绑定...")
    def update_table_data():
        try:
            print(f"📊 更新表格数据: {len(test_data.value)} 行")
            data_source.data = test_data.value
            table_view.reloadData()
        except Exception as e:
            print(f"❌ 数据更新失败: {e}")
    
    from macui.core.signal import Effect
    effect = Effect(update_table_data)
    lifecycle_tracker.track_object(effect, "data_effect", True)
    
    # 检查所有对象状态
    lifecycle_tracker.check_all_objects()
    
    return {
        'app': app,
        'scroll_view': scroll_view,
        'table_view': table_view,
        'data_source': data_source,
        'test_data': test_data,
        'effect': effect
    }

def test_object_lifecycle():
    """测试对象生命周期"""
    print("=== 开始对象生命周期测试 ===")
    
    # 创建测试组件
    components = create_safe_table_test()
    
    print("\n8. 创建窗口...")
    from macui.core.component import Component
    from AppKit import NSView
    from Foundation import NSMakeRect
    
    class SafeContainer(Component):
        def mount(self):
            container = NSView.alloc().init()
            container.setFrame_(NSMakeRect(0, 0, 500, 300))
            container.addSubview_(components['scroll_view'])
            lifecycle_tracker.track_object(container, "container_view", True)
            return container
    
    container_component = SafeContainer()
    lifecycle_tracker.track_object(container_component, "SafeContainer", True)
    
    window = components['app'].create_window(
        title="Object Lifecycle Test",
        size=(500, 300),
        content=container_component
    )
    lifecycle_tracker.track_object(window, "window", True)
    
    print("9. 显示窗口...")
    window.show()
    
    print("10. 强制保持所有对象引用...")
    lifecycle_tracker.force_retain_all()
    
    print("11. 检查对象状态...")
    lifecycle_tracker.check_all_objects()
    
    print("12. 手动触发数据源方法...")
    table_view = components['table_view']
    data_source = components['data_source']
    
    try:
        # 手动调用数据源方法
        row_count = data_source.numberOfRowsInTableView_(table_view)
        print(f"   数据源返回行数: {row_count}")
        
        for row in range(row_count):
            for col_idx, column in enumerate(table_view.tableColumns()):
                value = data_source.tableView_objectValueForTableColumn_row_(table_view, column, row)
                print(f"   [{row}, {col_idx}] = '{value}'")
        
        print("✅ 手动数据源调用成功")
        
    except Exception as e:
        print(f"❌ 手动数据源调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("13. 触发表格重绘...")
    try:
        table_view.reloadData()
        print("✅ 表格重绘成功")
        
        # 等待一会儿让渲染完成
        import time
        time.sleep(1)
        
        print("14. 再次重绘...")
        table_view.reloadData()
        time.sleep(0.5)
        
        print("✅ 所有测试完成，没有崩溃")
        
    except Exception as e:
        print(f"❌ 表格重绘失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 最终检查
    print("\n=== 最终对象状态检查 ===")
    lifecycle_tracker.check_all_objects()
    
    print(f"📊 跟踪的对象数量: {len(lifecycle_tracker.tracked_objects)}")
    print(f"📊 强引用数量: {len(lifecycle_tracker.strong_references)}")
    
    return True

if __name__ == "__main__":
    print("=== 对象生命周期调试器 ===")
    
    # 禁用垃圾回收来防止意外回收
    gc.disable()
    print("🛡️ 已禁用垃圾回收")
    
    try:
        success = test_object_lifecycle()
        
        if success:
            print("\n🎉 对象生命周期测试成功！")
        else:
            print("\n💥 对象生命周期测试失败！")
    
    finally:
        # 重新启用垃圾回收
        gc.enable()
        print("🔄 已重新启用垃圾回收")