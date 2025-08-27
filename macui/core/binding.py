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


class EnhancedSliderDelegate(NSObject):
    """增强的滑块委托，支持步长和事件处理"""

    def init(self):
        self = objc.super(EnhancedSliderDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        self.step_size = None
        logger.info(f"🎚️ EnhancedSliderDelegate初始化: {id(self)}")
        return self

    def sliderChanged_(self, sender):
        """滑块值改变时的处理"""
        new_value = sender.doubleValue()
        logger.info(f"🎚️ 滑块值改变: {new_value}")

        # 步长处理
        if self.step_size is not None:
            # 将值调整到最近的步长
            stepped_value = round(new_value / self.step_size) * self.step_size
            if stepped_value != new_value:
                sender.setDoubleValue_(stepped_value)
                new_value = stepped_value
                logger.info(f"🎚️ 滑块值调整到步长: {stepped_value}")

        # 更新信号
        if self.signal:
            # 防止循环更新
            if self.signal.value != new_value:
                self.signal.value = new_value

        # 调用回调
        if self.on_change:
            self.on_change(new_value)


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

    @staticmethod
    def bind_slider(slider: Any, signal: Signal[float]) -> Callable[[], None]:
        """为滑块创建双向绑定"""
        # 单向绑定：signal -> slider
        one_way_cleanup = ReactiveBinding.bind(slider, "doubleValue", signal)

        # 反向绑定：slider -> signal (通过现有的委托处理)
        # 如果滑块已有委托，确保信号被正确设置
        existing_delegate = slider.target()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: one_way_cleanup()

    @staticmethod  
    def bind_text_view(text_view: Any, signal: Signal[str]) -> Callable[[], None]:
        """为NSTextView创建双向绑定"""
        # 单向绑定：signal -> text_view (需要特殊处理NSTextView)
        def update_text_view():
            if hasattr(text_view, 'setString_'):
                text_view.setString_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_text_view)
        
        # 反向绑定：text_view -> signal (通过现有的委托处理)
        # 如果文本视图已有委托，确保信号被正确设置
        existing_delegate = text_view.delegate()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None  # NSTextView 清理较复杂，暂时简化

    @staticmethod
    def bind_button_state(button: Any, signal: Signal[bool]) -> Callable[[], None]:
        """为按钮状态（Switch/Checkbox）创建双向绑定"""
        # 单向绑定：signal -> button state
        def update_button_state():
            button.setState_(1 if signal.value else 0)
        
        from .signal import Effect
        effect = Effect(update_button_state)
        
        # 反向绑定：button -> signal (通过现有的委托处理)
        existing_delegate = button.target()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_radio_button(radio: Any, signal: Signal[str], option_value: str) -> Callable[[], None]:
        """为单选按钮创建双向绑定"""
        # 单向绑定：signal -> radio state
        def update_radio_state():
            radio.setState_(1 if signal.value == option_value else 0)
        
        from .signal import Effect
        effect = Effect(update_radio_state)
        
        # 反向绑定：radio -> signal (通过现有的委托处理)
        existing_delegate = radio.target()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal
            existing_delegate.option_value = option_value

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_segmented_control(segmented: Any, signal: Signal[int]) -> Callable[[], None]:
        """为分段控件创建双向绑定"""
        # 单向绑定：signal -> segmented control
        def update_segmented_selection():
            if 0 <= signal.value < segmented.segmentCount():
                segmented.setSelectedSegment_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_segmented_selection)
        
        # 反向绑定：segmented -> signal (通过现有的委托处理)
        existing_delegate = segmented.target()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_popup_button(popup: Any, signal: Signal[int]) -> Callable[[], None]:
        """为下拉按钮创建双向绑定"""
        # 单向绑定：signal -> popup button
        def update_popup_selection():
            if 0 <= signal.value < popup.numberOfItems():
                popup.selectItemAtIndex_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_popup_selection)
        
        # 反向绑定：popup -> signal (通过现有的委托处理)
        existing_delegate = popup.target()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_combo_box(combo: Any, signal: Signal[str]) -> Callable[[], None]:
        """为ComboBox创建双向绑定"""
        # 单向绑定：signal -> combo box
        def update_combo_text():
            combo.setStringValue_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_combo_text)
        
        # 反向绑定：combo -> signal (通过委托处理)
        existing_delegate = combo.delegate()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_date_picker(picker: Any, signal) -> Callable[[], None]:
        """为DatePicker创建双向绑定"""
        # 单向绑定：signal -> date picker
        def update_date():
            picker.setDateValue_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_date)
        
        # 反向绑定：picker -> signal (通过委托处理)
        existing_delegate = picker.delegate()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None

    @staticmethod
    def bind_tab_view(tab_view: Any, signal: Signal[int]) -> Callable[[], None]:
        """为TabView创建双向绑定"""
        # 单向绑定：signal -> tab view
        def update_selected_tab():
            if 0 <= signal.value < tab_view.numberOfTabViewItems():
                tab_view.selectTabViewItemAtIndex_(signal.value)
        
        from .signal import Effect
        effect = Effect(update_selected_tab)
        
        # 反向绑定：tab_view -> signal (通过委托处理)
        existing_delegate = tab_view.delegate()
        if existing_delegate and hasattr(existing_delegate, 'signal'):
            existing_delegate.signal = signal

        # 返回清理函数
        return lambda: None


