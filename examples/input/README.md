# Input Control Examples

输入控件示例，展示各种用户输入方式。

## 示例文件

### test_slider.py
滑块控件完整示例，展示：
- Slider双向数据绑定
- 范围设置和步长控制
- 垂直和水平滑块
- 实时值变化回调

**运行命令**:
```bash
uv run python examples/input/test_slider.py
```

### test_selection_controls.py
选择控件集合示例，展示：
- Checkbox复选框
- RadioButton单选按钮组
- SegmentedControl分段控件
- 各种选择状态管理

**运行命令**:
```bash
uv run python examples/input/test_selection_controls.py
```

## 特色功能

- **响应式绑定**: 所有输入控件都支持Signal双向绑定
- **事件回调**: 提供丰富的用户交互回调
- **样式定制**: 支持自定义外观和行为
- **状态管理**: 完整的启用/禁用状态控制