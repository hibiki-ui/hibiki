# macUI Component Catalog

完整的macUI组件目录，包含所有可用组件的详细说明、参数和使用示例。

## 基础组件

### Label - 文本标签

显示静态或动态文本的基础组件。

**导入:**
```python
from macui.components import Label
```

**基本用法:**
```python
# 静态文本
label = Label("Hello World")

# 响应式文本
text_signal = Signal("动态内容")
label = Label(text_signal)

# 带样式
label = Label("样式文本", style=LayoutStyle(
    height=40,
    padding=10
))
```

**参数:**
- `text: Union[str, Signal, Computed]` - 显示的文本内容
- `style: Optional[LayoutStyle]` - 布局样式对象

**特性:**
- ✅ 自动响应式更新
- ✅ 多行文本支持  
- ✅ 文字换行
- ✅ 样式继承

**适用场景:**
- 标题和说明文字
- 状态显示
- 动态内容展示

---

### Button - 按钮组件

可点击的交互按钮组件。

**导入:**
```python
from macui.components import Button
```

**基本用法:**
```python
# 简单按钮
button = Button("点击我")

# 带点击事件
def handle_click():
    print("按钮被点击")

button = Button("确认", on_click=handle_click)

# 带样式
button = Button("自定义", 
    style=LayoutStyle(width=120, height=40),
    on_click=my_handler
)
```

**参数:**
- `text: Union[str, Signal]` - 按钮显示文本
- `style: Optional[LayoutStyle]` - 布局样式
- `on_click: Optional[Callable]` - 点击事件回调

**回调签名:**
```python
def on_click() -> None:
    # 处理点击事件
    pass
```

**特性:**
- ✅ 标准macOS按钮样式
- ✅ 响应式文本更新
- ✅ 事件安全处理
- ✅ 键盘导航支持

**适用场景:**
- 表单提交
- 操作触发
- 导航控制

---

## 布局组件

### VStack - 垂直布局

垂直排列子组件的容器组件。

**导入:**
```python
from macui.components import VStack
```

**基本用法:**
```python
# 基础垂直布局
container = VStack([
    Label("标题"),
    Button("按钮1"),
    Button("按钮2")
])

# 带样式和间距
container = VStack(
    children=[component1, component2, component3],
    style=LayoutStyle(
        gap=15,                        # 子组件间距
        padding=20,                    # 内边距
        align_items=AlignItems.CENTER  # 水平对齐
    )
)
```

**参数:**
- `children: List[Component]` - 子组件列表
- `style: Optional[LayoutStyle]` - 布局样式

**样式属性:**
- `gap: float` - 子组件间的间距
- `padding: float` - 容器内边距
- `align_items: AlignItems` - 水平对齐方式
- `justify_content: JustifyContent` - 垂直分布方式

**对齐选项:**
```python
from macui.layout.styles import AlignItems, JustifyContent

AlignItems.START    # 左对齐
AlignItems.CENTER   # 居中对齐
AlignItems.END      # 右对齐
AlignItems.STRETCH  # 拉伸填满

JustifyContent.START         # 顶部对齐
JustifyContent.CENTER        # 垂直居中
JustifyContent.END           # 底部对齐
JustifyContent.SPACE_BETWEEN # 两端对齐
JustifyContent.SPACE_AROUND  # 环绕分布
```

**适用场景:**
- 表单布局
- 导航菜单
- 内容列表

---

### HStack - 水平布局

水平排列子组件的容器组件。

**导入:**
```python
from macui.components import HStack
```

**基本用法:**
```python
# 水平按钮组
button_row = HStack([
    Button("取消"),
    Button("确认")
])

# 带样式
toolbar = HStack(
    children=[button1, button2, button3],
    style=LayoutStyle(
        gap=10,
        justify_content=JustifyContent.SPACE_BETWEEN
    )
)
```

**参数:**
- `children: List[Component]` - 子组件列表
- `style: Optional[LayoutStyle]` - 布局样式

