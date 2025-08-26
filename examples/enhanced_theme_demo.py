#!/usr/bin/env python3
"""macUI v2 增强主题系统演示

展示完整的增强主题化能力：
- 响应式颜色系统
- 样式组合对象
- 毛玻璃视觉效果
- 设计令牌系统
- 动态样式计算
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label, TextField
from macui.core.component import Component
from macui.core.signal import Signal, Computed

# 导入增强主题系统
from macui.theme import (
    EnhancedThemeManager, EnhancedTheme, DesignTokens,
    ReactiveColorScheme, ReactiveColorFactory,
    Style, Styles, StyleBuilder, ComputedStyle,
    GlassBox, VisualEffect, StyleApplicator,
    ColorRole, TextStyle,
    theme_color, theme_style, theme_spacing,
    current_theme, get_enhanced_theme_manager
)

from AppKit import NSColor
from Foundation import NSMakeRect


class EnhancedThemeControls(Component):
    """增强主题控制面板"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = EnhancedThemeManager.shared()
        self.hover_states = {
            'system': self.create_signal(False),
            'developer': self.create_signal(False)
        }
    
    def switch_to_system_enhanced(self):
        """切换到系统增强主题"""
        self.theme_manager.set_theme_by_name("system_enhanced")
        print("🎨 切换到系统增强主题")
    
    def switch_to_developer_enhanced(self):
        """切换到开发者增强主题"""
        self.theme_manager.set_theme_by_name("developer_enhanced")
        print("🎨 切换到开发者增强主题")
    
    def create_styled_button(self, title: str, on_click, hover_signal: Signal):
        """创建带响应式样式的按钮"""
        button = Button(title, on_click=on_click)
        
        # 创建响应式样式
        button_style = Computed(lambda: {
            'background_color': theme_color(ColorRole.ACCENT_COLOR).value if hover_signal.value 
                               else theme_color(ColorRole.CONTROL_BACKGROUND).value,
            'corner_radius': theme_spacing('sm'),
            'scale': 1.05 if hover_signal.value else 1.0,
            'animation_duration': 0.15
        })
        
        # 应用响应式样式
        def apply_dynamic_style():
            style_props = button_style.value
            StyleApplicator.apply(button, style_props)
        
        self.create_effect(apply_dynamic_style)
        
        return button
    
    def mount(self):
        """挂载增强主题控制面板"""
        # 创建响应式样式按钮
        system_button = self.create_styled_button(
            "系统增强主题", 
            self.switch_to_system_enhanced,
            self.hover_states['system']
        )
        
        developer_button = self.create_styled_button(
            "开发者增强主题",
            self.switch_to_developer_enhanced, 
            self.hover_states['developer']
        )
        
        # 主题信息标签，使用响应式颜色
        theme_info_label = Label("当前主题信息")
        
        def update_theme_info():
            current = current_theme()
            info_text = f"🎨 {current.name}\n📐 间距系统: {current.design_tokens.spacing}\n🎭 响应式颜色: 已启用"
            theme_info_label.setStringValue_(info_text)
            
            # 应用主题颜色
            primary_color = theme_color(ColorRole.PRIMARY_TEXT).value
            theme_info_label.setTextColor_(primary_color)
        
        self.create_effect(update_theme_info)
        
        # 使用设计令牌创建布局
        spacing = theme_spacing('lg')
        
        container = VStack(
            children=[
                Label("🚀 macUI增强主题系统", font=current_theme().font(TextStyle.LARGE_TITLE)),
                Label("体验响应式样式和视觉效果", font=current_theme().font(TextStyle.SUBHEADLINE)),
                HStack(
                    children=[system_button, developer_button],
                    spacing=theme_spacing('md')
                ),
                theme_info_label
            ],
            spacing=spacing,
            alignment="leading"
        )
        
        return container


