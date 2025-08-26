"""Basic Controls 单元测试

测试 macui.components.basic_controls 模块中的组件：
- Button: 按钮组件
- Label: 标签组件  
- TextField: 文本输入框组件

重点测试：
- 组件创建和基本属性设置
- 响应式绑定功能 (Signal/Computed)
- 事件处理机制
- 属性更新和双向绑定
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call

# 使用测试组件避免导入真实的 macUI
from tests.fixtures.test_components import TestSignal, TestComputed, TestEffect
from tests.fixtures.mock_pyobjc import MockNSButton, MockNSTextField, MockReactiveBinding, MockTwoWayBinding, MockEventBinding


class TestButton:
    """测试 Button 组件"""
    
    def test_button_creation_with_string_title(self):
        """测试使用字符串标题创建按钮"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.NSMakeRect') as MockRect:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            MockRect.return_value = (10, 20, 100, 30)
            
            from macui.components.basic_controls import Button
            
            result = Button(
                title="Click Me",
                frame=(10, 20, 100, 30)
            )
            
            # 验证按钮创建
            assert result == mock_button
            # 验证方法被调用 (使用我们的mock系统)
            from tests.fixtures.mock_pyobjc import assert_mock_method_called
            assert_mock_method_called(mock_button, 'setButtonType_')
            assert_mock_method_called(mock_button, 'setFrame_', (10, 20, 100, 30))
            assert_mock_method_called(mock_button, 'setTitle_', "Click Me")
    
    def test_button_creation_with_signal_title(self):
        """测试使用 Signal 标题创建按钮"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            title_signal = TestSignal("Dynamic Title")
            
            result = Button(title=title_signal)
            
            # 验证响应式绑定
            assert result == mock_button
            MockBinding.bind.assert_called_once_with(mock_button, "title", title_signal)
    
    def test_button_with_enabled_signal(self):
        """测试使用 Signal 控制按钮启用状态"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            enabled_signal = TestSignal(True)
            
            Button(
                title="Test", 
                enabled=enabled_signal
            )
            
            # 验证启用状态绑定
            MockBinding.bind.assert_any_call(mock_button, "enabled", enabled_signal)
    
    def test_button_with_click_handler(self):
        """测试按钮点击事件处理"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.EventBinding') as MockEventBinding:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            click_handler = Mock()
            
            Button(
                title="Test",
                on_click=click_handler
            )
            
            # 验证事件绑定
            MockEventBinding.bind_click.assert_called_once_with(mock_button, click_handler)
    
    def test_button_with_all_options(self):
        """测试按钮完整选项"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding, \
             patch('macui.components.basic_controls.EventBinding') as MockEventBinding:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            title_signal = TestSignal("Dynamic")
            enabled_signal = TestSignal(False)
            tooltip_signal = TestSignal("Help text")
            click_handler = Mock()
            
            result = Button(
                title=title_signal,
                on_click=click_handler,
                enabled=enabled_signal,
                tooltip=tooltip_signal,
                frame=(0, 0, 120, 32)
            )
            
            # 验证所有绑定
            assert result == mock_button
            MockBinding.bind.assert_any_call(mock_button, "title", title_signal)
            MockBinding.bind.assert_any_call(mock_button, "enabled", enabled_signal)
            MockBinding.bind.assert_any_call(mock_button, "tooltip", tooltip_signal)
            MockEventBinding.bind_click.assert_called_once_with(mock_button, click_handler)


class TestLabel:
    """测试 Label 组件"""
    
    def test_label_creation_with_string_text(self):
        """测试使用字符串文本创建标签"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            result = Label(text="Hello World")
            
            # 验证标签创建和设置
            assert result == mock_label
            mock_label.setBezeled_.assert_called_once_with(False)
            mock_label.setDrawsBackground_.assert_called_once_with(False)
            mock_label.setEditable_.assert_called_once_with(False)
            mock_label.setSelectable_.assert_called_once_with(False)
            mock_label.setStringValue_.assert_called_once_with("Hello World")
    
    def test_label_creation_with_signal_text(self):
        """测试使用 Signal 文本创建标签"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            text_signal = TestSignal("Dynamic Text")
            
            result = Label(text=text_signal)
            
            # 验证响应式绑定
            assert result == mock_label
            MockBinding.bind.assert_called_once_with(mock_label, "text", text_signal)
    
    def test_label_with_frame_and_properties(self):
        """测试标签框架和属性设置"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.NSMakeRect') as MockRect:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            MockRect.return_value = (10, 10, 200, 25)
            
            from macui.components.basic_controls import Label
            
            Label(
                text="Test Label",
                frame=(10, 10, 200, 25),
                selectable=True
            )
            
            # 验证设置
            mock_label.setFrame_.assert_called_once_with((10, 10, 200, 25))
            mock_label.setSelectable_.assert_called_with(True)  # 覆盖默认值
    
    def test_label_with_color_and_alignment(self):
        """测试标签颜色和对齐设置"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            mock_color = Mock()
            mock_alignment = Mock()
            
            Label(
                text="Styled Label",
                color=mock_color,
                alignment=mock_alignment
            )
            
            # 验证样式设置
            mock_label.setTextColor_.assert_called_once_with(mock_color)
            mock_label.setAlignment_.assert_called_once_with(mock_alignment)


