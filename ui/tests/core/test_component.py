"""
Tests for the Component System
==============================

Testing UIComponent base class and Container functionality.
"""

import pytest
from unittest.mock import MagicMock, patch, call
from hibiki.ui.core.component import UIComponent, Container
from hibiki.ui.core.reactive import Signal, Computed, Effect
from hibiki.ui.core.styles import ComponentStyle, Display, FlexDirection


class MockComponent(UIComponent):
    """Mock component for testing."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mock_view = MagicMock()
    
    def _create_nsview(self):
        """Override abstract _create_nsview method."""
        return self._mock_view


class TestUIComponent:
    """Test the UIComponent base class."""
    
    def test_component_initialization(self):
        """Test basic component initialization."""
        component = MockComponent()
        
        assert component._nsview is None
        assert component._parent_container is None  # Initialized to None
        assert component._mounted is False
        assert isinstance(component._signals, list)
        assert isinstance(component._computed, list)
        assert isinstance(component._effects, list)
    
    def test_component_with_style(self):
        """Test component initialization with style."""
        style = ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN
        )
        component = MockComponent(style=style)
        
        assert component.style == style
    
    def test_component_mount(self, mock_layout_engine):
        """Test component mounting."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            # Mock the layout computation methods
            mock_layout_engine.get_node_for_component.return_value = None
            
            # Create a mock layout result with attributes
            mock_layout_result = MagicMock()
            mock_layout_result.x = 0
            mock_layout_result.y = 0
            mock_layout_result.width = 100
            mock_layout_result.height = 100
            mock_layout_engine.compute_layout_for_component.return_value = mock_layout_result
            
            component = MockComponent()
            view = component.mount()
            
            assert component._mounted is True
            assert component._nsview == component._mock_view
            assert view == component._mock_view
            mock_layout_engine.create_node_for_component.assert_called_once_with(component)
    
    def test_component_mount_only_once(self, mock_layout_engine):
        """Test that component can only be mounted once."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            # Mock the layout computation methods
            mock_layout_engine.get_node_for_component.return_value = None
            
            # Create a mock layout result with attributes
            mock_layout_result = MagicMock()
            mock_layout_result.x = 0
            mock_layout_result.y = 0
            mock_layout_result.width = 100
            mock_layout_result.height = 100
            mock_layout_engine.compute_layout_for_component.return_value = mock_layout_result
            
            component = MockComponent()
            view1 = component.mount()
            view2 = component.mount()
            
            assert view1 == view2
            # Should only create node once
            assert mock_layout_engine.create_node_for_component.call_count == 1
    
    def test_component_cleanup(self):
        """Test component cleanup."""
        component = MockComponent()
        
        # Create managed reactive objects
        signal = component.create_signal(42)
        computed = component.create_computed(lambda: signal.value * 2)
        effect = component.create_effect(lambda: signal.value)
        
        assert len(component._signals) == 1
        assert len(component._computed) == 1
        assert len(component._effects) == 1
        
        # Cleanup
        component.cleanup()
        
        # All managed objects should be cleaned up
        assert len(component._signals) == 0
        assert len(component._computed) == 0
        assert len(component._effects) == 0
    
    def test_create_signal(self):
        """Test creating a managed signal."""
        component = MockComponent()
        signal = component.create_signal(10)
        
        assert isinstance(signal, Signal)
        assert signal.value == 10
        assert signal in component._signals
    
    def test_create_computed(self):
        """Test creating a managed computed."""
        component = MockComponent()
        signal = component.create_signal(5)
        computed = component.create_computed(lambda: signal.value * 3)
        
        assert isinstance(computed, Computed)
        assert computed.value == 15
        assert computed in component._computed
    
    def test_create_effect(self):
        """Test creating a managed effect."""
        component = MockComponent()
        signal = component.create_signal(0)
        results = []
        
        effect = component.create_effect(lambda: results.append(signal.value))
        
        assert isinstance(effect, Effect)
        assert effect in component._effects
        assert results == [0]
        
        signal.value = 1
        assert results == [0, 1]
    
    def test_component_style_application(self, mock_layout_engine):
        """Test that styles are applied to the component."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            style = ComponentStyle(
                width=100,
                height=200,
                padding=10
            )
            component = MockComponent(style=style)
            component.mount()
            
            # Verify style is stored
            assert component.style == style
    
    def test_component_parent_child_relationship(self):
        """Test parent-child relationship management."""
        parent = MockComponent()
        child = MockComponent()
        
        child._parent_container = parent
        assert child._parent_container == parent


