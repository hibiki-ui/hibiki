from typing import Any, Callable, Optional, Union

from AppKit import (
    NSButton,
    NSButtonTypeMomentaryPushIn,
    NSButtonTypeSwitch,
    NSButtonTypeRadio,
    NSImageView,
    NSPopUpButton,
    NSProgressIndicator,
    NSSegmentedControl,
    NSSlider,
    NSTextField,
    NSTextFieldRoundedBezel,
    NSTextView,
    NSScrollView,
)
from Foundation import NSMakeRect

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding, EnhancedTextFieldDelegate, EnhancedSliderDelegate, EnhancedTextViewDelegate, EnhancedButtonDelegate, EnhancedRadioDelegate, EnhancedSegmentedDelegate, EnhancedPopUpDelegate
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

    # 标题绑定
    if isinstance(title, (Signal, Computed)):
        ReactiveBinding.bind(button, "title", title)
    else:
        button.setTitle_(str(title))

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
    placeholder: str = "",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    editable: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    secure: bool = False,
    multiline: bool = False,
    font_size: Optional[float] = None,
    alignment: str = "left",  # "left", "center", "right"
    max_length: Optional[int] = None,
    validation: Optional[Callable[[str], bool]] = None,
    formatting: Optional[Callable[[str], str]] = None,
    on_change: Optional[Callable[[str], None]] = None,
    on_enter: Optional[Callable[[], None]] = None,
    on_focus: Optional[Callable[[], None]] = None,
    on_blur: Optional[Callable[[], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSTextField:
    """创建增强的响应式文本框
    
    Args:
        value: 文本值 (字符串或Signal，支持双向绑定)
        placeholder: 占位符文本
        enabled: 启用状态 (支持响应式)
        editable: 可编辑状态 (支持响应式)
        secure: 是否为密码框 (隐藏文本)
        multiline: 是否支持多行 (创建NSTextView)
        font_size: 字体大小
        alignment: 文本对齐 ("left", "center", "right")
        max_length: 最大字符长度限制
        validation: 输入验证函数
        formatting: 文本格式化函数
        on_change: 文本改变回调
        on_enter: 回车键回调
        on_focus: 获得焦点回调
        on_blur: 失去焦点回调
        tooltip: 工具提示 (支持响应式)
        frame: 文本框框架
    
    Returns:
        NSTextField 或 NSSecureTextField 或 NSTextView 实例
    """
    # 根据类型创建不同的文本控件
    if secure:
        from AppKit import NSSecureTextField
        field = NSSecureTextField.alloc().init()
    elif multiline:
        from AppKit import NSTextView
        field = NSTextView.alloc().init()
        # NSTextView 需要滚动容器
        from AppKit import NSScrollView
        scroll_view = NSScrollView.alloc().init()
        scroll_view.setDocumentView_(field)
        field._scroll_container = scroll_view
    else:
        field = NSTextField.alloc().init()
        field.setBezelStyle_(NSTextFieldRoundedBezel)

    # 设置框架
    if frame:
        if multiline and hasattr(field, '_scroll_container'):
            field._scroll_container.setFrame_(NSMakeRect(*frame))
        else:
            field.setFrame_(NSMakeRect(*frame))

    # 占位符 (NSTextView 不支持占位符)
    if placeholder and not multiline:
        field.setPlaceholderString_(placeholder)

    # 初始值设置
    if value is not None:
        initial_value = value.value if isinstance(value, Signal) else str(value)
        if multiline:
            field.setString_(initial_value)
        else:
            field.setStringValue_(initial_value)

    # 可编辑状态
    if editable is not None:
        if isinstance(editable, (Signal, Computed)):
            ReactiveBinding.bind(field, "editable" if multiline else "editable", editable)
        else:
            field.setEditable_(bool(editable))

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(field, "enabled", enabled)
        else:
            field.setEnabled_(bool(enabled))

    # 字体大小
    if font_size:
        from AppKit import NSFont
        font = NSFont.systemFontOfSize_(font_size)
        field.setFont_(font)

    # 文本对齐
    if alignment != "left" and not multiline:
        from AppKit import NSTextAlignment
        alignment_map = {
            "left": NSTextAlignment.NSLeftTextAlignment,
            "center": NSTextAlignment.NSCenterTextAlignment,
            "right": NSTextAlignment.NSRightTextAlignment
        }
        if alignment in alignment_map:
            field.setAlignment_(alignment_map[alignment])

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(field, "tooltip", tooltip)
        else:
            field.setToolTip_(str(tooltip))

    # 值绑定（双向绑定）
    if value is not None and isinstance(value, Signal):
        TwoWayBinding.bind_text_field(field, value)

    # 事件处理增强
    if on_change or on_enter or on_focus or on_blur or validation or formatting or max_length:
        # 创建增强的委托类
        delegate = EnhancedTextFieldDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.on_enter = on_enter
        delegate.on_focus = on_focus
        delegate.on_blur = on_blur
        delegate.validation = validation
        delegate.formatting = formatting
        delegate.max_length = max_length
        delegate.signal = value if isinstance(value, Signal) else None
        
        field.setDelegate_(delegate)
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(field, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    # 返回适当的控件
    if multiline and hasattr(field, '_scroll_container'):
        return field._scroll_container
    return field


def Label(
    text: Union[str, Signal[str], Computed[str]],
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSTextField:
    """创建响应式标签
    
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
        print(f"🏷️ Label[{id(label)}]: 创建响应式文本绑定到 {type(text).__name__}[{id(text)}]")
        ReactiveBinding.bind(label, "text", text)
        print(f"🏷️ Label[{id(label)}]: 响应式绑定已创建")
    else:
        print(f"🏷️ Label[{id(label)}]: 设置静态文本: '{str(text)}'")
        label.setStringValue_(str(text))

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(label, "enabled", enabled)
        else:
            label.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(label, "tooltip", tooltip)
        else:
            label.setToolTip_(str(tooltip))

    return label


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
        objc.setAssociatedObject(radio, b"enhanced_radio_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return radio


def SegmentedControl(
    segments: list[str],
    selected: Optional[Union[int, Signal[int]]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[int], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSSegmentedControl:
    """创建分段选择控件
    
    Args:
        segments: 分段标题列表
        selected: 当前选中的分段索引 (支持双向绑定)
        enabled: 启用状态 (支持响应式)
        on_change: 选中分段改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 控件框架
    
    Returns:
        NSSegmentedControl 实例
    """
    segmented = NSSegmentedControl.alloc().init()

    if frame:
        segmented.setFrame_(NSMakeRect(*frame))

    # 设置分段数量和标题
    segmented.setSegmentCount_(len(segments))
    for i, title in enumerate(segments):
        segmented.setLabel_forSegment_(title, i)
        segmented.setWidth_forSegment_(0, i)  # 自动宽度

    # 初始选中状态
    initial_selected = 0
    if selected is not None:
        initial_selected = selected.value if isinstance(selected, Signal) else int(selected)
        if 0 <= initial_selected < len(segments):
            segmented.setSelectedSegment_(initial_selected)

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
    if selected is not None and isinstance(selected, Signal):
        TwoWayBinding.bind_segmented_control(segmented, selected)
    
    if on_change:
        # 创建分段控件委托
        delegate = EnhancedSegmentedDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = selected if isinstance(selected, Signal) else None
        
        segmented.setTarget_(delegate)
        segmented.setAction_("segmentChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(segmented, b"enhanced_segmented_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return segmented


def PopUpButton(
    items: list[str],
    selected: Optional[Union[int, Signal[int]]] = None,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[int], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSPopUpButton:
    """创建下拉选择按钮
    
    Args:
        items: 选项列表
        selected: 当前选中的项目索引 (支持双向绑定)
        enabled: 启用状态 (支持响应式)
        on_change: 选项改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 控件框架
    
    Returns:
        NSPopUpButton 实例
    """
    popup = NSPopUpButton.alloc().init()

    if frame:
        popup.setFrame_(NSMakeRect(*frame))

    # 添加选项
    popup.removeAllItems()
    for item in items:
        popup.addItemWithTitle_(item)

    # 初始选中状态
    initial_selected = 0
    if selected is not None:
        initial_selected = selected.value if isinstance(selected, Signal) else int(selected)
        if 0 <= initial_selected < len(items):
            popup.selectItemAtIndex_(initial_selected)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(popup, "enabled", enabled)
        else:
            popup.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(popup, "tooltip", tooltip)
        else:
            popup.setToolTip_(str(tooltip))

    # 双向绑定和事件处理
    if selected is not None and isinstance(selected, Signal):
        TwoWayBinding.bind_popup_button(popup, selected)
    
    if on_change:
        # 创建下拉按钮委托
        delegate = EnhancedPopUpDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = selected if isinstance(selected, Signal) else None
        
        popup.setTarget_(delegate)
        popup.setAction_("popUpChanged:")
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(popup, b"enhanced_popup_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

    return popup


def ImageView(
    image: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSImageView:
    """创建图像视图
    
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


def ProgressBar(
    value: Optional[Union[float, Signal[float]]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    indeterminate: bool = False,
    style: str = "bar",  # "bar", "spinning"
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSProgressIndicator:
    """创建进度条组件
    
    Args:
        value: 进度值 (0-100 或 min_value-max_value 范围)
        min_value: 最小值
        max_value: 最大值
        indeterminate: 是否为不确定进度条 (旋转动画)
        style: 进度条样式 ("bar", "spinning")
        enabled: 启用状态 (支持响应式)
        tooltip: 工具提示 (支持响应式)
        frame: 进度条框架
    
    Returns:
        NSProgressIndicator 实例
    """
    progress = NSProgressIndicator.alloc().init()

    if frame:
        progress.setFrame_(NSMakeRect(*frame))

    # 设置范围
    progress.setMinValue_(min_value)
    progress.setMaxValue_(max_value)

    # 设置样式
    if style == "spinning" or indeterminate:
        progress.setStyle_(1)  # NSProgressIndicatorSpinningStyle
        progress.setIndeterminate_(True)
    else:
        progress.setStyle_(0)  # NSProgressIndicatorBarStyle
        progress.setIndeterminate_(indeterminate)

    # 初始值设置
    if value is not None and not indeterminate:
        initial_value = value.value if isinstance(value, Signal) else float(value)
        progress.setDoubleValue_(initial_value)

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(progress, "enabled", enabled)
        else:
            progress.setEnabled_(bool(enabled))

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(progress, "tooltip", tooltip)
        else:
            progress.setToolTip_(str(tooltip))

    # 值绑定 (单向绑定，进度条通常不需要用户交互)
    if value is not None and isinstance(value, Signal) and not indeterminate:
        ReactiveBinding.bind(progress, "doubleValue", value)

    # 如果是不确定进度条，开始动画
    if indeterminate:
        progress.startAnimation_(None)

    return progress


def TextArea(
    value: Optional[Union[str, Signal[str]]] = None,
    placeholder: str = "",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    editable: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    font_size: Optional[float] = None,
    on_change: Optional[Callable[[str], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建多行文本区域组件
    
    Args:
        value: 文本值 (字符串或Signal，支持双向绑定)
        placeholder: 占位符文本 (NSTextView不直接支持，但可以模拟)
        enabled: 启用状态 (支持响应式)
        editable: 可编辑状态 (支持响应式)
        font_size: 字体大小
        on_change: 文本改变回调
        tooltip: 工具提示 (支持响应式)
        frame: 文本区域框架
    
    Returns:
        NSScrollView 包含 NSTextView 的实例
    """
    # 创建 NSTextView
    text_view = NSTextView.alloc().init()
    
    # 创建滚动容器
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setDocumentView_(text_view)
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)
    scroll_view.setAutohidesScrollers_(True)
    
    # 设置文本视图属性
    text_view.setVerticallyResizable_(True)
    text_view.setHorizontallyResizable_(False)
    text_view.textContainer().setWidthTracksTextView_(True)
    
    if frame:
        scroll_view.setFrame_(NSMakeRect(*frame))
        # 调整文本视图大小
        text_view.setFrame_(NSMakeRect(0, 0, frame[2], frame[3]))

    # 初始值设置
    if value is not None:
        initial_value = value.value if isinstance(value, Signal) else str(value)
        text_view.setString_(initial_value)

    # 可编辑状态
    if editable is not None:
        if isinstance(editable, (Signal, Computed)):
            ReactiveBinding.bind(text_view, "editable", editable)
        else:
            text_view.setEditable_(bool(editable))

    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(text_view, "enabled", enabled)
        else:
            text_view.setSelectable_(bool(enabled))
            text_view.setEditable_(bool(enabled) and (editable if editable is not None else True))

    # 字体大小
    if font_size:
        from AppKit import NSFont
        font = NSFont.systemFontOfSize_(font_size)
        text_view.setFont_(font)

    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(scroll_view, "tooltip", tooltip)
        else:
            scroll_view.setToolTip_(str(tooltip))

    # 值绑定和事件处理
    if value is not None and isinstance(value, Signal):
        # 双向绑定需要特殊处理 NSTextView
        TwoWayBinding.bind_text_view(text_view, value)
    
    if on_change:
        # 创建文本视图委托
        delegate = EnhancedTextViewDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = value if isinstance(value, Signal) else None
        
        text_view.setDelegate_(delegate)
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(text_view, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    # 将 text_view 引用存储到 scroll_view 中，方便访问
    import objc
    objc.setAssociatedObject(scroll_view, b"text_view", text_view, objc.OBJC_ASSOCIATION_RETAIN)
    
    return scroll_view
