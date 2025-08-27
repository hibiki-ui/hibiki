#!/usr/bin/env python3
"""
测试按钮点击后Label响应式更新问题
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
from macui_v4.components.basic import Label, Button

class ClickTestApp(NSObject):
    """点击测试应用"""
    
    def init(self):
        self = objc.super(ClickTestApp, self).init()
        if self is None:
            return None
        self.window = None
        self.counter = Signal(0)
        self.status = Signal("初始状态")
        
        # 创建计算属性
        self.counter_text = Computed(lambda: f"计数: {self.counter.value}")
        self.status_text = Computed(lambda: f"状态: {self.status.value}")
        
        print(f"🎯 初始化完成 - counter: {self.counter.value}, status: {self.status.value}")
        return self
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 应用启动，创建测试窗口...")
        
        # 初始化管理器
        ManagerFactory.initialize_all()
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 400, 300),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("按钮点击测试")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建界面
        self.create_ui()
        
        print("✅ 测试窗口创建完成")
    
    def create_ui(self):
        """创建用户界面"""
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 400, 300))
        
        # 标题
        title_label = Label("按钮点击响应式更新测试", width=300, height=30)
        title_view = title_label.mount()
        title_view.setFrame_(NSMakeRect(50, 240, 300, 30))
        container.addSubview_(title_view)
        
        # 计数显示 - 使用响应式
        print("📊 创建计数标签...")
        self.counter_label = Label(self.counter_text, width=200, height=30)
        counter_view = self.counter_label.mount()
        counter_view.setFrame_(NSMakeRect(50, 200, 200, 30))
        container.addSubview_(counter_view)
        print(f"📊 计数标签初始文本: '{self.counter_label.get_text()}'")
        
        # 状态显示 - 使用响应式
        print("📋 创建状态标签...")
        self.status_label = Label(self.status_text, width=300, height=30)
        status_view = self.status_label.mount()
        status_view.setFrame_(NSMakeRect(50, 160, 300, 30))
        container.addSubview_(status_view)
        print(f"📋 状态标签初始文本: '{self.status_label.get_text()}'")
        
        # 按钮
        inc_button = Button("点击增加", on_click=self.increment_counter)
        inc_view = inc_button.mount()
        inc_view.setFrame_(NSMakeRect(50, 120, 100, 30))
        container.addSubview_(inc_view)
        
        # 直接更新按钮（测试Signal是否工作）
        direct_button = Button("直接更新", on_click=self.direct_update)
        direct_view = direct_button.mount()
        direct_view.setFrame_(NSMakeRect(160, 120, 100, 30))
        container.addSubview_(direct_view)
        
        # 检查状态按钮
        check_button = Button("检查状态", on_click=self.check_status)
        check_view = check_button.mount()
        check_view.setFrame_(NSMakeRect(270, 120, 100, 30))
        container.addSubview_(check_view)
        
        self.window.setContentView_(container)
        print("✅ 用户界面创建完成")
        
        # 验证初始状态
        print(f"🔍 初始验证:")
        print(f"   Counter Signal: {self.counter.value}")
        print(f"   Counter Computed: {self.counter_text.value}")
        print(f"   Counter Label显示: '{self.counter_label.get_text()}'")
        print(f"   Status Signal: {self.status.value}")
        print(f"   Status Computed: {self.status_text.value}")
        print(f"   Status Label显示: '{self.status_label.get_text()}'")
    
    def increment_counter(self):
        """增加计数器"""
        old_counter = self.counter.value
        old_status = self.status.value
        
        print(f"\n🔥 按钮点击 - 增加计数器")
        print(f"   更新前 - Counter: {old_counter}, Status: '{old_status}'")
        
        # 更新Signal
        self.counter.value += 1
        self.status.value = f"点击了 {self.counter.value} 次"
        
        print(f"   更新后 - Counter: {self.counter.value}, Status: '{self.status.value}'")
        print(f"   Computed - Counter: '{self.counter_text.value}', Status: '{self.status_text.value}'")
        
        # 检查Label是否更新
        print(f"   Label显示 - Counter: '{self.counter_label.get_text()}', Status: '{self.status_label.get_text()}'")
        
        # 检查NSView的实际值
        counter_nsview = self.counter_label._nsview
        status_nsview = self.status_label._nsview
        if counter_nsview:
            print(f"   NSView实际值 - Counter: '{counter_nsview.stringValue()}'")
        if status_nsview:
            print(f"   NSView实际值 - Status: '{status_nsview.stringValue()}'")
    
    def direct_update(self):
        """直接更新测试"""
        print(f"\n⚡ 直接更新测试")
        self.counter.value = 999
        self.status.value = "直接更新测试"
        
        print(f"   Signal值 - Counter: {self.counter.value}, Status: '{self.status.value}'")
        print(f"   Computed值 - Counter: '{self.counter_text.value}', Status: '{self.status_text.value}'")
        print(f"   Label显示 - Counter: '{self.counter_label.get_text()}', Status: '{self.status_label.get_text()}'")
    
    def check_status(self):
        """检查当前状态"""
        print(f"\n🔍 检查当前状态")
        print(f"   Signal值 - Counter: {self.counter.value}, Status: '{self.status.value}'")
        print(f"   Computed值 - Counter: '{self.counter_text.value}', Status: '{self.status_text.value}'")
        print(f"   Label显示 - Counter: '{self.counter_label.get_text()}', Status: '{self.status_label.get_text()}'")
        
        # 检查Signal的观察者
        print(f"   Signal观察者数 - Counter: {len(self.counter._observers)}, Status: {len(self.status._observers)}")
        
        # 手动触发更新测试
        print("   手动触发UI更新测试...")
        if hasattr(self.counter_label, '_nsview') and self.counter_label._nsview:
            self.counter_label._nsview.setStringValue_(f"手动更新: {self.counter.value}")
        
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        return True


def main():
    """主函数"""
    print("🚀 启动按钮点击更新测试...")
    
    try:
        # 创建应用
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 创建菜单栏
        menubar = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_menu_item)
        app.setMainMenu_(menubar)
        
        app_menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit Test", "terminate:", "q"
        )
        app_menu.addItem_(quit_item)
        app_menu_item.setSubmenu_(app_menu)
        
        # 创建应用委托
        app_delegate = ClickTestApp.alloc().init()
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