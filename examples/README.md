# macUI 组件示例

这个文件夹包含了各种 macUI 组件的示例和测试代码。

## 示例目录

### 核心功能示例

#### Counter 计数器应用
- **文件**: `counter.py`
- **功能**: 展示 macUI 的核心响应式系统
- **特性**:
  - 基础计数器: Signal、Computed、Effect 系统演示
  - 高级计数器: 多计数器、步长控制、历史记录
  - 响应式编程模型完整展示
  - 组件系统和布局管理

### 组件功能示例

#### TextField 增强功能
- **文件**: `test_enhanced_textfield.py`
- **功能**: 展示 TextField 的所有增强功能
- **特性**:
  - 基础文本输入和双向绑定
  - 密码框（文本隐藏）
  - 邮箱验证（必须包含@和.）
  - 电话号码自动格式化
  - 回车键和焦点事件
  - 最大长度限制
  - 工具提示

#### Slider 滑块控件
- **文件**: `test_slider.py`
- **功能**: 展示 Slider 的各种配置
- **特性**:
  - 基础滑块（0-100）
  - 音量滑块（步长5）
  - 温度滑块（负数范围）
  - 精密滑块（步长0.25）
  - 垂直滑块
  - 双向数据绑定
  - 工具提示

#### TextArea 和 ProgressBar
- **文件**: `test_textarea_progressbar.py`
- **功能**: 展示多行文本区域和进度条
- **特性**:
  - **TextArea**: 多行文本编辑和滚动、双向数据绑定、实时文本统计
  - **ProgressBar**: 静态进度显示、动态进度更新、不确定进度动画
  - 响应式UI更新

#### 选择控件 (Checkbox, RadioButton, Switch)
- **文件**: `test_selection_controls.py`
- **功能**: 展示各种选择和开关控件
- **特性**:
  - **Checkbox**: 多选复选框，独立状态控制
  - **Switch**: 开关控件，布尔值切换
  - **RadioButton**: 单选按钮组，互斥选择
  - 双向数据绑定和实时状态更新
  - 批量控制功能（切换所有、重置所有）
  - 完整的事件回调和工具提示

#### 高级选择控件 (SegmentedControl, PopUpButton)
- **文件**: `test_advanced_controls.py`
- **功能**: 展示高级选择和下拉控件
- **特性**:
  - **SegmentedControl**: 分段选择控件，适合显示3-5个选项
  - **PopUpButton**: 下拉选择按钮，适合多个选项的列表选择
  - 双向数据绑定和实时状态更新
  - 批量控制功能（随机设置、重置所有）
  - 完整的选项管理和事件回调

#### 第二阶段剩余组件 (ComboBox, Menu, DatePicker, TimePicker)
- **文件**: `test_stage2_remaining.py`
- **功能**: 展示第二阶段剩余的组件功能
- **特性**:
  - **ComboBox**: 可编辑组合框，支持搜索建议和分类选择
  - **Menu/ContextMenu**: 菜单系统，主菜单和右键菜单
  - **DatePicker**: 日期选择器，支持多种样式（文本框、步进器、日历）
  - **TimePicker**: 时间选择器，基于DatePicker实现
  - 双向数据绑定和实时状态更新
  - 完整的事件处理和工具提示
  - 响应式UI更新

## 如何运行示例

确保你在项目根目录，然后运行：

```bash
# 核心功能示例 - 计数器应用
uv run python examples/counter.py

# 组件功能示例
uv run python examples/test_enhanced_textfield.py   # TextField 增强功能
uv run python examples/test_slider.py               # Slider 控件
uv run python examples/test_textarea_progressbar.py # TextArea 和 ProgressBar
uv run python examples/test_selection_controls.py   # 选择控件
uv run python examples/test_advanced_controls.py    # 高级选择控件
uv run python examples/test_stage2_remaining.py     # 第二阶段剩余组件
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