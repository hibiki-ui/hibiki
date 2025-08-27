"""
macUI v3.0 统一组件接口
基于Stretchable布局引擎的现代化组件库，提供简洁统一的API
"""

# 导入核心组件 - 直接使用最佳实现
from .components import Label, Button
from .components import LineBreakMode, LabelStyle

# 导入布局组件  
from .layout import VStackLayout as VStack
from .layout import HStackLayout as HStack

# 导入样式系统
from ..layout.styles import LayoutStyle

__all__ = [
    # 基础组件
    "Label",          # 文本标签组件
    "Button",         # 按钮组件
    
    # 布局组件
    "VStack",         # 垂直布局（支持Stretchable引擎）
    "HStack",         # 水平布局（支持Stretchable引擎） 
    
    # 样式系统
    "LayoutStyle",    # 布局样式
    
    # 文本相关枚举
    "LineBreakMode",  # 文本换行模式
    "LabelStyle",     # Label预设样式
]