# Hibiki UI

*其他语言版本: [English](README.md) | [日本語](README.ja.md)*

[![PyPI version](https://badge.fury.io/py/hibiki-ui.svg)](https://badge.fury.io/py/hibiki-ui)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个现代化的响应式 UI 框架，专为使用 Python 和 PyObjC 开发原生 macOS 应用程序而设计。Hibiki UI 将基于信号的响应式系统与原生 macOS 组件结合，提供简洁强大的 API 来创建响应式用户界面。

## 🎯 核心特性

- **🔄 基于信号的响应式系统** - 使用 Signal、Computed 和 Effect 原语实现细粒度响应式更新
- **🍎 原生 macOS 集成** - 直接与 AppKit 组件进行 PyObjC 集成
- **⚡ 高性能** - 仅使用 Core Animation APIs 的 GPU 加速动画
- **🧩 组件化架构** - 现代化的基于组件的开发，具有生命周期管理
- **📐 专业级布局系统** - 类似 Flexbox 的布局引擎，提供精确控制
- **🎨 完整的 UI 工具包** - 全套原生 macOS 控件和组件
- **🔧 类型安全** - 完整的类型注解，优秀的 IDE 支持

## 🚀 快速开始

### 安装

```bash
# 使用 uv（推荐）
uv add hibiki-ui

# 使用 pip
pip install hibiki-ui
```

### Hello World 示例

```python
from hibiki import Signal, Computed
from hibiki import Label, Button, Container, ComponentStyle, px
from hibiki import ManagerFactory

# 创建响应式状态
count = Signal(0)

# 创建具有响应式绑定的 UI 组件
button = Button(
    "点击我",
    style=ComponentStyle(width=px(120), height=px(32)),
    on_click=lambda: setattr(count, 'value', count.value + 1)
)

label = Label(
    Computed(lambda: f"点击了 {count.value} 次"),
    style=ComponentStyle(height=px(25))
)

# 创建布局容器
app_ui = Container(
    children=[label, button],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        gap=px(10),
        padding=px(20)
    )
)

# 创建并运行应用程序
app_manager = ManagerFactory.get_app_manager()
window = app_manager.create_window("Hello Hibiki UI", 300, 150)
window.set_content(app_ui)
app_manager.run()
```

## 🏗️ 架构

```
您的应用程序代码
       ↓
组件系统（Label、Button、Container）
       ↓
响应式系统（Signal、Computed、Effect）← 核心
       ↓
绑定层（ReactiveBinding、事件处理）
       ↓
AppKit/PyObjC（NSView、NSButton 等）
```

## 🔄 响应式系统

### Signals - 响应式状态

```python
from hibiki import Signal, Effect

# 创建可变的响应式状态
user_name = Signal("小明")
user_age = Signal(25)

# Signals 在更改时自动通知观察者
user_name.value = "小李"  # 触发所有相关计算和副作用
```

### Computed - 派生值

```python
from hibiki import Computed

# Computed 值在依赖项更改时自动重新计算
full_info = Computed(lambda: f"{user_name.value} 今年 {user_age.value} 岁")
is_adult = Computed(lambda: user_age.value >= 18)

print(full_info.value)  # "小李 今年 25 岁"
```

### Effects - 副作用

```python
# Effects 在其响应式依赖项更改时运行
def log_changes():
    print(f"用户信息更新: {full_info.value}")

effect = Effect(log_changes)  # 立即运行并在每次更改时运行
user_age.value = 30  # 触发副作用
```

## 🧩 组件系统

### 基础组件

```python
from hibiki import (
    Label, Button, TextField, Slider, Switch,
    ProgressBar, ImageView, Checkbox, RadioButton
)

# 具有响应式内容的文本显示
status_label = Label(
    Computed(lambda: f"状态: {'在线' if connected.value else '离线'}"),
    style=ComponentStyle(color="green" if connected.value else "red")
)

# 具有动态状态的交互式按钮
action_button = Button(
    title=Computed(lambda: "断开连接" if connected.value else "连接"),
    enabled=Computed(lambda: not is_loading.value),
    on_click=toggle_connection
)

# 与文本输入的双向数据绑定
username_field = TextField(
    value=username_signal,  # 自动双向绑定
    placeholder="请输入用户名...",
    style=ComponentStyle(width=px(200))
)
```

### 布局组件

```python
from hibiki import Container

# 类 Flexbox 布局
header = Container(
    children=[logo, title, menu_button],
    style=ComponentStyle(
        display="flex",
        flex_direction="row",
        justify_content="space-between",
        align_items="center",
        padding=px(15)
    )
)

sidebar = Container(
    children=[nav_menu, user_profile],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        width=px(250),
        background_color="lightgray"
    )
)

main_content = Container(
    children=[content_area],
    style=ComponentStyle(
        flex=1,  # 占据剩余空间
        padding=px(20)
    )
)

app_layout = Container(
    children=[header, Container(children=[sidebar, main_content])],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        height=px(600)
    )
)
```

## 🎨 高级特性

### 表单处理

```python
from hibiki import Form, FormField, RequiredValidator, EmailValidator

# 创建带验证的表单
contact_form = Form([
    FormField("name", TextField(), [RequiredValidator("姓名为必填项")]),
    FormField("email", TextField(), [EmailValidator(), RequiredValidator()]),
    FormField("age", TextField(), [NumberValidator(min_value=0, max_value=120)])
])

# 处理表单提交
def submit_form():
    if contact_form.is_valid():
        data = contact_form.get_data()
        print(f"提交数据: {data}")
    else:
        print("表单有错误:", contact_form.get_errors())
```

### 动画

```python
from hibiki import animate, fade_in, bounce

# 简单的声明式动画
animate(my_button, duration=0.3, scale=1.1, opacity=0.9)

# 预设动画效果
fade_in(welcome_label, duration=1.0)
bounce(notification_view, scale=1.05)

# 响应式动画
effect = Effect(lambda: animate(
    status_indicator,
    opacity=1.0 if is_online.value else 0.3,
    duration=0.2
))
```

### 自定义组件

```python
from hibiki import UIComponent

class CounterWidget(UIComponent):
    def __init__(self, initial_value=0):
        super().__init__()
        self.count = Signal(initial_value)
        self.count_text = Computed(lambda: f"计数: {self.count.value}")
    
    def _create_nsview(self):
        # 创建包含标签和按钮的容器
        container = Container(
            children=[
                Button("-", on_click=lambda: setattr(self.count, 'value', self.count.value - 1)),
                Label(self.count_text, style=ComponentStyle(min_width=px(60))),
                Button("+", on_click=lambda: setattr(self.count, 'value', self.count.value + 1))
            ],
            style=ComponentStyle(
                display="flex",
                flex_direction="row",
                gap=px(5),
                align_items="center"
            )
        )
        return container.mount()

# 使用方式
counter = CounterWidget(initial_value=10)
```

## 🎭 完整应用示例

```python
from hibiki import *

class TodoApp:
    def __init__(self):
        self.todos = Signal([])
        self.new_todo_text = Signal("")
        self.filter_mode = Signal("all")  # "all", "active", "completed"
    
    def add_todo(self):
        text = self.new_todo_text.value.strip()
        if text:
            new_todo = {"id": len(self.todos.value), "text": text, "completed": False}
            self.todos.value = [*self.todos.value, new_todo]
            self.new_todo_text.value = ""
    
    def toggle_todo(self, todo_id):
        todos = self.todos.value
        updated_todos = []
        for todo in todos:
            if todo["id"] == todo_id:
                updated_todos.append({**todo, "completed": not todo["completed"]})
            else:
                updated_todos.append(todo)
        self.todos.value = updated_todos
    
    def create_ui(self):
        # 计算值
        active_count = Computed(lambda: sum(1 for todo in self.todos.value if not todo["completed"]))
        filtered_todos = Computed(lambda: self._filter_todos())
        
        # UI 组件
        header = Container([
            Label("待办事项应用", style=ComponentStyle(font_size=px(24), font_weight="bold")),
            TextField(
                value=self.new_todo_text,
                placeholder="需要做什么？",
                on_enter=self.add_todo
            ),
            Button("添加待办", on_click=self.add_todo)
        ], style=ComponentStyle(gap=px(10)))
        
        # 动态待办列表
        todo_list = Container([
            *[self._create_todo_item(todo) for todo in filtered_todos.value]
        ], style=ComponentStyle(gap=px(5)))
        
        footer = Container([
            Label(Computed(lambda: f"剩余 {active_count.value} 项")),
            Container([
                Button("全部", on_click=lambda: setattr(self.filter_mode, 'value', "all")),
                Button("进行中", on_click=lambda: setattr(self.filter_mode, 'value', "active")),
                Button("已完成", on_click=lambda: setattr(self.filter_mode, 'value', "completed"))
            ], style=ComponentStyle(display="flex", flex_direction="row", gap=px(5)))
        ], style=ComponentStyle(display="flex", justify_content="space-between"))
        
        return Container([header, todo_list, footer], style=ComponentStyle(
            padding=px(20),
            gap=px(15),
            min_height=px(400)
        ))
    
    def _filter_todos(self):
        todos = self.todos.value
        if self.filter_mode.value == "active":
            return [todo for todo in todos if not todo["completed"]]
        elif self.filter_mode.value == "completed":
            return [todo for todo in todos if todo["completed"]]
        return todos
    
    def _create_todo_item(self, todo):
        return Container([
            Checkbox(
                checked=Signal(todo["completed"]),
                on_change=lambda checked: self.toggle_todo(todo["id"])
            ),
            Label(todo["text"], style=ComponentStyle(
                text_decoration="line-through" if todo["completed"] else "none"
            ))
        ], style=ComponentStyle(display="flex", flex_direction="row", gap=px(10)))

def main():
    app = TodoApp()
    
    # 创建应用程序
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window("Hibiki UI 待办应用", 500, 600)
    window.set_content(app.create_ui())
    
    app_manager.run()

if __name__ == "__main__":
    main()
```

## 📦 开发

### 项目设置

```bash
# 克隆仓库
git clone https://github.com/hibiki-ui/hibiki-ui.git
cd hibiki-ui

# 设置开发环境
uv sync --all-extras
uv run pre-commit install
```

### 开发命令

```bash
# 运行展示演示
uv run python showcase.py

# 运行测试
uv run pytest

# 代码质量
uv run ruff check .
uv run ruff check --fix .
uv run black .
uv run isort .
uv run mypy hibiki

# 构建包
uv build
```

## 🎯 为什么选择 Hibiki UI？

### 与其他 macOS GUI 框架对比

| 特性 | Hibiki UI | Tkinter | PyQt/PySide | Kivy |
|------|-----------|---------|-------------|------|
| 原生 macOS | ✅ 完全 AppKit | ❌ 模拟 | ⚠️ 主题化 | ❌ 自定义 |
| 响应式更新 | ✅ 自动 | ❌ 手动 | ❌ 信号/槽 | ❌ 手动 |
| 性能 | ✅ 原生 | ⚠️ 中等 | ⚠️ 良好 | ✅ 良好 |
| macOS 集成 | ✅ 完整 | ❌ 无 | ⚠️ 有限 | ❌ 无 |
| 学习曲线 | ✅ 现代 | ✅ 简单 | ❌ 复杂 | ⚠️ 中等 |
| 包大小 | ✅ 小 | ✅ 小 | ❌ 大 | ⚠️ 中等 |
| 动画支持 | ✅ GPU 加速 | ❌ 有限 | ⚠️ 基础 | ✅ 良好 |

### 主要优势

- **🍎 原生性能**：直接 AppKit 集成，零抽象开销
- **🔄 响应式设计**：自动 UI 更新，无需手动 DOM 操作
- **🚀 现代开发体验**：类型提示、IDE 支持、现代工具链
- **🎨 专业动画**：GPU 加速的 Core Animation 集成
- **📱 生产就绪**：完善的内存管理和生命周期处理

## 📄 许可证

MIT 许可证 - 请参阅 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- **SolidJS** - 响应式系统设计的灵感来源
- **PyObjC** - 让这一切成为可能的基础
- **AppKit** - 原生 macOS UI 框架
- **Core Animation** - GPU 加速动画系统

---

**Hibiki UI** - 为原生 macOS 应用程序带来响应式、现代化的 UI 开发体验。🍎✨