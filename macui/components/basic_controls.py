"""基础控件 - Button, Label, TextField

这些是macUI最基本的交互控件，提供文本显示、输入和基础操作功能。
"""

from typing import Any, Callable, Optional, Union

from AppKit import (
    NSButton,
    NSButtonTypeMomentaryPushIn,
    NSTextField,
    NSTextFieldRoundedBezel,
    NSLineBreakByWordWrapping,
    NSLineBreakByCharWrapping,
    NSLineBreakByClipping,
    NSLineBreakByTruncatingTail,
    NSLineBreakByTruncatingHead,
    NSLineBreakByTruncatingMiddle,
)
from Foundation import NSMakeRect
from enum import Enum

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding, EnhancedTextFieldDelegate
from ..core.signal import Computed, Signal
from ..layout.styles import LayoutStyle


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


def _apply_label_style_preset(style: LabelStyle) -> dict:
    """根据预设样式返回配置字典
    
    为常见使用场景提供优化的预设配置，简化接口使用。
    
    Args:
        style: 预设样式枚举
        
    Returns:
        包含配置参数的字典
    """
    if style == LabelStyle.MULTILINE:
        # 多行描述文本 - 默认配置，适合大多数场景
        return {
            'multiline': True,
            'line_break_mode': LineBreakMode.WORD_WRAPPING,
            'wraps': True,
            'scrollable': False,
            'preferred_max_width': 400.0
        }
    elif style == LabelStyle.TITLE:
        # 单行标题 - 适合状态栏、标题等
        return {
            'multiline': False,
            'line_break_mode': LineBreakMode.CLIPPING,
            'wraps': False,
            'scrollable': False,
            'preferred_max_width': None  # 单行不需要最大宽度限制
        }
    elif style == LabelStyle.TRUNCATED:
        # 单行截断 - 适合列表项、文件名等
        return {
            'multiline': False,
            'line_break_mode': LineBreakMode.TRUNCATE_TAIL,
            'wraps': False,
            'scrollable': False,
            'preferred_max_width': None
        }
    elif style == LabelStyle.FIXED_WIDTH:
        # 固定宽度 - 适合表单字段、固定布局
        return {
            'multiline': True,
            'line_break_mode': LineBreakMode.WORD_WRAPPING,
            'wraps': True,
            'scrollable': False,
            'preferred_max_width': 200.0  # 较小的固定宽度
        }
    else:
        # 默认配置（等同于MULTILINE）
        return {
            'multiline': True,
            'line_break_mode': LineBreakMode.WORD_WRAPPING,
            'wraps': True,
            'scrollable': False,
            'preferred_max_width': 400.0
        }


