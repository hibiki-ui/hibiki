#!/usr/bin/env python3
"""
立即布局调试 - 创建UI后立即分析布局状态
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack
from macui.components.modern_controls import ModernLabel
from macui.layout.debug import generate_debug_report
from AppKit import NSApplication

class ImmediateLayoutDebug(Component):
    
    def mount(self):
        print("🔧 创建布局测试组件...")
        
        # 创建两个标签
        label1 = ModernLabel(text="第一个标签", width=150, height=25)
        label2 = ModernLabel(text="第二个标签", width=150, height=25)
        
        print("📝 标签创建完成")
        
        # 创建垂直布局容器
        container = ModernVStack(
            children=[label1, label2],
            spacing=15,
            width=200,
            height=80,
            padding=10
        )
        
        print("📦 容器创建完成")
        
        # 获取视图
        view = container.get_view()
        print(f"🔍 视图获取完成: {view}")
        
        # 立即分析布局状态
        print("\n🔍 === 立即布局分析 ===")
        self.analyze_layout_immediately(view)
        
        return view
    
    def analyze_layout_immediately(self, view):
        """立即分析布局状态"""
        try:
            print("📊 生成调试报告:")
            generate_debug_report()
            
            print("\n🌳 检查视图层次:")
            frame = view.frame()
            print(f"根视图: {type(view).__name__} frame=({frame.origin.x:.1f}, {frame.origin.y:.1f}, {frame.size.width:.1f}, {frame.size.height:.1f})")
            
            if hasattr(view, 'subviews'):
                subviews = list(view.subviews())
                print(f"子视图数量: {len(subviews)}")
                
                for i, subview in enumerate(subviews):
                    sub_frame = subview.frame()
                    print(f"  子视图{i}: {type(subview).__name__} frame=({sub_frame.origin.x:.1f}, {sub_frame.origin.y:.1f}, {sub_frame.size.width:.1f}, {sub_frame.size.height:.1f})")
                    
                    # 如果是NSTextField，显示文本内容
                    if hasattr(subview, 'stringValue'):
                        text = subview.stringValue()
                        print(f"    文本: '{text}'")
            
            print("\n🎯 布局问题分析:")
            # 检查是否有重叠问题
            if hasattr(view, 'subviews'):
                subviews = list(view.subviews())
                if len(subviews) >= 2:
                    view1_frame = subviews[0].frame()
                    view2_frame = subviews[1].frame()
                    
                    if (abs(view1_frame.origin.x - view2_frame.origin.x) < 5 and 
                        abs(view1_frame.origin.y - view2_frame.origin.y) < 5):
                        print("❌ 检测到视图重叠问题!")
                        print(f"   视图1位置: ({view1_frame.origin.x:.1f}, {view1_frame.origin.y:.1f})")
                        print(f"   视图2位置: ({view2_frame.origin.x:.1f}, {view2_frame.origin.y:.1f})")
                    else:
                        print("✅ 视图位置看起来正常")
                        print(f"   视图1: ({view1_frame.origin.x:.1f}, {view1_frame.origin.y:.1f})")
                        print(f"   视图2: ({view2_frame.origin.x:.1f}, {view2_frame.origin.y:.1f})")
            
        except Exception as e:
            print(f"❌ 布局分析失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    print("🚀 启动立即布局调试...")
    
    app = MacUIApp("Immediate Layout Debug")
    test = ImmediateLayoutDebug()
    
    window = app.create_window(
        title="布局问题调试",
        size=(300, 150),
        content=test
    )
    
    window.show()
    
    print("🏁 布局创建完成 - 检查控制台输出的调试信息")
    print("💡 如果您看到UI重叠，调试信息将显示具体原因")
    
    # 运行一小段时间让用户看到UI
    from Foundation import NSTimer
    import objc
    
    class ExitTimer(object):
        @objc.typedSelector(b'v@:@')
        def exit_(self, timer):
            print("\n🔚 调试完成，退出应用")
            NSApplication.sharedApplication().terminate_(None)
    
    exit_timer = ExitTimer()
    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        3.0, exit_timer, 'exit:', None, False
    )
    
    app.run()

if __name__ == "__main__":
    main()