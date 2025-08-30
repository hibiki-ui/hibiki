# CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with the Hibiki UI ecosystem. It contains essential development patterns, architectural principles, and best practices for this modern macOS UI framework.

## Project Overview

**Hibiki UI** is a cutting-edge reactive UI framework for native macOS applications built with Python and PyObjC. It provides a signal-based reactivity system with fine-grained updates that directly manipulate native NSViews, delivering optimal performance without virtual DOM overhead.

### 🏗️ Core Architecture

The framework follows a sophisticated layered architecture:

```
Application Layer (User Code)
       ↓
Component System (Label, Button, Container, etc.)
       ↓
Reactive System (Signal, Computed, Effect) ← CORE ENGINE
       ↓
Binding & Layout (ReactiveBinding, Stretchable Engine)
       ↓
Managers (App, Viewport, Layer, Positioning, etc.)
       ↓
AppKit/PyObjC (NSView, NSButton, NSTextField, etc.)
```

### 🎯 Key Features

- **🔄 Reaktiv-inspired Signal System**: Enterprise-grade reactive programming with version control and batch processing
- **📐 Stretchable Layout Engine**: Professional CSS Grid and Flexbox implementation
- **🎨 Pure Core Animation**: GPU-accelerated animations using only Core Animation APIs
- **🔧 Unified Component API**: Simple, consistent interface across all components
- **📱 Responsive Design**: Built-in breakpoint system and viewport management
- **🎭 Theme System**: Complete theming with light/dark mode support
- **🚀 Performance Optimized**: Minimal overhead, direct NSView manipulation

## Directory Structure

```
hibiki-ui/
├── ui/                                    # Hibiki UI Framework
│   ├── src/hibiki/ui/                     # Main package
│   │   ├── core/                          # Core systems
│   │   │   ├── reactive.py               # Signal, Computed, Effect
│   │   │   ├── component.py              # UIComponent, Container base classes
│   │   │   ├── styles.py                 # ComponentStyle, layout enums
│   │   │   ├── binding.py                # Reactive binding system
│   │   │   ├── layout.py                 # Stretchable layout engine
│   │   │   ├── managers.py               # App, Window, Viewport managers
│   │   │   ├── animation.py              # Core Animation API
│   │   │   ├── responsive.py             # Breakpoint and responsive system
│   │   │   └── text_props.py             # Text styling system
│   │   ├── components/                   # UI component library
│   │   │   ├── basic.py                  # Label, Button, TextField, etc.
│   │   │   ├── layout.py                 # Grid, Stack, responsive containers
│   │   │   ├── forms.py                  # Form components and validation
│   │   │   └── custom_view.py            # Custom drawing utilities
│   │   ├── theme/                        # Theming system
│   │   │   ├── theme_manager.py          # Theme management
│   │   │   ├── colors.py                 # Color schemes
│   │   │   ├── fonts.py                  # Font management
│   │   │   └── appearance.py             # Light/dark mode
│   │   └── __init__.py                   # Main API exports
│   ├── examples/                         # Usage examples
│   │   └── basic/                        # Tutorial examples (01-11)
│   └── tests/                           # Test suite
├── music/                               # Hibiki Music (separate project)
└── docs/                               # Documentation
```

## Development Setup and Commands

### 🚀 Environment Setup

```bash
# Prerequisites
# - Python 3.11+
# - macOS 10.15+
# - uv (recommended package manager)

# Clone and setup
git clone <repository-url>
cd hibiki-ui

# Install dependencies (automatically installs project in editable mode)
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install
```

### 🧪 Testing and Quality Assurance

```bash
# Run comprehensive test suite
uv run pytest

# Code quality checks
uv run ruff check .
uv run ruff check --fix .       # Auto-fix issues
uv run black .                  # Format code
uv run isort .                  # Sort imports
uv run mypy hibiki              # Type checking

# Build distribution package
uv build

# Run GUI examples (timeout is expected and normal)
timeout 8 uv run python ui/examples/basic/01_hello_world.py
timeout 8 uv run python ui/examples/basic/02_reactive_basics.py
timeout 8 uv run python ui/examples/basic/11_modern_card_showcase.py
```

### 📚 Example Programs