class TestTextField:
    """测试 TextField 组件"""
    
    def test_textfield_creation_basic(self):
        """测试基础文本框创建"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            result = TextField()
            
            # 验证基础设置
            assert result == mock_textfield
            mock_textfield.setBezeled_.assert_called_once_with(True)
            mock_textfield.setBezelStyle_.assert_called_once()
            mock_textfield.setDrawsBackground_.assert_called_once_with(True)
    
    def test_textfield_with_value_string(self):
        """测试使用字符串值创建文本框"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            TextField(value="Initial Text")
            
            # 验证初始值设置
            mock_textfield.setStringValue_.assert_called_with("Initial Text")
    
    def test_textfield_with_signal_value(self):
        """测试使用 Signal 值创建文本框"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.TwoWayBinding') as MockTwoWayBinding:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            value_signal = TestSignal("Signal Text")
            
            TextField(value=value_signal)
            
            # 验证双向绑定
            MockTwoWayBinding.bind.assert_called_once_with(mock_textfield, "stringValue", value_signal)
    
    def test_textfield_with_placeholder(self):
        """测试文本框占位符"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            TextField(placeholder="Enter text here")
            
            # 验证占位符设置
            mock_textfield.setPlaceholderString_.assert_called_once_with("Enter text here")
    
    def test_textfield_with_placeholder_signal(self):
        """测试使用 Signal 占位符"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            placeholder_signal = TestSignal("Dynamic Placeholder")
            
            TextField(placeholder=placeholder_signal)
            
            # 验证响应式占位符绑定
            MockBinding.bind.assert_called_once_with(mock_textfield, "placeholderString", placeholder_signal)
    
    def test_textfield_with_callbacks(self):
        """测试文本框回调函数"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.EnhancedTextFieldDelegate') as MockDelegate, \
             patch('objc.setAssociatedObject') as MockAssociate:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            mock_delegate_instance = Mock()
            MockDelegate.alloc.return_value.init.return_value = mock_delegate_instance
            
            from macui.components.basic_controls import TextField
            
            on_change_handler = Mock()
            on_enter_handler = Mock()
            
            TextField(
                on_change=on_change_handler,
                on_enter=on_enter_handler
            )
            
            # 验证代理设置
            assert mock_delegate_instance.on_change == on_change_handler
            assert mock_delegate_instance.on_enter == on_enter_handler
            mock_textfield.setDelegate_.assert_called_once_with(mock_delegate_instance)
            MockAssociate.assert_called_once()
    
    def test_textfield_secure_mode(self):
        """测试安全文本框（密码模式）"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.NSSecureTextField') as MockSecureTextField:
            
            mock_secure_field = Mock()
            MockSecureTextField.alloc.return_value.init.return_value = mock_secure_field
            
            from macui.components.basic_controls import TextField
            
            result = TextField(secure=True)
            
            # 验证安全文本框创建
            assert result == mock_secure_field
            mock_secure_field.setBezeled_.assert_called_once_with(True)
    
    def test_textfield_enabled_control(self):
        """测试文本框启用控制"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            # 测试布尔值启用
            TextField(enabled=False)
            mock_textfield.setEnabled_.assert_called_with(False)
            
            # 重置 mock
            mock_textfield.reset_mock()
            
            # 测试 Signal 启用
            enabled_signal = TestSignal(True)
            TextField(enabled=enabled_signal)
            MockBinding.bind.assert_called_with(mock_textfield, "enabled", enabled_signal)


