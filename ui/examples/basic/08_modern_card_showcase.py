#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 11: 现代化Card组件设计展示
创建精美的Material Design风格卡片组件，展示现代UI设计元素

设计特色：
🎨 渐变背景和优雅配色
🔘 圆角设计和柔和阴影
🖼️ 图片占位符和内容布局
📱 响应式设计适配
✨ 悬停效果和交互反馈
🎯 多种卡片样式和用途
"""

from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container, TextField,
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems, 
    px, percent,
    ManagerFactory, ResponsiveStyle, BreakpointName, responsive_style, get_responsive_manager
)


def create_gradient_card(
    title: str, 
    subtitle: str, 
    content: str,
    gradient_colors: tuple,
    accent_color: str,
    card_type: str = "info"
):
    """创建带渐变背景的现代化Card
    
    Args:
        title: 卡片标题
        subtitle: 副标题
        content: 主要内容
        gradient_colors: 渐变色元组 (start_color, end_color)
        accent_color: 强调色
        card_type: 卡片类型 (info, feature, action, stats)
    """
    start_color, _ = gradient_colors  # end_color unused in this simple implementation
    
    # 🎨 现代化Card样式 - Material Design风格
    card_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        background_color=start_color,  # 基础背景色
        border_radius=px(16),  # 大圆角，现代感
        padding=px(24),
        margin=px(16),
        # 🌟 柔和阴影效果 - 模拟Material Design elevation
        border_color="rgba(0,0,0,0.12)",
        border_width=px(1),
        min_height=px(280),
        max_width=px(310),  # 稍微减小最大宽度避免重叠
        width=px(290),      # 减小固定宽度
        min_width=px(270)   # 调整最小宽度
    )
    
    # 📱 图片占位符样式
    image_placeholder_style = ComponentStyle(
        width=percent(100),
        height=px(120),
        background_color="#f0f0f0",
        border_radius=px(12),
        margin_bottom=px(16),
        display=Display.FLEX,
        justify_content=JustifyContent.CENTER,
        align_items=AlignItems.CENTER,
        border_color="#e0e0e0",
        border_width=px(1)
    )
    
    # 🏷️ 标题样式 - 现代typography
    title_style = ComponentStyle(
        margin_bottom=px(8)
    )
    
    # 📝 副标题样式
    subtitle_style = ComponentStyle(
        margin_bottom=px(16)
    )
    
    # 📄 内容样式
    content_style = ComponentStyle(
        margin_bottom=px(20),
        flex_grow=1  # 占用剩余空间
    )
    
    # 🎯 Action按钮样式
    action_button_style = ComponentStyle(
        background_color=accent_color,
        border_color=accent_color,
        border_width=px(0),
        border_radius=px(8),
        padding=px(12),
        min_width=px(100)
    )
    
    # 创建组件
    image_placeholder = Container(
        children=[
            Label(
                "🖼️ 图片占位符",
                color="#999",
                font_size=14,
                text_align="center"
            )
        ],
        style=image_placeholder_style
    )
    
    title_label = Label(
        title,
        font_size=20,
        font_weight="bold",
        color="#1a1a1a",
        text_align="left",
        style=title_style
    )
    
    subtitle_label = Label(
        subtitle,
        font_size=14,
        color="#666",
        text_align="left",
        style=subtitle_style
    )
    
    content_label = Label(
        content,
        font_size=15,
        color="#444",
        text_align="left",
        style=content_style
    )
    
    # 不同类型的Card有不同的底部元素
    if card_type == "action":
        bottom_element = Button(
            "了解更多",
            style=action_button_style
        )
    elif card_type == "stats":
        bottom_element = Container(
            children=[
                Label(
                    "📊 数据更新于 2分钟前",
                    font_size=12,
                    color="#888",
                    text_align="right"
                )
            ],
            style=ComponentStyle(
                justify_content=JustifyContent.FLEX_END,
                align_items=AlignItems.CENTER
            )
        )
    else:
        bottom_element = Label(
            f"• {card_type.upper()} •",
            font_size=12,
            color=accent_color,
            font_weight="bold",
            text_align="center",
            style=ComponentStyle()
        )
    
    return Container(
        children=[
            image_placeholder,
            title_label,
            subtitle_label, 
            content_label,
            bottom_element
        ],
        style=card_style
    )


def create_hero_card():
    """创建主要展示Card - 大尺寸，更多视觉元素"""
    
    hero_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        background_color="#ffffff",
        border_radius=px(20),
        padding=px(32),
        margin=px(20),
        border_color="rgba(0,0,0,0.08)",
        border_width=px(1),
        min_height=px(400),
        width=px(380)
    )
    
    # 大图片占位符
    hero_image_style = ComponentStyle(
        width=percent(100),
        height=px(180),
        background_color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",  # 渐变背景
        border_radius=px(16),
        margin_bottom=px(24),
        display=Display.FLEX,
        justify_content=JustifyContent.CENTER,
        align_items=AlignItems.CENTER
    )
    
    hero_image = Container(
        children=[
            Label(
                "🌟 Hero Image\n精美展示区域",
                color="white",
                font_size=18,
                font_weight="bold",
                text_align="center"
            )
        ],
        style=hero_image_style
    )
    
    # Hero标题
    hero_title = Label(
        "🎯 现代化UI设计",
        font_size=24,
        font_weight="bold",
        color="#2c3e50",
        text_align="center",
        style=ComponentStyle(margin_bottom=px(12))
    )
    
    # Hero描述
    hero_description = Label(
        "体验精美的Material Design风格卡片组件，"
        "包含渐变背景、优雅阴影、圆角设计等现代UI元素。",
        font_size=16,
        color="#5a6c7d",
        text_align="center",
        style=ComponentStyle(margin_bottom=px(24))
    )
    
    # Hero按钮组
    button_container = Container(
        children=[
            Button(
                "开始体验",
                style=ComponentStyle(
                    background_color="#3498db",
                    border_color="#3498db",
                    border_radius=px(10),
                    padding=px(16),
                    margin_right=px(12),
                    min_width=px(120)
                )
            ),
            Button(
                "了解更多",
                style=ComponentStyle(
                    background_color="transparent",
                    border_color="#3498db",
                    border_width=px(2),
                    border_radius=px(10),
                    padding=px(16),
                    min_width=px(120)
                )
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            gap=px(12)
        )
    )
    
    return Container(
        children=[
            hero_image,
            hero_title,
            hero_description,
            button_container
        ],
        style=hero_style
    )


def create_profile_card():
    """创建用户资料Card - 个性化信息展示"""
    
    profile_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        background_color="#fafbfc",
        border_radius=px(18),
        padding=px(24),
        margin=px(16),
        border_color="rgba(0,0,0,0.06)",
        border_width=px(1),
        width=px(300),
        min_height=px(320)
    )
    
    # 头像占位符
    avatar_style = ComponentStyle(
        width=px(80),
        height=px(80),
        background_color="#e74c3c",
        border_radius=px(40),  # 圆形头像
        margin_bottom=px(16),
        display=Display.FLEX,
        justify_content=JustifyContent.CENTER,
        align_items=AlignItems.CENTER,
# align_self will be handled by parent container alignment
    )
    
    avatar = Container(
        children=[
            Label(
                "👤",
                font_size=32,
                text_align="center"
            )
        ],
        style=avatar_style
    )
    
    # 用户信息
    user_name = Label(
        "张小明",
        font_size=20,
        font_weight="bold",
        color="#2c3e50",
        text_align="center",
        style=ComponentStyle(margin_bottom=px(6))
    )
    
    user_role = Label(
        "高级UI设计师",
        font_size=14,
        color="#7f8c8d",
        text_align="center", 
        style=ComponentStyle(margin_bottom=px(16))
    )
    
    # 统计信息
    stats_container = Container(
        children=[
            Container(
                children=[
                    Label("项目", font_size=12, color="#95a5a6", text_align="center"),
                    Label("24", font_size=18, font_weight="bold", color="#2c3e50", text_align="center")
                ],
                style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.COLUMN, flex_grow=1)
            ),
            Container(
                children=[
                    Label("经验", font_size=12, color="#95a5a6", text_align="center"),
                    Label("5年", font_size=18, font_weight="bold", color="#2c3e50", text_align="center")
                ],
                style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.COLUMN, flex_grow=1)
            ),
            Container(
                children=[
                    Label("评分", font_size=12, color="#95a5a6", text_align="center"),
                    Label("4.9⭐", font_size=18, font_weight="bold", color="#2c3e50", text_align="center")
                ],
                style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.COLUMN, flex_grow=1)
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.SPACE_AROUND,
            margin_bottom=px(20),
            padding=px(16),
            background_color="#ffffff",
            border_radius=px(12),
            border_color="rgba(0,0,0,0.05)",
            border_width=px(1)
        )
    )
    
    # 联系按钮
    contact_button = Button(
        "查看作品集",
        style=ComponentStyle(
            background_color="#9b59b6",
            border_color="#9b59b6",
            border_radius=px(10),
            padding=px(14),
            width=percent(100)
        )
    )
    
    return Container(
        children=[
            avatar,
            user_name,
            user_role,
            stats_container,
            contact_button
        ],
        style=profile_style
    )


def create_interactive_card():
    """创建可交互Card - 包含输入元素"""
    
    interactive_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        background_color="#ffffff",
        border_radius=px(16),
        padding=px(24),
        margin=px(16),
        border_color="rgba(52, 152, 219, 0.2)",
        border_width=px(2),
        width=px(320),
        min_height=px(300)
    )
    
    # 标题
    title = Label(
        "💬 快速联系",
        font_size=18,
        font_weight="bold",
        color="#2c3e50",
        text_align="left",
        style=ComponentStyle(margin_bottom=px(8))
    )
    
    # 描述
    description = Label(
        "有任何问题？请填写下面的表单，我们会尽快回复您。",
        font_size=14,
        color="#7f8c8d",
        text_align="left",
        style=ComponentStyle(margin_bottom=px(20))
    )
    
    # 输入字段样式
    input_style = ComponentStyle(
        margin_bottom=px(16),
        border_radius=px(8),
        border_color="#ddd",
        border_width=px(1),
        padding=px(12)
    )
    
    # 表单元素
    name_input = TextField(
        placeholder="您的姓名",
        style=input_style
    )
    
    email_input = TextField(
        placeholder="邮箱地址",
        style=input_style
    )
    
    # 提交按钮
    submit_button = Button(
        "发送消息",
        style=ComponentStyle(
            background_color="#27ae60",
            border_color="#27ae60",
            border_radius=px(8),
            padding=px(14),
            width=percent(100),
            margin_top=px(8)
        )
    )
    
    return Container(
        children=[
            title,
            description,
            name_input,
            email_input,
            submit_button
        ],
        style=interactive_style
    )


def create_card_grid():
    """创建Card网格布局 - 响应式多列布局"""
    
    # 各种Card实例
    cards = [
        create_gradient_card(
            "🚀 功能特色",
            "现代化设计",
            "采用Material Design设计语言，提供直观优雅的用户体验，支持响应式布局适配各种屏幕。",
            ("#f8f9fa", "#e9ecef"),
            "#007bff",
            "feature"
        ),
        
        create_gradient_card(
            "📊 数据分析",
            "实时统计",
            "强大的数据分析能力，实时处理和展示关键指标，助力业务决策优化。",
            ("#e8f5e9", "#c8e6c9"),
            "#28a745",
            "stats"
        ),
        
        create_gradient_card(
            "🎯 精准营销",
            "智能推荐", 
            "基于用户行为和偏好的智能推荐算法，提升用户参与度和转化率。",
            ("#fff3e0", "#ffe0b2"),
            "#ff9800",
            "action"
        ),
        
        create_gradient_card(
            "🔐 安全可靠",
            "企业级保护",
            "多层次安全防护体系，保障数据安全和隐私保护，符合国际安全标准。",
            ("#fce4ec", "#f8bbd9"),
            "#e91e63",
            "info"
        ),
        
        create_gradient_card(
            "⚡ 高性能",
            "极速体验",
            "优化的算法和架构设计，提供毫秒级响应时间，支持高并发访问场景。",
            ("#e8f5e9", "#c8e6c9"),
            "#28a745",
            "feature"
        ),
        
        create_gradient_card(
            "🎨 可定制",
            "灵活配置",
            "丰富的主题选项和自定义配置，满足不同业务场景的视觉需求。",
            ("#fff3e0", "#ffe0b2"),
            "#ff9800",
            "info"
        )
    ]
    
    # 基础Grid样式 - 使用更小的gap和padding避免重叠
    base_style = ComponentStyle(
        display=Display.GRID,
        grid_template_columns="1fr",  # 默认1列（小屏幕）
        gap=px(16),  # 减小gap避免重叠
        padding=px(16),  # 减小padding
        background_color="#f8f9fa",
        width=percent(100)  # 使用百分比宽度，适应父容器
    )
    
    # 响应式Grid布局 - 重新计算宽度避免重叠
    # 计算逻辑：列数 * 320px(卡片+间距) + 额外padding
    # 关键：不设置固定宽度，让容器自适应
    
    responsive_grid_style = (
        responsive_style(base_style)
        # 小屏幕：1列
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",
            max_width=px(350)
        ))
        .at_breakpoint(BreakpointName.SM, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",
            max_width=px(380)
        ))
        # 中屏幕：2列
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr",
            max_width=px(680)
        ))
        # 大屏幕：3列
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr 1fr",
            max_width=px(1020)
        ))
        # 超大屏幕：4列
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr 1fr 1fr",
            max_width=px(1360)
        ))
    )
    
    return Container(
        children=cards,
        style=ComponentStyle(),  # 空基础样式
        responsive_style=responsive_grid_style
    )


def create_special_cards_section():
    """创建特殊Card展示区域 - 响应式布局"""
    
    special_cards = [
        create_hero_card(),
        create_profile_card(),
        create_interactive_card()
    ]
    
    # 基础样式 - 使用更保守的间距
    base_style = ComponentStyle(
        display=Display.GRID,
        grid_template_columns="1fr",  # 默认1列（小屏幕）
        gap=px(24),  # 减小gap避免重叠
        padding=px(16),  # 减小padding
        width=percent(100)  # 使用百分比宽度
    )
    
    # 响应式布局 - 特殊卡片布局，避免重叠
    responsive_special_style = (
        responsive_style(base_style)
        # 小屏幕：1列
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",
            max_width=px(420)
        ))
        .at_breakpoint(BreakpointName.SM, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",
            max_width=px(450)
        ))
        # 中屏幕：1列（特殊卡片较宽）
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",
            max_width=px(500)
        ))
        # 大屏幕：2列
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr",
            max_width=px(880)  # 减小宽度避免重叠
        ))
        # 超大屏幕：3列
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr 1fr",
            max_width=px(1300)  # 减小宽度
        ))
    )
    
    return Container(
        children=special_cards,
        style=ComponentStyle(),
        responsive_style=responsive_special_style
    )


def main():
    """现代化Card组件展示主程序"""
    print("🚀 Starting Modern Card Showcase...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Modern Card Showcase - Hibiki UI",
        width=1400,  # 足够显示4列卡片的宽度
        height=1200
    )
    
    # 页面标题
    page_title = Label(
        "🎨 现代化Card组件展示",
        font_size=28,
        font_weight="bold",
        color="#2c3e50",
        text_align="center",
        style=ComponentStyle(
            margin_bottom=px(16),
            padding=px(20)
        )
    )
    
    # 副标题
    page_subtitle = Label(
        "Material Design风格 • 渐变背景 • 圆角阴影 • 响应式布局",
        font_size=16,
        color="#7f8c8d",
        text_align="center",
        style=ComponentStyle(
            margin_bottom=px(40),
            padding_bottom=px(20),
            border_color="rgba(0,0,0,0.1)",
            border_width=px(1)
        )
    )
    
    # 基础Card展示标题
    basic_section_title = Label(
        "📋 基础Card样式",
        font_size=22,
        font_weight="bold",
        color="#34495e",
        text_align="center",
        style=ComponentStyle(
            margin_top=px(20),
            margin_bottom=px(30)
        )
    )
    
    # 特殊Card展示标题
    special_section_title = Label(
        "✨ 特殊用途Card",
        font_size=22,
        font_weight="bold",
        color="#34495e",
        text_align="center",
        style=ComponentStyle(
            margin_top=px(50),
            margin_bottom=px(30)
        )
    )
    
    # 创建Card网格和特殊Card
    card_grid = create_card_grid()
    special_cards = create_special_cards_section()
    
    # 主容器 - 简化布局
    main_container = Container(
        children=[
            page_title,
            page_subtitle,
            basic_section_title,
            card_grid,
            special_section_title,
            special_cards
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20),  # 减小padding
            background_color="#f8f9fa",
            min_height=px(1000),
            width=percent(100),
            max_width=px(1400)  # 限制最大宽度避免过度拉伸
        )
    )
    
    # 设置窗口内容
    window.set_content(main_container)
    
    # 注册响应式管理器并触发更新
    responsive_mgr = get_responsive_manager()
    responsive_mgr.register_component(card_grid)
    responsive_mgr.register_component(special_cards)
    
    # 手动触发响应式更新，确保正确的列数显示
    responsive_mgr.update_viewport(1400.0, 1200.0)
    
    print("✅ Modern Card showcase ready!")
    print("🎨 特色展示:")
    print("   🌈 渐变背景和现代配色") 
    print("   🔘 圆角设计和柔和阴影")
    print("   🖼️ 图片占位符和内容布局")
    print("   📱 响应式网格布局 - 1400px窗口应显示4列")
    print("   ✨ 多样化Card类型和用途")
    print("   🎯 Material Design风格")
    print("   📏 网格计算: 4列×300px + 3×20px(gap) + 40px(padding) = 1300px")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()