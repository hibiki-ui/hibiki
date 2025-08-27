#!/usr/bin/env python3
"""macUI v3.0 动画API简单示例

展示如何使用macUI动画系统的各种功能。
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import Signal
from macui.components import Label, Button, VStack, LayoutStyle
from macui.app import create_app
from macui.core import Component
from macui.animation import animate, ShinyText, TypeWriter, FadeIn, SlideIn, Scale

from AppKit import *
from PyObjCTools import AppHelper


class SimpleAnimationDemo(Component):
    """简单动画演示"""
    
    def __init__(self):
        super().__init__()
        self.status = Signal("点击按钮看动画")
    
    def mount(self):
        # 标题
        title = Label("🎬 macUI动画系统", style=LayoutStyle(height=40))
        
        # 演示文本
        self.demo_text = Label("这是演示文本", style=LayoutStyle(height=60))
        
        # 状态显示
        status_label = Label(self.status.value, style=LayoutStyle(height=30))
        
        # 动画按钮
        shiny_btn = Button("✨ 闪光", style=LayoutStyle(width=100, height=35), 
                          on_click=self._demo_shiny)
        
        fade_btn = Button("🌅 淡入", style=LayoutStyle(width=100, height=35),
                         on_click=self._demo_fade)
        
        scale_btn = Button("🔍 缩放", style=LayoutStyle(width=100, height=35),
                          on_click=self._demo_scale)
        
        # 布局
        container = VStack(
            children=[title, self.demo_text, status_label, shiny_btn, fade_btn, scale_btn],
            style=LayoutStyle(gap=15, padding=25)
        )
        
        return container.mount()
    
    def _demo_shiny(self):
        """闪光效果演示"""
        self.status.value = "✨ 闪光动画中..."
        if hasattr(self, 'demo_text') and self.demo_text._nsview:
            shiny = ShinyText(duration=2.0, repeat=False)
            shiny.apply_to(self.demo_text._nsview)
    
    def _demo_fade(self):
        """淡入效果演示"""
        self.status.value = "🌅 淡入动画中..."
        if hasattr(self, 'demo_text') and self.demo_text._nsview:
            fade = FadeIn(duration=1.0)
            fade.apply_to(self.demo_text._nsview)
    
    def _demo_scale(self):
        """缩放效果演示"""
        self.status.value = "🔍 缩放动画中..."
        if hasattr(self, 'demo_text') and self.demo_text._nsview:
            scale = Scale(duration=1.0, from_scale=0.5, to_scale=1.2)
            scale.apply_to(self.demo_text._nsview)


def main():
    """主函数"""
    print("🎬 启动简单动画演示...")
    
    # 创建应用
    app = create_app("macUI动画演示")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 400, 300),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("macUI动画演示")
    window.makeKeyAndOrderFront_(None)
    
    # 创建演示组件
    demo = SimpleAnimationDemo()
    content_view = demo.mount()
    window.setContentView_(content_view)
    
    print("✅ 动画演示启动成功!")
    print("🎯 尝试点击不同按钮体验动画效果")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()