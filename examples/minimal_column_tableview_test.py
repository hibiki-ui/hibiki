#!/usr/bin/env python3
"""
最小列 TableView 测试 - 测试极简的列配置
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

set_log_level("INFO")

class MinimalColumnTableViewWrapper(Component):
    """最小列的 TableView 包装器"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化最小列 TableView...")
        
        # 最少数据
        self.table_data = self.create_signal([
            {"x": "1"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        print("🏗️ Creating minimal column wrapper...")
        
        container = NSView.alloc().init()
        
        print("📊 Creating TableView with single small column...")
        
        # 最小的TableView配置：单列，最小宽度
        table_view = TableView(
            columns=[
                {"title": "X", "key": "x", "width": 50},  # 很小的列宽
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_row_select
        )
        
        container.addSubview_(table_view)
        
        print("✅ Minimal column wrapper created")
        return container

def main():
    print("🚀 Minimal Column TableView Test Starting...")
    
    app = MacUIApp("Minimal Column TableView Test")
    
    test_component = MinimalColumnTableViewWrapper()
    
    window = app.create_window(
        title="Minimal Column TableView Test",
        size=(150, 100),
        resizable=True,
        content=test_component
    )
    
    window.show()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("✅ Minimal column test ended")

if __name__ == "__main__":
    main()