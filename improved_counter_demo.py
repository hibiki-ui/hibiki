#!/usr/bin/env python3
"""
改进的 macUI v2 计数器演示 - 遵循 PyObjC 命令行启动最佳实践

这个演示基于提供的技术文档，实现了：
1. 正确的应用激活策略
2. 最小化菜单栏
3. 使用 AppHelper 运行事件循环
4. 分离的应用代理和窗口控制器结构
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

# 添加父目录到路径以便导入 macui
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from core.signal import Signal, Computed, Effect


# --------------------------------------------------------------------------
# 1. 按钮目标类 (处理按钮点击事件)
# --------------------------------------------------------------------------
class CounterButtonTarget(NSObject):
    """计数器按钮目标处理类"""
    
    def initWithHandler_(self, handler):
        self = objc.super(CounterButtonTarget, self).init()
        if self is None:
            return None
        self.handler = handler
        return self
    
    @objc.python_method
    def buttonClicked_(self, sender):
        if self.handler:
            try:
                self.handler()
                print(f"Button clicked successfully")
            except Exception as e:
                print(f"Button handler error: {e}")
                import traceback
                traceback.print_exc()


# --------------------------------------------------------------------------
# 2. 窗口控制器 (负责UI和逻辑)
# --------------------------------------------------------------------------
class CounterWindowController(NSObject):
    """计数器窗口控制器"""
    
    def init(self):
        self = objc.super(CounterWindowController, self).init()
        if self is None:
            return None
        
        # 创建响应式状态
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
        self.double_text = Computed(lambda: f"Double: {self.count.value * 2}")
        self.is_even = Computed(lambda: "Even" if self.count.value % 2 == 0 else "Odd")
        
        print(f"Window controller initialized with count: {self.count.value}")
        return self
    
    def show(self):
        """创建和显示窗口"""
        print("Creating and showing counter window...")
        
        # 创建窗口
        window_rect = NSMakeRect(100, 100, 400, 300)
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("macUI v2 - Improved Counter Demo")
        self.window.center()
        
        # 创建内容视图
        content_view = self.window.contentView()
        
        # 创建标签
        self.count_label = NSTextField.alloc().init()
        self.count_label.setFrame_(NSMakeRect(50, 220, 300, 30))
        self.count_label.setStringValue_(self.count_text.value)
        self.count_label.setEditable_(False)
        self.count_label.setSelectable_(False)
        self.count_label.setBezeled_(False)
        self.count_label.setDrawsBackground_(False)
        
        self.double_label = NSTextField.alloc().init()
        self.double_label.setFrame_(NSMakeRect(50, 190, 300, 30))
        self.double_label.setStringValue_(self.double_text.value)
        self.double_label.setEditable_(False)
        self.double_label.setSelectable_(False)
        self.double_label.setBezeled_(False)
        self.double_label.setDrawsBackground_(False)
        
        self.status_label = NSTextField.alloc().init()
        self.status_label.setFrame_(NSMakeRect(50, 160, 300, 30))
        self.status_label.setStringValue_(f"Status: {self.is_even.value}")
        self.status_label.setEditable_(False)
        self.status_label.setSelectable_(False)
        self.status_label.setBezeled_(False)
        self.status_label.setDrawsBackground_(False)
        
        # 创建按钮
        self.inc_button = NSButton.alloc().init()
        self.inc_button.setFrame_(NSMakeRect(50, 100, 80, 30))
        self.inc_button.setTitle_("Increment")
        self.inc_button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        self.dec_button = NSButton.alloc().init()
        self.dec_button.setFrame_(NSMakeRect(140, 100, 80, 30))
        self.dec_button.setTitle_("Decrement")
        self.dec_button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        self.reset_button = NSButton.alloc().init()
        self.reset_button.setFrame_(NSMakeRect(230, 100, 80, 30))
        self.reset_button.setTitle_("Reset")
        self.reset_button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 添加控件到视图
        content_view.addSubview_(self.count_label)
        content_view.addSubview_(self.double_label)
        content_view.addSubview_(self.status_label)
        content_view.addSubview_(self.inc_button)
        content_view.addSubview_(self.dec_button)
        content_view.addSubview_(self.reset_button)
        
        # 设置按钮事件处理
        self.setup_button_handlers()
        
        # 设置响应式更新
        self.setup_reactive_updates()
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)
        print("Counter window displayed successfully")
    
    def setup_button_handlers(self):
        """设置按钮事件处理"""
        print("Setting up button handlers...")
        
        # 增加按钮
        def increment():
            old_value = self.count.value
            self.count.value += 1
            print(f"Incremented: {old_value} -> {self.count.value}")
        
        inc_target = CounterButtonTarget.alloc().initWithHandler_(increment)
        self.inc_button.setTarget_(inc_target)
        self.inc_button.setAction_(objc.selector(inc_target.buttonClicked_, signature=b'v@:@'))
        
        # 减少按钮
        def decrement():
            old_value = self.count.value
            self.count.value -= 1
            print(f"Decremented: {old_value} -> {self.count.value}")
        
        dec_target = CounterButtonTarget.alloc().initWithHandler_(decrement)
        self.dec_button.setTarget_(dec_target)
        self.dec_button.setAction_(objc.selector(dec_target.buttonClicked_, signature=b'v@:@'))
        
        # 重置按钮
        def reset():
            old_value = self.count.value
            self.count.value = 0
            print(f"Reset: {old_value} -> 0")
        
        reset_target = CounterButtonTarget.alloc().initWithHandler_(reset)
        self.reset_button.setTarget_(reset_target)
        self.reset_button.setAction_(objc.selector(reset_target.buttonClicked_, signature=b'v@:@'))
        
        # 保持目标对象的引用，防止被垃圾回收
        self.inc_target = inc_target
        self.dec_target = dec_target
        self.reset_target = reset_target
        
        print("Button handlers setup completed")
    
    def setup_reactive_updates(self):
        """设置响应式UI更新"""
        print("Setting up reactive updates...")
        
        def update_count_label():
            self.count_label.setStringValue_(self.count_text.value)
        
        def update_double_label():
            self.double_label.setStringValue_(self.double_text.value)
        
        def update_status_label():
            self.status_label.setStringValue_(f"Status: {self.is_even.value}")
        
        # 创建 Effects 来自动更新UI
        self.count_effect = Effect(update_count_label)
        self.double_effect = Effect(update_double_label)
        self.status_effect = Effect(update_status_label)
        
        print("Reactive updates setup completed")


# --------------------------------------------------------------------------
# 3. 应用代理 (负责生命周期)
# --------------------------------------------------------------------------
class CounterAppDelegate(NSObject):
    """计数器应用代理"""
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成后的回调"""
        print("Application finished launching, creating window controller...")
        
        # 创建窗口控制器实例并持有强引用
        self.window_controller = CounterWindowController.alloc().init()
        
        # 显示窗口
        self.window_controller.show()
        
        print("Application setup completed")
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """最后一个窗口关闭时终止应用"""
        return True


