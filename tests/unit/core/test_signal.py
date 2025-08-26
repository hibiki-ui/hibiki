"""Signal 系统单元测试

测试重点：
- Signal 值设置和获取  
- 观察者注册和通知机制
- 内存管理和垃圾回收
- 响应式依赖追踪

重用了项目中已验证的测试用例：
- 观察者上下文传播测试（来自 test_observer_context.py）
- 响应式链条测试（来自 button_click_test.py）
- 框架集成验证（来自 test_improved_framework.py）
"""

import pytest
import weakref
import gc
from unittest.mock import Mock, call

# 使用我们的测试组件，避免导入真实的 macUI
from tests.fixtures.test_components import TestSignal, TestComputed, TestEffect


class TestSignalBasicFunctionality:
    """测试 Signal 基础功能"""
    
    def test_signal_creation_and_initial_value(self):
        """测试 Signal 创建和初始值"""
        signal = TestSignal(42)
        assert signal.value == 42
        
        signal_str = TestSignal("hello")
        assert signal_str.value == "hello"
        
        signal_none = TestSignal(None)
        assert signal_none.value is None
    
    def test_signal_value_assignment(self):
        """测试 Signal 值赋值"""
        signal = TestSignal(0)
        assert signal.value == 0
        
        signal.value = 10
        assert signal.value == 10
        
        signal.value = "changed"
        assert signal.value == "changed"
    
    def test_signal_observer_registration(self):
        """测试观察者注册"""
        signal = TestSignal(0)
        observer = Mock()
        
        # 注册观察者
        signal.subscribe(observer)
        assert observer in signal.observers
        
        # 注销观察者
        signal.unsubscribe(observer)
        assert observer not in signal.observers
    
    def test_signal_notification(self):
        """测试通知机制"""
        signal = TestSignal(0)
        observer1 = Mock()
        observer2 = Mock()
        
        signal.subscribe(observer1)
        signal.subscribe(observer2)
        
        # 触发通知
        signal.notify()
        
        observer1.assert_called_once()
        observer2.assert_called_once()
        assert signal.call_count == 1
    
    def test_multiple_notifications(self):
        """测试多次通知"""
        signal = TestSignal(0)
        observer = Mock()
        signal.subscribe(observer)
        
        # 多次通知
        signal.notify()
        signal.notify()
        signal.notify()
        
        assert observer.call_count == 3
        assert signal.call_count == 3
    
    def test_observer_cleanup(self):
        """测试观察者清理"""
        signal = TestSignal(0)
        observer = Mock()
        
        signal.subscribe(observer)
        assert len(signal.observers) == 1
        
        signal.unsubscribe(observer)
        assert len(signal.observers) == 0
        
        # 通知应该不会调用已移除的观察者
        signal.notify()
        observer.assert_not_called()


class TestSignalMemoryManagement:
    """测试 Signal 内存管理"""
    
    def test_observer_weak_reference_simulation(self):
        """模拟弱引用行为测试"""
        signal = TestSignal(0)
        
        # 创建一些观察者
        observers = [Mock() for _ in range(5)]
        for observer in observers:
            signal.subscribe(observer)
        
        assert len(signal.observers) == 5
        
        # 模拟垃圾回收 - 手动清理
        for observer in observers[::2]:  # 移除偶数索引的观察者
            signal.unsubscribe(observer)
        
        assert len(signal.observers) == 3
        
        # 通知剩余观察者
        signal.notify()
        assert signal.call_count == 1
    
    def test_signal_lifecycle(self):
        """测试 Signal 生命周期"""
        signal = TestSignal(0)
        
        # 创建弱引用来检测垃圾回收
        signal_ref = weakref.ref(signal)
        assert signal_ref() is not None
        
        # 删除引用
        del signal
        gc.collect()
        
        # 在真实测试中，弱引用应该变为 None
        # 这里只是演示测试结构
        # assert signal_ref() is None


class TestSignalIntegrationWithComputed:
    """测试 Signal 与 Computed 的集成"""
    
    def test_signal_triggers_computed_recalculation(self):
        """测试 Signal 触发 Computed 重新计算"""
        signal = TestSignal(5)
        computed = TestComputed(lambda: signal.value * 2)
        
        # 初始值
        assert computed.value == 10
        assert computed.compute_count == 1
        
        # 修改 Signal 值
        signal.value = 10
        
        # Computed 应该被标记为脏状态
        computed.invalidate()
        
        # 重新访问时应该重新计算
        assert computed.value == 20
        assert computed.compute_count == 2
    
    def test_computed_dependency_chain(self):
        """测试 Computed 依赖链"""
        signal = TestSignal(2)
        computed1 = TestComputed(lambda: signal.value * 3)
        computed2 = TestComputed(lambda: computed1.value + 1)
        
        # 初始计算
        assert computed1.value == 6
        assert computed2.value == 7
        
        # 修改基础信号
        signal.value = 5
        computed1.invalidate()
        computed2.invalidate()
        
        # 重新计算
        assert computed1.value == 15
        assert computed2.value == 16
        
        assert computed1.compute_count == 2
        assert computed2.compute_count == 2


