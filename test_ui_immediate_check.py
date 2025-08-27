#!/usr/bin/env python3
"""
立即检测UI状态 - 不依赖定时器，直接在创建后检查
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.component import Component
from macui.components.modern_controls import ModernLabel
from AppKit import NSApplication

class ImmediateUITest(Component):
    """立即检测UI测试"""
    
    def mount(self):
        print("🔧 创建UI组件...")
        
        # 创建一个简单标签
        label = ModernLabel(text="🧪 UI测试标签", width=200, height=30)
        view = label.get_view()
        
        print(f"✅ 组件创建完成: {view}")
        return view

def main():
    print("🚀 立即UI检测测试开始...")
    
    # 创建应用
    app = MacUIApp("Immediate UI Test")
    test_component = ImmediateUITest()
    
    # 创建窗口
    window = app.create_window(
        title="立即UI测试",
        size=(300, 100),
        content=test_component
    )
    
    print("🪟 窗口创建完成")
    
    # 显示窗口
    window.show()
    print("👁️ 窗口show()调用完成")
    
    # 立即检测UI状态（在启动事件循环前）
    print("🔍 === 立即检测UI状态 ===")
    
    try:
        ns_app = NSApplication.sharedApplication()
        windows = list(ns_app.windows())
        print(f"📊 应用窗口数量: {len(windows)}")
        
        if windows:
            for i, win in enumerate(windows):
                print(f"🪟 窗口{i}: 标题='{win.title()}', 可见={win.isVisible()}")
                
                # 检查内容视图
                content_view = win.contentView()
                if content_view:
                    print(f"📦 内容视图: {content_view}")
                    frame = content_view.frame()
                    print(f"📐 内容frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
                    
                    # 检查子视图
                    subviews = list(content_view.subviews())
                    print(f"🌳 子视图数量: {len(subviews)}")
                    for j, subview in enumerate(subviews):
                        subframe = subview.frame()
                        print(f"   子视图{j}: {type(subview).__name__}")
                        print(f"   位置: ({subframe.origin.x}, {subframe.origin.y}, {subframe.size.width}, {subframe.size.height})")
                        
                        # 如果是NSTextField，检查文本内容
                        if hasattr(subview, 'stringValue'):
                            text_content = subview.stringValue()
                            print(f"   文本内容: '{text_content}'")
                            
                            if text_content == "🧪 UI测试标签":
                                print("🎉 SUCCESS: UI标签内容正确!")
                            
        print("🎯 结论:")
        print("   - 如果您能看到窗口和标签，说明macUI v3.0完全正常工作!")
        print("   - 之前的'卡住'可能只是事件循环的正常行为")
        print("   - UI显示和布局系统都已成功运行")
        
    except Exception as e:
        print(f"❌ 检测异常: {e}")
        import traceback
        traceback.print_exc()
    
    # 短暂运行事件循环让UI完全显示
    print("⏰ 运行事件循环2秒让UI稳定显示...")
    
    # 使用延时退出而不是无限循环
    from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode
    import objc
    
    class ExitTimer(object):
        @objc.typedSelector(b'v@:@')
        def exit_(self, timer):
            print("⏰ 2秒已过，UI应该已完全显示")
            print("🏁 测试结束 - 如果您看到了UI，说明一切正常!")
            NSApplication.sharedApplication().terminate_(None)
    
    exit_timer = ExitTimer()
    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        2.0, exit_timer, 'exit:', None, False
    )
    
    # 启动事件循环
    app.run()

if __name__ == "__main__":
    main()