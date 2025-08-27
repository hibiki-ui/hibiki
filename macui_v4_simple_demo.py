#!/usr/bin/env python3
"""
🎨 macUI v4 Simple Feature Demo
简化的v4框架功能演示

专注展示核心功能：
✅ 响应式系统 (Signal/Computed/Effect)
✅ 组件系统 (Label/Button/Container)  
✅ 布局系统 (Flexbox)
✅ 事件处理
"""

import sys
import os

# 添加macui_v4路径
sys.path.append(os.path.join(os.path.dirname(__file__), "macui_v4"))

# 导入v4核心
from core.managers import ManagerFactory
from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, JustifyContent, px
from core.reactive import Signal, Computed, Effect
from components.basic import Label, Button
from core.component import Container

# PyObjC导入
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

# ================================
# 🎯 简化的演示应用
# ================================

class SimpleV4Demo:
    """简化的v4演示"""
    
    def __init__(self):
        print("🎨 SimpleV4Demo初始化")
        
        # 响应式状态
        self.counter = Signal(0)
        self.status = Signal("欢迎使用 macUI v4!")
        
        # 计算属性
        self.counter_double = Computed(lambda: self.counter.value * 2)
        
        # 创建UI组件
        self.create_components()
        
        # 设置响应式更新
        self.setup_reactive_updates()
    
    def create_components(self):
        """创建UI组件"""
        
        # 标题
        self.title_label = Label(
            "🚀 macUI v4 功能演示",
            style=ComponentStyle(width=px(300), height=px(40))
        )
        
        # 状态标签
        self.status_label = Label(
            self.status.value,
            style=ComponentStyle(width=px(300), height=px(30))
        )
        
        # 计数器显示
        self.counter_label = Label(
            f"计数: {self.counter.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        self.double_label = Label(
            f"双倍: {self.counter_double.value}",
            style=ComponentStyle(width=px(200), height=px(30))
        )
        
        # 按钮
        self.inc_button = Button(
            "增加 +",
            on_click=self.increment,
            style=ComponentStyle(width=px(80), height=px(30))
        )
        
        self.dec_button = Button(
            "减少 -",
            on_click=self.decrement,
            style=ComponentStyle(width=px(80), height=px(30))
        )
        
        self.reset_button = Button(
            "重置",
            on_click=self.reset,
            style=ComponentStyle(width=px(80), height=px(30))
        )
        
        print("✅ UI组件创建完成")
    
    def setup_reactive_updates(self):
        """设置响应式UI更新"""
        
        def update_ui():
            # 更新计数器显示
            if hasattr(self.counter_label, '_nsview'):
                self.counter_label._nsview.setStringValue_(f"计数: {self.counter.value}")
            
            # 更新双倍显示
            if hasattr(self.double_label, '_nsview'):
                self.double_label._nsview.setStringValue_(f"双倍: {self.counter_double.value}")
            
            # 更新状态显示
            if hasattr(self.status_label, '_nsview'):
                self.status_label._nsview.setStringValue_(self.status.value)
        
        # 创建Effect来监听状态变化
        self.ui_effect = Effect(update_ui)
        print("🔄 响应式更新设置完成")
    
    def increment(self):
        """增加计数"""
        self.counter.value += 1
        self.status.value = f"计数增加到 {self.counter.value}"
        print(f"➕ 计数: {self.counter.value}")
    
    def decrement(self):
        """减少计数"""
        self.counter.value -= 1
        self.status.value = f"计数减少到 {self.counter.value}"
        print(f"➖ 计数: {self.counter.value}")
    
    def reset(self):
        """重置计数"""
        self.counter.value = 0
        self.status.value = "计数已重置"
        print("🔄 计数重置")
    
    def create_main_interface(self):
        """创建主界面"""
        
        # 按钮组
        button_group = Container(
            children=[self.inc_button, self.dec_button, self.reset_button],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                gap=px(10)
            )
        )
        
        # 主容器
        main_container = Container(
            children=[
                self.title_label,
                self.status_label,
                self.counter_label,
                self.double_label,
                button_group,
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(20),
                width=px(400),
                height=px(300)
            )
        )
        
        return main_container

# ================================
# 🚀 应用启动
# ================================

class SimpleAppDelegate(NSObject):
    """简化的应用委托"""
    
    def applicationDidFinishLaunching_(self, notification):
        print("🚀 应用启动")
        
        # 初始化管理器
        ManagerFactory.initialize_all()
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(200, 200, 500, 400),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("macUI v4 Simple Demo")
        
        # 创建演示应用
        self.demo = SimpleV4Demo()
        self.main_interface = self.demo.create_main_interface()
        
        # 挂载界面
        main_view = self.main_interface.mount()
        self.window.setContentView_(main_view)
        self.window.makeKeyAndOrderFront_(None)
        
        print("✅ 界面创建完成")
    
    def applicationWillTerminate_(self, notification):
        print("👋 应用退出")
        if hasattr(self, 'main_interface'):
            self.main_interface.cleanup()

def main():
    """主函数"""
    print("🎨 启动 macUI v4 Simple Demo")
    
    # 创建应用
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    
    # 设置委托
    delegate = SimpleAppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    # 创建基本菜单
    main_menu = NSMenu.alloc().init()
    app_menu_item = NSMenuItem.alloc().init()
    main_menu.addItem_(app_menu_item)
    
    app_menu = NSMenu.alloc().init()
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    app_menu_item.setSubmenu_(app_menu)
    app.setMainMenu_(main_menu)
    
    # 启动事件循环
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()