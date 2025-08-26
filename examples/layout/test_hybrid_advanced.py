#!/usr/bin/env python3
"""
高级混合布局测试
验证混合布局系统的边界情况和复杂场景
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_complex_nested_layout():
    """测试复杂嵌套布局"""
    
    print("=== 测试复杂嵌套布局 ===")
    
    try:
        from macui.components import VStack, HStack, Button, Label, TableView, LayoutMode
        
        # 创建表格
        table1 = TableView(
            columns=[{"title": "列1", "key": "col1", "width": 100}],
            data=[{"col1": "数据1"}]
        )
        
        table2 = TableView(
            columns=[{"title": "列2", "key": "col2", "width": 100}], 
            data=[{"col2": "数据2"}]
        )
        
        # 测试嵌套布局：VStack包含HStack，HStack包含TableView
        nested_layout = VStack(
            children=[
                Label("顶级标题"),
                HStack(
                    children=[
                        VStack(
                            children=[
                                Label("左侧"),
                                table1,
                                Button("左侧按钮")
                            ]
                        ),
                        VStack(
                            children=[
                                Label("右侧"),
                                table2,
                                Button("右侧按钮")
                            ]
                        )
                    ]
                ),
                Button("底部按钮")
            ],
            frame=(0, 0, 600, 400)
        )
        
        print(f"✅ 复杂嵌套布局创建成功: {type(nested_layout)}")
        print(f"   类型: {nested_layout.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 复杂嵌套布局测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_layout_mode_override():
    """测试布局模式强制指定"""
    
    print("\n=== 测试布局模式强制指定 ===")
    
    try:
        from macui.components import VStack, Button, Label, TableView, LayoutMode
        
        # 创建TableView
        table = TableView(
            columns=[{"title": "测试", "key": "test", "width": 100}],
            data=[{"test": "值"}]
        )
        
        # 测试1: 强制约束模式（即使有TableView）
        try:
            constraint_stack = VStack(
                layout_mode=LayoutMode.CONSTRAINTS,
                children=[Label("标签"), table, Button("按钮")]
            )
            print(f"✅ 强制约束模式: {type(constraint_stack)} - {constraint_stack.__class__.__name__}")
        except Exception as e:
            print(f"⚠️ 强制约束模式失败（预期）: {e}")
        
        # 测试2: 强制Frame模式
        frame_stack = VStack(
            layout_mode=LayoutMode.FRAME,
            children=[Label("标签"), Button("按钮")]  # 纯简单组件
        )
        print(f"✅ 强制Frame模式: {type(frame_stack)} - {frame_stack.__class__.__name__}")
        
        # 测试3: 混合模式
        hybrid_stack = VStack(
            layout_mode=LayoutMode.HYBRID,
            children=[Label("标签"), table, Button("按钮")]
        )
        print(f"✅ 混合模式: {type(hybrid_stack)} - {hybrid_stack.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 布局模式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """测试边界情况"""
    
    print("\n=== 测试边界情况 ===")
    
    try:
        from macui.components import VStack, HStack, FrameContainer, LayoutMode
        
        # 测试1: 空子组件列表
        empty_vstack = VStack(children=[])
        print(f"✅ 空VStack: {type(empty_vstack)} - {empty_vstack.__class__.__name__}")
        
        # 测试2: None子组件
        none_vstack = VStack(children=None)
        print(f"✅ None子组件VStack: {type(none_vstack)} - {none_vstack.__class__.__name__}")
        
        # 测试3: FrameContainer
        frame_container = FrameContainer(
            children=[],
            frame=(0, 0, 200, 200)
        )
        print(f"✅ FrameContainer: {type(frame_container)} - {frame_container.__class__.__name__}")
        
        # 测试4: HStack边界情况
        empty_hstack = HStack(children=[], layout_mode=LayoutMode.FRAME)
        print(f"✅ 空HStack Frame模式: {type(empty_hstack)} - {empty_hstack.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 边界情况测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_responsive_frame():
    """测试响应式Frame功能"""
    
    print("\n=== 测试响应式Frame ===")
    
    try:
        from macui.components import ResponsiveFrame
        
        # 创建响应式Frame
        frame = ResponsiveFrame(x=10, y=10, width=100, height=50)
        print(f"✅ ResponsiveFrame创建: x={frame.x}, y={frame.y}, w={frame.width}, h={frame.height}")
        
        # 测试相对定位
        parent_frame = ResponsiveFrame(x=0, y=0, width=400, height=300)
        child_frame = ResponsiveFrame().relative_to_parent(
            parent_frame, 
            x_ratio=0.1, y_ratio=0.1, 
            width_ratio=0.8, height_ratio=0.8
        )
        
        print(f"✅ 相对定位: x={child_frame.x}, y={child_frame.y}, w={child_frame.width}, h={child_frame.height}")
        
        # 转换为NSRect测试
        rect = frame.to_rect()
        print(f"✅ NSRect转换: {rect}")
        
        return True
        
    except Exception as e:
        print(f"❌ 响应式Frame测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance():
    """测试性能（创建多个组件）"""
    
    print("\n=== 测试性能 ===")
    
    try:
        from macui.components import VStack, Button, Label
        import time
        
        start_time = time.time()
        
        # 创建大量简单组件
        children = []
        for i in range(100):
            children.append(Button(f"按钮{i}"))
            children.append(Label(f"标签{i}"))
        
        # 创建大型VStack
        large_stack = VStack(children=children)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ 创建200个组件的VStack: {duration:.4f}秒")
        print(f"   结果类型: {type(large_stack)} - {large_stack.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    
    print("🚀 开始混合布局系统高级测试")
    
    # 运行所有高级测试
    tests = [
        test_complex_nested_layout,
        test_layout_mode_override,
        test_edge_cases,
        test_responsive_frame,
        test_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        print()
    
    # 总结
    print("=" * 50)
    print(f"高级测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有高级测试通过！混合布局系统功能完备")
        return True
    else:
        print(f"❌ {total - passed} 个测试失败，需要进一步调试")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)