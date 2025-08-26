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
        """切换状态（无动画版本）"""
        old_value = self.style_animation.value
        new_value = not old_value
        print(f"🔄 BUTTON_CLICK: toggle_style_animation被调用: {old_value} -> {new_value}")
        self.style_animation.value = new_value
        print(f"🔄 BUTTON_CLICK: 状态已更新为: {self.style_animation.value}")
        print("🔄 BUTTON_CLICK: 切换完成！")
    
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
            spacing=theme_spacing('lg')  # 增大按钮间距
        )
        
        # 动画测试按钮 - 放在已知可点击的区域
        animation_test_button = Button(
            "🎬 测试动画",
            on_click=self.toggle_style_animation,
            frame=(0, 0, 100, 32)
        )
        
        # 当前主题信息 - 设置更大的宽度确保完整显示
        theme_info = Label(
            current_theme().name,
            font=current_theme().font(TextStyle.HEADLINE),
            frame=(0, 0, 400, 30)  # 设置固定宽度和高度
        )
        
        # 响应式更新 - 包含动画状态
        def update_theme_info():
            theme = current_theme()
            animated = self.style_animation.value
            animation_status = " 🚀动画中" if animated else ""
            theme_info.setStringValue_(f"🎨 {theme.name}{animation_status}")
            theme_info.setTextColor_(theme_color(ColorRole.ACCENT_COLOR).value)
            
            # 更新动画按钮标题
            animation_test_button.setTitle_("⏹️ 停止动画" if animated else "🎬 测试动画")
        
        self.create_effect(update_theme_info)
        
        return VStack(
            children=[
                Label("🎨 macUI终极主题展示", font=current_theme().font(TextStyle.LARGE_TITLE)),
                theme_info,
                theme_buttons,
                animation_test_button,  # 添加动画测试按钮
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
        """创建样式展示 - 简化版解决交互问题"""
        print("🚀 开始创建样式展示区域...")
        
        # 创建独立的按钮，不嵌套在复杂VStack中
        def create_animation_button():
            animation_button = Button(
                "切换到激活",  # 无动画版本的标题
                on_click=self.toggle_style_animation,
                frame=(0, 0, 150, 40)  # 更大的按钮尺寸
            )
            print(f"🔧 状态切换按钮已创建（无动画）: {animation_button}")
            return animation_button
        
        animation_button = create_animation_button()
        
        # 状态指示标签 - 无动画版本
        status_label = Label(
            "⭕ 状态：关闭（无动画测试）",
            font=current_theme().font(TextStyle.HEADLINE)
        )
        
        # 完全无动画的简化更新 - 只改变文本，无任何样式效果
        def update_card_style():
            animated = self.style_animation.value
            print(f"🔄 update_card_style被调用，animated={animated}")
            
            if animated:
                # 只更改文本，不应用任何颜色或样式效果
                status_label.setStringValue_("✅ 状态已切换：激活")
                animation_button.setTitle_("切换到关闭")
                print("📝 文本已更新为激活状态（无动画效果）")
            else:
                status_label.setStringValue_("⭕ 状态已切换：关闭")
                animation_button.setTitle_("切换到激活")
                print("📝 文本已更新为关闭状态（无动画效果）")
        
        self.create_effect(update_card_style)
        # 强制初始调用
        update_card_style()
        
        # 简化的布局 - 减少嵌套层级
        return VStack(
            children=[
                Label("🎨 状态切换系统（无动画）", font=current_theme().font(TextStyle.TITLE_2)),
                status_label,
                animation_button,  # 直接添加按钮，减少嵌套
                Label("💡 测试按钮是否可点击（已移除动画效果）", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('md'),
            alignment="center"  # 居中对齐让按钮更显眼
        )
    
    def create_tokens_showcase(self) -> VStack:
        """创建设计令牌展示"""
        print("📐 开始创建设计令牌展示...")
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
        
        result = VStack(
            children=[
                Label("📐 设计令牌系统", font=current_theme().font(TextStyle.TITLE_2)),
                Label("📏 间距系统:", font=current_theme().font(TextStyle.HEADLINE)),
                spacing_demo,
                Label("🔘 圆角系统:", font=current_theme().font(TextStyle.HEADLINE)),
                radius_demo,
                Label("📍 右侧布局调试: 设计令牌区域正常", font=current_theme().font(TextStyle.CAPTION_1)),
                Label("💡 统一的设计价值管理", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('md'),
            alignment="leading"
        )
        print(f"📐 设计令牌展示已创建: {result}")
        return result
    
    def create_features_list(self) -> VStack:
        """创建功能特性列表"""
        print("🚀 开始创建功能特性列表...")
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
        
        result = VStack(
            children=[
                Label("🚀 增强主题系统特性", font=current_theme().font(TextStyle.TITLE_2)),
                *feature_labels,
                Label("📍 特性列表调试: 8个特性项正常", font=current_theme().font(TextStyle.CAPTION_1))
            ],
            spacing=theme_spacing('xs'),
            alignment="leading"
        )
        print(f"🚀 功能特性列表已创建: {result}, 特性数量={len(features)}")
        return result
    
    def mount(self):
        """挂载应用"""
        # 主题选择器
        theme_selector = self.create_theme_selector()
        
        # 演示内容区域 - 添加详细坐标调试
        print("🚀 开始创建主要演示内容HStack...")
        left_section = VStack(
            children=[
                self.create_color_showcase(),
                self.create_style_showcase()
            ],
            spacing=theme_spacing('xl'),
            alignment="leading"
        )
        print(f"✅ 左侧VStack已创建: {left_section}")
        
        right_section = VStack(
            children=[
                self.create_tokens_showcase(),
                self.create_features_list()
            ],
            spacing=theme_spacing('xl'),
            alignment="leading"
        )
        print(f"✅ 右侧VStack已创建: {right_section}")
        
        demo_content = HStack(
            children=[left_section, right_section],
            spacing=theme_spacing('xxl'),
            alignment="top"  # 确保左右两侧顶部对齐
        )
        print(f"🎯 主要HStack已创建: {demo_content}, 子视图数=2")
        
        # 主布局
        main_layout = VStack(
            children=[
                theme_selector,
                demo_content,
                Label("📍 布局调试: 窗口1600x1200, HStack左右分栏", font=current_theme().font(TextStyle.CAPTION_1)),
                Label(
                    "🎯 macUI v2 - 从Demo到生产级UI框架的完美进化",
                    font=current_theme().font(TextStyle.FOOTNOTE)
                )
            ],
            spacing=theme_spacing('xl'),  # 适当减小间距，让内容更紧凑
            alignment="leading"  # 改为左对齐，让内容更自然
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
    
    # 创建窗口 - 增大尺寸确保内容完整显示
    window = create_window(
        title="macUI v2 - 终极主题展示",
        size=(1600, 1200),  # 增大窗口尺寸
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