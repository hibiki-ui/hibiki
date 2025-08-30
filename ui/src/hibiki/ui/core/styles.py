#!/usr/bin/env python3
"""
Hibiki UI 样式系统
统一的样式定义，支持所有布局和视觉属性
"""

from dataclasses import dataclass, field
from typing import Optional, Union, Tuple, Any
from enum import Enum

# 导入管理器中定义的枚举
from .managers import Position, ZLayer, OverflowBehavior

from .logging import get_logger
logger = get_logger('core.styles')

# ================================
# 1. 单位和长度系统
# ================================

class LengthUnit(Enum):
    """长度单位枚举"""
    PX = "px"          # 像素
    PERCENT = "%"      # 百分比  
    VW = "vw"         # 视口宽度百分比
    VH = "vh"         # 视口高度百分比
    AUTO = "auto"     # 自动

@dataclass
class Length:
    """长度值 - 支持不同单位
    
    Examples:
        Length(100, LengthUnit.PX)     # 100px
        Length(50, LengthUnit.PERCENT) # 50%
        Length("auto")                 # auto
    """
    value: Union[int, float, str]
    unit: LengthUnit = LengthUnit.PX
    
    def __post_init__(self):
        """自动解析字符串格式的长度值"""
        if isinstance(self.value, str):
            if self.value == "auto":
                self.unit = LengthUnit.AUTO
            elif "%" in self.value:
                self.unit = LengthUnit.PERCENT
                self.value = float(self.value.replace("%", ""))
            elif "vw" in self.value:
                self.unit = LengthUnit.VW  
                self.value = float(self.value.replace("vw", ""))
            elif "vh" in self.value:
                self.unit = LengthUnit.VH
                self.value = float(self.value.replace("vh", ""))
            elif "px" in self.value:
                self.unit = LengthUnit.PX
                self.value = float(self.value.replace("px", ""))
    
    def __str__(self):
        if self.unit == LengthUnit.AUTO:
            return "auto"
        return f"{self.value}{self.unit.value}"

# 便捷构造函数
def px(value: Union[int, float]) -> Length:
    """创建像素长度"""
    return Length(value, LengthUnit.PX)

def percent(value: Union[int, float]) -> Length:
    """创建百分比长度"""
    return Length(value, LengthUnit.PERCENT)

def vw(value: Union[int, float]) -> Length:
    """创建视口宽度百分比长度"""
    return Length(value, LengthUnit.VW)

def vh(value: Union[int, float]) -> Length:
    """创建视口高度百分比长度"""
    return Length(value, LengthUnit.VH)

# 常用常量
auto = Length("auto", LengthUnit.AUTO)

# ================================
# 2. Flexbox相关枚举
# ================================

class FlexDirection(Enum):
    """Flex方向"""
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"

class JustifyContent(Enum):
    """主轴对齐"""
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"

class AlignItems(Enum):
    """交叉轴对齐"""
    STRETCH = "stretch"
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    BASELINE = "baseline"

class Display(Enum):
    """显示类型"""
    FLEX = "flex"
    GRID = "grid"
    BLOCK = "block"
    INLINE = "inline"
    NONE = "none"

# ================================
# 3. 核心样式数据结构
# ================================

