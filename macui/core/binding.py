from typing import Any, Callable, Dict, Union

import objc
from Foundation import NSObject

from .signal import Computed, Effect, Signal

# 导入日志系统
try:
    from .logging import get_logger
    logger = get_logger("binding")
except ImportError:
    # 如果日志系统不可用，使用基本的打印
    import logging
    logger = logging.getLogger("macui.binding")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


class ReactiveBinding:
    """绑定响应式信号到 NSView 属性"""

    # 属性设置器映射
    SETTERS: Dict[str, Callable[[Any, Any], None]] = {
        "text": lambda v, val: ReactiveBinding._set_with_log(v, "setStringValue_", str(val) if val is not None else ""),
        "title": lambda v, val: ReactiveBinding._set_with_log(v, "setTitle_", str(val) if val is not None else ""),
        "hidden": lambda v, val: ReactiveBinding._set_with_log(v, "setHidden_", bool(val)),
        "enabled": lambda v, val: ReactiveBinding._set_with_log(v, "setEnabled_", bool(val)),
        "alpha": lambda v, val: ReactiveBinding._set_with_log(v, "setAlphaValue_", float(val)),
        "frame": lambda v, val: ReactiveBinding._set_with_log(v, "setFrame_", val),
        "tooltip": lambda v, val: ReactiveBinding._set_with_log(v, "setToolTip_", str(val) if val is not None else ""),
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
                except:
                    pass
            
            method(value)
            
            if old_value is not None:
                logger.info(f"🎯 UI更新: {type(view).__name__}[{id(view)}].{method_name}({repr(value)}) - 从 '{old_value}' 更新为 '{value}'")
            else:
                logger.info(f"🎯 UI设置: {type(view).__name__}[{id(view)}].{method_name}({repr(value)})")
        except Exception as e:
            logger.error(f"❌ 视图属性设置失败: {type(view).__name__}[{id(view)}].{method_name}({repr(value)}) - {e}")

    # 样式属性映射（需要特殊处理）
    STYLE_SETTERS: Dict[str, Callable[[Any, Any], None]] = {
        "backgroundColor": lambda v, val: hasattr(v, "setBackgroundColor_") and v.setBackgroundColor_(val),
        "borderWidth": lambda v, val: hasattr(v, "setBorderWidth_") and v.setBorderWidth_(float(val)),
        "cornerRadius": lambda v, val: hasattr(v.layer(), "setCornerRadius_") and v.layer().setCornerRadius_(float(val)),
    }

    @staticmethod
    def bind(view: Any, prop: str, signal_or_value: Union[Signal, Computed, Callable, Any]) -> Callable[[], None]:
        """创建响应式绑定
        
        Args:
            view: NSView 或其子类实例
            prop: 属性名称（如 'text', 'hidden', 'enabled' 等）
            signal_or_value: Signal, Computed, 可调用对象或静态值
        
        Returns:
            更新函数，可用于手动解绑
        """
        logger.info(f"ReactiveBinding.bind: {type(view).__name__}[{id(view)}].{prop} -> {type(signal_or_value).__name__}[{id(signal_or_value)}]")
        
        if prop == "style":
            return ReactiveBinding._bind_style(view, signal_or_value)

        setter = ReactiveBinding.SETTERS.get(prop)
        if not setter:
            raise ValueError(f"Unknown property: {prop}. Available properties: {list(ReactiveBinding.SETTERS.keys())}")

        def update():
            try:
                logger.info(f"🔄 ReactiveBinding.update[{prop}]: 开始更新 {type(view).__name__}[{id(view)}]")
                
                # 获取值
                if hasattr(signal_or_value, "value"):
                    # Signal 或 Computed
                    value = signal_or_value.value
                    logger.info(f"🔄 Binding update[{prop}]: 从 {type(signal_or_value).__name__}[{id(signal_or_value)}] 获取值: {repr(value)}")
                elif callable(signal_or_value):
                    # 函数
                    value = signal_or_value()
                    logger.info(f"🔄 Binding update[{prop}]: 从函数获取值: {repr(value)}")
                else:
                    # 静态值
                    value = signal_or_value
                    logger.info(f"🔄 Binding update[{prop}]: 使用静态值: {repr(value)}")

                # 设置属性
                logger.info(f"🔄 Binding update[{prop}]: 即将设置 {type(view).__name__}[{id(view)}] = {repr(value)}")
                setter(view, value)
                logger.info(f"✅ Binding update[{prop}]: 设置完成")
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
            if not hasattr(view, '_macui_effects'):
                view._macui_effects = []
            view._macui_effects.append(effect)
            logger.debug(f"Effect存储到view上: 总Effect数 = {len(view._macui_effects)}")
        except AttributeError:
            # 对于NSObject，使用关联对象
            effects = objc.getAssociatedObject(view, b"macui_effects") or []
            effects.append(effect)
            objc.setAssociatedObject(view, b"macui_effects", effects, objc.OBJC_ASSOCIATION_RETAIN)
            logger.debug(f"Effect通过关联对象存储到view上: 总Effect数 = {len(effects)}")

        # 返回清理函数
        def cleanup():
            effect.cleanup()
            try:
                if hasattr(view, '_macui_effects') and effect in view._macui_effects:
                    view._macui_effects.remove(effect)
                    logger.debug(f"Effect从view清理: 剩余Effect数 = {len(view._macui_effects)}")
            except AttributeError:
                # 对于NSObject，从关联对象中清理
                import objc
                effects = objc.getAssociatedObject(view, b"macui_effects") or []
                if effect in effects:
                    effects.remove(effect)
                    objc.setAssociatedObject(view, b"macui_effects", effects, objc.OBJC_ASSOCIATION_RETAIN)
                    logger.debug(f"Effect从关联对象清理: 剩余Effect数 = {len(effects)}")
        
        return cleanup

    @staticmethod
    def _bind_style(view: Any, style_signal: Union[Signal, Computed, Dict, Callable]) -> Callable[[], None]:
        """绑定样式对象到视图"""
        def update():
            try:
                # 获取样式对象
                if hasattr(style_signal, "value"):
                    styles = style_signal.value
                elif callable(style_signal):
                    styles = style_signal()
                else:
                    styles = style_signal

                if not isinstance(styles, dict):
                    return

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
                        print(f"Unknown style property: {style_prop}")

            except Exception as e:
                print(f"Style binding error: {e}")

        # 创建 Effect 来自动更新
        effect = Effect(update)
        
        # 将effect存储在view上，防止被垃圾回收
        if not hasattr(view, '_macui_effects'):
            view._macui_effects = []
        view._macui_effects.append(effect)

        # 返回清理函数
        def cleanup():
            effect.cleanup()
            if hasattr(view, '_macui_effects') and effect in view._macui_effects:
                view._macui_effects.remove(effect)
        
        return cleanup

    @staticmethod
    def bind_multiple(view: Any, bindings: Dict[str, Union[Signal, Computed, Any]]) -> Callable[[], None]:
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


class TwoWayBinding:
    """双向绑定工具"""

    @staticmethod
    def bind_text_field(field: Any, signal: Signal[str]) -> Callable[[], None]:
        """为文本框创建双向绑定"""
        # 单向绑定：signal -> field
        one_way_cleanup = ReactiveBinding.bind(field, "text", signal)

        # 反向绑定：field -> signal
        delegate = MacUITextFieldDelegate.alloc().init()
        delegate.signal = signal
        field.setDelegate_(delegate)

        # 保持委托的引用
        objc.setAssociatedObject(field, b"text_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

        # 返回组合的清理函数
        return lambda: one_way_cleanup()


# 事件处理委托类
class MacUIButtonTarget(NSObject):
    """按钮点击目标类"""

    def initWithHandler_(self, handler):
        self = objc.super(MacUIButtonTarget, self).init()
        if self is None:
            return None
        self.handler = handler
        logger.info(f"🎯 MacUIButtonTarget.initWithHandler_: Target[{id(self)}] 初始化，handler={handler.__name__ if hasattr(handler, '__name__') else str(handler)}")
        return self

    def buttonClicked_(self, sender):
        """按钮点击处理方法 - 必须暴露给Objective-C"""
        logger.info(f"🎯 MacUIButtonTarget.buttonClicked_: Target[{id(self)}] 收到点击事件，sender={type(sender).__name__}[{id(sender)}]")
        if self.handler:
            try:
                logger.info(f"🎯 即将调用handler: {self.handler.__name__ if hasattr(self.handler, '__name__') else str(self.handler)}")
                self.handler()
                logger.info(f"🎯 Handler调用完成")
            except Exception as e:
                logger.error(f"❌ Button click handler error: {e}")
                import traceback
                logger.error(f"❌ 详细错误: {traceback.format_exc()}")
        else:
            logger.warning(f"⚠️ MacUIButtonTarget.buttonClicked_: Target[{id(self)}] 没有handler函数")


class MacUITextFieldDelegate(NSObject):
    """文本框委托类"""

    def init(self):
        self = objc.super(MacUITextFieldDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.change_handler = None
        return self

    def controlTextDidChange_(self, notification):
        """文本改变时的处理"""
        text_field = notification.object()
        new_value = str(text_field.stringValue())

        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = new_value

        # 调用变更处理器
        if self.change_handler:
            try:
                self.change_handler(new_value)
            except Exception as e:
                print(f"Text change handler error: {e}")

    def controlTextDidEndEditing_(self, notification):
        """文本编辑结束处理"""


# 事件绑定工具
class EventBinding:
    """事件绑定工具"""

    @staticmethod
    def bind_click(button: Any, handler: Callable[[], None]) -> Any:
        """绑定按钮点击事件"""
        logger.info(f"🔗 EventBinding.bind_click: 绑定点击事件到 {type(button).__name__}[{id(button)}]")
        logger.info(f"🔗 Handler函数: {handler.__name__ if hasattr(handler, '__name__') else str(handler)}")
        
        # 创建目标对象
        target = MacUIButtonTarget.alloc().initWithHandler_(handler)
        logger.info(f"🔗 MacUIButtonTarget已创建: {type(target).__name__}[{id(target)}]")

        # 设置目标和动作
        button.setTarget_(target)
        # 使用字符串设置action，这是最简单可靠的方法
        button.setAction_("buttonClicked:")
        logger.info(f"🔗 按钮目标和动作已设置")
        
        # 验证设置是否成功
        current_target = button.target()
        current_action = button.action()
        logger.info(f"🔗 验证 - 按钮target: {type(current_target).__name__ if current_target else 'None'}")
        logger.info(f"🔗 验证 - 按钮action: {current_action}")
        logger.info(f"🔗 验证 - target有buttonClicked_方法: {hasattr(target, 'buttonClicked_')}")

        # 使用关联对象保持目标的引用，避免被垃圾回收
        objc.setAssociatedObject(button, b"click_target", target, objc.OBJC_ASSOCIATION_RETAIN)
        logger.info(f"🔗 目标对象已关联到按钮，防止垃圾回收")

        return target

    @staticmethod
    def bind_text_change(text_field: Any, signal: Signal = None, handler: Callable[[str], None] = None) -> Any:
        """绑定文本变更事件"""
        # 创建委托对象
        delegate = MacUITextFieldDelegate.alloc().init()
        delegate.signal = signal
        delegate.change_handler = handler

        # 设置委托
        text_field.setDelegate_(delegate)

        # 保持委托的引用
        objc.setAssociatedObject(text_field, b"text_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)

        return delegate
