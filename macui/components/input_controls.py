"""输入控件 - Slider, Switch, Checkbox, RadioButton, SegmentedControl

这些控件用于用户数据输入和选择，提供各种交互方式。
"""

from typing import Any, Callable, List, Optional, Union

from AppKit import (
    NSButton,
    NSButtonTypeSwitch,
    NSButtonTypeRadio,
    NSSegmentedControl,
    NSSlider,
)
from Foundation import NSMakeRect

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding, EnhancedSliderDelegate, EnhancedButtonDelegate, EnhancedRadioDelegate, EnhancedSegmentedDelegate
from ..core.signal import Computed, Signal


def Slider(
    value: Optional[Signal[float]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    step_size: Optional[float] = None,
    orientation: str = "horizontal",  # "horizontal", "vertical"
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[float], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSSlider:
    """创建增强的响应式滑块
    
    Args:
        value: 滑块值信号 (双向绑定)
        min_value: 最小值
        max_value: 最大值
        step_size: 步长值 (可选)
        orientation: 方向 ("horizontal", "vertical")
        enabled: 启用状态 (支持响应式)
        on_change: 值改变回调
        tooltip: 工具提示 (支持响应式)
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
    
    # 设置步长
    if step_size is not None:
        # NSSlider doesn't have direct step support, but we can handle it in the delegate
        pass

    # 设置方向
    if orientation == "vertical":
        slider.setVertical_(True)
    else:
        slider.setVertical_(False)

    # 初始值设置
    initial_value = 0.0
    if value is not None:
        initial_value = value.value if isinstance(value, Signal) else float(value)
        slider.setDoubleValue_(initial_value)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(slider, "enabled", enabled)
        else:
            slider.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(slider, "tooltip", tooltip)
        else:
            slider.setToolTip_(str(tooltip))

    # 值绑定和事件处理
    if value is not None and isinstance(value, Signal):
        # 双向绑定：Slider -> Signal
        TwoWayBinding.bind_slider(slider, value)
    
    if on_change or step_size is not None:
        # 创建增强的委托类来处理事件
        delegate = EnhancedSliderDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.step_size = step_size
        delegate.signal = value if isinstance(value, Signal) else None
        
        slider.setTarget_(delegate)
        slider.setAction_("sliderChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(slider, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return slider


def Switch(
    value: Optional[Signal[bool]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[bool], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """创建响应式开关 (NSButton configured as switch)
    
    Args:
        value: 开关状态信号 (双向绑定)
        enabled: 启用状态 (支持响应式)
        on_change: 状态改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 开关框架
    
    Returns:
        NSButton 实例 (configured as switch)
    """
    switch = NSButton.alloc().init()
    switch.setButtonType_(3)  # NSButtonTypeSwitch

    if frame:
        switch.setFrame_(NSMakeRect(*frame))

    # 初始状态设置
    initial_state = False
    if value is not None:
        initial_state = value.value if isinstance(value, Signal) else bool(value)
    switch.setState_(1 if initial_state else 0)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(switch, "enabled", enabled)
        else:
            switch.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(switch, "tooltip", tooltip)
        else:
            switch.setToolTip_(str(tooltip))

    # 状态绑定和事件处理
    if value is not None and isinstance(value, Signal):
        TwoWayBinding.bind_button_state(switch, value)
    
    if on_change:
        # 创建按钮状态委托
        delegate = EnhancedButtonDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = value if isinstance(value, Signal) else None
        
        switch.setTarget_(delegate)
        switch.setAction_("buttonStateChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(switch, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return switch


def Checkbox(
    value: Optional[Signal[bool]] = None,
    text: str = "",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[bool], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """创建复选框组件
    
    Args:
        value: 复选框状态信号 (双向绑定)
        text: 复选框旁边的文本
        enabled: 启用状态 (支持响应式)
        on_change: 状态改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 复选框框架
    
    Returns:
        NSButton 实例 (configured as checkbox)
    """
    checkbox = NSButton.alloc().init()
    checkbox.setButtonType_(NSButtonTypeSwitch)  # Switch type for checkbox

    if frame:
        checkbox.setFrame_(NSMakeRect(*frame))

    # 设置文本
    if text:
        checkbox.setTitle_(text)

    # 初始状态设置
    initial_state = False
    if value is not None:
        initial_state = value.value if isinstance(value, Signal) else bool(value)
    checkbox.setState_(1 if initial_state else 0)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(checkbox, "enabled", enabled)
        else:
            checkbox.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(checkbox, "tooltip", tooltip)
        else:
            checkbox.setToolTip_(str(tooltip))

    # 状态绑定和事件处理
    if value is not None and isinstance(value, Signal):
        TwoWayBinding.bind_button_state(checkbox, value)
    
    if on_change:
        # 创建按钮状态委托
        delegate = EnhancedButtonDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = value if isinstance(value, Signal) else None
        
        checkbox.setTarget_(delegate)
        checkbox.setAction_("buttonStateChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(checkbox, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return checkbox


def RadioButton(
    value: Signal[str],
    option_value: str,
    text: str = "",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[str], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSButton:
    """创建单选按钮组件
    
    Args:
        value: 单选按钮组的值信号 (所有按钮共享同一个Signal)
        option_value: 这个按钮代表的选项值
        text: 单选按钮旁边的文本
        enabled: 启用状态 (支持响应式)
        on_change: 状态改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 单选按钮框架
    
    Returns:
        NSButton 实例 (configured as radio button)
    """
    radio = NSButton.alloc().init()
    radio.setButtonType_(NSButtonTypeRadio)

    if frame:
        radio.setFrame_(NSMakeRect(*frame))

    # 设置文本
    if text:
        radio.setTitle_(text)

    # 初始状态设置
    initial_selected = value.value == option_value
    radio.setState_(1 if initial_selected else 0)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(radio, "enabled", enabled)
        else:
            radio.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(radio, "tooltip", tooltip)
        else:
            radio.setToolTip_(str(tooltip))

    # 双向绑定和事件处理
    TwoWayBinding.bind_radio_button(radio, value, option_value)
    
    if on_change:
        # 创建单选按钮委托
        delegate = EnhancedRadioDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = value
        delegate.option_value = option_value
        
        radio.setTarget_(delegate)
        radio.setAction_("radioButtonChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(radio, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return radio


def SegmentedControl(
    value: Optional[Signal[int]] = None,
    segments: List[str] = [],
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[int], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSSegmentedControl:
    """创建分段控件
    
    Args:
        value: 选中段索引信号 (双向绑定)
        segments: 段标题列表
        enabled: 启用状态 (支持响应式)
        on_change: 选择改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 控件框架
    
    Returns:
        NSSegmentedControl 实例
    """
    segmented = NSSegmentedControl.alloc().init()

    if frame:
        segmented.setFrame_(NSMakeRect(*frame))

    # 设置段
    segmented.setSegmentCount_(len(segments))
    for i, title in enumerate(segments):
        segmented.setLabel_forSegment_(title, i)
        segmented.setWidth_forSegment_(0, i)  # 自动调整宽度

    # 初始选择设置
    initial_selection = 0
    if value is not None:
        initial_selection = value.value if isinstance(value, Signal) else int(value)
    segmented.setSelectedSegment_(initial_selection)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(segmented, "enabled", enabled)
        else:
            segmented.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(segmented, "tooltip", tooltip)
        else:
            segmented.setToolTip_(str(tooltip))

    # 双向绑定和事件处理
    if value is not None and isinstance(value, Signal):
        TwoWayBinding.bind_segmented_control(segmented, value)
    
    if on_change:
        # 创建分段控件委托
        delegate = EnhancedSegmentedDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = value if isinstance(value, Signal) else None
        
        segmented.setTarget_(delegate)
        segmented.setAction_("segmentChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(segmented, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return segmented