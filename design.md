# macui v2 设计文档

## 概述

macui v2 是一个基于信号机制的声明式 macOS 原生应用开发框架，使用 Python + PyObjC 实现。它的设计灵感来自 SolidJS，提供细粒度响应式更新，无虚拟DOM开销，直接操作原生视图。

## 核心设计原则

1. **无虚拟DOM** - 直接操作 NSView，避免中间层开销
2. **细粒度响应** - 只更新实际变化的属性
3. **原生优先** - 充分利用 AppKit 和 Core Animation
4. **零限制** - 可访问所有 macOS API
5. **高性能** - 最小化 Python-ObjC 桥接调用

## 架构

```
┌─────────────────────────────────────┐
│         Application Layer           │
│    (用户代码：组件、业务逻辑)        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│       Component System              │
│  (Component, mount, lifecycle)      │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│     Reactive System (核心)          │
│  (Signal, Computed, Effect)         │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Binding Layer                  │
│  (ReactiveBinding, 属性绑定)        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│        AppKit/PyObjC                │
│    (NSView, NSButton, etc.)         │
└─────────────────────────────────────┘
```

## 核心API

### 1. 响应式原语

```python
# 信号 - 基础响应式值
count = Signal(0)
count.value  # 读取
count.value = 1  # 设置

# 计算属性 - 自动缓存的派生值
double = Computed(lambda: count.value * 2)
double.value  # 读取（只读）

# 副作用 - 自动重新运行
Effect(lambda: print(f"Count is now {count.value}"))
```

### 2. 组件系统

```python
class MyComponent(Component):
    def __init__(self):
        super().__init__()
        # 创建响应式状态
        self.state = self.create_signal(initial_value)
        self.computed = self.create_computed(lambda: ...)
        
    def mount(self):
        """返回原生NSView"""
        return self.build_view()
```

### 3. 视图绑定

```python
# 文本绑定
ReactiveBinding.bind(label, 'text', signal)

# 可见性绑定
ReactiveBinding.bind(view, 'hidden', computed)

# 样式绑定
ReactiveBinding.bind(view, 'style', {
    'background': color_signal,
    'alpha': opacity_signal
})
```

### 4. 条件和列表渲染

```python
# 条件渲染
Show(when=is_visible_signal, children_fn=lambda: create_view())

# 列表渲染
For(items=todos_signal, render_fn=lambda item: create_item_view(item))
```

## 实现细节

### Signal 实现

```python
from weakref import WeakSet
from contextvars import ContextVar
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar('T')

class Signal(Generic[T]):
    _current_observer: ContextVar[Optional[Callable]] = ContextVar('observer', default=None)
    
    def __init__(self, initial_value: T):
        self._value = initial_value
        self._observers = WeakSet()
    
    def get(self) -> T:
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
        return self._value
    
    def set(self, new_value: T) -> None:
        if self._value != new_value:
            self._value = new_value
            # 批量更新优化
            batch_update(lambda: 
                [observer() for observer in list(self._observers)]
            )
    
    value = property(get, set)
```

### Computed 实现

```python
class Computed(Generic[T]):
    def __init__(self, fn: Callable[[], T]):
        self._fn = fn
        self._value: Optional[T] = None
        self._dirty = True
        self._observers = WeakSet()
    
    def get(self) -> T:
        if self._dirty:
            # 收集依赖
            token = Signal._current_observer.set(self._invalidate)
            try:
                self._value = self._fn()
                self._dirty = False
            finally:
                Signal._current_observer.reset(token)
        
        # 向上传播依赖
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
        
        return self._value
    
    def _invalidate(self):
        if not self._dirty:  # 避免重复失效
            self._dirty = True
            for observer in list(self._observers):
                observer()
    
    value = property(get)
```

### 批量更新系统

```python
from collections import deque

class BatchUpdater:
    def __init__(self):
        self._queue = deque()
        self._scheduled = False
    
    def batch_update(self, fn):
        """批量执行更新，避免多次渲染"""
        self._queue.append(fn)
        if not self._scheduled:
            self._scheduled = True
            # 使用performSelector延迟到下一个运行循环
            self._flush_updates()
    
    def _flush_updates(self):
        # 开始批量事务
        CATransaction.begin()
        CATransaction.setDisableActions_(True)
        
        while self._queue:
            update = self._queue.popleft()
            update()
        
        CATransaction.commit()
        self._scheduled = False

batch_updater = BatchUpdater()
batch_update = batch_updater.batch_update
```

### ReactiveBinding 实现

