#!/usr/bin/env python3
"""
自动测试计数器应用的UI更新功能
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
from macui.core.binding import ReactiveBinding, EventBinding

class TestCounterController(NSObject):
    """测试计数器控制器"""
    
    def init(self):
        self = objc.super(TestCounterController, self).init()
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
        self.window.setTitle_("Test Counter")
        self.window.center()
        
        content_view = self.window.contentView()
        
        # 创建标签
        self.label = NSTextField.alloc().init()
        self.label.setFrame_(NSMakeRect(20, 90, 200, 30))
        self.label.setEditable_(False)
        self.label.setSelectable_(False)
        self.label.setBezeled_(False)
        self.label.setDrawsBackground_(False)
        
        # 创建按钮
        self.button = NSButton.alloc().init()
        self.button.setFrame_(NSMakeRect(20, 50, 100, 30))
        self.button.setTitle_("Increment")
        self.button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 添加控件到视图
        content_view.addSubview_(self.label)
        content_view.addSubview_(self.button)
        
        # 使用ReactiveBinding绑定
        print("设置响应式绑定...")
        self.cleanup_fn = ReactiveBinding.bind(self.label, "text", self.count_text)
        
        # 绑定按钮事件
        EventBinding.bind_click(self.button, self.increment)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        print("窗口已显示")
        
        # 自动测试
        self.auto_test()
    
    def auto_test(self):
        """自动测试函数"""
        import threading
        import time
        
        def test_clicks():
            print("开始自动测试...")
            time.sleep(1)
            
            for i in range(5):
                print(f"自动点击 #{i+1}...")
                self.increment()
                print(f"当前count: {self.count.value}")
                print(f"当前label文本: {str(self.label.stringValue())}")
                time.sleep(0.5)
            
            print("自动测试完成!")
            
            # 验证结果
            expected_count = 5
            expected_text = f"Count: {expected_count}"
            actual_count = self.count.value
            actual_text = str(self.label.stringValue())
            
            print(f"预期count: {expected_count}, 实际count: {actual_count}")
            print(f"预期text: '{expected_text}', 实际text: '{actual_text}'")
            
            if actual_count == expected_count and actual_text == expected_text:
                print("✅ 测试成功! UI更新正常工作")
            else:
                print("❌ 测试失败! UI更新有问题")
            
            # 3秒后退出
            def quit_app():
                time.sleep(3)
                NSApplication.sharedApplication().terminate_(None)
            
            threading.Thread(target=quit_app).start()
        
        # 在后台线程运行测试
        threading.Thread(target=test_clicks).start()
    
    def increment(self):
        """增加计数"""
        old_value = self.count.value
        self.count.value += 1
        print(f"按钮点击: {old_value} -> {self.count.value}")

class TestAppDelegate(NSObject):
    """测试应用代理"""
    
    def applicationDidFinishLaunching_(self, notification):
        print("测试应用启动完成")
        self.controller = TestCounterController.alloc().init()
        self.controller.show()
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True

def main():
    """主函数"""
    print("启动自动测试计数器应用...")
    
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
        delegate = TestAppDelegate.alloc().init()
        app.setDelegate_(delegate)
        
        app.activateIgnoringOtherApps_(True)
        print("启动事件循环...")
        AppHelper.runEventLoop(installInterrupt=True)

if __name__ == "__main__":
    main()