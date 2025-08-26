#!/usr/bin/env python3
"""
专门模拟计数器应用的响应式逻辑，不涉及UI
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level

set_log_level("DEBUG")
logger = get_logger("counter_logic_test")

class DebugCounterLogic(Component):
    """调试计数器逻辑，纯响应式，无UI"""
    
    def __init__(self):
        logger.info("🚀 DebugCounterLogic.__init__: 开始初始化")
        super().__init__()
        
        # 创建响应式状态并记录详细信息
        logger.info("📊 创建Signal(count)...")
        self.count = self.create_signal(0)
        logger.info(f"📊 Signal(count)已创建:")
        logger.info(f"    - 初始值: {self.count.value}")
        logger.info(f"    - Signal对象ID: {id(self.count)}")
        logger.info(f"    - 观察者数量: {len(self.count._observers)}")
        
        # 创建计算属性
        logger.info("🧮 创建Computed(count_text)...")
        self.count_text = self.create_computed(
            lambda: f"Count: {self.count.value}"
        )
        logger.info(f"🧮 Computed(count_text)已创建:")
        logger.info(f"    - 初始值: '{self.count_text.value}'")
        logger.info(f"    - Computed对象ID: {id(self.count_text)}")
        logger.info(f"    - Signal观察者数量: {len(self.count._observers)}")
        logger.info(f"    - Computed观察者数量: {len(self.count_text._observers)}")
        
        # 创建监控Effect
        logger.info("👁️ 创建监控Effect...")
        def state_monitor():
            logger.info(f"👁️ STATE_MONITOR: count={self.count.value}, text='{self.count_text.value}'")
        
        self.monitor_effect = Effect(state_monitor)
        logger.info("👁️ 监控Effect已创建并执行")
        
        # 记录依赖关系
        logger.info("🔗 依赖关系分析:")
        logger.info(f"    - Signal[{id(self.count)}] 观察者: {len(self.count._observers)} 个")
        logger.info(f"    - Computed[{id(self.count_text)}] 观察者: {len(self.count_text._observers)} 个")
        
        logger.info("✅ DebugCounterLogic初始化完成")
    
    def increment(self):
        """增加计数 - 详细交互日志"""
        logger.info("")
        logger.info("🟢" + "="*50)
        logger.info("🟢 BUTTON CLICK EVENT: Increment")
        logger.info("🟢" + "="*50)
        
        # 记录点击前状态
        old_value = self.count.value
        old_text = self.count_text.value
        logger.info("📍 点击前状态:")
        logger.info(f"    - count.value = {old_value}")
        logger.info(f"    - count_text.value = '{old_text}'")
        logger.info(f"    - Signal观察者数: {len(self.count._observers)}")
        logger.info(f"    - Computed观察者数: {len(self.count_text._observers)}")
        
        # 执行状态变更
        logger.info("⚡ 执行状态变更: self.count.value += 1")
        self.count.value += 1
        logger.info("⚡ 状态变更语句执行完毕")
        
        # 记录变更后状态
        new_value = self.count.value
        new_text = self.count_text.value
        logger.info("📍 变更后状态:")
        logger.info(f"    - count.value = {new_value} (变化: {old_value} -> {new_value})")
        logger.info(f"    - count_text.value = '{new_text}' (变化: '{old_text}' -> '{new_text}')")
        
        logger.info("✅ Increment操作完成")
        logger.info("🟢" + "="*50)
        logger.info("")

def test_counter_logic():
    """测试计数器逻辑"""
    logger.info("=== 测试计数器应用逻辑 ===")
    
    # 创建计数器逻辑
    counter = DebugCounterLogic()
    
    # 模拟按钮点击
    logger.info("\n" + "="*60)
    logger.info("开始模拟按钮点击测试")
    logger.info("="*60)
    
    counter.increment()
    counter.increment()
    
    logger.info("=== 测试完成 ===")

if __name__ == "__main__":
    test_counter_logic()