The framework includes 9 comprehensive examples:
1. **01_hello_world.py** - Basic application structure
2. **02_reactive_basics.py** - Signal/Computed/Effect usage
3. **03_forms_and_inputs.py** - Form components and validation
4. **04_layout.py** - Flexbox and basic layouts
5. **05_responsive_layout.py** - Responsive design patterns
6. **06_dynamic_grid_columns.py** - Dynamic grid systems
7. **07_static_grid_basic.py** - Static grid layouts
8. **11_modern_card_showcase.py** - Advanced card components with responsive grid

## Core Programming Patterns

### 🔄 Signal-Based Reactivity

The framework uses a powerful reactive system inspired by SolidJS and enhanced with Reaktiv optimizations:

```python
from hibiki.ui import Signal, Computed, Effect

# Signal - reactive state
count = Signal(0)
count.value = 5  # Triggers dependent updates

# Computed - derived values with intelligent caching
double = Computed(lambda: count.value * 2)
formatted = Computed(lambda: f"Count: {count.value}, Double: {double.value}")

# Effect - side effects with automatic cleanup
effect = Effect(lambda: print(f"Current value: {count.value}"))
```

**Key Features:**
- **Version Control**: Each Signal/Computed tracks versions for intelligent caching
- **Batch Processing**: Multiple updates are automatically batched and deduplicated
- **Smart Dependencies**: Only recomputes when dependencies actually change
- **Automatic Cleanup**: Effects are automatically disposed when components unmount

### 🎨 Component Development

```python
from hibiki.ui import (
    UIComponent, Label, Button, Container,
    ComponentStyle, Display, FlexDirection, px
)

# Basic component usage
label = Label(
    "Hello World",
    font_size=16,
    color="#333",
    style=ComponentStyle(padding=px(10))
)

button = Button(
    "Click me",
    on_click=lambda: print("Clicked!"),
    style=ComponentStyle(
        background_color="#007acc",
        border_radius=px(8)
    )
)

# Container with flexbox layout
container = Container(
    children=[label, button],
    style=ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.COLUMN,
        gap=px(10),
        padding=px(20)
    )
)
```

### 📐 Advanced Layout System

The framework includes a professional layout system with CSS Grid and Flexbox support:

```python
from hibiki.ui import ComponentStyle, Display, px
from hibiki.ui.components.layout import GridContainer, ResponsiveGrid

# CSS Grid layout
grid = GridContainer(
    children=cards,
    columns="repeat(3, 1fr)",  # 3 equal columns
    rows="auto",
    gap=16,
    style=ComponentStyle(padding=px(20))
)

# Responsive grid that adapts to container width
responsive_grid = ResponsiveGrid(
    children=items,
    min_column_width=300,    # Minimum column width
    max_columns=4,           # Maximum columns
    gap=20
)

# Advanced grid positioning
grid.set_grid_position(child_component, 
                      column_start=1, column_end=3,
                      row_start=1, row_end=2)
```

### 📱 Responsive Design

Built-in responsive system with breakpoint management:

```python
from hibiki.ui import (
    ComponentStyle, responsive_style, BreakpointName, 
    get_responsive_manager, px
)

# Create responsive styles
responsive_style_obj = (
    responsive_style(
        ComponentStyle(
            display=Display.GRID,
            grid_template_columns="1fr",  # Mobile: 1 column
            gap=px(16)
        )
    )
    .at_breakpoint(BreakpointName.MD, ComponentStyle(
        grid_template_columns="1fr 1fr",  # Tablet: 2 columns
        gap=px(20)
    ))
    .at_breakpoint(BreakpointName.LG, ComponentStyle(
        grid_template_columns="1fr 1fr 1fr",  # Desktop: 3 columns
        gap=px(24)
    ))
)

# Apply to component
container = Container(
    children=items,
    responsive_style=responsive_style_obj
)

# Register with responsive manager
responsive_mgr = get_responsive_manager()
responsive_mgr.register_component(container)
```

### 🎭 Animation System

Pure Core Animation implementation for maximum performance:

```python
from hibiki.ui import animate, fade_in, fade_out, bounce

# Simple declarative animations
animate(view, duration=0.5, opacity=0.8, scale=1.2)

# Preset animation effects
fade_in(view, duration=1.0)
fade_out(view, duration=0.5)
bounce(view, scale=1.1)

# Signal-reactive animations
visible = Signal(True)
effect = Effect(lambda: animate(
    label, 
    opacity=1.0 if visible.value else 0.3,
    duration=0.3
))
```

