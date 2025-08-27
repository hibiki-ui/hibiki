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


class ModernVStack(LayoutAwareComponent):
    """现代化垂直布局组件 - 基于Stretchable布局引擎
    
    完全替代旧的VStack NSStackView实现
    提供CSS Flexbox标准的布局能力
    """
    
    def __init__(
        self,
        children: Optional[List[Union[LayoutAwareComponent, Component, Any]]] = None,
        spacing: Union[int, float] = 0,
        alignment: Union[AlignItems, str] = AlignItems.STRETCH,
        justify_content: Union[JustifyContent, str] = JustifyContent.FLEX_START,
        padding: Union[int, float] = 0,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化垂直布局
        
        Args:
            children: 子组件列表
            spacing: 子组件间距
            alignment: 水平对齐方式 (AlignItems枚举或字符串)
            justify_content: 垂直分布方式 (JustifyContent枚举或字符串)  
            padding: 内边距
            width: 容器宽度
            height: 容器高度
            **layout_kwargs: 其他布局样式参数
        """
        # 字符串到枚举的转换
        if isinstance(alignment, str):
            align_map = {
                "start": AlignItems.FLEX_START,
                "center": AlignItems.CENTER,
                "end": AlignItems.FLEX_END,
                "stretch": AlignItems.STRETCH
            }
            alignment = align_map.get(alignment, AlignItems.STRETCH)
        
        if isinstance(justify_content, str):
            justify_map = {
                "start": JustifyContent.FLEX_START,
                "center": JustifyContent.CENTER,
                "end": JustifyContent.FLEX_END,
                "space-between": JustifyContent.SPACE_BETWEEN,
                "space-around": JustifyContent.SPACE_AROUND,
                "space-evenly": JustifyContent.SPACE_EVENLY
            }
            justify_content = justify_map.get(justify_content, JustifyContent.FLEX_START)
        
        # 创建VStack样式
        layout_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=alignment,
            justify_content=justify_content,
            gap=spacing,
            padding=padding,
            width=width,
            height=height,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.children = children or []
        self.child_components: List[LayoutAwareComponent] = []
        
        # 处理子组件
        self._process_children()
    
    def _process_children(self):
        """处理和包装子组件"""
        for child in self.children:
            if isinstance(child, LayoutAwareComponent):
                # 已经是现代化组件
                self.child_components.append(child)
            elif isinstance(child, Component):
                # 传统Component，需要包装
                wrapped = self._wrap_legacy_component(child)
                self.child_components.append(wrapped)
            else:
                # 直接的NSView或其他对象
                wrapped = self._wrap_view_object(child)
                self.child_components.append(wrapped)
    
    def _wrap_legacy_component(self, component: Component) -> LayoutAwareComponent:
        """包装传统组件"""
        from .core import LegacyComponentWrapper
        return LegacyComponentWrapper(component)
    
    def _wrap_view_object(self, view_obj) -> LayoutAwareComponent:
        """包装视图对象"""
        from .core import LegacyComponentWrapper
        return LegacyComponentWrapper(view_obj)
    
    def add_child(self, child: Union[LayoutAwareComponent, Component, Any]) -> 'ModernVStack':
        """添加子组件 - 支持链式调用"""
        self.children.append(child)
        
        # 处理新增的子组件
        if isinstance(child, LayoutAwareComponent):
            wrapped_child = child
        elif isinstance(child, Component):
            wrapped_child = self._wrap_legacy_component(child)
        else:
            wrapped_child = self._wrap_view_object(child)
        
        self.child_components.append(wrapped_child)
        
        # 更新布局树
        if self.layout_node:
            child_node = wrapped_child.create_layout_node()
            self.layout_node.add_child(child_node)
        
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
        container = self._nsview
        
        # 挂载所有子组件
        for child_component in self.child_components:
            try:
                child_view = child_component.get_view()
                if child_view:
                    # 🔴 禁用子视图的AutoLayout
                    child_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
                    container.addSubview_(child_view)
            except Exception as e:
                print(f"⚠️ 子组件挂载失败: {e}")
        
        # 创建布局树结构
        self._setup_layout_tree()
        
        print(f"🔧 ModernVStack 创建完成，子组件数: {len(self.child_components)}")
    
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
            return
            
        try:
            # 计算布局
            result = self.compute_layout()
            
            # 首先应用自己容器的布局
            self.apply_layout_to_view()
            
            # 然后应用到所有子组件
            self._apply_layout_recursive(self.layout_node)
            
            print(f"✅ ModernVStack 布局计算完成: {result.compute_time:.2f}ms")
            
        except Exception as e:
            print(f"⚠️ ModernVStack 布局计算失败: {e}")
    
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


class ModernHStack(LayoutAwareComponent):
    """现代化水平布局组件 - 基于Stretchable布局引擎"""
    
    def __init__(
        self,
        children: Optional[List[Union[LayoutAwareComponent, Component, Any]]] = None,
        spacing: Union[int, float] = 0,
        alignment: Union[AlignItems, str] = AlignItems.STRETCH,
        justify_content: Union[JustifyContent, str] = JustifyContent.FLEX_START,
        padding: Union[int, float] = 0,
        # 布局样式支持  
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化水平布局 - 参数与ModernVStack类似，但使用ROW方向"""
        
        # 字符串到枚举的转换
        if isinstance(alignment, str):
            align_map = {
                "start": AlignItems.FLEX_START,
                "center": AlignItems.CENTER, 
                "end": AlignItems.FLEX_END,
                "stretch": AlignItems.STRETCH
            }
            alignment = align_map.get(alignment, AlignItems.STRETCH)
        
        if isinstance(justify_content, str):
            justify_map = {
                "start": JustifyContent.FLEX_START,
                "center": JustifyContent.CENTER,
                "end": JustifyContent.FLEX_END,
                "space-between": JustifyContent.SPACE_BETWEEN,
                "space-around": JustifyContent.SPACE_AROUND,
                "space-evenly": JustifyContent.SPACE_EVENLY
            }
            justify_content = justify_map.get(justify_content, JustifyContent.FLEX_START)
        
        # 创建HStack样式
        layout_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,  # 水平方向
            align_items=alignment,
            justify_content=justify_content,
            gap=spacing,
            padding=padding,
            width=width,
            height=height,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.children = children or []
        self.child_components: List[LayoutAwareComponent] = []
        
        # 处理子组件（复用VStack的逻辑）
        self._process_children()
    
    def _process_children(self):
        """处理和包装子组件 - 与VStack相同的逻辑"""
        for child in self.children:
            if isinstance(child, LayoutAwareComponent):
                self.child_components.append(child)
            elif isinstance(child, Component):
                wrapped = self._wrap_legacy_component(child)
                self.child_components.append(wrapped)
            else:
                wrapped = self._wrap_view_object(child)
                self.child_components.append(wrapped)
    
    def _wrap_legacy_component(self, component: Component) -> LayoutAwareComponent:
        """包装传统组件"""
        from .core import LegacyComponentWrapper
        return LegacyComponentWrapper(component)
    
    def _wrap_view_object(self, view_obj) -> LayoutAwareComponent:
        """包装视图对象"""
        from .core import LegacyComponentWrapper
        return LegacyComponentWrapper(view_obj)
    
    def add_child(self, child: Union[LayoutAwareComponent, Component, Any]) -> 'ModernHStack':
        """添加子组件 - 支持链式调用"""
        self.children.append(child)
        
        if isinstance(child, LayoutAwareComponent):
            wrapped_child = child
        elif isinstance(child, Component):
            wrapped_child = self._wrap_legacy_component(child)
        else:
            wrapped_child = self._wrap_view_object(child)
        
        self.child_components.append(wrapped_child)
        
        # 更新布局树
        if self.layout_node:
            child_node = wrapped_child.create_layout_node()
            self.layout_node.add_child(child_node)
        
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
        
        print(f"🔧 ModernHStack 创建完成，子组件数: {len(self.child_components)}")
    
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
            
            print(f"✅ ModernHStack 布局计算完成: {result.compute_time:.2f}ms")
        except Exception as e:
            print(f"⚠️ ModernHStack 布局计算失败: {e}")
    
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
    spacing: Union[int, float] = 0,
    alignment: str = "stretch",
    justify_content: str = "start",
    **kwargs
) -> ModernVStack:
    """创建现代化垂直布局 - 向后兼容接口
    
    Examples:
        # 基本用法（兼容旧API）
        vstack = VStack(children=[button, label], spacing=16)
        
        # 新功能 - 布局属性
        vstack = VStack(
            children=[button, label],
            spacing=16,
            alignment="center",
            width=400,
            padding=20
        )
        
        # 链式调用
        vstack = VStack(children=[button, label]) \
            .width(400) \
            .padding(20) \
            .margin(16)
    """
    return ModernVStack(
        children=children,
        spacing=spacing,
        alignment=alignment,
        justify_content=justify_content,
        **kwargs
    )


