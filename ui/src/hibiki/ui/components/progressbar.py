#!/usr/bin/env python3
"""
Hibiki UI v4.0 - ProgressBar组件
进度条组件，支持确定和不确定进度显示
"""

from typing import Optional, Union
from AppKit import (
    NSView, NSProgressIndicator, NSProgressIndicatorStyleBar, 
    NSProgressIndicatorStyleSpinning, NSMakeRect
)

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Effect
from ..core.logging import get_logger

logger = get_logger("components.progressbar")
logger.setLevel("INFO")


class ProgressBar(UIComponent):
    """进度条组件 - 基于NSProgressIndicator"""
    
    def __init__(
        self,
        initial_value: Union[float, "Signal"] = 0.0,
        maximum: Union[float, "Signal"] = 100.0,
        style: Optional[ComponentStyle] = None,
        indeterminate: bool = False,
    ):
        """初始化进度条组件
        
        Args:
            initial_value: 进度值（0-maximum之间）
            maximum: 最大值
            style: 组件样式
            indeterminate: 是否为不确定进度条
        """
        super().__init__(style)
        # 处理响应式值
        if hasattr(initial_value, "value"):
            self._is_reactive_value = True
            self.value = initial_value
        else:
            self._is_reactive_value = False
            self.value = initial_value
        
        if hasattr(maximum, "value"):
            self._is_reactive_maximum = True
            self.maximum = maximum
        else:
            self._is_reactive_maximum = False
            self.maximum = maximum
        
        self.indeterminate = indeterminate
        self._progress_indicator = None
        
        logger.debug(
            f"🔧 ProgressBar组件创建: value={self._get_value()}, max={self._get_maximum()}"
        )
    
    def _get_value(self) -> float:
        """获取当前进度值"""
        if self._is_reactive_value:
            return self.value.value if hasattr(self.value, "value") else 0.0
        return self.value
    
    def _get_maximum(self) -> float:
        """获取最大值"""
        if self._is_reactive_maximum:
            return self.maximum.value if hasattr(self.maximum, "value") else 100.0
        return self.maximum
    
    def _create_nsview(self) -> NSView:
        """创建NSProgressIndicator"""
        # 创建进度指示器
        progress = NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 20))
        
        if self.indeterminate:
            progress.setStyle_(NSProgressIndicatorStyleSpinning)
            progress.setIndeterminate_(True)
            progress.startAnimation_(None)
        else:
            progress.setStyle_(NSProgressIndicatorStyleBar)
            progress.setIndeterminate_(False)
            
            # 设置进度值
            progress.setMaxValue_(self._get_maximum())
            progress.setDoubleValue_(self._get_value())
        
        self._progress_indicator = progress
        
        # 建立响应式绑定
        if self._is_reactive_value:
            self._bind_reactive_value()
        if self._is_reactive_maximum:
            self._bind_reactive_maximum()
        
        logger.debug(f"📊 ProgressBar NSProgressIndicator创建完成")
        return progress
    
    def _bind_reactive_value(self):
        """建立进度值的响应式绑定"""
        if not hasattr(self.value, "value"):
            return
        
        def update_progress():
            if self._progress_indicator and not self.indeterminate:
                new_value = self.value.value
                self._progress_indicator.setDoubleValue_(float(new_value))
                logger.debug(f"📊 ProgressBar值更新: {new_value}")
        
        # 使用Effect建立响应式绑定
        self._value_effect = Effect(update_progress)
    
    def _bind_reactive_maximum(self):
        """建立最大值的响应式绑定"""
        if not hasattr(self.maximum, "value"):
            return
        
        def update_maximum():
            if self._progress_indicator and not self.indeterminate:
                new_maximum = self.maximum.value
                self._progress_indicator.setMaxValue_(float(new_maximum))
                logger.debug(f"📊 ProgressBar最大值更新: {new_maximum}")
        
        # 使用Effect建立响应式绑定
        self._maximum_effect = Effect(update_maximum)
    
    def set_value(self, value: float) -> "ProgressBar":
        """设置进度值
        
        Args:
            value: 新的进度值
        """
        if self._is_reactive_value:
            self.value.value = value
        else:
            self.value = value
            if self._progress_indicator and not self.indeterminate:
                self._progress_indicator.setDoubleValue_(float(value))
        
        logger.debug(f"📊 ProgressBar进度更新: {value}")
        return self
    
    def set_maximum(self, maximum: float) -> "ProgressBar":
        """设置最大值
        
        Args:
            maximum: 新的最大值
        """
        if self._is_reactive_maximum:
            self.maximum.value = maximum
        else:
            self.maximum = maximum
            if self._progress_indicator and not self.indeterminate:
                self._progress_indicator.setMaxValue_(float(maximum))
        
        logger.debug(f"📊 ProgressBar最大值更新: {maximum}")
        return self
    
    def start_animation(self) -> "ProgressBar":
        """开始动画（仅适用于不确定进度条）"""
        if self._progress_indicator and self.indeterminate:
            self._progress_indicator.startAnimation_(None)
            logger.debug(f"🎬 ProgressBar动画开始")
        return self
    
    def stop_animation(self) -> "ProgressBar":
        """停止动画（仅适用于不确定进度条）"""
        if self._progress_indicator and self.indeterminate:
            self._progress_indicator.stopAnimation_(None)
            logger.debug(f"⏹️ ProgressBar动画停止")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, "_value_effect"):
            self._value_effect.cleanup()
        if hasattr(self, "_maximum_effect"):
            self._maximum_effect.cleanup()
        super().cleanup()