"""Hibiki UI v4 主题管理器

统一管理应用的颜色、字体和外观，提供响应式主题切换
"""

from typing import Optional, Dict, List, Callable
import weakref

from .colors import ColorScheme, ColorRole, PresetColorSchemes
from .fonts import FontScheme, TextStyle, PresetFontSchemes  
from .appearance import AppearanceManager, AppearanceMode, AppearanceObserver
from ..core.reactive import Signal, Effect

from ..core.logging import get_logger
logger = get_logger('theme.theme_manager')



class Theme:
    """主题类 - 包含完整的外观定义"""
    
    def __init__(
        self,
        name: str,
        color_scheme: ColorScheme,
        font_scheme: FontScheme,
        appearance_mode: str = AppearanceMode.AUTO
    ):
        self.name = name
        self.color_scheme = color_scheme
        self.font_scheme = font_scheme
        self.appearance_mode = appearance_mode
    
    def get_color(self, role: ColorRole):
        """获取颜色"""
        return self.color_scheme.get_color(role)
    
    def get_font(self, style: TextStyle):
        """获取字体"""
        return self.font_scheme.get_font(style)
    
    def __str__(self):
        return f"Theme(name={self.name}, colors={self.color_scheme.name}, fonts={self.font_scheme.name})"


class ThemeChangeEvent:
    """主题变化事件"""
    
    def __init__(self, old_theme: Optional[Theme], new_theme: Theme, trigger: str):
        self.old_theme = old_theme
        self.new_theme = new_theme
        self.trigger = trigger  # "manual", "appearance_change", "system_preference"


