#!/usr/bin/env python3
"""
直接 TableView 测试 - 绕过所有布局容器，直接将TableView设为窗口内容
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import TableView
from macui.app import MacUIApp

set_log_level("INFO")

class DirectTableViewApp(Component):
    """直接返回 TableView 的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化直接 TableView 组件...")
        
        # 最简数据
        self.table_data = self.create_signal([
            {"name": "Test1", "value": "A"},
            {"name": "Test2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        """构建视图 - 直接返回 TableView，不用任何容器"""
        print("🏗️ Building direct TableView...")
        
        # 直接返回 TableView，设置 frame 让其撑满窗口
        return TableView(
            columns=[
                {"title": "Name", "key": "name", "width": 80},
                {"title": "Value", "key": "value", "width": 40},
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_row_select,
            frame=(0, 0, 180, 150)
        )

def main():
    """主函数"""
    print("🚀 Direct TableView Test Starting...")
    
    app = MacUIApp("Direct TableView Test")
    
    print("📱 Creating direct TableView component...")
    test_component = DirectTableViewApp()
    
    window = app.create_window(
        title="Direct TableView Test", 
        size=(200, 180),
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
        print("✅ Direct TableView test ended")

if __name__ == "__main__":
    main()