"""
macUI v3.0 现代化组件库
统一的style接口设计，完美集成Stretchable布局引擎
"""

from typing import Optional, List, Union, Any, Callable
from enum import Enum
from .core import LayoutAwareComponent
from ..layout.node import LayoutNode
from ..layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
from ..core.signal import Signal, Computed
from ..core.binding import ReactiveBinding
from AppKit import *
from Foundation import *

# 文本相关枚举（从basic_controls.py迁移）
class LineBreakMode(Enum):
    """文本换行模式枚举
    
    定义了NSTextField支持的各种文本换行和截断模式，
    提供类型安全和易于理解的接口。
    """
    WORD_WRAPPING = NSLineBreakByWordWrapping      # 按单词换行（默认）
    CHAR_WRAPPING = NSLineBreakByCharWrapping      # 按字符换行  
    CLIPPING = NSLineBreakByClipping               # 超出部分裁剪
    TRUNCATE_TAIL = NSLineBreakByTruncatingTail    # 尾部省略号...
    TRUNCATE_HEAD = NSLineBreakByTruncatingHead    # 头部省略号...
    TRUNCATE_MIDDLE = NSLineBreakByTruncatingMiddle # 中间省略号...

class LabelStyle(Enum):
    """Label预设样式枚举
    
    为常见使用场景提供预设配置，简化接口使用。
    """
    # 多行文本标签（默认）- 适用于描述、帮助文本等
    MULTILINE = "multiline"
    
    # 单行标题标签 - 适用于标题、状态栏等  
    TITLE = "title"
    
    # 单行截断标签 - 适用于列表项、表格单元格
    TRUNCATED = "truncated"
    
    # 固定宽度标签 - 适用于表单字段、固定布局
    FIXED_WIDTH = "fixed_width"

class Component(LayoutAwareComponent):
    """现代化组件基类 - 统一style接口"""
    
    def __init__(self, style: Optional[LayoutStyle] = None, **kwargs):
        """🏗️ CORE METHOD: Modern component initialization
        
        Args:
            style: 布局样式对象
            **kwargs: 其他组件特定参数
        """
        super().__init__(layout_style=style)
        self._nsview = None

class Label(Component):
    """现代化Label组件"""
    
    def __init__(self, text: Union[str, Any], style: Optional[LayoutStyle] = None):
        """🏗️ CORE METHOD: Label component initialization"""
        super().__init__(style=style)
        self.text = text
        
    def mount(self):
        """🚀 CORE METHOD: Label component mounting"""
        # 创建NSTextField作为Label
        label = NSTextField.alloc().init()
        
        # 设置文本内容 - 支持响应式绑定
        if isinstance(self.text, (Signal, Computed)):
            ReactiveBinding.bind(label, "stringValue", self.text)
            print(f"🔗 Label响应式绑定: {self.text}")
        else:
            label.setStringValue_(str(self.text))
            print(f"📝 Label静态文本: {str(self.text)}")
        
        label.setEditable_(False)
        label.setSelectable_(False)
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        
        # 应用样式
        self._setup_text_properties(label)
        
        # 创建布局节点
        self.create_layout_node()
        
        # 存储引用
        self._nsview = label
        
        return label
    
    def _setup_text_properties(self, label):
        """设置文本属性"""
        # 多行支持
        label.setUsesSingleLineMode_(False)
        label.setLineBreakMode_(NSLineBreakByWordWrapping)
        
        # 设置合适的宽度
        if self.layout_style and self.layout_style.width:
            label.setPreferredMaxLayoutWidth_(float(self.layout_style.width))
        else:
            label.setPreferredMaxLayoutWidth_(400.0)
        
        # 单元格配置
        cell = label.cell()
        cell.setWraps_(True)
        cell.setScrollable_(False)

class Button(Component):
    """现代化Button组件"""
    
    def __init__(self, title: str, style: Optional[LayoutStyle] = None, on_click: Optional[Callable] = None):
        """🏗️ CORE METHOD: Button component initialization"""
        super().__init__(style=style)
        self.title = title
        self.on_click = on_click
        
    def mount(self):
        """🚀 CORE METHOD: Button component mounting"""
        # 创建NSButton
        button = NSButton.alloc().init()
        button.setTitle_(self.title)
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 自动调整尺寸
        button.sizeToFit()
        
        # 绑定点击事件
        if self.on_click:
            self._bind_click_event(button)
        
        # 创建布局节点
        self.create_layout_node()
        
        # 存储引用
        self._nsview = button
        
        return button
    
    def _bind_click_event(self, button):
        """绑定点击事件"""
        from ..core.binding import EventBinding
        EventBinding.bind_click(button, self.on_click)

