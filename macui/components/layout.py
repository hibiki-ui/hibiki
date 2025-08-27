"""
现代化布局组件 - 基于新布局引擎v3.0 (Stretchable)

提供基于LayoutAwareComponent的现代化布局组件
完全替代旧的NSStackView hack实现，提供CSS-like布局API
"""

from typing import List, Optional, Union, Any
from AppKit import NSView
from Foundation import NSMakeRect

from ..core.component import Component
from ..layout.styles import (
    LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display,
    vstack_style, hstack_style
)
from .core import LayoutAwareComponent


class VStackLayout(LayoutAwareComponent):
    """现代化垂直布局组件 - 基于Stretchable布局引擎
    
    完全替代旧的VStack NSStackView实现
    提供CSS Flexbox标准的布局能力
    """
    
    def __init__(
        self,
        children: Optional[List[LayoutAwareComponent]] = None,
        style: Optional[LayoutStyle] = None
    ):
        """初始化现代化垂直布局
        
        Args:
            children: 子组件列表
            style: 布局样式 (LayoutStyle对象)
        """
        # 创建默认VStack样式或使用提供的样式
        if style is None:
            layout_style = LayoutStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.STRETCH,
                justify_content=JustifyContent.FLEX_START
            )
        else:
            layout_style = style
            # 确保是垂直布局
            layout_style.display = Display.FLEX
            layout_style.flex_direction = FlexDirection.COLUMN
        
        print(f"🔧 VStackLayout.__init__ 开始，子组件数: {len(children or [])}")
        super().__init__(layout_style)
        print("🔧 super().__init__ 完成")
        
        self.children = children or []
        self.child_components: List[LayoutAwareComponent] = []
        
        # 处理子组件
        print("🔧 开始处理子组件")
        self._process_children()
        print("🔧 子组件处理完成")
    
    def _process_children(self):
        """处理子组件 - 仅支持LayoutAwareComponent"""
        for child in self.children:
            if isinstance(child, LayoutAwareComponent):
                # 现代化组件，直接使用
                self.child_components.append(child)
            else:
                # 不支持的组件类型
                raise TypeError(f"不支持的子组件类型: {type(child).__name__}. 请使用macUI统一API组件 (Label, Button, VStack等)")
    
    
    def add_child(self, child: LayoutAwareComponent) -> 'VStackLayout':
        """添加子组件 - 支持链式调用"""
        self.children.append(child)
        
        # 处理新增的子组件
        if isinstance(child, LayoutAwareComponent):
            self.child_components.append(child)
            
            # 更新布局树
            if self.layout_node:
                child_node = child.create_layout_node()
                self.layout_node.add_child(child_node)
        else:
            raise TypeError(f"不支持的子组件类型: {type(child).__name__}. 请使用macUI统一API组件 (Label, Button, VStack等)")
        
        return self
    
    def _create_nsview(self) -> NSView:
        """创建容器NSView"""
        container = NSView.alloc().init()
        
        # 🔴 关键修复：禁用AutoLayout，完全使用手动布局
        container.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # 设置默认大小
        default_width = self.layout_style.width or 400
        default_height = self.layout_style.height or 300
        container.setFrame_(NSMakeRect(0, 0, default_width, default_height))
        
        return container
    
    def _setup_nsview(self):
        """设置容器和子组件"""
        print("🔧 VStackLayout._setup_nsview 开始")
        container = self._nsview
        print(f"🔧 容器获取完成: {container}")
        
        # 挂载所有子组件
        print(f"🔧 准备挂载 {len(self.child_components)} 个子组件")
        for i, child_component in enumerate(self.child_components):
            try:
                print(f"🔧 挂载子组件 {i}: {child_component}")
                child_view = child_component.get_view()
                print(f"🔧 子组件视图获取完成: {child_view}")
                if child_view:
                    # 🔴 禁用子视图的AutoLayout
                    child_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
                    container.addSubview_(child_view)
                    print(f"✅ 子组件 {i} 挂载完成")
            except Exception as e:
                print(f"⚠️ 子组件挂载失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 创建布局树结构
        print("🔧 开始创建布局树结构")
        self._setup_layout_tree()
        
        print(f"🔧 VStackLayout 创建完成，子组件数: {len(self.child_components)}")
    
    def _setup_layout_tree(self):
        """设置布局树结构"""
        # 创建根布局节点
        root_node = self.create_layout_node()
        
        # 添加子组件的布局节点
        for child_component in self.child_components:
            child_node = child_component.create_layout_node()
            root_node.add_child(child_node)
        
        # 计算初始布局
        self._compute_and_apply_layout()
    
    def _compute_and_apply_layout(self):
        """计算并应用布局"""
        if not self.layout_node:
            print("⚠️ layout_node 不存在，跳过布局计算")
            return
            
        try:
            print("🔄 开始计算布局...")
            # 计算布局
            result = self.compute_layout()
            print(f"✅ 布局计算完成: {result}")
            
            # 首先应用自己容器的布局
            print("📐 应用容器布局...")
            self.apply_layout_to_view()
            
            # 然后应用到所有子组件
            print("📐 应用子组件布局...")
            self._apply_layout_recursive(self.layout_node)
            
            print(f"✅ VStackLayout 布局计算完成: {result.compute_time:.2f}ms")
            
        except Exception as e:
            print(f"⚠️ VStackLayout 布局计算失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _apply_layout_recursive(self, node):
        """递归应用布局到视图"""
        # 跳过根节点自己(已经在外面应用过)
        if node != self.layout_node:
            # 应用当前节点布局
            if node.user_data and hasattr(node.user_data, 'apply_layout_to_view'):
                node.user_data.apply_layout_to_view()
            elif node.user_data and hasattr(node.user_data, '_nsview'):
                # 直接设置frame
                x, y, w, h = node.get_layout()
                frame = NSMakeRect(x, y, w, h)
                node.user_data._nsview.setFrame_(frame)
                print(f"📐 应用子组件布局: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        
        # 递归处理子节点
        for child_node in node.children:
            self._apply_layout_recursive(child_node)


class HStackLayout(LayoutAwareComponent):
    """现代化水平布局组件 - 基于Stretchable布局引擎"""
    
    def __init__(
        self,
        children: Optional[List[LayoutAwareComponent]] = None,
        style: Optional[LayoutStyle] = None
    ):
        """初始化现代化水平布局
        
        Args:
            children: 子组件列表
            style: 布局样式 (LayoutStyle对象)
        """
        
        # 创建默认HStack样式或使用提供的样式
        if style is None:
            layout_style = LayoutStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                align_items=AlignItems.STRETCH,
                justify_content=JustifyContent.FLEX_START
            )
        else:
            layout_style = style
            # 确保是水平布局
            layout_style.display = Display.FLEX
            layout_style.flex_direction = FlexDirection.ROW
        
        super().__init__(layout_style)
        
        self.children = children or []
        self.child_components: List[LayoutAwareComponent] = []
        
        # 处理子组件（复用VStack的逻辑）
        self._process_children()
    
    def _process_children(self):
        """处理子组件 - 仅支持LayoutAwareComponent"""
        for child in self.children:
            if isinstance(child, LayoutAwareComponent):
                # 现代化组件，直接使用
                self.child_components.append(child)
            else:
                # 不支持的组件类型
                raise TypeError(f"不支持的子组件类型: {type(child).__name__}. 请使用macUI统一API组件 (Label, Button, HStack等)")
    
    
    def add_child(self, child: LayoutAwareComponent) -> 'HStackLayout':
        """添加子组件 - 支持链式调用"""
        self.children.append(child)
        
        # 处理新增的子组件
        if isinstance(child, LayoutAwareComponent):
            self.child_components.append(child)
            
            # 更新布局树
            if self.layout_node:
                child_node = child.create_layout_node()
                self.layout_node.add_child(child_node)
        else:
            raise TypeError(f"不支持的子组件类型: {type(child).__name__}. 请使用macUI统一API组件 (Label, Button, HStack等)")
        
        return self
    
    def _create_nsview(self) -> NSView:
        """创建容器NSView"""
        container = NSView.alloc().init()
        
        # 🔴 关键修复：禁用AutoLayout，完全使用手动布局
        container.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # 设置默认大小
        default_width = self.layout_style.width or 600
        default_height = self.layout_style.height or 60
        container.setFrame_(NSMakeRect(0, 0, default_width, default_height))
        
        return container
    
    def _setup_nsview(self):
        """设置容器和子组件 - 与VStack相同的逻辑"""
        container = self._nsview
        
        # 挂载所有子组件
        for child_component in self.child_components:
            try:
                child_view = child_component.get_view()
                if child_view:
                    container.addSubview_(child_view)
            except Exception as e:
                print(f"⚠️ HStack子组件挂载失败: {e}")
        
        # 创建布局树结构
        self._setup_layout_tree()
        
        print(f"🔧 HStackLayout 创建完成，子组件数: {len(self.child_components)}")
    
    def _setup_layout_tree(self):
        """设置布局树结构 - 与VStack相同的逻辑"""
        root_node = self.create_layout_node()
        
        for child_component in self.child_components:
            child_node = child_component.create_layout_node()
            root_node.add_child(child_node)
        
        self._compute_and_apply_layout()
    
    def _compute_and_apply_layout(self):
        """计算并应用布局"""
        if not self.layout_node:
            return
            
        try:
            result = self.compute_layout()
            
            # 首先应用自己容器的布局
            self.apply_layout_to_view()
            
            # 然后应用到所有子组件
            self._apply_layout_recursive(self.layout_node)
            
            print(f"✅ HStackLayout 布局计算完成: {result.compute_time:.2f}ms")
        except Exception as e:
            print(f"⚠️ HStackLayout 布局计算失败: {e}")
    
    def _apply_layout_recursive(self, node):
        """递归应用布局到视图 - 与VStack相同的逻辑"""
        # 跳过根节点自己(已经在外面应用过)
        if node != self.layout_node:
            # 应用当前节点布局
            if node.user_data and hasattr(node.user_data, 'apply_layout_to_view'):
                node.user_data.apply_layout_to_view()
            elif node.user_data and hasattr(node.user_data, '_nsview'):
                x, y, w, h = node.get_layout()
                frame = NSMakeRect(x, y, w, h)
                node.user_data._nsview.setFrame_(frame)
                print(f"📐 应用HStack子组件布局: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        
        for child_node in node.children:
            self._apply_layout_recursive(child_node)


# 向后兼容的函数式接口
def VStack(
    children: Optional[List[Union[LayoutAwareComponent, Component, Any]]] = None,
    style: Optional[LayoutStyle] = None
) -> VStackLayout:
    """创建现代化垂直布局 - 统一style接口
    
    Args:
        children: 子组件列表
        style: 布局样式对象
    
    Examples:
        # 基本用法
        vstack = VStack(children=[button, label])
        
        # 使用style控制布局
        vstack = VStack(
            children=[button, label],
            style=LayoutStyle(
                gap=16,
                align_items=AlignItems.CENTER,
                padding=20
            )
        )
    """
    return VStackLayout(
        children=children,
        style=style
    )


def HStack(
    children: Optional[List[Union[LayoutAwareComponent, Component, Any]]] = None,
    style: Optional[LayoutStyle] = None
) -> HStackLayout:
    """创建现代化水平布局 - 统一style接口
    
    Args:
        children: 子组件列表
        style: 布局样式对象
    
    Examples:
        # 基本用法
        hstack = HStack(children=[button1, button2])
        
        # 使用style控制布局
        hstack = HStack(
            children=[button1, button2],
            style=LayoutStyle(
                gap=10,
                justify_content=JustifyContent.SPACE_BETWEEN,
                padding=15
            )
        )
    """
    return HStackLayout(
        children=children,
        style=style
    )


# 便捷构造函数
def CenteredVStack(
    children: Optional[List] = None,
    spacing: Union[int, float] = 16,
    **kwargs
) -> VStackLayout:
    """居中的垂直布局"""
    return VStackLayout(
        children=children,
        spacing=spacing,
        alignment=AlignItems.CENTER,
        justify_content=JustifyContent.CENTER,
        **kwargs
    )


def CenteredHStack(
    children: Optional[List] = None,
    spacing: Union[int, float] = 16,
    **kwargs
) -> HStackLayout:
    """居中的水平布局"""
    return HStackLayout(
        children=children,
        spacing=spacing,
        alignment=AlignItems.CENTER,
        justify_content=JustifyContent.CENTER,
        **kwargs
    )


def FlexVStack(
    children: Optional[List] = None,
    **kwargs
) -> VStackLayout:
    """弹性垂直布局 - 平均分布空间"""
    return VStackLayout(
        children=children,
        justify_content=JustifyContent.SPACE_BETWEEN,
        **kwargs
    )


def FlexHStack(
    children: Optional[List] = None,
    **kwargs
) -> HStackLayout:
    """弹性水平布局 - 平均分布空间"""
    return HStackLayout(
        children=children,
        justify_content=JustifyContent.SPACE_BETWEEN,
        **kwargs
    )