class TestContainer:
    """Test the Container class."""
    
    def test_container_initialization(self):
        """Test container initialization with children."""
        child1 = MockComponent()
        child2 = MockComponent()
        container = Container(children=[child1, child2])
        
        assert len(container.children) == 2
        assert child1 in container.children
        assert child2 in container.children
    
    def test_container_empty_initialization(self):
        """Test container with no children."""
        container = Container()
        assert container.children == []
    
    def test_container_reactive_children(self):
        """Test container with reactive children list."""
        child = MockComponent()
        children_list = [child]
        container = Container(children=children_list)
        
        assert container.children == children_list
        assert child in container._children  # Child added to internal list
        # Parent relationship is set during mount, not initialization
        assert child._parent_container is None
    
    def test_container_mount_children(self, mock_layout_engine):
        """Test that container mounts its children."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            # Mock the layout computation methods
            mock_layout_engine.get_node_for_component.return_value = None
            
            # Create a mock layout result with attributes
            mock_layout_result = MagicMock()
            mock_layout_result.x = 0
            mock_layout_result.y = 0
            mock_layout_result.width = 100
            mock_layout_result.height = 100
            mock_layout_engine.compute_layout_for_component.return_value = mock_layout_result
            
            child1 = MockComponent()
            child2 = MockComponent()
            container = Container(children=[child1, child2])
            
            # Mock HibikiContainerView instead of _create_nsview
            mock_container_view = MagicMock()
            mock_container_class = MagicMock()
            mock_container_class.alloc.return_value.init.return_value = mock_container_view
            
            with patch('hibiki.ui.core.base_view.HibikiContainerView', mock_container_class):
                container.mount()
                
                # Children should be mounted
                assert child1._mounted
                assert child2._mounted
                
                # Children should have parent set
                assert child1._parent_container == container
                assert child2._parent_container == container
    
    def test_container_add_child(self, mock_layout_engine):
        """Test adding a child to container."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            container = Container()
            child = MockComponent()
            
            container.add_child(child)
            
            # add_child adds to internal _children list, not public children
            assert child in container._children
            assert child not in container.children  # Public list unchanged
            assert len(container.children) == 0
    
    def test_container_add_child_when_mounted(self, mock_layout_engine):
        """Test adding a child to a mounted container."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            container = Container()
            
            # Mock the container's _create_nsview
            container_view = MagicMock()
            with patch.object(container, '_create_nsview', return_value=container_view):
                container.mount()
                
                child = MockComponent()
                container.add_child(child)
                
                # add_child only adds to internal _children, doesn't mount or set parent
                assert child in container._children
                assert child not in container.children  # Public list unchanged
                assert not child._mounted  # Not automatically mounted
                assert child._parent_container is None  # Parent not set by add_child
                
                # Layout engine should not be called by simple add_child
                mock_layout_engine.add_child_relationship.assert_not_called()
    
    def test_container_remove_child(self, mock_layout_engine):
        """Test removing a child from container."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            child = MockComponent()
            container = Container(children=[child])
            
            # Child should be in both public and internal lists after init
            assert child in container.children
            assert child in container._children
            
            container.remove_child(child)
            
            # remove_child removes from internal _children, not public children
            assert child in container.children  # Public list unchanged
            assert child not in container._children  # Removed from internal list
    
    def test_container_remove_child_when_mounted(self, mock_layout_engine):
        """Test removing a child from a mounted container."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            # Mock the layout computation methods
            mock_layout_engine.get_node_for_component.return_value = None
            
            # Create a mock layout result with attributes
            mock_layout_result = MagicMock()
            mock_layout_result.x = 0
            mock_layout_result.y = 0
            mock_layout_result.width = 100
            mock_layout_result.height = 100
            mock_layout_engine.compute_layout_for_component.return_value = mock_layout_result
            
            child = MockComponent()
            container = Container(children=[child])
            
            # Mock HibikiContainerView instead of _create_nsview
            mock_container_view = MagicMock()
            mock_container_class = MagicMock()
            mock_container_class.alloc.return_value.init.return_value = mock_container_view
            
            with patch('hibiki.ui.core.base_view.HibikiContainerView', mock_container_class):
                container.mount()
                
                # After mount, parent relationship should be set
                assert child._parent_container == container
                
                container.remove_child(child)
                
                # remove_child removes from internal list and cleans up child
                assert child in container.children  # Public list unchanged
                assert child not in container._children  # Removed from internal list
                # Parent relationship cleared by cleanup, not by remove_child directly
                
                # Layout engine should not be called by simple remove_child
                mock_layout_engine.remove_child_relationship.assert_not_called()
    
    def test_container_clear_children(self):
        """Test clearing all children from container."""
        child1 = MockComponent()
        child2 = MockComponent()
        container = Container(children=[child1, child2])
        
        container.clear_children()
        
        assert len(container.children) == 0
        assert child1 not in container.children
        assert child2 not in container.children
    
    def test_container_cleanup_cleans_children(self):
        """Test that container cleanup also cleans up children."""
        child1 = MockComponent()
        child2 = MockComponent()
        container = Container(children=[child1, child2])
        
        # Add managed objects to children
        child1_signal = child1.create_signal(1)
        child2_signal = child2.create_signal(2)
        
        container.cleanup()
        
        # Children should also be cleaned up
        assert len(child1._signals) == 0
        assert len(child2._signals) == 0
    
    def test_container_with_style(self):
        """Test container with custom style."""
        style = ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            gap=10
        )
        container = Container(style=style)
        
        assert container.style == style
    
    def test_container_reactive_children_updates(self):
        """Test container dynamic child addition/removal."""
        child1 = MockComponent()
        child2 = MockComponent()
        
        container = Container(children=[child1])
        assert len(container.children) == 1
        
        # Add second child dynamically to internal list
        container.add_child(child2)
        
        # Child added to internal list, but not public children list
        assert len(container.children) == 1  # Public list unchanged
        assert child2 in container._children  # Added to internal list
        # Parent relationship set during mount, not add_child
        assert child2._parent_container is None
    
    def test_container_nested_containers(self, mock_layout_engine):
        """Test nested container structures."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            # Mock the layout computation methods
            mock_layout_engine.get_node_for_component.return_value = None
            
            # Create a mock layout result with attributes
            mock_layout_result = MagicMock()
            mock_layout_result.x = 0
            mock_layout_result.y = 0
            mock_layout_result.width = 100
            mock_layout_result.height = 100
            mock_layout_engine.compute_layout_for_component.return_value = mock_layout_result
            
            inner_child = MockComponent()
            inner_container = Container(children=[inner_child])
            outer_container = Container(children=[inner_container])
            
            # Mock views
            outer_view = MagicMock()
            inner_view = MagicMock()
            # Mock HibikiContainerView for both containers
            mock_container_view = MagicMock()
            mock_container_class = MagicMock()
            mock_container_class.alloc.return_value.init.return_value = mock_container_view
            
            with patch('hibiki.ui.core.base_view.HibikiContainerView', mock_container_class):
                outer_container.mount()
                
                # All should be mounted
                assert outer_container._mounted
                assert inner_container._mounted
                assert inner_child._mounted
                
                # Parent relationships
                assert inner_container._parent_container == outer_container
                assert inner_child._parent_container == inner_container


