#!/usr/bin/env python3
"""
🎨 Hibiki UI v4 Complete Feature Showcase
完整可运行的v4框架功能演示应用

重点演示：
✅ 响应式系统完整功能
✅ 布局系统 (Flexbox演示)
✅ 组件系统 (Label/Button/Container)
✅ 事件处理系统
✅ 样式系统基础功能
"""

from hibiki.ui import (
    # 核心系统
    Signal, Computed, Effect, create_signal, create_computed, create_effect,
    Component, UIComponent, Container,
    ComponentStyle, px, percent, auto,
    ManagerFactory,
    animate, fade_in, fade_out, bounce,
    
    # 组件系统
    Label, Button, TextField, Slider, Switch,
    TextArea, Checkbox, RadioButton,
    ProgressBar, ImageView, PopUpButton, ComboBox,
    CustomView, DrawingUtils,
    
    # 主题系统
    get_theme_manager, get_current_theme, set_theme, get_color, get_font,
    AppearanceMode, is_dark_mode
)

import math
import random

# PyObjC导入
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

# ================================
# 🎯 应用数据模型
# ================================

class ShowcaseData:
    """应用数据和状态管理"""
    
    def __init__(self):
        # 响应式状态
        self.counter = Signal(0)
        self.user_name = Signal("Hibiki UI v4 User")
        self.theme = Signal("Light")
        
        # 新组件状态
        self.slider_value = Signal(50.0)
        self.volume = Signal(75.0)
        self.brightness = Signal(60.0)
        self.dark_mode = Signal(False)
        self.notifications = Signal(True)
        self.auto_save = Signal(True)
        self.text_input = Signal("输入一些文本...")
        
        # 计算属性
        self.double_counter = Computed(lambda: self.counter.value * 2)
        self.progress_percent = Computed(lambda: min(self.counter.value * 10, 100))
        self.user_greeting = Computed(lambda: f"Hello, {self.user_name.value}!")
        
        # 副作用
        Effect(lambda: print(f"📊 Counter changed: {self.counter.value}"))
        Effect(lambda: print(f"🎚️ Slider value: {self.slider_value.value}"))

# ================================
# 🎨 应用程序主类
# ================================

