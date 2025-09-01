"""
Tests for the Reactive System
=============================

Comprehensive testing of Signal, Computed, and Effect classes.
Tests the Reaktiv-inspired optimizations including version control,
batch processing, and smart dependency tracking.
"""

import pytest
from unittest.mock import MagicMock, call
from hibiki.ui.core.reactive import Signal, Computed, Effect, batch


class TestSignal:
    """Test the Signal class."""
    
    def test_signal_creation_and_value(self):
        """Test creating a signal and accessing its value."""
        signal = Signal(42)
        assert signal.value == 42
        
        signal.value = 100
        assert signal.value == 100
    
    def test_signal_version_increments(self):
        """Test that signal version increments on updates."""
        signal = Signal(0)
        initial_version = signal._version
        
        signal.value = 1
        assert signal._version == initial_version + 1
        
        signal.value = 2
        assert signal._version == initial_version + 2
    
    def test_signal_same_value_no_version_change(self):
        """Test that setting the same value doesn't increment version."""
        signal = Signal(42)
        initial_version = signal._version
        
        signal.value = 42  # Same value
        assert signal._version == initial_version
    
    def test_signal_subscriber_notification(self):
        """Test that subscribers are notified of changes."""
        signal = Signal(0)
        subscriber = MagicMock()
        
        # Mock the expected methods
        subscriber._needs_update = MagicMock(return_value=True)
        subscriber._active = True
        
        signal._observers.add(subscriber)
        signal.value = 1
        
        # Check that _needs_update was called
        subscriber._needs_update.assert_called_with(signal)
    
    def test_signal_multiple_subscribers(self):
        """Test multiple subscribers are all notified."""
        signal = Signal(0)
        subscriber1 = MagicMock()
        subscriber2 = MagicMock()
        
        # Mock the expected methods
        subscriber1._needs_update = MagicMock(return_value=True)
        subscriber1._active = True
        subscriber2._needs_update = MagicMock(return_value=True)
        subscriber2._active = True
        
        signal._observers.add(subscriber1)
        signal._observers.add(subscriber2)
        
        signal.value = 1
        
        subscriber1._needs_update.assert_called_with(signal)
        subscriber2._needs_update.assert_called_with(signal)
    
    def test_signal_repr(self):
        """Test string representation of Signal."""
        signal = Signal(42)
        assert "Signal(value=42" in repr(signal)


class TestComputed:
    """Test the Computed class."""
    
    def test_computed_basic_calculation(self):
        """Test basic computed value calculation."""
        count = Signal(5)
        double = Computed(lambda: count.value * 2)
        
        assert double.value == 10
        
        count.value = 7
        assert double.value == 14
    
    def test_computed_caching(self):
        """Test that computed values are cached."""
        count = Signal(5)
        call_count = 0
        
        def expensive_computation():
            nonlocal call_count
            call_count += 1
            return count.value * 2
        
        computed = Computed(expensive_computation)
        
        # First access computes
        assert computed.value == 10
        assert call_count == 1
        
        # Second access uses cache
        assert computed.value == 10
        assert call_count == 1
        
        # Signal change invalidates cache
        count.value = 7
        assert computed.value == 14
        assert call_count == 2
    
    def test_computed_dependency_tracking(self):
        """Test that computed tracks its dependencies."""
        a = Signal(1)
        b = Signal(2)
        
        sum_computed = Computed(lambda: a.value + b.value)
        
        assert sum_computed.value == 3
        # Dependencies are tracked internally during computation
        # We can verify by checking that changes trigger updates
        initial_value = sum_computed.value
        a.value = 2
        assert sum_computed.value == 4  # Recomputed
    
    def test_computed_chaining(self):
        """Test chained computed values."""
        base = Signal(10)
        double = Computed(lambda: base.value * 2)
        quadruple = Computed(lambda: double.value * 2)
        
        assert quadruple.value == 40
        
        base.value = 5
        assert double.value == 10
        assert quadruple.value == 20
    
    def test_computed_conditional_dependencies(self):
        """Test computed with conditional dependency access."""
        flag = Signal(True)
        a = Signal(10)
        b = Signal(20)
        
        conditional = Computed(lambda: a.value if flag.value else b.value)
        
        assert conditional.value == 10
        # Verify conditional dependencies work
        assert conditional.value == 10
        # b should not be a dependency when flag is True
        
        flag.value = False
        assert conditional.value == 20
        # b should now be a dependency
        assert conditional.value == 20
    
    def test_computed_version_tracking(self):
        """Test version-based cache invalidation."""
        signal = Signal(1)
        computed = Computed(lambda: signal.value * 2)
        
        # Initial computation
        assert computed.value == 2
        # Version tracking is internal
        initial_value = computed.value
        
        # Signal update changes version
        signal.value = 2
        assert computed.value == 4
        # Value should be recomputed
        assert computed.value == 4
    
    def test_computed_cleanup(self):
        """Test computed cleanup removes from dependencies."""
        signal = Signal(1)
        computed = Computed(lambda: signal.value * 2)
        
        # Access value to establish dependency
        _ = computed.value
        
        # Verify subscription
        assert computed in signal._observers
        
        # Cleanup
        computed.cleanup()
        assert computed not in signal._observers


