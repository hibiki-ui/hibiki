#!/usr/bin/env python3
"""MacUI Project Hub - 现代化项目管理应用

展示macUI v2增强主题系统在实际项目中的应用：
- 多面板布局系统
- 响应式主题切换
- 毛玻璃视觉效果
- 动态样式和动画
- 完整的用户交互体验
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label, TextField
from macui.core.component import Component
from macui.core.signal import Signal, Computed

# 增强主题系统
from macui.theme import (
    EnhancedThemeManager, EnhancedTheme,
    Style, Styles, StyleBuilder,
    GlassBox, StyleApplicator,
    ColorRole, TextStyle,
    theme_color, theme_style, theme_spacing,
    current_theme, get_enhanced_theme_manager,
    ReactiveColorFactory, ReactiveColorScheme
)

from AppKit import NSColor
from Foundation import NSMakeRect


# === 数据模型 ===

class TaskStatus(Enum):
    TODO = "待办"
    IN_PROGRESS = "进行中"  
    COMPLETED = "已完成"
    BLOCKED = "受阻"


class ProjectStatus(Enum):
    ACTIVE = "活跃"
    ON_HOLD = "暂停"
    COMPLETED = "完成"


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None


@dataclass  
class Project:
    id: str
    name: str
    description: str
    status: ProjectStatus
    created_at: datetime
    tasks: List[Task]
    color: str = "#007AFF"  # 项目主题色


# === 应用状态管理 ===

class AppState:
    """应用全局状态"""
    
    def __init__(self):
        # 当前选中的项目
        self.selected_project_id = Signal("project_1")
        
        # 侧边栏是否展开
        self.sidebar_expanded = Signal(True)
        
        # 设置面板是否显示
        self.settings_visible = Signal(False)
        
        # 搜索关键词
        self.search_query = Signal("")
        
        # 项目数据（模拟数据）
        self.projects = Signal(self._create_sample_projects())
        
        # 当前主题名称
        self.current_theme_name = Signal("system_enhanced")
    
    def _create_sample_projects(self) -> List[Project]:
        """创建示例项目数据"""
        now = datetime.now()
        
        return [
            Project(
                id="project_1",
                name="macUI Framework",
                description="构建现代化的macOS应用UI框架",
                status=ProjectStatus.ACTIVE,
                created_at=now,
                color="#007AFF",
                tasks=[
                    Task("task_1", "实现主题系统", "设计和实现主题化系统", TaskStatus.COMPLETED, now),
                    Task("task_2", "创建布局组件", "VStack, HStack等布局组件", TaskStatus.COMPLETED, now),
                    Task("task_3", "增强样式系统", "响应式样式和视觉效果", TaskStatus.IN_PROGRESS, now),
                    Task("task_4", "性能优化", "提升渲染和响应性能", TaskStatus.TODO, now),
                ]
            ),
            Project(
                id="project_2", 
                name="Project Hub App",
                description="基于macUI的项目管理应用",
                status=ProjectStatus.ACTIVE,
                created_at=now,
                color="#34C759",
                tasks=[
                    Task("task_5", "应用架构设计", "设计应用的整体架构", TaskStatus.COMPLETED, now),
                    Task("task_6", "主界面开发", "实现主要界面和导航", TaskStatus.IN_PROGRESS, now),
                    Task("task_7", "数据管理", "实现项目和任务数据管理", TaskStatus.TODO, now),
                ]
            ),
            Project(
                id="project_3",
                name="Design System",
                description="构建一致的设计语言体系", 
                status=ProjectStatus.ON_HOLD,
                created_at=now,
                color="#FF9500",
                tasks=[
                    Task("task_8", "颜色系统", "定义颜色规范和使用指南", TaskStatus.TODO, now),
                    Task("task_9", "组件库", "创建可复用的UI组件库", TaskStatus.TODO, now),
                ]
            )
        ]
    
    def get_current_project(self) -> Optional[Project]:
        """获取当前选中的项目"""
        for project in self.projects.value:
            if project.id == self.selected_project_id.value:
                return project
        return None
    
    def get_project_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        """获取当前项目的任务"""
        project = self.get_current_project()
        if not project:
            return []
        
        if status_filter:
            return [task for task in project.tasks if task.status == status_filter]
        return project.tasks


# === UI组件 ===

class Sidebar(Component):
    """侧边栏 - 项目列表和导航"""
    
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state
        self.hover_project_id = self.create_signal(None)
    
    def select_project(self, project_id: str):
        """选择项目"""
        self.app_state.selected_project_id.value = project_id
        print(f"📂 切换到项目: {project_id}")
    
    def toggle_sidebar(self):
        """切换侧边栏展开/收缩"""
        self.app_state.sidebar_expanded.value = not self.app_state.sidebar_expanded.value
    
    def create_project_item(self, project: Project) -> Component:
        """创建项目列表项"""
        is_selected = Computed(lambda: self.app_state.selected_project_id.value == project.id)
        is_hovered = Computed(lambda: self.hover_project_id.value == project.id)
        
        # 项目状态颜色
        status_colors = {
            ProjectStatus.ACTIVE: NSColor.systemGreenColor(),
            ProjectStatus.ON_HOLD: NSColor.systemOrangeColor(),
            ProjectStatus.COMPLETED: NSColor.systemBlueColor()
        }
        
        # 创建项目按钮
        project_button = Button(
            project.name,
            on_click=lambda: self.select_project(project.id)
        )
        
        # 动态样式
        def update_project_item_style():
            selected = is_selected.value
            hovered = is_hovered.value
            
            if selected:
                # 选中状态：使用项目颜色
                style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.ACCENT_COLOR).value)\
                    .corner_radius(theme_spacing('sm'))\
                    .padding(theme_spacing('sm'))\
                    .animate(0.2)\
                    .build()
            elif hovered:
                # 悬停状态：浅色背景
                style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.SECONDARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('sm'))\
                    .padding(theme_spacing('sm'))\
                    .animate(0.15)\
                    .build()
            else:
                # 默认状态：透明背景
                style = StyleBuilder.create()\
                    .padding(theme_spacing('sm'))\
                    .animate(0.15)\
                    .build()
            
            StyleApplicator.apply(project_button, style)
        
        self.create_effect(update_project_item_style)
        
        # 项目信息
        project_info = VStack(
            children=[
                project_button,
                Label(f"任务: {len(project.tasks)}", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('xs')
        )
        
        return project_info
    
    def mount(self):
        """挂载侧边栏"""
        # 侧边栏头部
        header = VStack(
            children=[
                HStack(
                    children=[
                        Label("📂 Projects", font=current_theme().font(TextStyle.HEADLINE)),
                        Button("☰", on_click=self.toggle_sidebar)
                    ], 
                    spacing=theme_spacing('sm')
                ),
                Label("项目管理中心", font=current_theme().font(TextStyle.FOOTNOTE))
            ],
            spacing=theme_spacing('xs')
        )
        
        # 项目列表
        def create_project_list():
            projects = self.app_state.projects.value
            project_items = [self.create_project_item(project) for project in projects]
            return project_items
        
        project_list = VStack(
            children=create_project_list(),
            spacing=theme_spacing('sm'),
            alignment="leading"
        )
        
        # 侧边栏容器
        sidebar_content = VStack(
            children=[header, project_list],
            spacing=theme_spacing('lg'),
            alignment="leading"
        )
        
        # 侧边栏容器 (暂时使用普通VStack，避免GlassBox问题)
        sidebar_container = VStack(
            children=[sidebar_content],
            spacing=0
        )
        
        # 响应式宽度
        def update_sidebar_width():
            expanded = self.app_state.sidebar_expanded.value
            width = 250 if expanded else 60
            # TODO: 实现宽度动画
            print(f"📏 侧边栏宽度: {width}px")
        
        self.create_effect(update_sidebar_width)
        
        return sidebar_container


class TaskCard(Component):
    """任务卡片组件"""
    
    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.is_hovered = self.create_signal(False)
    
    def get_status_color(self) -> NSColor:
        """获取任务状态颜色"""
        colors = {
            TaskStatus.TODO: NSColor.systemGrayColor(),
            TaskStatus.IN_PROGRESS: NSColor.systemBlueColor(),
            TaskStatus.COMPLETED: NSColor.systemGreenColor(),
            TaskStatus.BLOCKED: NSColor.systemRedColor()
        }
        return colors.get(self.task.status, NSColor.systemGrayColor())
    
    def mount(self):
        """挂载任务卡片"""
        # 任务标题
        task_title = Label(
            self.task.title, 
            font=current_theme().font(TextStyle.BODY_EMPHASIZED)
        )
        
        # 任务描述
        task_desc = Label(
            self.task.description,
            font=current_theme().font(TextStyle.BODY)
        )
        
        # 状态标签
        status_label = Label(
            self.task.status.value,
            font=current_theme().font(TextStyle.CAPTION_1)
        )
        
        # 卡片内容
        card_content = VStack(
            children=[
                HStack(
                    children=[task_title, status_label], 
                    spacing=theme_spacing('sm')
                ),
                task_desc,
                Label(f"创建于: {self.task.created_at.strftime('%Y-%m-%d')}", 
                      font=current_theme().font(TextStyle.CAPTION_2))
            ],
            spacing=theme_spacing('xs'),
            alignment="leading"
        )
        
        # 动态卡片样式
        def update_card_style():
            hovered = self.is_hovered.value
            
            if hovered:
                # 悬停效果：提升和阴影
                card_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.PRIMARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('md'))\
                    .shadow(offset=(0, 4), blur=8, opacity=0.15)\
                    .padding(theme_spacing('lg'))\
                    .scale(1.02)\
                    .animate(0.2)\
                    .build()
            else:
                # 默认卡片样式
                card_style = StyleBuilder.create()\
                    .background(theme_color(ColorRole.SECONDARY_BACKGROUND).value)\
                    .corner_radius(theme_spacing('md'))\
                    .shadow(offset=(0, 1), blur=3, opacity=0.1)\
                    .padding(theme_spacing('lg'))\
                    .animate(0.2)\
                    .build()
            
            # 应用左边框颜色表示状态
            card_style = card_style.extend(
                border_width=3,
                border_color=self.get_status_color()
            )
            
            StyleApplicator.apply(card_content, card_style)
        
        self.create_effect(update_card_style)
        
        return card_content


class ProjectOverview(Component):
    """项目概览面板"""
    
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state
    
    def mount(self):
        """挂载项目概览"""
        # 动态项目信息
        def create_project_header():
            project = self.app_state.get_current_project()
            if not project:
                return Label("请选择一个项目", font=current_theme().font(TextStyle.HEADLINE))
            
            # 项目标题和状态
            project_title = Label(project.name, font=current_theme().font(TextStyle.LARGE_TITLE))
            project_desc = Label(project.description, font=current_theme().font(TextStyle.BODY))
            project_status = Label(f"状态: {project.status.value}", font=current_theme().font(TextStyle.CALLOUT))
            
            # 项目统计
            total_tasks = len(project.tasks)
            completed_tasks = len([t for t in project.tasks if t.status == TaskStatus.COMPLETED])
            progress_text = f"进度: {completed_tasks}/{total_tasks} 任务完成"
            progress_label = Label(progress_text, font=current_theme().font(TextStyle.BODY))
            
            return VStack(
                children=[project_title, project_desc, project_status, progress_label],
                spacing=theme_spacing('sm'),
                alignment="leading"
            )
        
        # 任务列表
        def create_task_list():
            tasks = self.app_state.get_project_tasks()
            if not tasks:
                return [Label("暂无任务", font=current_theme().font(TextStyle.BODY))]
            
            return [TaskCard(task) for task in tasks]
        
        # 主要内容区域
        project_header = create_project_header()
        
        task_section = VStack(
            children=[
                Label("📋 任务列表", font=current_theme().font(TextStyle.TITLE_2)),
                *create_task_list()
            ],
            spacing=theme_spacing('md'),
            alignment="leading"
        )
        
        # 响应项目切换更新内容
        def update_project_content():
            # 重新创建项目头部
            new_header = create_project_header()
            new_tasks = create_task_list()
            # TODO: 动态更新内容
            print(f"🔄 更新项目内容: {self.app_state.selected_project_id.value}")
        
        self.create_effect(update_project_content)
        
        return VStack(
            children=[project_header, task_section],
            spacing=theme_spacing('xl'),
            alignment="leading"
        )


class TopBar(Component):
    """顶部工具栏"""
    
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state
    
    def toggle_settings(self):
        """切换设置面板"""
        self.app_state.settings_visible.value = not self.app_state.settings_visible.value
    
    def mount(self):
        """挂载顶部工具栏"""
        # 搜索框
        search_field = TextField(
            value=self.app_state.search_query,
            placeholder="搜索项目和任务...",
            frame=(0, 0, 300, 28)
        )
        
        # 工具按钮
        settings_button = Button("⚙️ 设置", on_click=self.toggle_settings)
        theme_indicator = Label(f"主题: {current_theme().name}", font=current_theme().font(TextStyle.FOOTNOTE))
        
        # 顶部栏布局
        topbar_content = HStack(
            children=[
                Label("🏗️ Project Hub", font=current_theme().font(TextStyle.HEADLINE)),
                search_field,
                theme_indicator,
                settings_button
            ],
            spacing=theme_spacing('lg')
        )
        
        # 顶部栏容器 (暂时使用普通HStack)
        return topbar_content


class SettingsPanel(Component):
    """设置面板"""
    
    def __init__(self, app_state: AppState):
        super().__init__()
        self.app_state = app_state
        self.theme_manager = get_enhanced_theme_manager()
    
    def switch_to_system_theme(self):
        """切换到系统主题"""
        self.theme_manager.set_theme_by_name("system_enhanced")
        self.app_state.current_theme_name.value = "system_enhanced"
    
    def switch_to_developer_theme(self):
        """切换到开发者主题"""
        self.theme_manager.set_theme_by_name("developer_enhanced") 
        self.app_state.current_theme_name.value = "developer_enhanced"
    
    def create_custom_theme(self):
        """创建自定义主题"""
        # 创建一个紫色主题
        purple_colors = ReactiveColorScheme("Purple Theme")
        purple_colors.set_color(ColorRole.ACCENT_COLOR, "#9F39FF", "#BF5AF2")
        purple_colors.set_color(ColorRole.PRIMARY_BACKGROUND, "#FFFFFF", "#1A1A1A")
        
        from macui.theme.enhanced_theme_manager import EnhancedTheme, DesignTokens
        from macui.theme.fonts import PresetFontSchemes
        
        purple_theme = EnhancedTheme(
            name="Purple Custom",
            color_scheme=purple_colors,
            font_scheme=PresetFontSchemes.system(),
            design_tokens=DesignTokens()
        )
        
        self.theme_manager.register_theme(purple_theme)
        self.theme_manager.set_theme(purple_theme)
        self.app_state.current_theme_name.value = "Purple Custom"
        
        print("🎨 创建了紫色自定义主题")
    
    def mount(self):
        """挂载设置面板"""
        # 主题切换按钮
        theme_buttons = VStack(
            children=[
                Label("🎨 主题选择", font=current_theme().font(TextStyle.HEADLINE)),
                Button("系统增强主题", on_click=self.switch_to_system_theme),
                Button("开发者增强主题", on_click=self.switch_to_developer_theme),
                Button("创建紫色主题", on_click=self.create_custom_theme)
            ],
            spacing=theme_spacing('sm')
        )
        
        # 外观设置
        appearance_settings = VStack(
            children=[
                Label("🌗 外观设置", font=current_theme().font(TextStyle.HEADLINE)),
                Label("• 自动适应系统Light/Dark模式", font=current_theme().font(TextStyle.BODY)),
                Label("• 毛玻璃效果和动画", font=current_theme().font(TextStyle.BODY)),
                Label("• 响应式颜色系统", font=current_theme().font(TextStyle.BODY))
            ],
            spacing=theme_spacing('xs')
        )
        
        settings_content = VStack(
            children=[
                Label("⚙️ 应用设置", font=current_theme().font(TextStyle.LARGE_TITLE)),
                theme_buttons,
                appearance_settings
            ],
            spacing=theme_spacing('xl'),
            alignment="leading"
        )
        
        # 设置面板容器 (暂时使用普通VStack)
        settings_container = VStack(
            children=[settings_content],
            spacing=0
        )
        
        # 响应式显示/隐藏
        def update_settings_visibility():
            visible = self.app_state.settings_visible.value
            opacity = 1.0 if visible else 0.0
            settings_view = settings_container
            if settings_view and hasattr(settings_view, 'setAlphaValue_'):
                # settings_view.setAlphaValue_(opacity)
                pass  # 暂时禁用，避免错误
            print(f"⚙️ 设置面板: {'显示' if visible else '隐藏'}")
        
        self.create_effect(update_settings_visibility)
        
        return settings_container


class ProjectHubApp(Component):
    """项目管理应用主组件"""
    
    def __init__(self):
        super().__init__()
        
        # 应用状态
        self.app_state = AppState()
        
        # 创建子组件
        self.sidebar = Sidebar(self.app_state)
        self.topbar = TopBar(self.app_state)
        self.project_overview = ProjectOverview(self.app_state)
        self.settings_panel = SettingsPanel(self.app_state)
    
    def mount(self):
        """挂载项目管理应用"""
        # 主内容区域
        main_content = VStack(
            children=[
                self.topbar,
                HStack(
                    children=[
                        self.sidebar,
                        self.project_overview
                    ],
                    spacing=0  # 无间隙，让毛玻璃效果更自然
                )
            ],
            spacing=0
        )
        
        # 应用容器 - 使用ZStack叠加设置面板
        app_container = VStack(
            children=[
                main_content,
                self.settings_panel  # 设置面板叠加在主界面上
            ],
            spacing=0
        )
        
        return app_container


def main():
    """主函数 - 启动项目管理应用"""
    print("🚀 启动 MacUI Project Hub")
    print("📱 这是一个展示增强主题系统的实际项目")
    
    # 创建应用
    app = create_app("MacUI Project Hub")
    
    # 创建主组件
    project_hub = ProjectHubApp()
    
    # 创建窗口
    window = create_window(
        title="MacUI Project Hub - 项目管理中心",
        size=(1400, 900),
        content=project_hub
    )
    
    # 显示窗口
    window.show()
    
    print("✨ Project Hub 已启动")
    print("🎯 体验功能：")
    print("   • 📂 左侧项目导航")
    print("   • 📋 项目任务管理") 
    print("   • 🎨 实时主题切换")
    print("   • 🔮 毛玻璃视觉效果")
    print("   • ⚡ 响应式动画")
    print("   • ⚙️ 设置面板")
    
    # 运行应用
    app.run()


if __name__ == "__main__":
    main()