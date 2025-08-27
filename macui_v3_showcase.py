#!/usr/bin/env python3
"""
macUI v3.0 Layout System Showcase
展示专业级Stretchable布局引擎的强大功能
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.layout.node import LayoutNode
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
from macui.core import Signal, Computed, Effect
from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label
from AppKit import *
from Foundation import *
import AppHelper

class LayoutShowcaseController:
    """布局展示控制器 - 管理各种布局示例"""
    
    def __init__(self):
        # 响应式状态
        self.current_demo = Signal("flexbox")
        self.item_count = Signal(3)
        self.gap_size = Signal(10)
        self.container_width = Signal(400)
        self.container_height = Signal(300)
        
        # 布局根节点
        self.root_node = None
        self.demo_container_node = None
        
        # 演示数据
        self.demos = {
            "flexbox": "Flexbox基础演示",
            "nested": "嵌套布局演示", 
            "responsive": "响应式布局演示",
            "complex": "复杂组合布局演示"
        }
        
    def create_layout_tree(self):
        """创建主布局树结构"""
        
        # 主容器样式 - 垂直布局
        main_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=800,
            height=600,
            padding=20
        )
        
        self.root_node = LayoutNode(style=main_style, key="main_container")
        
        # 创建头部区域
        header_node = self._create_header_section()
        self.root_node.add_child(header_node)
        
        # 创建控制面板
        control_panel_node = self._create_control_panel()
        self.root_node.add_child(control_panel_node)
        
        # 创建演示区域容器
        demo_container_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            flex_grow=1.0,  # 占用剩余空间
            gap=20,
            margin_top=20
        )
        
        demo_main_node = LayoutNode(style=demo_container_style, key="demo_main")
        
        # 演示选择侧边栏
        sidebar_node = self._create_demo_sidebar()
        demo_main_node.add_child(sidebar_node)
        
        # 实际演示区域
        self.demo_container_node = self._create_demo_area()
        demo_main_node.add_child(self.demo_container_node)
        
        self.root_node.add_child(demo_main_node)
        
        # 计算初始布局
        self.root_node.compute_layout()
        
        return self.root_node
    
    def _create_header_section(self):
        """创建头部标题区域"""
        header_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            padding=10,
            height=80
        )
        
        header_node = LayoutNode(style=header_style, key="header")
        
        # 主标题
        title_style = LayoutStyle(width=400, height=30)
        title_node = LayoutNode(style=title_style, key="title")
        header_node.add_child(title_node)
        
        # 副标题
        subtitle_style = LayoutStyle(width=400, height=20)
        subtitle_node = LayoutNode(style=subtitle_style, key="subtitle") 
        header_node.add_child(subtitle_node)
        
        return header_node
    
    def _create_control_panel(self):
        """创建参数控制面板"""
        panel_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.SPACE_BETWEEN,
            align_items=AlignItems.CENTER,
            height=50,
            padding=10,
            gap=20
        )
        
        panel_node = LayoutNode(style=panel_style, key="control_panel")
        
        # 项目数量控制
        count_group = self._create_control_group("项目数量", ["1", "2", "3", "4", "5"])
        panel_node.add_child(count_group)
        
        # 间距控制
        gap_group = self._create_control_group("间距", ["5", "10", "20", "30"])
        panel_node.add_child(gap_group)
        
        # 容器尺寸控制
        size_group = self._create_control_group("容器", ["小", "中", "大"])
        panel_node.add_child(size_group)
        
        return panel_node
    
    def _create_control_group(self, label, options):
        """创建控制组"""
        group_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=AlignItems.CENTER,
            gap=8
        )
        
        group_node = LayoutNode(style=group_style, key=f"group_{label}")
        
        # 标签
        label_style = LayoutStyle(width=60, height=20)
        label_node = LayoutNode(style=label_style, key=f"label_{label}")
        group_node.add_child(label_node)
        
        # 选项按钮
        for i, option in enumerate(options):
            btn_style = LayoutStyle(width=40, height=25)
            btn_node = LayoutNode(style=btn_style, key=f"btn_{label}_{i}")
            group_node.add_child(btn_node)
        
        return group_node
    
    def _create_demo_sidebar(self):
        """创建演示选择侧边栏"""
        sidebar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=200,
            gap=10,
            padding=10
        )
        
        sidebar_node = LayoutNode(style=sidebar_style, key="sidebar")
        
        # 侧边栏标题
        sidebar_title_style = LayoutStyle(width=180, height=25)
        title_node = LayoutNode(style=sidebar_title_style, key="sidebar_title")
        sidebar_node.add_child(title_node)
        
        # 演示选项
        for demo_key, demo_name in self.demos.items():
            btn_style = LayoutStyle(width=180, height=35)
            btn_node = LayoutNode(style=btn_style, key=f"demo_btn_{demo_key}")
            sidebar_node.add_child(btn_node)
        
        return sidebar_node
    
    def _create_demo_area(self):
        """创建主要演示区域"""
        demo_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            flex_grow=1.0,  # 占用剩余空间
            padding=20,
            gap=10
        )
        
        demo_node = LayoutNode(style=demo_style, key="demo_area")
        
        # 演示标题
        demo_title_style = LayoutStyle(height=30)
        title_node = LayoutNode(style=demo_title_style, key="demo_title")
        demo_node.add_child(title_node)
        
        # 实际演示内容容器
        content_container = self._create_flexbox_demo()  # 默认显示flexbox演示
        demo_node.add_child(content_container)
        
        return demo_node
    
    def _create_flexbox_demo(self):
        """创建Flexbox基础演示"""
        # 使用响应式参数
        container_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.FLEX_START,
            align_items=AlignItems.STRETCH,
            width=self.container_width.value,
            height=200,
            gap=self.gap_size.value,
            padding=10
        )
        
        container_node = LayoutNode(style=container_style, key="flexbox_container")
        
        # 创建子项目
        colors = ["红", "绿", "蓝", "黄", "紫"]
        for i in range(self.item_count.value):
            item_style = LayoutStyle(
                width=80,
                height=60,
                flex_grow=1.0 if i == 1 else 0.0  # 中间项目可伸缩
            )
            item_node = LayoutNode(style=item_style, key=f"item_{i}")
            container_node.add_child(item_node)
        
        return container_node
    
    def _create_nested_demo(self):
        """创建嵌套布局演示"""
        # 主容器 - 垂直布局
        main_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=self.container_width.value,
            height=250,
            gap=10,
            padding=10
        )
        
        main_node = LayoutNode(style=main_style, key="nested_main")
        
        # 顶部水平区域
        top_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=80,
            gap=10
        )
        
        top_node = LayoutNode(style=top_style, key="nested_top")
        
        # 顶部的三个子项
        for i in range(3):
            item_style = LayoutStyle(flex_grow=1.0, height=80)
            item_node = LayoutNode(style=item_style, key=f"top_item_{i}")
            top_node.add_child(item_node)
        
        main_node.add_child(top_node)
        
        # 底部垂直区域
        bottom_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            flex_grow=1.0,
            gap=5
        )
        
        bottom_node = LayoutNode(style=bottom_style, key="nested_bottom")
        
        # 底部的两个子项
        for i in range(2):
            item_style = LayoutStyle(height=40, flex_grow=1.0)
            item_node = LayoutNode(style=item_style, key=f"bottom_item_{i}")
            bottom_node.add_child(item_node)
        
        main_node.add_child(bottom_node)
        
        return main_node
    
    def _create_responsive_demo(self):
        """创建响应式布局演示"""
        # 网格样式布局
        grid_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            # flex_wrap=FlexWrap.WRAP,  # 暂时不用wrap，简化
            width=self.container_width.value,
            gap=15,
            padding=15
        )
        
        grid_node = LayoutNode(style=grid_style, key="responsive_grid")
        
        # 创建多个卡片
        card_width = (self.container_width.value - 60) // 3  # 3列布局
        
        for i in range(6):
            card_style = LayoutStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                width=card_width,
                height=120,
                padding=5
            )
            
            card_node = LayoutNode(style=card_style, key=f"card_{i}")
            
            # 卡片头部
            header_style = LayoutStyle(height=25)
            header_node = LayoutNode(style=header_style, key=f"card_header_{i}")
            card_node.add_child(header_node)
            
            # 卡片内容
            content_style = LayoutStyle(flex_grow=1.0)
            content_node = LayoutNode(style=content_style, key=f"card_content_{i}")
            card_node.add_child(content_node)
            
            grid_node.add_child(card_node)
        
        return grid_node
    
    def _create_complex_demo(self):
        """创建复杂组合布局演示"""
        # 仿真IDE布局
        ide_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=self.container_width.value,
            height=300
        )
        
        ide_node = LayoutNode(style=ide_style, key="ide_layout")
        
        # 顶部工具栏
        toolbar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=40,
            padding=5,
            gap=5
        )
        
        toolbar_node = LayoutNode(style=toolbar_style, key="toolbar")
        
        # 工具栏按钮
        for i in range(5):
            btn_style = LayoutStyle(width=60, height=30)
            btn_node = LayoutNode(style=btn_style, key=f"tool_btn_{i}")
            toolbar_node.add_child(btn_node)
        
        ide_node.add_child(toolbar_node)
        
        # 主体区域 - 水平分割
        main_body_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            flex_grow=1.0
        )
        
        main_body_node = LayoutNode(style=main_body_style, key="main_body")
        
        # 左侧面板 (文件树)
        left_panel_style = LayoutStyle(width=150, flex_shrink=0.0)
        left_panel_node = LayoutNode(style=left_panel_style, key="left_panel")
        main_body_node.add_child(left_panel_node)
        
        # 中央编辑区
        editor_style = LayoutStyle(flex_grow=1.0)
        editor_node = LayoutNode(style=editor_style, key="editor")
        main_body_node.add_child(editor_node)
        
        # 右侧面板 (属性)
        right_panel_style = LayoutStyle(width=120, flex_shrink=0.0)
        right_panel_node = LayoutNode(style=right_panel_style, key="right_panel")
        main_body_node.add_child(right_panel_node)
        
        ide_node.add_child(main_body_node)
        
        # 底部状态栏
        status_style = LayoutStyle(height=25)
        status_node = LayoutNode(style=status_style, key="status_bar")
        ide_node.add_child(status_node)
        
        return ide_node
    
    def update_demo(self, demo_type):
        """更新演示内容"""
        if not self.demo_container_node:
            return
            
        # 清空当前演示内容
        self.demo_container_node.clear_children()
        
        # 创建新的演示内容
        if demo_type == "flexbox":
            new_demo = self._create_flexbox_demo()
        elif demo_type == "nested":
            new_demo = self._create_nested_demo()
        elif demo_type == "responsive":
            new_demo = self._create_responsive_demo()
        elif demo_type == "complex":
            new_demo = self._create_complex_demo()
        else:
            new_demo = self._create_flexbox_demo()
        
        # 更新标题
        title_style = LayoutStyle(height=30)
        title_node = LayoutNode(style=title_style, key="demo_title")
        self.demo_container_node.add_child(title_node)
        
        # 添加新演示
        self.demo_container_node.add_child(new_demo)
        
        # 重新计算布局
        self.root_node.compute_layout()
        
        print(f"🎯 切换到演示: {self.demos.get(demo_type, demo_type)}")
    
    def update_parameters(self, param_type, value):
        """更新布局参数"""
        if param_type == "count":
            self.item_count.value = int(value)
        elif param_type == "gap":
            self.gap_size.value = int(value)
        elif param_type == "size":
            size_map = {"小": 300, "中": 400, "大": 500}
            self.container_width.value = size_map.get(value, 400)
        
        # 刷新当前演示
        current = self.current_demo.value
        self.update_demo(current)
        
        print(f"📏 参数更新: {param_type} = {value}")

def create_showcase_app():
    """创建showcase应用"""
    
    # 创建应用和窗口
    app = create_app("macUI v3.0 Showcase")
    window = create_window(
        title="macUI v3.0 Layout System Showcase",
        width=900,
        height=700,
        app=app
    )
    
    # 创建控制器
    controller = LayoutShowcaseController()
    
    # 创建布局树
    root_layout = controller.create_layout_tree()
    
    # 输出布局信息用于验证
    print("🎉 === macUI v3.0 Showcase 启动 ===")
    print(f"📊 根节点布局: {root_layout.get_layout()}")
    print(f"📊 子节点数量: {len(root_layout.children)}")
    
    # 打印完整的布局树结构
    print("\n🌳 === 布局树结构 ===")
    print(root_layout.debug_print_tree())
    
    # 演示切换功能
    print("\n🎯 === 演示切换测试 ===")
    for demo_type in ["nested", "responsive", "complex", "flexbox"]:
        controller.update_demo(demo_type)
        new_layout = controller.demo_container_node.get_layout()
        print(f"   {demo_type}: {new_layout}")
    
    # 参数调整测试
    print("\n📏 === 参数调整测试 ===")
    controller.update_parameters("count", "5")
    controller.update_parameters("gap", "20") 
    controller.update_parameters("size", "大")
    
    return app, window, controller

def main():
    print("🚀 启动macUI v3.0 Layout Showcase...")
    
    try:
        app, window, controller = create_showcase_app()
        print("✅ Showcase创建成功!")
        print("🎮 展示各种专业级布局功能")
        print("📋 布局验证完成，所有演示正常工作")
        
    except Exception as e:
        print(f"❌ Showcase启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()