#!/usr/bin/env python3
"""
高级NSTableView实现 - 纯PyObjC (简化版)
完整功能特性：动态数据、排序、选择、性能优化 + PyObjC最佳实践
避免复杂的自定义视图，专注于核心功能
"""

import objc
from Foundation import NSObject, NSString, NSSortDescriptor, NSMutableArray
from AppKit import (
    NSApplication, NSWindow, NSScrollView, NSTableView, NSTableColumn,
    NSTextField, NSButton, NSStackView,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
    NSMakeRect, NSColor, NSFont, NSMenu, NSMenuItem, NSApplicationActivationPolicyRegular
)
from PyObjCTools import AppHelper

class AdvancedTableDataSource(NSObject):
    """高级NSTableView数据源 - 支持动态数据和排序"""
    
    def init(self):
        self = objc.super(AdvancedTableDataSource, self).init()
        if self is None:
            return None
            
        # 更复杂的数据模型
        self.original_data = [
            {"name": "张三", "age": 28, "city": "北京", "salary": 8000, "department": "技术部"},
            {"name": "李四", "age": 32, "city": "上海", "salary": 12000, "department": "产品部"},
            {"name": "王五", "age": 25, "city": "广州", "salary": 6500, "department": "市场部"},
            {"name": "赵六", "age": 35, "city": "深圳", "salary": 15000, "department": "技术部"},
            {"name": "孙七", "age": 29, "city": "杭州", "salary": 9500, "department": "运营部"},
            {"name": "周八", "age": 26, "city": "成都", "salary": 7000, "department": "设计部"},
            {"name": "吴九", "age": 31, "city": "武汉", "salary": 11000, "department": "技术部"},
            {"name": "郑十", "age": 27, "city": "南京", "salary": 8500, "department": "产品部"},
        ]
        self.data = list(self.original_data)  # 当前显示的数据（可能被排序）
        
        return self
    
    def numberOfRowsInTableView_(self, tableView):
        """核心方法1: 返回行数"""
        return len(self.data)
    
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        """兼容方法 - 用于排序等功能"""
        if row < 0 or row >= len(self.data):
            return ""
        
        column_id = tableColumn.identifier()
        row_data = self.data[row]
        
        return row_data.get(column_id, "")
    
    def add_person(self, person_data):
        """添加新数据"""
        self.data.append(person_data)
        self.original_data.append(person_data)
    
    def remove_person(self, row):
        """移除数据"""
        if 0 <= row < len(self.data):
            removed = self.data.pop(row)
            if removed in self.original_data:
                self.original_data.remove(removed)
            return removed
        return None
    
    def sort_data(self, sort_descriptors):
        """根据排序描述符排序数据"""
        if not sort_descriptors:
            return
        
        # 简单排序实现
        for desc in reversed(sort_descriptors):
            key = desc.key()
            ascending = desc.ascending()
            
            def sort_key(item):
                value = item.get(key, "")
                # 尝试转换为数字以支持数值排序
                try:
                    return float(value) if isinstance(value, (int, float, str)) else str(value)
                except:
                    return str(value)
            
            self.data.sort(key=sort_key, reverse=not ascending)


class AdvancedTableDelegate(NSObject):
    """高级NSTableView代理 - 支持自定义视图和交互"""
    
    def init(self):
        self = objc.super(AdvancedTableDelegate, self).init()
        self.selection_callback = None
        return self
    
    def tableView_viewForTableColumn_row_(self, tableView, tableColumn, row):
        """为指定行列提供视图 - 简化版本，专注性能"""
        
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
            
            # 格式化显示
            if column_id == "salary":
                formatted_value = f"¥{value:,}"
                cell_view.setStringValue_(formatted_value)
                # 根据薪资设置颜色
                if value >= 12000:
                    cell_view.setTextColor_(NSColor.systemGreenColor())
                elif value >= 8000:
                    cell_view.setTextColor_(NSColor.systemBlueColor())
                else:
                    cell_view.setTextColor_(NSColor.systemOrangeColor())
            else:
                cell_view.setStringValue_(str(value))
                cell_view.setTextColor_(NSColor.labelColor())
        
        return cell_view
    
    def tableView_heightOfRow_(self, tableView, row):
        """自定义行高"""
        return 25  # 标准行高
    
    def tableViewSelectionDidChange_(self, notification):
        """选择变化处理"""
        tableView = notification.object()
        selected_row = tableView.selectedRow()
        
        if selected_row >= 0:
            data_source = tableView.dataSource()
            if hasattr(data_source, 'data') and selected_row < len(data_source.data):
                selected_data = data_source.data[selected_row]
                print(f"选择了: {selected_data['name']} - {selected_data['department']} (薪资: ¥{selected_data['salary']:,})")
        
        if self.selection_callback:
            self.selection_callback(selected_row)
    
    def tableView_sortDescriptorsDidChange_(self, tableView, oldDescriptors):
        """排序变化处理"""
        new_descriptors = tableView.sortDescriptors()
        sort_info = []
        for desc in new_descriptors:
            direction = "升序" if desc.ascending() else "降序"
            sort_info.append(f'{desc.key()}({direction})')
        print(f"排序变化: {sort_info}")
        
        # 对数据源进行排序
        data_source = tableView.dataSource()
        if hasattr(data_source, 'sort_data'):
            data_source.sort_data(new_descriptors)
            tableView.reloadData()


