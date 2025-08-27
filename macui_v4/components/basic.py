#!/usr/bin/env python3
"""
macUI v4.0 基础组件
Label, Button等基本UI组件的新架构实现
"""

from typing import Optional, Union, Callable, Any
from AppKit import NSView, NSTextField, NSButton, NSButtonTypeMomentaryPushIn

# 导入核心架构
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.component import UIComponent
from core.styles import ComponentStyle

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
        self._is_reactive_text = hasattr(text, 'value')  # 检查是否为Signal
        
        print(f"🏷️ Label创建: text='{text}', reactive={self._is_reactive_text}")
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为Label"""
        label = NSTextField.alloc().init()
        
        # 基础配置
        label.setBezeled_(False)         # 无边框
        label.setDrawsBackground_(False) # 无背景
        label.setEditable_(False)        # 不可编辑
        label.setSelectable_(False)      # 不可选择
        
        # 设置文本内容
        if self._is_reactive_text:
            # TODO: 集成响应式绑定系统
            # ReactiveBinding.bind(label, "stringValue", self.text)
            label.setStringValue_(str(getattr(self.text, 'value', self.text)))
            print(f"🔗 Label响应式绑定: {self.text}")
        else:
            label.setStringValue_(str(self.text))
            print(f"📝 Label静态文本: {str(self.text)}")
        
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
    
    def set_text(self, text: Union[str, Any]) -> 'Label':
        """动态设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.text = text
        self._is_reactive_text = hasattr(text, 'value')
        
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
            # 创建委托对象处理点击事件
            from Foundation import NSObject
            
            class ButtonDelegate(NSObject):
                def init(self):
                    self = NSObject.init(self)
                    self.callback = None
                    return self
                    
                def buttonClicked_(self, sender):
                    """PyObjC action method - must accept sender parameter"""
                    if hasattr(self, 'callback') and self.callback:
                        try:
                            self.callback()
                        except Exception as e:
                            print(f"⚠️ 按钮点击回调错误: {e}")
            
            self._target_delegate = ButtonDelegate.alloc().init()
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
# 3. 使用示例和测试
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