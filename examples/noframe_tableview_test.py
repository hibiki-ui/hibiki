#!/usr/bin/env python3
"""
无Frame TableView 测试 - 完全不设置任何frame参数
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import TableView
from macui.app import MacUIApp
from AppKit import NSView
from Foundation import NSMakeRect

set_log_level("INFO")

class NoFrameTableViewWrapper(Component):
    """无Frame的 TableView 包装器"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化无Frame TableView 包装器...")
        
        self.table_data = self.create_signal([
            {"name": "Test", "value": "1"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        print("🏗️ Creating no-frame wrapper...")
        
        # 创建容器，不设置frame
        container = NSView.alloc().init()
        
        print("📊 Creating TableView without frame...")
        
        # 创建 TableView，完全不设置frame参数
        table_view = TableView(
            columns=[
                {"title": "Name", "key": "name", "width": 80},
                {"title": "Value", "key": "value", "width": 40},
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_row_select
            # 注意：完全不设置frame参数
        )
        
        print("🔗 Adding TableView to container...")
        container.addSubview_(table_view)
        
        print("✅ No-frame wrapper created")
        return container

def main():
    print("🚀 No-Frame TableView Test Starting...")
    
    app = MacUIApp("No-Frame TableView Test")
    
    print("📱 Creating no-frame component...")
    test_component = NoFrameTableViewWrapper()
    
    print("🏠 Creating window...")
    window = app.create_window(
        title="No-Frame TableView Test",
        size=(200, 150),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    
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
        print("✅ No-frame test ended")

if __name__ == "__main__":
    main()