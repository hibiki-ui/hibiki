"""
现代化显示组件 - 基于新布局引擎v3.0 (Stretchable)

提供支持CSS-like布局属性的现代化显示组件
包括ImageView, ProgressBar, TextArea等
"""

from typing import Any, Callable, Optional, Union
from AppKit import (
    NSImageView, NSProgressIndicator, NSScrollView, NSTextView, NSFont,
    NSImage
)
from Foundation import NSMakeRect

from ..core.binding import ReactiveBinding, TwoWayBinding, EnhancedTextViewDelegate
from ..core.signal import Signal, Computed
from ..layout.styles import LayoutStyle
from .core import LayoutAwareComponent


class ModernImageView(LayoutAwareComponent):
    """现代化图像视图组件 - 支持新布局系统"""
    
    def __init__(
        self,
        image: Optional[Union[Any, Signal[Any], Computed[Any]]] = None,
        scaling: str = "proportionally_down",  # "proportionally_down", "to_fit", "none"
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化图像视图
        
        Args:
            image: NSImage对象或图像路径 (响应式)
            scaling: 图像缩放模式
            enabled: 启用状态 (响应式)
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        layout_style = LayoutStyle(
            width=width,
            height=height,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.image = image
        self.scaling = scaling
        self.enabled = enabled
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSImageView:
        """创建NSImageView实例"""
        image_view = NSImageView.alloc().init()
        
        # 设置默认frame
        width = self.layout_style.width or 100
        height = self.layout_style.height or 100
        image_view.setFrame_(NSMakeRect(0, 0, width, height))
        
        return image_view
    
    def _setup_nsview(self):
        """设置NSImageView属性和绑定"""
        image_view = self._nsview
        
        # 图像绑定
        if self.image is not None:
            if isinstance(self.image, (Signal, Computed)):
                ReactiveBinding.bind(image_view, "image", self.image)
            else:
                # 处理路径字符串
                if isinstance(self.image, str):
                    ns_image = NSImage.alloc().initWithContentsOfFile_(self.image)
                    image_view.setImage_(ns_image)
                else:
                    image_view.setImage_(self.image)
        
        # 缩放模式设置
        scaling_map = {
            "proportionally_down": 0,  # NSImageScaleProportionallyDown
            "to_fit": 1,               # NSImageScaleAxesIndependently  
            "none": 2                  # NSImageScaleNone
        }
        image_view.setImageScaling_(scaling_map.get(self.scaling, 0))
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(image_view, "enabled", self.enabled)
            else:
                image_view.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(image_view, "tooltip", self.tooltip)
            else:
                image_view.setToolTip_(str(self.tooltip))
        
        print(f"🖼️ ModernImageView 创建完成")


class ModernProgressBar(LayoutAwareComponent):
    """现代化进度条组件 - 支持新布局系统"""
    
    def __init__(
        self,
        value: Optional[Signal[float]] = None,
        min_value: float = 0.0,
        max_value: float = 100.0,
        indeterminate: bool = False,
        style: str = "bar",  # "bar", "spinning"
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化进度条
        
        Args:
            value: 进度值信号 (0-100)
            min_value: 最小值
            max_value: 最大值
            indeterminate: 是否为不确定进度条
            style: 进度条样式
            enabled: 启用状态 (响应式)
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        layout_style = LayoutStyle(
            width=width or 200,
            height=height or (20 if style == "bar" else 20),
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.value = value or Signal(min_value)
        self.min_value = min_value
        self.max_value = max_value
        self.indeterminate = indeterminate
        self.style = style
        self.enabled = enabled
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSProgressIndicator:
        """创建NSProgressIndicator实例"""
        progress = NSProgressIndicator.alloc().init()
        
        # 设置范围
        progress.setMinValue_(self.min_value)
        progress.setMaxValue_(self.max_value)
        
        # 设置样式
        if self.style == "spinning" or self.indeterminate:
            progress.setStyle_(1)  # NSProgressIndicatorSpinningStyle
            progress.setIndeterminate_(True)
            if not self.indeterminate:  # 如果不是不确定但选择了spinning样式
                progress.setIndeterminate_(False)
        else:
            progress.setStyle_(0)  # NSProgressIndicatorBarStyle
            progress.setIndeterminate_(self.indeterminate)
        
        # 设置初始值
        progress.setDoubleValue_(self.value.value)
        
        # 设置frame
        width = self.layout_style.width or 200
        height = self.layout_style.height or 20
        progress.setFrame_(NSMakeRect(0, 0, width, height))
        
        return progress
    
    def _setup_nsview(self):
        """设置NSProgressIndicator属性和绑定"""
        progress = self._nsview
        
        # 值绑定
        ReactiveBinding.bind(progress, "doubleValue", self.value)
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(progress, "enabled", self.enabled)
            else:
                progress.setEnabled_(bool(self.enabled))
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(progress, "tooltip", self.tooltip)
            else:
                progress.setToolTip_(str(self.tooltip))
        
        # 如果是不确定进度条，开始动画
        if self.indeterminate:
            progress.startAnimation_(None)
        
        print(f"📊 ModernProgressBar 创建完成 (类型: {self.style})")


class ModernTextArea(LayoutAwareComponent):
    """现代化文本区域组件 - 支持新布局系统"""
    
    def __init__(
        self,
        value: Optional[Signal[str]] = None,
        placeholder: str = "",
        enabled: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        editable: Optional[Union[bool, Signal[bool], Computed[bool]]] = None,
        font_size: Optional[float] = None,
        on_change: Optional[Callable[[str], None]] = None,
        tooltip: Optional[Union[str, Signal[str], Computed[str]]] = None,
        # 布局样式支持
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        **layout_kwargs
    ):
        """初始化现代化文本区域
        
        Args:
            value: 文本值信号 (双向绑定)
            placeholder: 占位符文本
            enabled: 启用状态 (响应式)
            editable: 可编辑状态 (响应式)
            font_size: 字体大小
            on_change: 文本改变回调
            tooltip: 工具提示 (响应式)
            width, height: 尺寸
            **layout_kwargs: 其他布局样式
        """
        layout_style = LayoutStyle(
            width=width or 300,
            height=height or 150,
            **layout_kwargs
        )
        
        super().__init__(layout_style)
        
        self.value = value or Signal("")
        self.placeholder = placeholder
        self.enabled = enabled
        self.editable = editable
        self.font_size = font_size
        self.on_change = on_change
        self.tooltip = tooltip
    
    def _create_nsview(self) -> NSScrollView:
        """创建NSScrollView包装的NSTextView"""
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
        
        # 设置frame
        width = self.layout_style.width or 300
        height = self.layout_style.height or 150
        scroll_view.setFrame_(NSMakeRect(0, 0, width, height))
        text_view.setFrame_(NSMakeRect(0, 0, width, height))
        
        # 将 text_view 引用存储到 scroll_view 中
        import objc
        objc.setAssociatedObject(scroll_view, b"text_view", text_view, objc.OBJC_ASSOCIATION_RETAIN)
        
        return scroll_view
    
    def _setup_nsview(self):
        """设置NSTextView属性和绑定"""
        scroll_view = self._nsview
        
        # 获取存储的text_view
        import objc
        text_view = objc.getAssociatedObject(scroll_view, b"text_view")
        
        # 初始值设置
        text_view.setString_(self.value.value)
        
        # 可编辑状态
        if self.editable is not None:
            if isinstance(self.editable, (Signal, Computed)):
                ReactiveBinding.bind(text_view, "editable", self.editable)
            else:
                text_view.setEditable_(bool(self.editable))
        else:
            text_view.setEditable_(True)  # 默认可编辑
        
        # 启用状态绑定
        if self.enabled is not None:
            if isinstance(self.enabled, (Signal, Computed)):
                ReactiveBinding.bind(text_view, "enabled", self.enabled)
            else:
                enabled_val = bool(self.enabled)
                text_view.setSelectable_(enabled_val)
                text_view.setEditable_(enabled_val and (self.editable if self.editable is not None else True))
        
        # 字体大小
        if self.font_size:
            font = NSFont.systemFontOfSize_(self.font_size)
            text_view.setFont_(font)
        
        # 工具提示绑定
        if self.tooltip is not None:
            if isinstance(self.tooltip, (Signal, Computed)):
                ReactiveBinding.bind(scroll_view, "tooltip", self.tooltip)
            else:
                scroll_view.setToolTip_(str(self.tooltip))
        
        # 双向绑定
        TwoWayBinding.bind_text_view(text_view, self.value)
        
        # 文本改变事件处理
        if self.on_change:
            delegate = EnhancedTextViewDelegate.alloc().init()
            delegate.on_change = self.on_change
            delegate.signal = self.value
            
            text_view.setDelegate_(delegate)
            
            # 保持委托引用
            objc.setAssociatedObject(text_view, b"enhanced_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        print(f"📄 ModernTextArea 创建完成")


# 向后兼容的函数式接口
def ImageView(
    image: Optional[Union[Any, Signal[Any], Computed[Any]]] = None,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernImageView:
    """创建现代化图像视图 - 向后兼容接口
    
    Examples:
        # 基本用法 (兼容旧API)
        image_view = ImageView(image=my_image)
        
        # 新功能 - 布局属性
        image_view = ImageView(image=my_image, width=200, height=150, margin=8)
        
        # 链式调用
        image_view = ImageView(image=my_image).width(200).height(150).margin(8)
    """
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    return ModernImageView(image, **kwargs)


def ProgressBar(
    value: Optional[Union[float, Signal[float]]] = None,
    min_value: float = 0.0,
    max_value: float = 100.0,
    indeterminate: bool = False,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernProgressBar:
    """创建现代化进度条 - 向后兼容接口"""
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    # 处理非Signal值
    if value is not None and not isinstance(value, Signal):
        value = Signal(float(value))
    
    return ModernProgressBar(value, min_value, max_value, indeterminate, **kwargs)


def TextArea(
    value: Optional[Union[str, Signal[str]]] = None,
    frame: Optional[tuple] = None,
    **kwargs
) -> ModernTextArea:
    """创建现代化文本区域 - 向后兼容接口"""
    # 处理旧的frame参数
    if frame:
        kwargs.setdefault('width', frame[2])
        kwargs.setdefault('height', frame[3])
    
    # 处理非Signal值
    if value is not None and not isinstance(value, Signal):
        value = Signal(str(value))
    
    return ModernTextArea(value, **kwargs)


# 便捷构造函数
def ResponsiveImageView(
    image_signal: Signal[Any],
    width: Union[int, float] = 200,
    height: Union[int, float] = 150,
    **kwargs
) -> ModernImageView:
    """响应式图像视图 - 图像内容会随Signal变化"""
    return ModernImageView(image_signal, width=width, height=height, **kwargs)


def AnimatedProgressBar(
    progress_signal: Signal[float],
    width: Union[int, float] = 250,
    **kwargs
) -> ModernProgressBar:
    """动画进度条 - 进度会随Signal变化"""
    return ModernProgressBar(progress_signal, width=width, **kwargs)


def SpinningProgressIndicator(
    width: Union[int, float] = 32,
    height: Union[int, float] = 32,
    **kwargs
) -> ModernProgressBar:
    """旋转进度指示器"""
    return ModernProgressBar(
        value=None,
        indeterminate=True,
        style="spinning",
        width=width,
        height=height,
        **kwargs
    )


def RichTextArea(
    text_signal: Signal[str],
    font_size: float = 14,
    width: Union[int, float] = 400,
    height: Union[int, float] = 200,
    **kwargs
) -> ModernTextArea:
    """富文本区域 - 自定义字体和尺寸"""
    return ModernTextArea(
        text_signal,
        font_size=font_size,
        width=width,
        height=height,
        **kwargs
    )