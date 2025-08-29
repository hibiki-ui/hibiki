#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 06: 真正的CSS Grid响应式布局
使用CSS Grid而不是FlexBox实现响应式网格布局
"""

from hibiki.ui import (
    Signal, Label, Container, ComponentStyle, 
    Display, px, percent,
    ManagerFactory, ResponsiveStyle, BreakpointName, responsive_style, get_responsive_manager
)


def create_grid_item(title: str, subtitle: str, bg_color: str):
    """创建网格项目"""
    return Container(
        children=[
            Label(
                title,
                font_size=14,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(margin_bottom=px(5))
            ),
            Label(
                subtitle,
                font_size=12,
                color="#666",
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
            flex_direction="column",
            justify_content="center",
            align_items="center"
        )
    )


def create_css_grid_container(grid_items: list):
    """使用CSS Grid创建响应式网格容器"""
    
    # 🔥 基础Grid样式
    base_style = ComponentStyle(
        display=Display.GRID,  # 使用CSS Grid！
        grid_template_columns="1fr",  # 默认单列
        gap=px(15),
        padding=px(20),
        background_color="#f8f9fa",
        border_color="#007acc",
        border_width=px(3),
        border_radius=px(10),
        margin=px(20)
    )
    
    # 🎯 响应式Grid样式
    grid_responsive_style = (
        responsive_style(base_style)
        # 超小屏幕：1列
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            grid_template_columns="1fr",  # 1列
            width=percent(95)
        ))
        # 小屏幕：1列
        .at_breakpoint(BreakpointName.SM, ComponentStyle(
            grid_template_columns="1fr",  # 1列
            width=percent(90)
        ))
        # 中屏幕：2列
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            grid_template_columns="repeat(2, 1fr)",  # 2列
            width=percent(95)
        ))
        # 大屏幕：3列
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            grid_template_columns="repeat(3, 1fr)",  # 3列
            width=percent(98)
        ))
        # 超大屏幕：4列
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            grid_template_columns="repeat(4, 1fr)",  # 4列
            width=percent(100)
        ))
    )
    
    print("🔥 创建CSS Grid容器")
    print(f"   基础样式: display=GRID, columns={base_style.grid_template_columns}")
    print(f"   响应式规则数: {len(grid_responsive_style.responsive_rules)}")
    
    return Container(
        children=grid_items,
        style=ComponentStyle(),  # 空基础样式，使用响应式样式
        responsive_style=grid_responsive_style
    )


def create_grid_status_panel():
    """创建Grid状态显示面板"""
    
    status_info = Signal("初始化中...")
    
    def update_status():
        try:
            responsive_mgr = get_responsive_manager()
            info = responsive_mgr.get_current_breakpoint_info()
            
            viewport_width = info['viewport_width']
            primary_breakpoint = info['primary_breakpoint']
            current_breakpoints = info['current_breakpoints']
            
            # 计算当前应该的列数
            if 'xl' in current_breakpoints:
                expected_columns = 4
                grid_template = "repeat(4, 1fr)"
            elif 'lg' in current_breakpoints:
                expected_columns = 3
                grid_template = "repeat(3, 1fr)"
            elif 'md' in current_breakpoints:
                expected_columns = 2
                grid_template = "repeat(2, 1fr)"
            else:  # xs, sm
                expected_columns = 1
                grid_template = "1fr"
            
            status_info.value = (
                f"🖥️ 视口: {viewport_width:.0f}px | "
                f"断点: {primary_breakpoint} | "
                f"Grid列数: {expected_columns} | "
                f"模板: {grid_template}"
            )
            
            print(f"📊 Grid状态更新: {status_info.value}")
            
        except Exception as e:
            status_info.value = f"错误: {e}"
    
    # 注册响应式回调
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_status())
    update_status()  # 立即更新一次
    
    return Container(
        children=[
            Label(
                "📊 CSS Grid 状态监控",
                font_size=16,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(margin_bottom=px(10))
            ),
            Label(
                status_info,
                font_size=14,
                color="#333",
                text_align="center",
                style=ComponentStyle()
            )
        ],
        style=ComponentStyle(
            background_color="#e7f3ff",
            border_color="#007acc",
            border_width=px(2),
            border_radius=px(8),
            padding=px(15),
            margin=px(20)
        )
    )


def main():
    """CSS Grid响应式布局演示"""
    print("🚀 Starting CSS Grid Responsive Demo...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="CSS Grid Responsive - Hibiki UI",
        width=1400,  # 大屏幕尺寸，应显示4列
        height=900
    )
    
    # 创建标题
    title = Label(
        "🔲 CSS Grid 响应式布局演示",
        font_size=22,
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
    
    # 创建说明
    description = Label(
        "📱 xs/sm: 1列 | 💻 md: 2列 | 🖥️ lg: 3列 | 📺 xl: 4列 - 使用真正的CSS Grid布局",
        font_size=14,
        color="#666",
        text_align="center",
        style=ComponentStyle(
            margin_bottom=px(15),
            padding=px(10),
            background_color="#fff3cd",
            border_radius=px(6)
        )
    )
    
    # 创建状态面板
    status_panel = create_grid_status_panel()
    
    # 创建12个网格项目用于测试多行显示
    grid_items_data = [
        ("Grid A", "第1个", "#ffebee"),
        ("Grid B", "第2个", "#e8f5e8"),
        ("Grid C", "第3个", "#e3f2fd"),
        ("Grid D", "第4个", "#fff3e0"),
        ("Grid E", "第5个", "#f3e5f5"),
        ("Grid F", "第6个", "#e0f2f1"),
        ("Grid G", "第7个", "#fce4ec"),
        ("Grid H", "第8个", "#e1f5fe"),
        ("Grid I", "第9个", "#f1f8e9"),
        ("Grid J", "第10个", "#faf2ff"),
        ("Grid K", "第11个", "#fff8e1"),
        ("Grid L", "第12个", "#e8eaf6")
    ]
    
    grid_items = []
    for title, subtitle, bg_color in grid_items_data:
        item = create_grid_item(title, subtitle, bg_color)
        grid_items.append(item)
    
    print(f"📦 创建了 {len(grid_items)} 个网格项目")
    
    # 创建CSS Grid容器
    grid_container = create_css_grid_container(grid_items)
    
    # 测试说明
    test_instructions = Label(
        "🧪 CSS Grid 测试:\n"
        "• 当前1400px宽度 → 应显示4列Grid布局\n"
        "• 调整到1000px → 3列布局\n"
        "• 调整到800px → 2列布局\n"
        "• 调整到600px → 1列布局\n"
        "• 12个项目会自动换行显示",
        font_size=13,
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
            description,
            status_panel,
            grid_container,
            test_instructions
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction="column",
            padding=px(30),
            background_color="#ffffff"
        )
    )
    
    # 设置窗口内容并确保响应式更新
    window.set_content(main_container)
    
    # 手动触发一次响应式更新确保Grid样式生效
    responsive_mgr = get_responsive_manager()
    responsive_mgr.update_viewport(1400.0, 900.0)
    
    print("✅ CSS Grid responsive demo ready!")
    print("🎯 期望结果: 1400px宽度应显示4列CSS Grid布局")
    print("📐 Grid模板: repeat(4, 1fr)")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()