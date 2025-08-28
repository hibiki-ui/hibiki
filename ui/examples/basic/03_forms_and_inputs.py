#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 03: Forms and Inputs
表单和输入控件

学习目标：
✅ 使用TextField进行文本输入
✅ 使用Slider进行数值选择
✅ 使用Switch和Checkbox进行布尔选择
✅ 表单数据的响应式处理
"""

from hibiki.ui import (
    Signal,
    Computed,
    Label,
    Button,
    TextField,
    Slider,
    Switch,
    Checkbox,
    Container,
    ManagerFactory,
    ComponentStyle,
    Display,
    FlexDirection,
    JustifyContent,
    AlignItems,
    px,
)


def main():
    """表单和输入控件演示"""
    print("🚀 Starting Forms and Inputs Example...")

    # 1. 创建表单状态
    name = Signal("")
    age = Signal(25)
    volume = Signal(50)
    dark_mode = Signal(False)
    notifications = Signal(True)

    # 2. 创建计算属性
    form_summary = Computed(
        lambda: f"Name: {name.value or 'Not set'}\n"
        f"Age: {age.value}\n"
        f"Volume: {int(volume.value)}%\n"
        f"Dark Mode: {'On' if dark_mode.value else 'Off'}\n"
        f"Notifications: {'Enabled' if notifications.value else 'Disabled'}"
    )

    # 3. 创建UI组件

    # 标题
    title = Label(
        "📝 Form Controls Demo",
        style=ComponentStyle(
            margin_bottom=px(30)
        ),
        # 文本属性
        font_size=24,
        font_weight="bold",
        text_align="center",
        color="#2c3e50"
    )

    # 文本输入
    name_field = TextField(
        name,
        placeholder="Enter your name...",
        style=ComponentStyle(width=px(300), height=px(32), margin_bottom=px(5)),
    )

    name_label = Label(
        "Your Name:",
        style=ComponentStyle(margin_bottom=px(5)),
        font_size=14,
        font_weight="bold"
    )

    # 年龄滑动条
    age_label = Label(
        lambda: f"Age: {int(age.value)}",
        style=ComponentStyle(margin_bottom=px(5)),
        font_size=14,
        font_weight="bold"
    )

    age_slider = Slider(
        age, min_value=0, max_value=100, style=ComponentStyle(width=px(300), margin_bottom=px(15))
    )

    # 音量滑动条
    volume_label = Label(
        lambda: f"Volume: {int(volume.value)}%",
        style=ComponentStyle(margin_bottom=px(5)),
        font_size=14,
        font_weight="bold"
    )

    volume_slider = Slider(
        volume,
        min_value=0,
        max_value=100,
        style=ComponentStyle(width=px(300), margin_bottom=px(15)),
    )

    # 开关和复选框
    dark_mode_switch = Switch(
        dark_mode, label="Dark Mode", style=ComponentStyle(margin_bottom=px(10))
    )

    notifications_checkbox = Checkbox(
        notifications, label="Enable Notifications", style=ComponentStyle(margin_bottom=px(20))
    )

    # 表单摘要显示
    summary_label = Label(
        form_summary,
        style=ComponentStyle(
            padding=px(15),
            width=px(300)
        ),
        # 文本属性 - 使用等宽字体显示数据
        font_size=12,
        font_family="monospace",
        color="#333"
    )

    # 重置按钮
    reset_btn = Button(
        "Reset Form",
        style=ComponentStyle(width=px(120), height=px(35), margin_top=px(15)),
        on_click=lambda: [
            setattr(name, "value", ""),
            setattr(age, "value", 25),
            setattr(volume, "value", 50),
            setattr(dark_mode, "value", False),
            setattr(notifications, "value", True),
        ],
    )

    # 主容器
    main_container = Container(
        children=[
            title,
            name_label,
            name_field,
            Container(children=[], style=ComponentStyle(height=px(10))),  # 间距
            age_label,
            age_slider,
            volume_label,
            volume_slider,
            dark_mode_switch,
            notifications_checkbox,
            Label(
                "Form Summary:",
                style=ComponentStyle(margin_bottom=px(10)),
                font_size=16,
                font_weight="bold"
            ),
            summary_label,
            Container(
                children=[reset_btn], style=ComponentStyle(display=Display.FLEX, justify_content=JustifyContent.CENTER)
            ),
        ],
        style=ComponentStyle(
            padding=px(40), display=Display.FLEX, flex_direction=FlexDirection.COLUMN, align_items=AlignItems.CENTER
        ),
    )

    # 4. 创建应用
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window(title="Forms and Inputs - Hibiki UI", width=600, height=700)

    window.set_content(main_container)

    print("✅ Forms and Inputs app ready!")
    print("🎯 Try changing the form values to see live updates!")
    print("📚 Next: Try advanced examples in the 'advanced' directory")

    app_manager.run()


if __name__ == "__main__":
    main()
