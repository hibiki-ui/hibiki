#!/usr/bin/env python3
"""
TableView NSLayoutConstraintNumberExceedsLimit 修复测试
基于网络调查结果的解决方案
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.app import MacUIApp
from AppKit import NSScrollView, NSTableView, NSTableColumn, NSTextField
from Foundation import NSMakeRect

# 设置日志
set_log_level("INFO")

def create_fixed_tableview(columns, data, frame=None):
    """创建修复版本的TableView - 基于网络调查结果"""
    
    # 创建滚动视图
    scroll_view = NSScrollView.alloc().init()
    
    # ✅ 关键修复1：确保ScrollView使用传统的autoresizing
    # 根据调查：NSScrollView应该设置translatesAutoresizingMaskIntoConstraints=True
    scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
    
    # 滚动视图配置
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)
    scroll_view.setAutohidesScrollers_(True)
    
    # 创建表格视图
    table_view = NSTableView.alloc().init()
    
    # ✅ 关键修复2：确保TableView也使用传统的autoresizing  
    # 根据调查：NSTableView应该管理自己的内部约束
    table_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
    
    # 创建列
    for col_config in columns:
        title = col_config.get("title", "")
        key = col_config.get("key", title)
        width = col_config.get("width", 100.0)
        
        column = NSTableColumn.alloc().initWithIdentifier_(key)
        column.setWidth_(width)
        column.headerCell().setStringValue_(title)
        table_view.addTableColumn_(column)
    
    # 设置表格到滚动视图
    scroll_view.setDocumentView_(table_view)
    
    # ✅ 关键修复3：只在设置了frame时才调用setFrame_，避免使用layout_utils
    if frame:
        # 直接设置frame，不使用可能有问题的layout_utils
        safe_rect = NSMakeRect(frame[0], frame[1], frame[2], frame[3])
        scroll_view.setFrame_(safe_rect)
    
    # 创建简单的数据源
    from macui.core.binding import EnhancedTableViewDataSource
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.data = data
    data_source.columns = [col.get("key", col.get("title", "")) for col in columns]
    
    # 设置数据源
    table_view.setDataSource_(data_source)
    
    # 创建委托
    from macui.core.binding import EnhancedTableViewDelegate
    delegate = EnhancedTableViewDelegate.alloc().init()
    table_view.setDelegate_(delegate)
    
    # 使用内存管理器保持引用
    from macui.core.memory_manager import associate_object
    associate_object(scroll_view, "table_data_source", data_source)
    associate_object(scroll_view, "table_delegate", delegate)
    
    return scroll_view, table_view, data_source, delegate

class TableViewFixApp:
    """TableView修复测试应用"""
    
    def __init__(self):
        self.table_data = Signal([
            {"name": "张三", "age": "28", "city": "北京"},
            {"name": "李四", "age": "32", "city": "上海"},
            {"name": "王五", "age": "25", "city": "广州"},
        ])
        self.message = Signal("TableView修复测试 - 基于网络调查结果")

def main():
    print("=== TableView NSLayoutConstraintNumberExceedsLimit 修复测试 ===")
    print("基于网络调查的关键修复：")
    print("1. NSScrollView.setTranslatesAutoresizingMaskIntoConstraints_(True)")
    print("2. NSTableView.setTranslatesAutoresizingMaskIntoConstraints_(True)")
    print("3. 避免使用可能有问题的layout_utils")
    
    app = MacUIApp("TableView Fix Test")
    test_app = TableViewFixApp()
    
    from macui import Component
    from macui.components import VStack, Label
    
    class TableViewFixComponent(Component):
        def mount(self):
            # 创建修复版本的TableView
            scroll_view, table_view, data_source, delegate = create_fixed_tableview(
                columns=[
                    {"title": "姓名", "key": "name", "width": 100},
                    {"title": "年龄", "key": "age", "width": 60},
                    {"title": "城市", "key": "city", "width": 100},
                ],
                data=test_app.table_data.value,
                frame=(20, 50, 350, 200)
            )
            
            # 保存引用防止回收
            self.scroll_view = scroll_view
            self.table_view = table_view
            self.data_source = data_source
            self.delegate = delegate
            
            # 创建容器
            container = VStack(spacing=15, padding=20, children=[
                Label("TableView修复测试"),
                Label("基于网络调查的解决方案"),
            ])
            
            # 手动添加TableView到容器
            container_view = container
            container_view.addSubview_(scroll_view)
            
            return container_view
    
    # 创建窗口
    window = app.create_window(
        title="TableView Fix Test - 基于网络调查",
        size=(450, 350),
        content=TableViewFixComponent()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 修复版TableView窗口已显示")
    print("📝 关键修复点:")
    print("   - ScrollView和TableView都使用translatesAutoresizingMaskIntoConstraints=True")
    print("   - 避免手动设置内部视图约束")
    print("   - 让NSTableView管理自己的内部布局")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()