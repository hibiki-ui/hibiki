#!/usr/bin/env python3
"""macUI v2 主题化系统演示

展示完整的主题化能力：
- Light/Dark模式自动适应
- 预设主题切换
- 动态颜色和字体
- 响应式主题更新
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label, TextField, Slider
from macui.core.component import Component
from macui.core.signal import Signal, Effect

# 导入主题系统
from macui.theme import (
    ThemeManager, Theme, PresetThemes,
    ColorRole, TextStyle, AppearanceMode,
    get_color, get_font
)

from AppKit import NSColor
from Foundation import NSMakeRect


class ThemeControls(Component):
    """主题控制面板组件"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager.shared()
        self.selected_theme = self.create_signal("system")
        
        # 监听主题变化
        self.theme_manager.add_theme_observer(self.on_theme_changed)
        
    def on_theme_changed(self, event):
        """主题变化回调"""
        print(f"🎨 主题变化事件: {event.old_theme.name if event.old_theme else 'None'} -> {event.new_theme.name}")
        print(f"   触发原因: {event.trigger}")
    
    def switch_to_system_theme(self):
        """切换到系统主题"""
        self.theme_manager.set_theme_by_name("system")
        self.selected_theme.value = "system"
    
    def switch_to_developer_theme(self):
        """切换到开发者主题"""
        self.theme_manager.set_theme_by_name("developer")
        self.selected_theme.value = "developer"
    
    def switch_to_high_contrast_theme(self):
        """切换到高对比度主题"""
        self.theme_manager.set_theme_by_name("high_contrast")
        self.selected_theme.value = "high_contrast"
    
    def mount(self):
        """挂载组件"""
        # 主题选择按钮组
        theme_buttons = HStack(
            children=[
                Button(
                    "系统主题",
                    on_click=self.switch_to_system_theme,
                    frame=(0, 0, 100, 32)
                ),
                Button(
                    "开发者主题",
                    on_click=self.switch_to_developer_theme,
                    frame=(0, 0, 100, 32)
                ),
                Button(
                    "高对比度主题",
                    on_click=self.switch_to_high_contrast_theme,
                    frame=(0, 0, 120, 32)
                )
            ],
            spacing=10.0
        )
        
        # 当前主题信息标签
        current_theme_label = Label(
            f"当前主题: {self.theme_manager.current_theme.value.name}",
            font=self.theme_manager.get_font(TextStyle.HEADLINE)
        )
        
        # 创建主题信息效果，响应主题变化
        def update_theme_info():
            current_theme = self.theme_manager.current_theme.value
            is_dark = self.theme_manager.is_dark_mode()
            mode_text = "深色模式" if is_dark else "浅色模式" 
            current_theme_label.setStringValue_(f"当前主题: {current_theme.name} ({mode_text})")
            
            # 应用主题颜色
            text_color = self.theme_manager.get_color(ColorRole.PRIMARY_TEXT)
            current_theme_label.setTextColor_(text_color)
        
        self.create_effect(update_theme_info)
        
        # 垂直布局
        container = VStack(
            children=[
                Label("🎨 macUI主题系统演示", font=self.theme_manager.get_font(TextStyle.LARGE_TITLE)),
                Label("选择不同主题查看效果变化", font=self.theme_manager.get_font(TextStyle.SUBHEADLINE)),
                theme_buttons,
                current_theme_label
            ],
            spacing=20.0,
            alignment="leading"
        )
        
        return container


