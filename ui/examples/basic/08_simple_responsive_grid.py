#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 08: 简化版响应式CSS Grid
基于已验证工作的静态Grid，添加最基本的响应式功能
"""

from hibiki.ui import (
    Signal, Label, Container, ComponentStyle, 
    Display, px, percent,
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


def create_responsive_grid(items: list):
    """创建简化版响应式Grid容器"""
    
    # 🔥 基础Grid样式（已验证工作）
    base_style = ComponentStyle(
        display=Display.GRID,
        grid_template_columns="1fr",  # 默认1列（小屏幕）
        gap=px(10),
        padding=px(20),
        background_color="#f8f9fa",
        border_color="#007acc",
        border_width=px(3),
        border_radius=px(10),
        margin=px(20)
    )
    
    # 🎯 简单的响应式规则
    responsive_style_obj = (
        responsive_style(base_style)
        # 大屏幕：使用已验证工作的3列布局
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            grid_template_columns="1fr 1fr 1fr",  # 3列（已验证工作）
            width=percent(90)
        ))
        # 超大屏幕：使用已验证工作的混合尺寸
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            grid_template_columns="2fr 1fr 1fr",  # 混合尺寸（已验证工作）
            width=percent(95)
        ))
    )
    
    print(f"🔧 创建响应式Grid容器，基础样式: {base_style.grid_template_columns}")
    
    return Container(
        children=items,
        style=ComponentStyle(),  # 空的基础样式
        responsive_style=responsive_style_obj
    )


def create_status_display():
    """创建状态显示"""
    
    status_text = Signal("初始化中...")
    
    def update_status():
        try:
            responsive_mgr = get_responsive_manager()
            info = responsive_mgr.get_current_breakpoint_info()
            
            viewport_width = info['viewport_width']
            primary_breakpoint = info['primary_breakpoint']
            
            # 根据断点确定预期的Grid布局
            if primary_breakpoint == 'xl':
                expected_grid = "2fr 1fr 1fr (混合尺寸)"
            elif primary_breakpoint == 'lg':
                expected_grid = "1fr 1fr 1fr (3列相等)"
            else:
                expected_grid = "1fr (单列)"
            
            status_text.value = f"视口: {viewport_width:.0f}px | 断点: {primary_breakpoint} | Grid: {expected_grid}"
            print(f"📊 状态更新: {status_text.value}")
            
        except Exception as e:
            status_text.value = f"错误: {e}"
    
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_status())
    update_status()
    
    return Label(
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


def main():
    """简化版响应式Grid演示"""
    print("🚀 Starting Simple Responsive Grid...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Simple Responsive Grid - Hibiki UI",
        width=1200,  # 大屏幕尺寸，应该触发LG断点
        height=700
    )
    
    # 创建标题
    title = Label(
        "🔲 简化版响应式Grid布局",
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
    )
    
    # 状态显示
    status_display = create_status_display()
    
    # 创建6个网格项目（与静态示例相同）
    items = [
        create_grid_item("Grid A", "#ffebee"),
        create_grid_item("Grid B", "#e8f5e8"),
        create_grid_item("Grid C", "#e3f2fd"),
        create_grid_item("Grid D", "#fff3e0"),
        create_grid_item("Grid E", "#f3e5f5"),
        create_grid_item("Grid F", "#e0f2f1")
    ]
    
    # 创建响应式Grid容器
    grid_container = create_responsive_grid(items)
    
    # 说明
    instructions = Label(
        "🧪 简化测试:\n"
        "• 当前1200px → 应显示LG断点的3列Grid\n"
        "• 调整到1400px → 应切换到XL断点的混合尺寸Grid\n"
        "• 调整到800px → 应切换回单列Grid\n"
        "\n基于已验证工作的静态Grid布局",
        font_size=14,
        color="#555",
        text_align="left",
        style=ComponentStyle(
            margin=px(20),
            padding=px(15),
            background_color="#f8f9fa",
            border_radius=px(6),
            border_color="#dee2e6",
            border_width=px(1)
        )
    )
    
    # 主容器
    main_container = Container(
        children=[
            title,
            status_display,
            grid_container,
            instructions
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
    
    # 手动触发一次响应式更新
    responsive_mgr = get_responsive_manager()
    responsive_mgr.update_viewport(1200.0, 700.0)
    
    print("✅ Simple responsive grid ready!")
    print("🎯 期望结果: 1200px应显示3列Grid布局")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()