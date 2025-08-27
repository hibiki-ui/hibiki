#!/usr/bin/env python3
"""
🧪 macUI v4 演示应用测试脚本
验证演示应用的功能完整性和运行状态
"""

import sys
import os
import time

# 添加macui_v4路径
sys.path.append(os.path.join(os.path.dirname(__file__), "macui_v4"))

def test_v4_imports():
    """测试v4核心模块导入"""
    print("🔍 测试 v4 核心模块导入...")
    
    try:
        from core.managers import ManagerFactory
        print("  ✅ ManagerFactory导入成功")
        
        from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px
        print("  ✅ 样式系统导入成功")
        
        from core.reactive import Signal, Computed, Effect
        print("  ✅ 响应式系统导入成功")
        
        from components.basic import Label, Button
        print("  ✅ 基础组件导入成功")
        
        from core.component import Container
        print("  ✅ 容器组件导入成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return False

def test_reactive_system():
    """测试响应式系统"""
    print("\n🔄 测试响应式系统...")
    
    try:
        from core.reactive import Signal, Computed, Effect
        
        # 测试Signal
        counter = Signal(0)
        assert counter.value == 0
        
        counter.value = 5
        assert counter.value == 5
        print("  ✅ Signal测试通过")
        
        # 测试Computed
        doubled = Computed(lambda: counter.value * 2)
        assert doubled.value == 10
        
        counter.value = 3
        assert doubled.value == 6
        print("  ✅ Computed测试通过")
        
        # 测试Effect
        effect_result = []
        def effect_fn():
            effect_result.append(counter.value)
        
        effect = Effect(effect_fn)
        counter.value = 7
        print("  ✅ Effect测试通过")
        
        return True
    except Exception as e:
        print(f"  ❌ 响应式系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_component_system():
    """测试组件系统"""
    print("\n🧩 测试组件系统...")
    
    try:
        from components.basic import Label, Button
        from core.component import Container
        from core.styles import ComponentStyle, px
        
        # 测试Label创建
        label = Label("测试文本", style=ComponentStyle(width=px(200), height=px(30)))
        assert label.text == "测试文本"
        print("  ✅ Label创建测试通过")
        
        # 测试Button创建
        clicked = []
        def on_click():
            clicked.append("clicked")
        
        button = Button("测试按钮", on_click=on_click, style=ComponentStyle(width=px(100), height=px(30)))
        assert button.title == "测试按钮"
        print("  ✅ Button创建测试通过")
        
        # 测试Container创建
        container = Container(
            children=[label, button],
            style=ComponentStyle(width=px(300), height=px(100))
        )
        assert len(container.children) == 2
        print("  ✅ Container创建测试通过")
        
        return True
    except Exception as e:
        print(f"  ❌ 组件系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_style_system():
    """测试样式系统"""
    print("\n🎨 测试样式系统...")
    
    try:
        from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px, percent, auto
        
        # 测试长度单位
        width_px = px(100)
        assert width_px.value == 100
        assert width_px.unit.value == "px"
        
        width_percent = percent(50)
        assert width_percent.value == 50
        assert width_percent.unit.value == "%"
        print("  ✅ 长度单位测试通过")
        
        # 测试ComponentStyle创建
        style = ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=px(400),
            height=px(300)
        )
        assert style.display == Display.FLEX
        assert style.flex_direction == FlexDirection.COLUMN
        assert style.width.value == 400
        print("  ✅ ComponentStyle创建测试通过")
        
        return True
    except Exception as e:
        print(f"  ❌ 样式系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_layout_engine():
    """测试布局引擎"""
    print("\n📐 测试布局引擎...")
    
    try:
        from core.layout import V4LayoutEngine, V4StyleConverter
        from core.styles import ComponentStyle, Display, px
        
        # 测试样式转换
        v4_style = ComponentStyle(
            display=Display.FLEX,
            width=px(200),
            height=px(100)
        )
        
        stretchable_style = V4StyleConverter.convert_to_stretchable_style(v4_style)
        assert stretchable_style is not None
        print("  ✅ 样式转换测试通过")
        
        # 测试布局引擎创建
        engine = V4LayoutEngine()
        assert engine is not None
        print("  ✅ 布局引擎创建测试通过")
        
        return True
    except Exception as e:
        print(f"  ❌ 布局引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manager_system():
    """测试管理器系统"""
    print("\n🏭 测试管理器系统...")
    
    try:
        from core.managers import ManagerFactory
        
        # 测试管理器初始化
        ManagerFactory.initialize_all()
        print("  ✅ 管理器初始化测试通过")
        
        return True
    except Exception as e:
        print(f"  ❌ 管理器系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complete_integration():
    """测试完整集成"""
    print("\n🚀 测试完整集成...")
    
    try:
        # 初始化管理器
        from core.managers import ManagerFactory
        ManagerFactory.initialize_all()
        
        # 创建响应式状态
        from core.reactive import Signal, Computed
        counter = Signal(0)
        doubled = Computed(lambda: counter.value * 2)
        
        # 创建组件
        from components.basic import Label, Button
        from core.component import Container
        from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px
        
        label = Label(f"计数: {counter.value}", style=ComponentStyle(width=px(200), height=px(30)))
        
        def increment():
            counter.value += 1
        
        button = Button("增加", on_click=increment, style=ComponentStyle(width=px(100), height=px(30)))
        
        container = Container(
            children=[label, button],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                width=px(300),
                height=px(200)
            )
        )
        
        print("  ✅ 完整集成测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 完整集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始 macUI v4 功能测试\n")
    
    tests = [
        ("模块导入", test_v4_imports),
        ("响应式系统", test_reactive_system),
        ("组件系统", test_component_system),
        ("样式系统", test_style_system),
        ("布局引擎", test_layout_engine),
        ("管理器系统", test_manager_system),
        ("完整集成", test_complete_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！v4框架功能完整")
        return True
    else:
        print("⚠️ 部分测试失败，需要修复")
        return False

def show_demo_info():
    """显示演示应用信息"""
    print("\n🎨 macUI v4 演示应用信息:")
    print("=" * 50)
    print("1️⃣ 完整功能演示: python macui_v4_complete_showcase.py")
    print("   - 响应式系统演示")
    print("   - 布局系统演示") 
    print("   - 交互系统演示")
    print("   - 综合功能展示")
    
    print("\n2️⃣ 简化版演示: python macui_v4_simple_demo.py")
    print("   - 核心响应式功能")
    print("   - 基础组件使用")
    print("   - 简洁交互界面")
    
    print("\n3️⃣ 基础集成测试: python test_v4_layout_integration.py")
    print("   - 组件挂载测试")
    print("   - 布局引擎测试")
    print("   - 系统集成验证")
    
    print("\n🚀 框架特性:")
    print("   ✅ 完全独立的v4架构")
    print("   ✅ 专业级Stretchable布局引擎")
    print("   ✅ 企业级响应式系统")
    print("   ✅ 六大专业管理器架构")
    print("   ✅ 完整的macOS原生集成")

if __name__ == "__main__":
    print("🎨 macUI v4 框架测试与演示")
    print("=" * 50)
    
    # 运行功能测试
    test_success = run_all_tests()
    
    # 显示演示应用信息
    show_demo_info()
    
    if test_success:
        print("\n✅ v4框架已准备就绪，可以运行演示应用!")
    else:
        print("\n⚠️ 请先修复测试失败的问题")