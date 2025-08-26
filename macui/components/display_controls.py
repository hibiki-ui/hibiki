"""显示控件 - ImageView, ProgressBar, TextArea

这些控件主要用于显示内容，包括图像、进度和多行文本。
"""

from typing import Any, Callable, Optional, Union

from AppKit import (
    NSImageView,
    NSProgressIndicator,
    NSScrollView,
    NSTextView,
    NSFont,
)
from Foundation import NSMakeRect

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedTextViewDelegate
from ..core.signal import Computed, Signal


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
        if not indeterminate:  # 如果不是不确定但选择了spinning样式
            progress.setIndeterminate_(False)
    else:
        progress.setStyle_(0)  # NSProgressIndicatorBarStyle
        progress.setIndeterminate_(indeterminate)

    # 设置初始值
    initial_value = min_value
    if value is not None:
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

    # 值绑定
    if value is not None and isinstance(value, Signal):
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