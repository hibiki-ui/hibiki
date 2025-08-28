#!/usr/bin/env python3
"""
Hibiki UI v4.0 高级布局组件
提供专业级的布局解决方案：Grid、ResponsiveGrid、Stack、Masonry等
"""

from typing import List, Optional, Union, Tuple, Callable, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import math

# 导入核心组件系统
try:
    from ..core.component import Component, Container
    from ..core.styles import ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems, px, percent, Length
    from ..core.reactive import Signal, Computed
except ImportError:
    # 作为独立模块运行时的导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.component import Component, Container
    from core.styles import ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems, px, percent, Length
    from core.reactive import Signal, Computed

from hibiki.core.logging import get_logger
logger = get_logger('components.layout')



# ================================
# 1. Grid布局系统
# ================================

@dataclass
class GridTemplate:
    """Grid模板定义"""
    columns: Union[str, List[str]]  # "repeat(3, 1fr)" 或 ["200px", "1fr", "100px"]
    rows: Union[str, List[str]]     # "auto" 或 ["50px", "auto", "100px"]
    gap: Optional[Union[int, str]] = None
    
    def __post_init__(self):
        """标准化模板定义"""
        if isinstance(self.columns, str):
            self.columns = self._parse_template(self.columns)
        if isinstance(self.rows, str):
            self.rows = self._parse_template(self.rows)
    
    def _parse_template(self, template: str) -> List[str]:
        """解析Grid模板字符串"""
        # 处理repeat()语法
        if template.startswith("repeat("):
            # 简单的repeat解析：repeat(3, 1fr) -> ["1fr", "1fr", "1fr"]
            content = template[7:-1]  # 去掉repeat()
            parts = content.split(",", 1)
            if len(parts) == 2:
                count = int(parts[0].strip())
                value = parts[1].strip()
                return [value] * count
        
        # 分割空格分隔的值
        return [item.strip() for item in template.split() if item.strip()]