class TestEffect:
    """Test the Effect class."""
    
    def test_effect_basic_execution(self):
        """Test that effects execute immediately and on changes."""
        signal = Signal(0)
        executions = []
        
        effect = Effect(lambda: executions.append(signal.value))
        
        # Should execute immediately
        assert executions == [0]
        
        signal.value = 1
        assert executions == [0, 1]
        
        signal.value = 2
        assert executions == [0, 1, 2]
    
    def test_effect_cleanup_function(self):
        """Test effect cleanup function is called."""
        signal = Signal(0)
        cleanups = []
        
        def effect_with_cleanup():
            value = signal.value
            cleanups.append(f"setup_{value}")
            return lambda: cleanups.append(f"cleanup_{value}")
        
        effect = Effect(effect_with_cleanup)
        
        assert cleanups == ["setup_0"]
        
        signal.value = 1
        assert cleanups == ["setup_0", "cleanup_0", "setup_1"]
        
        effect.cleanup()
        assert cleanups == ["setup_0", "cleanup_0", "setup_1", "cleanup_1"]
    
    def test_effect_dependency_tracking(self):
        """Test that effects track their dependencies."""
        a = Signal(1)
        b = Signal(2)
        sum_value = 0
        
        def update_sum():
            nonlocal sum_value
            sum_value = a.value + b.value
        
        effect = Effect(update_sum)
        
        assert sum_value == 3
        # Effects track dependencies internally
        # Verify by checking that changes trigger updates
        
        a.value = 5
        assert sum_value == 7
    
    def test_effect_error_handling(self):
        """Test that effect errors don't break the reactive system."""
        signal = Signal(0)
        executions = []
        
        def effect_with_error():
            executions.append(signal.value)
            if signal.value == 1:
                raise ValueError("Test error")
        
        effect = Effect(effect_with_error)
        assert executions == [0]
        
        # Error shouldn't prevent future executions
        signal.value = 1  # This will raise an error
        signal.value = 2  # This should still execute
        
        assert 2 in executions
    
    def test_effect_cleanup_on_rerun(self):
        """Test that cleanup is called before each re-run."""
        signal = Signal(0)
        cleanup_calls = []
        
        def effect_fn():
            current = signal.value
            return lambda: cleanup_calls.append(current)
        
        effect = Effect(effect_fn)
        
        signal.value = 1
        assert cleanup_calls == [0]  # Cleanup for value 0
        
        signal.value = 2
        assert cleanup_calls == [0, 1]  # Cleanup for values 0 and 1


class TestBatchProcessing:
    """Test batch processing functionality."""
    
    def test_batch_updates(self):
        """Test that batch prevents multiple updates."""
        signal1 = Signal(0)
        signal2 = Signal(0)
        executions = []
        
        effect = Effect(lambda: executions.append((signal1.value, signal2.value)))
        executions.clear()  # Clear initial execution
        
        with batch():
            signal1.value = 1
            signal2.value = 2
            # Effect should not run yet
            assert executions == []
        
        # Effect runs once after batch
        assert executions == [(1, 2)]
    
    def test_batch_deduplication(self):
        """Test that batch deduplicates updates."""
        signal = Signal(0)
        executions = []
        
        effect = Effect(lambda: executions.append(signal.value))
        executions.clear()
        
        with batch():
            signal.value = 1
            signal.value = 2
            signal.value = 3
        
        # Should only execute once with final value
        assert executions == [3]
    
    def test_nested_batch(self):
        """Test nested batch operations."""
        signal = Signal(0)
        executions = []
        
        effect = Effect(lambda: executions.append(signal.value))
        executions.clear()
        
        with batch():
            signal.value = 1
            with batch():
                signal.value = 2
            # Still in outer batch
            assert executions == []
        
        # Executes after outer batch
        assert executions == [2]
    
    def test_batch_with_computed(self):
        """Test batch with computed values."""
        a = Signal(1)
        b = Signal(2)
        sum_computed = Computed(lambda: a.value + b.value)
        results = []
        
        effect = Effect(lambda: results.append(sum_computed.value))
        results.clear()
        
        with batch():
            a.value = 5
            b.value = 10
        
        # Should compute once with final values
        assert results == [15]


