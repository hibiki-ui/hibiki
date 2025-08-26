#!/usr/bin/env python3
"""
最简单的Signal/Effect调试
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal

def test_basic_signal():
    print("=== Basic Signal Test ===")
    
    count = Signal(0)
    print(f"1. Signal created: {count.value}")
    
    # 直接修改观察者列表来测试通知
    def mock_observer():
        print("   Mock observer called!")
    
    count._observers.add(mock_observer)
    print(f"2. Added mock observer, count: {len(count._observers)}")
    
    print("3. Setting value...")
    count.value = 5
    print(f"   Value is now: {count.value}")
    
    # 手动通知
    print("4. Manual notify...")
    count._notify_observers()

if __name__ == "__main__":
    test_basic_signal()