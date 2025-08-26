#!/usr/bin/env python3
"""
调试观察者上下文传播问题
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, get_logger, set_log_level

set_log_level("DEBUG")
logger = get_logger("debug_context")

def test_observer_context():
    """测试观察者上下文是否正确传播"""
    logger.info("=== 测试观察者上下文传播 ===")
    
    # 创建一个简单的信号
    count = Signal(0)
    logger.info(f"创建Signal: count[{id(count)}] = {count.value}")
    
    # 创建计算属性
    count_text = Computed(lambda: f"Count: {count.value}")
    logger.info(f"创建Computed: count_text[{id(count_text)}] = '{count_text.value}'")
    
    # 现在应该有1个观察者（Computed观察Signal）
    logger.info(f"Signal观察者数: {len(count._observers)}")
    logger.info(f"Computed观察者数: {len(count_text._observers)}")
    
    # 创建Effect手动检查上下文传播
    def manual_effect():
        logger.info("manual_effect开始执行")
        
        # 检查当前观察者上下文
        from macui.core.signal import Signal
        current_observer = Signal._current_observer.get()
        logger.info(f"manual_effect中的当前观察者: {current_observer}")
        logger.info(f"当前观察者类型: {type(current_observer)}")
        logger.info(f"当前观察者ID: {id(current_observer) if current_observer else 'None'}")
        
        # 访问信号，应该会触发观察者注册
        logger.info("即将访问count.value...")
        count_value = count.value
        logger.info(f"count.value = {count_value}")
        
        logger.info("即将访问count_text.value...")
        text_value = count_text.value  
        logger.info(f"count_text.value = '{text_value}'")
        
        logger.info("manual_effect执行完成")
    
    logger.info("创建Effect...")
    effect = Effect(manual_effect)
    
    logger.info("Effect创建后的观察者数量:")
    logger.info(f"Signal观察者数: {len(count._observers)}")
    logger.info(f"Computed观察者数: {len(count_text._observers)}")
    
    logger.info("修改Signal值...")
    count.value = 42
    
    logger.info("修改后的观察者数量:")
    logger.info(f"Signal观察者数: {len(count._observers)}")
    logger.info(f"Computed观察者数: {len(count_text._observers)}")
    
    # 清理
    effect.cleanup()
    
    logger.info("=== 测试完成 ===")

if __name__ == "__main__":
    test_observer_context()