#!/usr/bin/env python3
"""
简单的Stretchable布局测试
用于隔离布局计算问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_simple_stretchable():
    """测试简单的Stretchable布局"""
    print("🧪 简单Stretchable测试\n")
    
    import stretchable as st
    from stretchable.style import Display, FlexDirection, AlignItems, JustifyContent, Length, Size
    
    # 创建根容器
    root_style = st.Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=AlignItems.CENTER,
        size=Size(width=Length.from_any(400), height=Length.from_any(300)),
        gap=Size(width=Length.from_any(10), height=Length.from_any(10))
    )
    root = st.Node(style=root_style)
    
    # 创建子节点1
    child1_style = st.Style(
        size=Size(width=Length.from_any(200), height=Length.from_any(30))
    )
    child1 = st.Node(style=child1_style)
    
    # 创建子节点2
    child2_style = st.Style(
        size=Size(width=Length.from_any(150), height=Length.from_any(25))
    )
    child2 = st.Node(style=child2_style)
    
    # 创建子节点3
    child3_style = st.Style(
        size=Size(width=Length.from_any(100), height=Length.from_any(32))
    )
    child3 = st.Node(style=child3_style)
    
    # 构建层级
    root.append(child1)
    root.append(child2)
    root.append(child3)
    
    print("🔧 节点树构建完成")
    
    # 计算布局
    try:
        result = root.compute_layout((500, 400))
        print(f"✅ 布局计算成功: {result}")
        
        # 获取布局结果
        root_box = root.get_box()
        print(f"📐 根容器: {root_box.x:.1f}, {root_box.y:.1f}, {root_box.width:.1f}x{root_box.height:.1f}")
        
        for i, child in enumerate([child1, child2, child3]):
            box = child.get_box()
            print(f"📐 子节点{i+1}: {box.x:.1f}, {box.y:.1f}, {box.width:.1f}x{box.height:.1f}")
            
    except Exception as e:
        print(f"❌ 布局计算失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_v4_conversion():
    """测试v4样式转换"""
    print("\n🔄 v4样式转换测试\n")
    
    from macui_v4.core.layout import V4StyleConverter
    from macui_v4.core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px
    
    # 创建v4样式
    v4_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=AlignItems.CENTER,
        width=px(400),
        height=px(300),
        gap=px(10)
    )
    
    # 转换为Stretchable样式
    stretchable_style = V4StyleConverter.convert_to_stretchable_style(v4_style)
    print(f"✅ v4样式转换成功")
    print(f"   Display: {stretchable_style.display}")
    print(f"   FlexDirection: {stretchable_style.flex_direction}")
    print(f"   AlignItems: {stretchable_style.align_items}")
    print(f"   Size: {stretchable_style.size}")
    print(f"   Gap: {stretchable_style.gap}")
    
    # 创建节点并测试
    import stretchable as st
    node = st.Node(style=stretchable_style)
    
    # 添加子节点
    child_style = ComponentStyle(width=px(200), height=px(30))
    child_stretchable_style = V4StyleConverter.convert_to_stretchable_style(child_style)
    child_node = st.Node(style=child_stretchable_style)
    node.append(child_node)
    
    # 测试布局计算
    try:
        result = node.compute_layout((500, 400))
        print(f"✅ v4转换的布局计算成功: {result}")
        
        parent_box = node.get_box()
        child_box = child_node.get_box()
        
        print(f"📐 父容器: {parent_box.x:.1f}, {parent_box.y:.1f}, {parent_box.width:.1f}x{parent_box.height:.1f}")
        print(f"📐 子节点: {child_box.x:.1f}, {child_box.y:.1f}, {child_box.width:.1f}x{child_box.height:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ v4转换的布局计算失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 简单布局测试\n")
    
    # 测试原生Stretchable
    success1 = test_simple_stretchable()
    
    # 测试v4转换
    success2 = test_v4_conversion()
    
    if success1 and success2:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 测试失败，需要调试")
        sys.exit(1)