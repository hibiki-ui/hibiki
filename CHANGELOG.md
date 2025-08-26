# Changelog

All notable changes to the macUI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-08-26

### Fixed
- **Critical Bug**: Fixed reactive system observer management issue
  - Replaced WeakSet with regular set for Effect observers to prevent garbage collection
  - Fixed UI components not updating when Signal values change
  - Resolved button click handlers not triggering UI updates in counter application
  - Improved observer notification mechanism with proper cleanup
- Simplified batch update system to prevent infinite loops
- Enhanced error handling in observer notification chain

### Technical Improvements
- Observer lifecycle management now uses explicit cleanup instead of weak references
- Removed complex batch update system that was causing timing issues
- Added comprehensive test suite for reactive system validation
- Improved debugging and logging for reactive system troubleshooting

### Testing
- Added `test_reactive_fix.py` for core reactive system validation
- Added `test_binding_simple.py` for UI binding verification
- Added `test_counter_auto.py` for automated application testing
- All reactive system tests now pass consistently

## [2.0.0] - 2024-08-26

### Added
- Signal-based reactive system with fine-grained reactivity
- Computed properties with automatic dependency tracking
- Effect system for side effects and UI updates
- Component-based architecture with lifecycle management
- Native macOS UI components via PyObjC integration
- Reactive binding system for automatic UI updates
- Event handling with proper target-action patterns
- Layout components (VStack, HStack, ZStack, ScrollView)
- Control components (Button, TextField, Label, Slider, Switch)
- Application framework with window management
- PyObjC command-line best practices implementation
- CLI tools for project creation and management
- Complete type annotations and IDE support
- Comprehensive testing framework
- Modern Python packaging with pyproject.toml

### Technical Features
- Direct PyObjC integration (removed all mock objects)
- AppHelper-based event loop for proper lifecycle management
- Automatic menu bar creation with quit functionality
- Proper application activation policy handling
- Strong reference management to prevent garbage collection
- Batch updates with CATransaction for performance
- WeakSet-based observer management
- Context-aware dependency tracking

### Development Experience
- Full uv package manager support
- Modern tooling (ruff, black, mypy, pytest)
- Pre-commit hooks for code quality
- Comprehensive documentation
- Multiple example applications
- Interactive CLI for project scaffolding

### Breaking Changes
- Complete rewrite from v1.x
- Removed compatibility with older PyObjC versions
- macOS-only support (removed cross-platform abstractions)
- Requires Python 3.8+

## [1.0.0] - Previous Version
- Initial release with basic PyObjC bindings