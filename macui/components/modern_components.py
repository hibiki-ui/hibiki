"""
macUI v3.0 现代化组件库
统一的style接口设计，完美集成Stretchable布局引擎
"""

from typing import Optional, List, Union, Any, Callable
from .core import LayoutAwareComponent
from ..layout.node import LayoutNode
from ..layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
from AppKit import *
from Foundation import *

class ModernComponent(LayoutAwareComponent):
    """现代化组件基类 - 统一style接口"""
    
    def __init__(self, style: Optional[LayoutStyle] = None, **kwargs):
        """
        Args:
            style: 布局样式对象
            **kwargs: 其他组件特定参数
        """
        super().__init__(layout_style=style)
        self._nsview = None

class ModernLabel(ModernComponent):
    """现代化Label组件"""
    
    def __init__(self, text: str, style: Optional[LayoutStyle] = None):
        super().__init__(style=style)
        self.text = text
        
    def mount(self):
        # 创建NSTextField作为Label
        label = NSTextField.alloc().init()
        label.setStringValue_(self.text)
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

class ModernButton(ModernComponent):
    """现代化Button组件"""
    
    def __init__(self, title: str, style: Optional[LayoutStyle] = None, on_click: Optional[Callable] = None):
        super().__init__(style=style)
        self.title = title
        self.on_click = on_click
        
    def mount(self):
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
        from ..binding.event import EventBinding
        EventBinding.bind_click(button, self.on_click)

class ModernVStack(ModernComponent):
    """现代化垂直布局组件"""
    
    def __init__(self, 
                 children: Optional[List[ModernComponent]] = None,
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

class ModernHStack(ModernComponent):
    """现代化水平布局组件"""
    
    def __init__(self, 
                 children: Optional[List[ModernComponent]] = None,
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

class ModernSpacer(ModernComponent):
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

# 便捷别名，保持API兼容性
Label = ModernLabel
Button = ModernButton
VStack = ModernVStack
HStack = ModernHStack
Spacer = ModernSpacer