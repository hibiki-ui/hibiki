#!/usr/bin/env python3
"""
单独测试 OutlineView 组件 - 缩小崩溃排查范围
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import OutlineView, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class OutlineViewTestApp:
    """纯 OutlineView 测试应用"""
    
    def __init__(self):
        # 树形数据
        self.tree_data = [
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
                "title": "框架",
                "type": "分类", 
                "children": [
                    {"title": "Django", "type": "Web框架"},
                    {"title": "React", "type": "前端框架"},
                    {"title": "SwiftUI", "type": "UI框架"},
                ]
            },
            {
                "title": "工具",
                "type": "分类",
                "children": [
                    {"title": "Git", "type": "版本控制"},
                    {"title": "Docker", "type": "容器化"},
                    {"title": "VS Code", "type": "编辑器"},
                ]
            }
        ]
        
        # 消息显示
        self.message = Signal("OutlineView 单独测试")
    
    def on_outline_select(self, row, item):
        """大纲视图选择事件"""
        if item:
            title = item.get('title', str(item))
            item_type = item.get('type', '未知类型')
            self.message.value = f"选择了行 {row}: {title} ({item_type})"
        else:
            self.message.value = f"取消选择 (行 {row})"
    
    def on_outline_expand(self, item):
        """大纲项展开事件"""
        if item:
            title = item.get('title', str(item))
            self.message.value = f"展开项: {title}"
    
    def on_outline_collapse(self, item):
        """大纲项收缩事件"""
        if item:
            title = item.get('title', str(item))
            self.message.value = f"收缩项: {title}"
    
    def get_tree_children(self, item):
        """获取树形数据的子项"""
        return item.get('children', []) if item else []
    
    def is_tree_expandable(self, item):
        """判断树形项目是否可展开"""
        children = item.get('children', []) if item else []
        return len(children) > 0
    
    def expand_all(self):
        """展开所有节点（演示功能）"""
        self.message.value = "请求展开所有节点"
    
    def collapse_all(self):
        """收缩所有节点（演示功能）"""
        self.message.value = "请求收缩所有节点"

def main():
    print("=== OutlineView 单独测试 ===")
    
    app = MacUIApp("OutlineView Only Test")
    test_app = OutlineViewTestApp()
    
    from macui import Component
    
    class OutlineViewOnlyComponent(Component):
        def mount(self):
            return VStack(spacing=15, padding=20, children=[
                Label("OutlineView 单独测试", frame=(0, 0, 400, 30)),
                Label(test_app.message),
                
                # 控制按钮
                HStack(spacing=10, children=[
                    Button("展开所有", on_click=test_app.expand_all),
                    Button("收缩所有", on_click=test_app.collapse_all),
                ]),
                
                # OutlineView - 这是重点测试对象
                OutlineView(
                    columns=[
                        {"title": "名称", "key": "title", "width": 200},
                        {"title": "类型", "key": "type", "width": 150},
                    ],
                    root_items=test_app.tree_data,
                    get_children=test_app.get_tree_children,
                    is_expandable=test_app.is_tree_expandable,
                    on_select=test_app.on_outline_select,
                    on_expand=test_app.on_outline_expand,
                    on_collapse=test_app.on_outline_collapse,
                    frame=(0, 0, 400, 300)
                ),
                
                # 状态显示
                VStack(spacing=3, children=[
                    Label(lambda: f"根项目数: {len(test_app.tree_data)}"),
                    Label("展开/收缩状态: 交互式"),
                ]),
            ])
    
    # 创建窗口
    window = app.create_window(
        title="OutlineView Only Test",
        size=(450, 500),
        content=OutlineViewOnlyComponent()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ OutlineView 测试窗口已显示")
    print("📝 测试功能:")
    print("   - OutlineView 树形数据显示")
    print("   - 节点展开和收缩")
    print("   - 选择事件处理")
    print("   - 多列显示")
    
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