#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 01: Hello World + 新特性展示
展示重构后的Label和TextField组件新功能

学习目标：
✅ 理解基本的应用程序结构
✅ 体验Label组件新特性（边框、背景、可选择文本）
✅ 体验TextField组件新特性（样式定制、占位符）
✅ 使用Container布局多个组件
"""

from hibiki.ui import (
    Label, TextField, Container, ManagerFactory, 
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems,
    px, percent
)
from hibiki.ui.components.text_field_config import BezelStyle


def main():
    """创建展示新特性的Hello World应用"""
    print("🚀 Starting Enhanced Hello World Example...")

    # 1. 获取应用管理器
    app_manager = ManagerFactory.get_app_manager()

    # 2. 创建窗口 - 调整大小以容纳更多内容
    window = app_manager.create_window(title="Hibiki UI v4.0 - 新特性展示", width=600, height=700)

    # 3. 创建多个Label组件展示新特性
    
    # 3.1 标题Label - 经典样式
    title_label = Label(
        "🎉 Hibiki UI v4.0 新特性展示",
        style=ComponentStyle(
            width=percent(100),
            height=px(50),
            padding=px(10)
        ),
        font_size=20,
        font_weight="bold",
        text_align="center",
        color="#2c3e50"
    )
    
    # 3.2 可选择文本的Label
    selectable_label = Label(
        "📝 这个文本可以被选择和复制！试试看吧~",
        selectable=True,  # 🆕 新特性：可选择文本
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        ),
        font_size=14,
        color="#27ae60",
        text_align="center"
    )
    
    # 3.3 带圆角边框的Label
    bordered_round_label = Label(
        "🔘 圆角边框样式",
        bordered=True,  # 🆕 新特性：边框
        bezel_style=BezelStyle.ROUNDED,  # 🆕 新特性：圆角样式
        style=ComponentStyle(
            width=px(200),
            height=px(35),
            margin=px(5)
        ),
        font_size=13,
        text_align="center",
        color="#8e44ad"
    )
    
    # 3.4 带方角边框的Label
    bordered_square_label = Label(
        "⬜ 方角边框样式",
        bordered=True,  # 🆕 新特性：边框
        bezel_style=BezelStyle.SQUARE,  # 🆕 新特性：方角样式
        style=ComponentStyle(
            width=px(200),
            height=px(35),
            margin=px(5)
        ),
        font_size=13,
        text_align="center",
        color="#e67e22"
    )
    
    # 3.5 带背景色的Label
    background_label = Label(
        "🎨 自定义背景颜色",
        background_color="#ecf0f1",  # 🆕 新特性：背景颜色
        style=ComponentStyle(
            width=px(200),
            height=px(35),
            margin=px(5)
        ),
        font_size=13,
        text_align="center",
        color="#2c3e50"
    )
    
    # 3.6 组合特性：可选择 + 边框 + 背景
    combo_label = Label(
        "✨ 组合特性：可选择+边框+背景",
        selectable=True,
        bordered=True,
        bezel_style=BezelStyle.ROUNDED,
        background_color="#fff3cd",
        style=ComponentStyle(
            width=percent(85),
            height=px(40),
            margin=px(10)
        ),
        font_size=14,
        text_align="center",
        color="#856404"
    )
    
    # 4. 创建TextField组件展示新特性
    
    # 4.1 分隔标题
    textfield_title = Label(
        "📝 TextField组件新特性：",
        style=ComponentStyle(
            width=percent(100),
            height=px(40),
            margin_top=px(20),
            padding=px(10)
        ),
        font_size=16,
        font_weight="bold",
        color="#2c3e50"
    )
    
    # 4.2 标准圆角TextField
    standard_textfield = TextField(
        text="标准圆角输入框",
        placeholder="请输入内容...",
        bordered=True,
        bezel_style=BezelStyle.ROUNDED,
        style=ComponentStyle(
            width=px(300),
            height=px(30),
            margin=px(5)
        ),
        font_size=13
    )
    
    # 4.3 方角TextField  
    square_textfield = TextField(
        text="方角边框输入框",
        placeholder="方角样式...",
        bordered=True,
        bezel_style=BezelStyle.SQUARE,
        style=ComponentStyle(
            width=px(300),
            height=px(30),
            margin=px(5)
        ),
        font_size=13
    )
    
    # 4.4 自定义背景色TextField
    colored_textfield = TextField(
        text="自定义背景色",
        placeholder="彩色背景...",
        background_color="#e8f5e8",
        style=ComponentStyle(
            width=px(300),
            height=px(30),
            margin=px(5)
        ),
        font_size=13,
        color="#2d5a2d"
    )
    
    # 4.5 带文本变化回调的TextField
    def on_text_change(text: str):
        print(f"📝 文本变化: '{text}'")
    
    interactive_textfield = TextField(
        text="",
        placeholder="输入文字试试看控制台输出...",
        on_text_change=on_text_change,
        style=ComponentStyle(
            width=px(350),
            height=px(30),
            margin=px(5)
        ),
        font_size=13
    )
    
    # 5. 创建Container布局所有组件
    main_container = Container(
        children=[
            title_label,
            selectable_label,
            # Label特性展示区域
            Container(
                children=[
                    bordered_round_label,
                    bordered_square_label,
                    background_label
                ],
                style=ComponentStyle(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    justify_content=JustifyContent.SPACE_AROUND,
                    width=percent(100),
                    margin=px(10)
                )
            ),
            combo_label,
            
            # TextField特性展示区域
            textfield_title,
            Container(
                children=[
                    standard_textfield,
                    square_textfield,
                    colored_textfield,
                    interactive_textfield
                ],
                style=ComponentStyle(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    align_items=AlignItems.CENTER,
                    width=percent(100),
                    margin=px(10),
                    gap=px(5)
                )
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=percent(100),
            height=percent(100),
            padding=px(20),
            background_color="#f8f9fa"
        )
    )

    # 6. 设置窗口内容
    window.set_content(main_container)

    print("✅ Enhanced Hello World with new features ready!")
    print("🆕 新特性展示:")
    print("   📝 Label: 可选择文本、边框样式、背景颜色")
    print("   ⌨️  TextField: 边框样式、背景色、占位符、事件回调")
    print("📚 Next: Try 02_reactive_basics.py to learn about reactive state")

    # 7. 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()
