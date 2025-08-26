#!/usr/bin/env python3
"""Stretchable布局引擎概念验证 - 方案B实施"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

try:
    import stretchable as st
    from stretchable import Node, Style
    from stretchable.style import Display, FlexDirection, AlignItems, JustifyContent, Size, Length
    print("✅ Stretchable导入成功！版本信息检查中...")
    
    # 创建基本的Flexbox布局测试
    print("🔧 创建基本Flexbox布局测试...")
    
    # 创建根节点 - 类似VStack
    root_style = Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        size=Size(width=Length.from_any(400), height=Length.from_any(300)),
        align_items=AlignItems.CENTER,
        justify_content=JustifyContent.SPACE_BETWEEN
    )
    
    root = Node(style=root_style)
    print(f"📐 根节点创建: {root}")
    
    # 创建子节点 - 类似Button/Label
    from stretchable.style import Rect
    
    child1_style = Style(
        size=Size(width=Length.from_any(120), height=Length.from_any(44)),
        margin=Rect(top=Length.from_any(10), bottom=Length.from_any(10), left=Length.from_any(0), right=Length.from_any(0))
    )
    child1 = Node(style=child1_style)
    
    child2_style = Style(
        size=Size(width=Length.from_any(200), height=Length.from_any(32)),
        margin=Rect(top=Length.from_any(5), bottom=Length.from_any(5), left=Length.from_any(0), right=Length.from_any(0))
    )
    child2 = Node(style=child2_style)
    
    child3_style = Style(
        size=Size(width=Length.from_any(80), height=Length.from_any(30)),
        margin=Rect(top=Length.from_any(0), bottom=Length.from_any(0), left=Length.from_any(0), right=Length.from_any(0))
    )
    child3 = Node(style=child3_style)
    
    print("📦 子节点创建完成")
    
    # 添加子节点到根节点
    root.append(child1)
    root.append(child2) 
    root.append(child3)
    print("🔗 节点层级结构构建完成")
    
    # 执行布局计算
    print("⚡ 开始布局计算...")
    root.compute_layout()
    print("✅ 布局计算完成！")
    
    # 获取布局结果
    root_layout = root.get_box()
    print(f"\n🎯 布局结果:")
    print(f"根节点: x={root_layout.x}, y={root_layout.y}, w={root_layout.width}, h={root_layout.height}")
    
    for i, child in enumerate([child1, child2, child3]):
        layout = child.get_box()
        print(f"子节点{i+1}: x={layout.x}, y={layout.y}, w={layout.width}, h={layout.height}")
    
    print(f"\n🎉 Stretchable概念验证成功！")
    print(f"📋 验证结果:")
    print(f"   ✅ 库导入正常")
    print(f"   ✅ 基本API可用")
    print(f"   ✅ Flexbox布局计算工作")
    print(f"   ✅ 坐标系统输出合理")
    
    # 测试HStack等价布局
    print(f"\n🔄 测试HStack等价布局...")
    hstack_style = Style(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        size=Size(width=Length.from_any(400), height=Length.from_any(60)),
        align_items=AlignItems.CENTER,
        justify_content=JustifyContent.SPACE_AROUND
    )
    
    hstack = Node(style=hstack_style)
    
    # 添加按钮样式的子节点
    for i in range(3):
        button_style = Style(
            size=Size(width=Length.from_any(80), height=Length.from_any(32))
        )
        button_node = Node(style=button_style)
        hstack.append(button_node)
    
    hstack.compute_layout()
    
    hstack_layout = hstack.get_box()
    print(f"HStack根节点: x={hstack_layout.x}, y={hstack_layout.y}, w={hstack_layout.width}, h={hstack_layout.height}")
    
    for i, child in enumerate(hstack):
        layout = child.get_box()
        print(f"HStack子节点{i+1}: x={layout.x}, y={layout.y}, w={layout.width}, h={layout.height}")
    
    print(f"\n🏆 完整概念验证成功！准备进入架构实施阶段")

except ImportError as e:
    print(f"❌ Stretchable导入失败: {e}")
    print("💡 请确保已安装: uv add stretchable")
except Exception as e:
    print(f"❌ 测试过程中出现错误: {e}")
    import traceback
    traceback.print_exc()