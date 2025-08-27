#!/usr/bin/env python3
"""测试ModernComponent的get_view()方法"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.components.modern_components import ModernLabel, ModernButton
from macui.layout.styles import LayoutStyle
from AppKit import *

def test_modern_components():
    print("🧪 测试ModernComponent的get_view()方法...")
    
    # 测试ModernLabel
    label = ModernLabel("测试文本", style=LayoutStyle(width=100, height=30))
    print(f"ModernLabel对象: {label}")
    print(f"ModernLabel类型: {type(label)}")
    
    view = label.get_view()
    print(f"get_view()返回: {view}")
    print(f"返回对象类型: {type(view)}")
    
    if hasattr(view, 'setFrame_'):
        print("✅ 返回对象有setFrame_方法")
    else:
        print("❌ 返回对象没有setFrame_方法")
    
    # 测试ModernButton  
    button = ModernButton("测试按钮", style=LayoutStyle(width=100, height=30))
    print(f"\nModernButton对象: {button}")
    
    button_view = button.get_view()
    print(f"get_view()返回: {button_view}")
    print(f"返回对象类型: {type(button_view)}")

if __name__ == "__main__":
    test_modern_components()