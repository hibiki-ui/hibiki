#!/usr/bin/env python3
"""
原始 TableView 测试 - 直接在窗口中显示 TableView
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import TableView
from macui.app import MacUIApp
from AppKit import NSView
from Foundation import NSMakeRect

set_log_level("INFO")

def main():
    print("🚀 Raw TableView Test Starting...")
    
    app = MacUIApp("Raw TableView Test")
    
    # 创建简单数据
    table_data = Signal([
        {"name": "Test1", "value": "A"},
        {"name": "Test2", "value": "B"},
    ])
    
    selected_row = Signal(-1)
    
    def on_select(row):
        print(f"📊 Selected row: {row}")
    
    print("📊 Creating TableView directly...")
    
    # 直接创建 TableView
    table_view = TableView(
        columns=[
            {"title": "Name", "key": "name", "width": 100},
            {"title": "Value", "key": "value", "width": 60},
        ],
        data=table_data,
        selected_row=selected_row,
        on_select=on_select,
        frame=(10, 10, 180, 130)
    )
    
    print("🏠 Creating window with TableView...")
    window = app.create_window(
        title="Raw TableView Test",
        size=(200, 150),
        resizable=True,
        content=table_view  # 直接使用 TableView 作为内容
    )
    
    print("👀 Showing window...")
    window.show()
    
    print("🎬 Starting app...")
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ Raw test ended")

if __name__ == "__main__":
    main()