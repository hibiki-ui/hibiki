#!/usr/bin/env python3
"""
macUI v4.0 布局引擎
直接集成Stretchable，提供现代化的CSS-like布局能力
完全独立的v4架构实现，不依赖旧版本代码
"""

from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import time

# 直接导入Stretchable - 这是外部依赖，不是旧版本代码
import stretchable as st
from stretchable.style import (
    Display as StDisplay,
    FlexDirection as StFlexDirection,
    AlignItems as StAlignItems,
    JustifyContent as StJustifyContent,
    Position as StPosition,
    Length,
    Size,
    Rect,
    PCT
)

# 导入v4样式系统 - 处理相对导入和绝对导入
try:
    # 作为包的一部分导入
    from .styles import (
        ComponentStyle, Display, FlexDirection, AlignItems, JustifyContent, 
        Length as V4Length, LengthUnit, px
    )
    from .managers import Position as V4Position
except ImportError:
    # 作为脚本运行时的导入
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from styles import (
        ComponentStyle, Display, FlexDirection, AlignItems, JustifyContent, 
        Length as V4Length, LengthUnit, px
    )
    from managers import Position as V4Position

# 导入日志系统
try:
    from .logging import get_logger
    logger = get_logger("layout")
except ImportError:
    import logging
    logger = logging.getLogger("macui_v4.layout")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)


@dataclass
class LayoutResult:
    """布局计算结果"""
    x: float
    y: float
    width: float
    height: float
    content_width: float
    content_height: float
    compute_time: float  # 计算耗时(毫秒)


