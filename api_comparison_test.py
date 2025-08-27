#!/usr/bin/env python3
"""对比统一API和直接导入的差异"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.layout.styles import LayoutStyle

print("🧪 测试统一API vs 直接导入...")

# 直接导入
from macui.components.modern_components import ModernLabel, ModernButton
from macui.components.modern_layout import VStack

# 统一API导入
from macui.components import Label, Button, VStack as UnifiedVStack

print(f"直接导入 - ModernLabel: {ModernLabel}")
print(f"统一API - Label: {Label}")
print(f"Label == ModernLabel: {Label is ModernLabel}")

print(f"直接导入 - VStack: {VStack}")  
print(f"统一API - VStack: {UnifiedVStack}")
print(f"VStack == UnifiedVStack: {VStack is UnifiedVStack}")

# 测试创建
print("\n🔧 测试组件创建...")

direct_label = ModernLabel("Direct Label", style=LayoutStyle(height=30))
unified_label = Label("Unified Label", style=LayoutStyle(height=30))

print(f"直接创建: {direct_label}")
print(f"统一API创建: {unified_label}")
print(f"类型相同: {type(direct_label) == type(unified_label)}")

# 测试VStack创建
print("\n🔧 测试VStack创建...")

try:
    direct_vstack = VStack(children=[direct_label], style=LayoutStyle(gap=10))
    print(f"直接VStack创建成功: {direct_vstack}")
except Exception as e:
    print(f"直接VStack创建失败: {e}")

try:
    unified_vstack = UnifiedVStack(children=[unified_label], style=LayoutStyle(gap=10))
    print(f"统一VStack创建成功: {unified_vstack}")
except Exception as e:
    print(f"统一VStack创建失败: {e}")