#!/usr/bin/env python3
"""
🎨 Hibiki UI 视觉样式增强系统

解决ComponentStyle定义了但未实现的视觉属性问题
提供完整的NSView/CALayer样式应用能力

设计原则：
1. 保持与ComponentStyle API兼容
2. 支持动态样式更新
3. 提供优雅的PyObjC集成
4. 支持响应式样式绑定
"""

from typing import Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
import objc
from AppKit import (
    NSView, NSColor, NSBezierPath, NSRectFill,
    NSCompositingOperationSourceOver, NSGraphicsContext
)
from Foundation import NSMakeRect
from Quartz import (
    CALayer, kCALayerMinXMinYCorner, kCALayerMaxXMinYCorner,
    kCALayerMinXMaxYCorner, kCALayerMaxXMaxYCorner,
    CGColorCreateGenericRGB
)

from hibiki.ui.core.styles import ComponentStyle
from hibiki.ui.core.reactive import Signal
from hibiki.ui.core.logging import get_logger

logger = get_logger("styling.enhanced")

# ================================
# 颜色处理工具
# ================================

def parse_color(color_value: Union[str, Tuple[float, float, float], Tuple[float, float, float, float]]) -> NSColor:
    """将各种颜色格式转换为NSColor
    
    支持格式：
    - Hex: '#ff0000', '#f00', 'red'
    - RGB tuple: (1.0, 0.0, 0.0)
    - RGBA tuple: (1.0, 0.0, 0.0, 1.0)
    - CSS名称: 'red', 'blue', 'transparent'
    """
    if isinstance(color_value, str):
        if color_value.startswith('#'):
            return parse_hex_color(color_value)
        else:
            return parse_css_color(color_value)
    elif isinstance(color_value, (tuple, list)):
        if len(color_value) == 3:
            r, g, b = color_value
            return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
        elif len(color_value) == 4:
            r, g, b, a = color_value
            return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
    
    # 默认透明色
    return NSColor.clearColor()

def parse_hex_color(hex_str: str) -> NSColor:
    """解析十六进制颜色"""
    hex_str = hex_str.lstrip('#')
    
    if len(hex_str) == 3:
        # #f00 -> #ff0000
        hex_str = ''.join([c*2 for c in hex_str])
    
    if len(hex_str) == 6:
        r = int(hex_str[0:2], 16) / 255.0
        g = int(hex_str[2:4], 16) / 255.0  
        b = int(hex_str[4:6], 16) / 255.0
        return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
    
    return NSColor.clearColor()

def parse_css_color(name: str) -> NSColor:
    """解析CSS颜色名称"""
    css_colors = {
        'red': NSColor.redColor(),
        'green': NSColor.greenColor(),
        'blue': NSColor.blueColor(),
        'white': NSColor.whiteColor(),
        'black': NSColor.blackColor(),
        'gray': NSColor.grayColor(),
        'yellow': NSColor.yellowColor(),
        'orange': NSColor.orangeColor(),
        'purple': NSColor.purpleColor(),
        'brown': NSColor.brownColor(),
        'clear': NSColor.clearColor(),
        'transparent': NSColor.clearColor(),
    }
    return css_colors.get(name.lower(), NSColor.clearColor())

# ================================
# 边框样式处理
# ================================

@dataclass
class BorderStyle:
    """边框样式数据类"""
    width: float = 1.0
    color: NSColor = None
    style: str = 'solid'  # solid, dashed, dotted
    radius: float = 0.0
    
    def __post_init__(self):
        if self.color is None:
            self.color = NSColor.blackColor()

def parse_border(border_value: str) -> BorderStyle:
    """解析边框样式字符串
    
    支持格式：
    - "1px solid #000"
    - "2px dashed red"  
    - "thin solid black"
    """
    parts = border_value.strip().split()
    border = BorderStyle()
    
    for part in parts:
        if part.endswith('px'):
            border.width = float(part[:-2])
        elif part in ['solid', 'dashed', 'dotted']:
            border.style = part
        elif part.startswith('#') or part in ['red', 'blue', 'green', 'black', 'white']:
            border.color = parse_color(part)
        elif part in ['thin', 'medium', 'thick']:
            width_map = {'thin': 1.0, 'medium': 2.0, 'thick': 3.0}
            border.width = width_map[part]
    
    return border

# ================================
# 核心样式应用器
# ================================

