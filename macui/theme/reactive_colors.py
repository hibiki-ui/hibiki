"""macUI v2 响应式颜色系统

将静态颜色转换为响应式Signal，实现真正的动态主题。
"""

from typing import Dict, Union, Any
from ..core.signal import Signal, Computed
from .appearance import AppearanceManager, AppearanceMode
from .colors import ColorRole, SystemColors
from AppKit import NSColor


class ReactiveColor:
    """响应式颜色类 - 根据外观模式返回不同颜色"""
    
    def __init__(
        self, 
        light_color: Union[NSColor, str], 
        dark_color: Union[NSColor, str],
        name: str = ""
    ):
        self.light_color = self._ensure_nscolor(light_color)
        self.dark_color = self._ensure_nscolor(dark_color)
        self.name = name
        
        # 创建响应式Signal
        self._appearance_manager = AppearanceManager.shared()
        self._color_signal = Signal(self._current_color())
        
        # 监听外观变化
        self._appearance_observer = self._appearance_manager.add_observer(
            self._on_appearance_changed
        )
    
    def _ensure_nscolor(self, color: Union[NSColor, str]) -> NSColor:
        """确保颜色为NSColor对象"""
        if isinstance(color, str):
            if color.startswith('#'):
                # 十六进制颜色转换
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                a = 1.0
                if len(hex_color) == 8:
                    a = int(hex_color[6:8], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
        return color
    
    def _current_color(self) -> NSColor:
        """获取当前外观下的颜色"""
        is_dark = self._appearance_manager.is_dark_mode()
        return self.dark_color if is_dark else self.light_color
    
    def _on_appearance_changed(self, appearance: str):
        """外观变化回调"""
        new_color = self._current_color()
        if new_color != self._color_signal.value:
            self._color_signal.value = new_color
            if self.name:
                print(f"🎨 响应式颜色'{self.name}'更新: {appearance}模式")
    
    @property
    def signal(self) -> Signal[NSColor]:
        """获取颜色的响应式Signal"""
        return self._color_signal
    
    def get_color(self) -> NSColor:
        """获取当前颜色值"""
        return self._color_signal.value


class ReactiveColorScheme:
    """响应式颜色方案"""
    
    def __init__(self, name: str):
        self.name = name
        self._reactive_colors: Dict[ColorRole, ReactiveColor] = {}
        self._static_colors: Dict[ColorRole, NSColor] = {}
        
        # 设置系统颜色的响应式版本
        self._setup_system_reactive_colors()
    
    def _setup_system_reactive_colors(self):
        """设置系统颜色的响应式版本"""
        # 创建系统颜色的响应式Signal
        for role in ColorRole:
            system_color = self._get_system_color(role)
            # 系统颜色本身就是动态的，我们包装成响应式Signal
            reactive_color = SystemReactiveColor(system_color, role.value)
            self._reactive_colors[role] = reactive_color
    
    def _get_system_color(self, role: ColorRole) -> NSColor:
        """获取系统默认颜色（复用现有逻辑）"""
        from .colors import SystemColors
        color_mapping = {
            ColorRole.PRIMARY_TEXT: SystemColors.primary_text,
            ColorRole.SECONDARY_TEXT: SystemColors.secondary_text,
            ColorRole.TERTIARY_TEXT: SystemColors.tertiary_text,
            ColorRole.PLACEHOLDER_TEXT: SystemColors.placeholder_text,
            
            ColorRole.PRIMARY_BACKGROUND: SystemColors.primary_background,
            ColorRole.SECONDARY_BACKGROUND: SystemColors.secondary_background, 
            ColorRole.TERTIARY_BACKGROUND: SystemColors.tertiary_background,
            
            ColorRole.ACCENT_COLOR: SystemColors.accent_color,
            ColorRole.SUCCESS_COLOR: SystemColors.success_color,
            ColorRole.WARNING_COLOR: SystemColors.warning_color,
            ColorRole.ERROR_COLOR: SystemColors.error_color,
            
            ColorRole.CONTROL_TEXT: SystemColors.control_text,
            ColorRole.CONTROL_BACKGROUND: SystemColors.control_background,
            ColorRole.SELECTED_TEXT: SystemColors.selected_text,
            ColorRole.SELECTED_BACKGROUND: SystemColors.selected_background,
        }
        
        getter = color_mapping.get(role)
        if getter:
            return getter()
        return SystemColors.primary_text()
    
    def color(self, role: ColorRole) -> Signal[NSColor]:
        """获取响应式颜色Signal"""
        if role in self._reactive_colors:
            return self._reactive_colors[role].signal
        elif role in self._static_colors:
            # 静态颜色包装为Signal
            return Signal(self._static_colors[role])
        else:
            # 回退到系统颜色
            return Signal(self._get_system_color(role))
    
    def set_color(
        self, 
        role: ColorRole, 
        light_color: Union[NSColor, str], 
        dark_color: Union[NSColor, str] = None
    ):
        """设置响应式颜色"""
        if dark_color is None:
            dark_color = light_color
        
        reactive_color = ReactiveColor(light_color, dark_color, role.value)
        self._reactive_colors[role] = reactive_color
        print(f"🎨 设置响应式颜色: {role.value}")
    
    def set_static_color(self, role: ColorRole, color: Union[NSColor, str]):
        """设置静态颜色（不响应外观变化）"""
        if isinstance(color, str):
            color = ReactiveColor._ensure_nscolor(None, color)
        self._static_colors[role] = color


class SystemReactiveColor(ReactiveColor):
    """系统颜色的响应式包装"""
    
    def __init__(self, system_color_getter: NSColor, name: str):
        self.system_color_getter = system_color_getter
        self.name = name
        
        # 直接使用系统颜色，它们本身就是动态的
        self._appearance_manager = AppearanceManager.shared()
        self._color_signal = Signal(system_color_getter)
        
        # 监听外观变化，重新获取系统颜色
        self._appearance_observer = self._appearance_manager.add_observer(
            self._on_appearance_changed
        )
    
    def _on_appearance_changed(self, appearance: str):
        """外观变化时重新获取系统颜色"""
        # 系统颜色会自动适应，但我们需要通知Signal更新
        self._color_signal.value = self.system_color_getter
        print(f"🎨 系统颜色'{self.name}'响应外观变化: {appearance}")


class ReactiveColorFactory:
    """响应式颜色工厂"""
    
    @staticmethod
    def create_adaptive_color(
        light: Union[NSColor, str], 
        dark: Union[NSColor, str],
        name: str = ""
    ) -> ReactiveColor:
        """创建自适应颜色"""
        return ReactiveColor(light, dark, name)
    
    @staticmethod
    def create_semantic_colors() -> Dict[str, ReactiveColor]:
        """创建语义化颜色集合"""
        return {
            'primary': ReactiveColor('#007AFF', '#0A84FF', 'primary'),
            'secondary': ReactiveColor('#8E8E93', '#8E8E93', 'secondary'),
            'success': ReactiveColor('#34C759', '#30D158', 'success'),
            'warning': ReactiveColor('#FF9500', '#FF9F0A', 'warning'),
            'error': ReactiveColor('#FF3B30', '#FF453A', 'error'),
            'background': ReactiveColor('#FFFFFF', '#000000', 'background'),
            'surface': ReactiveColor('#F2F2F7', '#1C1C1E', 'surface'),
            'card': ReactiveColor('#FFFFFF', '#2C2C2E', 'card'),
        }
    
    @staticmethod
    def create_brand_colors(brand_definition: dict) -> Dict[str, ReactiveColor]:
        """从品牌定义创建颜色"""
        colors = {}
        for name, definition in brand_definition.get('colors', {}).items():
            if isinstance(definition, dict) and 'light' in definition and 'dark' in definition:
                colors[name] = ReactiveColor(
                    definition['light'], 
                    definition['dark'], 
                    name
                )
            else:
                colors[name] = ReactiveColor(definition, definition, name)
        return colors