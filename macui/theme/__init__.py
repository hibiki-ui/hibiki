"""macUI v2 主题化系统

提供专业级外观定制和主题管理功能，支持：
- Light/Dark模式自动适应
- 响应式颜色系统
- 可组合样式对象
- 高级视觉效果（毛玻璃、阴影、动画）
- 设计令牌系统
- JSON主题定义
"""

# 基础主题系统
from .theme_manager import ThemeManager, Theme, PresetThemes, get_theme_manager, get_current_theme, set_theme, get_color, get_font
from .colors import ColorScheme, SystemColors, ColorRole, PresetColorSchemes
from .fonts import FontScheme, SystemFonts, TextStyle, PresetFontSchemes
from .appearance import AppearanceManager, AppearanceMode, get_appearance_manager, is_dark_mode, add_appearance_observer

# 增强主题系统
from .reactive_colors import ReactiveColor, ReactiveColorScheme, ReactiveColorFactory
from .styles import Style, Styles, ComputedStyle, StyleBuilder, style, responsive_style
from .visual_effects import (
    VisualEffect, VisualEffectMaterials, GlassBox, LayerEffects, StyleApplicator,
    glass_box, apply_glass_effect
)
from .enhanced_theme_manager import (
    EnhancedTheme, EnhancedThemeManager, DesignTokens,
    get_enhanced_theme_manager, current_theme, theme_color, theme_style, theme_spacing
)

__all__ = [
    # 基础主题系统
    "ThemeManager",
    "Theme", 
    "PresetThemes",
    "get_theme_manager",
    "get_current_theme", 
    "set_theme",
    "get_color",
    "get_font",
    "ColorScheme",
    "SystemColors",
    "ColorRole",
    "PresetColorSchemes",
    "FontScheme",
    "SystemFonts",
    "TextStyle",
    "PresetFontSchemes",
    "AppearanceManager",
    "AppearanceMode",
    "get_appearance_manager",
    "is_dark_mode",
    "add_appearance_observer",
    
    # 增强主题系统
    "ReactiveColor",
    "ReactiveColorScheme", 
    "ReactiveColorFactory",
    "Style",
    "Styles",
    "ComputedStyle",
    "StyleBuilder",
    "style",
    "responsive_style",
    "VisualEffect",
    "VisualEffectMaterials",
    "GlassBox",
    "LayerEffects",
    "StyleApplicator",
    "glass_box",
    "apply_glass_effect",
    "EnhancedTheme",
    "EnhancedThemeManager",
    "DesignTokens",
    "get_enhanced_theme_manager",
    "current_theme",
    "theme_color",
    "theme_style",
    "theme_spacing"
]