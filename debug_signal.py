#!/usr/bin/env python3
"""
调试Signal系统的内部状态
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Effect

def debug_signal_observers():
    print("=== Debugging Signal Observer Registration ===")
    
    count = Signal(0)
    print(f"1. Created signal: {count}")
    print(f"   Initial observers: {len(count._observers)}")
    
    def test_effect():
        print(f"   Effect accessing count.value: {count.value}")
        return f"Effect result with count: {count.value}"
    
    print("2. Creating effect...")
    effect = Effect(test_effect)
    print(f"   Observers after effect creation: {len(count._observers)}")
    print(f"   Observers: {list(count._observers)}")
    
    print("3. Manually checking if effect is registered...")
    print(f"   Effect._rerun method: {effect._rerun}")
    print(f"   Is _rerun in observers? {effect._rerun in count._observers}")
    
    print("4. Changing signal value...")
    print(f"   Before change - observers: {len(count._observers)}")
    count.value = 5
    print(f"   After change - observers: {len(count._observers)}")
    
    print("5. Manually calling _notify_observers...")
    count._notify_observers()
    
    effect.cleanup()

def debug_current_observer_context():
    print("\n=== Debugging Current Observer Context ===")
    
    count = Signal(0)
    
    print("1. Checking initial context...")
    current_observer = Signal._current_observer.get()
    print(f"   Current observer: {current_observer}")
    
    print("2. Manually setting observer context...")
    def mock_observer():
        print("   Mock observer called!")
    
    token = Signal._current_observer.set(mock_observer)
    try:
        print("   Getting count value with mock observer set...")
        value = count.get()
        print(f"   Value: {value}")
        print(f"   Observers after get: {len(count._observers)}")
        print(f"   Mock observer in set? {mock_observer in count._observers}")
    finally:
        Signal._current_observer.reset(token)
    
    print("3. Testing observer notification...")
    count.value = 10
    print("   Manual _notify_observers call:")
    count._notify_observers()

if __name__ == "__main__":
    debug_signal_observers()
    debug_current_observer_context()