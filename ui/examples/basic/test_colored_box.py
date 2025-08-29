#!/usr/bin/env python3
"""
ColoredBox 测试程序 - 验证边框和背景色显示
"""

from hibiki.ui import (
    Label, Container, ManagerFactory, ComponentStyle, 
    Display, FlexDirection, JustifyContent, AlignItems, px
)

class ColoredBox:
    """简化的彩色盒子测试组件"""
    
    def __init__(self, text: str, background_color: str, border_color: str, 
                 width=None, height=None):
        self.text = text
        self.background_color = background_color
        self.border_color = border_color
        
        # 创建标签
        self.label = Label(
            text,
            font_size=14,
            font_weight="bold", 
            text_align="center",
            color="#333"
        )
        
        # 创建容器 - 应该显示背景色和边框
        self.container = Container(
            children=[self.label],
            style=ComponentStyle(
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                padding=px(15),
                width=px(width) if width else px(120),
                height=px(height) if height else px(80),
                background_color=background_color,
                border_color=border_color,
                border_width=px(3),
                border_radius=px(8)
            )
        )
    
    def get_component(self):
        return self.container


def main():
    """测试彩色盒子显示"""
    print("🎨 测试 ColoredBox 边框和背景色...")
    
    # 创建测试盒子
    red_box = ColoredBox("红盒子", "#ffcdd2", "#d32f2f", 150, 100)
    green_box = ColoredBox("绿盒子", "#c8e6c9", "#388e3c", 150, 100)
    blue_box = ColoredBox("蓝盒子", "#e3f2fd", "#1976d2", 150, 100)
    
    # 主容器
    main_container = Container(
        children=[
            Label(
                "🔍 ColoredBox 测试",
                font_size=24,
                font_weight="bold",
                text_align="center",
                color="#2c3e50",
                style=ComponentStyle(margin_bottom=px(30))
            ),
            Container(
                children=[
                    red_box.get_component(),
                    green_box.get_component(),
                    blue_box.get_component()
                ],
                style=ComponentStyle(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    justify_content=JustifyContent.CENTER,
                    gap=px(20),
                    padding=px(20)
                )
            )
        ],
        style=ComponentStyle(
            padding=px(30),
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER
        )
    )
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window("ColoredBox 测试", 600, 400)
    window.set_content(main_container)
    
    print("✅ 测试窗口已创建，检查盒子是否显示颜色！")
    app_manager.run()


if __name__ == "__main__":
    main()