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


def VStack(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSStackView:
    """创建垂直堆栈布局
    
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
    alignment: str = "center",
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSStackView:
    """创建水平堆栈布局
    
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
    """创建层叠堆栈布局 (所有子视图重叠)
    
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
    """创建滚动视图
    
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
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(scroll_view, frame)

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
        orientation: str = "vertical",
        spacing: float = 0,
        padding: Union[float, tuple] = 0,
        alignment: str = "center",
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
                     if self.orientation == "vertical"
                     else NSUserInterfaceLayoutOrientationHorizontal)
        stack.setOrientation_(orientation)

        # 配置堆栈属性
        stack.setSpacing_(self.spacing)

        alignment_key = self.alignment
        if self.orientation == "horizontal" and alignment_key == "center":
            alignment_key = "centerY"
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
    alignment: str = "center",
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式垂直堆栈"""
    return ResponsiveStack("vertical", spacing, padding, alignment, children)


def HStackResponsive(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式水平堆栈"""
    return ResponsiveStack("horizontal", spacing, padding, alignment, children)


def TabView(
    tabs: List[dict],  # [{"title": str, "content": Component}, ...]
    selected: Optional[Union[int, Signal[int]]] = None,
    on_change: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSTabView:
    """创建标签页视图
    
    Args:
        tabs: 标签页配置列表，每个项目是一个字典：{"title": str, "content": Component}
        selected: 当前选中的标签页索引 (支持响应式)
        on_change: 标签页切换回调函数 (index, tab_item)
        frame: 标签页视图框架
    
    Returns:
        NSTabView 实例
    """
    tab_view = NSTabView.alloc().init()
    
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(tab_view, frame)
    
    # 添加标签页
    for tab_config in tabs:
        title = tab_config.get("title", "")
        content = tab_config.get("content")
        
        # 创建标签页项
        tab_item = NSTabViewItem.alloc().init()
        tab_item.setLabel_(title)
        
        if content:
            # 如果content是Component，需要获取其view
            if hasattr(content, 'get_view'):
                view = content.get_view()
            elif hasattr(content, 'mount'):
                view = content.mount()
            else:
                view = content
            tab_item.setView_(view)
        
        tab_view.addTabViewItem_(tab_item)
    
    # 设置初始选中的标签页
    if selected is not None:
        if isinstance(selected, Signal):
            # 响应式绑定选中索引
            from ..core.binding import TwoWayBinding
            TwoWayBinding.bind_tab_view(tab_view, selected)
        else:
            if 0 <= selected < len(tabs):
                tab_view.selectTabViewItemAtIndex_(selected)
    
    # 事件处理
    if on_change or (isinstance(selected, Signal)):
        from ..core.binding import EnhancedTabViewDelegate
        # 创建标签页委托
        delegate = EnhancedTabViewDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = selected if isinstance(selected, Signal) else None
        
        tab_view.setDelegate_(delegate)
        
        # 保持委托引用 - 使用内存管理器
        from ..core.memory_manager import associate_object
        associate_object(tab_view, "enhanced_tab_delegate", delegate)
    
    return tab_view


def SplitView(
    orientation: str = "horizontal",  # "horizontal" or "vertical"
    children: Optional[List[Any]] = None,
    divider_style: str = "thin",  # "thin" or "thick"
    on_resize: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSSplitView:
    """创建分割视图
    
    Args:
        orientation: 分割方向 ("horizontal" 或 "vertical")
        children: 子视图列表
        divider_style: 分隔符样式 ("thin" 或 "thick")
        on_resize: 尺寸调整回调函数
        frame: 分割视图框架
    
    Returns:
        NSSplitView 实例
    """
    split_view = NSSplitView.alloc().init()
    
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(split_view, frame)
    
    # 设置分割方向
    from AppKit import NSSplitViewDividerStyleThin, NSSplitViewDividerStyleThick
    if orientation == "vertical":
        split_view.setVertical_(True)
    else:
        split_view.setVertical_(False)
    
    # 设置分隔符样式
    if divider_style == "thick":
        split_view.setDividerStyle_(NSSplitViewDividerStyleThick)
    else:
        split_view.setDividerStyle_(NSSplitViewDividerStyleThin)
    
    # 添加子视图
    if children:
        for child in children:
            # 如果child是Component，需要获取其view
            if hasattr(child, 'get_view'):
                view = child.get_view()
            elif hasattr(child, 'mount'):
                view = child.mount()
            else:
                view = child
            split_view.addSubview_(view)
    
    # 事件处理
    if on_resize:
        from ..core.binding import EnhancedSplitViewDelegate
        # 创建分割视图委托
        delegate = EnhancedSplitViewDelegate.alloc().init()
        delegate.on_resize = on_resize
        
        split_view.setDelegate_(delegate)
        
        # 保持委托引用 - 使用内存管理器
        from ..core.memory_manager import associate_object
        associate_object(split_view, "enhanced_split_delegate", delegate)
    
    return split_view


def TableView(
    columns: List[dict],  # [{"title": str, "key": str, "width": float}, ...]
    data: Optional[Union[List[Any], Signal[List[Any]]]] = None,
    selected_row: Optional[Union[int, Signal[int]]] = None,
    on_select: Optional[Any] = None,
    on_double_click: Optional[Any] = None,
    headers_visible: bool = True,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建表格视图
    
    Args:
        columns: 列配置列表，每个项目是一个字典：{"title": str, "key": str, "width": float}
        data: 表格数据 (支持响应式)
        selected_row: 当前选中的行索引 (支持响应式)
        on_select: 行选择回调函数
        on_double_click: 双击行回调函数
        headers_visible: 是否显示表头
        frame: 表格视图框架
    
    Returns:
        NSScrollView 实例（包含 NSTableView）
    """
    # 创建滚动视图
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(True)
    scroll_view.setAutohidesScrollers_(True)
    
    # 创建表格视图
    table_view = NSTableView.alloc().init()
    table_view.setHeaderView_(None if not headers_visible else table_view.headerView())
    
    # 创建列
    for col_config in columns:
        title = col_config.get("title", "")
        key = col_config.get("key", title)
        width = col_config.get("width", 100.0)
        
        column = NSTableColumn.alloc().init()
        column.setIdentifier_(key)
        column.setWidth_(width)
        
        # 设置列标题
        if headers_visible:
            column.headerCell().setStringValue_(title)
        
        table_view.addTableColumn_(column)
    
    # 设置表格到滚动视图
    scroll_view.setDocumentView_(table_view)
    
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(scroll_view, frame)
    
    # 创建数据源 - 使用正确的内存管理
    from ..core.binding import EnhancedTableViewDataSource
    
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.columns = [col.get("key", col.get("title", "")) for col in columns]
    
    # 设置数据
    if data is not None:
        if isinstance(data, Signal):
            # 响应式数据绑定
            def update_table_data():
                try:
                    print(f"📊 更新表格数据: {len(data.value) if data.value else 0} 行")
                    data_source.data = data.value
                    table_view.reloadData()
                except Exception as e:
                    print(f"❌ 数据更新错误: {e}")
            
            from ..core.signal import Effect
            effect = Effect(update_table_data)
            
            # 使用内存管理器保持 Effect 引用
            from ..core.memory_manager import associate_object
            associate_object(scroll_view, "table_data_effect", effect)
            
        else:
            data_source.data = data
    
    # 设置数据源并使用内存管理器保持引用
    table_view.setDataSource_(data_source)
    
    # 使用内存管理器保持数据源引用 - 这是关键！
    from ..core.memory_manager import associate_object
    associate_object(scroll_view, "table_data_source", data_source)
    
    # 事件处理
    if on_select or on_double_click or (isinstance(selected_row, Signal)):
        from ..core.binding import EnhancedTableViewDelegate
        
        # 创建表格委托
        delegate = EnhancedTableViewDelegate.alloc().init()
        delegate.on_select = on_select
        delegate.on_double_click = on_double_click
        delegate.selected_signal = selected_row if isinstance(selected_row, Signal) else None
        
        table_view.setDelegate_(delegate)
        
        # 使用内存管理器保持委托引用
        associate_object(scroll_view, "table_delegate", delegate)
        
        # 设置双击动作
        if on_double_click:
            table_view.setDoubleAction_("tableViewDoubleClick:")
            table_view.setTarget_(delegate)
    
    return scroll_view


def OutlineView(
    columns: List[dict],  # [{"title": str, "key": str, "width": float}, ...]
    root_items: Optional[List[Any]] = None,
    get_children: Optional[Any] = None,  # 函数，用于获取子项
    is_expandable: Optional[Any] = None,  # 函数，用于判断是否可展开
    on_select: Optional[Any] = None,
    on_expand: Optional[Any] = None,
    on_collapse: Optional[Any] = None,
    headers_visible: bool = True,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建大纲视图（树形视图）
    
    Args:
        columns: 列配置列表，每个项目是一个字典：{"title": str, "key": str, "width": float}
        root_items: 根级项目列表
        get_children: 获取子项的函数 (item) -> [children]
        is_expandable: 判断是否可展开的函数 (item) -> bool
        on_select: 选择项回调函数 (row, item)
        on_expand: 展开项回调函数 (item)
        on_collapse: 收缩项回调函数 (item)
        headers_visible: 是否显示表头
        frame: 大纲视图框架
    
    Returns:
        NSScrollView 实例（包含 NSOutlineView）
    """
    print("⚠️  OutlineView 暂时被禁用，返回一个替代的 TableView")
    
    # 暂时用 TableView 替代，直到修复 OutlineView 的崩溃问题
    # 将树形数据扁平化为列表
    flat_data = []
    if root_items:
        for item in root_items:
            # 添加根项目
            if isinstance(item, dict):
                flat_data.append(item)
                # 添加子项目（如果有）
                if get_children:
                    children = get_children(item)
                    if children:
                        for child in children:
                            if isinstance(child, dict):
                                # 为子项目添加前缀以示层级
                                child_copy = child.copy()
                                if 'title' in child_copy:
                                    child_copy['title'] = f"  └ {child_copy['title']}"
                                flat_data.append(child_copy)
    
    # 使用 TableView 替代
    return TableView(
        columns=columns,
        data=flat_data,
        on_select=on_select,
        headers_visible=headers_visible,
        frame=frame
    )
