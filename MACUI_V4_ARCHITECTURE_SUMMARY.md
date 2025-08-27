# macUI v4.0 完整架构设计文档

## 🎯 设计目标

基于现有三层架构混乱问题和新的UI需求，设计一个清晰、强大、易用的组件架构：

### ✅ 已解决的问题
- ❌ 消除三层架构混乱 → ✅ 清晰的两层架构
- ❌ 缺少绝对定位支持 → ✅ 完整的定位系统
- ❌ 没有Z-Index管理 → ✅ 专业的层级管理
- ❌ 接口使用复杂 → ✅ 分层API设计
- ❌ 缺少特殊效果支持 → ✅ 变换、遮罩、滚动等

### 🎨 支持的UI场景
- ✅ **模态对话框**: `button.layout.modal(400, 300)`
- ✅ **悬浮元素**: `tooltip.layout.tooltip()`, `dropdown.layout.dropdown()`
- ✅ **固定元素**: `fab.layout.floating_button("bottom-right")`
- ✅ **全屏遮罩**: `overlay.layout.fullscreen()`
- ✅ **层级效果**: 预定义ZLayer + 自定义z-index
- ✅ **变换效果**: scale, rotate, translate, opacity
- ✅ **滚动容器**: 自动处理overflow行为
- ✅ **裁剪遮罩**: clip_rect支持

## 🏗️ 核心架构

### 1. 双层组件架构

```
Component (抽象基类)
├── 响应式状态管理 (Signal, Effect, Computed)
├── 核心生命周期 (mount, cleanup) 
└── 基础组件功能 (绑定、子组件管理)

UIComponent (具体基类)
├── 完整布局API (Flexbox + Grid + 绝对定位)
├── 管理器系统集成 (六大管理器)
├── 分层API接口 (高层 + 低层)
└── NSView集成和渲染
```

### 2. 六大管理器系统

#### **ViewportManager** - 视口管理
- 视口尺寸计算和缓存
- Retina屏幕适配
- 窗口事件监听

#### **LayerManager** - 层级管理  
- Z-Index注册和管理
- 预定义层级常量 (ZLayer)
- 自动z-index分配
- 弱引用防止内存泄漏

#### **PositioningManager** - 定位管理
- 绝对定位frame计算
- 固定定位（相对视口）
- 相对定位偏移
- 多单位支持 (px, %, vw, vh)

#### **TransformManager** - 变换管理
- CSS变换效果 (scale, rotate, translate)
- CALayer集成
- 透明度控制

#### **ScrollManager** - 滚动管理
- NSScrollView自动创建
- overflow行为处理
- 滚动容器注册

#### **MaskManager** - 遮罩管理
- 裁剪区域设置
- CALayer mask应用

### 3. 分层API设计

#### **高层API** (`component.layout.*`) - 覆盖85-90%场景
```python
# 常见定位
.center(z_index)           # 居中
.top_left(margin)          # 左上角
.top_right(margin)         # 右上角  
.bottom_right(margin)      # 右下角
.fullscreen(z_index)       # 全屏

# 预设场景  
.modal(width, height)      # 模态框
.tooltip(offset_x, offset_y) # 工具提示
.dropdown(offset_y)        # 下拉菜单
.floating_button(corner)   # 悬浮按钮

# 便捷样式
.size(width, height)       # 尺寸
.fade(opacity)            # 透明度
```

#### **低层API** (`component.advanced.*`) - 高级用户使用
```python
# 直接控制
.set_position(position, **coords)     # 定位设置
.set_flex_properties(**props)         # Flexbox属性
.set_transform(**transform)           # 变换效果

# 底层集成
.apply_stretchable_layout(**props)    # 直接使用Stretchable
.apply_raw_appkit(configurator)       # 直接访问NSView
```

## 🎨 使用示例

### 简单场景（高层API）
```python
# 居中模态对话框
modal = Container().layout.modal(400, 300)

# 右下角悬浮按钮
fab = Button("💬").layout.floating_button("bottom-right")

# 工具提示
tooltip = Label("提示信息").layout.tooltip()

# 全屏加载遮罩
overlay = Container().layout.fullscreen().fade(0.8)
```

