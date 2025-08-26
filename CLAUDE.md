# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**macUI v2** is a reactive UI framework for native macOS applications using Python and PyObjC. It provides signal-based reactivity inspired by SolidJS, with fine-grained updates that directly manipulate native NSViews without a virtual DOM.

## Development Commands

### Setup and Installation
```bash
# Install with uv (recommended)
uv add macui

# Development setup
uv sync --all-extras
uv run pre-commit install
```

### Testing and Quality
```bash
# Run tests
uv run pytest

# Code quality
uv run ruff check .
uv run ruff check --fix .
uv run black .
uv run isort .
uv run mypy macui

# Build package
uv build
```

### Running Examples
```bash
# Basic examples
uv run python examples/basic/counter.py
uv run python examples/basic/advanced_counter.py

# Input control examples  
uv run python examples/input/slider_example.py
uv run python examples/input/checkbox_example.py

# Layout examples
uv run python examples/layout/stack_example.py
uv run python examples/layout/responsive_example.py

# TableView examples (reference implementations)
uv run python examples/tableview/simple_pure_tableview.py
uv run python examples/tableview/advanced_pure_tableview_simple.py
```

## Core Architecture

The framework follows a layered architecture:

```
Application Layer (User Code)
       ↓
Component System (Component, mount, lifecycle)
       ↓
Reactive System (Signal, Computed, Effect) ← CORE
       ↓
Binding Layer (ReactiveBinding, property binding)
       ↓
AppKit/PyObjC (NSView, NSButton, etc.)
```

### Key Directories
- `macui/core/` - Reactive system core (Signal, Effect, Component)
- `macui/components/` - UI components (controls, layout)
- `macui/app.py` - Application and window management
- `examples/` - Usage examples and reference implementations

## Signal-Based Reactivity

The core reactive system uses three primitives:

```python
# Signal - reactive state
count = Signal(0)
count.value = 5  # Triggers updates

# Computed - derived values
double = Computed(lambda: count.value * 2)

# Effect - side effects
effect = Effect(lambda: print(f"Count: {count.value}"))
```

## PyObjC Best Practices

All PyObjC applications in this project must follow the 4 core requirements:

1. **Activation Policy**: `app.setActivationPolicy_(NSApplicationActivationPolicyRegular)`
2. **Menu Bar**: Create minimal menu bar with Cmd+Q quit functionality
3. **AppHelper Event Loop**: `AppHelper.runEventLoop(installInterrupt=True)`
4. **Separated Architecture**: AppDelegate + WindowController with strong references

Example structure:
```python
class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.window_controller = WindowController.alloc().init()  # Strong reference

class WindowController(NSObject):
    def __init__(self):
        self.window = None      # Strong reference
        self.components = None  # Strong reference
```

## Known Issues

### TableView Component (SOLVED)
- **Status**: ✅ Root cause identified and solved
- **Problem**: `NSLayoutConstraintNumberExceedsLimit` error when TableView used in VStack/HStack
- **Root Cause**: NSStackView constraint system conflicts with NSTableView internal constraints
- **Solution**: Never put TableView inside VStack/HStack - use simple NSView containers instead
- **Files**: 
  - Solution report: `TABLEVIEW_SOLUTION_REPORT.md`
  - Working example: `examples/tableview_no_stack_fix.py`
  - Correct usage: `examples/tableview_correct_usage.py`

### Component Organization (Updated 2025-08-26)

Components are now organized by logical groups for better maintainability and Claude Code efficiency:

**File Structure**:
- `basic_controls.py` (213 lines) - Button, Label, TextField
- `input_controls.py` (385 lines) - Slider, Switch, Checkbox, RadioButton, SegmentedControl  
- `selection_controls.py` (224 lines) - PopUpButton, ComboBox, Menu, ContextMenu
- `display_controls.py` (217 lines) - ImageView, ProgressBar, TextArea
- `picker_controls.py` (174 lines) - DatePicker, TimePicker
- `layout.py` (692 lines) - VStack, HStack, ScrollView, TableView, etc.

**API Compatibility**: All imports remain the same - `from macui.components import Button` still works.

### Working Components
- ✅ All basic controls (Button, Label, TextField)
- ✅ All input controls (Slider, Switch, Checkbox, etc.)
- ✅ All selection controls (PopUpButton, ComboBox, Menu, etc.)  
- ✅ All display controls (ImageView, ProgressBar, TextArea)
- ✅ All picker controls (DatePicker, TimePicker)
- ✅ Layout components (VStack, HStack, ScrollView)
- ✅ Reactive system (Signal, Computed, Effect)
- ✅ Window and app management

## Memory Management

The project uses a hybrid approach:
- `associate_object()` for NSObject associations
- Component-managed signal lifecycles
- Effect cleanup on component destruction

Critical: All UI objects must maintain strong references through the component hierarchy to prevent garbage collection.

## Component Development

When creating new components:

1. Inherit from `Component` base class
2. Use `self.create_signal()` for component-scoped state
3. Implement `mount()` method returning NSView
4. Use `ReactiveBinding.bind()` for property updates
5. Follow NSTableView patterns for complex components (see examples/tableview/)

### Critical Layout Constraint Rules

**❌ NEVER do this:**
```python
VStack(children=[
    TableView(...)  # Will cause NSLayoutConstraintNumberExceedsLimit crash
])
```

**✅ Correct approach:**
```python
# Use simple NSView container with frame-based layout
container = NSView.alloc().init()
table = TableView(columns=..., frame=(x, y, w, h))
container.addSubview_(table)
```

### Complex Component Guidelines
- Components with internal constraint systems (like TableView) should use `translatesAutoresizingMaskIntoConstraints=True`
- Never put NSScrollView/NSTableView inside NSStackView-based layouts
- Use frame-based layout for complex components that manage their own constraints

## Testing Strategy

- Unit tests for reactive system in `tests/`
- Integration tests for component behavior
- Reference implementations in `examples/` for validation
- TableView: Use pure PyObjC examples to validate NSTableView functionality

## Current Development Focus

1. **Fix TableView**: Resolve constraint conflicts in layout.py:460-578
2. **Component Library**: Expand available UI components
3. **Documentation**: Complete API documentation
4. **Performance**: Optimize batch updates and memory usage