class VStack(Component):
    """现代化垂直布局组件"""
    
    def __init__(self, 
                 children: Optional[List[Component]] = None,
                 style: Optional[LayoutStyle] = None,
                 spacing: Union[int, float] = 0,
                 alignment: Union[AlignItems, str] = AlignItems.STRETCH,
                 padding: Union[int, float] = 0):
        
        # 创建VStack样式
        vstack_style = style or LayoutStyle()
        
        # 如果没有显式设置布局属性，使用参数设置
        if not style:
            vstack_style.display = Display.FLEX
            vstack_style.flex_direction = FlexDirection.COLUMN
            vstack_style.gap = spacing
            vstack_style.padding = padding
            
            # 处理对齐方式
            if isinstance(alignment, str):
                align_map = {
                    "start": AlignItems.FLEX_START,
                    "center": AlignItems.CENTER, 
                    "end": AlignItems.FLEX_END,
                    "stretch": AlignItems.STRETCH
                }
                alignment = align_map.get(alignment, AlignItems.STRETCH)
            
            vstack_style.align_items = alignment
        
        super().__init__(style=vstack_style)
        self.children = children or []
        
    def mount(self):
        # 创建容器NSView
        container = NSView.alloc().init()
        
        # 创建布局节点
        layout_node = self.create_layout_node()
        
        # 挂载子组件并添加到布局树
        for child in self.children:
            child_nsview = child.mount()
            container.addSubview_(child_nsview)
            
            # 添加子组件的布局节点
            child_layout_node = child.create_layout_node()
            layout_node.add_child(child_layout_node)
        
        # 计算布局
        layout_node.compute_layout()
        
        # 应用布局到容器
        self.apply_layout_to_nsview(container)
        
        # 应用布局到所有子组件
        for child in self.children:
            child.apply_layout_to_nsview(child._nsview)
        
        # 存储引用
        self._nsview = container
        
        return container

class HStack(Component):
    """现代化水平布局组件"""
    
    def __init__(self, 
                 children: Optional[List[Component]] = None,
                 style: Optional[LayoutStyle] = None,
                 spacing: Union[int, float] = 0,
                 alignment: Union[AlignItems, str] = AlignItems.STRETCH,
                 justify_content: Union[JustifyContent, str] = JustifyContent.FLEX_START,
                 padding: Union[int, float] = 0):
        
        # 创建HStack样式
        hstack_style = style or LayoutStyle()
        
        # 如果没有显式设置布局属性，使用参数设置
        if not style:
            hstack_style.display = Display.FLEX
            hstack_style.flex_direction = FlexDirection.ROW
            hstack_style.gap = spacing
            hstack_style.padding = padding
            
            # 处理对齐方式
            if isinstance(alignment, str):
                align_map = {
                    "start": AlignItems.FLEX_START,
                    "center": AlignItems.CENTER,
                    "end": AlignItems.FLEX_END,
                    "stretch": AlignItems.STRETCH
                }
                alignment = align_map.get(alignment, AlignItems.STRETCH)
            
            if isinstance(justify_content, str):
                justify_map = {
                    "start": JustifyContent.FLEX_START,
                    "center": JustifyContent.CENTER,
                    "end": JustifyContent.FLEX_END,
                    "space-between": JustifyContent.SPACE_BETWEEN,
                    "space-around": JustifyContent.SPACE_AROUND,
                    "space-evenly": JustifyContent.SPACE_EVENLY
                }
                justify_content = justify_map.get(justify_content, JustifyContent.FLEX_START)
            
            hstack_style.align_items = alignment
            hstack_style.justify_content = justify_content
        
        super().__init__(style=hstack_style)
        self.children = children or []
        
    def mount(self):
        # 创建容器NSView
        container = NSView.alloc().init()
        
        # 创建布局节点
        layout_node = self.create_layout_node()
        
        # 挂载子组件并添加到布局树
        for child in self.children:
            child_nsview = child.mount()
            container.addSubview_(child_nsview)
            
            # 添加子组件的布局节点
            child_layout_node = child.create_layout_node()
            layout_node.add_child(child_layout_node)
        
        # 计算布局
        layout_node.compute_layout()
        
        # 应用布局到容器
        self.apply_layout_to_nsview(container)
        
        # 应用布局到所有子组件
        for child in self.children:
            child.apply_layout_to_nsview(child._nsview)
        
        # 存储引用
        self._nsview = container
        
        return container

class Spacer(Component):
    """弹性空间组件"""
    
    def __init__(self, style: Optional[LayoutStyle] = None):
        spacer_style = style or LayoutStyle(flex_grow=1.0)
        super().__init__(style=spacer_style)
        
    def mount(self):
        # 创建透明的NSView作为占位符
        spacer = NSView.alloc().init()
        
        # 创建布局节点
        self.create_layout_node()
        
        # 存储引用
        self._nsview = spacer
        
        return spacer

