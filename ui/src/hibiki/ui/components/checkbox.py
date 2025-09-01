#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Checkbox组件
复选框组件，支持选中状态管理和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSButton, NSButtonTypeSwitch
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect
from ..core.logging import get_logger

logger = get_logger("components.checkbox")
logger.setLevel("INFO")


class CheckboxDelegate(NSObject):
    """Checkbox事件委托类"""
    
    def init(self):
        self = objc.super(CheckboxDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.checkbox = None
        return self
    
    def checkboxToggled_(self, sender):
        """复选框状态切换事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                is_checked = sender.state() == 1
                self.callback(is_checked)
            except Exception as e:
                logger.error(f"⚠️ Checkbox状态变化回调错误: {e}")


class Checkbox(UIComponent):
    """复选框组件
    
    基于Hibiki UI v4.0架构的复选框组件。
    支持选中状态管理和响应式绑定。
    
    Features:
    - 选中/未选中状态管理
    - 响应式状态绑定
    - 自定义标题文本
    - 状态变化回调
    - 完整的布局支持
    """
    
    def __init__(
        self,
        title: str = "",
        checked: Union[bool, Any] = False,
        style: Optional[ComponentStyle] = None,
        on_change: Optional[Callable[[bool], None]] = None,
        **style_kwargs,
    ):
        """初始化Checkbox组件
        
        Args:
            title: 复选框标题文本
            checked: 初始选中状态，支持Signal绑定
            style: 组件样式对象
            on_change: 状态变化回调函数
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.checked = checked
        self.on_change = on_change
        
        # 检查是否为响应式状态
        self._is_reactive_checked = isinstance(checked, (Signal, Computed))
        self._bindings = []
        self._checkbox_delegate = None
        
        logger.debug(f"☑️ Checkbox创建: title='{title}', checked={checked}")
    
    def _create_nsview(self) -> NSView:
        """创建复选框NSView"""
        checkbox = NSButton.alloc().init()
        checkbox.setButtonType_(NSButtonTypeSwitch)
        checkbox.setTitle_(self.title)
        
        # 设置初始状态
        initial_checked = False
        if self._is_reactive_checked:
            initial_checked = bool(getattr(self.checked, "value", False))
        else:
            initial_checked = bool(self.checked)
        
        checkbox.setState_(1 if initial_checked else 0)
        
        # 自动调整尺寸
        checkbox.sizeToFit()
        
        # 绑定状态变化事件
        if self.on_change:
            self._bind_change_event(checkbox)
        
        # 响应式绑定
        if self._is_reactive_checked:
            # 自定义绑定函数，因为checkbox需要特殊的状态处理
            def update_checkbox_state():
                new_checked = bool(getattr(self.checked, "value", False))
                checkbox.setState_(1 if new_checked else 0)
            
            effect = Effect(update_checkbox_state)
            self._bindings.append(effect)
            logger.debug(f"🔗 Checkbox响应式绑定已创建")
        
        return checkbox
    
    def _bind_change_event(self, checkbox):
        """绑定状态变化事件"""
        delegate = CheckboxDelegate.alloc().init()
        delegate.callback = self.on_change
        delegate.checkbox = self
        
        checkbox.setTarget_(delegate)
        checkbox.setAction_("checkboxToggled:")
        self._checkbox_delegate = delegate
        logger.debug("🔗 Checkbox状态变化事件已绑定")
    
    def get_checked(self) -> bool:
        """获取当前选中状态"""
        if self._nsview:
            return self._nsview.state() == 1
        if self._is_reactive_checked:
            return bool(getattr(self.checked, "value", False))
        return bool(self.checked)
    
    def set_checked(self, checked: Union[bool, Any]) -> "Checkbox":
        """设置选中状态"""
        self.checked = checked
        self._is_reactive_checked = isinstance(checked, (Signal, Computed))
        
        if self._nsview:
            new_state = bool(getattr(checked, "value", checked))
            self._nsview.setState_(1 if new_state else 0)
        
        return self