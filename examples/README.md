# macUI Examples

macUI v2框架的完整示例集合，按功能分类组织。

## 📁 目录结构 (更新于 2025-08-26)

### 🔰 [basic/](basic/) - 基础示例
最适合初学者，展示macUI的核心概念：
- **counter.py** - 响应式计数器（推荐入门）
- **test_enhanced_textfield.py** - 文本输入处理

### 🎛️ [input/](input/) - 输入控件示例  
各种用户输入方式：
- **test_slider.py** - 滑块控件完整演示
- **test_selection_controls.py** - 选择控件集合

### 📺 [display/](display/) - 显示控件示例
内容展示和进度指示：
- **test_textarea_progressbar.py** - 文本区域和进度条

### 📐 [layout/](layout/) - 布局示例
界面布局和组织：
- **test_stage3_layout.py** - 高级堆叠布局

### 🔧 [complex/](complex/) - 复杂控件示例
高级UI组件：
- **test_splitview_only.py** - 分割视图
- **test_tabview_only.py** - 标签页视图
- **test_outlineview_only.py** - 大纲/树形视图

### 🗂️ [tableview/](tableview/) - TableView专项示例
TableView相关的所有工作示例（解决约束冲突问题后）：
- **simple_pure_tableview.py** - 纯PyObjC实现（推荐）
- **advanced_pure_tableview_simple.py** - 高级功能演示

## 🚀 快速开始

### 推荐学习路径
1. **新手**: `basic/counter.py` → `basic/test_enhanced_textfield.py`
2. **进阶**: `input/test_slider.py` → `layout/test_stage3_layout.py` 
3. **高级**: `complex/` 目录下的复杂控件
4. **TableView**: `tableview/` 目录下的专项示例

### 核心功能示例 (已移至 basic/)

#### Counter 计数器应用
- **文件**: `basic/counter.py`
- **功能**: 展示 macUI 的核心响应式系统
- **特性**:
  - 基础计数器: Signal、Computed、Effect 系统演示
  - 高级计数器: 多计数器、步长控制、历史记录
  - 响应式编程模型完整展示
  - 组件系统和布局管理

## 🎯 运行示例

### 按分类运行
```bash
# 基础示例（推荐新手从这里开始）
uv run python examples/basic/counter.py
uv run python examples/basic/test_enhanced_textfield.py

# 输入控件示例
uv run python examples/input/test_slider.py
uv run python examples/input/test_selection_controls.py

# 显示控件示例
uv run python examples/display/test_textarea_progressbar.py

# 布局示例
uv run python examples/layout/test_stage3_layout.py

# 复杂控件示例
uv run python examples/complex/test_splitview_only.py
uv run python examples/complex/test_tabview_only.py
uv run python examples/complex/test_outlineview_only.py

# TableView专项示例（推荐）
uv run python examples/tableview/simple_pure_tableview.py
uv run python examples/tableview/advanced_pure_tableview_simple.py
```

### 遗留未分类示例
以下示例还未分类整理，保持原有运行方式：
```bash
# 第二阶段剩余组件
uv run python examples/test_stage2_remaining.py     
uv run python examples/test_advanced_controls.py    
```

## 示例特点

1. **完整的功能展示**: 每个示例都展示了组件的所有主要功能
2. **实时反馈**: 所有示例都有实时的状态显示和反馈
3. **响应式设计**: 使用 Signal 系统进行响应式UI更新
4. **交互式测试**: 包含按钮和控件来测试各种功能
5. **详细日志**: 所有操作都有详细的日志输出，方便调试

## 技术特性展示

- **响应式编程**: 使用 Signal/Computed/Effect 系统
- **双向数据绑定**: UI组件与数据模型自动同步
- **事件处理**: 完整的用户交互事件支持
- **类型安全**: 完整的类型注解
- **macOS 原生**: 基于 PyObjC 和 AppKit 的原生界面