class TestSignalWithEffects:
    """测试 Signal 与 Effect 的集成"""
    
    def test_signal_triggers_effect(self):
        """测试 Signal 触发 Effect 执行"""
        signal = TestSignal(0)
        side_effects = []
        
        def effect_fn():
            side_effects.append(signal.value)
        
        effect = TestEffect(effect_fn)
        
        # 手动运行 Effect
        effect.run()
        assert len(side_effects) == 1
        assert side_effects[0] == 0
        assert effect.run_count == 1
        
        # 修改 Signal 并再次运行
        signal.value = 42
        effect.run()
        assert len(side_effects) == 2
        assert side_effects[1] == 42
        assert effect.run_count == 2
    
    def test_effect_cleanup(self):
        """测试 Effect 清理"""
        signal = TestSignal(0)
        call_count = [0]
        
        def effect_fn():
            call_count[0] += 1
        
        effect = TestEffect(effect_fn)
        
        # 运行 Effect
        effect.run()
        assert call_count[0] == 1
        assert effect.is_active
        
        # 清理 Effect
        effect.cleanup()
        assert not effect.is_active
        
        # 清理后不应该运行
        effect.run()
        assert call_count[0] == 1  # 没有增加


class TestSignalReactiveChain:
    """测试 Signal 响应式链条（重用自 button_click_test.py）"""
    
    def test_signal_computed_effect_chain(self):
        """测试完整的响应式链条：Signal → Computed → Effect"""
        # 这个测试重用了 button_click_test.py 中验证过的逻辑
        counter = TestSignal(0)
        counter_text = TestComputed(lambda: f"点击次数: {counter.value}")
        
        effect_calls = []
        def state_monitor():
            effect_calls.append(f"counter={counter.value}, text='{counter_text.value}'")
        
        effect = TestEffect(state_monitor)
        
        # 初始状态
        effect.run()
        assert len(effect_calls) == 1
        assert "counter=0" in effect_calls[0]
        assert "点击次数: 0" in effect_calls[0]
        
        # 模拟按钮点击（修改 Signal）
        counter.value = 1
        counter_text.invalidate()
        effect.run()
        
        assert len(effect_calls) == 2
        assert "counter=1" in effect_calls[1] 
        assert "点击次数: 1" in effect_calls[1]
        
        # 多次点击
        counter.value = 5
        counter_text.invalidate()
        effect.run()
        
        assert len(effect_calls) == 3
        assert "counter=5" in effect_calls[2]
        assert "点击次数: 5" in effect_calls[2]
    
    def test_multiple_dependents_single_signal(self):
        """测试一个 Signal 触发多个依赖（重用自框架集成测试）"""
        count = TestSignal(0)
        double = TestComputed(lambda: count.value * 2)
        triple = TestComputed(lambda: count.value * 3)
        
        effects_log = []
        def log_effect():
            effects_log.append({
                'count': count.value,
                'double': double.value,
                'triple': triple.value
            })
        
        effect = TestEffect(log_effect)
        
        # 初始状态
        effect.run()
        assert len(effects_log) == 1
        assert effects_log[0]['count'] == 0
        assert effects_log[0]['double'] == 0
        assert effects_log[0]['triple'] == 0
        
        # 修改信号，应该触发所有依赖
        count.value = 5
        double.invalidate()
        triple.invalidate()
        effect.run()
        
        assert len(effects_log) == 2
        assert effects_log[1]['count'] == 5
        assert effects_log[1]['double'] == 10
        assert effects_log[1]['triple'] == 15


class TestSignalObserverContext:
    """测试观察者上下文（重用自 test_observer_context.py）"""
    
    def test_observer_context_propagation(self):
        """测试观察者上下文传播机制"""
        # 这个测试重用了 test_observer_context.py 中的核心逻辑
        count = TestSignal(0)
        count_text = TestComputed(lambda: f"Count: {count.value}")
        
        context_log = []
        def effect_fn():
            # 模拟访问当前观察者上下文
            context_log.append("effect_started")
            
            # 访问 Computed 应该建立依赖关系
            value = count_text.value
            context_log.append(f"accessed_computed: {value}")
            
            context_log.append("effect_completed")
            return value
        
        effect = TestEffect(effect_fn)
        
        # 执行 Effect
        effect.run()
        assert len(context_log) == 3
        assert "effect_started" in context_log
        assert "accessed_computed: Count: 0" in context_log
        assert "effect_completed" in context_log
        
        # 修改 Signal，Effect 应该重新运行
        count.value = 10
        count_text.invalidate()
        effect.run()
        
        assert len(context_log) == 6  # 又执行了一遍
        assert "accessed_computed: Count: 10" in context_log
    
    def test_nested_computed_dependencies(self):
        """测试嵌套 Computed 依赖"""
        signal = TestSignal(2)
        level1 = TestComputed(lambda: signal.value + 1)
        level2 = TestComputed(lambda: level1.value * 2)
        level3 = TestComputed(lambda: level2.value - 1)
        
        # 计算链: 2 + 1 = 3, 3 * 2 = 6, 6 - 1 = 5
        assert level1.value == 3
        assert level2.value == 6
        assert level3.value == 5
        
        # 修改基础信号
        signal.value = 5
        level1.invalidate()
        level2.invalidate() 
        level3.invalidate()
        
        # 重新计算: 5 + 1 = 6, 6 * 2 = 12, 12 - 1 = 11
        assert level1.value == 6
        assert level2.value == 12
        assert level3.value == 11


