#!/usr/bin/env python3
"""
Hibiki UI v4.0 布局引擎
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
    PCT,
)

from .styles import (
    ComponentStyle,
    Display,
    FlexDirection,
    AlignItems,
    JustifyContent,
    Length as V4Length,
    LengthUnit,
    px,
)
from .managers import Position as V4Position

from .logging import get_logger

logger = get_logger("layout")
logger.setLevel("INFO")


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
            kwargs["display"] = StDisplay.FLEX
        elif v4_style.display == Display.BLOCK:
            kwargs["display"] = StDisplay.BLOCK
        elif v4_style.display == Display.GRID:
            kwargs["display"] = StDisplay.GRID
            logger.debug("🎯 使用原生Grid布局")
        elif v4_style.display == Display.NONE:
            kwargs["display"] = StDisplay.NONE

        # Position转换
        if v4_style.position == V4Position.RELATIVE:
            kwargs["position"] = StPosition.RELATIVE
        elif v4_style.position == V4Position.ABSOLUTE:
            kwargs["position"] = StPosition.ABSOLUTE

        # FlexDirection转换
        if v4_style.flex_direction == FlexDirection.ROW:
            kwargs["flex_direction"] = StFlexDirection.ROW
        elif v4_style.flex_direction == FlexDirection.COLUMN:
            kwargs["flex_direction"] = StFlexDirection.COLUMN
        elif v4_style.flex_direction == FlexDirection.ROW_REVERSE:
            kwargs["flex_direction"] = StFlexDirection.ROW_REVERSE
        elif v4_style.flex_direction == FlexDirection.COLUMN_REVERSE:
            kwargs["flex_direction"] = StFlexDirection.COLUMN_REVERSE

        # AlignItems转换
        if v4_style.align_items == AlignItems.FLEX_START:
            kwargs["align_items"] = StAlignItems.FLEX_START
        elif v4_style.align_items == AlignItems.CENTER:
            kwargs["align_items"] = StAlignItems.CENTER
        elif v4_style.align_items == AlignItems.FLEX_END:
            kwargs["align_items"] = StAlignItems.FLEX_END
        elif v4_style.align_items == AlignItems.STRETCH:
            kwargs["align_items"] = StAlignItems.STRETCH

        # JustifyContent转换
        if v4_style.justify_content == JustifyContent.FLEX_START:
            kwargs["justify_content"] = StJustifyContent.FLEX_START
        elif v4_style.justify_content == JustifyContent.CENTER:
            kwargs["justify_content"] = StJustifyContent.CENTER
        elif v4_style.justify_content == JustifyContent.FLEX_END:
            kwargs["justify_content"] = StJustifyContent.FLEX_END
        elif v4_style.justify_content == JustifyContent.SPACE_BETWEEN:
            kwargs["justify_content"] = StJustifyContent.SPACE_BETWEEN
        elif v4_style.justify_content == JustifyContent.SPACE_AROUND:
            kwargs["justify_content"] = StJustifyContent.SPACE_AROUND
        elif v4_style.justify_content == JustifyContent.SPACE_EVENLY:
            kwargs["justify_content"] = StJustifyContent.SPACE_EVENLY

        # Flex属性
        if v4_style.flex_grow is not None:
            kwargs["flex_grow"] = v4_style.flex_grow
        if v4_style.flex_shrink is not None:
            kwargs["flex_shrink"] = v4_style.flex_shrink

        # 尺寸转换
        size = V4StyleConverter._convert_size(v4_style.width, v4_style.height)
        if size:
            kwargs["size"] = size

        min_size = V4StyleConverter._convert_size(v4_style.min_width, v4_style.min_height)
        if min_size:
            kwargs["min_size"] = min_size

        max_size = V4StyleConverter._convert_size(v4_style.max_width, v4_style.max_height)
        if max_size:
            kwargs["max_size"] = max_size

        # Margin转换
        margin = V4StyleConverter._convert_rect(
            v4_style.margin_top or v4_style.margin,
            v4_style.margin_right or v4_style.margin,
            v4_style.margin_bottom or v4_style.margin,
            v4_style.margin_left or v4_style.margin,
        )
        if margin:
            kwargs["margin"] = margin

        # Padding转换
        padding = V4StyleConverter._convert_rect(
            v4_style.padding_top or v4_style.padding,
            v4_style.padding_right or v4_style.padding,
            v4_style.padding_bottom or v4_style.padding,
            v4_style.padding_left or v4_style.padding,
        )
        if padding:
            kwargs["padding"] = padding

        # Gap转换
        gap = V4StyleConverter._convert_gap(v4_style.gap, v4_style.row_gap, v4_style.column_gap)
        if gap:
            kwargs["gap"] = gap

        # Inset (positioning)转换
        inset = V4StyleConverter._convert_rect(
            v4_style.top, v4_style.right, v4_style.bottom, v4_style.left
        )
        if inset:
            kwargs["inset"] = inset

        # Grid属性转换（完全支持Stretchable Grid）
        if hasattr(v4_style, "grid_template_columns") and v4_style.grid_template_columns:
            grid_columns = V4StyleConverter._convert_grid_template(v4_style.grid_template_columns)
            if grid_columns:
                kwargs["grid_template_columns"] = grid_columns
                logger.debug(f"🎯 Grid模板列: {v4_style.grid_template_columns} -> {len(grid_columns)}列")

        if hasattr(v4_style, "grid_template_rows") and v4_style.grid_template_rows:
            grid_rows = V4StyleConverter._convert_grid_template(v4_style.grid_template_rows)
            if grid_rows:
                kwargs["grid_template_rows"] = grid_rows
                logger.debug(f"🎯 Grid模板行: {v4_style.grid_template_rows} -> {len(grid_rows)}行")

        if hasattr(v4_style, "grid_column") and v4_style.grid_column:
            grid_column_placement = V4StyleConverter._convert_grid_placement(v4_style.grid_column)
            if grid_column_placement:
                kwargs["grid_column"] = grid_column_placement
                logger.debug(f"🎯 Grid列定位: {v4_style.grid_column}")

        if hasattr(v4_style, "grid_row") and v4_style.grid_row:
            grid_row_placement = V4StyleConverter._convert_grid_placement(v4_style.grid_row)
            if grid_row_placement:
                kwargs["grid_row"] = grid_row_placement
                logger.debug(f"🎯 Grid行定位: {v4_style.grid_row}")

        if hasattr(v4_style, "grid_area") and v4_style.grid_area:
            # grid_area可以设置grid_row和grid_column
            row_placement, column_placement = V4StyleConverter._convert_grid_area(v4_style.grid_area)
            if row_placement:
                kwargs["grid_row"] = row_placement
            if column_placement:
                kwargs["grid_column"] = column_placement
            logger.debug(f"🎯 Grid区域: {v4_style.grid_area}")

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
            return Size(width=w or Length.default(), height=h or Length.default())
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
                left=l or Length.from_any(0),
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

    @staticmethod
    def _convert_grid_template(template_value: str):
        """
        转换CSS Grid模板值到Stretchable GridTrackSizing列表
        
        支持的CSS Grid语法:
        - "1fr 2fr 1fr" -> 分数单位
        - "100px auto 200px" -> 固定尺寸和自动
        - "repeat(3, 1fr)" -> 重复模式
        - "minmax(100px, 1fr)" -> 最小最大值
        """
        if not template_value or not isinstance(template_value, str):
            return None
            
        try:
            from stretchable.style import GridTrackSizing
            
            # 处理简单的空格分隔的值
            if " " in template_value and not template_value.startswith("repeat("):
                tracks = []
                for track_str in template_value.split():
                    track_str = track_str.strip()
                    if track_str:
                        track = GridTrackSizing.from_any(track_str)
                        tracks.append(track)
                return tracks
            else:
                # 单个值或复杂表达式
                track = GridTrackSizing.from_any(template_value)
                return [track]
                
        except Exception as e:
            logger.warning(f"⚠️ Grid模板转换失败: {template_value} - {e}")
            return None
    
    @staticmethod
    def _convert_grid_placement(placement_value: str):
        """
        转换CSS Grid定位值到Stretchable GridPlacement
        
        支持的CSS Grid定位语法:
        - "1" -> 第1行/列
        - "1 / 3" -> 从第1行/列到第3行/列
        - "span 2" -> 跨越2行/列
        - "auto" -> 自动定位（返回None）
        """
        if not placement_value or not isinstance(placement_value, str):
            return None
            
        # 特殊处理auto情况
        if placement_value.strip().lower() == "auto":
            # auto情况下返图None，让Stretchable自动处理
            logger.debug("🔍 Grid自动定位，使用默认行为")
            return None
            
        try:
            from stretchable.style import GridPlacement
            
            placement = GridPlacement.from_any(placement_value)
            return placement
                
        except Exception as e:
            logger.warning(f"⚠️ Grid定位转换失败: {placement_value} - {e}")
            return None
    
    @staticmethod
    def _convert_grid_area(area_value: str):
        """
        转换CSS Grid区域值到行和列的GridPlacement
        
        CSS grid-area语法: "row-start / column-start / row-end / column-end"
        例如: "1 / 2 / 3 / 4" -> 行 1-3, 列 2-4
        """
        if not area_value or not isinstance(area_value, str):
            return None, None
            
        try:
            # 解析 "row-start / column-start / row-end / column-end"
            parts = [p.strip() for p in area_value.split("/")]
            
            if len(parts) == 4:
                row_start, col_start, row_end, col_end = parts
                
                # 转换行定住
                row_placement = V4StyleConverter._convert_grid_placement(f"{row_start} / {row_end}")
                col_placement = V4StyleConverter._convert_grid_placement(f"{col_start} / {col_end}")
                
                return row_placement, col_placement
            
            elif len(parts) == 1:
                # 单个值，如果是命名区域
                logger.debug(f"🔍 Grid命名区域: {area_value}（暂不支持）")
                return None, None
            else:
                logger.warning(f"⚠️ 不支持的Grid区域格式: {area_value}")
                return None, None
                
        except Exception as e:
            logger.warning(f"⚠️ Grid区域转换失败: {area_value} - {e}")
            return None, None


class LayoutNode:
    """v4布局节点 - 封装Stretchable Node"""

    def __init__(
        self, component, style: Optional[ComponentStyle] = None, key: Optional[str] = None
    ):
        """初始化布局节点

        Args:
            component: v4组件引用
            style: 组件样式
            key: 节点标识符
        """
        self.component = component
        self.key = key or f"node_{id(component)}"
        self.children: List["LayoutNode"] = []
        self.parent: Optional["LayoutNode"] = None

        # 转换样式并创建Stretchable节点
        if style:
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(style)
        else:
            stretchable_style = st.Style()

        self._stretchable_node = st.Node(style=stretchable_style)

        logger.debug(f"📐 创建布局节点: {self.key} -> {component.__class__.__name__}")

    def add_child(self, child_node: "LayoutNode", index: Optional[int] = None):
        """添加子节点 - v3风格直接操作"""
        # 确保子节点从原父节点完全移除
        if child_node.parent:
            child_node.parent.remove_child(child_node)

        # 确保Stretchable节点的parent属性也清空
        if hasattr(child_node._stretchable_node, "parent") and child_node._stretchable_node.parent:
            logger.debug(f"🔍 清理Stretchable节点的parent引用: {child_node.key}")
            child_node._stretchable_node.parent = None

        child_node.parent = self

        try:
            # 简化版本：v4总是使用append，忽略index参数
            # 这样可以确保与v3的兼容性
            self.children.append(child_node)
            # v3风格：直接在Stretchable节点上操作
            self._stretchable_node.append(child_node._stretchable_node)
            logger.debug(f"🔍 Stretchable append 执行完成")

            # 验证添加结果（使用Python list接口）
            actual_children = len(self._stretchable_node)
            expected_children = len(self.children)

            if actual_children != expected_children:
                logger.error(f"❌ 子节点添加不一致: 期望{expected_children}, 实际{actual_children}")
                logger.debug(f"🔍 Stretchable Python list: {list(self._stretchable_node)}")
                return False

            logger.debug(
                f"➕ 布局节点添加子节点成功: {self.key} -> {child_node.key} (子节点数: {actual_children})"
            )
            return True

        except Exception as e:
            logger.error(f"❌ 添加子节点异常: {self.key} -> {child_node.key} - {e}")
            import traceback

            logger.error(f"❌ 详细异常: {traceback.format_exc()}")
            return False

    def remove_child(self, child_node: "LayoutNode"):
        """
        安全移除子节点 - 防止Taffy库崩溃

        这个方法实现了安全的节点移除策略，解决了动态内容切换时
        Rust Taffy库出现的 'Option::unwrap() on a None value' 崩溃问题。

        关键安全措施：
        1. 先从Python层移除节点引用
        2. 检查Stretchable节点是否仍存在于父节点中
        3. 先清空父引用，再执行移除操作
        4. 全程异常保护，确保不影响应用运行
        """
        if child_node not in self.children:
            logger.debug(f"⚠️ 子节点不在父节点列表中: {child_node.key}")
            return

        # 第一步：从Python层移除节点引用
        self.children.remove(child_node)

        # 第二步：安全移除底层Stretchable节点
        self._safe_remove_stretchable_child(child_node)

        # 第三步：清理节点间的引用关系
        child_node.parent = None

        logger.debug(f"✅ 安全移除子节点完成: {self.key} <- {child_node.key}")

    def _safe_remove_stretchable_child(self, child_node: "LayoutNode"):
        """
        安全移除Stretchable子节点的内部方法

        这是解决Taffy崩溃问题的核心方法，通过多重检查和
        异常保护确保底层Rust节点的安全移除。
        """
        try:
            stretchable_child = child_node._stretchable_node
            if not stretchable_child:
                logger.debug("⚠️ 子节点的Stretchable节点为空，跳过移除")
                return

            # 关键检查：确保节点确实存在于父节点中
            if stretchable_child in self._stretchable_node:
                # 步骤1：先断开父引用，防止循环引用导致的问题
                if hasattr(stretchable_child, "parent"):
                    stretchable_child.parent = None

                # 步骤2：从父节点的子列表中移除
                self._stretchable_node.remove(stretchable_child)
                logger.debug("🔗 Stretchable子节点安全移除成功")
            else:
                logger.debug("⚠️ Stretchable子节点已不在父节点中，跳过移除")

        except Exception as e:
            # 即使移除失败也不应该影响应用运行
            logger.warning(f"⚠️ Stretchable节点移除异常（应用继续运行）: {e}")
            # 在调试模式下可以显示更详细的错误信息
            if logger.isEnabledFor(10):  # DEBUG level
                import traceback

                logger.debug(f"详细异常信息: {traceback.format_exc()}")

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

        logger.debug("🏗️ V4LayoutEngine初始化完成")

    def create_node_for_component(self, component) -> LayoutNode:
        """为组件创建布局节点"""
        if component in self._component_nodes:
            existing_node = self._component_nodes[component]
            logger.debug(f"📐 使用已存在的布局节点: {component.__class__.__name__}")
            return existing_node

        style = getattr(component, "style", None)
        node = LayoutNode(component, style)
        self._component_nodes[component] = node

        logger.debug(f"📐 为组件创建布局节点: {component.__class__.__name__}")
        return node

    def get_node_for_component(self, component) -> Optional[LayoutNode]:
        """获取组件的布局节点"""
        return self._component_nodes.get(component)

    def add_child_relationship(
        self, parent_component, child_component, index: Optional[int] = None
    ):
        """建立父子布局关系"""
        parent_node = self.get_node_for_component(parent_component)
        if not parent_node:
            parent_node = self.create_node_for_component(parent_component)

        child_node = self.get_node_for_component(child_component)
        if not child_node:
            child_node = self.create_node_for_component(child_component)

        parent_node.add_child(child_node, index)

    def remove_child_relationship(self, parent_component, child_component):
        """
        安全移除父子布局关系

        这个方法是动态内容切换的核心，负责安全地断开
        父子组件间的布局关系，防止Taffy库崩溃。

        处理流程：
        1. 从父节点移除子节点
        2. 深度清理子节点及其后代
        3. 清理组件映射关系
        4. 提供多层次的错误恢复机制
        """
        if not parent_component or not child_component:
            logger.debug("⚠️ 父组件或子组件为空，跳过关系移除")
            return

        parent_node = self.get_node_for_component(parent_component)
        child_node = self.get_node_for_component(child_component)

        # 第一步：从父节点移除子节点
        if parent_node and child_node:
            self._remove_from_parent_node(parent_node, child_node, child_component)
        else:
            logger.debug(
                f"⚠️ 找不到布局节点: parent={parent_node is not None}, child={child_node is not None}"
            )

        # 第二步：清理子组件的布局映射和资源
        if child_node and child_component in self._component_nodes:
            self._cleanup_child_component_mapping(child_node, child_component)
        else:
            logger.debug(f"⚠️ 子组件不在映射中或节点无效: {child_component.__class__.__name__}")

    def _remove_from_parent_node(self, parent_node, child_node, child_component):
        """从父节点安全移除子节点"""
        try:
            # 使用我们改进的安全移除方法
            parent_node.remove_child(child_node)
            logger.debug(f"✅ 布局关系移除成功: {child_component.__class__.__name__}")

        except Exception as e:
            logger.warning(f"⚠️ 标准移除方法失败，尝试强制清理: {e}")

            # 强制清理作为备用方案
            try:
                self._force_remove_child_relationship(parent_node, child_node)
                logger.debug("🔧 强制清理布局关系成功")
            except Exception as force_e:
                logger.warning(f"⚠️ 强制清理也失败: {force_e}")
                # 即使强制清理失败，也不应该中断应用运行

    def _force_remove_child_relationship(self, parent_node, child_node):
        """强制清理父子关系 - 最后的保险措施"""
        # 从Python层强制移除引用
        if child_node in parent_node.children:
            parent_node.children.remove(child_node)

        # 断开子节点的父引用
        child_node.parent = None

        # 尝试从Stretchable层也移除（如果可能）
        try:
            stretchable_child = child_node._stretchable_node
            if stretchable_child and hasattr(stretchable_child, "parent"):
                stretchable_child.parent = None
        except:
            pass  # 如果Stretchable层已损坏，忽略错误

    def _cleanup_child_component_mapping(self, child_node, child_component):
        """清理子组件的映射和资源"""
        try:
            # 深度清理子节点及其后代
            self._deep_cleanup_node(child_node)

            # 从映射中移除
            del self._component_nodes[child_component]

            logger.debug(f"🧹 子组件清理完成: {child_component.__class__.__name__}")

        except Exception as cleanup_e:
            logger.warning(f"⚠️ 子组件清理异常: {cleanup_e}")

            # 至少确保映射被清理
            self._ensure_mapping_cleanup(child_component)

    def _ensure_mapping_cleanup(self, child_component):
        """确保组件映射被清理 - 最后保障"""
        try:
            if child_component in self._component_nodes:
                del self._component_nodes[child_component]
                logger.debug("🔧 组件映射强制清理成功")
        except Exception as e:
            logger.debug(f"⚠️ 映射清理也失败: {e}")
            # 即使映射清理失败，也不影响应用运行

    def _deep_cleanup_node(self, node):
        """
        深度清理布局节点 - 递归清理防止内存泄漏

        这个方法负责彻底清理布局节点及其所有子节点，
        确保在动态内容切换时不会产生悬空引用或内存泄漏。

        清理顺序：
        1. 清理所有子节点（自下而上）
        2. 清理父引用（断开向上链接）
        3. 重置布局状态（清理缓存）
        """
        if not node or not hasattr(node, "_stretchable_node"):
            logger.debug("⚠️ 节点无效或缺少Stretchable节点，跳过深度清理")
            return

        try:
            stretchable_node = node._stretchable_node
            if not stretchable_node:
                logger.debug("⚠️ Stretchable节点为空，跳过清理")
                return

            # 第一阶段：清理所有子节点
            self._cleanup_child_nodes(stretchable_node)

            # 第二阶段：清理父引用关系
            self._cleanup_parent_reference(stretchable_node)

            # 第三阶段：重置布局状态
            self._reset_node_layout_state(stretchable_node)

            logger.debug("✅ 深度清理节点完成")

        except Exception as e:
            # 深度清理失败不应该影响应用运行
            logger.debug(f"⚠️ 深度清理过程异常（应用继续运行）: {e}")
            if logger.isEnabledFor(10):  # DEBUG level
                import traceback

                logger.debug(f"深度清理异常详情: {traceback.format_exc()}")

    def _cleanup_child_nodes(self, stretchable_node):
        """清理所有子节点的内部方法"""
        try:
            # 创建子节点列表的副本，避免迭代时修改原列表
            children = list(stretchable_node) if stretchable_node else []

            if children:
                logger.debug(f"🧹 开始清理 {len(children)} 个子节点")

                for i, child in enumerate(children):
                    try:
                        self._cleanup_single_child(stretchable_node, child, i)
                    except Exception as e:
                        logger.debug(f"⚠️ 清理第 {i} 个子节点异常: {e}")
            else:
                logger.debug("ℹ️ 无子节点需要清理")

        except Exception as e:
            logger.debug(f"⚠️ 获取子节点列表异常: {e}")

    def _cleanup_single_child(self, parent_node, child_node, index):
        """清理单个子节点"""
        try:
            # 检查子节点是否仍在父节点中
            if child_node in parent_node:
                # 先断开父引用
                if hasattr(child_node, "parent"):
                    child_node.parent = None

                # 从父节点移除
                parent_node.remove(child_node)
                logger.debug(f"🗑️ 子节点 [{index}] 清理成功")
            else:
                logger.debug(f"⚠️ 子节点 [{index}] 已不在父节点中")

        except Exception as e:
            logger.debug(f"⚠️ 子节点 [{index}] 清理异常: {e}")

    def _cleanup_parent_reference(self, stretchable_node):
        """清理父引用关系"""
        try:
            if not hasattr(stretchable_node, "parent"):
                logger.debug("ℹ️ 节点无父引用，跳过父引用清理")
                return

            parent = stretchable_node.parent
            if parent:
                # 检查并从父节点中移除自己
                if stretchable_node in parent:
                    parent.remove(stretchable_node)
                    logger.debug("🔗 从父节点移除成功")

                # 断开父引用
                stretchable_node.parent = None
                logger.debug("🧹 父引用清理成功")
            else:
                logger.debug("ℹ️ 无父节点，跳过父引用清理")

        except Exception as e:
            logger.debug(f"⚠️ 父引用清理异常: {e}")

    def _reset_node_layout_state(self, stretchable_node):
        """重置节点的布局状态"""
        try:
            self._reset_layout_state(stretchable_node)
            logger.debug("🔄 布局状态重置完成")
        except Exception as e:
            logger.debug(f"⚠️ 布局状态重置异常: {e}")

    def compute_layout_for_component(
        self, component, available_size: Optional[Tuple[float, float]] = None
    ) -> Optional[LayoutResult]:
        """计算组件布局 - v3风格直接方式"""
        start_time = time.perf_counter()
        self._layout_calls += 1

        node = self.get_node_for_component(component)
        if not node:
            logger.warning(f"⚠️ 组件 {component.__class__.__name__} 没有布局节点")
            return None

        # v3风格：直接在原始Stretchable节点上计算布局
        stretchable_node = node._stretchable_node
        logger.debug(f"🔍 直接布局计算，子节点数: {len(stretchable_node)} (Python list接口)")

        # 执行布局计算
        try:
            # 关键修复：在布局计算前重置布局状态，避免递归可见性检查错误
            self._reset_layout_state(stretchable_node)

            success = stretchable_node.compute_layout(available_size)
            if not success:
                logger.warning(f"⚠️ 组件布局计算失败: {component.__class__.__name__}")
                return None
        except Exception as e:
            # 特殊处理Stretchable的LayoutNotComputedError
            if "LayoutNotComputedError" in str(type(e)) or "layout is not computed" in str(e):
                logger.warning(f"🔄 布局状态异常，尝试重建布局树: {component.__class__.__name__}")
                try:
                    # 强制重建布局树
                    self._rebuild_layout_tree(component, node)
                    success = stretchable_node.compute_layout(available_size)
                    if not success:
                        logger.error(f"❌ 重建后布局计算仍失败: {component.__class__.__name__}")
                        return None
                except Exception as rebuild_e:
                    logger.error(f"❌ 重建布局树失败: {component.__class__.__name__} - {rebuild_e}")
                    return None
            else:
                logger.error(f"❌ 布局计算异常: {component.__class__.__name__} - {e}")
                import traceback

                logger.error(f"❌ 详细错误: {traceback.format_exc()}")
                return None

        # 获取结果
        box = stretchable_node.get_box()
        x, y, width, height = box.x, box.y, box.width, box.height
        content_width, content_height = width, height

        compute_time = (time.perf_counter() - start_time) * 1000

        result = LayoutResult(
            x=x,
            y=y,
            width=width,
            height=height,
            content_width=content_width,
            content_height=content_height,
            compute_time=compute_time,
        )

        if self.debug_mode:
            logger.debug(
                f"✅ 布局计算完成: {component.__class__.__name__} -> {width:.1f}x{height:.1f} @ ({x:.1f}, {y:.1f}) [{compute_time:.2f}ms]"
            )

        return result

    def _reset_layout_state(self, stretchable_node):
        """重置布局状态，解决可见性检查循环问题"""
        try:
            # 重置任何可能的布局状态缓存
            if hasattr(stretchable_node, "_layout_computed"):
                stretchable_node._layout_computed = False
            if hasattr(stretchable_node, "_layout"):
                stretchable_node._layout = None
            if hasattr(stretchable_node, "_box"):
                stretchable_node._box = None

            # 递归重置子节点
            for child in stretchable_node:
                self._reset_layout_state(child)

        except Exception as e:
            logger.debug(f"⚠️ 重置布局状态时出现异常（可忽略）: {e}")

    def _rebuild_layout_tree(self, component, node):
        """重建布局树，解决父子关系混乱问题"""
        try:
            stretchable_node = node._stretchable_node

            # 清理当前节点的父引用
            if hasattr(stretchable_node, "parent"):
                stretchable_node.parent = None

            # 清理所有子节点的父引用
            children = list(stretchable_node)  # 复制子节点列表
            for child in children:
                if hasattr(child, "parent"):
                    child.parent = None
                # 从父节点移除
                try:
                    stretchable_node.remove(child)
                except:
                    pass

            # 重新建立干净的父子关系
            if hasattr(component, "children"):
                for child_component in component.children:
                    child_node = self.get_node_for_component(child_component)
                    if child_node:
                        child_stretchable = child_node._stretchable_node
                        # 确保子节点没有父引用
                        if hasattr(child_stretchable, "parent"):
                            child_stretchable.parent = None
                        # 重新添加
                        try:
                            stretchable_node.append(child_stretchable)
                        except Exception as append_e:
                            logger.debug(f"⚠️ 重建时添加子节点失败（可忽略）: {append_e}")

            # 重置布局状态
            self._reset_layout_state(stretchable_node)

            logger.debug(f"🔄 布局树重建完成: {component.__class__.__name__}")

        except Exception as e:
            logger.warning(f"⚠️ 布局树重建过程异常: {e}")

    def _create_single_stretchable_node(self, component):
        """为组件创建单个Stretchable节点（不递归处理子组件）"""
        try:
            import stretchable as st

            # 获取组件样式并转换
            component_style = getattr(component, "style", None)
            if not component_style:
                logger.warning(f"⚠️ 组件没有样式: {component.__class__.__name__}")
                # 为没有样式的组件创建默认样式
                from ..core.styles import ComponentStyle

                component_style = ComponentStyle()
                component.style = component_style
                logger.debug(f"✨ 为组件创建默认样式: {component.__class__.__name__}")

            logger.debug(
                f"🎨 转换单个节点样式: {component.__class__.__name__} -> {component_style}"
            )
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
            component_style = getattr(component, "style", None)
            if not component_style:
                logger.warning(f"⚠️ 组件没有样式: {component.__class__.__name__}")
                # 为没有样式的组件创建默认样式
                from ..core.styles import ComponentStyle

                component_style = ComponentStyle()
                component.style = component_style
                logger.debug(f"✨ 为组件创建默认样式: {component.__class__.__name__}")

            logger.debug(f"🎨 转换样式: {component.__class__.__name__} -> {component_style}")
            stretchable_style = V4StyleConverter.convert_to_stretchable_style(component_style)

            # 创建节点
            node = st.Node(style=stretchable_style)
            logger.debug(f"📐 创建Stretchable节点成功: {component.__class__.__name__}")

            # 递归处理子组件
            if hasattr(component, "children"):
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
        if node and hasattr(component, "style"):
            node.update_style(component.style)
            logger.debug(f"🎨 更新组件样式: {component.__class__.__name__}")

    def cleanup_component(self, component):
        """清理组件的布局节点"""
        if component in self._component_nodes:
            node = self._component_nodes[component]

            try:
                # 从父节点移除 - 需要安全处理
                if hasattr(node, "parent") and node.parent:
                    node.parent.remove_child(node)
            except Exception as e:
                logger.warning(f"⚠️ 布局节点清理警告: {e}")

            # 清理映射
            del self._component_nodes[component]
            logger.debug(f"🧹 清理组件布局节点: {component.__class__.__name__}")

    def debug_print_stats(self):
        """打印详细的调试统计信息"""
        logger.info("📊 Hibiki UI v4 布局引擎状态报告")
        logger.info("=" * 50)
        logger.info(f"🔄 布局计算调用次数: {self._layout_calls}")
        logger.info(f"📐 活跃布局节点数量: {len(self._component_nodes)}")
        logger.info(f"🧠 缓存启用状态: {self.enable_cache}")
        logger.info(f"🐛 调试模式状态: {self.debug_mode}")

        # 分析组件类型分布
        component_types = {}
        for component in self._component_nodes.keys():
            comp_type = component.__class__.__name__
            component_types[comp_type] = component_types.get(comp_type, 0) + 1

        if component_types:
            logger.info("📋 组件类型分布:")
            for comp_type, count in sorted(component_types.items()):
                logger.info(f"   {comp_type}: {count}")

        logger.info("=" * 50)

    def health_check(self) -> dict:
        """
        执行布局引擎健康检查

        Returns:
            dict: 包含健康状态信息的字典
        """
        health_status = {
            "healthy": True,
            "total_nodes": len(self._component_nodes),
            "orphaned_nodes": 0,
            "corrupted_references": 0,
            "warnings": [],
        }

        try:
            # 检查孤立节点
            for component, node in self._component_nodes.items():
                try:
                    if not node or not node._stretchable_node:
                        health_status["corrupted_references"] += 1
                        health_status["warnings"].append(
                            f"组件 {component.__class__.__name__} 的布局节点损坏"
                        )
                        continue

                    # 检查父子关系一致性
                    if hasattr(component, "parent") and component.parent:
                        parent_node = self.get_node_for_component(component.parent)
                        if parent_node and node not in parent_node.children:
                            health_status["orphaned_nodes"] += 1
                            health_status["warnings"].append(
                                f"组件 {component.__class__.__name__} 存在孤立的布局节点"
                            )

                except Exception as e:
                    health_status["corrupted_references"] += 1
                    health_status["warnings"].append(
                        f"检查组件 {component.__class__.__name__} 时出错: {e}"
                    )

            # 判断整体健康状态
            if health_status["corrupted_references"] > 0 or health_status["orphaned_nodes"] > 0:
                health_status["healthy"] = False

        except Exception as e:
            health_status["healthy"] = False
            health_status["warnings"].append(f"健康检查过程出错: {e}")

        return health_status

    def cleanup_orphaned_nodes(self) -> int:
        """
        清理孤立的布局节点

        Returns:
            int: 清理的节点数量
        """
        cleaned_count = 0
        components_to_remove = []

        try:
            for component, node in self._component_nodes.items():
                try:
                    # 检查节点是否损坏
                    if not node or not node._stretchable_node:
                        components_to_remove.append(component)
                        continue

                    # 检查组件是否还有效
                    if not hasattr(component, "__class__"):
                        components_to_remove.append(component)
                        continue

                except Exception:
                    components_to_remove.append(component)

            # 清理损坏的映射
            for component in components_to_remove:
                try:
                    del self._component_nodes[component]
                    cleaned_count += 1
                    logger.debug(f"🧹 清理孤立节点: {component}")
                except Exception as e:
                    logger.warning(f"⚠️ 清理孤立节点失败: {e}")

            if cleaned_count > 0:
                logger.info(f"🧹 清理了 {cleaned_count} 个孤立的布局节点")

        except Exception as e:
            logger.warning(f"⚠️ 孤立节点清理过程异常: {e}")

        return cleaned_count

    def get_node_tree_info(self, component) -> dict:
        """
        获取组件的布局树信息（用于调试）

        Returns:
            dict: 包含树结构信息的字典
        """
        node = self.get_node_for_component(component)
        if not node:
            return {"error": "未找到布局节点"}

        try:
            info = {
                "component_type": component.__class__.__name__,
                "node_key": getattr(node, "key", "unknown"),
                "children_count": len(node.children),
                "has_parent": node.parent is not None,
                "stretchable_valid": node._stretchable_node is not None,
                "children": [],
            }

            # 递归获取子节点信息
            for child_node in node.children:
                child_component = None
                # 找到对应的组件
                for comp, n in self._component_nodes.items():
                    if n == child_node:
                        child_component = comp
                        break

                if child_component:
                    child_info = self.get_node_tree_info(child_component)
                    info["children"].append(child_info)
                else:
                    info["children"].append({"error": "找不到对应的组件"})

            return info

        except Exception as e:
            return {"error": f"获取节点信息时出错: {e}"}


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
    logger.info("Hibiki UI v4.0 布局引擎测试\n")

    # 测试样式转换
    logger.info("🔄 样式转换测试:")
    # 导入已经在模块顶部处理了

    v4_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        align_items=AlignItems.CENTER,
        width=px(300),
        height=px(200),
        margin=px(10),
        gap=px(8),
    )

    stretchable_style = V4StyleConverter.convert_to_stretchable_style(v4_style)
    logger.info(f"✅ 转换完成: {stretchable_style}")

    # 测试布局引擎
    logger.info("\n📐 布局引擎测试:")
    engine = get_layout_engine()

    # 创建测试组件
    class MockComponent:
        def __init__(self, name: str, style: ComponentStyle):
            self.__class__.__name__ = f"Mock{name}"
            self.style = style

    parent = MockComponent(
        "Parent",
        ComponentStyle(
            display=Display.FLEX, flex_direction=FlexDirection.COLUMN, width=px(400), height=px(300)
        ),
    )

    child1 = MockComponent("Child1", ComponentStyle(width=px(200), height=px(100)))

    child2 = MockComponent("Child2", ComponentStyle(width=px(180), height=px(80)))

    # 创建布局节点并建立关系
    engine.create_node_for_component(parent)
    engine.create_node_for_component(child1)
    engine.create_node_for_component(child2)

    engine.add_child_relationship(parent, child1)
    engine.add_child_relationship(parent, child2)

    # 计算布局
    result = engine.compute_layout_for_component(parent, available_size=(500, 400))
    if result:
        logger.info(
            f"✅ 父组件布局: {result.width:.1f}x{result.height:.1f} @ ({result.x:.1f}, {result.y:.1f})"
        )

    # 打印统计
    engine.debug_print_stats()

    logger.info("\n✅ v4布局引擎测试完成！")
