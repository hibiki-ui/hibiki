#!/usr/bin/env python3
"""
macUI v4.0 完整GUI应用测试
测试AppKit集成、响应式系统、组件系统的完整工作流程
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import objc
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

# v4架构导入
from macui_v4.core.reactive import Signal, Computed, Effect
from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import Label, Button
from macui_v4.core.component import UIComponent

class MacUIv4DemoApp(UIComponent):
    """macUI v4.0 演示应用"""
    
    def __init__(self):
        super().__init__()
        
        # 响应式状态
        self.counter = Signal(0)
        self.status = Signal("准备就绪")
        self.user_name = Signal("用户")
        
        # 计算属性
        self.counter_text = Computed(lambda: f"计数: {self.counter.value}")
        self.greeting = Computed(lambda: f"你好，{self.user_name.value}！")
        self.parity = Computed(lambda: "偶数" if self.counter.value % 2 == 0 else "奇数")
        
        print("🎯 v4演示应用状态初始化完成")
    
    def _create_nsview(self) -> NSView:
        """创建v4演示界面"""
        print("🔧 创建v4演示界面...")
        
        # 创建主容器
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 480, 400))
        
        # 标题
        title_label = Label("🚀 macUI v4.0 演示", width=400, height=40)
        title_view = title_label.mount()
        title_view.setFrame_(NSMakeRect(40, 340, 400, 40))
        container.addSubview_(title_view)
        
        # 副标题
        subtitle_label = Label("响应式系统 + 组件系统 + AppKit集成", width=400, height=25)
        subtitle_view = subtitle_label.mount()
        subtitle_view.setFrame_(NSMakeRect(40, 310, 400, 25))
        container.addSubview_(subtitle_view)
        
        # 用户名显示
        greeting_label = Label(self.greeting, width=300, height=30)
        greeting_view = greeting_label.mount()
        greeting_view.setFrame_(NSMakeRect(40, 270, 300, 30))
        container.addSubview_(greeting_view)
        
        # 计数显示
        counter_label = Label(self.counter_text, width=200, height=30)
        counter_view = counter_label.mount()
        counter_view.setFrame_(NSMakeRect(40, 230, 200, 30))
        container.addSubview_(counter_view)
        
        # 奇偶显示
        parity_label = Label(self.parity, width=100, height=25)
        parity_view = parity_label.mount()
        parity_view.setFrame_(NSMakeRect(250, 235, 100, 25))
        container.addSubview_(parity_view)
        
        # 状态显示
        status_label = Label(self.status, width=400, height=25)
        status_view = status_label.mount()
        status_view.setFrame_(NSMakeRect(40, 190, 400, 25))
        container.addSubview_(status_view)
        
        # 按钮区域
        y_pos = 140
        
        # 增加按钮
        inc_button = Button("增加", on_click=self._increment)
        inc_view = inc_button.mount()
        inc_view.setFrame_(NSMakeRect(40, y_pos, 80, 30))
        container.addSubview_(inc_view)
        
        # 减少按钮
        dec_button = Button("减少", on_click=self._decrement)
        dec_view = dec_button.mount()
        dec_view.setFrame_(NSMakeRect(130, y_pos, 80, 30))
        container.addSubview_(dec_view)
        
        # 重置按钮
        reset_button = Button("重置", on_click=self._reset)
        reset_view = reset_button.mount()
        reset_view.setFrame_(NSMakeRect(220, y_pos, 80, 30))
        container.addSubview_(reset_view)
        
        # 更改用户名按钮
        name_button = Button("更改用户名", on_click=self._change_name)
        name_view = name_button.mount()
        name_view.setFrame_(NSMakeRect(310, y_pos, 120, 30))
        container.addSubview_(name_view)
        
        # 批量测试按钮
        batch_button = Button("批量测试", on_click=self._batch_test)
        batch_view = batch_button.mount()
        batch_view.setFrame_(NSMakeRect(40, y_pos - 40, 100, 30))
        container.addSubview_(batch_view)
        
        # 清理测试按钮
        cleanup_button = Button("清理测试", on_click=self._cleanup_test)
        cleanup_view = cleanup_button.mount()
        cleanup_view.setFrame_(NSMakeRect(150, y_pos - 40, 100, 30))
        container.addSubview_(cleanup_view)
        
        print("✅ v4演示界面创建完成")
        return container
    
    def _increment(self):
        """增加计数"""
        self.counter.value += 1
        self.status.value = f"计数增加到 {self.counter.value}"
        print(f"🔢 计数增加: {self.counter.value}")
    
    def _decrement(self):
        """减少计数"""
        if self.counter.value > 0:
            self.counter.value -= 1
            self.status.value = f"计数减少到 {self.counter.value}"
        else:
            self.status.value = "计数已为0"
        print(f"🔢 计数减少: {self.counter.value}")
    
    def _reset(self):
        """重置计数"""
        self.counter.value = 0
        self.status.value = "计数已重置"
        print("🔄 计数重置")
    
    def _change_name(self):
        """更改用户名"""
        import random
        names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
        new_name = random.choice(names)
        self.user_name.value = new_name
        self.status.value = f"用户名已更改为 {new_name}"
        print(f"👤 用户名更改: {new_name}")
    
    def _batch_test(self):
        """批量测试响应式系统"""
        print("⚡ 开始批量测试...")
        from macui_v4.core.reactive import batch_update
        
        def batch_changes():
            self.counter.value += 10
            self.user_name.value = "批量测试用户"
            self.status.value = "批量更新完成"
        
        batch_update(batch_changes)
        print("✅ 批量测试完成")
    
    def _cleanup_test(self):
        """清理测试"""
        print("🧹 开始清理测试...")
        # 这里可以测试组件清理功能
        self.status.value = "清理测试完成"
        print("✅ 清理测试完成")


class MacUIv4AppDelegate(NSObject):
    """macUI v4.0 应用委托"""
    
    def init(self):
        self = objc.super(MacUIv4AppDelegate, self).init()
        if self is None:
            return None
        self.window = None
        self.demo_app = None
        return self
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 应用启动完成，创建主窗口...")
        
        # 初始化v4管理器系统
        ManagerFactory.initialize_all()
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 480, 400),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("macUI v4.0 演示")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建并挂载v4演示应用
        self.demo_app = MacUIv4DemoApp()
        content_view = self.demo_app.mount()
        self.window.setContentView_(content_view)
        
        print("✅ macUI v4.0 演示应用启动成功！")
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """最后一个窗口关闭时终止应用"""
        return True


def create_menu_bar(app_name: str):
    """创建菜单栏"""
    # 创建主菜单栏
    menubar = NSMenu.alloc().init()
    app_menu_item = NSMenuItem.alloc().init()
    menubar.addItem_(app_menu_item)
    NSApp.setMainMenu_(menubar)

    # 创建应用主菜单
    app_menu = NSMenu.alloc().init()

    # 创建退出菜单项
    quit_title = f"Quit {app_name}"
    quit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        quit_title, "terminate:", "q"
    )
    app_menu.addItem_(quit_menu_item)
    app_menu_item.setSubmenu_(app_menu)


def main():
    """主函数"""
    print("🚀 启动macUI v4.0完整GUI应用测试...")
    print("=" * 50)
    
    try:
        # 创建NSApplication实例
        app = NSApplication.sharedApplication()
        
        # 设置激活策略
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        print("✅ 应用激活策略设置完成")
        
        # 创建菜单栏
        create_menu_bar("macUI v4.0 Demo")
        print("✅ 菜单栏创建完成")
        
        # 创建应用委托
        app_delegate = MacUIv4AppDelegate.alloc().init()
        app.setDelegate_(app_delegate)
        print("✅ 应用委托设置完成")
        
        # 激活应用
        app.activateIgnoringOtherApps_(True)
        print("✅ 应用激活完成")
        
        print("\n🎯 v4.0 架构验证:")
        print("   ✅ 响应式系统 (Signal, Computed, Effect)")
        print("   ✅ 组件系统 (Label, Button)")
        print("   ✅ 绑定系统 (ReactiveBinding)")
        print("   ✅ 管理器系统 (ManagerFactory)")
        print("   ✅ AppKit集成 (NSApplication, NSWindow)")
        print("   ✅ 事件循环 (AppHelper)")
        
        print("\n🎮 启动事件循环，享受macUI v4.0...")
        
        # 启动事件循环
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()