class TestComponentLifecycle:
    """Test component lifecycle management."""
    
    def test_lifecycle_mount_unmount_remount(self, mock_layout_engine):
        """Test mounting, unmounting, and remounting a component."""
        with patch('hibiki.ui.core.component.get_layout_engine', return_value=mock_layout_engine):
            component = MockComponent()
            
            # Initial mount
            view1 = component.mount()
            assert component._mounted
            
            # Unmount (cleanup)
            component.cleanup()
            component._mounted = False
            component._nsview = None
            
            # Remount
            view2 = component.mount()
            assert component._mounted
            # Should create a new view
            assert view2 == component._mock_view
    
    def test_lifecycle_effect_cleanup_on_unmount(self):
        """Test that effects are cleaned up on unmount."""
        component = MockComponent()
        signal = component.create_signal(0)
        executions = []
        
        effect = component.create_effect(lambda: executions.append(signal.value))
        assert executions == [0]
        
        signal.value = 1
        assert executions == [0, 1]
        
        # Unmount/cleanup
        component.cleanup()
        
        # Effect should no longer execute
        signal.value = 2
        assert executions == [0, 1]  # No new execution
    
    def test_lifecycle_parent_change(self):
        """Test changing a component's parent container."""
        child = MockComponent()
        parent1 = Container(children=[child])
        parent2 = Container()
        
        # Parent relationship not set during init, only during mount
        assert child._parent_container is None
        
        # Move child between internal lists
        parent1.remove_child(child)
        parent2.add_child(child)
        
        # Parent relationship still not set by add/remove operations
        assert child._parent_container is None
        # Public children lists unchanged by add/remove operations
        assert child in parent1.children  # Still in original parent's public list
        assert child not in parent2.children  # Not in new parent's public list
        # Internal lists are updated
        assert child not in parent1._children
        assert child in parent2._children