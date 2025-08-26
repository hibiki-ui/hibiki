#!/usr/bin/env python3
"""
深度检查Component创建的对象类型
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level

set_log_level("DEBUG")
logger = get_logger("object_inspection")

class InspectComponent(Component):
    """检查组件"""
    
    def __init__(self):
        super().__init__()
        
        self.count = self.create_signal(0)
        self.count_text = self.create_computed(lambda: f"Count: {self.count.value}")
        
        # 详细检查对象
        logger.info("=== 对象检查 ===")
        logger.info(f"self.count 类型: {type(self.count)}")
        logger.info(f"self.count 是Signal?: {isinstance(self.count, Signal)}")
        logger.info(f"self.count ID: {id(self.count)}")
        logger.info(f"self.count hasattr 'get': {hasattr(self.count, 'get')}")
        logger.info(f"self.count hasattr 'value': {hasattr(self.count, 'value')}")
        
        logger.info(f"self.count_text 类型: {type(self.count_text)}")
        logger.info(f"self.count_text 是Computed?: {isinstance(self.count_text, Computed)}")
        logger.info(f"self.count_text ID: {id(self.count_text)}")
        logger.info(f"self.count_text hasattr 'get': {hasattr(self.count_text, 'get')}")
        logger.info(f"self.count_text hasattr 'value': {hasattr(self.count_text, 'value')}")
        
        # 尝试手动调用get方法
        logger.info("\n=== 手动调用get方法 ===")
        try:
            count_val = self.count.get()
            logger.info(f"self.count.get() = {count_val}")
        except Exception as e:
            logger.error(f"self.count.get() 失败: {e}")
            
        try:
            text_val = self.count_text.get()
            logger.info(f"self.count_text.get() = '{text_val}'")
        except Exception as e:
            logger.error(f"self.count_text.get() 失败: {e}")
            
        # 尝试通过property访问
        logger.info("\n=== 通过property访问 ===")
        try:
            count_val = self.count.value
            logger.info(f"self.count.value = {count_val}")
        except Exception as e:
            logger.error(f"self.count.value 失败: {e}")
            
        try:
            text_val = self.count_text.value
            logger.info(f"self.count_text.value = '{text_val}'")
        except Exception as e:
            logger.error(f"self.count_text.value 失败: {e}")

def test_object_inspection():
    """测试对象检查"""
    logger.info("=== 开始对象检查 ===")
    
    component = InspectComponent()
    
    logger.info("=== 检查完成 ===")

if __name__ == "__main__":
    test_object_inspection()