#!/usr/bin/env python3
"""
对比直接创建vs通过Component创建的响应式对象
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level

set_log_level("DEBUG")
logger = get_logger("component_vs_direct")

def test_direct_creation():
    """测试直接创建Signal/Computed/Effect"""
    logger.info("=== 测试直接创建 ===")
    
    # 直接创建（这个方式工作正常）
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    def state_monitor():
        logger.info(f"DIRECT: count={count.value}, text='{count_text.value}'")
    
    effect = Effect(state_monitor)
    
    logger.info(f"直接创建后 - Signal观察者数: {len(count._observers)}")
    logger.info(f"直接创建后 - Computed观察者数: {len(count_text._observers)}")
    
    # 测试更新
    count.value = 42
    
    logger.info(f"更新后 - Signal观察者数: {len(count._observers)}")
    logger.info(f"更新后 - Computed观察者数: {len(count_text._observers)}")
    
    effect.cleanup()
    logger.info("直接创建测试完成\n")

class TestComponent(Component):
    """测试组件"""
    
    def __init__(self):
        super().__init__()
        
        # 通过Component创建（这个方式有问题）
        self.count = self.create_signal(0)
        self.count_text = self.create_computed(lambda: f"Count: {self.count.value}")
        
        def state_monitor():
            logger.info(f"COMPONENT: count={self.count.value}, text='{self.count_text.value}'")
        
        self.effect = Effect(state_monitor)
        
        logger.info(f"组件创建后 - Signal观察者数: {len(self.count._observers)}")
        logger.info(f"组件创建后 - Computed观察者数: {len(self.count_text._observers)}")

def test_component_creation():
    """测试通过Component创建Signal/Computed/Effect"""
    logger.info("=== 测试组件创建 ===")
    
    component = TestComponent()
    
    # 测试更新
    component.count.value = 42
    
    logger.info(f"更新后 - Signal观察者数: {len(component.count._observers)}")
    logger.info(f"更新后 - Computed观察者数: {len(component.count_text._observers)}")
    
    component.effect.cleanup()
    logger.info("组件创建测试完成\n")

if __name__ == "__main__":
    test_direct_creation()
    test_component_creation()