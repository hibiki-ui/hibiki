# Hibiki UI

*Read this in other languages: [简体中文](README.zh-CN.md) | [日本語](README.ja.md)*

[![PyPI version](https://badge.fury.io/py/hibiki-ui.svg)](https://badge.fury.io/py/hibiki-ui)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, reactive UI framework for native macOS applications using Python and PyObjC. Hibiki UI combines signal-based reactivity with native macOS components, providing a clean and powerful API for creating responsive user interfaces.

## 🎯 Core Features

- **🔄 Signal-based Reactivity** - Fine-grained reactive updates with Signal, Computed, and Effect primitives
- **🍎 Native macOS Integration** - Direct PyObjC integration with native AppKit components
- **⚡ High Performance** - GPU-accelerated animations using Core Animation APIs only
- **🧩 Component Architecture** - Modern component-based development with lifecycle management
- **📐 Professional Layout System** - Flexbox-style layout engine with precise control
- **🎨 Complete UI Toolkit** - Full set of native macOS controls and widgets
- **🔧 Type Safe** - Complete type annotations with excellent IDE support

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv add hibiki-ui

# Using pip
pip install hibiki-ui
```

### Hello World Example

```python
from hibiki import Signal, Computed
from hibiki import Label, Button, Container, ComponentStyle, px
from hibiki import ManagerFactory

# Create reactive state
count = Signal(0)

# Create UI components with reactive bindings
button = Button(
    "Click me",
    style=ComponentStyle(width=px(120), height=px(32)),
    on_click=lambda: setattr(count, 'value', count.value + 1)
)

label = Label(
    Computed(lambda: f"Clicked {count.value} times"),
    style=ComponentStyle(height=px(25))
)

# Create layout container
app_ui = Container(
    children=[label, button],
    style=ComponentStyle(
        display="flex",
        flex_direction="column",
        gap=px(10),
        padding=px(20)
    )
)

# Create and run application
app_manager = ManagerFactory.get_app_manager()
window = app_manager.create_window("Hello Hibiki UI", 300, 150)
window.set_content(app_ui)
app_manager.run()
```

## 🏗️ Architecture

```
Your Application Code
       ↓
Component System (Label, Button, Container)
       ↓
Reactive System (Signal, Computed, Effect) ← CORE
       ↓
Binding Layer (ReactiveBinding, Event handling)
       ↓
AppKit/PyObjC (NSView, NSButton, etc.)
```

## 🔄 Reactive System

### Signals - Reactive State

```python
from hibiki import Signal, Effect

# Create mutable reactive state
user_name = Signal("Alice")
user_age = Signal(25)

# Signals automatically notify observers when changed
user_name.value = "Bob"  # Triggers all dependent computations and effects
```

### Computed - Derived Values

```python
from hibiki import Computed

# Computed values automatically recalculate when dependencies change
full_info = Computed(lambda: f"{user_name.value} is {user_age.value} years old")
is_adult = Computed(lambda: user_age.value >= 18)

print(full_info.value)  # "Bob is 25 years old"
```

### Effects - Side Effects

```python
# Effects run when their reactive dependencies change
def log_changes():
    print(f"User info updated: {full_info.value}")

effect = Effect(log_changes)  # Runs immediately and on each change
user_age.value = 30  # Triggers the effect
```

## 🧩 Component System

### Basic Components

```python
from hibiki import (
    Label, Button, TextField, Slider, Switch,
    ProgressBar, ImageView, Checkbox, RadioButton
)

# Text display with reactive content
status_label = Label(
    Computed(lambda: f"Status: {'Online' if connected.value else 'Offline'}"),
    style=ComponentStyle(color="green" if connected.value else "red")
)

# Interactive button with dynamic state
action_button = Button(
    title=Computed(lambda: "Disconnect" if connected.value else "Connect"),
    enabled=Computed(lambda: not is_loading.value),
    on_click=toggle_connection
)

# Two-way data binding with text input
username_field = TextField(
    value=username_signal,  # Automatic two-way binding
    placeholder="Enter username...",
    style=ComponentStyle(width=px(200))
)
```

### Layout Components

```python
from hibiki import Container

# Flexbox-style layouts
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
        flex=1,  # Takes remaining space
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

## 🎨 Advanced Features

### Form Handling

```python
from hibiki import Form, FormField, RequiredValidator, EmailValidator

# Create form with validation
contact_form = Form([
    FormField("name", TextField(), [RequiredValidator("Name is required")]),
    FormField("email", TextField(), [EmailValidator(), RequiredValidator()]),
    FormField("age", TextField(), [NumberValidator(min_value=0, max_value=120)])
])

# Handle form submission
def submit_form():
    if contact_form.is_valid():
        data = contact_form.get_data()
        print(f"Submitting: {data}")
    else:
        print("Form has errors:", contact_form.get_errors())
```

### Animations

```python
from hibiki import animate, fade_in, bounce

# Simple declarative animations
animate(my_button, duration=0.3, scale=1.1, opacity=0.9)

# Preset animation effects
fade_in(welcome_label, duration=1.0)
bounce(notification_view, scale=1.05)

# Reactive animations
effect = Effect(lambda: animate(
    status_indicator,
    opacity=1.0 if is_online.value else 0.3,
    duration=0.2
))
```

### Custom Components

```python
from hibiki import UIComponent

class CounterWidget(UIComponent):
    def __init__(self, initial_value=0):
        super().__init__()
        self.count = Signal(initial_value)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
    
    def _create_nsview(self):
        # Create container with label and buttons
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

# Usage
counter = CounterWidget(initial_value=10)
```

## 🎭 Complete Application Example

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
        # Computed values
        active_count = Computed(lambda: sum(1 for todo in self.todos.value if not todo["completed"]))
        filtered_todos = Computed(lambda: self._filter_todos())
        
        # UI components
        header = Container([
            Label("Todo App", style=ComponentStyle(font_size=px(24), font_weight="bold")),
            TextField(
                value=self.new_todo_text,
                placeholder="What needs to be done?",
                on_enter=self.add_todo
            ),
            Button("Add Todo", on_click=self.add_todo)
        ], style=ComponentStyle(gap=px(10)))
        
        # Dynamic todo list
        todo_list = Container([
            *[self._create_todo_item(todo) for todo in filtered_todos.value]
        ], style=ComponentStyle(gap=px(5)))
        
        footer = Container([
            Label(Computed(lambda: f"{active_count.value} items left")),
            Container([
                Button("All", on_click=lambda: setattr(self.filter_mode, 'value', "all")),
                Button("Active", on_click=lambda: setattr(self.filter_mode, 'value', "active")),
                Button("Completed", on_click=lambda: setattr(self.filter_mode, 'value', "completed"))
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
    
    # Create application
    app_manager = ManagerFactory.get_app_manager()
    window = app_manager.create_window("Hibiki UI Todo App", 500, 600)
    window.set_content(app.create_ui())
    
    app_manager.run()

if __name__ == "__main__":
    main()
```

## 📦 Development

### Project Setup

```bash
# Clone the repository
git clone https://github.com/hibiki-ui/hibiki-ui.git
cd hibiki-ui

# Set up development environment
uv sync --all-extras
uv run pre-commit install
```

### Development Commands

```bash
# Run the showcase demo
uv run python showcase.py

# Run tests
uv run pytest

# Code quality
uv run ruff check .
uv run ruff check --fix .
uv run black .
uv run isort .
uv run mypy hibiki

# Build package
uv build
```

## 🎯 Why Hibiki UI?

### vs. Other macOS GUI Frameworks

| Feature | Hibiki UI | Tkinter | PyQt/PySide | Kivy |
|---------|-----------|---------|-------------|------|
| Native macOS | ✅ Full AppKit | ❌ Emulated | ⚠️ Themed | ❌ Custom |
| Reactive Updates | ✅ Automatic | ❌ Manual | ❌ Signals/Slots | ❌ Manual |
| Performance | ✅ Native | ⚠️ Medium | ⚠️ Good | ✅ Good |
| macOS Integration | ✅ Complete | ❌ None | ⚠️ Limited | ❌ None |
| Learning Curve | ✅ Modern | ✅ Simple | ❌ Complex | ⚠️ Medium |
| Bundle Size | ✅ Small | ✅ Small | ❌ Large | ⚠️ Medium |
| Animation Support | ✅ GPU-accelerated | ❌ Limited | ⚠️ Basic | ✅ Good |

### Key Advantages

- **🍎 Native Performance**: Direct AppKit integration with zero abstraction overhead
- **🔄 Reactive by Design**: Automatic UI updates, no manual DOM manipulation required
- **🚀 Modern Developer Experience**: Type hints, IDE support, contemporary tooling
- **🎨 Professional Animations**: GPU-accelerated Core Animation integration
- **📱 Production Ready**: Proper memory management and lifecycle handling

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SolidJS** - Inspiration for the reactive system design
- **PyObjC** - The foundation that makes this possible  
- **AppKit** - The native macOS UI framework
- **Core Animation** - GPU-accelerated animation system

---

**Hibiki UI** - Bringing reactive, modern UI development to native macOS applications. 🍎✨