class ThemeManager:
    """主题管理器 - 应用主题的中央控制器"""
    
    _instance: Optional["ThemeManager"] = None
    
    def __init__(self):
        if ThemeManager._instance is not None:
            raise RuntimeError("ThemeManager is a singleton. Use ThemeManager.shared() instead.")
        
        # 当前主题信号
        self._current_theme = Signal(self._create_default_theme())
        
        # 主题变化观察者
        self._theme_observers: List[weakref.ReferenceType] = []
        
        # 外观管理器
        self._appearance_manager = AppearanceManager.shared()
        self._appearance_observer: Optional[AppearanceObserver] = None
        
        # 注册的主题
        self._registered_themes: Dict[str, Theme] = {}
        
        # 设置默认主题
        self._register_preset_themes()
        self._setup_appearance_tracking()
        
        logger.info(f"🎨 ThemeManager初始化完成，默认主题: {self._current_theme.value}")
    
    @classmethod
    def shared(cls) -> "ThemeManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _create_default_theme(self) -> Theme:
        """创建默认主题"""
        return Theme(
            name="System Default",
            color_scheme=PresetColorSchemes.system(),
            font_scheme=PresetFontSchemes.system(),
            appearance_mode=AppearanceMode.AUTO
        )
    
    def _register_preset_themes(self):
        """注册预设主题"""
        # 系统主题
        system_theme = Theme(
            name="System",
            color_scheme=PresetColorSchemes.system(),
            font_scheme=PresetFontSchemes.system(),
            appearance_mode=AppearanceMode.AUTO
        )
        self._registered_themes["system"] = system_theme
        
        # 开发者主题
        developer_theme = Theme(
            name="Developer",
            color_scheme=PresetColorSchemes.developer_dark(),
            font_scheme=PresetFontSchemes.developer(),
            appearance_mode=AppearanceMode.DARK
        )
        self._registered_themes["developer"] = developer_theme
        
        # 高对比度主题
        high_contrast_theme = Theme(
            name="High Contrast",
            color_scheme=PresetColorSchemes.high_contrast(),
            font_scheme=PresetFontSchemes.accessibility(),
            appearance_mode=AppearanceMode.LIGHT
        )
        self._registered_themes["high_contrast"] = high_contrast_theme
    
    def _setup_appearance_tracking(self):
        """设置外观变化跟踪"""
        def on_appearance_change(appearance: str):
            current_theme = self._current_theme.value
            if current_theme.appearance_mode == AppearanceMode.AUTO:
                # 自动主题需要响应系统外观变化
                self._notify_theme_change(
                    ThemeChangeEvent(current_theme, current_theme, "appearance_change")
                )
                logger.info(f"🌗 主题响应外观变化: {appearance}")
        
        self._appearance_observer = self._appearance_manager.add_observer(on_appearance_change)
    
    def _notify_theme_change(self, event: ThemeChangeEvent):
        """通知主题变化"""
        # 清理无效的弱引用
        self._theme_observers = [ref for ref in self._theme_observers if ref() is not None]
        
        # 通知有效的观察者
        for observer_ref in self._theme_observers:
            callback = observer_ref()
            if callback:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"ThemeManager observer callback error: {e}")
    
    @property
    def current_theme(self) -> Signal[Theme]:
        """当前主题Signal"""
        return self._current_theme
    
    def get_color(self, role: ColorRole):
        """获取当前主题的颜色"""
        return self._current_theme.value.get_color(role)
    
    def get_font(self, style: TextStyle):
        """获取当前主题的字体"""
        return self._current_theme.value.get_font(style)
    
    def set_theme(self, theme: Theme, apply_appearance: bool = True):
        """设置当前主题
        
        Args:
            theme: 新主题
            apply_appearance: 是否应用外观模式到应用程序
        """
        old_theme = self._current_theme.value
        
        # 应用外观模式
        if apply_appearance and theme.appearance_mode != AppearanceMode.AUTO:
            self._appearance_manager.set_app_appearance(theme.appearance_mode)
        
        # 更新主题Signal
        self._current_theme.value = theme
        
        # 通知主题变化
        event = ThemeChangeEvent(old_theme, theme, "manual")
        self._notify_theme_change(event)
        
        logger.info(f"🎨 主题已切换: {old_theme.name} -> {theme.name}")
    
    def set_theme_by_name(self, theme_name: str):
        """通过名称设置主题"""
        theme = self._registered_themes.get(theme_name)
        if theme:
            self.set_theme(theme)
        else:
            logger.error(f"❌ 未找到主题: {theme_name}")
            logger.info(f"可用主题: {list(self._registered_themes.keys())}")
    
    def register_theme(self, theme: Theme):
        """注册自定义主题"""
        self._registered_themes[theme.name.lower().replace(" ", "_")] = theme
        logger.info(f"📝 已注册主题: {theme.name}")
    
    def get_registered_themes(self) -> Dict[str, Theme]:
        """获取所有注册的主题"""
        return self._registered_themes.copy()
    
    def add_theme_observer(self, callback: Callable[[ThemeChangeEvent], None]) -> int:
        """添加主题变化观察者
        
        Args:
            callback: 回调函数，参数为ThemeChangeEvent
            
        Returns:
            观察者ID
        """
        observer_ref = weakref.ref(callback)
        self._theme_observers.append(observer_ref)
        return len(self._theme_observers) - 1
    
    def is_dark_mode(self) -> bool:
        """当前主题是否为深色模式"""
        current_theme = self._current_theme.value
        if current_theme.appearance_mode == AppearanceMode.AUTO:
            return self._appearance_manager.is_dark_mode()
        else:
            return current_theme.appearance_mode == AppearanceMode.DARK
    
    def create_reactive_effect_for_theme(self, effect_fn: Callable[[Theme], None]) -> Effect:
        """创建响应主题变化的Effect
        
        Args:
            effect_fn: 效果函数，参数为当前主题
            
        Returns:
            Effect实例
        """
        def reactive_effect():
            current_theme = self._current_theme.value
            effect_fn(current_theme)
        
        return Effect(reactive_effect)


# 预设主题
class PresetThemes:
    """预设主题集合"""
    
    @classmethod
    def system(cls) -> Theme:
        """系统默认主题"""
        return Theme(
            name="System",
            color_scheme=PresetColorSchemes.system(),
            font_scheme=PresetFontSchemes.system(),
            appearance_mode=AppearanceMode.AUTO
        )
    
    @classmethod
    def developer_dark(cls) -> Theme:
        """开发者深色主题"""
        return Theme(
            name="Developer Dark",
            color_scheme=PresetColorSchemes.developer_dark(),
            font_scheme=PresetFontSchemes.developer(),
            appearance_mode=AppearanceMode.DARK
        )
    
    @classmethod
    def high_contrast(cls) -> Theme:
        """高对比度主题"""
        return Theme(
            name="High Contrast",
            color_scheme=PresetColorSchemes.high_contrast(),
            font_scheme=PresetFontSchemes.accessibility(),
            appearance_mode=AppearanceMode.LIGHT
        )


# 便捷函数
def get_theme_manager() -> ThemeManager:
    """获取主题管理器实例"""
    return ThemeManager.shared()


def get_current_theme() -> Theme:
    """获取当前主题"""
    return get_theme_manager().current_theme.value


def set_theme(theme: Theme):
    """设置当前主题"""
    get_theme_manager().set_theme(theme)


def get_color(role: ColorRole):
    """获取当前主题的颜色"""
    return get_theme_manager().get_color(role)


def get_font(style: TextStyle):
    """获取当前主题的字体"""
    return get_theme_manager().get_font(style)