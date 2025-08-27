#!/usr/bin/env python3
"""
macUI v4.0 完整GUI演示应用
展示新架构在真实应用环境中的运行效果
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# 导入macUI v4.0
from macui_v4.core.managers import ManagerFactory, ZLayer, Position
from macui_v4.core.component import Container
from macui_v4.components.basic import Label, Button, TextField

# 导入AppKit和Foundation
from AppKit import (
    NSApplication, NSApplicationActivationPolicyRegular, NSWindow, NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable, NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
    NSBackingStoreBuffered, NSMakeRect, NSMenu, NSMenuItem
)
from Foundation import NSObject
from PyObjCTools import AppHelper
import objc

class AppDelegate(NSObject):
    """应用程序委托"""
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 macUI v4.0 GUI应用启动")
        
        # 初始化macUI管理器系统
        ManagerFactory.initialize_all()
        
        # 创建窗口控制器
        self.window_controller = WindowController.alloc().init()
        self.window_controller.show_window()
        
        print("✅ GUI应用初始化完成")
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, app):
        """最后一个窗口关闭时退出应用"""
        return True


class WindowController(NSObject):
    """窗口控制器"""
    
    def __init__(self):
        self.window = None
        self.components = []
        self.counter = 0
    
    def init(self):
        self = objc.super(WindowController, self).init()
        if self is None:
            return None
        
        # 创建窗口
        self.create_window()
        
        # 创建UI组件
        self.create_ui_components()
        
        return self
    
    def create_window(self):
        """创建主窗口"""
        # 窗口样式
        style_mask = (NSWindowStyleMaskTitled | 
                     NSWindowStyleMaskClosable | 
                     NSWindowStyleMaskMiniaturizable | 
                     NSWindowStyleMaskResizable)
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 800, 600),  # x, y, width, height
            style_mask,
            NSBackingStoreBuffered,
            False
        )
        
        # 设置窗口属性
        self.window.setTitle_("macUI v4.0 GUI演示")
        self.window.center()
        
        print("🖼️ 主窗口创建完成")
    
    def create_ui_components(self):
        """创建UI组件"""
        print("\n🎨 创建UI组件...")
        
        # 1. 标题标签
        title_label = Label(
            "macUI v4.0 架构演示", 
            width=400, height=40
        )
        title_label.layout.center().fade(0.9).scale(1.2)
        
        # 相对于居中位置向上偏移
        title_label.style.top = "30%"  # 调整到上方
        title_view = title_label.mount()
        self.components.append((title_label, title_view))
        
        # 2. 输入文本框
        def on_text_change(text):
            print(f"💬 用户输入: '{text}'")
        
        input_field = TextField(
            value="请在这里输入...",
            placeholder="输入一些文本",
            on_change=on_text_change,
            width=300, height=30
        )
        input_field.layout.center()
        input_field.style.top = "45%"  # 在标题下方
        input_view = input_field.mount()
        self.components.append((input_field, input_view))
        
        # 3. 计数器按钮
        def increment_counter():
            self.counter += 1
            counter_button.set_title(f"点击次数: {self.counter}")
            print(f"🔢 按钮被点击 {self.counter} 次")
        
        counter_button = Button(
            f"点击次数: {self.counter}",
            on_click=increment_counter,
            width=200, height=35
        )
        counter_button.layout.center()
        counter_button.style.top = "60%"  # 在输入框下方
        counter_view = counter_button.mount()
        self.components.append((counter_button, counter_view))
        
        # 4. 悬浮提示按钮
        def show_floating_message():
            print("💬 悬浮消息：macUI v4.0运行正常！")
            # 创建临时提示标签
            message_label = Label("✨ macUI v4.0运行正常！", width=200, height=25)
            message_label.layout.modal(250, 80).fade(0.95)
            message_view = message_label.mount()
            
            # 添加到窗口
            self.window.contentView().addSubview_(message_view)
            
            # 3秒后移除（这里简化处理）
            print("💫 临时消息已显示")
        
        floating_button = Button(
            "显示提示", 
            on_click=show_floating_message,
            width=100, height=30
        )
        floating_button.layout.floating_button("bottom-right", margin=30)
        floating_view = floating_button.mount()
        self.components.append((floating_button, floating_view))
        
        # 5. 状态指示器
        status_label = Label("● 系统运行中", width=120, height=20)
        status_label.layout.top_left(margin=20).fade(0.7)
        status_view = status_label.mount()
        self.components.append((status_label, status_view))
        
        # 6. 容器演示
        container_items = [
            Label("项目 1", width=80, height=25),
            Label("项目 2", width=80, height=25), 
            Button("操作", width=60, height=25)
        ]
        
        demo_container = Container(
            children=container_items,
            width=250, height=100, padding=15
        )
        demo_container.advanced.set_flex_properties(
            direction="row",
            justify="space-around",
            align="center"
        )
        demo_container.layout.bottom_left(margin=50)
        container_view = demo_container.mount()
        self.components.append((demo_container, container_view))
        
        print(f"✅ 创建了 {len(self.components)} 个UI组件")
    
    def show_window(self):
        """显示窗口并添加所有组件"""
        # 获取窗口内容视图
        content_view = self.window.contentView()
        
        # 添加所有组件到窗口
        for i, (component, view) in enumerate(self.components):
            content_view.addSubview_(view)
            print(f"✅ 组件 {i+1}: {component.__class__.__name__} 已添加到窗口")
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        print(f"🖼️ 窗口已显示，包含 {len(self.components)} 个组件")


def create_menu_bar():
    """创建菜单栏"""
    # 创建主菜单
    main_menu = NSMenu.alloc().init()
    
    # 创建应用菜单
    app_menu_item = NSMenuItem.alloc().init()
    main_menu.addItem_(app_menu_item)
    
    app_menu = NSMenu.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    
    # 添加退出菜单项
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "退出 macUI Demo", 
        "terminate:", 
        "q"
    )
    app_menu.addItem_(quit_item)
    
    # 设置为应用菜单
    NSApplication.sharedApplication().setMainMenu_(main_menu)


def main():
    """主函数"""
    print("🚀 启动 macUI v4.0 完整GUI演示")
    print("=" * 50)
    
    # 创建应用实例
    app = NSApplication.sharedApplication()
    
    # 设置激活策略
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    
    # 创建菜单栏
    create_menu_bar()
    
    # 创建并设置应用委托
    app_delegate = AppDelegate.alloc().init()
    app.setDelegate_(app_delegate)
    
    print("🎯 启动事件循环...")
    print("💡 提示: 这是一个真实的macOS GUI应用")
    print("💡 你可以与界面交互: 输入文本、点击按钮等")
    print("💡 使用 Cmd+Q 退出应用")
    print("-" * 50)
    
    # 启动事件循环
    try:
        AppHelper.runEventLoop()
    except KeyboardInterrupt:
        print("\n👋 应用被用户中断")
    except Exception as e:
        print(f"❌ 应用运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()