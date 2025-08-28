#!/usr/bin/env python3
"""
macUI v4.0 基础组件
Label, Button等基本UI组件的新架构实现
"""

from typing import Optional, Union, Callable, Any
from AppKit import NSView, NSTextField, NSButton, NSButtonTypeMomentaryPushIn
from Foundation import NSObject

# 导入核心架构
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.component import UIComponent
from core.styles import ComponentStyle

# 导入objc
import objc

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
                print(f"⚠️ 按钮点击回调错误: {e}")

# ================================
# 1. Label - 文本标签组件
# ================================

class Label(UIComponent):
    """现代化Label组件
    
    基于macUI v4.0新架构的文本标签组件。
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
                 **style_kwargs):
        """🏗️ CORE METHOD: Label component initialization
        
        Args:
            text: 标签文本内容，支持字符串或响应式Signal
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.text = text
        # 导入响应式类型检查
        try:
            from ..core.reactive import Signal, Computed
        except ImportError:
            # 兜底导入
            from core.reactive import Signal, Computed
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        print(f"🏷️ Label创建: text='{text}', reactive={self._is_reactive_text}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为Label"""
        label = NSTextField.alloc().init()
        
        # 基础配置
        label.setBezeled_(False)         # 无边框
        label.setDrawsBackground_(False) # 无背景
        label.setEditable_(False)        # 不可编辑
        label.setSelectable_(False)      # 不可选择
        
        # 设置文本内容 - 使用响应式绑定系统
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from core.binding import bind_text
        
        # 绑定文本，自动处理响应式和静态文本
        binding_cleanup = bind_text(label, self.text)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            print(f"🔗 Label响应式绑定已创建: {self.text}")
        else:
            print(f"📝 Label静态文本已设置: {str(self.text)}")
        
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
        from ..core.reactive import Signal, Computed
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_text:
                content = str(getattr(text, 'value', text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            print(f"📝 Label文本更新: '{content}'")
        
        return self

# ================================
# 2. Button - 按钮组件
# ================================

class Button(UIComponent):
    """现代化Button组件
    
    基于macUI v4.0新架构的按钮组件。
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
        
        print(f"🔘 Button创建: title='{title}', has_click={on_click is not None}")
    
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
                print("⚠️ 无法创建ButtonDelegate")
                return
                
            self._target_delegate.callback = self.on_click
            
            button.setTarget_(self._target_delegate)
            button.setAction_("buttonClicked:")
            
            print(f"🔗 Button点击事件已绑定")
            
        except Exception as e:
            print(f"⚠️ Button事件绑定失败: {e}")
    
    def set_title(self, title: str) -> 'Button':
        """动态设置按钮标题
        
        Args:
            title: 新的按钮标题
        """
        self.title = title
        
        if self._nsview:
            self._nsview.setTitle_(title)
            self._nsview.sizeToFit()  # 重新调整尺寸
            print(f"📝 Button标题更新: '{title}'")
        
        return self
    
    def set_click_handler(self, callback: Callable[[], None]) -> 'Button':
        """设置或更新点击事件处理器
        
        Args:
            callback: 新的点击回调函数
        """
        self.on_click = callback
        
        if self._target_delegate:
            self._target_delegate.callback = callback
            print(f"🔗 Button点击回调已更新")
        elif self._nsview:
            # 如果按钮已创建但没有事件绑定，重新绑定
            self._bind_click_event(self._nsview)
        
        return self

# ================================
# 3. TextField - 文本输入组件
# ================================

class TextField(UIComponent):
    """现代化TextField组件
    
    基于macUI v4.0新架构的文本输入组件。
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
        # 导入响应式类型检查 - 使用与文件头部一致的导入方式
        from core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        self._delegate = None
        
        print(f"📝 TextField创建: value='{value}', placeholder='{placeholder}', reactive={self._is_reactive_value}")
    
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
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from core.binding import bind_text
        
        # 绑定文本值，自动处理响应式和静态值
        binding_cleanup = bind_text(textfield, self.value)
        if binding_cleanup:
            # 如果有响应式绑定，记录清理函数以便后续清理
            self._bindings.append(binding_cleanup)
            print(f"🔗 TextField响应式绑定已创建: {self.value}")
        else:
            print(f"📝 TextField静态值已设置: {str(self.value)}")
        
        # 设置占位符
        if self.placeholder:
            textfield.setPlaceholderString_(self.placeholder)
            print(f"💬 TextField占位符: '{self.placeholder}'")
        
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
                print("⚠️ 无法创建TextFieldDelegate")
                return
            
            self._delegate.callback = self.on_change
            self._delegate.textfield_component = self  # 保存组件引用
            
            textfield.setDelegate_(self._delegate)
            
            print(f"🔗 TextField文本改变事件已绑定")
            
        except Exception as e:
            print(f"⚠️ TextField事件绑定失败: {e}")
    
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
        from ..core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(text, (Signal, Computed))
        
        if self._nsview:
            if self._is_reactive_value:
                content = str(getattr(text, 'value', text))
            else:
                content = str(text)
            self._nsview.setStringValue_(content)
            print(f"📝 TextField文本更新: '{content}'")
        
        return self
    
    def set_placeholder(self, placeholder: str) -> 'TextField':
        """动态设置占位符文本
        
        Args:
            placeholder: 新的占位符文本
        """
        self.placeholder = placeholder
        
        if self._nsview:
            self._nsview.setPlaceholderString_(placeholder)
            print(f"💬 TextField占位符更新: '{placeholder}'")
        
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
                print(f"📝 TextField文本改变: '{current_text}'")
                
            except Exception as e:
                print(f"⚠️ TextField文本改变回调错误: {e}")

# ================================
# 4. Slider - 滑块组件
# ================================

class Slider(UIComponent):
    """现代化Slider滑块组件
    
    基于macUI v4.0新架构的滑块组件。
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
        
        # 导入响应式类型检查
        try:
            from ..core.reactive import Signal, Computed
        except ImportError:
            from core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        print(f"🎚️ Slider创建: value={value}, range=[{min_value}, {max_value}], reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSSlider作为滑块"""
        from AppKit import NSSlider
        
        slider = NSSlider.alloc().init()
        
        # 设置滑块范围
        slider.setMinValue_(self.min_value)
        slider.setMaxValue_(self.max_value)
        
        # 设置初始值 - 使用响应式绑定系统
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from core.binding import ReactiveBinding
        
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
                
                print(f"🔗 Slider值变化事件已绑定")
                
            except Exception as e:
                print(f"⚠️ Slider事件绑定失败: {e}")
        
        print(f"🎚️ NSSlider创建完成: range=[{self.min_value}, {self.max_value}]")
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
        
        from ..core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setDoubleValue_(value)
            print(f"🎚️ Slider值更新: {value}")
        
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
            print(f"🎚️ Slider范围更新: [{min_value}, {max_value}]")
        
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
                print(f"🎚️ Slider值变化: {current_value}")
                
            except Exception as e:
                print(f"⚠️ Slider值变化回调错误: {e}")

# ================================
# 5. Switch - 开关组件  
# ================================

class Switch(UIComponent):
    """现代化Switch开关组件
    
    基于macUI v4.0新架构的开关组件。
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
        
        # 导入响应式类型检查
        try:
            from ..core.reactive import Signal, Computed
        except ImportError:
            from core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        print(f"🔘 Switch创建: value={value}, reactive={self._is_reactive_value}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton配置为开关样式"""
        from AppKit import NSButton, NSButtonTypeSwitch
        
        switch = NSButton.alloc().init()
        
        # 设置为开关样式
        switch.setButtonType_(NSButtonTypeSwitch)
        switch.setTitle_("")  # 不显示标题
        
        # 设置初始状态 - 使用响应式绑定系统
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from core.binding import ReactiveBinding
        
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
                
                print(f"🔗 Switch状态变化事件已绑定")
                
            except Exception as e:
                print(f"⚠️ Switch事件绑定失败: {e}")
        
        print(f"🔘 NSButton(Switch)创建完成: state={self.get_value()}")
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
        
        from ..core.reactive import Signal, Computed
        self._is_reactive_value = isinstance(value, (Signal, Computed))
        
        if self._nsview:
            self._nsview.setState_(1 if value else 0)
            print(f"🔘 Switch状态更新: {value}")
        
        return self
    
    def toggle(self) -> 'Switch':
        """切换开关状态"""
        current_state = self.get_value()
        self.set_value(not current_state)
        return self


# 全局开关委托类
class SwitchDelegate(NSObject):
    """Switch状态变化事件委托类"""
    
    def init(self):
        self = objc.super(SwitchDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.switch_component = None
        return self
    
    def switchChanged_(self, sender):
        """开关状态变化事件处理"""
        if hasattr(self, 'callback') and self.callback:
            try:
                # 获取当前开关状态
                current_state = bool(sender.state())
                
                # 更新组件的值
                if hasattr(self, 'switch_component') and self.switch_component:
                    if self.switch_component._is_reactive_value and hasattr(self.switch_component.value, 'value'):
                        self.switch_component.value.value = current_state
                    else:
                        self.switch_component.value = current_state
                
                # 调用回调函数
                self.callback(current_state)
                print(f"🔘 Switch状态变化: {current_state}")
                
            except Exception as e:
                print(f"⚠️ Switch状态变化回调错误: {e}")

# ================================
# 6. 使用示例和测试
# ================================

if __name__ == "__main__":
    print("macUI v4.0 基础组件测试\n")
    
    # 初始化管理器系统
    from core.managers import ManagerFactory
    ManagerFactory.initialize_all()
    
    print("🧪 基础组件创建测试:")
    
    # 创建Label
    label = Label("Hello, macUI v4.0!")
    print(f"Label创建完成: {label.__class__.__name__}")
    
    # 创建Button
    def on_button_click():
        print("🎉 按钮被点击了！")
    
    button = Button("Click Me", on_click=on_button_click)
    print(f"Button创建完成: {button.__class__.__name__}")
    
    print("\n🎨 高层API测试:")
    
    # 测试高层API
    modal_label = Label("模态框内容").layout.modal(300, 200)
    print(f"模态Label: position={modal_label.style.position}")
    
    floating_button = Button("悬浮按钮").layout.floating_button("bottom-right")
    print(f"悬浮Button: position={floating_button.style.position}")
    
    # 测试链式调用
    styled_label = Label("样式化标签")
    styled_label.layout.center()
    styled_label.layout.fade(0.8)
    styled_label.layout.scale(1.2)
    print(f"样式化Label: opacity={styled_label.style.opacity}, scale={styled_label.style.scale}")
    
    print("\n🔧 低层API测试:")
    
    # 测试低层API
    from core.managers import Position
    advanced_button = Button("高级按钮")
    advanced_button.advanced.set_position(Position.ABSOLUTE, left=100, top=200)
    advanced_button.advanced.set_transform(rotation=15)
    print(f"高级Button: position={advanced_button.style.position}, rotation={advanced_button.style.rotation}°")
    
    print("\n🚀 挂载测试:")
    
    # 测试挂载
    label_view = label.mount()
    button_view = button.mount()
    
    print(f"Label NSView: {type(label_view).__name__}")
    print(f"Button NSView: {type(button_view).__name__}")
    
    # 测试动态更新
    print("\n📝 动态更新测试:")
    label.set_text("更新后的文本")
    button.set_title("更新后的按钮")
    
    print("\n✅ 基础组件测试完成！")