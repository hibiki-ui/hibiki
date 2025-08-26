#!/usr/bin/env python3
"""
干净的 TableView 测试 - 不使用任何内存hack，回到基本原理
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

class CleanTableTestApp(Component):
    """干净的 TableView 测试应用"""
    
    def __init__(self):
        super().__init__()
        
        print("🔧 初始化干净的测试组件...")
        
        # 创建响应式状态 - 使用更简单的数据
        self.data = self.create_signal([
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
        self.status = self.create_signal("Ready")
        
        # 创建计算属性
        self.status_text = self.create_computed(
            lambda: f"Status: {self.status.value}"
        )
        self.selection_text = self.create_computed(
            lambda: f"Selected: {self.selected_row.value}"
        )
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 Row selected: {row}")
        if 0 <= row < len(self.data.value):
            item = self.data.value[row]
            self.status.value = f"Selected: {item['name']}"
        else:
            self.status.value = f"Deselected (row {row})"
    
    def mount(self):
        """构建组件视图"""
        print("🏗️ Building clean view...")
        
        return VStack(spacing=10, padding=10, children=[
            Label("Clean TableView Test"),
            Label(self.status_text),
            
            # TableView - 使用更保守的尺寸
            TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 100},
                    {"title": "Value", "key": "value", "width": 60},
                ],
                data=self.data,
                selected_row=self.selected_row,
                on_select=self.on_row_select,
                frame=(0, 0, 200, 100)  # 更小的尺寸
            ),
            
            Label(self.selection_text),
        ])

def main():
    """主函数 - 不使用任何hack"""
    print("🚀 Clean TableView Test Starting...")
    
    # 创建应用
    app = MacUIApp("Clean TableView Test")
    
    print("📱 Creating component and window...")
    test_component = CleanTableTestApp()
    
    window = app.create_window(
        title="Clean TableView Test",
        size=(300, 250),  # 更小的窗口
        resizable=False,   # 禁用调整大小以避免布局问题
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    
    print("🎬 Starting application...")
    print("Instructions:")
    print("- You should see a window with a table")
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
        print("✅ Clean test ended")

if __name__ == "__main__":
    main()