class V4StyleConverter:
    """v4样式到Stretchable样式的转换器"""
    
    @staticmethod
    def convert_to_stretchable_style(v4_style: ComponentStyle) -> st.Style:
        """将v4 ComponentStyle转换为Stretchable Style"""
        kwargs = {}
        
        # Display转换
        if v4_style.display == Display.FLEX:
            kwargs['display'] = StDisplay.FLEX
        elif v4_style.display == Display.BLOCK:
            kwargs['display'] = StDisplay.BLOCK
        elif v4_style.display == Display.NONE:
            kwargs['display'] = StDisplay.NONE
        
        # Position转换
        if v4_style.position == V4Position.RELATIVE:
            kwargs['position'] = StPosition.RELATIVE
        elif v4_style.position == V4Position.ABSOLUTE:
            kwargs['position'] = StPosition.ABSOLUTE
        
        # FlexDirection转换
        if v4_style.flex_direction == FlexDirection.ROW:
            kwargs['flex_direction'] = StFlexDirection.ROW
        elif v4_style.flex_direction == FlexDirection.COLUMN:
            kwargs['flex_direction'] = StFlexDirection.COLUMN
        elif v4_style.flex_direction == FlexDirection.ROW_REVERSE:
            kwargs['flex_direction'] = StFlexDirection.ROW_REVERSE
        elif v4_style.flex_direction == FlexDirection.COLUMN_REVERSE:
            kwargs['flex_direction'] = StFlexDirection.COLUMN_REVERSE
        
        # AlignItems转换
        if v4_style.align_items == AlignItems.FLEX_START:
            kwargs['align_items'] = StAlignItems.FLEX_START
        elif v4_style.align_items == AlignItems.CENTER:
            kwargs['align_items'] = StAlignItems.CENTER
        elif v4_style.align_items == AlignItems.FLEX_END:
            kwargs['align_items'] = StAlignItems.FLEX_END
        elif v4_style.align_items == AlignItems.STRETCH:
            kwargs['align_items'] = StAlignItems.STRETCH
        
        # JustifyContent转换
        if v4_style.justify_content == JustifyContent.FLEX_START:
            kwargs['justify_content'] = StJustifyContent.FLEX_START
        elif v4_style.justify_content == JustifyContent.CENTER:
            kwargs['justify_content'] = StJustifyContent.CENTER
        elif v4_style.justify_content == JustifyContent.FLEX_END:
            kwargs['justify_content'] = StJustifyContent.FLEX_END
        elif v4_style.justify_content == JustifyContent.SPACE_BETWEEN:
            kwargs['justify_content'] = StJustifyContent.SPACE_BETWEEN
        elif v4_style.justify_content == JustifyContent.SPACE_AROUND:
            kwargs['justify_content'] = StJustifyContent.SPACE_AROUND
        elif v4_style.justify_content == JustifyContent.SPACE_EVENLY:
            kwargs['justify_content'] = StJustifyContent.SPACE_EVENLY
        
        # Flex属性
        if v4_style.flex_grow is not None:
            kwargs['flex_grow'] = v4_style.flex_grow
        if v4_style.flex_shrink is not None:
            kwargs['flex_shrink'] = v4_style.flex_shrink
        
        # 尺寸转换
        size = V4StyleConverter._convert_size(v4_style.width, v4_style.height)
        if size:
            kwargs['size'] = size
            
        min_size = V4StyleConverter._convert_size(v4_style.min_width, v4_style.min_height)
        if min_size:
            kwargs['min_size'] = min_size
            
        max_size = V4StyleConverter._convert_size(v4_style.max_width, v4_style.max_height)
        if max_size:
            kwargs['max_size'] = max_size
        
        # Margin转换
        margin = V4StyleConverter._convert_rect(
            v4_style.margin_top or v4_style.margin,
            v4_style.margin_right or v4_style.margin,
            v4_style.margin_bottom or v4_style.margin,
            v4_style.margin_left or v4_style.margin
        )
        if margin:
            kwargs['margin'] = margin
        
        # Padding转换
        padding = V4StyleConverter._convert_rect(
            v4_style.padding_top or v4_style.padding,
            v4_style.padding_right or v4_style.padding,
            v4_style.padding_bottom or v4_style.padding,
            v4_style.padding_left or v4_style.padding
        )
        if padding:
            kwargs['padding'] = padding
        
        # Gap转换
        gap = V4StyleConverter._convert_gap(v4_style.gap, v4_style.row_gap, v4_style.column_gap)
        if gap:
            kwargs['gap'] = gap
        
        # Inset (positioning)转换
        inset = V4StyleConverter._convert_rect(
            v4_style.top, v4_style.right, v4_style.bottom, v4_style.left
        )
        if inset:
            kwargs['inset'] = inset
        
        return st.Style(**kwargs)
    
    @staticmethod
    def _convert_length(v4_length) -> Optional[Length]:
        """转换v4长度值为Stretchable Length"""
        if v4_length is None:
            return None
        
        # v4 Length对象
        if isinstance(v4_length, V4Length):
            if v4_length.unit == LengthUnit.PX:
                return Length.from_any(float(v4_length.value))
            elif v4_length.unit == LengthUnit.PERCENT:
                return v4_length.value * PCT
            elif v4_length.unit == LengthUnit.AUTO:
                return Length.default()  # Stretchable的auto表示
        
        # 直接数值
        if isinstance(v4_length, (int, float)):
            return Length.from_any(float(v4_length))
        
        # 字符串
        if isinstance(v4_length, str):
            if v4_length == "auto":
                return Length.default()
            return Length.from_any(v4_length)
        
        return None
    
    @staticmethod
    def _convert_size(width, height) -> Optional[Size]:
        """转换尺寸"""
        w = V4StyleConverter._convert_length(width)
        h = V4StyleConverter._convert_length(height)
        
        if w is not None or h is not None:
            return Size(
                width=w or Length.default(),
                height=h or Length.default()
            )
        return None
    
    @staticmethod
    def _convert_rect(top, right, bottom, left) -> Optional[Rect]:
        """转换矩形值"""
        t = V4StyleConverter._convert_length(top)
        r = V4StyleConverter._convert_length(right)
        b = V4StyleConverter._convert_length(bottom)
        l = V4StyleConverter._convert_length(left)
        
        if any(x is not None for x in [t, r, b, l]):
            return Rect(
                top=t or Length.from_any(0),
                right=r or Length.from_any(0),
                bottom=b or Length.from_any(0),
                left=l or Length.from_any(0)
            )
        return None
    
    @staticmethod
    def _convert_gap(gap, row_gap, column_gap) -> Optional[Size]:
        """转换gap值"""
        if gap is not None:
            gap_length = V4StyleConverter._convert_length(gap)
            if gap_length:
                return Size(width=gap_length, height=gap_length)
        elif row_gap is not None or column_gap is not None:
            col_gap = V4StyleConverter._convert_length(column_gap) or Length.from_any(0)
            row_gap_val = V4StyleConverter._convert_length(row_gap) or Length.from_any(0)
            return Size(width=col_gap, height=row_gap_val)
        return None


