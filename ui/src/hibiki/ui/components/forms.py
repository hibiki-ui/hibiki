#!/usr/bin/env python3
"""
Hibiki UI v4.0 表单系统
Form validation, data binding, and form container components
"""

from typing import Optional, Union, Callable, Any, Dict, List, Tuple
from enum import Enum
import re
from datetime import datetime
from AppKit import NSView
from Foundation import NSObject

# 导入核心架构
from ..core.component import UIComponent, Container
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed, Effect

from hibiki.core.logging import get_logger
logger = get_logger('components.forms')


# ================================
# 验证系统核心
# ================================

class ValidationResult:
    """验证结果类"""
    
    def __init__(self, is_valid: bool, message: str = "", severity: str = "error"):
        self.is_valid = is_valid
        self.message = message
        self.severity = severity  # "error", "warning", "info"
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def __str__(self) -> str:
        return self.message if self.message else ("Valid" if self.is_valid else "Invalid")

class Validator:
    """验证器基类"""
    
    def __init__(self, message: str = "Validation failed"):
        self.message = message
    
    def validate(self, value: Any) -> ValidationResult:
        """执行验证逻辑，子类需要重写此方法"""
        return ValidationResult(True)

# ================================
# 内置验证器
# ================================

class RequiredValidator(Validator):
    """必填验证器"""
    
    def __init__(self, message: str = "This field is required"):
        super().__init__(message)
    
    def validate(self, value: Any) -> ValidationResult:
        if value is None or str(value).strip() == "":
            return ValidationResult(False, self.message)
        return ValidationResult(True)

class LengthValidator(Validator):
    """长度验证器"""
    
    def __init__(self, min_length: int = 0, max_length: int = None, 
                 message: str = None):
        self.min_length = min_length
        self.max_length = max_length
        if message is None:
            if max_length:
                message = f"Length must be between {min_length} and {max_length} characters"
            else:
                message = f"Length must be at least {min_length} characters"
        super().__init__(message)
    
    def validate(self, value: Any) -> ValidationResult:
        length = len(str(value))
        if length < self.min_length:
            return ValidationResult(False, self.message)
        if self.max_length and length > self.max_length:
            return ValidationResult(False, self.message)
        return ValidationResult(True)

class RegexValidator(Validator):
    """正则表达式验证器"""
    
    def __init__(self, pattern: str, message: str = "Invalid format"):
        self.pattern = re.compile(pattern)
        super().__init__(message)
    
    def validate(self, value: Any) -> ValidationResult:
        if self.pattern.match(str(value)):
            return ValidationResult(True)
        return ValidationResult(False, self.message)

class EmailValidator(RegexValidator):
    """邮箱验证器"""
    
    def __init__(self, message: str = "Please enter a valid email address"):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        super().__init__(email_pattern, message)

class NumberValidator(Validator):
    """数字验证器"""
    
    def __init__(self, min_value: float = None, max_value: float = None,
                 message: str = None):
        self.min_value = min_value
        self.max_value = max_value
        if message is None:
            if min_value is not None and max_value is not None:
                message = f"Number must be between {min_value} and {max_value}"
            elif min_value is not None:
                message = f"Number must be at least {min_value}"
            elif max_value is not None:
                message = f"Number must be at most {max_value}"
            else:
                message = "Please enter a valid number"
        super().__init__(message)
    
    def validate(self, value: Any) -> ValidationResult:
        try:
            num_value = float(value)
            if self.min_value is not None and num_value < self.min_value:
                return ValidationResult(False, self.message)
            if self.max_value is not None and num_value > self.max_value:
                return ValidationResult(False, self.message)
            return ValidationResult(True)
        except (ValueError, TypeError):
            return ValidationResult(False, "Please enter a valid number")

class CustomValidator(Validator):
    """自定义验证器"""
    
    def __init__(self, validate_func: Callable[[Any], Union[bool, ValidationResult]],
                 message: str = "Validation failed"):
        super().__init__(message)
        self.validate_func = validate_func
    
    def validate(self, value: Any) -> ValidationResult:
        result = self.validate_func(value)
        if isinstance(result, ValidationResult):
            return result
        elif isinstance(result, bool):
            return ValidationResult(result, self.message if not result else "")
        else:
            return ValidationResult(False, "Invalid validation function result")

