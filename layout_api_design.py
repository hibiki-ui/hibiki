#!/usr/bin/env python3
"""
macUI v4.0 完整布局API设计
支持Flexbox、Grid、绝对定位、Z-Index的统一布局系统
"""

from enum import Enum
from typing import Union, Optional, Literal
from dataclasses import dataclass

# ================================
# 1. Position 定位类型
# ================================

class Position(Enum):
    """定位类型枚举 - 类似CSS position属性"""
    
    # 默认定位 - 参与flex/grid布局计算
    STATIC = "static"
    
    # 相对定位 - 相对于原本位置偏移
    RELATIVE = "relative" 
    
    # 绝对定位 - 相对于最近的positioned父元素
    ABSOLUTE = "absolute"
    
    # 固定定位 - 相对于窗口视口
    FIXED = "fixed"
    
    # 粘性定位 - 滚动时在relative和fixed间切换
    STICKY = "sticky"

# ================================
# 2. Z-Index 层级管理
# ================================

class ZLayer(Enum):
    """预定义的Z层级常量"""
    
    # 基础内容层
    CONTENT = 0
    
    # 悬浮内容（工具提示、下拉菜单等）
    FLOATING = 1000
    
    # 模态层（对话框、弹窗等）
    MODAL = 2000
    
    # 最高层（系统通知、加载指示器等）
    OVERLAY = 3000
    
    # 调试层（开发工具等）
    DEBUG = 9000

# ================================
# 3. 坐标和尺寸单位
# ================================

class LengthUnit(Enum):
    """长度单位枚举"""
    PX = "px"      # 像素
    PERCENT = "%"   # 百分比
    VW = "vw"      # 视口宽度百分比
    VH = "vh"      # 视口高度百分比
    AUTO = "auto"   # 自动

@dataclass
class Length:
    """长度值 - 支持不同单位"""
    value: Union[int, float, str]
    unit: LengthUnit = LengthUnit.PX
    
    def __post_init__(self):
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

# 便捷构造函数
def px(value: Union[int, float]) -> Length:
    return Length(value, LengthUnit.PX)

def percent(value: Union[int, float]) -> Length:
    return Length(value, LengthUnit.PERCENT)

def vw(value: Union[int, float]) -> Length:
    return Length(value, LengthUnit.VW)

def vh(value: Union[int, float]) -> Length:
    return Length(value, LengthUnit.VH)

auto = Length("auto", LengthUnit.AUTO)

# ================================
# 4. 完整的样式系统
# ================================

@dataclass
class LayoutStyle:
    """完整的布局样式系统"""
    
    # ================================
    # Position & Z-Index
    # ================================
    position: Position = Position.STATIC
    z_index: Union[int, ZLayer] = ZLayer.CONTENT
    
    # 绝对/固定/相对定位的坐标
    top: Optional[Length] = None
    right: Optional[Length] = None  
    bottom: Optional[Length] = None
    left: Optional[Length] = None
    
    # ================================
    # Flexbox Properties (现有)
    # ================================
    display: str = "flex"
    flex_direction: str = "column"
    justify_content: str = "flex-start"
    align_items: str = "stretch"
    flex_grow: float = 0
    flex_shrink: float = 1
    flex_basis: Optional[Length] = None
    
    # ================================
    # Grid Properties (扩展)
    # ================================
    grid_template_columns: Optional[str] = None
    grid_template_rows: Optional[str] = None
    grid_column: Optional[str] = None
    grid_row: Optional[str] = None
    grid_area: Optional[str] = None
    gap: Optional[Length] = None
    
    # ================================
    # Box Model
    # ================================
    width: Optional[Length] = None
    height: Optional[Length] = None
    min_width: Optional[Length] = None
    min_height: Optional[Length] = None
    max_width: Optional[Length] = None
    max_height: Optional[Length] = None
    
    # Margin
    margin_top: Optional[Length] = None
    margin_right: Optional[Length] = None
    margin_bottom: Optional[Length] = None
    margin_left: Optional[Length] = None
    
    # Padding  
    padding_top: Optional[Length] = None
    padding_right: Optional[Length] = None
    padding_bottom: Optional[Length] = None
    padding_left: Optional[Length] = None
    
    # ================================
    # Visual Properties
    # ================================
    opacity: float = 1.0
    visible: bool = True
    overflow: str = "visible"  # visible, hidden, scroll, auto
    
    # 变换
    transform_origin: tuple = (0.5, 0.5)  # (x, y) 0-1
    scale: tuple = (1.0, 1.0)  # (x, y)
    rotation: float = 0.0  # degrees
    translation: tuple = (0.0, 0.0)  # (x, y) pixels

# ================================
# 5. 布局API便捷方法
# ================================

