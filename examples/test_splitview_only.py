#!/usr/bin/env python3
"""
单独测试 SplitView 组件
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import SplitView, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class SplitViewTestApp:
    """纯 SplitView 测试应用"""
    
    def __init__(self):
        self.message = Signal("SplitView 单独测试")
        self.left_counter = Signal(0)
        self.right_counter = Signal(0)
    
    def on_split_resize(self, frames):
        self.message.value = f"分割视图调整: {len(frames)}个子视图"
    
    def left_button_click(self):
        self.left_counter.value += 1
        self.message.value = f"左侧按钮点击: {self.left_counter.value}"
    
    def right_button_click(self):
        self.right_counter.value += 1
        self.message.value = f"右侧按钮点击: {self.right_counter.value}"
    
    def reset_counters(self):
        self.left_counter.value = 0
        self.right_counter.value = 0
        self.message.value = "计数器已重置"

def main():
    print("=== SplitView 单独测试 ===")
    
    app = MacUIApp("SplitView Only Test")
    test_app = SplitViewTestApp()
    
    from macui import Component
    
    class SplitViewOnlyComponent(Component):
        def mount(self):
            # 左侧面板内容
            left_panel = VStack(padding=15, children=[
                Label("左侧面板"),
                Label(lambda: f"左侧计数: {test_app.left_counter.value}"),
                Button("左侧按钮", on_click=test_app.left_button_click),
                Label("• 功能列表"),
                Label("• 导航菜单"),
                Label("• 设置选项"),
            ])
            
            # 右侧面板内容
            right_panel = VStack(padding=15, children=[
                Label("右侧面板"),
                Label(lambda: f"右侧计数: {test_app.right_counter.value}"),
                Button("右侧按钮", on_click=test_app.right_button_click),
                Label("• 主要内容"),
                Label("• 详细信息"),
                Label("• 操作区域"),
            ])
            
            return VStack(spacing=15, padding=20, children=[
                Label("SplitView 单独测试", frame=(0, 0, 400, 30)),
                Label(test_app.message),
                
                # 控制按钮
                HStack(spacing=10, children=[
                    Button("重置计数器", on_click=test_app.reset_counters),
                ]),
                
                # SplitView - 这是重点测试对象
                SplitView(
                    orientation="horizontal",
                    children=[left_panel, right_panel],
                    divider_style="thin",
                    on_resize=test_app.on_split_resize,
                    frame=(0, 0, 450, 250)
                ),
                
                # 状态显示
                VStack(spacing=3, children=[
                    Label(lambda: f"左侧计数: {test_app.left_counter.value}"),
                    Label(lambda: f"右侧计数: {test_app.right_counter.value}"),
                ]),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="SplitView Only Test",
        size=(500, 400),
        content=SplitViewOnlyComponent()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ SplitView 测试窗口已显示")
    print("📝 测试功能:")
    print("   - SplitView 水平分割")
    print("   - 子视图内容显示")
    print("   - 分割调整事件")
    print("   - 交互按钮测试")
    
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