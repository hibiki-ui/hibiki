"""Basic Controls 简化单元测试

测试 macui.components.basic_controls 模块的基本功能
使用简单的mock方式，重点测试组件创建逻辑
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

# 使用测试组件 
from tests.fixtures.test_components import TestSignal, TestComputed

# 为了测试，创建Signal和Computed的Mock版本
class MockSignal(TestSignal):
    """继承TestSignal的Mock Signal"""
    pass

class MockComputed(TestComputed):
    """继承TestComputed的Mock Computed"""
    pass


class TestBasicControlsCreation:
    """测试基础控件创建功能"""
    
    def test_button_creation_basic(self):
        """测试按钮基本创建"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton:
            # Setup mock
            mock_button_instance = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button_instance
            
            from macui.components.basic_controls import Button
            
            # 创建按钮
            result = Button("Test Button")
            
            # 验证
            assert result == mock_button_instance
            MockNSButton.alloc.assert_called_once()
            mock_button_instance.setTitle_.assert_called_once_with("Test Button")
    
    def test_button_with_signal_title(self):
        """测试按钮响应式标题"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding, \
             patch('macui.components.basic_controls.Signal', MockSignal), \
             patch('macui.components.basic_controls.Computed', MockComputed):
            
            # Setup mocks
            mock_button_instance = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button_instance
            
            from macui.components.basic_controls import Button
            
            # 创建信号和按钮
            title_signal = MockSignal("Dynamic Title")
            result = Button(title=title_signal)
            
            # 验证
            assert result == mock_button_instance
            MockBinding.bind.assert_called_once_with(mock_button_instance, "title", title_signal)
    
    def test_button_with_click_handler(self):
        """测试按钮点击处理"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.EventBinding') as MockEventBinding:
            
            # Setup mocks
            mock_button_instance = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button_instance
            
            from macui.components.basic_controls import Button
            
            # 创建按钮和处理函数
            click_handler = Mock()
            result = Button("Click Me", on_click=click_handler)
            
            # 验证
            assert result == mock_button_instance
            MockEventBinding.bind_click.assert_called_once_with(mock_button_instance, click_handler)
    
    def test_label_creation_basic(self):
        """测试标签基本创建"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField:
            # Setup mock
            mock_label_instance = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_label_instance
            
            from macui.components.basic_controls import Label
            
            # 创建标签
            result = Label("Hello World")
            
            # 验证基本设置
            assert result == mock_label_instance
            mock_label_instance.setBezeled_.assert_called_once_with(False)
            mock_label_instance.setDrawsBackground_.assert_called_once_with(False)
            mock_label_instance.setEditable_.assert_called_once_with(False)
            mock_label_instance.setSelectable_.assert_called_once_with(False)
            mock_label_instance.setStringValue_.assert_called_once_with("Hello World")
    
    def test_label_with_signal_text(self):
        """测试标签响应式文本"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            # Setup mocks
            mock_label_instance = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_label_instance
            
            from macui.components.basic_controls import Label
            
            # 创建信号和标签
            text_signal = TestSignal("Dynamic Text")
            result = Label(text=text_signal)
            
            # 验证
            assert result == mock_label_instance
            MockBinding.bind.assert_called_once_with(mock_label_instance, "text", text_signal)
    
    def test_textfield_creation_basic(self):
        """测试文本框基本创建"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField:
            # Setup mock
            mock_textfield_instance = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_textfield_instance
            
            from macui.components.basic_controls import TextField
            
            # 创建文本框
            result = TextField()
            
            # 验证基本设置
            assert result == mock_textfield_instance
            mock_textfield_instance.setBezeled_.assert_called_once_with(True)
            mock_textfield_instance.setDrawsBackground_.assert_called_once_with(True)
    
    def test_textfield_with_value(self):
        """测试文本框初始值"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField:
            # Setup mock
            mock_textfield_instance = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_textfield_instance
            
            from macui.components.basic_controls import TextField
            
            # 创建文本框
            result = TextField(value="Initial Text")
            
            # 验证
            assert result == mock_textfield_instance
            mock_textfield_instance.setStringValue_.assert_called_with("Initial Text")
    
    def test_textfield_with_signal_value(self):
        """测试文本框响应式值"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField, \
             patch('macui.components.basic_controls.TwoWayBinding') as MockTwoWayBinding:
            
            # Setup mocks
            mock_textfield_instance = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_textfield_instance
            
            from macui.components.basic_controls import TextField
            
            # 创建信号和文本框
            value_signal = TestSignal("Signal Text")
            result = TextField(value=value_signal)
            
            # 验证
            assert result == mock_textfield_instance
            MockTwoWayBinding.bind.assert_called_once_with(mock_textfield_instance, "stringValue", value_signal)


class TestBasicControlsIntegration:
    """测试基础控件集成场景"""
    
    def test_reactive_button_label_combo(self):
        """测试响应式按钮标签组合"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.NSTextField') as MockNSTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding, \
             patch('macui.components.basic_controls.EventBinding') as MockEventBinding:
            
            # Setup mocks
            mock_button = Mock()
            mock_label = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button
            MockNSTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Button, Label
            
            # 创建共享状态
            count = TestSignal(0)
            
            def increment():
                count.value += 1
            
            # 创建组件
            button = Button("Increment", on_click=increment)
            label = Label(text=count)
            
            # 验证组件创建
            assert button == mock_button
            assert label == mock_label
            
            # 验证绑定
            MockEventBinding.bind_click.assert_called_once_with(mock_button, increment)
            MockBinding.bind.assert_called_once_with(mock_label, "text", count)
            
            # 测试逻辑
            assert count.value == 0
            increment()
            assert count.value == 1
    
    def test_computed_values_with_controls(self):
        """测试控件与计算值集成"""
        with patch('macui.components.basic_controls.NSTextField') as MockNSTextField, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            # Setup mock
            mock_label = Mock()
            MockNSTextField.alloc.return_value.init.return_value = mock_label
            
            from macui.components.basic_controls import Label
            
            # 创建信号和计算值
            count = TestSignal(5)
            double_count = TestComputed(lambda: count.value * 2)
            message = TestComputed(lambda: f"Count: {count.value}, Double: {double_count.value}")
            
            # 创建标签
            Label(text=message)
            
            # 验证计算值工作正常
            assert count.value == 5
            assert double_count.value == 10
            assert message.value == "Count: 5, Double: 10"
            
            # 测试计算值更新
            count.value = 10
            double_count.invalidate()
            message.invalidate()
            
            assert double_count.value == 20
            assert message.value == "Count: 10, Double: 20"
    
    def test_error_handling_with_none_values(self):
        """测试空值错误处理"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton:
            # Setup mock
            mock_button = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            # 测试空值不会导致错误
            result = Button(
                title="Test",
                on_click=None,
                enabled=None,
                tooltip=None,
                frame=None
            )
            
            # 验证按钮创建成功
            assert result == mock_button
            # 只有title应该被调用
            mock_button.setTitle_.assert_called_once_with("Test")
            # 其他可选参数不应该引起错误


class TestBasicControlsSignalTypes:
    """测试基础控件的信号类型处理"""
    
    def test_signal_type_detection(self):
        """测试信号类型检测"""
        from macui.components.basic_controls import Button
        
        # 测试不同类型的值
        string_title = "Static Title"
        signal_title = TestSignal("Signal Title")
        computed_title = TestComputed(lambda: "Computed Title")
        
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_button = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button
            
            # 测试字符串标题
            Button(title=string_title)
            mock_button.setTitle_.assert_called_with("Static Title")
            
            # 重置mock
            mock_button.reset_mock()
            MockBinding.reset_mock() if hasattr(MockBinding, 'reset_mock') else None
            
            # 测试Signal标题
            Button(title=signal_title)
            MockBinding.bind.assert_called_with(mock_button, "title", signal_title)
            
            # 重置mock
            mock_button.reset_mock()
            MockBinding.reset_mock() if hasattr(MockBinding, 'reset_mock') else None
            
            # 测试Computed标题
            Button(title=computed_title)
            MockBinding.bind.assert_called_with(mock_button, "title", computed_title)
    
    def test_mixed_signal_and_static_properties(self):
        """测试混合信号和静态属性"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.ReactiveBinding') as MockBinding:
            
            mock_button = Mock()
            MockNSButton.alloc.return_value.init.return_value = mock_button
            
            from macui.components.basic_controls import Button
            
            # 混合使用静态和响应式属性
            title_signal = TestSignal("Dynamic Title")
            
            Button(
                title=title_signal,  # 响应式
                enabled=True,        # 静态
                tooltip="Static tooltip"  # 静态
            )
            
            # 验证混合使用
            MockBinding.bind.assert_called_once_with(mock_button, "title", title_signal)
            mock_button.setEnabled_.assert_called_once_with(True)
            mock_button.setToolTip_.assert_called_once_with("Static tooltip")


@pytest.mark.unit
@pytest.mark.components
class TestBasicControlsPerformance:
    """测试基础控件性能相关"""
    
    def test_multiple_components_creation(self):
        """测试多个组件创建性能"""
        with patch('macui.components.basic_controls.NSButton') as MockNSButton, \
             patch('macui.components.basic_controls.NSTextField') as MockNSTextField:
            
            # Setup mocks
            MockNSButton.alloc.return_value.init.return_value = Mock()
            MockNSTextField.alloc.return_value.init.return_value = Mock()
            
            from macui.components.basic_controls import Button, Label, TextField
            
            # 创建多个组件
            components = []
            for i in range(10):
                button = Button(f"Button {i}")
                label = Label(f"Label {i}")
                textfield = TextField(value=f"Field {i}")
                components.extend([button, label, textfield])
            
            # 验证所有组件都被创建
            assert len(components) == 30
            assert MockNSButton.alloc.call_count == 10
            assert MockNSTextField.alloc.call_count == 20  # Label + TextField


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])