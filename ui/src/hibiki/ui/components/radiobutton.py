#!/usr/bin/env python3
"""
Hibiki UI v4.0 - RadioButton组件
单选按钮组件，支持分组选择和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSButton, NSButtonTypeRadio
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect
from ..core.logging import get_logger

logger = get_logger("components.radiobutton")
logger.setLevel("INFO")


class RadioButtonDelegate(NSObject):
    """RadioButton事件委托类"""
    
    def init(self):
        self = objc.super(RadioButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.value = None
        self.radio_button = None
        return self
    
    def radioSelected_(self, sender):
        """单选按钮选中事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                if sender.state() == 1:  # 只在选中时触发回调
                    self.callback(self.value)
            except Exception as e:
                logger.error(f"⚠️ RadioButton选择回调错误: {e}")


class RadioButton(UIComponent):
    """单选按钮组件
    
    基于Hibiki UI v4.0架构的单选按钮组件。
    支持分组选择和响应式绑定。
    
    Features:
    - 分组单选功能
    - 响应式状态绑定
    - 自定义标题文本
    - 选择变化回调
    - 完整的布局支持
    """
    
    def __init__(
        self,
        title: str = "",
        value: Any = None,
        selected: Union[bool, Any] = False,
        group: Optional[str] = None,
        style: Optional[ComponentStyle] = None,
        on_select: Optional[Callable[[Any], None]] = None,
        **style_kwargs,
    ):
        """初始化RadioButton组件
        
        Args:
            title: 单选按钮标题文本
            value: 按钮的值（选中时返回的值）
            selected: 初始选中状态，支持Signal绑定
            group: 单选组名称
            style: 组件样式对象
            on_select: 选中回调函数，参数为value
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.value = value if value is not None else title
        self.selected = selected
        self.group = group
        self.on_select = on_select
        
        # 检查是否为响应式状态
        self._is_reactive_selected = isinstance(selected, (Signal, Computed))
        self._bindings = []
        self._radio_delegate = None
        
        logger.debug(
            f"🔘 RadioButton创建: title='{title}', value={self.value}, selected={selected}"
        )
    
    def _create_nsview(self) -> NSView:
        """创建单选按钮NSView"""
        radio = NSButton.alloc().init()
        radio.setButtonType_(NSButtonTypeRadio)
        radio.setTitle_(self.title)
        
        # 设置初始状态
        initial_selected = False
        if self._is_reactive_selected:
            initial_selected = bool(getattr(self.selected, "value", False))
        else:
            initial_selected = bool(self.selected)
        
        radio.setState_(1 if initial_selected else 0)
        
        # 自动调整尺寸
        radio.sizeToFit()
        
        # 绑定选择事件
        if self.on_select:
            self._bind_select_event(radio)
        
        # 响应式绑定
        if self._is_reactive_selected:
            # 自定义绑定函数
            def update_radio_state():
                new_selected = bool(getattr(self.selected, "value", False))
                radio.setState_(1 if new_selected else 0)
            
            effect = Effect(update_radio_state)
            self._bindings.append(effect)
            logger.debug(f"🔗 RadioButton响应式绑定已创建")
        
        return radio
    
    def _bind_select_event(self, radio):
        """绑定选择事件"""
        delegate = RadioButtonDelegate.alloc().init()
        delegate.callback = self.on_select
        delegate.value = self.value
        delegate.radio_button = self
        
        radio.setTarget_(delegate)
        radio.setAction_("radioSelected:")
        self._radio_delegate = delegate
        logger.debug("🔗 RadioButton选择事件已绑定")
    
    def get_selected(self) -> bool:
        """获取当前选中状态"""
        if self._nsview:
            return self._nsview.state() == 1
        if self._is_reactive_selected:
            return bool(getattr(self.selected, "value", False))
        return bool(self.selected)
    
    def set_selected(self, selected: Union[bool, Any]) -> "RadioButton":
        """设置选中状态"""
        self.selected = selected
        self._is_reactive_selected = isinstance(selected, (Signal, Computed))
        
        if self._nsview:
            new_state = bool(getattr(selected, "value", selected))
            self._nsview.setState_(1 if new_state else 0)
        
        return self