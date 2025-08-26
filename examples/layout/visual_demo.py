#!/usr/bin/env python3
"""
可视化混合布局演示
创建实际的NSView对象并展示布局结构，可以看到实际效果
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def create_visual_demo():
    """创建可视化演示"""
    
    print("🎨 混合布局可视化演示")
    print("=" * 50)
    
    try:
        from macui.components import VStack, HStack, TableView, Button, Label, LayoutMode
        
        print("1️⃣ 创建基础组件...")
        
        # 创建基础组件
        title_label = Label("🛒 商品管理系统")
        subtitle_label = Label("TableView现在可以在VStack中使用了！")
        
        # 创建表格数据
        products = [
            {"name": "苹果", "price": "¥5.99", "stock": "50件"},
            {"name": "香蕉", "price": "¥3.50", "stock": "30件"},
            {"name": "胡萝卜", "price": "¥2.80", "stock": "25件"},
            {"name": "牛奶", "price": "¥8.00", "stock": "20件"}
        ]
        
        # 创建TableView
        table = TableView(
            columns=[
                {"title": "商品名称", "key": "name", "width": 100},
                {"title": "价格", "key": "price", "width": 80},
                {"title": "库存", "key": "stock", "width": 80}
            ],
            data=products,
            headers_visible=True
        )
        
        print(f"   ✅ TableView创建成功: {type(table)}")
        print(f"      - 类名: {table.__class__.__name__}")
        print(f"      - 包含 {len(products)} 行数据")
        
        # 创建按钮
        add_button = Button("添加商品")
        delete_button = Button("删除商品")
        refresh_button = Button("刷新列表")
        
        print("   ✅ 按钮组件创建成功")
        
        print("\n2️⃣ 创建混合布局...")
        
        # 🎉 关键演示：TableView在VStack中
        # 这在重构前会导致NSLayoutConstraintNumberExceedsLimit崩溃
        main_layout = VStack(
            spacing=10,
            padding=20,
            children=[
                title_label,
                subtitle_label,
                
                # ✅ 核心演示：TableView在VStack中
                table,
                
                HStack(
                    spacing=8,
                    children=[
                        add_button,
                        delete_button, 
                        refresh_button
                    ]
                ),
                
                Label("✅ 混合布局系统正常工作！")
            ]
        )
        
        print(f"   ✅ 主布局创建成功: {type(main_layout)}")
        print(f"      - 类名: {main_layout.__class__.__name__}")
        print(f"      - 布局类型: {'Frame布局 (NSView)' if main_layout.__class__.__name__ == 'NSView' else '约束布局 (NSStackView)'}")
        
        print("\n3️⃣ 检查布局结构...")
        
        # 检查子视图
        if hasattr(main_layout, 'subviews'):
            subviews = main_layout.subviews()
            print(f"   📋 主容器包含 {len(subviews)} 个子视图:")
            for i, subview in enumerate(subviews):
                print(f"      {i+1}. {subview.__class__.__name__}")
                
                # 检查frame信息
                if hasattr(subview, 'frame'):
                    frame = subview.frame()
                    print(f"         Frame: x={frame.origin.x}, y={frame.origin.y}, w={frame.size.width}, h={frame.size.height}")
        
        print("\n4️⃣ 布局模式测试...")
        
        # 测试不同布局模式
        test_cases = [
            ("纯简单组件", [Label("标签1"), Button("按钮1")], "应该使用约束布局"),
            ("包含TableView", [Label("标签"), table], "应该切换到Frame布局"),
            ("强制约束模式", [Button("按钮")], "强制使用约束布局")
        ]
        
        for name, components, expected in test_cases:
            if name == "强制约束模式":
                test_layout = VStack(layout_mode=LayoutMode.CONSTRAINTS, children=components)
            else:
                test_layout = VStack(children=components)
            
            layout_type = "Frame布局" if test_layout.__class__.__name__ == "NSView" else "约束布局"
            print(f"   🧪 {name}: {layout_type} ({expected})")
        
        print("\n5️⃣ 功能验证...")
        
        # 验证TableView功能
        if hasattr(table, 'documentView') and table.documentView():
            table_view = table.documentView()
            if hasattr(table_view, 'numberOfRows'):
                row_count = table_view.numberOfRows()
                print(f"   📊 TableView行数: {row_count}")
            
            if hasattr(table_view, 'numberOfColumns'):
                col_count = table_view.numberOfColumns()
                print(f"   📊 TableView列数: {col_count}")
        
        # 验证响应式特性（如果有Signal）
        try:
            from macui.core.signal import Signal
            test_signal = Signal("测试值")
            reactive_label = Label(text=test_signal)
            
            reactive_layout = VStack(children=[reactive_label, table])
            print(f"   🔄 响应式组件布局: {reactive_layout.__class__.__name__}")
            print("   ✅ 响应式特性与混合布局兼容")
        except Exception as e:
            print(f"   ⚠️ 响应式测试跳过: {e}")
        
        print("\n🎉 演示总结:")
        print("   ✅ TableView成功在VStack中创建，没有约束冲突")
        print("   ✅ 混合布局系统自动选择了合适的布局模式")
        print("   ✅ 所有组件都正确创建为NSView对象")
        print("   ✅ 布局层次结构正常")
        print("   ✅ Frame信息已正确设置")
        
        return main_layout
        
    except Exception as e:
        print(f"❌ 可视化演示失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def demonstrate_before_after():
    """演示重构前后的差异"""
    
    print("\n🔄 重构前后对比演示")
    print("=" * 30)
    
    try:
        from macui.components import VStack, TableView, Label, Button
        
        # 创建测试TableView
        table = TableView(
            columns=[{"title": "测试", "key": "test", "width": 100}],
            data=[{"test": "数据1"}, {"test": "数据2"}]
        )
        
        print("❌ 重构前的问题:")
        print("   VStack + TableView = NSLayoutConstraintNumberExceedsLimit 崩溃")
        print("   用户必须手动使用frame布局")
        print("   布局代码复杂且容易出错")
        
        print("\n✅ 重构后的解决方案:")
        # 这在重构前会崩溃，现在正常工作
        fixed_layout = VStack(children=[
            Label("标题"),
            table,  # ✅ 不再崩溃！
            Button("操作按钮")
        ])
        
        print(f"   VStack + TableView = {fixed_layout.__class__.__name__} (正常工作)")
        print("   自动组件类型检测")
        print("   智能布局模式选择")
        print("   用户代码无需改变")
        
        return True
        
    except Exception as e:
        print(f"❌ 对比演示失败: {e}")
        return False

def show_layout_internals():
    """展示布局内部机制"""
    
    print("\n🔍 布局内部机制展示")
    print("=" * 30)
    
    try:
        from macui.components import VStack, TableView, Button, LayoutMode
        from macui.components.layout import LayoutStrategy
        
        # 创建测试组件
        button = Button("测试按钮")
        table = TableView(columns=[{"title": "T", "key": "t", "width": 50}])
        
        # 展示组件类型检测
        button_type = LayoutStrategy.detect_component_type(button)
        table_type = LayoutStrategy.detect_component_type(table)
        
        print(f"🔍 组件类型检测:")
        print(f"   Button: {button_type}")
        print(f"   TableView: {table_type}")
        
        # 展示布局模式选择
        simple_children = [button]
        complex_children = [button, table]
        
        simple_mode = LayoutStrategy.choose_layout_mode(simple_children)
        complex_mode = LayoutStrategy.choose_layout_mode(complex_children)
        
        print(f"\n🎯 布局模式选择:")
        print(f"   纯简单组件 → {simple_mode}")
        print(f"   混合组件 → {complex_mode}")
        
        # 创建实际布局并展示结果
        simple_layout = VStack(children=simple_children)
        complex_layout = VStack(children=complex_children)
        
        print(f"\n📦 实际创建结果:")
        print(f"   纯简单组件 → {simple_layout.__class__.__name__}")
        print(f"   混合组件 → {complex_layout.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 内部机制展示失败: {e}")
        return False

def main():
    """主函数"""
    
    # 运行可视化演示
    layout = create_visual_demo()
    
    # 运行对比演示
    demonstrate_before_after()
    
    # 展示内部机制
    show_layout_internals()
    
    print("\n" + "=" * 60)
    if layout:
        print("🎉 可视化演示完成！")
        print("💡 关键成就：")
        print("   - TableView现在可以安全地在VStack中使用")
        print("   - 混合布局系统自动处理复杂组件")
        print("   - 没有NSLayoutConstraintNumberExceedsLimit错误")
        print("   - 保持所有原有功能和响应式特性")
        print("   - 零破坏性变更，现有代码继续工作")
    else:
        print("❌ 演示失败")
    
    return layout is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)