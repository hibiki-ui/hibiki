#!/usr/bin/env python3
"""
Hibiki UI v4.0 基础组件
Label, Button等基本UI组件的新架构实现
"""

from typing import Optional, Union, Callable, Any, List
from AppKit import (
    NSView, NSTextField, NSButton, NSButtonTypeMomentaryPushIn,
    NSSlider, NSButtonTypeSwitch, NSButtonTypeRadio,
    NSScrollView, NSTextView, NSProgressIndicator, NSProgressIndicatorStyleBar, NSProgressIndicatorStyleSpinning,
    NSImageView, NSImage, NSImageScaleProportionallyUpOrDown, NSImageScaleAxesIndependently, NSImageScaleNone,
    NSPopUpButton, NSComboBox, NSRect, NSMakeRect
)
from Foundation import NSObject

# 导入核心架构
from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect
from ..core.binding import bind_text, ReactiveBinding

# 导入objc
import objc

from ..core.logging import get_logger
logger = get_logger('components.basic')


# 全局按钮委托类
class ButtonDelegate(NSObject):
    """Button事件委托类"""
    
    def init(self):
        self = objc.super(ButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        return self
    
    def buttonClicked_(self, sender):
        """按钮点击事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                self.callback()
            except Exception as e:
                logger.error(f"⚠️ 按钮点击回调错误: {e}")

# ================================
# 1. Label - 文本标签组件
# ================================

class Label(UIComponent):
    """现代化Label组件
    
    基于Hibiki UI v4.0新架构的文本标签组件。
    支持完整的布局API和响应式绑定。
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 高层和低层API支持
    """
    
    def __init__(self, 
                 text: Union[str, Any],
                 style: Optional[ComponentStyle] = None,
                 text_props: Optional['TextProps'] = None,
                 # 便捷参数 - 自动转换为TextProps
                 text_style: Optional[str] = None,
                 font_size: Optional[float] = None,
                 font_weight: Optional[str] = None,
                 font_family: Optional[str] = None,
                 color: Optional[str] = None,
                 text_align: Optional[str] = None,
                 **style_kwargs):
        """🏗️ CORE METHOD: Label component initialization
        
        Args:
            text: 标签文本内容，支持字符串或响应式Signal
            style: 组件样式对象 (布局属性)
            text_props: 文本属性对象 (字体、颜色等)
            text_style: 语义化文本样式 (便捷参数)
            font_size: 字体大小 (便捷参数)
            font_weight: 字体粗细 (便捷参数)
            font_family: 字体族 (便捷参数)
            color: 文字颜色 (便捷参数)
            text_align: 文本对齐 (便捷参数)
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.text = text
        
        # 处理文本属性
        if text_props:
            self.text_props = text_props
        elif any([text_style, font_size, font_weight, font_family, color, text_align]):
            # 从便捷参数创建TextProps
            from ..core.text_props import TextProps
            self.text_props = TextProps(
                text_style=text_style,
                font_size=font_size,
                font_weight=font_weight,
                font_family=font_family,
                color=color,
                text_align=text_align
            )
        else:
            # 默认文本属性
            from ..core.text_props import TextProps
            self.text_props = TextProps()
        
        # 检查是否为响应式文本
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        logger.info(f"🏷️ Label创建: text='{text}', reactive={self._is_reactive_text}, text_props={bool(self.text_props)}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为Label"""
        label = NSTextField.alloc().init()
        
        # 基础配置
        label.setBezeled_(False)         # 无边框
        label.setDrawsBackground_(False) # 无背景
        label.setEditable_(False)        # 不可编辑
        label.setSelectable_(False)      # 不可选择
        
        # 设置文本内容 - 使用响应式绑定系统
        
        # 绑定文本，自动处理响应式和静态文本
        binding_cleanup = bind_text(label, self.text)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            logger.info(f"🔗 Label响应式绑定已创建: {self.text}")
        else:
            logger.info(f"📝 Label静态文本已设置: {str(self.text)}")
        
        # 多行文本支持配置
        label.setUsesSingleLineMode_(False)
        from AppKit import NSLineBreakByWordWrapping
        label.setLineBreakMode_(NSLineBreakByWordWrapping)
        
        # 设置首选最大宽度以支持自动换行
        if self.style.width:
            if hasattr(self.style.width, 'value'):
                width_value = self.style.width.value
                if isinstance(width_value, (int, float)):
                    label.setPreferredMaxLayoutWidth_(float(width_value))
        
        # 应用文本样式
        if self.text_props:
            # 设置字体
            font = self.text_props.to_nsfont()
            label.setFont_(font)
            logger.info(f"🔤 Label字体: {font.fontName()}, 大小: {font.pointSize()}")
            
            # 设置文字颜色
            color = self.text_props.to_nscolor()
            label.setTextColor_(color)
            
            # 设置文本对齐
            alignment = self.text_props.get_text_alignment()
            label.setAlignment_(alignment)
            
            logger.info(f"🎨 Label样式已应用: 字体={font.fontName()}, 对齐={alignment}")
        
        return label
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if self._nsview:
            return self._nsview.stringValue()
        if self._is_reactive_text:
            return str(getattr(self.text, 'value', self.text))
        return str(self.text)
    
    def set_text(self, text: Union[str, Any]) -> 'Label':
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.text = text
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_text:
                content = str(getattr(text, 'value', text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            logger.info(f"📝 Label文本更新: '{content}'")
        
        return self

# ================================
# 2. Button - 按钮组件
# ================================

class Button(UIComponent):
    """现代化Button组件
    
    基于Hibiki UI v4.0新架构的按钮组件。
    支持完整的事件处理和布局API。
    
    Features:
    - 完整的定位和布局支持
    - 点击事件处理
    - 多种按钮样式
    - 响应式标题绑定
    - 高层和低层API支持
    """
    
    def __init__(self,
                 title: str,
                 on_click: Optional[Callable[[], None]] = None,
                 style: Optional[ComponentStyle] = None,
                 **style_kwargs):
        """🏗️ CORE METHOD: Button component initialization
        
        Args:
            title: 按钮标题文本
            on_click: 点击事件回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.on_click = on_click
        self._target_delegate = None
        
        logger.info(f"🔘 Button创建: title='{title}', has_click={on_click is not None}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton"""
        button = NSButton.alloc().init()
        
        # 基础配置
        button.setTitle_(self.title)
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 自动调整尺寸
        button.sizeToFit()
        
        # 绑定点击事件
        if self.on_click:
            self._bind_click_event(button)
            
        return button
    
    def _bind_click_event(self, button: NSButton):
        """绑定点击事件"""
        try:
            # 使用全局ButtonDelegate类
            self._target_delegate = ButtonDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建ButtonDelegate")
                return
                
            self._target_delegate.callback = self.on_click
            
            button.setTarget_(self._target_delegate)
            button.setAction_("buttonClicked:")
            
            logger.info(f"🔗 Button点击事件已绑定")
            
        except Exception as e:
            logger.warning(f"⚠️ Button事件绑定失败: {e}")
    
    def set_title(self, title: str) -> 'Button':
        """动态设置按钮标题
        
        Args:
            title: 新的按钮标题
        """
        self.title = title
        
        if self._nsview:
            self._nsview.setTitle_(title)
            self._nsview.sizeToFit()  # 重新调整尺寸
            logger.info(f"📝 Button标题更新: '{title}'")
        
        return self
    
    def set_click_handler(self, callback: Callable[[], None]) -> 'Button':
        """设置或更新点击事件处理器
        
        Args:
            callback: 新的点击回调函数
        """
        self.on_click = callback
        
        if self._target_delegate:
            self._target_delegate.callback = callback
            logger.info(f"🔗 Button点击回调已更新")
        elif self._nsview:
            # 如果按钮已创建但没有事件绑定，重新绑定
            self._bind_click_event(self._nsview)
        
        return self

# ================================
# 3. TextField - 文本输入组件
# ================================

class TextField(UIComponent):
    """现代化TextField组件
    
    基于Hibiki UI v4.0新架构的文本输入组件。
    支持完整的布局API和响应式绑定。
    
    Features:
    - 完整的定位支持 (static, relative, absolute, fixed)
    - Z-Index层级管理
    - 变换效果 (scale, rotate, translate, opacity)
    - 响应式文本绑定
    - 占位符文本支持
    - 输入验证和格式化
    - 高层和低层API支持
    """
    
    def __init__(self, 
                 value: Union[str, Any] = "",
                 placeholder: str = "",
                 on_change: Optional[Callable[[str], None]] = None,
                 style: Optional[ComponentStyle] = None, 
                 **style_kwargs):
        """🏗️ CORE METHOD: TextField component initialization
        
        Args:
            value: 初始文本值，支持字符串或响应式Signal
            placeholder: 占位符文本
            on_change: 文本改变事件回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.placeholder = placeholder
        self.on_change = on_change
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        self._delegate = None
        
        logger.info(f"📝 TextField创建: value='{value}', placeholder='{placeholder}', reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为文本输入框"""
        from AppKit import NSTextField
        
        textfield = NSTextField.alloc().init()
        
        # 基础配置
        textfield.setBezeled_(True)         # 有边框
        textfield.setDrawsBackground_(True) # 有背景
        textfield.setEditable_(True)        # 可编辑
        textfield.setSelectable_(True)      # 可选择
        
        # 设置初始值 - 使用响应式绑定系统
        
        # 绑定文本值，自动处理响应式和静态值
        binding_cleanup = bind_text(textfield, self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            logger.info(f"🔗 TextField响应式绑定已创建: {self.value}")
        else:
            logger.info(f"📝 TextField静态值已设置: {str(self.value)}")
        
        # 设置占位符
        if self.placeholder:
            textfield.setPlaceholderString_(self.placeholder)
            logger.info(f"💬 TextField占位符: '{self.placeholder}'")
        
        # 绑定文本改变事件
        if self.on_change:
            self._bind_text_change_event(textfield)
        
        return textfield
    
    def _bind_text_change_event(self, textfield: NSTextField):
        """绑定文本改变事件"""
        try:
            # 使用全局TextFieldDelegate类
            self._delegate = TextFieldDelegate.alloc().init()
            if self._delegate is None:
                logger.warning("⚠️ 无法创建TextFieldDelegate")
                return
            
            self._delegate.callback = self.on_change
            self._delegate.textfield_component = self  # 保存组件引用
            
            textfield.setDelegate_(self._delegate)
            
            logger.info(f"🔗 TextField文本改变事件已绑定")
            
        except Exception as e:
            logger.warning(f"⚠️ TextField事件绑定失败: {e}")
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if self._nsview:
            return self._nsview.stringValue()
        return str(self.value)
    
    def set_text(self, text: str) -> 'TextField':
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.value = text
        from core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_value:
                content = str(getattr(text, 'value', text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            logger.info(f"📝 TextField文本更新: '{content}'")
        
        return self
    
    def set_placeholder(self, placeholder: str) -> 'TextField':
        """动态设置占位符文本
        
        Args:
            placeholder: 新的占位符文本
        """
        self.placeholder = placeholder
        
        if self._nsview:
            self._nsview.setPlaceholderString_(placeholder)
            logger.info(f"💬 TextField占位符更新: '{placeholder}'")
        
        return self


# 全局文本框委托类
class TextFieldDelegate(NSObject):
    """TextField事件委托类"""
    
    def init(self):
        self = objc.super(TextFieldDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.textfield_component = None
        return self
    
    def controlTextDidChange_(self, notification):
        """文本改变时的处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                # 获取当前文本内容
                textfield = notification.object()
                current_text = textfield.stringValue()
                
                # 更新组件的值
                if hasattr(self, 'textfield_component') and self.textfield_component:
                    if self.textfield_component._is_reactive_value and hasattr(self.textfield_component.value, 'value'):
                        self.textfield_component.value.value = current_text
                    else:
                        self.textfield_component.value = current_text
                
                # 调用回调函数
                self.callback(current_text)
                logger.info(f"📝 TextField文本改变: '{current_text}'")
                
            except Exception as e:
                logger.error(f"⚠️ TextField文本改变回调错误: {e}")

# ================================
# 4. Slider - 滑块组件
# ================================

class Slider(UIComponent):
    """现代化Slider滑块组件
    
    基于Hibiki UI v4.0新架构的滑块组件。
    支持数值选择、范围限制和响应式绑定。
    
    Features:
    - 数值范围控制 (min_value, max_value)
    - 响应式值绑定
    - 值变化回调事件
    - 完整的布局API支持
    - 高层和低层API支持
    """
    
    def __init__(self, 
                 value: Union[float, int, Any] = 0.0,
                 min_value: float = 0.0,
                 max_value: float = 100.0,
                 on_change: Optional[Callable[[float], None]] = None,
                 style: Optional[ComponentStyle] = None, 
                 **style_kwargs):
        """🏗️ CORE METHOD: Slider component initialization
        
        Args:
            value: 当前滑块值，支持数字或响应式Signal
            min_value: 最小值
            max_value: 最大值
            on_change: 值变化回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change
        
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        logger.info(f"🎚️ Slider创建: value={value}, range=[{min_value}, {max_value}], reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSSlider作为滑块"""
        from AppKit import NSSlider
        
        slider = NSSlider.alloc().init()
        
        # 设置滑块范围
        slider.setMinValue_(self.min_value)
        slider.setMaxValue_(self.max_value)
        
        # 设置初始值 - 使用响应式绑定系统
        
        # 绑定滑块值，自动处理响应式和静态值
        binding_cleanup = ReactiveBinding.bind(slider, "doubleValue", self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            if not hasattr(self, '_binding_cleanups'):
                self._binding_cleanups = []
            self._binding_cleanups.append(binding_cleanup)
        
        # 绑定滑块值变化事件
        if self.on_change:
            try:
                # 创建滑块委托
                self._delegate = SliderDelegate.alloc().init()
                self._delegate.callback = self.on_change
                self._delegate.slider_component = self  # 保存组件引用
                
                # 设置委托和动作
                slider.setTarget_(self._delegate)
                slider.setAction_("sliderChanged:")
                
                logger.info(f"🔗 Slider值变化事件已绑定")
                
            except Exception as e:
                logger.warning(f"⚠️ Slider事件绑定失败: {e}")
        
        logger.info(f"🎚️ NSSlider创建完成: range=[{self.min_value}, {self.max_value}]")
        return slider
    
    def get_value(self) -> float:
        """获取当前滑块值"""
        if self._nsview:
            return self._nsview.doubleValue()
        
        # 如果NSView还未创建，从响应式值或静态值获取
        if self._is_reactive_value and hasattr(self.value, 'value'):
            return float(self.value.value)
        return float(self.value)
    
    def set_value(self, value: Union[float, int]) -> 'Slider':
        """动态设置滑块值
        
        Args:
            value: 新的滑块值
        """
        # 确保值在范围内
        value = max(self.min_value, min(self.max_value, float(value)))
        self.value = value
        
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setDoubleValue_(value)
            logger.info(f"🎚️ Slider值更新: {value}")
        
        return self
    
    def set_range(self, min_value: float, max_value: float) -> 'Slider':
        """动态设置滑块范围
        
        Args:
            min_value: 新的最小值
            max_value: 新的最大值
        """
        self.min_value = min_value
        self.max_value = max_value
        
        if self._nsview:
            self._nsview.setMinValue_(min_value)
            self._nsview.setMaxValue_(max_value)
            # 确保当前值仍在新范围内
            current_value = self._nsview.doubleValue()
            if current_value < min_value or current_value > max_value:
                new_value = max(min_value, min(max_value, current_value))
                self._nsview.setDoubleValue_(new_value)
            logger.info(f"🎚️ Slider范围更新: [{min_value}, {max_value}]")
        
        return self


# 全局滑块委托类
class SliderDelegate(NSObject):
    """Slider值变化事件委托类"""
    
    def init(self):
        self = objc.super(SliderDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.slider_component = None
        return self
    
    def sliderChanged_(self, sender):
        """滑块值变化事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                # 获取当前滑块值
                current_value = sender.doubleValue()
                
                # 更新组件的值
                if hasattr(self, 'slider_component') and self.slider_component:
                    if self.slider_component._is_reactive_value and hasattr(self.slider_component.value, 'value'):
                        self.slider_component.value.value = current_value
                    else:
                        self.slider_component.value = current_value
                
                # 调用回调函数
                self.callback(current_value)
                logger.info(f"🎚️ Slider值变化: {current_value}")
                
            except Exception as e:
                logger.error(f"⚠️ Slider值变化回调错误: {e}")

# ================================
# 5. Switch - 开关组件  
# ================================

class Switch(UIComponent):
    """现代化Switch开关组件
    
    基于Hibiki UI v4.0新架构的开关组件。
    支持布尔值切换、响应式绑定和状态回调。
    
    Features:
    - 布尔值状态切换 (True/False)
    - 响应式状态绑定
    - 状态变化回调事件
    - 完整的布局API支持
    - 高层和低层API支持
    """
    
    def __init__(self, 
                 value: Union[bool, Any] = False,
                 on_change: Optional[Callable[[bool], None]] = None,
                 style: Optional[ComponentStyle] = None, 
                 **style_kwargs):
        """🏗️ CORE METHOD: Switch component initialization
        
        Args:
            value: 开关状态，支持布尔值或响应式Signal
            on_change: 状态变化回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.value = value
        self.on_change = on_change
        
        # 响应式类型检查
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        logger.info(f"🔘 Switch创建: value={value}, reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton配置为开关样式"""
        from AppKit import NSButton, NSButtonTypeSwitch
        
        switch = NSButton.alloc().init()
        
        # 设置为开关样式
        switch.setButtonType_(NSButtonTypeSwitch)
        switch.setTitle_("")  # 不显示标题
        
        # 设置初始状态 - 使用响应式绑定系统
        
        # 绑定开关状态，自动处理响应式和静态值
        # 使用state属性来绑定NSButton的开关状态
        binding_cleanup = ReactiveBinding.bind(switch, "state", self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            if not hasattr(self, '_binding_cleanups'):
                self._binding_cleanups = []
            self._binding_cleanups.append(binding_cleanup)
        
        # 绑定开关状态变化事件
        if self.on_change:
            try:
                # 创建开关委托
                self._delegate = SwitchDelegate.alloc().init()
                self._delegate.callback = self.on_change
                self._delegate.switch_component = self  # 保存组件引用
                
                # 设置委托和动作
                switch.setTarget_(self._delegate)
                switch.setAction_("switchChanged:")
                
                logger.info(f"🔗 Switch状态变化事件已绑定")
                
            except Exception as e:
                logger.warning(f"⚠️ Switch事件绑定失败: {e}")
        
        logger.info(f"🔘 NSButton(Switch)创建完成: state={self.get_value()}")
        return switch
    
    def get_value(self) -> bool:
        """获取当前开关状态"""
        if self._nsview:
            return bool(self._nsview.state())
        
        # 如果NSView还未创建，从响应式值或静态值获取
        if self._is_reactive_value and hasattr(self.value, 'value'):
            return bool(self.value.value)
        return bool(self.value)
    
    def set_value(self, value: bool) -> 'Switch':
        """动态设置开关状态
        
        Args:
            value: 新的开关状态
        """
        self.value = value
        
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setState_(1 if value else 0)
            logger.info(f"🔘 Switch状态更新: {value}")
        
        return self
    
    def toggle(self) -> 'Switch':
        """切换开关状态"""
        current_state = self.get_value()
        self.set_value(not current_state)
        return self


# 全局开关委托类
class SwitchDelegate(NSObject):
    """Switch事件委托类"""
    
    def init(self):
        self = objc.super(SwitchDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        return self
    
    def switchToggled_(self, sender):
        """开关切换事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                is_on = sender.state() == 1  # NSOnState = 1
                self.callback(is_on)
            except Exception as e:
                logger.error(f"⚠️ Switch切换回调错误: {e}")


# ================================
# 6. TextArea - 多行文本编辑器组件
# ================================

class TextArea(UIComponent):
    """多行文本编辑器组件
    
    基于Hibiki UI v4.0架构的多行文本输入组件。
    支持滚动、文本换行、响应式绑定等功能。
    
    Features:
    - 多行文本编辑
    - 自动滚动支持
    - 响应式内容绑定
    - 占位符文本
    - 可配置的编辑模式
    - 完整的布局支持
    """
    
    def __init__(self,
                 text: Union[str, Any] = "",
                 placeholder: str = "",
                 style: Optional[ComponentStyle] = None,
                 editable: bool = True,
                 on_text_change: Optional[Callable[[str], None]] = None,
                 **style_kwargs):
        """初始化TextArea组件
        
        Args:
            text: 初始文本内容，支持Signal绑定
            placeholder: 占位符文本
            style: 组件样式对象
            editable: 是否可编辑
            on_text_change: 文本变化回调函数
            **style_kwargs: 样式快捷参数
        """
        # 确保有合适的默认尺寸
        if style is None:
            from core.styles import px
            style = ComponentStyle(width=px(300), height=px(150))
        
        super().__init__(style, **style_kwargs)
        self.text = text
        self.placeholder = placeholder
        self.editable = editable
        self.on_text_change = on_text_change
        
        # 检查是否为响应式文本
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        self._bindings = []  # 存储绑定清理函数
        self._text_delegate = None
        
        logger.info(f"📝 TextArea创建: text_length={len(str(text))}, editable={editable}")
    
    def _create_nsview(self) -> NSView:
        """创建多行文本编辑器NSView"""
        # 导入必要的类
        from AppKit import NSScrollView, NSTextView, NSMakeRect
        
        # 创建滚动视图容器
        scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(0, 0, 300, 150))
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.setHasHorizontalScroller_(False)
        scroll_view.setAutohidesScrollers_(False)
        scroll_view.setBorderType_(1)  # NSBezelBorder
        
        # 创建文本视图
        text_view = NSTextView.alloc().init()
        text_view.setVerticallyResizable_(True)
        text_view.setHorizontallyResizable_(False)
        text_view.setAutoresizingMask_(2)  # NSViewWidthSizable
        
        # 设置文本内容
        initial_text = ""
        if self._is_reactive_text:
            initial_text = str(getattr(self.text, 'value', ''))
        else:
            initial_text = str(self.text)
        
        text_view.setString_(initial_text)
        
        # 设置编辑模式
        text_view.setEditable_(self.editable)
        text_view.setSelectable_(True)
        
        # 设置占位符（如果为空）
        if not initial_text and self.placeholder:
            # 注意：NSTextView没有直接的placeholder支持
            # 这里可以通过其他方式实现占位符效果
            pass
        
        # 将文本视图添加到滚动视图
        scroll_view.setDocumentView_(text_view)
        
        # 设置文本变化事件
        if self.on_text_change:
            self._bind_text_change_event(text_view)
        
        # 响应式绑定
        if self._is_reactive_text:
            from core.binding import ReactiveBinding
            binding_cleanup = ReactiveBinding.bind(text_view, "string", self.text)
            self._bindings.append(binding_cleanup)
            logger.info(f"🔗 TextArea响应式绑定已创建")
        
        # 保存文本视图引用以便后续操作
        self._text_view = text_view
        
        return scroll_view
    
    def _bind_text_change_event(self, text_view):
        """绑定文本变化事件"""
        # 创建委托对象
        delegate = TextAreaDelegate.alloc().init()
        delegate.callback = self.on_text_change
        delegate.text_area = self  # 保持对TextArea的引用
        
        text_view.setDelegate_(delegate)
        self._text_delegate = delegate  # 保持引用防止被垃圾回收
        logger.info("🔗 TextArea文本变化事件已绑定")
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if hasattr(self, '_text_view') and self._text_view:
            return self._text_view.string()
        if self._is_reactive_text:
            return str(getattr(self.text, 'value', ''))
        return str(self.text)
    
    def set_text(self, text: Union[str, Any]) -> 'TextArea':
        """动态设置文本内容"""
        self.text = text
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        if hasattr(self, '_text_view') and self._text_view:
            if self._is_reactive_text:
                content = str(getattr(text, 'value', ''))
            else:
                content = str(text)
            self._text_view.setString_(content)
            logger.info(f"📝 TextArea文本更新: length={len(content)}")
        
        return self
    
    def set_editable(self, editable: bool) -> 'TextArea':
        """设置是否可编辑"""
        self.editable = editable
        if hasattr(self, '_text_view') and self._text_view:
            self._text_view.setEditable_(editable)
        return self
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        if hasattr(self, '_text_view') and self._text_view:
            text_length = len(self._text_view.string())
            self._text_view.scrollRangeToVisible_((text_length, 0))


class TextAreaDelegate(NSObject):
    """TextArea委托类，处理文本变化事件"""
    
    def init(self):
        self = objc.super(TextAreaDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.text_area = None
        return self
    
    def textDidChange_(self, notification):
        """文本内容变化时调用"""
        if hasattr(self, 'callback') and self.callback:
            try:
                text_view = notification.object()
                new_text = text_view.string()
                self.callback(new_text)
            except Exception as e:
                logger.error(f"⚠️ TextArea文本变化回调错误: {e}")


# ================================
# 7. Checkbox - 复选框组件
# ================================

class Checkbox(UIComponent):
    """复选框组件
    
    基于Hibiki UI v4.0架构的复选框组件。
    支持选中状态管理和响应式绑定。
    
    Features:
    - 选中/未选中状态管理
    - 响应式状态绑定
    - 自定义标题文本
    - 状态变化回调
    - 完整的布局支持
    """
    
    def __init__(self,
                 title: str = "",
                 checked: Union[bool, Any] = False,
                 style: Optional[ComponentStyle] = None,
                 on_change: Optional[Callable[[bool], None]] = None,
                 **style_kwargs):
        """初始化Checkbox组件
        
        Args:
            title: 复选框标题文本
            checked: 初始选中状态，支持Signal绑定
            style: 组件样式对象
            on_change: 状态变化回调函数
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.checked = checked
        self.on_change = on_change
        
        # 检查是否为响应式状态
        self._is_reactive_checked = isinstance(checked, (Signal, Computed))
        self._bindings = []
        self._checkbox_delegate = None
        
        logger.info(f"☑️ Checkbox创建: title='{title}', checked={checked}")
    
    def _create_nsview(self) -> NSView:
        """创建复选框NSView"""
        from AppKit import NSButton, NSButtonTypeSwitch
        
        checkbox = NSButton.alloc().init()
        checkbox.setButtonType_(NSButtonTypeSwitch)
        checkbox.setTitle_(self.title)
        
        # 设置初始状态
        initial_checked = False
        if self._is_reactive_checked:
            initial_checked = bool(getattr(self.checked, 'value', False))
        else:
            initial_checked = bool(self.checked)
        
        checkbox.setState_(1 if initial_checked else 0)
        
        # 自动调整尺寸
        checkbox.sizeToFit()
        
        # 绑定状态变化事件
        if self.on_change:
            self._bind_change_event(checkbox)
        
        # 响应式绑定
        if self._is_reactive_checked:
            from core.binding import ReactiveBinding
            
            # 自定义绑定函数，因为checkbox需要特殊的状态处理
            def update_checkbox_state():
                new_checked = bool(getattr(self.checked, 'value', False))
                checkbox.setState_(1 if new_checked else 0)
            
            effect = Effect(update_checkbox_state)
            self._bindings.append(effect)
            logger.info(f"🔗 Checkbox响应式绑定已创建")
        
        return checkbox
    
    def _bind_change_event(self, checkbox):
        """绑定状态变化事件"""
        delegate = CheckboxDelegate.alloc().init()
        delegate.callback = self.on_change
        delegate.checkbox = self
        
        checkbox.setTarget_(delegate)
        checkbox.setAction_("checkboxToggled:")
        self._checkbox_delegate = delegate
        logger.info("🔗 Checkbox状态变化事件已绑定")
    
    def get_checked(self) -> bool:
        """获取当前选中状态"""
        if self._nsview:
            return self._nsview.state() == 1
        if self._is_reactive_checked:
            return bool(getattr(self.checked, 'value', False))
        return bool(self.checked)
    
    def set_checked(self, checked: Union[bool, Any]) -> 'Checkbox':
        """设置选中状态"""
        self.checked = checked
        self._is_reactive_checked = isinstance(checked, (Signal, Computed))
        
        if self._nsview:
            new_state = bool(getattr(checked, 'value', checked))
            self._nsview.setState_(1 if new_state else 0)
        
        return self


class CheckboxDelegate(NSObject):
    """Checkbox事件委托类"""
    
    def init(self):
        self = objc.super(CheckboxDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.checkbox = None
        return self
    
    def checkboxToggled_(self, sender):
        """复选框状态切换事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                is_checked = sender.state() == 1
                self.callback(is_checked)
            except Exception as e:
                logger.error(f"⚠️ Checkbox状态变化回调错误: {e}")


# ================================
# 8. RadioButton - 单选按钮组件
# ================================

class RadioButton(UIComponent):
    """单选按钮组件
    
    基于Hibiki UI v4.0架构的单选按钮组件。
    支持分组选择和响应式绑定。
    
    Features:
    - 分组单选功能
    - 响应式状态绑定
    - 自定义标题文本
    - 选择变化回调
    - 完整的布局支持
    """
    
    def __init__(self,
                 title: str = "",
                 value: Any = None,
                 selected: Union[bool, Any] = False,
                 group: Optional[str] = None,
                 style: Optional[ComponentStyle] = None,
                 on_select: Optional[Callable[[Any], None]] = None,
                 **style_kwargs):
        """初始化RadioButton组件
        
        Args:
            title: 单选按钮标题文本
            value: 按钮的值（选中时返回的值）
            selected: 初始选中状态，支持Signal绑定
            group: 单选组名称
            style: 组件样式对象
            on_select: 选中回调函数，参数为value
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.title = title
        self.value = value if value is not None else title
        self.selected = selected
        self.group = group
        self.on_select = on_select
        
        # 检查是否为响应式状态
        self._is_reactive_selected = isinstance(selected, (Signal, Computed))
        self._bindings = []
        self._radio_delegate = None
        
        logger.info(f"🔘 RadioButton创建: title='{title}', value={self.value}, selected={selected}")
    
    def _create_nsview(self) -> NSView:
        """创建单选按钮NSView"""
        from AppKit import NSButton, NSButtonTypeRadio
        
        radio = NSButton.alloc().init()
        radio.setButtonType_(NSButtonTypeRadio)
        radio.setTitle_(self.title)
        
        # 设置初始状态
        initial_selected = False
        if self._is_reactive_selected:
            initial_selected = bool(getattr(self.selected, 'value', False))
        else:
            initial_selected = bool(self.selected)
        
        radio.setState_(1 if initial_selected else 0)
        
        # 自动调整尺寸
        radio.sizeToFit()
        
        # 绑定选择事件
        if self.on_select:
            self._bind_select_event(radio)
        
        # 响应式绑定
        if self._is_reactive_selected:
            from core.binding import ReactiveBinding
            
            # 自定义绑定函数
            def update_radio_state():
                new_selected = bool(getattr(self.selected, 'value', False))
                radio.setState_(1 if new_selected else 0)
            
            effect = Effect(update_radio_state)
            self._bindings.append(effect)
            logger.info(f"🔗 RadioButton响应式绑定已创建")
        
        return radio
    
    def _bind_select_event(self, radio):
        """绑定选择事件"""
        delegate = RadioButtonDelegate.alloc().init()
        delegate.callback = self.on_select
        delegate.value = self.value
        delegate.radio_button = self
        
        radio.setTarget_(delegate)
        radio.setAction_("radioSelected:")
        self._radio_delegate = delegate
        logger.info("🔗 RadioButton选择事件已绑定")
    
    def get_selected(self) -> bool:
        """获取当前选中状态"""
        if self._nsview:
            return self._nsview.state() == 1
        if self._is_reactive_selected:
            return bool(getattr(self.selected, 'value', False))
        return bool(self.selected)
    
    def set_selected(self, selected: Union[bool, Any]) -> 'RadioButton':
        """设置选中状态"""
        self.selected = selected
        self._is_reactive_selected = isinstance(selected, (Signal, Computed))
        
        if self._nsview:
            new_state = bool(getattr(selected, 'value', selected))
            self._nsview.setState_(1 if new_state else 0)
        
        return self


class RadioButtonDelegate(NSObject):
    """RadioButton事件委托类"""
    
    def init(self):
        self = objc.super(RadioButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.value = None
        self.radio_button = None
        return self
    
    def radioSelected_(self, sender):
        """单选按钮选中事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                if sender.state() == 1:  # 只在选中时触发回调
                    self.callback(self.value)
            except Exception as e:
                logger.error(f"⚠️ RadioButton选择回调错误: {e}")

# ================================
# 6. 显示组件 (Display Components)
# ================================

class ProgressBar(UIComponent):
    """进度条组件 - 基于NSProgressIndicator"""
    
    def __init__(self, 
                 initial_value: Union[float, 'Signal'] = 0.0, 
                 maximum: Union[float, 'Signal'] = 100.0,
                 style: Optional[ComponentStyle] = None,
                 indeterminate: bool = False):
        """初始化进度条组件
        
        Args:
            initial_value: 进度值（0-maximum之间）
            maximum: 最大值
            style: 组件样式
            indeterminate: 是否为不确定进度条
        """
        super().__init__(style)
        # 处理响应式值
        if hasattr(initial_value, 'value'):
            self._is_reactive_value = True
            self.value = initial_value
        else:
            self._is_reactive_value = False
            self.value = initial_value
            
        if hasattr(maximum, 'value'):
            self._is_reactive_maximum = True
            self.maximum = maximum
        else:
            self._is_reactive_maximum = False
            self.maximum = maximum
            
        self.indeterminate = indeterminate
        self._progress_indicator = None
        
        # 初始化基础组件
        super().__init__(style=style)
        
        logger.info(f"🔧 ProgressBar组件创建: value={self._get_value()}, max={self._get_maximum()}")
        
    def _get_value(self) -> float:
        """获取当前进度值"""
        if self._is_reactive_value:
            return self.value.value if hasattr(self.value, 'value') else 0.0
        return self.value
        
    def _get_maximum(self) -> float:
        """获取最大值"""
        if self._is_reactive_maximum:
            return self.maximum.value if hasattr(self.maximum, 'value') else 100.0
        return self.maximum
    
    def _create_nsview(self) -> NSView:
        """创建NSProgressIndicator"""
        # 创建进度指示器
        progress = NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 20))
        
        if self.indeterminate:
            progress.setStyle_(NSProgressIndicatorStyleSpinning)
            progress.setIndeterminate_(True)
            progress.startAnimation_(None)
        else:
            progress.setStyle_(NSProgressIndicatorStyleBar)
            progress.setIndeterminate_(False)
            
            # 设置进度值
            progress.setMaxValue_(self._get_maximum())
            progress.setDoubleValue_(self._get_value())
        
        self._progress_indicator = progress
        
        # 建立响应式绑定
        if self._is_reactive_value:
            self._bind_reactive_value()
        if self._is_reactive_maximum:
            self._bind_reactive_maximum()
            
        logger.info(f"📊 ProgressBar NSProgressIndicator创建完成")
        return progress
    
    def _bind_reactive_value(self):
        """建立进度值的响应式绑定"""
        if not hasattr(self.value, 'value'):
            return
            
        def update_progress():
            if self._progress_indicator and not self.indeterminate:
                new_value = self.value.value
                self._progress_indicator.setDoubleValue_(float(new_value))
                logger.info(f"📊 ProgressBar值更新: {new_value}")
        
        # 使用Effect建立响应式绑定
        from core.reactive import Effect
        self._value_effect = Effect(update_progress)
        
    def _bind_reactive_maximum(self):
        """建立最大值的响应式绑定"""
        if not hasattr(self.maximum, 'value'):
            return
            
        def update_maximum():
            if self._progress_indicator and not self.indeterminate:
                new_maximum = self.maximum.value
                self._progress_indicator.setMaxValue_(float(new_maximum))
                logger.info(f"📊 ProgressBar最大值更新: {new_maximum}")
        
        # 使用Effect建立响应式绑定
        from core.reactive import Effect
        self._maximum_effect = Effect(update_maximum)
    
    def set_value(self, value: float) -> 'ProgressBar':
        """设置进度值
        
        Args:
            value: 新的进度值
        """
        if self._is_reactive_value:
            self.value.value = value
        else:
            self.value = value
            if self._progress_indicator and not self.indeterminate:
                self._progress_indicator.setDoubleValue_(float(value))
                
        logger.info(f"📊 ProgressBar进度更新: {value}")
        return self
    
    def set_maximum(self, maximum: float) -> 'ProgressBar':
        """设置最大值
        
        Args:
            maximum: 新的最大值
        """
        if self._is_reactive_maximum:
            self.maximum.value = maximum
        else:
            self.maximum = maximum
            if self._progress_indicator and not self.indeterminate:
                self._progress_indicator.setMaxValue_(float(maximum))
                
        logger.info(f"📊 ProgressBar最大值更新: {maximum}")
        return self
        
    def start_animation(self) -> 'ProgressBar':
        """开始动画（仅适用于不确定进度条）"""
        if self._progress_indicator and self.indeterminate:
            self._progress_indicator.startAnimation_(None)
            logger.info(f"🎬 ProgressBar动画开始")
        return self
        
    def stop_animation(self) -> 'ProgressBar':
        """停止动画（仅适用于不确定进度条）"""
        if self._progress_indicator and self.indeterminate:
            self._progress_indicator.stopAnimation_(None)
            logger.info(f"⏹️ ProgressBar动画停止")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, '_value_effect'):
            self._value_effect.cleanup()
        if hasattr(self, '_maximum_effect'):
            self._maximum_effect.cleanup()
        super().cleanup()


class ImageView(UIComponent):
    """图像显示组件 - 基于NSImageView"""
    
    def __init__(self, 
                 image_path: Optional[str] = None,
                 image_name: Optional[str] = None,
                 style: Optional[ComponentStyle] = None,
                 scaling: str = "proportionally"):
        """初始化图像视图组件
        
        Args:
            image_path: 图像文件路径
            image_name: 图像资源名称（从应用包中加载）
            style: 组件样式
            scaling: 图像缩放模式 ("proportionally", "axesIndependently", "none")
        """
        self.image_path = image_path
        self.image_name = image_name
        self.scaling = scaling
        self._image_view = None
        
        # 初始化基础组件
        super().__init__(style=style)
        
        logger.info(f"🖼️ ImageView组件创建: path={image_path}, name={image_name}")
    
    def _create_nsview(self) -> NSView:
        """创建NSImageView"""
        # 创建图像视图
        image_view = NSImageView.alloc().initWithFrame_(NSMakeRect(0, 0, 100, 100))
        
        # 设置缩放模式
        if self.scaling == "proportionally":
            image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
        elif self.scaling == "axesIndependently":
            image_view.setImageScaling_(NSImageScaleAxesIndependently)
        else:  # "none"
            image_view.setImageScaling_(NSImageScaleNone)
        
        # 加载图像
        if self.image_path:
            self._load_image_from_path(image_view, self.image_path)
        elif self.image_name:
            self._load_image_from_name(image_view, self.image_name)
            
        self._image_view = image_view
        
        logger.info(f"🖼️ ImageView NSImageView创建完成")
        return image_view
    
    def _load_image_from_path(self, image_view: NSImageView, path: str):
        """从文件路径加载图像"""
        try:
            image = NSImage.alloc().initWithContentsOfFile_(path)
            if image:
                image_view.setImage_(image)
                logger.info(f"📁 图像加载成功: {path}")
            else:
                logger.warning(f"⚠️ 图像加载失败: {path}")
        except Exception as e:
            logger.error(f"❌ 图像加载异常: {e}")
    
    def _load_image_from_name(self, image_view: NSImageView, name: str):
        """从应用包资源加载图像"""
        try:
            image = NSImage.imageNamed_(name)
            if image:
                image_view.setImage_(image)
                logger.info(f"📦 系统图像加载成功: {name}")
            else:
                logger.warning(f"⚠️ 系统图像加载失败: {name}")
        except Exception as e:
            logger.error(f"❌ 系统图像加载异常: {e}")
    
    def set_image_path(self, path: str) -> 'ImageView':
        """设置图像文件路径
        
        Args:
            path: 图像文件路径
        """
        self.image_path = path
        
        if self._image_view:
            self._load_image_from_path(self._image_view, path)
            
        logger.info(f"🖼️ ImageView图像路径更新: {path}")
        return self
    
    def set_image_name(self, name: str) -> 'ImageView':
        """设置系统图像名称
        
        Args:
            name: 系统图像名称
        """
        self.image_name = name
        
        if self._image_view:
            self._load_image_from_name(self._image_view, name)
            
        logger.info(f"🖼️ ImageView图像名称更新: {name}")
        return self
    
    def set_scaling(self, scaling: str) -> 'ImageView':
        """设置图像缩放模式
        
        Args:
            scaling: 缩放模式 ("proportionally", "axesIndependently", "none")
        """
        self.scaling = scaling
        
        if self._image_view:
            if scaling == "proportionally":
                self._image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
            elif scaling == "axesIndependently":
                self._image_view.setImageScaling_(NSImageScaleAxesIndependently)
            else:  # "none"
                self._image_view.setImageScaling_(NSImageScaleNone)
                
        logger.info(f"🖼️ ImageView缩放模式更新: {scaling}")
        return self


# ================================
# 7. 选择组件 (Selection Components)
# ================================

class PopUpButtonDelegate(NSObject):
    """PopUpButton选择事件委托类"""
    
    def init(self):
        self = objc.super(PopUpButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.popup_component = None
        return self
    
    def itemSelected_(self, sender):
        """下拉选择项被选中事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                # 获取选中的索引和标题
                selected_index = sender.indexOfSelectedItem()
                selected_title = sender.titleOfSelectedItem()
                
                # 更新组件的选中值
                if hasattr(self, 'popup_component') and self.popup_component:
                    if self.popup_component._is_reactive_selected:
                        if hasattr(self.popup_component.selected_index, 'value'):
                            self.popup_component.selected_index.value = selected_index
                    else:
                        self.popup_component.selected_index = selected_index
                
                # 调用回调函数
                self.callback(selected_index, selected_title)
                logger.info(f"🔽 PopUpButton选择: index={selected_index}, title='{selected_title}'")
                
            except Exception as e:
                logger.error(f"⚠️ PopUpButton选择回调错误: {e}")


class PopUpButton(UIComponent):
    """下拉按钮组件 - 基于NSPopUpButton"""
    
    def __init__(self, 
                 items: List[str] = None,
                 selected_index: Union[int, 'Signal'] = 0,
                 on_selection: Optional[Callable[[int, str], None]] = None,
                 style: Optional[ComponentStyle] = None):
        """
        初始化下拉按钮组件
        
        Args:
            items: 下拉选项列表
            selected_index: 默认选中的索引
            on_selection: 选择回调函数 (index, title) -> None
            style: 组件样式
        """
        self.items = items or ["选项1", "选项2", "选项3"]
        
        # 处理响应式选中索引
        if hasattr(selected_index, 'value'):
            self._is_reactive_selected = True
            self.selected_index = selected_index
        else:
            self._is_reactive_selected = False
            self.selected_index = selected_index
            
        self.on_selection = on_selection
        self._popup_button = None
        self._target_delegate = None
        
        # 初始化基础组件
        super().__init__(style=style)
        
        logger.info(f"🔽 PopUpButton组件创建: items={len(self.items)}, selected={self._get_selected_index()}")
    
    def _get_selected_index(self) -> int:
        """获取当前选中索引"""
        if self._is_reactive_selected:
            return self.selected_index.value if hasattr(self.selected_index, 'value') else 0
        return self.selected_index
    
    def _create_nsview(self) -> NSView:
        """创建NSPopUpButton"""
        # 创建下拉按钮
        popup_button = NSPopUpButton.alloc().initWithFrame_pullsDown_(NSMakeRect(0, 0, 150, 26), False)
        
        # 添加选项
        for item in self.items:
            popup_button.addItemWithTitle_(item)
        
        # 设置默认选中项
        selected = self._get_selected_index()
        if 0 <= selected < len(self.items):
            popup_button.selectItemAtIndex_(selected)
        
        self._popup_button = popup_button
        
        # 绑定选择事件
        if self.on_selection:
            self._bind_selection_event(popup_button)
        
        # 建立响应式绑定
        if self._is_reactive_selected:
            self._bind_reactive_selection()
            
        logger.info(f"🔽 PopUpButton NSPopUpButton创建完成")
        return popup_button
    
    def _bind_selection_event(self, popup_button: NSPopUpButton):
        """绑定选择事件"""
        try:
            # 创建委托
            self._target_delegate = PopUpButtonDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建PopUpButtonDelegate")
                return
                
            self._target_delegate.callback = self.on_selection
            self._target_delegate.popup_component = self
            
            popup_button.setTarget_(self._target_delegate)
            popup_button.setAction_("itemSelected:")
            
            logger.info(f"🔗 PopUpButton选择事件已绑定")
            
        except Exception as e:
            logger.warning(f"⚠️ PopUpButton事件绑定失败: {e}")
    
    def _bind_reactive_selection(self):
        """建立选中索引的响应式绑定"""
        if not hasattr(self.selected_index, 'value'):
            return
            
        def update_selection():
            if self._popup_button:
                new_index = self.selected_index.value
                if 0 <= new_index < len(self.items):
                    self._popup_button.selectItemAtIndex_(new_index)
                    logger.info(f"🔽 PopUpButton选中更新: index={new_index}")
        
        # 使用Effect建立响应式绑定
        from core.reactive import Effect
        self._selection_effect = Effect(update_selection)
    
    def add_item(self, item: str, at_index: int = -1) -> 'PopUpButton':
        """添加选项
        
        Args:
            item: 选项文本
            at_index: 插入位置，-1表示末尾
        """
        if at_index == -1:
            self.items.append(item)
        else:
            self.items.insert(at_index, item)
        
        if self._popup_button:
            if at_index == -1:
                self._popup_button.addItemWithTitle_(item)
            else:
                self._popup_button.insertItemWithTitle_atIndex_(item, at_index)
        
        logger.info(f"🔽 PopUpButton添加选项: '{item}' at {at_index if at_index != -1 else len(self.items)-1}")
        return self
    
    def remove_item(self, index: int) -> 'PopUpButton':
        """移除选项
        
        Args:
            index: 要移除的索引
        """
        if 0 <= index < len(self.items):
            removed_item = self.items.pop(index)
            
            if self._popup_button:
                self._popup_button.removeItemAtIndex_(index)
            
            logger.info(f"🔽 PopUpButton移除选项: '{removed_item}' at {index}")
        
        return self
    
    def set_selected_index(self, index: int) -> 'PopUpButton':
        """设置选中索引
        
        Args:
            index: 要选中的索引
        """
        if self._is_reactive_selected:
            self.selected_index.value = index
        else:
            self.selected_index = index
            if self._popup_button and 0 <= index < len(self.items):
                self._popup_button.selectItemAtIndex_(index)
                
        logger.info(f"🔽 PopUpButton选中设置: index={index}")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, '_selection_effect'):
            self._selection_effect.cleanup()
        super().cleanup()


class ComboBoxDelegate(NSObject):
    """ComboBox文本变化和选择事件委托类"""
    
    def init(self):
        self = objc.super(ComboBoxDelegate, self).init()
        if self is None:
            return None
        self.text_callback = None
        self.selection_callback = None
        self.combo_component = None
        return self
    
    def comboBoxSelectionDidChange_(self, notification):
        """下拉选择变化事件处理"""
        if hasattr(self, 'selection_callback') and self.selection_callback:
            try:
                combo_box = notification.object()
                selected_index = combo_box.indexOfSelectedItem()
                selected_value = combo_box.stringValue()
                
                # 更新组件的选中值
                if hasattr(self, 'combo_component') and self.combo_component:
                    if self.combo_component._is_reactive_text:
                        if hasattr(self.combo_component.text, 'value'):
                            self.combo_component.text.value = selected_value
                    else:
                        self.combo_component.text = selected_value
                
                self.selection_callback(selected_index, selected_value)
                logger.info(f"📝 ComboBox选择: index={selected_index}, value='{selected_value}'")
                
            except Exception as e:
                logger.error(f"⚠️ ComboBox选择回调错误: {e}")
    
    def controlTextDidChange_(self, notification):
        """文本输入变化事件处理"""
        if hasattr(self, 'text_callback') and self.text_callback:
            try:
                combo_box = notification.object()
                current_text = combo_box.stringValue()
                
                # 更新组件的文本值
                if hasattr(self, 'combo_component') and self.combo_component:
                    if self.combo_component._is_reactive_text:
                        if hasattr(self.combo_component.text, 'value'):
                            self.combo_component.text.value = current_text
                    else:
                        self.combo_component.text = current_text
                
                self.text_callback(current_text)
                logger.info(f"📝 ComboBox文本变化: '{current_text}'")
                
            except Exception as e:
                logger.error(f"⚠️ ComboBox文本变化回调错误: {e}")


class ComboBox(UIComponent):
    """组合框组件 - 基于NSComboBox"""
    
    def __init__(self, 
                 items: List[str] = None,
                 text: Union[str, 'Signal'] = "",
                 editable: bool = True,
                 on_text_change: Optional[Callable[[str], None]] = None,
                 on_selection: Optional[Callable[[int, str], None]] = None,
                 style: Optional[ComponentStyle] = None):
        """
        初始化组合框组件
        
        Args:
            items: 下拉选项列表
            text: 当前文本内容
            editable: 是否可编辑
            on_text_change: 文本变化回调函数
            on_selection: 选择回调函数
            style: 组件样式
        """
        super().__init__(style)
        self.items = items or ["选项A", "选项B", "选项C"]
        
        # 处理响应式文本
        if hasattr(text, 'value'):
            self._is_reactive_text = True
            self.text = text
        else:
            self._is_reactive_text = False
            self.text = text
            
        self.editable = editable
        self.on_text_change = on_text_change
        self.on_selection = on_selection
        self._combo_box = None
        self._target_delegate = None
        
        # 初始化基础组件
        super().__init__(style=style)
        
        logger.info(f"📝 ComboBox组件创建: items={len(self.items)}, text='{self._get_text()}'")
    
    def _get_text(self) -> str:
        """获取当前文本"""
        if self._is_reactive_text:
            return self.text.value if hasattr(self.text, 'value') else ""
        return self.text
    
    def _create_nsview(self) -> NSView:
        """创建NSComboBox"""
        # 创建组合框
        combo_box = NSComboBox.alloc().initWithFrame_(NSMakeRect(0, 0, 150, 26))
        
        # 添加选项
        for item in self.items:
            combo_box.addItemWithObjectValue_(item)
        
        # 设置初始文本
        combo_box.setStringValue_(self._get_text())
        
        # 设置是否可编辑
        combo_box.setEditable_(self.editable)
        
        self._combo_box = combo_box
        
        # 绑定事件
        if self.on_text_change or self.on_selection:
            self._bind_events(combo_box)
        
        # 建立响应式绑定
        if self._is_reactive_text:
            self._bind_reactive_text()
            
        logger.info(f"📝 ComboBox NSComboBox创建完成")
        return combo_box
    
    def _bind_events(self, combo_box: NSComboBox):
        """绑定事件"""
        try:
            # 创建委托
            self._target_delegate = ComboBoxDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建ComboBoxDelegate")
                return
                
            self._target_delegate.text_callback = self.on_text_change
            self._target_delegate.selection_callback = self.on_selection
            self._target_delegate.combo_component = self
            
            # 设置委托
            combo_box.setDelegate_(self._target_delegate)
            
            logger.info(f"🔗 ComboBox事件已绑定")
            
        except Exception as e:
            logger.warning(f"⚠️ ComboBox事件绑定失败: {e}")
    
    def _bind_reactive_text(self):
        """建立文本的响应式绑定"""
        if not hasattr(self.text, 'value'):
            return
            
        def update_text():
            if self._combo_box:
                new_text = self.text.value
                self._combo_box.setStringValue_(new_text)
                logger.info(f"📝 ComboBox文本更新: '{new_text}'")
        
        # 使用Effect建立响应式绑定
        from core.reactive import Effect
        self._text_effect = Effect(update_text)
    
    def add_item(self, item: str) -> 'ComboBox':
        """添加选项
        
        Args:
            item: 选项文本
        """
        self.items.append(item)
        
        if self._combo_box:
            self._combo_box.addItemWithObjectValue_(item)
        
        logger.info(f"📝 ComboBox添加选项: '{item}'")
        return self
    
    def remove_item(self, item: str) -> 'ComboBox':
        """移除选项
        
        Args:
            item: 要移除的选项文本
        """
        if item in self.items:
            self.items.remove(item)
            
            if self._combo_box:
                self._combo_box.removeItemWithObjectValue_(item)
            
            logger.info(f"📝 ComboBox移除选项: '{item}'")
        
        return self
    
    def set_text(self, text: str) -> 'ComboBox':
        """设置文本内容
        
        Args:
            text: 新的文本内容
        """
        if self._is_reactive_text:
            self.text.value = text
        else:
            self.text = text
            if self._combo_box:
                self._combo_box.setStringValue_(text)
                
        logger.info(f"📝 ComboBox文本设置: '{text}'")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, '_text_effect'):
            self._text_effect.cleanup()
        super().cleanup()


# ================================
# 8. 使用示例和测试
# ================================

if __name__ == "__main__":
    logger.info("Hibiki UI v4.0 基础组件测试\n")
    
    # 初始化管理器系统
    from core.managers import ManagerFactory
    ManagerFactory.initialize_all()
    
    logger.info("🧪 基础组件创建测试:")
    
    # 创建Label
    label = Label("Hello, Hibiki UI v4.0!")
    logger.info(f"Label创建完成: {label.__class__.__name__}")
    
    # 创建Button
    def on_button_click():
        logger.info("🎉 按钮被点击了！")
    
    button = Button("Click Me", on_click=on_button_click)
    logger.info(f"Button创建完成: {button.__class__.__name__}")
    
    logger.info("\n🎨 高层API测试:")
    
    # 测试高层API
    modal_label = Label("模态框内容").layout.modal(300, 200)
    logger.info(f"模态Label: position={modal_label.style.position}")
    
    floating_button = Button("悬浮按钮").layout.floating_button("bottom-right")
    logger.info(f"悬浮Button: position={floating_button.style.position}")
    
    # 测试链式调用
    styled_label = Label("样式化标签")
    styled_label.layout.center()
    styled_label.layout.fade(0.8)
    styled_label.layout.scale(1.2)
    logger.info(f"样式化Label: opacity={styled_label.style.opacity}, scale={styled_label.style.scale}")
    
    logger.info("\n🔧 低层API测试:")
    
    # 测试低层API
    from core.managers import Position
    advanced_button = Button("高级按钮")
    advanced_button.advanced.set_position(Position.ABSOLUTE, left=100, top=200)
    advanced_button.advanced.set_transform(rotation=15)
    logger.info(f"高级Button: position={advanced_button.style.position}, rotation={advanced_button.style.rotation}°")
    
    logger.info("\n🚀 挂载测试:")
    
    # 测试挂载
    label_view = label.mount()
    button_view = button.mount()
    
    logger.info(f"Label NSView: {type(label_view).__name__}")
    logger.info(f"Button NSView: {type(button_view).__name__}")
    
    # 测试动态更新
    logger.info("\n📝 动态更新测试:")
    label.set_text("更新后的文本")
    button.set_title("更新后的按钮")
    
    logger.info("\n✅ 基础组件测试完成！")