#!/usr/bin/env python3
"""macUI Ultimate Theme Showcase - 终极主题展示

展示macUI v2增强主题系统的所有功能：
✨ 响应式颜色系统
🎨 样式组合对象  
🔮 视觉效果支持
📐 设计令牌系统
📄 JSON主题导入/导出
⚡ 动态样式计算
🌗 Light/Dark模式适配
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label, TextField
from macui.core.component import Component
from macui.core.signal import Signal, Computed

from macui.theme import (
    EnhancedThemeManager, EnhancedTheme,
    Style, Styles, StyleBuilder, StyleApplicator,
    ReactiveColorScheme, ReactiveColorFactory,
    ColorRole, TextStyle,
    theme_color, theme_style, theme_spacing, current_theme
)

from AppKit import NSColor


class UltimateThemeShowcase(Component):
    """终极主题展示应用"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = EnhancedThemeManager.shared()
        
        # 状态
        self.active_demo = Signal("colors")  # colors, styles, effects, tokens
        self.hover_states = {
            "colors": self.create_signal(False),
            "styles": self.create_signal(False), 
            "effects": self.create_signal(False),
            "tokens": self.create_signal(False)
        }
        
        # 样式演示状态
        self.style_animation = self.create_signal(False)
        self.card_elevated = self.create_signal(False)
    
    def switch_theme(self, theme_name: str):
        """切换主题"""
        if theme_name == "ocean":
            self.load_ocean_theme()
        elif theme_name == "sunset":
            self.load_sunset_theme()
        else:
            self.theme_manager.set_theme_by_name(theme_name)
        
        print(f"🎨 主题切换: {theme_name}")
    
    def load_ocean_theme(self):
        """加载海洋主题"""
        try:
            ocean_path = Path(__file__).parent / "themes" / "ocean_theme.json"
            if ocean_path.exists():
                with open(ocean_path, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                
                # 创建海洋主题
                ocean_colors = ReactiveColorScheme("Ocean Breeze")
                colors = theme_data.get('colors', {})
                
                for role_name, color_def in colors.items():
                    try:
                        if role_name == 'primary':
                            role = ColorRole.ACCENT_COLOR
                        elif role_name == 'background':
                            role = ColorRole.PRIMARY_BACKGROUND
                        elif role_name == 'surface':
                            role = ColorRole.SECONDARY_BACKGROUND
                        else:
                            continue
                        
                        if isinstance(color_def, dict):
                            ocean_colors.set_color(role, color_def['light'], color_def['dark'])
                        else:
                            ocean_colors.set_static_color(role, color_def)
                    except:
                        continue
                
                from macui.theme.enhanced_theme_manager import DesignTokens
                from macui.theme.fonts import PresetFontSchemes
                
                ocean_theme = EnhancedTheme(
                    name="Ocean Breeze",
                    color_scheme=ocean_colors,
                    font_scheme=PresetFontSchemes.system(),
                    design_tokens=DesignTokens()
                )
                
                self.theme_manager.register_theme(ocean_theme)
                self.theme_manager.set_theme(ocean_theme)
                print("🌊 海洋主题加载成功")
            else:
                print("❌ 海洋主题文件不存在")
        except Exception as e:
            print(f"❌ 加载海洋主题失败: {e}")
    
    def load_sunset_theme(self):
        """加载日落主题"""
        try:
            sunset_path = Path(__file__).parent / "themes" / "sunset_theme.json"
            if sunset_path.exists():
                # 简化版：创建日落色调主题
                sunset_colors = ReactiveColorScheme("Sunset Glow")
                sunset_colors.set_color(ColorRole.ACCENT_COLOR, "#FF6B35", "#FF8A65")
                sunset_colors.set_color(ColorRole.PRIMARY_BACKGROUND, "#FFF8F5", "#1A0F0A")
                sunset_colors.set_color(ColorRole.SECONDARY_BACKGROUND, "#FFEDE0", "#2D1B13")
                
                from macui.theme.enhanced_theme_manager import EnhancedTheme, DesignTokens
                from macui.theme.fonts import PresetFontSchemes
                
                sunset_theme = EnhancedTheme(
                    name="Sunset Glow",
                    color_scheme=sunset_colors,
                    font_scheme=PresetFontSchemes.system(),
                    design_tokens=DesignTokens()
                )
                
                self.theme_manager.register_theme(sunset_theme)
                self.theme_manager.set_theme(sunset_theme)
                print("🌅 日落主题加载成功")
            else:
                print("❌ 日落主题文件不存在")
        except Exception as e:
            print(f"❌ 加载日落主题失败: {e}")
    
    def toggle_style_animation(self):
        """切换样式动画"""
        self.style_animation.value = not self.style_animation.value
    
    def toggle_card_elevation(self):
        """切换卡片提升效果"""
        self.card_elevated.value = not self.card_elevated.value
    
    def create_theme_selector(self) -> VStack:
        """创建主题选择器"""
        theme_buttons = HStack(
            children=[
                Button("系统增强", on_click=lambda: self.switch_theme("system_enhanced")),
                Button("开发者", on_click=lambda: self.switch_theme("developer_enhanced")),
                Button("海洋风", on_click=lambda: self.switch_theme("ocean")),
                Button("日落橙", on_click=lambda: self.switch_theme("sunset"))
            ],
            spacing=theme_spacing('sm')
        )
        
        # 当前主题信息
        theme_info = Label(
            current_theme().name,
            font=current_theme().font(TextStyle.HEADLINE)
        )
        
        # 响应式更新
        def update_theme_info():
            theme = current_theme()
            theme_info.setStringValue_(f"🎨 {theme.name}")
            theme_info.setTextColor_(theme_color(ColorRole.ACCENT_COLOR).value)
        
        self.create_effect(update_theme_info)
        
        return VStack(
            children=[
                Label("🎨 macUI终极主题展示", font=current_theme().font(TextStyle.LARGE_TITLE)),
                theme_info,
                theme_buttons,
                Label("选择主题查看响应式效果", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('md'),
            alignment="center"
        )
    
    def create_color_showcase(self) -> VStack:
        """创建颜色展示"""
        def create_color_item(role: ColorRole, name: str) -> HStack:
            color_dot = Label("●")
            color_label = Label(name, font=current_theme().font(TextStyle.BODY))
            
            def update_color():
                color = theme_color(role).value
                color_dot.setTextColor_(color)
                color_label.setTextColor_(color)
            
            self.create_effect(update_color)
            
            return HStack(
                children=[color_dot, color_label],
                spacing=theme_spacing('xs')
            )
        
        color_items = VStack(
            children=[
                Label("🌈 响应式颜色系统", font=current_theme().font(TextStyle.TITLE_2)),
                create_color_item(ColorRole.ACCENT_COLOR, "强调色 - 跟随主题变化"),
                create_color_item(ColorRole.PRIMARY_TEXT, "主文本 - 自动适应明暗"),
                create_color_item(ColorRole.SUCCESS_COLOR, "成功色 - 系统语义化"),
                create_color_item(ColorRole.WARNING_COLOR, "警告色 - 动态适配"),
                create_color_item(ColorRole.ERROR_COLOR, "错误色 - 响应式更新"),
                Label("💡 切换主题观察颜色实时变化", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('sm'),
            alignment="leading"
        )
        
        return color_items
    
    def create_style_showcase(self) -> VStack:
        """创建样式展示"""
        # 动画按钮
        animation_button = Button(
            "切换动画效果",
            on_click=self.toggle_style_animation
        )
        
        # 响应式样式演示卡片
        demo_card_content = VStack(
            children=[
                Label("🎭 动态样式卡片", font=current_theme().font(TextStyle.HEADLINE)),
                Label("这个卡片会根据状态动态改变样式", font=current_theme().font(TextStyle.BODY)),
                animation_button
            ],
            spacing=theme_spacing('sm'),
            alignment="center"
        )
        
        # 应用动态样式到卡片
        def update_card_style():
            animated = self.style_animation.value
            
            if animated:
                # 动画状态：提升+阴影+缩放
                card_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.SECONDARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('lg'))\
                    .shadow(offset=(0, 8), blur=16, opacity=0.2)\
                    .padding(theme_spacing('xl'))\
                    .scale(1.05)\
                    .animate(0.3)\
                    .build()
            else:
                # 默认状态
                card_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.PRIMARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('md'))\
                    .shadow(offset=(0, 2), blur=4, opacity=0.1)\
                    .padding(theme_spacing('lg'))\
                    .animate(0.3)\
                    .build()
            
            StyleApplicator.apply(demo_card_content, card_style)
            
            # 更新按钮文字
            animation_button.setTitle_("停止动画" if animated else "开始动画")
        
        self.create_effect(update_card_style)
        
        return VStack(
            children=[
                Label("🎨 样式组合系统", font=current_theme().font(TextStyle.TITLE_2)),
                demo_card_content,
                Label("💡 支持样式扩展、合并和响应式计算", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('lg'),
            alignment="center"
        )
    
    def create_tokens_showcase(self) -> VStack:
        """创建设计令牌展示"""
        tokens = current_theme().design_tokens
        
        spacing_demo = HStack(
            children=[
                Label(f"XS({tokens.spacing['xs']}px)", font=current_theme().font(TextStyle.CAPTION_1)),
                Label(f"SM({tokens.spacing['sm']}px)", font=current_theme().font(TextStyle.CAPTION_1)),
                Label(f"MD({tokens.spacing['md']}px)", font=current_theme().font(TextStyle.CAPTION_1)),
                Label(f"LG({tokens.spacing['lg']}px)", font=current_theme().font(TextStyle.CAPTION_1)),
                Label(f"XL({tokens.spacing['xl']}px)", font=current_theme().font(TextStyle.CAPTION_1))
            ],
            spacing=tokens.spacing['xs']
        )
        
        radius_demo = Label(
            f"圆角系统: SM({tokens.radius['sm']}px) MD({tokens.radius['md']}px) LG({tokens.radius['lg']}px)",
            font=current_theme().font(TextStyle.BODY)
        )
        
        return VStack(
            children=[
                Label("📐 设计令牌系统", font=current_theme().font(TextStyle.TITLE_2)),
                Label("📏 间距系统:", font=current_theme().font(TextStyle.HEADLINE)),
                spacing_demo,
                Label("🔘 圆角系统:", font=current_theme().font(TextStyle.HEADLINE)),
                radius_demo,
                Label("💡 统一的设计价值管理", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('md'),
            alignment="leading"
        )
    
    def create_features_list(self) -> VStack:
        """创建功能特性列表"""
        features = [
            "✅ 响应式颜色 - 实时跟随主题变化",
            "✅ 样式组合 - 可扩展、可合并的样式对象", 
            "✅ 视觉效果 - 毛玻璃、阴影、动画支持",
            "✅ 设计令牌 - 统一的设计价值系统",
            "✅ JSON主题 - 支持主题导入和导出",
            "✅ 自动适配 - Light/Dark模式无缝切换",
            "✅ 类型安全 - 完整的TypeScript风格接口",
            "✅ 高性能 - 基于Signal的精确更新"
        ]
        
        feature_labels = [
            Label(feature, font=current_theme().font(TextStyle.BODY))
            for feature in features
        ]
        
        return VStack(
            children=[
                Label("🚀 增强主题系统特性", font=current_theme().font(TextStyle.TITLE_2)),
                *feature_labels
            ],
            spacing=theme_spacing('xs'),
            alignment="leading"
        )
    
    def mount(self):
        """挂载应用"""
        # 主题选择器
        theme_selector = self.create_theme_selector()
        
        # 演示内容区域
        demo_content = HStack(
            children=[
                # 左侧：颜色和样式
                VStack(
                    children=[
                        self.create_color_showcase(),
                        self.create_style_showcase()
                    ],
                    spacing=theme_spacing('xl'),
                    alignment="leading"
                ),
                
                # 右侧：令牌和特性
                VStack(
                    children=[
                        self.create_tokens_showcase(),
                        self.create_features_list()
                    ],
                    spacing=theme_spacing('xl'),
                    alignment="leading"
                )
            ],
            spacing=theme_spacing('xxl')
        )
        
        # 主布局
        main_layout = VStack(
            children=[
                theme_selector,
                demo_content,
                Label(
                    "🎯 macUI v2 - 从Demo到生产级UI框架的完美进化",
                    font=current_theme().font(TextStyle.FOOTNOTE)
                )
            ],
            spacing=theme_spacing('xxl'),
            alignment="center"
        )
        
        return main_layout


def main():
    """主函数"""
    print("🚀 启动 macUI 终极主题展示")
    print("=" * 60)
    print("🎨 功能亮点:")
    print("   • 响应式颜色系统")
    print("   • 样式组合对象")
    print("   • JSON主题导入")
    print("   • 设计令牌管理")
    print("   • 视觉效果支持")
    print("   • 动态样式计算")
    print("=" * 60)
    
    # 创建应用
    app = create_app("macUI Ultimate Theme Showcase")
    
    # 创建主组件
    showcase = UltimateThemeShowcase()
    
    # 创建窗口
    window = create_window(
        title="macUI v2 - 终极主题展示",
        size=(1400, 1000),
        content=showcase
    )
    
    # 显示窗口
    window.show()
    
    print("✨ 终极主题展示已启动!")
    print("🎯 尽情体验增强主题系统的强大功能!")
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()