#!/usr/bin/env python3
"""
布局组件集成测试 - 诊断和修复VStack/HStack集成问题

专门测试现代化布局组件在应用窗口中的集成和显示
识别挂载、布局计算、视图显示等潜在问题
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.core.component import Component
from macui.core.signal import Signal, Computed
from macui.layout.engine import set_debug_mode

# 导入现代化组件
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from macui.components.modern_layout import ModernVStack, ModernHStack

class LayoutIntegrationDemo(Component):
    """布局组件集成演示"""
    
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        set_debug_mode(True)
        
        print("🔧 布局组件集成测试开始...")
    
    def increment(self):
        """增加计数器"""
        self.counter.value += 1
        print(f"🔢 计数器更新: {self.counter.value}")
    
    def mount(self):
        """构建和测试现代化布局组件"""
        print("🏗️ 开始构建现代化布局UI...")
        
        try:
            # === 测试1: 简单VStack布局 ===
            print("\n=== 测试1: 简单VStack布局 ===")
            
            # 创建子组件
            title = ModernLabel(
                "📐 布局集成测试", 
                width=300, 
                margin=8
            )
            
            counter_label = ModernLabel(
                Computed(lambda: f"计数: {self.counter.value}"),
                width=150,
                margin=8
            )
            
            increment_btn = ModernButton(
                "+1",
                on_click=self.increment,
                width=80,
                height=32,
                margin=8
            )
            
            # 使用ModernVStack布局
            vstack = ModernVStack(
                children=[title, counter_label, increment_btn],
                spacing=16,
                width=400,
                height=200,
                padding=20
            )
            
            print(f"✅ VStack创建完成，子组件数: {len(vstack.child_components)}")
            
            # === 测试2: 嵌套布局 ===
            print("\n=== 测试2: 嵌套HStack+VStack布局 ===")
            
            # 创建更多测试组件
            text_input = ModernTextField(
                placeholder="输入测试",
                width=150,
                margin=8
            )
            
            reset_btn = ModernButton(
                "重置",
                on_click=lambda: setattr(self.counter, 'value', 0),
                width=80,
                height=32,
                margin=8
            )
            
            # 创建水平布局
            hstack = ModernHStack(
                children=[text_input, reset_btn],
                spacing=12,
                width=350,
                margin=8
            )
            
            # 创建包含嵌套布局的主VStack
            main_vstack = ModernVStack(
                children=[vstack, hstack],
                spacing=20,
                width=450,
                height=300,
                padding=25
            )
            
            print(f"✅ 嵌套布局创建完成")
            print(f"   - 主VStack子组件: {len(main_vstack.child_components)}")
            print(f"   - 内部HStack子组件: {len(hstack.child_components)}")
            
            # === 测试3: 获取最终NSView ===
            print("\n=== 测试3: 获取和验证NSView ===")
            
            final_view = main_vstack.get_view()
            print(f"✅ 获取到最终NSView: {type(final_view).__name__}")
            
            # 验证NSView属性
            if hasattr(final_view, 'frame'):
                frame = final_view.frame()
                print(f"📐 容器frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
            
            if hasattr(final_view, 'subviews'):
                subviews = final_view.subviews()
                print(f"🔗 子视图数量: {len(subviews) if subviews else 0}")
                
                # 检查每个子视图
                if subviews:
                    for i, subview in enumerate(subviews):
                        sub_frame = subview.frame()
                        print(f"   子视图{i+1}: {type(subview).__name__} frame=({sub_frame.origin.x}, {sub_frame.origin.y}, {sub_frame.size.width}, {sub_frame.size.height})")
            
            # === 测试4: 布局计算验证 ===
            print("\n=== 测试4: 布局计算验证 ===")
            
            # 检查布局节点
            if hasattr(main_vstack, 'layout_node') and main_vstack.layout_node:
                print(f"✅ 布局节点存在: {main_vstack.layout_node.key}")
                
                # 检查子节点
                if hasattr(main_vstack.layout_node, 'children'):
                    child_count = len(main_vstack.layout_node.children)
                    print(f"📊 布局子节点数量: {child_count}")
                    
                    for i, child_node in enumerate(main_vstack.layout_node.children):
                        if hasattr(child_node, 'get_layout'):
                            x, y, w, h = child_node.get_layout()
                            print(f"   节点{i+1}: 布局=({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
            else:
                print("⚠️ 布局节点不存在，可能是集成问题")
            
            print("\n✅ 布局组件集成测试完成")
            return final_view
            
        except Exception as e:
            print(f"❌ 布局集成测试失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 返回错误回退视图
            from AppKit import NSView
            from Foundation import NSMakeRect
            error_view = NSView.alloc().init()
            error_view.setFrame_(NSMakeRect(0, 0, 450, 300))
            return error_view


class DirectNSViewDemo(Component):
    """直接NSView演示 - 作为对比测试"""
    
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
    
    def increment(self):
        self.counter.value += 1
        print(f"🔢 直接NSView计数器: {self.counter.value}")
    
    def mount(self):
        """使用直接NSView构建相同的布局作为对比"""
        from AppKit import NSView, NSButton, NSTextField
        from Foundation import NSMakeRect
        
        print("🏗️ 构建直接NSView对比布局...")
        
        # 创建容器
        container = NSView.alloc().init()
        container.setFrame_(NSMakeRect(0, 0, 450, 300))
        
        # 创建标签
        title_label = NSTextField.alloc().init()
        title_label.setStringValue_("📐 直接NSView对比测试")
        title_label.setEditable_(False)
        title_label.setSelectable_(False) 
        title_label.setBezeled_(False)
        title_label.setDrawsBackground_(False)
        title_label.setFrame_(NSMakeRect(25, 250, 300, 20))
        container.addSubview_(title_label)
        
        # 创建计数标签
        counter_label = NSTextField.alloc().init()
        counter_label.setStringValue_(f"计数: {self.counter.value}")
        counter_label.setEditable_(False)
        counter_label.setSelectable_(False)
        counter_label.setBezeled_(False)
        counter_label.setDrawsBackground_(False)
        counter_label.setFrame_(NSMakeRect(25, 220, 150, 20))
        container.addSubview_(counter_label)
        
        # 创建按钮
        button = NSButton.alloc().init()
        button.setTitle_("+1")
        button.setFrame_(NSMakeRect(25, 180, 80, 32))
        
        # 绑定事件
        from macui.core.binding import EventBinding
        EventBinding.bind_click(button, self.increment)
        container.addSubview_(button)
        
        print("✅ 直接NSView布局完成")
        return container


def test_layout_component_mounting():
    """专门测试布局组件的挂载过程"""
    print("\n" + "="*60)
    print("🧪 布局组件挂载过程测试")
    print("="*60)
    
    try:
        # 测试单独的现代化组件创建
        print("\n--- 步骤1: 创建单独的现代化组件 ---")
        button = ModernButton("测试按钮", width=100, height=32)
        button_view = button.get_view()
        print(f"✅ 按钮视图: {type(button_view).__name__}")
        
        label = ModernLabel("测试标签", width=150)
        label_view = label.get_view()
        print(f"✅ 标签视图: {type(label_view).__name__}")
        
        # 测试VStack创建
        print("\n--- 步骤2: 创建VStack布局组件 ---")
        vstack = ModernVStack(
            children=[button, label],
            spacing=10,
            width=200,
            height=100
        )
        print(f"✅ VStack创建: 子组件数 = {len(vstack.child_components)}")
        
        # 测试VStack视图获取
        print("\n--- 步骤3: 获取VStack的NSView ---")
        vstack_view = vstack.get_view()
        print(f"✅ VStack视图: {type(vstack_view).__name__}")
        
        # 检查子视图
        if hasattr(vstack_view, 'subviews'):
            subviews = vstack_view.subviews()
            print(f"📊 VStack子视图数量: {len(subviews) if subviews else 0}")
        
        return True
        
    except Exception as e:
        print(f"❌ 挂载测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数 - 运行布局集成测试"""
    print("🧪 布局组件集成诊断测试")
    print("🎯 识别和修复VStack/HStack集成问题")
    print("=" * 50)
    
    # 先运行挂载测试
    mount_success = test_layout_component_mounting()
    
    if not mount_success:
        print("\n❌ 基础挂载测试失败，跳过UI测试")
        return
    
    print("\n✅ 基础挂载测试通过，开始UI集成测试")
    
    # 创建应用
    app = create_app("Layout Integration Test")
    
    # 创建两个演示组件进行对比
    modern_demo = LayoutIntegrationDemo()
    direct_demo = DirectNSViewDemo()
    
    # 创建现代化布局测试窗口
    modern_window = create_window(
        title="现代化布局组件测试",
        size=(500, 350),
        content=modern_demo
    )
    modern_window.show()
    
    # 创建直接NSView对比窗口
    direct_window = create_window(
        title="直接NSView对比测试", 
        size=(500, 350),
        content=direct_demo
    )
    # 设置第二个窗口的位置，避免重叠
    if hasattr(direct_window, '_window'):
        frame = direct_window._window.frame()
        new_frame = ((frame.origin.x + 520, frame.origin.y), frame.size)
        direct_window._window.setFrame_display_(new_frame, True)
    
    direct_window.show()
    
    print("✅ 布局集成测试启动!")
    print("🔧 请观察两个窗口:")
    print("   1. 左侧: 现代化布局组件 (ModernVStack/HStack)")
    print("   2. 右侧: 直接NSView实现 (对比参考)")
    print("   3. 测试按钮功能和布局显示")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()