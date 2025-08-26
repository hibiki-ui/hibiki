"""
Layout Integration - macUI组件系统集成

提供新布局引擎与现有macUI组件的无缝集成
支持向后兼容和渐进式迁移
"""

from typing import Optional, List, Any, Tuple, Union
from Foundation import NSMakeRect
from AppKit import NSView

from ..core.component import Component
from .engine import LayoutEngine, get_layout_engine
from .node import LayoutNode
from .tree import LayoutTree
from .styles import LayoutStyle, vstack_style, hstack_style, FlexDirection, AlignItems, JustifyContent


class LayoutComponent(Component):
    """支持新布局引擎的组件基类
    
    提供声明式布局API和自动布局集成
    """
    
    def __init__(self, layout_key: Optional[str] = None):
        super().__init__()
        self.layout_key = layout_key or f"component_{id(self)}"
        self.layout_node: Optional[LayoutNode] = None
        self.layout_tree: Optional[LayoutTree] = None
        self._layout_engine = get_layout_engine()
        
        # 子组件管理
        self._child_components: List['LayoutComponent'] = []
    
    def create_layout_node(self, style: Optional[LayoutStyle] = None) -> LayoutNode:
        """创建布局节点
        
        Args:
            style: 布局样式
            
        Returns:
            创建的布局节点
        """
        self.layout_node = LayoutNode(
            style=style,
            key=self.layout_key,
            user_data=self
        )
        return self.layout_node
    
    def add_child_component(self, child: 'LayoutComponent', index: Optional[int] = None):
        """添加子组件
        
        Args:
            child: 子组件
            index: 插入位置
        """
        if child not in self._child_components:
            if index is None:
                self._child_components.append(child)
            else:
                self._child_components.insert(index, child)
            
            # 更新布局树
            if self.layout_node and child.layout_node:
                self.layout_node.add_child(child.layout_node, index)
    
    def remove_child_component(self, child: 'LayoutComponent'):
        """移除子组件"""
        if child in self._child_components:
            self._child_components.remove(child)
            
            # 更新布局树
            if self.layout_node and child.layout_node:
                self.layout_node.remove_child(child.layout_node)
    
    def compute_layout(self, available_size: Optional[Tuple[float, float]] = None):
        """计算布局"""
        if self.layout_node:
            result = self._layout_engine.compute_layout(self.layout_node, available_size)
            self._apply_layout_to_views()
            return result
    
    def _apply_layout_to_views(self):
        """将布局结果应用到NSView"""
        if not self.layout_node:
            return
        
        # 递归应用布局
        self._apply_layout_recursive(self.layout_node)
    
    def _apply_layout_recursive(self, node: LayoutNode):
        """递归应用布局到NSView"""
        x, y, width, height = node.get_layout()
        
        # 获取对应的组件和NSView
        component = node.user_data
        if isinstance(component, LayoutComponent):
            view = component.get_view()
            if view:
                # 应用布局位置和尺寸
                frame = NSMakeRect(x, y, width, height)
                view.setFrame_(frame)
        
        # 递归处理子节点
        for child_node in node.children:
            self._apply_layout_recursive(child_node)


