"""测试用组件和辅助函数

包含用于测试的简单组件实例和常用测试辅助函数。
"""

from typing import Any, List
from unittest.mock import MagicMock


class TestSignal:
    """测试用的简单 Signal 实现"""
    
    def __init__(self, value):
        self.value = value
        self.observers = set()
        self.call_count = 0
        
    def subscribe(self, observer):
        self.observers.add(observer)
        
    def unsubscribe(self, observer):
        self.observers.discard(observer)
        
    def notify(self):
        self.call_count += 1
        for observer in self.observers:
            if callable(observer):
                observer()


class TestComputed:
    """测试用的简单 Computed 实现"""
    
    def __init__(self, compute_fn):
        self.compute_fn = compute_fn
        self._cached_value = None
        self._is_dirty = True
        self.compute_count = 0
        
    @property
    def value(self):
        if self._is_dirty:
            self._cached_value = self.compute_fn()
            self._is_dirty = False
            self.compute_count += 1
        return self._cached_value
        
    def invalidate(self):
        self._is_dirty = True


class TestEffect:
    """测试用的简单 Effect 实现"""
    
    def __init__(self, effect_fn):
        self.effect_fn = effect_fn
        self.run_count = 0
        self.is_active = True
        
    def run(self):
        if self.is_active:
            self.run_count += 1
            return self.effect_fn()
            
    def cleanup(self):
        self.is_active = False


class MockComponent:
    """测试用的 Mock 组件"""
    
    def __init__(self, name="MockComponent"):
        self.name = name
        self.signals = {}
        self.computed_values = {}
        self.effects = []
        self.mounted = False
        self.view = None
        
    def create_signal(self, initial_value):
        signal = TestSignal(initial_value)
        self.signals[len(self.signals)] = signal
        return signal
        
    def create_computed(self, compute_fn):
        computed = TestComputed(compute_fn)
        self.computed_values[len(self.computed_values)] = computed
        return computed
        
    def create_effect(self, effect_fn):
        effect = TestEffect(effect_fn)
        self.effects.append(effect)
        return effect
        
    def mount(self):
        self.mounted = True
        return MagicMock()  # Mock view
        
    def unmount(self):
        self.mounted = False
        for effect in self.effects:
            effect.cleanup()


def create_mock_button(**kwargs):
    """创建用于测试的 Mock 按钮"""
    from .mock_pyobjc import MockNSButton
    
    button = MockNSButton()
    
    # 设置默认属性
    if 'title' in kwargs:
        button.setTitle_(kwargs['title'])
    if 'enabled' in kwargs:
        button.setEnabled_(kwargs['enabled'])
    if 'tooltip' in kwargs:
        button.setToolTip_(kwargs['tooltip'])
        
    return button


def create_mock_label(**kwargs):
    """创建用于测试的 Mock 标签"""
    from .mock_pyobjc import MockNSTextField
    
    label = MockNSTextField()
    label.setEditable_(False)
    label.setSelectable_(False)
    label.setBezeled_(False)
    label.setDrawsBackground_(False)
    
    # 设置默认属性
    if 'text' in kwargs:
        label.setStringValue_(kwargs['text'])
        
    return label


def create_test_component_tree():
    """创建测试用的组件树结构"""
    root = MockComponent("Root")
    child1 = MockComponent("Child1")
    child2 = MockComponent("Child2")
    grandchild = MockComponent("GrandChild")
    
    # 建立层次关系
    root.children = [child1, child2]
    child1.children = [grandchild]
    child2.children = []
    grandchild.children = []
    
    # 设置父级关系
    child1.parent = root
    child2.parent = root
    grandchild.parent = child1
    
    return root


def assert_signal_value(signal, expected_value, message=""):
    """断言 Signal 的值"""
    actual = signal.value
    assert actual == expected_value, f"{message}Expected {expected_value}, got {actual}"


def assert_computed_value(computed, expected_value, message=""):
    """断言 Computed 的值"""
    actual = computed.value
    assert actual == expected_value, f"{message}Expected {expected_value}, got {actual}"


def assert_effect_run_count(effect, expected_count, message=""):
    """断言 Effect 的执行次数"""
    actual = effect.run_count
    assert actual == expected_count, f"{message}Expected {expected_count} runs, got {actual}"


def capture_reactive_chain():
    """捕获响应式链条的执行记录"""
    
    class ReactiveChainCapture:
        def __init__(self):
            self.signal_changes = []
            self.computed_recalculations = []
            self.effect_runs = []
            
        def record_signal_change(self, signal, old_value, new_value):
            self.signal_changes.append({
                'signal': signal,
                'old_value': old_value,
                'new_value': new_value,
                'timestamp': len(self.signal_changes)
            })
            
        def record_computed_recalculation(self, computed, new_value):
            self.computed_recalculations.append({
                'computed': computed,
                'new_value': new_value,
                'timestamp': len(self.computed_recalculations)
            })
            
        def record_effect_run(self, effect):
            self.effect_runs.append({
                'effect': effect,
                'timestamp': len(self.effect_runs)
            })
            
        def get_execution_order(self):
            """获取执行顺序"""
            all_events = []
            
            for change in self.signal_changes:
                all_events.append(('signal', change))
                
            for recalc in self.computed_recalculations:
                all_events.append(('computed', recalc))
                
            for run in self.effect_runs:
                all_events.append(('effect', run))
                
            # 按时间戳排序
            all_events.sort(key=lambda x: x[1]['timestamp'])
            return all_events
    
    return ReactiveChainCapture()


class MockEventTarget:
    """Mock 事件目标，用于测试事件处理"""
    
    def __init__(self):
        self.events = []
        self.handlers = {}
        
    def add_handler(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        
    def trigger_event(self, event_type, *args, **kwargs):
        event = {
            'type': event_type,
            'args': args,
            'kwargs': kwargs,
            'timestamp': len(self.events)
        }
        self.events.append(event)
        
        # 调用处理器
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    event['handler_error'] = str(e)
        
        return event
    
    def get_events(self, event_type=None):
        """获取事件列表"""
        if event_type is None:
            return self.events
        return [e for e in self.events if e['type'] == event_type]
    
    def clear_events(self):
        """清除事件记录"""
        self.events.clear()


def create_mock_reactive_system():
    """创建一个完整的 Mock 响应式系统用于测试"""
    
    class MockReactiveSystem:
        def __init__(self):
            self.signals = []
            self.computed_values = []
            self.effects = []
            self.update_queue = []
            
        def create_signal(self, initial_value):
            signal = TestSignal(initial_value)
            self.signals.append(signal)
            return signal
            
        def create_computed(self, compute_fn):
            computed = TestComputed(compute_fn)
            self.computed_values.append(computed)
            return computed
            
        def create_effect(self, effect_fn):
            effect = TestEffect(effect_fn)
            self.effects.append(effect)
            return effect
            
        def flush_updates(self):
            """处理待更新队列"""
            while self.update_queue:
                update = self.update_queue.pop(0)
                update()
                
        def cleanup(self):
            """清理所有资源"""
            for effect in self.effects:
                effect.cleanup()
            self.signals.clear()
            self.computed_values.clear()
            self.effects.clear()
            self.update_queue.clear()
    
    return MockReactiveSystem()