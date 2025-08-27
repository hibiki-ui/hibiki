# macUI Quick Start Guide

快速上手macUI v3.0框架 - 5分钟构建第一个响应式macOS应用。

## 安装

```bash
# 使用uv安装（推荐）
uv add macui

# 或pip安装
pip install macui
```

## Hello World

最简单的macUI应用：

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/path/to/macui')

from macui.components import Label, VStack, LayoutStyle
from macui.app import create_app
from macui.core import Component

from AppKit import NSWindow, NSMakeRect, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable
from PyObjCTools import AppHelper

class HelloApp(Component):
    def mount(self):
        return VStack([
            Label("Hello macUI!", style=LayoutStyle(height=40)),
            Label("欢迎使用响应式UI框架")
        ], style=LayoutStyle(gap=20, padding=40)).mount()

def main():
    app = create_app("Hello macUI")
    
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 400, 200),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered, False
    )
    
    window.setTitle_("Hello macUI")
    window.setContentView_(HelloApp().mount())
    window.makeKeyAndOrderFront_(None)
    
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()
```

## 响应式计数器

演示Signal响应式系统：

```python
from macui import Signal
from macui.components import Label, Button, VStack, LayoutStyle
from macui.core import Component

class Counter(Component):
    def __init__(self):
        super().__init__()
        # 响应式状态
        self.count = Signal(0)
    
    def mount(self):
        # 响应式标签 - count变化时自动更新
        count_label = Label(f"计数: {self.count.value}")
        
        # 按钮
        inc_button = Button("+1", on_click=self._increment)
        dec_button = Button("-1", on_click=self._decrement)
        reset_button = Button("重置", on_click=self._reset)
        
        # 布局
        return VStack([
            count_label,
            VStack([inc_button, dec_button, reset_button], 
                   style=LayoutStyle(gap=10))
        ], style=LayoutStyle(gap=20, padding=30)).mount()
    
    def _increment(self):
        self.count.value += 1
    
    def _decrement(self):
        self.count.value -= 1
    
    def _reset(self):
        self.count.value = 0
```

## 自定义绘制

创建自定义视图组件：

```python
from macui.components import CustomView, DrawingUtils, VStack
from macui.core import Component
from macui import Signal
import random

class DrawingCanvas(Component):
    def __init__(self):
        super().__init__()
        self.circles = Signal([])
    
    def mount(self):
        canvas = CustomView(
            style=LayoutStyle(width=400, height=300),
            on_draw=self._draw,
            on_mouse_down=self._add_circle
        )
        
        # 设置响应式重绘
        canvas.setup_auto_redraw(self.circles)
        
        return VStack([
            Label("点击画布添加圆形"),
            canvas
        ], style=LayoutStyle(gap=10, padding=20)).mount()
    
    def _draw(self, context, rect, bounds):
        # 白色背景
        DrawingUtils.fill_rect(context, 0, 0, 
                              bounds.size.width, bounds.size.height,
                              (1.0, 1.0, 1.0, 1.0))
        
        # 绘制所有圆形
        for x, y, radius, color in self.circles.value:
            DrawingUtils.fill_circle(context, x, y, radius, color)
    
    def _add_circle(self, x, y, event):
        circles = self.circles.value.copy()
        circles.append((
            x, y, 
            random.uniform(10, 30),  # 随机半径
            (random.random(), random.random(), random.random(), 0.7)  # 随机颜色
        ))
        self.circles.value = circles
```

## 动画效果

使用macUI动画系统：

```python
from macui.animation import ShinyText, FadeIn, Scale
from macui.components import Label, Button, VStack

class AnimatedText(Component):
    def mount(self):
        # 带光泽效果的标题
        title = Label("✨ 闪亮的标题")
        shiny = ShinyText(speed=3.0, intensity=0.8)
        # 注意：需要在mount后应用动画
        
        # 淡入按钮
        fade_button = Button("淡入效果")
        fade_in = FadeIn(duration=1.0)
        
        # 缩放按钮  
        scale_button = Button("缩放效果")
        scale_anim = Scale(duration=0.8, from_scale=0.5)
        
        container = VStack([title, fade_button, scale_button],
                          style=LayoutStyle(gap=15, padding=25))
        
        # 应用动画效果
        mounted_container = container.mount()
        
        # 应用动画到具体的NSView（需要获取实际的NSView引用）
        # shiny.apply_to(title._nsview)  # 实际使用时需要正确获取NSView
        
        return mounted_container
```

## 布局系统

使用VStack和HStack进行布局：

```python
from macui.components import VStack, HStack, Label, Button, LayoutStyle
from macui.layout.styles import AlignItems, JustifyContent

class LayoutDemo(Component):
    def mount(self):
        # 顶部标题区
        header = VStack([
            Label("布局演示", style=LayoutStyle(height=40)),
            Label("展示VStack和HStack的使用")
        ], style=LayoutStyle(gap=10, align_items=AlignItems.CENTER))
        
        # 按钮行
        button_row = HStack([
            Button("按钮1"),
            Button("按钮2"),
            Button("按钮3")
        ], style=LayoutStyle(
            gap=15, 
            justify_content=JustifyContent.SPACE_BETWEEN
        ))
        
        # 主容器
        return VStack([
            header,
            button_row,
            Label("底部说明文字")
        ], style=LayoutStyle(
            gap=20,
            padding=30,
            align_items=AlignItems.STRETCH
        )).mount()
