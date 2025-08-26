#!/usr/bin/env python3
"""
真正的GUI演示应用
展示混合布局系统的实际视觉效果 - 可以看到真正的macOS窗口和界面
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, '/Users/david/david/app/macui')

def create_gui_app():
    """创建真正的GUI应用"""
    
    try:
        # 导入所需的macOS框架
        from AppKit import (
            NSApp, NSApplication, NSApplicationActivationPolicyRegular, 
            NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, 
            NSWindowStyleMaskResizable, NSBackingStoreBuffered, NSMakeRect,
            NSMenu, NSMenuItem, NSColor, NSFont, NSRunLoop, NSDefaultRunLoopMode,
            NSDate
        )
        from Foundation import NSObject, NSTimer
        
        # 导入macUI组件
        from macui.components import (
            VStack, HStack, TableView, Button, Label, TextField
        )
        from macui.core.signal import Signal, Effect
        
        print("✅ 成功导入所有必要的组件")
        
        class DemoWindowController(NSObject):
            """演示窗口控制器"""
            
            def init(self):
                self = super().init()
                if self is None:
                    return None
                
                # 创建响应式数据
                self.item_count = Signal(4)
                self.selected_item = Signal("未选择")
                self.status_text = Signal("混合布局系统正常运行")
                
                # 商品数据
                self.products = [
                    {"name": "MacBook Pro", "price": "¥14,999", "category": "电脑", "stock": "5台"},
                    {"name": "iPhone 15 Pro", "price": "¥8,999", "category": "手机", "stock": "12台"},
                    {"name": "AirPods Pro", "price": "¥1,999", "category": "耳机", "stock": "20个"},
                    {"name": "Apple Watch", "price": "¥2,999", "category": "手表", "stock": "8个"}
                ]
                
                self.item_count.value = len(self.products)
                
                # 创建应用和窗口
                self._setup_app()
                self._create_window()
                
                return self
            
            def _setup_app(self):
                """设置应用"""
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                
                # 创建简单的菜单栏
                menubar = NSMenu.alloc().init()
                app_item = NSMenuItem.alloc().init()
                menubar.addItem_(app_item)
                NSApp.setMainMenu_(menubar)
                
                app_menu = NSMenu.alloc().init()
                quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    "退出演示", "terminate:", "q"
                )
                app_menu.addItem_(quit_item)
                app_item.setSubmenu_(app_menu)
                
            def _create_window(self):
                """创建主窗口"""
                self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                    NSMakeRect(100, 100, 750, 600),
                    NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
                    NSBackingStoreBuffered,
                    False
                )
                
                self.window.setTitle_("🎉 macUI 混合布局演示 - TableView在VStack中!")
                
                # 设置窗口背景色
                self.window.setBackgroundColor_(NSColor.controlBackgroundColor())
                
                # 创建UI
                self._create_ui()
                
                # 显示窗口
                self.window.makeKeyAndOrderFront_(None)
                NSApp.activateIgnoringOtherApps_(True)
            
            def _create_ui(self):
                """创建用户界面"""
                
                # 创建表格
                table = TableView(
                    columns=[
                        {"title": "商品名称", "key": "name", "width": 140},
                        {"title": "价格", "key": "price", "width": 100},
                        {"title": "分类", "key": "category", "width": 80},
                        {"title": "库存", "key": "stock", "width": 80}
                    ],
                    data=self.products,
                    on_select=self.on_table_select,
                    headers_visible=True
                )
                
                # 🎉 关键演示：这是混合布局的核心 - TableView在VStack中!
                # 在重构前，这会导致 NSLayoutConstraintNumberExceedsLimit 崩溃
                # 现在混合布局系统会自动检测并切换到frame布局模式
                
                main_layout = VStack(
                    spacing=15,
                    padding=25,
                    children=[
                        # 标题区域
                        VStack(
                            spacing=8,
                            children=[
                                Label("🎉 混合布局系统演示"),
                                Label("TableView 现在可以完美地在 VStack 中工作了！"),
                                Label(f"📊 商品总数: {self.item_count}")
                            ]
                        ),
                        
                        # 重点演示区域
                        VStack(
                            spacing=10,
                            children=[
                                Label("🔥 核心演示：TableView 在 VStack 中"),
                                Label("以下表格在重构前会导致应用崩溃，现在完美工作:"),
                                
                                # ✅ 这是关键！TableView现在可以在VStack中使用
                                table
                            ]
                        ),
                        
                        # 状态显示
                        VStack(
                            spacing=5,
                            children=[
                                Label(f"🔍 当前选择: {self.selected_item}"),
                                Label(f"📱 状态: {self.status_text}")
                            ]
                        ),
                        
                        # 操作按钮区域
                        HStack(
                            spacing=12,
                            children=[
                                Button("➕ 添加商品", on_click=self.add_product),
                                Button("🗑️ 删除商品", on_click=self.remove_product),
                                Button("🔄 刷新数据", on_click=self.refresh_data),
                                Button("📊 显示统计", on_click=self.show_stats)
                            ]
                        ),
                        
                        # 技术说明
                        VStack(
                            spacing=3,
                            children=[
                                Label("💡 技术说明:"),
                                Label("• 混合布局系统自动检测到TableView（复杂组件）"),
                                Label("• VStack自动从约束布局切换到frame布局模式"), 
                                Label("• 没有NSLayoutConstraintNumberExceedsLimit错误"),
                                Label("• 保持所有响应式特性和事件处理")
                            ]
                        )
                    ],
                    frame=(0, 0, 700, 550)
                )
                
                # 添加到窗口
                self.window.contentView().addSubview_(main_layout)
                
                # 保持强引用
                self.main_layout = main_layout
                self.table = table
                
                print("✅ GUI界面创建成功!")
                print(f"   主布局类型: {main_layout.__class__.__name__}")
                print("   🎯 关键成就: TableView成功在VStack中工作，没有约束冲突!")
            
            def on_table_select(self, row):
                """表格选择回调"""
                if 0 <= row < len(self.products):
                    product = self.products[row]
                    self.selected_item.value = f"{product['name']} - {product['price']}"
                else:
                    self.selected_item.value = "未选择"
                print(f"用户选择了: {self.selected_item.value}")
            
            def add_product(self):
                """添加商品"""
                import random
                new_products = [
                    {"name": "iPad Pro", "price": "¥6,999", "category": "平板", "stock": "3台"},
                    {"name": "Mac Studio", "price": "¥15,999", "category": "电脑", "stock": "2台"},
                    {"name": "Studio Display", "price": "¥11,999", "category": "显示器", "stock": "1台"},
                    {"name": "Magic Keyboard", "price": "¥2,399", "category": "配件", "stock": "10个"}
                ]
                
                new_product = random.choice(new_products)
                self.products.append(new_product)
                self.item_count.value = len(self.products)
                self.status_text.value = f"已添加商品: {new_product['name']}"
                print(f"添加了商品: {new_product['name']}")
            
            def remove_product(self):
                """删除商品"""
                if self.products:
                    removed = self.products.pop()
                    self.item_count.value = len(self.products)
                    self.status_text.value = f"已删除商品: {removed['name']}"
                    self.selected_item.value = "未选择"
                    print(f"删除了商品: {removed['name']}")
                else:
                    self.status_text.value = "没有商品可删除"
            
            def refresh_data(self):
                """刷新数据"""
                self.status_text.value = "数据已刷新"
                print("数据已刷新")
            
            def show_stats(self):
                """显示统计"""
                categories = {}
                for product in self.products:
                    cat = product['category']
                    categories[cat] = categories.get(cat, 0) + 1
                
                stats_text = f"商品统计: {', '.join([f'{k}({v}个)' for k, v in categories.items()])}"
                self.status_text.value = stats_text
                print(f"统计信息: {stats_text}")
        
        # 创建并显示应用
        print("🚀 启动真正的macOS GUI演示应用...")
        print("📱 即将显示包含TableView的VStack界面")
        
        controller = DemoWindowController.alloc().init()
        
        print("\n🎯 演示重点:")
        print("   1. 窗口中的TableView位于VStack布局中")
        print("   2. 在重构前这会导致NSLayoutConstraintNumberExceedsLimit崩溃")
        print("   3. 现在混合布局系统自动处理，完美工作")
        print("   4. 你可以:")
        print("      - 点击表格行查看选择效果")
        print("      - 使用按钮添加/删除商品")
        print("      - 观察响应式数据更新")
        print("      - 按Cmd+Q退出应用")
        print("\n🖥️ GUI窗口应该已经出现，请查看屏幕!")
        
        # 运行应用事件循环
        # 使用简单的runloop而不是AppHelper
        try:
            NSApp.run()
        except KeyboardInterrupt:
            print("\n👋 用户中断，退出应用")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 可能需要安装PyObjC:")
        print("   pip install pyobjc-framework-Cocoa")
        return False
        
    except Exception as e:
        print(f"❌ GUI应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    
    print("🎨 macUI 混合布局GUI演示")
    print("=" * 50)
    
    # 检查是否在macOS上运行
    if sys.platform != 'darwin':
        print("❌ 此演示需要在macOS上运行")
        return False
    
    # 尝试创建GUI应用
    success = create_gui_app()
    
    if success:
        print("\n✅ GUI演示完成")
    else:
        print("\n❌ GUI演示失败")
        print("\n🔧 故障排除:")
        print("   1. 确保在macOS上运行")
        print("   2. 检查PyObjC是否正确安装")
        print("   3. 尝试: pip install pyobjc-framework-Cocoa")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)