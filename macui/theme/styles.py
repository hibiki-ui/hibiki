"""macUI v2 样式组合系统

可组合、可扩展的样式对象系统，支持响应式样式计算。
"""

from typing import Dict, Any, Union, Optional, Callable
from dataclasses import dataclass, asdict
from ..core.signal import Signal, Computed
from AppKit import NSColor
from Foundation import NSMakeRect


@dataclass
class StyleProperties:
    """样式属性数据类"""
    # 背景
    background_color: Optional[Union[NSColor, Signal]] = None
    background_alpha: Optional[float] = None
    
    # 边框
    border_color: Optional[Union[NSColor, Signal]] = None
    border_width: Optional[float] = None
    corner_radius: Optional[float] = None
    
    # 阴影
    shadow_color: Optional[Union[NSColor, Signal]] = None
    shadow_offset: Optional[tuple] = None  # (x, y)
    shadow_blur: Optional[float] = None
    shadow_opacity: Optional[float] = None
    
    # 间距
    padding: Optional[Union[float, tuple]] = None  # 单值或(top, right, bottom, left)
    margin: Optional[Union[float, tuple]] = None
    
    # 尺寸
    width: Optional[float] = None
    height: Optional[float] = None
    min_width: Optional[float] = None
    min_height: Optional[float] = None
    max_width: Optional[float] = None
    max_height: Optional[float] = None
    
    # 变换
    scale: Optional[float] = None
    rotation: Optional[float] = None
    translation: Optional[tuple] = None  # (x, y)
    
    # 动画
    animation_duration: Optional[float] = None
    animation_curve: Optional[str] = None  # 'linear', 'ease-in', 'ease-out', 'ease-in-out'
    
    # 毛玻璃效果
    vibrancy: Optional[str] = None  # 'light', 'dark', None
    material: Optional[str] = None  # 'popover', 'sidebar', 'menu', etc.
    blur_radius: Optional[float] = None
    
    # 透明度
    opacity: Optional[float] = None


class Style:
    """可组合样式对象"""
    
    def __init__(self, **properties):
        """创建样式对象
        
        Args:
            **properties: 样式属性，可以是直接值或StyleProperties的字段
        """
        self.properties = StyleProperties(**properties)
        self._computed_properties: Dict[str, Computed] = {}
    
    def extend(self, **overrides) -> 'Style':
        """扩展样式，返回新的样式对象"""
        # 合并现有属性和覆盖属性
        current_props = asdict(self.properties)
        # 过滤None值
        current_props = {k: v for k, v in current_props.items() if v is not None}
        
        return Style(**{**current_props, **overrides})
    
    def merge(self, other: 'Style') -> 'Style':
        """合并另一个样式"""
        other_props = asdict(other.properties)
        other_props = {k: v for k, v in other_props.items() if v is not None}
        return self.extend(**other_props)
    
    def responsive(self, condition: Signal[bool], true_style: 'Style', false_style: 'Style' = None) -> 'ComputedStyle':
        """创建响应式样式"""
        if false_style is None:
            false_style = self
        
        def compute_style():
            base_style = true_style if condition.value else false_style
            return self.merge(base_style)
        
        return ComputedStyle(compute_style)
    
    def animate(self, duration: float = 0.3, curve: str = 'ease-out') -> 'Style':
        """添加动画属性"""
        return self.extend(
            animation_duration=duration,
            animation_curve=curve
        )
    
    def with_shadow(self, offset: tuple = (0, 2), blur: float = 4, opacity: float = 0.1, color: NSColor = None) -> 'Style':
        """添加阴影"""
        if color is None:
            color = NSColor.blackColor()
        
        return self.extend(
            shadow_offset=offset,
            shadow_blur=blur,
            shadow_opacity=opacity,
            shadow_color=color
        )
    
    def with_corner_radius(self, radius: float) -> 'Style':
        """添加圆角"""
        return self.extend(corner_radius=radius)
    
    def with_background(self, color: Union[NSColor, Signal]) -> 'Style':
        """设置背景色"""
        return self.extend(background_color=color)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {}
        for key, value in asdict(self.properties).items():
            if value is not None:
                result[key] = value
        return result


class ComputedStyle:
    """计算样式 - 动态计算样式属性"""
    
    def __init__(self, compute_fn: Callable[[], Style]):
        self.compute_fn = compute_fn
        self._computed = Computed(lambda: self.compute_fn().to_dict())
    
    @property
    def properties(self) -> Signal[Dict[str, Any]]:
        """获取计算后的样式属性Signal"""
        return self._computed
    
    def to_dict(self) -> Dict[str, Any]:
        """获取当前计算结果"""
        return self._computed.value


