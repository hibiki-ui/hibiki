#!/usr/bin/env python3
"""
调试get_box()失败的具体原因
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def debug_get_box_failure():
    print("🔧 调试get_box()失败原因...")
    
    import stretchable as st
    from stretchable.style import FlexDirection, AlignItems, JustifyContent, Display, Size, Length
    
    # 直接创建Stretchable节点测试
    print("\n1. 测试直接创建的Stretchable节点:")
    style = st.Style(
        display=Display.FLEX,
        size=Size(width=Length.from_any(150), height=Length.from_any(25))
    )
    
    node = st.Node(style=style)
    print(f"   节点: {node}")
    print(f"   is_dirty: {node.is_dirty}")
    
    try:
        box = node.get_box()
        print(f"   get_box() 成功: ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
    except Exception as e:
        print(f"   ❌ get_box() 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试通过macUI创建的节点
    print("\n2. 测试通过macUI创建的子节点:")
    from macui.layout.node import LayoutNode
    from macui.layout.styles import LayoutStyle
    
    child_style = LayoutStyle(width=150, height=25)
    child_node = LayoutNode(style=child_style, key="test_child")
    
    print(f"   macUI节点: {child_node}")
    print(f"   Stretchable节点: {child_node._stretchable_node}")
    print(f"   is_dirty: {child_node._stretchable_node.is_dirty if child_node._stretchable_node else 'N/A'}")
    
    try:
        box = child_node._stretchable_node.get_box()
        print(f"   get_box() 成功: ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
    except Exception as e:
        print(f"   ❌ get_box() 失败: {e}")
        print(f"   异常类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    # 测试计算布局后的状态
    print("\n3. 测试单独节点计算布局:")
    try:
        success = child_node._stretchable_node.compute_layout()
        print(f"   compute_layout() 成功: {success}")
        
        if success:
            box = child_node._stretchable_node.get_box()
            print(f"   计算后get_box(): ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
    except Exception as e:
        print(f"   ❌ 计算布局失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试父子关系
    print("\n4. 测试父子关系的影响:")
    
    # 创建父节点  
    from macui.layout.styles import FlexDirection
    parent_style = LayoutStyle(
        width=200, height=100,
        flex_direction=FlexDirection.COLUMN,
        gap=10
    )
    parent_node = LayoutNode(style=parent_style, key="test_parent")
    
    # 创建新的子节点
    child1_style = LayoutStyle(width=150, height=25)
    child1_node = LayoutNode(style=child1_style, key="test_child1")
    
    print(f"   父节点创建完成: {parent_node}")
    print(f"   子节点创建完成: {child1_node}")
    
    # 在添加到父节点之前测试
    print("\n   添加到父节点前:")
    try:
        box = child1_node._stretchable_node.get_box()
        print(f"     子节点get_box(): ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
    except Exception as e:
        print(f"     ❌ 子节点get_box()失败: {e}")
    
    # 添加到父节点
    parent_node.add_child(child1_node)
    print("   子节点已添加到父节点")
    
    # 添加后测试
    print("\n   添加到父节点后:")
    try:
        box = child1_node._stretchable_node.get_box()
        print(f"     子节点get_box(): ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
    except Exception as e:
        print(f"     ❌ 子节点get_box()失败: {e}")
    
    # 计算父节点布局后测试
    parent_node.compute_layout()
    print("   父节点布局计算完成")
    
    print("\n   父节点布局计算后:")
    try:
        parent_box = parent_node._stretchable_node.get_box()
        print(f"     父节点get_box(): ({parent_box.x:.1f}, {parent_box.y:.1f}, {parent_box.width:.1f}, {parent_box.height:.1f})")
        
        child_box = child1_node._stretchable_node.get_box()
        print(f"     子节点get_box(): ({child_box.x:.1f}, {child_box.y:.1f}, {child_box.width:.1f}, {child_box.height:.1f})")
    except Exception as e:
        print(f"     ❌ 布局计算后get_box()失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_get_box_failure()