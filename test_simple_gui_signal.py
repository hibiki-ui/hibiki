#!/usr/bin/env python3
"""
简化的GUI Signal测试，追踪重复执行问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import objc
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

from macui_v4.core.reactive import Signal, Computed, Effect
from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import Label

# 全局计数器追踪创建次数
label_create_count = 0
signal_create_count = 0

class SimpleGUITest(NSObject):
    """简化GUI测试"""
    
    def init(self):
        self = objc.super(SimpleGUITest, self).init()
        if self is None:
            return None
        self.window = None
        
        # 只创建一个Signal
        global signal_create_count
        signal_create_count += 1
        print(f"🎯 创建Signal #{signal_create_count}")
        self.counter = Signal(0)
        
        # 只创建一个Computed
        print(f"🎯 创建Computed基于Signal #{signal_create_count}")
        self.counter_text = Computed(lambda: f"计数: {self.counter.value}")
        
        return self
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 应用启动，创建窗口...")
        
        # 初始化管理器
        ManagerFactory.initialize_all()
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 300, 200),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("简化GUI测试")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建简单界面
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 300, 200))
        
        # 只创建一个Label
        global label_create_count
        label_create_count += 1
        print(f"🏷️ 创建Label #{label_create_count}")
        self.label = Label(self.counter_text, width=200, height=30)
        label_view = self.label.mount()
        label_view.setFrame_(NSMakeRect(50, 100, 200, 30))
        container.addSubview_(label_view)
        
        print(f"📊 初始状态检查:")
        print(f"   Signal观察者数: {len(self.counter._observers)}")
        print(f"   Computed观察者数: {len(self.counter_text._observers)}")
        print(f"   Label显示: '{self.label.get_text()}'")
        
        self.window.setContentView_(container)
        
        # 延迟更新测试
        self.performSelector_withObject_afterDelay_("test_update", None, 2.0)
        
        print("✅ 简化GUI创建完成")
    
    def test_update(self):
        """测试更新"""
        print("\n🔥 执行更新测试...")
        print(f"   更新前 - Signal: {self.counter.value}, Label: '{self.label.get_text()}'")
        
        # 只执行一次更新
        self.counter.value = 42
        
        print(f"   更新后 - Signal: {self.counter.value}, Label: '{self.label.get_text()}'")
        print(f"   Computed: '{self.counter_text.value}'")
        
        # 检查NSView实际显示
        if self.label._nsview:
            print(f"   NSView实际值: '{self.label._nsview.stringValue()}'")
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True

def main():
    """主函数"""
    print("🚀 启动简化GUI Signal测试...")
    
    try:
        # 创建应用
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 简化菜单栏
        menubar = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_menu_item)
        app.setMainMenu_(menubar)
        
        app_menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", "terminate:", "q"
        )
        app_menu.addItem_(quit_item)
        app_menu_item.setSubmenu_(app_menu)
        
        # 创建应用委托
        app_delegate = SimpleGUITest.alloc().init()
        app.setDelegate_(app_delegate)
        
        # 启动应用
        app.activateIgnoringOtherApps_(True)
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()