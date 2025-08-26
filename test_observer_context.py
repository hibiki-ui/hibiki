#!/usr/bin/env python3
"""
测试观察者上下文传播
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, get_logger, set_log_level

set_log_level("DEBUG")
logger = get_logger("observer_test")

def test_observer_context():
    """测试观察者上下文传播"""
    logger.info("=== 测试观察者上下文传播 ===")
    
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    def effect_fn():
        logger.info("Effect函数开始执行")
        
        # 检查当前观察者
        from macui.core.signal import Signal
        current_obs = Signal._current_observer.get()
        logger.info(f"Effect函数内的当前观察者: {current_obs}")
        
        # 访问Computed
        logger.info("访问count_text.value...")
        value = count_text.value
        logger.info(f"得到值: {value}")
        
        logger.info("Effect函数执行完成")
        return value
    
    logger.info("创建Effect...")
    effect = Effect(effect_fn)
    
    logger.info("修改Signal...")
    count.value = 10
    
    effect.cleanup()

if __name__ == "__main__":
    test_observer_context()