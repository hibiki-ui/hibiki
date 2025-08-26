#!/usr/bin/env python3
"""
详细调试Effect和Signal的交互
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 让我们修改Signal类添加调试信息
from macui.core.signal import Signal, Effect

# 给Signal类添加调试方法
original_get = Signal.get
original_set = Signal.set

def debug_get(self):
    current_observer = Signal._current_observer.get()
    print(f"  DEBUG: Signal.get() called")
    print(f"    Current observer: {current_observer}")
    print(f"    Observers before: {len(self._observers)}")
    
    result = original_get(self)
    
    print(f"    Observers after: {len(self._observers)}")
    if current_observer:
        print(f"    Observer added: {current_observer in self._observers}")
    
    return result

def debug_set(self, new_value):
    print(f"  DEBUG: Signal.set({new_value}) called")
    print(f"    Old value: {self._value}")
    print(f"    Observers count: {len(self._observers)}")
    print(f"    Observers: {list(self._observers)}")
    
    original_set(self, new_value)
    
    print(f"    New value: {self._value}")

# 修改方法
Signal.get = debug_get
Signal.set = debug_set

def test_effect_registration():
    print("=== Detailed Effect Registration Test ===")
    
    count = Signal(42)
    print(f"1. Created signal with value: {count._value}")
    
    def effect_function():
        print(f"    Effect function running...")
        value = count.value  # 这应该调用 get() 方法
        print(f"    Effect got value: {value}")
        return value
    
    print("2. Creating Effect...")
    effect = Effect(effect_function)
    
    print("3. Changing signal value...")
    count.value = 99
    
    print("4. Changing again...")
    count.value = 100
    
    effect.cleanup()

if __name__ == "__main__":
    test_effect_registration()