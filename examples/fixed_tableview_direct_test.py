#!/usr/bin/env python3
"""
直接修复的TableView测试 - 绕过所有可能有问题的macUI组件
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import objc
from Foundation import NSObject, NSMakeRect
from AppKit import (
    NSApplication, NSWindow, NSScrollView, NSTableView, NSTableColumn,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSApplicationActivationPolicyRegular, NSMenu, NSMenuItem
)
from PyObjCTools import AppHelper

def create_fixed_tableview_direct(columns, data, frame=None):
    """直接创建修复版本的TableView，完全避免macUI的工具函数"""
    
    # 创建滚动视图
    scroll_view = NSScrollView.alloc().init()
    
    # ✅ 确保使用传统的autoresizing
    scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)
    
    # 滚动视图配置
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)
    scroll_view.setAutohidesScrollers_(True)
    
    # 创建表格视图
    table_view = NSTableView.alloc().init()
    
    # ✅ 确保TableView也使用传统的autoresizing
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
    
    # ✅ 直接设置frame，不使用任何macUI工具函数
    if frame:
        scroll_view.setFrame_(NSMakeRect(frame[0], frame[1], frame[2], frame[3]))
    
    # ✅ 创建简单的数据源，避免使用macUI的响应式系统
    from macui.core.binding import EnhancedTableViewDataSource, EnhancedTableViewDelegate
    
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.data = data
    data_source.columns = [col.get("key", col.get("title", "")) for col in columns]
    
    delegate = EnhancedTableViewDelegate.alloc().init()
    
    # 设置数据源和委托
    table_view.setDataSource_(data_source)
    table_view.setDelegate_(delegate)
    
    # 使用objc关联对象保持引用，避免使用macUI的内存管理器
    objc.setAssociatedObject(scroll_view, b"data_source", data_source, objc.OBJC_ASSOCIATION_RETAIN)
    objc.setAssociatedObject(scroll_view, b"delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return scroll_view, table_view, data_source, delegate

class DirectTableTestApp(NSObject):
    """直接TableView测试应用"""
    
    def init(self):
        self = objc.super(DirectTableTestApp, self).init()
        if self is None:
            return None
            
        self.window = None
        self.table_components = None
        
        return self
    
    def create_window(self):
        """创建窗口"""
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 500, 350),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            2,
            False
        )
        self.window.setTitle_("Direct Fixed TableView Test")
        
        # 创建内容视图
        content_view = self.window.contentView()
        
        # 直接创建修复版本的TableView
        scroll_view, table_view, data_source, delegate = create_fixed_tableview_direct(
            columns=[
                {"title": "名称", "key": "name", "width": 150},
                {"title": "数值", "key": "value", "width": 100},
                {"title": "状态", "key": "status", "width": 120},
            ],
            data=[
                {"name": "项目A", "value": 100, "status": "正常"},
                {"name": "项目B", "value": 200, "status": "警告"},
                {"name": "项目C", "value": 300, "status": "正常"},
                {"name": "项目D", "value": 150, "status": "错误"},
            ],
            frame=(20, 20, 460, 300)
        )
        
        # 保存引用
        self.table_components = (scroll_view, table_view, data_source, delegate)
        
        # 添加到窗口
        content_view.addSubview_(scroll_view)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)

def create_menubar():
    """创建菜单栏"""
    menubar = NSMenu.alloc().init()
    
    app_menu = NSMenu.alloc().init()
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit Direct Test", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    
    app_menu_item = NSMenuItem.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    menubar.addItem_(app_menu_item)
    
    return menubar

if __name__ == "__main__":
    print("=== 直接修复的TableView测试 ===")
    print("完全绕过macUI的组件和工具函数")
    print("直接使用修复的TableView实现")
    
    try:
        # PyObjC最佳实践
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        menubar = create_menubar()
        app.setMainMenu_(menubar)
        
        # 创建应用实例
        test_app = DirectTableTestApp.alloc().init()
        test_app.create_window()
        
        print("✅ 直接修复版本的TableView已创建")
        
        # AppHelper事件循环
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()