class LayoutNode:
    """v4布局节点 - 封装Stretchable Node"""
    
    def __init__(self, component, style: Optional[ComponentStyle] = None, key: Optional[str] = None):
        """初始化布局节点
        
        Args:
            component: v4组件引用
            style: 组件样式
            key: 节点标识符
        """
        self.component = component
        self.key = key or f"node_{id(component)}"
        self.children: List['LayoutNode'] = []
        self.parent: Optional['LayoutNode'] = None
        
        # 转换样式并创建Stretchable节点
        if style:
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(style)
        else:
            stretchable_style = st.Style()
        
        self._stretchable_node = st.Node(style=stretchable_style)
        
        logger.info(f"📐 创建布局节点: {self.key} -> {component.__class__.__name__}")
    
    def add_child(self, child_node: 'LayoutNode', index: Optional[int] = None):
        """添加子节点"""
        if child_node.parent:
            child_node.parent.remove_child(child_node)
        
        child_node.parent = self
        
        if index is None:
            self.children.append(child_node)
            self._stretchable_node.append(child_node._stretchable_node)
        else:
            self.children.insert(index, child_node)
            self._stretchable_node.insert(index, child_node._stretchable_node)
        
        logger.info(f"➕ 布局节点添加子节点: {self.key} -> {child_node.key}")
    
    def remove_child(self, child_node: 'LayoutNode'):
        """移除子节点"""
        if child_node in self.children:
            self.children.remove(child_node)
            self._stretchable_node.remove(child_node._stretchable_node)
            child_node.parent = None
            logger.info(f"➖ 从布局节点移除子节点: {self.key} <- {child_node.key}")
    
    def update_style(self, style: ComponentStyle):
        """更新节点样式"""
        stretchable_style = V4StyleConverter.convert_to_stretchable_style(style)
        self._stretchable_node.style = stretchable_style
        self.mark_dirty()
    
    def compute_layout(self, available_size: Optional[Tuple[float, float]] = None) -> bool:
        """计算布局"""
        try:
            # Stretchable可以直接接受tuple作为available_space参数
            result = self._stretchable_node.compute_layout(available_size)
            if not result:
                logger.warning(f"⚠️ Stretchable布局计算返回False: {self.key}")
            return result
        except Exception as e:
            logger.error(f"❌ 布局计算异常: {self.key} - {e}")
            import traceback
            logger.error(f"❌ 详细错误: {traceback.format_exc()}")
            return False
    
    def get_layout(self) -> Tuple[float, float, float, float]:
        """获取计算后的布局结果"""
        box = self._stretchable_node.get_box()
        return (box.x, box.y, box.width, box.height)
    
    def get_content_size(self) -> Tuple[float, float]:
        """获取内容区域尺寸"""
        border_box = self._stretchable_node.border_box
        return (border_box.width, border_box.height)
    
    def mark_dirty(self):
        """标记需要重新布局"""
        self._stretchable_node.mark_dirty()
    
    def is_dirty(self) -> bool:
        """检查是否需要重新布局"""
        return self._stretchable_node.is_dirty


