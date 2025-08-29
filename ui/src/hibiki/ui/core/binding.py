from typing import Any, Callable, Dict, Union

import objc
from Foundation import NSObject

from .reactive import Computed, Effect, Signal

from .logging import get_logger

logger = get_logger("binding")
logger.setLevel("INFO")


class ReactiveBinding:
    """绑定响应式信号到 NSView 属性"""

    # 属性设置器映射
    SETTERS: Dict[str, Callable[[Any, Any], None]] = {
        "text": lambda v, val: ReactiveBinding._set_with_log(
            v, "setStringValue_", str(val) if val is not None else ""
        ),
        "stringValue": lambda v, val: ReactiveBinding._set_with_log(
            v, "setStringValue_", str(val) if val is not None else ""
        ),  # 添加stringValue支持
        "string": lambda v, val: ReactiveBinding._set_with_log(
            v, "setString_", str(val) if val is not None else ""
        ),  # NSTextView支持
        "title": lambda v, val: ReactiveBinding._set_with_log(
            v, "setTitle_", str(val) if val is not None else ""
        ),
        "hidden": lambda v, val: ReactiveBinding._set_with_log(v, "setHidden_", bool(val)),
        "enabled": lambda v, val: ReactiveBinding._set_with_log(v, "setEnabled_", bool(val)),
        "alpha": lambda v, val: ReactiveBinding._set_with_log(v, "setAlphaValue_", float(val)),
        "frame": lambda v, val: ReactiveBinding._set_with_log(v, "setFrame_", val),
        "tooltip": lambda v, val: ReactiveBinding._set_with_log(
            v, "setToolTip_", str(val) if val is not None else ""
        ),
        "doubleValue": lambda v, val: ReactiveBinding._set_with_log(
            v, "setDoubleValue_", float(val) if not hasattr(val, "value") else float(val.value)
        ),
        "state": lambda v, val: ReactiveBinding._set_with_log(
            v, "setState_", 1 if bool(val) else 0
        ),
    }

    @staticmethod
    def _set_with_log(view, method_name: str, value):
        """带日志的属性设置"""
        try:
            method = getattr(view, method_name)

            # 记录设置前的值（如果可能）
            old_value = None
            if hasattr(view, method_name.replace("set", "").replace("_", "").lower()):
                try:
                    getter_name = method_name.replace("set", "").replace("_", "")
                    if hasattr(view, getter_name):
                        old_value = getattr(view, getter_name)()
                    elif hasattr(view, "stringValue") and method_name == "setStringValue_":
                        old_value = view.stringValue()
                except Exception:
                    pass  # 忽略获取旧值的错误

            # UI设置的详细日志已移除，避免大量打印
            method(value)

            # 值变化的日志已移除，避免大量打印

        except Exception as e:
            logger.error(f"❌ UI设置错误: {method_name} = {value}, 错误: {e}")
            raise

    @staticmethod
    def bind(
        view: Any, prop: str, signal_or_value: Union[Signal, Computed, Callable, Any]
    ) -> Callable[[], None]:
        """创建响应式绑定

        Args:
            view: NSView 或其子类实例
            prop: 属性名称（如 'text', 'hidden', 'enabled' 等）
            signal_or_value: Signal, Computed, 可调用对象或静态值

        Returns:
            更新函数，可用于手动解绑
        """
        logger.debug(
            f"ReactiveBinding.bind: {type(view).__name__}[{id(view)}].{prop} -> {type(signal_or_value).__name__}[{id(signal_or_value)}]"
        )

        if prop == "style":
            return ReactiveBinding._bind_style(view, signal_or_value)

        setter = ReactiveBinding.SETTERS.get(prop)
        if not setter:
            raise ValueError(
                f"Unknown property: {prop}. Available properties: {list(ReactiveBinding.SETTERS.keys())}"
            )

        def update():
            try:
                # ReactiveBinding更新和线程调试日志已移除，避免大量打印

                # 获取值
                if isinstance(signal_or_value, (Signal, Computed)):
                    # Signal 或 Computed - 调用value属性来建立依赖关系
                    # Signal访问的日志已移除
                    value = signal_or_value.value  # 这里会触发Signal.get()并注册观察者
                    # 从Signal获取值的日志已移除
                    pass
                elif callable(signal_or_value):
                    # 可调用对象
                    value = signal_or_value()
                    # 从可调用对象获取值的日志已移除
                else:
                    # 静态值
                    value = signal_or_value
                    # 静态值使用的日志已移除

                # 应用值到视图
                # UI设置的详细日志已移除，避免大量打印
                setter(view, value)
                # 设置完成的日志已移除
            except Exception as e:
                logger.error(f"❌ Binding update error for {prop}: {e}")
                import traceback

                logger.error(f"❌ 详细错误: {traceback.format_exc()}")

        # 创建 Effect 来自动更新
        logger.debug(f"创建Effect进行绑定: {prop}")
        effect = Effect(update)

        # 将effect存储在view上，防止被垃圾回收
        # 使用objc.setAssociatedObject对NSObject存储Python对象
        import objc

        try:
            if not hasattr(view, "_hibiki_effects"):
                view._hibiki_effects = []
            view._hibiki_effects.append(effect)
            logger.debug(f"Effect存储到view上: 总Effect数 = {len(view._hibiki_effects)}")
        except AttributeError:
            # 对于NSObject，使用关联对象
            effects = objc.getAssociatedObject(view, b"hibiki_effects") or []
            effects.append(effect)
            objc.setAssociatedObject(view, b"hibiki_effects", effects, objc.OBJC_ASSOCIATION_RETAIN)
            logger.debug(f"Effect通过关联对象存储到view上: 总Effect数 = {len(effects)}")

        # 返回清理函数
        def cleanup():
            effect.cleanup()
            try:
                if hasattr(view, "_hibiki_effects") and effect in view._hibiki_effects:
                    view._hibiki_effects.remove(effect)
                    logger.debug(f"Effect从view清理: 剩余Effect数 = {len(view._hibiki_effects)}")
            except AttributeError:
                # 对于NSObject，从关联对象中清理
                import objc

                effects = objc.getAssociatedObject(view, b"hibiki_effects") or []
                if effect in effects:
                    effects.remove(effect)
                    objc.setAssociatedObject(
                        view, b"hibiki_effects", effects, objc.OBJC_ASSOCIATION_RETAIN
                    )
                    logger.debug(f"Effect从关联对象清理: 剩余Effect数 = {len(effects)}")

        return cleanup

    # 样式设置器映射
    STYLE_SETTERS: Dict[str, Callable[[Any, Any], None]] = {
        "backgroundColor": lambda v, val: ReactiveBinding._set_with_log(v, "setWantsLayer_", True)
        or ReactiveBinding._set_with_log(v.layer(), "setBackgroundColor_", val),
        "alpha": lambda v, val: ReactiveBinding._set_with_log(v, "setAlphaValue_", float(val)),
        "hidden": lambda v, val: ReactiveBinding._set_with_log(v, "setHidden_", bool(val)),
        "frame": lambda v, val: ReactiveBinding._set_with_log(v, "setFrame_", val),
    }

    @staticmethod
    def _bind_style(view: Any, style_dict: Dict[str, Any]) -> Callable[[], None]:
        """绑定样式字典"""

        def update():
            try:
                # 如果传入的是响应式样式字典
                if hasattr(style_dict, "value"):
                    styles = style_dict.value
                elif callable(style_dict):
                    styles = style_dict()
                else:
                    styles = style_dict

                # 应用每个样式属性
                for style_prop, style_value in styles.items():
                    style_setter = ReactiveBinding.STYLE_SETTERS.get(style_prop)
                    if style_setter:
                        # 如果样式值也是信号，需要获取其值
                        if hasattr(style_value, "value"):
                            actual_value = style_value.value
                        elif callable(style_value):
                            actual_value = style_value()
                        else:
                            actual_value = style_value

                        style_setter(view, actual_value)
                    else:
                        logger.info(f"Unknown style property: {style_prop}")

            except Exception as e:
                logger.error(f"Style binding error: {e}")

        # 创建 Effect 来自动更新
        effect = Effect(update)

        # 将effect存储在view上，防止被垃圾回收
        if not hasattr(view, "_hibiki_effects"):
            view._hibiki_effects = []
        view._hibiki_effects.append(effect)

        # 返回清理函数
        def cleanup():
            effect.cleanup()
            if hasattr(view, "_hibiki_effects") and effect in view._hibiki_effects:
                view._hibiki_effects.remove(effect)

        return cleanup

    @staticmethod
    def bind_multiple(
        view: Any, bindings: Dict[str, Union[Signal, Computed, Any]]
    ) -> Callable[[], None]:
        """绑定多个属性到视图

        Args:
            view: NSView 实例
            bindings: 属性名到信号/值的映射

        Returns:
            清理函数
        """
        cleanup_functions = []

        for prop, signal_or_value in bindings.items():
            cleanup_fn = ReactiveBinding.bind(view, prop, signal_or_value)
            cleanup_functions.append(cleanup_fn)

        # 返回组合的清理函数
        def cleanup_all():
            for cleanup_fn in cleanup_functions:
                cleanup_fn()

        return cleanup_all


