"""macUI v2 增强主题管理器

集成响应式颜色、样式组合系统和视觉效果的完整主题管理。
"""

import json
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

from .theme_manager import Theme as BaseTheme, ThemeManager as BaseThemeManager
from .reactive_colors import ReactiveColorScheme, ReactiveColorFactory
from .styles import Style, Styles, ComputedStyle, StyleBuilder
from .visual_effects import VisualEffect, GlassBox, StyleApplicator
from .colors import ColorRole
from .fonts import TextStyle, FontScheme, PresetFontSchemes
from .appearance import AppearanceMode, AppearanceManager
from ..core.signal import Signal, Computed, Effect


class DesignTokens:
    """设计令牌 - 定义设计系统的基础值"""
    
    def __init__(self):
        # 间距系统
        self.spacing = {
            'xs': 4,
            'sm': 8,
            'md': 12,
            'lg': 16,
            'xl': 24,
            'xxl': 32,
            'xxxl': 48
        }
        
        # 圆角系统
        self.radius = {
            'none': 0,
            'sm': 4,
            'md': 6,
            'lg': 8,
            'xl': 12,
            'xxl': 16,
            'full': 9999
        }
        
        # 阴影系统
        self.shadows = {
            'none': {'offset': (0, 0), 'blur': 0, 'opacity': 0},
            'sm': {'offset': (0, 1), 'blur': 2, 'opacity': 0.1},
            'md': {'offset': (0, 2), 'blur': 4, 'opacity': 0.12},
            'lg': {'offset': (0, 4), 'blur': 8, 'opacity': 0.15},
            'xl': {'offset': (0, 8), 'blur': 16, 'opacity': 0.18},
            'xxl': {'offset': (0, 12), 'blur': 24, 'opacity': 0.2}
        }
        
        # 动画系统
        self.animations = {
            'duration': {
                'fast': 0.15,
                'normal': 0.3,
                'slow': 0.5
            },
            'easing': {
                'linear': 'linear',
                'ease_in': 'ease-in',
                'ease_out': 'ease-out',
                'ease_in_out': 'ease-in-out',
                'bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
            }
        }


class EnhancedTheme:
    """增强主题类 - 集成所有样式系统"""
    
    def __init__(
        self,
        name: str,
        color_scheme: ReactiveColorScheme,
        font_scheme: FontScheme,
        design_tokens: DesignTokens,
        appearance_mode: str = AppearanceMode.AUTO,
        custom_styles: Dict[str, Style] = None
    ):
        self.name = name
        self.color_scheme = color_scheme
        self.font_scheme = font_scheme
        self.design_tokens = design_tokens
        self.appearance_mode = appearance_mode
        self.custom_styles = custom_styles or {}
        
        # 创建预定义样式
        self._create_component_styles()
    
    def _create_component_styles(self):
        """创建组件预定义样式"""
        # 按钮样式
        self.custom_styles.update({
            'button_primary': StyleBuilder.create()
                .background(self.color('primary'))
                .corner_radius(self.radius('md'))
                .padding(self.spacing('sm'))
                .animate(self.animation_duration('fast'))
                .build(),
            
            'button_secondary': StyleBuilder.create()
                .background(self.color('surface'))
                .corner_radius(self.radius('md'))
                .padding(self.spacing('sm'))
                .shadow(**self.shadow('sm'))
                .animate(self.animation_duration('fast'))
                .build(),
            
            'card': StyleBuilder.create()
                .background(self.color('background'))
                .corner_radius(self.radius('lg'))
                .shadow(**self.shadow('md'))
                .padding(self.spacing('lg'))
                .build(),
            
            'glass_panel': StyleBuilder.create()
                .corner_radius(self.radius('xl'))
                .shadow(**self.shadow('lg'))
                .build()
        })
    
    def color(self, role: Union[ColorRole, str]) -> Signal:
        """获取响应式颜色Signal"""
        if isinstance(role, str):
            # 尝试从语义化颜色获取
            semantic_colors = ReactiveColorFactory.create_semantic_colors()
            if role in semantic_colors:
                return semantic_colors[role].signal
            
            # 尝试解析为ColorRole
            try:
                color_role = ColorRole(role)
                return self.color_scheme.color(color_role)
            except ValueError:
                # 回退到主文本颜色
                return self.color_scheme.color(ColorRole.PRIMARY_TEXT)
        else:
            return self.color_scheme.color(role)
    
    def font(self, style: Union[TextStyle, str]):
        """获取字体"""
        if isinstance(style, str):
            try:
                text_style = TextStyle(style)
                return self.font_scheme.get_font(text_style)
            except ValueError:
                return self.font_scheme.get_font(TextStyle.BODY)
        else:
            return self.font_scheme.get_font(style)
    
    def spacing(self, size: str) -> float:
        """获取间距值"""
        return self.design_tokens.spacing.get(size, self.design_tokens.spacing['md'])
    
    def radius(self, size: str) -> float:
        """获取圆角值"""
        return self.design_tokens.radius.get(size, self.design_tokens.radius['md'])
    
    def shadow(self, size: str) -> dict:
        """获取阴影定义"""
        return self.design_tokens.shadows.get(size, self.design_tokens.shadows['md'])
    
    def animation_duration(self, speed: str) -> float:
        """获取动画持续时间"""
        return self.design_tokens.animations['duration'].get(speed, 0.3)
    
    def animation_easing(self, easing: str) -> str:
        """获取动画缓动函数"""
        return self.design_tokens.animations['easing'].get(easing, 'ease-out')
    
    def get_style(self, name: str) -> Optional[Style]:
        """获取预定义样式"""
        return self.custom_styles.get(name)
    
    def set_style(self, name: str, style: Style):
        """设置自定义样式"""
        self.custom_styles[name] = style
    
    def create_responsive_style(
        self,
        condition: Signal[bool],
        true_style: Style,
        false_style: Style = None
    ) -> ComputedStyle:
        """创建响应式样式"""
        if false_style is None:
            false_style = Style()
        
        def compute_style():
            return true_style if condition.value else false_style
        
        return ComputedStyle(compute_style)


