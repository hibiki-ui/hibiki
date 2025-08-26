#!/usr/bin/env python3
"""
专门调试Label创建过程
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level
from macui.components import Label

set_log_level("DEBUG")
logger = get_logger("label_debug")

class LabelDebugComponent(Component):
    """调试Label创建的组件"""
    
    def __init__(self):
        logger.info("=== LabelDebugComponent初始化 ===")
        super().__init__()
        
        # 创建Computed
        self.count = self.create_signal(42)
        self.count_text = self.create_computed(lambda: f"Count: {self.count.value}")
        
        logger.info(f"📊 创建的对象类型:")
        logger.info(f"    - count: {type(self.count)} - isinstance Signal: {isinstance(self.count, Signal)}")
        logger.info(f"    - count_text: {type(self.count_text)} - isinstance Computed: {isinstance(self.count_text, Computed)}")
        
        # 直接测试Label创建
        logger.info("📝 开始创建Label...")
        logger.info(f"📝 传入参数: {self.count_text}, 类型: {type(self.count_text)}")
        
        # 导入检查
        from macui.core.signal import Signal as DirectSignal, Computed as DirectComputed
        logger.info(f"📝 导入检查:")
        logger.info(f"    - macui.Signal == macui.core.signal.Signal: {Signal is DirectSignal}")
        logger.info(f"    - macui.Computed == macui.core.signal.Computed: {Computed is DirectComputed}")
        logger.info(f"    - isinstance(count_text, DirectComputed): {isinstance(self.count_text, DirectComputed)}")
        
        # 测试Label函数的isinstance检查
        logger.info(f"📝 Label函数会检查: isinstance({self.count_text}, (Signal, Computed))")
        result = isinstance(self.count_text, (Signal, Computed))
        logger.info(f"📝 检查结果: {result}")
        
        # 创建Label
        label = Label(self.count_text)
        logger.info(f"📝 Label已创建: {type(label)}")

def test_label_debug():
    """测试Label调试"""
    logger.info("=== 开始Label调试测试 ===")
    
    component = LabelDebugComponent()
    
    logger.info("=== Label调试测试完成 ===")

if __name__ == "__main__":
    test_label_debug()