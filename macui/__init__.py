"""macUI v2 - A reactive UI framework for native macOS apps using Python and PyObjC

macUI v2 is a modern, reactive UI framework that brings the power of signal-based 
reactivity to native macOS application development. Inspired by SolidJS, it provides
fine-grained reactivity without a virtual DOM, directly manipulating native Cocoa views.

Key Features:
- Signal-based reactive state management
- Native macOS UI components via PyObjC
- Component-based architecture
- Automatic UI updates through Effects
- Type-safe APIs with full IDE support
- Production-ready with proper lifecycle management

Quick Start:
    from macui import Signal, Computed, Effect
    from macui.components import Button, Label, VStack
    from macui.app import MacUIApp
    
    # Create reactive state
    count = Signal(0)
    count_text = Computed(lambda: f"Count: {count.value}")
    
    # Create UI
    button = Button("Click me", on_click=lambda: setattr(count, 'value', count.value + 1))
    label = Label(count_text)
    
    # Create and run app
    app = MacUIApp("My App")
    window = app.create_window("Demo", content=VStack(children=[label, button]))
    window.show()
    app.run()
"""

__version__ = "2.0.0"
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
