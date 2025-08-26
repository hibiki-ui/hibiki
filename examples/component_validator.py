#!/usr/bin/env python3
"""
组件验证工具 - 手动测试各个布局组件是否正常工作
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import (
    TableView, TabView, SplitView, OutlineView,
    VStack, HStack, Button, Label, TextField
)
from macui.app import MacUIApp

set_log_level("INFO")

def test_tableview():
    """测试 TableView 组件"""
    print("🧪 测试 TableView 组件...")
    
    app = MacUIApp("TableView 验证")
    
    data = Signal([
        {"name": "张三", "age": "28"},
        {"name": "李四", "age": "32"},
        {"name": "王五", "age": "25"},
    ])
    selected_row = Signal(-1)
    
    from macui import Component
    
    class TableTestComponent(Component):
        def mount(self):
            return VStack(spacing=10, padding=20, children=[
                Label("TableView 测试 - 请尝试点击行"),
                TableView(
                    columns=[
                        {"title": "姓名", "key": "name", "width": 120},
                        {"title": "年龄", "key": "age", "width": 80},
                    ],
                    data=data,
                    selected_row=selected_row,
                    on_select=lambda row: print(f"选择了行: {row}"),
                    frame=(0, 0, 300, 150)
                ),
                Label(lambda: f"选中行: {selected_row.value}"),
                Button("关闭测试", on_click=lambda: app.quit())
            ])
    
    window = app.create_window(
        title="TableView 验证",
        size=(350, 300),
        content=TableTestComponent()
    )
    
    window.show()
    app.run()
    return True

def test_tabview():
    """测试 TabView 组件"""
    print("🧪 测试 TabView 组件...")
    
    app = MacUIApp("TabView 验证")
    current_tab = Signal(0)
    
    from macui import Component
    
    class TabTestComponent(Component):
        def mount(self):
            tab1_content = VStack(padding=10, children=[
                Label("这是第一个标签页"),
                Label("可以点击标签页切换"),
            ])
            
            tab2_content = VStack(padding=10, children=[
                Label("这是第二个标签页"),
                Button("测试按钮", on_click=lambda: print("TabView中的按钮被点击")),
            ])
            
            return VStack(spacing=10, padding=20, children=[
                Label("TabView 测试"),
                TabView(
                    tabs=[
                        {"title": "标签页1", "content": tab1_content},
                        {"title": "标签页2", "content": tab2_content},
                    ],
                    selected=current_tab,
                    on_change=lambda idx, item: print(f"切换到标签页: {idx}"),
                    frame=(0, 0, 300, 200)
                ),
                Label(lambda: f"当前标签页: {current_tab.value}"),
                Button("关闭测试", on_click=lambda: app.quit())
            ])
    
    window = app.create_window(
        title="TabView 验证",
        size=(350, 350),
        content=TabTestComponent()
    )
    
    window.show()
    app.run()
    return True

def test_splitview():
    """测试 SplitView 组件"""
    print("🧪 测试 SplitView 组件...")
    
    app = MacUIApp("SplitView 验证")
    
    from macui import Component
    
    class SplitTestComponent(Component):
        def mount(self):
            left_panel = VStack(padding=10, children=[
                Label("左侧面板"),
                Label("可以拖拽中间分割线"),
                Label("调整两边大小"),
            ])
            
            right_panel = VStack(padding=10, children=[
                Label("右侧面板"),
                Label("SplitView 测试"),
                Button("测试按钮", on_click=lambda: print("SplitView中的按钮被点击")),
            ])
            
            return VStack(spacing=10, padding=20, children=[
                Label("SplitView 测试"),
                SplitView(
                    orientation="horizontal",
                    children=[left_panel, right_panel],
                    divider_style="thin",
                    on_resize=lambda frames: print(f"分割视图调整: {len(frames)}个子视图"),
                    frame=(0, 0, 400, 200)
                ),
                Button("关闭测试", on_click=lambda: app.quit())
            ])
    
    window = app.create_window(
        title="SplitView 验证",
        size=(450, 350),
        content=SplitTestComponent()
    )
    
    window.show()
    app.run()
    return True

def test_outlineview():
    """测试 OutlineView 组件"""
    print("🧪 测试 OutlineView 组件...")
    
    app = MacUIApp("OutlineView 验证")
    
    tree_data = [
        {
            "title": "编程语言",
            "type": "分类",
            "children": [
                {"title": "Python", "type": "语言"},
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
    
    from macui import Component
    
    class OutlineTestComponent(Component):
        def mount(self):
            return VStack(spacing=10, padding=20, children=[
                Label("OutlineView 测试 - 请点击展开节点"),
                OutlineView(
                    columns=[
                        {"title": "名称", "key": "title", "width": 150},
                        {"title": "类型", "key": "type", "width": 100},
                    ],
                    root_items=tree_data,
                    get_children=lambda item: item.get('children', []) if item else [],
                    is_expandable=lambda item: len(item.get('children', [])) > 0 if item else False,
                    on_select=lambda row, item: print(f"选择: {item.get('title') if item else 'None'}"),
                    on_expand=lambda item: print(f"展开: {item.get('title') if item else 'None'}"),
                    on_collapse=lambda item: print(f"收缩: {item.get('title') if item else 'None'}"),
                    frame=(0, 0, 300, 200)
                ),
                Button("关闭测试", on_click=lambda: app.quit())
            ])
    
    window = app.create_window(
        title="OutlineView 验证",
        size=(350, 350),
        content=OutlineTestComponent()
    )
    
    window.show()
    app.run()
    return True

def test_complete_layout():
    """测试完整的 Stage 3 布局"""
    print("🧪 测试完整的 Stage 3 布局...")
    
    app = MacUIApp("完整布局验证")
    
    # 简化版的 Stage 3 布局
    table_data = Signal([
        {"name": "项目A", "status": "进行中"},
        {"name": "项目B", "status": "已完成"},
    ])
    
    current_tab = Signal(0)
    
    tree_data = [{
        "title": "任务",
        "children": [
            {"title": "UI设计"},
            {"title": "开发"},
        ]
    }]
    
    from macui import Component
    
    class CompleteTestComponent(Component):
        def mount(self):
            # 标签页1：表格
            table_tab = VStack(spacing=10, padding=10, children=[
                Label("表格测试"),
                TableView(
                    columns=[
                        {"title": "名称", "key": "name", "width": 100},
                        {"title": "状态", "key": "status", "width": 80},
                    ],
                    data=table_data,
                    frame=(0, 0, 250, 120)
                ),
            ])
            
            # 标签页2：分割视图
            split_tab = VStack(spacing=10, padding=10, children=[
                Label("分割视图测试"),
                SplitView(
                    orientation="horizontal",
                    children=[
                        Label("左侧", padding=10),
                        Label("右侧", padding=10),
                    ],
                    frame=(0, 0, 250, 100)
                ),
            ])
            
            # 标签页3：大纲视图
            outline_tab = VStack(spacing=10, padding=10, children=[
                Label("大纲视图测试"),
                OutlineView(
                    columns=[{"title": "任务", "key": "title", "width": 200}],
                    root_items=tree_data,
                    get_children=lambda item: item.get('children', []) if item else [],
                    is_expandable=lambda item: len(item.get('children', [])) > 0 if item else False,
                    frame=(0, 0, 250, 120)
                ),
            ])
            
            return VStack(spacing=15, padding=20, children=[
                Label("完整布局测试 - 所有组件组合"),
                
                TabView(
                    tabs=[
                        {"title": "表格", "content": table_tab},
                        {"title": "分割", "content": split_tab},
                        {"title": "大纲", "content": outline_tab},
                    ],
                    selected=current_tab,
                    frame=(0, 0, 350, 250)
                ),
                
                Label(lambda: f"当前标签: {current_tab.value}"),
                Button("关闭测试", on_click=lambda: app.quit())
            ])
    
    window = app.create_window(
        title="完整布局验证",
        size=(400, 400),
        content=CompleteTestComponent()
    )
    
    window.show()
    app.run()
    return True

def main():
    """主函数 - 交互式测试选择"""
    print("="*50)
    print("macUI Stage 3 布局组件验证工具")
    print("="*50)
    print()
    print("请选择要测试的组件:")
    print("1. TableView (表格视图)")
    print("2. TabView (标签页视图)")
    print("3. SplitView (分割视图)")
    print("4. OutlineView (大纲视图)")
    print("5. 完整布局测试 (所有组件组合)")
    print("6. 全部依次测试")
    print("0. 退出")
    print()
    
    while True:
        try:
            choice = input("请输入选择 (0-6): ").strip()
            
            if choice == "0":
                print("👋 退出验证")
                break
            elif choice == "1":
                test_tableview()
                print("✅ TableView 测试完成")
            elif choice == "2":
                test_tabview()
                print("✅ TabView 测试完成")
            elif choice == "3":
                test_splitview()
                print("✅ SplitView 测试完成")
            elif choice == "4":
                test_outlineview()
                print("✅ OutlineView 测试完成")
            elif choice == "5":
                test_complete_layout()
                print("✅ 完整布局测试完成")
            elif choice == "6":
                print("🚀 开始全部测试...")
                components = [
                    ("TableView", test_tableview),
                    ("TabView", test_tabview),
                    ("SplitView", test_splitview),
                    ("OutlineView", test_outlineview),
                    ("完整布局", test_complete_layout),
                ]
                
                for name, test_func in components:
                    print(f"\n🧪 测试 {name}...")
                    try:
                        test_func()
                        print(f"✅ {name} 测试通过")
                    except Exception as e:
                        print(f"❌ {name} 测试失败: {e}")
                        import traceback
                        traceback.print_exc()
                
                print("\n🎉 全部测试完成！")
            else:
                print("❌ 无效选择，请输入 0-6")
            
            print("\n" + "="*30)
            
        except KeyboardInterrupt:
            print("\n👋 用户中断，退出验证")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()