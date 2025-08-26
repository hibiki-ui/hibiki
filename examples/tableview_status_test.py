#!/usr/bin/env python3
"""
TableView 状态测试 - 详细监控应用状态
"""

import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, Component, set_log_level
from macui.components import VStack, Label, TableView
from macui.app import MacUIApp

set_log_level("INFO")

class TableViewStatusApp(Component):
    """监控 TableView 状态的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化 TableView 状态监控...")
        
        self.table_data = self.create_signal([
            {"name": "Test1", "value": "A"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        print("🏗️ Building TableView with status monitoring...")
        
        return VStack(spacing=10, padding=10, children=[
            Label("TableView Status Test"),
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
    print("🚀 TableView Status Test Starting...")
    
    app = MacUIApp("TableView Status Test")
    
    print("📱 Creating component...")
    test_component = TableViewStatusApp()
    
    print("🏠 Creating window...")
    window = app.create_window(
        title="TableView Status Test", 
        size=(200, 150),
        resizable=True,
        content=test_component
    )
    
    print("👀 Showing window...")
    window.show()
    print("✅ Window.show() completed")
    
    print("⏰ Waiting 2 seconds...")
    time.sleep(2)
    
    print("🎬 Starting application run loop...")
    try:
        print("📍 About to call app.run()...")
        app.run()
        print("📍 app.run() returned normally")
    except KeyboardInterrupt:
        print("\n👋 User interrupted")
    except Exception as e:
        print(f"\n❌ Error in app.run(): {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ Application ended")

if __name__ == "__main__":
    main()