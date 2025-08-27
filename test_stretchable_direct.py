#!/usr/bin/env python3
"""
直接测试Stretchable布局引擎 - 绕过所有封装层
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_stretchable_directly():
    print("🔧 直接测试Stretchable布局引擎...")
    
    try:
        import stretchable as st
        from stretchable.style import FlexDirection, AlignItems, JustifyContent, Display, Size, Length
        
        print("✅ Stretchable导入成功")
        
        # 创建父容器 - VStack样式
        parent_style = st.Style(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,  # 垂直布局
            align_items=AlignItems.STRETCH,
            justify_content=JustifyContent.FLEX_START,
            size=Size(width=Length.from_any(200), height=Length.from_any(100)),
            gap=Size(width=Length.from_any(10), height=Length.from_any(10))
        )
        
        parent = st.Node(style=parent_style)
        print(f"🔹 父节点创建: 200x100, Column, gap=10")
        
        # 创建子节点
        child1_style = st.Style(
            size=Size(width=Length.from_any(150), height=Length.from_any(25))
        )
        child1 = st.Node(style=child1_style)
        parent.append(child1)
        print(f"🔹 子节点1: 150x25")
        
        child2_style = st.Style(
            size=Size(width=Length.from_any(150), height=Length.from_any(25))
        )
        child2 = st.Node(style=child2_style)
        parent.append(child2)
        print(f"🔹 子节点2: 150x25")
        
        # 计算布局
        success = parent.compute_layout()
        print(f"✅ 布局计算成功: {success}")
        
        # 检查结果
        parent_box = parent.get_box()
        print(f"📦 父节点结果: x={parent_box.x:.1f}, y={parent_box.y:.1f}, w={parent_box.width:.1f}, h={parent_box.height:.1f}")
        
        child1_box = child1.get_box()
        print(f"📦 子节点1结果: x={child1_box.x:.1f}, y={child1_box.y:.1f}, w={child1_box.width:.1f}, h={child1_box.height:.1f}")
        
        child2_box = child2.get_box()
        print(f"📦 子节点2结果: x={child2_box.x:.1f}, y={child2_box.y:.1f}, w={child2_box.width:.1f}, h={child2_box.height:.1f}")
        
        # 分析结果
        print("\n🎯 布局分析:")
        if child1_box.x == child2_box.x and child1_box.y == child2_box.y:
            print("❌ 两个子节点位置完全重叠!")
            print(f"   都在: ({child1_box.x:.1f}, {child1_box.y:.1f})")
        elif abs(child1_box.y - child2_box.y) >= 25:  # 应该有间距
            print("✅ 子节点垂直位置正确分离")
            print(f"   子1 Y: {child1_box.y:.1f}, 子2 Y: {child2_box.y:.1f}")
            print(f"   间距: {abs(child2_box.y - child1_box.y - 25):.1f}")
        else:
            print("⚠️ 子节点位置可能有问题")
            print(f"   子1: ({child1_box.x:.1f}, {child1_box.y:.1f})")
            print(f"   子2: ({child2_box.x:.1f}, {child2_box.y:.1f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Stretchable测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_macui_layout_node():
    print("\n🔧 测试macUI LayoutNode封装...")
    
    try:
        from macui.layout.node import LayoutNode
        from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
        
        # 创建父节点
        parent_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.STRETCH,
            justify_content=JustifyContent.FLEX_START,
            width=200,
            height=100,
            gap=10
        )
        
        parent_node = LayoutNode(style=parent_style, key="parent")
        print(f"🔹 macUI父节点创建")
        
        # 创建子节点
        child1_style = LayoutStyle(width=150, height=25)
        child1_node = LayoutNode(style=child1_style, key="child1")
        parent_node.add_child(child1_node)
        
        child2_style = LayoutStyle(width=150, height=25)  
        child2_node = LayoutNode(style=child2_style, key="child2")
        parent_node.add_child(child2_node)
        
        print(f"🔹 子节点添加完成")
        
        # 计算布局
        parent_node.compute_layout()
        print("✅ macUI布局计算完成")
        
        # 获取结果
        px, py, pw, ph = parent_node.get_layout()
        print(f"📦 父节点: ({px:.1f}, {py:.1f}, {pw:.1f}, {ph:.1f})")
        
        c1x, c1y, c1w, c1h = child1_node.get_layout()
        print(f"📦 子1: ({c1x:.1f}, {c1y:.1f}, {c1w:.1f}, {c1h:.1f})")
        
        c2x, c2y, c2w, c2h = child2_node.get_layout()
        print(f"📦 子2: ({c2x:.1f}, {c2y:.1f}, {c2w:.1f}, {c2h:.1f})")
        
        # 分析
        print("\n🎯 macUI布局分析:")
        if c1x == c2x and c1y == c2y:
            print("❌ macUI封装也导致重叠!")
        elif abs(c1y - c2y) >= 25:
            print("✅ macUI封装布局正确")
        else:
            print("⚠️ macUI封装布局可能有问题")
        
        return True
        
    except Exception as e:
        print(f"❌ macUI LayoutNode测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 === 直接布局引擎测试 ===")
    print("🎯 目标: 确定是Stretchable本身还是我们的封装有问题")
    
    # 测试1: 直接使用Stretchable
    stretchable_ok = test_stretchable_directly()
    
    # 测试2: 使用macUI的LayoutNode封装
    macui_ok = test_macui_layout_node()
    
    print("\n📊 === 测试结果 ===")
    if stretchable_ok and macui_ok:
        print("✅ 布局引擎本身工作正常")
        print("🔍 问题可能在NSView层的应用逻辑")
    elif stretchable_ok and not macui_ok:
        print("❌ macUI的LayoutNode封装有问题")
        print("🔍 需要检查styles.py中的转换逻辑")
    elif not stretchable_ok:
        print("❌ Stretchable引擎本身有问题")
        print("🔍 需要检查API使用方式")
    
    print("🏁 直接测试完成")

if __name__ == "__main__":
    main()