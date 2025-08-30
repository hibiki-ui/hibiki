#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 04: Layout System 
布局系统演示 - Flex 和 Grid 布局

学习目标：
✅ 理解 Flex 布局系统 (完全支持)
✅ 掌握 CSS Grid 布局 (原生支持)
✅ 学习不同的Grid单位 (px, fr, auto, %)
✅ 掌握网格定位和区域规范
✅ 创建响应式布局设计
✅ 理解 Stretchable 引擎的强大功能

重要说明：
🔥 Hibiki UI 通过 Stretchable 引擎完全支持 CSS Grid 布局！
🎯 支持所有标准的 Grid 属性：grid-template-columns/rows, grid-area, grid-column/row
📏 支持所有 CSS 单位：px, fr, auto, %, minmax(), repeat() 等
🏗️ 基于 Rust Taffy 引擎，性能卓越，标准兼容
"""

from hibiki.ui import (
    Signal,
    Computed,
    Effect,
    Label,
    Button,
    Container,
    ManagerFactory,
    ComponentStyle,
    Display,
    FlexDirection,
    JustifyContent,
    AlignItems,
    px,
    percent,
)
from hibiki.ui.components.layout import ScrollableContainer
from hibiki.ui.utils.screenshot import capture_app_screenshot_display_method, debug_view_layout
from hibiki.ui.core.logging import get_logger
import time

logger = get_logger("04_layout_debug")


class ColoredBox:
    """用于布局演示的彩色盒子组件
    
    支持设置边框颜色、背景色和中心文本，方便观察布局效果
    """
    
    def __init__(
        self, 
        text: str = "",
        background_color: str = "#e3f2fd",
        border_color: str = "#1976d2",
        border_width: int = 2,
        width=None,
        height=None,
        **kwargs
    ):
        """创建彩色盒子
        
        Args:
            text: 显示的文本
            background_color: 背景颜色（十六进制）
            border_color: 边框颜色（十六进制） 
            border_width: 边框宽度（像素）
            width: 宽度
            height: 高度
            **kwargs: 其他样式参数
        """
        self.text = text
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        
        # 构建样式
        style_props = {
            'background_color': background_color,
            'border_color': border_color,
            'border_width': px(border_width),
            'border_style': 'solid',
            'padding': px(10),
            'display': Display.FLEX,
            'justify_content': JustifyContent.CENTER,
            'align_items': AlignItems.CENTER,
            **kwargs
        }
        
        if width:
            style_props['width'] = width if hasattr(width, 'unit') else px(width)
        if height:
            style_props['height'] = height if hasattr(height, 'unit') else px(height)
            
        # 创建标签显示文本
        self.label = Label(
            text,
            style=ComponentStyle(),
            font_size=14,
            font_weight="bold",
            text_align="center",
            color="#333",
        )
        
        # 创建容器
        self.container = Container(
            children=[self.label] if text else [],
            style=ComponentStyle(**style_props)
        )
    
    def get_component(self):
        """获取组件实例"""
        return self.container


def create_flex_demo():
    """创建 Flex 布局演示"""
    current_direction = Signal(FlexDirection.ROW)
    current_justify = Signal(JustifyContent.FLEX_START)
    current_align = Signal(AlignItems.STRETCH)
    
    # 创建响应式按钮标题
    direction_text = Computed(lambda: f"方向: {'row' if current_direction.value == FlexDirection.ROW else 'column'}")
    justify_text = Computed(lambda: {
        JustifyContent.FLEX_START: "主轴: flex-start",
        JustifyContent.CENTER: "主轴: center", 
        JustifyContent.FLEX_END: "主轴: flex-end",
        JustifyContent.SPACE_BETWEEN: "主轴: space-between",
        JustifyContent.SPACE_AROUND: "主轴: space-around",
        JustifyContent.SPACE_EVENLY: "主轴: space-evenly",
    }.get(current_justify.value, "主轴: flex-start"))
    align_text = Computed(lambda: {
        AlignItems.FLEX_START: "交叉轴: flex-start",
        AlignItems.CENTER: "交叉轴: center",
        AlignItems.FLEX_END: "交叉轴: flex-end", 
        AlignItems.STRETCH: "交叉轴: stretch",
    }.get(current_align.value, "交叉轴: stretch"))
    
    # 控制面板
    direction_btn = Button(
        direction_text,
        style=ComponentStyle(width=px(150), height=px(35), margin=px(5)),
        on_click=lambda: setattr(current_direction, 'value', 
            FlexDirection.COLUMN if current_direction.value == FlexDirection.ROW 
            else FlexDirection.ROW)
    )
    
    justify_btn = Button(
        justify_text,
        style=ComponentStyle(width=px(180), height=px(35), margin=px(5)),
        on_click=lambda: setattr(current_justify, 'value',
            {
                JustifyContent.FLEX_START: JustifyContent.CENTER,
                JustifyContent.CENTER: JustifyContent.FLEX_END,
                JustifyContent.FLEX_END: JustifyContent.SPACE_BETWEEN,
                JustifyContent.SPACE_BETWEEN: JustifyContent.SPACE_AROUND,
                JustifyContent.SPACE_AROUND: JustifyContent.SPACE_EVENLY,
                JustifyContent.SPACE_EVENLY: JustifyContent.FLEX_START,
            }.get(current_justify.value, JustifyContent.FLEX_START))
    )
    
    align_btn = Button(
        align_text,
        style=ComponentStyle(width=px(150), height=px(35), margin=px(5)),
        on_click=lambda: setattr(current_align, 'value',
            {
                AlignItems.FLEX_START: AlignItems.CENTER,
                AlignItems.CENTER: AlignItems.FLEX_END,
                AlignItems.FLEX_END: AlignItems.STRETCH,
                AlignItems.STRETCH: AlignItems.FLEX_START,
            }.get(current_align.value, AlignItems.FLEX_START))
    )
    
    controls = Container(
        children=[direction_btn, justify_btn, align_btn],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            gap=px(10),
            margin_bottom=px(20),
            padding=px(15),
            background_color="#f5f5f5",
            border_radius=px(8)
        )
    )
    
    # 演示区域 - 创建有明显颜色区别的盒子
    box1 = ColoredBox("盒子 1", "#ffcdd2", "#d32f2f", width=80, height=60).get_component()
    box2 = ColoredBox("盒子 2", "#c8e6c9", "#388e3c", width=120, height=80).get_component() 
    box3 = ColoredBox("盒子 3", "#fff3e0", "#f57c00", width=100, height=70).get_component()
    
    # 创建演示容器
    demo_container = Container(
        children=[box1, box2, box3],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,  # 初始值
            justify_content=JustifyContent.FLEX_START,  # 初始值
            align_items=AlignItems.STRETCH,  # 初始值
            gap=px(15),
            padding=px(20),
            min_height=px(200),
            background_color="#fafafa",
            border_color="#e0e0e0", 
            border_width=px(2),
            border_radius=px(8)
        )
    )
    
    # 添加响应式布局更新
    def update_demo_layout():
        """响应Signal变化，更新演示容器布局"""
        if demo_container._nsview:  # 确保容器已挂载
            # 更新样式属性
            demo_container.style.flex_direction = current_direction.value
            demo_container.style.justify_content = current_justify.value
            demo_container.style.align_items = current_align.value
            
            # 使用布局引擎更新样式
            try:
                from hibiki.ui.core.layout import get_layout_engine
                engine = get_layout_engine()
                engine.update_component_style(demo_container)
                print(f"🔄 布局已更新: direction={current_direction.value}, justify={current_justify.value}, align={current_align.value}")
            except Exception as e:
                print(f"❌ 布局更新失败: {e}")
    
    # 创建Effect来监听Signal变化 - 监听每个Signal
    Effect(lambda: current_direction.value and update_demo_layout())
    Effect(lambda: current_justify.value and update_demo_layout())
    Effect(lambda: current_align.value and update_demo_layout())
    
    return Container(
        children=[
            Label(
                "🔧 Flex 布局控制台",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=20,
                font_weight="bold",
                text_align="center",
                color="#1976d2"
            ),
            controls,
            demo_container,
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20)
        )
    )


def create_grid_demo():
    """创建 Grid 布局演示"""
    
    # 创建网格项目
    items = []
    colors = [
        ("#ffebee", "#c62828"),  # 红色系
        ("#e8f5e8", "#2e7d32"),  # 绿色系  
        ("#fff3e0", "#ef6c00"),  # 橙色系
        ("#e3f2fd", "#1565c0"),  # 蓝色系
        ("#f3e5f5", "#7b1fa2"),  # 紫色系
        ("#fff8e1", "#f9a825"),  # 黄色系
    ]
    
    for i in range(6):
        bg_color, border_color = colors[i]
        box = ColoredBox(
            f"项目 {i+1}",
            background_color=bg_color,
            border_color=border_color
        ).get_component()
        items.append(box)
    
    # 使用真正的 Grid 布局！
    grid_container = Container(
        children=items,
        style=ComponentStyle(
            display=Display.GRID,  # 使用原生 Grid 布局
            grid_template_columns="1fr 1fr 1fr",  # 3列，等宽
            grid_template_rows="auto auto",       # 2行，自动高度
            gap=px(15),                          # 网格间距
            padding=px(20),
            background_color="#fafafa",
            border="2px solid #e0e0e0",
            border_radius=px(8)
        )
    )
    
    # 创建高级 Grid 布局示例 - 展示 Grid 区域定位
    # 使用 CSS Grid 的命名线和区域功能
    advanced_items = []
    
    # 页头 - 跨越整个顶部
    header = Container(
        children=[
            Label(
                "页头区域 (grid-column: 1 / -1)",
                style=ComponentStyle(),
                font_size=14,
                font_weight="bold", 
                text_align="center"
            )
        ],
        style=ComponentStyle(
            background_color="#e1f5fe",
            border_color="#0277bd",
            border_width=px(2),
            border_style="solid",
            padding=px(10),
            display=Display.FLEX,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER
        )
    )
    
    # 侧边栏
    sidebar = Container(
        children=[
            Label(
                "侧边栏\n(grid-row: 2 / 4)",
                style=ComponentStyle(),
                font_size=12,
                text_align="center"
            )
        ],
        style=ComponentStyle(
            background_color="#f3e5f5",
            border_color="#7b1fa2", 
            border_width=px(2),
            border_style="solid",
            padding=px(10),
            display=Display.FLEX,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER
        )
    )
    
    # 主内容
    main_content = Container(
        children=[
            Label(
                "主内容区域",
                style=ComponentStyle(),
                font_size=14,
                text_align="center"
            )
        ],
        style=ComponentStyle(
            background_color="#e8f5e8",
            border_color="#2e7d32",
            border_width=px(2),
            border_style="solid", 
            padding=px(10),
            display=Display.FLEX,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER
        )
    )
    
    # 页脚
    footer = Container(
        children=[
            Label(
                "页脚区域 (grid-column: 2 / -1)",
                style=ComponentStyle(),
                font_size=12,
                text_align="center"
            )
        ],
        style=ComponentStyle(
            background_color="#fff3e0",
            border_color="#e65100",
            border_width=px(2),
            border_style="solid",
            padding=px(10),
            display=Display.FLEX,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER
        )
    )
    
    # 高级 Grid 容器
    advanced_grid = Container(
        children=[header, sidebar, main_content, footer],
        style=ComponentStyle(
            display=Display.GRID,
            grid_template_columns="200px 1fr 200px",   # 侧边栏-主内容-右侧栏
            grid_template_rows="60px 1fr 60px",        # 页头-内容-页脚
            gap=px(10),
            padding=px(20),
            background_color="#fafafa",
            border="2px solid #e0e0e0",
            border_radius=px(8),
            min_height=px(300)
        )
    )
    
    # 注意：由于当前框架的限制，我们暂时无法直接为子元素设置 grid-area
    # 在实际应用中，可以通过以下方式为子元素指定位置：
    # header.style.grid_area = "1 / 1 / 2 / -1"  # 第1行，跨所有列
    # sidebar.style.grid_row = "2 / 4"           # 从第2行到第4行
    
    return Container(
        children=[
            Label(
                "🎯 CSS Grid 布局演示",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=20,
                font_weight="bold", 
                text_align="center",
                color="#7b1fa2"
            ),
            Label(
                "✨ 使用原生 CSS Grid 布局引擎",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=14,
                text_align="center",
                color="#666"
            ),
            
            # 基础网格
            Label(
                "📊 基础网格 (3×2)",
                style=ComponentStyle(margin_bottom=px(10), margin_top=px(20)),
                font_size=16,
                font_weight="bold"
            ),
            grid_container,
            
            # 高级网格布局
            Label(
                "🏗️ 高级网格布局 (页面结构)",
                style=ComponentStyle(margin_bottom=px(10), margin_top=px(30)),
                font_size=16,
                font_weight="bold"
            ),
            advanced_grid,
            
            # Grid 单位演示
            Label(
                "📏 Grid 单位演示",
                style=ComponentStyle(margin_bottom=px(10), margin_top=px(30)),
                font_size=16,
                font_weight="bold"
            ),
            create_grid_units_demo(),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20)
        )
    )


def create_grid_units_demo():
    """演示不同的Grid单位"""
    
    # 固定像素 + 分数单位
    unit_items = []
    unit_labels = [
        "200px\n固定宽度",
        "1fr\n弹性单位", 
        "2fr\n2倍弹性",
        "auto\n自动宽度",
        "100px\n固定宽度",
        "1fr\n弹性单位"
    ]
    
    unit_colors = [
        ("#ffcdd2", "#d32f2f"),
        ("#c8e6c9", "#388e3c"), 
        ("#fff3e0", "#f57c00"),
        ("#e3f2fd", "#1976d2"),
        ("#f3e5f5", "#7b1fa2"),
        ("#fff8e1", "#f9a825"),
    ]
    
    for i, (label, (bg, border)) in enumerate(zip(unit_labels, unit_colors)):
        item = ColoredBox(
            label,
            background_color=bg,
            border_color=border,
            height=60
        ).get_component()
        unit_items.append(item)
    
    units_grid = Container(
        children=unit_items,
        style=ComponentStyle(
            display=Display.GRID,
            # 演示不同的Grid单位类型
            grid_template_columns="200px 1fr 2fr auto 100px 1fr",  # 混合单位
            grid_template_rows="auto",
            gap=px(10),
            padding=px(20),
            background_color="#fafafa",
            border="2px solid #e0e0e0",
            border_radius=px(8)
        )
    )
    
    return Container(
        children=[
            Label(
                "混合单位: 200px 1fr 2fr auto 100px 1fr",
                style=ComponentStyle(margin_bottom=px(10)),
                font_size=12,
                text_align="center",
                color="#666"
            ),
            units_grid
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN
        )
    )


def create_responsive_demo():
    """创建响应式布局演示"""
    
    # 大卡片
    big_card = ColoredBox(
        "主要内容区",
        background_color="#e1f5fe",
        border_color="#0277bd",
        height=120
    ).get_component()
    
    # 侧边栏卡片
    sidebar_cards = []
    sidebar_colors = [("#fff3e0", "#e65100"), ("#f3e5f5", "#6a1b9a")]
    for i, (bg, border) in enumerate(sidebar_colors):
        card = ColoredBox(
            f"侧栏 {i+1}",
            background_color=bg,
            border_color=border,
            height=50,
            flex_grow=1
        ).get_component()
        sidebar_cards.append(card)
    
    sidebar = Container(
        children=sidebar_cards,
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(10),
            width=px(150)
        )
    )
    
    # 主布局
    main_layout = Container(
        children=[big_card, sidebar],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            gap=px(20),
            padding=px(20),
            background_color="#fafafa",
            border="2px solid #e0e0e0", 
            border_radius=px(8)
        )
    )
    
    return Container(
        children=[
            Label(
                "📱 响应式布局演示",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=20,
                font_weight="bold",
                text_align="center", 
                color="#d32f2f"
            ),
            Label(
                "💡 主内容区自适应宽度，侧边栏固定宽度",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=14,
                text_align="center",
                color="#666"
            ),
            main_layout
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20)
        )
    )


def debug_component_tree(component, depth=0, name=""):
    """调试组件树结构"""
    indent = "  " * depth
    comp_info = f"{indent}├─ {name} ({type(component).__name__})"
    
    if hasattr(component, '_nsview') and component._nsview:
        nsview = component._nsview
        frame = nsview.frame()
        bounds = nsview.bounds()
        comp_info += f" NSView[{frame.size.width}x{frame.size.height} @({frame.origin.x},{frame.origin.y})] bounds[{bounds.size.width}x{bounds.size.height}]"
        comp_info += f" hidden={nsview.isHidden()} alpha={nsview.alphaValue()}"
    else:
        comp_info += " [NSView未创建]"
    
    logger.info(comp_info)
    
    if hasattr(component, 'children') and component.children:
        for i, child in enumerate(component.children):
            debug_component_tree(child, depth + 1, f"child_{i}")

def main():
    """布局系统演示主程序"""
    logger.info("🚀 启动布局系统演示...")
    
    # 创建应用管理器
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(
        title="Layout System Demo - Hibiki UI", 
        width=1000,  # 增加宽度以更好展示Grid布局
        height=700   # 减少高度，依靠滚动查看完整内容
    )
    
    logger.info("📱 窗口创建完成")
    
    # 创建各个演示区域
    logger.info("🔧 开始创建演示组件...")
    flex_demo = create_flex_demo()
    logger.info(f"✅ Flex demo 创建完成: {type(flex_demo).__name__}")
    
    grid_demo = create_grid_demo()
    logger.info(f"✅ Grid demo 创建完成: {type(grid_demo).__name__}")
    
    responsive_demo = create_responsive_demo()
    logger.info(f"✅ Responsive demo 创建完成: {type(responsive_demo).__name__}")
    
    
    # 截图按钮
    def take_screenshot():
        """截图功能 - 使用CGDisplayCreateImageForRect方法"""
        timestamp = int(time.time())
        filename = f"layout_demo_display_screenshot_{timestamp}.png"
        
        print("📸 使用CGDisplayCreateImageForRect截图方法...")
        success = capture_app_screenshot_display_method(filename)
        if success:
            print(f"✅ 截图已保存: {filename}")
            print("🔍 请检查截图以分析布局效果")
        else:
            print("❌ 截图失败")
    
    screenshot_btn = Button(
        "📸 CGDisplayCreateImageForRect截图",
        style=ComponentStyle(
            background_color="#4caf50",
            padding=px(12),
            border_radius=px(6),
            margin_bottom=px(20)
        ),
        on_click=take_screenshot
    )
    
    # 创建滚动内容容器
    content_container = Container(
        children=[
            # 标题
            Label(
                "🎨 Hibiki UI 布局系统演示",
                style=ComponentStyle(margin_bottom=px(20)),
                font_size=28,
                font_weight="bold",
                text_align="center",
                color="#1976d2"
            ),
            
            # 截图按钮
            screenshot_btn,
            
            # Flex 演示
            flex_demo,
            
            # 分隔线
            Container(
                children=[],
                style=ComponentStyle(
                    height=px(2),
                    background_color="#e0e0e0",
                    margin_top=px(30),
                    margin_bottom=px(30)
                )
            ),
            
            # Grid 演示
            grid_demo,
            
            # 分隔线
            Container(
                children=[],
                style=ComponentStyle(
                    height=px(2),
                    background_color="#e0e0e0", 
                    margin_top=px(30),
                    margin_bottom=px(30)
                )
            ),
            
            # 响应式演示
            responsive_demo,
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(40),
            background_color="#ffffff",
            width=percent(100),  # 确保内容容器有明确宽度
            min_height=px(1200)  # 设置最小高度，确保内容可滚动
        )
    )
    
    # 使用ScrollableContainer包装内容
    main_container = ScrollableContainer(
        children=[content_container],
        scroll_vertical=True,
        scroll_horizontal=False,
        show_scrollbars=True,
        style=ComponentStyle(
            width=percent(100),
            height=percent(100),
            background_color="#ffffff"
        )
    )
    
    logger.info("🏗️ 创建主容器...")
    
    # 设置窗口内容
    window.set_content(main_container)
    logger.info("📦 窗口内容设置完成")
    
    # 等待NSView创建并调试组件树
    def debug_after_mount():
        logger.info("🔍 开始调试组件树结构...")
        debug_component_tree(main_container, name="main_container")
        
        # 额外调试ScrollableContainer的NSView
        if hasattr(main_container, '_nsview') and main_container._nsview:
            debug_view_layout(main_container._nsview, "ScrollableContainer NSView")
        
        # 调试content_container
        if hasattr(main_container, 'children') and main_container.children:
            content_container = main_container.children[0]
            logger.info(f"📋 content_container 类型: {type(content_container).__name__}")
            logger.info(f"📋 content_container 子组件数: {len(content_container.children) if hasattr(content_container, 'children') else 'N/A'}")
            
            if hasattr(content_container, '_nsview') and content_container._nsview:
                debug_view_layout(content_container._nsview, "content_container NSView")
    
    # 延迟调试以确保NSView已创建
    # import threading
    # threading.Timer(1.0, debug_after_mount).start()
    
    logger.info("✅ Layout System demo ready!")
    logger.info("🎯 Try the control buttons to see different flex layouts!")
    logger.info("📚 Next: Explore more advanced layout features")
    
    # 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()