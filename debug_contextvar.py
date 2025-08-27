#!/usr/bin/env python3
"""
测试ContextVar是否在不同导入路径下是同一个对象
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# 测试1: 从Effect中导入Signal（使用绝对路径）
from macui_v4.core.reactive import Signal as Signal1

# 测试2: 从binding中模拟相对导入（通过sys.modules）
import macui_v4.core.reactive as reactive_module
Signal2 = reactive_module.Signal

print(f"🔍 导入测试:")
print(f"   Signal1 (绝对导入): {Signal1}")  
print(f"   Signal2 (模块导入): {Signal2}")
print(f"   是否相同对象: {Signal1 is Signal2}")

print(f"   Signal1._current_observer: {Signal1._current_observer}")
print(f"   Signal2._current_observer: {Signal2._current_observer}")
print(f"   ContextVar是否相同对象: {Signal1._current_observer is Signal2._current_observer}")

# 测试ContextVar设置和获取
print(f"\n🧪 ContextVar测试:")

# 创建一个测试Effect对象
class TestEffect:
    def __init__(self, name):
        self.name = name
        
test_effect = TestEffect("test")

# 使用Signal1设置
token1 = Signal1._current_observer.set(test_effect)
print(f"   使用Signal1设置后:")
print(f"     Signal1._current_observer.get(): {Signal1._current_observer.get()}")
print(f"     Signal2._current_observer.get(): {Signal2._current_observer.get()}")

Signal1._current_observer.reset(token1)

# 使用Signal2设置  
token2 = Signal2._current_observer.set(test_effect)
print(f"   使用Signal2设置后:")
print(f"     Signal1._current_observer.get(): {Signal1._current_observer.get()}")
print(f"     Signal2._current_observer.get(): {Signal2._current_observer.get()}")

Signal2._current_observer.reset(token2)

print("✅ ContextVar测试完成")