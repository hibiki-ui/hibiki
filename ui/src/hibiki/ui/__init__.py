#!/usr/bin/env python3
"""
Hibiki UI - Reactive UI Framework for Native macOS Applications

Hibiki UI is a modern, Hibiki UI framework for building native macOS applications with Python and PyObjC.
It combines signal-based reactivity with native macOS components, providing a clean and powerful API
for creating responsive user interfaces.

## 🎯 Core Design Philosophy

**Reactive First**: Built around Signal, Computed, and Effect primitives for fine-grained reactivity
**Native Performance**: Direct PyObjC integration with native NSView components  
**Developer Experience**: Clean, type-safe APIs with comprehensive IDE support
**Professional Layouts**: Advanced layout system with flexbox-style controls
**Pure Core Animation**: GPU-accelerated animations using only Core Animation APIs

## 🏗️ Architecture Overview

```
Application Layer (Your Code)
       ↓
Component System (Label, Button, Container)
       ↓
Reactive System (Signal, Computed, Effect) ← CORE
       ↓
Binding Layer (ReactiveBinding, property binding)
       ↓
AppKit/PyObjC (NSView, NSButton, etc.)
```

## 🚀 Quick Start

```python
from hibiki.ui import Signal, Computed, Effect
from hibiki.ui import Label, Button, Container, ComponentStyle, px
from hibiki.ui import ManagerFactory

# Create reactive state
count = Signal(0)
double_count = Computed(lambda: count.value * 2)

# Create UI components
button = Button("Click me", 
               style=ComponentStyle(width=px(100), height=px(32)),
               on_click=lambda: setattr(count, 'value', count.value + 1))

label = Label(lambda: f"Count: {count.value}, Double: {double_count.value}",
             style=ComponentStyle(height=px(25)))

# Create layout container
container = Container(
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
window = app_manager.create_window("My App", 400, 300)
window.set_content(container)
app_manager.run()
```

## 🧩 Core Components

### Reactive System
- **Signal**: Reactive state primitive for mutable values
- **Computed**: Derived values that automatically update
- **Effect**: Side effects that run when dependencies change

### Component System  
- **UIComponent**: Base class for all UI components
- **Container**: Layout container with flexbox-style controls
- **Basic Components**: Label, Button, TextField, Slider, Switch
- **Advanced Components**: TextArea, Checkbox, RadioButton, ProgressBar, ImageView
- **Selection Components**: PopUpButton, ComboBox

### Layout System
- **ComponentStyle**: Comprehensive styling system
- **Layout Engine**: Professional flexbox-style layout
- **Responsive Design**: Flexible sizing and positioning

### Animation System
- **Pure Core Animation**: GPU-accelerated animations only
- **Declarative API**: Simple animate() function with preset effects
- **Signal Integration**: Reactive animations tied to state changes

### Theme System
- **ThemeManager**: Centralized theme management
- **ColorScheme**: System and custom color schemes  
- **AppearanceMode**: Light/dark mode support
- **Reactive Theming**: Themes update with Signal changes

## 🎨 Animation Design Principles

**GPU First**: All animations use Core Animation APIs for maximum performance
**No Threading**: Strictly prohibits time.sleep(), threading, or custom timing
**Declarative API**: Simple animate() calls hide Core Animation complexity
**Signal Integration**: Animations react to Signal state changes

```python
from hibiki.ui import animate, fade_in, bounce

# Simple declarative animations
animate(view, duration=0.5, opacity=0.8, scale=1.2)

# Preset effect chains
fade_in(view, duration=1.0).then(bounce(scale=1.1))

# Signal-reactive animations  
effect = Effect(lambda: animate(label, opacity=1.0 if visible.value else 0.3))
```

## 📊 Performance Features

**Reaktiv-Inspired Optimizations**:
- Version control system for intelligent dependency tracking
- Batch processing with deduplication for minimal UI updates
- Smart caching to avoid unnecessary recomputations
- Global version tracking for optimal performance

**Memory Management**:
- Component-scoped signal lifecycles
- Automatic Effect cleanup on component destruction  
- Efficient observer pattern with weak references

## 🔧 Advanced Usage

### Custom Components
```python
class MyCustomComponent(UIComponent):
    def __init__(self, data: Signal):
        super().__init__()
        self.data = data
        
    def _create_nsview(self) -> NSView:
        view = NSView.alloc().init()
        # Custom implementation
        return view
```

### Form Handling
```python
from hibiki.ui import Form, FormField, RequiredValidator, EmailValidator

form = Form([
    FormField("email", TextField(), [RequiredValidator(), EmailValidator()]),
    FormField("name", TextField(), [RequiredValidator()])
])
```

### Theme Customization
```python
from hibiki.ui import set_theme, get_theme_manager

theme_manager = get_theme_manager()
theme_manager.set_color_scheme("ocean")
set_theme("dark")
```

## 🧪 Testing & Debugging

Built-in debugging features:
- Comprehensive logging system
- Layout calculation visibility
- Reactive dependency tracking
- Performance metrics

## 📚 Key Concepts

**Signal-based Reactivity**: All UI updates flow from Signal changes through Computed 
values to Effect side-effects, ensuring predictable and efficient updates.

**Component Lifecycle**: Components follow mount/unmount patterns with automatic 
resource cleanup and proper NSView management.

**Professional Layouts**: The layout system provides flexbox-style controls with 
precise positioning, sizing, and responsive design capabilities.

**Native Integration**: Direct PyObjC usage ensures maximum performance and full 
access to native macOS functionality.

---

For complete documentation, examples, and guides, see the project repository.
"""

