#!/usr/bin/env python3
"""
macUI v3.0 Stretchable布局引擎展示Demo
========================================

这个demo展示了macUI v3.0的全新Stretchable布局引擎的强大功能：
- CSS Flexbox风格的布局属性
- 响应式设计能力
- 27个现代化组件的完整使用
- 链式API和直观的布局控制

运行: uv run python examples/stretchable_layout_showcase.py
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.signal import Signal, Computed
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack, ModernHStack
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from macui.components.modern_input import ModernSlider, ModernSwitch, ModernCheckbox, ModernSegmentedControl
from macui.components.modern_display import ModernImageView, ModernProgressBar, ModernTextArea
from macui.components.modern_selection import ModernPopUpButton
from macui.components.modern_time import ModernDatePicker, CalendarDatePicker
from macui.components import TableView  # Now using ModernTableView

class StretchableLayoutShowcase(Component):
    """Stretchable布局引擎功能展示 - 最小可用版本"""
    
    def __init__(self):
        super().__init__()
        
        # 第一阶段：最简单的状态
        self.app_title = Signal("🚀 macUI v3.0 - 最小测试版本")
    
    def mount(self):
        """最小可用界面 - 只有基础组件"""
        
        print("🔧 开始创建最小界面...")
        
        # 第一阶段：只有一个简单的Label
        simple_label = ModernLabel(
            text=self.app_title,
            width=400,
            height=30
        )
        
        print("📝 ModernLabel 创建完成")
        
        # 第一阶段：最简单的VStack容器
        main_container = ModernVStack(
            children=[simple_label],
            width=500,
            height=100,
            padding=20
        )
        
        print("📦 ModernVStack 创建完成")
        
        return main_container.get_view()
    
    # === 暂时注释掉复杂功能，逐步启用 ===
    
    def _create_header_section_DISABLED(self):
        """创建标题区域"""
        # 主标题
        title_label = ModernLabel(
            text=self.app_title,
            width=700,
            height=32
        ).margin(bottom=8)
        
        # 副标题
        subtitle_label = ModernLabel(
            text="展示CSS Flexbox风格布局 + 27个现代化组件的完整功能",
            width=700,
            height=20
        )
        
        # 欢迎消息（响应式）
        welcome_label = ModernLabel(
            text=self.welcome_message,
            width=700,
            height=24
        ).margin(top=8)
        
        return ModernVStack(
            children=[title_label, subtitle_label, welcome_label],
            spacing=4,
            width=700,
            height=84,
            alignment="start"
        )
    
    def _create_user_info_card_DISABLED(self):
        """创建用户信息卡片"""
        # 用户名输入
        name_field = ModernTextField(
            value=self.user_name,
            placeholder="输入你的用户名",
            width=200,
            height=28
        )
        
        # 主题切换 - 使用索引方式先简化实现
        theme_index = Signal(0)  # 对应"浅色"
        theme_popup = ModernPopUpButton(
            items=["浅色", "深色", "自动"],
            selected=theme_index,
            width=100,
            height=24
        )
        
        # 在线状态开关
        online_switch = ModernSwitch(
            value=self.is_online,
            width=40,
            height=24
        )
        
        # 通知计数stepper
        notification_label = ModernLabel(
            text="通知数量:",
            width=80,
            height=24
        )
        
        # 用户信息行
        user_row = ModernHStack(
            children=[
                ModernLabel("用户名:", width=60),
                name_field,
                ModernLabel("主题:", width=40).margin(left=20),
                theme_popup,
                ModernLabel("在线:", width=40).margin(left=20),
                online_switch
            ],
            spacing=8,
            height=32,
            alignment="center"
        )
        
        return ModernVStack(
            children=[
                ModernLabel("用户设置", width=100, height=20),
                user_row
            ],
            spacing=12,
            width=700,
            padding=16,
            justify_content="start"
        )
    
    def _create_control_panel_DISABLED(self):
        """创建控制面板"""
        # 音量滑块
        volume_slider = ModernSlider(
            value=self.volume_level,
            min_value=0.0,
            max_value=100.0,
            width=200,
            height=24
        )
        
        # 进度控制
        progress_buttons = ModernHStack(
            children=[
                ModernButton("开始任务", on_click=lambda: self.start_progress()),
                ModernButton("暂停", on_click=lambda: self.pause_progress()),
                ModernButton("重置", on_click=lambda: self.reset_progress())
            ],
            spacing=8,
            height=32
        )
        
        # 工具选择
        tool_segment = ModernSegmentedControl(
            segments=["编辑器", "浏览器", "终端", "设置"],
            selected_index=self.selected_tool,
            width=300,
            height=28
        )
        
        # 功能开关
        feature_switches = ModernHStack(
            children=[
                ModernCheckbox(title="自动保存", width=80),
                ModernCheckbox(title="语法高亮", width=80, checked=Signal(True)),
                ModernCheckbox(title="代码折叠", width=80, checked=Signal(True)),
                ModernCheckbox(title="行号显示", width=80)
            ],
            spacing=12,
            height=24
        )
        
        # 控制面板布局
        panel_content = ModernVStack(
            children=[
                # 音量控制行
                ModernHStack(
                    children=[
                        ModernLabel("音量:", width=40),
                        volume_slider,
                        ModernLabel(text=Computed(lambda: f"{int(self.volume_level.value)}%"), width=40)
                    ],
                    spacing=8,
                    height=32,
                    alignment="center"
                ),
                
                # 进度控制行
                ModernHStack(
                    children=[
                        ModernLabel("任务控制:", width=80),
                        progress_buttons
                    ],
                    spacing=8,
                    height=32,
                    alignment="center"
                ),
                
                # 工具选择行
                ModernHStack(
                    children=[
                        ModernLabel("当前工具:", width=80),
                        tool_segment
                    ],
                    spacing=8,
                    height=32,
                    alignment="center"
                ),
                
                # 功能开关行
                ModernHStack(
                    children=[
                        ModernLabel("功能选项:", width=80),
                        feature_switches
                    ],
                    spacing=8,
                    height=32,
                    alignment="center"
                )
            ],
            spacing=12,
            padding=16
        )
        
        return ModernVStack(
            children=[
                ModernLabel("控制面板"),
                panel_content
            ],
            spacing=8
        )
    
    def _create_data_section_DISABLED(self):
        """创建数据展示区域"""
        # 进度条展示
        progress_bar = ModernProgressBar(
            value=self.progress_value,
            width=300,
            height=20
        )
        
        # 进度信息
        progress_info = ModernHStack(
            children=[
                ModernLabel(text=self.progress_display, width=150),
                progress_bar
            ],
            spacing=12,
            height=24,
            alignment="center"
        )
        
        # 项目数据表格
        project_table = TableView(
            columns=[
                {"title": "项目名称", "key": "name", "width": 120},
                {"title": "状态", "key": "status", "width": 80},
                {"title": "进度", "key": "progress", "width": 60},
                {"title": "团队", "key": "team", "width": 100}
            ],
            data=self.table_data,
            frame=(0, 0, 380, 120)
        )
        
        # 笔记区域
        notes_area = ModernTextArea(
            value=self.notes,
            placeholder="在这里记录项目笔记...",
            width=280,
            height=120
        )
        
        # 日期选择器
        selected_date = Signal(None)  # 当前选择的日期
        date_picker = CalendarDatePicker(
            date_signal=selected_date,
            width=250,
            height=120
        )
        
        # 数据区域布局
        data_content = ModernHStack(
            children=[
                # 左侧：表格
                ModernVStack(
                    children=[
                        ModernLabel("项目概览"),
                        project_table
                    ],
                    spacing=8,
                    width=400
                ),
                
                # 右侧：笔记和日期
                ModernVStack(
                    children=[
                        ModernLabel("项目笔记"),
                        notes_area,
                        ModernLabel("项目日期").margin(top=8),
                        date_picker
                    ],
                    spacing=8,
                    width=300
                )
            ],
            spacing=20,
            height=280,
            alignment="start"
        )
        
        return ModernVStack(
            children=[
                ModernLabel("数据管理"),
                progress_info,
                data_content
            ],
            spacing=12
        )
    
    def _create_status_section_DISABLED(self):
        """创建底部状态栏"""
        # 状态指示器 - 简化实现，先不用颜色
        status_indicators = ModernHStack(
            children=[
                ModernLabel("●"),  # 简化状态指示器
                ModernLabel(text=self.status_text, width=400),
            ],
            spacing=8,
            height=20,
            alignment="center"
        )
        
        # 操作按钮
        action_buttons = ModernHStack(
            children=[
                ModernButton("保存项目", on_click=lambda: self.save_project()),
                ModernButton("导出数据", on_click=lambda: self.export_data()),
                ModernButton("设置", on_click=lambda: self.open_settings()),
                ModernButton("帮助", on_click=lambda: self.show_help())
            ],
            spacing=8,
            height=32
        )
        
        return ModernHStack(
            children=[status_indicators, action_buttons],
            spacing=20,
            height=40,
            padding=8,
            justify_content="space-between",
            alignment="center"
        )
    
    # === 事件处理方法 - 暂时禁用 ===
    def start_progress_DISABLED(self):
        """开始任务进度"""
        import random
        new_progress = min(100.0, self.progress_value.value + random.randint(10, 30))
        self.progress_value.value = new_progress
        print(f"📈 任务进度更新: {int(new_progress)}%")
    
    def pause_progress_DISABLED(self):
        """暂停任务"""
        print("⏸️ 任务已暂停")
    
    def reset_progress_DISABLED(self):
        """重置进度"""
        self.progress_value.value = 0.0
        print("🔄 进度已重置")
    
    def save_project_DISABLED(self):
        """保存项目"""
        print(f"💾 项目已保存 - 用户: {self.user_name.value}")
    
    def export_data_DISABLED(self):
        """导出数据"""
        print(f"📤 数据导出完成 - {len(self.table_data.value)} 个项目")
    
    def open_settings_DISABLED(self):
        """打开设置"""
        print(f"⚙️ 打开设置 - 当前主题: {self.theme_mode.value}")
    
    def show_help_DISABLED(self):
        """显示帮助"""
        print("❓ 帮助文档: 这是macUI v3.0 Stretchable布局引擎的功能展示demo")


def main():
    """主函数"""
    print("🚀 启动macUI v3.0 Stretchable布局引擎展示Demo")
    print("=" * 60)
    print("特性展示:")
    print("✨ CSS Flexbox风格布局属性")
    print("✨ 27个现代化组件完整使用")  
    print("✨ 响应式Signal绑定系统")
    print("✨ 链式API和直观布局控制")
    print("✨ 专业级UI组件集成")
    print("=" * 60)
    
    app = MacUIApp("macUI v3.0 Stretchable布局展示")
    
    # 创建展示组件
    showcase = StretchableLayoutShowcase()
    
    # 创建窗口并运行
    app.create_window(
        title="macUI v3.0 - Stretchable Layout Engine Showcase",
        size=(940, 760),
        content=showcase
    )
    
    print("\n🎯 Demo说明:")
    print("• 尝试修改用户名，观察响应式更新")
    print("• 调整音量滑块，查看实时数值显示")
    print("• 点击进度按钮，观察进度条变化")
    print("• 切换各种开关和选择器")
    print("• 在笔记区域输入内容")
    print("• 所有操作都会在终端输出日志")
    
    app.run()


if __name__ == "__main__":
    main()