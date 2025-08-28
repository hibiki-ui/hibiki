#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 02: Reactive Basics
响应式系统基础 - Signal 和 Computed

学习目标：
✅ 理解Signal响应式状态
✅ 使用Computed计算属性
✅ 创建交互式按钮
✅ 观察状态变化如何自动更新UI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import hibiki
from hibiki import (
    Signal, Computed, Effect,
    Label, Button, Container,
    ManagerFactory, ComponentStyle, px
)

def main():
    """响应式系统基础演示"""
    print("🚀 Starting Reactive Basics Example...")
    
    # 1. 创建响应式状态
    count = Signal(0)
    
    # 2. 创建计算属性
    doubled = Computed(lambda: count.value * 2)
    message = Computed(lambda: f"Count: {count.value}, Doubled: {doubled.value}")
    
    # 3. 创建副作用（可选 - 用于调试）
    Effect(lambda: print(f"📊 Count changed to: {count.value}"))
    
    # 4. 创建UI组件
    # 显示标签 - 会自动更新当count改变时
    display_label = Label(
        message,  # 使用Computed作为文本内容
        style=ComponentStyle(
            margin_bottom=px(20)
        ),
        # 文本属性
        font_size=18,
        text_align="center",
        color="#333"
    )
    
    # 增加按钮
    increment_btn = Button(
        "Increment (+1)",
        style=ComponentStyle(
            width=px(150),
            height=px(35),
            margin_right=px(10)
        ),
        on_click=lambda: setattr(count, 'value', count.value + 1)
    )
    
    # 减少按钮
    decrement_btn = Button(
        "Decrement (-1)",
        style=ComponentStyle(
            width=px(150),
            height=px(35)
        ),
        on_click=lambda: setattr(count, 'value', max(0, count.value - 1))
    )
    
    # 重置按钮
    reset_btn = Button(
        "Reset",
        style=ComponentStyle(
            width=px(100),
            height=px(35),
            margin_top=px(10)
        ),
        on_click=lambda: setattr(count, 'value', 0)
    )
    
    # 按钮容器
    button_row = Container(
        children=[increment_btn, decrement_btn],
        style=ComponentStyle(
            display="flex",
            flex_direction="row",
            justify_content="center",
            margin_bottom=px(10)
        )
    )
    
    # 主容器
    main_container = Container(
        children=[
            Label(
                "🔄 Reactive State Demo",
                style=ComponentStyle(
                    margin_bottom=px(30)
                ),
                # 文本属性
                font_size=24,
                font_weight="bold",
                text_align="center",
                color="#2c3e50"
            ),
            display_label,
            button_row,
            Container(
                children=[reset_btn],
                style=ComponentStyle(
                    display="flex",
                    justify_content="center"
                )
            )
        ],
        style=ComponentStyle(
            padding=px(40),
            display="flex",
            flex_direction="column",
            align_items="center"
        )
    )
    
    # 5. 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Reactive Basics - Hibiki UI",
        width=500,
        height=350
    )
    
    window.set_content(main_container)
    
    print("✅ Reactive Basics app ready!")
    print("🎯 Try clicking buttons to see reactive updates!")
    print("📚 Next: Try 03_forms_and_inputs.py to learn about form controls")
    
    app_manager.run()

if __name__ == "__main__":
    main()