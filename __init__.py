"""
macUI v2 - 基于信号机制的声明式 macOS 原生应用开发框架

macUI v2 使用响应式信号系统，提供细粒度更新，无虚拟DOM开销，直接操作原生视图。
设计灵感来自 SolidJS，特别适合 Python + PyObjC 开发 macOS 应用。

核心特性:
- 无虚拟DOM，直接操作 NSView
- 细粒度响应式更新
- 原生 AppKit 和 Core Animation 支持
- 零限制访问 macOS API
- 高性能批量更新机制

Example:
    from macui import *
    
    class CounterApp(Component):
        def __init__(self):
            super().__init__()
            self.count = self.create_signal(0)
        
        def increment(self):
            self.count.value += 1
        
        def mount(self):
            return VStack(spacing=20, children=[
                Label(Computed(lambda: f"Count: {self.count.value}")),
                Button("Increment", on_click=self.increment)
            ])
    
    if __name__ == "__main__":
        app = MacUIApp("Counter Demo")
        window = app.create_window("Counter", size=(400, 300), content=CounterApp())
        window.show()
        app.run()
"""

# 版本信息
__version__ = "2.0.0-alpha"
__author__ = "macui Team"
__license__ = "MIT"

# 核心响应式系统
from .core.signal import Signal, Computed, Effect, batch_update
from .core.binding import ReactiveBinding, TwoWayBinding, EventBinding
from .core.component import Component, FunctionalComponent, Show, For, create_component

# UI 组件
from .components.controls import (
    Button, TextField, Label, Slider, Switch, ImageView
)
from .components.layout import (
    VStack, HStack, ZStack, ScrollView,
    ResponsiveStack, VStackResponsive, HStackResponsive
)

# 应用程序和窗口管理
from .app import MacUIApp, Window, create_app, create_window

# 便捷导出
__all__ = [
    # 版本信息
    '__version__', '__author__', '__license__',
    
    # 核心响应式系统
    'Signal', 'Computed', 'Effect', 'batch_update',
    'ReactiveBinding', 'TwoWayBinding', 'EventBinding',
    'Component', 'FunctionalComponent', 'Show', 'For', 'create_component',
    
    # UI 组件 - 控件
    'Button', 'TextField', 'Label', 'Slider', 'Switch', 'ImageView',
    
    # UI 组件 - 布局
    'VStack', 'HStack', 'ZStack', 'ScrollView',
    'ResponsiveStack', 'VStackResponsive', 'HStackResponsive',
    
    # 应用程序管理
    'MacUIApp', 'Window', 'create_app', 'create_window',
]

# 检查 PyObjC 可用性 - macUI v2 必需依赖
import objc
from AppKit import NSApplication

# 打印欢迎信息
if __name__ != "__main__":
    print(f"macUI v2 {__version__} - Reactive Native macOS UI Framework")
    print(f"PyObjC {objc.__version__ if hasattr(objc, '__version__') else 'installed'} - Ready for macOS development")

# 开发者工具
def _debug_info():
    """打印调试信息"""
    print(f"""
macUI v2 Debug Info:
==================
Version: {__version__}
PyObjC Available: {APPKIT_AVAILABLE}
Components Loaded: {len(__all__)} modules
    """)

# 框架示例和教程
def _show_examples():
    """显示使用示例"""
    examples = """
macUI v2 Usage Examples:
=======================

1. Simple Counter:
    from macui import *
    
    class Counter(Component):
        def __init__(self):
            super().__init__()
            self.count = self.create_signal(0)
        
        def mount(self):
            return VStack(spacing=20, children=[
                Label(Computed(lambda: f"Count: {self.count.value}")),
                Button("Click me!", on_click=lambda: setattr(self.count, 'value', self.count.value + 1))
            ])

2. Text Input:
    class TextDemo(Component):
        def __init__(self):
            super().__init__()
            self.text = self.create_signal("")
        
        def mount(self):
            return VStack(spacing=10, children=[
                TextField(value=self.text, placeholder="Type here..."),
                Label(Computed(lambda: f"You typed: {self.text.value}"))
            ])

3. Todo List:
    class TodoList(Component):
        def __init__(self):
            super().__init__()
            self.todos = self.create_signal([])
            self.input_text = self.create_signal("")
        
        def add_todo(self):
            if self.input_text.value.strip():
                self.todos.value = self.todos.value + [self.input_text.value.strip()]
                self.input_text.value = ""
        
        def mount(self):
            return VStack(spacing=10, children=[
                HStack(spacing=10, children=[
                    TextField(value=self.input_text, placeholder="New todo..."),
                    Button("Add", on_click=self.add_todo)
                ]),
                For(items=self.todos, render=lambda todo, i: Label(todo))
            ])

4. Full Application:
    if __name__ == "__main__":
        app = MacUIApp("My App")
        window = app.create_window("Demo", size=(500, 400), content=Counter())
        window.show()
        app.run()
    """
    print(examples)

# 将工具函数添加到模块
debug_info = _debug_info
show_examples = _show_examples