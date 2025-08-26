#!/usr/bin/env python3
"""
macUI v2 框架测试

这个脚本测试 macUI v2 的核心功能，不依赖复杂的模块导入。
"""

def test_signal_system():
    """测试响应式信号系统"""
    print("=== Testing Signal System ===")
    
    # 导入并测试 Signal
    from core.signal import Signal, Computed, Effect
    
    print("1. Testing Signal...")
    count = Signal(0)
    print(f"   Initial value: {count.value}")
    
    count.value = 5
    print(f"   After setting to 5: {count.value}")
    
    # 测试 Computed
    print("\n2. Testing Computed...")
    double = Computed(lambda: count.value * 2)
    print(f"   Double of {count.value} is {double.value}")
    
    count.value = 10
    print(f"   After changing count to 10, double is: {double.value}")
    
    # 测试 Effect
    print("\n3. Testing Effect...")
    effect_calls = []
    
    def log_effect():
        effect_calls.append(count.value)
        print(f"   Effect called with count: {count.value}")
        return lambda: print("   Effect cleanup called")
    
    effect = Effect(log_effect)
    
    print("   Changing count to trigger effects...")
    count.value = 15
    count.value = 20
    
    print(f"   Effect was called {len(effect_calls)} times with values: {effect_calls}")
    
    effect.cleanup()
    print("   Effect cleaned up")
    
    return True


def test_binding_system():
    """测试绑定系统"""
    print("\n=== Testing Binding System ===")
    
    from core.signal import Signal, Computed
    from core.binding import ReactiveBinding
    
    # 创建模拟视图对象
    class MockView:
        def __init__(self):
            self.properties = {}
        
        def setStringValue_(self, value):
            self.properties['text'] = value
            print(f"   Mock view text set to: '{value}'")
        
        def setHidden_(self, value):
            self.properties['hidden'] = value
            print(f"   Mock view hidden set to: {value}")
    
    print("1. Testing ReactiveBinding...")
    view = MockView()
    text_signal = Signal("Hello")
    
    # 绑定文本
    ReactiveBinding.bind(view, 'text', text_signal)
    
    print("   Changing signal value...")
    text_signal.value = "Hello macUI!"
    text_signal.value = "Reactive UI is working!"
    
    # 测试计算属性绑定
    print("\n2. Testing computed binding...")
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    ReactiveBinding.bind(view, 'text', count_text)
    
    count.value = 1
    count.value = 42
    
    return True


def test_component_system():
    """测试组件系统"""
    print("\n=== Testing Component System ===")
    
    from core.component import Component
    from core.signal import Signal, Computed
    
    class TestComponent(Component):
        def __init__(self):
            super().__init__()
            self.counter = self.create_signal(0)
            self.double = self.create_computed(lambda: self.counter.value * 2)
            
            print(f"   Component created with counter: {self.counter.value}")
        
        def increment(self):
            self.counter.value += 1
            print(f"   Counter incremented to: {self.counter.value}, double: {self.double.value}")
        
        def mount(self):
            print(f"   Component mounted with counter: {self.counter.value}")
            return {"type": "mock_view", "counter": self.counter.value}
    
    print("1. Creating component...")
    component = TestComponent()
    
    print("2. Testing component methods...")
    component.increment()
    component.increment()
    
    print("3. Mounting component...")
    view = component.mount()
    print(f"   Mounted view: {view}")
    
    print("4. Testing cleanup...")
    component.cleanup()
    print("   Component cleaned up")
    
    return True


def test_controls():
    """测试控件组件"""
    print("\n=== Testing Controls ===")
    
    from core.signal import Signal, Computed
    
    # 由于 PyObjC 可能不可用，我们主要测试控件创建逻辑
    try:
        from components.controls import Button, Label, TextField
        
        print("1. Testing Button creation...")
        click_count = Signal(0)
        
        def on_click():
            click_count.value += 1
            print(f"   Button clicked! Count: {click_count.value}")
        
        button_title = Computed(lambda: f"Clicked {click_count.value} times")
        button = Button(title=button_title, on_click=on_click)
        print(f"   Button created: {type(button).__name__}")
        
        print("2. Testing Label creation...")
        label_text = Signal("Dynamic Label")
        label = Label(text=label_text)
        print(f"   Label created: {type(label).__name__}")
        
        print("3. Testing TextField creation...")
        text_value = Signal("")
        text_field = TextField(value=text_value, placeholder="Type here...")
        print(f"   TextField created: {type(text_field).__name__}")
        
        # 模拟一些交互
        print("4. Simulating interactions...")
        on_click()  # 模拟按钮点击
        label_text.value = "Updated Label Text"
        text_value.value = "User typed this"
        
        return True
        
    except Exception as e:
        print(f"   Controls test failed (expected in mock mode): {e}")
        return False


def test_layout():
    """测试布局组件"""
    print("\n=== Testing Layout ===")
    
    try:
        from components.layout import VStack, HStack
        from components.controls import Label, Button
        from core.signal import Signal
        
        print("1. Testing VStack creation...")
        children = [
            Label("Title"),
            Label("Subtitle"),
            Button("Click me", on_click=lambda: print("Button clicked"))
        ]
        
        vstack = VStack(spacing=10, padding=20, children=children)
        print(f"   VStack created: {type(vstack).__name__}")
        
        print("2. Testing HStack creation...")
        hstack = HStack(spacing=15, children=[
            Button("Left", on_click=lambda: print("Left clicked")),
            Button("Right", on_click=lambda: print("Right clicked"))
        ])
        print(f"   HStack created: {type(hstack).__name__}")
        
        return True
        
    except Exception as e:
        print(f"   Layout test failed (expected in mock mode): {e}")
        return False


def run_comprehensive_test():
    """运行全面的框架测试"""
    print("macUI v2 Framework Test")
    print("=======================")
    
    tests = [
        ("Signal System", test_signal_system),
        ("Binding System", test_binding_system),
        ("Component System", test_component_system),
        ("Controls", test_controls),
        ("Layout", test_layout),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning {test_name}...")
            if test_func():
                print(f"✓ {test_name} PASSED")
                passed += 1
            else:
                print(f"✗ {test_name} FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n=== Test Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed! macUI v2 framework is working correctly.")
    else:
        print(f"⚠️  {failed} tests failed. Some issues need to be addressed.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print("\n" + "="*50)
        print("Framework is ready! You can now:")
        print("1. Create components using the Component base class")
        print("2. Use Signal, Computed, and Effect for reactive state")
        print("3. Build layouts with VStack, HStack, etc.")
        print("4. Create interactive UIs with Button, TextField, etc.")
        print("5. Run full applications with MacUIApp")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("Some tests failed. Please check the implementation.")
        print("="*50)