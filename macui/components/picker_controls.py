"""时间选择控件 - DatePicker, TimePicker

这些控件用于日期和时间的选择输入。
"""

from typing import Any, Callable, Optional, Union

from AppKit import (
    NSDatePicker,
    NSDatePickerStyleTextField,
    NSDatePickerStyleTextFieldAndStepper,
    NSDatePickerStyleClockAndCalendar,
    NSDatePickerElementFlagHourMinute,
    NSDatePickerElementFlagYearMonth,
    NSDatePickerElementFlagYearMonthDay,
)
from Foundation import NSMakeRect

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedDatePickerDelegate
from ..core.signal import Computed, Signal


def DatePicker(
    date: Optional[Any] = None,  # NSDate 或 Signal[NSDate]
    style: str = "textfield",  # "textfield", "stepper", "calendar"
    date_only: bool = False,
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[Any], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSDatePicker:
    """创建日期选择器
    
    Args:
        date: 当前日期值 (支持响应式)
        style: 显示样式 ("textfield", "stepper", "calendar")
        date_only: 是否只显示日期（不显示时间）
        enabled: 启用状态 (支持响应式)
        on_change: 日期变更回调函数
        tooltip: 工具提示 (支持响应式)
        frame: 日期选择器框架
    
    Returns:
        NSDatePicker 实例
    """
    date_picker = NSDatePicker.alloc().init()
    
    if frame:
        date_picker.setFrame_(NSMakeRect(*frame))
    
    # 设置显示样式
    style_map = {
        "textfield": NSDatePickerStyleTextField,
        "stepper": NSDatePickerStyleTextFieldAndStepper,
        "calendar": NSDatePickerStyleClockAndCalendar
    }
    date_picker.setDatePickerStyle_(style_map.get(style, NSDatePickerStyleTextFieldAndStepper))
    
    # 设置显示元素
    if date_only:
        date_picker.setDatePickerElements_(NSDatePickerElementFlagYearMonthDay)
    else:
        # 显示日期和时间
        date_picker.setDatePickerElements_(NSDatePickerElementFlagYearMonthDay | NSDatePickerElementFlagHourMinute)
    
    # 设置初始日期
    if date is not None:
        if isinstance(date, Signal):
            # 响应式绑定日期
            TwoWayBinding.bind_date_picker(date_picker, date)
        else:
            date_picker.setDateValue_(date)
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(date_picker, "enabled", enabled)
        else:
            date_picker.setEnabled_(bool(enabled))
    
    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(date_picker, "tooltip", tooltip)
        else:
            date_picker.setToolTip_(str(tooltip))
    
    # 事件处理
    if on_change or (isinstance(date, Signal)):
        # 创建日期选择器委托
        delegate = EnhancedDatePickerDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = date if isinstance(date, Signal) else None
        
        date_picker.setDelegate_(delegate)
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(date_picker, b"enhanced_date_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return date_picker


def TimePicker(
    time: Optional[Any] = None,  # NSDate 或 Signal[NSDate]
    style: str = "stepper",
    enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
    on_change: Optional[Callable[[Any], None]] = None,
    tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
    frame: Optional[tuple] = None
) -> NSDatePicker:
    """创建时间选择器
    
    Args:
        time: 当前时间值 (支持响应式)
        style: 显示样式 ("textfield", "stepper")
        enabled: 启用状态 (支持响应式)
        on_change: 时间变更回调函数
        tooltip: 工具提示 (支持响应式)
        frame: 时间选择器框架
    
    Returns:
        NSDatePicker 实例（配置为只显示时间）
    """
    time_picker = NSDatePicker.alloc().init()
    
    if frame:
        time_picker.setFrame_(NSMakeRect(*frame))
    
    # 设置显示样式
    style_map = {
        "textfield": NSDatePickerStyleTextField,
        "stepper": NSDatePickerStyleTextFieldAndStepper
    }
    time_picker.setDatePickerStyle_(style_map.get(style, NSDatePickerStyleTextFieldAndStepper))
    
    # 设置只显示时间
    time_picker.setDatePickerElements_(NSDatePickerElementFlagHourMinute)
    
    # 设置初始时间
    if time is not None:
        if isinstance(time, Signal):
            # 响应式绑定时间
            TwoWayBinding.bind_date_picker(time_picker, time)
        else:
            time_picker.setDateValue_(time)
    
    # 启用状态绑定
    if enabled is not None:
        if isinstance(enabled, (Signal, Computed)):
            ReactiveBinding.bind(time_picker, "enabled", enabled)
        else:
            time_picker.setEnabled_(bool(enabled))
    
    # 工具提示绑定
    if tooltip is not None:
        if isinstance(tooltip, (Signal, Computed)):
            ReactiveBinding.bind(time_picker, "tooltip", tooltip)
        else:
            time_picker.setToolTip_(str(tooltip))
    
    # 事件处理
    if on_change or (isinstance(time, Signal)):
        # 创建时间选择器委托
        delegate = EnhancedDatePickerDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = time if isinstance(time, Signal) else None
        
        time_picker.setDelegate_(delegate)
        
        # 保持委托引用
        import objc
        objc.setAssociatedObject(time_picker, b"enhanced_time_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
    
    return time_picker