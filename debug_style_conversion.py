#!/usr/bin/env python3
"""
调试样式转换 - 专门测试LayoutStyle到Stretchable Style的转换
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def debug_style_conversion():
    print("🔧 调试LayoutStyle到Stretchable Style的转换...")
    
    from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
    
    # 创建LayoutStyle
    parent_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=AlignItems.STRETCH,
        justify_content=JustifyContent.FLEX_START,
        width=200,
        height=100,
        gap=10
    )
    
    print("📝 原始LayoutStyle:")
    print(f"  width: {parent_style.width}")
    print(f"  height: {parent_style.height}")
    print(f"  flex_direction: {parent_style.flex_direction}")
    print(f"  gap: {parent_style.gap}")
    
    # 转换为Stretchable Style
    stretchable_style = parent_style.to_stretchable_style()
    
    print("🔄 转换后的Stretchable Style:")
    print(f"  Style对象: {stretchable_style}")
    
    # 检查各个属性
    import stretchable as st
    from stretchable.style import Size, Length
    
    # 创建测试节点
    test_node = st.Node(style=stretchable_style)
    
    # 创建两个子节点测试gap
    child_style = LayoutStyle(width=150, height=25)
    child_stretchable_style = child_style.to_stretchable_style()
    
    print("📝 子节点LayoutStyle:")
    print(f"  width: {child_style.width}")
    print(f"  height: {child_style.height}")
    
    child1_node = st.Node(style=child_stretchable_style)
    child2_node = st.Node(style=child_stretchable_style)
    test_node.append(child1_node)
    test_node.append(child2_node)
    
    # 计算布局
    success = test_node.compute_layout()
    print(f"✅ 布局计算: {success}")
    
    if success:
        parent_box = test_node.get_box()
        child1_box = child1_node.get_box()
        child2_box = child2_node.get_box()
        
        print(f"📦 父节点结果: ({parent_box.x:.1f}, {parent_box.y:.1f}, {parent_box.width:.1f}, {parent_box.height:.1f})")
        print(f"📦 子节点1结果: ({child1_box.x:.1f}, {child1_box.y:.1f}, {child1_box.width:.1f}, {child1_box.height:.1f})")
        print(f"📦 子节点2结果: ({child2_box.x:.1f}, {child2_box.y:.1f}, {child2_box.width:.1f}, {child2_box.height:.1f})")
        
        # 分析gap问题
        if child1_box.y == child2_box.y:
            print("❌ Gap没有起作用 - 两个子节点Y坐标相同!")
        else:
            y_diff = abs(child2_box.y - child1_box.y)
            expected_diff = 25 + 10  # 第一个子节点高度 + gap
            print(f"✅ Gap正在工作: Y差异={y_diff:.1f}, 期望={expected_diff}")
        
        # 分析尺寸
        if parent_box.width != 200 or parent_box.height != 100:
            print("❌ 父节点尺寸错误!")
            print(f"   期望: 200x100, 实际: {parent_box.width:.1f}x{parent_box.height:.1f}")
        
        if child1_box.width != 150 or child1_box.height != 25:
            print("❌ 子节点1尺寸错误!")
            print(f"   期望: 150x25, 实际: {child1_box.width:.1f}x{child1_box.height:.1f}")
            
        if child2_box.width != 150 or child2_box.height != 25:
            print("❌ 子节点2尺寸错误!")
            print(f"   期望: 150x25, 实际: {child2_box.width:.1f}x{child2_box.height:.1f}")
    
    return success

def debug_length_conversion():
    print("\n🔧 调试Length转换...")
    
    from macui.layout.styles import to_length, to_size
    from stretchable.style import Length, Size
    
    # 测试各种长度值 (暂时跳过百分比)
    test_values = [100, 150.5, 0]
    
    for val in test_values:
        length = to_length(val)
        print(f"值 {val} -> Length: {length}")
    
    # 测试Size创建
    size = to_size(200, 100)
    print(f"Size(200, 100): {size}")
    print(f"Size width: {size.width}")
    print(f"Size height: {size.height}")

def main():
    print("🚀 === 样式转换调试 ===")
    
    debug_length_conversion()
    success = debug_style_conversion()
    
    if success:
        print("✅ 样式转换测试成功")
    else:
        print("❌ 样式转换测试失败")

if __name__ == "__main__":
    main()