# 核心系统
from .core import (
    Component, UIComponent, Container,
    Signal, Computed, Effect, create_signal, create_computed, create_effect,
    ComponentStyle, StylePresets, px, percent, auto,
    Display, FlexDirection, JustifyContent, AlignItems, LengthUnit,
    ReactiveBinding, FormDataBinding,
    TextProps, TextStyles, text_props,
    get_layout_engine, LayoutNode, LayoutEngine,
    ManagerFactory,
    Animation, AnimationGroup, AnimationManager,
    AnimationCurve, AnimationProperty, AnimationState,
    animate, fade_in, fade_out, bounce
)

# 响应式布局系统
from .core.responsive import (
    ResponsiveStyle, ResponsiveManager, BreakpointManager, BreakpointName,
    responsive_style, breakpoint_style, media_query_style,
    get_responsive_manager
)

# 组件系统
from .components import (
    # 基础组件
    Label, Button, TextField, Slider, Switch,
    # 扩展输入组件
    TextArea, Checkbox, RadioButton,
    # 显示组件
    ProgressBar, ImageView,
    # 选择组件
    PopUpButton, ComboBox,
    # 表格组件
    TableView, TableColumn,
    # 自定义组件
    CustomView, DrawingUtils
)

# 主题系统
from .theme import (
    ThemeManager, Theme, PresetThemes, ThemeChangeEvent,
    get_theme_manager, get_current_theme, set_theme, get_color, get_font,
    ColorScheme, SystemColors, ColorRole, PresetColorSchemes,
    FontScheme, SystemFonts, TextStyle, PresetFontSchemes,
    AppearanceManager, AppearanceMode,
    get_appearance_manager, is_dark_mode, add_appearance_observer
)

# 调试工具
from .utils import (
    ScreenshotTool, capture_app_screenshot, debug_view_layout
)

__all__ = [
    # 核心系统
    'Component', 'UIComponent', 'Container',
    'Signal', 'Computed', 'Effect', 'create_signal', 'create_computed', 'create_effect',
    'ComponentStyle', 'StylePresets', 'px', 'percent', 'auto',
    'Display', 'FlexDirection', 'JustifyContent', 'AlignItems', 'LengthUnit',
    'ReactiveBinding', 'FormDataBinding',
    'TextProps', 'TextStyles', 'text_props',
    'get_layout_engine', 'LayoutNode', 'LayoutEngine',
    'ManagerFactory',
    'Animation', 'AnimationGroup', 'AnimationManager',
    'AnimationCurve', 'AnimationProperty', 'AnimationState',
    'animate', 'fade_in', 'fade_out', 'bounce',
    
    # 响应式布局系统
    'ResponsiveStyle', 'ResponsiveManager', 'BreakpointManager', 'BreakpointName',
    'responsive_style', 'breakpoint_style', 'media_query_style',
    'get_responsive_manager',
    
    # 组件系统
    'Label', 'Button', 'TextField', 'Slider', 'Switch',
    'TextArea', 'Checkbox', 'RadioButton',
    'ProgressBar', 'ImageView',
    'PopUpButton', 'ComboBox',
    'TableView', 'TableColumn',
    'CustomView', 'DrawingUtils',
    
    # 主题系统
    'ThemeManager', 'Theme', 'PresetThemes', 'ThemeChangeEvent',
    'get_theme_manager', 'get_current_theme', 'set_theme', 'get_color', 'get_font',
    'ColorScheme', 'SystemColors', 'ColorRole', 'PresetColorSchemes',
    'FontScheme', 'SystemFonts', 'TextStyle', 'PresetFontSchemes',
    'AppearanceManager', 'AppearanceMode',
    'get_appearance_manager', 'is_dark_mode', 'add_appearance_observer',
    
    # 调试工具
    'ScreenshotTool', 'capture_app_screenshot', 'debug_view_layout'
]