# ================================
# 表单字段类
# ================================

class FormField:
    """表单字段类"""
    
    def __init__(self, component: UIComponent, validators: List[Validator] = None,
                 name: str = None):
        self.component = component
        self.validators = validators or []
        self.name = name or f"field_{id(component)}"
        
        # 响应式验证状态
        self.is_valid = Signal(True)
        self.validation_message = Signal("")
        self.is_dirty = Signal(False)  # 是否已修改过
        self.is_touched = Signal(False)  # 是否已被触摸过
        
        # 延迟绑定验证事件，避免在初始化时造成循环
        self._validation_effect = None
        
        logger.info(f"📝 FormField创建: name='{self.name}', validators={len(self.validators)}")
    
    def _bind_validation(self):
        """绑定验证事件"""
        # 只有在组件已经mount后才绑定验证
        if self._validation_effect is None and hasattr(self.component, 'value'):
            try:
                # 创建Effect来监听值变化，但只在值真正变化时触发
                def validation_callback():
                    if self.is_dirty.value:  # 只在已经dirty时才验证
                        self._validate_on_change()
                
                self._validation_effect = Effect(validation_callback)
                logger.info(f"🔗 FormField验证绑定: {self.name}")
            except Exception as e:
                logger.warning(f"⚠️ FormField验证绑定失败: {e}")
    
    def _validate_on_change(self):
        """值变化时触发验证"""
        # 执行验证（不再自动设置dirty状态，避免循环）
        self.validate()
    
    def mark_dirty(self):
        """手动标记为dirty状态"""
        if not self.is_dirty.value:
            self.is_dirty.value = True
            # 首次设置dirty时绑定验证
            self._bind_validation()
    
    def validate(self) -> ValidationResult:
        """执行所有验证器"""
        if not hasattr(self.component, 'get_text') and not hasattr(self.component, 'get_value'):
            return ValidationResult(True)
        
        # 获取当前值
        if hasattr(self.component, 'get_text'):
            current_value = self.component.get_text()
        elif hasattr(self.component, 'get_value'):
            current_value = self.component.get_value()
        else:
            current_value = ""
        
        # 执行所有验证器
        for validator in self.validators:
            result = validator.validate(current_value)
            if not result.is_valid:
                self.is_valid.value = False
                self.validation_message.value = result.message
                logger.error(f"❌ Field '{self.name}' validation failed: {result.message}")
                return result
        
        # 所有验证器都通过
        self.is_valid.value = True
        self.validation_message.value = ""
        logger.info(f"✅ Field '{self.name}' validation passed")
        return ValidationResult(True)
    
    def touch(self):
        """标记字段为已触摸"""
        self.is_touched.value = True
    
    def reset(self):
        """重置字段状态"""
        self.is_valid.value = True
        self.validation_message.value = ""
        self.is_dirty.value = False
        self.is_touched.value = False

# ================================
# 表单容器组件
# ================================