class ShowcaseApp:
    """Hibiki UI v4 完整功能演示应用"""
    
    def __init__(self):
        self.data = ShowcaseData()
        self.app_manager = ManagerFactory.get_app_manager()
        self.window = None
        self.main_container = None
        
    def create_counter_section(self):
        """创建计数器演示区域"""
        counter_label = Label(
            lambda: f"Count: {self.data.counter.value} (Double: {self.data.double_counter.value})",
            style=ComponentStyle(
                margin_bottom=px(10)
            ),
            font_size=16,
            font_weight="bold",
            text_align="center"
        )
        
        increment_btn = Button(
            "Increment (+1)",
            style=ComponentStyle(
                width=px(120),
                height=px(32),
                margin_right=px(10)
            ),
            on_click=lambda: setattr(self.data.counter, 'value', self.data.counter.value + 1)
        )
        
        decrement_btn = Button(
            "Decrement (-1)",
            style=ComponentStyle(
                width=px(120),
                height=px(32)
            ),
            on_click=lambda: setattr(self.data.counter, 'value', max(0, self.data.counter.value - 1))
        )
        
        button_container = Container(
            children=[increment_btn, decrement_btn],
            style=ComponentStyle(
                display="flex",
                flex_direction="row",
                justify_content="center",
                gap=px(10)
            )
        )
        
        return Container(
            children=[counter_label, button_container],
            style=ComponentStyle(
                padding=px(20),
                border="1px solid #ccc",
                border_radius=px(8),
                margin_bottom=px(20),
                background_color="#f9f9f9"
            )
        )
    
    def create_input_section(self):
        """创建输入组件演示区域"""
        
        # 文本输入
        text_field = TextField(
            self.data.text_input,
            placeholder="Enter some text...",
            style=ComponentStyle(
                width=px(300),
                height=px(32),
                margin_bottom=px(10)
            )
        )
        
        text_display = Label(
            lambda: f"You typed: {self.data.text_input.value}",
            style=ComponentStyle(
                margin_bottom=px(15)
            ),
            font_size=14,
            color="#666"
        )
        
        # 滑动条
        volume_slider = Slider(
            self.data.volume,
            min_value=0,
            max_value=100,
            style=ComponentStyle(
                width=px(250),
                margin_bottom=px(5)
            )
        )
        
        volume_label = Label(
            lambda: f"Volume: {int(self.data.volume.value)}%",
            style=ComponentStyle(
                margin_bottom=px(10)
            ),
            font_size=14
        )
        
        # 开关和复选框
        dark_mode_switch = Switch(
            self.data.dark_mode,
            label="Dark Mode",
            style=ComponentStyle(margin_bottom=px(10))
        )
        
        notifications_checkbox = Checkbox(
            self.data.notifications,
            label="Enable Notifications",
            style=ComponentStyle(margin_bottom=px(10))
        )
        
        return Container(
            children=[
                Label("Input Controls", 
                      style=ComponentStyle(margin_bottom=px(15)),
                      font_size=18, font_weight="bold"),
                text_field,
                text_display,
                volume_label,
                volume_slider,
                dark_mode_switch,
                notifications_checkbox
            ],
            style=ComponentStyle(
                padding=px(20),
                border="1px solid #ccc",
                border_radius=px(8),
                margin_bottom=px(20),
                background_color="#f9f9f9"
            )
        )
    
    def create_progress_section(self):
        """创建进度指示器演示"""
        progress_bar = ProgressBar(
            lambda: self.data.progress_percent.value,
            style=ComponentStyle(
                width=px(300),
                height=px(20),
                margin_bottom=px(10)
            )
        )
        
        progress_label = Label(
            lambda: f"Progress: {int(self.data.progress_percent.value)}%",
            font_size=14,
            text_align="center"
        )
        
        return Container(
            children=[
                Label("Progress Indicator", 
                      style=ComponentStyle(margin_bottom=px(15)),
                      font_size=18, font_weight="bold"),
                progress_bar,
                progress_label
            ],
            style=ComponentStyle(
                padding=px(20),
                border="1px solid #ccc",
                border_radius=px(8),
                margin_bottom=px(20),
                background_color="#f9f9f9"
            )
        )
    
    def create_layout_demo(self):
        """创建布局演示"""
        
        # 创建三个示例卡片
        cards = []
        for i in range(3):
            card = Container(
                children=[
                    Label(f"Card {i+1}", 
                          style=ComponentStyle(margin_bottom=px(5)),
                          font_size=16, font_weight="bold"),
                    Label(f"This is card content {i+1}", 
                          font_size=12, color="#666")
                ],
                style=ComponentStyle(
                    padding=px(15),
                    border="1px solid #ddd",
                    border_radius=px(6),
                    background_color="white",
                    flex="1",
                    margin_right=px(10) if i < 2 else px(0)
                )
            )
            cards.append(card)
        
        cards_container = Container(
            children=cards,
            style=ComponentStyle(
                display="flex",
                flex_direction="row",
                gap=px(10)
            )
        )
        
        return Container(
            children=[
                Label("Layout Demo (Flexbox)", 
                      style=ComponentStyle(margin_bottom=px(15)),
                      font_size=18, font_weight="bold"),
                cards_container
            ],
            style=ComponentStyle(
                padding=px(20),
                border="1px solid #ccc",
                border_radius=px(8),
                margin_bottom=px(20),
                background_color="#f9f9f9"
            )
        )
    
    def create_main_container(self):
        """创建主容器"""
        header = Label(
            "🎨 Hibiki UI v4.0 Complete Showcase",
            style=ComponentStyle(
                margin_bottom=px(30)
            ),
            font_size=24,
            font_weight="bold",
            text_align="center",
            color="#333"
        )
        
        subtitle = Label(
            lambda: f"Welcome, {self.data.user_name.value}! Explore reactive UI components below.",
            style=ComponentStyle(
                margin_bottom=px(30)
            ),
            font_size=14,
            text_align="center",
            color="#666"
        )
        
        # 创建各个演示区域
        counter_section = self.create_counter_section()
        input_section = self.create_input_section()
        progress_section = self.create_progress_section()
        layout_demo = self.create_layout_demo()
        
        # 主容器
        self.main_container = Container(
            children=[
                header,
                subtitle,
                counter_section,
                input_section,
                progress_section,
                layout_demo
            ],
            style=ComponentStyle(
                padding=px(30),
                display="flex",
                flex_direction="column",
                background_color="#ffffff"
            )
        )
        
        return self.main_container
    
    def run(self):
        """运行应用程序"""
        try:
            print("🚀 Starting Hibiki UI v4 Complete Showcase...")
            
            # 创建窗口
            self.window = self.app_manager.create_window(
                "Hibiki UI v4 Complete Showcase",
                width=800,
                height=900
            )
            
            # 创建并设置内容
            main_container = self.create_main_container()
            self.window.set_content(main_container)
            
            print("✅ Showcase application ready!")
            print("🎯 Features demonstrated:")
            print("   • Reactive state management (Signal, Computed, Effect)")
            print("   • Complete component library")
            print("   • Flexible layout system")
            print("   • Event handling")
            print("   • Professional styling")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            print(f"❌ Error running showcase: {e}")
            import traceback
            traceback.print_exc()

# ================================
# 🚀 程序入口
# ================================

if __name__ == "__main__":
    app = ShowcaseApp()
    app.run()