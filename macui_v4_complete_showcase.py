#!/usr/bin/env python3
"""
🎨 macUI v4 Complete Feature Showcase
完整可运行的v4框架功能演示应用

重点演示：
✅ 响应式系统完整功能
✅ 布局系统 (Flexbox演示)
✅ 组件系统 (Label/Button/Container)
✅ 事件处理系统
✅ 样式系统基础功能
"""

import sys
import os

# 添加macui_v4路径
sys.path.append(os.path.join(os.path.dirname(__file__), "macui_v4"))

# 导入v4核心
from core.managers import ManagerFactory
from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, JustifyContent, px, percent
from core.reactive import Signal, Computed, Effect
from components.basic import Label, Button, TextField, Slider, Switch
from core.component import Container

# 导入表单系统
from components.forms import (
    Form, FormField, FormBuilder, FormTemplates,
    RequiredValidator, EmailValidator, LengthValidator, NumberValidator, CustomValidator
)

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
        self.user_name = Signal("macUI v4 User")
        self.theme = Signal("Light")
        
        # 新组件状态
        self.slider_value = Signal(50.0)
        self.volume = Signal(75.0)
        self.brightness = Signal(60.0)
        self.dark_mode = Signal(False)
        self.notifications = Signal(True)
        self.auto_save = Signal(True)
        self.text_input = Signal("输入一些文本...")
        
        # 表单演示状态
        self.form_data = Signal({
            "name": "",
            "email": "",
            "age": 25,
            "subscribe": False,
            "bio": "",
            "rating": 5
        })
        self.form_submit_count = Signal(0)
        self.last_form_data = Signal({})
        
        # 计算属性
        self.counter_doubled = Computed(lambda: self.counter.value * 2)
        self.counter_squared = Computed(lambda: self.counter.value ** 2)
        self.greeting_message = Computed(
            lambda: f"Hello {self.user_name.value}! Counter: {self.counter.value}"
        )
        
        # 新组件的计算属性
        self.slider_percentage = Computed(lambda: f"{self.slider_value.value:.0f}%")
        self.volume_display = Computed(lambda: f"音量: {self.volume.value:.0f}%")
        self.brightness_display = Computed(lambda: f"亮度: {self.brightness.value:.0f}%")
        self.settings_summary = Computed(
            lambda: f"深色模式: {'开' if self.dark_mode.value else '关'} | "
                   f"通知: {'开' if self.notifications.value else '关'} | "
                   f"自动保存: {'开' if self.auto_save.value else '关'}"
        )
        
        # 表单相关的计算属性
        self.form_status = Computed(
            lambda: f"表单提交次数: {self.form_submit_count.value} | "
                   f"当前年龄: {self.form_data.value.get('age', 0)} | "
                   f"订阅状态: {'是' if self.form_data.value.get('subscribe', False) else '否'}"
        )
        self.form_summary = Computed(
            lambda: f"📝 姓名: {self.form_data.value.get('name', '未填写')} | "
                   f"📧 邮箱: {self.form_data.value.get('email', '未填写')}"
        )
        
        # 统计信息
        self.total_clicks = Signal(0)
        self.app_uptime = Signal(0)
        
        print("📊 ShowcaseData初始化完成")

# 全局数据实例
showcase_data = ShowcaseData()

# ================================
# 🎨 核心功能演示组件
# ================================