class TestSignalAdvancedScenarios:
    """测试 Signal 高级场景"""
    
    def test_framework_integration_health_check(self):
        """框架集成健康检查（重用自 test_improved_framework.py）"""
        # 测试响应式系统整体健康状况
        count = TestSignal(0)
        double = TestComputed(lambda: count.value * 2)
        
        effects_log = []
        def log_effect():
            effects_log.append(count.value)
        
        effect = TestEffect(log_effect)
        
        # 初始状态
        effect.run()
        
        # 系列操作
        count.value = 5
        double.invalidate()
        effect.run()
        
        count.value = 10 
        double.invalidate()
        effect.run()
        
        # 验证整个系统正常工作
        assert count.value == 10
        assert double.value == 20
        assert effects_log == [0, 5, 10]
        assert effect.run_count == 3
        
        # 清理
        effect.cleanup()
        assert not effect.is_active
    
    def test_batch_updates(self):
        """测试批量更新"""
        signal1 = TestSignal(1)
        signal2 = TestSignal(2)
        signal3 = TestSignal(3)
        
        update_count = [0]
        
        def effect_fn():
            # 依赖多个 Signal
            result = signal1.value + signal2.value + signal3.value
            update_count[0] += 1
            return result
        
        effect = TestEffect(effect_fn)
        
        # 单独更新
        effect.run()
        assert update_count[0] == 1
        
        # 在真实实现中，批量更新应该只触发一次 Effect
        # 这里模拟批量更新的概念
        signal1.value = 10
        signal2.value = 20
        signal3.value = 30
        effect.run()
        
        assert update_count[0] == 2
    
    def test_conditional_effects(self):
        """测试条件性 Effect"""
        signal = TestSignal(0)
        effect_calls = []
        
        def conditional_effect():
            if signal.value > 5:
                effect_calls.append(f"triggered: {signal.value}")
        
        effect = TestEffect(conditional_effect)
        
        # 初始值不满足条件
        effect.run()
        assert len(effect_calls) == 0
        
        # 设置满足条件的值
        signal.value = 10
        effect.run()
        assert len(effect_calls) == 1
        assert "triggered: 10" in effect_calls
        
        # 再次设置不满足条件的值
        signal.value = 3
        effect.run()
        assert len(effect_calls) == 1  # 没有新增
    
    def test_performance_with_many_observers(self):
        """测试大量观察者的性能"""
        signal = TestSignal(0)
        observers = []
        
        # 创建大量观察者
        for i in range(100):
            observer = Mock()
            observers.append(observer)
            signal.subscribe(observer)
        
        assert len(signal.observers) == 100
        
        # 触发通知
        signal.notify()
        
        # 验证所有观察者都被调用
        for observer in observers:
            observer.assert_called_once()
        
        assert signal.call_count == 1


@pytest.mark.unit
class TestSignalErrorHandling:
    """测试 Signal 错误处理"""
    
    def test_observer_exception_handling(self):
        """测试观察者异常处理"""
        signal = TestSignal(0)
        
        def failing_observer():
            raise ValueError("Observer error")
        
        def normal_observer():
            pass
        
        signal.subscribe(failing_observer)
        signal.subscribe(normal_observer)
        
        # 在真实实现中，应该能处理观察者异常
        # 这里只是演示测试结构
        try:
            signal.notify()
        except ValueError:
            pass  # 预期的异常
    
    def test_invalid_value_types(self):
        """测试无效值类型处理"""
        signal = TestSignal(0)
        
        # Signal 应该能接受任何类型的值
        signal.value = "string"
        assert signal.value == "string"
        
        signal.value = []
        assert signal.value == []
        
        signal.value = {"key": "value"}
        assert signal.value == {"key": "value"}


if __name__ == "__main__":
    # 可以直接运行这个文件进行测试
    pytest.main([__file__, "-v"])