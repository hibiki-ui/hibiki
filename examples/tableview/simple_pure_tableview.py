#!/usr/bin/env python3
"""
简单的NSTableView实现 - 纯PyObjC
严格按照NSTableView核心指南实现 + PyObjC最佳实践
"""

import objc
from Foundation import NSObject, NSString
from AppKit import (
    NSApplication, NSWindow, NSScrollView, NSTableView, NSTableColumn,
    NSTextField, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
    NSMakeRect, NSMenu, NSMenuItem, NSApplicationActivationPolicyRegular
)
from PyObjCTools import AppHelper

class SimpleTableDataSource(NSObject):
    """NSTableView数据源 - 严格按照指南实现"""
    
    def init(self):
        self = objc.super(SimpleTableDataSource, self).init()
        if self is None:
            return None
            
        # 简单的数据模型
        self.data = [
            {"name": "张三", "age": 28, "city": "北京"},
            {"name": "李四", "age": 32, "city": "上海"}, 
            {"name": "王五", "age": 25, "city": "广州"},
            {"name": "赵六", "age": 35, "city": "深圳"},
            {"name": "孙七", "age": 29, "city": "杭州"},
        ]
        
        return self
    
    def numberOfRowsInTableView_(self, tableView):
        """核心方法1: 返回行数 - 必须实现"""
        return len(self.data)
    
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        """已废弃方法 - 不应在View-Based表格中使用
        但为了向后兼容，有时仍需要实现
        """
        if row < 0 or row >= len(self.data):
            return ""
        
        column_id = tableColumn.identifier()
        row_data = self.data[row]
        
        return str(row_data.get(column_id, ""))


class SimpleTableDelegate(NSObject):
    """NSTableView代理 - 严格按照指南实现"""
    
    def init(self):
        self = objc.super(SimpleTableDelegate, self).init()
        return self
    
    def tableView_viewForTableColumn_row_(self, tableView, tableColumn, row):
        """核心方法: 为指定行列提供视图 - View-Based表格必须实现"""
        
        # Step 1: 获取列标识符
        column_id = tableColumn.identifier()
        
        # Step 2: 尝试从复用队列获取视图 - 关键性能优化
        cell_view = tableView.makeViewWithIdentifier_owner_(column_id, self)
        
        # Step 3: 如果没有可复用的视图，创建新的
        if cell_view is None:
            cell_view = NSTextField.alloc().init()
            cell_view.setIdentifier_(column_id)
            cell_view.setBezeled_(False)
            cell_view.setDrawsBackground_(False)
            cell_view.setEditable_(False)
            cell_view.setSelectable_(False)
        
        # Step 4: 配置视图内容（无论是复用的还是新创建的）
        data_source = tableView.dataSource()
        if hasattr(data_source, 'data') and 0 <= row < len(data_source.data):
            row_data = data_source.data[row]
            value = row_data.get(column_id, "")
            cell_view.setStringValue_(str(value))
        
        return cell_view
    
    def tableViewSelectionDidChange_(self, notification):
        """选择变化处理"""
        tableView = notification.object()
        selected_row = tableView.selectedRow()
        print(f"选择了行: {selected_row}")
    
    def tableView_shouldSelectRow_(self, tableView, row):
        """决定是否可以选择某行"""
        return True


class AppDelegate(NSObject):
    """应用程序委托 - 处理应用生命周期"""
    
    def init(self):
        self = objc.super(AppDelegate, self).init()
        if self is None:
            return None
        self.window_controller = None
        return self
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成 - 创建窗口控制器"""
        self.window_controller = SimpleTableWindowController.alloc().init()
        self.window_controller.show()


class SimpleTableWindowController(NSObject):
    """窗口控制器 - 处理UI逻辑和TableView"""
    
    def init(self):
        self = objc.super(SimpleTableWindowController, self).init()
        if self is None:
            return None
            
        # 保持强引用防止对象被回收
        self.window = None
        self.table_view = None
        self.data_source = None
        self.delegate = None
        
        return self
    
    def show(self):
        """创建并显示窗口"""
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 500, 400),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | 
            NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable,
            2,  # NSBackingStoreBuffered
            False
        )
        self.window.setTitle_("Simple NSTableView - Pure PyObjC")
        
        # 创建滚动视图
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 20, 460, 360))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setHasHorizontalScroller_(False)
        scroll_view.setAutohidesScrollers_(True)
        
        # 创建表格视图
        self.table_view = NSTableView.alloc().init()
        
        # 创建列
        columns_config = [
            {"title": "姓名", "key": "name", "width": 100},
            {"title": "年龄", "key": "age", "width": 60},
            {"title": "城市", "key": "city", "width": 100},
        ]
        
        for col_config in columns_config:
            column = NSTableColumn.alloc().initWithIdentifier_(col_config["key"])
            column.setWidth_(col_config["width"])
            column.headerCell().setStringValue_(col_config["title"])
            self.table_view.addTableColumn_(column)
        
        # 创建数据源和代理 - 保持强引用
        self.data_source = SimpleTableDataSource.alloc().init()
        self.delegate = SimpleTableDelegate.alloc().init()
        
        # 设置数据源和代理
        self.table_view.setDataSource_(self.data_source)
        self.table_view.setDelegate_(self.delegate)
        
        # 将表格添加到滚动视图
        scroll_view.setDocumentView_(self.table_view)
        
        # 将滚动视图添加到窗口
        self.window.contentView().addSubview_(scroll_view)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)


def create_menubar():
    """创建最小菜单栏 - macOS要求"""
    menubar = NSMenu.alloc().init()
    
    # 应用菜单
    app_menu = NSMenu.alloc().init()
    
    # 退出菜单项
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit Simple TableView", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    
    # 添加到菜单栏
    app_menu_item = NSMenuItem.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    menubar.addItem_(app_menu_item)
    
    return menubar


if __name__ == "__main__":
    print("=== 简单NSTableView示例 ===")
    print("严格按照NSTableView核心指南 + PyObjC最佳实践实现")
    print("- 正确实现数据源和代理模式")
    print("- 使用View-Based表格")
    print("- 实现视图复用机制")
    print("- AppDelegate + WindowController 分离架构")
    
    try:
        # 1. 激活策略 - 让应用获得前台焦点和Dock图标
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 2. 菜单栏 - macOS要求完整应用必须有菜单
        menubar = create_menubar()
        app.setMainMenu_(menubar)
        
        # 3. 分离架构 - AppDelegate负责生命周期
        app_delegate = AppDelegate.alloc().init()
        app.setDelegate_(app_delegate)
        
        print("✅ 应用激活策略设置完成")
        print("✅ 菜单栏创建完成") 
        print("✅ AppDelegate设置完成")
        print("✅ 按Cmd+Q退出应用")
        
        # 4. AppHelper事件循环 - 替代NSApp.run()防止对象被垃圾回收
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()