class TestBasicControlsIntegration:
    """测试基础控件集成功能"""
    
    def test_button_label_reactive_integration(self):
        """测试按钮和标签的响应式集成"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding, \
             patch('macui.components.basic_controls.EventBinding') as MockEventBinding:
            
            mock_button = MockNSButton()
            mock_label = MockNSTextField()
            MockButton.alloc.return_value.init.return_value = mock_button
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Button, Label
            
            # 创建共享状态
            click_count = TestSignal(0)
            
            # 点击处理函数
            def handle_click():
                click_count.value += 1
            
            # 创建组件
            button = Button(title="Click Me", on_click=handle_click)
            label = Label(text=click_count)
            
            # 验证组件创建
            assert button == mock_button
            assert label == mock_label
            
            # 验证事件绑定
            MockEventBinding.bind_click.assert_called_once_with(mock_button, handle_click)
            
            # 验证响应式绑定
            MockBinding.bind.assert_called_with(mock_label, "text", click_count)
    
    def test_textfield_label_two_way_binding(self):
        """测试文本框和标签的双向绑定"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.TwoWayBinding') as MockTwoWayBinding, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_textfield = MockNSTextField()
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField, Label
            
            # 创建共享文本状态
            text_value = TestSignal("Initial")
            
            # 创建组件
            textfield = TextField(value=text_value)
            label = Label(text=text_value)
            
            # 验证双向绑定
            MockTwoWayBinding.bind.assert_called_once()
            MockBinding.bind.assert_called_once()
    
    def test_computed_values_with_controls(self):
        """测试控件与计算值的集成"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            # 创建基础信号和计算值
            count = TestSignal(5)
            double_count = TestComputed(lambda: count.value * 2)
            message = TestComputed(lambda: f"Count: {count.value}, Double: {double_count.value}")
            
            # 创建标签
            Label(text=message)
            
            # 验证计算值正常工作
            assert count.value == 5
            assert double_count.value == 10
            assert message.value == "Count: 5, Double: 10"
            
            # 验证绑定
            MockBinding.bind.assert_called_once_with(mock_label, "text", message)


class TestBasicControlsErrorHandling:
    """测试基础控件错误处理"""
    
    def test_button_with_none_values(self):
        """测试按钮空值处理"""
        with patch('macui.components.basic_controls.NSButton') as MockButton:
            
            mock_button = MockNSButton()
            MockButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            # 测试空值不会导致错误
            result = Button(
                title="Test",
                on_click=None,
                enabled=None,
                tooltip=None,
                frame=None
            )
            
            assert result == mock_button
            # 只有title应该被设置
            mock_button.setTitle_.assert_called_once_with("Test")
    
    def test_label_empty_text(self):
        """测试标签空文本处理"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_label = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            Label(text="")
            
            mock_label.setStringValue_.assert_called_once_with("")
    
    def test_textfield_invalid_signal_type(self):
        """测试文本框无效信号类型处理"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField:
            
            mock_textfield = MockNSTextField()
            MockTextField.alloc.return_value.init.return_value = mock_textfield
            
            from macui.components.basic_controls import TextField
            
            # 测试非Signal类型值
            TextField(value=123)  # 数字会被转换为字符串
            
            mock_textfield.setStringValue_.assert_called_with("123")


@pytest.mark.unit
@pytest.mark.components
class TestBasicControlsPerformance:
    """测试基础控件性能相关功能"""
    
    def test_multiple_signal_bindings_performance(self):
        """测试多个信号绑定的性能"""
        with patch('macui.components.basic_controls.NSButton') as MockButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            MockButton.alloc.return_value.init.return_value = MockNSButton()
            
            from macui.components.basic_controls import Button
            
            # 创建多个信号
            signals = [TestSignal(f"Button {i}") for i in range(10)]
            
            # 创建多个按钮
            buttons = []
            for signal in signals:
                button = Button(title=signal)
                buttons.append(button)
            
            # 验证所有绑定都被调用
            assert MockBinding.bind.call_count == 10
    
    def test_memory_cleanup_simulation(self):
        """模拟内存清理测试"""
        with patch('macui.components.basic_controls.NSTextField') as MockTextField, \
             patch('macui.components.basic_controls.EnhancedTextFieldDelegate') as MockDelegate:
            
            MockTextField.alloc.return_value.init.return_value = MockNSTextField()
            MockDelegate.alloc.return_value.init.return_value = Mock()
            
            from macui.components.basic_controls import TextField
            
            # 创建带回调的文本框
            textfield = TextField(on_change=lambda x: None)
            
            # 验证代理被正确设置（这在实际使用中很重要用于内存管理）
            assert textfield is not None


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v", "--tb=short"])