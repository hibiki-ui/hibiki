#!/usr/bin/env python3
"""
测试第三阶段布局组件：TabView, SplitView, TableView, OutlineView
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import (
    TabView, SplitView, TableView, OutlineView,
    VStack, HStack, Button, Label, TextField
)
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class Stage3LayoutTestApp:
    """第三阶段布局组件测试应用"""
    
    def __init__(self):
        # TabView 状态
        self.current_tab = Signal(0)
        
        # TableView 状态
        self.selected_row = Signal(-1)
        self.table_data = Signal([
            {"name": "张三", "age": "28", "city": "北京"},
            {"name": "李四", "age": "32", "city": "上海"},
            {"name": "王五", "age": "25", "city": "广州"},
            {"name": "赵六", "age": "30", "city": "深圳"},
            {"name": "孙七", "age": "27", "city": "杭州"},
        ])
        
        # OutlineView 状态  
        self.tree_data = [
            {
                "title": "编程语言",
                "children": [
                    {"title": "Python", "type": "语言"},
                    {"title": "JavaScript", "type": "语言"},
                    {"title": "Swift", "type": "语言"},
                ]
            },
            {
                "title": "框架",
                "children": [
                    {"title": "Django", "type": "Web框架"},
                    {"title": "React", "type": "前端框架"},
                    {"title": "SwiftUI", "type": "UI框架"},
                ]
            },
            {
                "title": "工具",
                "children": [
                    {"title": "Git", "type": "版本控制"},
                    {"title": "Docker", "type": "容器化"},
                    {"title": "VS Code", "type": "编辑器"},
                ]
            }
        ]
        
        # 消息显示
        self.message = Signal("第三阶段布局组件测试准备就绪")
        
        # 动态数据
        self.new_name = Signal("")
        self.new_age = Signal("")
        self.new_city = Signal("")
        
    def on_tab_change(self, index, tab_item):
        tab_titles = ["表格视图", "大纲视图", "分割视图", "组合演示"]
        self.message.value = f"切换到标签页: {tab_titles[index] if index < len(tab_titles) else f'标签{index}'}"
        
    def on_table_select(self, row):
        if row >= 0 and row < len(self.table_data.value):
            person = self.table_data.value[row]
            self.message.value = f"选择了表格行 {row}: {person['name']}"
        else:
            self.message.value = f"取消选择 (行 {row})"
            
    def on_table_double_click(self, row):
        if row >= 0 and row < len(self.table_data.value):
            person = self.table_data.value[row]
            self.message.value = f"双击表格行 {row}: {person['name']} ({person['age']}岁, {person['city']})"
    
    def on_outline_select(self, row, item):
        if item:
            title = item.get('title', str(item))
            item_type = item.get('type', '分类')
            self.message.value = f"选择了大纲项: {title} ({item_type})"
    
    def on_outline_expand(self, item):
        if item:
            title = item.get('title', str(item))
            self.message.value = f"展开大纲项: {title}"
    
    def on_outline_collapse(self, item):
        if item:
            title = item.get('title', str(item))
            self.message.value = f"收缩大纲项: {title}"
    
    def on_split_resize(self, frames):
        self.message.value = f"分割视图调整: {len(frames)}个子视图"
    
    def get_tree_children(self, item):
        """获取树形数据的子项"""
        return item.get('children', []) if item else []
    
    def is_tree_expandable(self, item):
        """判断树形项目是否可展开"""
        children = item.get('children', []) if item else []
        return len(children) > 0
    
    def add_table_row(self):
        """添加表格行"""
        if self.new_name.value.strip() and self.new_age.value.strip() and self.new_city.value.strip():
            new_data = list(self.table_data.value)
            new_data.append({
                "name": self.new_name.value.strip(),
                "age": self.new_age.value.strip(),
                "city": self.new_city.value.strip()
            })
            self.table_data.value = new_data
            
            # 清空输入框
            self.new_name.value = ""
            self.new_age.value = ""
            self.new_city.value = ""
            
            self.message.value = f"添加了新行，当前共 {len(new_data)} 行"
    
    def remove_selected_row(self):
        """删除选中的表格行"""
        if self.selected_row.value >= 0 and self.selected_row.value < len(self.table_data.value):
            new_data = list(self.table_data.value)
            removed = new_data.pop(self.selected_row.value)
            self.table_data.value = new_data
            self.selected_row.value = -1
            self.message.value = f"删除了 {removed['name']}，剩余 {len(new_data)} 行"
        else:
            self.message.value = "没有选中行可删除"
    
    def clear_table(self):
        """清空表格"""
        self.table_data.value = []
        self.selected_row.value = -1
        self.message.value = "表格已清空"
    
    def reset_table_data(self):
        """重置表格数据"""
        self.table_data.value = [
            {"name": "张三", "age": "28", "city": "北京"},
            {"name": "李四", "age": "32", "city": "上海"},
            {"name": "王五", "age": "25", "city": "广州"},
            {"name": "赵六", "age": "30", "city": "深圳"},
            {"name": "孙七", "age": "27", "city": "杭州"},
        ]
        self.selected_row.value = -1
        self.message.value = "表格数据已重置"

def main():
    print("=== 第三阶段布局组件测试 ===")
    
    app = MacUIApp("Stage 3 Layout Components Test")
    test_app = Stage3LayoutTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class Stage3LayoutComponent(Component):
            def mount(self):
                # 创建标签页内容
                
                # 标签页1：表格视图
                table_tab_content = VStack(spacing=10, padding=10, children=[
                    Label("表格视图演示"),
                    
                    # 表格操作区
                    HStack(spacing=10, children=[
                        VStack(spacing=5, children=[
                            Label("添加新行:"),
                            HStack(spacing=5, children=[
                                TextField(placeholder="姓名", value=test_app.new_name, frame=(0, 0, 80, 25)),
                                TextField(placeholder="年龄", value=test_app.new_age, frame=(0, 0, 50, 25)),
                                TextField(placeholder="城市", value=test_app.new_city, frame=(0, 0, 80, 25)),
                            ]),
                            HStack(spacing=5, children=[
                                Button("添加", on_click=test_app.add_table_row),
                                Button("删除选中", on_click=test_app.remove_selected_row),
                                Button("清空", on_click=test_app.clear_table),
                                Button("重置", on_click=test_app.reset_table_data),
                            ]),
                        ]),
                    ]),
                    
                    # 表格视图
                    TableView(
                        columns=[
                            {"title": "姓名", "key": "name", "width": 100},
                            {"title": "年龄", "key": "age", "width": 60},
                            {"title": "城市", "key": "city", "width": 100},
                        ],
                        data=test_app.table_data,
                        selected_row=test_app.selected_row,
                        on_select=test_app.on_table_select,
                        on_double_click=test_app.on_table_double_click,
                        frame=(0, 0, 400, 200)
                    ),
                ])
                
                # 标签页2：大纲视图
                outline_tab_content = VStack(spacing=10, padding=10, children=[
                    Label("大纲视图演示（树形结构）"),
                    
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
                ])
                
                # 标签页3：分割视图
                split_tab_content = VStack(spacing=10, padding=10, children=[
                    Label("分割视图演示"),
                    
                    SplitView(
                        orientation="horizontal",
                        children=[
                            VStack(padding=10, children=[
                                Label("左侧面板"),
                                Label("• 文件列表"),
                                Label("• 工具栏"),
                                Label("• 设置"),
                            ]),
                            VStack(padding=10, children=[
                                Label("右侧面板"),
                                Label("• 主要内容"),
                                Label("• 编辑区域"),
                                Label("• 预览"),
                            ]),
                        ],
                        divider_style="thin",
                        on_resize=test_app.on_split_resize,
                        frame=(0, 0, 400, 200)
                    ),
                ])
                
                # 标签页4：组合演示
                combo_tab_content = VStack(spacing=10, padding=10, children=[
                    Label("组合布局演示"),
                    
                    SplitView(
                        orientation="vertical",
                        children=[
                            # 上半部分：表格
                            TableView(
                                columns=[
                                    {"title": "项目", "key": "name", "width": 120},
                                    {"title": "状态", "key": "age", "width": 80},
                                ],
                                data=Signal([
                                    {"name": "项目A", "age": "进行中"},
                                    {"name": "项目B", "age": "已完成"},
                                    {"name": "项目C", "age": "待开始"},
                                ]),
                                frame=(0, 0, 300, 120)
                            ),
                            # 下半部分：大纲视图
                            OutlineView(
                                columns=[
                                    {"title": "任务", "key": "title", "width": 200},
                                ],
                                root_items=[
                                    {
                                        "title": "开发任务",
                                        "children": [
                                            {"title": "UI设计"},
                                            {"title": "后端开发"},
                                            {"title": "测试"},
                                        ]
                                    }
                                ],
                                get_children=test_app.get_tree_children,
                                is_expandable=test_app.is_tree_expandable,
                                frame=(0, 0, 300, 120)
                            ),
                        ],
                        divider_style="thick",
                        frame=(0, 0, 400, 250)
                    ),
                ])
                
                return VStack(spacing=15, padding=20, children=[
                    Label("第三阶段布局组件测试", frame=(0, 0, 600, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # 主要内容：标签页视图
                    TabView(
                        tabs=[
                            {"title": "表格视图", "content": table_tab_content},
                            {"title": "大纲视图", "content": outline_tab_content},
                            {"title": "分割视图", "content": split_tab_content},
                            {"title": "组合演示", "content": combo_tab_content},
                        ],
                        selected=test_app.current_tab,
                        on_change=test_app.on_tab_change,
                        frame=(0, 0, 500, 400)
                    ),
                    
                    # 状态显示
                    VStack(spacing=3, children=[
                        Label(lambda: f"当前标签页: {test_app.current_tab.value}"),
                        Label(lambda: f"选中表格行: {test_app.selected_row.value}"),
                        Label(lambda: f"表格数据行数: {len(test_app.table_data.value)}"),
                    ]),
                ])
        
        return Stage3LayoutComponent()
    
    # 创建窗口
    window = app.create_window(
        title="Stage 3 Layout Components Test",
        size=(700, 600),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - TabView: 标签页视图")
    print("     * 多个标签页，支持切换")
    print("     * 双向数据绑定和事件处理")
    print("   - TableView: 表格视图")
    print("     * 多列表格，可选择行")
    print("     * 动态数据更新和CRUD操作")
    print("     * 双击事件支持")
    print("   - OutlineView: 大纲视图")
    print("     * 树形结构，可展开/收缩")
    print("     * 层级数据显示")
    print("   - SplitView: 分割视图")
    print("     * 水平/垂直分割")
    print("     * 可调整子视图大小")
    print("   - 组合布局演示")
    print("     * 多种组件组合使用")
    
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