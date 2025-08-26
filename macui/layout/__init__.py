"""
macUI Layout Engine v3.0 - Professional Stretchable-based Layout System

基于Taffy (Rust)布局引擎的专业级布局系统架构
实现方案B: 纯布局引擎架构 (Pure Layout Engine Architecture)

核心组件:
- LayoutEngine: 布局引擎核心
- LayoutTree: 布局树管理
- LayoutNode: 布局节点抽象
- CSS-like声明式API
"""

from .engine import LayoutEngine
from .node import LayoutNode
from .tree import LayoutTree
from .styles import (
    FlexDirection,
    AlignItems, 
    JustifyContent,
    Display,
    Position,
    LayoutStyle
)

__all__ = [
    'LayoutEngine',
    'LayoutNode', 
    'LayoutTree',
    'FlexDirection',
    'AlignItems',
    'JustifyContent',
    'Display',
    'Position',
    'LayoutStyle'
]