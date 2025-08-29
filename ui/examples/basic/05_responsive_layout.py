#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 05: 响应式布局系统
实现真正的响应式设计，让页面内容根据窗口大小动态调整

学习目标：
✅ 理解断点系统（breakpoints）
✅ 掌握响应式样式规则
✅ 学习媒体查询和条件样式
✅ 实现自适应布局
✅ 体验窗口大小变化的实时响应

重要特性：
🔥 智能断点系统：xs, sm, md, lg, xl
🎯 响应式样式规则：根据窗口大小自动切换
📱 媒体查询支持：灵活的条件样式
🏗️ 与现有布局引擎完美集成
"""

from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container,
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems, px, percent,
    ManagerFactory,
    # 🔥 新增：响应式布局系统
    ResponsiveStyle, BreakpointName, 
    responsive_style, breakpoint_style, media_query_style,
    get_responsive_manager
)


def create_responsive_card(title: str, content: str, color_scheme: tuple):
    """创建响应式卡片组件
    
    展示如何创建一个在不同屏幕尺寸下表现不同的卡片：
    - 小屏幕：垂直堆叠，全宽
    - 中屏幕：两列布局  
    - 大屏幕：三列布局，带更多边距
    """
    bg_color, border_color, text_color = color_scheme
    
    # 🎯 响应式样式定义
    card_responsive_style = (
        responsive_style(
            # 基础样式（所有尺寸通用）
            ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                padding=px(15),
                background_color=bg_color,
                border_color=border_color,
                border_width=px(2),
                border_radius=px(8),
                margin=px(10)
            )
        )
        # 📱 小屏幕 (xs: 0-575px) - 移动设备
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            width=percent(100),
            margin_bottom=px(15),
            padding=px(12)
        ))
        # 📺 中屏幕 (md: 768-991px) - 平板横屏
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            width=percent(45),
            margin=px(15),
            padding=px(18)
        ))
        # 🖥️ 大屏幕 (lg: 992-1199px) - 桌面
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            width=percent(30),
            margin=px(20),
            padding=px(25)
        ))
        # 🖥️ 超大屏幕 (xl: 1200px+) - 大桌面
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            width=percent(22),
            margin=px(25),
            padding=px(30),
            border_width=px(3)
        ))
    )
    
    # 标题样式 - 响应式布局
    title_responsive_style = (
        responsive_style(
            ComponentStyle(
                margin_bottom=px(10)
            )
        )
        # 在不同断点下调整字体大小（通过重新挂载实现）
        # 注意：这里仅为演示响应式布局，文本样式在实际应用中可能需要不同的处理方式
    )
    
    # 内容样式
    content_responsive_style = (
        responsive_style(
            ComponentStyle(
                margin_top=px(5)
            )
        )
    )
    
    # 创建组件 - 使用Label的文本参数
    title_label = Label(
        title,
        font_weight="bold",
        color=text_color,
        text_align="center",
        font_size=18,  # 基础字体大小
        style=ComponentStyle(),
        responsive_style=title_responsive_style
    )
    
    content_label = Label(
        content,
        color="#666",
        text_align="center", 
        font_size=14,  # 基础字体大小
        style=ComponentStyle(),
        responsive_style=content_responsive_style
    )
    
    return Container(
        children=[title_label, content_label],
        style=ComponentStyle(),  # 占位基础样式
        responsive_style=card_responsive_style
    )


def create_responsive_header():
    """创建响应式页面头部
    
    演示复杂的响应式布局：
    - 小屏幕：单行居中
    - 大屏幕：双行带副标题
    """
    
    # 主标题响应式样式 - 仅布局属性
    main_title_style = (
        responsive_style(
            ComponentStyle(
                margin_bottom=px(10)
            )
        )
    )
    
    # 副标题响应式样式 - 包含显示隐藏逻辑
    subtitle_style = (
        responsive_style(
            ComponentStyle(
                margin_bottom=px(20)
            )
        )
        # 🔥 关键特性：在小屏幕隐藏副标题
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            display=Display.NONE  # 小屏幕隐藏
        ))
        .at_breakpoint(BreakpointName.SM, ComponentStyle(
            display=Display.FLEX  # 其他尺寸显示
        ))
    )
    
    main_title = Label(
        "🎯 Hibiki UI 响应式布局演示",
        font_weight="bold",
        color="#1976d2",
        text_align="center",
        font_size=32,
        style=ComponentStyle(),
        responsive_style=main_title_style
    )
    
    subtitle = Label(
        "📱 调整窗口大小，观察页面内容的自适应变化",
        color="#666",
        text_align="center",
        font_size=16,
        style=ComponentStyle(),
        responsive_style=subtitle_style
    )
    
    return Container(
        children=[main_title, subtitle],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            margin_bottom=px(30)
        )
    )


def create_media_query_demo():
    """创建媒体查询演示
    
    展示基于具体像素值的媒体查询功能
    """
    
    # 使用像素值的媒体查询
    media_query_demo_style = (
        responsive_style(
            ComponentStyle(
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                padding=px(20),
                border_radius=px(10),
                margin=px(20),
                min_height=px(60)
            )
        )
        # 窄屏幕 (< 600px)
        .at_max_width(600, ComponentStyle(
            background_color="#ffcdd2",
            border_color="#d32f2f",
            border_width=px(2),
        ))
        # 中等屏幕 (600-1000px)
        .at_width_range(600, 1000, ComponentStyle(
            background_color="#c8e6c9",
            border_color="#388e3c",
            border_width=px(2),
        ))
        # 宽屏幕 (> 1000px)
        .at_min_width(1000, ComponentStyle(
            background_color="#bbdefb",
            border_color="#1976d2",
            border_width=px(3),
        ))
    )
    
    # 动态文本，显示当前窗口宽度信息
    viewport_signal = Signal("加载中...")
    
    def update_viewport_info():
        """更新视口信息"""
        try:
            from hibiki.ui.core.managers import ManagerFactory
            viewport_mgr = ManagerFactory.get_viewport_manager()
            width, height = viewport_mgr.get_viewport_size()
            
            # 根据宽度显示不同信息
            if width < 600:
                viewport_signal.value = f"📱 小屏幕模式 - {width:.0f}×{height:.0f}px"
            elif width < 1000:
                viewport_signal.value = f"💻 中屏幕模式 - {width:.0f}×{height:.0f}px"
            else:
                viewport_signal.value = f"🖥️ 大屏幕模式 - {width:.0f}×{height:.0f}px"
        except Exception as e:
            viewport_signal.value = f"视口信息获取失败: {e}"
    
    # 添加样式变化回调
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_viewport_info())
    
    # 初始更新
    update_viewport_info()
    
    return Container(
        children=[
            Label(
                viewport_signal,
                color="#333",
                text_align="center",
                font_size=16,
                style=ComponentStyle()
            )
        ],
        style=ComponentStyle(),
        responsive_style=media_query_demo_style
    )


def create_responsive_grid_demo():
    """创建响应式网格演示
    
    展示网格布局在不同屏幕尺寸下的自适应行为
    """
    
    # 网格容器的响应式样式
    grid_container_style = (
        responsive_style(
            ComponentStyle(
                display=Display.FLEX,  # 使用Flex模拟Grid的响应式行为
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                gap=px(15),
                padding=px(20),
                background_color="#fafafa",
                border_radius=px(10),
                margin=px(20)
            )
        )
        # 小屏幕：单列
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            flex_direction=FlexDirection.COLUMN
        ))
        # 中屏幕：两列（通过子元素宽度控制）
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            flex_direction=FlexDirection.ROW
        ))
    )
    
    # 创建网格项目
    grid_items = []
    item_colors = [
        ("#e1f5fe", "#0277bd", "项目 1"),
        ("#f3e5f5", "#7b1fa2", "项目 2"),
        ("#fff3e0", "#e65100", "项目 3"),
        ("#e8f5e8", "#2e7d32", "项目 4"),
    ]
    
    for bg_color, border_color, text in item_colors:
        # 网格项目的响应式样式
        item_style = (
            responsive_style(
                ComponentStyle(
                    display=Display.FLEX,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER,
                    padding=px(20),
                    background_color=bg_color,
                    border_color=border_color,
                    border_width=px(2),
                    border_radius=px(8),
                    margin=px(5)
                )
            )
            # 小屏幕：全宽
            .at_breakpoint(BreakpointName.XS, ComponentStyle(
                width=percent(100),
                height=px(60)
            ))
            # 中屏幕：约一半宽
            .at_breakpoint(BreakpointName.MD, ComponentStyle(
                width=percent(45),
                height=px(80)
            ))
            # 大屏幕：约四分之一宽
            .at_breakpoint(BreakpointName.LG, ComponentStyle(
                width=percent(22),
                height=px(100)
            ))
        )
        
        item = Container(
            children=[
                Label(
                    text,
                    font_weight="bold",
                    color="#333",
                    text_align="center",
                    style=ComponentStyle()
                )
            ],
            style=ComponentStyle(),
            responsive_style=item_style
        )
        grid_items.append(item)
    
    return Container(
        children=grid_items,
        style=ComponentStyle(),
        responsive_style=grid_container_style
    )


def create_breakpoint_info_panel():
    """创建断点信息面板
    
    实时显示当前匹配的断点信息
    """
    current_breakpoint = Signal("检测中...")
    viewport_info = Signal("获取中...")
    
    def update_breakpoint_info():
        """更新断点信息"""
        try:
            responsive_mgr = get_responsive_manager()
            info = responsive_mgr.get_current_breakpoint_info()
            
            current_breakpoints = info['current_breakpoints']
            primary_breakpoint = info['primary_breakpoint']
            viewport_width = info['viewport_width']
            
            current_breakpoint.value = f"主断点: {primary_breakpoint} | 匹配: {', '.join(current_breakpoints)}"
            viewport_info.value = f"窗口宽度: {viewport_width:.0f}px | 注册组件: {info['registered_components']}"
            
        except Exception as e:
            current_breakpoint.value = f"断点信息获取失败: {e}"
            viewport_info.value = "信息不可用"
    
    # 添加回调
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_breakpoint_info())
    
    # 初始更新
    update_breakpoint_info()
    
    return Container(
        children=[
            Label(
                "📊 实时断点信息",
                font_size=18,
                font_weight="bold",
                color="#1976d2",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(10)
                )
            ),
            Label(
                current_breakpoint,
                font_size=14,
                color="#333",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(5)
                )
            ),
            Label(
                viewport_info,
                font_size=12,
                color="#666",
                text_align="center",
                style=ComponentStyle()
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20),
            background_color="#f5f5f5",
            border_radius=px(8),
            margin=px(20)
        )
    )


def main():
    """响应式布局演示主程序"""
    print("🚀 Starting Responsive Layout Example...")
    
    # 创建应用管理器
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Responsive Layout Demo - Hibiki UI",
        width=1000,
        height=800
    )
    
    # 创建页面头部
    header = create_responsive_header()
    
    # 创建响应式卡片
    cards = [
        create_responsive_card(
            "移动优先设计",
            "小屏幕单列，大屏幕多列",
            ("#e1f5fe", "#0277bd", "#1976d2")
        ),
        create_responsive_card(
            "断点系统",
            "xs, sm, md, lg, xl 五个标准断点",
            ("#f3e5f5", "#7b1fa2", "#6a1b9a")
        ),
        create_responsive_card(
            "媒体查询",
            "灵活的条件样式规则",
            ("#fff3e0", "#e65100", "#d84315")
        ),
        create_responsive_card(
            "实时响应",
            "窗口大小变化即时更新",
            ("#e8f5e8", "#2e7d32", "#388e3c")
        ),
    ]
    
    # 卡片容器的响应式样式
    cards_container_style = (
        responsive_style(
            ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                gap=px(10),
                padding=px(20)
            )
        )
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            flex_direction=FlexDirection.COLUMN  # 小屏幕垂直排列
        ))
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            flex_direction=FlexDirection.ROW
        ))
    )
    
    cards_container = Container(
        children=cards,
        style=ComponentStyle(),
        responsive_style=cards_container_style
    )
    
    # 创建其他演示组件
    media_query_demo = create_media_query_demo()
    grid_demo = create_responsive_grid_demo()
    info_panel = create_breakpoint_info_panel()
    
    # 主容器
    main_container = Container(
        children=[
            header,
            info_panel,
            Label(
                "🃏 响应式卡片演示",
                font_size=20,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(10),
                    margin_top=px(20)
                )
            ),
            cards_container,
            Label(
                "📐 媒体查询演示",
                font_size=20,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(10),
                    margin_top=px(30)
                )
            ),
            media_query_demo,
            Label(
                "⚡ 响应式网格演示",
                font_size=20,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(
                    margin_bottom=px(10),
                    margin_top=px(30)
                )
            ),
            grid_demo,
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20),
            background_color="#ffffff"
        )
    )
    
    # 设置窗口内容
    window.set_content(main_container)
    
    print("✅ Responsive Layout demo ready!")
    print("🎯 调整窗口大小来测试响应式布局:")
    print("   📱 < 576px  : 超小屏幕 (xs)")
    print("   📟 576-767px : 小屏幕 (sm)")
    print("   💻 768-991px : 中屏幕 (md)")
    print("   🖥️ 992-1199px: 大屏幕 (lg)")
    print("   🖥️ > 1200px  : 超大屏幕 (xl)")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()