#!/usr/bin/env python3
"""
VStack + TableView 独立测试 - 只测试两者的组合
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import VStack, TableView
from macui.app import MacUIApp

set_log_level("INFO")

class VStackTableViewOnlyApp(Component):
    """只有 VStack 和 TableView 的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化 VStack+TableView 组件...")
        
        # 最简数据
        self.table_data = self.create_signal([
            {"name": "Test", "value": "A"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        """构建视图 - 只有 VStack 包含 TableView"""
        print("🏗️ Building VStack with TableView only...")
        
        return VStack(spacing=10, padding=10, children=[
            # 只有 TableView，没有其他组件
            TableView(
                columns=[
                    {"title": "Name", "key": "name", "width": 80},
                    {"title": "Value", "key": "value", "width": 40},
                ],
                data=self.table_data,
                selected_row=self.selected_row,
                on_select=self.on_row_select
            ),
        ])

def main():
    """主函数"""
    print("🚀 VStack+TableView Only Test Starting...")
    
    app = MacUIApp("VStack+TableView Test")
    
    print("📱 Creating VStack+TableView component...")
    test_component = VStackTableViewOnlyApp()
    
    window = app.create_window(
        title="VStack+TableView Test", 
        size=(200, 150),
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
        print("✅ VStack+TableView test ended")

if __name__ == "__main__":
    main()