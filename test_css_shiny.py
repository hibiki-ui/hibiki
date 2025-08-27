#!/usr/bin/env python3
"""测试CSS风格的ShinyText实现

完全对照CSS源码实现的background-clip: text效果
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.animation import ShinyText
from macui.app import create_app

from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper


def main():
    """主函数"""
    print("🎨 启动CSS风格ShinyText测试...")
    print("📋 CSS参考:")
    print("   color: #b5b5b5a4")
    print("   background: linear-gradient(120deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 60%)")
    print("   background-size: 200% 100%")
    print("   background-clip: text")
    print("   animation: shine 5s linear infinite")
    
    # 创建应用
    app = create_app("CSS ShinyText测试")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 800, 600),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("CSS风格ShinyText测试")
    window.makeKeyAndOrderFront_(None)
    
    # 主容器
    content_view = NSView.alloc().init()
    content_view.setFrame_(NSMakeRect(0, 0, 800, 600))
    window.setContentView_(content_view)
    
    # 标题文字
    title = NSTextField.alloc().init()
    title.setFrame_(NSMakeRect(50, 500, 700, 60))
    title.setStringValue_("CSS SHINY TEXT EFFECT")
    title.setEditable_(False)
    title.setSelectable_(False)
    title.setBezeled_(False)
    title.setDrawsBackground_(False)
    title.setFont_(NSFont.boldSystemFontOfSize_(36))
    title.setAlignment_(NSTextAlignmentCenter)
    content_view.addSubview_(title)
    
    # 应用默认速度的ShinyText (speed=5s)
    shiny1 = ShinyText(speed=5.0, disabled=False)
    shiny1.apply_to(title)
    
    # 英文测试
    english = NSTextField.alloc().init()
    english.setFrame_(NSMakeRect(50, 420, 700, 40))
    english.setStringValue_("Background-clip text animation with gradient sweep")
    english.setEditable_(False)
    english.setSelectable_(False)
    english.setBezeled_(False)
    english.setDrawsBackground_(False)
    english.setFont_(NSFont.boldSystemFontOfSize_(24))
    english.setAlignment_(NSTextAlignmentCenter)
    content_view.addSubview_(english)
    
    # 应用快速动画 (speed=3s)
    shiny2 = ShinyText(speed=3.0, intensity=0.9)
    shiny2.apply_to(english)
    
    # 中文测试
    chinese = NSTextField.alloc().init()
    chinese.setFrame_(NSMakeRect(50, 360, 700, 40))
    chinese.setStringValue_("基于CSS背景裁剪技术的文字光泽效果")
    chinese.setEditable_(False)
    chinese.setSelectable_(False)
    chinese.setBezeled_(False)
    chinese.setDrawsBackground_(False)
    chinese.setFont_(NSFont.boldSystemFontOfSize_(22))
    chinese.setAlignment_(NSTextAlignmentCenter)
    content_view.addSubview_(chinese)
    
    # 应用慢速动画 (speed=7s)
    shiny3 = ShinyText(speed=7.0, intensity=0.7)
    shiny3.apply_to(chinese)
    
    # 参数说明
    desc1 = NSTextField.alloc().init()
    desc1.setFrame_(NSMakeRect(50, 280, 700, 60))
    desc1.setStringValue_("实现要点：\n1. 基础文字颜色：#b5b5b5a4 (半透明灰色)\n2. 渐变背景：120度角，40%-50%-60%位置的白色高亮\n3. 背景尺寸：200%宽度，允许动画扫过")
    desc1.setEditable_(False)
    desc1.setSelectable_(False)
    desc1.setBezeled_(False)
    desc1.setDrawsBackground_(False)
    desc1.setFont_(NSFont.systemFontOfSize_(14))
    desc1.setTextColor_(NSColor.secondaryLabelColor())
    desc1.setUsesSingleLineMode_(False)
    desc1.setLineBreakMode_(NSLineBreakByWordWrapping)
    content_view.addSubview_(desc1)
    
    # 技术说明
    desc2 = NSTextField.alloc().init()
    desc2.setFrame_(NSMakeRect(50, 180, 700, 80))
    desc2.setStringValue_("Core Animation映射：\n• CSS background-clip: text → CAGradientLayer作为mask\n• CSS background-position动画 → position.x动画\n• CSS linear timing → CAMediaTimingFunction linear\n• CSS 200% background-size → 2倍宽度的gradient layer")
    desc2.setEditable_(False)
    desc2.setSelectable_(False)
    desc2.setBezeled_(False)
    desc2.setDrawsBackground_(False)
    desc2.setFont_(NSFont.systemFontOfSize_(12))
    desc2.setTextColor_(NSColor.tertiaryLabelColor())
    desc2.setUsesSingleLineMode_(False)
    desc2.setLineBreakMode_(NSLineBreakByWordWrapping)
    content_view.addSubview_(desc2)
    
    # 控制按钮
    stop_btn = NSButton.alloc().init()
    stop_btn.setFrame_(NSMakeRect(300, 100, 100, 35))
    stop_btn.setTitle_("停止动画")
    stop_btn.setButtonType_(NSMomentaryPushInButton)
    content_view.addSubview_(stop_btn)
    
    restart_btn = NSButton.alloc().init()
    restart_btn.setFrame_(NSMakeRect(420, 100, 100, 35))
    restart_btn.setTitle_("重启动画")
    restart_btn.setButtonType_(NSMomentaryPushInButton)
    content_view.addSubview_(restart_btn)
    
    # 版本对比文字 (禁用动画)
    static_text = NSTextField.alloc().init()
    static_text.setFrame_(NSMakeRect(50, 50, 700, 30))
    static_text.setStringValue_("对比：这是禁用动画的静态文字 (disabled=True)")
    static_text.setEditable_(False)
    static_text.setSelectable_(False)
    static_text.setBezeled_(False)
    static_text.setDrawsBackground_(False)
    static_text.setFont_(NSFont.boldSystemFontOfSize_(18))
    static_text.setAlignment_(NSTextAlignmentCenter)
    content_view.addSubview_(static_text)
    
    # 应用禁用的ShinyText
    shiny_disabled = ShinyText(speed=5.0, disabled=True)
    shiny_disabled.apply_to(static_text)
    
    print("✅ CSS风格ShinyText测试已启动")
    print("🎯 观察效果是否与CSS版本一致:")
    print("   • 基础文字保持半透明灰色")
    print("   • 白色光泽从右到左扫过")
    print("   • 120度倾斜角度的渐变")
    print("   • 5秒周期的线性动画")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()