#!/usr/bin/env python3
"""
验证修复后的macUI v3.0布局系统
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_fixed_layout():
    print("🎉 测试修复后的macUI v3.0布局系统")
    
    from macui.layout.node import LayoutNode
    from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
    
    # 创建VStack布局 (Column)
    parent_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=AlignItems.STRETCH,
        justify_content=JustifyContent.FLEX_START,
        width=300,
        height=200,
        gap=15
    )
    
    parent_node = LayoutNode(style=parent_style, key="vstack")
    
    # 创建三个子节点
    child1 = LayoutNode(
        style=LayoutStyle(width=250, height=40),
        key="child1"
    )
    
    child2 = LayoutNode(
        style=LayoutStyle(width=250, height=40), 
        key="child2"
    )
    
    child3 = LayoutNode(
        style=LayoutStyle(width=250, height=40),
        key="child3"
    )
    
    # 构建布局树
    parent_node.add_child(child1)
    parent_node.add_child(child2)  
    parent_node.add_child(child3)
    
    # 计算布局
    parent_node.compute_layout()
    
    # 获取布局结果
    px, py, pw, ph = parent_node.get_layout()
    print(f"📦 VStack: ({px:.1f}, {py:.1f}, {pw:.1f}, {ph:.1f})")
    
    c1x, c1y, c1w, c1h = child1.get_layout()
    print(f"📦 子1: ({c1x:.1f}, {c1y:.1f}, {c1w:.1f}, {c1h:.1f})")
    
    c2x, c2y, c2w, c2h = child2.get_layout() 
    print(f"📦 子2: ({c2x:.1f}, {c2y:.1f}, {c2w:.1f}, {c2h:.1f})")
    
    c3x, c3y, c3w, c3h = child3.get_layout()
    print(f"📦 子3: ({c3x:.1f}, {c3y:.1f}, {c3w:.1f}, {c3h:.1f})")
    
    # 验证布局正确性
    print("\n🎯 布局验证:")
    
    # 检查子节点间距
    gap1_2 = c2y - (c1y + c1h)
    gap2_3 = c3y - (c2y + c2h)
    
    print(f"   子1-子2间距: {gap1_2:.1f} (期望: 15)")
    print(f"   子2-子3间距: {gap2_3:.1f} (期望: 15)")
    
    # 检查是否有重叠
    if c1y == c2y == c3y:
        print("   ❌ 所有子节点重叠!")
        return False
    elif gap1_2 == 15 and gap2_3 == 15:
        print("   ✅ 子节点间距正确")
        return True
    else:
        print("   ⚠️ 子节点间距不正确")
        return False

def test_hstack_layout():
    print("\n🎉 测试HStack布局")
    
    from macui.layout.node import LayoutNode
    from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
    
    # 创建HStack布局 (Row)
    parent_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        align_items=AlignItems.CENTER,
        justify_content=JustifyContent.FLEX_START,
        width=400,
        height=80,
        gap=20
    )
    
    parent_node = LayoutNode(style=parent_style, key="hstack")
    
    # 创建三个子节点
    for i in range(3):
        child = LayoutNode(
            style=LayoutStyle(width=80, height=60),
            key=f"btn_{i+1}"
        )
        parent_node.add_child(child)
    
    # 计算布局
    parent_node.compute_layout()
    
    # 验证水平布局
    children_layouts = []
    for i, child in enumerate(parent_node.children):
        x, y, w, h = child.get_layout()
        children_layouts.append((x, y, w, h))
        print(f"📦 按钮{i+1}: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
    
    # 检查水平间距
    if len(children_layouts) >= 2:
        gap1 = children_layouts[1][0] - (children_layouts[0][0] + children_layouts[0][2])
        gap2 = children_layouts[2][0] - (children_layouts[1][0] + children_layouts[1][2])
        print(f"   按钮间距: {gap1:.1f}, {gap2:.1f} (期望: 20, 20)")
        
        if gap1 == 20 and gap2 == 20:
            print("   ✅ HStack布局正确")
            return True
        else:
            print("   ⚠️ HStack间距不正确")
            return False
    
    return False

def main():
    print("🚀 === macUI v3.0 布局系统验证 ===")
    
    vstack_ok = test_fixed_layout()
    hstack_ok = test_hstack_layout()
    
    print("\n📊 === 测试总结 ===")
    if vstack_ok and hstack_ok:
        print("🎉 布局系统完全修复! VStack和HStack都工作正常")
        print("✅ 可以开始构建showcase应用了")
    elif vstack_ok:
        print("✅ VStack修复完成，HStack需要进一步检查")
    elif hstack_ok:
        print("✅ HStack修复完成，VStack需要进一步检查")
    else:
        print("❌ 布局系统仍有问题")

if __name__ == "__main__":
    main()