#!/usr/bin/env python3
"""
包装器 TableView 测试 - 用简单的 NSView 包装 TableView
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

class SimpleTableViewWrapper(Component):
    """简单的 TableView 包装器"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化 TableView 包装器...")
        
        # 简单数据
        self.table_data = self.create_signal([
            {"name": "Item1", "value": "A"},
            {"name": "Item2", "value": "B"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        print("🏗️ Creating simple wrapper...")
        
        # 创建简单的容器视图
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 200, 150))
        
        print("📊 Creating TableView...")
        
        # 创建 TableView
        table_view = TableView(
            columns=[
                {"title": "Name", "key": "name", "width": 100},
                {"title": "Value", "key": "value", "width": 60},
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_row_select,
            frame=(5, 5, 190, 140)
        )
        
        print("🔗 Adding TableView to container...")
        container.addSubview_(table_view)
        
        print("✅ Wrapper created successfully")
        return container

def main():
    print("🚀 Wrapper TableView Test Starting...")
    
    app = MacUIApp("Wrapper TableView Test")
    
    print("📱 Creating wrapper component...")
    test_component = SimpleTableViewWrapper()
    
    print("🏠 Creating window...")
    window = app.create_window(
        title="Wrapper TableView Test",
        size=(220, 170),
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
        print("✅ Wrapper test ended")

if __name__ == "__main__":
    main()