#!/usr/bin/env python3
"""
带详细日志的响应式系统调试
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入并设置日志
from macui import get_logger, set_log_level
from macui import Signal, Computed, Effect
from macui.core.binding import ReactiveBinding

# 设置为DEBUG等级以查看所有日志
set_log_level("DEBUG")

logger = get_logger("debug_test")

# 模拟NSTextField
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
    
    def __str__(self):
        return f"{self.name}[{id(self)}]"

def test_full_reactive_chain():
    """测试完整的响应式链条"""
    logger.info("=" * 50)
    logger.info("开始完整响应式链条测试")
    logger.info("=" * 50)
    
    # 1. 创建Signal
    logger.info("步骤1: 创建Signal")
    count = Signal(0)
    
    # 2. 创建Computed
    logger.info("步骤2: 创建Computed")
    count_text = Computed(lambda: f"Count: {count.value}")
    
    # 3. 创建Mock UI组件
    logger.info("步骤3: 创建Mock UI组件")
    text_field = MockNSTextField("CounterLabel")
    
    # 4. 创建绑定
    logger.info("步骤4: 创建ReactiveBinding")
    cleanup = ReactiveBinding.bind(text_field, "text", count_text)
    
    # 5. 验证初始状态
    logger.info("步骤5: 验证初始状态")
    logger.info(f"count.value = {count.value}")
    logger.info(f"count_text.value = '{count_text.value}'")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    # 6. 模拟按钮点击 - 第一次
    logger.info("步骤6: 模拟按钮点击 #1")
    logger.info(">> count.value = 1")
    count.value = 1
    
    logger.info("验证第一次更新结果:")
    logger.info(f"count.value = {count.value}")
    logger.info(f"count_text.value = '{count_text.value}'")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    # 7. 模拟按钮点击 - 第二次
    logger.info("步骤7: 模拟按钮点击 #2")
    logger.info(">> count.value = 5")
    count.value = 5
    
    logger.info("验证第二次更新结果:")
    logger.info(f"count.value = {count.value}")
    logger.info(f"count_text.value = '{count_text.value}'")
    logger.info(f"text_field.stringValue() = '{text_field.stringValue()}'")
    
    # 8. 验证结果
    logger.info("步骤8: 验证最终结果")
    expected_text = "Count: 5"
    actual_text = text_field.stringValue()
    
    if actual_text == expected_text:
        logger.info("✅ 测试成功! 响应式更新工作正常")
    else:
        logger.error(f"❌ 测试失败! 期望: '{expected_text}', 实际: '{actual_text}'")
    
    # 9. 清理
    logger.info("步骤9: 清理资源")
    cleanup()
    
    logger.info("=" * 50)
    logger.info("完整响应式链条测试完成")
    logger.info("=" * 50)

def test_signal_only():
    """仅测试Signal基础功能"""
    logger.info("\n--- Signal基础功能测试 ---")
    
    count = Signal(42)
    updates = []
    
    def observer():
        updates.append(count.value)
        logger.debug(f"观察者收到更新: {count.value}")
    
    effect = Effect(observer)
    
    logger.info("更新Signal值...")
    count.value = 100
    count.value = 200
    
    logger.info(f"观察者收到的更新: {updates}")
    effect.cleanup()

def test_computed_only():
    """仅测试Computed功能"""
    logger.info("\n--- Computed功能测试 ---")
    
    base = Signal(10)
    computed = Computed(lambda: base.value * 2)
    
    logger.info(f"初始computed值: {computed.value}")
    
    base.value = 20
    logger.info(f"base更新后computed值: {computed.value}")

if __name__ == "__main__":
    # 运行所有测试
    test_signal_only()
    test_computed_only() 
    test_full_reactive_chain()
    
    logger.info("\n🔍 请检查logs/macui_debug.log文件查看详细日志")