#!/usr/bin/env python3
"""
简单布局测试 - 快速验证布局组件修复

测试ModernVStack和ModernHStack的基本功能
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core.signal import Signal
from macui.layout.engine import set_debug_mode

# 导入现代化组件
from macui.components.modern_controls import ModernButton, ModernLabel
from macui.components.modern_layout import ModernVStack, ModernHStack


def test_simple_vstack():
    """测试简单的VStack布局"""
    print("\n=== 测试简单VStack ===")
    
    set_debug_mode(True)
    
    # 创建子组件
    label = ModernLabel("测试标签", width=150, height=24)
    button = ModernButton("测试按钮", width=100, height=32)
    
    print(f"✅ 创建了子组件: Label和Button")
    
    # 创建VStack
    vstack = ModernVStack(
        children=[label, button],
        spacing=16,
        width=200,
        height=100,
        padding=20
    )
    
    print(f"✅ 创建了VStack，子组件数: {len(vstack.child_components)}")
    
    # 获取视图
    try:
        view = vstack.get_view()
        print(f"✅ 成功获取VStack视图: {type(view).__name__}")
        
        # 检查frame
        if hasattr(view, 'frame'):
            frame = view.frame()
            print(f"📐 VStack frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
        
        # 检查子视图
        if hasattr(view, 'subviews'):
            subviews = view.subviews()
            count = len(subviews) if subviews else 0
            print(f"🔗 VStack子视图数量: {count}")
            
            if count > 0:
                for i, subview in enumerate(subviews):
                    sub_frame = subview.frame()
                    print(f"   子视图{i+1}: frame=({sub_frame.origin.x:.1f}, {sub_frame.origin.y:.1f}, {sub_frame.size.width:.1f}, {sub_frame.size.height:.1f})")
        
        return True
        
    except Exception as e:
        print(f"❌ VStack测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_hstack():
    """测试简单的HStack布局"""
    print("\n=== 测试简单HStack ===")
    
    # 创建子组件
    label = ModernLabel("标签", width=80, height=24)
    button = ModernButton("按钮", width=60, height=24)
    
    print(f"✅ 创建了子组件: Label和Button")
    
    # 创建HStack
    hstack = ModernHStack(
        children=[label, button],
        spacing=12,
        width=200,
        height=60,
        padding=15
    )
    
    print(f"✅ 创建了HStack，子组件数: {len(hstack.child_components)}")
    
    # 获取视图
    try:
        view = hstack.get_view()
        print(f"✅ 成功获取HStack视图: {type(view).__name__}")
        
        # 检查frame
        if hasattr(view, 'frame'):
            frame = view.frame()
            print(f"📐 HStack frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
        
        # 检查子视图
        if hasattr(view, 'subviews'):
            subviews = view.subviews()
            count = len(subviews) if subviews else 0
            print(f"🔗 HStack子视图数量: {count}")
            
            if count > 0:
                for i, subview in enumerate(subviews):
                    sub_frame = subview.frame()
                    print(f"   子视图{i+1}: frame=({sub_frame.origin.x:.1f}, {sub_frame.origin.y:.1f}, {sub_frame.size.width:.1f}, {sub_frame.size.height:.1f})")
        
        return True
        
    except Exception as e:
        print(f"❌ HStack测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("🧪 简单布局组件测试")
    print("🎯 验证ModernVStack和ModernHStack修复")
    print("=" * 50)
    
    results = []
    
    # 运行测试
    results.append(("VStack测试", test_simple_vstack()))
    results.append(("HStack测试", test_simple_hstack())) 
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("🏁 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有布局组件测试通过！布局修复成功！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")


if __name__ == "__main__":
    main()