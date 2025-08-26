#!/usr/bin/env python3
"""
调试约束问题 - 逐步添加组件找出约束冲突
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import VStack, Label
from macui.app import MacUIApp

set_log_level("INFO")

class DebugConstraintApp(Component):
    """调试约束的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化调试约束组件...")
        
        self.message = self.create_signal("Debug Test Ready")
        self.status_text = self.create_computed(
            lambda: f"Status: {self.message.value}"
        )
    
    def mount(self):
        """构建最简视图 - 只有 VStack 和 Label"""
        print("🏗️ Building debug view with only VStack and Labels...")
        
        return VStack(spacing=10, padding=10, children=[
            Label("Debug Constraint Test"),
            Label(self.status_text),
            Label("This is a third label"),
        ])

def main():
    """主函数"""
    print("🚀 Debug Constraint Test Starting...")
    
    app = MacUIApp("Debug Constraint Test")
    
    print("📱 Creating debug component...")
    test_component = DebugConstraintApp()
    
    window = app.create_window(
        title="Debug Constraint Test", 
        size=(250, 150),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    print("✅ Window should be visible now")
    
    print("🎬 Starting application...")
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ Debug test ended")

if __name__ == "__main__":
    main()