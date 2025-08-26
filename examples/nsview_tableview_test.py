#!/usr/bin/env python3
"""
NSView + TableView 测试 - 避开 NSStackView 直接用 NSView
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

class NSViewTableViewApp(Component):
    """使用 NSView 而不是 VStack 的测试应用"""
    
    def __init__(self):
        super().__init__()
        print("🔧 初始化 NSView+TableView 组件...")
        
        # 最简数据
        self.table_data = self.create_signal([
            {"name": "Test", "value": "A"},
        ])
        
        self.selected_row = self.create_signal(-1)
    
    def on_row_select(self, row):
        """行选择回调"""
        print(f"📊 Row selected: {row}")
    
    def mount(self):
        """构建视图 - 使用 NSView 容器而不是 VStack"""
        print("🏗️ Building NSView with TableView...")
        
        # 创建容器视图
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 200, 150))
        
        # 创建 TableView
        table_view = TableView(
            columns=[
                {"title": "Name", "key": "name", "width": 80},
                {"title": "Value", "key": "value", "width": 40},
            ],
            data=self.table_data,
            selected_row=self.selected_row,
            on_select=self.on_row_select,
            frame=(10, 10, 180, 130)  # 手动设置 frame
        )
        
        # 添加到容器
        container.addSubview_(table_view)
        
        return container

def main():
    """主函数"""
    print("🚀 NSView+TableView Test Starting...")
    
    app = MacUIApp("NSView+TableView Test")
    
    print("📱 Creating NSView+TableView component...")
    test_component = NSViewTableViewApp()
    
    window = app.create_window(
        title="NSView+TableView Test", 
        size=(220, 170),
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
        print("✅ NSView+TableView test ended")

if __name__ == "__main__":
    main()