class TestCircularDependencies:
    """Test circular dependency detection and handling."""
    
    def test_computed_self_reference_detection(self):
        """Test that self-referencing computed is detected."""
        # This should ideally raise an error or handle gracefully
        signal = Signal(1)
        
        def circular_fn():
            # Accessing computed.value inside its own computation
            return signal.value + (computed.value if hasattr(computed, '_cached_value') else 0)
        
        computed = Computed(circular_fn)
        
        # Should handle gracefully without infinite recursion
        value = computed.value
        assert value == 1  # Initial value without self-reference
    
    def test_effect_modifying_dependency(self):
        """Test effect that modifies its own dependency."""
        counter = Signal(0)
        max_iterations = 10
        iteration_count = 0
        
        def incrementing_effect():
            nonlocal iteration_count
            iteration_count += 1
            current_value = counter.value
            # Only increment on first execution to avoid infinite loop
            if iteration_count == 1 and current_value < 5:
                # Use batch to prevent immediate re-execution
                with batch():
                    counter.value = current_value + 1
        
        effect = Effect(incrementing_effect)
        
        # Should execute twice: initial and after the update
        assert counter.value == 1
        assert iteration_count == 2  # Initial execution + one update


class TestMemoryManagement:
    """Test memory management and cleanup."""
    
    def test_signal_cleanup_removes_subscribers(self):
        """Test that signal cleanup removes all subscribers."""
        signal = Signal(0)
        computed1 = Computed(lambda: signal.value * 2)
        computed2 = Computed(lambda: signal.value * 3)
        
        # Access values to establish dependencies
        _ = computed1.value
        _ = computed2.value
        
        assert len(signal._observers) == 2
        
        computed1.cleanup()
        assert len(signal._observers) == 1
        
        computed2.cleanup()
        assert len(signal._observers) == 0
    
    def test_effect_cleanup_removes_from_dependencies(self):
        """Test that effect cleanup removes from all dependencies."""
        signal1 = Signal(1)
        signal2 = Signal(2)
        
        effect = Effect(lambda: signal1.value + signal2.value)
        
        assert effect in signal1._observers
        assert effect in signal2._observers
        
        effect.cleanup()
        
        assert effect not in signal1._observers
        assert effect not in signal2._observers
    
    def test_computed_cleanup_chain(self):
        """Test cleanup in a chain of computed values."""
        base = Signal(1)
        double = Computed(lambda: base.value * 2)
        quadruple = Computed(lambda: double.value * 2)
        
        # Access values to establish dependencies
        _ = double.value
        _ = quadruple.value
        
        assert double in base._observers
        assert quadruple in double._observers
        
        quadruple.cleanup()
        assert quadruple not in double._observers
        
        double.cleanup()
        assert double not in base._observers


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_signal_none_value(self):
        """Test signal with None value."""
        signal = Signal(None)
        assert signal.value is None
        
        signal.value = 42
        assert signal.value == 42
        
        signal.value = None
        assert signal.value is None
    
    def test_computed_returning_none(self):
        """Test computed that returns None."""
        signal = Signal(True)
        computed = Computed(lambda: None if signal.value else 42)
        
        assert computed.value is None
        
        signal.value = False
        assert computed.value == 42
    
    def test_effect_with_no_dependencies(self):
        """Test effect that doesn't access any signals."""
        executions = []
        
        effect = Effect(lambda: executions.append("executed"))
        
        # Should execute once immediately
        assert executions == ["executed"]
        
        # No further executions without dependencies
        assert executions == ["executed"]
    
    def test_large_dependency_graph(self):
        """Test performance with large dependency graph."""
        # Create a pyramid of dependencies
        base_signals = [Signal(i) for i in range(10)]
        
        level1 = [
            Computed(lambda i=i: base_signals[i].value + base_signals[i+1].value)
            for i in range(9)
        ]
        
        level2 = [
            Computed(lambda i=i: level1[i].value + level1[i+1].value)
            for i in range(8)
        ]
        
        top = Computed(lambda: sum(c.value for c in level2))
        
        initial_value = top.value
        
        # Update a base signal
        base_signals[0].value = 100
        
        # Should propagate through the graph
        assert top.value != initial_value
    
    def test_signal_equality(self):
        """Test signal value equality checks."""
        # Lists are compared by value equality using !=
        signal = Signal([1, 2, 3])
        version = signal._version
        
        # Setting to a new list with same content doesn't trigger update
        signal.value = [1, 2, 3]
        assert signal._version == version  # Same content, no update
        
        # Setting to a different list triggers update
        signal.value = [4, 5, 6]
        version2 = signal._version
        assert signal._version > version  # Different content, updates
        
        # Setting to the same list object doesn't trigger update
        same_list = [7, 8, 9]
        signal.value = same_list
        version3 = signal._version
        signal.value = same_list  # Same object
        assert signal._version == version3  # No change
        
        # For immutable values, equality works
        int_signal = Signal(42)
        int_version = int_signal._version
        int_signal.value = 42
        assert int_signal._version == int_version