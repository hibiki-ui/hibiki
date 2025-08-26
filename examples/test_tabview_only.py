#!/usr/bin/env python3
"""
单独测试 TabView 组件
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import TabView, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class TabViewTestApp:
    """纯 TabView 测试应用"""
    
    def __init__(self):
        self.current_tab = Signal(0)
        self.message = Signal("TabView 单独测试")
        self.counter = Signal(0)
    
    def on_tab_change(self, index, tab_item):
        tab_titles = ["第一页", "第二页", "第三页", "第四页"]
        self.message.value = f"切换到标签页 {index}: {tab_titles[index] if index < len(tab_titles) else f'标签{index}'}"
    
    def increment_counter(self):
        self.counter.value += 1
        self.message.value = f"计数器: {self.counter.value}"
    
    def reset_counter(self):
        self.counter.value = 0
        self.message.value = "计数器已重置"

def main():
    print("=== TabView 单独测试 ===")
    
    app = MacUIApp("TabView Only Test")
    test_app = TabViewTestApp()
    
    from macui import Component
    
    class TabViewOnlyComponent(Component):
        def mount(self):
            # 创建标签页内容
            tab1_content = VStack(spacing=10, padding=20, children=[
                Label("这是第一个标签页"),
                Label(lambda: f"计数器值: {test_app.counter.value}"),
                Button("增加计数器", on_click=test_app.increment_counter),
                Button("重置计数器", on_click=test_app.reset_counter),
            ])
            
            tab2_content = VStack(spacing=10, padding=20, children=[
                Label("这是第二个标签页"),
                Label("一些静态内容"),
                Label("• 项目1"),
                Label("• 项目2"),
                Label("• 项目3"),
            ])
            
            tab3_content = VStack(spacing=10, padding=20, children=[
                Label("这是第三个标签页"),
                HStack(spacing=10, children=[
                    Button("按钮A", on_click=lambda: test_app.message.set("点击了按钮A")),
                    Button("按钮B", on_click=lambda: test_app.message.set("点击了按钮B")),
                    Button("按钮C", on_click=lambda: test_app.message.set("点击了按钮C")),
                ]),
            ])
            
            tab4_content = VStack(spacing=10, padding=20, children=[
                Label("这是第四个标签页"),
                Label("动态信息显示:"),
                Label(test_app.message),
            ])
            
            return VStack(spacing=15, padding=20, children=[
                Label("TabView 单独测试", frame=(0, 0, 400, 30)),
                Label(test_app.message),
                
                # TabView - 这是重点测试对象
                TabView(
                    tabs=[
                        {"title": "第一页", "content": tab1_content},
                        {"title": "第二页", "content": tab2_content},
                        {"title": "第三页", "content": tab3_content},
                        {"title": "第四页", "content": tab4_content},
                    ],
                    selected=test_app.current_tab,
                    on_change=test_app.on_tab_change,
                    frame=(0, 0, 450, 300)
                ),
                
                # 状态显示
                VStack(spacing=3, children=[
                    Label(lambda: f"当前标签页: {test_app.current_tab.value}"),
                    Label(lambda: f"计数器: {test_app.counter.value}"),
                ]),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="TabView Only Test",
        size=(500, 450),
        content=TabViewOnlyComponent()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ TabView 测试窗口已显示")
    print("📝 测试功能:")
    print("   - TabView 标签页切换")
    print("   - 标签页内容显示")
    print("   - 事件处理")
    print("   - 动态内容更新")
    
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