#!/usr/bin/env python3
"""
macUI v4 Framework
完整的响应式UI框架，包含：
- 统一组件API
- 响应式系统
- 主题管理
- 布局引擎
- 动画系统
"""

# 核心系统
from .core import (
    Component, UIComponent, Container,
    Signal, Computed, Effect, create_signal, create_computed, create_effect,
    ComponentStyle, StylePresets, px, percent, auto,
    ReactiveBinding, FormDataBinding,
    get_layout_engine, LayoutNode, V4LayoutEngine,
    ManagerFactory,
    Animation, AnimationGroup, AnimationManager,
    AnimationCurve, AnimationProperty, AnimationState,
    animate, fade_in, fade_out, bounce
)

# 组件系统
from .components import (
    # 基础组件
    Label, Button, TextField, Slider, Switch,
    # 自定义组件
    CustomView, DrawingUtils
)

# 主题系统
from .theme import (
    ThemeManager, Theme, PresetThemes, ThemeChangeEvent,
    get_theme_manager, get_current_theme, set_theme, get_color, get_font,
    ColorScheme, SystemColors, ColorRole, PresetColorSchemes,
    FontScheme, SystemFonts, TextStyle, PresetFontSchemes,
    AppearanceManager, AppearanceMode,
    get_appearance_manager, is_dark_mode, add_appearance_observer
)

__all__ = [
    # 核心系统
    'Component', 'UIComponent', 'Container',
    'Signal', 'Computed', 'Effect', 'create_signal', 'create_computed', 'create_effect',
    'ComponentStyle', 'StylePresets', 'px', 'percent', 'auto',
    'ReactiveBinding', 'FormDataBinding',
    'get_layout_engine', 'LayoutNode', 'V4LayoutEngine',
    'ManagerFactory',
    'Animation', 'AnimationGroup', 'AnimationManager',
    'AnimationCurve', 'AnimationProperty', 'AnimationState',
    'animate', 'fade_in', 'fade_out', 'bounce',
    
    # 组件系统
    'Label', 'Button', 'TextField', 'Slider', 'Switch',
    'CustomView', 'DrawingUtils',
    
    # 主题系统
    'ThemeManager', 'Theme', 'PresetThemes', 'ThemeChangeEvent',
    'get_theme_manager', 'get_current_theme', 'set_theme', 'get_color', 'get_font',
    'ColorScheme', 'SystemColors', 'ColorRole', 'PresetColorSchemes',
    'FontScheme', 'SystemFonts', 'TextStyle', 'PresetFontSchemes',
    'AppearanceManager', 'AppearanceMode',
    'get_appearance_manager', 'is_dark_mode', 'add_appearance_observer'
]