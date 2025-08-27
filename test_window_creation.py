#!/usr/bin/env python3
"""
窗口创建测试 - 逐步检测UI显示过程中的阻塞点
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.component import Component
from macui.components.modern_controls import ModernLabel
from Foundation import NSTimer
import objc

class WindowCreationTest(Component):
    """窗口创建测试"""
    
    def __init__(self):
        super().__init__()
        print("🏗️ WindowCreationTest.__init__ 完成")
    
    def mount(self):
        print("🔧 开始mount()...")
        
        # 最简单的组件
        label = ModernLabel(text="测试标签", width=200, height=30)
        print("✅ ModernLabel 创建完成")
        
        view = label.get_view()
        print(f"✅ 获取到view: {view}")
        
        # 安排检查定时器
        print("⏰ 设置1秒后检查定时器...")
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, 'checkWindowStatus:', None, False
        )
        
        return view
    
    @objc.typedSelector(b'v@:@')
    def checkWindowStatus_(self, timer):
        print("🔍 === 窗口状态检查 ===")
        print("🎉 定时器回调成功执行!")
        
        # 这说明macOS事件循环正常工作
        print("✅ macOS事件循环正常工作")
        print("✅ NSTimer回调机制正常")
        
        # 尝试获取应用和窗口信息
        try:
            from AppKit import NSApplication
            app = NSApplication.sharedApplication()
            windows = list(app.windows())
            print(f"📊 应用窗口数量: {len(windows)}")
            
            if windows:
                for i, window in enumerate(windows):
                    print(f"🪟 窗口{i}: {window}")
                    print(f"   标题: {window.title()}")
                    print(f"   frame: {window.frame()}")
                    print(f"   可见: {window.isVisible()}")
                    print(f"   key窗口: {window.isKeyWindow()}")
                    
                    # 检查内容视图
                    content_view = window.contentView()
                    if content_view:
                        print(f"   内容视图: {content_view}")
                        print(f"   内容视图frame: {content_view.frame()}")
                        print(f"   子视图数: {len(list(content_view.subviews()))}")
        except Exception as e:
            print(f"❌ 窗口检查异常: {e}")

def main():
    print("🚀 启动窗口创建测试...")
    
    # 创建应用
    print("📱 创建MacUIApp...")
    app = MacUIApp("Window Creation Test")
    print("✅ MacUIApp创建完成")
    
    # 创建测试组件
    print("🧪 创建测试组件...")
    test_component = WindowCreationTest()
    print("✅ 测试组件创建完成")
    
    # 创建窗口
    print("🪟 创建窗口...")
    window = app.create_window(
        title="窗口创建测试",
        size=(300, 200),
        content=test_component
    )
    print(f"✅ 窗口创建完成: {window}")
    
    # 显示窗口
    print("👁️ 显示窗口...")
    window.show()
    print("✅ 窗口显示调用完成")
    
    # 启动应用
    print("🎮 启动应用事件循环...")
    print("🔄 如果应用正常启动，1秒后将看到定时器回调...")
    app.run()

if __name__ == "__main__":
    main()