# --------------------------------------------------------------------------
# 4. 主函数 (负责启动流程)
# --------------------------------------------------------------------------
def main():
    """主函数 - 遵循PyObjC最佳实践"""
    print("=== macUI v2 Improved Counter Demo ===")
    print("Following PyObjC command-line best practices:")
    print("• Proper activation policy")
    print("• Minimal menu bar")
    print("• AppHelper event loop")
    print("• Separated app delegate and window controller")
    print("=" * 50)
    
    with objc.autorelease_pool():
        # 创建应用实例
        app = NSApplication.sharedApplication()
        print("NSApplication created")
        
        # 要点 1: 设置激活策略
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        print("Activation policy set to Regular")
        
        # 要点 2: 创建最小化菜单栏
        print("Creating minimal menu bar...")
        menubar = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_menu_item)
        app.setMainMenu_(menubar)
        
        # 创建应用菜单
        app_menu = NSMenu.alloc().init()
        app_name = NSProcessInfo.processInfo().processName()
        quit_title = f"Quit {app_name}"
        quit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            quit_title, "terminate:", "q"
        )
        app_menu.addItem_(quit_menu_item)
        app_menu_item.setSubmenu_(app_menu)
        print("Menu bar created with Quit option")
        
        # 要点 4: 创建并设置应用代理
        delegate = CounterAppDelegate.alloc().init()
        app.setDelegate_(delegate)
        print("App delegate set")
        
        # 激活应用，使其成为焦点
        app.activateIgnoringOtherApps_(True)
        print("Application activated")
        
        print("\nStarting application...")
        print("💡 Click the buttons to test reactive functionality!")
        print("💡 Close the window to exit the application")
        
        # 要点 3: 使用 AppHelper 运行事件循环
        AppHelper.runEventLoop(installInterrupt=True)
        
        print("\nApplication terminated")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎊 Thank you for using the improved macUI v2 counter demo!")