#!/usr/bin/env python3
"""
简单的Signal测试，排除重复执行问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.reactive import Signal, Computed, Effect

def test_simple_signal():
    """测试简单Signal"""
    print("🧪 简单Signal测试")
    print("-" * 30)
    
    # 创建Signal
    counter = Signal(0)
    print(f"1. Signal创建: {counter.value}")
    
    # 创建Effect
    effect_count = 0
    def effect_fn():
        nonlocal effect_count  
        effect_count += 1
        print(f"   Effect执行 #{effect_count}: counter = {counter.value}")
    
    print("2. 创建Effect...")
    effect = Effect(effect_fn)
    print(f"3. Effect创建后，观察者数: {len(counter._observers)}")
    
    # 更新Signal
    print("4. 更新Signal...")
    counter.value = 5
    print(f"5. 更新后，Effect执行次数: {effect_count}")
    
    # 再次更新
    print("6. 再次更新Signal...")
    counter.value = 10
    print(f"7. 最终Effect执行次数: {effect_count}")
    
    effect.cleanup()
    return counter, effect

def test_computed_chain():
    """测试Computed链"""
    print("\n🧪 Computed链测试")
    print("-" * 30)
    
    # 创建Signal
    base = Signal(1)
    print(f"1. 基础Signal: {base.value}")
    
    # 创建Computed
    doubled = Computed(lambda: base.value * 2)
    print(f"2. Computed创建: {doubled.value}")
    
    # 创建基于Computed的Effect
    effect_count = 0
    def effect_fn():
        nonlocal effect_count
        effect_count += 1  
        print(f"   Effect执行 #{effect_count}: doubled = {doubled.value}")
    
    print("3. 创建Effect...")
    effect = Effect(effect_fn)
    
    print(f"4. 初始状态 - base观察者: {len(base._observers)}, doubled观察者: {len(doubled._observers)}")
    
    # 更新基础Signal
    print("5. 更新基础Signal...")
    base.value = 3
    print(f"6. 更新后 - Effect执行次数: {effect_count}")
    
    effect.cleanup()
    return base, doubled, effect

if __name__ == "__main__":
    print("🚀 简单响应式测试")
    print("=" * 40)
    
    # 简单Signal测试
    simple_result = test_simple_signal()
    
    # Computed链测试  
    computed_result = test_computed_chain()
    
    print("\n=" * 40)
    print("✅ 简单测试完成")