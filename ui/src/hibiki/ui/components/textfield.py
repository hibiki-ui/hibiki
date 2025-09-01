#!/usr/bin/env python3
"""
Hibiki UI v4.0 - TextField组件
文本输入组件，支持输入验证和响应式绑定
"""

from typing import Optional, Union, Any, Callable
from Foundation import NSObject, NSAttributedString
import objc

from ..core.styles import ComponentStyle
from ..core.logging import get_logger
from .base_text_field import _BaseTextField
from .text_field_config import TextFieldConfig, BezelStyle

logger = get_logger("components.textfield")
logger.setLevel("INFO")


# TextFieldDelegate已在base_text_field.py中实现，此处无需重复定义


class TextField(_BaseTextField):
    """现代化TextField组件
    
    基于Hibiki UI v4.0新架构的文本输入组件。
    支持完整的布局API和响应式绑定。
    
    🆕 新增功能：
    - 🔧 完整边框样式控制 (BezelStyle.ROUNDED/SQUARE)
    - 🎨 背景颜色定制 (background_color)
    - 💬 占位符文本支持 (placeholder)
    - 📝 文本变化事件 (on_text_change)
    - 🎯 委托支持 (delegate)
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 输入验证和格式化
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        text: Union[str, Any, NSAttributedString] = "",
        style: Optional[ComponentStyle] = None,
        # 🆕 新增TextField特有功能
        placeholder: str = "",
        attributed_placeholder: Optional[NSAttributedString] = None,
        bordered: bool = True,
        bezel_style: Optional[BezelStyle] = None,
        background_color: Optional[str] = None,
        on_text_change: Optional[Callable[[str], None]] = None,
        delegate: Optional[Any] = None,
        # 🎨 富文本支持
        rich_text_mode: bool = False,
        # 向后兼容参数
        value: Union[str, Any] = None,
        on_change: Optional[Callable[[str], None]] = None,
        font_size: Optional[float] = None,
        font_weight: Optional[str] = None,
        font_family: Optional[str] = None,
        color: Optional[str] = None,
        text_align: Optional[str] = None,
        line_height: Optional[Union[int, float, str]] = None,
        font_style: Optional[str] = None,
        **style_kwargs,
    ):
        """🔧 新架构TextField组件初始化
        
        Args:
            text: 文本内容，支持字符串或响应式Signal
            style: 组件样式对象
            placeholder: 占位符文本
            bordered: 是否显示边框
            bezel_style: 边框样式 (BezelStyle.ROUNDED/SQUARE)
            background_color: 背景颜色 (如 "#FFFFFF")
            on_text_change: 文本变化回调函数
            delegate: 自定义委托对象
            
            向后兼容参数:
            value, on_change, font_size, font_weight, color等
        """
        # 🔄 向后兼容处理
        if value is not None:
            text = value
        if on_change is not None:
            on_text_change = on_change
        
        # 🏗️ 创建TextField专用配置
        config = TextFieldConfig.for_text_field(
            bordered=bordered,
            bezel_style=bezel_style or BezelStyle.ROUNDED,
            placeholder=placeholder,
            on_text_change=on_text_change,
            background_color=background_color
        )
        
        # 设置富文本相关配置
        config.rich_text_mode = rich_text_mode or isinstance(text, NSAttributedString)
        config.attributed_placeholder = attributed_placeholder
        
        # 设置自定义委托
        if delegate:
            config.delegate = delegate
        
        # 调用基类初始化
        super().__init__(
            text=text,
            style=style,
            config=config,
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            color=color,
            text_align=text_align,
            line_height=line_height,
            font_style=font_style,
            **style_kwargs
        )
        
        logger.debug(
            f"📝 TextField创建: text='{text}', placeholder='{placeholder}', "
            f"bordered={bordered}, bezel_style={bezel_style}, background={background_color}"
        )
    
    # 继承基类的_create_nsview方法，无需重写
    # _BaseTextField已经提供了完整的NSTextField创建和配置逻辑
    
    # 继承基类的事件绑定逻辑，无需重写
    # _BaseTextField已经提供了完整的事件绑定实现
    
    # 继承基类的get_text方法
    # def get_text(self) -> str: 已在_BaseTextField中实现
    
    def set_text(self, text: Union[str, Any]) -> "TextField":
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        super().set_text(text)
        return self
    
    def set_placeholder(self, placeholder: str) -> "TextField":
        """动态设置占位符文本
        
        Args:
            placeholder: 新的占位符文本
        """
        self.config.placeholder = placeholder
        
        if self._nsview:
            self._nsview.setPlaceholderString_(placeholder)
            logger.debug(f"💬 TextField占位符更新: '{placeholder}'")
        
        return self
    
    def set_bordered(self, bordered: bool, bezel_style: Optional[BezelStyle] = None) -> "TextField":
        """🆕 动态设置边框样式
        
        Args:
            bordered: 是否显示边框
            bezel_style: 边框样式 (可选)
        """
        self.config.bordered = bordered
        if bezel_style:
            self.config.bezel_style = bezel_style
        elif bordered:
            self.config.bezel_style = BezelStyle.ROUNDED
        
        if self._nsview:
            self._nsview.setBezeled_(bordered)
            logger.debug(f"🎨 TextField边框更新: bordered={bordered}, style={self.config.bezel_style}")
        
        return self
    
    def set_background_color(self, color: Optional[str]) -> "TextField":
        """🆕 动态设置背景颜色
        
        Args:
            color: 背景颜色 (如 "#FFFFFF"，None为透明)
        """
        self.config.background_color = color
        self.config.draws_background = color is not None
        
        if self._nsview:
            self._nsview.setDrawsBackground_(self.config.draws_background)
            if color:
                ns_color = self._parse_color(color)
                self._nsview.setBackgroundColor_(ns_color)
            logger.debug(f"🎨 TextField背景更新: color={color}")
        
        return self
    
    # 新增功能方法，旧版TextField可能缺少的功能
    
    @property
    def value(self) -> Union[str, Any]:
        """向后兼容：获取text属性"""
        return self.text
    
    @value.setter 
    def value(self, new_value: Union[str, Any]):
        """向后兼容：设置text属性"""
        self.set_text(new_value)