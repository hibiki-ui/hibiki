#!/usr/bin/env python3
"""
测试第二阶段剩余组件：ComboBox, Menu, ContextMenu, DatePicker, TimePicker
"""

import sys
import os
from datetime import datetime

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import ComboBox, Menu, ContextMenu, DatePicker, TimePicker, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class Stage2RemainingTestApp:
    """第二阶段剩余组件测试应用"""
    
    def __init__(self):
        # ComboBox 状态
        self.search_text = Signal("")
        self.category_text = Signal("技术")
        
        # DatePicker 和 TimePicker 状态
        from Foundation import NSDate
        self.selected_date = Signal(NSDate.date())
        self.selected_time = Signal(NSDate.date())
        
        # 消息显示
        self.message = Signal("第二阶段剩余组件测试准备就绪")
        
        # 选项数据
        self.search_suggestions = ["Python", "macOS", "PyObjC", "AppKit", "Swift", "Objective-C"]
        self.categories = ["技术", "生活", "工作", "学习", "娱乐", "其他"]
        
    def on_search_change(self, text):
        self.message.value = f"搜索文本变更: '{text}'"
        
    def on_search_select(self, index, text):
        self.message.value = f"搜索选择: 索引{index}, 文本'{text}'"
        
    def on_category_change(self, text):
        self.message.value = f"分类变更: '{text}'"
        
    def on_category_select(self, index, text):
        self.message.value = f"分类选择: 索引{index}, 文本'{text}'"
        
    def on_date_change(self, date):
        self.message.value = f"日期变更: {date}"
        
    def on_time_change(self, time):
        self.message.value = f"时间变更: {time}"
        
    def create_main_menu(self):
        """创建主菜单"""
        return Menu("主菜单", [
            {"title": "新建文档", "action": lambda item_id: self.menu_action(item_id)},
            {"title": "打开文件", "action": lambda item_id: self.menu_action(item_id)},
            {"separator": True},
            {"title": "保存", "action": lambda item_id: self.menu_action(item_id), "id": "save"},
            {"title": "另存为...", "action": lambda item_id: self.menu_action(item_id)},
            {"separator": True},
            {"title": "退出", "action": lambda item_id: self.menu_action(item_id)},
        ])
    
    def create_context_menu(self):
        """创建右键菜单"""
        return ContextMenu([
            {"title": "复制", "action": lambda item_id: self.context_action(item_id)},
            {"title": "粘贴", "action": lambda item_id: self.context_action(item_id)},
            {"separator": True},
            {"title": "删除", "action": lambda item_id: self.context_action(item_id)},
            {"title": "重命名", "action": lambda item_id: self.context_action(item_id)},
        ])
    
    def menu_action(self, item_id):
        self.message.value = f"菜单操作: {item_id}"
        
    def context_action(self, item_id):
        self.message.value = f"右键菜单操作: {item_id}"
        
    def clear_search(self):
        self.search_text.value = ""
        self.message.value = "搜索框已清空"
        
    def reset_category(self):
        self.category_text.value = "技术"
        self.message.value = "分类已重置"
        
    def show_current_datetime(self):
        from Foundation import NSDate
        current = NSDate.date()
        self.selected_date.value = current
        self.selected_time.value = current
        self.message.value = f"已设置为当前日期时间: {current}"

def main():
    print("=== 第二阶段剩余组件测试 ===")
    
    app = MacUIApp("Stage 2 Remaining Components Test")
    test_app = Stage2RemainingTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class Stage2RemainingComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("第二阶段剩余组件测试", frame=(0, 0, 600, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # ComboBox 测试区域
                    Label("1. 组合框 (ComboBox):"),
                    
                    # 搜索组合框
                    VStack(spacing=8, children=[
                        Label("搜索建议 (可编辑):"),
                        ComboBox(
                            items=test_app.search_suggestions,
                            text=test_app.search_text,
                            editable=True,
                            on_change=test_app.on_search_change,
                            on_select=test_app.on_search_select,
                            tooltip="输入或选择搜索关键词",
                            frame=(0, 0, 200, 25)
                        ),
                    ]),
                    
                    # 分类组合框
                    VStack(spacing=8, children=[
                        Label("分类选择 (只读):"),
                        ComboBox(
                            items=test_app.categories,
                            text=test_app.category_text,
                            editable=False,
                            on_change=test_app.on_category_change,
                            on_select=test_app.on_category_select,
                            tooltip="选择分类",
                            frame=(0, 0, 150, 25)
                        ),
                    ]),
                    
                    # DatePicker 和 TimePicker 测试区域
                    Label("2. 日期时间选择器:"),
                    
                    # 日期选择器
                    VStack(spacing=8, children=[
                        Label("日期选择器 (Stepper 样式):"),
                        DatePicker(
                            date=test_app.selected_date,
                            style="stepper",
                            date_only=True,
                            on_change=test_app.on_date_change,
                            tooltip="选择日期",
                            frame=(0, 0, 200, 25)
                        ),
                    ]),
                    
                    # 时间选择器
                    VStack(spacing=8, children=[
                        Label("时间选择器:"),
                        TimePicker(
                            time=test_app.selected_time,
                            style="stepper",
                            on_change=test_app.on_time_change,
                            tooltip="选择时间",
                            frame=(0, 0, 150, 25)
                        ),
                    ]),
                    
                    # 控制按钮
                    HStack(spacing=15, children=[
                        Button("清空搜索", on_click=test_app.clear_search),
                        Button("重置分类", on_click=test_app.reset_category),
                        Button("当前日期时间", on_click=test_app.show_current_datetime),
                    ]),
                    
                    # 实时显示当前状态
                    VStack(spacing=5, children=[
                        Label("当前状态:"),
                        Label(lambda: f"搜索: '{test_app.search_text.value}'"),
                        Label(lambda: f"分类: '{test_app.category_text.value}'"),
                        Label(lambda: f"日期: {test_app.selected_date.value}"),
                        Label(lambda: f"时间: {test_app.selected_time.value}"),
                    ]),
                    
                    # 说明文字
                    VStack(spacing=3, children=[
                        Label("📝 组件说明:"),
                        Label("• ComboBox: 可编辑的下拉选择框"),
                        Label("• Menu/ContextMenu: 菜单系统 (需要在窗口菜单栏查看)"),
                        Label("• DatePicker: 日期选择器，支持多种样式"),
                        Label("• TimePicker: 时间选择器，基于DatePicker"),
                    ]),
                ])
        
        return Stage2RemainingComponent()
    
    # 创建窗口
    window = app.create_window(
        title="Stage 2 Remaining Components Test",
        size=(650, 700),
        content=create_content()
    )
    
    # 设置菜单（演示主菜单功能）
    main_menu = test_app.create_main_menu()
    # 注意：实际设置应用菜单需要额外的代码，这里只是创建了菜单对象
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - ComboBox: 组合框")
    print("     * 搜索建议框 (可编辑)")
    print("     * 分类选择框 (只读)")
    print("   - DatePicker: 日期选择器")
    print("     * Stepper 样式，只显示日期")
    print("   - TimePicker: 时间选择器") 
    print("     * 基于DatePicker，只显示时间")
    print("   - Menu/ContextMenu: 菜单系统")
    print("     * 主菜单和右键菜单功能")
    print("   - 双向数据绑定")
    print("   - 实时状态更新")
    print("   - 完整事件处理")
    
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