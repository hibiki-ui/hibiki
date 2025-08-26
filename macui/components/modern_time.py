"""
现代化时间组件 - 基于新布局引擎v3.0 (Stretchable)

提供支持CSS-like布局属性的现代化时间选择组件
包括DatePicker, TimePicker等
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
from Foundation import NSMakeRect, NSDate

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedDatePickerDelegate
from ..core.signal import Signal, Computed
from ..layout.styles import LayoutStyle
from .core import LayoutAwareComponent


class ModernDatePicker(LayoutAwareComponent):
    """现代化日期选择器组件 - 支持新布局系统"""
    
    def __init__(
        self,
        date: Optional[Union[Any, Signal[Any]]] = None,
        style: str = "textfield",  # "textfield", "stepper", "calendar"
        date_only: bool = False,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[Any], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化日期选择器
        
        Args:
            date: NSDate对象或Signal (响应式)
            style: 显示样式 ("textfield", "stepper", "calendar")
            date_only: 是否只显示日期
            enabled: 启用状态 (响应式)
            on_change: 日期变更回调
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        # 根据样式设置默认尺寸
        default_width = {
            "textfield": 150,
            "stepper": 200,
            "calendar": 250
        }.get(style, 150)
        
        default_height = {
            "textfield": 24,
            "stepper": 24,
            "calendar": 150 if not date_only else 120
        }.get(style, 24)
        
        layout_style = LayoutStyle(
            width=width or default_width,
            height=height or default_height,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.date = date or Signal(NSDate.date())
        self.style = style
        self.date_only = date_only
        self.enabled = enabled
        self.on_change = on_change
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSDatePicker:
        """创建NSDatePicker实例"""
        date_picker = NSDatePicker.alloc().init()
        
        # 设置显示样式
        style_map = {
            "textfield": NSDatePickerStyleTextField,
            "stepper": NSDatePickerStyleTextFieldAndStepper,
            "calendar": NSDatePickerStyleClockAndCalendar
        }
        date_picker.setDatePickerStyle_(style_map.get(self.style, NSDatePickerStyleTextFieldAndStepper))
        
        # 设置显示元素
        if self.date_only:
            date_picker.setDatePickerElements_(NSDatePickerElementFlagYearMonthDay)
        else:
            # 显示日期和时间
            date_picker.setDatePickerElements_(NSDatePickerElementFlagYearMonthDay | NSDatePickerElementFlagHourMinute)
        
        # 设置初始日期
        initial_date = self.date.value if isinstance(self.date, Signal) else self.date
        if initial_date:
            date_picker.setDateValue_(initial_date)
        
        # 设置frame
        width = self.layout_style.width
        height = self.layout_style.height
        date_picker.setFrame_(NSMakeRect(0, 0, width, height))
        
        return date_picker
    
    def _setup_nsview(self):
        """设置NSDatePicker属性和绑定"""
        date_picker = self._nsview
        
        # 双向绑定日期
        if isinstance(self.date, Signal):
            TwoWayBinding.bind_date_picker(date_picker, self.date)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(date_picker, "enabled", self.enabled)
            else:
                date_picker.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(date_picker, "tooltip", self.tooltip)
            else:
                date_picker.setToolTip_(str(self.tooltip))
        
        # 事件处理
        if self.on_change:
            delegate = EnhancedDatePickerDelegate.alloc().init()
            delegate.on_change = self.on_change
            delegate.signal = self.date if isinstance(self.date, Signal) else None
            
            date_picker.setDelegate_(delegate)
            
            # 保持委托引用
            import objc
            objc.setAssociatedObject(date_picker, b"enhanced_date_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        mode_str = "仅日期" if self.date_only else "日期时间"
        print(f"📅 ModernDatePicker 创建完成 (样式: {self.style}, 模式: {mode_str})")


class ModernTimePicker(LayoutAwareComponent):
    """现代化时间选择器组件 - 支持新布局系统"""
    
    def __init__(
        self,
        time: Optional[Union[Any, Signal[Any]]] = None,
        style: str = "stepper",
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[Any], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化时间选择器
        
        Args:
            time: NSDate对象或Signal (响应式)
            style: 显示样式 ("textfield", "stepper")
            enabled: 启用状态 (响应式)
            on_change: 时间变更回调
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        # 根据样式设置默认尺寸
        default_width = {
            "textfield": 100,
            "stepper": 120
        }.get(style, 120)
        
        layout_style = LayoutStyle(
            width=width or default_width,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.time = time or Signal(NSDate.date())
        self.style = style
        self.enabled = enabled
        self.on_change = on_change
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSDatePicker:
        """创建NSDatePicker实例 (配置为时间模式)"""
        time_picker = NSDatePicker.alloc().init()
        
        # 设置显示样式
        style_map = {
            "textfield": NSDatePickerStyleTextField,
            "stepper": NSDatePickerStyleTextFieldAndStepper
        }
        time_picker.setDatePickerStyle_(style_map.get(self.style, NSDatePickerStyleTextFieldAndStepper))
        
        # 设置只显示时间
        time_picker.setDatePickerElements_(NSDatePickerElementFlagHourMinute)
        
        # 设置初始时间
        initial_time = self.time.value if isinstance(self.time, Signal) else self.time
        if initial_time:
            time_picker.setDateValue_(initial_time)
        
        # 设置frame
        width = self.layout_style.width
        height = self.layout_style.height or 24
        time_picker.setFrame_(NSMakeRect(0, 0, width, height))
        
        return time_picker
    
    def _setup_nsview(self):
        """设置NSDatePicker属性和绑定"""
        time_picker = self._nsview
        
        # 双向绑定时间
        if isinstance(self.time, Signal):
            TwoWayBinding.bind_date_picker(time_picker, self.time)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(time_picker, "enabled", self.enabled)
            else:
                time_picker.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(time_picker, "tooltip", self.tooltip)
            else:
                time_picker.setToolTip_(str(self.tooltip))
        
        # 事件处理
        if self.on_change:
            delegate = EnhancedDatePickerDelegate.alloc().init()
            delegate.on_change = self.on_change
            delegate.signal = self.time if isinstance(self.time, Signal) else None
            
            time_picker.setDelegate_(delegate)
            
            # 保持委托引用
            import objc
            objc.setAssociatedObject(time_picker, b"enhanced_time_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        print(f"⏰ ModernTimePicker 创建完成 (样式: {self.style})")


# 向后兼容的函数式接口
def DatePicker(
    date: Optional[Union[Any, Signal[Any]]] = None,
    style: str = "textfield",
    date_only: bool = False,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernDatePicker:
    """创建现代化日期选择器 - 向后兼容接口
    
    Examples:
        # 基本用法 (兼容旧API)
        date_picker = DatePicker(date=Signal(NSDate.date()))
        
        # 新功能 - 布局属性
        date_picker = DatePicker(date=date_signal, style="calendar", width=300, margin=8)
        
        # 链式调用
        date_picker = DatePicker(date=date_signal).width(250).margin(8)
    """
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    return ModernDatePicker(date, style, date_only, **kwargs)


def TimePicker(
    time: Optional[Union[Any, Signal[Any]]] = None,
    style: str = "stepper",
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernTimePicker:
    """创建现代化时间选择器 - 向后兼容接口"""
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    return ModernTimePicker(time, style, **kwargs)


# 便捷构造函数
def DateOnlyPicker(
    date_signal: Signal[Any],
    style: str = "textfield",
    **kwargs
) -> ModernDatePicker:
    """仅日期选择器 - 不包含时间部分"""
    return ModernDatePicker(date_signal, style, date_only=True, **kwargs)


def CalendarDatePicker(
    date_signal: Signal[Any],
    width: Union[int, float] = 280,
    height: Union[int, float] = 200,
    **kwargs
) -> ModernDatePicker:
    """日历样式的日期选择器"""
    return ModernDatePicker(
        date_signal,
        style="calendar",
        width=width,
        height=height,
        **kwargs
    )


def CompactTimePicker(
    time_signal: Signal[Any],
    width: Union[int, float] = 80,
    **kwargs
) -> ModernTimePicker:
    """紧凑时间选择器 - 文本框样式"""
    return ModernTimePicker(
        time_signal,
        style="textfield",
        width=width,
        **kwargs
    )


def DateTimeCombo(
    date_signal: Signal[Any],
    spacing: Union[int, float] = 8,
    **kwargs
) -> 'ModernHStack':
    """日期时间组合选择器 - 分别选择日期和时间"""
    from .modern_layout import ModernHStack
    
    # 创建仅日期选择器
    date_picker = ModernDatePicker(
        date_signal,
        style="textfield", 
        date_only=True,
        width=120
    )
    
    # 创建时间选择器
    time_picker = ModernTimePicker(
        date_signal,  # 使用同一个信号，时间部分会同步
        style="stepper",
        width=100
    )
    
    # 用水平布局组合
    return ModernHStack(
        children=[date_picker, time_picker],
        spacing=spacing,
        **kwargs
    )