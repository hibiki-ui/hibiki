#!/usr/bin/env python3
"""
TableView 正确使用方法示例
基于 TABLEVIEW_SOLUTION_REPORT.md 的指导
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import MacUIApp, Signal, Component
from macui.components import TableView, Label
from Foundation import NSMakeRect
from AppKit import NSView

class TableViewCorrectUsageApp(Component):
    """展示 TableView 正确使用方法的应用"""
    
    def __init__(self):
        super().__init__()
        
        # 表格数据
        self.table_data = self.create_signal([
            {"name": "张三", "age": 28, "city": "北京", "salary": 8000},
            {"name": "李四", "age": 32, "city": "上海", "salary": 12000},
            {"name": "王五", "age": 25, "city": "广州", "salary": 7500},
            {"name": "赵六", "age": 35, "city": "深圳", "salary": 15000},
        ])
        
        # 选中行
        self.selected_row = self.create_signal(-1)
        
        # 状态消息
        self.message = self.create_signal("TableView 正确使用方法演示")
    
    def on_table_select(self, row):
        """处理表格行选择"""
        if 0 <= row < len(self.table_data.value):
            person = self.table_data.value[row]
            self.message.value = f"选择了: {person['name']} - {person['city']}"
        else:
            self.message.value = "没有选择任何行"
    
    def mount(self):
        """正确的 TableView 使用方法"""
        
        # ✅ 正确方法1: 创建简单的 NSView 容器
        container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 600, 400))
        
        # ✅ 使用传统的 autoresizing，不使用约束系统
        container.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # 创建标题标签
        title_label = Label("TableView 正确使用方法")
        title_label.setFrame_(NSMakeRect(20, 350, 560, 30))
        
        # 创建消息标签
        message_label = Label(self.message)
        message_label.setFrame_(NSMakeRect(20, 320, 560, 25))
        
        # ✅ 正确方法2: 直接创建 TableView，不放入 VStack/HStack
        table_view = TableView(
            columns=[
                {"title": "姓名", "key": "name", "width": 100},
                {"title": "年龄", "key": "age", "width": 60},
                {"title": "城市", "key": "city", "width": 100},
                {"title": "薪资", "key": "salary", "width": 120},
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_table_select,
            frame=(20, 50, 560, 250)  # 直接指定位置和大小
        )
        
        # ✅ 正确方法3: 手动添加到容器，使用 frame-based 布局
        container.addSubview_(title_label)
        container.addSubview_(message_label)
        container.addSubview_(table_view)
        
        return container

def main():
    """主函数"""
    print("=== TableView 正确使用方法示例 ===")
    print()
    print("✅ 本示例展示如何正确使用 TableView：")
    print("   1. 使用简单的 NSView 容器，而不是 VStack/HStack")
    print("   2. 直接创建 TableView，不放入堆栈布局")
    print("   3. 使用 frame-based 布局和 addSubview_ 手动添加")
    print("   4. 避免约束系统冲突")
    print()
    print("❌ 错误的做法会导致 NSLayoutConstraintNumberExceedsLimit 错误：")
    print("   - VStack(children=[TableView(...)])  # 绝对不要这样做")
    print("   - HStack(children=[TableView(...)])  # 也不要这样做")
    print()
    print("📖 技术详情请参考: TABLEVIEW_SOLUTION_REPORT.md")
    
    # 创建应用
    app = MacUIApp("TableView Correct Usage")
    
    # 创建窗口
    window = app.create_window(
        title="TableView 正确使用方法示例",
        size=(640, 450),
        content=TableViewCorrectUsageApp()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 应用已启动，TableView 应该正常显示而不会出现约束错误")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 应用被用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()