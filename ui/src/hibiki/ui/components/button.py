#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Button组件
按钮组件，支持点击事件处理和样式定制
"""

from typing import Optional, Callable
from AppKit import NSView, NSButton, NSButtonTypeMomentaryPushIn
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.logging import get_logger

logger = get_logger("components.button")
logger.setLevel("INFO")


# Button事件委托类
class ButtonDelegate(NSObject):
    """Button事件委托类"""
    
    def init(self):
        self = objc.super(ButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        return self
    
    def buttonClicked_(self, sender):
        """按钮点击事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                self.callback()
            except Exception as e:
                logger.error(f"⚠️ 按钮点击回调错误: {e}")


class Button(UIComponent):
    """现代化Button组件
    
    基于Hibiki UI v4.0新架构的按钮组件。
    支持完整的事件处理和布局API。
    
    Features:
    - 完整的定位和布局支持
    - 点击事件处理
    - 多种按钮样式
    - 响应式标题绑定
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        title: str,
        on_click: Optional[Callable[[], None]] = None,
        style: Optional[ComponentStyle] = None,
        **style_kwargs,
    ):
        """🏗️ CORE METHOD: Button component initialization
        
        Args:
            title: 按钮标题文本
            on_click: 点击事件回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.on_click = on_click
        self._target_delegate = None
        
        logger.debug(f"🔘 Button创建: title='{title}', has_click={on_click is not None}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton"""
        button = NSButton.alloc().init()
        
        # 基础配置
        button.setTitle_(self.title)
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 自动调整尺寸
        button.sizeToFit()
        
        # 绑定点击事件
        if self.on_click:
            self._bind_click_event(button)
        
        return button
    
    def _bind_click_event(self, button: NSButton):
        """绑定点击事件"""
        try:
            # 使用ButtonDelegate类
            self._target_delegate = ButtonDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建ButtonDelegate")
                return
            
            self._target_delegate.callback = self.on_click
            
            button.setTarget_(self._target_delegate)
            button.setAction_("buttonClicked:")
            
            logger.debug(f"🔗 Button点击事件已绑定")
        
        except Exception as e:
            logger.warning(f"⚠️ Button事件绑定失败: {e}")
    
    def set_title(self, title: str) -> "Button":
        """动态设置按钮标题
        
        Args:
            title: 新的按钮标题
        """
        self.title = title
        
        if self._nsview:
            self._nsview.setTitle_(title)
            self._nsview.sizeToFit()  # 重新调整尺寸
            logger.debug(f"📝 Button标题更新: '{title}'")
        
        return self
    
    def set_click_handler(self, callback: Callable[[], None]) -> "Button":
        """设置或更新点击事件处理器
        
        Args:
            callback: 新的点击回调函数
        """
        self.on_click = callback
        
        if self._target_delegate:
            self._target_delegate.callback = callback
            logger.debug(f"🔗 Button点击回调已更新")
        elif self._nsview:
            # 如果按钮已创建但没有事件绑定，重新绑定
            self._bind_click_event(self._nsview)
        
        return self