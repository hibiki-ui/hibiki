"""基础控件 - Button, Label, TextField

这些是macUI最基本的交互控件，提供文本显示、输入和基础操作功能。
"""

from typing import Any, Callable, Optional, Union

from AppKit import (
    NSButton,
    NSButtonTypeMomentaryPushIn,
    NSTextField,
    NSTextFieldRoundedBezel,
)
from Foundation import NSMakeRect

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding, EnhancedTextFieldDelegate
from ..core.signal import Computed, Signal


def Button(
    title: Union[str, Signal[str], Computed[str]],
    on_click: Optional[Callable[[], None]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """创建响应式按钮
    
    Args:
        title: 按钮标题 (支持响应式)
        on_click: 点击回调函数
        enabled: 启用状态 (支持响应式)  
        tooltip: 工具提示 (支持响应式)
        frame: 按钮框架 (x, y, width, height)
    
    Returns:
        NSButton 实例
    """
    button = NSButton.alloc().init()
    button.setButtonType_(NSButtonTypeMomentaryPushIn)

    if frame:
        button.setFrame_(NSMakeRect(*frame))
        print(f"🎯 按钮显式设置frame: {frame}")
    else:
        # 确保按钮有合理的默认尺寸
        button.setFrame_(NSMakeRect(0, 0, 100, 32))  # 提供合理默认尺寸
        print(f"🎯 按钮使用默认frame: (0, 0, 100, 32)")

    # 标题绑定
    if isinstance(title, (Signal, Computed)):
        ReactiveBinding.bind(button, "title", title)
        print(f"🏷️ 按钮标题绑定到Signal/Computed")
    else:
        button.setTitle_(str(title))
        print(f"🏷️ 按钮设置标题: '{str(title)}'")
        
        # 根据标题内容调整按钮大小
        if not frame:  # 只有在没有显式frame时才自动调整
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
    frame: Optional[tuple] = None,
    color: Optional[Any] = None,
    alignment: Optional[Any] = None,
    font: Optional[Any] = None,
    selectable: bool = False,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None
) -> NSTextField:
    """创建响应式标签
    
    Args:
        text: 显示文本 (支持响应式)
        frame: 标签框架 (x, y, width, height)
        color: 文本颜色
        alignment: 文本对齐方式
        font: 字体
        selectable: 是否可选择文本
        tooltip: 工具提示 (支持响应式)
    
    Returns:
        NSTextField 实例（作为标签使用）
    """
    label = NSTextField.alloc().init()
    
    # 设置标签样式
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    label.setEditable_(False)
    label.setSelectable_(selectable)
    
    if frame:
        label.setFrame_(NSMakeRect(*frame))
    
    # 文本绑定
    if isinstance(text, (Signal, Computed)):
        ReactiveBinding.bind(label, "text", text)
    else:
        label.setStringValue_(str(text))
    
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