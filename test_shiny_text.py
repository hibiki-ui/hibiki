#!/usr/bin/env python3
"""测试新版ShinyText光泽扫过效果

验证基于CAGradientLayer的光泽扫过动画是否正确实现了web版本的效果。
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import Signal
from macui.components import Label, Button, VStack, LayoutStyle
from macui.app import create_app
from macui.core import Component
from macui.animation import ShinyText

from AppKit import *
from PyObjCTools import AppHelper


class ShinyTextTest(Component):
    """ShinyText光泽扫过效果测试"""
    
    def __init__(self):
        super().__init__()
        self.status = Signal("点击按钮测试光泽扫过效果")
        self.shiny_effect = None
    
    def mount(self):
        # 测试标题
        title = Label("✨ ShinyText光泽扫过测试", style=LayoutStyle(height=40))
        
        # 大号演示文本
        self.demo_text = Label("SHINY TEXT EFFECT", style=LayoutStyle(height=80))
        
        # 中文演示文本
        self.demo_text_cn = Label("闪亮文字效果", style=LayoutStyle(height=60))
        
        # 状态显示
        status_label = Label(self.status.value, style=LayoutStyle(height=30))
        
        # 测试按钮
        start_btn = Button("🌟 开始光泽扫过", style=LayoutStyle(width=150, height=35), 
                          on_click=self._start_shiny)
        
        stop_btn = Button("⏹️ 停止动画", style=LayoutStyle(width=150, height=35),
                         on_click=self._stop_shiny)
        
        fast_btn = Button("⚡ 快速扫过", style=LayoutStyle(width=150, height=35),
                         on_click=self._fast_shiny)
        
        # 布局
        container = VStack(
            children=[title, self.demo_text, self.demo_text_cn, status_label, 
                     start_btn, stop_btn, fast_btn],
            style=LayoutStyle(gap=15, padding=25)
        )
        
        return container.mount()
    
    def _start_shiny(self):
        """开始标准光泽扫过动画"""
        self.status.value = "✨ 标准光泽扫过动画运行中..."
        
        print(f"🔍 检查demo_text: {hasattr(self, 'demo_text')}")
        if hasattr(self, 'demo_text'):
            print(f"🔍 检查_nsview: {hasattr(self.demo_text, '_nsview')}")
            if hasattr(self.demo_text, '_nsview'):
                print(f"🔍 _nsview对象: {self.demo_text._nsview}")
        
        # 停止之前的动画
        if self.shiny_effect:
            self.shiny_effect.stop_animation()
        
        # 创建新的光泽效果 - 3秒周期，匹配web版本
        self.shiny_effect = ShinyText(duration=3.0, intensity=0.8)
        print(f"🔍 ShinyText对象已创建: {self.shiny_effect}")
        
        # 同时应用到两个文本
        if hasattr(self, 'demo_text') and hasattr(self.demo_text, '_nsview') and self.demo_text._nsview:
            print("🎯 正在应用ShinyText到demo_text")
            self.shiny_effect.apply_to(self.demo_text._nsview)
        else:
            print("❌ demo_text._nsview不可用")
            
        if hasattr(self, 'demo_text_cn') and hasattr(self.demo_text_cn, '_nsview') and self.demo_text_cn._nsview:
            print("🎯 正在应用ShinyText到demo_text_cn")  
            self.shiny_effect.apply_to(self.demo_text_cn._nsview)
        else:
            print("❌ demo_text_cn._nsview不可用")
    
    def _stop_shiny(self):
        """停止光泽动画"""
        self.status.value = "⏸️ 光泽动画已停止"
        
        if self.shiny_effect:
            self.shiny_effect.stop_animation()
            self.shiny_effect = None
    
    def _fast_shiny(self):
        """快速光泽扫过测试"""
        self.status.value = "⚡ 快速光泽扫过测试中..."
        
        # 停止之前的动画
        if self.shiny_effect:
            self.shiny_effect.stop_animation()
        
        # 创建快速光泽效果 - 1秒周期
        self.shiny_effect = ShinyText(duration=1.0, intensity=1.0)
        
        # 应用到演示文本
        if hasattr(self, 'demo_text') and hasattr(self.demo_text, '_nsview') and self.demo_text._nsview:
            self.shiny_effect.apply_to(self.demo_text._nsview)
        if hasattr(self, 'demo_text_cn') and hasattr(self.demo_text_cn, '_nsview') and self.demo_text_cn._nsview:
            self.shiny_effect.apply_to(self.demo_text_cn._nsview)


def main():
    """主函数"""
    print("✨ 启动ShinyText光泽扫过效果测试...")
    
    # 创建应用
    app = create_app("ShinyText测试")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 500, 450),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("ShinyText光泽扫过测试")
    window.makeKeyAndOrderFront_(None)
    
    # 创建测试组件
    test = ShinyTextTest()
    content_view = test.mount()
    window.setContentView_(content_view)
    
    print("✅ ShinyText测试启动成功!")
    print("🎯 点击按钮测试不同的光泽扫过效果")
    print("📝 观察CAGradientLayer光泽扫过是否符合web版本效果")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()