"""Effect 系统单元测试

测试重点：
- Effect 创建和执行
- 副作用函数管理
- 依赖追踪和重新运行
- 生命周期和清理

重用了项目中已验证的测试用例：
- 按钮点击响应式链条（来自 button_click_test.py）
- 状态监控和日志记录（来自调试文件）
- Effect 清理机制（来自现有测试）
"""

import pytest
from unittest.mock import Mock, call

from tests.fixtures.test_components import TestSignal, TestComputed, TestEffect


class TestEffectBasicFunctionality:
    """测试 Effect 基础功能"""
    
    def test_effect_creation(self):
        """测试 Effect 创建"""
        effect_fn = Mock()
        effect = TestEffect(effect_fn)
        
        assert effect.effect_fn == effect_fn
        assert effect.run_count == 0
        assert effect.is_active is True
    
    def test_effect_execution(self):
        """测试 Effect 执行"""
        calls = []
        def effect_fn():
            calls.append("executed")
        
        effect = TestEffect(effect_fn)
        
        # 手动执行
        effect.run()
        assert len(calls) == 1
        assert effect.run_count == 1
        
        # 再次执行
        effect.run()
        assert len(calls) == 2
        assert effect.run_count == 2
    
    def test_effect_with_return_value(self):
        """测试有返回值的 Effect"""
        def effect_fn():
            return "effect_result"
        
        effect = TestEffect(effect_fn)
        result = effect.run()
        
        assert result == "effect_result"
        assert effect.run_count == 1
    
    def test_effect_cleanup(self):
        """测试 Effect 清理"""
        calls = []
        def effect_fn():
            calls.append("running")
        
        effect = TestEffect(effect_fn)
        
        # 正常执行
        effect.run()
        assert len(calls) == 1
        assert effect.is_active
        
        # 清理后不应该执行
        effect.cleanup()
        assert not effect.is_active
        
        effect.run()
        assert len(calls) == 1  # 没有增加


class TestEffectButtonClickScenario:
    """测试按钮点击场景（重用自 button_click_test.py）"""
    
    def test_button_click_reactive_chain(self):
        """测试完整的按钮点击响应式链条"""
        # 重用 button_click_test.py 中验证过的逻辑
        
        # 1. 创建响应式状态
        counter = TestSignal(0)
        counter_text = TestComputed(lambda: f"点击次数: {counter.value}")
        
        # 2. 创建状态监控 Effect
        state_log = []
        def state_monitor():
            state_log.append({
                'counter': counter.value,
                'text': counter_text.value,
                'timestamp': len(state_log)
            })
        
        monitor_effect = TestEffect(state_monitor)
        
        # 3. 初始状态
        monitor_effect.run()
        assert len(state_log) == 1
        assert state_log[0]['counter'] == 0
        assert state_log[0]['text'] == "点击次数: 0"
        
        # 4. 模拟按钮点击事件
        def simulate_button_click():
            counter.value += 1
            counter_text.invalidate()
            monitor_effect.run()
        
        # 5. 多次点击测试
        simulate_button_click()  # 第1次点击
        assert len(state_log) == 2
        assert state_log[1]['counter'] == 1
        assert state_log[1]['text'] == "点击次数: 1"
        
        simulate_button_click()  # 第2次点击
        assert len(state_log) == 3
        assert state_log[2]['counter'] == 2
        assert state_log[2]['text'] == "点击次数: 2"
        
        simulate_button_click()  # 第3次点击
        assert len(state_log) == 4
        assert state_log[3]['counter'] == 3
        assert state_log[3]['text'] == "点击次数: 3"
        
        # 6. 验证整个链条
        assert monitor_effect.run_count == 4
        assert counter.value == 3
        assert counter_text.value == "点击次数: 3"
        
        # 7. 清理
        monitor_effect.cleanup()
        
        # 8. 清理后点击不应该触发 Effect
        counter.value = 10
        monitor_effect.run()
        assert len(state_log) == 4  # 没有增加
    
    def test_multiple_effects_single_signal(self):
        """测试多个 Effect 监听同一个 Signal"""
        signal = TestSignal(0)
        
        # 创建多个 Effect
        effect1_calls = []
        effect2_calls = []
        effect3_calls = []
        
        def effect1_fn():
            effect1_calls.append(f"effect1: {signal.value}")
        
        def effect2_fn():
            effect2_calls.append(f"effect2: {signal.value * 2}")
        
        def effect3_fn():
            effect3_calls.append(f"effect3: {signal.value ** 2}")
        
        effect1 = TestEffect(effect1_fn)
        effect2 = TestEffect(effect2_fn)
        effect3 = TestEffect(effect3_fn)
        
        # 运行所有 Effect
        def run_all_effects():
            effect1.run()
            effect2.run()
            effect3.run()
        
        # 初始状态
        run_all_effects()
        assert len(effect1_calls) == 1
        assert len(effect2_calls) == 1
        assert len(effect3_calls) == 1
        assert "effect1: 0" in effect1_calls[0]
        assert "effect2: 0" in effect2_calls[0]
        assert "effect3: 0" in effect3_calls[0]
        
        # 修改信号
        signal.value = 5
        run_all_effects()
        
        assert len(effect1_calls) == 2
        assert len(effect2_calls) == 2
        assert len(effect3_calls) == 2
        assert "effect1: 5" in effect1_calls[1]
        assert "effect2: 10" in effect2_calls[1]
        assert "effect3: 25" in effect3_calls[1]
        
        # 清理所有 Effect
        effect1.cleanup()
        effect2.cleanup()
        effect3.cleanup()