class GlassEffectShowcase(Component):
    """毛玻璃效果展示"""
    
    def __init__(self):
        super().__init__()
        self.glass_visible = self.create_signal(True)
    
    def toggle_glass_effect(self):
        """切换毛玻璃效果"""
        self.glass_visible.value = not self.glass_visible.value
        print(f"🔮 毛玻璃效果: {'显示' if self.glass_visible.value else '隐藏'}")
    
    def mount(self):
        """挂载毛玻璃展示"""
        # 切换按钮
        toggle_button = Button(
            "切换毛玻璃效果",
            on_click=self.toggle_glass_effect
        )
        
        # 毛玻璃容器中的内容
        glass_content = VStack(
            children=[
                Label("✨ 毛玻璃效果", font=current_theme().font(TextStyle.HEADLINE)),
                Label("这是一个毛玻璃容器", font=current_theme().font(TextStyle.BODY)),
                Label("支持动态显示/隐藏", font=current_theme().font(TextStyle.FOOTNOTE)),
            ],
            spacing=theme_spacing('sm'),
            alignment="center"
        )
        
        # 创建毛玻璃容器
        glass_container = GlassBox(
            children=[glass_content],
            material='popover',
            corner_radius=theme_spacing('lg'),
            frame=(20, 20, 300, 150)
        )
        
        # 响应式显示/隐藏效果
        def update_glass_visibility():
            opacity = 1.0 if self.glass_visible.value else 0.3
            glass_view = glass_container.get_view()
            if glass_view:
                glass_view.setAlphaValue_(opacity)
        
        self.create_effect(update_glass_visibility)
        
        return VStack(
            children=[
                Label("🔮 视觉效果展示", font=current_theme().font(TextStyle.TITLE_2)),
                toggle_button,
                glass_container
            ],
            spacing=theme_spacing('lg'),
            alignment="leading"
        )


class StyleCombinationDemo(Component):
    """样式组合演示"""
    
    def __init__(self):
        super().__init__()
        self.style_variant = self.create_signal("default")
    
    def cycle_style_variant(self):
        """循环样式变体"""
        variants = ["default", "card", "glass", "shadow"]
        current_index = variants.index(self.style_variant.value)
        next_index = (current_index + 1) % len(variants)
        self.style_variant.value = variants[next_index]
        print(f"🎨 样式变体: {variants[next_index]}")
    
    def mount(self):
        """挂载样式组合演示"""
        # 样式切换按钮
        cycle_button = Button(
            "切换样式变体",
            on_click=self.cycle_style_variant
        )
        
        # 演示内容
        demo_content = VStack(
            children=[
                Label("📦 样式组合", font=current_theme().font(TextStyle.HEADLINE)),
                Label("这个容器会根据选择应用不同样式", font=current_theme().font(TextStyle.BODY)),
                TextField(value=self.create_signal("响应式样式输入框"), frame=(0, 0, 200, 24))
            ],
            spacing=theme_spacing('sm')
        )
        
        # 创建带动态样式的容器
        styled_container = VStack(
            children=[demo_content],
            spacing=theme_spacing('md'),
            alignment="center"
        )
        
        # 动态样式计算
        def apply_variant_style():
            variant = self.style_variant.value
            container_view = styled_container
            
            if variant == "card":
                # 卡片样式
                card_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.SECONDARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('lg'))\
                    .shadow()\
                    .padding(theme_spacing('lg'))\
                    .build()
                StyleApplicator.apply(container_view, card_style)
                
            elif variant == "glass":
                # 毛玻璃样式  
                glass_style = Styles.glass_light.extend(
                    corner_radius=theme_spacing('xl'),
                    padding=theme_spacing('lg')
                )
                StyleApplicator.apply(container_view, glass_style)
                
            elif variant == "shadow":
                # 阴影强调样式
                shadow_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.PRIMARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('md'))\
                    .shadow(offset=(0, 8), blur=16, opacity=0.2)\
                    .padding(theme_spacing('lg'))\
                    .animate(duration=0.3)\
                    .build()
                StyleApplicator.apply(container_view, shadow_style)
            
            # 更新按钮文本
            cycle_button.setTitle_(f"切换样式 (当前: {variant})")
        
        self.create_effect(apply_variant_style)
        
        return VStack(
            children=[
                Label("🎭 动态样式组合", font=current_theme().font(TextStyle.TITLE_2)),
                cycle_button,
                styled_container
            ],
            spacing=theme_spacing('xl'),
            alignment="leading"
        )