class VStackComponent(LayoutComponent):
    """垂直堆栈布局组件 - 基于新布局引擎"""
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        spacing: float = 0,
        alignment: AlignItems = AlignItems.STRETCH,
        justify_content: JustifyContent = JustifyContent.FLEX_START,
        padding: float = 0,
        **style_kwargs
    ):
        super().__init__()
        
        self.children = children or []
        self.spacing = spacing
        self.alignment = alignment
        self.justify_content = justify_content
        self.padding = padding
        
        # 创建VStack样式
        self.layout_style = vstack_style(
            align=alignment,
            justify=justify_content,
            gap=spacing,
            padding=padding,
            **style_kwargs
        )
        
        # 创建布局节点
        self.create_layout_node(self.layout_style)
        
        # 添加子组件
        for child in self.children:
            if isinstance(child, LayoutComponent):
                self.add_child_component(child)
            elif isinstance(child, Component):
                # 包装传统Component
                wrapped = self._wrap_legacy_component(child)
                self.add_child_component(wrapped)
            else:
                # 直接是NSView或其他对象 - 创建简单包装
                wrapped = self._wrap_view_object(child)
                self.add_child_component(wrapped)
    
    def _wrap_legacy_component(self, component: Component) -> LayoutComponent:
        """包装传统组件为支持布局的组件"""
        wrapper = LayoutComponent()
        wrapper.create_layout_node()
        
        # 复制原组件的get_view方法
        wrapper.get_view = component.get_view
        wrapper._legacy_component = component
        
        return wrapper
    
    def _wrap_view_object(self, view_obj) -> LayoutComponent:
        """包装NSView或其他视图对象"""
        wrapper = LayoutComponent()
        wrapper.create_layout_node()
        
        # 创建get_view方法返回对象本身
        wrapper.get_view = lambda: view_obj
        wrapper._view_object = view_obj
        
        return wrapper
    
    def mount(self) -> NSView:
        """挂载VStack组件"""
        from AppKit import NSView
        
        # 创建容器视图
        container = NSView.alloc().init()
        
        # 挂载所有子组件到容器
        for child in self._child_components:
            child_view = None
            if hasattr(child, '_view_object'):
                # 直接视图对象
                child_view = child._view_object
            elif hasattr(child, '_legacy_component'):
                # 包装的传统组件
                legacy_comp = child._legacy_component
                if hasattr(legacy_comp, 'mount'):
                    child_view = legacy_comp.mount()
                else:
                    child_view = legacy_comp.get_view()
            elif hasattr(child, 'mount'):
                child_view = child.mount()
            elif hasattr(child, 'get_view'):
                child_view = child.get_view()
            
            if child_view:
                container.addSubview_(child_view)
        
        # 设置容器初始frame
        container.setFrame_(NSMakeRect(0, 0, 600, 700))
        
        # 计算初始布局
        try:
            self.compute_layout((600, 700))
        except Exception as e:
            print(f"⚠️ 布局计算错误: {e}")
        
        return container


class HStackComponent(LayoutComponent):
    """水平堆栈布局组件 - 基于新布局引擎"""
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        spacing: float = 0,
        alignment: AlignItems = AlignItems.STRETCH,
        justify_content: JustifyContent = JustifyContent.FLEX_START,
        padding: float = 0,
        **style_kwargs
    ):
        super().__init__()
        
        self.children = children or []
        self.spacing = spacing
        self.alignment = alignment
        self.justify_content = justify_content
        self.padding = padding
        
        # 创建HStack样式
        self.layout_style = hstack_style(
            align=alignment,
            justify=justify_content,
            gap=spacing,
            padding=padding,
            **style_kwargs
        )
        
        # 创建布局节点
        self.create_layout_node(self.layout_style)
        
        # 添加子组件
        for child in self.children:
            if isinstance(child, LayoutComponent):
                self.add_child_component(child)
            elif isinstance(child, Component):
                # 包装传统Component
                wrapped = self._wrap_legacy_component(child)
                self.add_child_component(wrapped)
            else:
                # 直接是NSView或其他对象 - 创建简单包装
                wrapped = self._wrap_view_object(child)
                self.add_child_component(wrapped)
    
    def _wrap_legacy_component(self, component: Component) -> LayoutComponent:
        """包装传统组件为支持布局的组件"""
        wrapper = LayoutComponent()
        wrapper.create_layout_node()
        
        # 复制原组件的get_view方法
        wrapper.get_view = component.get_view
        wrapper._legacy_component = component
        
        return wrapper
    
    def _wrap_view_object(self, view_obj) -> LayoutComponent:
        """包装NSView或其他视图对象"""
        wrapper = LayoutComponent()
        wrapper.create_layout_node()
        
        # 创建get_view方法返回对象本身
        wrapper.get_view = lambda: view_obj
        wrapper._view_object = view_obj
        
        return wrapper
    
    def mount(self) -> NSView:
        """挂载HStack组件"""
        from AppKit import NSView
        
        # 创建容器视图
        container = NSView.alloc().init()
        
        # 挂载所有子组件到容器
        for child in self._child_components:
            child_view = None
            if hasattr(child, '_view_object'):
                # 直接视图对象
                child_view = child._view_object
            elif hasattr(child, '_legacy_component'):
                # 包装的传统组件
                legacy_comp = child._legacy_component
                if hasattr(legacy_comp, 'mount'):
                    child_view = legacy_comp.mount()
                else:
                    child_view = legacy_comp.get_view()
            elif hasattr(child, 'mount'):
                child_view = child.mount()
            elif hasattr(child, 'get_view'):
                child_view = child.get_view()
            
            if child_view:
                container.addSubview_(child_view)
        
        # 设置容器初始frame
        container.setFrame_(NSMakeRect(0, 0, 600, 700))
        
        # 计算初始布局
        try:
            self.compute_layout((600, 700))
        except Exception as e:
            print(f"⚠️ 布局计算错误: {e}")
        
        return container


