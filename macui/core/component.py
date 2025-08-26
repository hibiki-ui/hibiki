from typing import Any, Callable, List, Optional, TypeVar

from AppKit import NSView

from .binding import ReactiveBinding
from .signal import Computed, Effect, Signal

T = TypeVar("T")


class Component:
    """组件基类 - 提供响应式状态管理和生命周期"""

    def __init__(self):
        self._view: Optional[NSView] = None
        self._bindings: List[Callable[[], None]] = []
        self._effects: List[Effect] = []
        self._signals: List[Signal] = []
        self._computed: List[Computed] = []
        self._children: List[Component] = []
        self._mounted = False
        self._cleanup_callbacks: List[Callable[[], None]] = []

    def create_signal(self, initial_value: T) -> Signal[T]:
        """创建组件作用域的信号
        
        Args:
            initial_value: 信号的初始值
            
        Returns:
            创建的 Signal 实例
        """
        signal = Signal(initial_value)
        self._signals.append(signal)
        return signal

    def create_computed(self, fn: Callable[[], T]) -> Computed[T]:
        """创建计算属性
        
        Args:
            fn: 计算函数
            
        Returns:
            创建的 Computed 实例
        """
        computed = Computed(fn)
        self._computed.append(computed)
        return computed

    def create_effect(self, fn: Callable[[], Optional[Callable[[], None]]]) -> Effect:
        """创建副作用
        
        Args:
            fn: 副作用函数，可选返回清理函数
            
        Returns:
            创建的 Effect 实例
        """
        effect = Effect(fn)
        self._effects.append(effect)
        return effect

    def bind(self, view: NSView, prop: str, signal_or_value: Any) -> None:
        """绑定属性到视图
        
        Args:
            view: 目标视图
            prop: 属性名
            signal_or_value: 信号或静态值
        """
        cleanup_fn = ReactiveBinding.bind(view, prop, signal_or_value)
        self._bindings.append(cleanup_fn)

    def bind_multiple(self, view: NSView, bindings: dict) -> None:
        """绑定多个属性到视图
        
        Args:
            view: 目标视图
            bindings: 属性绑定字典
        """
        cleanup_fn = ReactiveBinding.bind_multiple(view, bindings)
        self._bindings.append(cleanup_fn)

    def add_child(self, child: "Component") -> None:
        """添加子组件"""
        if child not in self._children:
            self._children.append(child)

    def remove_child(self, child: "Component") -> None:
        """移除子组件"""
        if child in self._children:
            child.cleanup()
            self._children.remove(child)

    def on_cleanup(self, callback: Callable[[], None]) -> None:
        """添加清理回调"""
        self._cleanup_callbacks.append(callback)

    def mount(self) -> NSView:
        """挂载组件 - 子类需要重写
        
        Returns:
            组件的根视图
        """
        raise NotImplementedError("Component subclasses must implement mount()")

    def get_view(self) -> Optional[NSView]:
        """获取组件的根视图"""
        if not self._mounted:
            self._view = self.mount()
            self._mounted = True
            self._on_mounted()
        return self._view

    def _on_mounted(self) -> None:
        """挂载完成后的回调 - 子类可重写"""

    def cleanup(self) -> None:
        """清理组件资源"""
        # 清理所有绑定
        for cleanup_fn in self._bindings:
            try:
                cleanup_fn()
            except Exception as e:
                print(f"Binding cleanup error: {e}")
        self._bindings.clear()

        # 清理所有副作用
        for effect in self._effects:
            try:
                effect.cleanup()
            except Exception as e:
                print(f"Effect cleanup error: {e}")
        self._effects.clear()

        # 清理子组件
        for child in self._children:
            try:
                child.cleanup()
            except Exception as e:
                print(f"Child cleanup error: {e}")
        self._children.clear()

        # 调用自定义清理回调
        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Cleanup callback error: {e}")
        self._cleanup_callbacks.clear()

        # 从父视图移除
        if self._view and hasattr(self._view, "removeFromSuperview"):
            self._view.removeFromSuperview()

        self._mounted = False
        self._view = None

        # 清空信号和计算属性列表（它们会被 GC 回收）
        self._signals.clear()
        self._computed.clear()


class FunctionalComponent:
    """函数式组件包装器"""

    def __init__(self, render_fn: Callable[[], NSView], *args, **kwargs):
        self.render_fn = render_fn
        self.args = args
        self.kwargs = kwargs
        self._view = None

    def get_view(self) -> NSView:
        """获取组件视图"""
        if self._view is None:
            self._view = self.render_fn(*self.args, **self.kwargs)
        return self._view


# 工具函数
def create_component(render_fn: Callable[[], NSView]) -> Callable[..., FunctionalComponent]:
    """创建函数式组件的装饰器
    
    Usage:
        @create_component
        def MyComponent(props):
            return some_view
    """
    def wrapper(*args, **kwargs):
        return FunctionalComponent(render_fn, *args, **kwargs)
    return wrapper


# 条件渲染组件
class Show(Component):
    """条件渲染组件"""

    def __init__(self, when: Signal[bool], children_fn: Callable[[], NSView], fallback_fn: Optional[Callable[[], NSView]] = None):
        super().__init__()
        self.when = when
        self.children_fn = children_fn
        self.fallback_fn = fallback_fn
        self._current_child: Optional[NSView] = None

    def mount(self) -> NSView:
        container = NSView.alloc().init()

        def update_visibility():
            # 清除当前子视图
            if self._current_child and hasattr(self._current_child, "removeFromSuperview"):
                self._current_child.removeFromSuperview()
                self._current_child = None

            # 根据条件添加新子视图
            if self.when.value:
                self._current_child = self.children_fn()
            elif self.fallback_fn:
                self._current_child = self.fallback_fn()

            if self._current_child:
                container.addSubview_(self._current_child)

        # 创建响应式更新
        self.create_effect(update_visibility)

        return container


# 列表渲染组件
class For(Component):
    """列表渲染组件"""

    def __init__(self, items: Signal[List[T]], render_fn: Callable[[T, int], NSView], key_fn: Optional[Callable[[T], Any]] = None):
        super().__init__()
        self.items = items
        self.render_fn = render_fn
        self.key_fn = key_fn or (lambda item: id(item))
        self._rendered_items: List[NSView] = []

    def mount(self) -> NSView:
        container = NSView.alloc().init()

        def update_list():
            # 清除现有子视图
            for child in self._rendered_items:
                if hasattr(child, "removeFromSuperview"):
                    child.removeFromSuperview()
            self._rendered_items.clear()

            # 渲染新列表
            for index, item in enumerate(self.items.value):
                try:
                    child_view = self.render_fn(item, index)
                    self._rendered_items.append(child_view)
                    container.addSubview_(child_view)
                except Exception as e:
                    print(f"Error rendering list item {index}: {e}")

        # 创建响应式更新
        self.create_effect(update_list)

        return container
