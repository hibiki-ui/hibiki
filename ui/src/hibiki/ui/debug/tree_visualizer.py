#!/usr/bin/env python3
"""
Tree Visualizer - 组件树可视化工具
=================================

提供类似 Unix tree 命令的组件层次结构可视化功能。
基于 ScrollableContainer 调试过程中开发的成功实现。
"""

import time
from typing import Dict, Any, Optional, List, Union
from enum import Enum

from ..core.logging import get_logger
from ..core.layout import get_layout_engine

logger = get_logger("debug.tree_visualizer")


class ColorTheme(Enum):
    """颜色主题枚举"""
    NONE = "none"           # 无颜色
    TERMINAL = "terminal"   # 终端颜色
    HTML = "html"          # HTML颜色


class TreeVisualizer:
    """组件树可视化工具
    
    功能特性：
    - 树状结构显示（类似 tree 命令）
    - 健康状态可视化（✅❌符号）
    - 性能指标集成（布局时间、子组件数量）
    - 多种输出格式（纯文本、带颜色、HTML）
    - 可配置的显示选项
    """
    
    def __init__(self, 
                 color_theme: ColorTheme = ColorTheme.TERMINAL,
                 show_performance: bool = True,
                 show_memory_info: bool = False,
                 max_depth: Optional[int] = None):
        """初始化树状可视化工具
        
        Args:
            color_theme: 颜色主题
            show_performance: 是否显示性能信息
            show_memory_info: 是否显示内存信息
            max_depth: 最大显示深度
        """
        self.color_theme = color_theme
        self.show_performance = show_performance
        self.show_memory_info = show_memory_info
        self.max_depth = max_depth
        
        # 性能统计
        self._stats = {
            "total_nodes": 0,
            "healthy_nodes": 0,
            "unhealthy_nodes": 0,
            "max_depth": 0,
            "generation_time": 0.0
        }
    
    def format_tree(self, component, title: Optional[str] = None) -> str:
        """格式化组件树为字符串
        
        Args:
            component: 要可视化的根组件
            title: 可选的标题
            
        Returns:
            格式化后的树状字符串
        """
        start_time = time.time()
        
        # 重置统计信息
        self._stats = {
            "total_nodes": 0,
            "healthy_nodes": 0, 
            "unhealthy_nodes": 0,
            "max_depth": 0,
            "generation_time": 0.0
        }
        
        # 获取布局树信息
        engine = get_layout_engine()
        tree_info = engine.get_node_tree_info(component)
        
        if not tree_info:
            return self._format_error("❌ 无法获取组件树信息")
        
        # 生成树状结构
        result_lines = []
        
        if title:
            result_lines.append(self._format_title(title))
            result_lines.append("")
        
        # 递归生成树结构
        tree_output = self._format_node_recursive(tree_info, "", True, 0)
        result_lines.append(tree_output)
        
        # 添加统计信息
        if self.show_performance:
            result_lines.append("")
            result_lines.extend(self._format_stats())
        
        # 记录生成时间
        self._stats["generation_time"] = time.time() - start_time
        
        return "\n".join(result_lines)
    
    def _format_node_recursive(self, node_info: Dict[str, Any], 
                             prefix: str, is_last: bool, depth: int) -> str:
        """递归格式化节点
        
        Args:
            node_info: 节点信息字典
            prefix: 当前行的前缀
            is_last: 是否是最后一个子节点
            depth: 当前深度
            
        Returns:
            格式化后的节点字符串
        """
        # 检查深度限制
        if self.max_depth is not None and depth > self.max_depth:
            return prefix + self._format_text("...", "dim")
        
        # 更新统计
        self._stats["total_nodes"] += 1
        self._stats["max_depth"] = max(self._stats["max_depth"], depth)
        
        # 获取节点信息
        component_type = node_info.get('component_type', 'Unknown')
        node_key = node_info.get('node_key', 'N/A')
        children_count = node_info.get('children_count', 0)
        stretchable_valid = node_info.get('stretchable_valid', False)
        
        # 更新健康状态统计
        if stretchable_valid:
            self._stats["healthy_nodes"] += 1
        else:
            self._stats["unhealthy_nodes"] += 1
        
        # 格式化当前节点
        connector = "└── " if is_last else "├── "
        status_icon = self._format_status_icon(stretchable_valid)
        
        # 主要节点信息
        node_text = f"{component_type} ({self._format_node_id(node_key)})"
        
        # 子组件数量
        children_text = self._format_children_count(children_count)
        
        # 性能信息（如果启用）
        perf_text = ""
        if self.show_performance:
            perf_text = self._format_performance_info(node_info)
        
        # 内存信息（如果启用）  
        memory_text = ""
        if self.show_memory_info:
            memory_text = self._format_memory_info(node_info)
        
        # 组合当前行
        current_line = (prefix + connector + node_text + " " + 
                       children_text + " " + status_icon + 
                       perf_text + memory_text)
        
        result = current_line + "\n"
        
        # 处理子节点
        children = node_info.get('children', [])
        if children:
            for i, child in enumerate(children):
                is_child_last = (i == len(children) - 1)
                child_prefix = prefix + ("    " if is_last else "│   ")
                result += self._format_node_recursive(
                    child, child_prefix, is_child_last, depth + 1
                )
        
        return result
    
    def _format_status_icon(self, is_healthy: bool) -> str:
        """格式化状态图标"""
        if is_healthy:
            return self._format_text("✅", "green")
        else:
            return self._format_text("❌", "red")
    
    def _format_node_id(self, node_key: str) -> str:
        """格式化节点ID"""
        return self._format_text(node_key, "dim")
    
    def _format_children_count(self, count: int) -> str:
        """格式化子组件数量"""
        text = f"[{count} children]"
        if count == 0:
            return self._format_text(text, "dim")
        elif count > 10:
            return self._format_text(text, "yellow")
        else:
            return self._format_text(text, "blue")
    
    def _format_performance_info(self, node_info: Dict[str, Any]) -> str:
        """格式化性能信息"""
        # TODO: 从布局引擎获取更详细的性能信息
        return ""
    
    def _format_memory_info(self, node_info: Dict[str, Any]) -> str:
        """格式化内存信息"""
        # TODO: 添加内存使用统计
        return ""
    
    def _format_title(self, title: str) -> str:
        """格式化标题"""
        return self._format_text(f"🌳 {title}", "bold")
    
    def _format_stats(self) -> List[str]:
        """格式化统计信息"""
        # 预先计算时间字符串避免嵌套f-string
        time_str = f"{self._stats['generation_time']:.2f}ms"
        
        stats_lines = [
            self._format_text("📊 树结构统计:", "bold"),
            f"   总节点数: {self._format_text(str(self._stats['total_nodes']), 'blue')}",
            f"   健康节点: {self._format_text(str(self._stats['healthy_nodes']), 'green')}",
            f"   异常节点: {self._format_text(str(self._stats['unhealthy_nodes']), 'red')}",
            f"   最大深度: {self._format_text(str(self._stats['max_depth']), 'blue')}",
            f"   生成耗时: {self._format_text(time_str, 'blue')}"
        ]
        return stats_lines
    
    def _format_error(self, message: str) -> str:
        """格式化错误信息"""
        return self._format_text(message, "red")
    
    def _format_text(self, text: str, style: str) -> str:
        """根据主题格式化文本
        
        Args:
            text: 要格式化的文本
            style: 样式类型 (red, green, blue, yellow, bold, dim)
            
        Returns:
            格式化后的文本
        """
        if self.color_theme == ColorTheme.NONE:
            return text
        elif self.color_theme == ColorTheme.TERMINAL:
            return self._apply_terminal_color(text, style)
        elif self.color_theme == ColorTheme.HTML:
            return self._apply_html_color(text, style)
        else:
            return text
    
    def _apply_terminal_color(self, text: str, style: str) -> str:
        """应用终端颜色代码"""
        color_codes = {
            "red": "\033[91m",
            "green": "\033[92m", 
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "bold": "\033[1m",
            "dim": "\033[2m",
            "reset": "\033[0m"
        }
        
        code = color_codes.get(style, "")
        reset = color_codes["reset"]
        return f"{code}{text}{reset}"
    
    def _apply_html_color(self, text: str, style: str) -> str:
        """应用HTML颜色样式"""
        html_styles = {
            "red": "color: #e74c3c;",
            "green": "color: #2ecc71;",
            "yellow": "color: #f39c12;", 
            "blue": "color: #3498db;",
            "bold": "font-weight: bold;",
            "dim": "opacity: 0.6;",
        }
        
        style_attr = html_styles.get(style, "")
        if style_attr:
            return f'<span style="{style_attr}">{text}</span>'
        else:
            return text
    
    def get_stats(self) -> Dict[str, Any]:
        """获取最近一次生成的统计信息"""
        return self._stats.copy()


