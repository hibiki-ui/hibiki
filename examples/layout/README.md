# 混合布局系统演示

本目录包含了展示 macUI v2.1 混合布局系统功能的完整演示示例。

## 🎉 革命性改进

**重构前的问题**：
```python
# 这会导致 NSLayoutConstraintNumberExceedsLimit 崩溃 💥
VStack(children=[
    Label("标题"),
    TableView(columns=..., data=...),  # ❌ 崩溃!
    Button("按钮")
])
```

**重构后的解决方案**：
```python
# 现在完美工作! 🎉
VStack(children=[
    Label("标题"), 
    TableView(columns=..., data=...),  # ✅ 自动切换到frame布局
    Button("按钮")
])
```

## 📁 演示文件

### 1. `test_hybrid_basic.py` - 基础功能测试
```bash
uv run python examples/layout/test_hybrid_basic.py
```
- ✅ 测试混合布局系统基础功能
- ✅ 验证TableView在VStack中的使用
- ✅ 测试不同布局模式

### 2. `visual_demo.py` - 可视化演示 ⭐ 推荐
```bash
uv run python examples/layout/visual_demo.py
```
- 🎨 创建实际的NSView对象
- 📋 检查布局结构和Frame信息
- 🔍 展示内部机制
- ✅ 验证响应式特性

### 3. `comparison_demo.py` - 完整对比演示 ⭐ 推荐
```bash
uv run python examples/layout/comparison_demo.py
```
- 🆚 重构前后详细对比
- 🧠 智能组件检测演示
- ⚡ 性能对比分析
- 🌟 真实使用场景演示

### 4. 其他演示文件
- `test_hybrid_advanced.py` - 高级功能测试
- `simple_hybrid_demo.py` - 简单演示
- `hybrid_gui_demo.py` - GUI演示应用（需要PyObjC）

## 🚀 快速开始

推荐运行顺序：

1. **基础测试**：
   ```bash
   uv run python examples/layout/test_hybrid_basic.py
   ```

2. **看实际效果**：
   ```bash
   uv run python examples/layout/visual_demo.py
   ```

3. **完整对比**：
   ```bash
   uv run python examples/layout/comparison_demo.py
   ```

## 🎯 核心优势

- ✅ **零破坏性变更** - 现有代码无需修改
- ✅ **TableView现在可以在VStack/HStack中使用**
- ✅ **自动组件类型检测和智能布局选择**
- ✅ **支持复杂嵌套布局**
- ✅ **保持高性能和响应式特性**

## 🎉 结论

混合布局系统完全解决了macUI框架最大的约束问题，现在用户可以：

- ✅ 在任何布局容器中自由使用TableView
- ✅ 创建复杂的数据管理应用
- ✅ 享受简洁的声明式布局代码
- ✅ 无需担心约束冲突问题

**macUI v2.1 现已具备业界领先的布局能力！** 🎉