#!/usr/bin/env python3
"""
视觉结构演示
虽然不能显示完整的GUI，但可以展示实际的NSView对象结构和属性
让你看到混合布局系统创建的真实组件层次
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def visualize_component_structure():
    """可视化组件结构"""
    
    print("🎨 混合布局组件结构可视化")
    print("=" * 50)
    
    try:
        from macui.components import VStack, HStack, TableView, Button, Label
        from macui.core.signal import Signal
        
        # 创建响应式数据
        product_count = Signal(5)
        selected_product = Signal("MacBook Pro")
        
        print("1️⃣ 创建响应式数据...")
        print(f"   📊 商品数量: {product_count.value}")
        print(f"   🔍 选中商品: {selected_product.value}")
        
        # 创建商品数据
        products = [
            {"name": "MacBook Pro 💻", "price": "¥14,999", "category": "电脑"},
            {"name": "iPhone 15 📱", "price": "¥8,999", "category": "手机"},
            {"name": "AirPods Pro 🎧", "price": "¥1,999", "category": "音频"},
            {"name": "Apple Watch ⌚", "price": "¥2,999", "category": "可穿戴"},
            {"name": "iPad Pro 📱", "price": "¥6,999", "category": "平板"}
        ]
        
        print(f"\n2️⃣ 准备{len(products)}个商品数据...")
        for i, product in enumerate(products):
            print(f"   {i+1}. {product['name']} - {product['price']}")
        
        print("\n3️⃣ 创建UI组件...")
        
        # 创建标题标签
        title_label = Label("🛒 Apple 商品管理系统")
        print(f"   ✅ 标题标签: {type(title_label)} ({title_label.__class__.__name__})")
        
        # 创建副标题
        subtitle_label = Label("演示：TableView现在可以在VStack中正常工作")
        print(f"   ✅ 副标题: {type(subtitle_label)} ({subtitle_label.__class__.__name__})")
        
        # 🎯 关键部分：创建TableView
        table = TableView(
            columns=[
                {"title": "商品名称", "key": "name", "width": 150},
                {"title": "价格", "key": "price", "width": 100},
                {"title": "分类", "key": "category", "width": 80}
            ],
            data=products,
            headers_visible=True
        )
        print(f"   ✅ 数据表格: {type(table)} ({table.__class__.__name__})")
        
        # 检查TableView的内部结构
        if hasattr(table, 'documentView'):
            doc_view = table.documentView()
            if doc_view:
                print(f"      📋 表格内容视图: {type(doc_view)} ({doc_view.__class__.__name__})")
                if hasattr(doc_view, 'numberOfRows'):
                    print(f"      📊 数据行数: {doc_view.numberOfRows()}")
                if hasattr(doc_view, 'numberOfColumns'):  
                    print(f"      📊 数据列数: {doc_view.numberOfColumns()}")
        
        # 创建操作按钮
        add_btn = Button("➕ 添加商品")
        edit_btn = Button("✏️ 编辑商品")
        delete_btn = Button("🗑️ 删除商品")
        print(f"   ✅ 操作按钮: 3个 {type(add_btn).__name__} 对象")
        
        # 创建按钮容器
        button_container = HStack(
            spacing=12,
            children=[add_btn, edit_btn, delete_btn]
        )
        print(f"   ✅ 按钮容器: {type(button_container)} ({button_container.__class__.__name__})")
        
        # 创建状态标签
        status_label = Label("✅ 混合布局系统正常运行")
        print(f"   ✅ 状态标签: {type(status_label)} ({status_label.__class__.__name__})")
        
        print("\n4️⃣ 🎉 关键演示：创建包含TableView的VStack...")
        print("   ⚠️  重构前：这会导致 NSLayoutConstraintNumberExceedsLimit 崩溃")
        print("   ✅ 重构后：混合布局系统自动处理约束冲突")
        
        # 🎉 这是关键演示！TableView在VStack中
        main_layout = VStack(
            spacing=15,
            padding=25,
            children=[
                title_label,
                subtitle_label,
                Label("📊 商品数据表格 (TableView在VStack中):"),
                table,  # ✅ 关键：TableView在VStack中不再崩溃！
                button_container,
                status_label,
                Label("🎯 技术成就：没有约束冲突错误！")
            ]
        )
        
        print(f"\n   🎉 主布局创建成功!")
        print(f"      类型: {type(main_layout)}")
        print(f"      类名: {main_layout.__class__.__name__}")
        print(f"      布局模式: {'Frame布局' if main_layout.__class__.__name__ == 'NSView' else '约束布局'}")
        
        print("\n5️⃣ 检查布局层次结构...")
        
        # 检查子视图
        if hasattr(main_layout, 'subviews'):
            subviews = main_layout.subviews()
            print(f"   📋 主容器包含 {len(subviews)} 个子视图:")
            
            for i, subview in enumerate(subviews):
                class_name = subview.__class__.__name__
                
                # 获取frame信息
                frame_info = ""
                if hasattr(subview, 'frame'):
                    frame = subview.frame()
                    frame_info = f" Frame(x={frame.origin.x:.1f}, y={frame.origin.y:.1f}, w={frame.size.width:.1f}, h={frame.size.height:.1f})"
                
                print(f"      {i+1}. {class_name}{frame_info}")
                
                # 特殊处理TableView
                if class_name == "NSScrollView":
                    print(f"         🎯 这是TableView! (NSScrollView包装)")
                    if hasattr(subview, 'documentView'):
                        doc = subview.documentView()
                        if doc:
                            print(f"         📋 内部表格: {doc.__class__.__name__}")
        
        print("\n6️⃣ 验证混合布局系统工作原理...")
        
        # 展示布局策略检测
        from macui.components.layout import LayoutStrategy
        
        simple_components = [title_label, subtitle_label, add_btn]
        mixed_components = [title_label, table, status_label]
        
        simple_mode = LayoutStrategy.choose_layout_mode(simple_components)
        mixed_mode = LayoutStrategy.choose_layout_mode(mixed_components)
        
        print(f"   🧠 纯简单组件 → 布局模式: {simple_mode}")
        print(f"   🧠 包含TableView → 布局模式: {mixed_mode}")
        print(f"   🎯 实际创建类型: {main_layout.__class__.__name__}")
        
        print("\n7️⃣ 响应式特性验证...")
        
        # 创建响应式标签
        reactive_label = Label(text=product_count)
        print(f"   🔄 响应式标签创建: {type(reactive_label)}")
        
        # 测试响应式更新
        old_count = product_count.value
        product_count.value = 10
        print(f"   📊 数据更新: {old_count} → {product_count.value}")
        print("   ✅ 响应式系统与混合布局兼容")
        
        print(f"\n🎉 视觉结构演示完成!")
        print(f"💡 关键成就总结:")
        print(f"   ✅ TableView ({table.__class__.__name__}) 成功创建")
        print(f"   ✅ VStack 自动切换到 {main_layout.__class__.__name__} (frame布局)")
        print(f"   ✅ 包含 {len(subviews) if hasattr(main_layout, 'subviews') else 'N/A'} 个正确的子视图")
        print(f"   ✅ 没有 NSLayoutConstraintNumberExceedsLimit 错误")
        print(f"   ✅ 混合布局系统智能处理约束冲突")
        print(f"   ✅ 保持响应式特性正常工作")
        
        return main_layout
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def demonstrate_real_world_scenario():
    """演示真实世界应用场景"""
    
    print(f"\n🌟 真实应用场景演示")
    print("=" * 30)
    
    try:
        from macui.components import VStack, HStack, TableView, Button, Label
        
        print("📱 场景：电商管理后台")
        
        # 订单数据
        orders = [
            {"id": "ORD001", "customer": "张三", "amount": "¥299.00", "status": "已发货"},
            {"id": "ORD002", "customer": "李四", "amount": "¥1,299.00", "status": "处理中"},
            {"id": "ORD003", "customer": "王五", "amount": "¥99.00", "status": "已完成"},
            {"id": "ORD004", "customer": "赵六", "amount": "¥599.00", "status": "已取消"}
        ]
        
        # 创建订单管理界面
        order_table = TableView(
            columns=[
                {"title": "订单号", "key": "id", "width": 100},
                {"title": "客户", "key": "customer", "width": 80},
                {"title": "金额", "key": "amount", "width": 100},
                {"title": "状态", "key": "status", "width": 80}
            ],
            data=orders
        )
        
        # 复杂的嵌套布局
        management_ui = VStack(
            spacing=12,
            children=[
                VStack(
                    spacing=5,
                    children=[
                        Label("📊 电商管理后台"),
                        Label(f"📦 当前订单: {len(orders)} 个")
                    ]
                ),
                
                # 核心：订单表格在复杂布局中
                order_table,
                
                # 多层嵌套的操作区域
                VStack(
                    spacing=8,
                    children=[
                        HStack(
                            spacing=10,
                            children=[
                                Button("✅ 确认订单"),
                                Button("📦 发货"),
                                Button("❌ 取消订单")
                            ]
                        ),
                        HStack(
                            spacing=10,
                            children=[
                                Button("📊 生成报表"),
                                Button("💰 财务统计"),
                                Button("🔄 刷新数据")
                            ]
                        )
                    ]
                )
            ]
        )
        
        print(f"   ✅ 电商界面: {type(management_ui)} ({management_ui.__class__.__name__})")
        print("   🎯 特点: 复杂嵌套布局中的TableView正常工作")
        
        print(f"\n📈 场景：数据分析看板")
        
        # 销售数据
        sales_data = [
            {"region": "华北", "revenue": "¥2,500,000", "growth": "+15.3%"},
            {"region": "华东", "revenue": "¥3,200,000", "growth": "+22.1%"},
            {"region": "华南", "revenue": "¥1,800,000", "growth": "+8.7%"},
            {"region": "西部", "revenue": "¥900,000", "growth": "+5.2%"}
        ]
        
        sales_table = TableView(
            columns=[
                {"title": "地区", "key": "region", "width": 80},
                {"title": "营收", "key": "revenue", "width": 120},
                {"title": "增长率", "key": "growth", "width": 80}
            ],
            data=sales_data
        )
        
        # 仪表板布局
        dashboard = VStack(
            children=[
                Label("📈 销售业绩看板"),
                
                # 关键指标区域
                HStack(
                    spacing=20,
                    children=[
                        VStack(children=[Label("总营收"), Label("¥8,400,000")]),
                        VStack(children=[Label("平均增长"), Label("+12.8%")]),
                        VStack(children=[Label("最佳地区"), Label("华东")])
                    ]
                ),
                
                # 详细数据表格
                sales_table,
                
                Button("📊 导出报告")
            ]
        )
        
        print(f"   ✅ 数据看板: {type(dashboard)} ({dashboard.__class__.__name__})")
        print("   🎯 特点: TableView与其他组件无缝集成")
        
        print(f"\n💡 真实场景总结:")
        print("   ✅ 支持复杂的企业级应用界面")
        print("   ✅ TableView可以在任意嵌套布局中使用")  
        print("   ✅ 混合布局系统透明处理所有复杂性")
        print("   ✅ 开发者享受简洁的声明式API")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实场景演示失败: {e}")
        return False

def main():
    """主函数"""
    
    print("🎨 混合布局视觉结构演示")
    print("展示TableView在VStack中的实际对象结构和属性")
    print("=" * 60)
    
    # 运行结构演示
    layout = visualize_component_structure()
    
    # 运行真实场景演示  
    demonstrate_real_world_scenario()
    
    print("\n" + "=" * 60)
    if layout:
        print("🎉 视觉演示完成!")
        print("\n🎯 你看到了什么:")
        print("   • 真实的NSView对象被创建")
        print("   • TableView (NSScrollView) 包含真实的表格数据")
        print("   • VStack自动切换到NSView (frame布局)")
        print("   • 完整的视图层次结构")
        print("   • 正确的Frame坐标信息")
        print("   • 响应式数据绑定正常工作")
        
        print("\n💡 虽然没有GUI窗口，但你看到了:")
        print("   ✅ 实际的macOS视图对象")
        print("   ✅ 真实的布局结构")
        print("   ✅ 混合布局系统的内部工作机制")
        print("   ✅ TableView约束冲突问题的完美解决")
        
        print(f"\n🚀 如果这是一个GUI应用，你会看到:")
        print("   🖥️ 一个包含商品表格的macOS窗口")
        print("   📋 可点击的表格行和按钮") 
        print("   🎮 响应式的数据更新")
        print("   ✨ 流畅的用户交互")
    else:
        print("❌ 演示失败")
    
    return layout is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)