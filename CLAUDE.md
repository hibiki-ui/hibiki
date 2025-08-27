# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**macUI v3.0** is a reactive UI framework for native macOS applications using Python and PyObjC. It provides signal-based reactivity inspired by SolidJS, with fine-grained updates that directly manipulate native NSViews without a virtual DOM.

### Key v3.0 Features
- **Unified API**: Simple component names (`Label`, `Button`) automatically resolve to best implementations
- **Stretchable Layout Engine**: Professional layout system with CSS-like properties
- **Complete Reactive System**: Signal, Computed, Effect with full UI binding support
- **Event Handling**: Comprehensive click and interaction event system

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

## Debugging Techniques

### Gradual Feature Addition Method (Proven Effective)

When debugging complex UI issues, use this systematic approach:

1. **Start with working baseline** - Find the simplest version that works
2. **Add one feature at a time** - Create incremental versions (debug_showcase_1.py, debug_showcase_2.py, etc.)
3. **Test each increment** - Use `timeout 8 uv run python filename.py` to test GUI apps
4. **Identify exact failure point** - Know precisely which feature addition breaks functionality
5. **Fix at framework level** - Resolve root causes in framework code, not application workarounds

**Example progression:**
- v1: Basic unified API imports ✅
- v2: Add Signal/Computed state ✅  
- v3: Add click event handlers ❌ (Found EventBinding issue)
- v4: Add reactive binding ❌ (Found ReactiveBinding issue)
- v5: Combined features after fixes ✅

### GUI Application Testing
- Use `timeout 8 uv run python app.py` for GUI apps (longer timeout for manual testing)
- Success = App enters event loop without errors (timeout is expected)
- Failure = Error messages or immediate exit before timeout
- Watch for import errors, binding failures, layout issues

### Common Framework Issues
- **Import path errors**: Check `..core.binding` vs `..binding.event`  
- **Missing reactive properties**: Add support in `ReactiveBinding.SETTERS`
- **Missing dependencies**: Install with `uv add package-name`
- **Unified API issues**: Verify `__init__.py` imports point to working implementations

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

## Framework Status

### ✅ Core Framework (v3.0)
- Unified API system working correctly
- Reactive binding system (Signal, Computed, Effect)
- Event handling system (EventBinding)
- Layout components (VStack, HStack) with Stretchable engine

### 🔧 Recent Fixes (2025-08-27)
- ReactiveBinding now supports `stringValue` property
- EventBinding import path corrected (`..core.binding`)
- Unified API components fully functional

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

### Critical NSTextField/NSStackView Implementation Details

**Essential PyObjC Method Signatures** (verified working):
```python
# NSTextField configuration
label.setUsesSingleLineMode_(False)                    # Enable multi-line
label.setLineBreakMode_(NSLineBreakByWordWrapping)     # Word wrap mode
label.setPreferredMaxLayoutWidth_(400.0)              # Key for intrinsic size

# NSTextFieldCell configuration  
text_cell = label.cell()
text_cell.setWraps_(True)                              # Enable text wrapping
text_cell.setScrollable_(False)                        # Disable scroll for Auto Layout

# NSStackView constraint fixes
stack.setOrientation_(0)                               # 0=Horizontal, 1=Vertical
stack.setAlignment_(NSLayoutAttributeCenterY)          # HStack uses vertical alignment
stack.setAlignment_(NSLayoutAttributeCenterX)          # VStack uses horizontal alignment
stack.updateConstraintsForSubtreeIfNeeded()           # Force constraint generation
stack.layoutSubtreeIfNeeded()                         # Force layout update
```

**Layout Problem Diagnosis Patterns:**
- **Button overlap**: Usually NSStackView orientation mismatch (0 vs 1)
- **Text width 4px**: Missing `preferredMaxLayoutWidth` on NSTextField  
- **Negative coordinates**: Parent container has 0x0 frame size
- **Click not working**: Buttons positioned outside visible area

## Testing Strategy

- Unit tests for reactive system in `tests/`
- Integration tests for component behavior
- Reference implementations in `examples/` for validation
- TableView: Use pure PyObjC examples to validate NSTableView functionality

## Documentation Index

Complete project documentation for design decisions, investigations, and architecture:

- **Layout System Research Report**: `docs/LAYOUT_SYSTEM_RESEARCH.md` - Comprehensive research on Auto Layout systems, modern frameworks (React Native, Flutter), and architectural recommendations for professional layout implementation
- **Layout Problem Investigation**: `docs/LAYOUT_PROBLEM_INVESTIGATION.md` - Detailed technical investigation of NSStackView negative coordinate positioning bugs, systematic debugging process, and emergency fixes applied
- **Layout Engine v3.0 Implementation**: `docs/LAYOUT_ENGINE_V3_IMPLEMENTATION.md` - Complete implementation report for the professional Stretchable-based layout system (方案B), including architecture, performance metrics, and technical achievements
- **Component Refactoring Plan**: `docs/COMPONENT_REFACTORING_PLAN.md` - Comprehensive plan for refactoring existing components to work with the new layout system, including prioritization, migration strategies, and implementation roadmap
- **Component Refactoring Progress**: `docs/COMPONENT_REFACTORING_PROGRESS.md` - First phase completion report for LayoutAwareComponent base class and modern component implementation, including technical details, test results, and next phase planning

## Current Development Focus

1. **✅ Layout System Architecture Upgrade**: Successfully implemented professional Stretchable-based layout engine (方案B) - See implementation report for details
2. **Component Library**: Expand available UI components
3. **Documentation**: Complete API documentation 
4. **Performance**: Optimize batch updates and memory usage
5. **Advanced Features**: Enhanced responsive layout capabilities