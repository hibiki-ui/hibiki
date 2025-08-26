#!/usr/bin/env python3
"""
单独测试 TableView 组件 - 缩小崩溃排查范围
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import TableView, VStack, HStack, Button, Label, TextField
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class TableViewTestApp:
    """纯 TableView 测试应用"""
    
    def __init__(self):
        # 表格数据
        self.table_data = Signal([
            {"name": "张三", "age": "28", "city": "北京"},
            {"name": "李四", "age": "32", "city": "上海"},
            {"name": "王五", "age": "25", "city": "广州"},
        ])
        
        # 选中行
        self.selected_row = Signal(-1)
        
        # 消息
        self.message = Signal("TableView 单独测试")
        
        # 新行数据
        self.new_name = Signal("")
        self.new_age = Signal("")
        self.new_city = Signal("")
    
    def on_table_select(self, row):
        if row >= 0 and row < len(self.table_data.value):
            person = self.table_data.value[row]
            self.message.value = f"选择了行 {row}: {person['name']}"
        else:
            self.message.value = f"取消选择 (行 {row})"
    
    def on_table_double_click(self, row):
        if row >= 0 and row < len(self.table_data.value):
            person = self.table_data.value[row]
            self.message.value = f"双击行 {row}: {person['name']} ({person['age']}岁)"
    
    def add_table_row(self):
        if self.new_name.value.strip() and self.new_age.value.strip() and self.new_city.value.strip():
            new_data = list(self.table_data.value)
            new_data.append({
                "name": self.new_name.value.strip(),
                "age": self.new_age.value.strip(),
                "city": self.new_city.value.strip()
            })
            self.table_data.value = new_data
            
            # 清空输入框
            self.new_name.value = ""
            self.new_age.value = ""
            self.new_city.value = ""
            
            self.message.value = f"添加了新行，当前共 {len(new_data)} 行"
    
    def remove_selected_row(self):
        if self.selected_row.value >= 0 and self.selected_row.value < len(self.table_data.value):
            new_data = list(self.table_data.value)
            removed = new_data.pop(self.selected_row.value)
            self.table_data.value = new_data
            self.selected_row.value = -1
            self.message.value = f"删除了 {removed['name']}，剩余 {len(new_data)} 行"
        else:
            self.message.value = "没有选中行可删除"
    
    def clear_table(self):
        self.table_data.value = []
        self.selected_row.value = -1
        self.message.value = "表格已清空"
    
    def reset_table(self):
        self.table_data.value = [
            {"name": "张三", "age": "28", "city": "北京"},
            {"name": "李四", "age": "32", "city": "上海"},
            {"name": "王五", "age": "25", "city": "广州"},
        ]
        self.selected_row.value = -1
        self.message.value = "表格已重置"

def main():
    print("=== TableView 单独测试 ===")
    
    app = MacUIApp("TableView Only Test")
    test_app = TableViewTestApp()
    
    from macui import Component
    
    class TableViewOnlyComponent(Component):
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("TableView 单独测试", frame=(0, 0, 400, 30)),
                Label(test_app.message),
                
                # 添加数据区域
                HStack(spacing=10, children=[
                    VStack(spacing=5, children=[
                        Label("添加新行:"),
                        HStack(spacing=5, children=[
                            TextField(placeholder="姓名", value=test_app.new_name, frame=(0, 0, 80, 25)),
                            TextField(placeholder="年龄", value=test_app.new_age, frame=(0, 0, 50, 25)),
                            TextField(placeholder="城市", value=test_app.new_city, frame=(0, 0, 80, 25)),
                        ]),
                        HStack(spacing=5, children=[
                            Button("添加", on_click=test_app.add_table_row),
                            Button("删除选中", on_click=test_app.remove_selected_row),
                            Button("清空", on_click=test_app.clear_table),
                            Button("重置", on_click=test_app.reset_table),
                        ]),
                    ]),
                ]),
                
                # TableView - 这是重点测试对象
                TableView(
                    columns=[
                        {"title": "姓名", "key": "name", "width": 100},
                        {"title": "年龄", "key": "age", "width": 60},
                        {"title": "城市", "key": "city", "width": 100},
                    ],
                    data=test_app.table_data,
                    selected_row=test_app.selected_row,
                    on_select=test_app.on_table_select,
                    on_double_click=test_app.on_table_double_click,
                    frame=(0, 0, 350, 200)
                ),
                
                # 状态显示
                VStack(spacing=3, children=[
                    Label(lambda: f"选中行: {test_app.selected_row.value}"),
                    Label(lambda: f"数据行数: {len(test_app.table_data.value)}"),
                ]),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="TableView Only Test",
        size=(450, 500),
        content=TableViewOnlyComponent()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ TableView 测试窗口已显示")
    print("📝 测试功能:")
    print("   - TableView 数据显示")
    print("   - 行选择和双击")
    print("   - 动态数据更新")
    print("   - CRUD 操作")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()