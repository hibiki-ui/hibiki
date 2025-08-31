#!/usr/bin/env python3
"""
🎨 Hibiki UI 样式系统综合演示
============================

这是一个完整的样式系统展示面板，全面演示和验证Hibiki UI的样式特性：

📋 演示内容：
1. 基础样式系统 - 长度单位、颜色、Box Model
2. Flexbox布局 - 方向、对齐、弹性伸缩 
3. CSS Grid布局 - 网格模板、定位、高级语法
4. 滚动系统 - ScrollableContainer、NSScrollView集成
5. 响应式设计 - 断点、媒体查询、自适应
6. 动态样式 - Signal绑定、ReactiveBinding
7. 预设样式 - StylePresets、实用组件
8. 性能监控 - 布局性能、内存使用

🎯 教育价值：
- 直观学习每个API的视觉效果
- 实时体验参数调节的影响  
- 理解框架内部实现机制
- 掌握最佳实践和性能优化
"""

import time
from typing import List, Dict, Any, Optional

from hibiki.ui import (
    # 核心组件
    Label, Button, TextField, Container,
    
    # 布局组件  
    ManagerFactory, 
    
    # 样式系统
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems,
    px, percent, auto,
    
    # 响应式系统
    responsive_style, BreakpointName, get_responsive_manager,
    
    # 反应式系统
    Signal, Computed, Effect,
)

# 导入额外的样式函数和枚举
from hibiki.ui.core.styles import vw, vh, Position, ZLayer
from hibiki.ui.core.managers import OverflowBehavior

from hibiki.ui.components.layout import (
    GridContainer, ScrollableContainer, 
    HStack, VStack, SplitView, StackDirection
)

from hibiki.ui import StylePresets
from hibiki.ui.core.logging import get_logger
from hibiki.ui.utils.screenshot import capture_app_screenshot

logger = get_logger("style_demo")


