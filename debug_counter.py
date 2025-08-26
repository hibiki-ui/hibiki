#!/usr/bin/env python3
"""
调试计数器应用 - 不使用布局组件，直接测试响应式绑定
"""

import sys
import os
import objc
from Foundation import NSObject
from AppKit import (
    NSApplication, NSMenu, NSMenuItem, NSProcessInfo, NSApp,
    NSWindow, NSButton, NSTextField, NSView,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSBackingStoreBuffered, NSApplicationActivationPolicyRegular,
    NSButtonTypeMomentaryPushIn
)
from Foundation import NSMakeRect
from PyObjCTools import AppHelper

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect
from macui.components import Button, Label
from macui.core.binding import EventBinding


class DebugButtonTarget(NSObject):
    """调试按钮目标处理类"""
    
    def initWithHandler_(self, handler):
        self = objc.super(DebugButtonTarget, self).init()
        if self is None:
            return None
        self.handler = handler
        return self
    
    @objc.python_method
    def buttonClicked_(self, sender):
        print(f"🔴 DEBUG: Button clicked! Handler: {self.handler}")
        if self.handler:
            try:
                self.handler()
                print(f"🟢 DEBUG: Handler executed successfully")
            except Exception as e:
                print(f"❌ DEBUG: Button handler error: {e}")
                import traceback
                traceback.print_exc()


class DebugCounterWindowController(NSObject):
    """调试计数器窗口控制器"""
    
    def init(self):
        self = objc.super(DebugCounterWindowController, self).init()
        if self is None:
            return None
        
        # 创建响应式状态
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
        
        print(f"🔵 DEBUG: Initial count: {self.count.value}")
        print(f"🔵 DEBUG: Initial count_text: {self.count_text.value}")
        
        return self
    
    def show(self):
        """创建和显示窗口"""
        print("🔵 DEBUG: Creating debug counter window...")
        
        # 创建窗口
        window_rect = NSMakeRect(100, 100, 400, 200)
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("Debug Counter")
        self.window.center()
        
        # 创建内容视图
        content_view = self.window.contentView()
        
        # 方法1: 使用macUI组件
        print("🔵 DEBUG: Creating Label with macUI...")
        self.macui_label = Label(self.count_text, frame=(50, 120, 300, 30))
        print(f"🔵 DEBUG: Label created: {type(self.macui_label)}")
        
        self.macui_button = Button(
            "Increment", 
            on_click=self.increment_macui,
            frame=(50, 80, 100, 30)
        )
        print(f"🔵 DEBUG: Button created: {type(self.macui_button)}")
        
        # 方法2: 直接创建原生控件用于对比
        print("🔵 DEBUG: Creating native controls for comparison...")
        self.native_label = NSTextField.alloc().init()
        self.native_label.setFrame_(NSMakeRect(200, 120, 150, 30))
        self.native_label.setStringValue_(self.count_text.value)
        self.native_label.setEditable_(False)
        self.native_label.setSelectable_(False)
        self.native_label.setBezeled_(False)
        self.native_label.setDrawsBackground_(False)
        
        self.native_button = NSButton.alloc().init()
        self.native_button.setFrame_(NSMakeRect(200, 80, 100, 30))
        self.native_button.setTitle_("Native Inc")
        self.native_button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 设置原生按钮事件
        native_target = DebugButtonTarget.alloc().initWithHandler_(self.increment_native)
        self.native_button.setTarget_(native_target)
        self.native_button.setAction_(objc.selector(native_target.buttonClicked_, signature=b'v@:@'))
        self.native_target = native_target  # 保持引用
        
        # 添加所有控件到视图
        content_view.addSubview_(self.macui_label)
        content_view.addSubview_(self.macui_button)
        content_view.addSubview_(self.native_label)
        content_view.addSubview_(self.native_button)
        
        # 设置响应式更新用于原生标签
        print("🔵 DEBUG: Setting up reactive update for native label...")
        
        def update_native_label():
            print(f"🟡 DEBUG: Effect triggered - updating native label to: {self.count_text.value}")
            self.native_label.setStringValue_(self.count_text.value)
        
        self.native_effect = Effect(update_native_label)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        print("🟢 DEBUG: Debug counter window displayed")
        
    def increment_macui(self):
        """macUI按钮的增加处理"""
        old_value = self.count.value
        self.count.value += 1
        print(f"🔵 DEBUG: macUI increment: {old_value} -> {self.count.value}")
        print(f"🔵 DEBUG: count_text now: {self.count_text.value}")
        
    def increment_native(self):
        """原生按钮的增加处理"""
        old_value = self.count.value
        self.count.value += 1
        print(f"🟠 DEBUG: Native increment: {old_value} -> {self.count.value}")
        print(f"🟠 DEBUG: count_text now: {self.count_text.value}")


class DebugAppDelegate(NSObject):
    """调试应用代理"""
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成后的回调"""
        print("🔵 DEBUG: App finished launching")
        self.window_controller = DebugCounterWindowController.alloc().init()
        self.window_controller.show()
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True


def main():
    """主函数"""
    print("🔵 DEBUG: Starting debug counter application...")
    
    with objc.autorelease_pool():
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 创建菜单栏
        menubar = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_menu_item)
        app.setMainMenu_(menubar)
        
        app_menu = NSMenu.alloc().init()
        app_name = NSProcessInfo.processInfo().processName()
        quit_title = f"Quit {app_name}"
        quit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            quit_title, "terminate:", "q"
        )
        app_menu.addItem_(quit_menu_item)
        app_menu_item.setSubmenu_(app_menu)
        
        # 创建应用代理
        delegate = DebugAppDelegate.alloc().init()
        app.setDelegate_(delegate)
        
        # 激活应用
        app.activateIgnoringOtherApps_(True)
        
        print("🔵 DEBUG: Starting event loop...")
        AppHelper.runEventLoop(installInterrupt=True)


if __name__ == "__main__":
    main()