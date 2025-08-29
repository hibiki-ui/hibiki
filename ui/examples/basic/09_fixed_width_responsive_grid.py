#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 09: 固定宽度响应式Grid
避免百分比宽度，使用固定宽度验证响应式Grid
"""

from hibiki.ui import (
    Signal, Label, Container, ComponentStyle, 
    Display, px,
    ManagerFactory, ResponsiveStyle, BreakpointName, responsive_style, get_responsive_manager
)


def create_grid_item(title: str, bg_color: str):
    """创建网格项目"""
    return Container(
        children=[
            Label(
                title,
                font_size=14,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle()
            )
        ],
        style=ComponentStyle(
            background_color=bg_color,
            border_color="#333",
            border_width=px(2),
            border_radius=px(8),
            padding=px(15),
            display=Display.FLEX,
            justify_content="center",
            align_items="center",
            min_height=px(80)
        )
    )


def main():
    """固定宽度响应式Grid测试"""
    print("🚀 Starting Fixed Width Responsive Grid...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Fixed Width Responsive Grid - Hibiki UI",
        width=1200,
        height=700
    )
    
    # 状态显示
    status_text = Signal("初始化中...")
    
    def update_status():
        try:
            responsive_mgr = get_responsive_manager()
            info = responsive_mgr.get_current_breakpoint_info()
            status_text.value = f"视口: {info['viewport_width']:.0f}px | 断点: {info['primary_breakpoint']}"
            print(f"📊 {status_text.value}")
        except Exception as e:
            status_text.value = f"错误: {e}"
    
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_status())
    update_status()
    
    status_display = Label(
        status_text,
        font_size=14,
        color="#333",
        text_align="center",
        style=ComponentStyle(
            padding=px(15),
            background_color="#e7f3ff",
            border_color="#007acc",
            border_width=px(2),
            border_radius=px(8),
            margin=px(20)
        )
    )
    
    # 创建6个网格项目
    items = [
        create_grid_item("A", "#ffebee"),
        create_grid_item("B", "#e8f5e8"),
        create_grid_item("C", "#e3f2fd"),
        create_grid_item("D", "#fff3e0"),
        create_grid_item("E", "#f3e5f5"),
        create_grid_item("F", "#e0f2f1")
    ]
    
    # 🔥 基础样式 - 使用固定宽度
    base_style = ComponentStyle(
        display=Display.GRID,
        grid_template_columns="1fr",  # 默认1列
        gap=px(15),
        padding=px(20),
        background_color="#f8f9fa",
        border_color="#007acc",
        border_width=px(3),
        border_radius=px(10),
        margin=px(20),
        width=px(800)  # 🔥 固定宽度，避免百分比问题
    )
    
    # 响应式样式
    grid_responsive_style = (
        responsive_style(base_style)
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            grid_template_columns="1fr 1fr 1fr",  # 3列
            width=px(900)  # 3列需要更宽
        ))
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            grid_template_columns="2fr 1fr 1fr",  # 混合尺寸
            width=px(1000)  # 混合尺寸需要最宽
        ))
    )
    
    # 创建响应式Grid容器
    grid_container = Container(
        children=items,
        style=ComponentStyle(),  # 空基础样式
        responsive_style=grid_responsive_style
    )
    
    # 主容器
    main_container = Container(
        children=[
            Label(
                "🔲 固定宽度响应式Grid测试",
                font_size=20,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(15),
                    padding=px(20),
                    background_color="#f8f9ff",
                    border_radius=px(8)
                )
            ),
            status_display,
            grid_container,
            Label(
                "🧪 测试说明:\n"
                "• 所有宽度都是固定像素值，避免百分比计算问题\n"
                "• 小屏幕: 1列，宽度800px\n"  
                "• LG断点: 3列，宽度900px\n"
                "• XL断点: 混合尺寸，宽度1000px\n"
                "• 1200px窗口应该触发XL断点",
                font_size=14,
                color="#555",
                text_align="left",
                style=ComponentStyle(
                    margin=px(20),
                    padding=px(15),
                    background_color="#f8f9fa",
                    border_radius=px(6)
                )
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction="column",
            padding=px(30),
            background_color="#ffffff"
        )
    )
    
    # 设置窗口内容
    window.set_content(main_container)
    
    # 手动触发响应式更新
    responsive_mgr.update_viewport(1200.0, 700.0)
    
    print("✅ Fixed width responsive grid ready!")
    print("🎯 期望: 1200px应显示1000px宽的混合尺寸Grid (2fr 1fr 1fr)")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()