class TableControlPanel(NSObject):
    """表格控制面板 - 演示动态数据操作"""
    
    def initWithTableView_(self, table_view):
        self = objc.super(TableControlPanel, self).init()
        if self is None:
            return None
        
        self.table_view = table_view
        return self
    
    def addRandomPerson_(self, sender):
        """添加随机人员"""
        import random
        
        names = ["新员工A", "新员工B", "新员工C", "新员工D"]
        cities = ["北京", "上海", "深圳", "杭州", "成都"]
        departments = ["技术部", "产品部", "市场部", "运营部", "设计部"]
        
        new_person = {
            "name": random.choice(names) + str(random.randint(1, 99)),
            "age": random.randint(22, 45),
            "city": random.choice(cities),
            "salary": random.randint(5000, 20000),
            "department": random.choice(departments)
        }
        
        data_source = self.table_view.dataSource()
        data_source.add_person(new_person)
        self.table_view.reloadData()
        print(f"添加了新员工: {new_person['name']} - {new_person['department']} (薪资: ¥{new_person['salary']:,})")
    
    def removeSelectedPerson_(self, sender):
        """移除选中的人员"""
        selected_row = self.table_view.selectedRow()
        if selected_row >= 0:
            data_source = self.table_view.dataSource()
            removed = data_source.remove_person(selected_row)
            if removed:
                self.table_view.reloadData()
                print(f"移除了员工: {removed['name']}")
        else:
            print("请先选择要移除的员工")
    
    def clearAllData_(self, sender):
        """清空所有数据"""
        data_source = self.table_view.dataSource()
        data_source.data = []
        self.table_view.reloadData()
        print("清空了所有数据")
    
    def resetData_(self, sender):
        """重置为原始数据"""
        data_source = self.table_view.dataSource()
        data_source.data = list(data_source.original_data)
        self.table_view.reloadData()
        print("重置为原始数据")


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
        self.window_controller = AdvancedTableWindowController.alloc().init()
        self.window_controller.show()


