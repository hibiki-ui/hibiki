"""
Pytest Configuration and Fixtures
=================================

Shared fixtures and configuration for all tests.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the ui/src directory to the path so we can import hibiki.ui
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def mock_nsview():
    """Mock NSView object for testing without AppKit dependencies."""
    view = MagicMock()
    view.frame.return_value = ((0, 0), (100, 100))
    view.bounds.return_value = ((0, 0), (100, 100))
    view.superview.return_value = None
    view.subviews.return_value = []
    view.isFlipped.return_value = True
    return view


@pytest.fixture
def mock_nswindow():
    """Mock NSWindow object for testing."""
    window = MagicMock()
    window.frame.return_value = ((0, 0), (800, 600))
    window.contentView.return_value = MagicMock()
    window.isVisible.return_value = True
    return window


@pytest.fixture
def mock_layout_engine():
    """Mock layout engine for isolated component testing."""
    engine = MagicMock()
    engine.create_node_for_component.return_value = MagicMock()
    engine.add_child_relationship.return_value = None
    engine.remove_child_relationship.return_value = None
    engine.compute_layout.return_value = None
    engine.get_node_tree_info.return_value = {
        'component_type': 'MockComponent',
        'node_key': 'mock_key',
        'children_count': 0,
        'stretchable_valid': True,
        'children': []
    }
    return engine


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    # Reset any global singletons to prevent test interference
    from hibiki.ui.core import reactive
    
    # Clear the reactive system's internal state if needed
    if hasattr(reactive, '_batch_queue'):
        reactive._batch_queue = []
    if hasattr(reactive, '_is_batching'):
        reactive._is_batching = False
    
    yield
    
    # Cleanup after test
    if hasattr(reactive, '_batch_queue'):
        reactive._batch_queue = []
    if hasattr(reactive, '_is_batching'):
        reactive._is_batching = False


@pytest.fixture
def cleanup_effects():
    """Ensure effects are properly cleaned up after tests."""
    effects = []
    
    def track_effect(effect):
        effects.append(effect)
        return effect
    
    yield track_effect
    
    # Cleanup all tracked effects
    for effect in effects:
        if hasattr(effect, 'cleanup') and callable(effect.cleanup):
            effect.cleanup()


@pytest.fixture
def mock_app_manager():
    """Mock AppManager for testing without macOS dependencies."""
    with patch('hibiki.ui.core.managers.AppManager') as MockAppManager:
        manager = MagicMock()
        manager.create_window.return_value = MagicMock()
        manager.run.return_value = None
        manager.stop.return_value = None
        MockAppManager.return_value = manager
        yield manager


@pytest.fixture
def mock_viewport_manager():
    """Mock ViewportManager for testing viewport functionality."""
    manager = MagicMock()
    manager.width = 800
    manager.height = 600
    manager.content_width = 800
    manager.content_height = 600
    manager.scale_factor = 1.0
    return manager


# Test markers for categorizing tests
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "gui: mark test as requiring GUI (skip in CI)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "macos_only: mark test as macOS specific"
    )