class ReactiveCounterDemo:
    """响应式计数器演示"""
    
    def __init__(self):
        # 显示标签 - 使用Computed对象实现真正的响应式绑定
        self.counter_text = Computed(lambda: f"计数: {showcase_data.counter.value}")
        self.doubled_text = Computed(lambda: f"双倍: {showcase_data.counter_doubled.value}") 
        self.squared_text = Computed(lambda: f"平方: {showcase_data.counter_squared.value}")
        
        self.counter_label = Label(
            self.counter_text,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.doubled_label = Label(
            self.doubled_text,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.squared_label = Label(
            self.squared_text,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.greeting_label = Label(
            showcase_data.greeting_message,
            style=ComponentStyle(width=px(400), height=px(30))
        )
        
        # 设置Effect来自动更新UI
        self.setup_reactive_updates()
    
    def setup_reactive_updates(self):
        """设置响应式UI更新"""
        
        # 现在使用真正的响应式绑定，Label会自动更新
        # 创建一个简单的Effect来演示响应式系统工作
        def update_counter_display():
            # 仅用于日志记录，实际UI更新由ReactiveBinding自动处理
            print(f"📢 响应式更新触发: 计数={showcase_data.counter.value}, 双倍={showcase_data.counter_doubled.value}")
        
        # 创建Effect来监听状态变化
        self.update_effect = Effect(update_counter_display)
        print("🔄 响应式更新Effect创建完成 - 使用真正的响应式绑定")
    
    def increment(self):
        """增加计数"""
        showcase_data.counter.value += 1
        showcase_data.total_clicks.value += 1
        print(f"➕ 计数增加: {showcase_data.counter.value}")
    
    def decrement(self):
        """减少计数"""
        showcase_data.counter.value -= 1
        showcase_data.total_clicks.value += 1
        print(f"➖ 计数减少: {showcase_data.counter.value}")
    
    def reset(self):
        """重置计数"""
        showcase_data.counter.value = 0
        showcase_data.total_clicks.value += 1
        print("🔄 计数重置")
    
    def create_component(self):
        """创建组件界面"""
        
        # 按钮容器
        button_container = Container(
            children=[
                Button("+ 增加", on_click=self.increment, 
                      style=ComponentStyle(width=px(80), height=px(35))),
                Button("- 减少", on_click=self.decrement, 
                      style=ComponentStyle(width=px(80), height=px(35))),
                Button("重置", on_click=self.reset, 
                      style=ComponentStyle(width=px(80), height=px(35))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                gap=px(15)
            )
        )
        
        # 主容器
        main_container = Container(
            children=[
                Label("🔄 响应式系统演示", 
                      style=ComponentStyle(width=px(300), height=px(40))),
                
                # 状态显示区
                self.counter_label,
                self.doubled_label,
                self.squared_label,
                self.greeting_label,
                
                # 控制按钮
                button_container,
                
                Label("✨ 展示Signal、Computed和Effect的响应式特性", 
                      style=ComponentStyle(width=px(450), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(20),
                width=px(600),
                height=px(450)
            )
        )
        
        return main_container

# ================================
# 🏗️ 布局演示组件
# ================================

class LayoutDemo:
    """布局系统演示"""
    
    def __init__(self):
        self.current_direction = Signal("column")
        self.current_alignment = Signal("center")
        
        # 演示盒子
        self.box1 = Label("📦 Box 1", style=ComponentStyle(width=px(100), height=px(50)))
        self.box2 = Label("📦 Box 2", style=ComponentStyle(width=px(120), height=px(60)))
        self.box3 = Label("📦 Box 3", style=ComponentStyle(width=px(80), height=px(40)))
        
        # 动态布局容器 (需要重新创建来更新样式)
        self.layout_container = self.create_layout_container()
    
    def create_layout_container(self):
        """创建动态布局容器"""
        direction = FlexDirection.COLUMN if self.current_direction.value == "column" else FlexDirection.ROW
        
        alignment_map = {
            "center": AlignItems.CENTER,
            "start": AlignItems.FLEX_START,
            "end": AlignItems.FLEX_END,
            "stretch": AlignItems.STRETCH,
        }
        alignment = alignment_map.get(self.current_alignment.value, AlignItems.CENTER)
        
        return Container(
            children=[self.box1, self.box2, self.box3],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=direction,
                align_items=alignment,
                justify_content=JustifyContent.CENTER,
                gap=px(15),
                width=px(400),
                height=px(200)
            )
        )
    
    def toggle_direction(self):
        """切换布局方向"""
        self.current_direction.value = "row" if self.current_direction.value == "column" else "column"
        print(f"🔄 切换布局方向: {self.current_direction.value}")
        # 注意：实际应用中需要重新创建container来应用新样式
    
    def cycle_alignment(self):
        """循环切换对齐方式"""
        alignments = ["center", "start", "end", "stretch"]
        current_index = alignments.index(self.current_alignment.value)
        self.current_alignment.value = alignments[(current_index + 1) % len(alignments)]
        print(f"🔄 切换对齐方式: {self.current_alignment.value}")
    
    def create_component(self):
        """创建布局演示组件"""
        
        # 控制按钮
        control_buttons = Container(
            children=[
                Button("切换方向", on_click=self.toggle_direction, 
                      style=ComponentStyle(width=px(100), height=px(30))),
                Button("切换对齐", on_click=self.cycle_alignment, 
                      style=ComponentStyle(width=px(100), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                gap=px(15)
            )
        )
        
        # 状态显示 - 使用响应式绑定
        status_text = Computed(lambda: f"方向: {self.current_direction.value}, 对齐: {self.current_alignment.value}")
        status_label = Label(
            status_text,
            style=ComponentStyle(width=px(300), height=px(30))
        )
        
        return Container(
            children=[
                Label("📐 布局系统演示", 
                      style=ComponentStyle(width=px(300), height=px(40))),
                
                control_buttons,
                status_label,
                self.layout_container,
                
                Label("✨ 展示Flexbox布局和动态样式", 
                      style=ComponentStyle(width=px(350), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(20),
                width=px(600),
                height=px(450)
            )
        )

# ================================
# 🎮 用户交互演示
# ================================

class InteractionDemo:
    """交互功能演示"""
    
    def __init__(self):
        self.click_count = Signal(0)
        self.last_button = Signal("None")
        self.user_message = Signal("点击任意按钮开始交互")
        
        # 状态显示标签 - 使用真正的响应式绑定
        self.click_count_text = Computed(lambda: f"总点击次数: {self.click_count.value}")
        self.last_action_text = Computed(lambda: f"最后操作: {self.last_button.value}")
        
        self.status_label = Label(
            self.user_message,
            style=ComponentStyle(width=px(400), height=px(30))
        )
        
        self.click_label = Label(
            self.click_count_text,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.last_action_label = Label(
            self.last_action_text,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        # 设置响应式更新
        self.setup_updates()
    
    def setup_updates(self):
        """设置UI更新"""
        # 现在使用真正的响应式绑定，Label会自动更新
        def update_display():
            # 仅用于日志记录，实际UI更新由ReactiveBinding自动处理
            print(f"📢 交互更新触发: 点击={self.click_count.value}, 按钮={self.last_button.value}")
        
        self.update_effect = Effect(update_display)
    
    def handle_button_click(self, button_name, message):
        """处理按钮点击"""
        def handler():
            self.click_count.value += 1
            self.last_button.value = button_name
            self.user_message.value = message
            print(f"🎮 交互: {button_name} - {message}")
        return handler
    
    def create_component(self):
        """创建交互演示组件"""
        
        # 交互按钮组
        action_buttons = Container(
            children=[
                Button("打招呼", 
                      on_click=self.handle_button_click("打招呼", "👋 你好！欢迎使用macUI v4"), 
                      style=ComponentStyle(width=px(100), height=px(30))),
                Button("显示时间", 
                      on_click=self.handle_button_click("显示时间", "⏰ 现在是演示时间"), 
                      style=ComponentStyle(width=px(100), height=px(30))),
                Button("切换主题", 
                      on_click=self.handle_button_click("切换主题", "🎨 主题已切换"), 
                      style=ComponentStyle(width=px(100), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                gap=px(10)
            )
        )
        
        # 功能按钮组
        function_buttons = Container(
            children=[
                Button("重置计数", 
                      on_click=self.handle_button_click("重置", "🔄 计数已重置"), 
                      style=ComponentStyle(width=px(100), height=px(30))),
                Button("清空消息", 
                      on_click=self.handle_button_click("清空", "✨ 消息已清空"), 
                      style=ComponentStyle(width=px(100), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                gap=px(10)
            )
        )
        
        return Container(
            children=[
                Label("🎮 交互系统演示", 
                      style=ComponentStyle(width=px(300), height=px(40))),
                
                # 状态显示区
                self.status_label,
                self.click_label,
                self.last_action_label,
                
                # 交互按钮区
                action_buttons,
                function_buttons,
                
                Label("✨ 展示事件处理和状态更新", 
                      style=ComponentStyle(width=px(300), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(20),
                width=px(600),
                height=px(450)
            )
        )

# ================================
# 🧩 组件库演示
# ================================

class ComponentsDemo:
    """五大组件完整演示"""
    
    def __init__(self):
        print("🧩 ComponentsDemo初始化完成")
    
    def on_slider_change(self, value):
        """滑块值变化回调"""
        showcase_data.slider_value.value = value
        print(f"🎚️ 滑块值变化: {value}")
    
    def on_volume_change(self, value):
        """音量滑块变化回调"""
        showcase_data.volume.value = value
        print(f"🔊 音量变化: {value}")
    
    def on_brightness_change(self, value):
        """亮度滑块变化回调"""
        showcase_data.brightness.value = value
        print(f"☀️ 亮度变化: {value}")
    
    def on_dark_mode_change(self, state):
        """深色模式开关回调"""
        showcase_data.dark_mode.value = state
        print(f"🌙 深色模式: {state}")
    
    def on_notifications_change(self, state):
        """通知开关回调"""
        showcase_data.notifications.value = state
        print(f"🔔 通知: {state}")
    
    def on_auto_save_change(self, state):
        """自动保存开关回调"""
        showcase_data.auto_save.value = state
        print(f"💾 自动保存: {state}")
    
    def on_text_change(self, text):
        """文本输入回调"""
        showcase_data.text_input.value = text
        print(f"📝 文本输入: {text}")
    
    def create_component(self):
        """创建组件演示界面"""
        
        # 标题
        title = Label("🧩 macUI v4 五大组件演示", 
                     style=ComponentStyle(width=px(400), height=px(40)))
        
        # === 滑块组件演示 ===
        slider_section = Container(
            children=[
                Label("🎚️ Slider 滑块组件", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                # 主滑块
                Container(
                    children=[
                        Label("数值:", style=ComponentStyle(width=px(50), height=px(30))),
                        Slider(
                            value=showcase_data.slider_value,
                            min_value=0.0,
                            max_value=100.0,
                            on_change=self.on_slider_change,
                            style=ComponentStyle(width=px(200), height=px(30))
                        ),
                        Label(showcase_data.slider_percentage, 
                             style=ComponentStyle(width=px(60), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
                
                # 音量滑块
                Container(
                    children=[
                        Label("音量:", style=ComponentStyle(width=px(50), height=px(30))),
                        Slider(
                            value=showcase_data.volume,
                            min_value=0.0,
                            max_value=100.0,
                            on_change=self.on_volume_change,
                            style=ComponentStyle(width=px(200), height=px(30))
                        ),
                        Label(showcase_data.volume_display, 
                             style=ComponentStyle(width=px(80), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
                
                # 亮度滑块
                Container(
                    children=[
                        Label("亮度:", style=ComponentStyle(width=px(50), height=px(30))),
                        Slider(
                            value=showcase_data.brightness,
                            min_value=0.0,
                            max_value=100.0,
                            on_change=self.on_brightness_change,
                            style=ComponentStyle(width=px(200), height=px(30))
                        ),
                        Label(showcase_data.brightness_display, 
                             style=ComponentStyle(width=px(80), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
        
        # === 开关组件演示 ===
        switch_section = Container(
            children=[
                Label("🔘 Switch 开关组件", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                # 深色模式开关
                Container(
                    children=[
                        Label("深色模式:", style=ComponentStyle(width=px(80), height=px(30))),
                        Switch(
                            value=showcase_data.dark_mode,
                            on_change=self.on_dark_mode_change,
                            style=ComponentStyle(width=px(60), height=px(30))
                        ),
                        Label(Computed(lambda: "🌙" if showcase_data.dark_mode.value else "☀️"), 
                             style=ComponentStyle(width=px(30), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
                
                # 通知开关
                Container(
                    children=[
                        Label("通知:", style=ComponentStyle(width=px(80), height=px(30))),
                        Switch(
                            value=showcase_data.notifications,
                            on_change=self.on_notifications_change,
                            style=ComponentStyle(width=px(60), height=px(30))
                        ),
                        Label(Computed(lambda: "🔔" if showcase_data.notifications.value else "🔕"), 
                             style=ComponentStyle(width=px(30), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
                
                # 自动保存开关
                Container(
                    children=[
                        Label("自动保存:", style=ComponentStyle(width=px(80), height=px(30))),
                        Switch(
                            value=showcase_data.auto_save,
                            on_change=self.on_auto_save_change,
                            style=ComponentStyle(width=px(60), height=px(30))
                        ),
                        Label(Computed(lambda: "💾" if showcase_data.auto_save.value else "📄"), 
                             style=ComponentStyle(width=px(30), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
        
        # === 文本输入组件演示 ===
        textfield_section = Container(
            children=[
                Label("📝 TextField 文本输入组件", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                Container(
                    children=[
                        Label("输入:", style=ComponentStyle(width=px(50), height=px(30))),
                        TextField(
                            value=showcase_data.text_input,
                            placeholder="请输入文本...",
                            on_change=self.on_text_change,
                            style=ComponentStyle(width=px(200), height=px(30))
                        ),
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        align_items=AlignItems.CENTER,
                        gap=px(10)
                    )
                ),
                
                # 显示输入的文本
                Label(
                    Computed(lambda: f"您输入的文本: {showcase_data.text_input.value}"),
                    style=ComponentStyle(width=px(350), height=px(25))
                ),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
        
        # === 设置状态摘要 ===
        settings_summary = Container(
            children=[
                Label("⚙️ 设置状态摘要", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                Label(showcase_data.settings_summary, 
                     style=ComponentStyle(width=px(500), height=px(30))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
        
        # 主容器
        return Container(
            children=[
                title,
                slider_section,
                switch_section,
                textfield_section,
                settings_summary,
                Label("✨ 所有组件都支持响应式绑定和事件处理", 
                     style=ComponentStyle(width=px(400), height=px(25))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(15),
                width=px(600),
                height=px(700)
            )
        )

# ================================
# 📋 表单演示组件
# ================================

class FormsDemo:
    """表单系统完整演示"""
    
    def __init__(self):
        print("📋 FormsDemo初始化完成")
    
    def on_form_submit(self, form_data):
        """表单提交处理"""
        showcase_data.form_submit_count.value += 1
        showcase_data.last_form_data.value = form_data.copy()
        # 更新全局表单数据
        showcase_data.form_data.value = form_data.copy()
        print(f"📤 表单提交#{showcase_data.form_submit_count.value}: {form_data}")
    
    def on_form_reset(self):
        """表单重置处理"""
        initial_data = {
            "name": "",
            "email": "",
            "age": 25,
            "subscribe": False,
            "bio": "",
            "rating": 5
        }
        showcase_data.form_data.value = initial_data
        print("🔄 表单已重置")
    
    def create_form_demo(self):
        """创建表单演示界面"""
        title = Label("📋 macUI v4 表单系统演示", 
                     style=ComponentStyle(width=px(400), height=px(40)))
        
        # === 基础表单演示 ===
        basic_form_section = self.create_basic_form()
        
        # === 验证器演示 ===
        validation_section = self.create_validation_demo()
        
        # === 表单模板演示 ===
        template_section = self.create_template_demo()
        
        # === 表单状态显示 ===
        status_section = self.create_status_display()
        
        # 主容器
        return Container(
            children=[
                title,
                basic_form_section,
                validation_section,
                template_section,
                status_section,
                Label("✨ 支持响应式验证、数据绑定和模板系统", 
                     style=ComponentStyle(width=px(400), height=px(25))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(20),
                width=px(600),
                height=px(800)
            )
        )
    
    def create_basic_form(self):
        """创建基础表单"""
        # 创建表单字段
        name_field = TextField(
            placeholder="请输入姓名",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        email_field = TextField(
            placeholder="请输入邮箱",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        age_slider = Slider(
            value=25, min_value=18, max_value=65,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        rating_slider = Slider(
            value=5, min_value=1, max_value=10,
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        subscribe_switch = Switch(
            value=False,
            style=ComponentStyle(width=px(60), height=px(30))
        )
        
        bio_field = TextField(
            placeholder="请输入个人简介（可选）",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        # 创建FormField对象
        form_fields = [
            FormField(name_field, [
                RequiredValidator("姓名不能为空"),
                LengthValidator(2, 30, "姓名长度必须在2-30字符之间")
            ], "name"),
            
            FormField(email_field, [
                RequiredValidator("邮箱不能为空"),
                EmailValidator("请输入有效的邮箱地址")
            ], "email"),
            
            FormField(age_slider, [
                NumberValidator(18, 65, "年龄必须在18-65岁之间")
            ], "age"),
            
            FormField(rating_slider, [
                NumberValidator(1, 10, "评分必须在1-10分之间")
            ], "rating"),
            
            FormField(subscribe_switch, [], "subscribe"),
            
            FormField(bio_field, [
                LengthValidator(0, 200, "个人简介不能超过200字符")
            ], "bio")
        ]
        
        # 创建Form容器
        self.demo_form = Form(
            fields=form_fields,
            on_submit=self.on_form_submit,
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
        
        # 创建提交和重置按钮
        submit_btn = Button(
            "📤 提交表单",
            on_click=lambda: self.demo_form.submit(),
            style=ComponentStyle(width=px(120), height=px(30))
        )
        
        reset_btn = Button(
            "🔄 重置表单",
            on_click=lambda: self.demo_form.reset(),
            style=ComponentStyle(width=px(120), height=px(30))
        )
        
        return Container(
            children=[
                Label("📝 基础表单演示", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                # 表单字段行
                Container([
                    Container([
                        Label("姓名:", style=ComponentStyle(width=px(50), height=px(30))),
                        name_field
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                    Container([
                        Label("邮箱:", style=ComponentStyle(width=px(50), height=px(30))),
                        email_field
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                    Container([
                        Label("年龄:", style=ComponentStyle(width=px(50), height=px(30))),
                        age_slider,
                        Label(Computed(lambda: f"{showcase_data.form_data.value.get('age', 25)}岁"),
                             style=ComponentStyle(width=px(50), height=px(30)))
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                    Container([
                        Label("评分:", style=ComponentStyle(width=px(50), height=px(30))),
                        rating_slider,
                        Label(Computed(lambda: f"{showcase_data.form_data.value.get('rating', 5)}分"),
                             style=ComponentStyle(width=px(50), height=px(30)))
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                    Container([
                        Label("订阅:", style=ComponentStyle(width=px(50), height=px(30))),
                        subscribe_switch,
                        Label(Computed(lambda: "✅" if showcase_data.form_data.value.get('subscribe', False) else "❌"),
                             style=ComponentStyle(width=px(30), height=px(30)))
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                    Container([
                        Label("简介:", style=ComponentStyle(width=px(50), height=px(30))),
                        bio_field
                    ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=px(10))),
                    
                ], style=ComponentStyle(display=Display.FLEX, flex_direction=FlexDirection.COLUMN, gap=px(5))),
                
                # 按钮组
                Container(
                    children=[submit_btn, reset_btn],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        gap=px(10)
                    )
                )
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
    
    def create_validation_demo(self):
        """创建验证器演示"""
        return Container(
            children=[
                Label("🔍 验证器演示", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                # 表单验证状态显示
                Container(
                    children=[
                        Label("验证状态:", style=ComponentStyle(width=px(80), height=px(30))),
                        Label(
                            Computed(lambda: "✅ 通过" if hasattr(self, 'demo_form') and self.demo_form.is_valid.value else "❌ 有错误"),
                            style=ComponentStyle(width=px(80), height=px(30))
                        )
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        gap=px(10)
                    )
                ),
                
                # 错误信息显示
                Label(
                    Computed(lambda: f"错误: {', '.join(self.demo_form.validation_errors.value) if hasattr(self, 'demo_form') and self.demo_form.validation_errors.value else '无错误'}"),
                    style=ComponentStyle(width=px(400), height=px(40))
                ),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(5)
            )
        )
    
    def create_template_demo(self):
        """创建表单模板演示"""
        def create_login_form():
            """创建登录表单"""
            login_form = FormTemplates.login_form(
                lambda data: print(f"🔐 登录: {data}")
            )
            print(f"✅ 登录表单创建: {len(login_form.fields)} 字段")
            return f"登录表单 ({len(login_form.fields)} 字段)"
        
        def create_register_form():
            """创建注册表单"""
            register_form = FormTemplates.registration_form(
                lambda data: print(f"📝 注册: {data}")
            )
            print(f"✅ 注册表单创建: {len(register_form.fields)} 字段")
            return f"注册表单 ({len(register_form.fields)} 字段)"
        
        return Container(
            children=[
                Label("📋 表单模板演示", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                Container(
                    children=[
                        Button("🔐 创建登录表单", 
                              on_click=lambda: print(create_login_form()),
                              style=ComponentStyle(width=px(150), height=px(30))),
                        Button("📝 创建注册表单", 
                              on_click=lambda: print(create_register_form()),
                              style=ComponentStyle(width=px(150), height=px(30)))
                    ],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW,
                        gap=px(10)
                    )
                )
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(10)
            )
        )
    
    def create_status_display(self):
        """创建状态显示"""
        return Container(
            children=[
                Label("📊 表单状态显示", 
                     style=ComponentStyle(width=px(350), height=px(25))),
                
                # 表单摘要
                Label(showcase_data.form_summary, 
                     style=ComponentStyle(width=px(400), height=px(30))),
                
                # 表单状态
                Label(showcase_data.form_status, 
                     style=ComponentStyle(width=px(400), height=px(30))),
                
                # 最后提交的数据
                Label(
                    Computed(lambda: f"📤 最后提交: {showcase_data.last_form_data.value}" if showcase_data.last_form_data.value else "📤 尚未提交"),
                    style=ComponentStyle(width=px(500), height=px(40))
                ),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(5)
            )
        )

# ================================
# 🚀 主应用
# ================================

class ShowcaseApp:
    """主应用类"""
    
    def __init__(self):
        # 演示组件
        self.reactive_demo = ReactiveCounterDemo()
        self.layout_demo = LayoutDemo()
        self.interaction_demo = InteractionDemo()
        self.components_demo = ComponentsDemo()
        self.forms_demo = FormsDemo()
        
        # 当前演示页面
        self.current_demo = Signal("components")  # 默认显示组件演示
        
        print("🎨 ShowcaseApp初始化完成")
    
    def switch_demo(self, demo_name):
        """切换演示页面 - 使用动态内容更新"""
        def handler():
            old_demo = self.current_demo.value
            self.current_demo.value = demo_name
            print(f"🔄 切换演示: {old_demo} -> {demo_name}")
            
            # 动态更新内容区域
            if hasattr(self, '_content_container') and self._content_container:
                new_content = self._create_demo_content(demo_name)
                self._content_container.set_children([new_content])
                print(f"🔄 内容区域已动态更新为: {demo_name}")
            
            print(f"💡 导航切换完成! 当前演示: {demo_name}")
        return handler
    
    def _create_demo_content(self, demo_name):
        """根据演示类型创建对应的内容"""
        if demo_name == "components":
            return self.components_demo.create_component()
        elif demo_name == "reactive":
            return self.reactive_demo.create_component()
        elif demo_name == "layout":
            return self.layout_demo.create_component()
        elif demo_name == "interaction":
            return self.interaction_demo.create_component()
        elif demo_name == "forms":
            return self.forms_demo.create_form_demo()
        else:
            # 默认返回组件演示
            return self.components_demo.create_component()
    
    def create_dynamic_content(self):
        """创建动态内容区域"""
        # 创建一个显示当前演示状态的响应式标签
        def get_current_status():
            demo_name = self.current_demo.value
            status_map = {
                "components": "✅ 当前: 🧩 五大组件演示",
                "reactive": "✅ 当前: 🔄 响应式系统演示", 
                "layout": "✅ 当前: 📐 布局系统演示",
                "interaction": "✅ 当前: 🎮 交互系统演示",
                "forms": "✅ 当前: 📋 表单系统演示"
            }
            return status_map.get(demo_name, "🎨 macUI v4 框架演示")
        
        current_status = Computed(get_current_status)
        status_label = Label(current_status, 
                           style=ComponentStyle(width=px(400), height=px(30)))
        
        # 创建初始内容
        initial_content = self._create_demo_content(self.current_demo.value)
        
        # 创建动态内容容器（用于动态更新）
        self._content_container = Container(
            children=[initial_content],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(10)
            )
        )
        
        # 创建包含状态标签和动态内容的主容器
        main_content_container = Container(
            children=[
                status_label,
                self._content_container
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(15)
            )
        )
        
        return main_content_container
    
    def create_main_interface(self):
        """创建主界面"""
        
        # 标题
        title = Label(
            "🎨 macUI v4 Complete Showcase - 组件演示&表单系统",
            style=ComponentStyle(width=px(500), height=px(50))
        )
        
        # 导航按钮
        nav_buttons = Container(
            children=[
                Button("🧩 组件演示", on_click=self.switch_demo("components"), 
                      style=ComponentStyle(width=px(120), height=px(35))),
                Button("🔄 响应式演示", on_click=self.switch_demo("reactive"), 
                      style=ComponentStyle(width=px(120), height=px(35))),
                Button("📐 布局演示", on_click=self.switch_demo("layout"), 
                      style=ComponentStyle(width=px(100), height=px(35))),
                Button("🎮 交互演示", on_click=self.switch_demo("interaction"), 
                      style=ComponentStyle(width=px(100), height=px(35))),
                Button("📋 表单演示", on_click=self.switch_demo("forms"), 
                      style=ComponentStyle(width=px(100), height=px(35))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                gap=px(10)
            )
        )
        
        # 内容区域 - 根据current_demo动态显示不同演示
        content_area = self.create_dynamic_content()
        
        # 主容器
        main_container = Container(
            children=[title, nav_buttons, content_area],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(25),
                width=percent(100),
                height=percent(100)
            )
        )
        
        return main_container

# ================================
# 🎯 应用启动和窗口管理
# ================================

class ShowcaseAppDelegate(NSObject):
    """应用委托"""
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 macUI v4 Complete Showcase 启动")
        
        # 初始化管理器
        ManagerFactory.initialize_all()
        
        # 创建主窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 800, 650),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable,
            2,  # NSBackingStoreBuffered
            False
        )
        
        self.window.setTitle_("macUI v4 Complete Feature Showcase")
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建应用界面
        self.app = ShowcaseApp()
        self.main_interface = self.app.create_main_interface()
        
        # 挂载到窗口
        main_view = self.main_interface.mount()
        self.window.setContentView_(main_view)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        
        print("✅ 应用界面创建完成，窗口已显示")
    
    def create_menu(self):
        """创建菜单栏"""
        # 创建主菜单
        main_menu = NSMenu.alloc().init()
        
        # 应用菜单
        app_menu_item = NSMenuItem.alloc().init()
        main_menu.addItem_(app_menu_item)
        
        app_menu = NSMenu.alloc().init()
        app_menu_item.setSubmenu_(app_menu)
        
        # 退出菜单项
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit macUI v4 Showcase", "terminate:", "q"
        )
        app_menu.addItem_(quit_item)
        
        # 设置为应用菜单
        NSApplication.sharedApplication().setMainMenu_(main_menu)
    
    def applicationWillTerminate_(self, notification):
        """应用即将退出"""
        print("👋 应用退出，清理资源")
        if hasattr(self, 'main_interface'):
            self.main_interface.cleanup()

def main():
    """主函数 - 启动应用"""
    print("🎨 启动 macUI v4 Complete Feature Showcase")
    
    try:
        # 创建应用实例
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 设置应用委托
        delegate = ShowcaseAppDelegate.alloc().init()
        app.setDelegate_(delegate)
        
        # 进入事件循环
        print("🔄 进入事件循环...")
        AppHelper.runEventLoop()
        
    except KeyboardInterrupt:
        print("\n⚡ 用户中断，退出应用")
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()