class ThemeShowcase(Component):
    """主题效果展示组件"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager.shared()
        self.slider_value = self.create_signal(50.0)
        self.text_input = self.create_signal("主题化文本输入")
    
    def mount(self):
        """挂载组件"""
        # 文本样式展示
        text_samples = VStack(
            children=[
                Label("大标题样式", font=self.theme_manager.get_font(TextStyle.LARGE_TITLE)),
                Label("标题1样式", font=self.theme_manager.get_font(TextStyle.TITLE_1)),
                Label("标题2样式", font=self.theme_manager.get_font(TextStyle.TITLE_2)),
                Label("标题栏样式", font=self.theme_manager.get_font(TextStyle.HEADLINE)),
                Label("正文样式 - 这是常规的正文文本", font=self.theme_manager.get_font(TextStyle.BODY)),
                Label("强调正文样式", font=self.theme_manager.get_font(TextStyle.BODY_EMPHASIZED)),
                Label("说明文字样式", font=self.theme_manager.get_font(TextStyle.FOOTNOTE)),
            ],
            spacing=8.0,
            alignment="leading"
        )
        
        # 交互控件展示
        controls = VStack(
            children=[
                TextField(
                    value=self.text_input,
                    placeholder="输入一些文本...",
                    frame=(0, 0, 300, 24)
                ),
                HStack(
                    children=[
                        Label("滑块控件:"),
                        Slider(
                            value=self.slider_value,
                            min_value=0.0,
                            max_value=100.0,
                            frame=(0, 0, 200, 24)
                        )
                    ],
                    spacing=10.0
                ),
                Button("示例按钮", frame=(0, 0, 100, 32))
            ],
            spacing=15.0,
            alignment="leading"
        )
        
        # 颜色展示
        color_info = VStack(
            children=[
                Label("🎨 主题颜色展示:", font=self.theme_manager.get_font(TextStyle.HEADLINE)),
                Label("主要文本颜色", color=self.theme_manager.get_color(ColorRole.PRIMARY_TEXT)),
                Label("次要文本颜色", color=self.theme_manager.get_color(ColorRole.SECONDARY_TEXT)), 
                Label("强调色展示", color=self.theme_manager.get_color(ColorRole.ACCENT_COLOR)),
                Label("成功色展示", color=self.theme_manager.get_color(ColorRole.SUCCESS_COLOR)),
                Label("警告色展示", color=self.theme_manager.get_color(ColorRole.WARNING_COLOR)),
                Label("错误色展示", color=self.theme_manager.get_color(ColorRole.ERROR_COLOR)),
            ],
            spacing=8.0,
            alignment="leading"
        )
        
        # 创建响应式效果
        def update_colors():
            """更新所有颜色以响应主题变化"""
            # 这个效果会在主题变化时自动执行
            pass
        
        self.create_effect(update_colors)
        
        # 主布局
        showcase = VStack(
            children=[
                Label("📝 文本样式展示", font=self.theme_manager.get_font(TextStyle.TITLE_2)),
                text_samples,
                Label("🎛️ 交互控件展示", font=self.theme_manager.get_font(TextStyle.TITLE_2)),
                controls,
                color_info
            ],
            spacing=25.0,
            alignment="leading"
        )
        
        return showcase


class ThemeDemo(Component):
    """主题演示主组件"""
    
    def __init__(self):
        super().__init__()
        self.theme_controls = ThemeControls()
        self.theme_showcase = ThemeShowcase()
    
    def mount(self):
        """挂载组件"""
        # 主布局 - 使用HStack分为控制面板和展示区域
        main_layout = HStack(
            children=[
                # 左侧控制面板
                VStack(
                    children=[
                        self.theme_controls,
                        Label("💡 提示:", font=ThemeManager.shared().get_font(TextStyle.HEADLINE)),
                        Label("• 切换macOS系统外观查看自动适应效果", 
                              font=ThemeManager.shared().get_font(TextStyle.FOOTNOTE)),
                        Label("• 系统主题会自动跟随Light/Dark模式",
                              font=ThemeManager.shared().get_font(TextStyle.FOOTNOTE)),
                        Label("• 其他主题使用固定的外观模式",
                              font=ThemeManager.shared().get_font(TextStyle.FOOTNOTE))
                    ],
                    spacing=15.0,
                    alignment="leading"
                ),
                
                # 右侧展示区域
                self.theme_showcase
            ],
            spacing=40.0
        )
        
        return main_layout


def main():
    """主函数"""
    print("🎨 启动macUI主题系统演示")
    
    # 创建应用
    app = create_app("macUI主题演示")
    
    # 创建主组件
    theme_demo = ThemeDemo()
    
    # 创建窗口
    window = create_window(
        title="macUI v2 - 主题系统演示",
        size=(1000, 700),
        content=theme_demo
    )
    
    # 显示窗口
    window.show()
    
    print("🚀 主题演示应用已启动")
    print("💡 尝试:")
    print("   1. 点击不同主题按钮查看效果")
    print("   2. 切换macOS系统外观查看自动适应")
    print("   3. 观察控制台的主题变化日志")
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()