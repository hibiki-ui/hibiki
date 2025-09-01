#!/usr/bin/env python3
"""
🎨 Hibiki UI Rich Text Demo
展示新的富文本支持功能

学习目标：
✅ 理解富文本构建器的使用
✅ 体验各种文本样式（粗体、斜体、下划线、颜色）
✅ 学习富文本在Label和TextField中的应用
✅ 掌握类Markdown语法的使用
"""

from hibiki.ui import (
    Label, TextField, Container, ManagerFactory,
    ComponentStyle, Display, FlexDirection, AlignItems,
    px, percent,
    # 富文本相关导入
    RichText, TextAttributes, TextStyle, UnderlineStyle,
    rich_text, attributed_string, markdown_text
)


def main():
    """创建富文本演示应用"""
    print("🎨 Starting Rich Text Demo...")

    # 1. 获取应用管理器
    app_manager = ManagerFactory.get_app_manager()

    # 2. 创建窗口
    window = app_manager.create_window(
        title="Hibiki UI - 富文本功能演示",
        width=800,
        height=900
    )

    # 3. 创建各种富文本示例

    # 3.1 标题
    title = Label(
        "🎨 Hibiki UI 富文本功能演示",
        style=ComponentStyle(
            width=percent(100),
            height=px(50),
            padding=px(10)
        ),
        font_size=22,
        font_weight="bold",
        text_align="center",
        color="#2c3e50"
    )

    # 3.2 简单富文本示例
    simple_rich_text = rich_text().add_text("欢迎使用 ").add_bold_text("粗体文字", color="#e74c3c").add_text(" 和 ").add_italic_text("斜体文字", color="#3498db").add_text("！").build()

    rich_label_1 = Label(
        simple_rich_text,
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        ),
        font_size=16
    )

    # 3.3 复杂富文本示例
    complex_rich_text = (
        rich_text()
        .add_text("这是")
        .add_colored_text("彩色文字", "#9b59b6")
        .add_text("，这是")
        .add_underlined_text("下划线文字", color="#e67e22")
        .add_text("，这是")
        .add_highlighted_text("高亮文字", "#fff3cd", foreground_color="#856404")
        .add_text("。")
        .build()
    )

    rich_label_2 = Label(
        complex_rich_text,
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        ),
        font_size=16
    )

    # 3.4 使用TextAttributes的高级示例
    advanced_attrs = TextAttributes(
        font_size=18,
        text_style=TextStyle.BOLD,
        foreground_color="#2980b9",
        underline_style=UnderlineStyle.THICK,
        underline_color="#e74c3c",
        kern=2.0  # 字符间距
    )

    advanced_rich_text = (
        rich_text()
        .add_text("高级样式：", advanced_attrs)
        .add_text(" 带字符间距和粗下划线的文字")
        .build()
    )

    rich_label_3 = Label(
        advanced_rich_text,
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        )
    )

    # 3.5 类Markdown语法示例
    markdown_text_content = "这是 **粗体** 和 *斜体* 的组合演示！"
    markdown_attributed_string = markdown_text(markdown_text_content)

    markdown_label = Label(
        markdown_attributed_string,
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        ),
        font_size=16
    )

    # 3.6 便捷函数示例
    simple_attributed = attributed_string(
        "便捷函数创建的富文本",
        font_size=17,
        color="#27ae60",
        bold=True,
        underlined=True
    )

    simple_label = Label(
        simple_attributed,
        style=ComponentStyle(
            width=percent(90),
            height=px(40),
            margin=px(10)
        )
    )

    # 4. TextField富文本支持示例

    # 4.1 富文本占位符
    placeholder_rich_text = (
        rich_text()
        .add_text("请输入")
        .add_italic_text("富文本", color="#95a5a6")
        .add_text("内容...")
        .build()
    )

    rich_textfield = TextField(
        text="",
        attributed_placeholder=placeholder_rich_text,
        style=ComponentStyle(
            width=px(400),
            height=px(35),
            margin=px(10)
        ),
        font_size=14
    )

    # 4.2 预设富文本内容的TextField
    preset_rich_text = (
        rich_text()
        .add_bold_text("粗体开头", color="#e74c3c")
        .add_text(" 然后是普通文字 ")
        .add_italic_text("斜体结尾", color="#3498db")
        .build()
    )

    preset_textfield = TextField(
        text=preset_rich_text,
        style=ComponentStyle(
            width=px(400),
            height=px(35),
            margin=px(10)
        ),
        font_size=14
    )

    # 5. 使用说明
    instruction_text = (
        rich_text()
        .add_bold_text("使用说明：", foreground_color="#2c3e50", font_size=16)
        .add_text("\n• 使用", TextAttributes(font_size=14))
        .add_colored_text(" rich_text() ", "#e67e22")
        .add_text("创建构建器", TextAttributes(font_size=14))
        .add_text("\n• 使用", TextAttributes(font_size=14))
        .add_colored_text(" attributed_string() ", "#e67e22")
        .add_text("快速创建简单富文本", TextAttributes(font_size=14))
        .add_text("\n• 使用", TextAttributes(font_size=14))
        .add_colored_text(" markdown_text() ", "#e67e22")
        .add_text("解析类Markdown语法", TextAttributes(font_size=14))
        .add_text("\n• 支持粗体、斜体、下划线、颜色、高亮等", TextAttributes(font_size=14))
        .build()
    )

    instruction_label = Label(
        instruction_text,
        style=ComponentStyle(
            width=percent(90),
            height=px(120),
            margin=px(10),
            padding=px(15),
            background_color="#f8f9fa"
        ),
        bordered=True,
        background_color="#f8f9fa"
    )

    # 6. 创建主容器
    main_container = Container(
        children=[
            title,
            Label(
                "1. 基础富文本示例：",
                font_size=14,
                font_weight="bold",
                color="#34495e",
                style=ComponentStyle(
                    width=percent(90),
                    height=px(30),
                    margin_top=px(20),
                    margin_left=px(10)
                )
            ),
            rich_label_1,
            rich_label_2,
            rich_label_3,

            Label(
                "2. 类Markdown语法：",
                font_size=14,
                font_weight="bold",
                color="#34495e",
                style=ComponentStyle(
                    width=percent(90),
                    height=px(30),
                    margin_top=px(10),
                    margin_left=px(10)
                )
            ),
            markdown_label,

            Label(
                "3. 便捷函数示例：",
                font_size=14,
                font_weight="bold",
                color="#34495e",
                style=ComponentStyle(
                    width=percent(90),
                    height=px(30),
                    margin_top=px(10),
                    margin_left=px(10)
                )
            ),
            simple_label,

            Label(
                "4. TextField富文本支持：",
                font_size=14,
                font_weight="bold",
                color="#34495e",
                style=ComponentStyle(
                    width=percent(90),
                    height=px(30),
                    margin_top=px(10),
                    margin_left=px(10)
                )
            ),
            rich_textfield,
            preset_textfield,

            instruction_label
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            width=percent(100),
            height=percent(100),
            padding=px(20),
            background_color="#ffffff"
        )
    )

    # 7. 设置窗口内容
    window.set_content(main_container)

    print("✅ Rich Text Demo ready!")
    print("🎨 演示功能:")
    print("   • 富文本构建器 (RichTextBuilder)")
    print("   • 文本属性配置 (TextAttributes)")
    print("   • 类Markdown语法解析")
    print("   • 便捷创建函数")
    print("   • Label和TextField富文本支持")

    # 8. 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()