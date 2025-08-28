# Hibiki UI Examples

Welcome to the Hibiki UI examples collection! This directory contains comprehensive examples demonstrating all aspects of the Hibiki UI framework.

## 📁 Directory Structure

```
examples/
├── basic/          # 🌟 Start here - Basic concepts
├── advanced/       # 🚀 Advanced features
├── complete/       # 💎 Full applications
└── tutorials/      # 📚 Step-by-step guides
```

## 🌟 Getting Started

### Prerequisites
- Python 3.11 or higher
- macOS (Hibiki UI is macOS-specific)
- Hibiki UI installed (`uv add hibiki`)

### Quick Start

1. **Hello World** - Your first Hibiki UI app:
   ```bash
   uv run python examples/basic/01_hello_world.py
   ```

2. **Reactive Basics** - Learn about Signal and Computed:
   ```bash
   uv run python examples/basic/02_reactive_basics.py
   ```

3. **Forms and Inputs** - Explore UI controls:
   ```bash
   uv run python examples/basic/03_forms_and_inputs.py
   ```

4. **Complete Showcase** - See everything in action:
   ```bash
   uv run python examples/complete/showcase.py
   ```

## 📚 Learning Path

### 🌟 Basic Examples
Perfect for newcomers to Hibiki UI:

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| `01_hello_world.py` | Simplest possible app | Label, ManagerFactory |
| `02_reactive_basics.py` | Reactive state management | Signal, Computed, Button events |
| `03_forms_and_inputs.py` | Form controls | TextField, Slider, Switch, Checkbox |

### 🚀 Advanced Examples
For developers ready to explore complex features:

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| `layout_systems.py` | Advanced layout patterns | Flexbox, Grid, ResponsiveGrid |
| `animation_demos.py` | Animation and transitions | Core Animation, declarative API |
| `theme_customization.py` | Theming and appearance | Dark mode, custom themes |
| `custom_components.py` | Building custom components | CustomView, DrawingUtils |

### 💎 Complete Applications
Full-featured example applications:

| Example | Description | Features |
|---------|-------------|----------|
| `showcase.py` | Complete feature demonstration | All components, theming, animations |
| `todo_app.py` | Production-ready todo app | CRUD operations, persistence |
| `dashboard.py` | Analytics dashboard | Charts, real-time data |

### 📚 Tutorials
Step-by-step learning materials:

| Tutorial | Description | Duration |
|----------|-------------|----------|
| `getting_started.md` | Framework introduction | 15 min |
| `reactive_patterns.md` | Advanced reactive patterns | 30 min |
| `performance_guide.md` | Optimization techniques | 20 min |

## 🎯 Key Concepts Demonstrated

### Reactive System
- **Signal**: Mutable reactive state
- **Computed**: Derived values that auto-update
- **Effect**: Side effects triggered by state changes

### Component System
- **Basic Components**: Label, Button, TextField, etc.
- **Layout Components**: Container, VStack, HStack
- **Custom Components**: Build your own with CustomView

### Styling System
- **ComponentStyle**: Comprehensive styling API
- **Layout Properties**: Flexbox-style layout control
- **Responsive Design**: Adaptive layouts

### Animation System
- **Pure Core Animation**: GPU-accelerated animations
- **Declarative API**: Simple animate() function
- **Preset Effects**: fade_in, bounce, and more

## 🔧 Running Examples

### Using uv (Recommended)
```bash
# Run specific example
uv run python examples/basic/01_hello_world.py

# Run with timeout for GUI testing
timeout 8 uv run python examples/basic/01_hello_world.py
```

### Direct Python
```bash
# Make sure hibiki is installed
python examples/basic/01_hello_world.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'hibiki'
   ```
   **Solution**: Install with `uv add hibiki` or `pip install hibiki`

2. **GUI Not Appearing**
   ```
   App starts but no window shows
   ```
   **Solution**: Ensure you're on macOS and have proper permissions

3. **PyObjC Errors**
   ```
   AttributeError: ... NSView ...
   ```
   **Solution**: Update PyObjC with `uv add pyobjc>=11.1`

### Getting Help

- Check the main documentation in `CLAUDE.md`
- Review the debugging section for systematic troubleshooting
- Use the timeout command for GUI testing: `timeout 8 uv run python app.py`

## 🌟 Best Practices

1. **Start Simple**: Begin with basic examples before advanced features
2. **Use Signals**: Embrace reactive programming patterns
3. **Style Consistently**: Use ComponentStyle for all styling
4. **Test Regularly**: Use timeout command for quick GUI testing
5. **Follow Patterns**: Study the showcase.py for best practices

## 📈 Next Steps

After exploring these examples:

1. **Build Your Own App**: Start with a basic example and extend it
2. **Explore Advanced Features**: Check out animation and theming examples
3. **Contribute**: Share your own examples with the community
4. **Read Documentation**: Deep dive into framework internals in `/docs`

---

Happy coding with Hibiki UI! 🎨✨