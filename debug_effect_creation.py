#!/usr/bin/env python3
"""
专门调试Effect创建的问题
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.reactive import Signal, Computed, Effect

# 保存原始的Effect.__init__
_original_effect_init = Effect.__init__

# 创建一个计数器来跟踪调用
effect_call_count = 0

def debug_effect_init(self, fn):
    """调试版本的Effect.__init__"""
    global effect_call_count
    effect_call_count += 1
    
    # 强制输出到stderr以确保能看到
    import sys
    sys.stderr.write(f"🚨 DEBUG: Effect.__init__ 调用 #{effect_call_count}, id={id(self)}, fn={getattr(fn, '__name__', 'unknown')}\n")
    sys.stderr.flush()
    
    # 调用原始方法
    return _original_effect_init(self, fn)

# 替换Effect.__init__
Effect.__init__ = debug_effect_init

def test_with_gui():
    """测试GUI环境下的Effect创建"""
    print("🧪 开始GUI环境Effect创建测试")
    
    # 创建Signal和Computed
    counter = Signal(0)
    text = Computed(lambda: f"计数: {counter.value}")
    
    # 创建NSTextField并绑定
    from AppKit import NSTextField
    from macui_v4.core.binding import bind_text
    
    textfield = NSTextField.alloc().init()
    print("准备绑定...")
    
    bind_text(textfield, text)
    print("绑定完成")
    
    print(f"总共创建了 {effect_call_count} 个Effect")

if __name__ == "__main__":
    test_with_gui()