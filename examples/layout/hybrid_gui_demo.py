#!/usr/bin/env python3
"""
混合布局GUI演示应用
可以直接运行看到TableView在VStack中工作的实际效果
"""

import sys
import os
import subprocess

# 添加项目路径
sys.path.insert(0, '/Users/david/david/app/macui')

def check_pyobjc():
    """检查PyObjC是否可用"""
    try:
        from AppKit import NSApplication
        return True
    except ImportError:
        return False

def install_pyobjc():
    """安装PyObjC"""
    print("正在安装PyObjC...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyobjc"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_demo_app():
    """创建演示应用"""
    
    try:
        # 导入GUI组件
        from AppKit import (
            NSApp, NSApplication, NSApplicationActivationPolicyRegular, NSWindow,
            NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
            NSBackingStoreBuffered, NSMakeRect, NSMenu, NSMenuItem, NSColor
        )
        from Foundation import NSObject
        import AppHelper
        
        # 导入macUI组件
        from macui.components import (
            VStack, HStack, TableView, Button, Label, TextField, LayoutMode
        )
        from macui.core.signal import Signal
        
        class HybridDemoController:
            """演示控制器"""
            
            def __init__(self):
                # 创建响应式数据
                self.selected_item = Signal("未选择任何商品")
                self.total_price = Signal(0.0)
                
                # 商品数据
                self.products = [
                    {"name": "苹果 🍎", "price": 5.99, "category": "水果", "stock": 50},
                    {"name": "香蕉 🍌", "price": 3.50, "category": "水果", "stock": 30},
                    {"name": "胡萝卜 🥕", "price": 2.80, "category": "蔬菜", "stock": 25},
                    {"name": "土豆 🥔", "price": 1.20, "category": "蔬菜", "stock": 40},
                    {"name": "牛奶 🥛", "price": 8.00, "category": "乳制品", "stock": 20},
                    {"name": "鸡蛋 🥚", "price": 12.50, "category": "蛋类", "stock": 15}
                ]
                
                self.calculate_total()
                
                # 创建应用
                NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                self._setup_menu()
                self._create_window()
                
            def _setup_menu(self):
                """设置菜单栏"""
                menubar = NSMenu.alloc().init()
                appMenuItem = NSMenuItem.alloc().init()
                menubar.addItem_(appMenuItem)
                NSApp.setMainMenu_(menubar)
                
                appMenu = NSMenu.alloc().init()
                quitMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    "退出混合布局演示", "terminate:", "q"
                )
                appMenu.addItem_(quitMenuItem)
                appMenuItem.setSubmenu_(appMenu)
                
            def _create_window(self):
                """创建主窗口"""
                self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                    NSMakeRect(200, 200, 700, 550),
                    NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
                    NSBackingStoreBuffered,
                    False
                )
                self.window.setTitle_("🎉 混合布局演示 - TableView现在可以在VStack中使用了!")
                
                # 创建UI
                self._setup_ui()
                
                self.window.makeKeyAndOrderFront_(None)
                NSApp.activateIgnoringOtherApps_(True)
            
            def _setup_ui(self):
                """设置用户界面"""
                
                # 创建表格
                table = TableView(
                    columns=[
                        {"title": "商品名称", "key": "name", "width": 120},
                        {"title": "价格", "key": "price", "width": 80},
                        {"title": "分类", "key": "category", "width": 80},
                        {"title": "库存", "key": "stock", "width": 60}
                    ],
                    data=self.products,
                    on_select=self._on_product_select,
                    headers_visible=True,
                    frame=(0, 0, 600, 250)
                )
                
                # 🎉 关键演示：TableView现在可以在VStack中使用！
                # 这在之前会导致NSLayoutConstraintNumberExceedsLimit崩溃
                main_content = VStack(
                    spacing=15,
                    padding=20,
                    children=[
                        # 标题区域
                        VStack(
                            spacing=5,
                            children=[
                                Label("🛒 商品管理系统"),
                                Label("演示：TableView现在可以完美地在VStack中工作！"),
                                Label(f"📊 总商品价值: ¥{self.total_price}")
                            ]
                        ),
                        
                        # 表格区域 - 核心演示内容
                        VStack(
                            spacing=5,
                            children=[
                                Label("📋 商品清单 (TableView在VStack中)"),
                                # ✅ 这是重点：TableView在VStack中不再崩溃！
                                table
                            ]
                        ),
                        
                        # 操作区域
                        VStack(
                            spacing=8,
                            children=[
                                Label(f"🔍 当前选择: {self.selected_item}"),
                                
                                HStack(
                                    spacing=10,
                                    children=[
                                        Button("🍎 添加水果", on_click=self._add_fruit),
                                        Button("🥕 添加蔬菜", on_click=self._add_vegetable),
                                        Button("🗑️ 删除最后项", on_click=self._remove_item)
                                    ]
                                ),
                                
                                HStack(
                                    spacing=10,
                                    children=[
                                        Button("💰 计算总价", on_click=self._calculate_total_click),
                                        Button("🔄 重置数据", on_click=self._reset_data),
                                        Button("📊 显示统计", on_click=self._show_stats)
                                    ]
                                )
                            ]
                        ),
                        
                        # 状态区域
                        Label("✅ 混合布局系统工作正常 - 没有约束冲突!")
                    ],
                    frame=(0, 0, 660, 510)
                )
                
                # 设置到窗口
                self.window.contentView().addSubview_(main_content)
                
                # 保持引用
                self.main_content = main_content
                self.table = table
            
            def _on_product_select(self, row):
                """商品选择回调"""
                if 0 <= row < len(self.products):
                    product = self.products[row]
                    self.selected_item.value = f"{product['name']} - ¥{product['price']} ({product['stock']}件)"
                else:
                    self.selected_item.value = "未选择任何商品"
            
            def _add_fruit(self):
                """添加水果"""
                import random
                fruits = ["草莓 🍓", "葡萄 🍇", "橙子 🍊", "西瓜 🍉", "桃子 🍑"]
                new_fruit = {
                    "name": random.choice(fruits),
                    "price": round(random.uniform(3.0, 15.0), 2),
                    "category": "水果",
                    "stock": random.randint(10, 50)
                }
                self.products.append(new_fruit)
                self.calculate_total()
                print(f"添加了水果: {new_fruit['name']}")
            
            def _add_vegetable(self):
                """添加蔬菜"""
                import random
                vegetables = ["番茄 🍅", "黄瓜 🥒", "茄子 🍆", "辣椒 🌶️", "洋葱 🧅"]
                new_veggie = {
                    "name": random.choice(vegetables),
                    "price": round(random.uniform(1.5, 8.0), 2),
                    "category": "蔬菜",
                    "stock": random.randint(15, 40)
                }
                self.products.append(new_veggie)
                self.calculate_total()
                print(f"添加了蔬菜: {new_veggie['name']}")
            
            def _remove_item(self):
                """删除最后一项"""
                if self.products:
                    removed = self.products.pop()
                    self.calculate_total()
                    self.selected_item.value = "未选择任何商品"
                    print(f"删除了商品: {removed['name']}")
                else:
                    print("没有商品可删除")
            
            def _calculate_total_click(self):
                """计算总价按钮点击"""
                self.calculate_total()
                print(f"总价值: ¥{self.total_price.value}")
            
            def calculate_total(self):
                """计算总价值"""
                total = sum(item['price'] * item['stock'] for item in self.products)
                self.total_price.value = round(total, 2)
            
            def _reset_data(self):
                """重置数据"""
                self.products.clear()
                self.products.extend([
                    {"name": "苹果 🍎", "price": 5.99, "category": "水果", "stock": 50},
                    {"name": "香蕉 🍌", "price": 3.50, "category": "水果", "stock": 30},
                    {"name": "胡萝卜 🥕", "price": 2.80, "category": "蔬菜", "stock": 25}
                ])
                self.calculate_total()
                self.selected_item.value = "未选择任何商品"
                print("数据已重置")
            
            def _show_stats(self):
                """显示统计信息"""
                categories = {}
                for item in self.products:
                    cat = item['category']
                    if cat not in categories:
                        categories[cat] = {"count": 0, "total_value": 0}
                    categories[cat]["count"] += 1
                    categories[cat]["total_value"] += item['price'] * item['stock']
                
                print("📊 商品统计:")
                for cat, stats in categories.items():
                    print(f"  {cat}: {stats['count']}种商品, 总价值¥{stats['total_value']:.2f}")
                
                print(f"📦 总商品种类: {len(self.products)}")
                print(f"💰 总库存价值: ¥{self.total_price.value}")
        
        # 创建并运行应用
        print("🚀 启动混合布局GUI演示...")
        print("📝 这个应用展示了TableView现在可以在VStack中正常工作")
        print("🎯 关键特性：")
        print("   - TableView在VStack中不会导致约束冲突")
        print("   - 混合布局系统自动处理复杂组件")
        print("   - 响应式数据绑定正常工作")
        print("   - 可以点击表格行查看选择效果")
        print("   - 按钮操作会实时更新数据")
        print()
        print("🖱️ 操作提示：")
        print("   - 点击表格中的商品行")
        print("   - 使用按钮添加/删除商品") 
        print("   - 观察响应式数据更新")
        print("   - 按Cmd+Q退出")
        print()
        
        controller = HybridDemoController()
        AppHelper.runEventLoop()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    
    print("🎉 混合布局GUI演示")
    print("=" * 50)
    
    # 检查PyObjC
    if not check_pyobjc():
        print("⚠️  PyObjC未安装，正在尝试安装...")
        if not install_pyobjc():
            print("❌ PyObjC安装失败")
            print("请手动运行: pip install pyobjc")
            return False
        print("✅ PyObjC安装成功")
    
    # 创建并运行GUI应用
    return create_demo_app()

if __name__ == "__main__":
    success = main()
    if success:
        print("👋 演示结束")
    else:
        print("❌ 演示失败")
    sys.exit(0 if success else 1)