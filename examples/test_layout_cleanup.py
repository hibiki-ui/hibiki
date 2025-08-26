#!/usr/bin/env python3
"""
布局清理验证测试 - 验证清理混合布局系统后一切正常

测试：
1. 传统VStack/HStack仍然可用
2. 现代化ModernVStack/ModernHStack正常工作
3. 其他布局组件（TableView等）正常工作
4. 导入系统正常
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

print("🧪 布局系统清理验证测试")
print("=" * 50)

def test_imports():
    """测试导入系统"""
    print("\n=== 测试1: 导入系统 ===")
    
    try:
        # 测试传统布局组件导入
        from macui.components import VStack, HStack, TableView, ScrollView
        print("✅ 传统布局组件导入成功")
        
        # 测试现代化布局组件导入
        from macui.components import ModernVStack, ModernHStack
        print("✅ 现代化布局组件导入成功")
        
        # 测试控件组件导入
        from macui.components import Button, Label, TextField
        print("✅ 控件组件导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_traditional_layout():
    """测试传统布局组件"""
    print("\n=== 测试2: 传统布局组件 ===")
    
    try:
        from macui.components import VStack, HStack, Button, Label
        
        # 创建一些基本组件
        button1 = Button("按钮1")
        button2 = Button("按钮2")
        label = Label("标签")
        
        print("✅ 创建了基本组件")
        
        # 创建传统VStack
        vstack = VStack(children=[button1, label], spacing=10)
        print(f"✅ 传统VStack创建成功: {type(vstack).__name__}")
        
        # 创建传统HStack
        hstack = HStack(children=[button1, button2], spacing=8)
        print(f"✅ 传统HStack创建成功: {type(hstack).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 传统布局测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modern_layout():
    """测试现代化布局组件"""
    print("\n=== 测试3: 现代化布局组件 ===")
    
    try:
        from macui.components.modern_layout import ModernVStack, ModernHStack
        from macui.components.modern_controls import ModernButton, ModernLabel
        
        # 创建现代化组件
        button = ModernButton("现代化按钮", width=120, height=32)
        label = ModernLabel("现代化标签", width=150)
        
        print("✅ 创建了现代化组件")
        
        # 创建现代化VStack
        modern_vstack = ModernVStack(
            children=[button, label],
            spacing=16,
            width=200,
            height=100
        )
        print(f"✅ ModernVStack创建成功")
        
        # 测试获取视图
        view = modern_vstack.get_view()
        print(f"✅ ModernVStack视图获取成功: {type(view).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 现代化布局测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_table_view():
    """测试TableView组件"""
    print("\n=== 测试4: TableView组件 ===")
    
    try:
        from macui.components import TableView
        
        # 创建表格
        columns = [
            {"title": "姓名", "key": "name", "width": 120},
            {"title": "年龄", "key": "age", "width": 80}
        ]
        
        data = [
            {"name": "张三", "age": 25},
            {"name": "李四", "age": 30}
        ]
        
        table = TableView(columns=columns, data=data)
        print(f"✅ TableView创建成功: {type(table).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ TableView测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_removed_features():
    """测试被移除的混合布局功能"""
    print("\n=== 测试5: 确认混合布局功能已移除 ===")
    
    try:
        # 这些导入应该失败
        from macui.components import LayoutMode
        print("❌ LayoutMode仍然存在，清理不完整")
        return False
        
    except ImportError:
        print("✅ LayoutMode已正确移除")
    
    try:
        from macui.components import FrameContainer
        print("❌ FrameContainer仍然存在，清理不完整")
        return False
        
    except ImportError:
        print("✅ FrameContainer已正确移除")
    
    try:
        from macui.components import ResponsiveFrame
        print("❌ ResponsiveFrame仍然存在，清理不完整")
        return False
        
    except ImportError:
        print("✅ ResponsiveFrame已正确移除")
    
    print("✅ 所有混合布局功能已正确移除")
    return True


def main():
    """主测试函数"""
    tests = [
        ("导入系统测试", test_imports),
        ("传统布局组件测试", test_traditional_layout),
        ("现代化布局组件测试", test_modern_layout),
        ("TableView组件测试", test_table_view),
        ("混合布局功能移除确认", test_removed_features)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        result = test_func()
        if result:
            passed += 1
    
    print("\n" + "=" * 50)
    print("🏁 测试结果汇总:")
    print(f"📊 {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 布局系统清理成功！")
        print("✅ 混合布局系统已完全移除")
        print("✅ 传统组件保持兼容")
        print("✅ 现代化组件正常工作")
    else:
        print("⚠️ 部分测试失败，需要进一步检查")


if __name__ == "__main__":
    main()