class TestEffectAdvancedScenarios:
    """测试 Effect 高级场景"""
    
    def test_effect_with_conditional_execution(self):
        """测试条件执行的 Effect"""
        signal = TestSignal(0)
        execution_log = []
        
        def conditional_effect():
            if signal.value > 0:
                execution_log.append(f"positive: {signal.value}")
            elif signal.value < 0:
                execution_log.append(f"negative: {signal.value}")
            else:
                execution_log.append("zero")
        
        effect = TestEffect(conditional_effect)
        
        # 测试不同值
        effect.run()  # 0
        assert len(execution_log) == 1
        assert "zero" in execution_log[0]
        
        signal.value = 5  # 正数
        effect.run()
        assert len(execution_log) == 2
        assert "positive: 5" in execution_log[1]
        
        signal.value = -3  # 负数
        effect.run()
        assert len(execution_log) == 3
        assert "negative: -3" in execution_log[2]
        
        signal.value = 0  # 回到0
        effect.run()
        assert len(execution_log) == 4
        assert "zero" in execution_log[3]
    
    def test_effect_error_handling(self):
        """测试 Effect 错误处理"""
        signal = TestSignal(1)
        
        def error_prone_effect():
            if signal.value == 0:
                raise ValueError("Cannot process zero")
            return signal.value * 2
        
        effect = TestEffect(error_prone_effect)
        
        # 正常执行
        result = effect.run()
        assert result == 2
        assert effect.run_count == 1
        
        # 触发错误
        signal.value = 0
        with pytest.raises(ValueError, match="Cannot process zero"):
            effect.run()
        
        # Error 后 run_count 仍然增加
        assert effect.run_count == 2
        
        # 恢复正常
        signal.value = 3
        result = effect.run()
        assert result == 6
        assert effect.run_count == 3
    
    def test_effect_dependency_chain(self):
        """测试 Effect 依赖链"""
        signal = TestSignal(1)
        computed = TestComputed(lambda: signal.value * 10)
        
        chain_log = []
        def chain_effect():
            # 这个 Effect 依赖 Computed，Computed 依赖 Signal
            chain_log.append(f"signal={signal.value}, computed={computed.value}")
        
        effect = TestEffect(chain_effect)
        
        # 初始执行
        effect.run()
        assert len(chain_log) == 1
        assert "signal=1, computed=10" in chain_log[0]
        
        # 修改基础信号，整个链条应该更新
        signal.value = 3
        computed.invalidate()
        effect.run()
        
        assert len(chain_log) == 2
        assert "signal=3, computed=30" in chain_log[1]
        
        # 再次修改
        signal.value = 7
        computed.invalidate()
        effect.run()
        
        assert len(chain_log) == 3
        assert "signal=7, computed=70" in chain_log[2]