class V4LayoutEngine:
    """v4布局引擎 - 完全独立的实现"""
    
    def __init__(self, enable_cache: bool = True, debug_mode: bool = False):
        self.enable_cache = enable_cache
        self.debug_mode = debug_mode
        
        # 组件到布局节点的映射
        self._component_nodes: Dict[Any, LayoutNode] = {}
        
        # 性能统计
        self._layout_calls = 0
        self._cache_hits = 0
        self._cache_misses = 0
        
        logger.info("🏗️ V4LayoutEngine初始化完成")
    
    def create_node_for_component(self, component) -> LayoutNode:
        """为组件创建布局节点"""
        if component in self._component_nodes:
            existing_node = self._component_nodes[component]
            logger.info(f"📐 使用已存在的布局节点: {component.__class__.__name__}")
            return existing_node
        
        style = getattr(component, 'style', None)
        node = LayoutNode(component, style)
        self._component_nodes[component] = node
        
        logger.info(f"📐 为组件创建布局节点: {component.__class__.__name__}")
        return node
    
    def get_node_for_component(self, component) -> Optional[LayoutNode]:
        """获取组件的布局节点"""
        return self._component_nodes.get(component)
    
    def add_child_relationship(self, parent_component, child_component, index: Optional[int] = None):
        """建立父子布局关系"""
        parent_node = self.get_node_for_component(parent_component)
        if not parent_node:
            parent_node = self.create_node_for_component(parent_component)
        
        child_node = self.get_node_for_component(child_component)
        if not child_node:
            child_node = self.create_node_for_component(child_component)
        
        parent_node.add_child(child_node, index)
    
    def compute_layout_for_component(self, component, available_size: Optional[Tuple[float, float]] = None) -> Optional[LayoutResult]:
        """计算组件布局"""
        start_time = time.perf_counter()
        self._layout_calls += 1
        
        node = self.get_node_for_component(component)
        if not node:
            logger.warning(f"⚠️ 组件 {component.__class__.__name__} 没有布局节点")
            return None
        
        # 完全重建Stretchable节点树以避免状态不一致
        rebuilt_node = self._rebuild_stretchable_tree(component)
        if not rebuilt_node:
            logger.warning(f"⚠️ 重建布局树失败: {component.__class__.__name__}")
            return None
        
        # 执行布局计算
        try:
            success = rebuilt_node.compute_layout(available_size)
            if not success:
                logger.warning(f"⚠️ 组件布局计算失败: {component.__class__.__name__}")
                return None
        except Exception as e:
            logger.error(f"❌ 重建节点布局计算异常: {component.__class__.__name__} - {e}")
            import traceback
            logger.error(f"❌ 重建节点详细错误: {traceback.format_exc()}")
            return None
        
        # 获取结果
        box = rebuilt_node.get_box()
        x, y, width, height = box.x, box.y, box.width, box.height
        # Stretchable Node没有get_content_size方法，直接使用box尺寸
        content_width, content_height = width, height
        
        compute_time = (time.perf_counter() - start_time) * 1000
        
        result = LayoutResult(
            x=x, y=y, 
            width=width, height=height,
            content_width=content_width, content_height=content_height,
            compute_time=compute_time
        )
        
        if self.debug_mode:
            logger.info(f"✅ 布局计算完成: {component.__class__.__name__} -> {width:.1f}x{height:.1f} @ ({x:.1f}, {y:.1f}) [{compute_time:.2f}ms]")
        
        # 将重建的节点更新到缓存中
        node._stretchable_node = rebuilt_node
        
        return result
    
    def _rebuild_stretchable_tree(self, root_component):
        """完全重建Stretchable节点树，模拟简单测试的方式"""
        try:
            import stretchable as st
            
            # 获取根组件样式并转换
            root_style = getattr(root_component, 'style', None)
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(root_style)
            
            # 创建新的根节点
            root_node = st.Node(style=stretchable_style)
            
            # 递归创建子节点
            if hasattr(root_component, 'children'):
                logger.info(f"   发现子组件: {len(root_component.children)} 个")
                for i, child_component in enumerate(root_component.children):
                    # 只创建单个节点，不递归处理子组件（避免重复处理）
                    child_node = self._create_single_stretchable_node(child_component)
                    logger.debug(f"🔍 子节点创建结果: {child_component.__class__.__name__} -> {type(child_node)} {child_node is not None}")
                    logger.debug(f"🔍 即将检查child_node: id={id(child_node)}, type={type(child_node)}")
                    
                    # 立即检查以避免变量污染
                    child_node_is_valid = child_node is not None
                    logger.debug(f"🔍 child_node_is_valid = {child_node_is_valid}")
                    
                    if child_node_is_valid:
                        try:
                            root_node.append(child_node)
                            logger.info(f"   ✅ 添加子节点 {i+1}: {child_component.__class__.__name__}")
                            
                            # 递归处理孙子节点
                            if hasattr(child_component, 'children'):
                                logger.debug(f"🔍 处理孙子节点: {child_component.__class__.__name__} 有 {len(child_component.children)} 个子组件")
                                for grandchild in child_component.children:
                                    grandchild_node = self._create_stretchable_node_for_component(grandchild)
                                    if grandchild_node:
                                        child_node.append(grandchild_node)
                                        logger.debug(f"     ✅ 添加孙子节点: {grandchild.__class__.__name__}")
                        except Exception as e:
                            logger.error(f"   ❌ 添加子节点异常: {child_component.__class__.__name__} - {e}")
                            import traceback
                            logger.error(f"   ❌ 异常详情: {traceback.format_exc()}")
                    else:
                        logger.warning(f"   ⚠️ 子节点创建失败 {i+1}: {child_component.__class__.__name__} (返回值为None)")
            
            logger.info(f"🔄 重建布局树完成: {root_component.__class__.__name__}")
            logger.info(f"   根节点样式: display={stretchable_style.display}, size={stretchable_style.size}")
            logger.info(f"   子节点数量: {len(root_node)}")
            return root_node
            
        except Exception as e:
            logger.error(f"❌ 重建布局树失败: {e}")
            import traceback
            logger.error(f"❌ 详细错误: {traceback.format_exc()}")
            return None
    
    def _create_single_stretchable_node(self, component):
        """为组件创建单个Stretchable节点（不递归处理子组件）"""
        try:
            import stretchable as st
            
            # 获取组件样式并转换
            component_style = getattr(component, 'style', None)
            if not component_style:
                logger.warning(f"⚠️ 组件没有样式: {component.__class__.__name__}")
                # 为没有样式的组件创建默认样式
                from ..core.styles import ComponentStyle
                component_style = ComponentStyle()
                component.style = component_style
                logger.info(f"✨ 为组件创建默认样式: {component.__class__.__name__}")
                
            logger.debug(f"🎨 转换单个节点样式: {component.__class__.__name__} -> {component_style}")
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(component_style)
            
            # 创建节点（不处理子组件）
            node = st.Node(style=stretchable_style)
            logger.debug(f"📐 创建单个Stretchable节点成功: {component.__class__.__name__}")
            
            return node
            
        except Exception as e:
            logger.error(f"❌ 创建单个Stretchable节点异常: {component.__class__.__name__} - {e}")
            import traceback
            logger.error(f"❌ 详细异常: {traceback.format_exc()}")
            return None
    
    def _create_stretchable_node_for_component(self, component):
        """为组件创建纯Stretchable节点（不涉及v4布局缓存）"""
        try:
            import stretchable as st
            
            # 获取组件样式并转换
            component_style = getattr(component, 'style', None)
            if not component_style:
                logger.warning(f"⚠️ 组件没有样式: {component.__class__.__name__}")
                # 为没有样式的组件创建默认样式
                from ..core.styles import ComponentStyle
                component_style = ComponentStyle()
                component.style = component_style
                logger.info(f"✨ 为组件创建默认样式: {component.__class__.__name__}")
                
            logger.debug(f"🎨 转换样式: {component.__class__.__name__} -> {component_style}")
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(component_style)
            
            # 创建节点
            node = st.Node(style=stretchable_style)
            logger.debug(f"📐 创建Stretchable节点成功: {component.__class__.__name__}")
            
            # 递归处理子组件
            if hasattr(component, 'children'):
                for child_component in component.children:
                    child_node = self._create_stretchable_node_for_component(child_component)
                    if child_node:
                        node.append(child_node)
            
            return node
            
        except Exception as e:
            logger.error(f"❌ 创建Stretchable节点异常: {component.__class__.__name__} - {e}")
            import traceback
            logger.error(f"❌ 详细异常: {traceback.format_exc()}")
            return None
    
    def update_component_style(self, component):
        """更新组件样式"""
        node = self.get_node_for_component(component)
        if node and hasattr(component, 'style'):
            node.update_style(component.style)
            logger.info(f"🎨 更新组件样式: {component.__class__.__name__}")
    
    def cleanup_component(self, component):
        """清理组件的布局节点"""
        if component in self._component_nodes:
            node = self._component_nodes[component]
            
            # 从父节点移除
            if node.parent:
                node.parent.remove_child(node)
            
            # 清理映射
            del self._component_nodes[component]
            logger.info(f"🧹 清理组件布局节点: {component.__class__.__name__}")
    
    def debug_print_stats(self):
        """打印调试统计"""
        logger.info(f"📊 布局引擎统计:")
        logger.info(f"   🔄 布局调用次数: {self._layout_calls}")
        logger.info(f"   📐 活跃布局节点: {len(self._component_nodes)}")


