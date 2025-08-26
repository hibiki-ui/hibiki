#!/usr/bin/env python3
"""
无 Frame 的 TableView 测试 - 让系统自动布局
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import TableView, VStack, Label
from macui.app import MacUIApp

set_log_level("INFO")

class NoFrameTableTestApp(Component):
    """无 Frame 的 TableView 测试应用"""
    
    def __init__(self):
        super().__init__()
        
        print("🔧 初始化无Frame测试组件...")
        
        # 创建响应式状态
        self.data = self.create_signal([
            {"name": "Test1", "value": "A"},
            {"name": "Test2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
        self.status = self.create_signal("Ready")
        
        # 创建计算属性
        self.status_text = self.create_computed(
            lambda: f"Status: {self.status.value}"
        )
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 Row selected: {row}")
        if 0 <= row < len(self.data.value):
            item = self.data.value[row]
            self.status.value = f"Selected: {item['name']}"
        else:
            self.status.value = f"Deselected"
    
    def mount(self):
        """构建组件视图"""
        print("🏗️ Building no-frame view...")
        
        return VStack(spacing=10, padding=10, children=[
            Label("No-Frame TableView Test"),
            Label(self.status_text),
            
            # TableView - 不设置 frame，让系统自动布局
            TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 100},
                    {"title": "Value", "key": "value", "width": 60},
                ],
                data=self.data,
                selected_row=self.selected_row,
                on_select=self.on_row_select
                # 注意：没有 frame 参数
            ),
        ])

def main():
    """主函数"""
    print("🚀 No-Frame TableView Test Starting...")
    
    # 创建应用
    app = MacUIApp("No-Frame TableView Test")
    
    print("📱 Creating component and window...")
    test_component = NoFrameTableTestApp()
    
    window = app.create_window(
        title="No-Frame TableView Test",
        size=(300, 200),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    
    print("🎬 Starting application...")
    print("Instructions:")
    print("- You should see a window with a table")
    print("- No frame constraints - system auto-layout")
    print("- Click rows to select")
    print("- Press Ctrl+C to exit")
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ No-frame test ended")

if __name__ == "__main__":
    main()