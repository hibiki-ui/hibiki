#!/usr/bin/env python3
"""
混合 TableView 测试 - 从工作的组件开始，逐步添加 TableView
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import VStack, Label, Button, TableView
from macui.app import MacUIApp

set_log_level("INFO")

class HybridTableViewApp(Component):
    """混合 TableView 应用 - 从简单组件开始"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化混合测试组件...")
        
        # 基础状态 - 模仿 minimal_working_test.py
        self.message = self.create_signal("Ready")
        self.counter = self.create_signal(0)
        self.show_table = self.create_signal(False)
        
        # TableView 数据
        self.table_data = self.create_signal([
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
        
        # 计算属性
        self.status_text = self.create_computed(
            lambda: f"Status: {self.message.value}"
        )
        self.counter_text = self.create_computed(
            lambda: f"Count: {self.counter.value}"
        )
        self.table_status = self.create_computed(
            lambda: "Table Visible" if self.show_table.value else "Table Hidden"
        )
    
    def increment(self):
        """增加计数"""
        self.counter.value += 1
        self.message.value = f"Clicked {self.counter.value} times"
        print(f"✅ Button clicked: {self.counter.value}")
    
    def toggle_table(self):
        """切换 TableView 显示"""
        self.show_table.value = not self.show_table.value
        status = "显示" if self.show_table.value else "隐藏"
        self.message.value = f"TableView {status}"
        print(f"🔄 TableView toggled: {status}")
    
    def on_row_select(self, row):
        """TableView 行选择回调"""
        print(f"📊 TableView row selected: {row}")
        if 0 <= row < len(self.table_data.value):
            item = self.table_data.value[row]
            self.message.value = f"Selected: {item['name']}"
        else:
            self.message.value = "No selection"
    
    def mount(self):
        """构建组件视图"""
        print("🏗️ Building hybrid view...")
        
        # 基础控件（已验证可工作）
        basic_controls = [
            Label("Hybrid TableView Test"),
            Label(self.status_text),
            Label(self.counter_text),
            Label(self.table_status),
            
            Button("Click Me", on_click=self.increment),
            Button("Toggle Table", on_click=self.toggle_table),
        ]
        
        # 如果启用 TableView，添加它
        if self.show_table.value:
            print("📋 Adding TableView to layout...")
            table_view = TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 100},
                    {"title": "Value", "key": "value", "width": 60},
                ],
                data=self.table_data,
                selected_row=self.selected_row,
                on_select=self.on_row_select,
                frame=(0, 0, 180, 100)
            )
            basic_controls.append(table_view)
        else:
            print("📋 TableView hidden")
        
        return VStack(spacing=15, padding=20, children=basic_controls)

def main():
    """主函数"""
    print("🚀 Hybrid TableView Test Starting...")
    
    # 创建应用
    app = MacUIApp("Hybrid TableView Test")
    
    print("📱 Creating component and window...")
    test_component = HybridTableViewApp()
    
    window = app.create_window(
        title="Hybrid TableView Test",
        size=(350, 300),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    
    print("🎬 Starting application...")
    print("Instructions:")
    print("- Window should show with basic controls")
    print("- Click 'Click Me' to test basic functionality")
    print("- Click 'Toggle Table' to show/hide TableView")
    print("- Observe when/if window disappears")
    print("- Press Ctrl+C to exit")
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ Hybrid test ended")

if __name__ == "__main__":
    main()