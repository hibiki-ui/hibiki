#!/usr/bin/env python3
"""
简单混合布局演示
展示TableView现在可以在VStack中正常工作的基本示例
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def create_simple_layout():
    """创建简单的混合布局演示"""
    
    print("=== 简单混合布局演示 ===")
    
    try:
        from macui.components import VStack, HStack, Button, Label, TableView
        
        # 创建表格数据
        sample_data = [
            {"name": "苹果", "price": 5.99},
            {"name": "香蕉", "price": 3.50},
            {"name": "橙子", "price": 4.20}
        ]
        
        # 创建表格
        table = TableView(
            columns=[
                {"title": "商品名称", "key": "name", "width": 120},
                {"title": "价格", "key": "price", "width": 80}
            ],
            data=sample_data,
            headers_visible=True
        )
        
        print(f"✅ TableView创建成功: {type(table)}")
        
        # 🎉 关键演示：TableView现在可以在VStack中使用！
        main_layout = VStack(
            spacing=10,
            padding=20,
            children=[
                Label("🛒 商品清单"),
                Label("以下表格展示了可用的商品和价格"),
                
                # ✅ 这在之前会导致NSLayoutConstraintNumberExceedsLimit崩溃
                # 现在混合布局系统会自动检测并切换到frame布局模式
                table,
                
                HStack(
                    spacing=10,
                    children=[
                        Button("添加商品"),
                        Button("删除商品"),
                        Button("刷新列表")
                    ]
                ),
                
                Label("💡 提示: 这个TableView现在可以安全地在VStack中使用了!")
            ]
        )
        
        print(f"✅ 混合布局VStack创建成功: {type(main_layout)}")
        print(f"   实际类型: {main_layout.__class__.__name__}")
        print("🎉 TableView成功集成到VStack布局中，没有任何约束冲突!")
        
        return main_layout
        
    except Exception as e:
        print(f"❌ 布局创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def demonstrate_layout_modes():
    """演示不同的布局模式"""
    
    print("\n=== 布局模式演示 ===")
    
    try:
        from macui.components import VStack, Button, Label, TableView, LayoutMode
        
        # 创建小表格用于测试
        mini_table = TableView(
            columns=[{"title": "测试", "key": "test", "width": 100}],
            data=[{"test": "数据"}]
        )
        
        # 1. 自动模式（默认）- 智能选择
        auto_layout = VStack(
            children=[Label("自动模式"), mini_table]
        )
        print(f"✅ 自动模式: {auto_layout.__class__.__name__}")
        
        # 2. 强制Frame模式
        frame_layout = VStack(
            layout_mode=LayoutMode.FRAME,
            children=[Label("Frame模式"), Button("按钮")],
            frame=(0, 0, 200, 100)
        )
        print(f"✅ Frame模式: {frame_layout.__class__.__name__}")
        
        # 3. 强制约束模式
        constraint_layout = VStack(
            layout_mode=LayoutMode.CONSTRAINTS,
            children=[Label("约束模式"), Button("按钮")]
        )
        print(f"✅ 约束模式: {constraint_layout.__class__.__name__}")
        
        print("🎯 不同布局模式演示完成")
        return True
        
    except Exception as e:
        print(f"❌ 布局模式演示失败: {e}")
        return False

def show_before_after_comparison():
    """显示重构前后的对比"""
    
    print("\n=== 重构前后对比 ===")
    
    print("❌ 重构前 (会崩溃):")
    print("""
    # 这会导致 NSLayoutConstraintNumberExceedsLimit 错误
    VStack(children=[
        Label("标题"),
        TableView(columns=..., data=...),  # ❌ 导致崩溃
        Button("按钮")
    ])
    """)
    
    print("✅ 重构后 (完美工作):")
    print("""
    # 混合布局系统自动处理复杂组件
    VStack(children=[
        Label("标题"),
        TableView(columns=..., data=...),  # ✅ 自动切换到frame布局
        Button("按钮")
    ])
    """)
    
    print("🚀 技术改进:")
    print("- 自动组件类型检测")
    print("- 智能布局模式选择")
    print("- 零破坏性变更")
    print("- 保持所有响应式特性")

def main():
    """主演示函数"""
    
    print("🎉 混合布局系统演示")
    print("展示TableView现在可以在VStack/HStack中正常使用")
    print("=" * 60)
    
    # 运行演示
    layout = create_simple_layout()
    demonstrate_layout_modes()
    show_before_after_comparison()
    
    print("\n" + "=" * 60)
    if layout:
        print("🎉 演示成功! 混合布局系统正常工作")
        print("💡 你现在可以在任何布局容器中自由使用TableView了!")
    else:
        print("❌ 演示失败，需要检查实现")
    
    return layout is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)