#!/usr/bin/env python3
"""
测试优化后的macUI Signal系统

验证版本控制、批处理去重、智能缓存等优化功能
"""

import sys
import logging
sys.path.insert(0, '/Users/david/david/app/macui')

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

from macui import Signal, Computed, Effect

def test_version_control():
    """测试版本控制优化"""
    print("🚀 测试版本控制优化\n")
    
    # 创建信号
    base = Signal(10)
    print(f"📡 创建Signal: base = {base.value} (版本: v{base._version})\n")
    
    # 创建计算值
    doubled = Computed(lambda: base.value * 2)
    quadrupled = Computed(lambda: doubled.value * 2)
    
    print("1️⃣ 初始计算链:")
    result1 = quadrupled.value
    print(f"📊 结果: quadrupled = {result1}\n")
    
    print("2️⃣ 再次获取（应该使用缓存）:")
    result2 = quadrupled.value
    print(f"📊 结果: quadrupled = {result2}\n")
    
    print("3️⃣ 修改基础值 (触发版本控制):")
    base.value = 15
    print()
    
    print("4️⃣ 重新计算:")
    result3 = quadrupled.value
    print(f"📊 结果: quadrupled = {result3}\n")

def test_batch_deduplication():
    """测试批处理去重优化"""
    print("🧹 测试批处理去重优化\n")
    
    # 创建信号
    x = Signal(1)
    y = Signal(2)
    
    # 创建计算值（依赖两个信号）
    sum_xy = Computed(lambda: x.value + y.value)
    
    # 创建Effect（观察计算值）
    effect_count = {'value': 0}
    
    def sum_effect():
        result = sum_xy.value
        effect_count['value'] += 1
        print(f"💡 Effect执行 #{effect_count['value']}: sum = {result}")
    
    effect = Effect(sum_effect)
    
    print("\n🔥 批量修改两个信号（测试去重）:")
    print("注意观察Effect是否只执行一次\n")
    
    # 快速连续修改（应该批处理去重）
    print("- 修改x:")
    x.value = 10
    
    print("- 修改y:")
    y.value = 20
    
    print(f"\n📊 最终Effect执行次数: {effect_count['value']} (期望: 3次 - 初始1次 + 批处理后1次)")

def test_smart_caching():
    """测试智能缓存"""
    print("\n\n💡 测试智能缓存优化\n")
    
    # 创建昂贵计算的Signal
    expensive_count = {'value': 0}
    
    base = Signal(100)
    
    def expensive_computation():
        expensive_count['value'] += 1
        result = base.value ** 2
        print(f"🔥 昂贵计算执行 #{expensive_count['value']}: {base.value}² = {result}")
        return result
    
    expensive = Computed(expensive_computation)
    
    print("1️⃣ 首次计算:")
    result1 = expensive.value
    
    print("\n2️⃣ 再次获取（应使用缓存）:")
    result2 = expensive.value
    
    print("\n3️⃣ 再次获取（应使用缓存）:")
    result3 = expensive.value
    
    print("\n4️⃣ 修改依赖后重新计算:")
    base.value = 200
    result4 = expensive.value
    
    print(f"\n📊 昂贵计算执行次数: {expensive_count['value']} (期望: 2次 - 首次 + 依赖变化后)")

def test_mixed_scenario():
    """测试综合场景"""
    print("\n\n🎯 综合场景测试\n")
    
    # 复杂的依赖图
    a = Signal(1)
    b = Signal(2)
    c = Signal(3)
    
    # 计算链
    sum_ab = Computed(lambda: a.value + b.value)
    sum_bc = Computed(lambda: b.value + c.value)
    final = Computed(lambda: sum_ab.value * sum_bc.value)
    
    # Effects
    updates = []
    
    def track_final():
        result = final.value
        updates.append(f"final = {result}")
        print(f"📈 Final更新: {result}")
    
    def track_sum_ab():
        result = sum_ab.value  
        updates.append(f"sum_ab = {result}")
        print(f"🔢 Sum_AB更新: {result}")
    
    effect1 = Effect(track_final)
    effect2 = Effect(track_sum_ab)
    
    print("\n🔄 批量修改多个信号:")
    print("观察批处理去重效果\n")
    
    # 快速连续修改
    a.value = 10  # 影响sum_ab和final
    b.value = 20  # 影响sum_ab, sum_bc和final  
    c.value = 30  # 影响sum_bc和final
    
    print(f"\n📊 总更新次数: {len(updates)}")
    print("更新历史:", updates)

if __name__ == "__main__":
    test_version_control()
    test_batch_deduplication() 
    test_smart_caching()
    test_mixed_scenario()