class StyleDemoApp:
    """Hibiki UI 样式系统综合演示应用"""
    
    def __init__(self):
        # 应用状态管理
        self.current_demo = Signal("basic")  # 当前演示区域
        self.demo_data = Signal({})  # 演示数据
        
        # 性能监控
        self.performance_stats = Signal({
            "layout_time": 0.0,
            "component_count": 0,
            "node_count": 0,
            "memory_usage": 0
        })
        
        # 响应式状态
        self.viewport_info = Signal({
            "width": 1200,
            "height": 800, 
            "breakpoint": "lg"
        })
        
        # 动态样式控制
        self.style_controls = Signal({
            "primary_color": "#007acc",
            "border_radius": 8,
            "spacing": 16,
            "animation_speed": 0.3
        })
        
        logger.info("🎨 StyleDemoApp初始化完成")
    
    def create_main_app(self):
        """创建主应用界面"""
        logger.info("🚀 创建样式演示应用...")
        
        # 创建应用管理器
        app_manager = ManagerFactory.get_app_manager()
        window = app_manager.create_window(
            title="Hibiki UI 样式系统综合演示",
            width=1400,
            height=900
        )
        
        # 创建主界面
        main_content = self._create_main_layout()
        
        # 设置窗口内容
        window.set_content(main_content)
        
        # 启动性能监控
        self._start_performance_monitoring()
        
        # 启动响应式监控
        self._start_responsive_monitoring()
        
        logger.info("✅ 样式演示应用创建完成")
        
        # 运行应用
        app_manager.run()
    
    def _create_main_layout(self) -> Container:
        """创建主界面布局"""
        # 左侧导航面板
        nav_panel = self._create_navigation_panel()
        
        # 右侧内容区域
        content_area = self._create_content_area()
        
        # 底部状态栏
        status_bar = self._create_status_bar()
        
        # 使用SplitView创建左右分割布局
        main_split = SplitView(
            primary=nav_panel,
            secondary=content_area,
            orientation=StackDirection.HORIZONTAL,
            split_ratio=0.25,  # 左侧占25%
            resizable=True,
            style=ComponentStyle(
                width=percent(100),
                height=percent(90)  # 为状态栏留出空间
            )
        )
        
        # 主容器：垂直布局
        return VStack(
            children=[main_split, status_bar],
            spacing=0,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                background_color="#f5f5f5"
            )
        )
    
    def _create_navigation_panel(self) -> Container:
        """创建左侧导航面板"""
        # 演示模块列表
        demo_modules = [
            ("basic", "🎨 基础样式", "长度单位、颜色、Box Model"),
            ("flexbox", "📐 Flexbox布局", "方向、对齐、弹性伸缩"),
            ("grid", "🔲 CSS Grid", "网格模板、定位、高级语法"),
            ("scroll", "📜 滚动系统", "ScrollableContainer、NSScrollView"),
            ("responsive", "📱 响应式设计", "断点、媒体查询、自适应"),
            ("reactive", "⚡ 动态样式", "Signal绑定、ReactiveBinding"),
            ("presets", "🎯 预设样式", "StylePresets、实用组件"),
            ("performance", "📊 性能监控", "布局性能、内存使用")
        ]
        
        # 创建导航按钮
        nav_buttons = []
        for module_id, title, description in demo_modules:
            button = self._create_nav_button(module_id, title, description)
            nav_buttons.append(button)
        
        # 导航标题
        nav_title = Label(
            "演示模块",
            font_size=18,
            color="#333333",
            style=ComponentStyle(
                padding=px(16),
                background_color="#ffffff",
                width=percent(100)
            )
        )
        
        # 导航内容容器
        nav_content = VStack(
            children=nav_buttons,
            spacing=4,
            style=ComponentStyle(
                padding=px(12),
                width=percent(100)
            )
        )
        
        # 滚动容器包装导航内容
        nav_scroll = ScrollableContainer(
            children=[nav_content],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                flex_grow=1,
                background_color="#ffffff"
            )
        )
        
        # 导航面板主容器
        return VStack(
            children=[nav_title, nav_scroll],
            spacing=0,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                background_color="#ffffff",
                border="1px solid #e0e0e0"  # 修复：使用通用border
            )
        )
    
    def _create_nav_button(self, module_id: str, title: str, description: str) -> Container:
        """创建导航按钮"""
        def on_click():
            self.current_demo.value = module_id
            logger.info(f"🎯 切换到演示模块: {title}")
        
        # 创建简单的Button组件
        nav_button = Button(
            title,
            on_click=on_click,
            style=ComponentStyle(
                width=percent(100),
                height=px(60),
                padding=px(12),
                background_color="#f8f9fa",  # 简化样式，避免Computed问题
                border_radius=px(6),
                border="2px solid #e9ecef"
            )
        )
        
        # 描述标签
        desc_label = Label(
            description,
            font_size=11,
            color="#666666",
            style=ComponentStyle(
                width=percent(100),
                margin_top=px(4)
            )
        )
        
        # 按钮容器
        button_container = VStack(
            children=[nav_button, desc_label],
            spacing=0,
            style=ComponentStyle(
                width=percent(100),
                margin_bottom=px(4)
            )
        )
        
        return button_container
    
    def _create_content_area(self) -> Container:
        """创建右侧内容区域"""
        # 内容标题栏
        title_bar = self._create_content_title_bar()
        
        # 演示内容区域（动态切换）
        demo_content = Container(
            children=[],  # 内容将根据current_demo动态更新
            style=ComponentStyle(
                width=percent(100),
                flex_grow=1,
                padding=px(20),
                background_color="#ffffff"
            )
        )
        
        # 监听演示模块切换
        def update_demo_content():
            demo_type = self.current_demo.value
            new_content = self._create_demo_content(demo_type)
            
            # 清除旧内容，添加新内容
            demo_content.children.clear()
            demo_content.children.append(new_content)
            
            # 触发重新渲染
            if hasattr(demo_content, '_update_layout'):
                demo_content._update_layout()
        
        Effect(update_demo_content)
        
        # 内容区域主容器
        return VStack(
            children=[title_bar, demo_content],
            spacing=0,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                background_color="#ffffff"
            )
        )
    
    def _create_content_title_bar(self) -> Container:
        """创建内容标题栏"""
        # 当前演示标题
        current_title = Computed(lambda: {
            "basic": "🎨 基础样式系统",
            "flexbox": "📐 Flexbox布局演示", 
            "grid": "🔲 CSS Grid布局",
            "scroll": "📜 滚动系统演示",
            "responsive": "📱 响应式设计",
            "reactive": "⚡ 动态样式绑定",
            "presets": "🎯 预设样式组件",
            "performance": "📊 性能监控面板"
        }.get(self.current_demo.value, "演示面板"))
        
        title_label = Label(
            current_title,
            font_size=20,
            color="#333333",
            style=ComponentStyle(flex_grow=1)
        )
        
        # 截图按钮
        screenshot_btn = Button(
            "📸 截图",
            on_click=self._take_screenshot,
            style=ComponentStyle(
                padding=px(8),
                background_color="#28a745",
                border_radius=px(4)
            )
        )
        
        # 性能信息
        perf_info = Label(
            Computed(lambda: f"组件: {self.performance_stats.value.get('component_count', 0)} | "
                           f"布局: {self.performance_stats.value.get('layout_time', 0):.1f}ms"),
            font_size=11,
            color="#666666"
        )
        
        return HStack(
            children=[title_label, perf_info, screenshot_btn],
            spacing=12,
            style=ComponentStyle(
                width=percent(100),
                padding=px(16),
                background_color="#f8f9fa",
                border="1px solid #e9ecef",
                align_items=AlignItems.CENTER
            )
        )
    
    def _create_status_bar(self) -> Container:
        """创建底部状态栏"""
        # 视口信息
        viewport_info = Label(
            Computed(lambda: f"视口: {self.viewport_info.value['width']}x{self.viewport_info.value['height']} | "
                           f"断点: {self.viewport_info.value['breakpoint']}"),
            font_size=12,
            color="#666666"
        )
        
        # 样式控制信息
        style_info = Label(
            Computed(lambda: f"主题色: {self.style_controls.value['primary_color']} | "
                           f"圆角: {self.style_controls.value['border_radius']}px | "
                           f"间距: {self.style_controls.value['spacing']}px"),
            font_size=12,
            color="#666666"
        )
        
        # Hibiki UI 版本信息
        version_info = Label(
            "Hibiki UI v4.0 - 样式系统演示",
            font_size=12,
            color="#999999"
        )
        
        return HStack(
            children=[viewport_info, style_info, version_info],
            spacing=16,
            style=ComponentStyle(
                width=percent(100),
                padding=px(8),
                background_color="#f8f9fa",
                border="1px solid #e9ecef",
                justify_content=JustifyContent.SPACE_BETWEEN,
                align_items=AlignItems.CENTER
            )
        )
    
    def _create_demo_content(self, demo_type: str) -> Container:
        """根据演示类型创建对应的演示内容"""
        if demo_type == "basic":
            return self._create_basic_style_demo()
        elif demo_type == "flexbox":
            return self._create_flexbox_demo()
        elif demo_type == "grid":
            return self._create_grid_demo()
        elif demo_type == "scroll":
            return self._create_scroll_demo()
        elif demo_type == "responsive":
            return self._create_responsive_demo()
        elif demo_type == "reactive":
            return self._create_reactive_demo()
        elif demo_type == "presets":
            return self._create_presets_demo()
        elif demo_type == "performance":
            return self._create_performance_demo()
        else:
            return self._create_welcome_demo()
    
    def _create_basic_style_demo(self) -> Container:
        """创建基础样式演示"""
        # 长度单位对比区域
        length_units_demo = self._create_length_units_section()
        
        # Box Model演示区域
        box_model_demo = self._create_box_model_section()
        
        # 视觉效果演示区域
        visual_effects_demo = self._create_visual_effects_section()
        
        return VStack(
            children=[
                Label(
                    "基础样式系统演示",
                    font_size=18,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(20))
                ),
                length_units_demo,
                box_model_demo,
                visual_effects_demo
            ],
            spacing=24,
            style=ComponentStyle(
                width=percent(100),
                padding=px(20)
            )
        )
    
    def _create_length_units_section(self) -> Container:
        """创建长度单位演示区域"""
        # 创建不同单位的示例框
        units_examples = [
            (px(100), "px(100)", "#ff6b6b", "像素单位"),
            (percent(50), "percent(50)", "#4ecdc4", "百分比单位"), 
            (vw(10), "vw(10)", "#45b7d1", "视口宽度单位"),
            (vh(15), "vh(15)", "#96ceb4", "视口高度单位"),
            (auto, "auto", "#ffeaa7", "自动尺寸")
        ]
        
        demo_boxes = []
        for width_value, unit_text, bg_color, description in units_examples:
            box = Container(
                children=[
                    Label(
                        unit_text,
                        font_size=14,
                        color="#333333",
                        style=ComponentStyle(margin_bottom=px(4))  # text_align暂时移除
                    ),
                    Label(
                        description,
                        font_size=11,
                        color="#666666",
                        style=ComponentStyle()  # text_align暂时移除
                    )
                ],
                style=ComponentStyle(
                    width=width_value,
                    height=px(80),
                    background_color=bg_color,
                    border_radius=px(8),
                    padding=px(12),
                    border="2px solid #ffffff",
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            demo_boxes.append(box)
        
        return Container(
            children=[
                Label(
                    "📏 长度单位对比",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(12))
                ),
                HStack(
                    children=demo_boxes,
                    spacing=16,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16),
                        background_color="#f8f9fa",
                        border_radius=px(8),
# wrap=True  # 暂时移除，需要框架支持
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_box_model_section(self) -> Container:
        """创建Box Model演示区域"""
        # Box Model可视化示例
        box_model_demo = Container(
            children=[
                Label(
                    "内容区域",
                    font_size=14,
                    color="#333333",
                    style=ComponentStyle(
                        background_color="#e3f2fd"
                    )
                )
            ],
            style=ComponentStyle(
                # Content
                width=px(200),
                height=px(100),
                background_color="#e3f2fd",
                
                # Padding  
                padding=px(20),
                
                # Border
                border="4px solid #2196f3",
                border_radius=px(8),
                
                # Margin
                margin=px(16),
                
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
        
        # Box Model说明
        box_model_explanation = VStack(
            children=[
                Label("Box Model 结构:", font_size=14, color="#333333"),
                Label("• Margin (外边距): 16px", font_size=12, color="#666666"),
                Label("• Border (边框): 4px solid #2196f3", font_size=12, color="#666666"), 
                Label("• Padding (内边距): 20px", font_size=12, color="#666666"),
                Label("• Content (内容): 200x100px", font_size=12, color="#666666")
            ],
            spacing=4,
            style=ComponentStyle(
                padding=px(16),
                background_color="#f5f5f5",
                border_radius=px(8),
                flex_grow=1
            )
        )
        
        return Container(
            children=[
                Label(
                    "📦 Box Model 演示",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(12))
                ),
                HStack(
                    children=[box_model_demo, box_model_explanation],
                    spacing=24,
                    style=ComponentStyle(
                        width=percent(100),
                        align_items=AlignItems.CENTER
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_visual_effects_section(self) -> Container:
        """创建视觉效果演示区域"""
        # 各种视觉效果示例
        effects_examples = [
            ("圆角", px(12), "#ff9ff3", None, None),
            ("半透明", px(8), "#54a0ff", 0.7, None),
            ("渐变边框", px(16), "#5f27cd", None, "3px solid #00d2d3"),
            ("阴影效果", px(8), "#ff6b6b", None, "2px solid #c44569")
        ]
        
        effect_boxes = []
        for title, radius, bg_color, opacity, border in effects_examples:
            style_props = {
                "width": px(120),
                "height": px(80),
                "background_color": bg_color,
                "border_radius": radius,
                "padding": px(12),
                "display": Display.FLEX,
                "justify_content": JustifyContent.CENTER,
                "align_items": AlignItems.CENTER
            }
            
            if opacity:
                style_props["opacity"] = opacity
            if border:
                style_props["border"] = border
            
            box = Container(
                children=[
                    Label(
                        title,
                        font_size=12,
                        color="#ffffff",
                        style=ComponentStyle()  # text_align暂时移除
                    )
                ],
                style=ComponentStyle(**style_props)
            )
            effect_boxes.append(box)
        
        return Container(
            children=[
                Label(
                    "🎨 视觉效果演示",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(12))
                ),
                HStack(
                    children=effect_boxes,
                    spacing=16,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16),
                        background_color="#f8f9fa",
                        border_radius=px(8)
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_welcome_demo(self) -> Container:
        """创建欢迎演示内容"""
        return Container(
            children=[
                Label(
                    "欢迎使用 Hibiki UI 样式系统演示",
                    font_size=24,
                    color="#333333",
                    style=ComponentStyle(
                        margin_bottom=px(20)
                    )
                ),
                Label(
                    "请从左侧导航选择要查看的演示模块",
                    font_size=16,
                    color="#666666",
                    style=ComponentStyle()
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
    
    # TODO: 其他演示区域的实现将在后续步骤中添加
    def _create_flexbox_demo(self) -> Container:
        """创建Flexbox布局演示"""
        # Flex方向演示
        direction_demo = self._create_flex_direction_section()
        
        # 对齐方式演示
        alignment_demo = self._create_flex_alignment_section()
        
        # 弹性伸缩演示
        flex_grow_demo = self._create_flex_grow_section()
        
        # 换行演示
        wrap_demo = self._create_flex_wrap_section()
        
        return ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            "📐 Flexbox布局演示",
                            font_size=18,
                            color="#333333",
                            style=ComponentStyle(margin_bottom=px(20))
                        ),
                        direction_demo,
                        alignment_demo,
                        flex_grow_demo,
                        wrap_demo
                    ],
                    spacing=32,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100)
            )
        )
    
    def _create_grid_demo(self) -> Container:
        """创建CSS Grid布局演示"""
        # Grid基本语法演示
        basic_grid_demo = self._create_basic_grid_section()
        
        # Grid定位演示
        positioning_demo = self._create_grid_positioning_section()
        
        # Grid模板演示
        template_demo = self._create_grid_template_section()
        
        # 响应式Grid演示
        responsive_grid_demo = self._create_responsive_grid_section()
        
        return ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            "🔲 CSS Grid布局演示",
                            font_size=18,
                            color="#333333",
                            style=ComponentStyle(margin_bottom=px(20))
                        ),
                        basic_grid_demo,
                        positioning_demo,
                        template_demo,
                        responsive_grid_demo
                    ],
                    spacing=32,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100)
            )
        )
    
    def _create_scroll_demo(self) -> Container:
        """创建滚动系统演示"""
        # 垂直滚动演示
        vertical_scroll_demo = self._create_vertical_scroll_section()
        
        # 水平滚动演示
        horizontal_scroll_demo = self._create_horizontal_scroll_section()
        
        # 双向滚动演示
        bidirectional_scroll_demo = self._create_bidirectional_scroll_section()
        
        # 嵌套滚动演示
        nested_scroll_demo = self._create_nested_scroll_section()
        
        return ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            "📜 滚动系统演示",
                            font_size=18,
                            color="#333333",
                            style=ComponentStyle(margin_bottom=px(20))
                        ),
                        vertical_scroll_demo,
                        horizontal_scroll_demo,
                        bidirectional_scroll_demo,
                        nested_scroll_demo
                    ],
                    spacing=32,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100)
            )
        )
    
    def _create_vertical_scroll_section(self) -> Container:
        """创建垂直滚动演示区域"""
        # 创建大量内容项目以触发滚动
        scroll_items = []
        for i in range(20):
            item = Container(
                children=[
                    Label(
                        f"垂直滚动项目 {i+1}",
                        font_size=14,
                        color="#333333",
                        style=ComponentStyle(margin_bottom=px(4))
                    ),
                    Label(
                        f"这是第 {i+1} 项的详细描述，展示了ScrollableContainer的垂直滚动能力。"
                        f"当内容高度超过容器高度时，会自动显示滚动条。",
                        font_size=11,
                        color="#666666"
                    )
                ],
                style=ComponentStyle(
                    width=percent(100),
                    padding=px(12),
                    margin_bottom=px(8),
                    background_color="#f8f9fa",
                    border_radius=px(6),
                    border="1px solid #e9ecef"
                )
            )
            scroll_items.append(item)
        
        # 垂直滚动容器
        vertical_scroll = ScrollableContainer(
            children=[
                VStack(
                    children=scroll_items,
                    spacing=4,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            show_scrollbars=True,
            style=ComponentStyle(
                width=px(400),
                height=px(300),
                background_color="#ffffff",
                border_radius=px(8),
                border="2px solid #007acc"
            )
        )
        
        return Container(
            children=[
                Label(
                    "📜 垂直滚动",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("ScrollableContainer 垂直滚动演示:", font_size=14, color="#333333"),
                        vertical_scroll,
                        VStack(
                            children=[
                                Label("特性:", font_size=12, color="#333333"),
                                Label("• scroll_vertical=True", font_size=11, color="#666666"),
                                Label("• scroll_horizontal=False", font_size=11, color="#666666"),
                                Label("• show_scrollbars=True", font_size=11, color="#666666"),
                                Label("• 自动显示NSScrollView原生滚动条", font_size=11, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#f0f8ff",
                                border_radius=px(6),
                                margin_top=px(8)
                            )
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_horizontal_scroll_section(self) -> Container:
        """创建水平滚动演示区域"""
        # 创建宽度很大的内容以触发水平滚动
        horizontal_items = []
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#fd79a8"]
        
        for i in range(12):
            item = Container(
                children=[
                    Label(
                        f"Card {i+1}",
                        font_size=14,
                        color="#ffffff",
                        style=ComponentStyle(margin_bottom=px(8))
                    ),
                    Label(
                        f"项目 {i+1}",
                        font_size=12,
                        color="#ffffff"
                    )
                ],
                style=ComponentStyle(
                    width=px(150),
                    height=px(100),
                    background_color=colors[i % len(colors)],
                    border_radius=px(8),
                    padding=px(12),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER,
                    flex_shrink=0  # 防止收缩
                )
            )
            horizontal_items.append(item)
        
        # 水平滚动容器
        horizontal_scroll = ScrollableContainer(
            children=[
                HStack(
                    children=horizontal_items,
                    spacing=16,
                    style=ComponentStyle(
                        padding=px(16),
                        align_items=AlignItems.CENTER
                    )
                )
            ],
            scroll_vertical=False,
            scroll_horizontal=True,
            show_scrollbars=True,
            style=ComponentStyle(
                width=px(500),
                height=px(140),
                background_color="#ffffff",
                border_radius=px(8),
                border="2px solid #28a745"
            )
        )
        
        return Container(
            children=[
                Label(
                    "↔️ 水平滚动",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("ScrollableContainer 水平滚动演示:", font_size=14, color="#333333"),
                        horizontal_scroll,
                        VStack(
                            children=[
                                Label("特性:", font_size=12, color="#333333"),
                                Label("• scroll_vertical=False", font_size=11, color="#666666"),
                                Label("• scroll_horizontal=True", font_size=11, color="#666666"),
                                Label("• 内容宽度超过容器时自动滚动", font_size=11, color="#666666"),
                                Label("• flex_shrink=0 防止项目被压缩", font_size=11, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#f0fff4",
                                border_radius=px(6),
                                margin_top=px(8)
                            )
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_bidirectional_scroll_section(self) -> Container:
        """创建双向滚动演示区域"""
        # 创建一个大的Grid，既有垂直也有水平溢出
        bidirectional_items = []
        for i in range(30):
            item = Container(
                children=[
                    Label(f"Cell {i+1}", font_size=12, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(120),
                    height=px(80),
                    background_color="#6c5ce7",
                    border_radius=px(6),
                    padding=px(8),
                    margin=px(4),
                    display=Display.FLEX,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            bidirectional_items.append(item)
        
        # 使用GridContainer创建大网格
        large_grid = GridContainer(
            children=bidirectional_items,
            columns="repeat(6, 120px)",  # 6列固定宽度
            gap=8,
            style=ComponentStyle(
                padding=px(16),
                background_color="#f8f9fa"
            )
        )
        
        # 双向滚动容器
        bidirectional_scroll = ScrollableContainer(
            children=[large_grid],
            scroll_vertical=True,
            scroll_horizontal=True,
            show_scrollbars=True,
            style=ComponentStyle(
                width=px(450),
                height=px(300),
                background_color="#ffffff",
                border_radius=px(8),
                border="2px solid #e17055"
            )
        )
        
        return Container(
            children=[
                Label(
                    "🔄 双向滚动",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("ScrollableContainer 双向滚动演示:", font_size=14, color="#333333"),
                        bidirectional_scroll,
                        VStack(
                            children=[
                                Label("特性:", font_size=12, color="#333333"),
                                Label("• scroll_vertical=True", font_size=11, color="#666666"),
                                Label("• scroll_horizontal=True", font_size=11, color="#666666"),
                                Label("• 支持同时垂直和水平滚动", font_size=11, color="#666666"),
                                Label("• 适用于大表格和复杂布局", font_size=11, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#fff5f5",
                                border_radius=px(6),
                                margin_top=px(8)
                            )
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_nested_scroll_section(self) -> Container:
        """创建嵌套滚动演示区域"""
        # 创建内层垂直滚动内容
        inner_items = []
        for i in range(10):
            item = Label(
                f"内层项目 {i+1}: 这是嵌套滚动区域中的内容项目。",
                font_size=12,
                color="#333333",
                style=ComponentStyle(
                    width=percent(100),
                    padding=px(8),
                    margin_bottom=px(4),
                    background_color="#e3f2fd",
                    border_radius=px(4)
                )
            )
            inner_items.append(item)
        
        # 内层滚动容器
        inner_scroll = ScrollableContainer(
            children=[
                VStack(
                    children=inner_items,
                    spacing=4,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(8)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            show_scrollbars=True,
            style=ComponentStyle(
                width=px(250),
                height=px(150),
                background_color="#ffffff",
                border_radius=px(6),
                border="1px solid #2196f3"
            )
        )
        
        # 创建外层内容，包含多个内层滚动区域
        outer_items = []
        for i in range(3):
            section = Container(
                children=[
                    Label(f"嵌套区域 {i+1}", font_size=14, color="#333333", 
                          style=ComponentStyle(margin_bottom=px(8))),
                    inner_scroll,  # 每个区域都包含一个滚动区域
                    Label("这展示了ScrollableContainer的嵌套能力", font_size=11, color="#666666",
                          style=ComponentStyle(margin_top=px(8)))
                ],
                style=ComponentStyle(
                    width=percent(100),
                    padding=px(16),
                    margin_bottom=px(16),
                    background_color="#f5f5f5",
                    border_radius=px(8),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    align_items=AlignItems.CENTER
                )
            )
            outer_items.append(section)
        
        # 外层滚动容器
        outer_scroll = ScrollableContainer(
            children=[
                VStack(
                    children=outer_items,
                    spacing=0,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            show_scrollbars=True,
            style=ComponentStyle(
                width=px(400),
                height=px(400),
                background_color="#ffffff",
                border_radius=px(8),
                border="2px solid #9c27b0"
            )
        )
        
        return Container(
            children=[
                Label(
                    "📚 嵌套滚动",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("ScrollableContainer 嵌套滚动演示:", font_size=14, color="#333333"),
                        outer_scroll,
                        VStack(
                            children=[
                                Label("嵌套滚动特性:", font_size=12, color="#333333"),
                                Label("• 外层容器：垂直滚动多个区域", font_size=11, color="#666666"),
                                Label("• 内层容器：独立的垂直滚动", font_size=11, color="#666666"),
                                Label("• ScrollManager自动处理滚动冲突", font_size=11, color="#666666"),
                                Label("• NSScrollView原生嵌套支持", font_size=11, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#faf5ff",
                                border_radius=px(6),
                                margin_top=px(8)
                            )
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )

    def _create_responsive_demo(self) -> Container:
        """创建响应式设计演示"""
        # 断点演示
        breakpoint_demo = self._create_breakpoint_section()
        
        # 响应式Grid演示
        responsive_grid_demo = self._create_responsive_grid_live_section()
        
        # 媒体查询演示
        media_query_demo = self._create_media_query_section()
        
        # 视口单位演示
        viewport_units_demo = self._create_viewport_units_section()
        
        return ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            "📱 响应式设计演示",
                            font_size=18,
                            color="#333333",
                            style=ComponentStyle(margin_bottom=px(20))
                        ),
                        breakpoint_demo,
                        responsive_grid_demo,
                        media_query_demo,
                        viewport_units_demo
                    ],
                    spacing=32,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100)
            )
        )
    
    def _create_breakpoint_section(self) -> Container:
        """创建断点演示区域"""
        # 展示不同断点的信息
        breakpoint_info = [
            ("XS", "≤ 576px", "超小屏幕", "#e53e3e"),
            ("SM", "577px - 768px", "小屏幕", "#dd6b20"),
            ("MD", "769px - 992px", "中等屏幕", "#38a169"),
            ("LG", "993px - 1200px", "大屏幕", "#3182ce"),
            ("XL", "> 1200px", "超大屏幕", "#805ad5")
        ]
        
        breakpoint_cards = []
        for name, range_text, desc, color in breakpoint_info:
            card = Container(
                children=[
                    Label(name, font_size=18, color="#ffffff", 
                          style=ComponentStyle(margin_bottom=px(8))),
                    Label(range_text, font_size=14, color="#ffffff",
                          style=ComponentStyle(margin_bottom=px(4))),
                    Label(desc, font_size=12, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(140),
                    height=px(120),
                    background_color=color,
                    border_radius=px(8),
                    padding=px(16),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            breakpoint_cards.append(card)
        
        # 当前断点指示器
        current_breakpoint_display = Container(
            children=[
                Label(
                    Computed(lambda: f"当前断点: {self.viewport_info.value.get('breakpoint', 'unknown').upper()}"),
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(8))
                ),
                Label(
                    Computed(lambda: f"视口宽度: {self.viewport_info.value.get('width', 0)}px"),
                    font_size=14,
                    color="#666666"
                )
            ],
            style=ComponentStyle(
                padding=px(16),
                background_color="#f0f8ff",
                border_radius=px(8),
                border="2px solid #3182ce",
                margin_bottom=px(16)
            )
        )
        
        return Container(
            children=[
                Label(
                    "📊 BreakpointManager 断点系统",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                current_breakpoint_display,
                HStack(
                    children=breakpoint_cards,
                    spacing=12,
                    style=ComponentStyle(
                        width=percent(100),
                        justify_content=JustifyContent.CENTER,
                        margin_bottom=px(16)
                    )
                ),
                VStack(
                    children=[
                        Label("BreakpointManager 特性:", font_size=14, color="#333333"),
                        Label("• 自动检测视口尺寸变化", font_size=11, color="#666666"),
                        Label("• 实时更新当前断点状态", font_size=11, color="#666666"),
                        Label("• 支持自定义断点配置", font_size=11, color="#666666"),
                        Label("• 与ResponsiveStyle无缝集成", font_size=11, color="#666666")
                    ],
                    spacing=4,
                    style=ComponentStyle(
                        padding=px(16),
                        background_color="#f8f9fa",
                        border_radius=px(8)
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_responsive_grid_live_section(self) -> Container:
        """创建实时响应式Grid演示区域"""
        # 创建响应式内容项目
        responsive_items = self._create_grid_items(12)
        
        # 创建响应式Grid - 根据断点自动调整列数
        responsive_grid_style = (
            responsive_style(
                ComponentStyle(
                    width=percent(100),
                    padding=px(16),
                    background_color="#f8f9fa",
                    border_radius=px(8),
                    border="2px dashed #007acc"
                )
            )
            .at_breakpoint(BreakpointName.XS, ComponentStyle(
                # 超小屏：1列
                display=Display.GRID,
                grid_template_columns="1fr",
                gap=px(8)
            ))
            .at_breakpoint(BreakpointName.SM, ComponentStyle(
                # 小屏：2列
                display=Display.GRID,
                grid_template_columns="1fr 1fr",
                gap=px(12)
            ))
            .at_breakpoint(BreakpointName.MD, ComponentStyle(
                # 中屏：3列
                display=Display.GRID,
                grid_template_columns="1fr 1fr 1fr",
                gap=px(16)
            ))
            .at_breakpoint(BreakpointName.LG, ComponentStyle(
                # 大屏：4列
                display=Display.GRID,
                grid_template_columns="1fr 1fr 1fr 1fr",
                gap=px(20)
            ))
        )
        
        # 响应式Grid容器
        responsive_grid = Container(
            children=responsive_items,
            responsive_style=responsive_grid_style
        )
        
        # 注册到响应式管理器
        try:
            responsive_mgr = get_responsive_manager()
            responsive_mgr.register_component(responsive_grid)
        except Exception as e:
            logger.warning(f"响应式组件注册失败: {e}")
        
        return Container(
            children=[
                Label(
                    "🔄 实时响应式Grid",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("根据当前断点自动调整布局的Grid:", font_size=14, color="#333333"),
                        responsive_grid,
                        VStack(
                            children=[
                                Label("响应式规则:", font_size=12, color="#333333"),
                                Label("• XS (≤576px): 1列布局", font_size=11, color="#666666"),
                                Label("• SM (577-768px): 2列布局", font_size=11, color="#666666"),
                                Label("• MD (769-992px): 3列布局", font_size=11, color="#666666"),
                                Label("• LG (≥993px): 4列布局", font_size=11, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#e6f3ff",
                                border_radius=px(6),
                                margin_top=px(16)
                            )
                        )
                    ],
                    spacing=16,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_media_query_section(self) -> Container:
        """创建媒体查询演示区域"""
        # 媒体查询样式示例
        media_query_examples = [
            ("手机优先", "从小屏向大屏适配"),
            ("桌面优先", "从大屏向小屏适配"),
            ("范围查询", "特定尺寸范围样式"),
            ("方向查询", "横屏/竖屏适配")
        ]
        
        example_cards = []
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"]
        
        for i, (title, desc) in enumerate(media_query_examples):
            card = Container(
                children=[
                    Label(title, font_size=14, color="#ffffff",
                          style=ComponentStyle(margin_bottom=px(8))),
                    Label(desc, font_size=11, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(160),
                    height=px(100),
                    background_color=colors[i % len(colors)],
                    border_radius=px(8),
                    padding=px(12),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            example_cards.append(card)
        
        # 媒体查询代码示例
        code_example = Container(
            children=[
                Label("ResponsiveStyle 使用示例:", font_size=12, color="#333333",
                      style=ComponentStyle(margin_bottom=px(8))),
                Label(
                    "responsive_style(base_style)\n"
                    "  .at_breakpoint(BreakpointName.SM, sm_style)\n"
                    "  .at_breakpoint(BreakpointName.MD, md_style)",
                    font_size=10,
                    color="#2d3748",
                    style=ComponentStyle(
                        font_family="Monaco, Consolas, monospace"
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(16),
                background_color="#f7fafc",
                border_radius=px(6),
                border="1px solid #e2e8f0"
            )
        )
        
        return Container(
            children=[
                Label(
                    "📐 媒体查询与响应式样式",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("ResponsiveStyle 媒体查询模式:", font_size=14, color="#333333"),
                        HStack(
                            children=example_cards,
                            spacing=12,
                            style=ComponentStyle(
                                justify_content=JustifyContent.CENTER,
                                margin=px(16)
                            )
                        ),
                        code_example
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_viewport_units_section(self) -> Container:
        """创建视口单位演示区域"""
        # 不同视口单位的演示框
        viewport_examples = [
            (vw(20), "vw(20)", "视口宽度20%", "#ff6b6b"),
            (vh(15), "vh(15)", "视口高度15%", "#4ecdc4"),
            (vw(10), "vw(10)", "视口宽度10%", "#45b7d1"),
            (px(100), "px(100)", "固定像素对比", "#96ceb4")
        ]
        
        viewport_boxes = []
        for width_value, unit_text, description, bg_color in viewport_examples:
            box = Container(
                children=[
                    Label(unit_text, font_size=14, color="#ffffff",
                          style=ComponentStyle(margin_bottom=px(4))),
                    Label(description, font_size=11, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=width_value,
                    height=vh(12),  # 使用视口高度
                    background_color=bg_color,
                    border_radius=px(8),
                    padding=px(12),
                    border="2px solid #ffffff",
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER,
                    margin=px(8)
                )
            )
            viewport_boxes.append(box)
        
        # 视口信息显示
        viewport_info_display = Container(
            children=[
                Label(
                    Computed(lambda: f"当前视口: {self.viewport_info.value.get('width', 0)}x{self.viewport_info.value.get('height', 0)}"),
                    font_size=14,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(4))
                ),
                Label(
                    "vw/vh单位会根据视口尺寸自动计算",
                    font_size=12,
                    color="#666666"
                )
            ],
            style=ComponentStyle(
                padding=px(12),
                background_color="#fff5f5",
                border_radius=px(6),
                border="1px solid #fed7d7",
                margin_bottom=px(16)
            )
        )
        
        return Container(
            children=[
                Label(
                    "📏 视口单位 (vw/vh)",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        viewport_info_display,
                        Container(
                            children=viewport_boxes,
                            style=ComponentStyle(
                                width=percent(100),
                                padding=px(16),
                                background_color="#f8f9fa",
                                border_radius=px(8),
                                display=Display.FLEX,
                                flex_direction=FlexDirection.ROW,
                                justify_content=JustifyContent.CENTER,
                                align_items=AlignItems.CENTER,
                                gap=px(8)
                            )
                        ),
                        VStack(
                            children=[
                                Label("视口单位特性:", font_size=12, color="#333333"),
                                Label("• vw: 视口宽度的百分比 (1vw = 1% viewport width)", font_size=10, color="#666666"),
                                Label("• vh: 视口高度的百分比 (1vh = 1% viewport height)", font_size=10, color="#666666"),
                                Label("• 响应式设计的利器，自动适应屏幕尺寸", font_size=10, color="#666666"),
                                Label("• ViewportManager实时监控尺寸变化", font_size=10, color="#666666")
                            ],
                            spacing=4,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#f0f8ff",
                                border_radius=px(6),
                                margin_top=px(16)
                            )
                        )
                    ],
                    spacing=16,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )

    def _create_reactive_demo(self) -> Container:
        """创建动态样式和Signal绑定演示"""
        # Signal基础演示
        signal_basics_demo = self._create_signal_basics_section()
        
        # Computed值演示
        computed_demo = self._create_computed_section()
        
        # Effect副作用演示
        effect_demo = self._create_effect_section()
        
        # 动态样式绑定演示
        dynamic_styles_demo = self._create_dynamic_styles_section()
        
        return ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            "⚡ 动态样式和Signal绑定演示",
                            font_size=18,
                            color="#333333",
                            style=ComponentStyle(margin_bottom=px(20))
                        ),
                        signal_basics_demo,
                        computed_demo,
                        effect_demo,
                        dynamic_styles_demo
                    ],
                    spacing=32,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100)
            )
        )
    
    def _create_signal_basics_section(self) -> Container:
        """创建Signal基础演示区域"""
        # 创建演示用的Signal
        demo_counter = Signal(0)
        demo_text = Signal("Hello Hibiki UI!")
        demo_enabled = Signal(True)
        
        # 计数器控制按钮
        increment_btn = Button(
            "增加计数",
            on_click=lambda: setattr(demo_counter, 'value', demo_counter.value + 1),
            style=ComponentStyle(
                background_color="#007acc",
                border_radius=px(6),
                padding=px(8),
                margin=px(4)
            )
        )
        
        decrement_btn = Button(
            "减少计数", 
            on_click=lambda: setattr(demo_counter, 'value', demo_counter.value - 1),
            style=ComponentStyle(
                background_color="#dc3545",
                border_radius=px(6),
                padding=px(8),
                margin=px(4)
            )
        )
        
        reset_btn = Button(
            "重置",
            on_click=lambda: setattr(demo_counter, 'value', 0),
            style=ComponentStyle(
                background_color="#28a745",
                border_radius=px(6),
                padding=px(8),
                margin=px(4)
            )
        )
        
        # 动态显示计数器值
        counter_display = Container(
            children=[
                Label(
                    Computed(lambda: f"计数器值: {demo_counter.value}"),
                    font_size=18,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(8))
                ),
                Label(
                    Computed(lambda: f"计数器状态: {'偶数' if demo_counter.value % 2 == 0 else '奇数'}"),
                    font_size=14,
                    color=Computed(lambda: "#007acc" if demo_counter.value % 2 == 0 else "#dc3545")
                )
            ],
            style=ComponentStyle(
                padding=px(16),
                background_color=Computed(lambda: "#e6f3ff" if demo_counter.value >= 0 else "#ffe6e6"),
                border_radius=px(8),
                border=Computed(lambda: "2px solid " + ("#007acc" if demo_counter.value >= 0 else "#dc3545")),
                margin_bottom=px(16)
            )
        )
        
        # 文本输入演示
        text_input = TextField(
            placeholder="输入文本...",
            value=demo_text,
            style=ComponentStyle(
                width=px(300),
                padding=px(8),
                border="1px solid #ccc",
                border_radius=px(4),
                margin_bottom=px(8)
            )
        )
        
        text_display = Label(
            Computed(lambda: f"输入的文本: {demo_text.value}"),
            font_size=14,
            color="#333333"
        )
        
        return Container(
            children=[
                Label(
                    "🔄 Signal 基础演示",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                
                # 计数器演示
                VStack(
                    children=[
                        Label("Signal 响应式计数器:", font_size=14, color="#333333"),
                        counter_display,
                        HStack(
                            children=[increment_btn, decrement_btn, reset_btn],
                            spacing=8,
                            style=ComponentStyle(justify_content=JustifyContent.CENTER)
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(
                        width=percent(100),
                        margin_bottom=px(24)
                    )
                ),
                
                # 文本输入演示
                VStack(
                    children=[
                        Label("Signal 文本绑定:", font_size=14, color="#333333"),
                        text_input,
                        text_display
                    ],
                    spacing=8,
                    style=ComponentStyle(
                        width=percent(100),
                        align_items=AlignItems.CENTER
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_computed_section(self) -> Container:
        """创建Computed演示区域"""
        # 创建基础Signal
        base_value = Signal(10)
        
        # 各种Computed值
        doubled = Computed(lambda: base_value.value * 2)
        squared = Computed(lambda: base_value.value ** 2)
        is_even = Computed(lambda: base_value.value % 2 == 0)
        description = Computed(lambda: f"数字 {base_value.value} 是{'偶数' if is_even.value else '奇数'}，"
                                    f"平方是 {squared.value}，双倍是 {doubled.value}")
        
        # 控制按钮
        controls = HStack(
            children=[
                Button(
                    "+1",
                    on_click=lambda: setattr(base_value, 'value', base_value.value + 1),
                    style=ComponentStyle(
                        background_color="#007acc",
                        border_radius=px(4),
                        padding=px(6)
                    )
                ),
                Button(
                    "+5",
                    on_click=lambda: setattr(base_value, 'value', base_value.value + 5),
                    style=ComponentStyle(
                        background_color="#28a745",
                        border_radius=px(4),
                        padding=px(6)
                    )
                ),
                Button(
                    "×2",
                    on_click=lambda: setattr(base_value, 'value', base_value.value * 2),
                    style=ComponentStyle(
                        background_color="#fd7e14",
                        border_radius=px(4),
                        padding=px(6)
                    )
                ),
                Button(
                    "重置",
                    on_click=lambda: setattr(base_value, 'value', 10),
                    style=ComponentStyle(
                        background_color="#6c757d",
                        border_radius=px(4),
                        padding=px(6)
                    )
                )
            ],
            spacing=8,
            style=ComponentStyle(justify_content=JustifyContent.CENTER)
        )
        
        # 计算结果显示
        results_grid = GridContainer(
            children=[
                # 基础值
                Container(
                    children=[
                        Label("基础值", font_size=12, color="#666666"),
                        Label(
                            Computed(lambda: str(base_value.value)),
                            font_size=20,
                            color="#333333"
                        )
                    ],
                    style=ComponentStyle(
                        padding=px(16),
                        background_color="#f8f9fa",
                        border_radius=px(6),
                        display=Display.FLEX,
                        flex_direction=FlexDirection.COLUMN,
                        align_items=AlignItems.CENTER
                    )
                ),
                
                # 双倍值
                Container(
                    children=[
                        Label("双倍", font_size=12, color="#666666"),
                        Label(
                            Computed(lambda: str(doubled.value)),
                            font_size=20,
                            color="#007acc"
                        )
                    ],
                    style=ComponentStyle(
                        padding=px(16),
                        background_color="#e6f3ff",
                        border_radius=px(6),
                        display=Display.FLEX,
                        flex_direction=FlexDirection.COLUMN,
                        align_items=AlignItems.CENTER
                    )
                ),
                
                # 平方值
                Container(
                    children=[
                        Label("平方", font_size=12, color="#666666"),
                        Label(
                            Computed(lambda: str(squared.value)),
                            font_size=20,
                            color="#28a745"
                        )
                    ],
                    style=ComponentStyle(
                        padding=px(16),
                        background_color="#e6ffe6",
                        border_radius=px(6),
                        display=Display.FLEX,
                        flex_direction=FlexDirection.COLUMN,
                        align_items=AlignItems.CENTER
                    )
                ),
                
                # 奇偶性
                Container(
                    children=[
                        Label("奇偶性", font_size=12, color="#666666"),
                        Label(
                            Computed(lambda: "偶数" if is_even.value else "奇数"),
                            font_size=20,
                            color=Computed(lambda: "#6f42c1" if is_even.value else "#dc3545")
                        )
                    ],
                    style=ComponentStyle(
                        padding=px(16),
                        background_color=Computed(lambda: "#f3e6ff" if is_even.value else "#ffe6e6"),
                        border_radius=px(6),
                        display=Display.FLEX,
                        flex_direction=FlexDirection.COLUMN,
                        align_items=AlignItems.CENTER
                    )
                )
            ],
            columns="1fr 1fr 1fr 1fr",
            gap=16,
            style=ComponentStyle(
                width=percent(100),
                margin_bottom=px(16)
            )
        )
        
        # 描述文本
        description_display = Container(
            children=[
                Label(
                    description,
                    font_size=14,
                    color="#333333"
                )
            ],
            style=ComponentStyle(
                padding=px(12),
                background_color="#f8f9fa",
                border_radius=px(6),
                border="1px solid #e9ecef"
            )
        )
        
        return Container(
            children=[
                Label(
                    "🧮 Computed 值演示",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("Computed自动计算和缓存衍生值:", font_size=14, color="#333333"),
                        controls,
                        results_grid,
                        description_display,
                        VStack(
                            children=[
                                Label("Computed 特性:", font_size=12, color="#333333"),
                                Label("• 自动追踪Signal依赖", font_size=10, color="#666666"),
                                Label("• 智能缓存，仅在依赖变化时重算", font_size=10, color="#666666"),
                                Label("• 支持复杂的计算链", font_size=10, color="#666666"),
                                Label("• 版本控制系统优化性能", font_size=10, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#fff5f5",
                                border_radius=px(6),
                                margin_top=px(12)
                            )
                        )
                    ],
                    spacing=16,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_effect_section(self) -> Container:
        """创建Effect演示区域"""
        # 演示用Signal
        effect_counter = Signal(0)
        log_messages = Signal([])
        auto_increment = Signal(False)
        
        # Effect: 记录计数器变化
        Effect(lambda: log_messages.value.append(f"计数器变更为: {effect_counter.value}") if effect_counter.value > 0 else None)
        
        # Effect: 自动增长
        def auto_increment_effect():
            if auto_increment.value:
                # 这里应该使用定时器，但为了简化演示，我们使用按钮触发
                pass
        Effect(auto_increment_effect)
        
        # 控制按钮
        effect_controls = HStack(
            children=[
                Button(
                    "增加",
                    on_click=lambda: setattr(effect_counter, 'value', effect_counter.value + 1),
                    style=ComponentStyle(
                        background_color="#007acc",
                        border_radius=px(4),
                        padding=px(8)
                    )
                ),
                Button(
                    "清空日志",
                    on_click=lambda: setattr(log_messages, 'value', []),
                    style=ComponentStyle(
                        background_color="#dc3545",
                        border_radius=px(4),
                        padding=px(8)
                    )
                ),
                Button(
                    Computed(lambda: "停止自动" if auto_increment.value else "开始自动"),
                    on_click=lambda: setattr(auto_increment, 'value', not auto_increment.value),
                    style=ComponentStyle(
                        background_color=Computed(lambda: "#fd7e14" if auto_increment.value else "#28a745"),
                        border_radius=px(4),
                        padding=px(8)
                    )
                )
            ],
            spacing=8,
            style=ComponentStyle(justify_content=JustifyContent.CENTER)
        )
        
        # 当前状态显示
        status_display = Container(
            children=[
                Label(
                    Computed(lambda: f"当前计数: {effect_counter.value}"),
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(8))
                ),
                Label(
                    Computed(lambda: f"自动模式: {'开启' if auto_increment.value else '关闭'}"),
                    font_size=14,
                    color=Computed(lambda: "#28a745" if auto_increment.value else "#6c757d")
                ),
                Label(
                    Computed(lambda: f"日志条数: {len(log_messages.value)}"),
                    font_size=14,
                    color="#666666"
                )
            ],
            style=ComponentStyle(
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="1px solid #e9ecef",
                margin_bottom=px(16)
            )
        )
        
        # 日志显示区域
        log_display = ScrollableContainer(
            children=[
                VStack(
                    children=[
                        Label(
                            Computed(lambda: "\n".join(log_messages.value[-10:]) if log_messages.value else "暂无日志"),
                            font_size=12,
                            color="#333333",
                            style=ComponentStyle(
                                font_family="Monaco, Consolas, monospace"
                            )
                        )
                    ],
                    spacing=4,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(12)
                    )
                )
            ],
            scroll_vertical=True,
            scroll_horizontal=False,
            style=ComponentStyle(
                width=percent(100),
                height=px(150),
                background_color="#f8f9fa",
                border_radius=px(6),
                border="1px solid #e9ecef"
            )
        )
        
        return Container(
            children=[
                Label(
                    "⚡ Effect 副作用演示",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("Effect自动响应Signal变化执行副作用:", font_size=14, color="#333333"),
                        status_display,
                        effect_controls,
                        Label("操作日志:", font_size=12, color="#333333", 
                              style=ComponentStyle(margin_top=px(16), margin_bottom=px(8))),
                        log_display,
                        VStack(
                            children=[
                                Label("Effect 特性:", font_size=12, color="#333333"),
                                Label("• 自动追踪Signal依赖", font_size=10, color="#666666"),
                                Label("• 依赖变化时自动执行", font_size=10, color="#666666"),
                                Label("• 组件卸载时自动清理", font_size=10, color="#666666"),
                                Label("• 批处理优化减少重复执行", font_size=10, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#e6f3ff",
                                border_radius=px(6),
                                margin_top=px(12)
                            )
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_dynamic_styles_section(self) -> Container:
        """创建动态样式绑定演示区域"""
        # 动态样式控制Signal
        bg_hue = Signal(200)  # 色相值 0-360
        border_radius = Signal(8)  # 圆角大小
        padding_size = Signal(16)  # 内边距
        is_animated = Signal(False)  # 是否开启动画
        
        # 动态颜色计算
        dynamic_bg_color = Computed(lambda: f"hsl({bg_hue.value}, 70%, 85%)")
        dynamic_border_color = Computed(lambda: f"hsl({bg_hue.value}, 80%, 60%)")
        dynamic_text_color = Computed(lambda: f"hsl({bg_hue.value}, 90%, 30%)")
        
        # 控制滑块/按钮
        color_controls = VStack(
            children=[
                Label("颜色控制:", font_size=12, color="#333333"),
                HStack(
                    children=[
                        Button("红", on_click=lambda: setattr(bg_hue, 'value', 0),
                               style=ComponentStyle(background_color="#ff6b6b", padding=px(6))),
                        Button("橙", on_click=lambda: setattr(bg_hue, 'value', 30),
                               style=ComponentStyle(background_color="#ff9f43", padding=px(6))),
                        Button("绿", on_click=lambda: setattr(bg_hue, 'value', 120),
                               style=ComponentStyle(background_color="#00d2d3", padding=px(6))),
                        Button("蓝", on_click=lambda: setattr(bg_hue, 'value', 200),
                               style=ComponentStyle(background_color="#54a0ff", padding=px(6))),
                        Button("紫", on_click=lambda: setattr(bg_hue, 'value', 280),
                               style=ComponentStyle(background_color="#5f27cd", padding=px(6)))
                    ],
                    spacing=4
                )
            ],
            spacing=8,
            style=ComponentStyle(align_items=AlignItems.CENTER)
        )
        
        geometry_controls = VStack(
            children=[
                Label("几何控制:", font_size=12, color="#333333"),
                HStack(
                    children=[
                        Button("小圆角", on_click=lambda: setattr(border_radius, 'value', 4),
                               style=ComponentStyle(padding=px(6))),
                        Button("中圆角", on_click=lambda: setattr(border_radius, 'value', 12),
                               style=ComponentStyle(padding=px(6))),
                        Button("大圆角", on_click=lambda: setattr(border_radius, 'value', 24),
                               style=ComponentStyle(padding=px(6))),
                        Button("超大圆角", on_click=lambda: setattr(border_radius, 'value', 40),
                               style=ComponentStyle(padding=px(6)))
                    ],
                    spacing=4
                ),
                HStack(
                    children=[
                        Button("小间距", on_click=lambda: setattr(padding_size, 'value', 8),
                               style=ComponentStyle(padding=px(6))),
                        Button("中间距", on_click=lambda: setattr(padding_size, 'value', 16),
                               style=ComponentStyle(padding=px(6))),
                        Button("大间距", on_click=lambda: setattr(padding_size, 'value', 32),
                               style=ComponentStyle(padding=px(6)))
                    ],
                    spacing=4
                )
            ],
            spacing=8,
            style=ComponentStyle(align_items=AlignItems.CENTER)
        )
        
        # 动态样式演示框
        dynamic_demo_box = Container(
            children=[
                Label(
                    "动态样式演示",
                    font_size=18,
                    color=dynamic_text_color,
                    style=ComponentStyle(margin_bottom=px(8))
                ),
                Label(
                    Computed(lambda: f"色相: {bg_hue.value}° | 圆角: {border_radius.value}px | 内边距: {padding_size.value}px"),
                    font_size=12,
                    color=dynamic_text_color
                )
            ],
            style=ComponentStyle(
                width=px(300),
                height=px(120),
                background_color=dynamic_bg_color,
                border=Computed(lambda: f"3px solid {dynamic_border_color.value}"),
                border_radius=Computed(lambda: px(border_radius.value)),
                padding=Computed(lambda: px(padding_size.value)),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                # transition: "all 0.3s ease" if is_animated.value else "none",  # CSS过渡效果
            )
        )
        
        # 样式值显示
        style_values = VStack(
            children=[
                Label("当前样式值:", font_size=12, color="#333333"),
                Label(Computed(lambda: f"background-color: {dynamic_bg_color.value}"), font_size=10, color="#666666"),
                Label(Computed(lambda: f"border: 3px solid {dynamic_border_color.value}"), font_size=10, color="#666666"),
                Label(Computed(lambda: f"border-radius: {border_radius.value}px"), font_size=10, color="#666666"),
                Label(Computed(lambda: f"padding: {padding_size.value}px"), font_size=10, color="#666666")
            ],
            spacing=2,
            style=ComponentStyle(
                padding=px(12),
                background_color="#f8f9fa",
                border_radius=px(6),
                font_family="Monaco, Consolas, monospace"
            )
        )
        
        return Container(
            children=[
                Label(
                    "🎨 动态样式绑定",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("Signal驱动的实时样式更新:", font_size=14, color="#333333"),
                        dynamic_demo_box,
                        HStack(
                            children=[color_controls, geometry_controls],
                            spacing=32,
                            style=ComponentStyle(
                                justify_content=JustifyContent.CENTER,
                                margin=px(16)
                            )
                        ),
                        style_values,
                        VStack(
                            children=[
                                Label("动态样式特性:", font_size=12, color="#333333"),
                                Label("• Computed值自动更新CSS属性", font_size=10, color="#666666"),
                                Label("• 支持HSL色彩空间动态计算", font_size=10, color="#666666"),
                                Label("• 几何属性实时响应Signal变化", font_size=10, color="#666666"),
                                Label("• ReactiveBinding高效更新DOM", font_size=10, color="#666666")
                            ],
                            spacing=2,
                            style=ComponentStyle(
                                padding=px(12),
                                background_color="#fff0e6",
                                border_radius=px(6),
                                margin_top=px(12)
                            )
                        )
                    ],
                    spacing=16,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )

    def _create_presets_demo(self) -> Container:
        """创建预设样式演示"""
        from hibiki.ui.components.layout import VStack, HStack
        
        sections = [
            self._create_style_presets_section(),
            self._create_theme_presets_section(),
            self._create_utility_components_section()
        ]
        
        return VStack(
            children=sections,
            spacing=32,
            style=ComponentStyle(
                width=percent(100),
                padding=px(20)
            )
        )
    
    def _create_style_presets_section(self) -> Container:
        """创建样式预设区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        # StylePresets 示例
        preset_examples = [
            ("模态对话框样式", "modal", "适用于弹出对话框的居中定位"),
            ("悬浮按钮样式", "floating_button", "固定位置的操作按钮"),
            ("居中内容样式", "centered_content", "Flex布局的完美居中"),
            ("水平布局样式", "horizontal_layout", "一行排列的组件"),
            ("垂直布局样式", "vertical_layout", "垂直堆叠的组件"),
        ]
        
        preset_demos = []
        
        for title, preset_name, description in preset_examples:
            # 创建示例容器
            demo_container = Container(
                children=[
                    Label("预设样式演示", font_size=12, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(200),
                    height=px(80),
                    background_color="#007acc",
                    border_radius=px(8),
                    margin=px(8),
                    **self._get_preset_style(preset_name)
                )
            )
            
            # 说明文本
            info_section = VStack(
                children=[
                    Label(title, font_size=14, color="#333333"),
                    Label(f"StylePresets.{preset_name}()", font_size=11, color="#666666"),
                    Label(description, font_size=10, color="#888888")
                ],
                spacing=4,
                style=ComponentStyle(width=px(200))
            )
            
            preset_demo = HStack(
                children=[demo_container, info_section],
                spacing=20,
                style=ComponentStyle(
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(16)
                )
            )
            preset_demos.append(preset_demo)
        
        return Container(
            children=[
                Label("🎯 样式预设 (StylePresets)", font_size=18, color="#333333"),
                Label("框架提供的常用样式预设，可以快速应用到组件上", 
                      font_size=12, color="#666666",
                      style=ComponentStyle(margin_bottom=px(20))),
                VStack(
                    children=preset_demos,
                    spacing=12,
                    style=ComponentStyle(width=percent(100))
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _get_preset_style(self, preset_name: str) -> dict:
        """获取预设样式的字典表示（简化版）"""
        if preset_name == "centered_content":
            return {
                "display": Display.FLEX,
                "justify_content": JustifyContent.CENTER,
                "align_items": AlignItems.CENTER
            }
        elif preset_name == "horizontal_layout":
            return {
                "display": Display.FLEX,
                "flex_direction": FlexDirection.ROW,
                "align_items": AlignItems.CENTER
            }
        elif preset_name == "vertical_layout":
            return {
                "display": Display.FLEX,
                "flex_direction": FlexDirection.COLUMN
            }
        else:
            # modal 和 floating_button 样式在演示中简化
            return {
                "display": Display.FLEX,
                "justify_content": JustifyContent.CENTER,
                "align_items": AlignItems.CENTER
            }

    def _create_theme_presets_section(self) -> Container:
        """创建主题预设区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        # 主题示例
        theme_examples = [
            ("系统主题", "system", "#007acc", "跟随系统外观设置"),
            ("开发者深色", "developer_dark", "#2d3748", "适合代码开发的深色主题"),
            ("高对比度", "high_contrast", "#000000", "提升可访问性的高对比度")
        ]
        
        theme_demos = []
        
        for theme_name, theme_id, color, description in theme_examples:
            # 主题色彩示例
            theme_preview = Container(
                children=[
                    Label("Aa", font_size=18, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(60),
                    height=px(60),
                    background_color=color,
                    border_radius=px(8),
                    display=Display.FLEX,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            
            # 主题信息
            theme_info = VStack(
                children=[
                    Label(theme_name, font_size=14, color="#333333"),
                    Label(f"PresetThemes.{theme_id}()", font_size=11, color="#666666"),
                    Label(description, font_size=10, color="#888888")
                ],
                spacing=4,
                style=ComponentStyle(width=px(300))
            )
            
            theme_demo = HStack(
                children=[theme_preview, theme_info],
                spacing=16,
                style=ComponentStyle(
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(12)
                )
            )
            theme_demos.append(theme_demo)
        
        return Container(
            children=[
                Label("🎨 主题预设 (PresetThemes)", font_size=18, color="#333333"),
                Label("内置的主题方案，支持自动切换和自定义配色", 
                      font_size=12, color="#666666",
                      style=ComponentStyle(margin_bottom=px(20))),
                VStack(
                    children=theme_demos,
                    spacing=8,
                    style=ComponentStyle(width=percent(100))
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )

    def _create_utility_components_section(self) -> Container:
        """创建实用组件区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        # 实用组件示例
        utility_examples = [
            ("VStack", "垂直堆叠容器", "自动管理垂直间距"),
            ("HStack", "水平排列容器", "自动管理水平间距"),
            ("GridContainer", "网格布局容器", "支持CSS Grid语法"),
            ("ScrollableContainer", "滚动容器", "处理内容溢出滚动")
        ]
        
        utility_demos = []
        
        for component_name, description, feature in utility_examples:
            # 组件图标
            component_icon = Container(
                children=[
                    Label(component_name[0], font_size=16, color="#ffffff")
                ],
                style=ComponentStyle(
                    width=px(40),
                    height=px(40),
                    background_color="#28a745",
                    border_radius=px(20),
                    display=Display.FLEX,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER
                )
            )
            
            # 组件信息
            component_info = VStack(
                children=[
                    Label(component_name, font_size=14, color="#333333"),
                    Label(description, font_size=12, color="#666666"),
                    Label(feature, font_size=10, color="#888888")
                ],
                spacing=2,
                style=ComponentStyle(width=px(280))
            )
            
            utility_demo = HStack(
                children=[component_icon, component_info],
                spacing=12,
                style=ComponentStyle(
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(10)
                )
            )
            utility_demos.append(utility_demo)
        
        return Container(
            children=[
                Label("🧩 实用组件", font_size=18, color="#333333"),
                Label("高级布局容器和实用工具组件", 
                      font_size=12, color="#666666",
                      style=ComponentStyle(margin_bottom=px(20))),
                VStack(
                    children=utility_demos,
                    spacing=8,
                    style=ComponentStyle(width=percent(100))
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_performance_demo(self) -> Container:
        """创建性能监控演示"""
        from hibiki.ui.components.layout import VStack, HStack
        import time
        
        # 获取当前性能统计
        current_stats = self.performance_stats.value
        viewport_info = self.viewport_info.value
        
        sections = [
            self._create_system_metrics_section(),
            self._create_layout_performance_section(),
            self._create_reactive_system_stats_section(),
            self._create_debug_tools_section()
        ]
        
        return VStack(
            children=sections,
            spacing=24,
            style=ComponentStyle(
                width=percent(100),
                padding=px(20)
            )
        )
    
    def _create_system_metrics_section(self) -> Container:
        """创建系统指标区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        viewport_info = self.viewport_info.value
        current_stats = self.performance_stats.value
        
        metrics = [
            ("窗口分辨率", f"{viewport_info.get('width', 0):.0f} × {viewport_info.get('height', 0):.0f} px", "#007acc"),
            ("视口尺寸", f"{viewport_info.get('viewport_width', 0):.0f} × {viewport_info.get('viewport_height', 0):.0f} px", "#28a745"),
            ("布局引擎", "Stretchable/Taffy", "#6f42c1"),
            ("当前断点", viewport_info.get('breakpoint', 'LG'), "#fd7e14")
        ]
        
        metric_cards = []
        for title, value, color in metrics:
            card = Container(
                children=[
                    Label(value, font_size=16, color=color),
                    Label(title, font_size=11, color="#666666")
                ],
                style=ComponentStyle(
                    width=px(160),
                    padding=px(16),
                    background_color="#f8f9fa",
                    border_radius=px(8),
                    border="1px solid #e9ecef",
                    display=Display.FLEX,
                    flex_direction=FlexDirection.COLUMN,
                    align_items=AlignItems.CENTER
                )
            )
            metric_cards.append(card)
        
        return Container(
            children=[
                Label("📊 系统指标", font_size=18, color="#333333"),
                HStack(
                    children=metric_cards,
                    spacing=16,
                    style=ComponentStyle(
                        width=percent(100),
                        margin_top=px(16)
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_layout_performance_section(self) -> Container:
        """创建布局性能区域"""  
        from hibiki.ui.components.layout import VStack, HStack
        
        current_stats = self.performance_stats.value
        
        # 模拟布局性能数据
        performance_data = [
            ("布局计算时间", f"{current_stats.get('layout_time_ms', 1.18):.2f}ms", "#28a745"),
            ("组件数量", f"{current_stats.get('component_count', 145)}", "#007acc"),  
            ("布局节点", f"{current_stats.get('layout_nodes', 98)}", "#6f42c1"),
            ("渲染帧率", "60 FPS", "#fd7e14")
        ]
        
        perf_items = []
        for metric, value, color in performance_data:
            item = HStack(
                children=[
                    Container(
                        children=[Label("●", font_size=16, color=color)],
                        style=ComponentStyle(
                            width=px(20),
                            display=Display.FLEX,
                            align_items=AlignItems.CENTER
                        )
                    ),
                    VStack(
                        children=[
                            Label(value, font_size=14, color="#333333"),
                            Label(metric, font_size=11, color="#666666")
                        ],
                        spacing=2,
                        style=ComponentStyle(width=px(120))
                    )
                ],
                spacing=8,
                style=ComponentStyle(
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(8)
                )
            )
            perf_items.append(item)
        
        return Container(
            children=[
                Label("⚡ 布局性能", font_size=18, color="#333333"),
                VStack(
                    children=perf_items,
                    spacing=8,
                    style=ComponentStyle(
                        width=percent(100),
                        margin_top=px(16)
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff", 
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_reactive_system_stats_section(self) -> Container:
        """创建响应式系统统计区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        # 响应式系统统计数据
        reactive_stats = [
            ("Signal数量", "12", "活跃的Signal实例"),
            ("Computed缓存", "8", "已缓存的Computed值"),
            ("Effect监听", "15", "活跃的Effect监听器"),
            ("批次更新", "3", "已优化的批次操作")
        ]
        
        stat_cards = []
        for title, count, description in reactive_stats:
            card = VStack(
                children=[
                    Label(count, font_size=18, color="#007acc"),
                    Label(title, font_size=12, color="#333333"),
                    Label(description, font_size=10, color="#666666")
                ],
                spacing=4,
                style=ComponentStyle(
                    width=px(120),
                    padding=px(12),
                    background_color="#f8f9fa",
                    border_radius=px(6),
                    border="1px solid #e9ecef",
                    align_items=AlignItems.CENTER
                )
            )
            stat_cards.append(card)
        
        return Container(
            children=[
                Label("🔄 响应式系统", font_size=18, color="#333333"),
                HStack(
                    children=stat_cards,
                    spacing=12,
                    style=ComponentStyle(
                        width=percent(100),
                        margin_top=px(16)
                    )
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_debug_tools_section(self) -> Container:
        """创建调试工具区域"""
        from hibiki.ui.components.layout import VStack, HStack
        
        # 调试工具列表
        debug_tools = [
            ("capture_app_screenshot()", "📸", "应用截图工具"),
            ("debug_view_layout()", "📐", "视图布局调试"),
            ("get_layout_engine()", "🏗️", "布局引擎访问"),
            ("ScreenshotTool", "🛠️", "高级截图工具")
        ]
        
        tool_items = []
        for tool_name, icon, description in debug_tools:
            item = HStack(
                children=[
                    Container(
                        children=[Label(icon, font_size=16)],
                        style=ComponentStyle(
                            width=px(40),
                            height=px(40),
                            background_color="#f8f9fa",
                            border_radius=px(20),
                            display=Display.FLEX,
                            align_items=AlignItems.CENTER,
                            justify_content=JustifyContent.CENTER
                        )
                    ),
                    VStack(
                        children=[
                            Label(tool_name, font_size=12, color="#333333"),
                            Label(description, font_size=10, color="#666666")
                        ],
                        spacing=2,
                        style=ComponentStyle(width=px(200))
                    )
                ],
                spacing=12,
                style=ComponentStyle(
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(8)
                )
            )
            tool_items.append(item)
        
        return Container(
            children=[
                Label("🛠️ 调试工具", font_size=18, color="#333333"),
                Label("框架内置的调试和开发工具", font_size=12, color="#666666",
                      style=ComponentStyle(margin_bottom=px(16))),
                VStack(
                    children=tool_items,
                    spacing=8,
                    style=ComponentStyle(width=percent(100))
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(12),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_flex_direction_section(self) -> Container:
        """创建Flex方向演示区域"""
        # 四种flex-direction的演示
        direction_examples = [
            (FlexDirection.ROW, "flex-direction: ROW", "水平排列（左到右）"),
            (FlexDirection.ROW_REVERSE, "flex-direction: ROW_REVERSE", "水平排列（右到左）"),
            (FlexDirection.COLUMN, "flex-direction: COLUMN", "垂直排列（上到下）"),
            (FlexDirection.COLUMN_REVERSE, "flex-direction: COLUMN_REVERSE", "垂直排列（下到上）")
        ]
        
        direction_demos = []
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"]
        
        for i, (direction, title, description) in enumerate(direction_examples):
            # 创建子项目
            flex_items = []
            for j in range(3):
                item = Container(
                    children=[
                        Label(f"Item {j+1}", font_size=12, color="#ffffff")
                    ],
                    style=ComponentStyle(
                        width=px(60),
                        height=px(40),
                        background_color=colors[j % len(colors)],
                        border_radius=px(4),
                        display=Display.FLEX,
                        justify_content=JustifyContent.CENTER,
                        align_items=AlignItems.CENTER
                    )
                )
                flex_items.append(item)
            
            # Flex容器
            flex_container = Container(
                children=flex_items,
                style=ComponentStyle(
                    width=px(200),
                    height=px(120),
                    background_color="#f8f9fa",
                    border="2px dashed #dee2e6",
                    border_radius=px(8),
                    padding=px(10),
                    display=Display.FLEX,
                    flex_direction=direction,
                    gap=px(8),
                    align_items=AlignItems.CENTER,
                    justify_content=JustifyContent.CENTER
                )
            )
            
            # 说明文字
            explanation = VStack(
                children=[
                    Label(title, font_size=14, color="#333333"),
                    Label(description, font_size=11, color="#666666")
                ],
                spacing=4,
                style=ComponentStyle(width=px(180))
            )
            
            demo_item = VStack(
                children=[flex_container, explanation],
                spacing=8,
                style=ComponentStyle(align_items=AlignItems.CENTER)
            )
            
            direction_demos.append(demo_item)
        
        return Container(
            children=[
                Label(
                    "📐 Flex Direction (方向)",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                GridContainer(
                    children=direction_demos,
                    columns="1fr 1fr",
                    rows="auto auto",
                    gap=24,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20),
                        background_color="#ffffff",
                        border_radius=px(8),
                        border="1px solid #e9ecef"
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_flex_alignment_section(self) -> Container:
        """创建Flex对齐演示区域"""
        # justify_content选项
        justify_options = [
            (JustifyContent.FLEX_START, "FLEX_START", "起始对齐"),
            (JustifyContent.CENTER, "CENTER", "居中对齐"),
            (JustifyContent.FLEX_END, "FLEX_END", "末端对齐"),
            (JustifyContent.SPACE_BETWEEN, "SPACE_BETWEEN", "两端对齐"),
            (JustifyContent.SPACE_AROUND, "SPACE_AROUND", "环绕对齐"),
            (JustifyContent.SPACE_EVENLY, "SPACE_EVENLY", "平均对齐")
        ]
        
        justify_demos = []
        for justify, name, desc in justify_options:
            # 创建Flex项目
            items = []
            for i in range(3):
                item = Container(
                    children=[Label(f"{i+1}", font_size=10, color="#ffffff")],
                    style=ComponentStyle(
                        width=px(30),
                        height=px(30),
                        background_color="#007acc",
                        border_radius=px(4),
                        display=Display.FLEX,
                        justify_content=JustifyContent.CENTER,
                        align_items=AlignItems.CENTER
                    )
                )
                items.append(item)
            
            # Flex容器
            flex_demo = Container(
                children=items,
                style=ComponentStyle(
                    width=px(200),
                    height=px(50),
                    background_color="#f8f9fa",
                    border="1px solid #dee2e6",
                    border_radius=px(4),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    justify_content=justify,
                    align_items=AlignItems.CENTER,
                    padding=px(5)
                )
            )
            
            demo_item = VStack(
                children=[
                    Label(name, font_size=11, color="#333333"),
                    flex_demo,
                    Label(desc, font_size=10, color="#666666")
                ],
                spacing=4,
                style=ComponentStyle(align_items=AlignItems.CENTER)
            )
            
            justify_demos.append(demo_item)
        
        # align_items选项
        align_options = [
            (AlignItems.STRETCH, "STRETCH", "拉伸填充"),
            (AlignItems.FLEX_START, "FLEX_START", "起始对齐"),
            (AlignItems.CENTER, "CENTER", "居中对齐"),
            (AlignItems.FLEX_END, "FLEX_END", "末端对齐")
        ]
        
        align_demos = []
        for align, name, desc in align_options:
            items = []
            heights = [px(20), px(30), px(25)]  # 不同高度
            for i, height in enumerate(heights):
                item = Container(
                    children=[Label(f"{i+1}", font_size=10, color="#ffffff")],
                    style=ComponentStyle(
                        width=px(40),
                        height=height if align != AlignItems.STRETCH else None,
                        background_color="#28a745",
                        border_radius=px(4),
                        display=Display.FLEX,
                        justify_content=JustifyContent.CENTER,
                        align_items=AlignItems.CENTER
                    )
                )
                items.append(item)
            
            flex_demo = Container(
                children=items,
                style=ComponentStyle(
                    width=px(160),
                    height=px(50),
                    background_color="#f8f9fa",
                    border="1px solid #dee2e6",
                    border_radius=px(4),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    justify_content=JustifyContent.CENTER,
                    align_items=align,
                    gap=px(5),
                    padding=px(5)
                )
            )
            
            demo_item = VStack(
                children=[
                    Label(name, font_size=11, color="#333333"),
                    flex_demo,
                    Label(desc, font_size=10, color="#666666")
                ],
                spacing=4,
                style=ComponentStyle(align_items=AlignItems.CENTER)
            )
            
            align_demos.append(demo_item)
        
        return VStack(
            children=[
                Label(
                    "🎯 Flex Alignment (对齐)",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                
                # Justify Content演示
                Container(
                    children=[
                        Label("Justify Content (主轴对齐):", font_size=14, color="#333333", 
                              style=ComponentStyle(margin_bottom=px(12))),
                        GridContainer(
                            children=justify_demos,
                            columns="1fr 1fr 1fr",
                            gap=16,
                            style=ComponentStyle(width=percent(100))
                        )
                    ],
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16),
                        background_color="#ffffff",
                        border_radius=px(8),
                        border="1px solid #e9ecef",
                        margin_bottom=px(16)
                    )
                ),
                
                # Align Items演示
                Container(
                    children=[
                        Label("Align Items (交叉轴对齐):", font_size=14, color="#333333",
                              style=ComponentStyle(margin_bottom=px(12))),
                        HStack(
                            children=align_demos,
                            spacing=20,
                            style=ComponentStyle(
                                width=percent(100),
                                justify_content=JustifyContent.CENTER
                            )
                        )
                    ],
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(16),
                        background_color="#ffffff",
                        border_radius=px(8),
                        border="1px solid #e9ecef"
                    )
                )
            ],
            spacing=0,
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_flex_grow_section(self) -> Container:
        """创建Flex弹性伸缩演示区域"""
        # 不同flex_grow值的演示
        flex_grow_examples = [
            ([0, 0, 0], "全部为0", "固定尺寸，不伸缩"),
            ([1, 1, 1], "全部为1", "平均分配剩余空间"),
            ([1, 2, 1], "1:2:1", "按比例分配空间"),
            ([0, 1, 0], "0:1:0", "只有中间项伸缩")
        ]
        
        grow_demos = []
        colors = ["#ff6b6b", "#4ecdc4", "#45b7d1"]
        
        for grow_values, title, description in flex_grow_examples:
            items = []
            for i, grow_value in enumerate(grow_values):
                item = Container(
                    children=[
                        VStack(
                            children=[
                                Label(f"Item {i+1}", font_size=11, color="#ffffff"),
                                Label(f"grow: {grow_value}", font_size=9, color="#ffffff")
                            ],
                            spacing=2,
                            style=ComponentStyle(align_items=AlignItems.CENTER)
                        )
                    ],
                    style=ComponentStyle(
                        width=px(60) if grow_value == 0 else None,  # 固定宽度 vs 弹性宽度
                        height=px(50),
                        flex_grow=grow_value,
                        background_color=colors[i],
                        border_radius=px(4),
                        display=Display.FLEX,
                        justify_content=JustifyContent.CENTER,
                        align_items=AlignItems.CENTER,
                        margin=px(2)
                    )
                )
                items.append(item)
            
            flex_container = Container(
                children=items,
                style=ComponentStyle(
                    width=px(300),
                    height=px(60),
                    background_color="#f8f9fa",
                    border="2px dashed #dee2e6",
                    border_radius=px(8),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    align_items=AlignItems.CENTER,
                    padding=px(5)
                )
            )
            
            explanation = VStack(
                children=[
                    Label(title, font_size=13, color="#333333"),
                    Label(description, font_size=11, color="#666666")
                ],
                spacing=4,
                style=ComponentStyle(width=px(280), align_items=AlignItems.CENTER)
            )
            
            demo_item = VStack(
                children=[explanation, flex_container],
                spacing=8,
                style=ComponentStyle(align_items=AlignItems.CENTER)
            )
            
            grow_demos.append(demo_item)
        
        return Container(
            children=[
                Label(
                    "🔄 Flex Grow (弹性伸缩)",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=grow_demos,
                    spacing=20,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20),
                        background_color="#ffffff",
                        border_radius=px(8),
                        border="1px solid #e9ecef"
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_flex_wrap_section(self) -> Container:
        """创建Flex换行演示区域"""
        # 创建多个项目用于换行测试
        def create_flex_items(count: int, item_width: int = 80):
            items = []
            colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#fd79a8"]
            for i in range(count):
                item = Container(
                    children=[Label(f"Item {i+1}", font_size=10, color="#ffffff")],
                    style=ComponentStyle(
                        width=px(item_width),
                        height=px(40),
                        background_color=colors[i % len(colors)],
                        border_radius=px(4),
                        display=Display.FLEX,
                        justify_content=JustifyContent.CENTER,
                        align_items=AlignItems.CENTER,
                        flex_shrink=0  # 防止收缩
                    )
                )
                items.append(item)
            return items
        
        wrap_examples = [
            ("nowrap", "不换行（默认）", "项目会被压缩以适应容器"),
            ("wrap", "换行", "项目超出容器时换到下一行"),
            ("wrap-reverse", "反向换行", "换行但行的顺序相反")
        ]
        
        wrap_demos = []
        for wrap_value, title, description in wrap_examples:
            # 创建足够多的项目以触发换行
            items = create_flex_items(6, 80)
            
            flex_container = Container(
                children=items,
                style=ComponentStyle(
                    width=px(350),
                    height=px(120) if wrap_value != "nowrap" else px(60),
                    background_color="#f8f9fa",
                    border="2px dashed #dee2e6",
                    border_radius=px(8),
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    gap=px(8),
                    padding=px(10),
                    # flex_wrap=wrap_value,  # TODO: 需要确认Hibiki UI是否支持flex-wrap
                    align_items=AlignItems.FLEX_START,
                    justify_content=JustifyContent.FLEX_START,
                    # overflow=OverflowBehavior.HIDDEN if wrap_value == "nowrap" else OverflowBehavior.VISIBLE
                )
            )
            
            demo_item = VStack(
                children=[
                    Label(title, font_size=14, color="#333333"),
                    Label(description, font_size=11, color="#666666"),
                    flex_container
                ],
                spacing=8,
                style=ComponentStyle(align_items=AlignItems.CENTER)
            )
            
            wrap_demos.append(demo_item)
        
        return Container(
            children=[
                Label(
                    "📦 Flex Wrap (换行)",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=wrap_demos,
                    spacing=24,
                    style=ComponentStyle(
                        width=percent(100),
                        padding=px(20),
                        background_color="#ffffff",
                        border_radius=px(8),
                        border="1px solid #e9ecef"
                    )
                )
            ],
            style=ComponentStyle(width=percent(100))
        )
    
    def _create_grid_items(self, count: int, color_scheme: str = "primary"):
        """创建Grid项目的辅助方法"""
        items = []
        colors = {
            "primary": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#fd79a8"],
            "secondary": ["#6c5ce7", "#00b894", "#fdcb6e", "#e17055", "#74b9ff", "#a29bfe"]
        }
        color_list = colors.get(color_scheme, colors["primary"])
        
        for i in range(count):
            item = Container(
                children=[
                    Label(
                        f"Item {i+1}",
                        font_size=12,
                        color="#ffffff",
                        style=ComponentStyle()
                    )
                ],
                style=ComponentStyle(
                    background_color=color_list[i % len(color_list)],
                    border_radius=px(4),
                    padding=px(8),
                    display=Display.FLEX,
                    justify_content=JustifyContent.CENTER,
                    align_items=AlignItems.CENTER,
                    min_height=px(60)
                )
            )
            items.append(item)
        return items

    def _create_basic_grid_section(self) -> Container:
        """创建基本Grid演示区域"""
        
        # 基本网格：3x2
        basic_grid_items = self._create_grid_items(6)
        basic_grid = GridContainer(
            children=basic_grid_items,
            columns="1fr 1fr 1fr",  # 3列等宽
            rows="auto auto",       # 2行自动高度
            gap=16,
            style=ComponentStyle(
                width=px(400),
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        # 不等宽列网格：2fr 1fr 1fr
        unequal_grid_items = self._create_grid_items(6, "secondary")
        unequal_grid = GridContainer(
            children=unequal_grid_items,
            columns="2fr 1fr 1fr",  # 第一列占2份，其他列各占1份
            rows="auto auto",
            gap=12,
            style=ComponentStyle(
                width=px(400),
                padding=px(16),
                background_color="#f8f9fa", 
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        return Container(
            children=[
                Label(
                    "🔲 Grid 基本语法",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                
                # 等宽Grid演示
                VStack(
                    children=[
                        Label("等宽3列网格 (1fr 1fr 1fr):", font_size=14, color="#333333"),
                        basic_grid,
                        Label("grid-template-columns: 1fr 1fr 1fr", font_size=11, color="#666666")
                    ],
                    spacing=8,
                    style=ComponentStyle(
                        align_items=AlignItems.CENTER,
                        margin_bottom=px(24)
                    )
                ),
                
                # 不等宽Grid演示
                VStack(
                    children=[
                        Label("不等宽3列网格 (2fr 1fr 1fr):", font_size=14, color="#333333"),
                        unequal_grid,
                        Label("grid-template-columns: 2fr 1fr 1fr", font_size=11, color="#666666")
                    ],
                    spacing=8,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_grid_positioning_section(self) -> Container:
        """创建Grid定位演示区域"""
        # 创建特殊定位的Grid项目
        positioned_items = []
        
        # Header: 跨3列
        header = Container(
            children=[Label("Header (跨3列)", font_size=14, color="#ffffff")],
            style=ComponentStyle(
                background_color="#2d3436",
                border_radius=px(4),
                padding=px(12),
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
        
        # Sidebar: 跨2行
        sidebar = Container(
            children=[Label("Sidebar\n(跨2行)", font_size=12, color="#ffffff")],
            style=ComponentStyle(
                background_color="#00b894",
                border_radius=px(4),
                padding=px(12),
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                min_height=px(120)
            )
        )
        
        # Main Content
        main_content = Container(
            children=[Label("Main Content", font_size=12, color="#ffffff")],
            style=ComponentStyle(
                background_color="#0984e3",
                border_radius=px(4),
                padding=px(12),
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
        
        # Right Panel
        right_panel = Container(
            children=[Label("Right Panel", font_size=12, color="#ffffff")],
            style=ComponentStyle(
                background_color="#6c5ce7",
                border_radius=px(4),
                padding=px(12),
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
        
        # Footer: 跨3列
        footer = Container(
            children=[Label("Footer (跨3列)", font_size=14, color="#ffffff")],
            style=ComponentStyle(
                background_color="#636e72",
                border_radius=px(4),
                padding=px(12),
                display=Display.FLEX,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER
            )
        )
        
        # 使用GridContainer创建复杂布局
        layout_grid = GridContainer(
            children=[header, sidebar, main_content, right_panel, footer],
            columns="200px 1fr 1fr",  # 固定宽度 + 弹性宽度
            rows="auto 1fr auto",     # 自动 + 弹性 + 自动
            gap=12,
            style=ComponentStyle(
                width=px(500),
                height=px(250),
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        # 设置Grid项目位置
        layout_grid.set_grid_position(header, column_start=1, column_end=4, row_start=1, row_end=2)  # 跨3列
        layout_grid.set_grid_position(sidebar, column_start=1, column_end=2, row_start=2, row_end=3)  # 左侧，跨1行
        layout_grid.set_grid_position(main_content, column_start=2, column_end=3, row_start=2, row_end=3)  # 中间
        layout_grid.set_grid_position(right_panel, column_start=3, column_end=4, row_start=2, row_end=3)  # 右侧
        layout_grid.set_grid_position(footer, column_start=1, column_end=4, row_start=3, row_end=4)  # 跨3列
        
        return Container(
            children=[
                Label(
                    "📍 Grid 定位与跨列",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                VStack(
                    children=[
                        Label("经典网页布局 (Header-Sidebar-Main-Footer):", font_size=14, color="#333333"),
                        layout_grid,
                        VStack(
                            children=[
                                Label("• Header & Footer: grid-column: 1 / 4 (跨3列)", font_size=11, color="#666666"),
                                Label("• Sidebar: grid-column: 1 / 2, grid-row: 2 / 3", font_size=11, color="#666666"),
                                Label("• Main: grid-column: 2 / 3, Right: grid-column: 3 / 4", font_size=11, color="#666666")
                            ],
                            spacing=2
                        )
                    ],
                    spacing=12,
                    style=ComponentStyle(align_items=AlignItems.CENTER)
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_grid_template_section(self) -> Container:
        """创建Grid模板演示区域"""
        # repeat()语法演示
        repeat_items = self._create_grid_items(8)
        repeat_grid = GridContainer(
            children=repeat_items,
            columns="repeat(4, 1fr)",  # 重复4次1fr
            rows="repeat(2, auto)",    # 重复2次auto
            gap=12,
            style=ComponentStyle(
                width=px(400),
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        # minmax()语法演示
        minmax_items = self._create_grid_items(6, "secondary")
        minmax_grid = GridContainer(
            children=minmax_items,
            columns="minmax(100px, 1fr) minmax(80px, 200px) 1fr",  # 最小-最大值
            rows="auto auto",
            gap=12,
            style=ComponentStyle(
                width=px(400),
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        # 混合单位演示
        mixed_items = self._create_grid_items(6)
        mixed_grid = GridContainer(
            children=mixed_items,
            columns="100px 50% 1fr",   # 固定-百分比-弹性
            rows="60px auto",          # 固定-自动
            gap=16,
            style=ComponentStyle(
                width=px(400),
                padding=px(16),
                background_color="#f8f9fa",
                border_radius=px(8),
                border="2px dashed #dee2e6"
            )
        )
        
        return Container(
            children=[
                Label(
                    "📐 Grid 模板语法",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                
                VStack(
                    children=[
                        # repeat()演示
                        VStack(
                            children=[
                                Label("repeat() 重复语法:", font_size=14, color="#333333"),
                                repeat_grid,
                                Label("columns: repeat(4, 1fr) = 1fr 1fr 1fr 1fr", font_size=11, color="#666666")
                            ],
                            spacing=8,
                            style=ComponentStyle(align_items=AlignItems.CENTER, margin_bottom=px(20))
                        ),
                        
                        # minmax()演示
                        VStack(
                            children=[
                                Label("minmax() 最值语法:", font_size=14, color="#333333"),
                                minmax_grid,
                                Label("columns: minmax(100px, 1fr) minmax(80px, 200px) 1fr", font_size=11, color="#666666")
                            ],
                            spacing=8,
                            style=ComponentStyle(align_items=AlignItems.CENTER, margin_bottom=px(20))
                        ),
                        
                        # 混合单位演示
                        VStack(
                            children=[
                                Label("混合单位:", font_size=14, color="#333333"),
                                mixed_grid,
                                Label("columns: 100px 50% 1fr (固定-百分比-弹性)", font_size=11, color="#666666")
                            ],
                            spacing=8,
                            style=ComponentStyle(align_items=AlignItems.CENTER)
                        )
                    ],
                    spacing=0
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )
    
    def _create_responsive_grid_section(self) -> Container:
        """创建响应式Grid演示区域"""
        # 这里我们演示不同列数的Grid
        responsive_items = self._create_grid_items(12)
        
        # 使用ResponsiveGrid组件（如果可用）或常规GridContainer
        # 1列（手机）-> 2列（平板）-> 3列（桌面）-> 4列（大屏）
        mobile_grid = GridContainer(
            children=responsive_items[:4],  # 显示4个项目
            columns="1fr",  # 1列
            gap=12,
            style=ComponentStyle(
                width=px(200),
                padding=px(12),
                background_color="#fff5f5",
                border_radius=px(6),
                border="2px solid #fed7d7"
            )
        )
        
        tablet_grid = GridContainer(
            children=responsive_items[:6],  # 显示6个项目
            columns="1fr 1fr",  # 2列
            gap=12,
            style=ComponentStyle(
                width=px(280),
                padding=px(12),
                background_color="#f0fff4",
                border_radius=px(6),
                border="2px solid #9ae6b4"
            )
        )
        
        desktop_grid = GridContainer(
            children=responsive_items[:9],  # 显示9个项目
            columns="1fr 1fr 1fr",  # 3列
            gap=12,
            style=ComponentStyle(
                width=px(360),
                padding=px(12),
                background_color="#f0f8ff",
                border_radius=px(6),
                border="2px solid #90cdf4"
            )
        )
        
        large_grid = GridContainer(
            children=responsive_items,  # 显示所有12个项目
            columns="1fr 1fr 1fr 1fr",  # 4列
            gap=12,
            style=ComponentStyle(
                width=px(440),
                padding=px(12),
                background_color="#faf5ff",
                border_radius=px(6),
                border="2px solid #d6bcfa"
            )
        )
        
        return Container(
            children=[
                Label(
                    "📱 响应式 Grid",
                    font_size=16,
                    color="#333333",
                    style=ComponentStyle(margin_bottom=px(16))
                ),
                
                VStack(
                    children=[
                        Label("不同屏幕尺寸下的Grid布局:", font_size=14, color="#333333", 
                              style=ComponentStyle(margin_bottom=px(16))),
                        
                        # 响应式演示网格
                        HStack(
                            children=[
                                VStack(
                                    children=[
                                        Label("📱 手机 (1列)", font_size=12, color="#e53e3e"),
                                        mobile_grid
                                    ],
                                    spacing=8,
                                    style=ComponentStyle(align_items=AlignItems.CENTER)
                                ),
                                VStack(
                                    children=[
                                        Label("📱 平板 (2列)", font_size=12, color="#38a169"),
                                        tablet_grid
                                    ],
                                    spacing=8,
                                    style=ComponentStyle(align_items=AlignItems.CENTER)
                                )
                            ],
                            spacing=20,
                            style=ComponentStyle(
                                justify_content=JustifyContent.CENTER,
                                margin_bottom=px(20)
                            )
                        ),
                        
                        HStack(
                            children=[
                                VStack(
                                    children=[
                                        Label("💻 桌面 (3列)", font_size=12, color="#3182ce"),
                                        desktop_grid
                                    ],
                                    spacing=8,
                                    style=ComponentStyle(align_items=AlignItems.CENTER)
                                ),
                                VStack(
                                    children=[
                                        Label("🖥️ 大屏 (4列)", font_size=12, color="#805ad5"),
                                        large_grid
                                    ],
                                    spacing=8,
                                    style=ComponentStyle(align_items=AlignItems.CENTER)
                                )
                            ],
                            spacing=20,
                            style=ComponentStyle(justify_content=JustifyContent.CENTER)
                        )
                    ],
                    spacing=0
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                padding=px(20),
                background_color="#ffffff",
                border_radius=px(8),
                border="1px solid #e9ecef"
            )
        )

    def _create_placeholder_demo(self, title: str, icon: str) -> Container:
        """创建占位符演示内容"""
        return Container(
            children=[
                Label(
                    f"{icon} {title}",
                    font_size=20,
                    color="#333333",
                    style=ComponentStyle(
                        margin_bottom=px(16)
                    )
                ),
                Label(
                    "此演示区域正在开发中...",
                    font_size=14,
                    color="#666666",
                    style=ComponentStyle()
                )
            ],
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                background_color="#f8f9fa",
                border_radius=px(8)
            )
        )
    
    def _start_performance_monitoring(self):
        """启动性能监控"""
        def update_performance_stats():
            try:
                from hibiki.ui.core.layout import get_layout_engine
                engine = get_layout_engine()
                
                stats = {
                    "component_count": len(engine._component_nodes),
                    "layout_time": 0.0,  # 将在布局计算时更新
                    "node_count": len(engine._component_nodes),
                    "memory_usage": 0  # TODO: 实现内存监控
                }
                
                self.performance_stats.value = stats
                
            except Exception as e:
                logger.warning(f"性能统计更新失败: {e}")
        
        # 每2秒更新一次性能统计
        import threading
        def performance_timer():
            while True:
                time.sleep(2)
                update_performance_stats()
        
        thread = threading.Thread(target=performance_timer, daemon=True)
        thread.start()
    
    def _start_responsive_monitoring(self):
        """启动响应式监控"""
        try:
            responsive_mgr = get_responsive_manager()
            
            def update_viewport_info():
                info = responsive_mgr.get_current_breakpoint_info()
                self.viewport_info.value = {
                    "width": info["viewport_width"],
                    "height": 600,  # TODO: 获取实际高度
                    "breakpoint": info["primary_breakpoint"]
                }
            
            # 添加响应式变化回调
            responsive_mgr.add_style_change_callback(
                lambda width, breakpoints: update_viewport_info()
            )
            
            # 初始更新
            update_viewport_info()
            
        except Exception as e:
            logger.warning(f"响应式监控启动失败: {e}")
    
    def _take_screenshot(self):
        """截图功能"""
        try:
            timestamp = int(time.time())
            filename = f"hibiki_style_demo_{timestamp}.png"
            success = capture_app_screenshot(filename)
            
            if success:
                logger.info(f"📸 截图保存成功: {filename}")
            else:
                logger.error("📸 截图保存失败")
                
        except Exception as e:
            logger.error(f"截图异常: {e}")


def main():
    """主函数"""
    try:
        logger.info("🎨 启动Hibiki UI样式系统综合演示...")
        
        # 创建并运行演示应用
        demo_app = StyleDemoApp()
        demo_app.create_main_app()
        
    except Exception as e:
        logger.error(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()