class EnhancedStyleApplier:
    """增强样式应用器 - 将ComponentStyle真正应用到NSView"""
    
    def __init__(self, view: NSView):
        self.view = view
        self.layer = view.layer()
        self._background_layer: Optional[CALayer] = None
        self._border_layer: Optional[CALayer] = None
        
        # 确保视图有layer
        if not self.layer:
            view.setWantsLayer_(True)
            self.layer = view.layer()
    
    def apply_style(self, style: ComponentStyle) -> None:
        """应用完整样式到视图"""
        logger.info(f"🎨 应用增强样式到视图: {type(self.view).__name__}")
        
        # 应用背景色
        if style.background_color:
            self._apply_background_color(style.background_color)
        
        # 应用边框
        if style.border:
            border = parse_border(style.border)
            self._apply_border(border)
        
        # 应用圆角
        if style.border_radius:
            self._apply_border_radius(style.border_radius)
        
        # 应用透明度
        if style.opacity is not None:
            self.layer.setOpacity_(style.opacity)
        
        # 应用阴影
        if hasattr(style, 'box_shadow') and style.box_shadow:
            self._apply_shadow(style.box_shadow)
        
        logger.info(f"✅ 样式应用完成")
    
    def _apply_background_color(self, color_value: Union[str, tuple]) -> None:
        """应用背景色"""
        ns_color = parse_color(color_value)
        
        # 使用CALayer的backgroundColor（性能更好）
        cg_color = ns_color.CGColor()
        self.layer.setBackgroundColor_(cg_color)
        
        logger.debug(f"🎨 应用背景色: {color_value}")
    
    def _apply_border(self, border: BorderStyle) -> None:
        """应用边框"""
        # 设置边框颜色和宽度
        cg_color = border.color.CGColor()
        self.layer.setBorderColor_(cg_color)
        self.layer.setBorderWidth_(border.width)
        
        logger.debug(f"🔲 应用边框: {border.width}px {border.style} {border.color}")
    
    def _apply_border_radius(self, radius_value: Union[int, float, str, Any]) -> None:
        """应用圆角"""
        if isinstance(radius_value, str):
            if radius_value.endswith('px'):
                radius = float(radius_value[:-2])
            else:
                radius = float(radius_value)
        elif hasattr(radius_value, 'value'):
            # 处理Length对象
            radius = float(radius_value.value)
        else:
            radius = float(radius_value)
        
        self.layer.setCornerRadius_(radius)
        self.layer.setMasksToBounds_(True)  # 确保内容被裁切
        
        logger.debug(f"🔘 应用圆角: {radius}px")
    
    def _apply_shadow(self, shadow_value: str) -> None:
        """应用阴影"""
        # 解析阴影值：如 "0 2px 4px rgba(0,0,0,0.1)"
        # 简化实现，可以后续扩展
        self.layer.setShadowOpacity_(0.3)
        self.layer.setShadowRadius_(2.0)
        self.layer.setShadowOffset_((0, -2))
        
        logger.debug(f"🌫️ 应用阴影: {shadow_value}")

# ================================
# 响应式样式绑定
# ================================

class ReactiveStyleBinding:
    """响应式样式绑定 - 支持Signal驱动的样式更新"""
    
    def __init__(self, view: NSView):
        self.view = view
        self.applier = EnhancedStyleApplier(view)
        self._bindings: Dict[str, Any] = {}
    
    def bind_style_property(self, property_name: str, signal: Signal) -> None:
        """绑定样式属性到Signal"""
        
        def update_property():
            value = signal.value
            logger.debug(f"🔄 更新样式属性 {property_name}: {value}")
            
            # 创建临时样式对象
            temp_style = ComponentStyle()
            setattr(temp_style, property_name, value)
            
            # 应用单个属性
            if property_name == 'background_color':
                self.applier._apply_background_color(value)
            elif property_name == 'border':
                border = parse_border(value)
                self.applier._apply_border(border)
            elif property_name == 'border_radius':
                self.applier._apply_border_radius(value)
            elif property_name == 'opacity':
                self.applier.layer.setOpacity_(value)
        
        # 立即执行一次
        update_property()
        
        # 创建响应式绑定
        from hibiki.ui.core.reactive import Effect
        effect = Effect(update_property)
        self._bindings[property_name] = effect
        
        logger.info(f"📡 绑定响应式样式属性: {property_name}")
    
    def unbind_all(self) -> None:
        """解除所有绑定"""
        self._bindings.clear()
        logger.info("🔌 解除所有样式绑定")

# ================================
# 便捷工具函数
# ================================

def enhance_view_styling(view: NSView, style: ComponentStyle) -> EnhancedStyleApplier:
    """为NSView启用增强样式支持"""
    applier = EnhancedStyleApplier(view)
    applier.apply_style(style)
    return applier

def create_reactive_styling(view: NSView) -> ReactiveStyleBinding:
    """为NSView创建响应式样式绑定"""
    return ReactiveStyleBinding(view)

# ================================
# 组件集成工具
# ================================

class StylableViewMixin:
    """可样式化视图Mixin - 为组件添加增强样式能力"""
    
    def __init__(self):
        self._style_applier: Optional[EnhancedStyleApplier] = None
        self._reactive_styling: Optional[ReactiveStyleBinding] = None
    
    def apply_enhanced_style(self, style: ComponentStyle) -> None:
        """应用增强样式"""
        if hasattr(self, '_nsview') and self._nsview:
            if not self._style_applier:
                self._style_applier = EnhancedStyleApplier(self._nsview)
            
            self._style_applier.apply_style(style)
    
    def setup_reactive_styling(self) -> ReactiveStyleBinding:
        """设置响应式样式"""
        if hasattr(self, '_nsview') and self._nsview:
            if not self._reactive_styling:
                self._reactive_styling = ReactiveStyleBinding(self._nsview)
            return self._reactive_styling
        
        raise RuntimeError("视图未初始化，无法设置响应式样式")