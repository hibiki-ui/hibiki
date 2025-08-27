#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px
from macui_v4.core.layout import V4StyleConverter

def test_style_conversion():
    print("🔍 测试样式转换")
    
    # 测试Label样式
    label_style = ComponentStyle(width=px(200), height=px(30))
    print(f"📝 原始Label样式: {label_style}")
    
    try:
        converted = V4StyleConverter.convert_to_stretchable_style(label_style)
        print(f"✅ 转换成功: {converted}")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试Container样式
    container_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        align_items=AlignItems.CENTER,
        width=px(400),
        height=px(300),
        gap=px(10)
    )
    print(f"\n📦 原始Container样式: {container_style}")
    
    try:
        converted = V4StyleConverter.convert_to_stretchable_style(container_style)
        print(f"✅ 转换成功: {converted}")
        print(f"   Display: {converted.display}")
        print(f"   Size: {converted.size}")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_style_conversion()