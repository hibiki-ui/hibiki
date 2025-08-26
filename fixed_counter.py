#!/usr/bin/env python3
"""
修复后的简单计数器应用 - 不依赖复杂的组件系统
"""

import sys
import os
import objc
from Foundation import NSObject
from AppKit import (
    NSApplication, NSMenu, NSMenuItem, NSProcessInfo,
    NSWindow, NSButton, NSTextField, 
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSBackingStoreBuffered, NSApplicationActivationPolicyRegular,
    NSButtonTypeMomentaryPushIn
)
from Foundation import NSMakeRect
from PyObjCTools import AppHelper

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed


class SimpleButtonTarget(NSObject):
    """简单按钮目标处理类"""
    
    def initWithHandler_(self, handler):
        self = objc.super(SimpleButtonTarget, self).init()
        if self is None:
            return None
        self.handler = handler
        return self
    
    @objc.python_method
    def buttonClicked_(self, sender):
        if self.handler:
            try:
                self.handler()
            except Exception as e:
                print(f"Button handler error: {e}")


class FixedCounterController(NSObject):
    """修复的计数器控制器"""
    
    def init(self):
        self = objc.super(FixedCounterController, self).init()
        if self is None:
            return None
        
        # 创建响应式状态
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
        
        print(f"初始化: count={self.count.value}, text='{self.count_text.value}'")
        return self
    
    def show(self):
        """创建和显示窗口"""
        # 创建窗口
        window_rect = NSMakeRect(100, 100, 350, 150)
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("Fixed Counter")
        self.window.center()
        
        content_view = self.window.contentView()
        
        # 创建标签
        self.label = NSTextField.alloc().init()
        self.label.setFrame_(NSMakeRect(20, 90, 200, 30))
        self.label.setStringValue_(self.count_text.value)
        self.label.setEditable_(False)
        self.label.setSelectable_(False)
        self.label.setBezeled_(False)
        self.label.setDrawsBackground_(False)
        
        # 创建按钮
        self.button = NSButton.alloc().init()
        self.button.setFrame_(NSMakeRect(20, 50, 100, 30))
        self.button.setTitle_("Increment")
        self.button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 设置按钮目标
        self.button_target = SimpleButtonTarget.alloc().initWithHandler_(self.increment)
        self.button.setTarget_(self.button_target)
        self.button.setAction_(objc.selector(self.button_target.buttonClicked_, signature=b'v@:@'))
        
        # 添加控件到视图
        content_view.addSubview_(self.label)
        content_view.addSubview_(self.button)
        
        # 设置手动的响应式更新
        print("设置响应式更新...")
        self.setup_manual_binding()
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        print("窗口已显示")
    
    def setup_manual_binding(self):
        """设置手动的响应式绑定"""
        # 不使用Effect，而是手动管理更新
        
        # 保存原始的signal set方法
        original_set = self.count.__class__.set
        
        def custom_set(signal_self, new_value):
            # 调用原始的set方法
            original_set(signal_self, new_value)
            
            # 手动更新UI
            if signal_self is self.count:
                print(f"手动更新UI: {self.count_text.value}")
                self.label.setStringValue_(self.count_text.value)
        
        # 替换set方法
        self.count.__class__.set = custom_set
        
        print("手动绑定设置完成")
    
    def increment(self):
        """增加计数"""
        old_value = self.count.value
        self.count.value += 1
        print(f"按钮点击: {old_value} -> {self.count.value}")


class SimpleAppDelegate(NSObject):
    """简单应用代理"""
    
    def applicationDidFinishLaunching_(self, notification):
        print("应用启动完成")
        self.controller = FixedCounterController.alloc().init()
        self.controller.show()
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True


def main():
    """主函数"""
    print("启动修复的计数器应用...")
    
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
        
        # 设置代理
        delegate = SimpleAppDelegate.alloc().init()
        app.setDelegate_(delegate)
        
        app.activateIgnoringOtherApps_(True)
        print("启动事件循环...")
        AppHelper.runEventLoop(installInterrupt=True)


if __name__ == "__main__":
    main()