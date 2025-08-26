"""
macUI Layout Styles - CSS-like声明式样式系统

提供熟悉的CSS概念和Web标准兼容的布局样式定义
基于Stretchable/Taffy的专业实现，确保性能和标准兼容性
"""

from typing import Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

import stretchable as st
from stretchable.style import (
    Display as StretchableDisplay,
    FlexDirection as StretchableFlexDirection,
    AlignItems as StretchableAlignItems,
    JustifyContent as StretchableJustifyContent,
    Position as StretchablePosition,
    Length,
    Size,
    Rect
)


class Display(Enum):
    """显示模式 - CSS display属性"""
    FLEX = "flex"
    BLOCK = "block"
    NONE = "none"
    
    def to_stretchable(self) -> StretchableDisplay:
        mapping = {
            Display.FLEX: StretchableDisplay.FLEX,
            Display.BLOCK: StretchableDisplay.BLOCK,
            Display.NONE: StretchableDisplay.NONE
        }
        return mapping[self]


class FlexDirection(Enum):
    """Flex方向 - CSS flex-direction属性"""
    ROW = "row"               # 水平排列 (HStack等价)
    COLUMN = "column"         # 垂直排列 (VStack等价)
    ROW_REVERSE = "row-reverse"
    COLUMN_REVERSE = "column-reverse"
    
    def to_stretchable(self) -> StretchableFlexDirection:
        mapping = {
            FlexDirection.ROW: StretchableFlexDirection.ROW,
            FlexDirection.COLUMN: StretchableFlexDirection.COLUMN,
            FlexDirection.ROW_REVERSE: StretchableFlexDirection.ROW_REVERSE,
            FlexDirection.COLUMN_REVERSE: StretchableFlexDirection.COLUMN_REVERSE
        }
        return mapping[self]


class AlignItems(Enum):
    """对齐项目 - CSS align-items属性"""
    FLEX_START = "flex-start"
    CENTER = "center"
    FLEX_END = "flex-end"
    STRETCH = "stretch"
    
    def to_stretchable(self) -> StretchableAlignItems:
        mapping = {
            AlignItems.FLEX_START: StretchableAlignItems.FLEX_START,
            AlignItems.CENTER: StretchableAlignItems.CENTER,
            AlignItems.FLEX_END: StretchableAlignItems.FLEX_END,
            AlignItems.STRETCH: StretchableAlignItems.STRETCH
        }
        return mapping[self]


class JustifyContent(Enum):
    """内容对齐 - CSS justify-content属性"""
    FLEX_START = "flex-start"
    CENTER = "center"
    FLEX_END = "flex-end"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"
    
    def to_stretchable(self) -> StretchableJustifyContent:
        mapping = {
            JustifyContent.FLEX_START: StretchableJustifyContent.FLEX_START,
            JustifyContent.CENTER: StretchableJustifyContent.CENTER,
            JustifyContent.FLEX_END: StretchableJustifyContent.FLEX_END,
            JustifyContent.SPACE_BETWEEN: StretchableJustifyContent.SPACE_BETWEEN,
            JustifyContent.SPACE_AROUND: StretchableJustifyContent.SPACE_AROUND,
            JustifyContent.SPACE_EVENLY: StretchableJustifyContent.SPACE_EVENLY
        }
        return mapping[self]


class Position(Enum):
    """定位模式 - CSS position属性"""
    RELATIVE = "relative"
    ABSOLUTE = "absolute"
    
    def to_stretchable(self) -> StretchablePosition:
        mapping = {
            Position.RELATIVE: StretchablePosition.RELATIVE,
            Position.ABSOLUTE: StretchablePosition.ABSOLUTE
        }
        return mapping[self]


# 便捷类型定义
LengthValue = Union[int, float, str]
SizeValue = Union[LengthValue, Tuple[LengthValue, LengthValue]]
EdgeValue = Union[LengthValue, Tuple[LengthValue, ...]]


def to_length(value: LengthValue) -> Length:
    """转换为Stretchable Length对象"""
    if isinstance(value, (int, float)):
        return Length.from_any(value)
    elif isinstance(value, str):
        if value.endswith('%'):
            # 处理百分比 - 例如 "50%"
            percent_val = float(value[:-1]) / 100.0
            return Length.from_any(f"{percent_val*100}%") 
        else:
            return Length.from_any(float(value))
    else:
        return Length.from_any(value)


def to_size(width: Optional[LengthValue] = None, height: Optional[LengthValue] = None) -> Optional[Size]:
    """创建Size对象"""
    if width is None and height is None:
        return None
    
    w = to_length(width) if width is not None else Length.from_any(0)  # Auto?
    h = to_length(height) if height is not None else Length.from_any(0)  # Auto?
    return Size(width=w, height=h)


def to_rect(
    top: Optional[LengthValue] = None,
    right: Optional[LengthValue] = None,
    bottom: Optional[LengthValue] = None, 
    left: Optional[LengthValue] = None,
    all: Optional[LengthValue] = None
) -> Optional[Rect]:
    """创建Rect对象 - 支持CSS简写形式"""
    if all is not None:
        # 所有边都相同
        l = to_length(all)
        return Rect(top=l, right=l, bottom=l, left=l)
    
    if all([x is None for x in [top, right, bottom, left]]):
        return None
    
    # 使用默认值0
    t = to_length(top or 0)
    r = to_length(right or 0) 
    b = to_length(bottom or 0)
    l = to_length(left or 0)
    
    return Rect(top=t, right=r, bottom=b, left=l)


