#!/usr/bin/env python3
"""
混合布局系统演示
演示新的混合布局功能，包括 TableView 在 VStack 中的使用
"""

import sys
import AppHelper
from AppKit import (
    NSApp, NSApplication, NSApplicationActivationPolicyRegular, NSWindow,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSBackingStoreBuffered, NSMakeRect, NSMenu, NSMenuItem
)
from Foundation import NSObject

# 添加项目路径
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.components import (
    VStack, HStack, FrameContainer, TableView, Button, Label, TextField, LayoutMode
)
from macui.core.signal import Signal


class HybridLayoutDemoApp:
    """混合布局系统演示应用"""
    
    def __init__(self):
        # 创建应用
        NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 创建菜单栏
        self._setup_menu()
        
        # 创建窗口
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 800, 600),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("混合布局系统演示")
        
        # 创建响应式数据
        self.selected_item = Signal("未选择")
        self.item_count = Signal(0)
        
        # 设置UI
        self._setup_ui()
        
        self.window.makeKeyAndOrderFront_(None)
    
    def _setup_menu(self):
        """设置菜单栏"""
        menubar = NSMenu.alloc().init()
        appMenuItem = NSMenuItem.alloc().init()
        menubar.addItem_(appMenuItem)
        NSApp.setMainMenu_(menubar)
        
        appMenu = NSMenu.alloc().init()
        quitMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "退出", "terminate:", "q"
        )
        appMenu.addItem_(quitMenuItem)
        appMenuItem.setSubmenu_(appMenu)
    
    def _setup_ui(self):
        """设置用户界面"""
        
        # 准备表格数据
        table_data = [
            {"name": "苹果", "price": "¥5.99", "category": "水果"},
            {"name": "香蕉", "price": "¥3.50", "category": "水果"},
            {"name": "胡萝卜", "price": "¥2.80", "category": "蔬菜"},
            {"name": "土豆", "price": "¥1.20", "category": "蔬菜"},
            {"name": "鸡蛋", "price": "¥8.00", "category": "蛋类"},
        ]
        
        # 表格列配置
        columns = [
            {"title": "名称", "key": "name", "width": 120},
            {"title": "价格", "key": "price", "width": 100},
            {"title": "分类", "key": "category", "width": 100}
        ]
        
        self.item_count.value = len(table_data)
        
        # 创建表格
        table = TableView(
            columns=columns,
            data=table_data,
            on_select=self._on_table_select,
            frame=(0, 0, 400, 200)
        )
        
        # 测试1：TableView 在 VStack 中（新功能！）
        main_content = VStack(
            spacing=10,
            padding=20,
            children=[
                Label(f"🎉 混合布局演示：TableView 现在可以在 VStack 中使用了！"),
                Label(f"数据项数量: {self.item_count}"),
                Label(f"当前选择: {self.selected_item}"),
                
                # ✅ 这在以前会导致崩溃，现在可以正常工作！
                table,
                
                # 控制按钮
                HStack(
                    spacing=10,
                    children=[
                        Button("添加项目", on_click=self._add_item),
                        Button("删除项目", on_click=self._remove_item),
                        Button("清空选择", on_click=self._clear_selection),
                    ]
                )
            ],
            frame=(0, 0, 760, 560)
        )
        
        # 设置到窗口
        self.window.contentView().addSubview_(main_content)
        
        # 保持引用
        self.main_content = main_content
        self.table = table
        self.table_data = table_data
    
    def _on_table_select(self, row):
        """表格选择回调"""
        if 0 <= row < len(self.table_data):
            item = self.table_data[row]
            self.selected_item.value = f"{item['name']} ({item['price']})"
        else:
            self.selected_item.value = "未选择"
    
    def _add_item(self):
        """添加新项目"""
        new_items = [
            {"name": "新项目1", "price": "¥10.00", "category": "其他"},
            {"name": "新项目2", "price": "¥15.50", "category": "其他"},
        ]
        import random
        new_item = random.choice(new_items)
        new_item["name"] = f"{new_item['name']}_{len(self.table_data)+1}"
        
        self.table_data.append(new_item)
        self.item_count.value = len(self.table_data)
        
        # 这里应该更新表格数据，但为了演示简单化暂时省略
        print(f"添加了项目: {new_item['name']}")
    
    def _remove_item(self):
        """删除最后一个项目"""
        if self.table_data:
            removed = self.table_data.pop()
            self.item_count.value = len(self.table_data)
            print(f"删除了项目: {removed['name']}")
            
            if not self.table_data:
                self.selected_item.value = "未选择"
    
    def _clear_selection(self):
        """清空选择"""
        self.selected_item.value = "未选择"


def test_layout_modes():
    """测试不同的布局模式"""
    
    print("=== 测试布局策略选择 ===")
    
    # 导入测试需要的类
    from macui.components.layout import LayoutStrategy, ComponentType
    from macui.components.basic_controls import Button, Label
    
    # 创建测试组件
    simple_button = Button("测试按钮")
    simple_label = Label("测试标签")
    
    # 创建表格（复杂组件）
    table = TableView(columns=[{"title": "测试", "key": "test", "width": 100}])
    
    # 测试组件类型检测
    print(f"Button 类型: {LayoutStrategy.detect_component_type(simple_button)}")
    print(f"Label 类型: {LayoutStrategy.detect_component_type(simple_label)}")  
    print(f"TableView 类型: {LayoutStrategy.detect_component_type(table)}")
    
    # 测试布局模式选择
    simple_children = [simple_button, simple_label]
    complex_children = [simple_label, table, simple_button]
    
    simple_mode = LayoutStrategy.choose_layout_mode(simple_children)
    complex_mode = LayoutStrategy.choose_layout_mode(complex_children)
    
    print(f"纯简单组件选择模式: {simple_mode}")
    print(f"混合组件选择模式: {complex_mode}")
    
    return True


def main():
    """主函数"""
    print("启动混合布局演示...")
    
    # 运行布局模式测试
    test_layout_modes()
    
    # 创建并运行应用
    app = HybridLayoutDemoApp()
    
    print("应用已启动，按 Cmd+Q 退出")
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()