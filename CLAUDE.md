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

## Hybrid Layout System (New in v2.1)

The framework now features a revolutionary **Hybrid Layout System** that automatically resolves the TableView constraint conflicts and provides seamless layout capabilities.

### Key Features

1. **Automatic Component Detection**: Intelligently detects simple vs complex components
2. **Dynamic Layout Selection**: Automatically chooses the best layout strategy
3. **Zero Breaking Changes**: Existing code continues to work unchanged
4. **Enhanced Capabilities**: Complex components now work in VStack/HStack

### Layout Modes

```python
from macui.components import VStack, LayoutMode

# Auto mode (default) - intelligent selection
VStack(children=[...])  # layout_mode="auto" implicit

# Force specific modes
VStack(layout_mode=LayoutMode.CONSTRAINTS, children=[...])  # NSStackView
VStack(layout_mode=LayoutMode.FRAME, children=[...])       # NSView + frame
VStack(layout_mode=LayoutMode.HYBRID, children=[...])      # Smart combination
```

### Component Classification

- **Simple Components**: Button, Label, TextField, Slider, etc. → Constraints layout
- **Complex Components**: TableView, OutlineView, SplitView, etc. → Frame layout

### Usage Examples

```python
# Simple components - uses efficient NSStackView (unchanged behavior)
VStack(children=[
    Label("Title"),
    Button("Click Me"),
    TextField(value="Input")
])

# Complex components - automatically switches to frame layout
VStack(children=[
    Label("Data Management"),
    TableView(columns=..., data=...),    # ✅ Now works!
    HStack(children=[
        Button("Add Row"), 
        Button("Delete Row")
    ])
])

# Manual frame layout for precise control
FrameContainer(
    frame=(0, 0, 400, 300),
    children=[
        TableView(frame=(10, 50, 380, 200), ...),
        Button(frame=(10, 10, 100, 30), ...)
    ]
)

# Responsive frame calculations
frame = ResponsiveFrame(x=0, y=0, width=100, height=50)
frame.relative_to_parent(parent, width_ratio=0.8, height_ratio=0.6)
```

### Migration Path

**For Simple Applications**: No changes required! Existing code works identically.

**For Complex Applications**: Simply use TableView in VStack/HStack - it now works automatically!

```python
# Before (would crash):
# VStack(children=[TableView(...)])  # ❌ NSLayoutConstraintNumberExceedsLimit

# After (works perfectly):
VStack(children=[TableView(...)])     # ✅ Automatic frame layout
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

### TableView Component & Hybrid Layout System (FULLY SOLVED)
- **Status**: ✅ Completely resolved with hybrid layout system
- **Old Problem**: `NSLayoutConstraintNumberExceedsLimit` error when TableView used in VStack/HStack
- **Revolutionary Solution**: Hybrid Layout System automatically handles complex components
- **New Capability**: TableView now works seamlessly in VStack/HStack!

**🎉 What's New:**
```python
# This now works perfectly! 🎉
VStack(children=[
    Label("Data Table"),
    TableView(columns=..., data=...),  # ✅ No more crashes!
    HStack(children=[Button("Add"), Button("Delete")])
])
```

**Technical Implementation:**
- Automatic component type detection (simple vs complex)
- Dynamic layout mode selection (constraints vs frame vs hybrid)
- Zero-cost abstraction for simple applications
- Seamless upgrade path for complex applications

**Test Files:**
  - Basic tests: `examples/layout/test_hybrid_basic.py`
  - Advanced tests: `examples/layout/test_hybrid_advanced.py`
  - Demo app: `examples/layout/hybrid_layout_demo.py`

### Auto Layout System Breakthrough (Updated 2025-08-26)

#### **🏆 Major Achievement: Professional NSStackView Implementation**

macUI v2.1 now features a **world-class Auto Layout system** that rivals native SwiftUI performance and reliability. Through systematic debugging and Apple-compliant implementation, we've solved the fundamental NSStackView layout issues.

#### **Key Technical Breakthroughs:**

1. **🔧 NSStackView Constraint System**: Complete resolution of button overlap and text layout issues
   - Fixed NSStackView orientation constants (HStack vs VStack)
   - Corrected alignment constant mappings for proper centering
   - Implemented forced layout updates with `layoutSubtreeIfNeeded()`

2. **✅ NSTextField Professional Configuration**: Apple-compliant text layout implementation
   - `preferredMaxLayoutWidth` property for proper intrinsic content size calculation
   - Multi-line text support with `setUsesSingleLineMode_(False)`
   - Word wrapping configuration with `setLineBreakMode_(NSLineBreakByWordWrapping)`
   - Cell-level controls: `setWraps_(True)` and `setScrollable_(False)`

3. **🎯 Mixed Layout Architecture**: Hybrid constraint/frame system
   - Constraint-based layout for simple components (NSStackView)
   - Frame-based layout for complex components (TableView, etc.)
   - Automatic component detection and layout mode selection

#### **Professional Interface Design (New v2.1)**

**Enhanced Label API** - From hardcoded values to professional flexibility:

```python
# Import professional enums
from macui.components import Label, LabelStyle, LineBreakMode

