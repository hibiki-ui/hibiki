#!/usr/bin/env python3
"""最终的ShinyText效果测试

基于对Claude Code CLI效果的理解，重新实现更自然的shiny text
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper
import math


class PerfectShinyText:
    """完美的ShinyText实现 - 模拟Claude Code CLI效果"""
    
    def __init__(self, duration=2.5, intensity=0.6):
        self.duration = duration
        self.intensity = intensity
        self._shine_layer = None
        self._animation_key = "perfectShiny"
    
    def apply_to(self, text_field):
        """应用完美的光泽扫过效果"""
        print(f"✨ 应用PerfectShinyText到: {text_field}")
        
        # 确保有layer
        text_field.setWantsLayer_(True)
        layer = text_field.layer()
        bounds = layer.bounds()
        
        # 创建光泽遮罩层 - 这次用mask的正确方式
        mask_layer = CAGradientLayer.layer()
        
        # 设置比文字更宽的遮罩，让光泽可以扫过
        mask_width = bounds.size.width * 2.5
        mask_layer.setFrame_(NSMakeRect(-bounds.size.width * 0.75, 0, mask_width, bounds.size.height))
        
        # 设置渐变 - 这是关键！
        # 大部分区域是完全不透明(显示文字)，只有一小部分是光泽高亮
        normal = NSColor.colorWithRed_green_blue_alpha_(0.0, 0.0, 0.0, 1.0).CGColor()  # 完全不透明黑
        highlight = NSColor.colorWithRed_green_blue_alpha_(1.0, 1.0, 1.0, 1.0).CGColor()  # 完全不透明白
        
        # 关键：大部分是正常显示，只有中间一小段是高亮
        mask_layer.setColors_([normal, normal, highlight, normal, normal])
        mask_layer.setLocations_([0.0, 0.45, 0.5, 0.55, 1.0])
        
        # 水平方向
        mask_layer.setStartPoint_((0.0, 0.5))
        mask_layer.setEndPoint_((1.0, 0.5))
        
        # 设置为遮罩
        layer.setMask_(mask_layer)
        self._shine_layer = mask_layer
        
        # 动画：让遮罩从左到右移动
        position_anim = CABasicAnimation.animationWithKeyPath_("position.x")
        
        start_x = -bounds.size.width * 0.5
        end_x = bounds.size.width * 1.5
        
        position_anim.setFromValue_(start_x)
        position_anim.setToValue_(end_x)
        position_anim.setDuration_(self.duration)
        position_anim.setRepeatCount_(float('inf'))
        position_anim.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_("linear")
        )
        
        mask_layer.addAnimation_forKey_(position_anim, self._animation_key)
        
        print("✨ PerfectShinyText遮罩动画已启动")
    
    def stop(self):
        if self._shine_layer:
            self._shine_layer.removeAnimationForKey_(self._animation_key)
            print("⏹️ PerfectShinyText已停止")


def main():
    """主函数"""
    print("🔮 启动Perfect ShinyText测试...")
    
    # 创建应用
    app = create_app("Perfect ShinyText")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 700, 500),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("Perfect ShinyText测试")
    window.makeKeyAndOrderFront_(None)
    
    # 主容器
    content_view = NSView.alloc().init()
    content_view.setFrame_(NSMakeRect(0, 0, 700, 500))
    window.setContentView_(content_view)
    
    # 标题
    title = NSTextField.alloc().init()
    title.setFrame_(NSMakeRect(0, 420, 700, 60))
    title.setStringValue_("PERFECT SHINY TEXT")
    title.setEditable_(False)
    title.setSelectable_(False)
    title.setBezeled_(False)
    title.setDrawsBackground_(False)
    title.setFont_(NSFont.boldSystemFontOfSize_(32))
    title.setAlignment_(NSTextAlignmentCenter)
    content_view.addSubview_(title)
    
    # 应用perfect shiny效果
    perfect1 = PerfectShinyText(duration=3.0, intensity=0.8)
    perfect1.apply_to(title)
    
    # 英文示例
    english = NSTextField.alloc().init()
    english.setFrame_(NSMakeRect(50, 340, 600, 40))
    english.setStringValue_("Shiny text animation like Claude Code CLI")
    english.setEditable_(False)
    english.setSelectable_(False)
    english.setBezeled_(False)
    english.setDrawsBackground_(False)
    english.setFont_(NSFont.boldSystemFontOfSize_(20))
    content_view.addSubview_(english)
    
    perfect2 = PerfectShinyText(duration=2.5)
    perfect2.apply_to(english)
    
    # 中文示例
    chinese = NSTextField.alloc().init()
    chinese.setFrame_(NSMakeRect(50, 280, 600, 40))
    chinese.setStringValue_("完美的光泽文字动画效果")
    chinese.setEditable_(False)
    chinese.setSelectable_(False)
    chinese.setBezeled_(False)
    chinese.setDrawsBackground_(False)
    chinese.setFont_(NSFont.boldSystemFontOfSize_(20))
    content_view.addSubview_(chinese)
    
    perfect3 = PerfectShinyText(duration=4.0)
    perfect3.apply_to(chinese)
    
    # 描述文字
    desc = NSTextField.alloc().init()
    desc.setFrame_(NSMakeRect(50, 200, 600, 60))
    desc.setStringValue_("这个实现使用遮罩层技术\n文字始终可见，光泽扫过时产生高亮效果")
    desc.setEditable_(False)
    desc.setSelectable_(False)
    desc.setBezeled_(False)
    desc.setDrawsBackground_(False)
    desc.setFont_(NSFont.systemFontOfSize_(14))
    desc.setTextColor_(NSColor.secondaryLabelColor())
    desc.setUsesSingleLineMode_(False)
    desc.setLineBreakMode_(NSLineBreakByWordWrapping)
    content_view.addSubview_(desc)
    
    print("✅ Perfect ShinyText演示已启动")
    print("🎯 观察是否更接近Claude Code CLI的效果")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()