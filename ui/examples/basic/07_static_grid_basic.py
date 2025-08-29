#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 07: 基础静态CSS Grid布局
验证Grid布局引擎的基本功能，不涉及响应式
"""

from hibiki.ui import (
    Label, Container, ComponentStyle, 
    Display, px,
    ManagerFactory
)


def create_grid_item(title: str, bg_color: str):
    """创建简单的网格项目"""
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
            min_height=px(100)
        )
    )


def test_simple_2x2_grid():
    """测试最简单的2x2网格"""
    
    # 创建4个网格项目
    items = [
        create_grid_item("Item 1", "#ffebee"),
        create_grid_item("Item 2", "#e8f5e8"), 
        create_grid_item("Item 3", "#e3f2fd"),
        create_grid_item("Item 4", "#fff3e0")
    ]
    
    # 2x2网格容器
    grid_container = Container(
        children=items,
        style=ComponentStyle(
            display=Display.GRID,  # 🔥 使用CSS Grid
            grid_template_columns="1fr 1fr",  # 2列，每列相等
            grid_template_rows="auto auto",   # 2行，高度自动
            gap=px(10),
            padding=px(20),
            background_color="#f8f9fa",
            border_color="#007acc",
            border_width=px(3),
            border_radius=px(10),
            margin=px(20)
        )
    )
    
    return Container(
        children=[
            Label(
                "📊 简单 2x2 Grid 布局测试",
                font_size=18,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(margin_bottom=px(10))
            ),
            grid_container
        ],
        style=ComponentStyle(margin=px(20))
    )


def test_fixed_columns_grid():
    """测试固定列数的网格布局"""
    
    # 创建6个项目
    items = []
    colors = ["#ffebee", "#e8f5e8", "#e3f2fd", "#fff3e0", "#f3e5f5", "#e0f2f1"]
    for i, color in enumerate(colors, 1):
        items.append(create_grid_item(f"Grid {i}", color))
    
    # 3列网格，自动换行
    grid_container = Container(
        children=items,
        style=ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr 1fr 1fr",  # 3列相等宽度
            gap=px(15),
            padding=px(20),
            background_color="#f0f8ff",
            border_color="#4169e1",
            border_width=px(3),
            border_radius=px(10),
            margin=px(20)
        )
    )
    
    return Container(
        children=[
            Label(
                "🔢 固定 3列 Grid 布局测试",
                font_size=18,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(margin_bottom=px(10))
            ),
            grid_container
        ],
        style=ComponentStyle(margin=px(20))
    )


def test_mixed_sizes_grid():
    """测试混合尺寸的网格布局"""
    
    # 创建4个项目
    items = [
        create_grid_item("Big Item", "#fce4ec"),
        create_grid_item("Small 1", "#e1f5fe"),
        create_grid_item("Small 2", "#f1f8e9"),
        create_grid_item("Medium", "#fff8e1")
    ]
    
    # 混合尺寸网格：第一列2倍宽，第二列和第三列相等
    grid_container = Container(
        children=items,
        style=ComponentStyle(
            display=Display.GRID,
            grid_template_columns="2fr 1fr 1fr",  # 第一列占2份，其他各占1份
            gap=px(12),
            padding=px(20),
            background_color="#faf2ff",
            border_color="#8e24aa",
            border_width=px(3),
            border_radius=px(10),
            margin=px(20)
        )
    )
    
    return Container(
        children=[
            Label(
                "⚖️ 混合尺寸 Grid 布局测试 (2fr 1fr 1fr)",
                font_size=18,
                font_weight="bold",
                color="#333",
                text_align="center",
                style=ComponentStyle(margin_bottom=px(10))
            ),
            grid_container
        ],
        style=ComponentStyle(margin=px(20))
    )


def main():
    """静态Grid布局测试主程序"""
    print("🚀 Starting Static Grid Layout Tests...")
    
    # 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Static Grid Layout Tests - Hibiki UI",
        width=1000,
        height=800
    )
    
    # 创建页面标题
    main_title = Label(
        "🔲 CSS Grid 静态布局测试",
        font_size=24,
        font_weight="bold",
        color="#333",
        text_align="center",
        style=ComponentStyle(
            margin_bottom=px(20),
            padding=px(20),
            background_color="#f8f9ff",
            border_radius=px(10)
        )
    )
    
    # 创建说明
    description = Label(
        "验证CSS Grid基础功能：固定网格布局，无响应式逻辑",
        font_size=16,
        color="#666",
        text_align="center",
        style=ComponentStyle(
            margin_bottom=px(20),
            padding=px(10),
            background_color="#fff3cd",
            border_radius=px(6)
        )
    )
    
    # 创建三个测试用例
    test_2x2 = test_simple_2x2_grid()
    test_3col = test_fixed_columns_grid()
    test_mixed = test_mixed_sizes_grid()
    
    # 使用说明
    instructions = Label(
        "🧪 测试说明:\n"
        "1. 第一个测试：2x2网格，4个项目应该排列成2行2列\n"
        "2. 第二个测试：3列网格，6个项目应该排列成2行3列\n" 
        "3. 第三个测试：混合尺寸，第一列应该是其他列的2倍宽\n"
        "\n如果看到项目垂直排列成一列，说明Grid布局没有生效",
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
    
    # 主容器 - 使用FlexBox垂直排列各个测试
    main_container = Container(
        children=[
            main_title,
            description,
            test_2x2,
            test_3col,
            test_mixed,
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
    
    print("✅ Static Grid tests ready!")
    print("🎯 期望结果:")
    print("   - 第一个容器: 2x2网格 (4个项目)")
    print("   - 第二个容器: 2x3网格 (6个项目)")  
    print("   - 第三个容器: 混合宽度网格")
    print("   - 如果都显示为单列，说明Grid布局有问题")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()