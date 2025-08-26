#!/usr/bin/env python3
"""
TableView 修复测试 - 完全避免 NSStackView
基于网络调查：NSStackView 和 NSTableView 约束冲突
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
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
    NSApplicationActivationPolicyRegular, NSMenu, NSMenuItem
)
from PyObjCTools import AppHelper

class TableViewNoStackApp(NSObject):
    """完全避免NSStackView的TableView测试"""
    
    def init(self):
        self = objc.super(TableViewNoStackApp, self).init()
        if self is None:
            return None
            
        # 保持强引用
        self.window = None
        self.table_view = None
        self.scroll_view = None
        self.data_source = None
        self.delegate = None
        
        return self
    
    def create_window(self):
        """创建窗口 - 完全不使用macUI的VStack"""
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 500, 400),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | 
            NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable,
            2,  # NSBackingStoreBuffered
            False
        )
        self.window.setTitle_("TableView Fix - No NSStackView")
        
        # 获取内容视图
        content_view = self.window.contentView()
        
        # ✅ 关键修复：创建一个简单的NSView容器，不使用NSStackView
        container = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 500, 400))
        container.setTranslatesAutoresizingMaskIntoConstraints_(True)  # 使用传统autoresizing
        
        # 创建标签
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 350, 460, 30))
        title_label.setStringValue_("TableView 修复测试 - 无 NSStackView 冲突")
        title_label.setBezeled_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # ✅ 创建 TableView - 关键修复点
        self.scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 50, 460, 280))
        
        # 确保ScrollView使用传统的autoresizing
        self.scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
        self.scroll_view.setHasVerticalScroller_(True)
        self.scroll_view.setHasHorizontalScroller_(False)
        self.scroll_view.setAutohidesScrollers_(True)
        
        # 创建表格视图
        self.table_view = NSTableView.alloc().init()
        
        # 确保TableView也使用传统的autoresizing  
        self.table_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
        
        # 创建列
        columns_config = [
            {"title": "姓名", "key": "name", "width": 150},
            {"title": "年龄", "key": "age", "width": 80},
            {"title": "城市", "key": "city", "width": 150},
        ]
        
        for col_config in columns_config:
            column = NSTableColumn.alloc().initWithIdentifier_(col_config["key"])
            column.setWidth_(col_config["width"])
            column.headerCell().setStringValue_(col_config["title"])
            self.table_view.addTableColumn_(column)
        
        # 设置表格到滚动视图
        self.scroll_view.setDocumentView_(self.table_view)
        
        # 创建数据源和委托（使用macUI的）
        from macui.core.binding import EnhancedTableViewDataSource, EnhancedTableViewDelegate
        
        self.data_source = EnhancedTableViewDataSource.alloc().init()
        self.data_source.data = [
            {"name": "张三", "age": 28, "city": "北京"},
            {"name": "李四", "age": 32, "city": "上海"},
            {"name": "王五", "age": 25, "city": "广州"},
            {"name": "赵六", "age": 35, "city": "深圳"},
        ]
        self.data_source.columns = ["name", "age", "city"]
        
        self.delegate = EnhancedTableViewDelegate.alloc().init()
        
        # 设置数据源和委托
        self.table_view.setDataSource_(self.data_source)
        self.table_view.setDelegate_(self.delegate)
        
        # 使用objc关联对象保持引用
        objc.setAssociatedObject(self.scroll_view, b"data_source", self.data_source, objc.OBJC_ASSOCIATION_RETAIN)
        objc.setAssociatedObject(self.scroll_view, b"delegate", self.delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        # ✅ 添加视图到容器 - 不使用任何StackView或约束系统
        container.addSubview_(title_label)
        container.addSubview_(self.scroll_view)
        
        # 设置内容视图
        content_view.addSubview_(container)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)

def create_menubar():
    """创建菜单栏"""
    menubar = NSMenu.alloc().init()
    
    # 应用菜单
    app_menu = NSMenu.alloc().init()
    
    # 退出菜单项
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit TableView Fix", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    
    # 添加到菜单栏
    app_menu_item = NSMenuItem.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    menubar.addItem_(app_menu_item)
    
    return menubar

if __name__ == "__main__":
    print("=== TableView 修复测试 - 避免 NSStackView 冲突 ===")
    print("基于网络调查的关键发现：")
    print("1. NSStackView 的 translatesAutoresizingMaskIntoConstraints_(False) 导致冲突")
    print("2. NSStackView 试图约束 NSScrollView")
    print("3. NSScrollView 内部的 NSTableView 约束与外部冲突")
    print("4. 解决方案：完全避免使用 NSStackView")
    
    try:
        # 1. 激活策略
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 2. 菜单栏
        menubar = create_menubar()
        app.setMainMenu_(menubar)
        
        # 3. 创建应用实例
        table_app = TableViewNoStackApp.alloc().init()
        table_app.create_window()
        
        print("✅ 窗口已创建，避免了NSStackView冲突")
        print("✅ 使用传统的 NSView 容器和 frame-based 布局")
        print("✅ NSScrollView 和 NSTableView 都使用 translatesAutoresizingMaskIntoConstraints=True")
        
        # 4. AppHelper事件循环
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()