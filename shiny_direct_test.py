#!/usr/bin/env python3
"""直接测试ShinyText效果

不依赖复杂组件系统，直接创建NSTextField并应用ShinyText效果。
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.animation import ShinyText
from macui.app import create_app

from AppKit import *
from PyObjCTools import AppHelper


def main():
    """主函数"""
    print("✨ 启动直接ShinyText测试...")
    
    # 创建应用
    app = create_app("直接ShinyText测试")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 500, 300),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("直接ShinyText测试")
    window.makeKeyAndOrderFront_(None)
    
    # 创建主容器视图
    content_view = NSView.alloc().init()
    content_view.setFrame_(NSMakeRect(0, 0, 500, 300))
    window.setContentView_(content_view)
    
    # 创建文本标签
    text_label = NSTextField.alloc().init()
    text_label.setFrame_(NSMakeRect(50, 150, 400, 60))
    text_label.setStringValue_("SHINY TEXT ANIMATION")
    text_label.setEditable_(False)
    text_label.setSelectable_(False)
    text_label.setBezeled_(False)
    text_label.setDrawsBackground_(False)
    text_label.setFont_(NSFont.boldSystemFontOfSize_(24))
    text_label.setAlignment_(NSTextAlignmentCenter)
    
    # 添加到容器
    content_view.addSubview_(text_label)
    
    # 创建中文标签
    chinese_label = NSTextField.alloc().init()
    chinese_label.setFrame_(NSMakeRect(50, 100, 400, 40))
    chinese_label.setStringValue_("闪亮文字效果测试")
    chinese_label.setEditable_(False)
    chinese_label.setSelectable_(False)
    chinese_label.setBezeled_(False)
    chinese_label.setDrawsBackground_(False)
    chinese_label.setFont_(NSFont.boldSystemFontOfSize_(20))
    chinese_label.setAlignment_(NSTextAlignmentCenter)
    
    # 添加到容器
    content_view.addSubview_(chinese_label)
    
    # 创建按钮
    start_button = NSButton.alloc().init()
    start_button.setFrame_(NSMakeRect(200, 50, 100, 30))
    start_button.setTitle_("开始动画")
    start_button.setButtonType_(NSMomentaryPushInButton)
    
    content_view.addSubview_(start_button)
    
    print("✅ UI创建完成，准备应用ShinyText效果")
    
    # 直接创建ShinyText效果并应用
    shiny_effect = ShinyText(duration=3.0, intensity=0.8)
    print(f"🔍 ShinyText对象: {shiny_effect}")
    
    # 应用到英文标签
    print("🎯 应用到英文标签...")
    animation1 = shiny_effect.apply_to(text_label)
    
    # 创建另一个效果应用到中文标签
    shiny_effect2 = ShinyText(duration=2.0, intensity=1.0)
    print("🎯 应用到中文标签...")
    animation2 = shiny_effect2.apply_to(chinese_label)
    
    print("✅ 动画已应用，观察光泽扫过效果")
    print("📝 应该能看到两个文本标签上的光泽扫过动画")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()