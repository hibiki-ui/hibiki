#!/usr/bin/env python3
"""调试版本5 - 结合点击事件和响应式绑定"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Computed, Component
from macui.components import Label, Button, VStack, LayoutStyle
from macui.layout.styles import AlignItems, JustifyContent
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class DebugShowcase5(Component):
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        # 🆕 特性5: 计算属性用于响应式绑定
        self.counter_text = Computed(lambda: f"计数: {self.counter.value}")
        print("📱 DebugShowcase5.__init__() 调用 - Signal + Computed + 事件处理")
        
    def mount(self):
        print("🔧 DebugShowcase5.mount() 开始...")
        
        # 静态Label
        label = Label("Hello macUI v3.0!", style=LayoutStyle(height=30))
        print(f"✅ 创建了Label: {label}")
        
        # 🆕 特性5: 响应式绑定的计数显示
        counter_label = Label(self.counter_text, style=LayoutStyle(height=30))
        print(f"✅ 创建了counter_label with reactive binding: {counter_label}")
        
        # 🆕 特性5: 有点击事件的按钮
        button = Button("点击增加", 
                       style=LayoutStyle(width=100, height=30),
                       on_click=self._increment)
        print(f"✅ 创建了Button with click handler: {button}")
        
        # 创建VStack
        vstack = VStack(
            children=[label, counter_label, button],
            style=LayoutStyle(gap=10, padding=20)
        )
        print(f"✅ 创建了VStack: {vstack}")
        
        # 挂载VStack
        print("🔧 开始挂载VStack...")
        result = vstack.mount()
        print(f"✅ VStack挂载完成: {result}")
        
        return result
    
    def _increment(self):
        """增加计数"""
        print(f"🎯 按钮被点击! 当前计数: {self.counter.value}")
        self.counter.value += 1
        print(f"🎯 计数更新为: {self.counter.value}")

def main():
    print("🚀 启动调试版showcase v5 - 完整响应式...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 调试版 v5")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 400, 300),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("macUI v3.0 调试版 v5")
        window.makeKeyAndOrderFront_(None)
        print("✅ 窗口创建成功")
        
        # 创建应用组件
        print("🔧 创建应用组件...")
        showcase = DebugShowcase5()
        
        # 挂载组件到窗口
        print("🔧 挂载组件到窗口...")
        content_view = showcase.mount()
        window.setContentView_(content_view)
        print("✅ 组件挂载成功")
        
        # 启动事件循环
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()