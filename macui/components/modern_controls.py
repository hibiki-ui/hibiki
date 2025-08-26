"""
现代化组件 - 基于新布局引擎v3.0 (Stretchable)

提供支持CSS-like布局属性的现代化组件实现
这些组件完全兼容新布局系统，提供声明式API
"""

from typing import Any, Callable, Optional, Union
from AppKit import NSButton, NSButtonTypeMomentaryPushIn, NSTextField, NSTextFieldRoundedBezel
from Foundation import NSMakeRect

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding
from ..core.signal import Signal, Computed
from ..layout.styles import LayoutStyle
from .core import LayoutAwareComponent


class ModernButton(LayoutAwareComponent):
    """现代化按钮组件 - 支持新布局系统
    
    提供CSS-like布局属性和声明式API
    完全兼容响应式Signal系统
    """
    
    def __init__(
        self,
        title: Union[str, Signal[str], Computed[str]],
        on_click: Optional[Callable[[], None]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 新增：布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        margin: Optional[Union[int, float]] = None,
        padding: Optional[Union[int, float]] = None,
        flex_grow: Optional[float] = None,
        flex_shrink: Optional[float] = None,
        **layout_kwargs
    ):
        """初始化现代化按钮
        
        Args:
            title: 按钮标题 (支持响应式)
            on_click: 点击回调函数
            enabled: 启用状态 (支持响应式)
            tooltip: 工具提示 (支持响应式)
            width: 按钮宽度
            height: 按钮高度  
            margin: 外边距
            padding: 内边距
            flex_grow: flex grow 值
            flex_shrink: flex shrink 值
            **layout_kwargs: 其他布局样式参数
        """
        # 构建布局样式
        layout_style = LayoutStyle(
            width=width,
            height=height or 32,  # 默认按钮高度
            margin=margin,
            padding=padding,
            flex_grow=flex_grow,
            flex_shrink=flex_shrink,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        # 按钮属性
        self.title = title
        self.on_click = on_click
        self.enabled = enabled
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSButton:
        """创建NSButton实例"""
        button = NSButton.alloc().init()
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 设置默认frame（后续会被布局系统覆盖）
        if self.layout_style and (self.layout_style.width or self.layout_style.height):
            width = self.layout_style.width or 100
            height = self.layout_style.height or 32
            button.setFrame_(NSMakeRect(0, 0, width, height))
        else:
            button.setFrame_(NSMakeRect(0, 0, 100, 32))
        
        return button
    
    def _setup_nsview(self):
        """设置NSButton属性和绑定"""
        button = self._nsview
        
        # 标题绑定
        if isinstance(self.title, (Signal, Computed)):
            ReactiveBinding.bind(button, "title", self.title)
        else:
            button.setTitle_(str(self.title))
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(button, "enabled", self.enabled)
            else:
                button.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(button, "toolTip", self.tooltip)
            else:
                button.setToolTip_(str(self.tooltip))
        
        # 点击事件绑定
        if self.on_click:
            EventBinding.bind_click(button, self.on_click)
        
        # 自动调整尺寸
        button.sizeToFit()
        
        print(f"🎯 ModernButton '{self.title}' 创建完成")


class ModernLabel(LayoutAwareComponent):
    """现代化标签组件 - 支持新布局系统"""
    
    def __init__(
        self,
        text: Union[str, Signal[str], Computed[str]],
        multiline: bool = True,
        line_break_mode: Optional[Any] = None,
        preferred_max_width: Optional[float] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        margin: Optional[Union[int, float]] = None,
        flex_grow: Optional[float] = None,
        **layout_kwargs
    ):
        """初始化现代化标签
        
        Args:
            text: 标签文本 (支持响应式)
            multiline: 是否支持多行
            line_break_mode: 换行模式
            preferred_max_width: 首选最大宽度
            其他参数同ModernButton
        """
        layout_style = LayoutStyle(
            width=width,
            height=height,
            margin=margin,
            flex_grow=flex_grow,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.text = text
        self.multiline = multiline
        self.line_break_mode = line_break_mode
        self.preferred_max_width = preferred_max_width or 400
    
    def _create_nsview(self) -> NSTextField:
        """创建NSTextField实例"""
        label = NSTextField.alloc().init()
        label.setEditable_(False)
        label.setSelectable_(False) 
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        
        return label
    
    def _setup_nsview(self):
        """设置NSTextField属性"""
        label = self._nsview
        
        # 文本绑定
        if isinstance(self.text, (Signal, Computed)):
            ReactiveBinding.bind(label, "text", self.text)
        else:
            label.setStringValue_(str(self.text))
        
        # 多行配置
        if self.multiline:
            label.setUsesSingleLineMode_(False)
            label.setPreferredMaxLayoutWidth_(self.preferred_max_width)
            
            # 文本框cell配置
            text_cell = label.cell()
            text_cell.setWraps_(True)
            text_cell.setScrollable_(False)
        
        print(f"✅ ModernLabel '{self.text}' 创建完成")


class ModernTextField(LayoutAwareComponent):
    """现代化文本输入框 - 支持新布局系统"""
    
    def __init__(
        self,
        value: Optional[Signal[str]] = None,
        placeholder: Optional[str] = None,
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        flex_grow: Optional[float] = None,
        **layout_kwargs
    ):
        """初始化现代化文本框"""
        layout_style = LayoutStyle(
            width=width,
            height=height or 24,  # 默认文本框高度
            flex_grow=flex_grow,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.value = value or Signal("")
        self.placeholder = placeholder
        self.on_change = on_change
        self.on_submit = on_submit
        self.enabled = enabled
    
    def _create_nsview(self) -> NSTextField:
        """创建NSTextField实例"""
        textfield = NSTextField.alloc().init()
        textfield.setBezeled_(True)
        textfield.setBezelStyle_(NSTextFieldRoundedBezel)
        textfield.setEditable_(True)
        textfield.setSelectable_(True)
        
        return textfield
    
    def _setup_nsview(self):
        """设置NSTextField属性和绑定"""
        textfield = self._nsview
        
        # 占位符
        if self.placeholder:
            textfield.setPlaceholderString_(self.placeholder)
        
        # 双向绑定
        if self.value:
            TwoWayBinding.bind_textfield(textfield, self.value, self.on_change)
        
        # 启用状态
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(textfield, "enabled", self.enabled)
            else:
                textfield.setEnabled_(bool(self.enabled))
        
        print(f"📝 ModernTextField 创建完成")


# 向后兼容的函数式接口
def Button(
    title: Union[str, Signal[str], Computed[str]],
    on_click: Optional[Callable[[], None]] = None,
    **kwargs
) -> ModernButton:
    """创建现代化按钮 - 向后兼容接口
    
    Examples:
        # 基本用法 (兼容旧API)
        button = Button("点击我", on_click=handler)
        
        # 新功能 - 布局属性 
        button = Button("点击我", on_click=handler, width=120, margin=8)
        
        # 链式调用
        button = Button("点击我").width(120).margin(8).flex_grow(1)
    """
    return ModernButton(title, on_click, **kwargs)


def Label(
    text: Union[str, Signal[str], Computed[str]],
    **kwargs
) -> ModernLabel:
    """创建现代化标签 - 向后兼容接口"""
    return ModernLabel(text, **kwargs)


def TextField(
    value: Optional[Signal[str]] = None,
    **kwargs
) -> ModernTextField:
    """创建现代化文本框 - 向后兼容接口"""
    return ModernTextField(value, **kwargs)


# 布局增强的便捷函数
def FlexButton(
    title: Union[str, Signal[str], Computed[str]],
    on_click: Optional[Callable[[], None]] = None,
    flex_grow: float = 1.0,
    **kwargs
) -> ModernButton:
    """创建弹性按钮 - 自动占据可用空间"""
    return ModernButton(title, on_click, flex_grow=flex_grow, **kwargs)


def FixedButton(
    title: Union[str, Signal[str], Computed[str]],
    width: Union[int, float],
    on_click: Optional[Callable[[], None]] = None,
    **kwargs
) -> ModernButton:
    """创建固定宽度按钮"""
    return ModernButton(title, on_click, width=width, **kwargs)


def SpacedLabel(
    text: Union[str, Signal[str], Computed[str]],
    margin: Union[int, float] = 8,
    **kwargs
) -> ModernLabel:
    """创建带边距的标签"""
    return ModernLabel(text, margin=margin, **kwargs)