@dataclass
class ComponentStyle:
    """组件样式定义 - 涵盖所有布局和视觉属性
    
    这是Hibiki UI的核心样式系统，支持：
    - 完整的定位系统 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - Flexbox和Grid布局
    - Box Model (margin, padding, size)
    - 变换效果 (scale, rotate, translate)
    - 视觉效果 (opacity, overflow, clip)
    """
    
    # ================================
    # 定位和层级
    # ================================
    position: Position = Position.STATIC
    z_index: Union[int, ZLayer] = ZLayer.CONTENT
    
    # 坐标（用于非static定位）
    top: Optional[Union[int, float, str, Length]] = None
    right: Optional[Union[int, float, str, Length]] = None
    bottom: Optional[Union[int, float, str, Length]] = None
    left: Optional[Union[int, float, str, Length]] = None
    
    # ================================
    # 显示和布局
    # ================================
    display: Display = Display.FLEX
    
    # Flexbox属性
    flex_direction: FlexDirection = FlexDirection.COLUMN
    justify_content: JustifyContent = JustifyContent.FLEX_START
    align_items: AlignItems = AlignItems.STRETCH
    flex_wrap: Optional[str] = None  # "wrap", "nowrap", "wrap-reverse"
    flex_grow: float = 0
    flex_shrink: float = 1
    flex_basis: Optional[Union[int, float, str, Length]] = None
    flex: Optional[Union[str, int, float]] = None  # CSS flex shorthand "1", "auto", etc.
    
    # Grid属性
    grid_template_columns: Optional[str] = None  # 网格列模板 "1fr 2fr 1fr"
    grid_template_rows: Optional[str] = None     # 网格行模板 "auto 200px auto"
    grid_column: Optional[str] = None            # 网格列定位 "1 / 3"
    grid_row: Optional[str] = None               # 网格行定位 "2 / span 2" 
    grid_area: Optional[str] = None              # 网格区域 "1 / 2 / 3 / 4"
    
    # ================================
    # 尺寸
    # ================================
    width: Optional[Union[int, float, str, Length]] = None
    height: Optional[Union[int, float, str, Length]] = None
    min_width: Optional[Union[int, float, str, Length]] = None
    min_height: Optional[Union[int, float, str, Length]] = None
    max_width: Optional[Union[int, float, str, Length]] = None
    max_height: Optional[Union[int, float, str, Length]] = None
    
    # ================================
    # 间距
    # ================================
    # Margin
    margin: Optional[Union[int, float, str, Length]] = None
    margin_top: Optional[Union[int, float, str, Length]] = None
    margin_right: Optional[Union[int, float, str, Length]] = None
    margin_bottom: Optional[Union[int, float, str, Length]] = None
    margin_left: Optional[Union[int, float, str, Length]] = None
    
    # Padding  
    padding: Optional[Union[int, float, str, Length]] = None
    padding_top: Optional[Union[int, float, str, Length]] = None
    padding_right: Optional[Union[int, float, str, Length]] = None
    padding_bottom: Optional[Union[int, float, str, Length]] = None
    padding_left: Optional[Union[int, float, str, Length]] = None
    
    # Gap
    gap: Optional[Union[int, float, str, Length]] = None
    row_gap: Optional[Union[int, float, str, Length]] = None
    column_gap: Optional[Union[int, float, str, Length]] = None
    
    # ================================
    # 视觉效果
    # ================================
    opacity: float = 1.0
    visible: bool = True
    overflow: OverflowBehavior = OverflowBehavior.VISIBLE
    
    # 边框和背景
    border: Optional[str] = None  # CSS-style border "1px solid #ccc"
    border_radius: Optional[Union[int, float, str, Length]] = None
    border_width: Optional[Union[int, float, str, Length]] = None
    border_color: Optional[str] = None
    border_style: Optional[str] = None  # "solid", "dashed", "dotted"
    background_color: Optional[str] = None  # 背景颜色
    
    # ================================
    # 变换
    # ================================
    scale: Tuple[float, float] = (1.0, 1.0)
    rotation: float = 0.0  # degrees
    translation: Tuple[float, float] = (0.0, 0.0)  # (x, y) pixels
    transform_origin: Tuple[float, float] = (0.5, 0.5)  # (x, y) 0-1
    
    # ================================
    # 裁剪和遮罩
    # ================================
    clip_rect: Optional[Tuple[float, float, float, float]] = None  # (x, y, w, h)
    
    def __post_init__(self):
        """后处理：标准化属性值"""
        # 标准化长度属性
        self._normalize_length_properties()
        
    def _normalize_length_properties(self):
        """标准化长度属性为Length对象"""
        length_props = [
            'top', 'right', 'bottom', 'left',
            'width', 'height', 'min_width', 'min_height', 'max_width', 'max_height',
            'margin', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left',
            'padding', 'padding_top', 'padding_right', 'padding_bottom', 'padding_left',
            'gap', 'row_gap', 'column_gap', 'flex_basis',
            'border_radius', 'border_width'
        ]
        
        for prop in length_props:
            value = getattr(self, prop)
            if value is not None and not isinstance(value, Length):
                setattr(self, prop, self._parse_length_value(value))
    
    def _parse_length_value(self, value: Union[int, float, str]) -> Length:
        """解析长度值"""
        if isinstance(value, (int, float)):
            return px(value)
        elif isinstance(value, str):
            return Length(value)
        return value
    
    def copy(self) -> 'ComponentStyle':
        """创建样式副本"""
        return ComponentStyle(**self.__dict__)
    
    def merge(self, other: 'ComponentStyle') -> 'ComponentStyle':
        """合并两个样式，other中的非None值会覆盖self"""
        merged_dict = self.__dict__.copy()
        
        for key, value in other.__dict__.items():
            if value is not None:
                merged_dict[key] = value
                
        return ComponentStyle(**merged_dict)

# ================================
# 4. 预设样式工厂
# ================================