## Application Development Patterns

### 📱 Standard Application Structure

All Hibiki UI applications must follow these essential patterns:

```python
from hibiki.ui import ManagerFactory, Container, ComponentStyle

def create_main_app():
    """Standard application setup pattern"""
    
    # 1. Create application manager
    app_manager = ManagerFactory.get_app_manager()
    
    # 2. Create window with appropriate size
    window = app_manager.create_window(
        title="My App",
        width=1200,
        height=800
    )
    
    # 3. Create main UI content
    main_content = Container(
        children=[
            # Your components here
        ],
        style=ComponentStyle(
            padding=px(20),
            width=percent(100)
        )
    )
    
    # 4. Set window content
    window.set_content(main_content)
    
    # 5. Run application event loop
    app_manager.run()

if __name__ == "__main__":
    create_main_app()
```

### 🏗️ Component Lifecycle Management

Components follow a clear lifecycle with automatic resource management:

```python
class CustomComponent(UIComponent):
    def __init__(self, initial_data):
        super().__init__()
        
        # Create component-scoped signals
        self.data = self.create_signal(initial_data)
        self.computed_value = self.create_computed(
            lambda: self.process_data(self.data.value)
        )
        
        # Effects are automatically cleaned up on unmount
        self.create_effect(lambda: self.handle_data_change(self.data.value))
    
    def _create_nsview(self) -> NSView:
        """Create and return the native NSView"""
        view = NSView.alloc().init()
        # Configure view...
        return view
    
    def mount(self) -> NSView:
        """Called when component is added to the UI tree"""
        nsview = super().mount()
        # Additional setup after mount...
        return nsview
```

## Critical Development Guidelines

### 🚨 Import Best Practices

**CRITICAL: Always use standard Python imports, never sys.path manipulation**

```python
# ✅ CORRECT: Standard package imports
from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container, 
    ComponentStyle, Display, FlexDirection, px, percent,
    ManagerFactory
)

# ❌ WRONG: Never use sys.path.insert()
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
```

### 🎨 Styling Best Practices

**Always use enum values for consistent styling:**

```python
# ✅ CORRECT: Use enums for type safety
from hibiki.ui import Display, FlexDirection, JustifyContent, AlignItems

style = ComponentStyle(
    display=Display.FLEX,
    flex_direction=FlexDirection.COLUMN,
    justify_content=JustifyContent.CENTER,
    align_items=AlignItems.STRETCH
)

# ❌ WRONG: String literals are error-prone
style = ComponentStyle(
    display="flex",
    flex_direction="column",
    justify_content="center",
    align_items="stretch"
)
```

### 🎯 Performance Optimization

**Leverage the reactive system's built-in optimizations:**

```python
# ✅ CORRECT: Let the system batch updates automatically
def update_multiple_values():
    # These updates are automatically batched
    signal1.value = new_value1
    signal2.value = new_value2
    signal3.value = new_value3
    # Single batch update occurs here

# ✅ CORRECT: Use Computed for expensive calculations
expensive_calculation = Computed(lambda: heavy_computation(data.value))

# ❌ WRONG: Manual batching or frequent recalculation
```

### 🖥️ macOS Integration Best Practices

**Essential PyObjC application requirements:**

1. **Application Activation**: `app.setActivationPolicy_(NSApplicationActivationPolicyRegular)`
2. **Menu Bar**: Create minimal menu with Cmd+Q quit functionality
3. **Event Loop**: Use `AppHelper.runEventLoop(installInterrupt=True)`
4. **Strong References**: Maintain references to prevent garbage collection

```python
# ✅ CORRECT: Proper macOS app structure
class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Strong reference prevents garbage collection
        self.window_controller = WindowController.alloc().init()

class WindowController(NSObject):
    def __init__(self):
        # Strong references to UI components
        self.window = None
        self.main_component = None
```

## Advanced Features

### 🎨 Theme System

Comprehensive theming with reactive updates:

```python
from hibiki.ui import (
    get_theme_manager, ThemeManager, PresetThemes,
    get_appearance_manager, is_dark_mode
)

# Theme management
theme_manager = get_theme_manager()
theme_manager.set_theme(PresetThemes.OCEAN)

# Reactive theme changes
appearance_manager = get_appearance_manager()
dark_mode = Signal(is_dark_mode())
appearance_manager.add_observer(lambda mode: setattr(dark_mode, 'value', mode == 'dark'))
```

### 🧩 Custom Component Development

```python
from hibiki.ui import UIComponent, ComponentStyle
from AppKit import NSView

class ProgressCircle(UIComponent):
    """Custom circular progress component"""
    
    def __init__(self, progress: Union[float, Signal[float]]):
        super().__init__()
        
        # Handle both static and reactive progress
        if isinstance(progress, Signal):
            self.progress = progress
        else:
            self.progress = self.create_signal(progress)
        
        # Reactive drawing updates
        self.create_effect(lambda: self._update_drawing())
    
    def _create_nsview(self) -> NSView:
        from .custom_view import CustomView
        
        view = CustomView.alloc().init()
        view.set_draw_callback(self._draw_progress)
        return view
    
    def _draw_progress(self, rect):
        # Custom Core Graphics drawing code
        pass
```

### 📊 Form Handling and Validation

```python
from hibiki.ui.components.forms import Form, FormField, RequiredValidator, EmailValidator

# Create form with validation
form = Form([
    FormField("email", TextField(placeholder="Email"), [
        RequiredValidator("Email is required"),
        EmailValidator("Invalid email format")
    ]),
    FormField("name", TextField(placeholder="Full Name"), [
        RequiredValidator("Name is required")
    ])
])

# Handle form submission
submit_button = Button(
    "Submit",
    on_click=lambda: handle_form_submit(form)
)

def handle_form_submit(form):
    if form.is_valid():
        data = form.get_data()
        # Process valid form data
    else:
        errors = form.get_errors()
        # Handle validation errors
```

## 🧭 坐标系统

Hibiki UI使用**top-left坐标系**以保持与现代UI框架的一致性：

- **原点**: 左上角 (0, 0)
- **X轴**: 向右递增
- **Y轴**: 向下递增

这与Web CSS、React、SwiftUI等框架保持一致，但与macOS原生的bottom-left坐标系不同。

### 技术实现

框架通过设置`NSView.isFlipped = True`来实现坐标系转换：

```python
class HibikiBaseView(NSView):
    def isFlipped(self) -> bool:
        return True  # 启用top-left坐标系
```

### 开发考虑

- **布局计算**: 所有Y坐标按top-left逻辑计算
- **事件处理**: 点击坐标自动转换为top-left坐标系
- **截屏工具**: 生成的截图按macOS原生坐标系显示（正确行为）
- **调试工具**: 坐标信息以top-left格式显示

### 迁移注意事项

从bottom-left坐标系迁移时：
- 布局代码无需修改（框架自动处理）
- 手动坐标计算需要适应top-left逻辑
- 与原生Cocoa API交互时注意坐标系差异

## Debugging and Development Tools

### 🔍 Debugging GUI Applications

Use the systematic "Gradual Feature Addition" method:

1. **Start with working baseline** - Begin with simplest version that works
2. **Add features incrementally** - Create debug versions (debug_v1.py, debug_v2.py)
3. **Test each increment** - Use `timeout 8 uv run python filename.py`
4. **Identify failure points** - Know exactly which addition breaks functionality
5. **Fix at framework level** - Resolve root causes, not application workarounds

```bash
# Testing GUI applications
timeout 8 uv run python my_app.py    # Success = enters event loop
timeout 15 uv run python complex_app.py  # Longer timeout for complex apps

# Debugging output
uv run python app.py 2>&1 | grep -E "(ERROR|WARNING|Exception)"
```

### 📝 Logging and Diagnostics

The framework includes comprehensive logging:

```python
from hibiki.ui.core.logging import get_logger

# Component-specific logging
logger = get_logger("my_component")
logger.info("Component initialized")
logger.debug("Detailed debug information")
logger.warning("Potential issue detected")
logger.error("Error occurred", exc_info=True)

# Built-in system logging provides:
# - Reactive system debugging (Signal updates, batch processing)
# - Layout calculation visibility
# - Component lifecycle tracking
# - Performance metrics
```