def bind_text(view: Any, text_source: Union[Signal, Computed, str]) -> Callable[[], None]:
    """绑定文本的便捷函数"""
    return ReactiveBinding.bind(view, "stringValue", text_source)


def bind_visibility(view: Any, visibility_source: Union[Signal, Computed, bool]) -> "Effect":
    """绑定可见性的便捷函数"""
    return ReactiveBinding.bind(view, "hidden", visibility_source)


def bind_enabled(view: Any, enabled_source: Union[Signal, Computed, bool]) -> "Effect":
    """绑定启用状态的便捷函数"""
    return ReactiveBinding.bind(view, "enabled", enabled_source)


# ================================
# 表单数据绑定扩展
# ================================


class FormDataBinding:
    """表单数据绑定系统，支持双向数据绑定"""

    @staticmethod
    def bind_form_field(view: Any, field_name: str, form_data: Signal) -> Callable[[], None]:
        """绑定表单字段到表单数据Signal

        Args:
            view: NSView控件实例
            field_name: 字段名称
            form_data: 包含表单数据字典的Signal

        Returns:
            清理函数
        """
        logger.debug(f"FormDataBinding: 绑定字段 {field_name} 到 {type(view).__name__}")

        # 单向绑定：从form_data到UI
        def update_ui():
            try:
                data_dict = form_data.value
                if isinstance(data_dict, dict) and field_name in data_dict:
                    field_value = data_dict[field_name]

                    # 根据控件类型设置值
                    if hasattr(view, "setStringValue_"):
                        # TextField类型
                        view.setStringValue_(str(field_value))
                    elif hasattr(view, "setDoubleValue_"):
                        # Slider类型
                        view.setDoubleValue_(float(field_value))
                    elif hasattr(view, "setState_"):
                        # Switch类型
                        view.setState_(1 if bool(field_value) else 0)

                    logger.debug(f"FormDataBinding: UI更新 {field_name} = {field_value}")

            except Exception as e:
                logger.error(f"FormDataBinding UI更新错误: {e}")

        # 创建Effect进行单向绑定
        ui_effect = Effect(update_ui)

        # 双向绑定：从UI到form_data (需要UI控件支持change事件)
        change_cleanup = None
        if hasattr(view, "setTarget_") and hasattr(view, "setAction_"):
            # 为支持target/action的控件创建双向绑定
            change_cleanup = FormDataBinding._create_change_binding(view, field_name, form_data)

        # 存储effect到view上
        if not hasattr(view, "_hibiki_form_effects"):
            view._hibiki_form_effects = []
        view._hibiki_form_effects.append(ui_effect)

        # 返回清理函数
        def cleanup():
            ui_effect.cleanup()
            if change_cleanup:
                change_cleanup()
            if hasattr(view, "_hibiki_form_effects") and ui_effect in view._hibiki_form_effects:
                view._hibiki_form_effects.remove(ui_effect)

        return cleanup

    @staticmethod
    def _create_change_binding(view: Any, field_name: str, form_data: Signal) -> Callable[[], None]:
        """创建UI到数据的变化绑定"""
        try:
            from Foundation import NSObject
            import objc

            # 创建委托类处理UI变化
            class FormFieldDelegate(NSObject):
                def init(self):
                    self = objc.super(FormFieldDelegate, self).init()
                    if self is None:
                        return None
                    self.field_name = field_name
                    self.form_data = form_data
                    return self

                def fieldChanged_(self, sender):
                    try:
                        # 获取新值
                        new_value = None
                        if hasattr(sender, "stringValue"):
                            new_value = sender.stringValue()
                        elif hasattr(sender, "doubleValue"):
                            new_value = sender.doubleValue()
                        elif hasattr(sender, "state"):
                            new_value = bool(sender.state())

                        # 更新form_data
                        current_data = (
                            self.form_data.value.copy()
                            if isinstance(self.form_data.value, dict)
                            else {}
                        )
                        current_data[self.field_name] = new_value
                        self.form_data.value = current_data

                        logger.debug(f"FormDataBinding: 数据更新 {self.field_name} = {new_value}")

                    except Exception as e:
                        logger.error(f"FormDataBinding 变化处理错误: {e}")

            # 创建并设置委托
            delegate = FormFieldDelegate.alloc().init()
            delegate.field_name = field_name
            delegate.form_data = form_data

            view.setTarget_(delegate)
            view.setAction_("fieldChanged:")

            # 存储委托引用防止被回收
            if not hasattr(view, "_hibiki_form_delegates"):
                view._hibiki_form_delegates = []
            view._hibiki_form_delegates.append(delegate)

            # 返回清理函数
            def cleanup():
                if (
                    hasattr(view, "_hibiki_form_delegates")
                    and delegate in view._hibiki_form_delegates
                ):
                    view._hibiki_form_delegates.remove(delegate)
                    view.setTarget_(None)
                    view.setAction_(None)

            return cleanup

        except Exception as e:
            logger.error(f"创建变化绑定失败: {e}")
            return lambda: None

    @staticmethod
    def bind_form_data(
        form_container: Any, form_data: Signal, field_mappings: Dict[str, Any]
    ) -> Callable[[], None]:
        """批量绑定表单数据到容器中的控件

        Args:
            form_container: 表单容器组件
            form_data: 表单数据Signal
            field_mappings: 字段名到控件的映射

        Returns:
            清理函数
        """
        cleanup_functions = []

        for field_name, view in field_mappings.items():
            cleanup_fn = FormDataBinding.bind_form_field(view, field_name, form_data)
            cleanup_functions.append(cleanup_fn)

        logger.debug(f"FormDataBinding: 批量绑定完成，共 {len(field_mappings)} 个字段")

        # 返回组合清理函数
        def cleanup_all():
            for cleanup_fn in cleanup_functions:
                cleanup_fn()

        return cleanup_all


def bind_form_field(view: Any, field_name: str, form_data: Signal) -> Callable[[], None]:
    """绑定表单字段的便捷函数"""
    return FormDataBinding.bind_form_field(view, field_name, form_data)


def bind_form_data(
    form_container: Any, form_data: Signal, field_mappings: Dict[str, Any]
) -> Callable[[], None]:
    """批量绑定表单数据的便捷函数"""
    return FormDataBinding.bind_form_data(form_container, form_data, field_mappings)


# 导出
__all__ = [
    "ReactiveBinding",
    "FormDataBinding",
    "bind_text",
    "bind_visibility",
    "bind_enabled",
    "bind_form_field",
    "bind_form_data",
]