def HStack(
    children: Optional[List[Union[LayoutAwareComponent, Component, Any]]] = None,
    spacing: Union[int, float] = 0,
    alignment: str = "stretch", 
    justify_content: str = "start",
    **kwargs
) -> ModernHStack:
    """创建现代化水平布局 - 向后兼容接口"""
    return ModernHStack(
        children=children,
        spacing=spacing,
        alignment=alignment,
        justify_content=justify_content,
        **kwargs
    )


# 便捷构造函数
def CenteredVStack(
    children: Optional[List] = None,
    spacing: Union[int, float] = 16,
    **kwargs
) -> ModernVStack:
    """居中的垂直布局"""
    return ModernVStack(
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
) -> ModernHStack:
    """居中的水平布局"""
    return ModernHStack(
        children=children,
        spacing=spacing,
        alignment=AlignItems.CENTER,
        justify_content=JustifyContent.CENTER,
        **kwargs
    )


def FlexVStack(
    children: Optional[List] = None,
    **kwargs
) -> ModernVStack:
    """弹性垂直布局 - 平均分布空间"""
    return ModernVStack(
        children=children,
        justify_content=JustifyContent.SPACE_BETWEEN,
        **kwargs
    )


def FlexHStack(
    children: Optional[List] = None,
    **kwargs
) -> ModernHStack:
    """弹性水平布局 - 平均分布空间"""
    return ModernHStack(
        children=children,
        justify_content=JustifyContent.SPACE_BETWEEN,
        **kwargs
    )