# Simple usage (90% of cases) - optimized defaults
Label("Multi-line text")                           # Uses intelligent defaults
Label("Status: Connected", style=LabelStyle.TITLE) # Single-line title
Label("file.txt", style=LabelStyle.TRUNCATED)      # Ellipsis truncation

# Advanced usage (10% of cases) - full control
Label("Custom text",
      multiline=False,
      line_break_mode=LineBreakMode.TRUNCATE_MIDDLE,
      preferred_max_width=200.0)
```

**Key Interface Features:**
- **Perfect Backward Compatibility**: Existing code works unchanged
- **Smart Defaults**: 400px width for VStack usage, multi-line enabled
- **Type Safety**: Enum-based configuration prevents magic number errors
- **Parameter Override System**: User parameters override preset styles
- **Self-Documenting**: Parameter names and enums serve as inline documentation

#### **Layout Debugging & Quality Assurance**

Comprehensive debugging system for development and troubleshooting:
- Real-time frame coordinate logging
- Layout mode decision tracking  
- Constraint generation verification
- Component type detection reporting

**Example Debug Output:**
```
✅ Label配置(预设样式title): 单行模式, 无宽度限制
🔧 VStack使用混合布局模式
📏 按钮 'Add Item' sizeToFit后: 78.0 x 32.0
子视图 1 NSTextField '🎉 macUI Demo': Frame(x=30.0, y=44.0, w=193.0, h=16.0)
```

### Component Organization (Updated 2025-08-26)

Components are now organized by logical groups for better maintainability and Claude Code efficiency:

**File Structure**:
- `basic_controls.py` (450+ lines) - Button, Label, TextField + Professional Interface System
- `input_controls.py` (385 lines) - Slider, Switch, Checkbox, RadioButton, SegmentedControl  
- `selection_controls.py` (224 lines) - PopUpButton, ComboBox, Menu, ContextMenu
- `display_controls.py` (217 lines) - ImageView, ProgressBar, TextArea
- `picker_controls.py` (174 lines) - DatePicker, TimePicker
- `layout.py` (1200+ lines) - VStack, HStack, ScrollView, TableView, etc. + Advanced Layout System

**New Professional APIs**:
- `LabelStyle` enum: MULTILINE, TITLE, TRUNCATED, FIXED_WIDTH
- `LineBreakMode` enum: WORD_WRAPPING, CHAR_WRAPPING, CLIPPING, TRUNCATE_*
- Intelligent configuration system with preset override capabilities

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

**Debugging Commands:**
```bash
# Test layout components
uv run python test_hstack_debug.py          # HStack button layout
uv run python test_vstack_debug.py          # VStack text layout  
uv run python test_professional_label.py   # Professional Label interface
uv run python examples/macui_demo_app.py   # Full demo application
```

### Layout Best Practices (Updated for Hybrid System)

With the new Hybrid Layout System, complex component usage is now seamless:

**✅ Now fully supported:**
```python
VStack(children=[
    TableView(...)  # ✅ Works perfectly with hybrid layout!
])
```

**🎯 Layout Guidelines:**
- Simple components automatically use efficient constraint-based layout
- Complex components automatically switch to frame-based layout
- Manual layout control available when needed via `layout_mode` parameter
- Responsive frame calculations for advanced positioning

## Testing Strategy

- Unit tests for reactive system in `tests/`
- Integration tests for component behavior
- Reference implementations in `examples/` for validation
- TableView: Use pure PyObjC examples to validate NSTableView functionality

## Documentation Index

Complete project documentation for design decisions, investigations, and architecture:

- **Layout System Research Report**: `docs/LAYOUT_SYSTEM_RESEARCH.md` - Comprehensive research on Auto Layout systems, modern frameworks (React Native, Flutter), and architectural recommendations for professional layout implementation
- **Layout Problem Investigation**: `docs/LAYOUT_PROBLEM_INVESTIGATION.md` - Detailed technical investigation of NSStackView negative coordinate positioning bugs, systematic debugging process, and emergency fixes applied

## Current Development Focus

1. **⚠️ Layout System Architecture Upgrade**: Transitioning from hack fixes to professional Stretchable-based layout engine (方案B)
2. **Component Library**: Expand available UI components
3. **Documentation**: Complete API documentation 
4. **Performance**: Optimize batch updates and memory usage
5. **Advanced Features**: Enhanced responsive layout capabilities