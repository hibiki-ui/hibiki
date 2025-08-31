#!/usr/bin/env python3
"""
调试工具演示 - 验证 hibiki.ui.debug 模块功能
"""

from hibiki.ui import Label, Container, ComponentStyle, px, ManagerFactory
from hibiki.ui.components.layout import VStack
from hibiki.ui.debug import debug_tree, debug_layout, export_debug_info

def main():
    """演示调试工具功能"""
    print("🧪 Hibiki UI 调试工具演示")
    print("=" * 50)
    
    # 创建测试组件
    test_component = VStack(
        children=[
            Label("标题", style=ComponentStyle(padding=px(10))),
            Label("内容", style=ComponentStyle(padding=px(8))),
            Container(
                children=[Label("嵌套内容")],
                style=ComponentStyle(padding=px(5))
            )
        ],
        spacing=8,
        style=ComponentStyle(width=px(300), height=px(200))
    )
    
    print("\n🌳 组件树结构:")
    tree_output = debug_tree(test_component)
    print(tree_output)
    
    print("\n🔍 布局信息:")
    layout_info = debug_layout(test_component)
    for key, value in layout_info.items():
        if key not in ['computed_style', 'layout_properties']:  # 简化显示
            print(f"   {key}: {value}")
    
    print("\n📄 导出测试:")
    try:
        export_path = export_debug_info(test_component, format="html", filename="demo_debug.html")
        print(f"✅ 调试报告已导出: {export_path}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
    
    print("\n✅ 调试工具演示完成！")

if __name__ == "__main__":
    main()