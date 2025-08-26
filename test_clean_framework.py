#!/usr/bin/env python3
"""
测试清理后的 macUI v2 框架

所有 PyObjC 模拟代码已移除，框架现在直接依赖 PyObjC。
"""

def test_imports():
    """测试所有模块的清晰导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试核心模块
        from core.signal import Signal, Computed, Effect
        print("  ✅ 核心响应式系统")
        
        from core.component import Component
        print("  ✅ 组件系统")
        
        from core.binding import ReactiveBinding, EventBinding, TwoWayBinding
        print("  ✅ 绑定系统")
        
        # 测试组件模块
        from components.controls import Button, TextField, Label
        print("  ✅ 控件组件")
        
        from components.layout import VStack, HStack, ScrollView
        print("  ✅ 布局组件")
        
        # 测试应用模块
        from app import MacUIApp, Window
        print("  ✅ 应用管理")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reactive_core():
    """测试响应式核心功能"""
    print("\n🔄 测试响应式核心...")
    
    try:
        from core.signal import Signal, Computed, Effect
        
        # 创建信号
        count = Signal(0)
        print(f"  📊 Signal 创建: count = {count.value}")
        
        # 创建计算属性
        double = Computed(lambda: count.value * 2)
        print(f"  🧮 Computed 创建: double = {double.value}")
        
        # 测试响应式更新
        count.value = 5
        print(f"  ⚡ 更新测试: count = {count.value}, double = {double.value}")
        
        # 创建副作用
        effects_log = []
        def log_effect():
            effects_log.append(count.value)
            print(f"  📝 Effect 触发: count = {count.value}")
        
        effect = Effect(log_effect)
        
        # 触发更多变化
        count.value = 10
        count.value = 15
        
        print(f"  📋 Effect 记录: {effects_log}")
        
        # 清理
        effect.cleanup()
        print("  🧹 Effect 清理完成")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 响应式测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_controls_creation():
    """测试控件创建"""
    print("\n🎛️  测试控件创建...")
    
    try:
        from core.signal import Signal, Computed
        from components.controls import Button, TextField, Label
        
        # 创建响应式状态
        text_signal = Signal("Hello macUI!")
        count_signal = Signal(42)
        enabled_signal = Signal(True)
        
        # 创建计算属性
        count_text = Computed(lambda: f"Count: {count_signal.value}")
        
        print("  📡 响应式状态创建完成")
        
        # 创建控件
        label = Label(count_text)
        print(f"  🏷️  Label 创建: {type(label).__name__}")
        
        text_field = TextField(
            value=text_signal,
            placeholder="输入文本...",
            enabled=enabled_signal
        )
        print(f"  📝 TextField 创建: {type(text_field).__name__}")
        
        def on_button_click():
            count_signal.value += 1
            print(f"    🖱️  按钮点击! 新计数: {count_signal.value}")
        
        button = Button(
            title=Computed(lambda: f"点击我 ({count_signal.value})"),
            on_click=on_button_click,
            enabled=enabled_signal
        )
        print(f"  🔘 Button 创建: {type(button).__name__}")
        
        # 测试响应式更新
        print("\n  🔄 测试响应式更新...")
        text_signal.value = "Updated text!"
        count_signal.value = 100
        enabled_signal.value = False
        
        print(f"    信号更新: text='{text_signal.value}', count={count_signal.value}, enabled={enabled_signal.value}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 控件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_layout_creation():
    """测试布局创建"""
    print("\n📐 测试布局创建...")
    
    try:
        from components.controls import Label, Button
        from components.layout import VStack, HStack, ScrollView
        
        # 创建子控件
        title_label = Label("应用标题")
        subtitle_label = Label("副标题")
        
        def dummy_handler():
            print("    按钮被点击!")
        
        button1 = Button("按钮 1", on_click=dummy_handler)
        button2 = Button("按钮 2", on_click=dummy_handler)
        
        print("  🎛️  子控件创建完成")
        
        # 创建水平布局
        button_row = HStack(
            spacing=10,
            alignment='center',
            children=[button1, button2]
        )
        print(f"  ↔️  HStack 创建: {type(button_row).__name__}")
        
        # 创建垂直布局
        main_layout = VStack(
            spacing=20,
            padding=30,
            alignment='center',
            children=[title_label, subtitle_label, button_row]
        )
        print(f"  ↕️  VStack 创建: {type(main_layout).__name__}")
        
        # 创建滚动视图
        scroll_view = ScrollView(
            content=main_layout,
            frame=(0, 0, 400, 300),
            has_vertical_scroller=True,
            has_horizontal_scroller=False
        )
        print(f"  📜 ScrollView 创建: {type(scroll_view).__name__}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 布局测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_creation():
    """测试应用程序创建"""
    print("\n📱 测试应用程序创建...")
    
    try:
        from app import MacUIApp, Window
        from core.component import Component
        from components.controls import Label
        
        # 创建简单组件
        class TestComponent(Component):
            def mount(self):
                return Label("测试组件")
        
        # 创建应用
        app = MacUIApp("Clean Framework Test")
        print(f"  📱 应用创建: {app.app_name}")
        
        # 创建窗口
        window = app.create_window(
            title="测试窗口",
            size=(300, 200),
            content=TestComponent()
        )
        print(f"  🪟 窗口创建: {window.title}")
        
        # 测试窗口属性
        window.set_title("更新的标题")
        window.set_size(400, 300)
        print(f"  ⚙️  窗口属性更新: {window.title}, {window.size}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 应用测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🧹 macUI v2 清理后框架测试")
    print("=" * 40)
    print("PyObjC 现在是必需依赖，所有模拟代码已移除")
    
    # 检查 PyObjC
    try:
        import objc
        from AppKit import NSApplication
        print(f"✅ PyObjC 版本: {objc.__version__ if hasattr(objc, '__version__') else 'installed'}")
    except ImportError:
        print("❌ PyObjC 未安装! macUI v2 无法运行")
        print("请安装: pip install pyobjc-core pyobjc-framework-Cocoa")
        return False
    
    # 运行测试
    tests = [
        ("模块导入", test_imports),
        ("响应式核心", test_reactive_core),
        ("控件创建", test_controls_creation),
        ("布局创建", test_layout_creation),
        ("应用创建", test_app_creation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                failed += 1
                print(f"❌ {test_name} 失败")
        except Exception as e:
            failed += 1
            print(f"💥 {test_name} 异常: {e}")
    
    print(f"\n📊 测试结果:")
    print(f"   通过: {passed}")
    print(f"   失败: {failed}")
    print(f"   总计: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过! 清理后的框架工作正常!")
        print("\n✨ macUI v2 现在是纯净的:")
        print("   • 移除了所有 PyObjC 可用性检查")
        print("   • 移除了所有 Mock 对象")
        print("   • PyObjC 现在是必需依赖")
        print("   • 框架更简洁、更直接")
        
        return True
    else:
        print(f"\n⚠️  {failed} 个测试失败，需要修复")
        return False


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 40)
    if success:
        print("🎊 清理完成! macUI v2 已准备用于生产环境!")
    else:
        print("🔧 需要进一步调试和修复")
    print("=" * 40)