# Layout Examples

布局组件示例，展示界面布局和组织。

## 示例文件

### test_stage3_layout.py
高级布局示例，展示：
- VStack和HStack嵌套布局
- 响应式布局调整
- 复杂界面组织
- 布局约束和对齐

**运行命令**:
```bash
uv run python examples/layout/test_stage3_layout.py
```

## 布局组件

- **VStack**: 垂直堆叠布局
- **HStack**: 水平堆叠布局
- **ScrollView**: 滚动容器
- **ResponsiveStack**: 响应式堆叠布局

## 注意事项

⚠️ **TableView布局约束**: TableView不能直接放在VStack/HStack中，需要使用简单容器。详见 `examples/tableview/` 中的正确使用示例。