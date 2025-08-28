#!/usr/bin/env python3
"""
🌟 Hibiki UI Tutorial 01: Hello World
最简单的Hibiki UI应用程序

学习目标：
✅ 理解基本的应用程序结构
✅ 创建简单的Label组件
✅ 使用ManagerFactory启动应用
"""

from hibiki import Label, ManagerFactory, ComponentStyle, px


def main():
    """创建最简单的Hello World应用"""
    print("🚀 Starting Hello World Example...")

    # 1. 获取应用管理器
    app_manager = ManagerFactory.get_app_manager()

    # 2. 创建窗口
    window = app_manager.create_window(title="Hello Hibiki UI", width=400, height=200)

    # 3. 创建Label组件 - 使用正确的文本属性API
    hello_label = Label(
        "Hello, Hibiki UI! 🎉",
        style=ComponentStyle(width=px(350), height=px(60), padding=px(20)),
        # 文本属性使用便捷参数
        font_size=24,
        font_weight="bold",
        text_align="center",
        color="#333",
    )

    # 4. 设置窗口内容
    window.set_content(hello_label)

    print("✅ Hello World app ready!")
    print("📚 Next: Try 02_reactive_basics.py to learn about reactive state")

    # 5. 运行应用
    app_manager.run()


if __name__ == "__main__":
    main()
