# TableView 示例说明

## 🎯 当前状态

macUI v2 的原始 TableView 实现存在 `NSLayoutConstraintNumberExceedsLimit` 约束冲突问题。
本目录提供了多个工作的 TableView 实现示例。

## ✅ 推荐使用的工作示例

### 1. **`test_tableview_working.py`** (主要推荐)
- **状态**: ✅ 完全正常工作
- **特点**: 使用纯PyObjC实现，避免macUI的约束问题
- **功能**: 完整的TableView功能，包括数据显示、行选择、自定义格式
- **用途**: 作为TableView的标准实现参考

### 2. **`tableview/simple_pure_tableview.py`**
- **状态**: ✅ 完全正常工作
- **特点**: 简单的TableView实现，使用PyObjC最佳实践
- **功能**: 基础数据显示和行选择
- **用途**: 学习NSTableView基本用法

### 3. **`tableview/advanced_pure_tableview_simple.py`**
- **状态**: ✅ 完全正常工作  
- **特点**: 高级TableView功能，包括排序、动态数据操作
- **功能**: 排序、添加/删除数据、条件格式化
- **用途**: 复杂TableView功能参考

## ⚠️ 有问题的示例

### macUI框架的TableView相关示例
以下示例使用了有问题的macUI TableView实现，会导致约束错误：

- `test_tableview_only.py` - 使用VStack包装TableView
- 其他使用 `from macui.components import TableView` 的示例

**错误症状**: `NSLayoutConstraintNumberExceedsLimit` 错误，应用崩溃

## 🔧 技术要点

### 工作的实现模式
```python
# ✅ 正确的做法
scroll_view = NSScrollView.alloc().init()
scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)  # 传统autoresizing

table_view = NSTableView.alloc().init()  
table_view.setTranslatesAutoresizingMaskIntoConstraints_(True)   # 传统autoresizing

# 使用frame-based布局
container = NSView.alloc().init()
container.addSubview_(scroll_view)
```

### 避免的错误模式
```python
# ❌ 错误的做法 - 导致约束冲突
VStack(children=[
    TableView(...)  # 这会导致NSLayoutConstraintNumberExceedsLimit错误
])
```

## 📋 运行测试

```bash
# 运行主要工作示例
python3 examples/test_tableview_working.py

# 运行纯PyObjC示例
python3 examples/tableview/simple_pure_tableview.py
python3 examples/tableview/advanced_pure_tableview_simple.py

# 测试纯PyObjC最佳实践版本
python3 examples/tableview_no_stack_fix.py
```

## 🔍 问题诊断

如果遇到TableView问题：

1. **检查是否使用了VStack/HStack包装TableView**
2. **确认使用了`translatesAutoresizingMaskIntoConstraints_(True)`**
3. **使用frame-based布局而不是约束系统**
4. **参考工作示例的实现模式**

## 📚 参考文档

- `TABLEVIEW_SOLUTION_REPORT.md` - 完整的问题分析和解决方案
- `CLAUDE.md` - macUI项目的完整开发指导
- `tableview/README.md` - 纯PyObjC TableView实现指南

## 🎯 总结

**当前推荐**: 使用纯PyObjC实现的TableView示例，避免macUI框架中有问题的TableView实现。

**长期计划**: 等待macUI框架修复TableView的约束冲突问题。

---

**最后更新**: 2025-08-26  
**状态**: TableView问题已诊断，工作示例已验证