**样式属性:**
- `gap: float` - 子组件间的间距
- `align_items: AlignItems` - 垂直对齐方式
- `justify_content: JustifyContent` - 水平分布方式

**适用场景:**
- 工具栏
- 按钮组
- 状态栏

---

## 高级组件

### CustomView - 自定义视图

完全可定制的视图组件，支持自定义绘制和事件处理。

**导入:**
```python
from macui.components import CustomView, DrawingUtils
```

**基本用法:**
```python
def my_draw(context, rect, bounds):
    # 绘制白色背景
    DrawingUtils.fill_rect(context, 0, 0, 
                          bounds.size.width, bounds.size.height,
                          (1.0, 1.0, 1.0, 1.0))
    
    # 绘制红色圆形
    DrawingUtils.fill_circle(context, 100, 100, 50, 
                            (1.0, 0.0, 0.0, 0.8))

def handle_click(x, y, event):
    print(f"点击位置: ({x}, {y})")

custom_view = CustomView(
    style=LayoutStyle(width=400, height=300),
    on_draw=my_draw,
    on_mouse_down=handle_click
)
```

**参数:**
- `style: Optional[LayoutStyle]` - 布局样式
- `on_draw: Optional[Callable]` - 绘制回调函数
- `on_mouse_down: Optional[Callable]` - 鼠标按下事件
- `on_mouse_up: Optional[Callable]` - 鼠标抬起事件
- `on_mouse_moved: Optional[Callable]` - 鼠标移动事件
- `on_mouse_dragged: Optional[Callable]` - 鼠标拖拽事件
- `on_key_down: Optional[Callable]` - 键盘按下事件
- `on_key_up: Optional[Callable]` - 键盘抬起事件

**回调签名:**
```python
# 绘制回调
def on_draw(context, rect, bounds):
    # context: CGContext - 绘制上下文
    # rect: NSRect - 需要重绘的区域
    # bounds: NSRect - 视图完整边界
    pass

# 鼠标事件回调
def on_mouse_event(x: float, y: float, event):
    # x, y: 鼠标在视图内的坐标
    # event: NSEvent - 事件对象
    pass

# 键盘事件回调
def on_key_event(key_code: int, characters: str, event):
    # key_code: 键码
    # characters: 按键字符
    # event: NSEvent - 事件对象
    pass
```

**方法:**
```python
# 设置响应式重绘
custom_view.setup_auto_redraw(signal1, signal2, ...)

# 手动触发重绘
custom_view.redraw()

# 成为第一响应者(接收键盘事件)
custom_view.make_first_responder()

# 获取视图边界
x, y, width, height = custom_view.get_bounds()
```

**响应式属性:**
```python
# 内置响应式状态
custom_view.mouse_position  # Signal[(float, float)] - 鼠标位置
custom_view.is_mouse_inside # Signal[bool] - 鼠标是否在视图内
custom_view.is_dragging     # Signal[bool] - 是否正在拖拽

# 监听状态变化
def on_position_change(position):
    x, y = position
    print(f"鼠标移动到: {x}, {y}")

# 使用Effect监听(需要手动实现订阅机制)
```

**适用场景:**
- 图表和数据可视化
- 绘图应用
- 游戏界面
- 自定义控件

---

## 绘制工具

### DrawingUtils - 绘制辅助类

提供常用绘制操作的静态方法集合。

**导入:**
```python
from macui.components import DrawingUtils
```

**矩形绘制:**
```python
def my_draw(context, rect, bounds):
    # 填充矩形 - (x, y, width, height, color)
    DrawingUtils.fill_rect(context, 10, 10, 200, 100, (1.0, 0.0, 0.0, 0.8))
    
    # 描边矩形 - (x, y, width, height, color, line_width)
    DrawingUtils.stroke_rect(context, 10, 10, 200, 100, (0.0, 0.0, 1.0, 1.0), 2.0)
```

**圆形绘制:**
```python
def my_draw(context, rect, bounds):
    # 填充圆形 - (center_x, center_y, radius, color)
    DrawingUtils.fill_circle(context, 100, 100, 50, (0.0, 1.0, 0.0, 0.6))
```

