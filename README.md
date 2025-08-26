# macUI v2

[![PyPI version](https://badge.fury.io/py/macui.svg)](https://badge.fury.io/py/macui)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, reactive UI framework for native macOS apps using Python and PyObjC. Inspired by SolidJS, macUI v2 provides signal-based reactivity with fine-grained updates, directly manipulating native Cocoa views without a virtual DOM.

## 🚀 Quick Start

### Installation with uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project
uv init my-macui-app
cd my-macui-app

# Add macui as dependency
uv add macui

# Create your first app
cat > main.py << 'EOF'
from macui import MacUIApp, Signal, Computed
from macui.components import Button, Label, VStack

class CounterApp:
    def __init__(self):
        self.count = Signal(0)
        self.count_text = Computed(lambda: f"Count: {self.count.value}")
    
    def increment(self):
        self.count.value += 1
    
    def create_ui(self):
        return VStack(children=[
            Label(self.count_text),
            Button("Click me!", on_click=self.increment)
        ])

def main():
    app = MacUIApp("Counter Demo")
    counter = CounterApp()
    window = app.create_window("My First macUI App", content=counter.create_ui())
    window.show()
    app.run()

if __name__ == "__main__":
    main()
EOF

# Run your app
uv run main.py
```

### Traditional Installation

```bash
pip install macui
```

### Using CLI Tools

```bash
# Create a new project from template
uv run macui create my-app

# Show system information
uv run macui info

# Run examples
uv run macui examples
```

## ✨ Key Features

- 🎯 **Signal-based Reactivity** - Fine-grained reactive updates inspired by SolidJS
- ⚡ **No Virtual DOM** - Direct manipulation of native NSViews for maximum performance  
- 🍎 **Native macOS** - Full access to AppKit and macOS-specific features
- 🔓 **Zero Abstractions** - Direct PyObjC integration without limitations
- 🧩 **Component Architecture** - Modern component-based development
- 🔧 **Type Safe** - Complete type annotations with excellent IDE support
- 📱 **Production Ready** - Proper lifecycle management and memory handling

## 🏗️ Architecture

```
macui/
├── core/                 # Core reactive system
│   ├── signal.py        # Signal, Computed, Effect primitives  
│   ├── component.py     # Component base class and lifecycle
│   └── binding.py       # Reactive view bindings
├── components/          # UI components
│   ├── controls.py      # Button, TextField, Label, etc.
│   └── layout.py        # VStack, HStack, ZStack, ScrollView
├── app.py              # Application and window management
└── cli.py              # Command-line tools
```

## 🎨 Reactive System

### Signals - Reactive State

```python
from macui import Signal, Computed, Effect

# Create reactive state
count = Signal(0)
name = Signal("World")

# Signals automatically notify dependents when changed
count.value = 5  # Triggers reactive updates
```

### Computed - Derived Values

```python
# Computed values automatically update when dependencies change
double_count = Computed(lambda: count.value * 2)
greeting = Computed(lambda: f"Hello, {name.value}!")

print(double_count.value)  # 10 (automatically computed from count)
```

### Effects - Side Effects

```python
# Effects run automatically when their dependencies change
def log_count():
    print(f"Count changed to: {count.value}")

effect = Effect(log_count)  # Runs immediately and on each count change
count.value = 10  # Triggers the effect -> prints "Count changed to: 10"
```

## 🧩 Component System

### Basic Component

```python
from macui import Component, Signal, Computed
from macui.components import VStack, Label, Button

class CounterComponent(Component):
    def __init__(self):
        super().__init__()
        self.count = self.create_signal(0)  # Component-managed signal
        self.count_text = self.create_computed(lambda: f"Count: {self.count.value}")
    
    def increment(self):
        self.count.value += 1
    
    def mount(self):
        return VStack(children=[
            Label(self.count_text),  # Automatically updates
            Button("Increment", on_click=self.increment)
        ])
```

### Reactive UI Components

```python
from macui.components import Button, Label, TextField, VStack, HStack

# Reactive button with dynamic title
button = Button(
    title=Computed(lambda: f"Clicked {clicks.value} times"),
    on_click=lambda: setattr(clicks, 'value', clicks.value + 1),
    enabled=Computed(lambda: clicks.value < 10)  # Disable after 10 clicks
)

# Two-way data binding with text field
text = Signal("Type here...")
field = TextField(
    value=text,  # Automatic two-way binding
    placeholder="Enter text..."
)

# Layout with reactive visibility
ui = VStack(children=[
    Label("Reactive Demo"),
    field,
    Show(
        when=Computed(lambda: len(text.value) > 0),  # Conditional rendering
        children=lambda: Label(f"You typed: {text.value}")
    ),
    button
])
```

## 📱 Application Framework

### Complete Application

```python
from macui import MacUIApp, Component, Signal, Computed
from macui.components import VStack, HStack, Label, Button, TextField

class TodoApp(Component):
    def __init__(self):
        super().__init__()
        self.todos = self.create_signal([])
        self.new_todo = self.create_signal("")
        self.todo_count = self.create_computed(lambda: len(self.todos.value))
    
    def add_todo(self):
        if self.new_todo.value.strip():
            self.todos.value = [*self.todos.value, self.new_todo.value.strip()]
            self.new_todo.value = ""
    
    def mount(self):
        return VStack(padding=20, spacing=15, children=[
            Label("Todo App"),
            
            HStack(spacing=10, children=[
                TextField(
                    value=self.new_todo,
                    placeholder="Add a new todo...",
                    on_enter=self.add_todo
                ),
                Button("Add", on_click=self.add_todo)
            ]),
            
            Label(Computed(lambda: f"Total todos: {self.todo_count.value}")),
            
            # Dynamic list rendering
            For(
                items=self.todos,
                render_fn=lambda todo, index: Label(f"{index + 1}. {todo}")
            )
        ])

def main():
    app = MacUIApp("Todo App")
    
    window = app.create_window(
        title="My Todo List",
        size=(400, 500),
        content=TodoApp()
    )
    
    window.show()
    app.run()  # Uses AppHelper for proper lifecycle management

if __name__ == "__main__":
    main()
```

## 🔧 Development with uv

### Project Setup

```bash
# Initialize new project
uv init my-macui-project
cd my-macui-project

# Add macui with development dependencies
uv add macui[dev]

# Install pre-commit hooks
uv run pre-commit install
```

### Development Commands

```bash
# Run tests
uv run pytest

# Code formatting
uv run black .
uv run isort .

# Linting
uv run ruff check .
uv run ruff check --fix .

# Type checking
uv run mypy macui

# Build package
uv build

# Run examples
uv run python examples/counter.py
```

### Development Dependencies

The `[dev]` extra includes:
- **Testing**: pytest, pytest-cov, pytest-xdist
- **Code Quality**: ruff, black, isort, mypy
- **Documentation**: sphinx, sphinx-rtd-theme  
- **Tools**: pre-commit, build, twine

## 📖 Examples

### Counter App
```bash
uv run python examples/counter.py
```

### Advanced Counter with Multiple States
```bash
uv run python examples/advanced_counter.py  
```

### Form Handling
```bash
uv run python examples/form_demo.py
```

## 🎯 Why macUI v2?

### vs. Other GUI Frameworks

| Feature | macUI v2 | Tkinter | PyQt/PySide | Kivy |
|---------|----------|---------|-------------|------|
| Native macOS | ✅ Full | ❌ Emulated | ⚠️ Themed | ❌ Custom |
| Reactive Updates | ✅ Automatic | ❌ Manual | ❌ Signals/Slots | ❌ Manual |
| Performance | ✅ Native | ⚠️ Medium | ⚠️ Medium | ✅ Good |
| macOS Integration | ✅ Complete | ❌ None | ⚠️ Limited | ❌ None |
| Learning Curve | ✅ Gentle | ✅ Easy | ❌ Steep | ⚠️ Medium |
| Bundle Size | ✅ Small | ✅ Small | ❌ Large | ⚠️ Medium |

### Key Advantages

- **Native Performance**: Direct AppKit integration, no abstraction overhead
- **Reactive by Design**: Automatic UI updates, no manual DOM manipulation
- **macOS-First**: Built specifically for macOS, leveraging platform strengths
- **Modern Developer Experience**: Type hints, IDE support, modern tooling
- **Production Ready**: Proper memory management, lifecycle handling

## 📚 Documentation

- [API Reference](docs/api.md)
- [Component Guide](docs/components.md)
- [Reactive Patterns](docs/reactivity.md)
- [Best Practices](docs/best-practices.md)
- [PyObjC Integration](docs/pyobjc.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and development process.

### Development Setup

```bash
git clone https://github.com/macui/macui.git
cd macui
uv sync --all-extras
uv run pre-commit install
uv run pytest
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SolidJS** - Inspiration for the reactive system design
- **PyObjC** - The foundation that makes this possible
- **macOS AppKit** - The native UI framework we build upon

---

**macUI v2** - Bringing reactive, modern UI development to native macOS applications. 🍎✨