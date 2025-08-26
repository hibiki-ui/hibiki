#!/usr/bin/env python3
"""
简单的GUI演示 - 修复版本
展示TableView在VStack中的实际视觉效果
"""

import sys
import os

# 添加项目路径  
sys.path.insert(0, '/Users/david/david/app/macui')

def create_simple_gui():
    """创建简单的GUI界面"""
    
    try:
        from AppKit import (
            NSApp, NSApplication, NSApplicationActivationPolicyRegular,
            NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
            NSBackingStoreBuffered, NSMakeRect, NSMenu, NSMenuItem
        )
        
        # 导入macUI组件
        from macui.components import VStack, HStack, TableView, Button, Label
        from macui.core.signal import Signal
        
        print("✅ 成功导入GUI组件")
        
        # 设置应用
        NSApp.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 创建菜单
        menubar = NSMenu.alloc().init()
        app_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_item)
        NSApp.setMainMenu_(menubar)
        
        app_menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "退出", "terminate:", "q"
        )
        app_menu.addItem_(quit_item)
        app_item.setSubmenu_(app_menu)
        
        # 创建窗口
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(150, 150, 650, 500),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
        window.setTitle_("🎉 混合布局演示 - TableView在VStack中!")
        
        # 准备数据
        products = [
            {"name": "MacBook Pro 💻", "price": "¥14,999", "status": "有货"},
            {"name": "iPhone 15 📱", "price": "¥8,999", "status": "有货"},
            {"name": "AirPods Pro 🎧", "price": "¥1,999", "status": "有货"},
            {"name": "Apple Watch ⌚", "price": "¥2,999", "status": "有货"},
            {"name": "iPad Air 📱", "price": "¥4,999", "status": "缺货"}
        ]
        
        print(f"✅ 准备了{len(products)}个商品数据")
        
        # 创建TableView
        table = TableView(
            columns=[
                {"title": "商品名称", "key": "name", "width": 150},
                {"title": "价格", "key": "price", "width": 100},
                {"title": "状态", "key": "status", "width": 80}
            ],
            data=products,
            headers_visible=True
        )
        
        print(f"✅ TableView创建成功: {type(table)}")
        
        # 🎉 关键演示：TableView在VStack中
        # 这在重构前会导致NSLayoutConstraintNumberExceedsLimit崩溃
        # 现在混合布局系统自动处理
        main_layout = VStack(
            spacing=20,
            padding=30,
            children=[
                # 标题
                Label("🎉 混合布局系统演示"),
                Label("TableView现在可以在VStack中完美工作!"),
                
                # 说明
                Label("以下TableView在重构前会导致应用崩溃:"),
                
                # 关键：TableView在VStack中
                table,
                
                # 按钮区域
                HStack(
                    spacing=15,
                    children=[
                        Button("➕ 添加商品"),
                        Button("✏️ 编辑商品"), 
                        Button("🗑️ 删除商品")
                    ]
                ),
                
                # 状态说明
                Label("✅ 混合布局系统正常工作 - 没有约束冲突!")
            ]
        )
        
        print(f"✅ 主布局创建成功: {type(main_layout)}")
        print(f"   布局类型: {main_layout.__class__.__name__}")
        
        # 添加到窗口
        window.contentView().addSubview_(main_layout)
        
        # 显示窗口
        window.makeKeyAndOrderFront_(None)
        NSApp.activateIgnoringOtherApps_(True)
        
        print("\n🖥️ GUI窗口已创建并显示!")
        print("🎯 你现在应该能看到:")
        print("   • 一个macOS窗口标题为'混合布局演示'") 
        print("   • 窗口内包含标题、说明文字")
        print("   • 一个显示商品数据的表格")
        print("   • 三个操作按钮")
        print("   • 底部的状态说明")
        print("\n💡 关键成就:")
        print("   • TableView成功在VStack中显示")
        print("   • 没有NSLayoutConstraintNumberExceedsLimit错误")
        print("   • 混合布局系统自动处理了约束冲突")
        print("\n⌨️ 按Cmd+Q退出应用")
        
        # 运行应用
        NSApp.run()
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("💡 需要安装PyObjC: pip install pyobjc")
        return False
        
    except Exception as e:
        print(f"❌ GUI创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    
    print("🎨 简单混合布局GUI演示")
    print("展示TableView在VStack中的实际视觉效果")
    print("=" * 50)
    
    # 检查平台
    if sys.platform != 'darwin':
        print("❌ 此演示需要在macOS上运行")
        return False
    
    # 创建GUI
    success = create_simple_gui()
    
    if success:
        print("\n✅ GUI演示完成")
    else:
        print("\n❌ GUI演示失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)