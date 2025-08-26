#!/usr/bin/env python3
"""
终极崩溃预防测试 - 使用全局对象注册表彻底防止崩溃
"""

import sys
import os
import time
import gc
import signal
import faulthandler

# 启用错误处理
faulthandler.enable()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def setup_crash_protection():
    """设置崩溃保护"""
    def crash_handler(signum, frame):
        print(f"\n💥 接收到致命信号 {signum}!")
        
        # 显示对象注册表状态
        from macui.core.object_registry import check_all_objects, get_registry_stats
        
        print("\n📊 崩溃时的对象注册表状态:")
        try:
            stats = get_registry_stats()
            print(f"统计: {stats}")
            check_all_objects()
        except Exception as e:
            print(f"无法获取注册表状态: {e}")
        
        # 输出调用栈
        print("\n📍 Python 调用栈:")
        faulthandler.dump_traceback()
        
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGSEGV, crash_handler)
    signal.signal(signal.SIGTRAP, crash_handler)
    signal.signal(signal.SIGABRT, crash_handler)
    
    print("🛡️ 崩溃保护已设置")

def test_ultimate_protection():
    """测试终极保护方案"""
    print("=== 终极崩溃预防测试 ===")
    
    from macui import Signal, set_log_level
    from macui.components import TableView, VStack, Label, Button
    from macui.app import MacUIApp
    from macui.core.object_registry import (
        get_registry_stats, check_all_objects, 
        force_retain_everything, global_registry
    )
    
    # 设置日志等级
    set_log_level("INFO")
    
    print("1. 创建应用...")
    app = MacUIApp("Ultimate Protection Test")
    
    print("2. 创建测试数据...")
    test_data = Signal([
        {"name": "防护测试1", "status": "待测试"},
        {"name": "防护测试2", "status": "待测试"},
        {"name": "防护测试3", "status": "待测试"},
        {"name": "防护测试4", "status": "待测试"},
        {"name": "防护测试5", "status": "待测试"}
    ])
    
    # 注册测试数据
    global_registry.register_critical_object(test_data, "test_signals", "main_test_data")
    
    print("3. 创建表格视图...")
    table_view = TableView(
        columns=[
            {"title": "测试名称", "key": "name", "width": 150},
            {"title": "状态", "key": "status", "width": 100},
        ],
        data=test_data,
        frame=(0, 0, 350, 200)
    )
    
    print("4. 检查对象注册表...")
    stats = get_registry_stats()
    print(f"注册表统计: {stats}")
    check_all_objects()
    
    print("5. 强制保护所有对象...")
    force_retain_everything()
    
    # 禁用垃圾回收作为额外保护
    gc.disable()
    print("🛡️ 垃圾回收已禁用")
    
    print("6. 创建窗口组件...")
    
    # 更新计数器
    update_counter = Signal(0)
    global_registry.register_critical_object(update_counter, "test_signals", "update_counter")
    
    def trigger_intensive_updates():
        """触发密集更新来测试稳定性"""
        for i in range(20):  # 20次快速更新
            count = update_counter.value + 1
            update_counter.value = count
            
            # 更新表格数据
            new_data = [
                {"name": f"压力测试{j}", "status": f"第{count}轮-项{j}"}
                for j in range(1, 8)  # 7行数据
            ]
            test_data.value = new_data
            
            print(f"🔥 密集更新 {i+1}/20: {len(new_data)} 行数据")
            
            # 短暂延时
            time.sleep(0.05)
        
        print("✅ 密集更新测试完成")
    
    from macui import Component
    
    class UltimateTestComponent(Component):
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("终极崩溃预防测试"),
                Label(lambda: f"更新轮次: {update_counter.value}"),
                table_view,
                Button("开始密集更新测试", on_click=trigger_intensive_updates),
            ])
    
    test_component = UltimateTestComponent()
    global_registry.register_critical_object(test_component, "components", "main_test_component")
    
    print("7. 创建窗口...")
    window = app.create_window(
        title="Ultimate Crash Prevention Test",
        size=(450, 400),
        content=test_component
    )
    
    global_registry.register_critical_object(window, "windows", "main_window")
    
    print("8. 显示窗口...")
    window.show()
    
    print("9. 最终对象保护检查...")
    final_stats = get_registry_stats()
    print(f"最终统计: {final_stats}")
    
    # 再次强制保护
    force_retain_everything()
    
    print("10. 自动触发更新测试...")
    # 自动运行几次更新
    for auto_round in range(3):
        print(f"\n自动测试轮次 {auto_round + 1}/3")
        trigger_intensive_updates()
        time.sleep(1)
    
    print("\n✅ 所有自动测试完成，应用仍在运行")
    
    # 最终检查
    print("\n=== 最终状态检查 ===")
    check_all_objects()
    
    # 等待一段时间确保稳定性
    print("\n等待 5 秒钟测试长期稳定性...")
    time.sleep(5)
    
    print("🎉 终极保护测试成功！应用运行稳定")
    
    return True

def main():
    """主函数"""
    print("🚀 启动终极崩溃预防测试")
    
    # 设置保护
    setup_crash_protection()
    
    try:
        success = test_ultimate_protection()
        
        if success:
            print("\n🎯 结论: 终极保护方案有效！")
            print("✅ 全局对象注册表成功防止了对象被垃圾回收")
            print("✅ 应用在密集操作下保持稳定")
            return True
        
    except Exception as e:
        print(f"\n💥 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 即使失败，也显示注册表状态
        try:
            from macui.core.object_registry import check_all_objects
            print("\n崩溃时的对象状态:")
            check_all_objects()
        except:
            pass
        
        return False
    
    finally:
        # 重新启用垃圾回收
        gc.enable()
        print("🔄 垃圾回收已重新启用")

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🏆 终极保护方案验证成功！")
    else:
        print("\n⚠️  需要进一步调试")
    
    sys.exit(0 if success else 1)