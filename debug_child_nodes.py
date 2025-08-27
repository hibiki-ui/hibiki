#!/usr/bin/env python3
"""
调试子节点布局问题 - 检查子节点的Stretchable节点状态
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def debug_child_nodes():
    print("🔧 调试子节点布局问题...")
    
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
    print(f"🔹 父节点创建: {parent_node}")
    print(f"   Stretchable节点: {parent_node._stretchable_node}")
    print(f"   父节点是否为None: {parent_node._stretchable_node is None}")
    
    # 创建子节点
    child1_style = LayoutStyle(width=150, height=25)
    child1_node = LayoutNode(style=child1_style, key="child1")
    print(f"🔹 子节点1创建: {child1_node}")
    print(f"   Stretchable节点: {child1_node._stretchable_node}")
    print(f"   子1节点是否为None: {child1_node._stretchable_node is None}")
    
    child2_style = LayoutStyle(width=150, height=25)
    child2_node = LayoutNode(style=child2_style, key="child2")  
    print(f"🔹 子节点2创建: {child2_node}")
    print(f"   Stretchable节点: {child2_node._stretchable_node}")
    print(f"   子2节点是否为None: {child2_node._stretchable_node is None}")
    
    # 添加到父节点
    parent_node.add_child(child1_node)
    parent_node.add_child(child2_node)
    print("✅ 子节点添加完成")
    
    # 检查父节点的Stretchable children
    try:
        if parent_node._stretchable_node is not None:
            parent_st_node = parent_node._stretchable_node
            st_children = parent_st_node.children
            print(f"📦 父节点Stretchable children数量: {len(st_children)}")
            
            for i, st_child in enumerate(st_children):
                print(f"   子节点{i+1} Stretchable: {st_child}")
        else:
            print("❌ 父节点的Stretchable节点为None!")
    except Exception as e:
        print(f"❌ 检查父节点children失败: {e}")
    
    # 计算布局
    print("\n🔧 计算布局...")
    parent_node.compute_layout()
    
    # 再次检查父节点的Stretchable状态
    try:
        if parent_node._stretchable_node is not None:
            parent_box = parent_node._stretchable_node.get_box()
            print(f"📦 父节点Stretchable布局: ({parent_box.x:.1f}, {parent_box.y:.1f}, {parent_box.width:.1f}, {parent_box.height:.1f})")
            
            st_children = parent_node._stretchable_node.children
            for i, st_child in enumerate(st_children):
                child_box = st_child.get_box()
                print(f"📦 子节点{i+1} Stretchable布局: ({child_box.x:.1f}, {child_box.y:.1f}, {child_box.width:.1f}, {child_box.height:.1f})")
    except Exception as e:
        print(f"❌ 获取Stretchable布局失败: {e}")
    
    # 通过macUI接口获取布局 
    print("\n🔧 通过macUI接口获取布局...")
    px, py, pw, ph = parent_node.get_layout()
    print(f"📦 父节点macUI: ({px:.1f}, {py:.1f}, {pw:.1f}, {ph:.1f})")
    
    c1x, c1y, c1w, c1h = child1_node.get_layout()
    print(f"📦 子1 macUI: ({c1x:.1f}, {c1y:.1f}, {c1w:.1f}, {c1h:.1f})")
    
    c2x, c2y, c2w, c2h = child2_node.get_layout()
    print(f"📦 子2 macUI: ({c2x:.1f}, {c2y:.1f}, {c2w:.1f}, {c2h:.1f})")
    
    # 分析问题
    print("\n🎯 问题分析:")
    if c1x == c2x and c1y == c2y:
        print("❌ 子节点重叠 - 问题确认!")
        
        # 检查子节点的Stretchable节点状态
        print("\n🔍 详细检查子节点:")
        for i, child in enumerate([child1_node, child2_node], 1):
            print(f"子节点{i} ({child.key}):")
            print(f"  _stretchable_node: {child._stretchable_node}")
            print(f"  is None: {child._stretchable_node is None}")
            print(f"  bool(): {bool(child._stretchable_node) if child._stretchable_node is not None else 'N/A'}")
            
            # 尝试直接获取box
            if child._stretchable_node is not None:
                try:
                    box = child._stretchable_node.get_box()
                    print(f"  直接get_box(): ({box.x:.1f}, {box.y:.1f}, {box.width:.1f}, {box.height:.1f})")
                except Exception as e:
                    print(f"  直接get_box()失败: {e}")

if __name__ == "__main__":
    debug_child_nodes()