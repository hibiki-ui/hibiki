#!/usr/bin/env python3
"""
最小 TableView 测试 - 只包含必要的组件
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import TableView, VStack, Label
from macui.app import MacUIApp
from macui.core.object_registry import global_registry

set_log_level("INFO")

class MinimalTableTestApp(Component):
    """TableView 测试应用组件"""
    
    def __init__(self):
        super().__init__()
        
        # 使用 Component 的内置方法创建响应式状态
        self.data = self.create_signal([
            {"name": "测试1", "value": "值1"},
            {"name": "测试2", "value": "值2"},
        ])
        
        self.selected_row = self.create_signal(-1)
        self.status = self.create_signal("TableView 测试准备就绪")
        
        # 创建计算属性
        self.status_text = self.create_computed(
            lambda: f"状态: {self.status.value}"
        )
        self.selection_text = self.create_computed(
            lambda: f"选中行: {self.selected_row.value}"
        )
        
        # 立即注册关键对象到全局注册表以防止垃圾回收
        global_registry.register_critical_object(self.data, "signals", "tableview_data")
        global_registry.register_critical_object(self.selected_row, "signals", "tableview_selected")
        global_registry.register_critical_object(self.status, "signals", "tableview_status")
        global_registry.register_critical_object(self, "components", "tableview_test_app")
        print("🔒 关键对象已注册到全局注册表")
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 选择了行: {row}")
        if 0 <= row < len(self.data.value):
            item = self.data.value[row]
            self.status.value = f"选中: {item['name']} = {item['value']}"
        else:
            self.status.value = f"取消选择 (行 {row})"
    
    def mount(self):
        """构建组件视图"""
        return VStack(spacing=15, padding=20, children=[
            Label("最小 TableView 测试"),
            Label(self.status_text),
            
            TableView(
                columns=[
                    {"title": "名称", "key": "name", "width": 150},
                    {"title": "值", "key": "value", "width": 100},
                ],
                data=self.data,
                selected_row=self.selected_row,
                on_select=self.on_row_select,
                frame=(0, 0, 300, 150)
            ),
            
            Label(self.selection_text),
        ])

def main():
    print("🧪 最小 TableView 测试开始...")
    print("请稍等，正在初始化...")
    
    # 创建应用
    app = MacUIApp("最小 TableView 测试")
    global_registry.register_critical_object(app, "apps", "main_app")
    
    print("📱 创建组件和窗口...")
    test_component = MinimalTableTestApp()
    
    window = app.create_window(
        title="最小 TableView 测试",
        size=(400, 300),
        resizable=True,
        content=test_component
    )
    
    # 注册窗口和组件
    global_registry.register_critical_object(window, "windows", "main_window")
    
    print("👀 显示窗口...")
    window.show()
    
    # 强制保护所有对象
    from macui.core.object_registry import force_retain_everything
    force_retain_everything()
    print("🛡️ 所有对象已强制保护")
    
    print("🎬 开始运行应用...")
    print("=" * 40)
    print("测试说明:")
    print("- 应该看到一个包含表格的窗口")
    print("- 可以点击行来选择")
    print("- 选择行时状态会更新")
    print("- 按 Ctrl+C 退出")
    print("=" * 40)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    except Exception as e:
        print(f"\n❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ 测试结束")

if __name__ == "__main__":
    main()