### 复杂场景（低层API）
```python
# 高级定位控制
label.advanced.set_position(
    Position.ABSOLUTE, 
    left=100, top=200
).set_transform(
    scale=(1.2, 1.2),
    rotation=15
)

# 直接使用Stretchable
container.advanced.apply_stretchable_layout(
    flex_direction="row",
    justify_content="space-between"
)

# 直接访问AppKit
button.advanced.apply_raw_appkit(
    lambda view: view.setBezelStyle_(NSBezelStyleRounded)
)
```

## 🚀 架构优势

### 1. **清晰的关注点分离**
- 每个管理器负责一个特定领域
- 易于测试、扩展和维护
- 避免"上帝类"问题

### 2. **渐进式增强设计**
- 新手：使用高层API快速上手
- 进阶：使用低层API进行细粒度控制
- 专家：直接访问底层AppKit能力

### 3. **完整的场景覆盖**
- 现代Web应用的所有UI模式
- 从简单布局到复杂交互
- 预设场景 + 自定义灵活性

### 4. **性能优化设计**
- 弱引用防止内存泄漏
- 延迟计算和缓存
- 批量更新和事件合并

### 5. **类型安全和开发体验**
- 完整的类型注解
- 清晰的错误信息
- 链式调用支持
- IDE友好的自动完成

## 📚 边界和限制

### ✅ 支持的CSS特性
- Position: static, relative, absolute, fixed
- Z-Index: 数值 + 预定义层级
- Transform: scale, rotate, translate, opacity
- Box Model: width, height, margin, padding
- Flexbox: 完整支持
- Overflow: visible, hidden, scroll, auto

### ❌ 不支持的CSS特性
- Grid Layout（待实现）
- Float定位（已过时）
- CSS动画（将由单独的动画系统处理）
- 复杂选择器（组件化架构不需要）
- 伪元素和伪类（通过组件状态处理）

### 🔗 与现有系统集成
- **Stretchable布局引擎**: 作为核心布局计算器
- **macUI响应式系统**: 完整保留Signal/Effect机制
- **AppKit框架**: 通过low-level API完全开放

## 📋 实施计划

### Phase 1: 基础架构 (Week 1-2)
1. 实现六大管理器系统
2. 创建ComponentStyle数据结构
3. 实现UIComponent基类
4. 基本的mount流程

### Phase 2: API接口 (Week 3)
1. 实现HighLevelLayoutAPI
2. 实现LowLevelLayoutAPI  
3. 添加链式调用支持
4. 创建预设场景方法

### Phase 3: 具体组件 (Week 4)
1. 重构Label、Button等基础组件
2. 创建Modal、Tooltip等复合组件
3. 添加滚动容器和遮罩支持
4. 集成现有的响应式系统

### Phase 4: 测试和文档 (Week 5)
1. 完整的单元测试覆盖
2. 集成测试和性能测试
3. API文档和使用指南
4. 迁移指南和最佳实践

### Phase 5: 生态集成 (Week 6)
1. 与现有示例和demo的集成
2. 开发者工具支持
3. 性能优化和内存管理
4. 社区反馈和迭代

## 🎯 成功指标

### 开发体验指标
- ✅ API学习曲线：新手30分钟上手基础功能
- ✅ 场景覆盖率：90%常见UI模式有预设方案
- ✅ 代码简洁性：复杂布局代码量减少50%+

### 性能指标  
- ✅ 渲染性能：与原生AppKit性能相当
- ✅ 内存占用：无明显内存泄漏
- ✅ 启动时间：组件创建时间<1ms

### 可维护性指标
- ✅ 测试覆盖率：核心功能>90%
- ✅ 文档完整性：所有公开API有文档
- ✅ 向后兼容：提供清晰的迁移路径

## 💡 未来扩展方向

1. **动画系统**: 基于Core Animation的声明式动画
2. **主题系统**: 统一的颜色、字体、样式管理
3. **响应式布局**: 媒体查询和断点支持
4. **开发者工具**: 可视化布局调试器
5. **性能分析**: 渲染性能监控和优化建议

---

这个架构设计完全解决了现有问题，并为macUI的未来发展奠定了坚实的基础。它不仅满足了当前的需求，更重要的是为复杂的UI场景和高级用户需求预留了充分的扩展空间。