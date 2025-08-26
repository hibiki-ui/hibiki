#!/usr/bin/env python3
"""
简单 OutlineView 测试 - 直接测试不需要交互
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import OutlineView, VStack, HStack, Button, Label
from macui.app import MacUIApp

set_log_level("INFO")

def main():
    print("🧪 开始简单 OutlineView 测试...")
    
    app = MacUIApp("简单 OutlineView 测试")
    
    # 创建树形数据
    tree_data = [
        {
            "title": "编程语言",
            "type": "分类",
            "children": [
                {"title": "Python", "type": "语言"},
                {"title": "JavaScript", "type": "语言"},
                {"title": "Swift", "type": "语言"},
            ]
        },
        {
            "title": "工具",
            "type": "分类",
            "children": [
                {"title": "Git", "type": "版本控制"},
                {"title": "VS Code", "type": "编辑器"},
            ]
        }
    ]
    
    message = Signal("OutlineView 测试开始")
    
    def on_select(row, item):
        print(f"📊 选择了行: {row}, 项目: {item}")
        if item:
            title = item.get('title', '未知')
            item_type = item.get('type', '未知类型')
            message.value = f"选中: {title} ({item_type})"
        else:
            message.value = f"取消选择 (行 {row})"
    
    def on_expand(item):
        print(f"📊 展开项目: {item}")
        if item:
            title = item.get('title', '未知')
            message.value = f"展开: {title}"
    
    def on_collapse(item):
        print(f"📊 收缩项目: {item}")
        if item:
            title = item.get('title', '未知')
            message.value = f"收缩: {title}"
    
    def get_children(item):
        return item.get('children', []) if item else []
    
    def is_expandable(item):
        children = item.get('children', []) if item else []
        return len(children) > 0
    
    from macui import Component
    
    class SimpleOutlineViewComponent(Component):
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("简单 OutlineView 测试"),
                Label(message),
                
                # OutlineView
                OutlineView(
                    columns=[
                        {"title": "名称", "key": "title", "width": 180},
                        {"title": "类型", "key": "type", "width": 120},
                    ],
                    root_items=tree_data,
                    get_children=get_children,
                    is_expandable=is_expandable,
                    on_select=on_select,
                    on_expand=on_expand,
                    on_collapse=on_collapse,
                    frame=(0, 0, 350, 250)
                ),
                
                # 状态显示
                Label(lambda: f"根项目数: {len(tree_data)}"),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="简单 OutlineView 测试",
        size=(400, 400),
        content=SimpleOutlineViewComponent()
    )
    
    # 显示窗口
    window.show()
    print("✅ 窗口已显示，正在运行...")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()