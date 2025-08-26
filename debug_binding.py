#!/usr/bin/env python3
"""
调试绑定系统
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect

def test_effect_behavior():
    """测试Effect的具体行为"""
    print("=== Testing Effect Behavior ===")
    
    count = Signal(0)
    print(f"1. Created signal with value: {count.value}")
    
    effect_calls = []
    def track_effect():
        current_value = count.value
        effect_calls.append(current_value)
        print(f"   Effect called with value: {current_value}")
    
    print("2. Creating Effect...")
    effect = Effect(track_effect)
    print(f"   Effect calls so far: {effect_calls}")
    
    print("3. Changing signal value to 1...")
    count.value = 1
    print(f"   Effect calls so far: {effect_calls}")
    
    print("4. Changing signal value to 2...")  
    count.value = 2
    print(f"   Effect calls so far: {effect_calls}")
    
    print("5. Changing signal value to 5...")
    count.value = 5  
    print(f"   Effect calls so far: {effect_calls}")
    
    effect.cleanup()
    print("6. Effect cleaned up")

def test_computed_with_effect():
    """测试Computed和Effect的组合"""
    print("\n=== Testing Computed + Effect ===")
    
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    print(f"1. Initial values: count={count.value}, text='{count_text.value}'")
    
    effect_calls = []
    def track_computed():
        current_text = count_text.value
        effect_calls.append(current_text)
        print(f"   Effect sees: '{current_text}'")
    
    print("2. Creating Effect that watches Computed...")
    effect = Effect(track_computed)
    print(f"   Effect calls so far: {effect_calls}")
    
    print("3. Changing count to 1...")
    count.value = 1
    print(f"   count={count.value}, text='{count_text.value}'")
    print(f"   Effect calls so far: {effect_calls}")
    
    print("4. Changing count to 3...")
    count.value = 3
    print(f"   count={count.value}, text='{count_text.value}'")
    print(f"   Effect calls so far: {effect_calls}")
    
    effect.cleanup()

def test_reactive_binding():
    """测试ReactiveBinding的具体行为"""
    print("\n=== Testing ReactiveBinding ===")
    
    from macui.core.binding import ReactiveBinding
    
    # 创建Mock视图用于测试
    class TestView:
        def __init__(self):
            self.text = ""
            self.hidden = False
            
        def setStringValue_(self, value):
            print(f"   setStringValue called with: '{value}'")
            self.text = value
            
        def setHidden_(self, hidden):
            print(f"   setHidden called with: {hidden}")
            self.hidden = hidden
    
    view = TestView()
    text_signal = Signal("Initial")
    hidden_signal = Signal(False)
    
    print(f"1. Initial state: text='{view.text}', hidden={view.hidden}")
    print(f"   Signal values: text='{text_signal.value}', hidden={hidden_signal.value}")
    
    print("2. Creating bindings...")
    text_cleanup = ReactiveBinding.bind(view, 'text', text_signal)
    hidden_cleanup = ReactiveBinding.bind(view, 'hidden', hidden_signal)
    print(f"   After binding: text='{view.text}', hidden={view.hidden}")
    
    print("3. Changing text signal...")
    text_signal.value = "Updated Text"
    print(f"   Signal: '{text_signal.value}', View: '{view.text}'")
    
    print("4. Changing hidden signal...")
    hidden_signal.value = True
    print(f"   Signal: {hidden_signal.value}, View: {view.hidden}")
    
    print("5. Changing text again...")
    text_signal.value = "Final Text"
    print(f"   Signal: '{text_signal.value}', View: '{view.text}'")
    
    # 清理
    text_cleanup()
    hidden_cleanup()
    print("6. Bindings cleaned up")

if __name__ == "__main__":
    test_effect_behavior()
    test_computed_with_effect()
    test_reactive_binding()