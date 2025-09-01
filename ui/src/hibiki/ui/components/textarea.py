#!/usr/bin/env python3
"""
Hibiki UI v4.0 - TextArea组件
多行文本编辑器组件，支持滚动和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSScrollView, NSTextView, NSMakeRect
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle, px
from ..core.reactive import Signal, Computed, Effect
from ..core.logging import get_logger

logger = get_logger("components.textarea")
logger.setLevel("INFO")


class TextAreaDelegate(NSObject):
    """TextArea委托类，处理文本变化事件"""
    
    def init(self):
        self = objc.super(TextAreaDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.text_area = None
        return self
    
    def textDidChange_(self, notification):
        """文本内容变化时调用"""
        if hasattr(self, "callback") and self.callback:
            try:
                text_view = notification.object()
                new_text = text_view.string()
                self.callback(new_text)
            except Exception as e:
                logger.error(f"⚠️ TextArea文本变化回调错误: {e}")


class TextArea(UIComponent):
    """多行文本编辑器组件
    
    基于Hibiki UI v4.0架构的多行文本输入组件。
    支持滚动、文本换行、响应式绑定等功能。
    
    Features:
    - 多行文本编辑
    - 自动滚动支持
    - 响应式内容绑定
    - 占位符文本
    - 可配置的编辑模式
    - 完整的布局支持
    """
    
    def __init__(
        self,
        text: Union[str, Any] = "",
        placeholder: str = "",
        style: Optional[ComponentStyle] = None,
        editable: bool = True,
        on_text_change: Optional[Callable[[str], None]] = None,
        **style_kwargs,
    ):
        """初始化TextArea组件
        
        Args:
            text: 初始文本内容，支持Signal绑定
            placeholder: 占位符文本
            style: 组件样式对象
            editable: 是否可编辑
            on_text_change: 文本变化回调函数
            **style_kwargs: 样式快捷参数
        """
        # 确保有合适的默认尺寸
        if style is None:
            style = ComponentStyle(width=px(300), height=px(150))
        
        super().__init__(style, **style_kwargs)
        self.text = text
        self.placeholder = placeholder
        self.editable = editable
        self.on_text_change = on_text_change
        
        # 检查是否为响应式文本
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        self._bindings = []  # 存储绑定清理函数
        self._text_delegate = None
        
        logger.debug(f"📝 TextArea创建: text_length={len(str(text))}, editable={editable}")
    
    def _create_nsview(self) -> NSView:
        """创建多行文本编辑器NSView"""
        # 创建滚动视图容器
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(0, 0, 300, 150))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setHasHorizontalScroller_(False)
        scroll_view.setAutohidesScrollers_(False)
        scroll_view.setBorderType_(1)  # NSBezelBorder
        
        # 创建文本视图
        text_view = NSTextView.alloc().init()
        text_view.setVerticallyResizable_(True)
        text_view.setHorizontallyResizable_(False)
        text_view.setAutoresizingMask_(2)  # NSViewWidthSizable
        
        # 设置文本内容
        initial_text = ""
        if self._is_reactive_text:
            initial_text = str(getattr(self.text, "value", ""))
        else:
            initial_text = str(self.text)
        
        text_view.setString_(initial_text)
        
        # 设置编辑模式
        text_view.setEditable_(self.editable)
        text_view.setSelectable_(True)
        
        # 设置占位符（如果为空）
        if not initial_text and self.placeholder:
            # 注意：NSTextView没有直接的placeholder支持
            # 这里可以通过其他方式实现占位符效果
            pass
        
        # 将文本视图添加到滚动视图
        scroll_view.setDocumentView_(text_view)
        
        # 设置文本变化事件
        if self.on_text_change:
            self._bind_text_change_event(text_view)
        
        # 响应式绑定
        if self._is_reactive_text:
            from ..core.binding import ReactiveBinding
            
            binding_cleanup = ReactiveBinding.bind(text_view, "string", self.text)
            self._bindings.append(binding_cleanup)
            logger.debug(f"🔗 TextArea响应式绑定已创建")
        
        # 保存文本视图引用以便后续操作
        self._text_view = text_view
        
        return scroll_view
    
    def _bind_text_change_event(self, text_view):
        """绑定文本变化事件"""
        # 创建委托对象
        delegate = TextAreaDelegate.alloc().init()
        delegate.callback = self.on_text_change
        delegate.text_area = self  # 保持对TextArea的引用
        
        text_view.setDelegate_(delegate)
        self._text_delegate = delegate  # 保持引用防止被垃圾回收
        logger.debug("🔗 TextArea文本变化事件已绑定")
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if hasattr(self, "_text_view") and self._text_view:
            return self._text_view.string()
        if self._is_reactive_text:
            return str(getattr(self.text, "value", ""))
        return str(self.text)
    
    def set_text(self, text: Union[str, Any]) -> "TextArea":
        """动态设置文本内容"""
        self.text = text
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        if hasattr(self, "_text_view") and self._text_view:
            if self._is_reactive_text:
                content = str(getattr(text, "value", ""))
            else:
                content = str(text)
            self._text_view.setString_(content)
            logger.debug(f"📝 TextArea文本更新: length={len(content)}")
        
        return self
    
    def set_editable(self, editable: bool) -> "TextArea":
        """设置是否可编辑"""
        self.editable = editable
        if hasattr(self, "_text_view") and self._text_view:
            self._text_view.setEditable_(editable)
        return self
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        if hasattr(self, "_text_view") and self._text_view:
            text_length = len(self._text_view.string())
            self._text_view.scrollRangeToVisible_((text_length, 0))