#!/usr/bin/env python3
"""
macUI v3.0 布局系统核心功能展示
专注于验证Stretchable布局引擎的各种布局能力
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.layout.node import LayoutNode
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display

class LayoutShowcase:
    """布局系统功能展示"""
    
    def __init__(self):
        self.demos = []
        self.current_demo = 0
    
    def create_flexbox_basics_demo(self):
        """演示1: Flexbox基础功能"""
        print("\n🎯 === Flexbox基础功能演示 ===")
        
        # 水平布局容器
        hstack_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.SPACE_BETWEEN,
            align_items=AlignItems.CENTER,
            width=500,
            height=100,
            gap=20,
            padding=10
        )
        
        container = LayoutNode(style=hstack_style, key="hstack_demo")
        
        # 创建不同尺寸的子项
        sizes = [(80, 60), (120, 80), (100, 70)]
        for i, (w, h) in enumerate(sizes):
            item_style = LayoutStyle(width=w, height=h)
            item = LayoutNode(style=item_style, key=f"item_{i}")
            container.add_child(item)
        
        # 计算布局
        container.compute_layout()
        
        # 显示结果
        self._print_layout_tree(container)
        self._analyze_spacing(container, "SPACE_BETWEEN")
        
        return container
    
    def create_nested_layout_demo(self):
        """演示2: 嵌套布局复杂性"""
        print("\n🎯 === 嵌套布局复杂性演示 ===")
        
        # 主容器 - 垂直布局
        main_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=400,
            height=300,
            gap=15,
            padding=20
        )
        
        main_container = LayoutNode(style=main_style, key="main_container")
        
        # 顶部区域 - 水平布局
        top_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=80,
            gap=10,
            justify_content=JustifyContent.FLEX_START
        )
        
        top_section = LayoutNode(style=top_style, key="top_section")
        
        # 顶部三个项目
        for i in range(3):
            item_style = LayoutStyle(
                width=100,
                height=80,
                flex_grow=1.0 if i == 1 else 0.0  # 中间项可伸缩
            )
            item = LayoutNode(style=item_style, key=f"top_item_{i}")
            top_section.add_child(item)
        
        main_container.add_child(top_section)
        
        # 中间区域 - 单个拉伸项目
        middle_style = LayoutStyle(
            height=60,
            flex_grow=1.0  # 占用剩余空间
        )
        middle_item = LayoutNode(style=middle_style, key="middle_item")
        main_container.add_child(middle_item)
        
        # 底部区域 - 水平布局，居中对齐
        bottom_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER,
            height=50,
            gap=15
        )
        
        bottom_section = LayoutNode(style=bottom_style, key="bottom_section")
        
        # 底部两个按钮
        for i in range(2):
            btn_style = LayoutStyle(width=80, height=30)
            btn = LayoutNode(style=btn_style, key=f"bottom_btn_{i}")
            bottom_section.add_child(btn)
        
        main_container.add_child(bottom_section)
        
        # 计算布局
        main_container.compute_layout()
        
        # 显示结果
        self._print_layout_tree(main_container)
        
        return main_container
    
    def create_flex_grow_demo(self):
        """演示3: Flex-grow动态分配空间"""
        print("\n🎯 === Flex-grow动态空间分配演示 ===")
        
        # 容器
        container_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            width=600,
            height=80,
            gap=10,
            padding=10
        )
        
        container = LayoutNode(style=container_style, key="flex_container")
        
        # 不同flex-grow值的项目
        grow_values = [1.0, 2.0, 1.0, 3.0]  # 按比例分配剩余空间
        
        for i, grow_value in enumerate(grow_values):
            item_style = LayoutStyle(
                width=50,  # 最小宽度
                height=60,
                flex_grow=grow_value
            )
            item = LayoutNode(style=item_style, key=f"flex_item_{i}")
            container.add_child(item)
        
        # 计算布局
        container.compute_layout()
        
        # 显示结果和分析
        self._print_layout_tree(container)
        self._analyze_flex_distribution(container, grow_values)
        
        return container
    
    def create_alignment_demo(self):
        """演示4: 对齐方式组合"""
        print("\n🎯 === 对齐方式组合演示 ===")
        
        # 主容器
        main_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=400,
            height=400,
            gap=20,
            padding=20
        )
        
        main_container = LayoutNode(style=main_style, key="alignment_demo")
        
        # 不同对齐方式的容器
        alignment_configs = [
            (JustifyContent.FLEX_START, AlignItems.FLEX_START, "左上"),
            (JustifyContent.CENTER, AlignItems.CENTER, "居中"),
            (JustifyContent.FLEX_END, AlignItems.FLEX_END, "右下"),
            (JustifyContent.SPACE_BETWEEN, AlignItems.STRETCH, "分散拉伸")
        ]
        
        for justify, align, name in alignment_configs:
            # 子容器
            sub_style = LayoutStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=justify,
                align_items=align,
                height=80,
                gap=10
            )
            
            sub_container = LayoutNode(style=sub_style, key=f"sub_{name}")
            
            # 添加小项目
            for i in range(3):
                item_style = LayoutStyle(
                    width=40,
                    height=30 if align != AlignItems.STRETCH else None  # STRETCH时不设置高度
                )
                item = LayoutNode(style=item_style, key=f"{name}_item_{i}")
                sub_container.add_child(item)
            
            main_container.add_child(sub_container)
        
        # 计算布局
        main_container.compute_layout()
        
        # 显示结果
        self._print_layout_tree(main_container)
        
        return main_container
    
    def create_complex_layout_demo(self):
        """演示5: 复杂真实场景布局"""
        print("\n🎯 === 复杂真实场景布局演示 (仿IDE界面) ===")
        
        # IDE主界面布局
        ide_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=800,
            height=600
        )
        
        ide_container = LayoutNode(style=ide_style, key="ide_interface")
        
        # 顶部菜单栏
        menubar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=30,
            justify_content=JustifyContent.SPACE_BETWEEN,
            align_items=AlignItems.CENTER,
            padding=5
        )
        
        menubar = LayoutNode(style=menubar_style, key="menubar")
        
        # 菜单项目
        menu_items = ["文件", "编辑", "查看", "运行"]
        for item in menu_items:
            menu_style = LayoutStyle(width=60, height=20)
            menu_node = LayoutNode(style=menu_style, key=f"menu_{item}")
            menubar.add_child(menu_node)
        
        ide_container.add_child(menubar)
        
        # 工具栏
        toolbar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=40,
            gap=5,
            padding=5
        )
        
        toolbar = LayoutNode(style=toolbar_style, key="toolbar")
        
        # 工具按钮
        for i in range(8):
            tool_style = LayoutStyle(width=35, height=30)
            tool_btn = LayoutNode(style=tool_style, key=f"tool_{i}")
            toolbar.add_child(tool_btn)
        
        ide_container.add_child(toolbar)
        
        # 主体工作区域 - 三栏布局
        workspace_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            flex_grow=1.0  # 占用剩余空间
        )
        
        workspace = LayoutNode(style=workspace_style, key="workspace")
        
        # 左侧面板 (项目浏览器)
        left_panel_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=200,
            flex_shrink=0.0  # 固定宽度，不收缩
        )
        
        left_panel = LayoutNode(style=left_panel_style, key="project_browser")
        
        # 左侧面板内容
        left_header_style = LayoutStyle(height=30)
        left_header = LayoutNode(style=left_header_style, key="left_header")
        left_panel.add_child(left_header)
        
        left_content_style = LayoutStyle(flex_grow=1.0)
        left_content = LayoutNode(style=left_content_style, key="left_content")
        left_panel.add_child(left_content)
        
        workspace.add_child(left_panel)
        
        # 中央编辑器区域
        editor_area_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            flex_grow=1.0  # 占用主要空间
        )
        
        editor_area = LayoutNode(style=editor_area_style, key="editor_area")
        
        # 标签栏
        tab_bar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=35
        )
        
        tab_bar = LayoutNode(style=tab_bar_style, key="tab_bar")
        
        # 文件标签
        tabs = ["main.py", "utils.py", "config.json"]
        for tab in tabs:
            tab_style = LayoutStyle(width=100, height=35)
            tab_node = LayoutNode(style=tab_style, key=f"tab_{tab}")
            tab_bar.add_child(tab_node)
        
        editor_area.add_child(tab_bar)
        
        # 编辑器内容
        editor_content_style = LayoutStyle(flex_grow=1.0)
        editor_content = LayoutNode(style=editor_content_style, key="editor_content")
        editor_area.add_child(editor_content)
        
        workspace.add_child(editor_area)
        
        # 右侧面板 (属性和输出)
        right_panel_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=250,
            flex_shrink=0.0
        )
        
        right_panel = LayoutNode(style=right_panel_style, key="properties_panel")
        
        # 属性区域
        props_style = LayoutStyle(height=200)
        props_area = LayoutNode(style=props_style, key="properties")
        right_panel.add_child(props_area)
        
        # 输出区域
        output_style = LayoutStyle(flex_grow=1.0)
        output_area = LayoutNode(style=output_style, key="output")
        right_panel.add_child(output_area)
        
        workspace.add_child(right_panel)
        
        ide_container.add_child(workspace)
        
        # 底部状态栏
        statusbar_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            height=25,
            justify_content=JustifyContent.SPACE_BETWEEN,
            align_items=AlignItems.CENTER,
            padding=5
        )
        
        statusbar = LayoutNode(style=statusbar_style, key="statusbar")
        
        # 状态信息
        status_left_style = LayoutStyle(width=200, height=15)
        status_left = LayoutNode(style=status_left_style, key="status_left")
        statusbar.add_child(status_left)
        
        status_right_style = LayoutStyle(width=100, height=15)
        status_right = LayoutNode(style=status_right_style, key="status_right")
        statusbar.add_child(status_right)
        
        ide_container.add_child(statusbar)
        
        # 计算布局
        ide_container.compute_layout()
        
        # 显示结果
        self._print_layout_tree(ide_container, max_depth=2)  # 限制深度避免输出太长
        
        return ide_container
    
    def _print_layout_tree(self, node, indent=0, max_depth=None):
        """打印布局树结构"""
        if max_depth is not None and indent > max_depth:
            return
            
        prefix = "  " * indent
        x, y, w, h = node.get_layout()
        
        print(f"{prefix}📦 {node.key}: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        
        for child in node.children:
            self._print_layout_tree(child, indent + 1, max_depth)
    
    def _analyze_spacing(self, container, justify_type):
        """分析间距分布"""
        if len(container.children) < 2:
            return
            
        children = container.children
        layouts = [child.get_layout() for child in children]
        
        print(f"\n📏 间距分析 ({justify_type}):")
        for i in range(len(layouts) - 1):
            current_x, _, current_w, _ = layouts[i]
            next_x, _, _, _ = layouts[i + 1]
            
            gap = next_x - (current_x + current_w)
            print(f"   项目{i} -> 项目{i+1}: 间距 {gap:.1f}px")
    
    def _analyze_flex_distribution(self, container, expected_grows):
        """分析flex-grow空间分配"""
        print(f"\n📊 Flex-grow空间分配分析:")
        
        container_layout = container.get_layout()
        container_width = container_layout[2]
        
        # 计算可用空间 (总宽度 - padding - gaps - 固定内容)
        style = container.style
        padding = (getattr(style, 'padding_left', 0) or 0) + (getattr(style, 'padding_right', 0) or 0)
        gap_total = (getattr(style, 'gap', 0) or 0) * (len(container.children) - 1)
        
        fixed_width = len(container.children) * 50  # 每个项目的基础宽度
        available_space = container_width - padding - gap_total - fixed_width
        
        total_grow = sum(expected_grows)
        
        print(f"   容器总宽度: {container_width:.1f}px")
        print(f"   可分配空间: {available_space:.1f}px")
        print(f"   总grow值: {total_grow}")
        
        for i, (child, expected_grow) in enumerate(zip(container.children, expected_grows)):
            x, y, w, h = child.get_layout()
            expected_extra = (expected_grow / total_grow) * available_space
            expected_total_width = 50 + expected_extra
            
            print(f"   项目{i}: 实际宽度{w:.1f}px, 期望{expected_total_width:.1f}px, grow={expected_grow}")
    
    def run_all_demos(self):
        """运行所有演示"""
        print("🚀 === macUI v3.0 Stretchable布局系统全功能展示 ===")
        
        demos = [
            self.create_flexbox_basics_demo,
            self.create_nested_layout_demo,
            self.create_flex_grow_demo,
            self.create_alignment_demo,
            self.create_complex_layout_demo
        ]
        
        results = []
        for i, demo_func in enumerate(demos, 1):
            try:
                print(f"\n{'='*50}")
                print(f"演示 {i}/5")
                result = demo_func()
                results.append(result)
                print("✅ 演示成功完成")
            except Exception as e:
                print(f"❌ 演示失败: {e}")
                import traceback
                traceback.print_exc()
                results.append(None)
        
        # 总结
        print(f"\n{'='*50}")
        print("🎉 === 展示总结 ===")
        successful = sum(1 for r in results if r is not None)
        print(f"成功完成: {successful}/5 个演示")
        
        if successful == 5:
            print("🏆 macUI v3.0 Stretchable布局系统功能完备!")
            print("✅ 支持复杂嵌套、flex-grow、多种对齐方式")
            print("✅ 适合构建专业级应用界面")
        else:
            print("⚠️ 部分演示存在问题，需要进一步调试")
        
        return results

def main():
    showcase = LayoutShowcase()
    showcase.run_all_demos()

if __name__ == "__main__":
    main()