class GridContainer(Container):
    """CSS Grid容器组件
    
    提供强大的二维网格布局功能，支持：
    - 显式网格定义（grid-template-columns/rows）
    - 自动网格生成
    - 网格区域命名
    - 子项定位控制
    """
    
    def __init__(
        self, 
        children: Optional[List[Component]] = None,
        template: Optional[GridTemplate] = None,
        columns: Optional[Union[str, List[str]]] = None,
        rows: Optional[Union[str, List[str]]] = None,
        gap: Optional[Union[int, str]] = None,
        justify_items: Optional[str] = "stretch",
        align_items: Optional[str] = "stretch",
        justify_content: Optional[str] = "start",
        align_content: Optional[str] = "start",
        auto_rows: Optional[str] = "auto",
        auto_columns: Optional[str] = "auto",
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化Grid容器
        
        Args:
            template: Grid模板对象
            columns: 列定义，如 "repeat(3, 1fr)" 或 ["200px", "1fr", "100px"]  
            rows: 行定义
            gap: 网格间距
            justify_items: 子项水平对齐
            align_items: 子项垂直对齐
            justify_content: 整体网格水平对齐
            align_content: 整体网格垂直对齐
            auto_rows: 自动行高
            auto_columns: 自动列宽
        """
        # 构建Grid样式
        if not style:
            style = ComponentStyle()
        
        style.display = Display.GRID
        
        # 使用template或直接参数
        if template:
            columns = template.columns
            rows = template.rows
            gap = gap or template.gap
        
        # 设置Grid属性（存储为字符串，让Stretchable处理）
        if columns:
            if isinstance(columns, list):
                style.grid_template_columns = " ".join(columns)
            else:
                style.grid_template_columns = columns
                
        if rows:
            if isinstance(rows, list):
                style.grid_template_rows = " ".join(rows)
            else:
                style.grid_template_rows = rows
        
        if gap:
            if isinstance(gap, (int, float)):
                style.gap = px(gap)
            else:
                style.gap = Length(gap)
        
        # 保存Grid特有属性
        self.justify_items = justify_items
        self.align_items = align_items
        self.justify_content = justify_content
        self.align_content = align_content
        self.auto_rows = auto_rows
        self.auto_columns = auto_columns
        
        super().__init__(children=children, style=style, **kwargs)
    
    def set_grid_area(self, child: Component, area: str):
        """设置子组件的网格区域
        
        Args:
            child: 子组件
            area: 网格区域，如 "header" 或 "1 / 1 / 2 / 4"
        """
        if child in self.children:
            if not child.style:
                child.style = ComponentStyle()
            child.style.grid_area = area
            self._update_layout()
    
    def set_grid_position(self, child: Component, 
                         column_start: Optional[int] = None,
                         column_end: Optional[int] = None,
                         row_start: Optional[int] = None,
                         row_end: Optional[int] = None):
        """设置子组件的网格位置
        
        Args:
            child: 子组件
            column_start: 开始列
            column_end: 结束列
            row_start: 开始行
            row_end: 结束行
        """
        if child in self.children:
            if not child.style:
                child.style = ComponentStyle()
            
            grid_column_parts = []
            if column_start is not None:
                grid_column_parts.append(str(column_start))
            if column_end is not None:
                if not grid_column_parts:
                    grid_column_parts.append("auto")
                grid_column_parts.append(str(column_end))
            
            grid_row_parts = []
            if row_start is not None:
                grid_row_parts.append(str(row_start))
            if row_end is not None:
                if not grid_row_parts:
                    grid_row_parts.append("auto")
                grid_row_parts.append(str(row_end))
            
            if grid_column_parts:
                child.style.grid_column = " / ".join(grid_column_parts)
            if grid_row_parts:
                child.style.grid_row = " / ".join(grid_row_parts)
            
            self._update_layout()


class ResponsiveGrid(GridContainer):
    """响应式网格容器
    
    根据容器宽度自动调整列数，实现响应式布局
    """
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        min_column_width: Union[int, str] = 200,  # 最小列宽
        max_columns: Optional[int] = None,        # 最大列数
        gap: Optional[Union[int, str]] = 16,
        aspect_ratio: Optional[float] = None,     # 子项宽高比
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化响应式网格
        
        Args:
            min_column_width: 列的最小宽度
            max_columns: 最大列数限制
            aspect_ratio: 子项的宽高比（宽/高）
        """
        self.min_column_width = min_column_width
        self.max_columns = max_columns
        self.aspect_ratio = aspect_ratio
        
        # 创建响应式列定义
        if isinstance(min_column_width, int):
            column_template = f"repeat(auto-fit, minmax({min_column_width}px, 1fr))"
        else:
            column_template = f"repeat(auto-fit, minmax({min_column_width}, 1fr))"
        
        super().__init__(
            children=children,
            columns=column_template,
            gap=gap,
            style=style,
            **kwargs
        )
    
    def update_responsive_layout(self, container_width: float):
        """根据容器宽度更新响应式布局"""
        if isinstance(self.min_column_width, int):
            min_width = self.min_column_width
        else:
            # 简化：假设是px值
            min_width = int(self.min_column_width.replace("px", ""))
        
        # 计算可能的列数
        gap_value = 16 if isinstance(self.style.gap, type(None)) else (
            self.style.gap.value if hasattr(self.style.gap, 'value') else 16
        )
        
        available_width = container_width - gap_value
        possible_columns = max(1, int(available_width / (min_width + gap_value)))
        
        # 应用最大列数限制
        if self.max_columns:
            possible_columns = min(possible_columns, self.max_columns)
        
        # 更新Grid模板
        self.style.grid_template_columns = f"repeat({possible_columns}, 1fr)"
        self._update_layout()


# ================================
# 2. Stack布局系统
# ================================

class StackDirection(Enum):
    """Stack方向"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Stack(Container):
    """通用Stack布局容器
    
    提供简化的线性布局，支持：
    - 水平/垂直方向
    - 间距控制
    - 对齐方式
    - 分布方式
    """
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        direction: StackDirection = StackDirection.VERTICAL,
        spacing: Union[int, str] = 8,
        alignment: str = "stretch",  # start, center, end, stretch
        distribution: str = "start",  # start, center, end, space-between, space-around, space-evenly
        wrap: bool = False,
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化Stack容器
        
        Args:
            direction: Stack方向
            spacing: 子组件间距
            alignment: 交叉轴对齐方式
            distribution: 主轴分布方式
            wrap: 是否允许换行
        """
        if not style:
            style = ComponentStyle()
        
        # 配置Flexbox
        style.display = Display.FLEX
        
        if direction == StackDirection.HORIZONTAL:
            style.flex_direction = FlexDirection.ROW
        else:
            style.flex_direction = FlexDirection.COLUMN
        
        # 设置间距
        if isinstance(spacing, int):
            style.gap = px(spacing)
        else:
            style.gap = Length(spacing)
        
        # 设置对齐
        align_mapping = {
            "start": AlignItems.FLEX_START,
            "center": AlignItems.CENTER, 
            "end": AlignItems.FLEX_END,
            "stretch": AlignItems.STRETCH
        }
        style.align_items = align_mapping.get(alignment, AlignItems.STRETCH)
        
        # 设置分布
        justify_mapping = {
            "start": JustifyContent.FLEX_START,
            "center": JustifyContent.CENTER,
            "end": JustifyContent.FLEX_END,
            "space-between": JustifyContent.SPACE_BETWEEN,
            "space-around": JustifyContent.SPACE_AROUND,
            "space-evenly": JustifyContent.SPACE_EVENLY
        }
        style.justify_content = justify_mapping.get(distribution, JustifyContent.FLEX_START)
        
        self.direction = direction
        self.spacing = spacing
        self.alignment = alignment
        self.distribution = distribution
        self.wrap = wrap
        
        super().__init__(children=children, style=style, **kwargs)


class HStack(Stack):
    """水平Stack容器（语法糖）"""
    
    def __init__(self, children: Optional[List[Component]] = None, **kwargs):
        super().__init__(children=children, direction=StackDirection.HORIZONTAL, **kwargs)


class VStack(Stack):
    """垂直Stack容器（语法糖）"""
    
    def __init__(self, children: Optional[List[Component]] = None, **kwargs):
        super().__init__(children=children, direction=StackDirection.VERTICAL, **kwargs)


class ZStack(Container):
    """层叠Stack容器
    
    将子组件按Z轴层叠布局，类似于绝对定位的容器
    """
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        alignment: str = "center",  # 子项对齐方式
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化ZStack容器"""
        if not style:
            style = ComponentStyle()
        
        # ZStack使用相对定位作为容器
        style.position = ComponentStyle().position  # static/relative
        
        self.alignment = alignment
        super().__init__(children=children, style=style, **kwargs)
    
    def add_layer(self, child: Component, z_index: int = 0, 
                  offset_x: float = 0, offset_y: float = 0):
        """添加层级子组件
        
        Args:
            child: 子组件
            z_index: Z轴层级
            offset_x: X轴偏移
            offset_y: Y轴偏移
        """
        # 设置子组件为绝对定位
        if not child.style:
            child.style = ComponentStyle()
        
        from ..core.managers import Position
        child.style.position = Position.ABSOLUTE
        child.style.z_index = z_index
        
        if offset_x != 0:
            child.style.left = px(offset_x)
        if offset_y != 0:
            child.style.top = px(offset_y)
        
        self.add_child(child)


# ================================
# 3. Masonry瀑布流布局
# ================================

class MasonryContainer(Container):
    """瀑布流布局容器
    
    实现Pinterest风格的瀑布流布局：
    - 多列等宽布局
    - 子项按高度自动排列
    - 最小化空白区域
    """
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        columns: int = 3,
        gap: Union[int, str] = 16,
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化瀑布流容器
        
        Args:
            columns: 列数
            gap: 间距
        """
        if not style:
            style = ComponentStyle()
        
        # 瀑布流使用CSS Grid实现
        style.display = Display.GRID
        style.grid_template_columns = f"repeat({columns}, 1fr)"
        
        if isinstance(gap, int):
            style.gap = px(gap)
        else:
            style.gap = Length(gap)
        
        self.columns = columns
        self._column_heights = [0.0] * columns  # 跟踪每列高度
        
        super().__init__(children=children, style=style, **kwargs)
    
    def add_masonry_item(self, child: Component):
        """添加瀑布流项目（自动分配到最短列）"""
        # 找到高度最小的列
        min_height = min(self._column_heights)
        target_column = self._column_heights.index(min_height)
        
        # 设置子项的grid-column
        if not child.style:
            child.style = ComponentStyle()
        child.style.grid_column = str(target_column + 1)
        
        # 添加子项
        self.add_child(child)
        
        # 更新列高度（这里需要在实际布局后更新）
        # 在实际实现中，需要在布局计算后更新
        estimated_height = getattr(child.style, 'height', px(100)).value if hasattr(child.style, 'height') and child.style.height else 100
        self._column_heights[target_column] += estimated_height
    
    def rebalance_masonry(self):
        """重新平衡瀑布流布局"""
        # 重置列高度
        self._column_heights = [0.0] * self.columns
        
        # 重新分配所有子项
        for child in self.children.copy():
            self.remove_child(child)
            self.add_masonry_item(child)


# ================================
# 4. 专业布局容器
# ================================

class SplitView(Container):
    """分割视图容器
    
    实现可调整大小的分割面板：
    - 水平/垂直分割
    - 可拖拽分割线
    - 最小/最大尺寸限制
    - 折叠功能
    """
    
    def __init__(
        self,
        primary: Component,
        secondary: Component,
        orientation: StackDirection = StackDirection.HORIZONTAL,
        split_ratio: float = 0.5,  # 0.0-1.0
        min_primary_size: int = 100,
        min_secondary_size: int = 100,
        resizable: bool = True,
        collapsible: bool = False,
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化分割视图
        
        Args:
            primary: 主面板
            secondary: 次面板
            orientation: 分割方向
            split_ratio: 分割比例
            min_primary_size: 主面板最小尺寸
            min_secondary_size: 次面板最小尺寸
            resizable: 是否可调整大小
            collapsible: 是否可折叠
        """
        if not style:
            style = ComponentStyle()
        
        style.display = Display.FLEX
        
        if orientation == StackDirection.HORIZONTAL:
            style.flex_direction = FlexDirection.ROW
        else:
            style.flex_direction = FlexDirection.COLUMN
        
        # 设置flex比例
        if not primary.style:
            primary.style = ComponentStyle()
        if not secondary.style:
            secondary.style = ComponentStyle()
        
        primary.style.flex_grow = split_ratio
        secondary.style.flex_grow = 1 - split_ratio
        
        self.orientation = orientation
        self.split_ratio = Signal(split_ratio)
        self.min_primary_size = min_primary_size
        self.min_secondary_size = min_secondary_size
        self.resizable = resizable
        self.collapsible = collapsible
        
        # 创建分割线
        splitter = self._create_splitter()
        
        children = [primary, splitter, secondary] if resizable else [primary, secondary]
        super().__init__(children=children, style=style, **kwargs)
    
    def _create_splitter(self) -> Component:
        """创建分割线组件"""
        # 使用已导入的Container
        BasicContainer = Container
        
        splitter_style = ComponentStyle()
        if self.orientation == StackDirection.HORIZONTAL:
            splitter_style.width = px(4)
            splitter_style.height = percent(100)
        else:
            splitter_style.width = percent(100)
            splitter_style.height = px(4)
        
        # TODO: 添加鼠标事件处理
        splitter = BasicContainer(style=splitter_style)
        return splitter
    
    def set_split_ratio(self, ratio: float):
        """设置分割比例"""
        ratio = max(0.1, min(0.9, ratio))  # 限制范围
        self.split_ratio.value = ratio
        
        # 更新flex比例
        if len(self.children) >= 2:
            primary = self.children[0]
            secondary = self.children[-1]
            
            primary.style.flex_grow = ratio
            secondary.style.flex_grow = 1 - ratio
            
            self._update_layout()


class ScrollableContainer(Container):
    """可滚动容器
    
    提供内容滚动功能：
    - 水平/垂直滚动
    - 滚动条样式控制
    - 虚拟化支持（大数据集）
    """
    
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        scroll_horizontal: bool = False,
        scroll_vertical: bool = True,
        show_scrollbars: bool = True,
        style: Optional[ComponentStyle] = None,
        **kwargs
    ):
        """初始化滚动容器"""
        if not style:
            style = ComponentStyle()
        
        # 设置overflow属性
        from ..core.managers import OverflowBehavior
        if scroll_horizontal and scroll_vertical:
            style.overflow = OverflowBehavior.SCROLL
        elif scroll_vertical:
            style.overflow = OverflowBehavior.SCROLL_VERTICAL
        elif scroll_horizontal:
            style.overflow = OverflowBehavior.SCROLL_HORIZONTAL
        else:
            style.overflow = OverflowBehavior.HIDDEN
        
        self.scroll_horizontal = scroll_horizontal
        self.scroll_vertical = scroll_vertical  
        self.show_scrollbars = show_scrollbars
        
        super().__init__(children=children, style=style, **kwargs)


# ================================
# 5. 布局工具和助手
# ================================

class LayoutPresets:
    """布局预设工厂"""
    
    @staticmethod
    def card_grid(columns: int = 3, gap: int = 16) -> GridContainer:
        """卡片网格布局"""
        return GridContainer(
            columns=f"repeat({columns}, 1fr)",
            gap=gap,
            style=ComponentStyle(padding=px(16))
        )
    
    @staticmethod
    def sidebar_layout(sidebar_width: int = 250) -> SplitView:
        """侧边栏布局"""
        BasicContainer = Container
        
        sidebar = BasicContainer(style=ComponentStyle(
            width=px(sidebar_width),
            min_width=px(200)
        ))
        main = BasicContainer()
        
        return SplitView(
            primary=sidebar,
            secondary=main,
            orientation=StackDirection.HORIZONTAL,
            split_ratio=0.3,
            resizable=True
        )
    
    @staticmethod
    def header_content_layout(header_height: int = 60) -> VStack:
        """头部-内容布局"""
        BasicContainer = Container
        
        header = BasicContainer(style=ComponentStyle(
            height=px(header_height),
            width=percent(100)
        ))
        
        content = BasicContainer(style=ComponentStyle(
            flex_grow=1
        ))
        
        return VStack(
            children=[header, content],
            spacing=0,
            style=ComponentStyle(height=percent(100))
        )
    
    @staticmethod
    def masonry_gallery(columns: int = 3) -> MasonryContainer:
        """瀑布流画廊"""
        return MasonryContainer(
            columns=columns,
            gap=12,
            style=ComponentStyle(padding=px(12))
        )


class LayoutAnimator:
    """布局动画器（预留接口）"""
    
    @staticmethod
    def animate_grid_resize(grid: GridContainer, new_columns: Union[str, List[str]], duration: float = 0.3):
        """动画化Grid列变化"""
        # TODO: 实现布局动画
        pass
    
    @staticmethod 
    def animate_split_ratio(split_view: SplitView, new_ratio: float, duration: float = 0.3):
        """动画化分割比例变化"""
        # TODO: 实现比例动画
        pass


# ================================
# 6. 测试代码
# ================================

if __name__ == "__main__":
    logger.info("Hibiki UI v4.0 高级布局组件测试\n")
    
    # 测试Grid容器
    logger.info("📐 Grid容器测试:")
    grid = GridContainer(
        columns="repeat(3, 1fr)",
        rows="100px auto",
        gap=16
    )
    logger.info(f"Grid列定义: {grid.style.grid_template_columns}")
    logger.info(f"Grid行定义: {grid.style.grid_template_rows}")
    logger.info(f"Grid间距: {grid.style.gap}")
    
    # 测试响应式Grid
    logger.info("\n📱 响应式Grid测试:")
    responsive_grid = ResponsiveGrid(
        min_column_width=200,
        max_columns=4,
        gap=16
    )
    logger.info(f"响应式Grid列模板: {responsive_grid.style.grid_template_columns}")
    
    # 测试Stack容器
    logger.info("\n📚 Stack容器测试:")
    vstack = VStack(spacing=12, alignment="center")
    hstack = HStack(spacing=8, distribution="space-between")
    logger.info(f"VStack方向: {vstack.style.flex_direction}")
    logger.info(f"HStack分布: {vstack.style.justify_content}")
    
    # 测试瀑布流
    logger.info("\n🌊 瀑布流测试:")
    masonry = MasonryContainer(columns=3, gap=16)
    logger.info(f"瀑布流列数: {masonry.columns}")
    logger.info(f"瀑布流Grid模板: {masonry.style.grid_template_columns}")
    
    logger.info("\n✅ 高级布局组件测试完成！")