class LayoutAPI:
    """布局API便捷方法类 - 用于组件继承"""
    
    def __init__(self):
        self.style = LayoutStyle()
    
    # ================================
    # Position & Z-Index API
    # ================================
    
    def absolute(self, top=None, right=None, bottom=None, left=None, z_index=None):
        """设置绝对定位"""
        self.style.position = Position.ABSOLUTE
        if top is not None: self.style.top = self._parse_length(top)
        if right is not None: self.style.right = self._parse_length(right)
        if bottom is not None: self.style.bottom = self._parse_length(bottom)
        if left is not None: self.style.left = self._parse_length(left)
        if z_index is not None: self.style.z_index = z_index
        return self
    
    def fixed(self, top=None, right=None, bottom=None, left=None, z_index=None):
        """设置固定定位"""
        self.style.position = Position.FIXED
        if top is not None: self.style.top = self._parse_length(top)
        if right is not None: self.style.right = self._parse_length(right)
        if bottom is not None: self.style.bottom = self._parse_length(bottom)
        if left is not None: self.style.left = self._parse_length(left)
        if z_index is not None: self.style.z_index = z_index
        return self
        
    def relative(self, top=None, right=None, bottom=None, left=None):
        """设置相对定位"""
        self.style.position = Position.RELATIVE
        if top is not None: self.style.top = self._parse_length(top)
        if right is not None: self.style.right = self._parse_length(right)
        if bottom is not None: self.style.bottom = self._parse_length(bottom)
        if left is not None: self.style.left = self._parse_length(left)
        return self
    
    def z_index(self, value: Union[int, ZLayer]):
        """设置Z层级"""
        self.style.z_index = value
        return self
        
    def layer(self, layer: ZLayer):
        """设置到预定义层级"""
        self.style.z_index = layer
        return self
    
    # ================================
    # 高级定位便捷方法
    # ================================
    
    def top_left(self, top=0, left=0, z_index=None):
        """定位到左上角"""
        return self.absolute(top=top, left=left, z_index=z_index)
    
    def top_right(self, top=0, right=0, z_index=None):
        """定位到右上角"""
        return self.absolute(top=top, right=right, z_index=z_index)
    
    def bottom_left(self, bottom=0, left=0, z_index=None):
        """定位到左下角"""
        return self.absolute(bottom=bottom, left=left, z_index=z_index)
        
    def bottom_right(self, bottom=0, right=0, z_index=None):
        """定位到右下角"""
        return self.absolute(bottom=bottom, right=right, z_index=z_index)
    
    def center(self, z_index=None):
        """居中定位（使用transform）"""
        return self.absolute(top="50%", left="50%", z_index=z_index).translate(-0.5, -0.5)
    
    def fullscreen(self, z_index=ZLayer.OVERLAY):
        """全屏覆盖"""
        return self.fixed(top=0, right=0, bottom=0, left=0, z_index=z_index)
    
    # ================================
    # 变换API
    # ================================
    
    def scale(self, x=1.0, y=None):
        """设置缩放"""
        if y is None: y = x
        self.style.scale = (x, y)
        return self
    
    def rotate(self, degrees):
        """设置旋转"""
        self.style.rotation = degrees
        return self
        
    def translate(self, x=0, y=0):
        """设置平移"""
        self.style.translation = (x, y)
        return self
    
    def opacity(self, value):
        """设置透明度"""
        self.style.opacity = max(0.0, min(1.0, value))
        return self
    
    # ================================
    # Size API
    # ================================
    
    def width(self, value):
        """设置宽度"""
        self.style.width = self._parse_length(value)
        return self
        
    def height(self, value):
        """设置高度"""
        self.style.height = self._parse_length(value)
        return self
    
    # ================================
    # 工具方法
    # ================================
    
    def _parse_length(self, value):
        """解析长度值"""
        if isinstance(value, Length):
            return value
        elif isinstance(value, (int, float)):
            return px(value)
        elif isinstance(value, str):
            return Length(value)
        return value

# ================================
# 6. 使用示例
# ================================

if __name__ == "__main__":
    print("macUI v4.0 完整布局API设计示例\n")
    
    # 示例1：模态对话框
    print("🎨 示例1：创建模态对话框")
    modal_api = LayoutAPI()
    modal = modal_api.center(z_index=ZLayer.MODAL).width(px(400)).height(px(300))
    print(f"模态框样式: position={modal.style.position}, z_index={modal.style.z_index}")
    print()
    
    # 示例2：悬浮工具栏
    print("🎨 示例2：创建悬浮工具栏")
    toolbar_api = LayoutAPI() 
    toolbar = toolbar_api.top_right(top=20, right=20, z_index=ZLayer.FLOATING)
    print(f"工具栏样式: top={toolbar.style.top}, right={toolbar.style.right}")
    print()
    
    # 示例3：全屏加载遮罩
    print("🎨 示例3：创建全屏加载遮罩")
    overlay_api = LayoutAPI()
    overlay = overlay_api.fullscreen().opacity(0.8)
    print(f"遮罩样式: position={overlay.style.position}, opacity={overlay.style.opacity}")
    print()
    
    # 示例4：相对定位的提示框
    print("🎨 示例4：创建相对定位的提示框")
    tooltip_api = LayoutAPI()
    tooltip = tooltip_api.relative(top=-30).z_index(ZLayer.FLOATING)
    print(f"提示框样式: position={tooltip.style.position}, top={tooltip.style.top}")
    print()