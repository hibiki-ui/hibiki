"""
布局组件 - 传统布局组件和容器

提供传统的布局组件如TableView, ScrollView等
现在VStack/HStack已经由modern_layout.py中的现代化版本替代
"""

from typing import Any, List, Optional, Union

from AppKit import (
    NSCollectionView,
    NSLayoutAttributeBottom,
    NSLayoutAttributeCenterX,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSOutlineView,
    NSScrollView,
    NSSplitView,
    NSStackView,
    NSStackViewDistributionGravityAreas,
    NSStackViewDistributionFill,
    NSStackViewDistributionFillEqually,
    NSStackViewDistributionFillProportionally,
    NSStackViewDistributionEqualSpacing,
    NSStackViewDistributionEqualCentering,
    NSTableColumn,
    NSTableView,
    NSTabView,
    NSTabViewItem,
    NSUserInterfaceLayoutOrientationHorizontal,
    NSUserInterfaceLayoutOrientationVertical,
    NSView,
)
from Foundation import NSEdgeInsets, NSMakeRect

from ..core.component import Component
from ..core.signal import Signal

# 对齐方式映射
ALIGNMENT_MAP = {
    "leading": NSLayoutAttributeLeading,
    "trailing": NSLayoutAttributeTrailing,
    "center": NSLayoutAttributeCenterX,
    "top": NSLayoutAttributeTop,
    "bottom": NSLayoutAttributeBottom,
    "centerY": NSLayoutAttributeCenterY,
}


# ================================
# 传统布局组件 (保留用于向后兼容)
# ================================

def VStack(
    children: Optional[List[Union[Any, Component]]] = None,
    spacing: Union[int, float] = 0,
    padding: Union[int, float, tuple] = 0,
    alignment: str = "leading",
    frame: Optional[tuple] = None
) -> NSStackView:
    """创建垂直堆栈布局 - 传统实现
    
    注意：现在推荐使用 modern_layout.ModernVStack 获得更好的布局能力
    
    Args:
        children: 子视图列表
        spacing: 子视图间距
        padding: 内边距
        alignment: 对齐方式 ("leading", "center", "trailing")
        frame: 容器框架 (x, y, width, height)
    
    Returns:
        NSStackView 实例
    """
    if not children:
        children = []
    
    print(f"⚠️ 使用传统VStack，推荐升级到ModernVStack")
    
    stack = NSStackView.alloc().init()
    stack.setOrientation_(NSUserInterfaceLayoutOrientationVertical)  # 1 = Vertical
    stack.setSpacing_(spacing)
    
    # 设置对齐
    align_attr = ALIGNMENT_MAP.get(alignment, NSLayoutAttributeLeading)
    stack.setAlignment_(align_attr)
    
    # 添加子视图
    for child in children:
        view = child
        if hasattr(child, 'mount'):
            view = child.mount()
        elif hasattr(child, 'get_view'):
            view = child.get_view()
        
        if view:
            stack.addArrangedSubview_(view)
    
    # 设置frame
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
    else:
        # 设置默认frame
        stack.setFrame_(NSMakeRect(0, 0, 300, 200))
    
    return stack


def HStack(
    children: Optional[List[Union[Any, Component]]] = None,
    spacing: Union[int, float] = 0,
    padding: Union[int, float, tuple] = 0,
    alignment: str = "center",
    frame: Optional[tuple] = None
) -> NSStackView:
    """创建水平堆栈布局 - 传统实现
    
    注意：现在推荐使用 modern_layout.ModernHStack 获得更好的布局能力
    
    Args:
        children: 子视图列表
        spacing: 子视图间距
        padding: 内边距
        alignment: 对齐方式 ("top", "center", "bottom")
        frame: 容器框架 (x, y, width, height)
    
    Returns:
        NSStackView 实例
    """
    if not children:
        children = []
    
    print(f"⚠️ 使用传统HStack，推荐升级到ModernHStack")
    
    stack = NSStackView.alloc().init()
    stack.setOrientation_(NSUserInterfaceLayoutOrientationHorizontal)  # 0 = Horizontal
    stack.setSpacing_(spacing)
    
    # 设置对齐
    align_attr = ALIGNMENT_MAP.get(alignment, NSLayoutAttributeCenterY)
    stack.setAlignment_(align_attr)
    
    # 添加子视图
    for child in children:
        view = child
        if hasattr(child, 'mount'):
            view = child.mount()
        elif hasattr(child, 'get_view'):
            view = child.get_view()
        
        if view:
            stack.addArrangedSubview_(view)
    
    # 设置frame
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
    else:
        # 设置默认frame
        stack.setFrame_(NSMakeRect(0, 0, 400, 100))
    
    return stack