class EnhancedPopUpDelegate(NSObject):
    """增强的下拉按钮委托"""

    def init(self):
        self = objc.super(EnhancedPopUpDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        logger.info(f"📋 EnhancedPopUpDelegate初始化: {id(self)}")
        return self

    def popUpChanged_(self, sender):
        """下拉选择改变时的处理"""
        new_index = sender.indexOfSelectedItem()
        logger.info(f"📋 下拉按钮选择改变: {new_index}")

        # 更新信号
        if self.signal:
            # 防止循环更新
            if self.signal.value != new_index:
                self.signal.value = new_index

        # 调用回调
        if self.on_change:
            self.on_change(new_index)


class EnhancedSegmentedDelegate(NSObject):
    """增强的分段控件委托"""

    def init(self):
        self = objc.super(EnhancedSegmentedDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        logger.info(f"🎛️ EnhancedSegmentedDelegate初始化: {id(self)}")
        return self

    def segmentChanged_(self, sender):
        """分段选择改变时的处理"""
        new_segment = sender.selectedSegment()
        logger.info(f"🎛️ 分段控件选择改变: {new_segment}")

        # 更新信号
        if self.signal:
            # 防止循环更新
            if self.signal.value != new_segment:
                self.signal.value = new_segment

        # 调用回调
        if self.on_change:
            self.on_change(new_segment)


class EnhancedButtonDelegate(NSObject):
    """增强的按钮委托，支持Switch/Checkbox状态改变事件"""

    def init(self):
        self = objc.super(EnhancedButtonDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        logger.info(f"🔘 EnhancedButtonDelegate初始化: {id(self)}")
        return self

    def buttonStateChanged_(self, sender):
        """按钮状态改变时的处理"""
        new_state = sender.state() == 1
        logger.info(f"🔘 按钮状态改变: {new_state}")

        # 更新信号
        if self.signal:
            # 防止循环更新
            if self.signal.value != new_state:
                self.signal.value = new_state

        # 调用回调
        if self.on_change:
            self.on_change(new_state)


class EnhancedRadioDelegate(NSObject):
    """增强的单选按钮委托"""

    def init(self):
        self = objc.super(EnhancedRadioDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        self.option_value = None
        logger.info(f"📻 EnhancedRadioDelegate初始化: {id(self)}")
        return self

    def radioButtonChanged_(self, sender):
        """单选按钮改变时的处理"""
        if sender.state() == 1:  # 只处理选中状态
            logger.info(f"📻 单选按钮选中: {self.option_value}")

            # 更新信号
            if self.signal and self.option_value is not None:
                # 防止循环更新
                if self.signal.value != self.option_value:
                    self.signal.value = self.option_value

            # 调用回调
            if self.on_change and self.option_value is not None:
                self.on_change(self.option_value)


class EnhancedTextViewDelegate(NSObject):
    """增强的文本视图委托，支持NSTextView的文本改变事件"""

    def init(self):
        self = objc.super(EnhancedTextViewDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        logger.info(f"📝 EnhancedTextViewDelegate初始化: {id(self)}")
        return self

    def textDidChange_(self, notification):
        """文本改变时的处理"""
        text_view = notification.object()
        if hasattr(text_view, 'string'):
            new_value = str(text_view.string())
        else:
            new_value = ""
        
        logger.info(f"📝 文本视图内容改变: '{new_value[:50]}...' (长度: {len(new_value)})")

        # 更新信号
        if self.signal:
            # 防止循环更新
            if self.signal.value != new_value:
                self.signal.value = new_value

        # 调用回调
        if self.on_change:
            self.on_change(new_value)


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
        pass


class EnhancedTextFieldDelegate(NSObject):
    """增强的文本框委托类 - 支持验证、格式化等高级功能"""

    def init(self):
        self = objc.super(EnhancedTextFieldDelegate, self).init()
        if self is None:
            return None
        self.signal = None
        self.on_change = None
        self.on_enter = None
        self.on_focus = None
        self.on_blur = None
        self.validation = None
        self.formatting = None
        self.max_length = None
        logger.info(f"🔧 EnhancedTextFieldDelegate初始化: {id(self)}")
        return self

    def controlTextDidChange_(self, notification):
        """文本改变时的处理 - 包含验证和长度限制"""
        text_field = notification.object()
        new_value = str(text_field.stringValue())
        logger.info(f"🔧 文本改变: '{new_value}'")

        # 长度限制
        if self.max_length and len(new_value) > self.max_length:
            truncated_value = new_value[:self.max_length]
            text_field.setStringValue_(truncated_value)
            new_value = truncated_value
            logger.info(f"🔧 文本截断到最大长度 {self.max_length}: '{truncated_value}'")

        # 验证
        if self.validation:
            try:
                is_valid = self.validation(new_value)
                if not is_valid:
                    logger.info(f"🔧 文本验证失败: '{new_value}'")
                    # 可以在这里添加视觉反馈
                    return
            except Exception as e:
                logger.error(f"🔧 验证函数错误: {e}")

        # 格式化
        if self.formatting:
            try:
                formatted_value = self.formatting(new_value)
                if formatted_value != new_value:
                    text_field.setStringValue_(formatted_value)
                    new_value = formatted_value
                    logger.info(f"🔧 文本格式化: '{new_value}'")
            except Exception as e:
                logger.error(f"🔧 格式化函数错误: {e}")

        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = new_value

        # 调用变更处理器
        if self.on_change:
            try:
                self.on_change(new_value)
            except Exception as e:
                logger.error(f"🔧 文本变更处理器错误: {e}")

    def controlTextDidEndEditing_(self, notification):
        """文本编辑结束处理 - 检查回车键"""
        logger.info("🔧 文本编辑结束")
        
        # 检查是否按了回车键
        if self.on_enter:
            # 获取结束编辑的原因
            user_info = notification.userInfo()
            if user_info:
                movement = user_info.get("NSTextMovement")
                if movement == 16:  # NSReturnTextMovement
                    try:
                        logger.info("🔧 检测到回车键，调用on_enter")
                        self.on_enter()
                    except Exception as e:
                        logger.error(f"🔧 回车处理器错误: {e}")

        # 失去焦点回调
        if self.on_blur:
            try:
                self.on_blur()
            except Exception as e:
                logger.error(f"🔧 失去焦点处理器错误: {e}")

    def controlTextDidBeginEditing_(self, notification):
        """文本开始编辑处理 - 获得焦点"""
        logger.info("🔧 文本开始编辑")
        
        if self.on_focus:
            try:
                self.on_focus()
            except Exception as e:
                logger.error(f"🔧 获得焦点处理器错误: {e}")

    def control_textView_doCommandBySelector_(self, control, text_view, command):
        """处理特殊键盘命令"""
        logger.info(f"🔧 键盘命令: {command}")
        
        # 处理回车键（另一种方式）
        if command == "insertNewline:" and self.on_enter:
            try:
                self.on_enter()
                return True  # 阻止默认行为
            except Exception as e:
                logger.error(f"🔧 回车命令处理错误: {e}")
        
        return False  # 允许默认处理


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


class EnhancedComboBoxDelegate(NSObject):
    """增强的 ComboBox 委托类，处理文本变更和选择事件"""
    
    def init(self):
        self = objc.super(EnhancedComboBoxDelegate, self).init()
        if self is None:
            return None
            
        self.signal = None
        self.on_change = None
        self.on_select = None
        
        logger.info("🎛️ ComboBox委托对象已初始化")
        return self
    
    def comboBoxSelectionDidChange_(self, notification):
        """ComboBox 选择发生变化"""
        combo_box = notification.object()
        selected_index = combo_box.indexOfSelectedItem()
        selected_text = combo_box.stringValue()
        
        logger.info(f"🎛️ ComboBox选择变化 - 索引: {selected_index}, 文本: '{selected_text}'")
        
        # 更新信号（如果绑定的是文本）
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = selected_text
            
        # 调用选择变更处理器
        if self.on_select:
            try:
                self.on_select(selected_index, selected_text)
            except Exception as e:
                logger.error(f"🎛️ 选择处理器错误: {e}")
    
    def controlTextDidChange_(self, notification):
        """文本输入发生变化（可编辑模式）"""
        combo_box = notification.object()
        new_value = combo_box.stringValue()
        
        logger.info(f"🎛️ ComboBox文本变化: '{new_value}'")
        
        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = new_value
            
        # 调用变更处理器
        if self.on_change:
            try:
                self.on_change(new_value)
            except Exception as e:
                logger.error(f"🎛️ 文本变更处理器错误: {e}")
    
    def controlTextDidEndEditing_(self, notification):
        """文本编辑结束"""
        logger.info("🎛️ ComboBox文本编辑结束")


class EnhancedMenuItemDelegate(NSObject):
    """增强的 MenuItem 委托类，处理菜单项点击事件"""
    
    def init(self):
        self = objc.super(EnhancedMenuItemDelegate, self).init()
        if self is None:
            return None
            
        self.on_click = None
        self.item_id = None
        
        logger.info("📋 MenuItem委托对象已初始化")
        return self
    
    def menuItemClicked_(self, sender):
        """菜单项被点击"""
        logger.info(f"📋 菜单项被点击: {self.item_id}")
        
        # 调用点击处理器
        if self.on_click:
            try:
                self.on_click(self.item_id, sender)
            except Exception as e:
                logger.error(f"📋 菜单项点击处理器错误: {e}")


class EnhancedDatePickerDelegate(NSObject):
    """增强的 DatePicker 委托类，处理日期时间变更事件"""
    
    def init(self):
        self = objc.super(EnhancedDatePickerDelegate, self).init()
        if self is None:
            return None
            
        self.signal = None
        self.on_change = None
        
        logger.info("📅 DatePicker委托对象已初始化")
        return self
    
    def datePickerCell_dateChanged_(self, cell, date):
        """日期选择器日期变更"""
        logger.info(f"📅 DatePicker日期变更: {date}")
        
        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = date
            
        # 调用变更处理器
        if self.on_change:
            try:
                self.on_change(date)
            except Exception as e:
                logger.error(f"📅 日期变更处理器错误: {e}")
    
    def controlTextDidChange_(self, notification):
        """文本输入模式的日期变更"""
        date_picker = notification.object()
        date = date_picker.dateValue()
        
        logger.info(f"📅 DatePicker文本日期变更: {date}")
        
        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = date
            
        # 调用变更处理器
        if self.on_change:
            try:
                self.on_change(date)
            except Exception as e:
                logger.error(f"📅 文本日期变更处理器错误: {e}")


class EnhancedTabViewDelegate(NSObject):
    """增强的 TabView 委托类，处理标签页切换事件"""
    
    def init(self):
        self = objc.super(EnhancedTabViewDelegate, self).init()
        if self is None:
            return None
            
        self.signal = None
        self.on_change = None
        
        logger.info("📑 TabView委托对象已初始化")
        return self
    
    def tabView_didSelectTabViewItem_(self, tab_view, tab_item):
        """标签页选择发生变化"""
        selected_index = tab_view.indexOfTabViewItem_(tab_item)
        logger.info(f"📑 TabView标签页切换: 索引{selected_index}")
        
        # 更新信号
        if self.signal and hasattr(self.signal, "value"):
            self.signal.value = selected_index
            
        # 调用变更处理器
        if self.on_change:
            try:
                self.on_change(selected_index, tab_item)
            except Exception as e:
                logger.error(f"📑 标签页变更处理器错误: {e}")


class EnhancedSplitViewDelegate(NSObject):
    """增强的 SplitView 委托类，处理分割视图调整事件"""
    
    def init(self):
        self = objc.super(EnhancedSplitViewDelegate, self).init()
        if self is None:
            return None
            
        self.on_resize = None
        
        logger.info("📐 SplitView委托对象已初始化")
        return self
    
    def splitViewDidResizeSubviews_(self, notification):
        """分割视图子视图大小发生变化"""
        split_view = notification.object()
        logger.info("📐 SplitView子视图大小变化")
        
        # 调用调整处理器
        if self.on_resize:
            try:
                # 获取所有子视图的frame
                frames = []
                for subview in split_view.subviews():
                    frames.append(subview.frame())
                self.on_resize(frames)
            except Exception as e:
                logger.error(f"📐 分割视图调整处理器错误: {e}")


class EnhancedTableViewDataSource(NSObject):
    """增强的 TableView 数据源，处理表格数据"""
    
    def init(self):
        self = objc.super(EnhancedTableViewDataSource, self).init()
        if self is None:
            return None
            
        self.data = []
        self.columns = []
        
        logger.info("📊 TableView数据源已初始化")
        return self
    
    def numberOfRowsInTableView_(self, table_view):
        """返回表格行数 - 安全版本"""
        try:
            if not hasattr(self, 'data') or self.data is None:
                return 0
            return len(self.data)
        except Exception as e:
            logger.error(f"📊 numberOfRowsInTableView 错误: {e}")
            return 0
    
    def tableView_objectValueForTableColumn_row_(self, table_view, column, row):
        """返回指定单元格的值 - 增强错误处理"""
        try:
            # 参数验证
            if not self.data:
                return ""
            
            # 检查 row 是否为有效整数
            if row is None or not isinstance(row, int):
                logger.debug(f"📊 行索引无效: {row} (类型: {type(row)})")
                return ""
            
            if row < 0 or row >= len(self.data):
                logger.warning(f"📊 行索引超出范围: {row} >= {len(self.data)}")
                return ""
            
            # 获取行数据
            row_data = self.data[row]
            if row_data is None:
                return ""
            
            # 安全获取列标识符
            try:
                column_id = column.identifier()
                if column_id is None:
                    logger.warning("📊 列标识符为 None")
                    return ""
            except Exception as e:
                logger.error(f"📊 获取列标识符失败: {e}")
                return ""
            
            # 处理不同类型的行数据
            if isinstance(row_data, dict):
                value = row_data.get(column_id, "")
            elif isinstance(row_data, (list, tuple)):
                try:
                    col_index = int(column_id) if str(column_id).isdigit() else 0
                    value = row_data[col_index] if col_index < len(row_data) else ""
                except Exception:
                    value = ""
            else:
                value = row_data
            
            # 安全转换为字符串
            if value is None:
                return ""
            
            try:
                result = str(value)
                # 确保返回的字符串不会导致编码问题
                if isinstance(result, str):
                    return result
                else:
                    return ""
            except Exception as e:
                logger.error(f"📊 字符串转换失败: {e}, value={value}, type={type(value)}")
                return ""
                
        except Exception as e:
            logger.error(f"📊 tableView_objectValueForTableColumn_row 严重错误: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""


class EnhancedTableViewDelegate(NSObject):
    """增强的 TableView 委托类，处理表格事件"""
    
    def init(self):
        self = objc.super(EnhancedTableViewDelegate, self).init()
        if self is None:
            return None
            
        self.on_select = None
        self.on_double_click = None
        self.selected_signal = None
        
        logger.info("📊 TableView委托对象已初始化")
        return self
    
    def tableViewSelectionDidChange_(self, notification):
        """表格选择发生变化"""
        table_view = notification.object()
        selected_row = table_view.selectedRow()
        
        logger.info(f"📊 TableView选择变化: 行{selected_row}")
        
        # 更新信号
        if self.selected_signal and hasattr(self.selected_signal, "value"):
            self.selected_signal.value = selected_row
        
        # 调用选择处理器
        if self.on_select:
            try:
                self.on_select(selected_row)
            except Exception as e:
                logger.error(f"📊 表格选择处理器错误: {e}")
    
    def tableView_shouldSelectRow_(self, table_view, row):
        """是否允许选择指定行"""
        return True
    
    def tableViewDoubleClick_(self, sender):
        """表格双击事件"""
        selected_row = sender.selectedRow()
        logger.info(f"📊 TableView双击: 行{selected_row}")
        
        if self.on_double_click:
            try:
                self.on_double_click(selected_row)
            except Exception as e:
                logger.error(f"📊 表格双击处理器错误: {e}")


class EnhancedOutlineViewDataSource(NSObject):
    """增强的 OutlineView 数据源，处理树形数据"""
    
    def init(self):
        self = objc.super(EnhancedOutlineViewDataSource, self).init()
        if self is None:
            return None
            
        self.root_items = []
        self.get_children = None  # 函数，用于获取子项
        self.is_expandable = None  # 函数，用于判断是否可展开
        
        logger.info("🌳 OutlineView数据源已初始化")
        return self
    
    def outlineView_numberOfChildrenOfItem_(self, outline_view, item):
        """返回指定项的子项数量 - NSOutlineViewDataSource 必需方法"""
        try:
            logger.info(f"🌳 numberOfChildren 被调用，item: {item}")
            if item is None:
                # 根级项目
                count = len(self.root_items) if self.root_items else 0
                logger.info(f"🌳 根级项目数量: {count}")
                return count
            else:
                if self.get_children and callable(self.get_children):
                    children = self.get_children(item)
                    count = len(children) if children else 0
                    logger.info(f"🌳 项目 {item} 的子项数量: {count}")
                    return count
                else:
                    logger.warning(f"🌳 get_children 不可用或不可调用")
                    return 0
        except Exception as e:
            logger.error(f"🌳 获取子项数量错误: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def outlineView_child_ofItem_(self, outline_view, index, item):
        """返回指定项的子项 - NSOutlineViewDataSource 必需方法"""
        try:
            logger.info(f"🌳 child:ofItem 被调用，index: {index}, item: {item}")
            
            if item is None:
                # 根级项目
                if self.root_items and isinstance(self.root_items, list) and 0 <= index < len(self.root_items):
                    child = self.root_items[index]
                    logger.info(f"🌳 根级子项[{index}]: {child}")
                    return child
                else:
                    logger.warning(f"🌳 无法获取根级子项[{index}]，root_items长度: {len(self.root_items) if self.root_items else 0}")
                    return None
            else:
                if self.get_children and callable(self.get_children):
                    children = self.get_children(item)
                    if children and isinstance(children, list) and 0 <= index < len(children):
                        child = children[index]
                        logger.info(f"🌳 项目 {item} 的子项[{index}]: {child}")
                        return child
                    else:
                        logger.warning(f"🌳 无法获取子项[{index}]，children: {children}")
                        return None
                else:
                    logger.warning(f"🌳 get_children 不可用或不可调用")
                    return None
        except Exception as e:
            logger.error(f"🌳 获取子项错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def outlineView_isItemExpandable_(self, outline_view, item):
        """判断项目是否可展开 - NSOutlineViewDataSource 必需方法"""
        try:
            logger.info(f"🌳 isItemExpandable 被调用，item: {item}")
            
            if item is None:
                logger.info(f"🌳 根项目不可展开")
                return False
                
            if self.is_expandable and callable(self.is_expandable):
                result = bool(self.is_expandable(item))
                logger.info(f"🌳 项目 {item} 是否可展开 (用户函数): {result}")
                return result
            elif self.get_children and callable(self.get_children):
                children = self.get_children(item)
                result = len(children) > 0 if children else False
                logger.info(f"🌳 项目 {item} 是否可展开 (子项检查): {result}")
                return result
            else:
                logger.warning(f"🌳 无可用的展开判断函数")
                return False
        except Exception as e:
            logger.error(f"🌳 判断是否可展开错误: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def outlineView_objectValueForTableColumn_byItem_(self, outline_view, column, item):
        """返回指定单元格的值 - NSOutlineViewDataSource 必需方法"""
        try:
            logger.info(f"🌳 objectValue 被调用，column: {column}, item: {item}")
            
            if item is None:
                logger.info(f"🌳 项目为空，返回空字符串")
                return ""
            
            column_id = column.identifier() if column and hasattr(column, 'identifier') else "title"
            
            if isinstance(item, dict):
                # 优先使用列标识符，然后尝试 title，最后转换为字符串
                value = item.get(column_id)
                if value is None:
                    value = item.get('title')
                if value is None:
                    value = str(item)
                
                result = str(value) if value is not None else ""
                logger.info(f"🌳 单元格值 {column_id}: '{result}'")
                return result
            else:
                result = str(item)
                logger.info(f"🌳 单元格值（非字典）: '{result}'")
                return result
        except Exception as e:
            logger.error(f"🌳 获取单元格值错误: {e}")
            import traceback
            traceback.print_exc()
            return ""


class EnhancedOutlineViewDelegate(NSObject):
    """增强的 OutlineView 委托类，处理大纲视图事件"""
    
    def init(self):
        self = objc.super(EnhancedOutlineViewDelegate, self).init()
        if self is None:
            return None
            
        self.on_select = None
        self.on_expand = None
        self.on_collapse = None
        
        logger.info("🌳 OutlineView委托对象已初始化")
        return self
    
    def outlineViewSelectionDidChange_(self, notification):
        """大纲视图选择发生变化"""
        outline_view = notification.object()
        selected_row = outline_view.selectedRow()
        selected_item = outline_view.itemAtRow_(selected_row) if selected_row >= 0 else None
        
        logger.info(f"🌳 OutlineView选择变化: 行{selected_row}")
        
        if self.on_select:
            try:
                self.on_select(selected_row, selected_item)
            except Exception as e:
                logger.error(f"🌳 大纲视图选择处理器错误: {e}")
    
    def outlineViewItemDidExpand_(self, notification):
        """项目展开"""
        item = notification.userInfo().get("NSObject")
        logger.info(f"🌳 OutlineView项目展开: {item}")
        
        if self.on_expand:
            try:
                self.on_expand(item)
            except Exception as e:
                logger.error(f"🌳 项目展开处理器错误: {e}")
    
    def outlineViewItemDidCollapse_(self, notification):
        """项目收缩"""
        item = notification.userInfo().get("NSObject")
        logger.info(f"🌳 OutlineView项目收缩: {item}")
        
        if self.on_collapse:
            try:
                self.on_collapse(item)
            except Exception as e:
                logger.error(f"🌳 项目收缩处理器错误: {e}")
