#!/usr/bin/env python3
"""逐步增加复杂度来定位问题"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
from macui.components import Label, Button, VStack, HStack, LayoutStyle
from macui.layout.styles import JustifyContent, AlignItems
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class ComplexityTest(Component):
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        
    def mount(self):
        print("🔧 ComplexityTest.mount() 开始...")
        
        # 测试1: 单个Label（类似debug_showcase）
        print("📋 测试1: 单个Label")
        title = Label("测试标题", style=LayoutStyle(height=30))
        print(f"✅ 创建title: {title}")
        
        # 测试2: 添加Button
        print("📋 测试2: 添加Button") 
        button = Button("测试按钮", style=LayoutStyle(width=100, height=30))
        print(f"✅ 创建button: {button}")
        
        # 测试3: 简单VStack（类似debug_showcase）
        print("📋 测试3: 简单VStack")
        try:
            simple_stack = VStack(
                children=[title, button],
                style=LayoutStyle(gap=10, padding=20)
            )
            print(f"✅ 创建simple_stack: {simple_stack}")
        except Exception as e:
            print(f"❌ 简单VStack创建失败: {e}")
            return None
        
        # 测试4: 添加HStack嵌套
        print("📋 测试4: 添加HStack嵌套")
        try:
            button1 = Button("按钮1", style=LayoutStyle(width=80, height=30))
            button2 = Button("按钮2", style=LayoutStyle(width=80, height=30))
            
            button_row = HStack(
                children=[button1, button2],
                style=LayoutStyle(gap=10)
            )
            print(f"✅ 创建button_row: {button_row}")
        except Exception as e:
            print(f"❌ HStack创建失败: {e}")
            return simple_stack.mount()
        
        # 测试5: VStack嵌套HStack
        print("📋 测试5: VStack嵌套HStack")  
        try:
            nested_stack = VStack(
                children=[title, button_row],
                style=LayoutStyle(gap=15, padding=25)
            )
            print(f"✅ 创建nested_stack: {nested_stack}")
        except Exception as e:
            print(f"❌ 嵌套VStack创建失败: {e}")
            return simple_stack.mount()
        
        # 测试6: 挂载复杂布局
        print("📋 测试6: 挂载复杂布局")
        try:
            result = nested_stack.mount()
            print(f"✅ 复杂布局挂载成功: {result}")
            return result
        except Exception as e:
            print(f"❌ 复杂布局挂载失败: {e}")
            import traceback
            traceback.print_exc()
            return simple_stack.mount()

def main():
    print("🚀 启动复杂度测试...")
    
    try:
        app = create_app("复杂度测试")
        
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 400, 300),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("复杂度测试")
        window.makeKeyAndOrderFront_(None)
        
        test = ComplexityTest()
        content_view = test.mount()
        
        if content_view:
            window.setContentView_(content_view)
            print("✅ 测试成功，启动UI")
        else:
            print("❌ 测试失败")
            return
        
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()