#!/usr/bin/env python3
"""
测试修复后的响应式系统
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect

def test_reactive_fix():
    print("=== 测试修复后的响应式系统 ===")
    
    # 创建信号
    count = Signal(0)
    print(f"1. 创建Signal: {count.value}")
    
    # 创建计算属性
    count_text = Computed(lambda: f"Count: {count.value}")
    print(f"2. 计算属性: {count_text.value}")
    
    # 测试更新次数
    update_count = [0]
    
    def effect_fn():
        # 访问信号值建立依赖关系
        current_value = count.value
        current_text = count_text.value
        update_count[0] += 1
        print(f"   Effect #{update_count[0]}: value={current_value}, text='{current_text}'")
    
    # 创建Effect
    print("3. 创建Effect...")
    effect = Effect(effect_fn)
    
    # 测试信号更新
    print("4. 更新信号值...")
    count.value = 5
    
    print("5. 再次更新...")
    count.value = 10
    
    print("6. 最后更新...")
    count.value = 15
    
    print(f"7. Effect总共被调用了 {update_count[0]} 次")
    
    # 清理
    effect.cleanup()
    print("8. Effect已清理")
    
    # 验证清理后不会再触发
    count.value = 20
    print(f"9. 清理后更新，Effect调用次数仍为: {update_count[0]}")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_reactive_fix()