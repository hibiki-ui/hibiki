#!/usr/bin/env python3
"""
简单测试ReactiveBinding功能，不需要完整的macOS应用
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed

# 模拟NSTextField的简单实现
class MockNSTextField:
    def __init__(self):
        self._string_value = ""
        
    def setStringValue_(self, value):
        self._string_value = str(value)
        print(f"MockNSTextField.setStringValue_: '{value}'")
        
    def stringValue(self):
        return self._string_value

def test_binding():
    print("=== 测试ReactiveBinding功能 ===")
    
    # 创建信号和计算属性
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    # 创建模拟的文本框
    mock_label = MockNSTextField()
    
    print(f"1. 初始状态: count={count.value}, text='{count_text.value}'")
    
    # 手动实现绑定逻辑（模拟ReactiveBinding.bind）
    from macui.core.signal import Effect
    
    def update_label():
        new_text = count_text.value
        mock_label.setStringValue_(new_text)
    
    # 创建Effect来自动更新
    print("2. 创建Effect进行绑定...")
    effect = Effect(update_label)
    
    # 测试更新
    print("3. 更新count值...")
    count.value = 5
    print(f"   Label文本: '{mock_label.stringValue()}'")
    
    print("4. 再次更新count值...")
    count.value = 10
    print(f"   Label文本: '{mock_label.stringValue()}'")
    
    # 验证结果
    expected_text = "Count: 10"
    actual_text = mock_label.stringValue()
    
    if actual_text == expected_text:
        print("✅ 测试成功! 响应式绑定正常工作")
    else:
        print(f"❌ 测试失败! 期望: '{expected_text}', 实际: '{actual_text}'")
    
    # 清理
    effect.cleanup()
    print("5. Effect已清理")
    
    # 验证清理后不会更新
    count.value = 15
    print(f"6. 清理后更新，Label文本仍为: '{mock_label.stringValue()}'")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_binding()