class StylePresets:
    """预设样式工厂 - 提供常见场景的样式预设"""
    
    @staticmethod
    def modal(width: int = 400, height: int = 300) -> ComponentStyle:
        """模态对话框样式"""
        return ComponentStyle(
            position=Position.ABSOLUTE,
            z_index=ZLayer.MODAL,
            left="50%",
            top="50%", 
            width=px(width),
            height=px(height),
            translation=(-width//2, -height//2)
        )
    
    @staticmethod
    def tooltip(offset_x: int = 0, offset_y: int = -30) -> ComponentStyle:
        """工具提示样式"""
        return ComponentStyle(
            position=Position.RELATIVE,
            z_index=ZLayer.FLOATING,
            left=px(offset_x),
            top=px(offset_y)
        )
    
    @staticmethod
    def floating_button(corner: str = "bottom-right", margin: int = 20) -> ComponentStyle:
        """悬浮按钮样式"""
        style = ComponentStyle(
            position=Position.FIXED,
            z_index=ZLayer.FLOATING
        )
        
        if corner == "bottom-right":
            style.bottom = px(margin)
            style.right = px(margin)
        elif corner == "top-right":
            style.top = px(margin) 
            style.right = px(margin)
        elif corner == "bottom-left":
            style.bottom = px(margin)
            style.left = px(margin)
        elif corner == "top-left":
            style.top = px(margin)
            style.left = px(margin)
            
        return style
    
    @staticmethod
    def fullscreen_overlay(opacity: float = 0.8) -> ComponentStyle:
        """全屏遮罩样式"""
        return ComponentStyle(
            position=Position.FIXED,
            z_index=ZLayer.OVERLAY,
            top=px(0),
            right=px(0),
            bottom=px(0),
            left=px(0),
            opacity=opacity
        )
    
    @staticmethod
    def centered_content() -> ComponentStyle:
        """居中内容样式"""
        return ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER
        )
    
    @staticmethod
    def horizontal_layout(gap: int = 10) -> ComponentStyle:
        """水平布局样式"""
        return ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=AlignItems.CENTER,
            gap=px(gap)
        )
    
    @staticmethod
    def vertical_layout(gap: int = 10) -> ComponentStyle:
        """垂直布局样式"""
        return ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(gap)
        )

# ================================
# 5. 样式工具函数
# ================================

class StyleUtils:
    """样式工具函数"""
    
    @staticmethod
    def parse_margin_padding(value: Union[int, str, Tuple]) -> Tuple[Length, Length, Length, Length]:
        """解析margin/padding的简写形式
        
        支持的格式:
        - 10 -> (10, 10, 10, 10)
        - "10px 20px" -> (10, 20, 10, 20)  
        - (10, 20) -> (10, 20, 10, 20)
        - (10, 20, 30, 40) -> (10, 20, 30, 40)
        
        Returns:
            (top, right, bottom, left)
        """
        if isinstance(value, (int, float)):
            length = px(value)
            return (length, length, length, length)
        elif isinstance(value, str):
            parts = value.split()
            if len(parts) == 1:
                length = Length(parts[0])
                return (length, length, length, length)
            elif len(parts) == 2:
                top_bottom = Length(parts[0])
                left_right = Length(parts[1])
                return (top_bottom, left_right, top_bottom, left_right)
            elif len(parts) == 4:
                return tuple(Length(part) for part in parts)
        elif isinstance(value, (tuple, list)):
            if len(value) == 2:
                top_bottom, left_right = value
                return (px(top_bottom), px(left_right), px(top_bottom), px(left_right))
            elif len(value) == 4:
                return tuple(px(v) for v in value)
        
        # 默认返回0
        zero = px(0)
        return (zero, zero, zero, zero)
    
    @staticmethod
    def merge_styles(*styles: ComponentStyle) -> ComponentStyle:
        """合并多个样式"""
        if not styles:
            return ComponentStyle()
        
        result = styles[0].copy()
        for style in styles[1:]:
            result = result.merge(style)
            
        return result

# ================================
# 6. 测试代码
# ================================

if __name__ == "__main__":
    logger.info("Hibiki UI 样式系统测试\n")
    
    # 测试基础样式创建
    logger.info("🎨 基础样式测试:")
    style = ComponentStyle(
        width=px(200),
        height=px(100),
        margin=px(10),
        position=Position.ABSOLUTE,
        z_index=ZLayer.MODAL
    )
    logger.info(f"宽度: {style.width}")
    logger.info(f"位置: {style.position}")
    logger.info(f"层级: {style.z_index}")
    
    # 测试长度单位解析
    logger.info("\n📏 长度单位测试:")
    lengths = [
        px(100),
        percent(50),
        vw(30),
        vh(40),
        auto,
        Length("200px"),
        Length("75%"),
        Length("50vw")
    ]
    
    for length in lengths:
        logger.info(f"{length} -> value={length.value}, unit={length.unit}")
    
    # 测试预设样式
    logger.info("\n🎯 预设样式测试:")
    modal_style = StylePresets.modal(400, 300)
    logger.info(f"模态框: position={modal_style.position}, z_index={modal_style.z_index}")
    
    tooltip_style = StylePresets.tooltip()
    logger.info(f"工具提示: position={tooltip_style.position}, top={tooltip_style.top}")
    
    fab_style = StylePresets.floating_button("bottom-right")
    logger.info(f"悬浮按钮: position={fab_style.position}, bottom={fab_style.bottom}, right={fab_style.right}")
    
    # 测试样式合并
    logger.info("\n🔄 样式合并测试:")
    base_style = ComponentStyle(width=px(100), height=px(50))
    override_style = ComponentStyle(width=px(200), opacity=0.8)
    merged_style = base_style.merge(override_style)
    logger.info(f"合并结果: width={merged_style.width}, height={merged_style.height}, opacity={merged_style.opacity}")
    
    logger.info("\n✅ 样式系统测试完成！")