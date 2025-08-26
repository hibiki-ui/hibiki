from typing import Optional, Callable, Union, Any
from core.signal import Signal, Computed
from core.binding import ReactiveBinding, TwoWayBinding, EventBinding

import objc
from AppKit import (
    NSButton, NSTextField, NSImageView, NSSlider, NSSwitch,
    NSButtonTypeMomentaryPushIn, NSTextFieldRoundedBezel
)
from Foundation import NSString, NSRect, NSMakeRect


def Button(
    title: Union[str, Signal[str], Computed[str]], 
    on_click: Optional[Callable[[], None]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """
    创建响应式按钮
    
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
    
    # 标题绑定
    if isinstance(title, (Signal, Computed)):
        ReactiveBinding.bind(button, 'title', title)
    else:
        button.setTitle_(str(title))
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(button, 'enabled', enabled)
        else:
            button.setEnabled_(bool(enabled))
    
    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(button, 'tooltip', tooltip)
        else:
            button.setToolTip_(str(tooltip))
    
    # 点击事件处理
    if on_click:
        EventBinding.bind_click(button, on_click)
    
    return button


def TextField(
    value: Optional[Signal[str]] = None,
    placeholder: str = "",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[str], None]] = None,
    on_enter: Optional[Callable[[], None]] = None,
    frame: Optional[tuple] = None
) -> NSTextField:
    """
    创建响应式文本框 (支持双向绑定)
    
    Args:
        value: 文本值信号 (双向绑定)
        placeholder: 占位符文本
        enabled: 启用状态 (支持响应式)
        on_change: 文本改变回调
        on_enter: 回车键回调
        frame: 文本框框架
    
    Returns:
        NSTextField 实例
    """
    field = NSTextField.alloc().init()
    field.setBezelStyle_(NSTextFieldRoundedBezel)
    
    if frame:
        field.setFrame_(NSMakeRect(*frame))
    
    # 占位符
    if placeholder:
        field.setPlaceholderString_(placeholder)
    
    # 值绑定
    if value is not None:
        if isinstance(value, Signal):
            # 双向绑定
            TwoWayBinding.bind_text_field(field, value)
        else:
            # 单向绑定
            ReactiveBinding.bind(field, 'text', value)
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(field, 'enabled', enabled)
        else:
            field.setEnabled_(bool(enabled))
    
    # 事件处理
    if value and isinstance(value, Signal):
        # 双向绑定 - 文本变更时更新信号
        EventBinding.bind_text_change(field, signal=value, handler=on_change)
    elif on_change:
        # 只有变更处理器
        EventBinding.bind_text_change(field, handler=on_change)
    
    return field


def Label(
    text: Union[str, Signal[str], Computed[str]],
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSTextField:
    """
    创建响应式标签
    
    Args:
        text: 标签文本 (支持响应式)
        enabled: 启用状态 (支持响应式)
        tooltip: 工具提示 (支持响应式)
        frame: 标签框架
    
    Returns:
        NSTextField 实例 (configured as label)
    """
    label = NSTextField.alloc().init()
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    
    if frame:
        label.setFrame_(NSMakeRect(*frame))
    
    # 文本绑定
    if isinstance(text, (Signal, Computed)):
        ReactiveBinding.bind(label, 'text', text)
    else:
        label.setStringValue_(str(text))
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(label, 'enabled', enabled)
        else:
            label.setEnabled_(bool(enabled))
    
    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(label, 'tooltip', tooltip)
        else:
            label.setToolTip_(str(tooltip))
    
    return label


def Slider(
    value: Optional[Signal[float]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[float], None]] = None,
    frame: Optional[tuple] = None
) -> NSSlider:
    """
    创建响应式滑块
    
    Args:
        value: 滑块值信号 (双向绑定)
        min_value: 最小值
        max_value: 最大值
        enabled: 启用状态 (支持响应式)
        on_change: 值改变回调
        frame: 滑块框架
    
    Returns:
        NSSlider 实例
    """
    slider = NSSlider.alloc().init()
    
    if frame:
        slider.setFrame_(NSMakeRect(*frame))
    
    # 设置范围
    slider.setMinValue_(min_value)
    slider.setMaxValue_(max_value)
    
    # 值绑定
    if value is not None:
        if isinstance(value, Signal):
            # 双向绑定 (需要在实际实现中处理)
            ReactiveBinding.bind(slider, 'doubleValue', value)
        else:
            slider.setDoubleValue_(float(value))
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(slider, 'enabled', enabled)
        else:
            slider.setEnabled_(bool(enabled))
    
    # 事件处理
    if on_change:
        # 在实际实现中设置目标-动作
        pass
    
    return slider


def Switch(
    value: Optional[Signal[bool]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[bool], None]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """
    创建响应式开关 (NSButton configured as switch)
    
    Args:
        value: 开关状态信号 (双向绑定)
        enabled: 启用状态 (支持响应式)
        on_change: 状态改变回调
        frame: 开关框架
    
    Returns:
        NSButton 实例 (configured as switch)
    """
    switch = NSButton.alloc().init()
    switch.setButtonType_(3)  # NSButtonTypeSwitch
    
    if frame:
        switch.setFrame_(NSMakeRect(*frame))
    
    # 状态绑定
    if value is not None:
        if isinstance(value, Signal):
            # 双向绑定 (需要在实际实现中处理)
            def update_switch_state():
                switch.setState_(1 if value.value else 0)
            
            from ..core.signal import Effect
            Effect(update_switch_state)
        else:
            switch.setState_(1 if bool(value) else 0)
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(switch, 'enabled', enabled)
        else:
            switch.setEnabled_(bool(enabled))
    
    # 事件处理
    if on_change:
        # 在实际实现中设置目标-动作
        pass
    
    return switch


def ImageView(
    image: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSImageView:
    """
    创建图像视图
    
    Args:
        image: NSImage 对象或图像路径
        frame: 图像视图框架
    
    Returns:
        NSImageView 实例
    """
    image_view = NSImageView.alloc().init()
    
    if frame:
        image_view.setFrame_(NSMakeRect(*frame))
    
    if image:
        image_view.setImage_(image)
    
    return image_view