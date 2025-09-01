#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Slider组件
滑块组件，支持数值选择和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSSlider
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed
from ..core.binding import ReactiveBinding
from ..core.logging import get_logger

logger = get_logger("components.slider")
logger.setLevel("INFO")


# Slider事件委托类
class SliderDelegate(NSObject):
    """Slider值变化事件委托类"""
    
    def init(self):
        self = objc.super(SliderDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.slider_component = None
        return self
    
    def sliderChanged_(self, sender):
        """滑块值变化事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                # 获取当前滑块值
                current_value = sender.doubleValue()
                
                # 更新组件的值
                if hasattr(self, "slider_component") and self.slider_component:
                    if self.slider_component._is_reactive_value and hasattr(
                        self.slider_component.value, "value"
                    ):
                        self.slider_component.value.value = current_value
                    else:
                        self.slider_component.value = current_value
                
                # 调用回调函数
                self.callback(current_value)
                logger.debug(f"🎚️ Slider值变化: {current_value}")
            
            except Exception as e:
                logger.error(f"⚠️ Slider值变化回调错误: {e}")


class Slider(UIComponent):
    """现代化Slider滑块组件
    
    基于Hibiki UI v4.0新架构的滑块组件。
    支持数值选择、范围限制和响应式绑定。
    
    Features:
    - 数值范围控制 (min_value, max_value)
    - 响应式值绑定
    - 值变化回调事件
    - 完整的布局API支持
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        value: Union[float, int, Any] = 0.0,
        min_value: float = 0.0,
        max_value: float = 100.0,
        on_change: Optional[Callable[[float], None]] = None,
        style: Optional[ComponentStyle] = None,
        **style_kwargs,
    ):
        """🏗️ CORE METHOD: Slider component initialization
        
        Args:
            value: 当前滑块值，支持数字或响应式Signal
            min_value: 最小值
            max_value: 最大值
            on_change: 值变化回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change
        
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        logger.debug(
            f"🎚️ Slider创建: value={value}, range=[{min_value}, {max_value}], reactive={self._is_reactive_value}"
        )
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSSlider作为滑块"""
        slider = NSSlider.alloc().init()
        
        # 设置滑块范围
        slider.setMinValue_(self.min_value)
        slider.setMaxValue_(self.max_value)
        
        # 设置初始值 - 使用响应式绑定系统
        
        # 绑定滑块值，自动处理响应式和静态值
        binding_cleanup = ReactiveBinding.bind(slider, "doubleValue", self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            if not hasattr(self, "_binding_cleanups"):
                self._binding_cleanups = []
            self._binding_cleanups.append(binding_cleanup)
        
        # 绑定滑块值变化事件
        if self.on_change:
            try:
                # 创建滑块委托
                self._delegate = SliderDelegate.alloc().init()
                self._delegate.callback = self.on_change
                self._delegate.slider_component = self  # 保存组件引用
                
                # 设置委托和动作
                slider.setTarget_(self._delegate)
                slider.setAction_("sliderChanged:")
                
                logger.debug(f"🔗 Slider值变化事件已绑定")
            
            except Exception as e:
                logger.warning(f"⚠️ Slider事件绑定失败: {e}")
        
        logger.debug(f"🎚️ NSSlider创建完成: range=[{self.min_value}, {self.max_value}]")
        return slider
    
    def get_value(self) -> float:
        """获取当前滑块值"""
        if self._nsview:
            return self._nsview.doubleValue()
        
        # 如果NSView还未创建，从响应式值或静态值获取
        if self._is_reactive_value and hasattr(self.value, "value"):
            return float(self.value.value)
        return float(self.value)
    
    def set_value(self, value: Union[float, int]) -> "Slider":
        """动态设置滑块值
        
        Args:
            value: 新的滑块值
        """
        # 确保值在范围内
        value = max(self.min_value, min(self.max_value, float(value)))
        self.value = value
        
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setDoubleValue_(value)
            logger.debug(f"🎚️ Slider值更新: {value}")
        
        return self
    
    def set_range(self, min_value: float, max_value: float) -> "Slider":
        """动态设置滑块范围
        
        Args:
            min_value: 新的最小值
            max_value: 新的最大值
        """
        self.min_value = min_value
        self.max_value = max_value
        
        if self._nsview:
            self._nsview.setMinValue_(min_value)
            self._nsview.setMaxValue_(max_value)
            # 确保当前值仍在新范围内
            current_value = self._nsview.doubleValue()
            if current_value < min_value or current_value > max_value:
                new_value = max(min_value, min(max_value, current_value))
                self._nsview.setDoubleValue_(new_value)
            logger.debug(f"🎚️ Slider范围更新: [{min_value}, {max_value}]")
        
        return self