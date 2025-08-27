#!/usr/bin/env python3
"""测试统一API接口"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
# 使用新的统一API - 简洁的命名
from macui.components import Label, Button, VStack, HStack, LayoutStyle
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class UnifiedAPIDemo(Component):
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        print("📱 UnifiedAPIDemo.__init__() - 使用统一API")
        
    def mount(self):
        print("🔧 使用统一API创建界面...")
        
        # 🎯 新的统一API - 简洁明了
        title = Label(
            "🎉 macUI v3.0 统一API", 
            style=LayoutStyle(height=40)
        )
        
        subtitle = Label(
            "Label和Button现在使用最佳实现", 
            style=LayoutStyle(height=25)
        )
        
        # 计数显示
        counter = Label(
            f"点击计数: {self.click_count.value}",
            style=LayoutStyle(height=30)
        )
        
        # 按钮组
        button1 = Button(
            "点击 +1", 
            style=LayoutStyle(width=80, height=35),
            on_click=lambda: self._increment()
        )
        
        button2 = Button(
            "重置", 
            style=LayoutStyle(width=80, height=35),
            on_click=lambda: self._reset()
        )
        
        button_row = HStack(
            children=[button1, button2],
            style=LayoutStyle(gap=15)
        )
        
        # 主容器
        main_container = VStack(
            children=[title, subtitle, counter, button_row],
            style=LayoutStyle(gap=15, padding=25)
        )
        
        print("✅ 统一API界面创建完成")
        return main_container.mount()
    
    def _increment(self):
        self.click_count.value += 1
        print(f"🔘 计数增加: {self.click_count.value}")
    
    def _reset(self):
        self.click_count.value = 0
        print("🔄 计数重置")

def main():
    print("🚀 测试macUI v3.0统一API...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 统一API测试")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 400, 250),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("macUI v3.0 统一API")
        window.makeKeyAndOrderFront_(None)
        
        # 创建演示组件
        demo = UnifiedAPIDemo()
        content_view = demo.mount()
        window.setContentView_(content_view)
        
        print("✅ 统一API测试应用启动成功!")
        print("🎯 验证内容:")
        print("   - Label现在指向ModernLabel (最佳实现)")
        print("   - Button现在指向ModernButton (最佳实现)")  
        print("   - VStack/HStack指向Modern实现")
        print("   - 用户只需要记住简洁的名称")
        
        # 启动事件循环
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()