class Form(Container):
    """表单容器组件
    
    提供表单数据绑定、验证、提交等功能
    
    Features:
    - 表单字段管理
    - 全局验证状态
    - 数据收集和提交
    - 响应式表单状态
    """
    
    def __init__(self, fields: List[FormField] = None,
                 on_submit: Callable[[Dict[str, Any]], None] = None,
                 style: Optional[ComponentStyle] = None, 
                 **style_kwargs):
        """初始化表单容器
        
        Args:
            fields: 表单字段列表
            on_submit: 表单提交回调函数
            style: 组件样式对象
            **style_kwargs: 样式快捷参数
        """
        super().__init__([], style, **style_kwargs)
        self.fields = {}  # 字段名 -> FormField映射
        self.on_submit = on_submit
        
        # 响应式表单状态
        self.is_valid = Signal(True)
        self.is_submitting = Signal(False)
        self.validation_errors = Signal([])
        
        # 添加字段
        if fields:
            for field in fields:
                self.add_field(field)
        
        # 创建验证状态计算属性
        self._create_validation_computed()
        
        logger.info(f"📋 Form创建: fields={len(self.fields)}")
    
    def add_field(self, field: FormField):
        """添加表单字段"""
        self.fields[field.name] = field
        
        # 添加组件到容器
        self.add_child_component(field.component)
        
        # 重新计算表单验证状态
        self._update_form_validation()
        
        logger.info(f"➕ Form字段添加: '{field.name}'")
    
    def remove_field(self, field_name: str):
        """移除表单字段"""
        if field_name in self.fields:
            field = self.fields[field_name]
            del self.fields[field_name]
            
            # 从容器中移除组件
            self.remove_child_component(field.component)
            
            # 重新计算表单验证状态
            self._update_form_validation()
            
            logger.info(f"➖ Form字段移除: '{field_name}'")
    
    def _create_validation_computed(self):
        """创建表单验证状态计算属性"""
        def compute_form_validation():
            all_valid = True
            errors = []
            
            for field_name, field in self.fields.items():
                if not field.is_valid.value:
                    all_valid = False
                    if field.validation_message.value:
                        errors.append(f"{field_name}: {field.validation_message.value}")
            
            self.is_valid.value = all_valid
            self.validation_errors.value = errors
            
            return all_valid
        
        self._validation_computed = Computed(compute_form_validation)
    
    def _update_form_validation(self):
        """更新表单验证状态"""
        if hasattr(self, '_validation_computed'):
            # 触发重新计算
            self._validation_computed.value
    
    def validate(self) -> bool:
        """验证所有字段"""
        all_valid = True
        errors = []
        
        for field_name, field in self.fields.items():
            result = field.validate()
            if not result.is_valid:
                all_valid = False
                errors.append(f"{field_name}: {result.message}")
        
        self.is_valid.value = all_valid
        self.validation_errors.value = errors
        
        logger.error(f"📋 Form validation: valid={all_valid}, errors={len(errors)}")
        return all_valid
    
    def get_form_data(self) -> Dict[str, Any]:
        """收集表单数据"""
        data = {}
        
        for field_name, field in self.fields.items():
            if hasattr(field.component, 'get_text'):
                data[field_name] = field.component.get_text()
            elif hasattr(field.component, 'get_value'):
                data[field_name] = field.component.get_value()
            else:
                data[field_name] = None
        
        return data
    
    def set_form_data(self, data: Dict[str, Any]):
        """设置表单数据"""
        for field_name, value in data.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                if hasattr(field.component, 'set_text'):
                    field.component.set_text(str(value))
                elif hasattr(field.component, 'set_value'):
                    field.component.set_value(value)
        
        logger.info(f"📋 Form数据设置: {list(data.keys())}")
    
    def submit(self):
        """提交表单"""
        if self.is_submitting.value:
            logger.warning("⚠️ Form已在提交中，忽略重复提交")
            return
        
        # 验证表单
        if not self.validate():
            logger.error("❌ Form验证失败，不能提交")
            return
        
        # 设置提交状态
        self.is_submitting.value = True
        
        try:
            # 收集表单数据
            form_data = self.get_form_data()
            
            # 调用提交回调
            if self.on_submit:
                self.on_submit(form_data)
                logger.info(f"✅ Form提交成功: {list(form_data.keys())}")
            else:
                logger.info("📋 Form数据已收集但无提交处理器")
        
        except Exception as e:
            logger.error(f"❌ Form提交失败: {e}")
        
        finally:
            self.is_submitting.value = False
    
    def reset(self):
        """重置表单"""
        for field in self.fields.values():
            field.reset()
            
            # 重置组件值
            if hasattr(field.component, 'set_text'):
                field.component.set_text("")
            elif hasattr(field.component, 'set_value'):
                field.component.set_value(0)
        
        logger.info("🔄 Form已重置")

# ================================
# 便捷表单构建器
# ================================

