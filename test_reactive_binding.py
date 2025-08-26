#!/usr/bin/env python3
"""
专门测试ReactiveBinding问题
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, get_logger, set_log_level
from macui.core.binding import ReactiveBinding

set_log_level("DEBUG")
logger = get_logger("binding_test")

class MockNSTextField:
    def __init__(self, name="MockField"):
        self.name = name
        self._string_value = ""
        logger.info(f"MockNSTextField创建: {self.name}[{id(self)}]")
        
    def setStringValue_(self, value):
        old_value = self._string_value
        self._string_value = str(value)
        logger.info(f"MockNSTextField[{id(self)}].setStringValue_: '{old_value}' -> '{value}'")
        
    def stringValue(self):
        return self._string_value

def test_reactive_binding_issue():
    """测试ReactiveBinding的具体问题"""
    logger.info("=== 测试ReactiveBinding问题 ===")
    
    # 创建信号和计算属性
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    # 创建mock视图
    text_field = MockNSTextField("TestField")
    
    # 手动模拟ReactiveBinding.bind中的update函数
    def manual_update():
        logger.info("manual_update函数执行开始")
        
        # 检查当前观察者
        from macui.core.signal import Signal
        current_obs = Signal._current_observer.get()
        logger.info(f"manual_update内的当前观察者: {current_obs}")
        
        # 获取值（这里是问题的关键）
        if hasattr(count_text, "value"):
            logger.info("使用hasattr检查 - 是Signal或Computed")
            value = count_text.value
            logger.info(f"从Computed获取到值: {repr(value)}")
        else:
            logger.info("不是Signal或Computed")
            value = count_text
        
        # 设置到视图
        text_field.setStringValue_(value)
        logger.info("manual_update函数执行完成")
    
    logger.info("1. 创建Effect进行绑定...")
    effect = Effect(manual_update)
    
    logger.info("2. 验证初始状态...")
    logger.info(f"count.value = {count.value}")
    logger.info(f"count_text.value = '{count_text.value}'")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    logger.info("3. 修改count值...")
    count.value = 42
    
    logger.info("4. 验证更新后状态...")
    logger.info(f"count.value = {count.value}")
    logger.info(f"count_text.value = '{count_text.value}'")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    # 清理
    effect.cleanup()
    
    if text_field.stringValue() == "Count: 42":
        logger.info("✅ 手动测试成功!")
    else:
        logger.error(f"❌ 手动测试失败! 期望: 'Count: 42', 实际: '{text_field.stringValue()}'")

def test_actual_reactive_binding():
    """测试实际的ReactiveBinding"""
    logger.info("=== 测试实际ReactiveBinding ===")
    
    count = Signal(100)
    count_text = Computed(lambda: f"Count: {count.value}")
    text_field = MockNSTextField("ActualTest")
    
    logger.info("使用ReactiveBinding.bind...")
    cleanup = ReactiveBinding.bind(text_field, "text", count_text)
    
    logger.info("初始状态:")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    logger.info("修改count值...")
    count.value = 999
    
    logger.info("更新后状态:")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    # 清理
    cleanup()
    
    if text_field.stringValue() == "Count: 999":
        logger.info("✅ 实际测试成功!")
    else:
        logger.error(f"❌ 实际测试失败! 期望: 'Count: 999', 实际: '{text_field.stringValue()}'")

if __name__ == "__main__":
    test_reactive_binding_issue()
    logger.info("\n" + "="*50 + "\n")
    test_actual_reactive_binding()