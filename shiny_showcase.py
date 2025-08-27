#!/usr/bin/env python3
"""ShinyText光泽扫过效果完整展示

展示基于CAGradientLayer的光泽扫过动画的各种参数和效果配置。
模拟web版本的光泽扫过效果: https://reactbits.dev/text-animations/shiny-text
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.animation import ShinyText
from macui.app import create_app

from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper


def create_text_label(text, frame, font_size=18):
    """创建标准文本标签"""
    label = NSTextField.alloc().init()
    label.setFrame_(frame)
    label.setStringValue_(text)
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setFont_(NSFont.boldSystemFontOfSize_(font_size))
    label.setAlignment_(NSTextAlignmentCenter)
    return label


def create_description_label(text, frame):
    """创建描述标签"""
    label = NSTextField.alloc().init()
    label.setFrame_(frame)
    label.setStringValue_(text)
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setFont_(NSFont.systemFontOfSize_(12))
    label.setAlignment_(NSTextAlignmentCenter)
    label.setTextColor_(NSColor.secondaryLabelColor())
    return label


class ShinyShowcase:
    """ShinyText展示应用"""
    
    def __init__(self):
        self.effects = []
        self.labels = []
    
    def setup_ui(self):
        """设置用户界面"""
        print("🎬 设置ShinyText展示界面...")
        
        # 创建应用和窗口
        app = create_app("ShinyText光泽扫过展示")
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 800, 700),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("ShinyText光泽扫过效果展示")
        self.window.makeKeyAndOrderFront_(None)
        
        # 主容器
        self.content_view = NSView.alloc().init()
        self.content_view.setFrame_(NSMakeRect(0, 0, 800, 700))
        self.window.setContentView_(self.content_view)
        
        # 标题
        title_label = create_text_label("✨ ShinyText光泽扫过效果展示", NSMakeRect(0, 650, 800, 40), 24)
        title_label.setTextColor_(NSColor.labelColor())
        self.content_view.addSubview_(title_label)
        
        # 子标题
        subtitle = create_description_label("CSS风格实现：background-clip: text + background-position动画", NSMakeRect(0, 620, 800, 20))
        self.content_view.addSubview_(subtitle)
        
        # 创建不同参数的演示
        self._create_demo_sections()
        
        # 控制按钮
        self._create_control_buttons()
        
    def _create_demo_sections(self):
        """创建演示区块"""
        y_pos = 570
        
        # 1. CSS默认效果 (speed=5s)
        self._add_demo_section(
            "CSS默认效果 (speed=5.0s)", 
            "SHINY TEXT EFFECT", 
            y_pos,
            ShinyText(speed=5.0, intensity=0.8)
        )
        y_pos -= 80
        
        # 2. 快速效果 (speed=2s)
        self._add_demo_section(
            "快速扫过 (speed=2.0s)", 
            "FAST SHINE", 
            y_pos,
            ShinyText(speed=2.0, intensity=0.9)
        )
        y_pos -= 80
        
        # 3. 慢速效果 (speed=8s)
        self._add_demo_section(
            "慢速扫过 (speed=8.0s)", 
            "SLOW SHINE", 
            y_pos,
            ShinyText(speed=8.0, intensity=0.7)
        )
        y_pos -= 80
        
        # 4. 高强度效果
        self._add_demo_section(
            "高强度光泽 (intensity=1.0)", 
            "BRIGHT SHINE", 
            y_pos,
            ShinyText(speed=4.0, intensity=1.0)
        )
        y_pos -= 80
        
        # 5. 中文文本
        self._add_demo_section(
            "中文光泽效果", 
            "闪亮的中文文字", 
            y_pos,
            ShinyText(speed=6.0, intensity=0.8),
            font_size=20
        )
        y_pos -= 80
        
        # 6. 禁用对比
        self._add_demo_section(
            "禁用对比 (disabled=True)", 
            "DISABLED TEXT", 
            y_pos,
            ShinyText(speed=5.0, disabled=True)
        )
        
    def _add_demo_section(self, title, text, y_pos, shiny_effect, font_size=18):
        """添加演示区块"""
        # 描述标签
        desc_label = create_description_label(title, NSMakeRect(50, y_pos + 25, 300, 20))
        self.content_view.addSubview_(desc_label)
        
        # 文本标签
        text_label = create_text_label(text, NSMakeRect(50, y_pos, 700, 30), font_size)
        self.content_view.addSubview_(text_label)
        
        # 保存引用
        self.labels.append(text_label)
        self.effects.append(shiny_effect)
    
    def _create_control_buttons(self):
        """创建控制按钮"""
        y_pos = 50
        
        # 开始所有动画按钮
        start_all_btn = NSButton.alloc().init()
        start_all_btn.setFrame_(NSMakeRect(150, y_pos, 120, 35))
        start_all_btn.setTitle_("🌟 开始所有动画")
        start_all_btn.setButtonType_(NSMomentaryPushInButton)
        start_all_btn.setTarget_(self)
        start_all_btn.setAction_("startAllAnimations:")
        self.content_view.addSubview_(start_all_btn)
        
        # 停止所有动画按钮
        stop_all_btn = NSButton.alloc().init()
        stop_all_btn.setFrame_(NSMakeRect(300, y_pos, 120, 35))
        stop_all_btn.setTitle_("⏹️ 停止所有动画")
        stop_all_btn.setButtonType_(NSMomentaryPushInButton)
        stop_all_btn.setTarget_(self)
        stop_all_btn.setAction_("stopAllAnimations:")
        self.content_view.addSubview_(stop_all_btn)
        
        # 重启动画按钮
        restart_btn = NSButton.alloc().init()
        restart_btn.setFrame_(NSMakeRect(450, y_pos, 120, 35))
        restart_btn.setTitle_("🔄 重启动画")
        restart_btn.setButtonType_(NSMomentaryPushInButton)
        restart_btn.setTarget_(self)
        restart_btn.setAction_("restartAnimations:")
        self.content_view.addSubview_(restart_btn)
        
    def startAllAnimations_(self, sender):
        """开始所有动画"""
        print("🌟 开始所有ShinyText动画...")
        for i, (label, effect) in enumerate(zip(self.labels, self.effects)):
            print(f"  🎯 启动动画 {i+1}: {effect}")
            effect.apply_to(label)
    
    def stopAllAnimations_(self, sender):
        """停止所有动画"""
        print("⏹️ 停止所有ShinyText动画...")
        for i, effect in enumerate(self.effects):
            print(f"  🛑 停止动画 {i+1}")
            effect.stop_animation()
    
    def restartAnimations_(self, sender):
        """重启动画"""
        print("🔄 重启所有动画...")
        self.stopAllAnimations_(sender)
        # 延迟一点再启动
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.1, self, "startAllAnimations:", None, False
        )


def main():
    """主函数"""
    print("✨ 启动ShinyText光泽扫过效果展示...")
    
    # 创建展示应用
    showcase = ShinyShowcase()
    showcase.setup_ui()
    
    print("✅ 界面创建完成")
    print("🎬 展示包含以下效果:")
    print("   • CSS默认效果 (5秒周期)")
    print("   • 快速扫过 (2秒周期)")
    print("   • 慢速扫过 (8秒周期)")
    print("   • 高强度光泽")
    print("   • 中文文字效果")
    print("   • 禁用对比")
    print("🎯 点击按钮控制动画播放")
    print("✨ 完全对照CSS实现：background-clip: text + background-position动画！")
    
    # 自动启动所有动画
    print("🚀 自动启动所有动画...")
    showcase.startAllAnimations_(None)
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()