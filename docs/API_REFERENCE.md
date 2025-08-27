# macUI v3.0 API Reference

本文档提供macUI框架的完整API参考，面向大语言模型和开发者，确保准确、高效地使用框架功能。

## 目录

- [Core System](#core-system)
- [Components](#components)
- [Layout System](#layout-system)
- [Animation System](#animation-system)
- [Signal System](#signal-system)
- [Application Management](#application-management)

---

## Core System

### Component Base Class

所有macUI组件的基类，提供生命周期管理和响应式集成。

```python
from macui.core import Component
from macui.layout.styles import LayoutStyle

class MyComponent(Component):
    def __init__(self):
        super().__init__()
        # 组件初始化逻辑
    
    def mount(self) -> NSView:
        # 返回NSView实例
        return view
```

**关键方法:**
- `mount()` -> `NSView`: 挂载组件，返回NSView
- `create_signal(value)` -> `Signal`: 创建组件作用域的Signal
- `create_computed(func)` -> `Computed`: 创建计算属性

### LayoutAwareComponent

支持布局系统的组件基类，继承自Component。

```python
from macui.components.core import LayoutAwareComponent

class CustomComponent(LayoutAwareComponent):
    def __init__(self, layout_style=None):
        super().__init__(layout_style=layout_style)
        # layout_style: LayoutStyle对象
    
    def create_layout_node(self):
        # 创建布局节点，在mount()中调用
        pass
```

---

## Components

### Label - 文本标签

显示静态或响应式文本的组件。

```python
from macui.components import Label, LayoutStyle

# 静态文本
label = Label("Hello World")

# 响应式文本
from macui import Signal
text_signal = Signal("动态文本")
label = Label(text_signal)

# 带样式
label = Label("文本", style=LayoutStyle(
    width=200, 
    height=30,
    padding=10
))
```

**参数:**
- `text: Union[str, Signal, Computed]` - 文本内容
- `style: Optional[LayoutStyle]` - 布局样式

**特性:**
- 自动响应式绑定：传入Signal时自动更新
- 多行文本支持
- 样式继承

### Button - 按钮组件

交互式按钮组件，支持点击事件。

```python
from macui.components import Button

def handle_click():
    print("按钮被点击")

button = Button(
    "点击我",
    style=LayoutStyle(width=100, height=35),
    on_click=handle_click
)
```

**参数:**
- `text: Union[str, Signal]` - 按钮文本
- `style: Optional[LayoutStyle]` - 布局样式  
- `on_click: Optional[Callable]` - 点击回调函数

**事件:**
- `on_click()` - 按钮点击时触发

### CustomView - 自定义视图

完全自定义的视图组件，支持绘制和事件处理。

```python
from macui.components import CustomView, DrawingUtils

def my_draw(context, rect, bounds):
    # 绘制白色背景
    DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                          (1.0, 1.0, 1.0, 1.0))
    # 绘制红色圆形
    DrawingUtils.fill_circle(context, 100, 100, 50, (1.0, 0.0, 0.0, 0.8))

def handle_mouse(x, y, event):
    print(f"鼠标点击: ({x}, {y})")

custom_view = CustomView(
    style=LayoutStyle(width=400, height=300),
    on_draw=my_draw,
    on_mouse_down=handle_mouse
)

# 设置响应式重绘
custom_view.setup_auto_redraw(my_signal)
```

**参数:**
- `style: Optional[LayoutStyle]` - 布局样式
- `on_draw: Optional[Callable]` - 绘制回调
- `on_mouse_down: Optional[Callable]` - 鼠标按下回调
- `on_mouse_up: Optional[Callable]` - 鼠标抬起回调
- `on_mouse_moved: Optional[Callable]` - 鼠标移动回调
- `on_mouse_dragged: Optional[Callable]` - 鼠标拖拽回调
- `on_key_down: Optional[Callable]` - 键盘按下回调

**方法:**
- `setup_auto_redraw(*signals)` - 设置Signal变化时自动重绘
- `redraw()` - 手动触发重绘
- `make_first_responder()` - 成为第一响应者(接收键盘事件)

**绘制回调签名:**
```python
def on_draw(context, rect, bounds):
    # context: CGContext对象
    # rect: 需要重绘的区域 NSRect
    # bounds: 视图完整边界 NSRect
    pass
```

**鼠标回调签名:**
```python
def on_mouse_event(x, y, event):
    # x, y: 鼠标在视图内的坐标
    # event: NSEvent对象
    pass
```

**键盘回调签名:**
```python
def on_key_event(key_code, characters, event):
    # key_code: 键码
    # characters: 字符串
    # event: NSEvent对象
    pass
```

---

## Layout System

### VStack - 垂直布局

垂直排列子组件的布局容器。

```python
from macui.components import VStack, Label, Button

container = VStack(
    children=[
        Label("标题"),
        Button("按钮1"),
        Button("按钮2")
    ],
    style=LayoutStyle(
        gap=10,        # 子组件间距
        padding=20,    # 内边距
        alignment=AlignItems.CENTER  # 对齐方式
    )
)
```

**参数:**
- `children: List[Component]` - 子组件列表
- `style: Optional[LayoutStyle]` - 布局样式

### HStack - 水平布局

水平排列子组件的布局容器。

```python
from macui.components import HStack

container = HStack(
    children=[label1, button1, button2],
    style=LayoutStyle(
        gap=15,
        justifyContent=JustifyContent.SPACE_BETWEEN
    )
)
```

**参数:**
- `children: List[Component]` - 子组件列表  
- `style: Optional[LayoutStyle]` - 布局样式

### LayoutStyle - 样式定义

定义组件布局样式的数据类。

```python
from macui.layout.styles import LayoutStyle, AlignItems, JustifyContent

style = LayoutStyle(
    # 尺寸
    width=200,           # 宽度
    height=100,          # 高度
    min_width=50,        # 最小宽度
    max_width=300,       # 最大宽度
    min_height=30,       # 最小高度
    max_height=200,      # 最大高度
    
    # 间距
    padding=10,          # 内边距(所有方向)
    padding_top=5,       # 上内边距
    padding_bottom=5,    # 下内边距
    padding_left=8,      # 左内边距
    padding_right=8,     # 右内边距
    margin=5,            # 外边距
    
    # Flexbox
    flex_direction=FlexDirection.COLUMN,    # 主轴方向
    align_items=AlignItems.CENTER,          # 交叉轴对齐
    justify_content=JustifyContent.START,   # 主轴对齐
    gap=10,              # 子元素间距
    
    # 显示
    display=Display.FLEX  # 显示模式
)
```

**主要属性:**
- **尺寸:** `width`, `height`, `min_width`, `max_width`, `min_height`, `max_height`
- **间距:** `padding*`, `margin*`, `gap`
- **Flexbox:** `flex_direction`, `align_items`, `justify_content`

**枚举值:**
```python
from macui.layout.styles import FlexDirection, AlignItems, JustifyContent

# 主轴方向
FlexDirection.ROW      # 水平
FlexDirection.COLUMN   # 垂直

# 对齐方式
AlignItems.START       # 起始对齐
AlignItems.CENTER      # 居中对齐
AlignItems.END         # 末尾对齐
AlignItems.STRETCH     # 拉伸

# 主轴分布
JustifyContent.START         # 起始
JustifyContent.CENTER        # 居中
JustifyContent.END           # 末尾
JustifyContent.SPACE_BETWEEN # 两端对齐
JustifyContent.SPACE_AROUND  # 环绕分布
```

---

## Animation System

### 基础动画

简单的声明式动画API。

```python
from macui.animation import animate

# 简单动画
animate(view, duration=0.5, opacity=0.8, scale=1.2)
```

### 预设动画效果

#### ShinyText - 光泽扫过文字

```python
from macui.animation import ShinyText

# CSS风格的光泽扫过效果
shiny = ShinyText(
    speed=5.0,         # 动画速度(秒)
    disabled=False,    # 是否禁用
    intensity=0.8      # 光泽强度
)

# 应用到文本视图
animation = shiny.apply_to(text_field)

# 停止动画
shiny.stop_animation()
```

#### 其他动画效果

```python
from macui.animation import FadeIn, SlideIn, Scale

# 淡入效果
fade = FadeIn(duration=1.0, from_opacity=0.0)
fade.apply_to(view)

# 滑入效果
slide = SlideIn(duration=0.8, direction="left", distance=100.0)
slide.apply_to(view)

# 缩放效果
scale = Scale(duration=0.5, from_scale=0.0, to_scale=1.0)
scale.apply_to(view)
```

### DrawingUtils - 绘制工具

用于CustomView的绘制辅助函数。

```python
from macui.components import DrawingUtils

def my_draw(context, rect, bounds):
    # 填充矩形 - (x, y, width, height, color)
    DrawingUtils.fill_rect(context, 0, 0, 200, 100, (1.0, 0.0, 0.0, 0.8))
    
    # 描边矩形 - (x, y, width, height, color, line_width)
    DrawingUtils.stroke_rect(context, 10, 10, 180, 80, (0.0, 0.0, 1.0, 1.0), 2.0)
    
    # 填充圆形 - (center_x, center_y, radius, color)
    DrawingUtils.fill_circle(context, 100, 50, 30, (0.0, 1.0, 0.0, 0.6))
    
    # 绘制线条 - (from_x, from_y, to_x, to_y, color, line_width)
    DrawingUtils.draw_line(context, 0, 0, 200, 100, (0.0, 0.0, 0.0, 1.0), 1.0)
    
    # 绘制文本 - (text, x, y, font_size, color)
    DrawingUtils.draw_text(context, "Hello", 10, 10, 16, (0.0, 0.0, 0.0, 1.0))
```

**颜色格式:** 所有颜色使用 `(red, green, blue, alpha)` 格式，值范围 0.0-1.0。

---

## Signal System

### Signal - 响应式状态

```python
from macui import Signal

# 创建Signal
count = Signal(0)              # 数字
text = Signal("Hello")         # 字符串  
items = Signal([])             # 列表
data = Signal({"key": "value"}) # 字典

# 读取值
current_value = count.value

# 设置值 (触发响应式更新)
count.value = 5
text.value = "World"
items.value = [1, 2, 3]
```

### Computed - 计算属性

```python
from macui import Computed

count = Signal(0)

# 创建计算属性
doubled = Computed(lambda: count.value * 2)
is_even = Computed(lambda: count.value % 2 == 0)

# 读取计算值
print(doubled.value)  # 自动重新计算
```

### Effect - 副作用

```python
from macui.core.signal import Effect

count = Signal(0)

# 创建Effect - 当依赖的Signal变化时自动执行
def log_count():
    print(f"当前计数: {count.value}")

effect = Effect(log_count)

# count变化时会自动执行log_count
count.value = 1  # 输出: "当前计数: 1"
count.value = 2  # 输出: "当前计数: 2"
```

**注意:** Effect会自动跟踪函数内读取的Signal，建立依赖关系。

---

## Application Management

### 创建应用

```python
from macui.app import create_app
from AppKit import NSWindow, NSMakeRect
from PyObjCTools import AppHelper

# 创建应用
app = create_app("My App")

# 创建窗口
window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    NSMakeRect(100, 100, 800, 600),
    NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
    NSBackingStoreBuffered,
    False
)

window.setTitle_("My macUI App")
window.makeKeyAndOrderFront_(None)

# 设置根组件
root_component = MyRootComponent()
window.setContentView_(root_component.mount())

# 启动事件循环
AppHelper.runEventLoop()
```

---

## 常见模式

### 1. 响应式组件

```python
class CounterComponent(Component):
    def __init__(self):
        super().__init__()
        self.count = Signal(0)
    
    def mount(self):
        label = Label(self.count.value)
        button = Button("增加", on_click=self._increment)
        
        return VStack([label, button]).mount()
    
    def _increment(self):
        self.count.value += 1
```

### 2. 自定义绘制组件

```python
class ChartComponent(Component):
    def __init__(self):
        super().__init__()
        self.data = Signal([10, 20, 15, 25])
    
    def mount(self):
        chart = CustomView(
            style=LayoutStyle(width=400, height=200),
            on_draw=self._draw_chart
        )
        
        # 数据变化时自动重绘
        chart.setup_auto_redraw(self.data)
        
        return chart.mount()
    
    def _draw_chart(self, context, rect, bounds):
        data = self.data.value
        # 绘制图表...
```

### 3. 事件处理

```python
class InteractiveComponent(Component):
    def __init__(self):
        super().__init__()
        self.mouse_pos = Signal((0, 0))
        self.clicked_points = Signal([])
    
    def mount(self):
        canvas = CustomView(
            style=LayoutStyle(width=300, height=200),
            on_draw=self._draw,
            on_mouse_down=self._handle_click,
            on_mouse_moved=self._handle_move
        )
        
        canvas.setup_auto_redraw(self.mouse_pos, self.clicked_points)
        return canvas.mount()
    
    def _handle_click(self, x, y, event):
        points = self.clicked_points.value.copy()
        points.append((x, y))
        self.clicked_points.value = points
    
    def _handle_move(self, x, y, event):
        self.mouse_pos.value = (x, y)
```

---

## 类型提示

macUI支持完整的类型提示，建议使用：

```python
from typing import List, Optional, Callable, Union
from macui import Signal, Computed
from macui.components import Component, LayoutStyle
from AppKit import NSView

class MyComponent(Component):
    def __init__(self, data: List[str]) -> None:
        super().__init__()
        self.data: Signal[List[str]] = Signal(data)
    
    def mount(self) -> NSView:
        # 实现...
        pass
    
    def handle_click(self) -> None:
        # 实现...
        pass
```

---

## 最佳实践

1. **使用Signal管理状态** - 避免直接修改组件属性
2. **合理使用Effect** - 用于副作用，不要在其中修改其他Signal
3. **组件职责单一** - 每个组件专注一个功能
4. **响应式重绘** - CustomView使用`setup_auto_redraw()`
5. **事件处理安全** - 使用try-catch包装事件回调
6. **内存管理** - 组件销毁时清理资源

---

## 版本信息

- **当前版本:** 3.0
- **最后更新:** 2025-08-27
- **兼容性:** macOS 10.14+, Python 3.8+

---

*本文档随macUI框架同步更新，确保API信息的准确性和完整性。*