#!/usr/bin/env python3
"""简单的新布局系统测试 - 仅使用基础组件验证概念"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import Button, Label
from macui.core.component import Component

# 导入新布局引擎核心部分
from macui.layout.engine import LayoutEngine, set_debug_mode
from macui.layout.node import LayoutNode
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display

class SimpleLayoutDemo(Component):
    """简单布局演示 - 直接使用布局引擎核心API"""
    
    def __init__(self):
        super().__init__()
        set_debug_mode(True)
        self.layout_engine = LayoutEngine()
    
    def mount(self):
        """使用新布局引擎直接控制NSView位置"""
        from AppKit import NSView
        from Foundation import NSMakeRect
        
        print("🧪 简单布局系统测试开始...")
        
        # 创建容器视图
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 400, 300))
        
        # 创建按钮NSView (Button函数直接返回NSButton)
        btn1_view = Button("按钮 1")
        btn2_view = Button("按钮 2") 
        btn3_view = Button("按钮 3")
        
        # 添加到容器
        container.addSubview_(btn1_view)
        container.addSubview_(btn2_view)
        container.addSubview_(btn3_view)
        
        # 创建布局节点结构
        root_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=400,
            height=300,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.SPACE_AROUND,
            padding=20
        )
        
        root_node = LayoutNode(style=root_style, key="root", user_data=container)
        
        # 子节点
        btn1_node = LayoutNode(style=LayoutStyle(width=100, height=32), key="btn1", user_data=btn1_view)
        btn2_node = LayoutNode(style=LayoutStyle(width=100, height=32), key="btn2", user_data=btn2_view)
        btn3_node = LayoutNode(style=LayoutStyle(width=100, height=32), key="btn3", user_data=btn3_view)
        
        root_node.add_child(btn1_node)
        root_node.add_child(btn2_node)
        root_node.add_child(btn3_node)
        
        # 计算布局
        result = self.layout_engine.compute_layout(root_node)
        
        print(f"✅ 布局计算完成: {result.compute_time:.2f}ms")
        
        # 应用布局结果到NSView
        self._apply_layout_to_views(root_node)
        
        print("🎯 简单布局系统测试完成")
        return container
    
    def _apply_layout_to_views(self, node: LayoutNode):
        """将布局结果应用到NSView"""
        from Foundation import NSMakeRect
        
        x, y, w, h = node.get_layout()
        
        # 如果节点有对应的NSView，设置其frame
        if hasattr(node, 'user_data') and node.user_data:
            view = node.user_data
            if hasattr(view, 'setFrame_'):  # 确认是NSView
                frame = NSMakeRect(x, y, w, h)
                view.setFrame_(frame)
                print(f"📐 {node.key}: 设置frame({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        
        # 递归处理子节点
        for child in node.children:
            self._apply_layout_to_views(child)


def main():
    """主函数"""
    print("🧪 简单新布局系统概念验证")
    print("📐 直接使用LayoutEngine核心API")
    print("=" * 50)
    
    # 创建应用
    app = create_app("Simple Layout Test")
    
    # 创建演示组件
    demo = SimpleLayoutDemo()
    
    # 创建窗口
    window = create_window(
        title="简单布局引擎测试",
        size=(400, 300),
        content=demo
    )
    
    window.show()
    
    print("✅ 简单布局系统演示启动!")
    
    # 运行应用 (快速测试，自动退出)
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()