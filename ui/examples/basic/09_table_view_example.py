#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 09: TableView Example
TableView表格组件使用示例

学习目标：
✅ 理解TableView组件的基本用法
✅ 学习列定义和数据绑定
✅ 掌握响应式数据更新
✅ 了解用户交互事件处理
✅ 体验表格数据的增删改查
"""

from hibiki.ui import (
    Label, Button, TextField, Container, TableView, TableColumn,
    ManagerFactory, ComponentStyle, Signal,
    Display, FlexDirection, JustifyContent, AlignItems, px, percent
)


def main():
    """创建TableView示例应用"""
    print("🚀 Starting TableView Example...")

    # 1. 获取应用管理器
    app_manager = ManagerFactory.get_app_manager()

    # 2. 创建窗口
    window = app_manager.create_window(title="TableView Example - Hibiki UI", width=800, height=600)

    # 3. 准备示例数据
    initial_data = [
        {"name": "张三", "age": 25, "city": "北京", "salary": "8000"},
        {"name": "李四", "age": 30, "city": "上海", "salary": "12000"},
        {"name": "王五", "age": 28, "city": "深圳", "salary": "15000"},
        {"name": "赵六", "age": 35, "city": "广州", "salary": "13000"},
        {"name": "钱七", "age": 26, "city": "杭州", "salary": "11000"},
    ]

    # 4. 创建响应式数据
    table_data = Signal(initial_data)
    selected_info = Signal("未选择任何行")
    new_name = Signal("")
    new_age = Signal("")
    new_city = Signal("")
    new_salary = Signal("")

    # 5. 定义表格列
    columns = [
        TableColumn(
            identifier="name",
            title="姓名",
            width=120,
            min_width=80,
            max_width=200,
            resizable=True,
            editable=True
        ),
        TableColumn(
            identifier="age",
            title="年龄",
            width=80,
            min_width=60,
            max_width=120,
            resizable=True,
            editable=True
        ),
        TableColumn(
            identifier="city",
            title="城市",
            width=100,
            min_width=80,
            max_width=150,
            resizable=True,
            editable=True
        ),
        TableColumn(
            identifier="salary",
            title="薪资",
            width=120,
            min_width=80,
            max_width=180,
            resizable=True,
            editable=True
        ),
    ]

    # 6. 事件处理函数
    def on_selection_change(row):
        """选择变化处理"""
        if row >= 0 and row < len(table_data.value):
            person = table_data.value[row]
            selected_info.value = f"选中: {person['name']}, {person['age']}岁, {person['city']}, 薪资{person['salary']}元"
        else:
            selected_info.value = "未选择任何行"

    def on_double_click(row):
        """双击处理"""
        if row >= 0 and row < len(table_data.value):
            person = table_data.value[row]
            print(f"🖱️ 双击了: {person['name']}")
            selected_info.value = f"双击了: {person['name']} 的记录"

    def on_data_change(row, column_id, new_value):
        """数据变化处理"""
        print(f"📝 数据修改: 第{row}行, 列'{column_id}' -> '{new_value}'")

    def add_person():
        """添加新人员"""
        if new_name.value and new_age.value and new_city.value and new_salary.value:
            new_person = {
                "name": new_name.value,
                "age": int(new_age.value) if new_age.value.isdigit() else 0,
                "city": new_city.value,
                "salary": new_salary.value
            }

            # 更新响应式数据
            current_data = list(table_data.value)
            current_data.append(new_person)
            table_data.value = current_data

            # 清空输入框
            new_name.value = ""
            new_age.value = ""
            new_city.value = ""
            new_salary.value = ""

            selected_info.value = f"已添加: {new_person['name']}"

    def delete_selected():
        """删除选中行"""
        # 这里需要从TableView获取选中行，暂时用索引0示例
        if len(table_data.value) > 0:
            current_data = list(table_data.value)
            removed = current_data.pop(0)  # 删除第一行作为示例
            table_data.value = current_data
            selected_info.value = f"已删除: {removed['name']}"

    def clear_all():
        """清空所有数据"""
        table_data.value = []
        selected_info.value = "已清空所有数据"

    def reset_data():
        """重置为初始数据"""
        table_data.value = list(initial_data)
        selected_info.value = "已重置为初始数据"

    # 7. 创建TableView
    table_view = TableView(
        data=table_data,
        columns=columns,
        editable=True,  # 允许单元格编辑
        allows_multiple_selection=False,  # 单选模式
        on_selection_change=on_selection_change,
        on_double_click=on_double_click,
        on_data_change=on_data_change,
        style=ComponentStyle(
            width=percent(100),
            height=px(300)
        )
    )

    # 8. 创建信息显示标签
    info_label = Label(
        selected_info,
        style=ComponentStyle(
            width=percent(100),
            height=px(30),
            padding=px(10)
        ),
        font_size=14,
        color="#666"
    )

    # 9. 创建输入表单
    input_container = Container(
        children=[
            # 表单标题
            Label(
                "添加新人员:",
                font_size=16,
                font_weight="bold",
                color="#333",
                style=ComponentStyle(margin_bottom=px(10))
            ),

            # 输入字段行
            Container(
                children=[
                    TextField(
                        value=new_name,
                        placeholder="姓名",
                        style=ComponentStyle(width=px(120), margin_right=px(10))
                    ),
                    TextField(
                        value=new_age,
                        placeholder="年龄",
                        style=ComponentStyle(width=px(80), margin_right=px(10))
                    ),
                    TextField(
                        value=new_city,
                        placeholder="城市",
                        style=ComponentStyle(width=px(100), margin_right=px(10))
                    ),
                    TextField(
                        value=new_salary,
                        placeholder="薪资",
                        style=ComponentStyle(width=px(120), margin_right=px(10))
                    ),
                    Button(
                        "添加",
                        on_click=add_person,
                        style=ComponentStyle(
                            background_color="#4CAF50",
                            padding=px(8)
                        )
                    ),
                ],
                style=ComponentStyle(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    align_items=AlignItems.CENTER,
                    margin_bottom=px(10)
                )
            )
        ],
        style=ComponentStyle(
            padding=px(15),
            background_color="#f8f9fa",
            border_radius=px(8)
        )
    )

    # 10. 创建操作按钮组
    button_container = Container(
        children=[
            Button(
                "删除首行",
                on_click=delete_selected,
                style=ComponentStyle(
                    background_color="#f44336",
                    margin_right=px(10),
                    padding=px(8)
                )
            ),
            Button(
                "清空所有",
                on_click=clear_all,
                style=ComponentStyle(
                    background_color="#ff9800",
                    margin_right=px(10),
                    padding=px(8)
                )
            ),
            Button(
                "重置数据",
                on_click=reset_data,
                style=ComponentStyle(
                    background_color="#2196F3",
                    padding=px(8)
                )
            ),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            margin_top=px(10)
        )
    )

    # 11. 创建主容器
    main_container = Container(
        children=[
            # 标题
            Label(
                "📊 TableView 表格组件示例",
                font_size=24,
                font_weight="bold",
                text_align="center",
                color="#333",
                style=ComponentStyle(
                    width=percent(100),
                    margin_bottom=px(20)
                )
            ),

            # 说明文字
            Label(
                "✨ 功能演示: 响应式数据绑定、行选择、双击事件、单元格编辑、数据增删",
                font_size=14,
                text_align="center",
                color="#666",
                style=ComponentStyle(
                    width=percent(100),
                    margin_bottom=px(20)
                )
            ),

            # 表格视图
            table_view,

            # 选择信息
            info_label,

            # 输入表单
            input_container,

            # 操作按钮
            button_container,

            # 帮助文字
            Label(
                "💡 提示: 双击表格行可触发事件，直接点击单元格可进行编辑",
                font_size=12,
                text_align="center",
                color="#999",
                style=ComponentStyle(
                    width=percent(100),
                    margin_top=px(20)
                )
            )
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            padding=px(20),
            width=percent(100),
            height=percent(100)
        )
    )

    # 12. 设置窗口内容
    window.set_content(main_container)

    print("✅ TableView example ready!")
    print("📚 Features demonstrated:")
    print("   🔸 Reactive data binding with Signal")
    print("   🔸 Column definitions and customization")
    print("   🔸 Row selection and double-click events")
    print("   🔸 Editable cells and data change callbacks")
    print("   🔸 Dynamic data manipulation (add/delete/reset)")
    print("   🔸 Responsive layout integration")

    print("\n🎯 Try these interactions:")
    print("   • Click on table rows to see selection")
    print("   • Double-click rows to trigger events")
    print("   • Edit cells directly by clicking")
    print("   • Add new people using the form")
    print("   • Use buttons to manipulate data")

    # 13. 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()