class AdvancedTableWindowController(NSObject):
    """窗口控制器 - 处理UI逻辑和TableView"""
    
    def init(self):
        self = objc.super(AdvancedTableWindowController, self).init()
        if self is None:
            return None
            
        # 保持强引用防止对象被回收
        self.window = None
        self.table_view = None
        self.data_source = None
        self.delegate = None
        self.control_panel = None
        
        return self
    
    def show(self):
        """创建并显示窗口"""
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 500),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | 
            NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable,
            2,  # NSBackingStoreBuffered
            False
        )
        self.window.setTitle_("Advanced NSTableView - Pure PyObjC (Simplified)")
        
        # 创建主容器
        content_view = self.window.contentView()
        
        # 创建控制按钮栈
        button_stack = NSStackView.alloc().initWithFrame_(NSMakeRect(20, 450, 660, 30))
        button_stack.setOrientation_(0)  # NSUserInterfaceLayoutOrientationHorizontal
        button_stack.setSpacing_(10)
        
        # 创建滚动视图
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 20, 660, 420))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setHasHorizontalScroller_(False)
        scroll_view.setAutohidesScrollers_(True)
        
        # 创建表格视图
        self.table_view = NSTableView.alloc().init()
        
        # 创建列（包含排序功能）
        columns_config = [
            {"title": "姓名", "key": "name", "width": 100, "sortable": True},
            {"title": "年龄", "key": "age", "width": 60, "sortable": True},
            {"title": "城市", "key": "city", "width": 80, "sortable": True},
            {"title": "薪资", "key": "salary", "width": 120, "sortable": True},
            {"title": "部门", "key": "department", "width": 100, "sortable": True},
        ]
        
        for col_config in columns_config:
            column = NSTableColumn.alloc().initWithIdentifier_(col_config["key"])
            column.setWidth_(col_config["width"])
            column.headerCell().setStringValue_(col_config["title"])
            
            # 启用排序
            if col_config.get("sortable", False):
                sort_descriptor = NSSortDescriptor.alloc().initWithKey_ascending_(
                    col_config["key"], True
                )
                column.setSortDescriptorPrototype_(sort_descriptor)
            
            self.table_view.addTableColumn_(column)
        
        # 创建数据源和代理 - 保持强引用
        self.data_source = AdvancedTableDataSource.alloc().init()
        self.delegate = AdvancedTableDelegate.alloc().init()
        
        # 设置数据源和代理
        self.table_view.setDataSource_(self.data_source)
        self.table_view.setDelegate_(self.delegate)
        
        # 启用排序
        self.table_view.setSortDescriptors_([])
        
        # 将表格添加到滚动视图
        scroll_view.setDocumentView_(self.table_view)
        
        # 创建控制面板 - 保持强引用
        self.control_panel = TableControlPanel.alloc().initWithTableView_(self.table_view)
        
        # 创建控制按钮
        add_button = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 80, 25))
        add_button.setTitle_("添加员工")
        add_button.setTarget_(self.control_panel)
        add_button.setAction_("addRandomPerson:")
        
        remove_button = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 80, 25))
        remove_button.setTitle_("移除选中")
        remove_button.setTarget_(self.control_panel)
        remove_button.setAction_("removeSelectedPerson:")
        
        clear_button = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 60, 25))
        clear_button.setTitle_("清空")
        clear_button.setTarget_(self.control_panel)
        clear_button.setAction_("clearAllData:")
        
        reset_button = NSButton.alloc().initWithFrame_(NSMakeRect(0, 0, 60, 25))
        reset_button.setTitle_("重置")
        reset_button.setTarget_(self.control_panel)
        reset_button.setAction_("resetData:")
        
        # 添加按钮到栈
        button_stack.addArrangedSubview_(add_button)
        button_stack.addArrangedSubview_(remove_button)
        button_stack.addArrangedSubview_(clear_button)
        button_stack.addArrangedSubview_(reset_button)
        
        # 添加到窗口
        content_view.addSubview_(button_stack)
        content_view.addSubview_(scroll_view)
        
        # 显示窗口
        self.window.makeKeyAndOrderFront_(None)


def create_menubar():
    """创建最小菜单栏 - macOS要求"""
    menubar = NSMenu.alloc().init()
    
    # 应用菜单
    app_menu = NSMenu.alloc().init()
    
    # 退出菜单项
    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit Advanced TableView", "terminate:", "q"
    )
    app_menu.addItem_(quit_item)
    
    # 添加到菜单栏
    app_menu_item = NSMenuItem.alloc().init()
    app_menu_item.setSubmenu_(app_menu)
    menubar.addItem_(app_menu_item)
    
    return menubar


if __name__ == "__main__":
    print("=== 高级NSTableView示例 (简化版) ===")
    print("功能特性:")
    print("- View-Based表格 + 视图复用")
    print("- 列排序功能")
    print("- 动态数据添加/删除/清空/重置")
    print("- 条件格式化显示（薪资颜色）")
    print("- 严格按照NSTableView指南 + PyObjC最佳实践")
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
        print("✅ 强引用链建立，防止对象回收")
        
        print("\n操作说明:")
        print("- 点击列标题进行排序")
        print("- 选择行查看详细信息")
        print("- 使用按钮进行数据操作")
        print("- 薪资列有颜色编码")
        print("- 按Cmd+Q退出应用")
        
        # 4. AppHelper事件循环 - 替代NSApp.run()防止对象被垃圾回收
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()