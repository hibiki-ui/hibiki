#!/usr/bin/env python3
"""
简化的布局调试测试 - 专注于发现布局问题
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack
from macui.components.modern_controls import ModernLabel
from macui.layout.debug import generate_debug_report
from Foundation import NSTimer
from AppKit import NSApplication
import objc

class LayoutDebugTest(Component):
    """布局调试测试 - 最简化版本"""
    
    def mount(self):
        print("🔧 创建简化布局测试...")
        
        # 只创建两个简单的标签
        label1 = ModernLabel(text="标签1", width=100, height=30)
        label2 = ModernLabel(text="标签2", width=100, height=30) 
        
        # 创建简单的垂直布局
        container = ModernVStack(
            children=[label1, label2],
            spacing=10,
            width=200,
            height=100
        )
        
        view = container.get_view()
        
        # 1.5秒后生成调试报告并退出
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.5, self, 'generateReportAndExit:', None, False
        )
        
        print("✅ 简化布局创建完成")
        return view
    
    @objc.typedSelector(b'v@:@')
    def generateReportAndExit_(self, timer):
        print("\n📊 === 生成布局调试报告 ===")
        generate_debug_report()
        
        print("\n🔍 === 手动检查NSView层次 ===")
        try:
            from AppKit import NSApplication
            app = NSApplication.sharedApplication()
            windows = list(app.windows())
            
            if windows:
                window = windows[0]
                content_view = window.contentView()
                print(f"窗口内容视图: {content_view}")
                print(f"内容视图frame: {content_view.frame()}")
                
                subviews = list(content_view.subviews())
                print(f"子视图数量: {len(subviews)}")
                
                def print_view_hierarchy(view, level=0):
                    indent = "  " * level
                    frame = view.frame()
                    print(f"{indent}{type(view).__name__}: ({frame.origin.x:.1f}, {frame.origin.y:.1f}, {frame.size.width:.1f}, {frame.size.height:.1f})")
                    
                    if hasattr(view, 'subviews'):
                        subs = list(view.subviews())
                        for sub in subs:
                            print_view_hierarchy(sub, level + 1)
                
                for i, subview in enumerate(subviews):
                    print(f"\n子视图 {i}:")
                    print_view_hierarchy(subview)
        
        except Exception as e:
            print(f"检查视图层次失败: {e}")
        
        print("\n🏁 调试测试完成，退出...")
        NSApplication.sharedApplication().terminate_(None)

def main():
    print("🚀 启动布局调试测试...")
    print("🎯 目标: 发现布局重叠问题的根本原因")
    
    app = MacUIApp("Layout Debug Test")
    test = LayoutDebugTest()
    
    window = app.create_window(
        title="布局调试",
        size=(300, 200),
        content=test
    )
    
    window.show()
    
    app.run()

if __name__ == "__main__":
    main()