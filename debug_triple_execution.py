#!/usr/bin/env python3
"""
最小化调试三重执行问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.reactive import Signal, Computed
from macui_v4.core.binding import bind_text
from AppKit import NSTextField

def test_minimal_binding():
    """最小化绑定测试"""
    print("🧪 最小化绑定测试")
    print("-" * 30)
    
    # 创建Signal
    counter = Signal(0)
    print(f"1. Signal创建: {counter.value}")
    
    # 创建Computed
    text = Computed(lambda: f"计数: {counter.value}")
    print(f"2. Computed创建: {text.value}")
    
    # 创建NSTextField
    textfield = NSTextField.alloc().init()
    print(f"3. NSTextField创建: {id(textfield)}")
    
    # 绑定 - 这里应该看到问题
    print("4. 开始绑定...")
    bind_text(textfield, text)
    print("5. 绑定完成")
    
    # 更新测试
    print("6. 更新Signal...")
    counter.value = 42
    print("7. 更新完成")

if __name__ == "__main__":
    test_minimal_binding()