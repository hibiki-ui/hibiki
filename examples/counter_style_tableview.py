#!/usr/bin/env python3
"""
模仿 counter.py 结构的 TableView 测试
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Computed, Effect, Component, set_log_level
from macui.components import VStack, HStack, Label, Button, TableView
from macui.app import MacUIApp

set_log_level("INFO")

class TableViewApp(Component):
    """TableView 应用组件 - 模仿 Counter 结构"""
    
    def __init__(self):
        super().__init__()
        
        # 创建响应式状态 - 完全按照 Counter 的方式
        self.data = self.create_signal([
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
        self.message = self.create_signal("Ready")
        
        # 创建计算属性
        self.status_text = self.create_computed(
            lambda: f"Status: {self.message.value}"
        )
        self.selection_text = self.create_computed(
            lambda: f"Selected Row: {self.selected_row.value}"
        )
    
    def on_select(self, row):
        """选择行回调"""
        if row >= 0 and row < len(self.data.value):
            item = self.data.value[row]
            self.message.value = f"Selected: {item['name']}"
            print(f"Row selected: {row} - {item['name']}")
        else:
            self.message.value = "No selection"
            print(f"Row deselected: {row}")
    
    def add_item(self):
        """添加项目"""
        current_data = list(self.data.value)
        new_item = {"name": f"Item{len(current_data)+1}", "value": chr(65 + len(current_data))}
        current_data.append(new_item)
        self.data.value = current_data
        self.message.value = f"Added {new_item['name']}"
        print(f"Added item: {new_item}")
    
    def clear_data(self):
        """清空数据"""
        self.data.value = []
        self.selected_row.value = -1
        self.message.value = "Data cleared"
        print("Data cleared")
    
    def reset_data(self):
        """重置数据"""
        self.data.value = [
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
        ]
        self.selected_row.value = -1
        self.message.value = "Data reset"
        print("Data reset")
    
    def mount(self):
        """构建组件的视图结构 - 完全按照 Counter 的方式"""
        return VStack(spacing=20, padding=40, children=[
            # 标题
            Label("macUI v2 TableView Demo", frame=(0, 0, 300, 30)),
            
            # 显示区域
            VStack(spacing=10, children=[
                Label(self.status_text),
                Label(self.selection_text),
            ]),
            
            # TableView 区域
            TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 120},
                    {"title": "Value", "key": "value", "width": 60},
                ],
                data=self.data,
                selected_row=self.selected_row,
                on_select=self.on_select,
                frame=(0, 0, 200, 120)
            ),
            
            # 按钮区域 - 完全按照 Counter 的方式
            HStack(spacing=15, children=[
                Button(
                    "Add Item", 
                    on_click=self.add_item,
                    tooltip="Add a new item"
                ),
                Button(
                    "Clear All", 
                    on_click=self.clear_data,
                    tooltip="Clear all data"
                ),
                Button(
                    "Reset", 
                    on_click=self.reset_data,
                    tooltip="Reset to default data"
                )
            ]),
            
            # 信息区域 - 完全按照 Counter 的方式
            VStack(spacing=5, children=[
                Label("This demo showcases:"),
                Label("• TableView with reactive data"),
                Label("• Row selection events"),
                Label("• Dynamic data updates"),
                Label("• CRUD operations"),
            ])
        ])

def run_tableview_demo():
    """运行 TableView 演示 - 完全按照 Counter 的方式"""
    print("Starting TableView demo...")
    
    # 创建应用程序 - 完全按照 Counter 的方式
    app = MacUIApp("TableView Demo")
    
    # 创建窗口 - 完全按照 Counter 的方式
    window = app.create_window(
        title="macUI v2 - TableView Demo",
        size=(400, 500),
        resizable=True,
        content=TableViewApp()
    )
    
    # 显示窗口
    window.show()
    
    # 运行应用
    app.run()

def test_reactive_system():
    """测试响应式系统 - 完全按照 Counter 的方式"""
    print("\n=== Testing Reactive System ===")
    
    # 测试 Signal
    print("Testing Signal:")
    data = Signal([{"name": "Test", "value": "X"}])
    print(f"Initial value: {data.value}")
    
    data.value = [{"name": "Test1", "value": "Y"}, {"name": "Test2", "value": "Z"}]
    print(f"After setting new data: {len(data.value)} items")
    
    # 测试 Computed
    print("\nTesting Computed:")
    count_computed = Computed(lambda: len(data.value))
    print(f"Computed count: {count_computed.value}")
    
    # 测试 Effect
    print("\nTesting Effect:")
    effect_calls = []
    
    def log_effect():
        effect_calls.append(len(data.value))
        print(f"Effect called with data length: {len(data.value)}")
    
    effect = Effect(log_effect)
    data.value = [{"name": "Test3", "value": "W"}]
    
    print(f"Effect was called {len(effect_calls)} times with values: {effect_calls}")
    
    effect.cleanup()
    print("Effect cleaned up")

if __name__ == "__main__":
    print("macUI v2 TableView Example")
    print("==========================")
    
    # 首先测试响应式系统 - 完全按照 Counter 的方式
    test_reactive_system()
    
    # 然后选择运行哪个示例 - 完全按照 Counter 的方式
    print("\nAvailable demos:")
    print("1. TableView Demo (default)")
    print("2. Exit")
    
    try:
        choice = input("\nSelect demo (1-2): ").strip()
        
        if choice == "2":
            print("Goodbye!")
        else:
            run_tableview_demo()
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()