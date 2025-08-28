"""Hibiki UI v4 主题化系统

提供专业级外观定制和主题管理功能，支持：
- Light/Dark模式自动适应
- 响应式颜色系统
- 可组合字体方案
- 主题切换和观察
"""

# 基础主题系统
from .theme_manager import (
    ThemeManager, Theme, PresetThemes, ThemeChangeEvent,
    get_theme_manager, get_current_theme, set_theme, get_color, get_font
)
from .colors import ColorScheme, SystemColors, ColorRole, PresetColorSchemes
from .fonts import FontScheme, SystemFonts, TextStyle, PresetFontSchemes
from .appearance import (
    AppearanceManager, AppearanceMode, 
    get_appearance_manager, is_dark_mode, add_appearance_observer
)

__all__ = [
    # 主题管理
    "ThemeManager",
    "Theme", 
    "PresetThemes",
    "ThemeChangeEvent",
    "get_theme_manager",
    "get_current_theme", 
    "set_theme",
    "get_color",
    "get_font",
    
    # 颜色系统
    "ColorScheme",
    "SystemColors",
    "ColorRole",
    "PresetColorSchemes",
    
    # 字体系统
    "FontScheme",
    "SystemFonts",
    "TextStyle",
    "PresetFontSchemes",
    
    # 外观管理
    "AppearanceManager",
    "AppearanceMode",
    "get_appearance_manager",
    "is_dark_mode",
    "add_appearance_observer",
]