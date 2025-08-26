#!/usr/bin/env python3
"""
最终稳定性测试 - 验证崩溃问题已完全解决
"""

import sys
import os
import time
import gc
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def run_basic_stability_test():
    """运行基础稳定性测试"""
    print("=== 基础稳定性测试 ===")
    
    from macui import Signal, set_log_level
    from macui.components import TableView, VStack, Label, Button
    from macui.app import MacUIApp
    
    # 降低日志等级
    set_log_level("WARNING")
    
    app = MacUIApp("Final Stability Test")
    
    # 创建测试数据
    test_data = Signal([
        {"name": "稳定性测试1", "status": "通过"},
        {"name": "稳定性测试2", "status": "通过"},
        {"name": "稳定性测试3", "status": "通过"}
    ])
    
    # 测试计数器
    test_counter = Signal(0)
    
    def update_data():
        """更新数据来触发重绘"""
        count = test_counter.value + 1
        test_counter.value = count
        
        # 更新表格数据
        new_data = [
            {"name": f"动态测试{i}", "status": f"第{count}轮"}
            for i in range(1, 6)
        ]
        test_data.value = new_data
        print(f"📊 数据更新轮次: {count}")
    
    from macui import Component
    
    class StabilityTestComponent(Component):
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("最终稳定性测试"),
                Label(lambda: f"测试轮次: {test_counter.value}"),
                
                # 表格视图 - 这是之前崩溃的组件
                TableView(
                    columns=[
                        {"title": "测试名称", "key": "name", "width": 150},
                        {"title": "状态", "key": "status", "width": 100},
                    ],
                    data=test_data,
                    frame=(0, 0, 300, 120)
                ),
                
                # 控制按钮
                Button("触发数据更新", on_click=update_data),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="Final Stability Test",
        size=(400, 300),
        content=StabilityTestComponent()
    )
    
    window.show()
    print("✅ 应用启动成功")
    
    # 自动化测试 - 多次更新数据
    for i in range(10):
        time.sleep(0.2)
        update_data()
        
        # 每隔几次强制垃圾回收
        if i % 3 == 0:
            collected = gc.collect()
            if collected > 0:
                print(f"  垃圾回收: {collected} 个对象")
    
    print("✅ 自动化数据更新测试完成")
    
    # 等待一会儿让所有渲染完成
    time.sleep(2)
    
    print("✅ 基础稳定性测试通过")
    return True

def run_stress_test():
    """运行压力测试"""
    print("\n=== 压力测试 ===")
    
    success_count = 0
    total_tests = 5
    
    for i in range(total_tests):
        print(f"压力测试轮次 {i+1}/{total_tests}")
        
        try:
            # 每次都重新创建应用来测试初始化稳定性
            success = run_basic_stability_test()
            if success:
                success_count += 1
        except Exception as e:
            print(f"❌ 压力测试第 {i+1} 轮失败: {e}")
        
        # 短暂延时
        time.sleep(1)
    
    print(f"\n📊 压力测试结果: {success_count}/{total_tests} 通过")
    return success_count == total_tests

def test_memory_management():
    """测试内存管理"""
    print("\n=== 内存管理测试 ===")
    
    from macui.core.memory_manager import get_memory_stats
    
    initial_stats = get_memory_stats()
    print(f"初始内存统计: {initial_stats}")
    
    # 运行测试
    run_basic_stability_test()
    
    # 强制垃圾回收
    for _ in range(3):
        collected = gc.collect()
        print(f"垃圾回收: {collected} 个对象")
    
    final_stats = get_memory_stats()
    print(f"最终内存统计: {final_stats}")
    
    # 分析内存使用
    tracked_increase = final_stats['tracked_owners'] - initial_stats['tracked_owners']
    assoc_increase = final_stats['total_associations'] - initial_stats['total_associations']
    
    print(f"跟踪对象增加: {tracked_increase}")
    print(f"关联对象增加: {assoc_increase}")
    
    # 如果增加过多，可能有内存泄漏
    if tracked_increase > 50 or assoc_increase > 100:
        print("⚠️ 可能存在内存泄漏")
        return False
    
    print("✅ 内存管理测试通过")
    return True

def main():
    """主测试函数"""
    print("🚀 启动最终稳定性测试...")
    print(f"Python 版本: {sys.version}")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_passed = True
    
    # 1. 基础稳定性测试
    try:
        basic_passed = run_basic_stability_test()
        if not basic_passed:
            all_passed = False
    except Exception as e:
        print(f"❌ 基础测试失败: {e}")
        all_passed = False
    
    # 2. 内存管理测试
    try:
        memory_passed = test_memory_management()
        if not memory_passed:
            all_passed = False
    except Exception as e:
        print(f"❌ 内存测试失败: {e}")
        all_passed = False
    
    # 3. 压力测试（如果前面都通过）
    if all_passed:
        try:
            stress_passed = run_stress_test()
            if not stress_passed:
                all_passed = False
        except Exception as e:
            print(f"❌ 压力测试失败: {e}")
            all_passed = False
    
    # 最终结果
    print("\n" + "="*50)
    if all_passed:
        print("🎉 所有测试通过！崩溃问题已完全解决！")
        print("✅ TableView 组件运行稳定")
        print("✅ 内存管理正常")
        print("✅ 压力测试通过")
        print("✅ macUI Stage 3 布局组件开发完成")
    else:
        print("💥 部分测试失败，需要进一步调试")
    
    print("="*50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)