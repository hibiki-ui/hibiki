#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 10: 动态Grid列数调整
基于验证工作的静态Grid，实现根据窗口宽度动态调整列数
"""

from hibiki.ui import (
    Signal, Label, Container, ComponentStyle, 
    Display, px,
    ManagerFactory, ResponsiveStyle, BreakpointName, responsive_style, get_responsive_manager
)


def create_grid_item(title: str, bg_color: str):
    """创建网格项目 - 使用固定宽度300px"""
    return Container(
        children=[
            Label(
                title,
                font_size=16,
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
            padding=px(20),
            display=Display.FLEX,
            justify_content="center",
            align_items="center",
            min_height=px(100),
            width=px(300)  # 🔥 固定宽度300px
        )
    )


def create_dynamic_grid_container(items: list):
    """创建动态列数Grid容器"""
    
    # 🔥 基础Grid样式（使用已验证工作的设置）
    base_style = ComponentStyle(
        display=Display.GRID,
        grid_template_columns="1fr",  # 默认1列（小屏幕）
        gap=px(15),
        padding=px(20),
        background_color="#f8f9fa",
        border_color="#007acc",
        border_width=px(3),
        border_radius=px(10),
        margin=px(20),
        justify_content="center"  # Grid项目居中
    )
    
    # 🎯 动态列数响应式规则 - 基于容器能容纳多少个300px宽的元素
    # 计算逻辑：容器宽度 ≈ 列数 * (300px + gap) + padding
    # 1列需要：300 + 40(padding) = 340px
    # 2列需要：300*2 + 15(gap) + 40(padding) = 655px  
    # 3列需要：300*3 + 30(gap) + 40(padding) = 970px
    # 4列需要：300*4 + 45(gap) + 40(padding) = 1285px
    
    responsive_style_obj = (
        responsive_style(base_style)
        # 小屏幕：1列（默认）
        .at_breakpoint(BreakpointName.XS, ComponentStyle(
            display=Display.GRID,  # 🔥 确保Grid布局
            grid_template_columns="1fr",  # 1列
            width=px(360)  # 容纳1列的最小宽度
        ))
        .at_breakpoint(BreakpointName.SM, ComponentStyle(
            display=Display.GRID,  # 🔥 确保Grid布局
            grid_template_columns="1fr",  # 1列 
            width=px(400)
        ))
        # 中屏幕：2列（容器宽度≥655px）
        .at_breakpoint(BreakpointName.MD, ComponentStyle(
            display=Display.GRID,  # 🔥 确保Grid布局
            grid_template_columns="1fr 1fr",  # 2列（已验证工作）
            width=px(700)  # 容纳2列
        ))
        # 大屏幕：3列（容器宽度≥970px）
        .at_breakpoint(BreakpointName.LG, ComponentStyle(
            display=Display.GRID,  # 🔥 确保Grid布局
            grid_template_columns="1fr 1fr 1fr",  # 3列（已验证工作）
            width=px(1000)  # 容纳3列
        ))
        # 超大屏幕：4列（容器宽度≥1285px）
        .at_breakpoint(BreakpointName.XL, ComponentStyle(
            display=Display.GRID,  # 🔥 确保Grid布局
            grid_template_columns="1fr 1fr 1fr 1fr",  # 4列
            width=px(1320)  # 容纳4列
        ))
    )
    
    print(f"🔧 创建动态列数Grid容器")
    print(f"   基础样式: display=GRID, columns={base_style.grid_template_columns}")
    print(f"   响应式规则: XS(1列) -> MD(2列) -> LG(3列) -> XL(4列)")
    
    return Container(
        children=items,
        style=ComponentStyle(),  # 空基础样式，使用响应式样式
        responsive_style=responsive_style_obj
    )


def create_status_display():
    """创建状态显示面板"""
    
    status_text = Signal("初始化中...")
    
    def update_status():
        try:
            responsive_mgr = get_responsive_manager()
            info = responsive_mgr.get_current_breakpoint_info()
            
            viewport_width = info['viewport_width']
            primary_breakpoint = info['primary_breakpoint']
            
            # 根据断点确定预期的Grid列数和容器宽度
            if primary_breakpoint == 'xl':
                expected_columns = 4
                expected_width = "1320px"
                grid_template = "1fr 1fr 1fr 1fr"
            elif primary_breakpoint == 'lg':
                expected_columns = 3
                expected_width = "1000px"
                grid_template = "1fr 1fr 1fr"
            elif primary_breakpoint == 'md':
                expected_columns = 2
                expected_width = "700px" 
                grid_template = "1fr 1fr"
            else:  # xs, sm
                expected_columns = 1
                expected_width = "360-400px"
                grid_template = "1fr"
            
            status_text.value = (
                f"🖥️ 视口: {viewport_width:.0f}px | "
                f"断点: {primary_breakpoint} | "
                f"Grid列数: {expected_columns} | "
                f"容器: {expected_width}"
            )
            
            print(f"📊 动态Grid状态: {status_text.value}")
            print(f"   Grid模板: {grid_template}")
            
        except Exception as e:
            status_text.value = f"错误: {e}"
    
    # 注册响应式回调
    responsive_mgr = get_responsive_manager()
    responsive_mgr.add_style_change_callback(lambda w, bp: update_status())
    update_status()  # 立即更新一次
    
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
    """动态Grid列数调整演示"""
    print("🚀 Starting Dynamic Grid Columns Demo...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Dynamic Grid Columns - Hibiki UI",
        width=1200,  # 大屏幕尺寸，应该显示3列
        height=800
    )
    
    # 创建标题
    title = Label(
        "🔲 动态Grid列数调整演示",
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
    
    # 说明
    description = Label(
        "🎯 固定宽度300px的Grid项目，根据窗口宽度自动调整列数",
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
    
    # 创建状态显示
    status_display = create_status_display()
    
    # 创建8个网格项目用于测试多行显示
    items_data = [
        ("Item A", "#ffebee"),
        ("Item B", "#e8f5e8"), 
        ("Item C", "#e3f2fd"),
        ("Item D", "#fff3e0"),
        ("Item E", "#f3e5f5"),
        ("Item F", "#e0f2f1"),
        ("Item G", "#fce4ec"),
        ("Item H", "#e1f5fe")
    ]
    
    grid_items = []
    for title, bg_color in items_data:
        item = create_grid_item(title, bg_color)
        grid_items.append(item)
    
    print(f"📦 创建了 {len(grid_items)} 个固定宽度(300px)的Grid项目")
    
    # 创建动态Grid容器
    grid_container = create_dynamic_grid_container(grid_items)
    
    # 测试说明
    instructions = Label(
        "🧪 动态列数测试:\n"
        "• 当前1200px → 应显示3列Grid (LG断点)\n"
        "• 调整到800px → 2列Grid (MD断点)\n" 
        "• 调整到500px → 1列Grid (XS/SM断点)\n"
        "• 调整到1400px → 4列Grid (XL断点)\n"
        "\n🎯 每个Grid项目固定宽度300px，列数根据容器宽度自动调整",
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
    
    # 设置窗口内容并触发响应式更新
    window.set_content(main_container)
    
    # 手动触发一次响应式更新
    responsive_mgr = get_responsive_manager()
    responsive_mgr.update_viewport(1200.0, 800.0)
    
    print("✅ Dynamic grid columns demo ready!")
    print("🎯 期望结果: 1200px应显示3列Grid，每列宽度300px")
    print("📏 容器计算: 3列 * 300px + 2*15px(gap) + 40px(padding) = 970px")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()