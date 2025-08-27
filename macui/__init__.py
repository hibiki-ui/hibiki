"""macUI v3.0 - A reactive UI framework for native macOS apps using Python and PyObjC

macUI v3.0 is a modern, reactive UI framework with unified component APIs and the 
powerful Stretchable layout engine. It provides signal-based reactivity with 
native macOS components, featuring a clean and consistent API design.

Key Features:
- Unified component API (Label, Button, VStack, HStack)
- Stretchable layout engine for professional layouts
- Signal-based reactive state management  
- Native macOS UI components via PyObjC
- Component-based architecture with LayoutAwareComponent
- Type-safe APIs with full IDE support

Quick Start:
    from macui import Signal, Computed, Effect
    from macui.components import Button, Label, VStack, LayoutStyle
    from macui.app import create_app
    
    # Create reactive state
    count = Signal(0)
    
    # Create UI with unified API
    button = Button("Click me", 
                   style=LayoutStyle(width=100, height=32),
                   on_click=lambda: setattr(count, 'value', count.value + 1))
    label = Label(f"Count: {count.value}", style=LayoutStyle(height=25))
    
    # Create app with modern layout
    app = create_app("My App")
    content = VStack(children=[label, button], 
                    style=LayoutStyle(gap=10, padding=20))
"""

__version__ = "3.0.0"
__author__ = "macUI Team"
__license__ = "MIT"

# Core reactive primitives
# Application framework
from .app import MacUIApp, Window, create_app, create_window

# Binding system
from .core.binding import EventBinding, ReactiveBinding, TwoWayBinding

# Component system
from .core.component import Component, For, Show, create_component
from .core.signal import Computed, Effect, Signal, batch_update

# Logging system
from .core.logging import get_logger, set_log_level

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",

    # Core reactive primitives
    "Signal",
    "Computed",
    "Effect",
    "batch_update",

    # Component system
    "Component",
    "Show",
    "For",
    "create_component",

    # Binding system
    "ReactiveBinding",
    "EventBinding",
    "TwoWayBinding",

    # Application framework
    "MacUIApp",
    "Window",
    "create_app",
    "create_window",

    # Logging system
    "get_logger",
    "set_log_level",
]

# Submodules for explicit imports
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

# Print welcome message when imported interactively
import sys

if hasattr(sys, "ps1"):  # Interactive interpreter
    print(f"macUI v{__version__} - Reactive UI framework for native macOS apps")
    print("Quick start: https://github.com/macui/macui#quick-start")
