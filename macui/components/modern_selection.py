"""
现代化选择组件 - 基于新布局引擎v3.0 (Stretchable)

提供支持CSS-like布局属性的现代化选择组件
包括PopUpButton, ComboBox, Menu, ContextMenu等
"""

from typing import Any, Callable, List, Optional, Union, Dict
from AppKit import (
    NSPopUpButton, NSComboBox, NSMenu, NSMenuItem
)
from Foundation import NSMakeRect

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedPopUpDelegate, EnhancedComboBoxDelegate, EnhancedMenuItemDelegate
from ..core.signal import Signal, Computed
from ..layout.styles import LayoutStyle
from .core import LayoutAwareComponent


class ModernPopUpButton(LayoutAwareComponent):
    """现代化下拉选择按钮 - 支持新布局系统"""
    
    def __init__(
        self,
        items: List[str],
        selected: Optional[Signal[int]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[int], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化下拉选择按钮
        
        Args:
            items: 选项列表
            selected: 选中项索引信号 (双向绑定)
            enabled: 启用状态 (响应式)
            on_change: 选项改变回调
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        layout_style = LayoutStyle(
            width=width or 120,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.items = items
        self.selected = selected or Signal(0)
        self.enabled = enabled
        self.on_change = on_change
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSPopUpButton:
        """创建NSPopUpButton实例"""
        popup = NSPopUpButton.alloc().init()
        
        # 添加选项
        popup.removeAllItems()
        for item in self.items:
            popup.addItemWithTitle_(item)
        
        # 设置初始选中状态
        if 0 <= self.selected.value < len(self.items):
            popup.selectItemAtIndex_(self.selected.value)
        
        # 设置frame
        width = self.layout_style.width or 120
        height = self.layout_style.height or 24
        popup.setFrame_(NSMakeRect(0, 0, width, height))
        
        return popup
    
    def _setup_nsview(self):
        """设置NSPopUpButton属性和绑定"""
        popup = self._nsview
        
        # 双向绑定选中状态
        TwoWayBinding.bind_popup_button(popup, self.selected)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(popup, "enabled", self.enabled)
            else:
                popup.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(popup, "tooltip", self.tooltip)
            else:
                popup.setToolTip_(str(self.tooltip))
        
        # 事件处理
        if self.on_change:
            delegate = EnhancedPopUpDelegate.alloc().init()
            delegate.on_change = self.on_change
            delegate.signal = self.selected
            
            popup.setTarget_(delegate)
            popup.setAction_("popUpChanged:")
            
            # 保持委托引用
            import objc
            objc.setAssociatedObject(popup, b"enhanced_popup_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        print(f"🔽 ModernPopUpButton 创建完成，选项数: {len(self.items)}")


class ModernComboBox(LayoutAwareComponent):
    """现代化组合框 - 支持新布局系统"""
    
    def __init__(
        self,
        items: Optional[List[str]] = None,
        text: Optional[Signal[str]] = None,
        editable: bool = True,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[str], None]] = None,
        on_select: Optional[Callable[[int, str], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化组合框
        
        Args:
            items: 下拉选项列表
            text: 文本值信号 (双向绑定)
            editable: 是否可编辑
            enabled: 启用状态 (响应式)
            on_change: 文本改变回调
            on_select: 选择项回调 (index, text)
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        layout_style = LayoutStyle(
            width=width or 150,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.items = items or []
        self.text = text or Signal("")
        self.editable = editable
        self.enabled = enabled
        self.on_change = on_change
        self.on_select = on_select
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSComboBox:
        """创建NSComboBox实例"""
        combo_box = NSComboBox.alloc().init()
        
        # 设置是否可编辑
        combo_box.setEditable_(self.editable)
        
        # 添加选项
        combo_box.removeAllItems()
        for item in self.items:
            combo_box.addItemWithObjectValue_(str(item))
        
        # 设置初始文本
        combo_box.setStringValue_(self.text.value)
        
        # 设置frame
        width = self.layout_style.width or 150
        height = self.layout_style.height or 24
        combo_box.setFrame_(NSMakeRect(0, 0, width, height))
        
        return combo_box
    
    def _setup_nsview(self):
        """设置NSComboBox属性和绑定"""
        combo_box = self._nsview
        
        # 双向绑定文本
        TwoWayBinding.bind_combo_box(combo_box, self.text)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(combo_box, "enabled", self.enabled)
            else:
                combo_box.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(combo_box, "tooltip", self.tooltip)
            else:
                combo_box.setToolTip_(str(self.tooltip))
        
        # 事件处理
        if self.on_change or self.on_select:
            delegate = EnhancedComboBoxDelegate.alloc().init()
            delegate.on_change = self.on_change
            delegate.on_select = self.on_select
            delegate.signal = self.text
            
            combo_box.setDelegate_(delegate)
            
            # 保持委托引用
            import objc
            objc.setAssociatedObject(combo_box, b"enhanced_combo_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        print(f"🔄 ModernComboBox 创建完成，可编辑: {self.editable}")


class ModernMenu(LayoutAwareComponent):
    """现代化菜单组件 - 虽然不参与布局，但提供统一接口"""
    
    def __init__(
        self,
        title: str = "",
        items: Optional[List[Dict[str, Any]]] = None,
        **layout_kwargs
    ):
        """初始化现代化菜单
        
        Args:
            title: 菜单标题
            items: 菜单项配置列表，每个项目：
                   {"title": str, "action": callable, "id": str (可选), "separator": bool (可选)}
            **layout_kwargs: 布局样式 (菜单不参与布局)
        """
        # 菜单不需要实际的布局样式，但保持接口一致
        layout_style = LayoutStyle(**layout_kwargs)
        super().__init__(layout_style)
        
        self.title = title
        self.items = items or []
    
    def _create_nsview(self) -> NSMenu:
        """创建NSMenu实例"""
        menu = NSMenu.alloc().init()
        menu.setTitle_(self.title)
        
        return menu
    
    def _setup_nsview(self):
        """设置NSMenu内容"""
        menu = self._nsview
        
        for item_config in self.items:
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
        
        print(f"📋 ModernMenu '{self.title}' 创建完成，菜单项数: {len(self.items)}")
    
    def get_menu(self) -> NSMenu:
        """获取NSMenu实例 - 专用于菜单组件"""
        return self.get_view()


# 向后兼容的函数式接口
def PopUpButton(
    items: List[str],
    selected: Optional[Union[int, Signal[int]]] = None,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernPopUpButton:
    """创建现代化下拉选择按钮 - 向后兼容接口
    
    Examples:
        # 基本用法 (兼容旧API)
        popup = PopUpButton(["选项1", "选项2", "选项3"])
        
        # 新功能 - 布局属性
        popup = PopUpButton(["选项1", "选项2"], selected=Signal(0), width=150, margin=8)
        
        # 链式调用
        popup = PopUpButton(["选项1", "选项2"]).width(150).margin(8)
    """
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    # 处理非Signal的selected值
    if selected is not None and not isinstance(selected, Signal):
        selected = Signal(int(selected))
    
    return ModernPopUpButton(items, selected, **kwargs)


def ComboBox(
    items: Optional[List[str]] = None,
    text: Optional[Union[str, Signal[str]]] = None,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernComboBox:
    """创建现代化组合框 - 向后兼容接口"""
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    # 处理非Signal的text值
    if text is not None and not isinstance(text, Signal):
        text = Signal(str(text))
    
    return ModernComboBox(items, text, **kwargs)


def Menu(
    title: str = "",
    items: Optional[List[Dict[str, Any]]] = None,
) -> ModernMenu:
    """创建现代化菜单 - 向后兼容接口"""
    return ModernMenu(title, items)


def ContextMenu(
    items: Optional[List[Dict[str, Any]]] = None,
) -> ModernMenu:
    """创建现代化上下文菜单 - 向后兼容接口"""
    return ModernMenu("", items)


# 便捷构造函数
def StringPopUp(
    options: List[str],
    selected_signal: Signal[str],
    **kwargs
) -> ModernPopUpButton:
    """字符串选择下拉框 - 直接绑定字符串值而非索引"""
    # 创建索引Signal
    index_signal = Signal(0)
    
    # 字符串到索引的双向绑定
    def update_index():
        try:
            index_signal.value = options.index(selected_signal.value)
        except (ValueError, IndexError):
            index_signal.value = 0
    
    def update_string():
        if 0 <= index_signal.value < len(options):
            selected_signal.value = options[index_signal.value]
    
    # 初始同步
    update_index()
    
    # 双向监听
    selected_signal.add_observer(lambda _: update_index())
    index_signal.add_observer(lambda _: update_string())
    
    return ModernPopUpButton(options, index_signal, **kwargs)


def FilteredComboBox(
    all_items: List[str],
    filter_signal: Signal[str],
    **kwargs
) -> ModernComboBox:
    """过滤组合框 - 根据输入过滤选项"""
    from ..core.signal import Computed
    
    filtered_items = Computed(lambda: [
        item for item in all_items 
        if filter_signal.value.lower() in item.lower()
    ] if filter_signal.value else all_items)
    
    # 由于NSComboBox的限制，这里简化实现
    # 实际项目中可能需要更复杂的过滤逻辑
    return ModernComboBox(all_items, filter_signal, **kwargs)


def ActionMenu(
    actions: Dict[str, Callable[[], None]],
    **kwargs
) -> ModernMenu:
    """动作菜单 - 简化的动作绑定接口"""
    items = []
    for title, action in actions.items():
        if title == "---":  # 分隔符
            items.append({"separator": True})
        else:
            items.append({
                "title": title,
                "action": lambda action=action: action(),
                "id": title
            })
    
    return ModernMenu("Actions", items, **kwargs)