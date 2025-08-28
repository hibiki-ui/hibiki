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
from components.basic import Label, Button
from core.component import Container

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
        
        # 计算属性
        self.counter_doubled = Computed(lambda: self.counter.value * 2)
        self.counter_squared = Computed(lambda: self.counter.value ** 2)
        self.greeting_message = Computed(
            lambda: f"Hello {self.user_name.value}! Counter: {self.counter.value}"
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
        # 显示标签 - 需要手动更新文本
        self.counter_label = Label(
            f"计数: {showcase_data.counter.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.doubled_label = Label(
            f"双倍: {showcase_data.counter_doubled.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.squared_label = Label(
            f"平方: {showcase_data.counter_squared.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.greeting_label = Label(
            showcase_data.greeting_message.value,
            style=ComponentStyle(width=px(400), height=px(30))
        )
        
        # 设置Effect来自动更新UI
        self.setup_reactive_updates()
    
    def setup_reactive_updates(self):
        """设置响应式UI更新"""
        
        # Effect: 当counter变化时更新标签
        def update_counter_display():
            # 手动更新NSTextField的文本 - 添加安全检查
            try:
                if hasattr(self.counter_label, '_nsview') and self.counter_label._nsview is not None:
                    self.counter_label._nsview.setStringValue_(f"计数: {showcase_data.counter.value}")
                if hasattr(self.doubled_label, '_nsview') and self.doubled_label._nsview is not None:
                    self.doubled_label._nsview.setStringValue_(f"双倍: {showcase_data.counter_doubled.value}")
                if hasattr(self.squared_label, '_nsview') and self.squared_label._nsview is not None:
                    self.squared_label._nsview.setStringValue_(f"平方: {showcase_data.counter_squared.value}")
                if hasattr(self.greeting_label, '_nsview') and self.greeting_label._nsview is not None:
                    self.greeting_label._nsview.setStringValue_(showcase_data.greeting_message.value)
            except Exception as e:
                print(f"⚠️  UI更新错误: {e}")
        
        # 创建Effect来监听状态变化
        self.update_effect = Effect(update_counter_display)
        print("🔄 响应式更新Effect创建完成")
    
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
        
        # 状态显示
        status_label = Label(
            f"方向: {self.current_direction.value}, 对齐: {self.current_alignment.value}",
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
        
        # 状态显示标签
        self.status_label = Label(
            self.user_message.value,
            style=ComponentStyle(width=px(400), height=px(30))
        )
        
        self.click_label = Label(
            f"总点击次数: {self.click_count.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.last_action_label = Label(
            f"最后操作: {self.last_button.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        # 设置响应式更新
        self.setup_updates()
    
    def setup_updates(self):
        """设置UI更新"""
        def update_display():
            try:
                if hasattr(self.status_label, '_nsview') and self.status_label._nsview is not None:
                    self.status_label._nsview.setStringValue_(self.user_message.value)
                if hasattr(self.click_label, '_nsview') and self.click_label._nsview is not None:
                    self.click_label._nsview.setStringValue_(f"总点击次数: {self.click_count.value}")
                if hasattr(self.last_action_label, '_nsview') and self.last_action_label._nsview is not None:
                    self.last_action_label._nsview.setStringValue_(f"最后操作: {self.last_button.value}")
            except Exception as e:
                print(f"⚠️  交互UI更新错误: {e}")
        
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
# 🚀 主应用
# ================================

class ShowcaseApp:
    """主应用类"""
    
    def __init__(self):
        # 演示组件
        self.reactive_demo = ReactiveCounterDemo()
        self.layout_demo = LayoutDemo()
        self.interaction_demo = InteractionDemo()
        
        # 当前演示页面
        self.current_demo = Signal("reactive")
        
        print("🎨 ShowcaseApp初始化完成")
    
    def switch_demo(self, demo_name):
        """切换演示页面"""
        def handler():
            self.current_demo.value = demo_name
            print(f"🔄 切换到演示: {demo_name}")
            # 注意：实际应用中需要重新创建内容区域
        return handler
    
    def create_main_interface(self):
        """创建主界面"""
        
        # 标题
        title = Label(
            "🎨 macUI v4 Complete Feature Showcase",
            style=ComponentStyle(width=px(500), height=px(50))
        )
        
        # 导航按钮
        nav_buttons = Container(
            children=[
                Button("响应式演示", on_click=self.switch_demo("reactive"), 
                      style=ComponentStyle(width=px(120), height=px(35))),
                Button("布局演示", on_click=self.switch_demo("layout"), 
                      style=ComponentStyle(width=px(100), height=px(35))),
                Button("交互演示", on_click=self.switch_demo("interaction"), 
                      style=ComponentStyle(width=px(100), height=px(35))),
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                gap=px(15)
            )
        )
        
        # 内容区域 - 默认显示响应式演示
        content_area = self.reactive_demo.create_component()
        
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