```

## 常用模式

### 1. 数据列表组件

```python
class TodoList(Component):
    def __init__(self):
        super().__init__()
        self.todos = Signal([
            {"id": 1, "text": "学习macUI", "done": False},
            {"id": 2, "text": "构建应用", "done": False}
        ])
    
    def mount(self):
        todo_items = []
        for todo in self.todos.value:
            item = HStack([
                Label(todo["text"]),
                Button("完成" if not todo["done"] else "取消",
                      on_click=lambda t=todo: self._toggle_todo(t["id"]))
            ], style=LayoutStyle(gap=10, justify_content=JustifyContent.SPACE_BETWEEN))
            todo_items.append(item)
        
        return VStack([
            Label("Todo列表"),
            *todo_items
        ], style=LayoutStyle(gap=10, padding=20)).mount()
    
    def _toggle_todo(self, todo_id):
        todos = self.todos.value.copy()
        for todo in todos:
            if todo["id"] == todo_id:
                todo["done"] = not todo["done"]
                break
        self.todos.value = todos
```

### 2. 表单组件

```python
class LoginForm(Component):
    def __init__(self):
        super().__init__()
        self.username = Signal("")
        self.password = Signal("")
        self.message = Signal("")
    
    def mount(self):
        return VStack([
            Label("用户登录"),
            
            # 用户名输入（这里简化为Label，实际需要TextField组件）
            Label(f"用户名: {self.username.value}"),
            
            # 消息显示
            Label(self.message.value),
            
            # 登录按钮
            Button("登录", on_click=self._login),
            
        ], style=LayoutStyle(gap=15, padding=30)).mount()
    
    def _login(self):
        if self.username.value and self.password.value:
            self.message.value = "登录成功！"
        else:
            self.message.value = "请输入用户名和密码"
```

### 3. 设置面板

```python
class SettingsPanel(Component):
    def __init__(self):
        super().__init__()
        self.theme = Signal("light")
        self.notifications = Signal(True)
        self.auto_save = Signal(False)
    
    def mount(self):
        return VStack([
            Label("应用设置"),
            
            # 主题设置
            HStack([
                Label("主题:"),
                Button("切换", on_click=self._toggle_theme)
            ]),
            
            # 通知设置  
            HStack([
                Label(f"通知: {'开启' if self.notifications.value else '关闭'}"),
                Button("切换", on_click=self._toggle_notifications)
            ]),
            
            # 自动保存
            HStack([
                Label(f"自动保存: {'开启' if self.auto_save.value else '关闭'}"),
                Button("切换", on_click=self._toggle_auto_save)
            ]),
            
        ], style=LayoutStyle(gap=15, padding=25)).mount()
    
    def _toggle_theme(self):
        self.theme.value = "dark" if self.theme.value == "light" else "light"
    
    def _toggle_notifications(self):
        self.notifications.value = not self.notifications.value
    
    def _toggle_auto_save(self):
        self.auto_save.value = not self.auto_save.value
```

## 调试技巧

### 1. Signal调试

```python
# 启用Signal调试日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 创建Signal时会看到日志
count = Signal(0)  # DEBUG: Signal创建: 初始值=0

# 修改值时会看到日志
count.value = 5    # INFO: Signal.set: 0 -> 5, 观察者数: X
```

### 2. 组件调试

```python
class DebugComponent(Component):
    def mount(self):
        print(f"🔧 {self.__class__.__name__} mount() 被调用")
        # ... 组件逻辑
        print(f"✅ {self.__class__.__name__} mount() 完成")
        return view
```

### 3. 事件调试

```python
def debug_click():
    print("🖱️ 按钮被点击")
    # 实际处理逻辑...

button = Button("调试按钮", on_click=debug_click)
```

## 常见问题

### Q: Signal更新但UI没有变化？
A: 确保使用Signal作为值传递给组件，而不是Signal.value。

```python
# ❌ 错误 - 传递静态值
Label(my_signal.value)

# ✅ 正确 - 传递Signal对象
Label(my_signal)
```

### Q: CustomView不重绘？
A: 使用`setup_auto_redraw()`设置响应式重绘。

```python
canvas = CustomView(on_draw=my_draw)
canvas.setup_auto_redraw(my_data_signal)  # 数据变化时自动重绘
```

### Q: 事件回调出错？
A: 使用try-catch包装事件处理。

```python
def safe_click():
    try:
        # 事件处理逻辑
        pass
    except Exception as e:
        print(f"事件处理出错: {e}")

button = Button("安全按钮", on_click=safe_click)
```

## 下一步

- 阅读 [API Reference](API_REFERENCE.md) 了解完整API
- 查看 [Component Catalog](COMPONENT_CATALOG.md) 了解所有组件
- 学习 [Best Practices](BEST_PRACTICES.md) 最佳实践
- 探索 [Examples](../examples/) 示例代码

---

*现在您已经掌握了macUI的基础用法，可以开始构建强大的macOS应用了！*