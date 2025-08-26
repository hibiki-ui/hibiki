#!/usr/bin/env python3
"""
高级NSTableView实现 - 纯PyObjC
完整功能特性：动态数据、排序、选择、自定义视图、性能优化 + PyObjC最佳实践
"""

import objc
from Foundation import NSObject, NSString, NSSortDescriptor, NSMutableArray
from AppKit import (
    NSApplication, NSWindow, NSScrollView, NSTableView, NSTableColumn,
    NSTextField, NSButton, NSStackView, NSView,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
    NSMakeRect, NSColor, NSFont, NSUserInterfaceLayoutOrientationVertical,
    NSLayoutAttributeTrailing, NSLayoutAttributeLeading, NSLayoutAttributeCenterY,
    NSMenu, NSMenuItem, NSApplicationActivationPolicyRegular
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
        """为指定行列提供自定义视图"""
        
        column_id = tableColumn.identifier()
        
        # 根据列类型创建不同的视图
        if column_id == "salary":
            return self._create_salary_view(tableView, column_id, row)
        elif column_id == "department":
            return self._create_department_view(tableView, column_id, row)
        else:
            return self._create_text_view(tableView, column_id, row)
    
    def _create_text_view(self, tableView, column_id, row):
        """创建文本视图"""
        cell_view = tableView.makeViewWithIdentifier_owner_(column_id, self)
        
        if cell_view is None:
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
            cell_view.setStringValue_(str(value))
        
        return cell_view
    
    def _create_salary_view(self, tableView, column_id, row):
        """创建薪资视图 - 自定义格式和颜色"""
        cell_view = tableView.makeViewWithIdentifier_owner_(column_id, self)
        
        if cell_view is None:
            cell_view = NSTextField.alloc().init()
            cell_view.setIdentifier_(column_id)
            cell_view.setBezeled_(False)
            cell_view.setDrawsBackground_(False)
            cell_view.setEditable_(False)
            cell_view.setSelectable_(False)
            
            # 设置字体和颜色
            font = NSFont.boldSystemFontOfSize_(12)
            cell_view.setFont_(font)
        
        # 获取薪资数据并格式化
        data_source = tableView.dataSource()
        if hasattr(data_source, 'data') and 0 <= row < len(data_source.data):
            row_data = data_source.data[row]
            salary = row_data.get('salary', 0)
            
            # 格式化薪资显示
            formatted_salary = f"¥{salary:,}"
            cell_view.setStringValue_(formatted_salary)
            
            # 根据薪资范围设置颜色
            if salary >= 12000:
                cell_view.setTextColor_(NSColor.systemGreenColor())
            elif salary >= 8000:
                cell_view.setTextColor_(NSColor.systemBlueColor())
            else:
                cell_view.setTextColor_(NSColor.systemOrangeColor())
        
        return cell_view
    
    def _create_department_view(self, tableView, column_id, row):
        """创建部门视图 - 带背景色的标签"""
        cell_view = tableView.makeViewWithIdentifier_owner_(column_id, self)
        
        if cell_view is None:
            # 创建容器视图
            cell_view = NSView.alloc().init()
            cell_view.setIdentifier_(column_id)
            
            # 创建文本标签
            label = NSTextField.alloc().init()
            label.setBezeled_(False)
            label.setDrawsBackground_(True)
            label.setEditable_(False)
            label.setSelectable_(False)
            label.setAlignment_(1)  # NSTextAlignmentCenter
            
            # 设置圆角 - 需要先启用layer
            label.setWantsLayer_(True)
            if label.layer():
                label.layer().setCornerRadius_(4)
            
            # 添加到容器
            cell_view.addSubview_(label)
            
            # 设置约束
            label.setTranslatesAutoresizingMaskIntoConstraints_(False)
            label.centerXAnchor().constraintEqualToAnchor_(cell_view.centerXAnchor()).setActive_(True)
            label.centerYAnchor().constraintEqualToAnchor_(cell_view.centerYAnchor()).setActive_(True)
            label.widthAnchor().constraintEqualToConstant_(80).setActive_(True)
            label.heightAnchor().constraintEqualToConstant_(20).setActive_(True)
            
            # 保存标签引用 - 使用objc关联对象
            objc.setAssociatedObject(cell_view, b"label", label, objc.OBJC_ASSOCIATION_RETAIN)
        
        # 获取部门数据并配置样式
        data_source = tableView.dataSource()
        if hasattr(data_source, 'data') and 0 <= row < len(data_source.data):
            row_data = data_source.data[row]
            department = row_data.get('department', '')
            
            label = objc.getAssociatedObject(cell_view, b"label")
            label.setStringValue_(department)
            
            # 根据部门设置背景色
            department_colors = {
                '技术部': NSColor.systemBlueColor(),
                '产品部': NSColor.systemGreenColor(),
                '市场部': NSColor.systemOrangeColor(),
                '运营部': NSColor.systemPurpleColor(),
                '设计部': NSColor.systemPinkColor(),
            }
            
            bg_color = department_colors.get(department, NSColor.systemGrayColor())
            label.setBackgroundColor_(bg_color.colorWithAlphaComponent_(0.2))
            label.setTextColor_(bg_color)
        
        return cell_view
    
    def tableView_heightOfRow_(self, tableView, row):
        """自定义行高"""
        return 30  # 稍微高一点以容纳自定义视图
    
    def tableViewSelectionDidChange_(self, notification):
        """选择变化处理"""
        tableView = notification.object()
        selected_row = tableView.selectedRow()
        
        if selected_row >= 0:
            data_source = tableView.dataSource()
            if hasattr(data_source, 'data') and selected_row < len(data_source.data):
                selected_data = data_source.data[selected_row]
                print(f"选择了: {selected_data['name']} - {selected_data['department']}")
        
        if self.selection_callback:
            self.selection_callback(selected_row)
    
    def tableView_sortDescriptorsDidChange_(self, tableView, oldDescriptors):
        """排序变化处理"""
        new_descriptors = tableView.sortDescriptors()
        print(f"排序变化: {[f'{desc.key()}({desc.ascending()})' for desc in new_descriptors]}")
        
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
        print(f"添加了新员工: {new_person['name']}")
    
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
        print("注意：此版本存在自定义视图问题，推荐使用 advanced_pure_tableview_simple.py")
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 500),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | 
            NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable,
            2,  # NSBackingStoreBuffered
            False
        )
        self.window.setTitle_("Advanced NSTableView - Pure PyObjC (有问题版本)")
        
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
    print("=== 高级NSTableView示例 ===")
    print("功能特性:")
    print("- 自定义视图和样式")
    print("- 列排序功能")
    print("- 动态数据添加/删除")
    print("- 性能优化的视图复用")
    print("- 多种数据类型展示")
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
        print("- 使用按钮添加/删除员工")
        print("- 按Cmd+Q退出应用")
        
        # 4. AppHelper事件循环 - 替代NSApp.run()防止对象被垃圾回收
        AppHelper.runEventLoop(installInterrupt=True)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()