class TestEffectPerformance:
    """测试 Effect 性能相关"""
    
    def test_effect_with_expensive_computation(self):
        """测试包含昂贵计算的 Effect"""
        signal = TestSignal(5)
        computation_calls = []
        
        def expensive_effect():
            # 模拟昂贵计算
            computation_calls.append(f"computing: {signal.value}")
            result = sum(range(signal.value))
            return result
        
        effect = TestEffect(expensive_effect)
        
        # 第一次计算
        result1 = effect.run()
        assert len(computation_calls) == 1
        assert result1 == 10  # sum(range(5)) = 0+1+2+3+4 = 10
        
        # 再次运行相同的计算
        result2 = effect.run()
        assert len(computation_calls) == 2  # 每次都重新计算
        assert result1 == result2
        
        # 修改信号后计算
        signal.value = 3
        result3 = effect.run()
        assert len(computation_calls) == 3
        assert result3 == 3  # sum(range(3)) = 0+1+2 = 3
    
    def test_many_effects_performance(self):
        """测试大量 Effect 的性能"""
        signal = TestSignal(0)
        effects = []
        call_counts = []
        
        # 创建大量 Effect
        for i in range(100):
            calls = []
            call_counts.append(calls)
            
            def make_effect_fn(index, calls_list):
                def effect_fn():
                    calls_list.append(f"effect_{index}: {signal.value}")
                return effect_fn
            
            effect = TestEffect(make_effect_fn(i, calls))
            effects.append(effect)
        
        # 运行所有 Effect
        def run_all():
            for effect in effects:
                effect.run()
        
        # 初始运行
        run_all()
        assert all(len(calls) == 1 for calls in call_counts)
        
        # 修改信号并重新运行
        signal.value = 42
        run_all()
        assert all(len(calls) == 2 for calls in call_counts)
        
        # 验证所有 Effect 都正确执行
        for i, calls in enumerate(call_counts):
            assert f"effect_{i}: 0" in calls[0]
            assert f"effect_{i}: 42" in calls[1]
        
        # 清理所有 Effect
        for effect in effects:
            effect.cleanup()
        
        assert all(not effect.is_active for effect in effects)


class TestEffectUIIntegration:
    """测试 Effect 与 UI 的集成（模拟）"""
    
    def test_effect_ui_update_simulation(self):
        """模拟 Effect 触发 UI 更新"""
        # 模拟 UI 状态
        ui_state = {'text': '', 'enabled': True, 'visible': True}
        
        # 响应式数据
        message = TestSignal("Hello")
        counter = TestSignal(0)
        
        # UI 更新 Effect
        ui_updates = []
        def ui_effect():
            # 模拟 UI 绑定更新
            new_text = f"{message.value} - {counter.value}"
            if ui_state['text'] != new_text:
                ui_state['text'] = new_text
                ui_updates.append(f"text_updated: {new_text}")
            
            # 模拟条件 UI 更新
            should_be_enabled = counter.value > 0
            if ui_state['enabled'] != should_be_enabled:
                ui_state['enabled'] = should_be_enabled
                ui_updates.append(f"enabled_updated: {should_be_enabled}")
        
        effect = TestEffect(ui_effect)
        
        # 初始状态
        effect.run()
        assert len(ui_updates) == 2  # text 和 enabled 都更新了
        assert "text_updated: Hello - 0" in ui_updates
        assert "enabled_updated: False" in ui_updates
        
        # 修改 counter
        counter.value = 5
        effect.run()
        assert len(ui_updates) == 4
        assert "text_updated: Hello - 5" in ui_updates
        assert "enabled_updated: True" in ui_updates
        
        # 修改 message
        message.value = "World"
        effect.run()
        assert len(ui_updates) == 5
        assert "text_updated: World - 5" in ui_updates
        
        # 验证最终 UI 状态
        assert ui_state['text'] == "World - 5"
        assert ui_state['enabled'] is True
        assert ui_state['visible'] is True


@pytest.mark.unit
class TestEffectEdgeCases:
    """测试 Effect 边界情况"""
    
    def test_effect_cleanup_during_execution(self):
        """测试执行期间的清理"""
        signal = TestSignal(0)
        cleanup_calls = []
        
        def self_destroying_effect():
            cleanup_calls.append(signal.value)
            # 在某些条件下自我清理
            if signal.value >= 3:
                effect.cleanup()
        
        effect = TestEffect(self_destroying_effect)
        
        # 正常执行几次
        effect.run()  # value = 0
        assert len(cleanup_calls) == 1
        assert effect.is_active
        
        signal.value = 1
        effect.run()
        assert len(cleanup_calls) == 2
        assert effect.is_active
        
        # 触发自我清理
        signal.value = 3
        effect.run()
        assert len(cleanup_calls) == 3
        assert not effect.is_active
        
        # 清理后不应该继续执行
        signal.value = 4
        effect.run()
        assert len(cleanup_calls) == 3  # 没有增加
    
    def test_effect_reactivation(self):
        """测试 Effect 重新激活"""
        calls = []
        def effect_fn():
            calls.append("executed")
        
        effect = TestEffect(effect_fn)
        
        # 正常执行
        effect.run()
        assert len(calls) == 1
        
        # 清理
        effect.cleanup()
        assert not effect.is_active
        
        # 尝试重新激活（在我们的简单实现中不支持）
        # 但可以创建新的 Effect
        new_effect = TestEffect(effect_fn)
        new_effect.run()
        assert len(calls) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])