def Button(
    title: Union[str, Signal[str], Computed[str]],
    on_click: Optional[Callable[[], None]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    style: Optional['LayoutStyle'] = None
) -> NSButton:
    """创建响应式按钮
    
    Args:
        title: 按钮标题 (支持响应式)
        on_click: 点击回调函数
        enabled: 启用状态 (支持响应式)  
        tooltip: 工具提示 (支持响应式)
        style: 布局样式 (LayoutStyle对象)
    
    Returns:
        NSButton 实例
    """
    button = NSButton.alloc().init()
    button.setButtonType_(NSButtonTypeMomentaryPushIn)

    # 根据style设置frame或使用默认尺寸
    if style and (style.width or style.height):
        width = style.width or 100
        height = style.height or 32
        button.setFrame_(NSMakeRect(0, 0, width, height))
        print(f"🎯 按钮使用style尺寸: ({width}, {height})")
    else:
        # 确保按钮有合理的默认尺寸
        button.setFrame_(NSMakeRect(0, 0, 100, 32))
        print(f"🎯 按钮使用默认frame: (0, 0, 100, 32)")

    # 标题绑定
    if isinstance(title, (Signal, Computed)):
        ReactiveBinding.bind(button, "title", title)
        print(f"🏷️ 按钮标题绑定到Signal/Computed")
    else:
        button.setTitle_(str(title))
        print(f"🏷️ 按钮设置标题: '{str(title)}'")
        
        # 根据标题内容调整按钮大小
        if not (style and (style.width or style.height)):  # 只有在没有显式尺寸时才自动调整
            button.sizeToFit()
            new_size = button.frame().size
            print(f"📏 按钮sizeToFit后尺寸: {new_size.width:.1f} x {new_size.height:.1f}")

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(button, "enabled", enabled)
        else:
            button.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(button, "tooltip", tooltip)
        else:
            button.setToolTip_(str(tooltip))

    # 点击事件处理
    if on_click:
        EventBinding.bind_click(button, on_click)

    return button


def TextField(
    value: Optional[Union[str, Signal[str]]] = None,
    placeholder: Optional[Union[str, Signal[str], Computed[str]]] = None,
    on_change: Optional[Callable[[str], None]] = None,
    on_enter: Optional[Callable[[str], None]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    secure: bool = False,
    frame: Optional[tuple] = None
) -> NSTextField:
    """创建响应式文本输入框
    
    Args:
        value: 文本值 (支持双向绑定)
        placeholder: 占位文本 (支持响应式)
        on_change: 文本变化回调
        on_enter: 按下回车键回调
        enabled: 启用状态 (支持响应式)
        secure: 是否为密码输入框
        frame: 输入框框架 (x, y, width, height)
    
    Returns:
        NSTextField 实例
    """
    text_field = NSTextField.alloc().init()
    
    # 设置样式
    text_field.setBezeled_(True)
    text_field.setBezelStyle_(NSTextFieldRoundedBezel)
    text_field.setDrawsBackground_(True)
    
    if frame:
        text_field.setFrame_(NSMakeRect(*frame))
    
    # 设置是否为安全输入
    if secure:
        from AppKit import NSSecureTextField
        # 对于密码字段，使用NSSecureTextField
        secure_field = NSSecureTextField.alloc().init()
        secure_field.setBezeled_(True)
        secure_field.setBezelStyle_(NSTextFieldRoundedBezel)
        secure_field.setDrawsBackground_(True)
        if frame:
            secure_field.setFrame_(NSMakeRect(*frame))
        text_field = secure_field
    
    # 设置值 - 支持双向绑定
    if value is not None:
        if isinstance(value, Signal):
            # 双向绑定
            TwoWayBinding.bind_text_field(text_field, value)
        else:
            text_field.setStringValue_(str(value))
    
    # 占位文本绑定
    if placeholder is not None:
        if isinstance(placeholder, (Signal, Computed)):
            ReactiveBinding.bind(text_field, "placeholderString", placeholder)
        else:
            text_field.setPlaceholderString_(str(placeholder))
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(text_field, "enabled", enabled)
        else:
            text_field.setEnabled_(bool(enabled))
    
    # 创建并设置代理
    if on_change or on_enter:
        delegate = EnhancedTextFieldDelegate.alloc().init()
        if on_change:
            delegate.on_change = on_change
        if on_enter:
            delegate.on_enter = on_enter
        text_field.setDelegate_(delegate)
        
        # 保持代理引用
        import objc
        objc.setAssociatedObject(text_field, b"delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return text_field


def Label(
    text: Union[str, Signal[str], Computed[str]],
    color: Optional[Any] = None,
    alignment: Optional[Any] = None,
    font: Optional[Any] = None,
    selectable: bool = False,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    multiline: bool = True,
    line_break_mode: LineBreakMode = LineBreakMode.WORD_WRAPPING,
    wraps: bool = True,
    scrollable: bool = False,
    preferred_max_width: Optional[float] = None,
    style: Optional['LayoutStyle'] = None
) -> NSTextField:
    """创建响应式标签
    
    Args:
        text: 显示文本 (支持响应式)
        color: 文本颜色
        alignment: 文本对齐方式
        font: 字体
        selectable: 是否可选择文本
        tooltip: 工具提示 (支持响应式)
        multiline: 是否支持多行显示
        line_break_mode: 文本换行/截断模式
        wraps: 是否启用文本换行
        scrollable: 是否可滚动
        preferred_max_width: 首选最大宽度（优先级低于style中的width）
        style: 布局样式 (LayoutStyle对象)
    
    Returns:
        NSTextField 实例（作为标签使用）
    """
    label = NSTextField.alloc().init()
    
    # 设置标签样式
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(selectable)
    
    # 配置文本显示属性
    label.setUsesSingleLineMode_(not multiline)
    label.setLineBreakMode_(line_break_mode.value)
    
    # 配置Cell属性
    text_cell = label.cell()
    text_cell.setWraps_(wraps)
    text_cell.setScrollable_(scrollable)
    
    # 设置最大宽度 - style中的width优先级最高，其次是preferred_max_width参数
    max_width = None
    if style and style.width:
        max_width = float(style.width)
    elif preferred_max_width is not None:
        max_width = preferred_max_width
    elif multiline:  # 多行模式使用默认最大宽度
        max_width = 400.0
    
    if max_width is not None:
        label.setPreferredMaxLayoutWidth_(max_width)
    
    mode_desc = "多行" if multiline else "单行"
    width_desc = f"最大宽度={max_width:.1f}px" if max_width else "无宽度限制"
    print(f"✅ Label配置: {mode_desc}模式, {width_desc}")
    
    # 文本绑定
    if isinstance(text, (Signal, Computed)):
        ReactiveBinding.bind(label, "text", text)
    else:
        label.setStringValue_(str(text))
        # 文本变化后，需要重新计算intrinsic content size
        label.invalidateIntrinsicContentSize()
    
    # 设置颜色
    if color:
        label.setTextColor_(color)
    
    # 设置对齐方式
    if alignment:
        label.setAlignment_(alignment)
    
    # 设置字体
    if font:
        label.setFont_(font)
    
    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(label, "tooltip", tooltip)
        else:
            label.setToolTip_(str(tooltip))
    
    return label