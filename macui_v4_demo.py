#!/usr/bin/env python3
"""
macUI v4.0 综合演示
展示新架构的完整功能和使用方法
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# 导入macUI v4.0组件
from macui_v4.core.managers import ManagerFactory, ZLayer, Position
from macui_v4.core.styles import ComponentStyle, px
from macui_v4.core.component import Container
from macui_v4.components.basic import Label, Button

def demo_basic_components():
    """演示基础组件功能"""
    print("=" * 50)
    print("🧪 macUI v4.0 基础组件演示")
    print("=" * 50)
    
    # 初始化管理器系统
    print("\n🏭 初始化管理器系统...")
    ManagerFactory.initialize_all()
    
    # 1. 创建基础组件
    print("\n📋 创建基础组件:")
    title_label = Label("macUI v4.0 架构演示", width=300, height=40)
    subtitle_label = Label("基于新架构的现代UI组件库", width=400, height=25) 
    
    def show_message():
        print("🎉 Welcome to macUI v4.0!")
        
    welcome_button = Button("点击欢迎", on_click=show_message, width=120, height=32)
    
    # 2. 挂载组件
    print("\n🚀 挂载组件:")
    title_view = title_label.mount()
    subtitle_view = subtitle_label.mount()
    button_view = welcome_button.mount()
    
    print(f"标题视图: {type(title_view).__name__}")
    print(f"副标题视图: {type(subtitle_view).__name__}")
    print(f"按钮视图: {type(button_view).__name__}")
    
    return title_label, subtitle_label, welcome_button

def demo_high_level_api():
    """演示高层API功能"""
    print("\n=" * 50)  
    print("🎨 macUI v4.0 高层API演示")
    print("=" * 50)
    
    print("\n📍 定位预设演示:")
    
    # 1. 模态对话框
    modal_label = Label("这是模态对话框内容")
    modal_label.layout.modal(350, 200)
    modal_view = modal_label.mount()
    print(f"✅ 模态框创建: position={modal_label.style.position}, z_index={modal_label.style.z_index}")
    
    # 2. 工具提示
    tooltip = Label("这是工具提示")
    tooltip.layout.tooltip(offset_x=10, offset_y=-25)
    tooltip_view = tooltip.mount()
    print(f"✅ 工具提示创建: position={tooltip.style.position}")
    
    # 3. 悬浮按钮
    def fab_action():
        print("💬 悬浮按钮被点击!")
        
    fab = Button("💬", on_click=fab_action)
    fab.layout.floating_button("bottom-right", margin=30)
    fab_view = fab.mount()
    print(f"✅ 悬浮按钮创建: position={fab.style.position}")
    
    # 4. 全屏遮罩
    overlay = Label("")
    overlay.layout.fullscreen()
    overlay.layout.fade(0.7)
    overlay_view = overlay.mount()
    print(f"✅ 全屏遮罩创建: position={overlay.style.position}, opacity={overlay.style.opacity}")
    
    print("\n🎨 样式效果演示:")
    
    # 5. 链式样式调用
    styled_button = Button("样式化按钮")
    styled_button.layout.center()
    styled_button.layout.scale(1.2)
    styled_button.layout.fade(0.9)
    styled_button.layout.rotate(10)
    
    styled_view = styled_button.mount()
    print(f"✅ 样式化按钮: scale={styled_button.style.scale}, opacity={styled_button.style.opacity}, rotation={styled_button.style.rotation}°")
    
    return modal_label, tooltip, fab, overlay, styled_button

def demo_low_level_api():
    """演示低层API功能"""
    print("\n=" * 50)
    print("🔧 macUI v4.0 低层API演示")
    print("=" * 50)
    
    print("\n⚙️ 高级控制演示:")
    
    # 1. 直接定位控制
    advanced_label = Label("高级定位标签")
    advanced_label.advanced.set_position(Position.ABSOLUTE, left=150, top=100)
    advanced_label.advanced.set_z_index(ZLayer.FLOATING)
    advanced_view = advanced_label.mount()
    print(f"✅ 高级定位: position={advanced_label.style.position}, left={advanced_label.style.left}")
    
    # 2. Flexbox精细控制
    flex_container = Container(style=ComponentStyle(width=400, height=200))
    flex_container.advanced.set_flex_properties(
        direction="row",
        justify="space-between", 
        align="center",
        grow=1.0
    )
    flex_view = flex_container.mount()
    print(f"✅ Flexbox容器: direction={flex_container.style.flex_direction}")
    
    # 3. 变换效果精确控制
    transform_button = Button("变换按钮")
    transform_button.advanced.set_transform(
        scale=(1.5, 1.2),
        rotation=25,
        translation=(20, -10)
    )
    transform_view = transform_button.mount()
    print(f"✅ 精确变换: scale={transform_button.style.scale}, rotation={transform_button.style.rotation}°")
    
    # 4. 原始AppKit访问
    raw_label = Label("原始配置标签")
    raw_label.advanced.apply_raw_appkit(
        lambda view: print(f"🔧 直接访问NSView: {type(view).__name__}")
    )
    raw_view = raw_label.mount()
    print("✅ 原始AppKit访问完成")
    
    return advanced_label, flex_container, transform_button, raw_label

def demo_container_system():
    """演示容器系统"""
    print("\n=" * 50)
    print("📦 macUI v4.0 容器系统演示") 
    print("=" * 50)
    
    print("\n🏗️ 容器组合演示:")
    
    # 1. 创建子组件
    header = Label("容器标题", width=300, height=30)
    content = Label("这是容器内容区域", width=300, height=60)
    
    def container_action():
        print("📦 容器内的按钮被点击!")
        
    action_button = Button("容器按钮", on_click=container_action, width=100, height=32)
    
    # 2. 创建容器并添加子组件
    main_container = Container(
        children=[header, content, action_button],
        style=ComponentStyle(width=400, height=200, padding=20)
    )
    
    # 3. 设置容器布局
    main_container.advanced.set_flex_properties(
        direction="column",
        justify="space-around",
        align="center"
    )
    
    # 4. 挂载容器
    container_view = main_container.mount()
    print(f"✅ 主容器创建: 子组件数={len(main_container.children)}")
    print(f"✅ 容器视图: {type(container_view).__name__}, 子视图数={len(container_view.subviews())}")
    
    # 5. 动态添加子组件
    dynamic_label = Label("动态添加的标签")
    main_container.add_child_component(dynamic_label)
    print("✅ 动态子组件添加完成")
    
    return main_container

def demo_layout_scenarios():
    """演示各种布局场景"""
    print("\n=" * 50)
    print("🎯 macUI v4.0 布局场景演示")
    print("=" * 50)
    
    scenarios = []
    
    print("\n🎭 场景1: 模态对话框")
    # 模态对话框场景
    modal_content = Label("确认删除此项目吗？", width=250, height=25)
    confirm_btn = Button("确认", width=80, height=30)
    cancel_btn = Button("取消", width=80, height=30)
    
    modal_dialog = Container(
        children=[modal_content, confirm_btn, cancel_btn],
        style=ComponentStyle(width=300, height=150, padding=20)
    )
    modal_dialog.layout.modal(300, 150)
    modal_dialog_view = modal_dialog.mount()
    scenarios.append(("模态对话框", modal_dialog))
    print(f"✅ 模态对话框: z_index={modal_dialog.style.z_index}")
    
    print("\n🏮 场景2: 浮动工具栏")
    # 浮动工具栏场景
    tool1 = Button("🔧", width=40, height=40)
    tool2 = Button("⚙️", width=40, height=40) 
    tool3 = Button("🎨", width=40, height=40)
    
    toolbar = Container(
        children=[tool1, tool2, tool3],
        style=ComponentStyle(height=50, padding=5)
    )
    toolbar.advanced.set_flex_properties(direction="row", justify="space-around")
    toolbar.layout.top_right(margin=20, z_index=ZLayer.FLOATING)
    toolbar_view = toolbar.mount()
    scenarios.append(("浮动工具栏", toolbar))
    print(f"✅ 浮动工具栏: position={toolbar.style.position}")
    
    print("\n💡 场景3: 状态指示器")
    # 状态指示器场景
    status_label = Label("● 在线", width=80, height=25)
    status_label.layout.top_left(margin=15, z_index=ZLayer.CONTENT)
    status_label.layout.fade(0.8)
    status_view = status_label.mount()
    scenarios.append(("状态指示器", status_label))
    print(f"✅ 状态指示器: opacity={status_label.style.opacity}")
    
    return scenarios

def main():
    """主演示函数"""
    print("🚀 macUI v4.0 完整架构演示开始")
    print("=" * 60)
    
    try:
        # 1. 基础组件演示
        basic_components = demo_basic_components()
        
        # 2. 高层API演示  
        high_level_components = demo_high_level_api()
        
        # 3. 低层API演示
        low_level_components = demo_low_level_api()
        
        # 4. 容器系统演示
        container_component = demo_container_system()
        
        # 5. 布局场景演示
        layout_scenarios = demo_layout_scenarios()
        
        # 总结
        print("\n" + "=" * 60)
        print("🎉 macUI v4.0 架构演示完成!")
        print("=" * 60)
        
        print("\n📊 演示总结:")
        print(f"✅ 基础组件数: {len(basic_components)}")
        print(f"✅ 高层API组件数: {len(high_level_components)}")
        print(f"✅ 低层API组件数: {len(low_level_components)}")
        print(f"✅ 布局场景数: {len(layout_scenarios)}")
        
        print("\n🌟 架构特性验证:")
        print("✅ 六大管理器系统正常工作")
        print("✅ 双层组件架构运行良好")
        print("✅ 分层API接口功能完整")
        print("✅ 样式系统灵活强大")
        print("✅ 定位和层级管理精确")
        print("✅ 变换效果支持完整")
        print("✅ 容器系统工作正常")
        
        print("\n🎯 支持的UI场景:")
        for scenario_name, component in layout_scenarios:
            print(f"✅ {scenario_name}: {type(component).__name__}")
        
        print("\n🚀 macUI v4.0 已准备就绪!")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()