class DesignTokensDemo(Component):
    """设计令牌演示"""
    
    def __init__(self):
        super().__init__()
    
    def mount(self):
        """挂载设计令牌演示"""
        current = current_theme()
        tokens = current.design_tokens
        
        # 间距演示
        spacing_demo = VStack(
            children=[
                Label("📏 间距系统", font=current.font(TextStyle.HEADLINE)),
                HStack([
                    Label("xs", frame=(0, 0, 30, 20)),
                    Label("sm", frame=(0, 0, 30, 20)),
                    Label("md", frame=(0, 0, 30, 20)),
                    Label("lg", frame=(0, 0, 30, 20)),
                    Label("xl", frame=(0, 0, 30, 20))
                ], spacing=tokens.spacing['xs']),
                HStack([
                    Label(f"{tokens.spacing['xs']}px", frame=(0, 0, 40, 16)),
                    Label(f"{tokens.spacing['sm']}px", frame=(0, 0, 40, 16)),
                    Label(f"{tokens.spacing['md']}px", frame=(0, 0, 40, 16)),
                    Label(f"{tokens.spacing['lg']}px", frame=(0, 0, 40, 16)),
                    Label(f"{tokens.spacing['xl']}px", frame=(0, 0, 40, 16))
                ], spacing=tokens.spacing['xs'])
            ],
            spacing=tokens.spacing['sm']
        )
        
        # 圆角演示
        radius_demo = VStack(
            children=[
                Label("📐 圆角系统", font=current.font(TextStyle.HEADLINE)),
                Label(f"小: {tokens.radius['sm']}px, 中: {tokens.radius['md']}px, 大: {tokens.radius['lg']}px", 
                      font=current.font(TextStyle.BODY))
            ],
            spacing=tokens.spacing['sm']
        )
        
        # 阴影演示
        shadow_demo = VStack(
            children=[
                Label("🌟 阴影系统", font=current.font(TextStyle.HEADLINE)),
                Label("小、中、大、特大阴影效果", font=current.font(TextStyle.BODY))
            ],
            spacing=tokens.spacing['sm']
        )
        
        return VStack(
            children=[
                Label("🔧 设计令牌系统", font=current.font(TextStyle.TITLE_2)),
                spacing_demo,
                radius_demo,
                shadow_demo
            ],
            spacing=tokens.spacing['xl'],
            alignment="leading"
        )


class EnhancedThemeDemo(Component):
    """增强主题演示主组件"""
    
    def __init__(self):
        super().__init__()
        
        # 创建子组件
        self.theme_controls = EnhancedThemeControls()
        self.glass_showcase = GlassEffectShowcase()
        self.style_demo = StyleCombinationDemo()
        self.tokens_demo = DesignTokensDemo()
    
    def mount(self):
        """挂载增强主题演示"""
        # 主布局：左右分栏
        main_layout = HStack(
            children=[
                # 左侧控制和效果区
                VStack(
                    children=[
                        self.theme_controls,
                        self.glass_showcase,
                        Label("💡 增强特性:", font=current_theme().font(TextStyle.HEADLINE)),
                        Label("• 响应式颜色自动适应主题变化", font=current_theme().font(TextStyle.FOOTNOTE)),
                        Label("• 样式对象支持组合和扩展", font=current_theme().font(TextStyle.FOOTNOTE)),
                        Label("• 毛玻璃效果和图层动画", font=current_theme().font(TextStyle.FOOTNOTE)),
                        Label("• 设计令牌统一管理", font=current_theme().font(TextStyle.FOOTNOTE))
                    ],
                    spacing=theme_spacing('lg'),
                    alignment="leading"
                ),
                
                # 右侧样式和令牌演示区
                VStack(
                    children=[
                        self.style_demo,
                        self.tokens_demo
                    ],
                    spacing=theme_spacing('xl'),
                    alignment="leading"
                )
            ],
            spacing=theme_spacing('xxl')
        )
        
        return main_layout


def main():
    """主函数"""
    print("🚀 启动macUI增强主题系统演示")
    
    # 创建应用
    app = create_app("macUI增强主题演示")
    
    # 创建主组件
    enhanced_demo = EnhancedThemeDemo()
    
    # 创建窗口
    window = create_window(
        title="macUI v2 - 增强主题系统演示",
        size=(1200, 800),
        content=enhanced_demo
    )
    
    # 显示窗口
    window.show()
    
    print("🎨 增强主题演示应用已启动")
    print("💡 体验功能:")
    print("   1. 切换增强主题查看响应式效果")
    print("   2. 观察毛玻璃和动画效果")
    print("   3. 体验样式组合和设计令牌")
    print("   4. 切换macOS外观查看自动适应")
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()