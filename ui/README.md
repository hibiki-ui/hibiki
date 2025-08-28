# 🎨 Hibiki UI

Reactive UI Framework for Native macOS Applications

## 快速开始

```python
from hibiki.ui import Signal, Label, Button, Container, ComponentStyle, px, ManagerFactory

# 创建响应式状态
count = Signal(0)

# 创建 UI 组件
button = Button("点击我", on_click=lambda: setattr(count, 'value', count.value + 1))
label = Label(lambda: f"点击次数: {count.value}")

# 创建容器
container = Container(
    children=[label, button],
    style=ComponentStyle(padding=px(20))
)

# 运行应用
app_manager = ManagerFactory.get_app_manager()
window = app_manager.create_window("Hibiki UI Demo", 400, 300)
window.set_content(container)
app_manager.run()
```

详细文档请参考主项目。