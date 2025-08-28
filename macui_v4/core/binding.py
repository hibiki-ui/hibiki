from typing import Any, Callable, Dict, Union

import objc
from Foundation import NSObject

from .reactive import Computed, Effect, Signal

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
        "stringValue": lambda v, val: ReactiveBinding._set_with_log(v, "setStringValue_", str(val) if val is not None else ""),  # 添加stringValue支持
        "title": lambda v, val: ReactiveBinding._set_with_log(v, "setTitle_", str(val) if val is not None else ""),
        "hidden": lambda v, val: ReactiveBinding._set_with_log(v, "setHidden_", bool(val)),
        "enabled": lambda v, val: ReactiveBinding._set_with_log(v, "setEnabled_", bool(val)),
        "alpha": lambda v, val: ReactiveBinding._set_with_log(v, "setAlphaValue_", float(val)),
        "frame": lambda v, val: ReactiveBinding._set_with_log(v, "setFrame_", val),
        "tooltip": lambda v, val: ReactiveBinding._set_with_log(v, "setToolTip_", str(val) if val is not None else ""),
        "doubleValue": lambda v, val: ReactiveBinding._set_with_log(v, "setDoubleValue_", float(val)),
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
            
            logger.info(f"🎯 UI设置: {type(view).__name__}[{id(view)}].{method_name}({repr(value)})")
            method(value)
            
            if old_value is not None:
                logger.debug(f"🔄 值变化: {old_value} -> {value}")
                
        except Exception as e:
            logger.error(f"❌ UI设置错误: {method_name} = {value}, 错误: {e}")
            raise

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
                
                # 直接使用当前模块中导入的Signal类
                current_observer = Signal._current_observer.get()
                import threading
                thread_id = threading.get_ident()
                logger.info(f"🔍 Binding.update: 线程ID={thread_id}, 当前观察者 = {type(current_observer).__name__ if current_observer else 'None'}[{id(current_observer) if current_observer else 'N/A'}]")
                
                # 获取值
                if isinstance(signal_or_value, (Signal, Computed)):
                    # Signal 或 Computed - 调用value属性来建立依赖关系
                    logger.info(f"🎯 Binding: 访问 {type(signal_or_value).__name__}.value，当前观察者: {current_observer}")
                    value = signal_or_value.value  # 这里会触发Signal.get()并注册观察者
                    logger.info(f"🔄 Binding update[{prop}]: 从{type(signal_or_value).__name__}获取值: {value}")
                elif callable(signal_or_value):
                    # 可调用对象
                    value = signal_or_value()
                    logger.info(f"🔄 Binding update[{prop}]: 从可调用对象获取值: {value}")
                else:
                    # 静态值
                    value = signal_or_value
                    logger.info(f"🔄 Binding update[{prop}]: 使用静态值: {repr(value)}")
                
                # 应用值到视图
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

    # 样式设置器映射
    STYLE_SETTERS: Dict[str, Callable[[Any, Any], None]] = {
        "backgroundColor": lambda v, val: ReactiveBinding._set_with_log(v, "setWantsLayer_", True) or ReactiveBinding._set_with_log(v.layer(), "setBackgroundColor_", val),
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


def bind_text(view: Any, text_source: Union[Signal, Computed, str]) -> Callable[[], None]:
    """绑定文本的便捷函数"""
    return ReactiveBinding.bind(view, "stringValue", text_source)

def bind_visibility(view: Any, visibility_source: Union[Signal, Computed, bool]) -> 'Effect':
    """绑定可见性的便捷函数"""
    return ReactiveBinding.bind(view, "hidden", visibility_source)

def bind_enabled(view: Any, enabled_source: Union[Signal, Computed, bool]) -> 'Effect':
    """绑定启用状态的便捷函数"""
    return ReactiveBinding.bind(view, "enabled", enabled_source)

# 导出
__all__ = [
    'ReactiveBinding',
    'bind_text', 'bind_visibility', 'bind_enabled'
]