```python
class ReactiveBinding:
    """绑定信号到NSView属性"""
    
    # 属性设置器映射
    SETTERS = {
        'text': lambda v, val: v.setStringValue_(str(val)),
        'hidden': lambda v, val: v.setHidden_(bool(val)),
        'enabled': lambda v, val: v.setEnabled_(bool(val)),
        'alpha': lambda v, val: v.setAlphaValue_(float(val)),
        'frame': lambda v, val: v.setFrame_(val),
        # 扩展更多...
    }
    
    @staticmethod
    def bind(view, prop, signal_or_value):
        """创建响应式绑定"""
        setter = ReactiveBinding.SETTERS.get(prop)
        if not setter:
            raise ValueError(f"Unknown property: {prop}")
        
        def update():
            if hasattr(signal_or_value, 'value'):
                value = signal_or_value.value
            elif callable(signal_or_value):
                value = signal_or_value()
            else:
                value = signal_or_value
            
            setter(view, value)
        
        # 初始更新
        update()
        
        # 设置响应式更新
        if hasattr(signal_or_value, '_observers'):
            signal_or_value._observers.add(update)
        
        return update  # 返回以便手动解绑
```

### Component 基类

```python
import objc
from AppKit import NSView

class Component:
    """组件基类"""
    
    def __init__(self):
        self._view: Optional[NSView] = None
        self._bindings = []
        self._effects = []
        self._children = []
    
    def create_signal(self, initial):
        """创建组件作用域的信号"""
        signal = Signal(initial)
        return signal
    
    def create_computed(self, fn):
        """创建计算属性"""
        return Computed(fn)
    
    def create_effect(self, fn):
        """创建副作用"""
        effect = Effect(fn)
        self._effects.append(effect)
        return effect
    
    def mount(self) -> NSView:
        """子类需要实现 - 返回NSView"""
        raise NotImplementedError
    
    def cleanup(self):
        """清理资源"""
        for effect in self._effects:
            effect.cleanup()
        self._effects.clear()
        self._bindings.clear()
```

## 内置组件

### 布局组件

```python
def VStack(spacing=0, padding=0, alignment='center', children=None):
    """垂直栈"""
    stack = NSStackView.alloc().init()
    stack.setOrientation_(NSUserInterfaceLayoutOrientationVertical)
    stack.setSpacing_(spacing)
    stack.setAlignment_(ALIGNMENT_MAP[alignment])
    
    if children:
        for child in children:
            if isinstance(child, Component):
                child = child.mount()
            stack.addArrangedSubview_(child)
    
    if padding:
        stack.setEdgeInsets_((padding, padding, padding, padding))
    
    return stack

def HStack(spacing=0, padding=0, alignment='center', children=None):
    """水平栈"""
    # 类似实现...
```

### 基础控件

```python
def Button(title, on_click=None, enabled=None):
    """响应式按钮"""
    button = NSButton.alloc().init()
    
    # 标题绑定
    if isinstance(title, (Signal, Computed)):
        ReactiveBinding.bind(button, 'title', title)
    else:
        button.setTitle_(title)
    
    # 启用状态绑定
    if enabled is not None:
        ReactiveBinding.bind(button, 'enabled', enabled)
    
    # 点击处理
    if on_click:
        button.setTarget_(button)
        button.setAction_(SEL(b'performClick:'))
        objc.setAssociatedObject(button, 'click_handler', on_click)
    
    return button

def TextField(value=None, placeholder="", on_change=None):
    """双向绑定的文本框"""
    field = NSTextField.alloc().init()
    field.setPlaceholderString_(placeholder)
    
    if value:
        # 单向绑定
        ReactiveBinding.bind(field, 'text', value)
        
        # 双向绑定
        if hasattr(value, 'set'):
            delegate = TextFieldDelegate.alloc().init()
            delegate.signal = value
            field.setDelegate_(delegate)
    
    return field
```

## 使用示例

### 简单计数器

```python
from macui import *

class CounterApp(Component):
    def __init__(self):
        super().__init__()
        self.count = self.create_signal(0)
        self.double = self.create_computed(lambda: self.count.value * 2)
    
    def increment(self):
        self.count.value += 1
    
    def decrement(self):
        self.count.value -= 1
    
    def mount(self):
        return VStack(spacing=20, padding=40, children=[
            Label(Computed(lambda: f"Count: {self.count.value}")),
            Label(Computed(lambda: f"Double: {self.double.value}")),
            HStack(spacing=10, children=[
                Button("Increment", on_click=self.increment),
                Button("Decrement", on_click=self.decrement),
                Button(
                    "Reset", 
                    on_click=lambda: setattr(self.count, 'value', 0),
                    enabled=Computed(lambda: self.count.value != 0)
                )
            ])
        ])

# 启动应用
if __name__ == "__main__":
    app = MacUIApp()
    window = Window(
        title="Counter Demo",
        size=(400, 300),
        content=CounterApp()
    )
    app.run()
```

