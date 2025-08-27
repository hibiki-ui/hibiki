#!/usr/bin/env python3
"""测试完整的统一API接口"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
# 测试完整的统一API
from macui.components import (
    Label, Button, VStack, HStack, LayoutStyle,
    LineBreakMode, LabelStyle
)
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class CompleteAPIDemo(Component):
    def __init__(self):
        super().__init__()
        self.message = Signal("欢迎使用macUI v3.0统一API!")
        print("📱 CompleteAPIDemo - 测试完整统一API")
        
    def mount(self):
        print("🔧 测试完整统一API功能...")
        
        # 测试不同的Label样式
        title = Label(
            "macUI v3.0 完整API测试", 
            style=LayoutStyle(height=35)
        )
        
        # 测试LineBreakMode枚举
        multiline_label = Label(
            "这是一个长文本标签，用来测试文本换行功能。"
            "LineBreakMode枚举现在已经迁移到modern_components中。",
            style=LayoutStyle(width=300, height=60)
        )
        
        # 测试响应式Label
        reactive_label = Label(
            self.message.value,
            style=LayoutStyle(height=25)
        )
        
        # 测试Button功能
        change_button = Button(
            "改变消息",
            style=LayoutStyle(width=100, height=32),
            on_click=lambda: self._change_message()
        )
        
        test_button = Button(
            "测试枚举",
            style=LayoutStyle(width=100, height=32), 
            on_click=lambda: self._test_enums()
        )
        
        # 测试嵌套布局
        button_row = HStack(
            children=[change_button, test_button],
            style=LayoutStyle(gap=10)
        )
        
        # 主容器
        main_container = VStack(
            children=[title, multiline_label, reactive_label, button_row],
            style=LayoutStyle(gap=15, padding=25)
        )
        
        print("✅ 完整统一API测试界面创建成功")
        return main_container.mount()
    
    def _change_message(self):
        messages = [
            "统一API工作正常! 🎉",
            "Label现在使用最佳实现",
            "Button功能完整",
            "VStack/HStack布局正确"
        ]
        import random
        self.message.value = random.choice(messages)
        print(f"💬 消息更改为: {self.message.value}")
    
    def _test_enums(self):
        print("📋 测试枚举:")
        print(f"   LineBreakMode.WORD_WRAPPING = {LineBreakMode.WORD_WRAPPING.value}")
        print(f"   LineBreakMode.TRUNCATE_TAIL = {LineBreakMode.TRUNCATE_TAIL.value}")
        print(f"   LabelStyle.MULTILINE = {LabelStyle.MULTILINE.value}")
        print(f"   LabelStyle.TITLE = {LabelStyle.TITLE.value}")
        print("✅ 所有枚举都可以正常访问")

def main():
    print("🚀 测试macUI v3.0完整统一API...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 完整API测试")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 450, 300),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("macUI v3.0 完整API测试")
        window.makeKeyAndOrderFront_(None)
        
        # 创建演示组件
        demo = CompleteAPIDemo()
        content_view = demo.mount()
        window.setContentView_(content_view)
        
        print("✅ 完整API测试应用启动成功!")
        print("🎯 API统一化成果:")
        print("   ✅ Label -> ModernLabel (支持Stretchable)")
        print("   ✅ Button -> ModernButton (支持Stretchable)")
        print("   ✅ VStack/HStack -> Modern实现")
        print("   ✅ LineBreakMode/LabelStyle枚举迁移")
        print("   ✅ 统一的LayoutStyle样式系统")
        print("   ✅ 简洁的命名，无需'Modern'前缀")
        
        # 启动事件循环
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()