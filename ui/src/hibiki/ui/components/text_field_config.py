#!/usr/bin/env python3
"""
Hibiki UI v4.0 - TextField配置系统
提供NSTextField的完整功能配置
"""

from dataclasses import dataclass
from typing import Optional, Callable, Any, Union
from enum import Enum
from Foundation import NSAttributedString


class BezelStyle(Enum):
    """边框样式枚举"""
    NONE = "none"
    ROUNDED = "rounded" 
    SQUARE = "square"


@dataclass
class TextFieldConfig:
    """NSTextField完整配置对象"""
    
    # 🔧 核心功能配置
    editable: bool = False
    selectable: bool = False
    
    # 🎨 外观配置
    bordered: bool = False
    bezel_style: Optional[BezelStyle] = None
    draws_background: bool = False
    background_color: Optional[str] = None
    
    # 📝 文本功能
    placeholder: Optional[str] = None
    
    # 🎨 富文本支持
    rich_text_mode: bool = False
    attributed_placeholder: Optional[NSAttributedString] = None
    
    # 🔗 事件配置
    on_text_change: Optional[Callable[[str], None]] = None
    delegate: Optional[Any] = None
    
    @classmethod
    def for_label(
        cls, 
        selectable: bool = False,
        bordered: bool = False,
        background_color: Optional[str] = None
    ) -> "TextFieldConfig":
        """创建Label专用配置"""
        return cls(
            editable=False,      # Label不可编辑
            selectable=selectable,
            bordered=bordered,
            bezel_style=BezelStyle.NONE if not bordered else BezelStyle.ROUNDED,
            draws_background=background_color is not None,
            background_color=background_color,
        )
    
    @classmethod  
    def for_text_field(
        cls,
        bordered: bool = True,
        bezel_style: BezelStyle = BezelStyle.ROUNDED,
        placeholder: Optional[str] = None,
        on_text_change: Optional[Callable[[str], None]] = None,
        background_color: Optional[str] = None
    ) -> "TextFieldConfig":
        """创建TextField专用配置"""
        return cls(
            editable=True,       # TextField可编辑
            selectable=True,     # TextField可选择
            bordered=bordered,
            bezel_style=bezel_style,
            draws_background=True,  # TextField默认有背景
            background_color=background_color,
            placeholder=placeholder,
            on_text_change=on_text_change,
        )