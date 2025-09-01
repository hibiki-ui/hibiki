#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Label组件
文本标签组件，支持响应式绑定和样式定制
"""

from typing import Optional, Union, Any
from AppKit import NSView, NSTextField, NSLineBreakByWordWrapping, NSMakeRect

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect
from ..core.binding import bind_text
from ..core.logging import get_logger

logger = get_logger("components.label")
logger.setLevel("INFO")


class Label(UIComponent):
    """现代化Label组件
    
    基于Hibiki UI v4.0新架构的文本标签组件。
    支持完整的布局API和响应式绑定。
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        text: Union[str, Any],
        style: Optional[ComponentStyle] = None,
        text_props: Optional["TextProps"] = None,
        # 便捷参数 - 向后兼容，会自动合并到ComponentStyle
        text_style: Optional[str] = None,
        font_size: Optional[float] = None,
        font_weight: Optional[str] = None,
        font_family: Optional[str] = None,
        color: Optional[str] = None,
        text_align: Optional[str] = None,
        line_height: Optional[Union[int, float, str]] = None,
        font_style: Optional[str] = None,
        **style_kwargs,
    ):
        """🔧 统一API：Label组件初始化，文本属性统一到ComponentStyle
        
        Args:
            text: 标签文本内容，支持字符串或响应式Signal
            style: 组件样式对象 (包含文本属性)
            text_props: 文本属性对象 (向后兼容)
            
            便捷参数 (向后兼容，会自动合并到ComponentStyle):
            font_size, font_weight, font_family, color, text_align等
            **style_kwargs: 样式快捷参数
        """
        # 🔧 统一样式处理：将便捷参数合并到ComponentStyle
        if not style:
            from ..core.styles import ComponentStyle
            style = ComponentStyle()
        
        # 合并便捷文本参数到ComponentStyle
        text_params = {
            'color': color,
            'font_size': font_size,
            'font_weight': font_weight,
            'font_family': font_family,
            'text_align': text_align,
            'line_height': line_height,
            'font_style': font_style
        }
        
        for param, value in text_params.items():
            if value is not None:
                # 只有当style中对应属性为None时才设置
                if getattr(style, param) is None:
                    setattr(style, param, value)
        
        super().__init__(style, **style_kwargs)
        self.text = text
        
        # 🔧 向后兼容：处理text_props参数
        if text_props:
            # 如果提供了text_props，从中提取属性到style
            if hasattr(text_props, 'color') and text_props.color and not self.style.color:
                self.style.color = text_props.color
            if hasattr(text_props, 'font_size') and text_props.font_size and not self.style.font_size:
                self.style.font_size = text_props.font_size
            # 可以继续添加其他属性的映射
            
            self.text_props = text_props
        else:
            # 从ComponentStyle创建对应的TextProps (向后兼容)
            from ..core.text_props import TextProps
            
            self.text_props = TextProps(
                color=self.style.color,
                font_size=self.style.font_size,
                font_weight=self.style.font_weight,
                font_family=self.style.font_family,
                text_align=self.style.text_align,
            )
        
        # 检查是否为响应式文本
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        logger.debug(
            f"🏷️ Label创建: text='{text}', reactive={self._is_reactive_text}, text_props={bool(self.text_props)}"
        )
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为Label"""
        # 🔧 修复：使用固定frame创建，防止自动尺寸调整
        label = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 100, 20))
        
        # 基础配置
        label.setBezeled_(False)  # 无边框
        label.setDrawsBackground_(False)  # 无背景
        label.setEditable_(False)  # 不可编辑
        label.setSelectable_(False)  # 不可选择
        
        # 🔑 关键修复：多层面禁用自动尺寸调整
        label.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # 禁用内容驱动的尺寸调整
        if hasattr(label, 'setPreferredMaxLayoutWidth_'):
            label.setPreferredMaxLayoutWidth_(0)
        # 强制禁用自动尺寸适配
        label.setAutoresizingMask_(0)
        
        # 设置文本内容 - 使用响应式绑定系统
        
        # 绑定文本，自动处理响应式和静态文本
        binding_cleanup = bind_text(label, self.text)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            logger.debug(f"🔗 Label响应式绑定已创建: {self.text}")
        else:
            logger.debug(f"📝 Label静态文本已设置: {str(self.text)}")
        
        # 多行文本支持配置
        label.setUsesSingleLineMode_(False)
        label.setLineBreakMode_(NSLineBreakByWordWrapping)
        
        # 设置首选最大宽度以支持自动换行
        if self.style.width:
            if hasattr(self.style.width, "value"):
                width_value = self.style.width.value
                if isinstance(width_value, (int, float)):
                    label.setPreferredMaxLayoutWidth_(float(width_value))
        
        # 应用文本样式
        if self.text_props:
            # 设置字体
            font = self.text_props.to_nsfont()
            label.setFont_(font)
            logger.debug(f"🔤 Label字体: {font.fontName()}, 大小: {font.pointSize()}")
            
            # 设置文字颜色
            color = self.text_props.to_nscolor()
            label.setTextColor_(color)
            
            # 设置文本对齐
            alignment = self.text_props.get_text_alignment()
            label.setAlignment_(alignment)
            
            logger.debug(f"🎨 Label样式已应用: 字体={font.fontName()}, 对齐={alignment}")
        
        return label
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if self._nsview:
            return self._nsview.stringValue()
        if self._is_reactive_text:
            return str(getattr(self.text, "value", self.text))
        return str(self.text)
    
    def set_text(self, text: Union[str, Any]) -> "Label":
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.text = text
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_text:
                content = str(getattr(text, "value", text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            logger.debug(f"📝 Label文本更新: '{content}'")
        
        return self