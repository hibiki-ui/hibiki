#!/usr/bin/env python3
"""
测试Label的垂直居中效果
"""

from hibiki.ui import (
    Label, Container, ManagerFactory,
    ComponentStyle, Display, FlexDirection, AlignItems,
    px, percent
)
from hibiki.ui.components.text_field_config import BezelStyle


def main():
    """测试Label垂直居中"""
    print("🧪 Testing Label Vertical Centering...")

    # 1. 获取应用管理器
    app_manager = ManagerFactory.get_app_manager()

    # 2. 创建窗口
    window = app_manager.create_window(
        title="Label垂直居中测试",
        width=600,
        height=400
    )

    # 3. 创建不同高度的有边框Label来测试垂直居中效果

    # 高度30px的Label
    label_30 = Label(
        "高度30px - 应该垂直居中",
        bordered=True,
        bezel_style=BezelStyle.ROUNDED,
        style=ComponentStyle(
            width=px(350),
            height=px(30),
            margin=px(10)
        ),
        font_size=13,
        text_align="center"
    )

    # 高度40px的Label
    label_40 = Label(
        "高度40px - 应该垂直居中",
        bordered=True,
        bezel_style=BezelStyle.ROUNDED,
        style=ComponentStyle(
            width=px(350),
            height=px(40),
            margin=px(10)
        ),
        font_size=13,
        text_align="center"
    )

    # 高度50px的Label  
    label_50 = Label(
        "高度50px - 应该垂直居中",
        bordered=True,
        bezel_style=BezelStyle.ROUNDED,
        style=ComponentStyle(
            width=px(350),
            height=px(50),
            margin=px(10)
        ),
        font_size=13,
        text_align="center"
    )

    # 方角边框的Label
    label_square = Label(
        "方角边框 - 高度45px",
        bordered=True,
        bezel_style=BezelStyle.SQUARE,
        style=ComponentStyle(
            width=px(350),
            height=px(45),
            margin=px(10)
        ),
        font_size=13,
        text_align="center"
    )

    # 对比：没有边框但有背景色的Label
    label_no_border = Label(
        "无边框有背景Label - 高度40px (现在也应该居中)",
        background_color="#e8f4f8",
        style=ComponentStyle(
            width=px(350),
            height=px(40),
            margin=px(10)
        ),
        font_size=13,
        text_align="center",
        color="#2c3e50"
    )
    
    # 另一个背景色Label测试
    label_bg_yellow = Label(
        "黄色背景 - 高度35px (也应该垂直居中)",
        background_color="#fff3cd",
        style=ComponentStyle(
            width=px(350),
            height=px(35),
            margin=px(10)
        ),
        font_size=13,
        text_align="center",
        color="#856404"
    )

    # 4. 创建主容器
    main_container = Container(
        children=[
            Label(
                "Label垂直居中测试",
                font_size=20,
                font_weight="bold",
                text_align="center",
                style=ComponentStyle(
                    width=percent(100),
                    height=px(50),
                    margin_bottom=px(20)
                )
            ),
            label_30,
            label_40,
            label_50,
            label_square,
            label_no_border,
            label_bg_yellow
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=percent(100),
            height=percent(100),
            padding=px(20),
            background_color="#ffffff"
        )
    )

    # 5. 设置窗口内容
    window.set_content(main_container)

    print("✅ Label垂直居中测试准备就绪!")
    print("🔍 观察不同高度的有边框Label中文本是否垂直居中")

    # 6. 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()