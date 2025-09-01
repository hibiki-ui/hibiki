#!/usr/bin/env python3
"""
Hibiki UI v4.0 - Label组件
文本标签组件，支持响应式绑定和样式定制
"""

from typing import Optional, Union, Any
from Foundation import NSAttributedString
from ..core.styles import ComponentStyle
from ..core.logging import get_logger
from .base_text_field import _BaseTextField
from .text_field_config import TextFieldConfig, BezelStyle

logger = get_logger("components.label")
logger.setLevel("INFO")


class Label(_BaseTextField):
    """现代化Label组件
    
    基于Hibiki UI v4.0新架构的文本标签组件。
    支持完整的布局API和响应式绑定。
    
    🆕 新增功能：
    - 🎨 边框和背景支持 (bordered, background_color)
    - 📝 文本选择功能 (selectable)
    - 💎 边框样式定制 (bezel_style)
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 高层和低层API支持
    """
    
    def __init__(
        self,
        text: Union[str, Any, NSAttributedString],
        style: Optional[ComponentStyle] = None,
        # 🆕 新增Label特有功能
        selectable: bool = False,
        bordered: bool = False,
        bezel_style: Optional[BezelStyle] = None,
        background_color: Optional[str] = None,
        # 🎨 富文本支持
        rich_text_mode: bool = False,
        # 向后兼容参数
        text_props: Optional["TextProps"] = None,
        font_size: Optional[float] = None,
        font_weight: Optional[str] = None,
        font_family: Optional[str] = None,
        color: Optional[str] = None,
        text_align: Optional[str] = None,
        line_height: Optional[Union[int, float, str]] = None,
        font_style: Optional[str] = None,
        **style_kwargs,
    ):
        """🔧 新架构Label组件初始化
        
        Args:
            text: 标签文本内容，支持字符串或响应式Signal
            style: 组件样式对象
            selectable: 是否允许文本选择（用于复制等）
            bordered: 是否显示边框
            bezel_style: 边框样式 (BezelStyle.ROUNDED/SQUARE)
            background_color: 背景颜色 (如 "#FFFFFF")
            
            向后兼容参数:
            text_props, font_size, font_weight, color等
        """
        # 🏗️ 创建Label专用配置
        config = TextFieldConfig.for_label(
            selectable=selectable,
            bordered=bordered,
            background_color=background_color
        )
        
        # 设置边框样式
        if bordered and bezel_style:
            config.bezel_style = bezel_style
        elif bordered:
            config.bezel_style = BezelStyle.ROUNDED  # 默认圆角
        
        # 设置富文本模式
        config.rich_text_mode = rich_text_mode or isinstance(text, NSAttributedString)
        
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
        
        # 🔧 向后兼容：处理text_props参数
        if text_props:
            if hasattr(text_props, 'color') and text_props.color and not self.style.color:
                self.style.color = text_props.color
            if hasattr(text_props, 'font_size') and text_props.font_size and not self.style.font_size:
                self.style.font_size = text_props.font_size
            # 重新创建TextProps
            self._create_text_props()

        logger.debug(
            f"🏷️ Label创建: text='{text}', selectable={selectable}, bordered={bordered}, "
            f"bezel_style={bezel_style}, background={background_color}"
        )