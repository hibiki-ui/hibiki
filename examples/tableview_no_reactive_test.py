#!/usr/bin/env python3
"""
非响应式TableView测试 - 避免响应式数据绑定
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import MacUIApp
from macui.components import TableView
from AppKit import NSView
from Foundation import NSMakeRect

def main():
    print("=== 非响应式TableView测试 ===")
    print("使用静态数据，避免响应式绑定")
    
    # 创建应用
    app = MacUIApp("Non-Reactive TableView Test")
    
    # 静态数据（不使用Signal）
    static_data = [
        {"name": "测试1", "value": 100, "type": "A"},
        {"name": "测试2", "value": 200, "type": "B"},
        {"name": "测试3", "value": 300, "type": "C"},
    ]
    
    # 创建简单容器
    container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 500, 300))
    container.setTranslatesAutoresizingMaskIntoConstraints_(True)
    
    # 创建TableView（不使用Signal数据）
    try:
        table_view = TableView(
            columns=[
                {"title": "名称", "key": "name", "width": 150},
                {"title": "数值", "key": "value", "width": 100},
                {"title": "类型", "key": "type", "width": 100},
            ],
            data=static_data,  # 直接使用静态数据，不是Signal
            frame=(20, 20, 460, 260)
        )
        
        # 添加到容器
        container.addSubview_(table_view)
        
        print("✅ 非响应式TableView创建成功")
        
    except Exception as e:
        print(f"❌ TableView创建失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 创建窗口
    from AppKit import NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable
    
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 500, 300),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
        2,
        False
    )
    window.setTitle_("Non-Reactive TableView Test")
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