### TodoMVC

```python
class TodoApp(Component):
    def __init__(self):
        super().__init__()
        self.todos = self.create_signal([])
        self.input = self.create_signal("")
        self.filter = self.create_signal("all")
        
        self.filtered_todos = self.create_computed(lambda:
            self._filter_todos(self.todos.value, self.filter.value)
        )
    
    def add_todo(self):
        if text := self.input.value.strip():
            self.todos.value = self.todos.value + [{
                'id': len(self.todos.value),
                'text': text,
                'done': False
            }]
            self.input.value = ""
    
    def toggle_todo(self, todo_id):
        todos = self.todos.value.copy()
        for todo in todos:
            if todo['id'] == todo_id:
                todo['done'] = not todo['done']
        self.todos.value = todos
    
    def mount(self):
        return VStack(spacing=20, children=[
            # 输入区
            HStack(spacing=10, children=[
                TextField(
                    value=self.input,
                    placeholder="What needs to be done?",
                    on_enter=self.add_todo
                ),
                Button("Add", on_click=self.add_todo)
            ]),
            
            # 过滤器
            SegmentedControl(
                options=["All", "Active", "Done"],
                value=self.filter
            ),
            
            # Todo列表
            ScrollView(
                For(
                    items=self.filtered_todos,
                    key=lambda t: t['id'],
                    render=lambda todo: self.render_todo_item(todo)
                )
            ),
            
            # 统计
            Label(Computed(lambda: 
                f"{len([t for t in self.todos.value if not t['done']])} items left"
            ))
        ])
```

## 高级特性

### 动画集成

```python
def animate(view, duration=0.3, **properties):
    """声明式动画"""
    CATransaction.begin()
    CATransaction.setAnimationDuration_(duration)
    
    for prop, value_signal in properties.items():
        if prop == 'position':
            animation = CABasicAnimation.animationWithKeyPath_("position")
            animation.setToValue_(NSValue.valueWithPoint_(value_signal.value))
            view.layer().addAnimation_forKey_(animation, prop)
    
    CATransaction.commit()
```

### 全局状态管理

```python
class Store:
    """全局响应式存储"""
    
    def __init__(self):
        self._state = {}
    
    def create_slice(self, name, initial):
        self._state[name] = Signal(initial)
        return self._state[name]
    
    def get(self, name):
        return self._state.get(name)

# 使用
store = Store()
user = store.create_slice('user', {'name': '', 'id': None})
theme = store.create_slice('theme', 'light')
```

## 开发路线图

### Phase 1 - MVP (核心功能)
- [x] Signal/Computed/Effect 实现
- [x] 基础 ReactiveBinding
- [x] Component 系统
- [ ] 基础控件 (Button, TextField, Label)
- [ ] 布局组件 (VStack, HStack)
- [ ] Window 管理

### Phase 2 - 基础组件
- [ ] 更多控件 (Slider, Switch, Select)
- [ ] ScrollView
- [ ] For/Show 组件
- [ ] 样式系统
- [ ] 事件处理优化

### Phase 3 - 高级特性
- [ ] 动画 API
- [ ] 全局状态管理
- [ ] 路由系统
- [ ] 热重载支持
- [ ] 开发者工具

### Phase 4 - 生态
- [ ] CLI 工具
- [ ] 项目模板
- [ ] 组件库
- [ ] 文档和教程

## 性能考虑

1. **批量更新** - 使用 CATransaction 批量处理
2. **懒计算** - Computed 自动缓存
3. **弱引用** - 避免循环引用
4. **最小桥接** - 减少 Python-ObjC 调用
5. **原生动画** - 使用 Core Animation

## 注意事项

1. 所有 UI 操作必须在主线程
2. 使用 `objc.python_method` 装饰器优化 Python 方法
3. 大列表使用虚拟化
4. 避免在 render 中创建新函数
5. 合理使用 Computed 缓存

## 开始开发

```bash
# 依赖
pip install pyobjc-core pyobjc-framework-Cocoa

# 项目结构
macui/
  core/
    signal.py      # 响应式系统
    component.py   # 组件基类
    binding.py     # 视图绑定
  components/
    layout.py      # 布局组件
    controls.py    # 控件组件
  app.py          # 应用入口
  window.py       # 窗口管理
```

## 许可

MIT License - 自由使用和修改

---

这个设计文档为 macui v2 提供了完整的技术规范。基于信号机制的架构避免了虚拟DOM的开销，特别适合 PyObjC 的使用场景。核心理念是：**响应式但不虚拟，声明式但仍原生**。

