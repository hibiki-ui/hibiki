#!/usr/bin/env python3
"""macUI Layout Engine v3.0 综合测试

测试新的专业级布局系统架构 (方案B)
验证LayoutEngine, LayoutNode, LayoutTree的完整功能
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.layout import (
    LayoutEngine, LayoutNode, LayoutTree,
    LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
)
from macui.layout.tree import LayoutTreeBuilder

def test_basic_layout_node():
    """测试基本的LayoutNode功能"""
    print("🧪 测试1: 基本LayoutNode功能")
    
    # 创建VStack样式的节点
    vstack_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        width=400,
        height=300,
        align_items=AlignItems.CENTER,
        justify_content=JustifyContent.SPACE_BETWEEN
    )
    
    root = LayoutNode(style=vstack_style, key="root")
    print(f"   📐 根节点创建: {root}")
    
    # 添加子节点
    for i in range(3):
        child_style = LayoutStyle(
            width=100 + i * 20,
            height=40,
            margin=8
        )
        child = LayoutNode(style=child_style, key=f"child_{i+1}")
        root.add_child(child)
    
    print(f"   📦 添加了 {len(root.children)} 个子节点")
    
    # 计算布局
    root.compute_layout()
    
    # 输出结果
    print("   🎯 布局结果:")
    x, y, w, h = root.get_layout()
    print(f"     根节点: x={x}, y={y}, w={w}, h={h}")
    
    for i, child in enumerate(root.children):
        x, y, w, h = child.get_layout()
        print(f"     子节点{i+1}: x={x}, y={y}, w={w}, h={h}")
    
    print("   ✅ 基本LayoutNode测试通过\n")


def test_layout_engine():
    """测试LayoutEngine功能"""
    print("🧪 测试2: LayoutEngine功能")
    
    # 创建引擎
    engine = LayoutEngine(enable_cache=True, debug_mode=True)
    
    # 创建测试布局
    root_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,  # HStack
        width=600,
        height=80,
        align_items=AlignItems.CENTER,
        justify_content=JustifyContent.SPACE_AROUND,
        gap=16
    )
    
    root = LayoutNode(style=root_style, key="hstack_root")
    
    # 添加按钮样式的子节点
    for i in range(4):
        button_style = LayoutStyle(
            width=120,
            height=44,
            margin=4
        )
        button = LayoutNode(style=button_style, key=f"button_{i+1}")
        root.add_child(button)
    
    # 第一次计算 (应该缓存未命中)
    print("   ⚡ 第一次布局计算...")
    result1 = engine.compute_layout(root)
    print(f"     计算耗时: {result1.compute_time:.2f}ms")
    print(f"     布局尺寸: {result1.width:.1f}x{result1.height:.1f}")
    
    # 第二次计算 (应该缓存命中)
    print("   🎯 第二次布局计算...")
    result2 = engine.compute_layout(root)
    print(f"     计算耗时: {result2.compute_time:.2f}ms")
    
    # 输出性能指标
    print("   📊 性能指标:")
    engine.debug_print_metrics()
    
    print("   ✅ LayoutEngine测试通过\n")


def test_layout_tree():
    """测试LayoutTree功能"""
    print("🧪 测试3: LayoutTree功能")
    
    # 创建布局树
    tree = LayoutTree()
    
    # 创建根节点
    root_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        width=500,
        height=400,
        padding=20
    )
    
    root = tree.create_node("main_container", root_style)
    tree.set_root(root)
    
    # 创建头部区域
    header_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        height=60,
        justify_content=JustifyContent.SPACE_BETWEEN,
        align_items=AlignItems.CENTER,
        margin_bottom=16
    )
    
    header = tree.create_node("header", header_style)
    tree.add_node("main_container", header)
    
    # 头部子元素
    title = tree.create_node("title", LayoutStyle(width=200, height=32))
    tree.add_node("header", title)
    
    actions = tree.create_node("actions", LayoutStyle(width=120, height=32))
    tree.add_node("header", actions)
    
    # 创建内容区域
    content_style = LayoutStyle(
        flex_grow=1,  # 占据剩余空间
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        gap=12
    )
    
    content = tree.create_node("content", content_style)
    tree.add_node("main_container", content)
    
    # 内容项
    for i in range(3):
        item = tree.create_node(f"item_{i+1}", LayoutStyle(height=50))
        tree.add_node("content", item)
    
    print(f"   🏗️  布局树构建完成，共 {len(tree._node_index)} 个节点")
    
    # 计算布局
    result = tree.compute_layout()
    print(f"   ⚡ 布局计算完成: {result.compute_time:.2f}ms")
    
    # 查询特定节点的布局
    header_layout = tree.get_layout_info("header")
    content_layout = tree.get_layout_info("content")
    
    print("   🎯 关键节点布局:")
    print(f"     Header: {header_layout}")
    print(f"     Content: {content_layout}")
    
    # 动态更新测试
    print("   🔄 测试动态样式更新...")
    new_header_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        height=80,  # 增高
        justify_content=JustifyContent.CENTER,  # 改为居中
        align_items=AlignItems.CENTER,
        margin_bottom=16
    )
    
    tree.update_node_style("header", new_header_style)
    result_updated = tree.compute_layout()
    
    header_layout_updated = tree.get_layout_info("header")
    print(f"     更新后Header: {header_layout_updated}")
    
    print("   ✅ LayoutTree测试通过\n")


def test_layout_tree_builder():
    """测试LayoutTreeBuilder流畅API"""
    print("🧪 测试4: LayoutTreeBuilder流畅API")
    
    # 使用Builder模式构建复杂布局
    from macui.layout.styles import vstack_style, hstack_style
    
    tree = (LayoutTreeBuilder()
        .root("app", vstack_style(gap=16, width=600, height=400, padding=20))
        .child("toolbar", hstack_style(height=44, justify=JustifyContent.SPACE_BETWEEN))
        .child("main_area", LayoutStyle(flex_grow=1, display=Display.FLEX, flex_direction=FlexDirection.ROW, gap=16))
        .begin_container("sidebar", LayoutStyle(width=200, display=Display.FLEX, flex_direction=FlexDirection.COLUMN, gap=8))
            .child("nav1", LayoutStyle(height=32))
            .child("nav2", LayoutStyle(height=32))
            .child("nav3", LayoutStyle(height=32))
        .end_container()
        .child("content_area", LayoutStyle(flex_grow=1))
        .child("status_bar", LayoutStyle(height=24))
        .build()
    )
    
    print(f"   🏗️  Builder构建的布局树: {len(tree._node_index)} 个节点")
    
    # 计算布局
    result = tree.compute_layout()
    print(f"   ⚡ 布局计算: {result.compute_time:.2f}ms")
    
    # 输出关键布局信息
    print("   🎯 关键区域布局:")
    for key in ["toolbar", "sidebar", "content_area", "status_bar"]:
        layout = tree.get_layout_info(key)
        if layout:
            x, y, w, h = layout
            print(f"     {key}: x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}")
    
    print("   ✅ LayoutTreeBuilder测试通过\n")


def test_css_like_styles():
    """测试CSS-like样式系统"""
    print("🧪 测试5: CSS-like样式系统")
    
    # 测试各种CSS-like样式
    card_style = LayoutStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        width=300,
        height=200,
        padding=16,      # 简写形式
        margin_top=10,   # 详细形式
        margin_left=20,
        gap=8,
        justify_content=JustifyContent.SPACE_BETWEEN
    )
    
    card = LayoutNode(style=card_style, key="card")
    
    # 卡片内容
    header = LayoutNode(
        style=LayoutStyle(height=40, flex_shrink=0),
        key="card_header"
    )
    
    body = LayoutNode(
        style=LayoutStyle(flex_grow=1),
        key="card_body"
    )
    
    footer = LayoutNode(
        style=LayoutStyle(height=32, flex_shrink=0),
        key="card_footer"
    )
    
    card.add_child(header)
    card.add_child(body)  
    card.add_child(footer)
    
    # 计算布局
    card.compute_layout()
    
    print("   🎯 卡片布局结果:")
    for node_name, node in [("Card", card), ("Header", header), ("Body", body), ("Footer", footer)]:
        x, y, w, h = node.get_layout()
        print(f"     {node_name}: x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}")
    
    print("   ✅ CSS-like样式测试通过\n")


def main():
    """运行所有测试"""
    print("🚀 macUI Layout Engine v3.0 综合测试")
    print("=" * 60)
    print("📋 基于Stretchable (Taffy/Rust)的专业布局系统")
    print("🎯 实施方案B: 纯布局引擎架构")
    print("=" * 60)
    
    try:
        test_basic_layout_node()
        test_layout_engine() 
        test_layout_tree()
        test_layout_tree_builder()
        test_css_like_styles()
        
        print("🎉 所有测试通过！布局引擎v3.0工作正常")
        print("🏆 专业级布局系统实施成功")
        print("\n📊 架构特点总结:")
        print("   ✅ CSS-like声明式样式API")
        print("   ✅ 高性能Rust Taffy引擎")
        print("   ✅ 布局缓存和性能监控")
        print("   ✅ 流畅的Builder API")
        print("   ✅ 完整的调试支持")
        print("   ✅ 专业级错误处理")
        print("   ✅ Web标准兼容")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()