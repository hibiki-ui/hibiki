# Changelog

All notable changes to the Hibiki UI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-28

### Added
- **🎉 Initial Release** - Complete reactive UI framework for native macOS applications
- **🔄 Signal-based Reactivity** - Core reactive system with Signal, Computed, and Effect primitives
- **🧩 Component System** - Modern component architecture with UIComponent base class
- **📐 Professional Layout Engine** - Flexbox-style layout system with precise control
- **🎨 Complete UI Toolkit** - Full set of native macOS components:
  - Basic components: Label, Button, TextField, Slider, Switch
  - Advanced components: TextArea, Checkbox, RadioButton, ProgressBar, ImageView
  - Selection components: PopUpButton, ComboBox
  - Layout components: Container with flexbox properties
- **🎭 Form Handling System** - Complete form management with validation
- **⚡ Animation System** - GPU-accelerated animations using Pure Core Animation
- **🎨 Theme Management** - Comprehensive theme system with appearance mode support
- **🔧 Advanced Layout Features** - Grid layouts, responsive design, and complex positioning

### Technical Features
- **Native Performance** - Direct PyObjC integration with AppKit components
- **Reaktiv-Inspired Optimizations** - Performance enhancements including:
  - Version control system for intelligent dependency tracking
  - Batch processing with deduplication for minimal UI updates
  - Smart caching to avoid unnecessary recomputations
  - Global version tracking for optimal performance
- **Memory Management** - Proper lifecycle management and automatic cleanup
- **Type Safety** - Complete type annotations with excellent IDE support
- **Professional Architecture** - Layered architecture with clear separation of concerns

### Animation System
- **Pure Core Animation** - Strictly GPU-accelerated animations using Core Animation APIs
- **Declarative API** - Simple animate() function with preset effects
- **Signal Integration** - Reactive animations tied to state changes
- **Performance First** - Zero threading or custom timing, all animations run on GPU

### Development Experience
- **Modern Tooling** - Full uv package manager support
- **Code Quality** - Integrated ruff, black, mypy, pytest
- **Documentation** - Comprehensive README with examples
- **Showcase Application** - Complete demo showing all features
- **Project Structure** - Clean, organized codebase with clear documentation

### Project Structure
```
hibiki/
├── core/           # Core reactive system and architecture
├── components/     # UI components and forms
├── theme/          # Theme and appearance management
└── showcase.py     # Complete feature demonstration
```

### Breaking Changes
- Initial 0.1.0 release - no previous versions to break compatibility with

### Migration from macUI
- **Project Rename** - Complete migration from macUI to Hibiki UI
- **Package Name** - Now available as `hibiki-ui` package
- **Import Changes** - All imports now use `from hibiki import ...`
- **Documentation** - Updated all documentation and examples

---

**Note**: Starting with v0.1.0, Hibiki UI follows semantic versioning. This release represents the foundation of the framework with all core features implemented and tested.