class Styles:
    """预定义样式库"""
    
    # === 基础样式 ===
    base = Style()
    
    # === 阴影 ===
    shadow_sm = Style(
        shadow_offset=(0, 1),
        shadow_blur=2,
        shadow_opacity=0.1,
        shadow_color=NSColor.blackColor()
    )
    
    shadow_md = Style(
        shadow_offset=(0, 2),
        shadow_blur=4,
        shadow_opacity=0.12,
        shadow_color=NSColor.blackColor()
    )
    
    shadow_lg = Style(
        shadow_offset=(0, 4),
        shadow_blur=8,
        shadow_opacity=0.15,
        shadow_color=NSColor.blackColor()
    )
    
    shadow_xl = Style(
        shadow_offset=(0, 8),
        shadow_blur=16,
        shadow_opacity=0.18,
        shadow_color=NSColor.blackColor()
    )
    
    # === 圆角 ===
    rounded_none = Style(corner_radius=0)
    rounded_sm = Style(corner_radius=4)
    rounded_md = Style(corner_radius=6)
    rounded_lg = Style(corner_radius=8)
    rounded_xl = Style(corner_radius=12)
    rounded_full = Style(corner_radius=9999)  # 完全圆形
    
    # === 毛玻璃效果 ===
    glass_light = Style(
        vibrancy='light',
        material='popover',
        blur_radius=20
    )
    
    glass_dark = Style(
        vibrancy='dark',
        material='popover',
        blur_radius=20
    )
    
    glass_sidebar = Style(
        vibrancy='light',
        material='sidebar',
        blur_radius=15
    )
    
    # === 动画 ===
    transition_none = Style(animation_duration=0)
    transition_fast = Style(animation_duration=0.15, animation_curve='ease-out')
    transition_normal = Style(animation_duration=0.3, animation_curve='ease-out')
    transition_slow = Style(animation_duration=0.5, animation_curve='ease-out')
    
    # === 交互状态 ===
    hover_lift = Style(
        scale=1.02,
        shadow_offset=(0, 4),
        shadow_blur=8,
        shadow_opacity=0.2
    )
    
    pressed_scale = Style(scale=0.95)
    
    # === 组合样式 ===
    @classmethod
    def card(cls) -> Style:
        """卡片样式"""
        return cls.base.extend(
            background_color=NSColor.controlBackgroundColor(),
            corner_radius=8,
            shadow_offset=(0, 2),
            shadow_blur=4,
            shadow_opacity=0.1,
            padding=16
        )
    
    @classmethod
    def button_primary(cls) -> Style:
        """主按钮样式"""
        return cls.base.extend(
            background_color=NSColor.systemBlueColor(),
            corner_radius=6,
            padding=(8, 16),
            animation_duration=0.15
        )
    
    @classmethod
    def button_secondary(cls) -> Style:
        """次要按钮样式"""
        return cls.base.extend(
            background_color=NSColor.controlColor(),
            corner_radius=6,
            padding=(8, 16),
            border_width=1,
            border_color=NSColor.separatorColor(),
            animation_duration=0.15
        )
    
    @classmethod
    def glass_panel(cls) -> Style:
        """毛玻璃面板样式"""
        return cls.glass_light.extend(
            corner_radius=12,
            border_width=1,
            border_color=NSColor.colorWithRed_green_blue_alpha_(1, 1, 1, 0.2),
            shadow_offset=(0, 4),
            shadow_blur=16,
            shadow_opacity=0.1
        )


class StyleBuilder:
    """样式构建器 - 链式API"""
    
    def __init__(self, base_style: Style = None):
        self._style = base_style or Style()
    
    def background(self, color: Union[NSColor, Signal]) -> 'StyleBuilder':
        """设置背景色"""
        self._style = self._style.with_background(color)
        return self
    
    def corner_radius(self, radius: float) -> 'StyleBuilder':
        """设置圆角"""
        self._style = self._style.with_corner_radius(radius)
        return self
    
    def shadow(self, offset: tuple = (0, 2), blur: float = 4, opacity: float = 0.1) -> 'StyleBuilder':
        """设置阴影"""
        self._style = self._style.with_shadow(offset, blur, opacity)
        return self
    
    def padding(self, padding: Union[float, tuple]) -> 'StyleBuilder':
        """设置内边距"""
        self._style = self._style.extend(padding=padding)
        return self
    
    def animate(self, duration: float = 0.3, curve: str = 'ease-out') -> 'StyleBuilder':
        """设置动画"""
        self._style = self._style.animate(duration, curve)
        return self
    
    def build(self) -> Style:
        """构建最终样式"""
        return self._style
    
    @classmethod
    def create(cls) -> 'StyleBuilder':
        """创建新的样式构建器"""
        return cls()


# 便捷函数
def style(**properties) -> Style:
    """创建样式的便捷函数"""
    return Style(**properties)


def responsive_style(condition: Signal[bool], true_style: Style, false_style: Style = None) -> ComputedStyle:
    """创建响应式样式的便捷函数"""
    base = false_style or Style()
    return base.responsive(condition, true_style, false_style)