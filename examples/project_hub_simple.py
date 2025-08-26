#!/usr/bin/env python3
"""MacUI Project Hub - 简化版演示

精简的项目管理应用，重点展示增强主题系统的核心功能。
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label, TextField
from macui.core.component import Component
from macui.core.signal import Signal, Computed

# 增强主题系统
from macui.theme import (
    EnhancedThemeManager,
    ColorRole, TextStyle,
    theme_color, theme_spacing,
    current_theme, get_enhanced_theme_manager
)

from AppKit import NSColor


# === 数据模型 ===
class TaskStatus(Enum):
    TODO = "📋 待办"
    IN_PROGRESS = "⚡ 进行中"  
    COMPLETED = "✅ 已完成"


@dataclass
class SimpleTask:
    title: str
    status: TaskStatus


# === 组件 ===
class ThemeSelector(Component):
    """主题选择器"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_enhanced_theme_manager()
    
    def switch_to_system(self):
        """切换到系统主题"""
        self.theme_manager.set_theme_by_name("system_enhanced")
        print("🎨 切换到系统增强主题")
    
    def switch_to_developer(self):
        """切换到开发者主题"""
        self.theme_manager.set_theme_by_name("developer_enhanced")
        print("🎨 切换到开发者增强主题")
    
    def create_purple_theme(self):
        """创建紫色自定义主题"""
        from macui.theme import ReactiveColorScheme, EnhancedTheme, DesignTokens
        from macui.theme.fonts import PresetFontSchemes
        
        # 创建紫色响应式颜色方案
        purple_colors = ReactiveColorScheme("Purple Enhanced")
        purple_colors.set_color(ColorRole.ACCENT_COLOR, "#9F39FF", "#BF5AF2")
        purple_colors.set_color(ColorRole.PRIMARY_BACKGROUND, "#FAFAFA", "#1A1A1A") 
        purple_colors.set_color(ColorRole.SECONDARY_BACKGROUND, "#F0F0F0", "#2A2A2A")
        
        purple_theme = EnhancedTheme(
            name="Purple Magic",
            color_scheme=purple_colors,
            font_scheme=PresetFontSchemes.system(),
            design_tokens=DesignTokens()
        )
        
        self.theme_manager.register_theme(purple_theme)
        self.theme_manager.set_theme(purple_theme)
        print("🎨 创建了紫色魔法主题")
    
    def mount(self):
        """挂载主题选择器"""
        # 当前主题信息
        theme_info = Label(
            f"当前主题: {current_theme().name}",
            font=current_theme().font(TextStyle.HEADLINE)
        )
        
        # 响应主题变化更新信息
        def update_theme_info():
            theme = current_theme()
            theme_info.setStringValue_(f"🎨 {theme.name}")
            
            # 应用主题颜色
            color = theme_color(ColorRole.ACCENT_COLOR).value
            theme_info.setTextColor_(color)
        
        self.create_effect(update_theme_info)
        
        # 主题切换按钮
        theme_buttons = HStack(
            children=[
                Button("系统主题", on_click=self.switch_to_system),
                Button("开发者主题", on_click=self.switch_to_developer),
                Button("紫色主题", on_click=self.create_purple_theme)
            ],
            spacing=theme_spacing('sm')
        )
        
        return VStack(
            children=[
                Label("🎨 主题系统演示", font=current_theme().font(TextStyle.LARGE_TITLE)),
                theme_info,
                theme_buttons,
                Label("切换主题查看响应式效果", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('lg'),
            alignment="center"
        )


class TaskList(Component):
    """任务列表"""
    
    def __init__(self):
        super().__init__()
        
        # 示例任务数据
        self.tasks = Signal([
            SimpleTask("实现响应式主题系统", TaskStatus.COMPLETED),
            SimpleTask("创建样式组合对象", TaskStatus.COMPLETED),
            SimpleTask("添加视觉效果支持", TaskStatus.IN_PROGRESS),
            SimpleTask("优化性能表现", TaskStatus.TODO),
            SimpleTask("编写使用文档", TaskStatus.TODO)
        ])
        
        # 新任务输入
        self.new_task_text = Signal("")
    
    def get_status_color(self, status: TaskStatus) -> NSColor:
        """获取状态颜色"""
        colors = {
            TaskStatus.TODO: NSColor.systemGrayColor(),
            TaskStatus.IN_PROGRESS: theme_color(ColorRole.ACCENT_COLOR).value,
            TaskStatus.COMPLETED: NSColor.systemGreenColor()
        }
        return colors.get(status, NSColor.systemGrayColor())
    
    def add_new_task(self):
        """添加新任务"""
        text = self.new_task_text.value.strip()
        if text:
            new_task = SimpleTask(text, TaskStatus.TODO)
            current_tasks = self.tasks.value.copy()
            current_tasks.append(new_task)
            self.tasks.value = current_tasks
            self.new_task_text.value = ""
            print(f"📋 添加新任务: {text}")
    
    def create_task_item(self, task: SimpleTask) -> VStack:
        """创建任务项"""
        # 任务标题
        task_title = Label(task.title, font=current_theme().font(TextStyle.BODY))
        
        # 状态标签
        status_label = Label(
            task.status.value, 
            font=current_theme().font(TextStyle.CAPTION_1),
            color=self.get_status_color(task.status)
        )
        
        return VStack(
            children=[
                HStack(
                    children=[task_title, status_label],
                    spacing=theme_spacing('sm')
                )
            ],
            spacing=theme_spacing('xs'),
            alignment="leading"
        )
    
    def mount(self):
        """挂载任务列表"""
        # 任务列表标题
        title = Label("📋 项目任务", font=current_theme().font(TextStyle.TITLE_2))
        
        # 新任务输入
        new_task_input = TextField(
            value=self.new_task_text,
            placeholder="输入新任务...",
            frame=(0, 0, 300, 28)
        )
        
        add_task_button = Button("添加", on_click=self.add_new_task)
        
        input_row = HStack(
            children=[new_task_input, add_task_button],
            spacing=theme_spacing('sm')
        )
        
        # 动态任务列表
        def create_task_items():
            tasks = self.tasks.value
            return [self.create_task_item(task) for task in tasks]
        
        task_items = create_task_items()
        task_list = VStack(
            children=task_items,
            spacing=theme_spacing('sm'),
            alignment="leading"
        )
        
        # 响应任务变化
        def update_task_list():
            # 重新创建任务项
            print(f"📋 任务列表更新: {len(self.tasks.value)}个任务")
        
        self.create_effect(update_task_list)
        
        return VStack(
            children=[
                title,
                input_row,
                task_list
            ],
            spacing=theme_spacing('lg'),
            alignment="leading"
        )


class ColorShowcase(Component):
    """颜色展示"""
    
    def mount(self):
        """挂载颜色展示"""
        # 创建颜色示例
        def create_color_sample(role: ColorRole, name: str) -> HStack:
            color_label = Label(name, font=current_theme().font(TextStyle.BODY))
            
            # 响应式颜色更新
            def update_color():
                color = theme_color(role).value
                color_label.setTextColor_(color)
            
            self.create_effect(update_color)
            
            return HStack(
                children=[
                    Label("●", color=theme_color(role).value),
                    color_label
                ],
                spacing=theme_spacing('xs')
            )
        
        color_samples = VStack(
            children=[
                Label("🎨 响应式颜色系统", font=current_theme().font(TextStyle.TITLE_2)),
                create_color_sample(ColorRole.PRIMARY_TEXT, "主文本颜色"),
                create_color_sample(ColorRole.ACCENT_COLOR, "强调色"),
                create_color_sample(ColorRole.SUCCESS_COLOR, "成功色"),
                create_color_sample(ColorRole.WARNING_COLOR, "警告色"),
                create_color_sample(ColorRole.ERROR_COLOR, "错误色")
            ],
            spacing=theme_spacing('sm'),
            alignment="leading"
        )
        
        return color_samples


class ProjectHubSimple(Component):
    """简化版项目管理应用"""
    
    def __init__(self):
        super().__init__()
        
        # 创建组件
        self.theme_selector = ThemeSelector()
        self.task_list = TaskList()
        self.color_showcase = ColorShowcase()
    
    def mount(self):
        """挂载应用"""
        # 主布局
        main_layout = VStack(
            children=[
                self.theme_selector,
                
                # 内容区域
                HStack(
                    children=[
                        self.task_list,
                        self.color_showcase
                    ],
                    spacing=theme_spacing('xxl')
                ),
                
                # 底部信息
                Label(
                    "💡 尝试切换主题，观察颜色和样式的响应式变化",
                    font=current_theme().font(TextStyle.FOOTNOTE)
                )
            ],
            spacing=theme_spacing('xl'),
            alignment="center"
        )
        
        return main_layout


def main():
    """主函数"""
    print("🚀 启动 MacUI Project Hub (简化版)")
    print("🎯 演示增强主题系统核心功能")
    
    # 创建应用
    app = create_app("MacUI Project Hub")
    
    # 创建主组件
    project_hub = ProjectHubSimple()
    
    # 创建窗口
    window = create_window(
        title="MacUI Project Hub - 增强主题演示",
        size=(1000, 700),
        content=project_hub
    )
    
    # 显示窗口
    window.show()
    
    print("✨ 应用已启动，体验以下功能：")
    print("   🎨 实时主题切换")
    print("   🌈 响应式颜色系统")
    print("   📐 设计令牌应用")
    print("   📋 交互式任务管理")
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()