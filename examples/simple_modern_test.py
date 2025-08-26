#!/usr/bin/env python3
"""
简单现代化组件测试 - 直接测试LayoutAwareComponent

验证新的组件基类和布局属性功能
不依赖复杂的集成系统
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.core.component import Component
from macui.core.signal import Signal, Computed

# 导入现代化组件
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField

# 导入新布局引擎
from macui.layout.engine import set_debug_mode
from macui.layout.node import LayoutNode
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display


class SimpleModernDemo(Component):
    """简单现代化组件演示"""
    
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        set_debug_mode(True)
    
    def increment(self):
        """增加计数器"""
        self.counter.value += 1
        print(f"🔢 计数器: {self.counter.value}")
    
    def mount(self):
        """使用现代化组件直接构建UI"""
        from AppKit import NSView
        from Foundation import NSMakeRect
        
        print("🧪 简单现代化组件测试开始...")
        
        # 创建容器
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 400, 300))
        
        try:
            # 创建现代化组件实例
            title_label = ModernLabel(
                "🎨 现代化组件测试",
                width=300,
                margin=16
            )
            
            counter_label = ModernLabel(
                Computed(lambda: f"计数: {self.counter.value}"),
                width=200,
                margin=8
            )
            
            button = ModernButton(
                "+1",
                on_click=self.increment,
                width=80,
                height=32,
                margin=8
            )
            
            info_label = ModernLabel(
                "基于LayoutAwareComponent的现代化组件",
                width=350,
                margin=8
            )
            
            # 获取所有组件的NSView
            title_view = title_label.get_view()
            counter_view = counter_label.get_view()
            button_view = button.get_view()
            info_view = info_label.get_view()
            
            # 添加到容器
            container.addSubview_(title_view)
            container.addSubview_(counter_view)
            container.addSubview_(button_view)
            container.addSubview_(info_view)
            
            # 创建布局节点结构来测试布局引擎
            root_style = LayoutStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                width=400,
                height=300,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.SPACE_AROUND,
                padding=20
            )
            
            root_node = LayoutNode(style=root_style, key="root")
            
            # 使用组件的布局节点
            title_node = title_label.create_layout_node()
            counter_node = counter_label.create_layout_node()
            button_node = button.create_layout_node()
            info_node = info_label.create_layout_node()
            
            # 构建布局树
            root_node.add_child(title_node)
            root_node.add_child(counter_node)
            root_node.add_child(button_node)
            root_node.add_child(info_node)
            
            # 计算布局
            from macui.layout.engine import get_layout_engine
            engine = get_layout_engine()
            result = engine.compute_layout(root_node)
            
            print(f"✅ 布局计算完成: {result.compute_time:.2f}ms")
            
            # 应用布局到视图
            self._apply_layout_recursive(root_node, title_view)
            self._apply_layout_recursive(title_node, title_view) 
            self._apply_layout_recursive(counter_node, counter_view)
            self._apply_layout_recursive(button_node, button_view)
            self._apply_layout_recursive(info_node, info_view)
            
            print("🎯 现代化组件测试完成")
            return container
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return container
    
    def _apply_layout_recursive(self, node: LayoutNode, view):
        """应用布局到视图"""
        from Foundation import NSMakeRect
        
        if view is None:
            return
            
        x, y, w, h = node.get_layout()
        frame = NSMakeRect(x, y, w, h)
        view.setFrame_(frame)
        
        print(f"📐 {node.key}: 设置frame({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")


def main():
    """主函数"""
    print("🧪 简单现代化组件测试")
    print("📐 验证LayoutAwareComponent + 布局引擎")
    print("=" * 50)
    
    # 创建应用
    app = create_app("Simple Modern Test")
    
    # 创建演示组件
    demo = SimpleModernDemo()
    
    # 创建窗口
    window = create_window(
        title="简单现代化组件测试",
        size=(400, 300),
        content=demo
    )
    
    window.show()
    
    print("✅ 简单现代化组件测试启动!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()