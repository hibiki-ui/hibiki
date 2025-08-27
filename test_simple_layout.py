#!/usr/bin/env python3
"""简单测试 - 找出NSLayoutConstraint警告的源头"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.signal import Signal
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack
from macui.components.modern_controls import ModernLabel, ModernButton

class SimpleTest(Component):
    def __init__(self):
        super().__init__()
    
    def mount(self):
        # 测试只有基础组件
        simple_layout = ModernVStack(
            children=[
                ModernLabel("Test Label", width=200, height=30),
                ModernButton("Test Button", width=150, height=32)
            ],
            width=300,
            height=100
        )
        return simple_layout.get_view()

if __name__ == "__main__":
    print("🔍 简单布局测试 - 寻找NSLayoutConstraint警告源头")
    
    app = MacUIApp("Simple Layout Test")
    test = SimpleTest()
    
    app.create_window(
        title="Simple Test",
        size=(400, 200),
        content=test
    )
    
    print("✅ 窗口创建完成，开始事件循环...")
    app.run()