# 全局布局引擎实例
_global_layout_engine: Optional[V4LayoutEngine] = None


def get_layout_engine() -> V4LayoutEngine:
    """获取全局v4布局引擎实例"""
    global _global_layout_engine
    if _global_layout_engine is None:
        _global_layout_engine = V4LayoutEngine(enable_cache=True, debug_mode=True)
    return _global_layout_engine


def set_debug_mode(enabled: bool):
    """设置调试模式"""
    get_layout_engine().debug_mode = enabled


# ================================
# 测试代码
# ================================

if __name__ == "__main__":
    print("macUI v4.0 布局引擎测试\n")
    
    # 测试样式转换
    print("🔄 样式转换测试:")
    # 导入已经在模块顶部处理了
    
    v4_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        align_items=AlignItems.CENTER,
        width=px(300),
        height=px(200),
        margin=px(10),
        gap=px(8)
    )
    
    stretchable_style = V4StyleConverter.convert_to_stretchable_style(v4_style)
    print(f"✅ 转换完成: {stretchable_style}")
    
    # 测试布局引擎
    print("\n📐 布局引擎测试:")
    engine = get_layout_engine()
    
    # 创建测试组件
    class MockComponent:
        def __init__(self, name: str, style: ComponentStyle):
            self.__class__.__name__ = f"Mock{name}"
            self.style = style
    
    parent = MockComponent("Parent", ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        width=px(400),
        height=px(300)
    ))
    
    child1 = MockComponent("Child1", ComponentStyle(
        width=px(200),
        height=px(100)
    ))
    
    child2 = MockComponent("Child2", ComponentStyle(
        width=px(180),
        height=px(80)
    ))
    
    # 创建布局节点并建立关系
    engine.create_node_for_component(parent)
    engine.create_node_for_component(child1)
    engine.create_node_for_component(child2)
    
    engine.add_child_relationship(parent, child1)
    engine.add_child_relationship(parent, child2)
    
    # 计算布局
    result = engine.compute_layout_for_component(parent, available_size=(500, 400))
    if result:
        print(f"✅ 父组件布局: {result.width:.1f}x{result.height:.1f} @ ({result.x:.1f}, {result.y:.1f})")
    
    # 打印统计
    engine.debug_print_stats()
    
    print("\n✅ v4布局引擎测试完成！")