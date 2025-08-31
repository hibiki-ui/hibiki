#!/usr/bin/env python3
"""
Hibiki UI Debug Tools
=====================

专业的调试工具集，帮助开发者分析和优化 Hibiki UI 应用。

核心功能：
- 布局树可视化：类似 tree 命令的组件层次结构显示
- 性能监控：实时跟踪布局计算和组件生命周期
- 布局检查器：详细的组件样式和布局信息分析
- 导出工具：支持 JSON、HTML 等格式的调试信息导出
- 命令行工具：集成的CLI调试命令

使用示例：
```python
from hibiki.ui.debug import TreeVisualizer, PerformanceMonitor
from hibiki.ui.debug import inspect_layout, export_debug_info

# 可视化组件树
visualizer = TreeVisualizer()
tree_output = visualizer.format_tree(my_component)
print(tree_output)

# 性能监控
monitor = PerformanceMonitor()
monitor.start_monitoring(my_app)

# 布局检查
layout_info = inspect_layout(my_component)
export_debug_info(layout_info, "debug_report.html")
```
"""

from .tree_visualizer import TreeVisualizer, format_component_tree, ColorTheme
from .performance_monitor import PerformanceMonitor, get_performance_stats, MetricType
from .layout_inspector import LayoutInspector, inspect_layout, InspectionLevel
from .export_tools import export_debug_info, DebugExporter
from .cli import DebugCLI, debug_component_tree, debug_component_layout, quick_debug

# 便捷函数
def debug_tree(component) -> str:
    """快速显示组件树结构"""
    return format_component_tree(component)

def debug_performance(component) -> dict:
    """获取组件性能统计"""
    return get_performance_stats(component)

def debug_layout(component) -> dict:
    """检查组件布局信息"""
    return inspect_layout(component)

# 版本信息
__version__ = "1.0.0"
__author__ = "Hibiki UI Team"

# 导出的公共API
__all__ = [
    # 核心类
    "TreeVisualizer",
    "PerformanceMonitor", 
    "LayoutInspector",
    "DebugExporter",
    "DebugCLI",
    
    # 枚举和常量
    "ColorTheme",
    "MetricType", 
    "InspectionLevel",
    
    # 便捷函数
    "format_component_tree",
    "get_performance_stats",
    "inspect_layout",
    "export_debug_info",
    "debug_component_tree",
    "debug_component_layout", 
    "quick_debug",
    
    # 快捷API
    "debug_tree",
    "debug_performance", 
    "debug_layout",
]