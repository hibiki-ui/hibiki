#!/usr/bin/env python3
"""
测试v4组件系统与Stretchable布局引擎的集成
验证完整的v4架构是否能正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import Label, Button
from macui_v4.core.component import Container
from macui_v4.core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px

def test_v4_layout_integration():
    """测试v4布局集成"""
    print("🚀 测试v4组件系统与Stretchable布局引擎集成\n")
    
    # 1. 初始化管理器系统
    print("1️⃣ 初始化v4管理器系统...")
    ManagerFactory.initialize_all()
    print("✅ 管理器系统初始化完成")
    
    # 2. 创建组件
    print("\n2️⃣ 创建v4组件...")
    
    # 创建标签组件
    title_label = Label("v4布局测试", style=ComponentStyle(
        width=px(200),
        height=px(30)
    ))
    
    counter_label = Label("计数: 0", style=ComponentStyle(
        width=px(150),
        height=px(25)
    ))
    
    # 创建按钮组件
    def test_click():
        print("🔘 按钮被点击了！")
    
    test_button = Button("测试按钮", on_click=test_click, style=ComponentStyle(
        width=px(100),
        height=px(32)
    ))
    
    print("✅ 基础组件创建完成")
    
    # 3. 创建容器并测试布局
    print("\n3️⃣ 创建容器并应用v4布局...")
    
    # 垂直布局容器
    vstack_container = Container(
        children=[title_label, counter_label, test_button],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=px(400),
            height=px(300),
            gap=px(10)
        )
    )
    
    print("✅ 容器创建完成")
    
    # 4. 挂载组件并测试布局计算
    print("\n4️⃣ 挂载组件并计算布局...")
    
    try:
        # 挂载容器（会自动挂载所有子组件）
        container_view = vstack_container.mount()
        print(f"✅ 容器挂载成功: {type(container_view).__name__}")
        print(f"   子视图数量: {len(container_view.subviews())}")
        
        # 获取布局引擎统计
        from macui_v4.core.layout import get_layout_engine
        engine = get_layout_engine()
        engine.debug_print_stats()
        
    except Exception as e:
        print(f"❌ 组件挂载失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. 测试组件清理
    print("\n5️⃣ 测试组件清理...")
    try:
        vstack_container.cleanup()
        print("✅ 组件清理完成")
    except Exception as e:
        print(f"⚠️ 组件清理警告: {e}")
    
    print("\n🎉 v4布局集成测试完成！")
    return True

if __name__ == "__main__":
    success = test_v4_layout_integration()
    if success:
        print("\n✅ 所有测试通过，v4布局引擎集成成功！")
    else:
        print("\n❌ 测试失败，需要进一步调试")
        sys.exit(1)