#!/usr/bin/env python3
"""
简单 TableView 测试 - 直接测试不需要交互
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import TableView, VStack, HStack, Button, Label
from macui.app import MacUIApp

set_log_level("INFO")

def main():
    print("🧪 开始简单 TableView 测试...")
    
    app = MacUIApp("简单 TableView 测试")
    
    # 创建数据
    data = Signal([
        {"name": "张三", "age": "28", "city": "北京"},
        {"name": "李四", "age": "32", "city": "上海"},
        {"name": "王五", "age": "25", "city": "广州"},
    ])
    
    selected_row = Signal(-1)
    message = Signal("TableView 测试开始")
    
    def on_select(row):
        print(f"📊 选择了行: {row}")
        if 0 <= row < len(data.value):
            person = data.value[row]
            message.value = f"选中: {person['name']} ({person['age']}岁, {person['city']})"
        else:
            message.value = f"取消选择 (行 {row})"
    
    def on_double_click(row):
        print(f"📊 双击了行: {row}")
        if 0 <= row < len(data.value):
            person = data.value[row]
            message.value = f"双击: {person['name']} - {person['city']}"
    
    def add_row():
        new_data = list(data.value)
        new_data.append({"name": "新用户", "age": "30", "city": "深圳"})
        data.value = new_data
        message.value = f"添加了新行，共 {len(new_data)} 行"
        print(f"📊 添加了新行，总计 {len(new_data)} 行")
    
    from macui import Component
    
    class SimpleTableViewComponent(Component):
        def __init__(self):
            super().__init__()
            # 创建计算属性来避免 lambda 问题
            self.selected_text = self.create_computed(lambda: f"选中行: {selected_row.value}")
            self.count_text = self.create_computed(lambda: f"数据行数: {len(data.value)}")
        
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("简单 TableView 测试"),
                Label(message),
                
                # 控制按钮
                HStack(spacing=10, children=[
                    Button("添加行", on_click=add_row),
                ]),
                
                # TableView
                TableView(
                    columns=[
                        {"title": "姓名", "key": "name", "width": 120},
                        {"title": "年龄", "key": "age", "width": 60},
                        {"title": "城市", "key": "city", "width": 100},
                    ],
                    data=data,
                    selected_row=selected_row,
                    on_select=on_select,
                    on_double_click=on_double_click,
                    frame=(0, 0, 350, 200)
                ),
                
                # 状态显示 - 使用计算属性
                Label(self.selected_text),
                Label(self.count_text),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="简单 TableView 测试",
        size=(400, 400),
        content=SimpleTableViewComponent()
    )
    
    # 显示窗口
    window.show()
    print("✅ 窗口已显示，正在运行...")
    print("📋 测试说明:")
    print("   - 应该看到一个包含表格的窗口")
    print("   - 可以点击行来选择")
    print("   - 可以双击行来触发事件") 
    print("   - 可以点击'添加行'按钮")
    print("   - 按 Ctrl+C 退出")
    print()
    
    # 运行应用
    try:
        app.run()
        print("应用正常结束")
    except Exception as e:
        print(f"应用运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()