#!/usr/bin/env python3
"""
TableView 工作示例 - 使用验证过的纯PyObjC方式
替代有问题的macUI TableView实现
"""

import sys
import os
import objc

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Foundation import NSObject, NSMakeRect
from AppKit import (
    NSApplication, NSWindow, NSScrollView, NSTableView, NSTableColumn,
    NSTextField, NSButton, NSView,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSApplicationActivationPolicyRegular, NSMenu, NSMenuItem
)
from PyObjCTools import AppHelper

class WorkingTableDataSource(NSObject):
    """工作的TableView数据源"""
    
    def init(self):
        self = objc.super(WorkingTableDataSource, self).init()
        if self is None:
            return None
            
        # 表格数据
        self.data = [
            {"name": "张三", "age": 28, "city": "北京", "salary": 8000},
            {"name": "李四", "age": 32, "city": "上海", "salary": 12000},
            {"name": "王五", "age": 25, "city": "广州", "salary": 7500},
            {"name": "赵六", "age": 35, "city": "深圳", "salary": 15000},
            {"name": "孙七", "age": 29, "city": "杭州", "salary": 9500},
        ]
        
        # 列配置
        self.columns = ["name", "age", "city", "salary"]
        
        return self
    
    def numberOfRowsInTableView_(self, tableView):
        """返回行数"""
        return len(self.data)
    
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        """返回单元格数据"""
        if row < 0 or row >= len(self.data):
            return ""
        
        column_id = tableColumn.identifier()
        row_data = self.data[row]
        
        value = row_data.get(column_id, "")
        if column_id == "salary":
            return f"¥{value:,}"
        return str(value)

class WorkingTableDelegate(NSObject):
    """工作的TableView代理"""
    
    def init(self):
        self = objc.super(WorkingTableDelegate, self).init()
        if self is None:
            return None
        self.on_select_callback = None
        return self
    
    def tableView_viewForTableColumn_row_(self, tableView, tableColumn, row):
        """为指定行列提供视图"""
        
        column_id = tableColumn.identifier()
        
        # 尝试从复用队列获取视图
        cell_view = tableView.makeViewWithIdentifier_owner_(column_id, self)
        
        if cell_view is None:
            # 创建新的文本视图
            cell_view = NSTextField.alloc().init()
            cell_view.setIdentifier_(column_id)
            cell_view.setBezeled_(False)
            cell_view.setDrawsBackground_(False)
            cell_view.setEditable_(False)
            cell_view.setSelectable_(False)
        
        # 获取数据并配置视图
        data_source = tableView.dataSource()
        if hasattr(data_source, 'data') and 0 <= row < len(data_source.data):
            row_data = data_source.data[row]
            value = row_data.get(column_id, "")
            
            if column_id == "salary":
                cell_view.setStringValue_(f"¥{value:,}")
            else:
                cell_view.setStringValue_(str(value))
        
        return cell_view
    
    def tableViewSelectionDidChange_(self, notification):
        """选择变化处理"""
        tableView = notification.object()
        selected_row = tableView.selectedRow()
        
        if selected_row >= 0:
            data_source = tableView.dataSource()
            if hasattr(data_source, 'data') and selected_row < len(data_source.data):
                selected_data = data_source.data[selected_row]
                print(f"选择了: {selected_data['name']} - {selected_data['city']} (薪资: ¥{selected_data['salary']:,})")
        
        if self.on_select_callback:
            self.on_select_callback(selected_row)

class WorkingTableApp(NSObject):
    """工作的TableView应用"""
    
    def init(self):
        self = objc.super(WorkingTableApp, self).init()
        if self is None:
            return None
            
        # 强引用
        self.window = None
        self.table_view = None
        self.scroll_view = None
        self.data_source = None
        self.delegate = None
        
        return self
    
    def create_window(self):
        """创建主窗口"""
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 500),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            2,
            False
        )
        self.window.setTitle_("Working TableView Example")
        
        # 创建内容视图
        content_view = self.window.contentView()
        
        # 创建标题
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 450, 660, 30))
        title_label.setStringValue_("TableView 工作示例 - 使用纯PyObjC模式")
        title_label.setBezeled_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        
        # 创建说明
        info_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 420, 660, 25))
        info_label.setStringValue_("✅ 此示例避免了NSStackView约束冲突，使用传统的frame-based布局")
        info_label.setBezeled_(False)
        info_label.setDrawsBackground_(False)
        info_label.setEditable_(False)
        info_label.setSelectable_(False)
        
        # 创建TableView
        self.scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 50, 660, 360))
        
        # ✅ 关键：使用传统的autoresizing
        self.scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
        self.scroll_view.setHasVerticalScroller_(True)
        self.scroll_view.setHasHorizontalScroller_(False)
        self.scroll_view.setAutohidesScrollers_(True)
        
        # 创建表格视图
        self.table_view = NSTableView.alloc().init()
        self.table_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # 创建列
        columns_config = [
            {"title": "姓名", "key": "name", "width": 120},
            {"title": "年龄", "key": "age", "width": 80},
            {"title": "城市", "key": "city", "width": 120},
            {"title": "薪资", "key": "salary", "width": 150},
        ]
        
        for col_config in columns_config:
            column = NSTableColumn.alloc().initWithIdentifier_(col_config["key"])
            column.setWidth_(col_config["width"])
            column.headerCell().setStringValue_(col_config["title"])
            self.table_view.addTableColumn_(column)
        
        # 设置表格到滚动视图
        self.scroll_view.setDocumentView_(self.table_view)
        
        # 创建数据源和代理
        self.data_source = WorkingTableDataSource.alloc().init()
        self.delegate = WorkingTableDelegate.alloc().init()
        
        # 设置数据源和代理
        self.table_view.setDataSource_(self.data_source)
        self.table_view.setDelegate_(self.delegate)
        
        # 使用objc关联对象保持引用
        objc.setAssociatedObject(self.scroll_view, b"data_source", self.data_source, objc.OBJC_ASSOCIATION_RETAIN)
        objc.setAssociatedObject(self.scroll_view, b"delegate", self.delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        # 添加到窗口 - 不使用VStack，直接添加
        content_view.addSubview_(title_label)
        content_view.addSubview_(info_label)
        content_view.addSubview_(self.scroll_view)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)

def create_menubar():
    """创建菜单栏"""
    menubar = NSMenu.alloc().init()
    
    app_menu = NSMenu.alloc().init()
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit Working TableView", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    
    app_menu_item = NSMenuItem.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    menubar.addItem_(app_menu_item)
    
    return menubar

def main():
    """主函数"""
    print("=== TableView 工作示例 ===")
    print("✅ 使用验证过的纯PyObjC实现")
    print("✅ 避免NSStackView约束冲突")
    print("✅ 使用传统的frame-based布局")
    print("✅ 正确的内存管理")
    
    try:
        # PyObjC最佳实践
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        menubar = create_menubar()
        app.setMainMenu_(menubar)
        
        # 创建应用实例
        table_app = WorkingTableApp.alloc().init()
        table_app.create_window()
        
        print("✅ TableView应用已启动")
        print("📝 功能:")
        print("   - 显示员工信息表格")
        print("   - 支持行选择")
        print("   - 自定义薪资格式显示")
        print("   - 无约束错误！")
        
        # AppHelper事件循环
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()