class EnhancedThemeManager:
    """增强主题管理器"""
    
    _instance: Optional["EnhancedThemeManager"] = None
    
    def __init__(self):
        if EnhancedThemeManager._instance is not None:
            raise RuntimeError("EnhancedThemeManager is a singleton. Use shared() instead.")
        
        # 设计令牌
        self.design_tokens = DesignTokens()
        
        # 当前主题
        self._current_theme: Signal[EnhancedTheme] = Signal(self._create_default_theme())
        
        # 外观管理器
        self._appearance_manager = AppearanceManager.shared()
        self._appearance_observer = self._appearance_manager.add_observer(
            self._on_appearance_changed
        )
        
        # 注册的主题
        self._registered_themes: Dict[str, EnhancedTheme] = {}
        self._register_preset_themes()
        
        print(f"🎨 EnhancedThemeManager初始化完成")
    
    @classmethod
    def shared(cls) -> "EnhancedThemeManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _create_default_theme(self) -> EnhancedTheme:
        """创建默认增强主题"""
        from .colors import PresetColorSchemes
        
        color_scheme = ReactiveColorScheme("System Enhanced")
        font_scheme = PresetFontSchemes.system()
        
        return EnhancedTheme(
            name="System Enhanced",
            color_scheme=color_scheme,
            font_scheme=font_scheme,
            design_tokens=self.design_tokens,
            appearance_mode=AppearanceMode.AUTO
        )
    
    def _register_preset_themes(self):
        """注册预设增强主题"""
        # 系统增强主题
        system_theme = self._create_default_theme()
        self._registered_themes["system_enhanced"] = system_theme
        
        # 开发者增强主题
        dev_colors = ReactiveColorScheme("Developer Enhanced")
        dev_colors.set_color(ColorRole.PRIMARY_TEXT, '#FFFFFF', '#FFFFFF')
        dev_colors.set_color(ColorRole.PRIMARY_BACKGROUND, '#1E1E1E', '#0D1117')
        dev_colors.set_color(ColorRole.ACCENT_COLOR, '#58A6FF', '#1F6FEB')
        
        dev_theme = EnhancedTheme(
            name="Developer Enhanced",
            color_scheme=dev_colors,
            font_scheme=PresetFontSchemes.developer(),
            design_tokens=self.design_tokens,
            appearance_mode=AppearanceMode.DARK
        )
        self._registered_themes["developer_enhanced"] = dev_theme
    
    def _on_appearance_changed(self, appearance: str):
        """外观变化回调"""
        current_theme = self._current_theme.value
        if current_theme.appearance_mode == AppearanceMode.AUTO:
            print(f"🌗 增强主题响应外观变化: {appearance}")
    
    @property
    def current_theme(self) -> Signal[EnhancedTheme]:
        """当前主题Signal"""
        return self._current_theme
    
    def set_theme(self, theme: EnhancedTheme):
        """设置当前主题"""
        old_theme = self._current_theme.value
        self._current_theme.value = theme
        
        # 应用外观模式
        if theme.appearance_mode != AppearanceMode.AUTO:
            self._appearance_manager.set_app_appearance(theme.appearance_mode)
        
        print(f"🎨 增强主题已切换: {old_theme.name} -> {theme.name}")
    
    def set_theme_by_name(self, name: str):
        """通过名称设置主题"""
        theme = self._registered_themes.get(name)
        if theme:
            self.set_theme(theme)
        else:
            print(f"❌ 未找到增强主题: {name}")
    
    def register_theme(self, theme: EnhancedTheme):
        """注册自定义主题"""
        key = theme.name.lower().replace(" ", "_")
        self._registered_themes[key] = theme
        print(f"📝 已注册增强主题: {theme.name}")
    
    def load_theme_from_json(self, file_path: Union[str, Path]) -> EnhancedTheme:
        """从JSON文件加载主题"""
        with open(file_path, 'r', encoding='utf-8') as f:
            theme_data = json.load(f)
        
        return self.create_theme_from_definition(theme_data)
    
    def create_theme_from_definition(self, definition: dict) -> EnhancedTheme:
        """从定义字典创建主题"""
        name = definition.get('name', 'Custom Theme')
        
        # 创建颜色方案
        color_scheme = ReactiveColorScheme(f"{name} Colors")
        
        # 加载颜色定义
        colors = definition.get('colors', {})
        for color_name, color_def in colors.items():
            try:
                role = ColorRole(color_name)
                if isinstance(color_def, dict) and 'light' in color_def and 'dark' in color_def:
                    color_scheme.set_color(role, color_def['light'], color_def['dark'])
                else:
                    color_scheme.set_static_color(role, color_def)
            except ValueError:
                print(f"⚠️ 未知颜色角色: {color_name}")
        
        # 创建字体方案
        font_scheme = PresetFontSchemes.system()  # 默认使用系统字体
        
        # 创建设计令牌
        design_tokens = DesignTokens()
        if 'spacing' in definition:
            design_tokens.spacing.update(definition['spacing'])
        if 'animations' in definition:
            design_tokens.animations.update(definition['animations'])
        
        # 外观模式
        appearance_mode = definition.get('appearance_mode', AppearanceMode.AUTO)
        
        theme = EnhancedTheme(
            name=name,
            color_scheme=color_scheme,
            font_scheme=font_scheme,
            design_tokens=design_tokens,
            appearance_mode=appearance_mode
        )
        
        print(f"🎨 从定义创建主题: {name}")
        return theme
    
    def export_theme_to_json(self, theme: EnhancedTheme, file_path: Union[str, Path]):
        """导出主题到JSON文件"""
        # 构建主题定义
        definition = {
            'name': theme.name,
            'appearance_mode': theme.appearance_mode,
            'colors': {},
            'spacing': theme.design_tokens.spacing,
            'radius': theme.design_tokens.radius,
            'shadows': theme.design_tokens.shadows,
            'animations': theme.design_tokens.animations
        }
        
        # 导出颜色（这里简化处理）
        for role in ColorRole:
            try:
                color_signal = theme.color_scheme.color(role)
                # 注意：这里只能导出当前值，无法导出响应式定义
                definition['colors'][role.value] = str(color_signal.value)
            except:
                pass
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(definition, f, indent=2, ensure_ascii=False)
        
        print(f"📄 主题已导出: {file_path}")
    
    # 便捷方法
    def color(self, role: Union[ColorRole, str]) -> Signal:
        """获取当前主题的响应式颜色"""
        return self._current_theme.value.color(role)
    
    def font(self, style: Union[TextStyle, str]):
        """获取当前主题的字体"""
        return self._current_theme.value.font(style)
    
    def style(self, name: str) -> Optional[Style]:
        """获取当前主题的预定义样式"""
        return self._current_theme.value.get_style(name)
    
    def spacing(self, size: str) -> float:
        """获取间距值"""
        return self._current_theme.value.spacing(size)
    
    def radius(self, size: str) -> float:
        """获取圆角值"""
        return self._current_theme.value.radius(size)
    
    def shadow(self, size: str) -> dict:
        """获取阴影定义"""
        return self._current_theme.value.shadow(size)
    
    def create_glass_box(
        self,
        children: List = None,
        style_name: str = 'glass_panel',
        **kwargs
    ) -> GlassBox:
        """创建主题化毛玻璃容器"""
        base_style = self.style(style_name) or Styles.glass_panel()
        
        return GlassBox(
            children=children,
            style=base_style,
            **kwargs
        )
    
    def apply_component_style(self, view, style_name: str, **overrides):
        """应用组件样式到视图"""
        base_style = self.style(style_name)
        if base_style and overrides:
            final_style = base_style.extend(**overrides)
        else:
            final_style = base_style
        
        if final_style:
            StyleApplicator.apply(view, final_style)


# 便捷函数
def get_enhanced_theme_manager() -> EnhancedThemeManager:
    """获取增强主题管理器实例"""
    return EnhancedThemeManager.shared()


def current_theme() -> EnhancedTheme:
    """获取当前增强主题"""
    return get_enhanced_theme_manager().current_theme.value


def theme_color(role: Union[ColorRole, str]) -> Signal:
    """获取主题响应式颜色"""
    return get_enhanced_theme_manager().color(role)


def theme_style(name: str) -> Optional[Style]:
    """获取主题样式"""
    return get_enhanced_theme_manager().style(name)


def theme_spacing(size: str) -> float:
    """获取主题间距"""
    return get_enhanced_theme_manager().spacing(size)