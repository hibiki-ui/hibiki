"""
现代化输入控件 - 基于新布局引擎v3.0 (Stretchable)

提供支持CSS-like布局属性的现代化输入组件
包括Slider, Switch, Checkbox, RadioButton, SegmentedControl等
"""

from typing import Any, Callable, List, Optional, Union
from enum import Enum

from AppKit import (
    NSButton, NSButtonTypeSwitch, NSButtonTypeRadio,
    NSSegmentedControl, NSSlider,
    NSControlStateValueOn, NSControlStateValueOff
)
from Foundation import NSMakeRect

from ..core.binding import EventBinding, ReactiveBinding, TwoWayBinding
from ..core.signal import Signal, Computed
from ..layout.styles import LayoutStyle
from .core import LayoutAwareComponent


class Orientation(Enum):
    """方向枚举"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ModernSlider(LayoutAwareComponent):
    """现代化滑块组件 - 支持新布局系统"""
    
    def __init__(
        self,
        value: Optional[Signal[float]] = None,
        min_value: float = 0.0,
        max_value: float = 100.0,
        step_size: Optional[float] = None,
        orientation: Union[Orientation, str] = Orientation.HORIZONTAL,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[float], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化滑块
        
        Args:
            value: 滑块值 (响应式)
            min_value: 最小值
            max_value: 最大值
            step_size: 步长
            orientation: 方向 (horizontal/vertical)
            enabled: 启用状态 (响应式)
            on_change: 值变化回调
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        # 处理字符串方向
        if isinstance(orientation, str):
            orientation = Orientation.HORIZONTAL if orientation == "horizontal" else Orientation.VERTICAL
        
        # 根据方向设置默认尺寸
        if width is None:
            width = 200 if orientation == Orientation.HORIZONTAL else 20
        if height is None:
            height = 20 if orientation == Orientation.HORIZONTAL else 200
        
        layout_style = LayoutStyle(
            width=width,
            height=height,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.value = value or Signal(min_value)
        self.min_value = min_value
        self.max_value = max_value
        self.step_size = step_size
        self.orientation = orientation
        self.enabled = enabled
        self.on_change = on_change
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSSlider:
        """创建NSSlider实例"""
        slider = NSSlider.alloc().init()
        
        # 设置范围
        slider.setMinValue_(self.min_value)
        slider.setMaxValue_(self.max_value)
        
        # 设置初始值
        slider.setDoubleValue_(self.value.value)
        
        # 设置frame
        width = self.layout_style.width or 200
        height = self.layout_style.height or 20
        slider.setFrame_(NSMakeRect(0, 0, width, height))
        
        return slider
    
    def _setup_nsview(self):
        """设置NSSlider属性和绑定"""
        slider = self._nsview
        
        # 双向绑定值
        TwoWayBinding.bind_slider(slider, self.value, self.on_change)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(slider, "enabled", self.enabled)
            else:
                slider.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(slider, "tooltip", self.tooltip)
            else:
                slider.setToolTip_(str(self.tooltip))
        
        print(f"🎚️ ModernSlider 创建完成 (范围: {self.min_value}-{self.max_value})")


class ModernSwitch(LayoutAwareComponent):
    """现代化开关组件"""
    
    def __init__(
        self,
        value: Optional[Signal[bool]] = None,
        title: Optional[Union[str, Signal[str], Computed[str]]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[bool], None]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化开关"""
        layout_style = LayoutStyle(
            width=width or 60,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.value = value or Signal(False)
        self.title = title
        self.enabled = enabled
        self.on_change = on_change
    
    def _create_nsview(self) -> NSButton:
        """创建NSButton (Switch类型)"""
        switch = NSButton.alloc().init()
        switch.setButtonType_(NSButtonTypeSwitch)
        
        # 设置初始状态
        switch.setState_(NSControlStateValueOn if self.value.value else NSControlStateValueOff)
        
        # 设置frame
        width = self.layout_style.width or 60
        height = self.layout_style.height or 24
        switch.setFrame_(NSMakeRect(0, 0, width, height))
        
        return switch
    
    def _setup_nsview(self):
        """设置NSButton属性和绑定"""
        switch = self._nsview
        
        # 标题绑定
        if self.title:
            if isinstance(self.title, (Signal, Computed)):
                ReactiveBinding.bind(switch, "title", self.title)
            else:
                switch.setTitle_(str(self.title))
        
        # 双向绑定状态
        TwoWayBinding.bind_switch(switch, self.value, self.on_change)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(switch, "enabled", self.enabled)
            else:
                switch.setEnabled_(bool(self.enabled))
        
        print(f"🔘 ModernSwitch 创建完成")


class ModernCheckbox(LayoutAwareComponent):
    """现代化复选框组件"""
    
    def __init__(
        self,
        title: Union[str, Signal[str], Computed[str]],
        checked: Optional[Signal[bool]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[bool], None]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化复选框"""
        layout_style = LayoutStyle(
            width=width,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.title = title
        self.checked = checked or Signal(False)
        self.enabled = enabled
        self.on_change = on_change
    
    def _create_nsview(self) -> NSButton:
        """创建NSButton (Checkbox类型)"""
        checkbox = NSButton.alloc().init()
        checkbox.setButtonType_(NSButtonTypeSwitch)
        
        # 设置初始状态
        checkbox.setState_(NSControlStateValueOn if self.checked.value else NSControlStateValueOff)
        
        # 自动调整尺寸
        checkbox.sizeToFit()
        
        return checkbox
    
    def _setup_nsview(self):
        """设置NSButton属性和绑定"""
        checkbox = self._nsview
        
        # 标题绑定
        if isinstance(self.title, (Signal, Computed)):
            ReactiveBinding.bind(checkbox, "title", self.title)
        else:
            checkbox.setTitle_(str(self.title))
        
        # 双向绑定状态
        TwoWayBinding.bind_checkbox(checkbox, self.checked, self.on_change)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(checkbox, "enabled", self.enabled)
            else:
                checkbox.setEnabled_(bool(self.enabled))
        
        print(f"☑️ ModernCheckbox '{self.title}' 创建完成")


class ModernRadioButton(LayoutAwareComponent):
    """现代化单选按钮组件"""
    
    def __init__(
        self,
        title: Union[str, Signal[str], Computed[str]],
        selected: Optional[Signal[bool]] = None,
        group: Optional[str] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_select: Optional[Callable[[], None]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化单选按钮"""
        layout_style = LayoutStyle(
            width=width,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.title = title
        self.selected = selected or Signal(False)
        self.group = group
        self.enabled = enabled
        self.on_select = on_select
    
    def _create_nsview(self) -> NSButton:
        """创建NSButton (Radio类型)"""
        radio = NSButton.alloc().init()
        radio.setButtonType_(NSButtonTypeRadio)
        
        # 设置初始状态
        radio.setState_(NSControlStateValueOn if self.selected.value else NSControlStateValueOff)
        
        # 自动调整尺寸
        radio.sizeToFit()
        
        return radio
    
    def _setup_nsview(self):
        """设置NSButton属性和绑定"""
        radio = self._nsview
        
        # 标题绑定
        if isinstance(self.title, (Signal, Computed)):
            ReactiveBinding.bind(radio, "title", self.title)
        else:
            radio.setTitle_(str(self.title))
        
        # 选择状态绑定
        TwoWayBinding.bind_radio(radio, self.selected, self.on_select)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(radio, "enabled", self.enabled)
            else:
                radio.setEnabled_(bool(self.enabled))
        
        print(f"🔘 ModernRadioButton '{self.title}' 创建完成")


class ModernSegmentedControl(LayoutAwareComponent):
    """现代化分段控件组件"""
    
    def __init__(
        self,
        segments: List[str],
        selected_index: Optional[Signal[int]] = None,
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        on_change: Optional[Callable[[int], None]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化分段控件"""
        layout_style = LayoutStyle(
            width=width or len(segments) * 80,
            height=height or 24,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.segments = segments
        self.selected_index = selected_index or Signal(0)
        self.enabled = enabled
        self.on_change = on_change
    
    def _create_nsview(self) -> NSSegmentedControl:
        """创建NSSegmentedControl"""
        control = NSSegmentedControl.alloc().init()
        
        # 设置段数
        control.setSegmentCount_(len(self.segments))
        
        # 设置段标题
        for i, segment in enumerate(self.segments):
            control.setLabel_forSegment_(segment, i)
            control.setWidth_forSegment_(80, i)  # 默认宽度
        
        # 设置初始选择
        control.setSelectedSegment_(self.selected_index.value)
        
        # 设置frame
        width = self.layout_style.width or len(self.segments) * 80
        height = self.layout_style.height or 24
        control.setFrame_(NSMakeRect(0, 0, width, height))
        
        return control
    
    def _setup_nsview(self):
        """设置NSSegmentedControl属性和绑定"""
        control = self._nsview
        
        # 双向绑定选择的索引
        TwoWayBinding.bind_segmented_control(control, self.selected_index, self.on_change)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(control, "enabled", self.enabled)
            else:
                control.setEnabled_(bool(self.enabled))
        
        print(f"📊 ModernSegmentedControl 创建完成，段数: {len(self.segments)}")


# 向后兼容的函数式接口
def Slider(
    value: Optional[Signal[float]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    **kwargs
) -> ModernSlider:
    """创建现代化滑块 - 向后兼容接口"""
    return ModernSlider(value, min_value, max_value, **kwargs)


def Switch(
    value: Optional[Signal[bool]] = None,
    title: Optional[Union[str, Signal[str], Computed[str]]] = None,
    **kwargs
) -> ModernSwitch:
    """创建现代化开关 - 向后兼容接口"""
    return ModernSwitch(value, title, **kwargs)


def Checkbox(
    title: Union[str, Signal[str], Computed[str]],
    checked: Optional[Signal[bool]] = None,
    **kwargs
) -> ModernCheckbox:
    """创建现代化复选框 - 向后兼容接口"""
    return ModernCheckbox(title, checked, **kwargs)


def RadioButton(
    title: Union[str, Signal[str], Computed[str]],
    selected: Optional[Signal[bool]] = None,
    **kwargs
) -> ModernRadioButton:
    """创建现代化单选按钮 - 向后兼容接口"""
    return ModernRadioButton(title, selected, **kwargs)


def SegmentedControl(
    segments: List[str],
    selected_index: Optional[Signal[int]] = None,
    **kwargs
) -> ModernSegmentedControl:
    """创建现代化分段控件 - 向后兼容接口"""
    return ModernSegmentedControl(segments, selected_index, **kwargs)


# 便捷构造函数
def HorizontalSlider(
    value: Optional[Signal[float]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    width: int = 200,
    **kwargs
) -> ModernSlider:
    """水平滑块"""
    return ModernSlider(value, min_value, max_value, orientation=Orientation.HORIZONTAL, width=width, **kwargs)


def VerticalSlider(
    value: Optional[Signal[float]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    height: int = 200,
    **kwargs
) -> ModernSlider:
    """垂直滑块"""
    return ModernSlider(value, min_value, max_value, orientation=Orientation.VERTICAL, height=height, **kwargs)


def LabeledCheckbox(
    title: str,
    checked: Optional[Signal[bool]] = None,
    margin: Union[int, float] = 8,
    **kwargs
) -> ModernCheckbox:
    """带标签的复选框"""
    return ModernCheckbox(title, checked, margin=margin, **kwargs)


def RadioGroup(
    options: List[str],
    selected: Optional[Signal[int]] = None,
    spacing: Union[int, float] = 8,
    **kwargs
) -> List[ModernRadioButton]:
    """单选按钮组 - 返回按钮列表，需要手动添加到布局"""
    selected = selected or Signal(0)
    buttons = []
    
    for i, option in enumerate(options):
        is_selected = Signal(i == selected.value)
        
        def make_select_handler(index):
            def handler():
                selected.value = index
                # 更新所有按钮状态
                for j, btn in enumerate(buttons):
                    btn.selected.value = (j == index)
            return handler
        
        button = ModernRadioButton(
            option,
            selected=is_selected,
            on_select=make_select_handler(i),
            margin=spacing,
            **kwargs
        )
        buttons.append(button)
    
    return buttons