# 便捷函数
def format_component_tree(component, 
                         title: Optional[str] = None,
                         color: bool = True,
                         show_performance: bool = True) -> str:
    """快速格式化组件树
    
    Args:
        component: 要可视化的组件
        title: 可选标题
        color: 是否使用颜色
        show_performance: 是否显示性能信息
        
    Returns:
        格式化的树状字符串
    """
    theme = ColorTheme.TERMINAL if color else ColorTheme.NONE
    visualizer = TreeVisualizer(
        color_theme=theme,
        show_performance=show_performance
    )
    
    return visualizer.format_tree(component, title)


# 用于向后兼容的函数（基于原始实现）
def format_tree_structure(tree_info: dict, prefix: str = "", is_last: bool = True) -> str:
    """向后兼容的树结构格式化函数
    
    这是原始调试过程中使用的函数，保留用于兼容性。
    新代码建议使用 TreeVisualizer 类或 format_component_tree 函数。
    """
    if not tree_info:
        return ""
    
    # 获取节点信息
    component_type = tree_info.get('component_type', 'Unknown')
    node_key = tree_info.get('node_key', 'N/A')
    children_count = tree_info.get('children_count', 0)
    stretchable_valid = tree_info.get('stretchable_valid', False)
    
    # 格式化当前节点
    connector = "└── " if is_last else "├── "
    status_icon = "✅" if stretchable_valid else "❌"
    node_info = f"{component_type} ({node_key}) [{children_count} children] {status_icon}"
    
    result = prefix + connector + node_info + "\n"
    
    # 处理子节点
    children = tree_info.get('children', [])
    if children:
        for i, child in enumerate(children):
            is_child_last = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            result += format_tree_structure(child, child_prefix, is_child_last)
    
    return result


if __name__ == "__main__":
    # 简单的测试代码
    print("🌳 Hibiki UI Tree Visualizer")
    print("============================")
    print()
    print("这是一个专业的组件树可视化工具。")
    print("要使用此工具，请在您的 Hibiki UI 应用中导入并调用相关函数。")
    print()
    print("示例用法:")
    print("```python")
    print("from hibiki.ui.debug import format_component_tree")
    print("tree_output = format_component_tree(my_component)")
    print("print(tree_output)")
    print("```")