class FormBuilder:
    """表单构建器，提供链式API构建表单"""
    
    def __init__(self):
        self.fields = []
        self.submit_handler = None
    
    def add_text_field(self, name: str, label: str = None, 
                      validators: List[Validator] = None,
                      placeholder: str = "") -> 'FormBuilder':
        """添加文本字段"""
        from .basic import TextField, Label
        
        # 创建组件
        if label:
            # 创建带标签的字段组
            pass  # 后续实现
        else:
            component = TextField(value="", placeholder=placeholder)
        
        # 创建字段
        field = FormField(component, validators or [], name)
        self.fields.append(field)
        
        return self
    
    def add_number_field(self, name: str, label: str = None,
                        validators: List[Validator] = None,
                        min_value: float = 0, max_value: float = 100) -> 'FormBuilder':
        """添加数字字段"""
        from .basic import Slider
        
        component = Slider(value=min_value, min_value=min_value, max_value=max_value)
        field = FormField(component, validators or [], name)
        self.fields.append(field)
        
        return self
    
    def add_switch_field(self, name: str, label: str = None,
                        validators: List[Validator] = None) -> 'FormBuilder':
        """添加开关字段"""
        from .basic import Switch
        
        component = Switch(value=False)
        field = FormField(component, validators or [], name)
        self.fields.append(field)
        
        return self
    
    def on_submit(self, handler: Callable[[Dict[str, Any]], None]) -> 'FormBuilder':
        """设置提交处理器"""
        self.submit_handler = handler
        return self
    
    def build(self) -> Form:
        """构建表单"""
        return Form(fields=self.fields, on_submit=self.submit_handler)

# ================================
# 预设表单模板
# ================================

class FormTemplates:
    """常用表单模板"""
    
    @staticmethod
    def login_form(on_submit: Callable[[Dict[str, Any]], None] = None) -> Form:
        """登录表单模板"""
        from .basic import TextField
        
        # 用户名字段
        username_field = TextField(placeholder="Username")
        username_form_field = FormField(
            username_field, 
            [RequiredValidator("Username is required")], 
            "username"
        )
        
        # 密码字段
        password_field = TextField(placeholder="Password")
        password_form_field = FormField(
            password_field,
            [RequiredValidator("Password is required"),
             LengthValidator(6, message="Password must be at least 6 characters")],
            "password"
        )
        
        return Form([username_form_field, password_form_field], on_submit)
    
    @staticmethod
    def registration_form(on_submit: Callable[[Dict[str, Any]], None] = None) -> Form:
        """注册表单模板"""
        from .basic import TextField
        
        # 邮箱字段
        email_field = TextField(placeholder="Email")
        email_form_field = FormField(
            email_field,
            [RequiredValidator(), EmailValidator()],
            "email"
        )
        
        # 用户名字段
        username_field = TextField(placeholder="Username")
        username_form_field = FormField(
            username_field,
            [RequiredValidator(), LengthValidator(3, 20)],
            "username"
        )
        
        # 密码字段
        password_field = TextField(placeholder="Password")
        password_form_field = FormField(
            password_field,
            [RequiredValidator(), LengthValidator(8, message="Password must be at least 8 characters")],
            "password"
        )
        
        return Form([email_form_field, username_form_field, password_form_field], on_submit)

# ================================
# 使用示例
# ================================

if __name__ == "__main__":
    logger.info("🔧 Hibiki UI v4.0 表单系统测试\n")
    
    # 初始化管理器系统
    from ..core.managers import ManagerFactory
    ManagerFactory.initialize_all()
    
    logger.info("🧪 验证器测试:")
    
    # 测试验证器
    required_validator = RequiredValidator()
    logger.info(f"Required validation (empty): {required_validator.validate('')}")
    logger.info(f"Required validation (filled): {required_validator.validate('hello')}")
    
    email_validator = EmailValidator()
    logger.info(f"Email validation (invalid): {email_validator.validate('invalid-email')}")
    logger.info(f"Email validation (valid): {email_validator.validate('test@example.com')}")
    
    logger.info("\n📋 表单构建器测试:")
    
    # 使用构建器创建表单
    def handle_submit(data):
        logger.info(f"📤 Form submitted: {data}")
    
    form = (FormBuilder()
            .add_text_field("name", validators=[RequiredValidator(), LengthValidator(2, 50)])
            .add_text_field("email", validators=[RequiredValidator(), EmailValidator()])
            .add_number_field("age", validators=[NumberValidator(0, 120)])
            .add_switch_field("subscribe")
            .on_submit(handle_submit)
            .build())
    
    logger.info(f"Form created with {len(form.fields)} fields")
    
    logger.info("\n🎯 表单模板测试:")
    
    # 测试登录表单模板
    login_form = FormTemplates.login_form(handle_submit)
    logger.info(f"Login form created with {len(login_form.fields)} fields")
    
    logger.info("\n✅ 表单系统测试完成！")