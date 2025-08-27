# macUI自定义视图开发指南

本指南介绍如何在macUI框架中创建完全自定义的视图组件，包括自定义绘制、事件处理和响应式状态管理。

## 核心组件

### CustomView组件

`CustomView`是macUI提供的自定义视图基础组件，支持：

- **自定义绘制**: 通过CoreGraphics进行2D绘制
- **鼠标事件**: 点击、拖拽、移动等完整鼠标交互
- **键盘事件**: 键盘输入处理
- **响应式状态**: 与macUI Signal系统无缝集成

### 基本使用

```python
from macui.components import CustomView, LayoutStyle

def my_draw_function(context, rect, bounds):
    # 自定义绘制逻辑
    DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                          (1.0, 1.0, 1.0, 1.0))  # 白色背景

def my_mouse_handler(x, y, event):
    print(f"鼠标点击位置: ({x}, {y})")

custom_view = CustomView(
    style=LayoutStyle(width=400, height=300),
    on_draw=my_draw_function,
    on_mouse_down=my_mouse_handler
)
```

## 事件处理

### 鼠标事件

```python
CustomView(
    on_mouse_down=lambda x, y, event: print(f"按下: {x}, {y}"),
    on_mouse_up=lambda x, y, event: print(f"抬起: {x}, {y}"),
    on_mouse_moved=lambda x, y, event: print(f"移动: {x}, {y}"),
    on_mouse_dragged=lambda x, y, event: print(f"拖拽: {x}, {y}")
)
```

### 键盘事件

```python
def handle_key(key_code, characters, event):
    if characters == ' ':
        print("空格键被按下")
    elif characters.lower() == 'c':
        print("C键被按下")

CustomView(
    on_key_down=handle_key
)
```

**注意**: 视图需要成为第一响应者才能接收键盘事件：
```python
custom_view.make_first_responder()
```

## 自定义绘制

### 使用DrawingUtils

macUI提供了`DrawingUtils`工具类，简化常见的绘制操作：

```python
def draw_shapes(context, rect, bounds):
    # 填充背景
    DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                          (0.9, 0.9, 0.9, 1.0))
    
    # 绘制圆形
    DrawingUtils.fill_circle(context, 100, 100, 50, (1.0, 0.0, 0.0, 0.8))
    
    # 绘制线条
    DrawingUtils.draw_line(context, 0, 0, bounds.size.width, bounds.size.height, 
                          (0.0, 0.0, 1.0, 1.0), 2.0)
    
    # 绘制文本
    DrawingUtils.draw_text(context, "Hello macUI", 10, 10, 16, (0, 0, 0, 1))
```

### 可用绘制方法

- `fill_rect(context, x, y, width, height, color)` - 填充矩形
- `stroke_rect(context, x, y, width, height, color, line_width)` - 描边矩形  
- `fill_circle(context, center_x, center_y, radius, color)` - 填充圆形
- `draw_line(context, from_x, from_y, to_x, to_y, color, line_width)` - 绘制线条
- `draw_text(context, text, x, y, font_size, color)` - 绘制文本

### 颜色格式

所有颜色使用RGBA元组格式: `(red, green, blue, alpha)`，值范围0.0-1.0。

```python
red = (1.0, 0.0, 0.0, 1.0)        # 纯红色
blue_transparent = (0.0, 0.0, 1.0, 0.5)  # 半透明蓝色
white = (1.0, 1.0, 1.0, 1.0)      # 白色
```

## 响应式状态集成

### 内置响应式属性

CustomView提供了内置的响应式状态：

```python
custom_view = CustomView(...)

# 监听鼠标位置变化
def on_mouse_move(position):
    x, y = position
    print(f"鼠标位置更新: {x}, {y}")

custom_view.mouse_position.subscribe(on_mouse_move)

# 监听拖拽状态
custom_view.is_dragging.subscribe(lambda dragging: 
    print("开始拖拽" if dragging else "结束拖拽"))
```

### 自定义响应式状态

在组件类中可以定义自己的响应式状态：

```python
class DrawingCanvas(Component):
    def __init__(self):
        super().__init__()
        self.drawing_points = Signal([])  # 绘制点列表
        self.current_color = Signal((1.0, 0.0, 0.0, 1.0))  # 当前颜色
        self.status_text = Signal("准备绘制")  # 状态文本
    
    def mount(self):
        canvas = CustomView(
            on_draw=self._on_draw,
            on_mouse_down=self._add_point
        )
        return canvas.mount()
    
    def _add_point(self, x, y, event):
        points = self.drawing_points.value.copy()
        points.append((x, y))
        self.drawing_points.value = points  # 触发响应式更新
        self.status_text.value = f"已绘制 {len(points)} 个点"
```

## 完整示例

### 简单绘图应用

```python
class SimpleDrawingApp(Component):
    def __init__(self):
        super().__init__()
        self.points = Signal([])
        self.color = Signal((0.0, 0.5, 1.0, 0.8))
    
    def mount(self):
        canvas = CustomView(
            style=LayoutStyle(width=500, height=400),
            on_draw=self._draw,
            on_mouse_down=self._add_point,
            on_key_down=self._handle_key
        )
        
        return VStack([
            Label("绘图应用 - 点击绘制，空格清空"),
            canvas
        ]).mount()
    
    def _draw(self, context, rect, bounds):
        # 白色背景
        DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                             (1.0, 1.0, 1.0, 1.0))
        
        # 绘制所有点
        color = self.color.value
        for x, y in self.points.value:
            DrawingUtils.fill_circle(context, x, y, 5, color)
    
    def _add_point(self, x, y, event):
        points = self.points.value.copy()
        points.append((x, y))
        self.points.value = points
    
    def _handle_key(self, key_code, characters, event):
        if characters == ' ':  # 空格键清空
            self.points.value = []
```

## 最佳实践

### 1. 性能优化

- 只在必要时调用`redraw()`重绘
- 避免在绘制函数中进行复杂计算
- 使用响应式状态而不是直接修改视图

### 2. 事件处理

- 使用try-catch包装回调函数，避免崩溃
- 合理使用事件参数中的信息
- 键盘事件需要视图获得焦点

### 3. 状态管理

- 使用Signal进行状态管理，确保响应式更新
- 在组件内部维护状态，通过props传递配置
- 避免直接修改传入的数据

### 4. 布局集成

- 正确设置LayoutStyle进行布局
- 考虑视图的固有尺寸和约束
- 与macUI布局系统协调工作

## 常见问题

### Q: 键盘事件不响应？
A: 确保调用`custom_view.make_first_responder()`让视图成为第一响应者。

### Q: 绘制不更新？
A: 使用`custom_view.redraw()`手动触发重绘，或者通过响应式状态自动触发。

### Q: 鼠标事件坐标不准确？
A: CustomView使用翻转坐标系(左上角为原点)，坐标已经转换为视图内坐标。

### Q: 如何处理复杂绘制？
A: 可以直接使用CoreGraphics API，或者考虑使用CALayer进行硬件加速绘制。

## 扩展阅读

- [macUI布局系统文档](LAYOUT_SYSTEM.md)
- [Signal响应式系统指南](SIGNAL_GUIDE.md) 
- [组件开发最佳实践](COMPONENT_BEST_PRACTICES.md)
- [Apple CoreGraphics官方文档](https://developer.apple.com/documentation/coregraphics)

---

通过CustomView组件，您可以在macUI框架内创建任何类型的自定义视图，从简单的绘图工具到复杂的数据可视化组件，同时保持与框架响应式系统的完美集成。