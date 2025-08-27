#!/usr/bin/env python3
"""调试版本的showcase"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
from macui.components.modern_components import ModernLabel, ModernButton
from macui.components.modern_layout import VStack, HStack
from macui.layout.styles import LayoutStyle, AlignItems, JustifyContent
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class DebugShowcase(Component):
    def __init__(self):
        super().__init__()
        print("📱 DebugShowcase.__init__() 调用")
        
    def mount(self):
        print("🔧 DebugShowcase.mount() 开始...")
        
        # 创建一个简单的Label
        label = ModernLabel("Hello macUI v3.0!", style=LayoutStyle(height=30))
        print(f"✅ 创建了ModernLabel: {label}")
        
        # 创建一个简单的按钮
        button = ModernButton("Click Me", style=LayoutStyle(width=100, height=30))
        print(f"✅ 创建了ModernButton: {button}")
        
        # 创建VStack
        vstack = VStack(
            children=[label, button],
            style=LayoutStyle(gap=10, padding=20)
        )
        print(f"✅ 创建了VStack: {vstack}")
        
        # 挂载VStack
        print("🔧 开始挂载VStack...")
        result = vstack.mount()
        print(f"✅ VStack挂载完成: {result}")
        
        return result

def main():
    print("🚀 启动调试版showcase...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 调试版")
        
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
        
        window.setTitle_("macUI v3.0 调试版")
        window.makeKeyAndOrderFront_(None)
        print("✅ 窗口创建成功")
        
        # 创建应用组件
        print("🔧 创建应用组件...")
        showcase = DebugShowcase()
        
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