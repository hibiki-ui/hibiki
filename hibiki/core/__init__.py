#!/usr/bin/env python3
"""
Hibiki UI v4 Core Module
核心模块导出
"""

# 核心组件系统
from .component import Component, UIComponent, Container

# 响应式系统
from .reactive import Signal, Computed, Effect, create_signal, create_computed, create_effect

# 样式系统
from .styles import ComponentStyle, StylePresets, px, percent, auto

# 绑定系统
from .binding import ReactiveBinding, FormDataBinding

# 文本属性系统
from .text_props import TextProps, TextStyles, text_props

# 布局系统
from .layout import get_layout_engine, LayoutNode, V4LayoutEngine

# 管理器系统
from .managers import ManagerFactory

# 动画系统
from .animation import (
    Animation, AnimationGroup, AnimationManager, 
    AnimationCurve, AnimationProperty, AnimationState,
    animate, fade_in, fade_out, bounce
)

__all__ = [
    # 组件系统
    'Component',
    'UIComponent', 
    'Container',
    
    # 响应式系统
    'Signal',
    'Computed',
    'Effect',
    'create_signal',
    'create_computed', 
    'create_effect',
    
    # 样式系统
    'ComponentStyle',
    'StylePresets',
    'px',
    'percent', 
    'auto',
    
    # 绑定系统
    'ReactiveBinding',
    'FormDataBinding',
    
    # 文本属性系统
    'TextProps',
    'TextStyles',
    'text_props',
    
    # 布局系统
    'get_layout_engine',
    'LayoutNode',
    'V4LayoutEngine',
    
    # 管理器系统
    'ManagerFactory',
    
    # 动画系统
    'Animation',
    'AnimationGroup',
    'AnimationManager',
    'AnimationCurve',
    'AnimationProperty', 
    'AnimationState',
    'animate',
    'fade_in',
    'fade_out',
    'bounce'
]