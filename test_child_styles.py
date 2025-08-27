#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import Label, Button
from macui_v4.core.component import Container
from macui_v4.core.styles import ComponentStyle, Display, FlexDirection, AlignItems, px

def test_child_styles():
    print("🔍 测试子组件样式")
    
    # 初始化管理器
    ManagerFactory.initialize_all()
    
    # 创建子组件
    label1 = Label("测试1", style=ComponentStyle(width=px(200), height=px(30)))
    label2 = Label("测试2", style=ComponentStyle(width=px(150), height=px(25)))
    button = Button("按钮", on_click=lambda: None, style=ComponentStyle(width=px(100), height=px(32)))
    
    # 创建容器
    container = Container(
        children=[label1, label2, button],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=px(400),
            height=px(300),
            gap=px(10)
        )
    )
    
    print(f"📦 容器样式: {container.style}")
    print(f"📦 子组件数量: {len(container.children)}")
    
    for i, child in enumerate(container.children):
        print(f"   子组件 {i+1}: {child.__class__.__name__}")
        print(f"   样式: {child.style}")
        print(f"   有样式: {hasattr(child, 'style')}")
        if hasattr(child, 'style'):
            print(f"   样式类型: {type(child.style)}")

if __name__ == "__main__":
    test_child_styles()