**线条绘制:**
```python
def my_draw(context, rect, bounds):
    # 绘制线条 - (from_x, from_y, to_x, to_y, color, line_width)
    DrawingUtils.draw_line(context, 0, 0, 200, 200, (0.0, 0.0, 0.0, 1.0), 1.5)
```

**文本绘制:**
```python
def my_draw(context, rect, bounds):
    # 绘制文本 - (text, x, y, font_size, color)
    DrawingUtils.draw_text(context, "Hello World", 10, 50, 16, (0.0, 0.0, 0.0, 1.0))
```

**颜色格式:**
所有颜色使用RGBA元组: `(red, green, blue, alpha)`
- 值范围: 0.0 - 1.0
- 示例:
  - 红色: `(1.0, 0.0, 0.0, 1.0)`
  - 半透明蓝色: `(0.0, 0.0, 1.0, 0.5)`
  - 白色: `(1.0, 1.0, 1.0, 1.0)`
  - 黑色: `(0.0, 0.0, 0.0, 1.0)`

**方法列表:**
- `fill_rect(context, x, y, width, height, color)` - 填充矩形
- `stroke_rect(context, x, y, width, height, color, line_width=1.0)` - 描边矩形
- `fill_circle(context, center_x, center_y, radius, color)` - 填充圆形
- `draw_line(context, from_x, from_y, to_x, to_y, color, line_width=1.0)` - 绘制线条
- `draw_text(context, text, x, y, font_size=12, color=(0,0,0,1))` - 绘制文本

---

## 样式系统

### LayoutStyle - 样式定义

定义组件布局和样式的配置类。

**导入:**
```python
from macui.layout.styles import LayoutStyle, AlignItems, JustifyContent, FlexDirection
```

**基本用法:**
```python
style = LayoutStyle(
    # 尺寸
    width=200,
    height=100,
    min_width=50,
    max_width=300,
    min_height=30,
    max_height=200,
    
    # 间距
    padding=10,        # 所有方向内边距
    padding_top=5,     # 上内边距
    padding_bottom=5,  # 下内边距  
    padding_left=8,    # 左内边距
    padding_right=8,   # 右内边距
    margin=5,          # 外边距
    
    # Flexbox布局
    flex_direction=FlexDirection.COLUMN,
    align_items=AlignItems.CENTER,
    justify_content=JustifyContent.START,
    gap=10
)
```

**属性分类:**

#### 尺寸属性
- `width: Optional[float]` - 宽度
- `height: Optional[float]` - 高度
- `min_width: Optional[float]` - 最小宽度
- `max_width: Optional[float]` - 最大宽度
- `min_height: Optional[float]` - 最小高度  
- `max_height: Optional[float]` - 最大高度

#### 间距属性
- `padding: Optional[float]` - 所有方向内边距
- `padding_top: Optional[float]` - 上内边距
- `padding_bottom: Optional[float]` - 下内边距
- `padding_left: Optional[float]` - 左内边距
- `padding_right: Optional[float]` - 右内边距
- `margin: Optional[float]` - 外边距
- `gap: Optional[float]` - 子元素间距

#### Flexbox属性
- `flex_direction: Optional[FlexDirection]` - 主轴方向
- `align_items: Optional[AlignItems]` - 交叉轴对齐
- `justify_content: Optional[JustifyContent]` - 主轴分布

**枚举值:**

#### FlexDirection - 主轴方向
```python
FlexDirection.ROW       # 水平方向(默认HStack)
FlexDirection.COLUMN    # 垂直方向(默认VStack)
```

#### AlignItems - 交叉轴对齐
```python
AlignItems.START     # 起始边对齐
AlignItems.CENTER    # 居中对齐
AlignItems.END       # 结束边对齐
AlignItems.STRETCH   # 拉伸填满
```

