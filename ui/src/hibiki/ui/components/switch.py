#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Switch组件
开关组件，支持布尔值切换和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSButton, NSButtonTypeSwitch
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed
from ..core.binding import ReactiveBinding
from ..core.logging import get_logger

logger = get_logger("components.switch")
logger.setLevel("INFO")


# Switch事件委托类
class SwitchDelegate(NSObject):
    """Switch事件委托类"""
    
    def init(self):
        self = objc.super(SwitchDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        return self
    
    def switchToggled_(self, sender):
        """开关切换事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                is_on = sender.state() == 1  # NSOnState = 1
                self.callback(is_on)
            except Exception as e:
                logger.error(f"⚠️ Switch切换回调错误: {e}")


class Switch(UIComponent):
    """现代化Switch开关组件
    
    基于Hibiki UI v4.0新架构的开关组件。
    支持布尔值切换、响应式绑定和状态回调。
    
    Features:
    - 布尔值状态切换 (True/False)
    - 响应式状态绑定
    - 状态变化回调事件
    - 完整的布局API支持
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        value: Union[bool, Any] = False,
        on_change: Optional[Callable[[bool], None]] = None,
        style: Optional[ComponentStyle] = None,
        **style_kwargs,
    ):
        """🏗️ CORE METHOD: Switch component initialization
        
        Args:
            value: 开关状态，支持布尔值或响应式Signal
            on_change: 状态变化回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.on_change = on_change
        
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        logger.debug(f"🔘 Switch创建: value={value}, reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton配置为开关样式"""
        switch = NSButton.alloc().init()
        
        # 设置为开关样式
        switch.setButtonType_(NSButtonTypeSwitch)
        switch.setTitle_("")  # 不显示标题
        
        # 设置初始状态 - 使用响应式绑定系统
        
        # 绑定开关状态，自动处理响应式和静态值
        # 使用state属性来绑定NSButton的开关状态
        binding_cleanup = ReactiveBinding.bind(switch, "state", self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            if not hasattr(self, "_binding_cleanups"):
                self._binding_cleanups = []
            self._binding_cleanups.append(binding_cleanup)
        
        # 绑定开关状态变化事件
        if self.on_change:
            try:
                # 创建开关委托
                self._delegate = SwitchDelegate.alloc().init()
                self._delegate.callback = self.on_change
                self._delegate.switch_component = self  # 保存组件引用
                
                # 设置委托和动作
                switch.setTarget_(self._delegate)
                switch.setAction_("switchChanged:")
                
                logger.debug(f"🔗 Switch状态变化事件已绑定")
            
            except Exception as e:
                logger.warning(f"⚠️ Switch事件绑定失败: {e}")
        
        logger.debug(f"🔘 NSButton(Switch)创建完成: state={self.get_value()}")
        return switch
    
    def get_value(self) -> bool:
        """获取当前开关状态"""
        if self._nsview:
            return bool(self._nsview.state())
        
        # 如果NSView还未创建，从响应式值或静态值获取
        if self._is_reactive_value and hasattr(self.value, "value"):
            return bool(self.value.value)
        return bool(self.value)
    
    def set_value(self, value: bool) -> "Switch":
        """动态设置开关状态
        
        Args:
            value: 新的开关状态
        """
        self.value = value
        
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setState_(1 if value else 0)
            logger.debug(f"🔘 Switch状态更新: {value}")
        
        return self
    
    def toggle(self) -> "Switch":
        """切换开关状态"""
        current_state = self.get_value()
        self.set_value(not current_state)
        return self