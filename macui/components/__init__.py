"""
macUI v3.0 统一组件接口
基于Stretchable布局引擎的现代化组件库，提供简洁统一的API
"""

# 导入最佳的现代化实现 - 来自modern_components.py
from .modern_components import ModernLabel as Label
from .modern_components import ModernButton as Button
from .modern_components import LineBreakMode, LabelStyle

# 导入现代化布局组件  
from .modern_layout import ModernVStack as VStack
from .modern_layout import ModernHStack as HStack

# 导入样式系统
from ..layout.styles import LayoutStyle

__all__ = [
    # 基础组件（现代化实现）
    "Label",          # -> ModernLabel (最佳实现)
    "Button",         # -> ModernButton (最佳实现)
    
    # 布局组件（现代化实现）
    "VStack",         # -> ModernVStack (支持Stretchable)
    "HStack",         # -> ModernHStack (支持Stretchable) 
    
    # 样式系统
    "LayoutStyle",
    
    # 文本相关枚举
    "LineBreakMode",  # 文本换行模式
    "LabelStyle",     # Label预设样式
]