def ZStack(
    children: Optional[List[Any]] = None,
    frame: Optional[tuple] = None
) -> NSView:
    """创建层叠布局（子视图层叠在一起）
    
    Args:
        children: 子视图列表
        frame: 容器框架 (x, y, width, height)
    
    Returns:
        NSView 实例
    """
    container = NSView.alloc().init()
    
    if frame:
        container.setFrame_(NSMakeRect(*frame))
    
    if children:
        for child in children:
            view = child
            if hasattr(child, 'mount'):
                view = child.mount()
            elif hasattr(child, 'get_view'):
                view = child.get_view()
            
            if view:
                container.addSubview_(view)
    
    return container


def ScrollView(
    content: Optional[Any] = None,
    frame: Optional[tuple] = None,
    has_vertical_scroller: bool = True,
    has_horizontal_scroller: bool = False
) -> NSScrollView:
    """创建滚动视图
    
    Args:
        content: 内容视图
        frame: 滚动视图框架
        has_vertical_scroller: 是否显示垂直滚动条
        has_horizontal_scroller: 是否显示水平滚动条
    
    Returns:
        NSScrollView 实例
    """
    scroll_view = NSScrollView.alloc().init()
    
    if frame:
        scroll_view.setFrame_(NSMakeRect(*frame))
    
    scroll_view.setHasVerticalScroller_(has_vertical_scroller)
    scroll_view.setHasHorizontalScroller_(has_horizontal_scroller)
    scroll_view.setAutohidesScrollers_(True)
    
    if content:
        content_view = content
        if hasattr(content, 'mount'):
            content_view = content.mount()
        elif hasattr(content, 'get_view'):
            content_view = content.get_view()
        
        if content_view:
            scroll_view.setDocumentView_(content_view)
    
    return scroll_view


def TabView(
    tabs: Optional[List[dict]] = None,
    frame: Optional[tuple] = None
) -> NSTabView:
    """创建标签页视图
    
    Args:
        tabs: 标签页配置列表 [{"title": str, "content": view}, ...]
        frame: 标签页视图框架
    
    Returns:
        NSTabView 实例
    """
    tab_view = NSTabView.alloc().init()
    
    if frame:
        tab_view.setFrame_(NSMakeRect(*frame))
    
    if tabs:
        for tab_config in tabs:
            title = tab_config.get("title", "Tab")
            content = tab_config.get("content")
            
            tab_item = NSTabViewItem.alloc().init()
            tab_item.setLabel_(title)
            
            if content:
                content_view = content
                if hasattr(content, 'mount'):
                    content_view = content.mount()
                elif hasattr(content, 'get_view'):
                    content_view = content.get_view()
                
                if content_view:
                    tab_item.setView_(content_view)
            
            tab_view.addTabViewItem_(tab_item)
    
    return tab_view


def SplitView(
    views: Optional[List[Any]] = None,
    vertical: bool = False,
    frame: Optional[tuple] = None
) -> NSSplitView:
    """创建分割视图
    
    Args:
        views: 子视图列表
        vertical: 是否为垂直分割
        frame: 分割视图框架
    
    Returns:
        NSSplitView 实例
    """
    split_view = NSSplitView.alloc().init()
    split_view.setVertical_(vertical)
    
    if frame:
        split_view.setFrame_(NSMakeRect(*frame))
    
    if views:
        for view_item in views:
            view = view_item
            if hasattr(view_item, 'mount'):
                view = view_item.mount()
            elif hasattr(view_item, 'get_view'):
                view = view_item.get_view()
            
            if view:
                split_view.addSubview_(view)
    
    return split_view


