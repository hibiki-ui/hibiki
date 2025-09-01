#!/usr/bin/env python3
"""
Hibiki UI v4.0 - TextField组件
文本输入组件，支持输入验证和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from AppKit import NSView, NSTextField
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed
from ..core.binding import bind_text
from ..core.logging import get_logger

logger = get_logger("components.textfield")
logger.setLevel("INFO")


# TextField事件委托类
class TextFieldDelegate(NSObject):
    """TextField事件委托类"""
    
    def init(self):
        self = objc.super(TextFieldDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.textfield_component = None
        return self
    
    def controlTextDidChange_(self, notification):
        """文本改变时的处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                # 获取当前文本内容
                textfield = notification.object()
                current_text = textfield.stringValue()
                
                # 更新组件的值
                if hasattr(self, "textfield_component") and self.textfield_component:
                    if self.textfield_component._is_reactive_value and hasattr(
                        self.textfield_component.value, "value"
                    ):
                        self.textfield_component.value.value = current_text
                    else:
                        self.textfield_component.value = current_text
                
                # 调用回调函数
                self.callback(current_text)
                logger.debug(f"📝 TextField文本改变: '{current_text}'")
            
            except Exception as e:
                logger.error(f"⚠️ TextField文本改变回调错误: {e}")


class TextField(UIComponent):
    """现代化TextField组件
    
    基于Hibiki UI v4.0新架构的文本输入组件。
    支持完整的布局API和响应式绑定。
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 占位符文本支持
    - 输入验证和格式化
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        value: Union[str, Any] = "",
        placeholder: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        style: Optional[ComponentStyle] = None,
        **style_kwargs,
    ):
        """🏗️ CORE METHOD: TextField component initialization
        
        Args:
            value: 初始文本值，支持字符串或响应式Signal
            placeholder: 占位符文本
            on_change: 文本改变事件回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        self._delegate = None
        
        logger.debug(
            f"📝 TextField创建: value='{value}', placeholder='{placeholder}', reactive={self._is_reactive_value}"
        )
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为文本输入框"""
        textfield = NSTextField.alloc().init()
        
        # 基础配置
        textfield.setBezeled_(True)  # 有边框
        textfield.setDrawsBackground_(True)  # 有背景
        textfield.setEditable_(True)  # 可编辑
        textfield.setSelectable_(True)  # 可选择
        
        # 设置初始值 - 使用响应式绑定系统
        
        # 绑定文本值，自动处理响应式和静态值
        binding_cleanup = bind_text(textfield, self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            logger.debug(f"🔗 TextField响应式绑定已创建: {self.value}")
        else:
            logger.debug(f"📝 TextField静态值已设置: {str(self.value)}")
        
        # 设置占位符
        if self.placeholder:
            textfield.setPlaceholderString_(self.placeholder)
            logger.debug(f"💬 TextField占位符: '{self.placeholder}'")
        
        # 绑定文本改变事件
        if self.on_change:
            self._bind_text_change_event(textfield)
        
        return textfield
    
    def _bind_text_change_event(self, textfield: NSTextField):
        """绑定文本改变事件"""
        try:
            # 使用TextFieldDelegate类
            self._delegate = TextFieldDelegate.alloc().init()
            if self._delegate is None:
                logger.warning("⚠️ 无法创建TextFieldDelegate")
                return
            
            self._delegate.callback = self.on_change
            self._delegate.textfield_component = self  # 保存组件引用
            
            textfield.setDelegate_(self._delegate)
            
            logger.debug(f"🔗 TextField文本改变事件已绑定")
        
        except Exception as e:
            logger.warning(f"⚠️ TextField事件绑定失败: {e}")
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if self._nsview:
            return self._nsview.stringValue()
        return str(self.value)
    
    def set_text(self, text: str) -> "TextField":
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.value = text
        from ..core.reactive import Signal, Computed
        
        self._is_reactive_value = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_value:
                content = str(getattr(text, "value", text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            logger.debug(f"📝 TextField文本更新: '{content}'")
        
        return self
    
    def set_placeholder(self, placeholder: str) -> "TextField":
        """动态设置占位符文本
        
        Args:
            placeholder: 新的占位符文本
        """
        self.placeholder = placeholder
        
        if self._nsview:
            self._nsview.setPlaceholderString_(placeholder)
            logger.debug(f"💬 TextField占位符更新: '{placeholder}'")
        
        return self