#### JustifyContent - 主轴分布
```python
JustifyContent.START           # 起始对齐
JustifyContent.CENTER          # 居中对齐
JustifyContent.END             # 结束对齐
JustifyContent.SPACE_BETWEEN   # 两端对齐
JustifyContent.SPACE_AROUND    # 环绕分布
JustifyContent.SPACE_EVENLY    # 平均分布
```

---

## 组件组合模式

### 卡片容器

```python
def Card(title: str, content: Component, actions: List[Component] = None):
    """创建卡片样式容器"""
    header = Label(title, style=LayoutStyle(height=40))
    
    children = [header, content]
    if actions:
        action_row = HStack(actions, style=LayoutStyle(gap=10))
        children.append(action_row)
    
    return VStack(
        children=children,
        style=LayoutStyle(
            padding=20,
            gap=15,
            # 可添加边框、阴影等视觉效果
        )
    )

# 使用示例
card = Card(
    title="设置",
    content=VStack([
        Label("主题: 深色模式"),
        Label("语言: 中文")
    ]),
    actions=[
        Button("取消"),
        Button("保存")
    ]
)
```

### 表单字段

```python
def FormField(label: str, input_component: Component, error_message: str = ""):
    """表单字段组合"""
    children = [
        Label(label, style=LayoutStyle(height=20)),
        input_component
    ]
    
    if error_message:
        error_label = Label(error_message, style=LayoutStyle(height=16))
        # 可设置错误样式: 红色文字等
        children.append(error_label)
    
    return VStack(
        children=children,
        style=LayoutStyle(gap=5, align_items=AlignItems.STRETCH)
    )
```

### 工具栏

```python
def Toolbar(items: List[Component], position: str = "top"):
    """工具栏容器"""
    return HStack(
        children=items,
        style=LayoutStyle(
            gap=8,
            padding=10,
            justify_content=JustifyContent.START,
            align_items=AlignItems.CENTER
        )
    )

# 使用示例
toolbar = Toolbar([
    Button("新建"),
    Button("打开"),
    Button("保存"),
    # 分隔符可以用空Label实现
    Label("", style=LayoutStyle(width=1, height=20)),
    Button("设置")
])
```

---

## 最佳实践

### 1. 组件命名

```python
# ✅ 推荐: 描述性命名
save_button = Button("保存", on_click=save_data)
user_name_label = Label(user.name)

# ❌ 避免: 通用命名
button1 = Button("按钮")
label = Label("文本")
```

### 2. 样式复用

```python
# ✅ 推荐: 定义样式常量
BUTTON_STYLE = LayoutStyle(width=100, height=35)
TITLE_STYLE = LayoutStyle(height=40, padding=10)

title = Label("标题", style=TITLE_STYLE)
button = Button("确认", style=BUTTON_STYLE)
```

### 3. 组件组合

```python
# ✅ 推荐: 创建可复用的组合组件
def ActionButton(text: str, action: Callable, primary: bool = False):
    style = LayoutStyle(
        width=120 if primary else 80,
        height=35
    )
    return Button(text, style=style, on_click=action)

# 使用
primary_btn = ActionButton("确认", confirm_action, primary=True)
secondary_btn = ActionButton("取消", cancel_action)
```

### 4. 错误处理

```python
# ✅ 推荐: 安全的事件处理
def safe_click_handler():
    try:
        # 业务逻辑
        process_data()
    except Exception as e:
        print(f"处理失败: {e}")
        # 用户提示或错误恢复

button = Button("处理", on_click=safe_click_handler)
```

---

## 版本兼容性

| 组件 | v3.0 | 说明 |
|-----|------|------|
| Label | ✅ | 稳定 |
| Button | ✅ | 稳定 |
| VStack | ✅ | 稳定 |
| HStack | ✅ | 稳定 |
| CustomView | ✅ | 新增 |
| DrawingUtils | ✅ | 新增 |
| LayoutStyle | ✅ | 增强 |

---

*本目录涵盖了macUI v3.0的所有可用组件。随着框架发展，新组件将持续添加到此目录中。*