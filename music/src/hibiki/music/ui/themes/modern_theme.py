#!/usr/bin/env python3
"""
🎨 现代化音乐播放器主题系统
深色优雅主题 + 动态配色 + 视觉效果
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ColorScheme:
    """颜色方案数据类"""
    
    # 背景层次
    bg_primary: str      # 主背景
    bg_secondary: str    # 次级背景
    bg_card: str         # 卡片背景
    bg_overlay: str      # 浮层背景
    
    # 文字层次
    text_primary: str    # 主要文字
    text_secondary: str  # 次要文字
    text_tertiary: str   # 辅助文字
    text_placeholder: str # 占位文字
    
    # 品牌色
    accent_primary: str   # 主品牌色
    accent_secondary: str # 次品牌色
    
    # 功能色
    success: str         # 成功
    warning: str         # 警告
    error: str           # 错误
    info: str            # 信息

@dataclass
class VisualEffects:
    """视觉效果配置"""
    
    # 阴影效果
    shadow_soft: str
    shadow_medium: str
    shadow_strong: str
    glow_accent: str
    
    # 边框和分割线
    border_subtle: str
    border_medium: str
    divider: str
    
    # 毛玻璃和透明效果
    glass_bg: str
    overlay_dark: str
    overlay_light: str

class ModernTheme:
    """现代化音乐播放器主题"""
    
    def __init__(self):
        self.current_theme = "dark"
        self._init_color_schemes()
        self._init_visual_effects()
        self._init_typography()
        self._init_component_styles()
    
    def _init_color_schemes(self):
        """初始化配色方案"""
        
        # 深色主题（主推）
        self.dark_scheme = ColorScheme(
            # 背景层次
            bg_primary='#0a0a0a',      # 主背景
            bg_secondary='#1a1a1a',    # 次级背景  
            bg_card='#242424',         # 卡片背景
            bg_overlay='#2a2a2a',      # 浮层背景
            
            # 文字层次
            text_primary='#ffffff',     # 主要文字
            text_secondary='#b3b3b3',   # 次要文字  
            text_tertiary='#666666',    # 辅助文字
            text_placeholder='#404040', # 占位文字
            
            # 品牌色
            accent_primary='#1db954',   # Spotify绿（可动态替换）
            accent_secondary='#1ed760', # 渐变色
            
            # 功能色
            success='#1db954',         # 成功
            warning='#ffa726',         # 警告
            error='#f44336',           # 错误
            info='#2196f3',           # 信息
        )
        
        # 亮色主题（备用）
        self.light_scheme = ColorScheme(
            bg_primary='#ffffff',
            bg_secondary='#f8f9fa',
            bg_card='#ffffff',
            bg_overlay='#f5f5f5',
            
            text_primary='#212529',
            text_secondary='#6c757d',
            text_tertiary='#adb5bd',
            text_placeholder='#ced4da',
            
            accent_primary='#1db954',
            accent_secondary='#1ed760',
            
            success='#28a745',
            warning='#ffc107',
            error='#dc3545',
            info='#007bff',
        )
    
    def _init_visual_effects(self):
        """初始化视觉效果"""
        
        self.dark_effects = VisualEffects(
            # 阴影和发光
            shadow_soft='rgba(0,0,0,0.1)',
            shadow_medium='rgba(0,0,0,0.2)',
            shadow_strong='rgba(0,0,0,0.4)',
            glow_accent='rgba(29,185,84,0.3)',
            
            # 边框和分割线
            border_subtle='rgba(255,255,255,0.1)',
            border_medium='rgba(255,255,255,0.2)',
            divider='rgba(255,255,255,0.05)',
            
            # 毛玻璃和透明度
            glass_bg='rgba(36,36,36,0.8)',
            overlay_dark='rgba(0,0,0,0.6)',
            overlay_light='rgba(255,255,255,0.1)',
        )
        
        self.light_effects = VisualEffects(
            shadow_soft='rgba(0,0,0,0.05)',
            shadow_medium='rgba(0,0,0,0.1)',
            shadow_strong='rgba(0,0,0,0.15)',
            glow_accent='rgba(29,185,84,0.2)',
            
            border_subtle='rgba(0,0,0,0.1)',
            border_medium='rgba(0,0,0,0.2)',
            divider='rgba(0,0,0,0.05)',
            
            glass_bg='rgba(255,255,255,0.8)',
            overlay_dark='rgba(0,0,0,0.4)',
            overlay_light='rgba(0,0,0,0.1)',
        )
    
    def _init_typography(self):
        """初始化字体系统"""
        
        self.typography = {
            # 系统字体栈
            'font_family_primary': 'SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif',
            'font_family_mono': 'SF Mono, Monaco, Menlo, monospace',
            
            # 字体大小
            'font_size_xs': '12px',
            'font_size_sm': '14px',
            'font_size_base': '16px',
            'font_size_lg': '18px',
            'font_size_xl': '20px',
            'font_size_2xl': '24px',
            'font_size_3xl': '28px',
            'font_size_4xl': '32px',
            
            # 字重
            'font_weight_light': '300',
            'font_weight_normal': '400',
            'font_weight_medium': '500',
            'font_weight_semibold': '600',
            'font_weight_bold': '700',
            
            # 行高
            'line_height_tight': '1.2',
            'line_height_normal': '1.5',
            'line_height_relaxed': '1.8',
        }
    
    def _init_component_styles(self):
        """初始化组件样式配置"""
        
        self.component_styles = {
            # 卡片样式
            'card_styles': {
                'now_playing_card': {
                    'border_radius': '20px',
                    'padding': '32px',
                    'shadow': 'shadow_strong',
                    'backdrop_blur': True,
                    'margin_bottom': '24px'
                },
                
                'playlist_card': {
                    'border_radius': '16px', 
                    'padding': '24px',
                    'shadow': 'shadow_medium',
                    'margin_bottom': '16px'
                },
                
                'lyrics_card': {
                    'border_radius': '16px',
                    'padding': '24px',
                    'shadow': 'shadow_medium',
                    'backdrop_blur': True,
                    'overflow': 'hidden'
                }
            },
            
            # 按钮样式
            'button_styles': {
                'primary_button': {
                    'border_radius': '12px',
                    'padding': '12px 24px',
                    'font_weight': 'font_weight_semibold',
                    'background': 'accent_primary',
                    'hover_scale': 1.02,
                    'active_scale': 0.98
                },
                
                'play_button': {
                    'border_radius': '50%',
                    'width': '48px',
                    'height': '48px',
                    'background': 'accent_primary',
                    'shadow': 'shadow_medium',
                    'hover_scale': 1.05,
                    'active_scale': 0.95
                },
                
                'control_button': {
                    'border_radius': '50%',
                    'width': '40px',
                    'height': '40px',
                    'background': 'transparent',
                    'hover_background': 'overlay_light',
                    'hover_scale': 1.1,
                    'active_scale': 0.9
                }
            },
            
            # 布局配置
            'layout_config': {
                'header_height': '60px',
                'control_bar_height': '80px',
                'sidebar_width': '300px',
                'main_padding': '24px',
                'card_gap': '16px'
            },
            
            # 动画配置
            'animation_config': {
                'duration_fast': 0.15,
                'duration_normal': 0.3,
                'duration_slow': 0.5,
                'easing_ease_out': 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
                'easing_ease_in': 'cubic-bezier(0.55, 0.055, 0.675, 0.19)',
                'easing_bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
            }
        }
    
    @property
    def colors(self) -> ColorScheme:
        """获取当前主题的颜色方案"""
        return self.dark_scheme if self.current_theme == "dark" else self.light_scheme
    
    @property
    def effects(self) -> VisualEffects:
        """获取当前主题的视觉效果"""
        return self.dark_effects if self.current_theme == "dark" else self.light_effects
    
    def set_theme(self, theme: str):
        """切换主题"""
        if theme in ["dark", "light"]:
            self.current_theme = theme
    
    def set_dynamic_accent(self, primary_color: str, secondary_color: Optional[str] = None):
        """设置动态品牌色（从专辑封面提取）"""
        if self.current_theme == "dark":
            self.dark_scheme.accent_primary = primary_color
            if secondary_color:
                self.dark_scheme.accent_secondary = secondary_color
        else:
            self.light_scheme.accent_primary = primary_color
            if secondary_color:
                self.light_scheme.accent_secondary = secondary_color
    
    def get_component_style(self, component_type: str, style_name: str) -> Dict[str, Any]:
        """获取组件样式配置"""
        return self.component_styles.get(component_type, {}).get(style_name, {})
    
    def get_css_variables(self) -> Dict[str, str]:
        """生成CSS变量字典（用于动态主题切换）"""
        css_vars = {}
        
        # 颜色变量
        colors = self.colors
        for attr_name, value in colors.__dict__.items():
            css_vars[f'--color-{attr_name.replace("_", "-")}'] = value
        
        # 效果变量
        effects = self.effects
        for attr_name, value in effects.__dict__.items():
            css_vars[f'--effect-{attr_name.replace("_", "-")}'] = value
        
        # 字体变量
        for key, value in self.typography.items():
            css_vars[f'--{key.replace("_", "-")}'] = value
        
        return css_vars

# 全局主题实例
modern_theme = ModernTheme()