def TableView(
    columns: List[dict],
    data: Optional[Union[List[dict], Signal[List[dict]]]] = None,
    headers_visible: bool = True,
    on_select: Optional[Any] = None,
    on_double_click: Optional[Any] = None,
    selected_row: Optional[Signal[int]] = None,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建表格视图 - 优化版本，支持在任何布局中使用
    
    Args:
        columns: 列配置 [{"title": str, "key": str, "width": float}, ...]
        data: 表格数据或Signal
        headers_visible: 是否显示表头
        on_select: 行选择回调
        on_double_click: 双击回调
        selected_row: 选中行Signal
        frame: 表格框架
    
    Returns:
        NSScrollView 实例（包含 NSTableView）
    """
    # 创建滚动视图
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setFrame_(NSMakeRect(0, 0, 400, 300) if not frame else NSMakeRect(*frame))
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(True)
    scroll_view.setAutohidesScrollers_(True)
    
    # 创建表格视图
    table_view = NSTableView.alloc().init()
    table_view.setFrame_(NSMakeRect(0, 0, 400, 300))
    table_view.setHeaderView_(None if not headers_visible else table_view.headerView())
    
    # 创建列
    for col_config in columns:
        title = col_config.get("title", "")
        key = col_config.get("key", title)
        width = col_config.get("width", 100.0)
        
        column = NSTableColumn.alloc().init()
        column.setIdentifier_(key)
        column.setWidth_(width)
        
        if headers_visible:
            column.headerCell().setStringValue_(title)
        
        table_view.addTableColumn_(column)
    
    # 设置表格到滚动视图
    scroll_view.setDocumentView_(table_view)
    
    # 创建数据源
    from ..core.binding import EnhancedTableViewDataSource
    
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.columns = [col.get("key", col.get("title", "")) for col in columns]
    
    # 设置数据
    if data is not None:
        if isinstance(data, Signal):
            # 响应式数据绑定
            def update_table_data():
                try:
                    data_source.data = data.value
                    table_view.reloadData()
                except Exception as e:
                    print(f"❌ TableView数据更新错误: {e}")
            
            from ..core.signal import Effect
            effect = Effect(update_table_data)
            
            # 保持Effect引用
            import objc
            objc.setAssociatedObject(scroll_view, b"table_data_effect", effect, objc.OBJC_ASSOCIATION_RETAIN)
        else:
            data_source.data = data
    
    # 设置数据源
    table_view.setDataSource_(data_source)
    
    # 保持数据源引用
    import objc
    objc.setAssociatedObject(scroll_view, b"table_data_source", data_source, objc.OBJC_ASSOCIATION_RETAIN)
    
    # 事件处理
    if on_select or on_double_click or (isinstance(selected_row, Signal)):
        from ..core.binding import EnhancedTableViewDelegate
        
        delegate = EnhancedTableViewDelegate.alloc().init()
        delegate.on_select = on_select
        delegate.on_double_click = on_double_click
        delegate.selected_signal = selected_row if isinstance(selected_row, Signal) else None
        
        table_view.setDelegate_(delegate)
        
        # 保持委托引用
        objc.setAssociatedObject(scroll_view, b"table_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return scroll_view


def OutlineView(
    data: Optional[List[dict]] = None,
    columns: Optional[List[dict]] = None,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建大纲视图
    
    Args:
        data: 层次数据
        columns: 列配置
        frame: 大纲视图框架
    
    Returns:
        NSScrollView 实例（包含 NSOutlineView）
    """
    scroll_view = NSScrollView.alloc().init()
    
    if frame:
        scroll_view.setFrame_(NSMakeRect(*frame))
    else:
        scroll_view.setFrame_(NSMakeRect(0, 0, 300, 200))
    
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setAutohidesScrollers_(True)
    
    outline_view = NSOutlineView.alloc().init()
    scroll_view.setDocumentView_(outline_view)
    
    # 简单实现，可以根据需要扩展
    return scroll_view


# ================================
# 响应式布局工具 (保留用于特殊用途)
# ================================

def ResponsiveStack(
    children: Optional[List[Any]] = None,
    vertical: bool = True,
    spacing: Union[int, float] = 8
) -> NSStackView:
    """响应式堆栈布局 - 根据内容自动调整
    
    Args:
        children: 子视图列表
        vertical: 是否为垂直布局
        spacing: 间距
    
    Returns:
        NSStackView 实例
    """
    if vertical:
        return VStack(children, spacing=spacing)
    else:
        return HStack(children, spacing=spacing)