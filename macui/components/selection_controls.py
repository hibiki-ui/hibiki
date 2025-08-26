"""选择控件 - PopUpButton, ComboBox, Menu, ContextMenu

这些控件提供下拉选择、菜单选择等功能。
"""

from typing import Any, Callable, List, Optional, Union

from AppKit import (
    NSComboBox,
    NSMenu,
    NSMenuItem,
    NSPopUpButton,
)
from Foundation import NSMakeRect

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedPopUpDelegate, EnhancedComboBoxDelegate, EnhancedMenuItemDelegate
from ..core.signal import Computed, Signal


def PopUpButton(
    items: list[str],
    selected: Optional[Union[int, Signal[int]]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[int], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSPopUpButton:
    """创建下拉选择按钮
    
    Args:
        items: 选项列表
        selected: 当前选中的项目索引 (支持双向绑定)
        enabled: 启用状态 (支持响应式)
        on_change: 选项改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 控件框架
    
    Returns:
        NSPopUpButton 实例
    """
    popup = NSPopUpButton.alloc().init()

    if frame:
        popup.setFrame_(NSMakeRect(*frame))

    # 添加选项
    popup.removeAllItems()
    for item in items:
        popup.addItemWithTitle_(item)

    # 初始选中状态
    initial_selected = 0
    if selected is not None:
        initial_selected = selected.value if isinstance(selected, Signal) else int(selected)
        if 0 <= initial_selected < len(items):
            popup.selectItemAtIndex_(initial_selected)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(popup, "enabled", enabled)
        else:
            popup.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(popup, "tooltip", tooltip)
        else:
            popup.setToolTip_(str(tooltip))

    # 双向绑定和事件处理
    if selected is not None and isinstance(selected, Signal):
        TwoWayBinding.bind_popup_button(popup, selected)
    
    if on_change:
        # 创建下拉按钮委托
        delegate = EnhancedPopUpDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = selected if isinstance(selected, Signal) else None
        
        popup.setTarget_(delegate)
        popup.setAction_("popUpChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(popup, b"enhanced_popup_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return popup


def ComboBox(
    items: Optional[list[str]] = None,
    text: Optional[Union[str, Signal[str]]] = None,
    editable: bool = True,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[str], None]] = None,
    on_select: Optional[Callable[[int, str], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSComboBox:
    """创建组合框（可编辑下拉框）
    
    Args:
        items: 下拉选项列表
        text: 当前文本值 (支持响应式)
        editable: 是否可编辑
        enabled: 启用状态 (支持响应式)
        on_change: 文本变更回调函数 
        on_select: 选择项变更回调函数 (index, text)
        tooltip: 工具提示 (支持响应式)
        frame: 组合框框架
    
    Returns:
        NSComboBox 实例
    """
    combo_box = NSComboBox.alloc().init()
    
    if frame:
        combo_box.setFrame_(NSMakeRect(*frame))
    
    # 设置是否可编辑
    combo_box.setEditable_(editable)
    
    # 添加选项
    if items:
        combo_box.removeAllItems()
        for item in items:
            combo_box.addItemWithObjectValue_(str(item))
    
    # 设置初始文本
    if text is not None:
        if isinstance(text, (Signal, Computed)):
            # 响应式绑定文本
            TwoWayBinding.bind_combo_box(combo_box, text)
        else:
            combo_box.setStringValue_(str(text))
    
    # 启用状态绑定
    if enabled is not None:
        ReactiveBinding.bind(combo_box, "enabled", enabled)
    
    # 工具提示绑定
    if tooltip is not None:
        ReactiveBinding.bind(combo_box, "tooltip", tooltip)
    
    # 事件处理
    if on_change or on_select or (isinstance(text, Signal)):
        # 创建组合框委托
        delegate = EnhancedComboBoxDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.on_select = on_select
        delegate.signal = text if isinstance(text, Signal) else None
        
        combo_box.setDelegate_(delegate)
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(combo_box, b"enhanced_combo_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return combo_box


def Menu(
    title: str = "",
    items: Optional[list[dict]] = None,
) -> NSMenu:
    """创建菜单
    
    Args:
        title: 菜单标题
        items: 菜单项配置列表，每个项目是一个字典：
               {"title": str, "action": callable, "id": str (可选), "separator": bool (可选)}
    
    Returns:
        NSMenu 实例
    """
    menu = NSMenu.alloc().init()
    menu.setTitle_(title)
    
    if items:
        for item_config in items:
            if item_config.get("separator", False):
                # 添加分隔符
                separator = NSMenuItem.separatorItem()
                menu.addItem_(separator)
            else:
                # 创建普通菜单项
                title = item_config.get("title", "")
                action_handler = item_config.get("action")
                item_id = item_config.get("id", title)
                
                menu_item = NSMenuItem.alloc().init()
                menu_item.setTitle_(title)
                
                if action_handler:
                    # 创建委托处理点击事件
                    delegate = EnhancedMenuItemDelegate.alloc().init()
                    delegate.on_click = lambda item_id=item_id, handler=action_handler: handler(item_id)
                    delegate.item_id = item_id
                    
                    menu_item.setTarget_(delegate)
                    menu_item.setAction_("menuItemClicked:")
                    
                    # 保持委托引用
                    import objc
                    objc.setAssociatedObject(menu_item, b"menu_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
                
                menu.addItem_(menu_item)
    
    return menu


def ContextMenu(
    items: Optional[list[dict]] = None,
) -> NSMenu:
    """创建上下文菜单（右键菜单）
    
    Args:
        items: 菜单项配置列表，格式与 Menu 相同
    
    Returns:
        NSMenu 实例，可用作视图的 contextMenu
    """
    return Menu("", items)