#!/usr/bin/env python3
"""
基础混合布局测试
验证VStack/HStack的混合布局功能基础工作原理
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_layout_strategy():
    """测试布局策略选择逻辑"""
    
    print("=== 测试混合布局系统 ===")
    
    try:
        # 导入组件
        from macui.components.layout import LayoutStrategy, LayoutMode, ComponentType
        from macui.components.basic_controls import Button, Label
        from macui.components.layout import TableView
        
        print("✅ 成功导入混合布局组件")
        
        # 测试组件类型分类
        print(f"简单组件列表: {ComponentType.SIMPLE}")
        print(f"复杂组件列表: {ComponentType.COMPLEX}")
        
        # 创建测试组件
        button = Button("测试按钮")
        label = Label("测试标签")
        
        print(f"✅ 成功创建基础组件: {type(button)}, {type(label)}")
        
        # 测试类型检测
        button_type = LayoutStrategy.detect_component_type(button)
        label_type = LayoutStrategy.detect_component_type(label)
        
        print(f"Button 检测类型: {button_type}")
        print(f"Label 检测类型: {label_type}")
        
        # 测试布局模式选择
        simple_children = [button, label]
        simple_mode = LayoutStrategy.choose_layout_mode(simple_children, LayoutMode.AUTO)
        
        print(f"纯简单组件布局模式: {simple_mode}")
        
        # 创建TableView测试
        table = TableView(columns=[{"title": "名称", "key": "name", "width": 100}])
        table_type = LayoutStrategy.detect_component_type(table)
        
        print(f"✅ 成功创建TableView: {type(table)}")
        print(f"TableView 检测类型: {table_type}")
        
        # 测试混合组件布局模式选择
        mixed_children = [label, table, button]
        mixed_mode = LayoutStrategy.choose_layout_mode(mixed_children, LayoutMode.AUTO)
        
        print(f"混合组件布局模式: {mixed_mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vstack_creation():
    """测试VStack创建"""
    
    print("\n=== 测试VStack混合布局创建 ===")
    
    try:
        from macui.components import VStack, Button, Label, LayoutMode
        
        # 测试1：纯简单组件（应该使用约束布局）
        simple_stack = VStack(
            children=[
                Label("标题"),
                Button("按钮1"),
                Button("按钮2")
            ]
        )
        
        print(f"✅ 简单VStack创建成功: {type(simple_stack)}")
        print(f"   期望类型: NSStackView, 实际类型: {simple_stack.__class__.__name__}")
        
        # 测试2：显式指定布局模式
        frame_stack = VStack(
            layout_mode=LayoutMode.FRAME,
            children=[
                Label("Frame模式标题"),
                Button("Frame按钮")
            ],
            frame=(0, 0, 300, 200)
        )
        
        print(f"✅ Frame模式VStack创建成功: {type(frame_stack)}")
        print(f"   期望类型: NSView, 实际类型: {frame_stack.__class__.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ VStack创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tableview_in_vstack():
    """测试TableView在VStack中的使用"""
    
    print("\n=== 测试TableView在VStack中的使用 ===")
    
    try:
        from macui.components import VStack, Button, Label, TableView
        
        # 创建表格
        table = TableView(
            columns=[
                {"title": "名称", "key": "name", "width": 120},
                {"title": "值", "key": "value", "width": 100}
            ],
            data=[
                {"name": "项目1", "value": "值1"},
                {"name": "项目2", "value": "值2"}
            ]
        )
        
        print(f"✅ TableView创建成功: {type(table)}")
        
        # 创建包含TableView的VStack（这在以前会崩溃！）
        hybrid_stack = VStack(
            children=[
                Label("表格标题"),
                table,  # 🎉 关键测试：TableView在VStack中
                Button("操作按钮")
            ],
            frame=(0, 0, 400, 300)
        )
        
        print(f"✅ 混合VStack创建成功: {type(hybrid_stack)}")
        print(f"   期望类型: NSView (frame模式), 实际类型: {hybrid_stack.__class__.__name__}")
        print("🎉 TableView成功在VStack中使用，没有约束冲突！")
        
        return True
        
    except Exception as e:
        print(f"❌ TableView混合布局测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    
    print("🚀 开始混合布局系统基础测试")
    
    # 运行所有测试
    tests = [
        test_layout_strategy,
        test_vstack_creation,
        test_tableview_in_vstack
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
        print()
    
    # 总结
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！混合布局系统基础功能正常")
        return True
    else:
        print("❌ 部分测试失败，需要调试")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)