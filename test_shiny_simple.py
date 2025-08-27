#!/usr/bin/env python3
"""简单测试ShinyText的不同实现方案

尝试更接近Claude Code CLI的shiny text效果
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper
from Quartz import *


class SimpleShinyText:
    """更简单的ShinyText实现 - 直接修改文字颜色"""
    
    def __init__(self, duration=3.0):
        self.duration = duration
        self._text_layer = None
        self._original_color = None
    
    def apply_to(self, text_field):
        """应用简单的颜色变化动画"""
        print(f"🔄 应用简单ShinyText到: {text_field}")
        
        # 确保有layer
        text_field.setWantsLayer_(True)
        layer = text_field.layer()
        
        # 保存原始颜色
        self._original_color = text_field.textColor()
        
        # 创建颜色动画 - 从原色到亮色再回到原色
        color_animation = CAKeyframeAnimation.animationWithKeyPath_("backgroundColor")
        
        # 准备颜色值
        original = self._original_color.CGColor()
        bright = NSColor.colorWithRed_green_blue_alpha_(1.0, 1.0, 1.0, 0.3).CGColor()
        
        # 设置关键帧
        color_animation.setValues_([original, bright, original])
        color_animation.setKeyTimes_([0.0, 0.5, 1.0])
        color_animation.setDuration_(self.duration)
        color_animation.setRepeatCount_(float('inf'))
        
        # 应用到layer
        layer.addAnimation_forKey_(color_animation, "shinyColor")
        
        print("✨ 简单颜色动画已启动")


def main():
    """主函数"""
    print("🧪 测试简单ShinyText实现...")
    
    # 创建应用
    app = create_app("简单ShinyText测试")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 600, 400),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("简单ShinyText测试")
    window.makeKeyAndOrderFront_(None)
    
    # 创建主容器
    content_view = NSView.alloc().init()
    content_view.setFrame_(NSMakeRect(0, 0, 600, 400))
    window.setContentView_(content_view)
    
    # 创建文本标签 - 使用不同的方法
    y_pos = 320
    
    # 方法1: 基础文字 + 背景动画
    label1 = NSTextField.alloc().init()
    label1.setFrame_(NSMakeRect(50, y_pos, 500, 40))
    label1.setStringValue_("Method 1: Background Color Animation")
    label1.setEditable_(False)
    label1.setSelectable_(False)
    label1.setBezeled_(False)
    label1.setDrawsBackground_(True)
    label1.setBackgroundColor_(NSColor.clearColor())
    label1.setFont_(NSFont.boldSystemFontOfSize_(18))
    content_view.addSubview_(label1)
    
    # 应用简单动画
    simple1 = SimpleShinyText(duration=2.0)
    simple1.apply_to(label1)
    
    y_pos -= 60
    
    # 方法2: 创建CATextLayer测试
    text_layer = CATextLayer.layer()
    text_layer.setFrame_(NSMakeRect(50, y_pos, 500, 40))
    text_layer.setString_("Method 2: CATextLayer with Gradient")
    text_layer.setFont_(NSFont.boldSystemFontOfSize_(18))
    text_layer.setFontSize_(18)
    text_layer.setAlignmentMode_("left")
    content_view.layer().addSublayer_(text_layer)
    
    # 为CATextLayer添加渐变动画
    gradient = CAGradientLayer.layer()
    gradient.setFrame_(text_layer.frame())
    
    # 设置渐变颜色
    transparent = NSColor.colorWithRed_green_blue_alpha_(0.0, 0.0, 0.0, 0.0).CGColor()
    highlight = NSColor.colorWithRed_green_blue_alpha_(1.0, 1.0, 0.0, 0.5).CGColor()  # 黄色高亮
    
    gradient.setColors_([transparent, highlight, transparent])
    gradient.setLocations_([0.0, 0.5, 1.0])
    gradient.setStartPoint_((0.0, 0.5))
    gradient.setEndPoint_((1.0, 0.5))
    
    # 位置动画
    pos_anim = CABasicAnimation.animationWithKeyPath_("position.x")
    pos_anim.setFromValue_(-200)
    pos_anim.setToValue_(700)
    pos_anim.setDuration_(3.0)
    pos_anim.setRepeatCount_(float('inf'))
    
    content_view.layer().addSublayer_(gradient)
    gradient.addAnimation_forKey_(pos_anim, "sweep")
    
    y_pos -= 80
    
    # 方法3: 使用当前的ShinyText
    from macui.animation import ShinyText
    
    label3 = NSTextField.alloc().init()
    label3.setFrame_(NSMakeRect(50, y_pos, 500, 40))
    label3.setStringValue_("Method 3: Current ShinyText Implementation")
    label3.setEditable_(False)
    label3.setSelectable_(False)
    label3.setBezeled_(False)
    label3.setDrawsBackground_(False)
    label3.setFont_(NSFont.boldSystemFontOfSize_(18))
    content_view.addSubview_(label3)
    
    # 应用当前的ShinyText
    shiny3 = ShinyText(duration=3.0, intensity=0.8)
    shiny3.apply_to(label3)
    
    print("✅ 三种不同的ShinyText实现已启动")
    print("🔍 比较不同方法的视觉效果")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()