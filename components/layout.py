from typing import List, Optional, Union, Any
from core.signal import Signal, Computed
from core.component import Component

from AppKit import (
    NSView, NSStackView, NSScrollView,
    NSUserInterfaceLayoutOrientationVertical,
    NSUserInterfaceLayoutOrientationHorizontal,
    NSLayoutAttributeLeading, NSLayoutAttributeTrailing,
    NSLayoutAttributeTop, NSLayoutAttributeBottom,
    NSLayoutAttributeCenterX, NSLayoutAttributeCenterY
)
from Foundation import NSMakeRect, NSEdgeInsets

# 对齐方式映射
ALIGNMENT_MAP = {
    'leading': NSLayoutAttributeLeading,
    'trailing': NSLayoutAttributeTrailing,
    'center': NSLayoutAttributeCenterX,
    'top': NSLayoutAttributeTop,
    'bottom': NSLayoutAttributeBottom,
    'centerY': NSLayoutAttributeCenterY,
}


def VStack(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = 'center',
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSStackView:
    """
    创建垂直堆栈布局
    
    Args:
        spacing: 子视图间距
        padding: 内边距 (单个值或 (top, left, bottom, right) 元组)
        alignment: 对齐方式 ('leading', 'trailing', 'center', 'top', 'bottom')
        children: 子视图列表
        frame: 堆栈框架 (x, y, width, height)
    
    Returns:
        NSStackView 实例
    """
    stack = NSStackView.alloc().init()
    stack.setOrientation_(NSUserInterfaceLayoutOrientationVertical)
    
    # 设置框架
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
    
    # 设置间距
    stack.setSpacing_(spacing)
    
    # 设置对齐
    alignment_constant = ALIGNMENT_MAP.get(alignment, NSLayoutAttributeCenterX)
    stack.setAlignment_(alignment_constant)
    
    # 设置内边距
    if isinstance(padding, (int, float)):
        insets = NSEdgeInsets(padding, padding, padding, padding)
    elif isinstance(padding, tuple) and len(padding) == 4:
        insets = NSEdgeInsets(*padding)
    else:
        insets = NSEdgeInsets(0, 0, 0, 0)
    
    stack.setEdgeInsets_(insets)
    
    # 添加子视图
    if children:
        for child in children:
            child_view = child.get_view() if isinstance(child, Component) else child
            if child_view:
                stack.addArrangedSubview_(child_view)
    
    return stack


def HStack(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = 'center',
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSStackView:
    """
    创建水平堆栈布局
    
    Args:
        spacing: 子视图间距
        padding: 内边距 (单个值或 (top, left, bottom, right) 元组)
        alignment: 对齐方式 ('leading', 'trailing', 'center', 'top', 'bottom')
        children: 子视图列表
        frame: 堆栈框架 (x, y, width, height)
    
    Returns:
        NSStackView 实例
    """
    stack = NSStackView.alloc().init()
    stack.setOrientation_(NSUserInterfaceLayoutOrientationHorizontal)
    
    # 设置框架
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
    
    # 设置间距
    stack.setSpacing_(spacing)
    
    # 设置对齐
    alignment_constant = ALIGNMENT_MAP.get(alignment, NSLayoutAttributeCenterY)
    stack.setAlignment_(alignment_constant)
    
    # 设置内边距
    if isinstance(padding, (int, float)):
        insets = NSEdgeInsets(padding, padding, padding, padding)
    elif isinstance(padding, tuple) and len(padding) == 4:
        insets = NSEdgeInsets(*padding)
    else:
        insets = NSEdgeInsets(0, 0, 0, 0)
    
    stack.setEdgeInsets_(insets)
    
    # 添加子视图
    if children:
        for child in children:
            child_view = child.get_view() if isinstance(child, Component) else child
            if child_view:
                stack.addArrangedSubview_(child_view)
    
    return stack


def ZStack(
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSView:
    """
    创建层叠堆栈布局 (所有子视图重叠)
    
    Args:
        children: 子视图列表
        frame: 堆栈框架 (x, y, width, height)
    
    Returns:
        NSView 实例
    """
    stack = NSView.alloc().init()
    
    # 设置框架
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
    
    # 添加子视图 (所有子视图会重叠显示)
    if children:
        for child in children:
            child_view = child.get_view() if isinstance(child, Component) else child
            if child_view:
                stack.addSubview_(child_view)
    
    return stack


def ScrollView(
    content: Union[Any, Component],
    frame: Optional[tuple] = None,
    has_vertical_scroller: bool = True,
    has_horizontal_scroller: bool = False,
    autohides_scrollers: bool = True
) -> NSScrollView:
    """
    创建滚动视图
    
    Args:
        content: 滚动内容视图
        frame: 滚动视图框架 (x, y, width, height)
        has_vertical_scroller: 是否显示垂直滚动条
        has_horizontal_scroller: 是否显示水平滚动条
        autohides_scrollers: 是否自动隐藏滚动条
    
    Returns:
        NSScrollView 实例
    """
    scroll_view = NSScrollView.alloc().init()
    
    # 设置框架
    if frame:
        scroll_view.setFrame_(NSMakeRect(*frame))
    
    # 配置滚动条
    scroll_view.setHasVerticalScroller_(has_vertical_scroller)
    scroll_view.setHasHorizontalScroller_(has_horizontal_scroller)
    scroll_view.setAutohidesScrollers_(autohides_scrollers)
    
    # 设置文档视图
    content_view = content.get_view() if isinstance(content, Component) else content
    if content_view:
        scroll_view.setDocumentView_(content_view)
    
    return scroll_view


class ResponsiveStack(Component):
    """响应式堆栈组件 - 子视图可以动态添加/移除"""
    
    def __init__(
        self, 
        orientation: str = 'vertical',
        spacing: float = 0,
        padding: Union[float, tuple] = 0,
        alignment: str = 'center',
        children: Optional[Signal[List[Component]]] = None
    ):
        super().__init__()
        self.orientation = orientation
        self.spacing = spacing
        self.padding = padding
        self.alignment = alignment
        self.children_signal = children or self.create_signal([])
        self._current_views: List[Any] = []
    
    def mount(self) -> NSStackView:
        """创建并返回堆栈视图"""
        stack = NSStackView.alloc().init()
        orientation = (NSUserInterfaceLayoutOrientationVertical 
                     if self.orientation == 'vertical' 
                     else NSUserInterfaceLayoutOrientationHorizontal)
        stack.setOrientation_(orientation)
        
        # 配置堆栈属性
        stack.setSpacing_(self.spacing)
        
        alignment_key = self.alignment
        if self.orientation == 'horizontal' and alignment_key == 'center':
            alignment_key = 'centerY'
        alignment_constant = ALIGNMENT_MAP.get(alignment_key, NSLayoutAttributeCenterX)
        stack.setAlignment_(alignment_constant)
        
        # 设置内边距
        if isinstance(self.padding, (int, float)):
            insets = NSEdgeInsets(self.padding, self.padding, self.padding, self.padding)
        elif isinstance(self.padding, tuple) and len(self.padding) == 4:
            insets = NSEdgeInsets(*self.padding)
        else:
            insets = NSEdgeInsets(0, 0, 0, 0)
        
        stack.setEdgeInsets_(insets)
        
        # 响应式更新子视图
        def update_children():
            # 移除现有子视图
            for view in self._current_views:
                stack.removeArrangedSubview_(view)
            self._current_views.clear()
            
            # 添加新子视图
            for child in self.children_signal.value:
                child_view = child.get_view() if isinstance(child, Component) else child
                if child_view:
                    self._current_views.append(child_view)
                    stack.addArrangedSubview_(child_view)
        
        # 创建响应式更新
        self.create_effect(update_children)
        
        return stack
    
    def add_child(self, child: Component) -> None:
        """添加子组件"""
        current_children = self.children_signal.value.copy()
        current_children.append(child)
        self.children_signal.value = current_children
    
    def remove_child(self, child: Component) -> None:
        """移除子组件"""
        current_children = self.children_signal.value.copy()
        if child in current_children:
            current_children.remove(child)
            self.children_signal.value = current_children
    
    def clear_children(self) -> None:
        """清空所有子组件"""
        self.children_signal.value = []


# 便捷构造函数
def VStackResponsive(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = 'center',
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式垂直堆栈"""
    return ResponsiveStack('vertical', spacing, padding, alignment, children)


def HStackResponsive(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = 'center',
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式水平堆栈"""
    return ResponsiveStack('horizontal', spacing, padding, alignment, children)