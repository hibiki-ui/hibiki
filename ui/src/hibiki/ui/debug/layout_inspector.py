#!/usr/bin/env python3
"""
Layout Inspector - 布局检查器
============================

深度分析组件布局信息，提供详细的样式和布局属性检查。
类似浏览器开发者工具的元素检查功能。
"""

import inspect
import time
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from ..core.logging import get_logger
from ..core.layout import get_layout_engine
from ..core.styles import ComponentStyle

logger = get_logger("debug.layout_inspector")


@dataclass
class LayoutInfo:
    """布局信息数据结构"""
    component_type: str
    component_id: str
    position: Optional[Tuple[float, float]]  # (x, y)
    size: Optional[Tuple[float, float]]      # (width, height)
    computed_style: Dict[str, Any]
    layout_properties: Dict[str, Any]
    children_count: int
    parent_info: Optional[str]
    stretchable_valid: bool
    warnings: List[str]


class InspectionLevel(Enum):
    """检查深度级别"""
    BASIC = "basic"           # 基础信息
    DETAILED = "detailed"     # 详细信息
    COMPLETE = "complete"     # 完整信息（包括内部状态）


class LayoutInspector:
    """布局检查器
    
    功能特性：
    - 详细的组件样式分析
    - 布局计算结果检查
    - 样式属性冲突检测
    - 布局问题诊断和建议
    - 组件层次结构分析
    """
    
    def __init__(self, inspection_level: InspectionLevel = InspectionLevel.DETAILED):
        """初始化布局检查器
        
        Args:
            inspection_level: 检查深度级别
        """
        self.inspection_level = inspection_level
        
        # 样式属性映射（用于检查）
        self._style_attributes = [
            'width', 'height', 'padding', 'margin', 'border',
            'background_color', 'color', 'font_size', 'border_radius',
            'display', 'flex_direction', 'justify_content', 'align_items',
            'flex_grow', 'flex_shrink', 'flex_basis', 'position',
            'top', 'left', 'right', 'bottom', 'z_index', 'opacity'
        ]
    
    def inspect_component(self, component) -> LayoutInfo:
        """检查单个组件的布局信息
        
        Args:
            component: 要检查的组件
            
        Returns:
            详细的布局信息
        """
        logger.debug(f"🔍 检查组件: {type(component).__name__}")
        
        # 基础信息
        component_type = type(component).__name__
        component_id = str(id(component))
        
        # 获取布局引擎信息
        engine = get_layout_engine()
        tree_info = engine.get_node_tree_info(component)
        
        # 位置和尺寸信息
        position, size = self._extract_position_size(component, tree_info)
        
        # 计算样式信息
        computed_style = self._extract_computed_style(component)
        
        # 布局属性
        layout_properties = self._extract_layout_properties(component, tree_info)
        
        # 父子关系
        children_count = len(component.children) if hasattr(component, 'children') else 0
        parent_info = self._get_parent_info(component)
        
        # 健康状态
        stretchable_valid = tree_info.get('stretchable_valid', False) if tree_info else False
        
        # 问题诊断
        warnings = self._diagnose_layout_issues(component, computed_style, layout_properties)
        
        return LayoutInfo(
            component_type=component_type,
            component_id=component_id,
            position=position,
            size=size,
            computed_style=computed_style,
            layout_properties=layout_properties,
            children_count=children_count,
            parent_info=parent_info,
            stretchable_valid=stretchable_valid,
            warnings=warnings
        )
    
    def inspect_component_hierarchy(self, component) -> List[LayoutInfo]:
        """检查组件及其所有子组件
        
        Args:
            component: 根组件
            
        Returns:
            组件层次结构的布局信息列表
        """
        results = []
        
        # 检查当前组件
        layout_info = self.inspect_component(component)
        results.append(layout_info)
        
        # 递归检查子组件
        if hasattr(component, 'children') and component.children:
            for child in component.children:
                child_results = self.inspect_component_hierarchy(child)
                results.extend(child_results)
        
        return results
    
    def _extract_position_size(self, component, tree_info) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        """提取位置和尺寸信息"""
        position = None
        size = None
        
        try:
            if hasattr(component, '_nsview') and component._nsview:
                frame = component._nsview.frame()
                position = (frame.origin.x, frame.origin.y)
                size = (frame.size.width, frame.size.height)
        except Exception as e:
            logger.debug(f"提取位置尺寸失败: {e}")
        
        return position, size
    
    def _extract_computed_style(self, component) -> Dict[str, Any]:
        """提取计算后的样式信息"""
        computed_style = {}
        
        if hasattr(component, 'style') and component.style:
            style = component.style
            
            for attr_name in self._style_attributes:
                if hasattr(style, attr_name):
                    attr_value = getattr(style, attr_name)
                    if attr_value is not None:
                        computed_style[attr_name] = self._serialize_style_value(attr_value)
        
        return computed_style
    
    def _extract_layout_properties(self, component, tree_info) -> Dict[str, Any]:
        """提取布局属性"""
        properties = {}
        
        if tree_info:
            properties.update({
                "node_key": tree_info.get('node_key'),
                "children_count": tree_info.get('children_count', 0),
                "stretchable_valid": tree_info.get('stretchable_valid', False),
                "has_parent": tree_info.get('has_parent', False)
            })
        
        # 组件特定属性
        if hasattr(component, 'orientation'):
            properties['orientation'] = str(component.orientation)
        
        if hasattr(component, 'split_ratio'):
            if hasattr(component.split_ratio, 'value'):
                properties['split_ratio'] = component.split_ratio.value
            else:
                properties['split_ratio'] = component.split_ratio
        
        if hasattr(component, 'scroll_vertical'):
            properties['scroll_vertical'] = component.scroll_vertical
            properties['scroll_horizontal'] = getattr(component, 'scroll_horizontal', False)
        
        return properties
    
    def _get_parent_info(self, component) -> Optional[str]:
        """获取父组件信息"""
        if hasattr(component, '_parent_container') and component._parent_container:
            parent = component._parent_container
            return f"{type(parent).__name__} ({id(parent)})"
        return None
    
    def _serialize_style_value(self, value) -> Any:
        """序列化样式值为可JSON化的格式"""
        if hasattr(value, 'value'):
            return f"{value.value}{getattr(value, 'unit', '')}"
        elif hasattr(value, '__dict__'):
            return str(value)
        elif isinstance(value, (str, int, float, bool)):
            return value
        else:
            return str(value)
    
    def _diagnose_layout_issues(self, component, computed_style, layout_properties) -> List[str]:
        """诊断布局问题
        
        Args:
            component: 组件
            computed_style: 计算样式
            layout_properties: 布局属性
            
        Returns:
            问题列表
        """
        warnings = []
        
        # 检查Stretchable健康状态
        if not layout_properties.get('stretchable_valid', True):
            warnings.append("⚠️ 布局节点状态异常，可能导致布局计算错误")
        
        # 检查尺寸设置
        if 'width' not in computed_style and 'flex_grow' not in computed_style:
            warnings.append("💡 建议设置 width 或 flex_grow 以确保正确的布局计算")
        
        # 检查Flexbox配置
        if computed_style.get('display') == 'flex':
            if 'flex_direction' not in computed_style:
                warnings.append("💡 Flex容器建议明确设置 flex_direction")
        
        # 检查子组件数量
        children_count = layout_properties.get('children_count', 0)
        if hasattr(component, 'children'):
            actual_children = len(component.children)
            if actual_children != children_count:
                warnings.append(f"⚠️ 子组件数量不匹配: 实际{actual_children} vs 布局引擎{children_count}")
        
        # 检查ScrollableContainer特殊情况
        if component_type := type(component).__name__ == 'ScrollableContainer':
            if children_count == 0:
                warnings.append("❌ ScrollableContainer子组件挂载失败")
            elif not layout_properties.get('scroll_vertical', False) and not layout_properties.get('scroll_horizontal', False):
                warnings.append("💡 ScrollableContainer建议至少启用一个滚动方向")
        
        return warnings
    
    def generate_inspection_report(self, component, 
                                 include_hierarchy: bool = True) -> Dict[str, Any]:
        """生成详细的检查报告
        
        Args:
            component: 要检查的组件
            include_hierarchy: 是否包含整个层次结构
            
        Returns:
            检查报告字典
        """
        start_time = time.time()
        
        if include_hierarchy:
            layout_infos = self.inspect_component_hierarchy(component)
        else:
            layout_infos = [self.inspect_component(component)]
        
        # 统计信息
        total_components = len(layout_infos)
        healthy_components = sum(1 for info in layout_infos if info.stretchable_valid)
        total_warnings = sum(len(info.warnings) for info in layout_infos)
        
        # 组件类型分布
        type_distribution = {}
        for info in layout_infos:
            component_type = info.component_type
            type_distribution[component_type] = type_distribution.get(component_type, 0) + 1
        
        report = {
            "timestamp": time.time(),
            "inspection_level": self.inspection_level.value,
            "summary": {
                "total_components": total_components,
                "healthy_components": healthy_components,
                "unhealthy_components": total_components - healthy_components,
                "total_warnings": total_warnings,
                "type_distribution": type_distribution,
                "inspection_time": time.time() - start_time
            },
            "components": [self._layout_info_to_dict(info) for info in layout_infos]
        }
        
        return report
    
    def _layout_info_to_dict(self, layout_info: LayoutInfo) -> Dict[str, Any]:
        """将LayoutInfo转换为字典"""
        return {
            "component_type": layout_info.component_type,
            "component_id": layout_info.component_id,
            "position": layout_info.position,
            "size": layout_info.size,
            "computed_style": layout_info.computed_style,
            "layout_properties": layout_info.layout_properties,
            "children_count": layout_info.children_count,
            "parent_info": layout_info.parent_info,
            "stretchable_valid": layout_info.stretchable_valid,
            "warnings": layout_info.warnings
        }
    
    def find_layout_issues(self, component) -> List[Dict[str, Any]]:
        """查找布局问题
        
        Args:
            component: 要检查的组件
            
        Returns:
            问题列表，每个问题包含位置、类型、描述等信息
        """
        layout_infos = self.inspect_component_hierarchy(component)
        issues = []
        
        for info in layout_infos:
            if info.warnings:
                for warning in info.warnings:
                    issues.append({
                        "component_type": info.component_type,
                        "component_id": info.component_id,
                        "issue_type": "warning",
                        "description": warning,
                        "position": info.position,
                        "suggestions": self._get_suggestions(warning)
                    })
            
            if not info.stretchable_valid:
                issues.append({
                    "component_type": info.component_type,
                    "component_id": info.component_id,
                    "issue_type": "error",
                    "description": "布局节点状态异常",
                    "position": info.position,
                    "suggestions": ["检查组件是否正确挂载", "验证样式属性设置", "查看布局引擎日志"]
                })
        
        return issues
    
    def _get_suggestions(self, warning: str) -> List[str]:
        """根据警告获取修复建议"""
        suggestions = []
        
        if "子组件数量不匹配" in warning:
            suggestions.extend([
                "检查子组件是否正确添加到容器",
                "验证容器的mount()方法实现",
                "查看布局引擎的add_child_relationship()调用"
            ])
        elif "ScrollableContainer" in warning:
            suggestions.extend([
                "确保ScrollableContainer正确实现mount()方法",
                "检查_content_view是否正确创建",
                "验证子组件是否添加到布局树"
            ])
        elif "width 或 flex_grow" in warning:
            suggestions.extend([
                "为组件设置明确的width属性",
                "或在Flex容器中设置flex_grow属性", 
                "考虑使用percent(100)或px()单位"
            ])
        elif "flex_direction" in warning:
            suggestions.extend([
                "明确设置flex_direction为ROW或COLUMN",
                "从hibiki.ui导入FlexDirection枚举",
                "避免使用字符串，使用枚举值"
            ])
        
        return suggestions
    
    def get_style_conflicts(self, component) -> List[Dict[str, Any]]:
        """检测样式属性冲突
        
        Args:
            component: 要检查的组件
            
        Returns:
            冲突列表
        """
        conflicts = []
        
        if not hasattr(component, 'style') or not component.style:
            return conflicts
        
        style = component.style
        
        # 检查常见冲突
        # 1. 绝对定位 + Flexbox
        if (hasattr(style, 'position') and style.position == 'absolute' and
            hasattr(style, 'display') and style.display == 'flex'):
            conflicts.append({
                "type": "positioning_conflict",
                "description": "绝对定位与Flexbox布局可能产生冲突",
                "affected_properties": ["position", "display"],
                "suggestion": "考虑使用相对定位或修改布局策略"
            })
        
        # 2. 百分比尺寸 + 父容器无明确尺寸
        if (hasattr(style, 'width') and str(style.width).startswith('percent') and
            hasattr(component, '_parent_container')):
            parent = component._parent_container
            if parent and hasattr(parent, 'style') and parent.style:
                if not hasattr(parent.style, 'width') or parent.style.width is None:
                    conflicts.append({
                        "type": "percentage_sizing_conflict",
                        "description": "百分比尺寸需要父容器有明确的尺寸",
                        "affected_properties": ["width"],
                        "suggestion": "为父容器设置明确的width属性"
                    })
        
        # 3. ScrollableContainer + 固定高度冲突
        if type(component).__name__ == 'ScrollableContainer':
            if hasattr(style, 'height') and style.height and str(style.height).endswith('px'):
                conflicts.append({
                    "type": "scroll_sizing_conflict", 
                    "description": "ScrollableContainer使用固定高度可能影响滚动效果",
                    "affected_properties": ["height"],
                    "suggestion": "考虑使用flex_grow或百分比高度"
                })
        
        return conflicts
    
    def get_optimization_suggestions(self, component) -> List[Dict[str, Any]]:
        """获取性能优化建议
        
        Args:
            component: 要分析的组件
            
        Returns:
            优化建议列表
        """
        suggestions = []
        
        # 分析组件层次深度
        depth = self._calculate_component_depth(component)
        if depth > 10:
            suggestions.append({
                "type": "hierarchy_optimization",
                "priority": "medium",
                "description": f"组件层次过深 (深度: {depth})，可能影响性能",
                "suggestion": "考虑扁平化组件结构或使用组合模式"
            })
        
        # 分析子组件数量
        if hasattr(component, 'children'):
            children_count = len(component.children)
            if children_count > 50:
                suggestions.append({
                    "type": "children_optimization", 
                    "priority": "high",
                    "description": f"子组件过多 ({children_count})，可能影响性能",
                    "suggestion": "考虑使用虚拟化滚动或分页机制"
                })
        
        # 分析样式复杂度
        if hasattr(component, 'style') and component.style:
            style_complexity = len([attr for attr in self._style_attributes 
                                  if hasattr(component.style, attr) and 
                                  getattr(component.style, attr) is not None])
            
            if style_complexity > 15:
                suggestions.append({
                    "type": "style_optimization",
                    "priority": "low", 
                    "description": f"样式属性过多 ({style_complexity})，考虑简化",
                    "suggestion": "使用StylePresets或提取公共样式"
                })
        
        return suggestions
    
    def _calculate_component_depth(self, component, current_depth: int = 0) -> int:
        """计算组件层次深度"""
        max_depth = current_depth
        
        if hasattr(component, 'children') and component.children:
            for child in component.children:
                child_depth = self._calculate_component_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth


# 便捷函数
def inspect_layout(component, level: str = "detailed") -> Dict[str, Any]:
    """检查组件布局（便捷函数）
    
    Args:
        component: 要检查的组件
        level: 检查级别 ("basic", "detailed", "complete")
        
    Returns:
        布局检查结果字典
    """
    level_enum = InspectionLevel(level)
    inspector = LayoutInspector(level_enum)
    
    layout_info = inspector.inspect_component(component)
    return inspector._layout_info_to_dict(layout_info)


def find_layout_problems(component) -> List[Dict[str, Any]]:
    """查找布局问题（便捷函数）
    
    Args:
        component: 要检查的组件
        
    Returns:
        问题列表
    """
    inspector = LayoutInspector()
    return inspector.find_layout_issues(component)


def get_optimization_tips(component) -> List[Dict[str, Any]]:
    """获取优化建议（便捷函数）
    
    Args:
        component: 要分析的组件
        
    Returns:
        优化建议列表
    """
    inspector = LayoutInspector()
    return inspector.get_optimization_suggestions(component)


if __name__ == "__main__":
    # 测试代码
    print("🔍 Hibiki UI Layout Inspector")
    print("=============================")
    print()
    print("这是一个专业的布局检查器。")
    print("提供详细的组件样式和布局分析功能。")
    print()
    print("示例用法:")
    print("```python")
    print("from hibiki.ui.debug import inspect_layout, find_layout_problems")
    print("layout_info = inspect_layout(my_component)")
    print("problems = find_layout_problems(my_component)")
    print("```")