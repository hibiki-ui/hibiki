#!/usr/bin/env python3
"""macUI v3.0 动画效果展示

展示macUI动画系统的各种功能：
- Shiny Text 闪亮文字
- TypeWriter 打字机效果  
- Scale & Fade 缩放淡入
- Slide In 滑入动画
- Shake 抖动效果
- 响应式动画绑定
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import Signal, Computed, Effect
from macui.components import Label, Button, VStack, HStack, LayoutStyle
from macui.layout.styles import JustifyContent, AlignItems
from macui.app import create_app
from macui.core import Component
from macui.animation import ShinyText, TypeWriter, FadeIn, SlideIn, Scale, Shake, animate

from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper
import threading
import time


class AnimationShowcase(Component):
    """动画效果展示应用"""
    
    def __init__(self):
        super().__init__()
        
        # 动画控制状态
        self.current_demo = Signal("欢迎使用macUI动画系统")
        self.animation_progress = Signal(0.0)
        self.is_animating = Signal(False)
        
        # 演示文本
        self.demo_texts = [
            "✨ 这是闪亮文字效果",
            "⌨️ 打字机效果演示文本", 
            "🎭 缩放和淡入组合",
            "➡️ 滑入动画展示",
            "🤳 抖动引起注意"
        ]
        self.current_text_index = Signal(0)
        
        # 计算属性
        self.status_text = Computed(lambda: 
            f"状态: {'动画中' if self.is_animating.value else '待机'} | 进度: {self.animation_progress.value:.0f}%"
        )
    
    def mount(self):
        """创建动画展示界面"""
        print("🎬 AnimationShowcase.mount() 开始...")
        
        # 🎯 标题
        title = Label(
            "🎬 macUI v3.0 动画系统展示",
            style=LayoutStyle(height=50)
        )
        
        # 📱 主演示区域
        self.demo_label = Label(
            self.current_demo.value,
            style=LayoutStyle(height=80, width=400)
        )
        
        # 🎮 动画控制按钮
        shiny_btn = Button(
            "✨ 闪亮文字",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_shiny_text
        )
        
        typewriter_btn = Button(
            "⌨️ 打字机",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_typewriter
        )
        
        scale_btn = Button(
            "🎭 缩放淡入",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_scale_fade
        )
        
        slide_btn = Button(
            "➡️ 滑入动画",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_slide_in
        )
        
        shake_btn = Button(
            "🤳 抖动效果",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_shake
        )
        
        combo_btn = Button(
            "🎆 组合动画",
            style=LayoutStyle(width=120, height=35),
            on_click=self._demo_combo
        )
        
        # 按钮组 - 两行布局
        button_row1 = HStack(
            children=[shiny_btn, typewriter_btn, scale_btn],
            style=LayoutStyle(gap=15, justify_content=JustifyContent.CENTER)
        )
        
        button_row2 = HStack(
            children=[slide_btn, shake_btn, combo_btn],
            style=LayoutStyle(gap=15, justify_content=JustifyContent.CENTER)
        )
        
        # 📊 状态显示
        status_label = Label(
            self.status_text.value,
            style=LayoutStyle(height=30)
        )
        
        # 🎨 响应式动画演示
        reactive_section = VStack(
            children=[
                Label("🔄 响应式动画演示:", style=LayoutStyle(height=25)),
                Label(f"当前文本索引: {self.current_text_index.value}", style=LayoutStyle(height=25)),
                Button("🔄 循环文本", style=LayoutStyle(width=100, height=30),
                      on_click=self._cycle_text)
            ],
            style=LayoutStyle(gap=8, padding=10)
        )
        
        # 📋 动画系统特性
        features = VStack(
            children=[
                Label("🏗️ macUI动画系统特性:", style=LayoutStyle(height=25)),
                Label("• Core Animation 硬件加速", style=LayoutStyle(height=20)),
                Label("• 声明式API设计", style=LayoutStyle(height=20)),
                Label("• Signal响应式集成", style=LayoutStyle(height=20)),
                Label("• 预设动画效果库", style=LayoutStyle(height=20)),
                Label("• 链式动画组合", style=LayoutStyle(height=20))
            ],
            style=LayoutStyle(gap=3, padding=15)
        )
        
        # 🏗️ 主容器
        main_container = VStack(
            children=[
                title,
                self.demo_label,
                status_label,
                button_row1,
                button_row2,
                reactive_section,
                features
            ],
            style=LayoutStyle(
                gap=20,
                padding=30,
                align_items=AlignItems.CENTER
            )
        )
        
        # 设置响应式动画
        self._setup_reactive_animations()
        
        print("✅ AnimationShowcase界面创建完成")
        return main_container.mount()
    
    def _setup_reactive_animations(self):
        """设置响应式动画"""
        # 文本变化时的动画
        def on_text_change():
            text = self.demo_texts[self.current_text_index.value % len(self.demo_texts)]
            self.current_demo.value = text
            
            # 获取Label的NSView并应用动画
            if hasattr(self, 'demo_label') and self.demo_label._nsview:
                # 先淡出再淡入
                animate(self.demo_label._nsview, duration=0.3, opacity=0.3)
                def fade_back():
                    time.sleep(0.3)
                    animate(self.demo_label._nsview, duration=0.3, opacity=1.0)
                threading.Thread(target=fade_back, daemon=True).start()
        
        # 创建Effect来响应文本变化
        Effect(on_text_change)
    
    def _demo_shiny_text(self):
        """演示闪亮文字效果"""
        print("✨ 开始闪亮文字演示")
        self.is_animating.value = True
        self.current_demo.value = "✨ 这就是闪亮文字效果！"
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            shiny = ShinyText(duration=3.0, repeat=False)
            shiny.apply_to(self.demo_label._nsview)
            
            # 动画完成后重置状态
            def reset_state():
                time.sleep(3.0)
                self.is_animating.value = False
                self.animation_progress.value = 100.0
            threading.Thread(target=reset_state, daemon=True).start()
    
    def _demo_typewriter(self):
        """演示打字机效果"""
        print("⌨️ 开始打字机演示")
        self.is_animating.value = True
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            typewriter = TypeWriter("⌨️ 这是打字机效果演示，逐字显示文本内容...", duration=4.0)
            typewriter.apply_to(self.demo_label._nsview)
            
            def reset_state():
                time.sleep(4.0)
                self.is_animating.value = False
            threading.Thread(target=reset_state, daemon=True).start()
    
    def _demo_scale_fade(self):
        """演示缩放淡入效果"""
        print("🎭 开始缩放淡入演示")
        self.is_animating.value = True
        self.current_demo.value = "🎭 缩放淡入组合效果"
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            # 组合缩放和淡入
            scale = Scale(duration=1.0, from_scale=0.5, to_scale=1.2)
            fade = FadeIn(duration=1.0, from_opacity=0.0)
            
            scale.apply_to(self.demo_label._nsview)
            fade.apply_to(self.demo_label._nsview)
            
            def reset_state():
                time.sleep(1.5)
                self.is_animating.value = False
            threading.Thread(target=reset_state, daemon=True).start()
    
    def _demo_slide_in(self):
        """演示滑入动画"""
        print("➡️ 开始滑入动画演示")
        self.is_animating.value = True
        self.current_demo.value = "➡️ 从左侧滑入的文字"
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            slide = SlideIn(duration=1.0, direction="left", distance=200.0)
            slide.apply_to(self.demo_label._nsview)
            
            def reset_state():
                time.sleep(1.5)
                self.is_animating.value = False
            threading.Thread(target=reset_state, daemon=True).start()
    
    def _demo_shake(self):
        """演示抖动效果"""
        print("🤳 开始抖动演示")
        self.is_animating.value = True
        self.current_demo.value = "🤳 注意！我在抖动！"
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            shake = Shake(duration=1.0, intensity=15.0, repeat_count=4)
            shake.apply_to(self.demo_label._nsview)
            
            def reset_state():
                time.sleep(1.5)
                self.is_animating.value = False
            threading.Thread(target=reset_state, daemon=True).start()
    
    def _demo_combo(self):
        """演示组合动画"""
        print("🎆 开始组合动画演示")
        self.is_animating.value = True
        self.current_demo.value = "🎆 多种效果的华丽组合！"
        
        if hasattr(self, 'demo_label') and self.demo_label._nsview:
            # 连续应用多种效果
            def combo_sequence():
                # 1. 淡入 + 缩放
                scale = Scale(duration=0.5, from_scale=0.0, to_scale=1.0)
                fade = FadeIn(duration=0.5)
                scale.apply_to(self.demo_label._nsview)
                fade.apply_to(self.demo_label._nsview)
                
                time.sleep(0.8)
                
                # 2. 轻微抖动
                shake = Shake(duration=0.5, intensity=5.0, repeat_count=2)
                shake.apply_to(self.demo_label._nsview)
                
                time.sleep(1.0)
                
                # 3. 闪亮效果
                shiny = ShinyText(duration=2.0, repeat=False)
                shiny.apply_to(self.demo_label._nsview)
                
                time.sleep(2.5)
                self.is_animating.value = False
            
            threading.Thread(target=combo_sequence, daemon=True).start()
    
    def _cycle_text(self):
        """循环切换文本"""
        self.current_text_index.value = (self.current_text_index.value + 1) % len(self.demo_texts)
        print(f"🔄 切换到文本 {self.current_text_index.value}: {self.demo_texts[self.current_text_index.value]}")


def main():
    """主函数"""
    print("🎬 启动macUI动画系统展示...")
    
    try:
        # 创建应用
        app = create_app("macUI动画展示")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 800),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("macUI v3.0 动画系统展示")
        window.makeKeyAndOrderFront_(None)
        
        # 创建并挂载展示组件
        print("🔧 创建AnimationShowcase...")
        showcase = AnimationShowcase()
        print("🔧 调用showcase.mount()...")
        content_view = showcase.mount()
        print(f"✅ mount()返回: {content_view}")
        window.setContentView_(content_view)
        print("✅ 动画展示界面已设置到窗口")
        
        print("✅ macUI动画展示应用启动成功!")
        print()
        print("🎯 动画系统功能:")
        print("   ✨ ShinyText - 基于渐变遮罩的闪光效果")
        print("   ⌨️ TypeWriter - 逐字显示打字机效果")
        print("   🎭 Scale & Fade - 缩放淡入组合动画")
        print("   ➡️ SlideIn - 多方向滑入动画")
        print("   🤳 Shake - 引人注意的抖动效果")
        print("   🎆 组合动画 - 多效果链式组合")
        print("   🔄 响应式绑定 - Signal驱动的动画")
        print()
        print("🔥 技术特性:")
        print("   • Core Animation硬件加速")
        print("   • 声明式API设计")
        print("   • 与macUI响应式系统无缝集成")
        print("   • 丰富的预设动画效果")
        print("   • 支持复杂动画组合")
        
        # 启动事件循环
        print("\\n🎮 启动事件循环，体验macUI动画系统...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()