@dataclass
class LayoutStyle:
    """布局样式 - CSS-like声明式样式定义
    
    提供熟悉的Web开发体验，自动转换为Stretchable样式
    """
    
    # Display & Position
    display: Optional[Display] = None
    position: Optional[Position] = None
    
    # Flexbox Layout  
    flex_direction: Optional[FlexDirection] = None
    align_items: Optional[AlignItems] = None
    justify_content: Optional[JustifyContent] = None
    flex_grow: Optional[float] = None
    flex_shrink: Optional[float] = None
    
    # Size
    width: Optional[LengthValue] = None
    height: Optional[LengthValue] = None
    min_width: Optional[LengthValue] = None
    min_height: Optional[LengthValue] = None
    max_width: Optional[LengthValue] = None
    max_height: Optional[LengthValue] = None
    
    # Spacing
    margin_top: Optional[LengthValue] = None
    margin_right: Optional[LengthValue] = None
    margin_bottom: Optional[LengthValue] = None
    margin_left: Optional[LengthValue] = None
    margin: Optional[LengthValue] = None  # 简写形式
    
    padding_top: Optional[LengthValue] = None
    padding_right: Optional[LengthValue] = None
    padding_bottom: Optional[LengthValue] = None
    padding_left: Optional[LengthValue] = None
    padding: Optional[LengthValue] = None  # 简写形式
    
    # Gap
    gap: Optional[LengthValue] = None
    row_gap: Optional[LengthValue] = None
    column_gap: Optional[LengthValue] = None
    
    # Positioning
    top: Optional[LengthValue] = None
    right: Optional[LengthValue] = None
    bottom: Optional[LengthValue] = None
    left: Optional[LengthValue] = None
    
    def to_stretchable_style(self) -> st.Style:
        """转换为Stretchable样式对象"""
        kwargs = {}
        
        # Display & Position
        if self.display is not None:
            kwargs['display'] = self.display.to_stretchable()
        if self.position is not None:
            kwargs['position'] = self.position.to_stretchable()
        
        # Flexbox
        if self.flex_direction is not None:
            kwargs['flex_direction'] = self.flex_direction.to_stretchable()
        if self.align_items is not None:
            kwargs['align_items'] = self.align_items.to_stretchable()
        if self.justify_content is not None:
            kwargs['justify_content'] = self.justify_content.to_stretchable()
        if self.flex_grow is not None:
            kwargs['flex_grow'] = self.flex_grow
        if self.flex_shrink is not None:
            kwargs['flex_shrink'] = self.flex_shrink
        
        # Size
        size = to_size(self.width, self.height)
        if size is not None:
            kwargs['size'] = size
            
        min_size = to_size(self.min_width, self.min_height)
        if min_size is not None:
            kwargs['min_size'] = min_size
            
        max_size = to_size(self.max_width, self.max_height)
        if max_size is not None:
            kwargs['max_size'] = max_size
        
        # Margin - 支持简写和详细形式
        margin = to_rect(
            top=self.margin_top,
            right=self.margin_right,
            bottom=self.margin_bottom,
            left=self.margin_left,
            all=self.margin
        )
        if margin is not None:
            kwargs['margin'] = margin
            
        # Padding - 支持简写和详细形式  
        padding = to_rect(
            top=self.padding_top,
            right=self.padding_right,
            bottom=self.padding_bottom,
            left=self.padding_left,
            all=self.padding
        )
        if padding is not None:
            kwargs['padding'] = padding
            
        # Gap
        if self.gap is not None:
            kwargs['gap'] = to_size(self.gap, self.gap)
        elif self.row_gap is not None or self.column_gap is not None:
            kwargs['gap'] = to_size(self.column_gap, self.row_gap)
            
        # Inset (positioning)
        inset = to_rect(
            top=self.top,
            right=self.right,
            bottom=self.bottom,
            left=self.left
        )
        if inset is not None:
            kwargs['inset'] = inset
        
        return st.Style(**kwargs)


# 便捷构造函数
def flex_style(
    direction: FlexDirection = FlexDirection.ROW,
    align: AlignItems = AlignItems.STRETCH,
    justify: JustifyContent = JustifyContent.FLEX_START,
    **kwargs
) -> LayoutStyle:
    """快速创建Flexbox样式"""
    return LayoutStyle(
        display=Display.FLEX,
        flex_direction=direction,
        align_items=align,
        justify_content=justify,
        **kwargs
    )


def vstack_style(
    align: AlignItems = AlignItems.STRETCH,
    justify: JustifyContent = JustifyContent.FLEX_START,
    gap: Optional[LengthValue] = None,
    **kwargs
) -> LayoutStyle:
    """VStack样式 (Column Flexbox)"""
    return flex_style(
        direction=FlexDirection.COLUMN,
        align=align,
        justify=justify,
        gap=gap,
        **kwargs
    )


def hstack_style(
    align: AlignItems = AlignItems.STRETCH,
    justify: JustifyContent = JustifyContent.FLEX_START, 
    gap: Optional[LengthValue] = None,
    **kwargs
) -> LayoutStyle:
    """HStack样式 (Row Flexbox)"""
    return flex_style(
        direction=FlexDirection.ROW,
        align=align,
        justify=justify,
        gap=gap,
        **kwargs
    )