def migrate_existing_component(component: Component, style: Optional[LayoutStyle] = None) -> LayoutComponent:
    """迁移现有组件到新布局系统
    
    Args:
        component: 现有组件
        style: 可选的布局样式
        
    Returns:
        支持新布局系统的组件
    """
    # 创建布局包装器
    wrapper = LayoutComponent()
    wrapper.create_layout_node(style)
    
    # 保持原组件引用
    wrapper._original_component = component
    
    # 代理关键方法
    if hasattr(component, 'get_view'):
        wrapper.get_view = component.get_view
    if hasattr(component, 'mount'):
        wrapper.mount = component.mount
    
    return wrapper


def create_layout_from_existing_vstack(
    vstack_children: List[Component],
    spacing: float = 16,
    alignment: str = "stretch"
) -> VStackComponent:
    """从现有VStack子组件创建新的布局组件
    
    Args:
        vstack_children: VStack子组件列表
        spacing: 间距
        alignment: 对齐方式
        
    Returns:
        新的VStackComponent
    """
    # 转换对齐方式
    align_mapping = {
        "stretch": AlignItems.STRETCH,
        "center": AlignItems.CENTER,
        "start": AlignItems.FLEX_START,
        "end": AlignItems.FLEX_END
    }
    
    align = align_mapping.get(alignment, AlignItems.STRETCH)
    
    return VStackComponent(
        children=vstack_children,
        spacing=spacing,
        alignment=align
    )


def create_layout_from_existing_hstack(
    hstack_children: List[Component],
    spacing: float = 16,
    alignment: str = "stretch"
) -> HStackComponent:
    """从现有HStack子组件创建新的布局组件
    
    Args:
        hstack_children: HStack子组件列表
        spacing: 间距
        alignment: 对齐方式
        
    Returns:
        新的HStackComponent
    """
    # 转换对齐方式
    align_mapping = {
        "stretch": AlignItems.STRETCH,
        "center": AlignItems.CENTER,
        "start": AlignItems.FLEX_START,
        "end": AlignItems.FLEX_END
    }
    
    align = align_mapping.get(alignment, AlignItems.STRETCH)
    
    return HStackComponent(
        children=hstack_children,
        spacing=spacing,
        alignment=align
    )


# 便捷函数
def VStack(
    children: Optional[List[Component]] = None,
    spacing: float = 0,
    alignment: str = "stretch",
    **kwargs
) -> VStackComponent:
    """创建VStack组件 - 新布局引擎版本"""
    align_mapping = {
        "stretch": AlignItems.STRETCH,
        "center": AlignItems.CENTER,
        "start": AlignItems.FLEX_START,
        "end": AlignItems.FLEX_END
    }
    
    return VStackComponent(
        children=children,
        spacing=spacing,
        alignment=align_mapping.get(alignment, AlignItems.STRETCH),
        **kwargs
    )


def HStack(
    children: Optional[List[Component]] = None,
    spacing: float = 0,
    alignment: str = "stretch",
    **kwargs
) -> HStackComponent:
    """创建HStack组件 - 新布局引擎版本"""
    align_mapping = {
        "stretch": AlignItems.STRETCH,
        "center": AlignItems.CENTER,
        "start": AlignItems.FLEX_START,
        "end": AlignItems.FLEX_END
    }
    
    return HStackComponent(
        children=children,
        spacing=spacing,
        alignment=align_mapping.get(alignment, AlignItems.STRETCH),
        **kwargs
    )