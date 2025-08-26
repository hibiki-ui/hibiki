#!/usr/bin/env python3
"""
终极 TableView 测试 - 使用所有可能的崩溃防护措施
"""

import sys
import os
import gc
import signal
import faulthandler

# 启用错误处理
faulthandler.enable()

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import TableView, VStack, Label, Button
from macui.app import MacUIApp
from macui.core.object_registry import global_registry, force_retain_everything

set_log_level("INFO")

def setup_crash_protection():
    """设置崩溃保护"""
    def crash_handler(signum, frame):
        print(f"\n💥 接收到致命信号 {signum}!")
        print("📊 崩溃时的对象注册表状态:")
        
        try:
            from macui.core.object_registry import get_registry_stats, check_all_objects
            stats = get_registry_stats()
            print(f"统计: {stats}")
            check_all_objects()
        except Exception as e:
            print(f"无法获取注册表状态: {e}")
        
        print("\n📍 Python 调用栈:")
        faulthandler.dump_traceback()
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGSEGV, crash_handler)
    signal.signal(signal.SIGTRAP, crash_handler)
    signal.signal(signal.SIGABRT, crash_handler)
    print("🛡️ 崩溃保护已设置")

class UltimateTableTestApp(Component):
    """终极 TableView 测试应用组件"""
    
    def __init__(self):
        super().__init__()
        
        print("🔧 初始化终极测试组件...")
        
        # 使用 Component 的内置方法创建响应式状态
        self.data = self.create_signal([
            {"name": "终极测试1", "value": "稳定值1"},
            {"name": "终极测试2", "value": "稳定值2"},
            {"name": "终极测试3", "value": "稳定值3"},
        ])
        
        self.selected_row = self.create_signal(-1)
        self.status = self.create_signal("终极 TableView 测试准备就绪")
        self.update_count = self.create_signal(0)
        
        # 创建计算属性
        self.status_text = self.create_computed(
            lambda: f"状态: {self.status.value}"
        )
        self.selection_text = self.create_computed(
            lambda: f"选中行: {self.selected_row.value}"
        )
        self.count_text = self.create_computed(
            lambda: f"更新次数: {self.update_count.value}"
        )
        
        # 立即注册所有关键对象到全局注册表
        global_registry.register_critical_object(self.data, "signals", "ultimate_tableview_data")
        global_registry.register_critical_object(self.selected_row, "signals", "ultimate_tableview_selected")
        global_registry.register_critical_object(self.status, "signals", "ultimate_tableview_status")
        global_registry.register_critical_object(self.update_count, "signals", "ultimate_tableview_count")
        global_registry.register_critical_object(self.status_text, "computed", "ultimate_status_text")
        global_registry.register_critical_object(self.selection_text, "computed", "ultimate_selection_text")
        global_registry.register_critical_object(self.count_text, "computed", "ultimate_count_text")
        global_registry.register_critical_object(self, "components", "ultimate_tableview_test_app")
        
        print("🔒 所有关键对象已注册到全局注册表")
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 选择了行: {row}")
        self.update_count.value += 1
        
        if 0 <= row < len(self.data.value):
            item = self.data.value[row]
            self.status.value = f"选中: {item['name']} = {item['value']}"
        else:
            self.status.value = f"取消选择 (行 {row})"
    
    def add_test_row(self):
        """添加测试行"""
        current_count = len(self.data.value)
        new_data = list(self.data.value)
        new_data.append({
            "name": f"新增测试{current_count + 1}", 
            "value": f"新值{current_count + 1}"
        })
        self.data.value = new_data
        self.update_count.value += 1
        self.status.value = f"添加了新行，总共 {len(new_data)} 行"
        print(f"📊 添加了新行，总共 {len(new_data)} 行")
    
    def stress_test(self):
        """压力测试 - 快速更新数据"""
        print("🔥 开始压力测试...")
        for i in range(5):
            current_data = list(self.data.value)
            # 更新现有数据
            for j, item in enumerate(current_data):
                current_data[j] = {
                    "name": f"压力测试{j+1}",
                    "value": f"轮次{i+1}-值{j+1}"
                }
            self.data.value = current_data
            self.update_count.value += 1
            print(f"🔥 压力测试轮次 {i+1}/5 完成")
        
        self.status.value = "压力测试完成，数据更新5轮"
        print("✅ 压力测试完成")
    
    def mount(self):
        """构建组件视图"""
        print("🏗️ 构建终极测试视图...")
        
        return VStack(spacing=15, padding=20, children=[
            Label("终极 TableView 测试"),
            Label(self.status_text),
            Label(self.count_text),
            
            # 控制按钮
            VStack(spacing=8, children=[
                Button("添加测试行", on_click=self.add_test_row),
                Button("压力测试", on_click=self.stress_test),
            ]),
            
            # TableView - 核心测试对象
            TableView(
                columns=[
                    {"title": "名称", "key": "name", "width": 160},
                    {"title": "值", "key": "value", "width": 120},
                ],
                data=self.data,
                selected_row=self.selected_row,
                on_select=self.on_row_select,
                frame=(0, 0, 320, 180)
            ),
            
            Label(self.selection_text),
        ])

def main():
    """主函数"""
    print("🚀 启动终极 TableView 测试")
    
    # 设置崩溃保护
    setup_crash_protection()
    
    # 禁用垃圾回收作为额外保护
    gc.disable()
    print("🛡️ 垃圾回收已禁用")
    
    try:
        print("🧪 终极 TableView 测试开始...")
        
        # 创建应用
        app = MacUIApp("终极 TableView 测试")
        global_registry.register_critical_object(app, "apps", "ultimate_main_app")
        
        print("📱 创建终极组件...")
        test_component = UltimateTableTestApp()
        
        print("🏠 创建窗口...")
        window = app.create_window(
            title="终极 TableView 测试",
            size=(450, 450),
            resizable=True,
            content=test_component
        )
        
        # 注册窗口
        global_registry.register_critical_object(window, "windows", "ultimate_main_window")
        
        print("👀 显示窗口...")
        window.show()
        
        # 多次强制保护
        force_retain_everything()
        force_retain_everything()  # 双重保护
        
        print("🛡️ 终极对象保护已启用")
        
        # 显示注册表统计
        from macui.core.object_registry import get_registry_stats, check_all_objects
        stats = get_registry_stats()
        print(f"📊 对象注册表统计: {stats}")
        
        print("🎬 开始运行终极测试应用...")
        print("=" * 50)
        print("终极测试说明:")
        print("- 应该看到一个包含表格的窗口")
        print("- 可以点击行来选择")
        print("- 可以点击'添加测试行'按钮")
        print("- 可以点击'压力测试'按钮")
        print("- 选择行时状态会更新")
        print("- 按 Ctrl+C 退出")
        print("=" * 50)
        
        # 运行应用
        app.run()
        
        print("✅ 应用正常结束")
        
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
        
        # 显示崩溃时的对象状态
        try:
            from macui.core.object_registry import check_all_objects
            print("\n崩溃时的对象状态:")
            check_all_objects()
        except:
            pass
    
    finally:
        # 重新启用垃圾回收
        gc.enable()
        print("🔄 垃圾回收已重新启用")
        print("✅ 终极测试结束")

if __name__ == "__main__":
    main()