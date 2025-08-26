# Complex Control Examples

复杂控件示例，展示高级UI组件的使用。

## 示例文件

### test_splitview_only.py
分割视图示例，展示：
- SplitView双面板布局
- 可调整分割比例
- 左右或上下分割
- 嵌套内容管理

**运行命令**:
```bash
uv run python examples/complex/test_splitview_only.py
```

### test_tabview_only.py
标签页视图示例，展示：
- TabView多标签界面
- 标签切换和管理
- 每个标签的独立内容
- 动态添加/删除标签

**运行命令**:
```bash
uv run python examples/complex/test_tabview_only.py
```

### test_outlineview_only.py
大纲视图示例，展示：
- OutlineView树形结构
- 可展开/折叠节点
- 层级数据展示
- 节点选择和编辑

**运行命令**:
```bash
uv run python examples/complex/test_outlineview_only.py
```

## 复杂性说明

这些组件具有较高的复杂性，需要：
- 深入理解macUI的数据绑定机制
- 熟悉NSView的高级特性
- 掌握复杂的事件处理模式

建议在掌握基础控件后再学习这些示例。