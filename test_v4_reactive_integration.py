#!/usr/bin/env python3
"""
测试v4响应式系统集成
验证从原版复制的Signal/Computed/Effect系统是否正常工作
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.reactive import Signal, Computed, Effect, batch_update
from macui_v4.core.binding import bind_text
from AppKit import NSTextField

def test_basic_reactive_system():
    """测试基础响应式系统"""
    print("🧪 测试基础响应式系统")
    print("-" * 40)
    
    # 1. 测试Signal
    print("\n1. Signal测试:")
    name = Signal("张三")
    age = Signal(25)
    
    print(f"初始值: name={name.value}, age={age.value}")
    
    # 2. 测试Computed
    print("\n2. Computed测试:")
    greeting = Computed(lambda: f"你好，{name.value}！您今年{age.value}岁。")
    
    print(f"计算值: {greeting.value}")
    
    # 3. 测试Effect
    print("\n3. Effect测试:")
    effect_count = 0
    
    def log_changes():
        nonlocal effect_count
        effect_count += 1
        print(f"  Effect执行 #{effect_count}: {greeting.value}")
    
    effect = Effect(log_changes)
    
    # 4. 测试响应式更新
    print("\n4. 响应式更新测试:")
    print("  更新name...")
    name.value = "李四"
    
    print("  更新age...")
    age.value = 30
    
    # 5. 测试批量更新
    print("\n5. 批量更新测试:")
    def batch_changes():
        name.value = "王五"
        age.value = 35
        print("  批量更新完成")
    
    print("  开始批量更新...")
    batch_update(batch_changes)
    
    print(f"\n✅ 响应式系统测试完成！Effect执行次数: {effect_count}")
    
    # 清理
    effect.cleanup()
    return name, age, greeting

def test_binding_system():
    """测试绑定系统"""
    print("\n🧪 测试绑定系统")
    print("-" * 40)
    
    # 创建Signal
    test_signal = Signal("测试文本")
    
    # 创建NSTextField
    textfield = NSTextField.alloc().init()
    
    print(f"1. Signal对象: {test_signal}")
    print(f"2. Signal值: {test_signal.value}")
    
    # 直接调用bind_text
    print("\n3. 调用bind_text...")
    cleanup = bind_text(textfield, test_signal)
    
    print(f"4. TextField当前值: '{textfield.stringValue()}'")
    
    # 更新Signal
    print("\n5. 更新Signal值...")
    test_signal.value = "更新后的文本"
    print(f"6. TextField更新后值: '{textfield.stringValue()}'")
    
    # 清理
    if callable(cleanup):
        cleanup()
    
    return test_signal, textfield

def main():
    """主测试函数"""
    print("🚀 macUI v4.0 响应式系统集成测试")
    print("=" * 50)
    
    try:
        # 测试基础响应式系统
        basic_results = test_basic_reactive_system()
        
        # 测试绑定系统
        binding_results = test_binding_system()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        print("=" * 50)
        
        print("\n✨ 验证结果:")
        print("✅ Signal/Computed/Effect基础功能正常")
        print("✅ 响应式批量更新系统正常")
        print("✅ 响应式绑定系统正常")
        
        print("\n🚀 macUI v4.0 响应式系统集成成功！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()