### 📸 Screenshot and Visual Debugging Tools

For debugging visual layout issues and verifying UI rendering:

```python
from hibiki.ui import capture_app_screenshot, debug_view_layout, ScreenshotTool

# Quick screenshot capture
success = capture_app_screenshot("debug_screenshot.png")

# Debug NSView layout properties
debug_view_layout(my_component._nsview, "My Component")

# Advanced screenshot tools
ScreenshotTool.capture_window(window, "window_capture.png")
ScreenshotTool.capture_view(view, "view_capture.png", format="jpg")

# Get detailed view information
info = ScreenshotTool.get_view_debug_info(view)
print(f"Frame: {info['frame']}")
print(f"Bounds: {info['bounds']}")
```

**Key Features:**
- **capture_app_screenshot()**: Quick current window capture
- **debug_view_layout()**: NSView property inspection with formatted logging
- **ScreenshotTool**: Advanced capture with format options (PNG/JPG)
- **get_view_debug_info()**: Detailed view metrics and hierarchy info

**Usage Tips:**
- **Bitmap Method (Recommended)**: Uses CoreGraphics for accurate screen capture
- Screenshots can be taken from any thread (with automatic handling)
- Use for visual verification after layout changes
- Combine with layout debugging for comprehensive analysis
- Ideal for before/after comparison testing
- **Superior Quality**: Bitmap capture produces more accurate results than PDF-based methods

**API Methods Available:**
- `capture_app_screenshot()`: Quick screenshot of current window (uses CoreGraphics)
- `ScreenshotTool.capture_window_with_cg()`: Direct CoreGraphics window capture
- `ScreenshotTool.capture_view_bitmap()`: NSView bitmap rendering for precise view capture
- `debug_view_layout()`: Layout debugging with visual verification

## Framework Status and Roadmap

### ✅ Production Ready (v4.0)

- **Core Reactive System**: Signal, Computed, Effect with Reaktiv optimizations
- **Component Library**: 15+ production-ready components
- **Layout Engine**: Professional CSS Grid and Flexbox implementation
- **Animation System**: Pure Core Animation with declarative API
- **Responsive Design**: Complete breakpoint and viewport management
- **Theme System**: Light/dark mode with custom theme support
- **Performance**: 30-50% UI responsiveness improvement over previous versions

### 🚀 Recent Major Improvements

**Reaktiv-Inspired Signal System Upgrade** (2025-08):
- Version control system for intelligent caching
- Batch processing with automatic deduplication  
- Smart dependency tracking prevents unnecessary recomputation
- 30-50% UI responsiveness improvement
- 20-40% computation performance boost
- 100% backward compatibility

### 🔬 Testing Strategy

- **Unit Tests**: Core reactive system (`tests/test_reactive.py`)
- **Integration Tests**: Component behavior and interactions
- **GUI Tests**: Visual validation through example programs
- **Performance Tests**: Benchmarks for reactive system optimizations

## Memory Management

The framework uses a hybrid memory management approach:

- **Component Lifecycle**: Automatic signal cleanup on component destruction
- **NSObject Associations**: `associate_object()` for Objective-C bridge
- **Strong References**: Component hierarchy maintains references to prevent GC
- **Effect Cleanup**: Automatic disposal of effects when components unmount

## Best Practices Summary

### ✅ Do

- Use standard Python imports with proper package structure
- Leverage enum values for styling consistency
- Take advantage of automatic batch processing
- Use Computed for expensive calculations
- Follow the 4 core PyObjC requirements for GUI apps
- Use `timeout` for testing GUI applications
- Create incremental debug versions when troubleshooting

### ❌ Don't

- Use `sys.path.insert()` or path manipulation
- Use string literals instead of enums for styles
- Create manual batching or frequent recalculation
- Use threading, time.sleep(), or custom timers for animations
- Skip the gradual feature addition method when debugging
- Assume libraries are available without checking imports

## Getting Help

- **Examples**: Comprehensive tutorial series in `ui/examples/basic/`
- **Documentation**: In-code documentation and type hints
- **Source Code**: Well-structured, readable implementation
- **Community**: GitHub issues for bug reports and feature requests

---

**For complete API reference and advanced examples, see the source code and example programs.**