#!/usr/bin/env python3
"""
调试响应式绑定问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.reactive import Signal, Computed, Effect
from macui_v4.core.binding import ReactiveBinding
from AppKit import NSTextField

def test_direct_binding():
    """测试直接绑定"""
    print("🔧 调试响应式绑定")
    print("-" * 30)
    
    # 创建Signal
    test_signal = Signal("测试文本")
    
    # 创建NSTextField
    textfield = NSTextField.alloc().init()
    
    print(f"1. Signal对象: {test_signal}")
    print(f"2. Signal值: {test_signal.value}")
    print(f"3. Signal观察者数: {len(test_signal._observers)}")
    
    # 直接调用ReactiveBinding.bind
    print("\n4. 调用ReactiveBinding.bind...")
    cleanup = ReactiveBinding.bind(textfield, "stringValue", test_signal)
    
    print(f"5. 返回的cleanup: {cleanup}")
    print(f"6. TextField当前值: '{textfield.stringValue()}'")
    print(f"7. Signal观察者数（绑定后）: {len(test_signal._observers)}")
    
    # 手动访问Signal.value来看是否会建立依赖
    print("\n8. 手动访问Signal.value...")
    manual_value = test_signal.value
    print(f"   手动获取的值: '{manual_value}'")
    print(f"   Signal观察者数（手动访问后）: {len(test_signal._observers)}")
    
    # 更新Signal
    print("\n9. 更新Signal值...")
    test_signal.value = "更新后的文本"
    print(f"10. TextField更新后值: '{textfield.stringValue()}'")
    print(f"11. Signal观察者数（更新后）: {len(test_signal._observers)}")
    
    return cleanup

def test_manual_effect():
    """手动测试Effect和Signal"""
    print("\n🧪 手动测试Effect和Signal")
    print("-" * 30)
    
    # 创建Signal
    counter = Signal(0)
    print(f"1. Counter初始值: {counter.value}")
    print(f"2. Counter初始观察者数: {len(counter._observers)}")
    
    # 创建Effect
    effect_run_count = 0
    def effect_fn():
        nonlocal effect_run_count
        effect_run_count += 1
        current_value = counter.value  # 这里应该建立依赖关系
        print(f"   Effect执行 #{effect_run_count}: counter = {current_value}")
    
    print("\n3. 创建Effect...")
    effect = Effect(effect_fn)
    print(f"4. Effect创建后，Counter观察者数: {len(counter._observers)}")
    
    # 更新Signal
    print("\n5. 更新Counter...")
    counter.value = 1
    print(f"6. 更新后Counter观察者数: {len(counter._observers)}")
    print(f"7. Effect执行总次数: {effect_run_count}")
    
    # 再次更新
    print("\n8. 再次更新Counter...")
    counter.value = 2  
    print(f"9. Effect执行总次数: {effect_run_count}")
    
    # 清理
    effect.cleanup()
    return effect

def main():
    """主函数"""
    print("🚀 响应式绑定调试")
    print("=" * 40)
    
    try:
        # 测试手动Effect
        effect_result = test_manual_effect()
        
        # 测试直接绑定
        binding_result = test_direct_binding()
        
        print("\n" + "=" * 40)
        print("🎉 调试完成！")
        
    except Exception as e:
        print(f"\n❌ 调试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()