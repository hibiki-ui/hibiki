#!/usr/bin/env python3
"""
始终存在的 TableView 测试 - TableView 总是在组件树中，但可以控制可见性
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

class AlwaysPresentTableViewApp(Component):
    """始终包含 TableView 的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化始终存在TableView测试组件...")
        
        # 基础状态
        self.message = self.create_signal("Ready")
        self.counter = self.create_signal(0)
        
        # TableView 数据和状态
        self.table_data = self.create_signal([
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
            {"name": "Item3", "value": "C"},
        ])
        
        self.selected_row = self.create_signal(-1)
        
        # 计算属性
        self.status_text = self.create_computed(
            lambda: f"Status: {self.message.value}"
        )
        self.counter_text = self.create_computed(
            lambda: f"Count: {self.counter.value}"
        )
        self.selection_text = self.create_computed(
            lambda: f"Selected Row: {self.selected_row.value}"
        )
    
    def increment(self):
        """增加计数"""
        self.counter.value += 1
        self.message.value = f"Clicked {self.counter.value} times"
        print(f"✅ Button clicked: {self.counter.value}")
    
    def add_item(self):
        """添加表格项目"""
        current_data = list(self.table_data.value)
        new_item = {
            "name": f"Item{len(current_data)+1}", 
            "value": chr(65 + len(current_data))
        }
        current_data.append(new_item)
        self.table_data.value = current_data
        self.message.value = f"Added {new_item['name']}"
        print(f"📊 Added item: {new_item}")
    
    def on_row_select(self, row):
        """TableView 行选择回调"""
        print(f"📊 TableView row selected: {row}")
        if 0 <= row < len(self.table_data.value):
            item = self.table_data.value[row]
            self.message.value = f"Selected: {item['name']}"
        else:
            self.message.value = "No selection"
    
    def mount(self):
        """构建组件视图 - TableView 始终存在"""
        print("🏗️ Building always-present TableView view...")
        
        return VStack(spacing=15, padding=20, children=[
            # 标题和状态
            Label("Always-Present TableView Test"),
            Label(self.status_text),
            Label(self.counter_text),
            Label(self.selection_text),
            
            # 控制按钮
            Button("Click Me", on_click=self.increment),
            Button("Add Item", on_click=self.add_item),
            
            # TableView - 始终存在
            TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 100},
                    {"title": "Value", "key": "value", "width": 60},
                ],
                data=self.table_data,
                selected_row=self.selected_row,
                on_select=self.on_row_select,
                frame=(0, 0, 180, 120)
            ),
        ])

def main():
    """主函数"""
    print("🚀 Always-Present TableView Test Starting...")
    
    # 创建应用
    app = MacUIApp("Always-Present TableView Test")
    
    print("📱 Creating component and window...")
    test_component = AlwaysPresentTableViewApp()
    
    window = app.create_window(
        title="Always-Present TableView Test",
        size=(350, 400),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    
    print("🎬 Starting application...")
    print("Instructions:")
    print("- Window should show with TableView always visible")
    print("- Click 'Click Me' to test basic functionality")
    print("- Click 'Add Item' to test table updates")
    print("- Click table rows to test selection")
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
        print("✅ Always-present test ended")

if __name__ == "__main__":
    main()