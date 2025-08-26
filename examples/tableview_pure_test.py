#!/usr/bin/env python3
"""
纯TableView测试 - 只测试TableView功能，不使用其他macUI组件
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import MacUIApp, Signal
from macui.components import TableView
from AppKit import NSView
from Foundation import NSMakeRect

def main():
    print("=== 纯TableView功能测试 ===")
    print("只测试TableView本身，不使用其他macUI组件")
    
    # 创建应用
    app = MacUIApp("Pure TableView Test")
    
    # 创建测试数据
    table_data = Signal([
        {"name": "测试1", "value": 100, "type": "A"},
        {"name": "测试2", "value": 200, "type": "B"},
        {"name": "测试3", "value": 300, "type": "C"},
    ])
    
    # 创建简单容器
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 500, 300))
    container.setTranslatesAutoresizingMaskIntoConstraints_(True)
    
    # 直接创建TableView
    try:
        table_view = TableView(
            columns=[
                {"title": "名称", "key": "name", "width": 150},
                {"title": "数值", "key": "value", "width": 100},
                {"title": "类型", "key": "type", "width": 100},
            ],
            data=table_data,
            frame=(20, 20, 460, 260)
        )
        
        # 添加到容器
        container.addSubview_(table_view)
        
        print("✅ TableView创建成功")
        
    except Exception as e:
        print(f"❌ TableView创建失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 创建窗口并设置内容
    from AppKit import NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable
    
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 500, 300),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
        2,
        False
    )
    window.setTitle_("Pure TableView Test")
    window.contentView().addSubview_(container)
    window.makeKeyAndOrderFront_(None)
    
    print("✅ 窗口创建成功")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()