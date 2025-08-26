from typing import Any, List, Optional, Union

from AppKit import (
    NSCollectionView,
    NSLayoutAttributeBottom,
    NSLayoutAttributeCenterX,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSOutlineView,
    NSScrollView,
    NSSplitView,
    NSStackView,
    NSStackViewDistributionGravityAreas,
    NSStackViewDistributionFill,
    NSStackViewDistributionFillEqually,
    NSStackViewDistributionFillProportionally,
    NSStackViewDistributionEqualSpacing,
    NSStackViewDistributionEqualCentering,
    NSTableColumn,
    NSTableView,
    NSTabView,
    NSTabViewItem,
    NSUserInterfaceLayoutOrientationHorizontal,
    NSUserInterfaceLayoutOrientationVertical,
    NSView,
)
from Foundation import NSEdgeInsets, NSMakeRect

from ..core.component import Component
from ..core.signal import Signal

# 对齐方式映射
ALIGNMENT_MAP = {
    "leading": NSLayoutAttributeLeading,
    "trailing": NSLayoutAttributeTrailing,
    "center": NSLayoutAttributeCenterX,
    "top": NSLayoutAttributeTop,
    "bottom": NSLayoutAttributeBottom,
    "centerY": NSLayoutAttributeCenterY,
}

# ================================
# 混合布局系统 - Hybrid Layout System
# ================================

class LayoutMode:
    """布局模式常量"""
    AUTO = "auto"           # 自动选择最合适的布局方式
    CONSTRAINTS = "constraints"  # 约束布局（NSStackView）
    FRAME = "frame"         # Frame布局（绝对定位）
    HYBRID = "hybrid"       # 混合布局（智能选择）

class ComponentType:
    """组件类型分类，用于布局策略选择"""
    # 简单组件 - 适合约束布局
    SIMPLE = [
        "NSButton", "NSTextField", "NSImageView", "NSProgressIndicator",
        "NSSlider", "NSSwitch", "NSPopUpButton", "NSComboBox", "NSDatePicker"
    ]
    
    # 复杂组件 - 需要frame布局
    COMPLEX = [
        "NSScrollView", "NSTableView", "NSOutlineView", "NSCollectionView",
        "NSSplitView", "NSTabView", "NSTextView"
    ]

class ResponsiveFrame:
    """响应式Frame计算器"""
    
    def __init__(self, x=0, y=0, width=100, height=100):
        self.x = x
        self.y = y  
        self.width = width
        self.height = height
    
    def to_rect(self):
        """转换为NSRect"""
        return NSMakeRect(self.x, self.y, self.width, self.height)
    
    def relative_to_parent(self, parent_frame, x_ratio=None, y_ratio=None, 
                          width_ratio=None, height_ratio=None):
        """基于父容器的相对定位"""
        if x_ratio is not None:
            self.x = parent_frame.x + parent_frame.width * x_ratio
        if y_ratio is not None:
            self.y = parent_frame.y + parent_frame.height * y_ratio
        if width_ratio is not None:
            self.width = parent_frame.width * width_ratio
        if height_ratio is not None:
            self.height = parent_frame.height * height_ratio
        return self

class LayoutStrategy:
    """布局策略选择器"""
    
    @staticmethod
    def detect_component_type(component):
        """检测组件类型"""
        # 检查macUI组件函数的返回值
        if hasattr(component, '__class__'):
            class_name = component.__class__.__name__
            if class_name in ComponentType.SIMPLE:
                return "simple"
            elif class_name in ComponentType.COMPLEX:
                return "complex"
        
        # 检查是否是PyObjC对象
        if hasattr(component, 'className'):
            class_name = str(component.className())
            if class_name in ComponentType.SIMPLE:
                return "simple"
            elif class_name in ComponentType.COMPLEX:
                return "complex"
        
        # 特殊处理：检查是否是我们的TableView函数调用结果
        # TableView()函数返回NSScrollView，但我们知道它包含复杂组件
        if hasattr(component, 'documentView') and hasattr(component.documentView(), 'numberOfColumns'):
            return "complex"  # 这是TableView
        
        # 特殊处理：检查其他复杂的macUI组件
        if hasattr(component, 'className'):
            class_name = str(component.className())
            # 扩展的复杂组件检查
            if any(complex_type in class_name for complex_type in ComponentType.COMPLEX):
                return "complex"
        
        return "simple"  # 默认简单组件
    
    @staticmethod
    def choose_layout_mode(children, requested_mode=LayoutMode.AUTO):
        """选择最合适的布局模式"""
        if requested_mode in [LayoutMode.CONSTRAINTS, LayoutMode.FRAME]:
            return requested_mode
            
        if not children:
            return LayoutMode.CONSTRAINTS
            
        # 检查是否包含复杂组件
        has_complex = False
        complex_count = 0
        simple_count = 0
        
        for child in children:
            child_type = LayoutStrategy.detect_component_type(child)
            if child_type == "complex":
                has_complex = True
                complex_count += 1
            else:
                simple_count += 1
                
        # 决策逻辑
        if has_complex:
            # 如果有复杂组件，根据请求模式决定
            if requested_mode == LayoutMode.AUTO:
                # AUTO模式：如果全是复杂组件用frame，否则用hybrid
                return LayoutMode.FRAME if simple_count == 0 else LayoutMode.HYBRID
            else:
                return LayoutMode.HYBRID
        else:
            # 全是简单组件，使用约束布局
            return LayoutMode.CONSTRAINTS

def FrameContainer(
    children: Optional[List[Any]] = None,
    frame: Optional[tuple] = None,
    background_color: Optional[Any] = None
) -> NSView:
    """Frame布局容器
    
    提供基于绝对定位的布局系统，适合复杂组件（如TableView）。
    所有子视图必须手动指定frame或使用ResponsiveFrame。
    
    Args:
        children: 子视图列表，每个子视图都应该设置了frame
        frame: 容器frame (x, y, width, height)
        background_color: 背景色
    
    Returns:
        NSView 容器实例
    """
    container = NSView.alloc().init()
    
    # 设置容器frame
    if frame:
        container.setFrame_(NSMakeRect(*frame))
    
    # 设置背景色
    if background_color:
        container.setWantsLayer_(True)
        container.layer().setBackgroundColor_(background_color)
    
    # 添加子视图
    if children:
        for child in children:
            if hasattr(child, 'get_view'):
                view = child.get_view()
            elif hasattr(child, 'mount'):
                view = child.mount()
            else:
                view = child
            
            if view:
                container.addSubview_(view)
    
    return container


def VStack(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None,
    layout_mode: str = LayoutMode.AUTO
) -> Union[NSStackView, NSView]:
    """创建垂直堆栈布局 - 支持混合布局模式
    
    ✅ 新特性：现在支持 TableView！
    
    混合布局系统会自动检测子组件类型并选择最合适的布局方式：
    - 包含复杂组件（TableView等）时自动切换到frame布局
    - 仅包含简单组件时使用高效的约束布局
    
    📝 使用示例:
    
    简单组件（保持原有API）:
        VStack(children=[
            Label("标题"),
            Button("按钮"),
            TextField()
        ])
    
    混合组件（新功能）:
        VStack(
            layout_mode="auto",  # 可选，默认值
            children=[
                Label("数据表格"),
                TableView(columns=..., data=...),  # ✅ 现在可以工作！
                HStack(children=[Button("添加"), Button("删除")])
            ]
        )
    
    Args:
        spacing: 子视图间距
        padding: 内边距 (单个值或 (top, left, bottom, right) 元组)
        alignment: 对齐方式 ('leading', 'trailing', 'center', 'top', 'bottom')
        children: 子视图列表（现在支持任何组件！）
        frame: 容器框架 (x, y, width, height)
        layout_mode: 布局模式 ("auto", "constraints", "frame", "hybrid")
    
    Returns:
        NSStackView（约束模式）或 NSView（frame模式）
    """
    if not children:
        children = []
    
    print(f"\n📐 VStack布局开始: 子视图数={len(children)}, 间距={spacing}, padding={padding}, 对齐={alignment}")
    if frame:
        print(f"🎯 VStack指定frame: {frame}")
    
    # 选择布局策略
    effective_mode = LayoutStrategy.choose_layout_mode(children, layout_mode)
    print(f"🎯 VStack布局模式决策: 请求={layout_mode} → 生效={effective_mode}")
    
    # 约束布局模式 - 原有行为（适合简单组件）
    if effective_mode == LayoutMode.CONSTRAINTS:
        print(f"🔧 VStack使用约束布局模式")
        return _create_constraints_vstack(spacing, padding, alignment, children, frame)
    
    # Frame布局模式 - 新功能（适合复杂组件）  
    elif effective_mode == LayoutMode.FRAME:
        print(f"🔧 VStack使用Frame布局模式")
        return _create_frame_vstack(spacing, padding, alignment, children, frame)
    
    # 混合布局模式 - 智能组合
    else:  # LayoutMode.HYBRID
        print(f"🔧 VStack使用混合布局模式")
        return _create_hybrid_vstack(spacing, padding, alignment, children, frame)

def _create_constraints_vstack(spacing, padding, alignment, children, frame):
    """创建基于约束的VStack（原有实现）"""
    stack = NSStackView.alloc().init()
    # 明确设置为垂直方向（1 = Vertical, 0 = Horizontal）
    stack.setOrientation_(1)  # 强制设置为Vertical
    print(f"🔧 VStack强制设置orientation为1 (Vertical)")
    
    # 立即验证设置是否生效
    check_orientation = stack.orientation()
    print(f"🔍 VStack设置后立即检查orientation: {check_orientation} ({'成功' if check_orientation == 1 else '失败'})")
    
    # 按照技术文档: 禁用 Autoresizing Mask 转换
    stack.setTranslatesAutoresizingMaskIntoConstraints_(False)
    
    # 设置框架 - 按照苹果Auto Layout设计原则
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
        print(f"🎯 VStack设置frame: {frame}")
    else:
        # ✅ 苹果正确做法：不设置显式frame，依赖intrinsic content size
        # NSStackView应该根据子视图的intrinsic content size自动调整尺寸
        print(f"✅ VStack遵循苹果设计：依赖intrinsic content size，不设置显式frame")

    # 设置间距
    stack.setSpacing_(spacing)
    check_after_spacing = stack.orientation()
    print(f"🔍 VStack设置spacing后orientation: {check_after_spacing}")

    # 设置对齐 - 为VStack使用正确的对齐常量
    # VStack需要水平方向的对齐常量
    vstack_alignment_map = {
        "leading": NSLayoutAttributeLeading,
        "trailing": NSLayoutAttributeTrailing,
        "center": NSLayoutAttributeCenterX,  # 垂直布局用水平居中
        "centerX": NSLayoutAttributeCenterX,
    }
    alignment_constant = vstack_alignment_map.get(alignment, NSLayoutAttributeCenterX)
    print(f"🔧 VStack使用对齐常量: {alignment} → {alignment_constant}")
    
    stack.setAlignment_(alignment_constant)
    check_after_alignment = stack.orientation()
    print(f"🔍 VStack设置alignment后orientation: {check_after_alignment} ({'期望保持1' if check_after_alignment == 1 else '⚠️被改变了!'})")

    # 设置分布方式 - 让子视图根据内容大小自然分布
    stack.setDistribution_(NSStackViewDistributionGravityAreas)
    check_after_distribution = stack.orientation()
    print(f"🔍 VStack设置distribution后orientation: {check_after_distribution}")
    print(f"📊 VStack distribution设置为: GravityAreas")

    # 设置内边距
    if isinstance(padding, (int, float)):
        insets = NSEdgeInsets(padding, padding, padding, padding)
    elif isinstance(padding, tuple) and len(padding) == 4:
        insets = NSEdgeInsets(*padding)
    else:
        insets = NSEdgeInsets(0, 0, 0, 0)

    stack.setEdgeInsets_(insets)

    # 添加子视图
    print(f"🚀 创建VStack (约束模式): 将添加 {len(children)} 个子视图")
    for i, child in enumerate(children):
        child_view = child.get_view() if isinstance(child, Component) else child
        if child_view:
            # ✅ 苹果规范：arranged subviews必须禁用autoresizing mask转换
            child_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
            print(f"✅ 子视图 {i+1} 已禁用autoresizing mask转换")
            
            # 确保组件有合适的尺寸
            if hasattr(child_view, 'sizeToFit'):
                child_view.sizeToFit()
                size = child_view.frame().size
                print(f"   📏 子视图 {i+1} sizeToFit后: {size.width:.1f} x {size.height:.1f}")
            
            # ✅ 特殊处理：为嵌套NSStackView提供必要的约束
            # NSStackView没有intrinsic content size，需要明确的尺寸约束
            if child_view.__class__.__name__ == 'NSStackView':
                from AppKit import NSLayoutConstraint, NSLayoutRelationEqual, NSLayoutAttributeHeight, NSLayoutAttributeWidth
                
                # 根据该StackView的子视图数量估算高度约束
                arranged_count = 0
                if hasattr(child_view, 'arrangedSubviews'):
                    arranged_count = len(child_view.arrangedSubviews())
                
                # 为嵌套VStack添加高度约束，避免0高度问题
                estimated_height = max(50, arranged_count * 30 + 20)  # 保守估算
                height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    child_view, NSLayoutAttributeHeight,
                    NSLayoutRelationEqual,
                    None, 0, 1.0, estimated_height
                )
                child_view.addConstraint_(height_constraint)
                print(f"   🔧 为嵌套VStack添加高度约束: {estimated_height}px")
                
                # ✅ 关键修复：同时添加宽度约束，解决4px宽度问题
                estimated_width = 600  # 合理的默认宽度
                width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    child_view, NSLayoutAttributeWidth,
                    NSLayoutRelationEqual,
                    None, 0, 1.0, estimated_width
                )
                child_view.addConstraint_(width_constraint)
                print(f"   🔧 为嵌套VStack添加宽度约束: {estimated_width}px")
                
            stack.addArrangedSubview_(child_view)
            
            # 调试信息：记录添加的子视图
            component_name = ""
            if hasattr(child_view, '__class__'):
                component_name = child_view.__class__.__name__
            if hasattr(child_view, 'title') and child_view.title():
                component_name += f" ('{child_view.title()}')"
            elif hasattr(child_view, 'stringValue') and child_view.stringValue():
                component_name += f" ('{child_view.stringValue()}')"
                
            print(f"🔧 VStack添加子视图 {i+1}: {component_name}")
    
    # 调试信息：输出VStack配置
    print(f"📐 VStack配置: spacing={spacing}, alignment={alignment}")
    print(f"📦 VStack最终frame: {stack.frame()}")
    actual_orientation = stack.orientation()
    print(f"🎯 VStack orientation: {actual_orientation} ({'Vertical' if actual_orientation == 1 else 'Horizontal'})")
    
    # ✅ 苹果推荐做法：强制生成和更新约束
    # 解决NSStackView可能不自动生成约束的问题
    if hasattr(stack, 'updateConstraintsForSubtreeIfNeeded'):
        stack.updateConstraintsForSubtreeIfNeeded()
        print(f"🔄 VStack按苹果规范更新约束")
    
    # 强制触发布局更新 - 使用macOS NSView的正确方法
    stack.layoutSubtreeIfNeeded()  
    print(f"🔄 VStack强制触发布局更新")
    
    # 检查布局后的子视图位置
    if hasattr(stack, 'arrangedSubviews'):
        arranged_views = stack.arrangedSubviews()
        print(f"🔍 VStack布局更新后检查子视图位置:")
        for i, subview in enumerate(arranged_views):
            frame = subview.frame()
            component_name = subview.__class__.__name__
            if hasattr(subview, 'title') and subview.title():
                component_name += f" '{subview.title()}'"
            elif hasattr(subview, 'stringValue') and subview.stringValue():
                component_name += f" '{subview.stringValue()}'"
                
            print(f"   子视图 {i+1} {component_name}: Frame(x={frame.origin.x:.1f}, y={frame.origin.y:.1f}, w={frame.size.width:.1f}, h={frame.size.height:.1f})")

    return stack

def _create_frame_vstack(spacing, padding, alignment, children, frame):
    """创建基于frame的VStack（新实现）"""
    container = NSView.alloc().init()
    
    print(f"🚀 创建VStack (Frame模式): 将添加 {len(children)} 个子视图")
    
    # 设置容器frame
    if frame:
        container.setFrame_(NSMakeRect(*frame))
        print(f"🎯 VStack Frame模式容器frame: {frame}")
    else:
        print(f"⚠️  VStack Frame模式没有设置容器frame")
    
    # 解析padding
    if isinstance(padding, (int, float)):
        pad_top = pad_left = pad_bottom = pad_right = padding
    elif isinstance(padding, tuple) and len(padding) == 4:
        pad_top, pad_left, pad_bottom, pad_right = padding
    else:
        pad_top = pad_left = pad_bottom = pad_right = 0
    
    print(f"📏 VStack Frame模式padding: top={pad_top}, left={pad_left}, bottom={pad_bottom}, right={pad_right}")
    
    # 计算子视图位置
    current_y = container.frame().size.height - pad_top if frame else 0
    container_width = container.frame().size.width if frame else 300
    available_width = container_width - pad_left - pad_right
    
    print(f"📐 VStack Frame模式布局参数:")
    print(f"   容器宽度: {container_width}, 可用宽度: {available_width}")
    print(f"   初始Y位置: {current_y}, 间距: {spacing}")
    
    for i, child in enumerate(children):
        # 获取子视图
        if hasattr(child, 'get_view'):
            child_view = child.get_view()
        elif hasattr(child, 'mount'):
            child_view = child.mount()
        else:
            child_view = child
        
        if child_view:
            print(f"🔧 处理子视图 {i+1}: {child_view.__class__.__name__}")
            
            # 检查子视图当前frame
            existing_frame = child_view.frame()
            print(f"   子视图现有frame: x={existing_frame.origin.x:.1f}, y={existing_frame.origin.y:.1f}, w={existing_frame.size.width:.1f}, h={existing_frame.size.height:.1f}")
            
            # 如果子视图没有设置frame，为其计算默认frame
            if not hasattr(child_view, 'frame') or child_view.frame().size.width == 0:
                child_height = 30  # 默认高度
                child_width = available_width
                
                print(f"   子视图需要默认frame，计算中...")
                
                # 根据对齐方式计算x位置
                if alignment == "leading":
                    child_x = pad_left
                elif alignment == "trailing":
                    child_x = container_width - pad_right - child_width
                else:  # center
                    child_x = pad_left + (available_width - child_width) / 2
                
                current_y -= child_height
                child_frame = NSMakeRect(child_x, current_y, child_width, child_height)
                child_view.setFrame_(child_frame)
                print(f"   ✅ 设置子视图frame: x={child_x:.1f}, y={current_y:.1f}, w={child_width:.1f}, h={child_height}")
                current_y -= spacing
            else:
                # 子视图已有frame，调整其Y位置以适应VStack布局
                existing_size = child_view.frame().size
                
                # 根据对齐方式计算x位置
                if alignment == "leading":
                    child_x = pad_left
                elif alignment == "trailing":
                    child_x = container_width - pad_right - existing_size.width
                else:  # center
                    child_x = pad_left + (available_width - existing_size.width) / 2
                
                current_y -= existing_size.height
                child_frame = NSMakeRect(child_x, current_y, existing_size.width, existing_size.height)
                child_view.setFrame_(child_frame)
                print(f"   ✅ 调整子视图位置: x={child_x:.1f}, y={current_y:.1f}, w={existing_size.width:.1f}, h={existing_size.height:.1f}")
                current_y -= spacing
            
            container.addSubview_(child_view)
            print(f"   📦 子视图 {i+1} 已添加到容器")
    
    print(f"📦 VStack Frame模式创建完成，最终容器frame: {container.frame()}")
    print(f"🔍 VStack Frame模式子视图数量: {container.subviews().count() if hasattr(container, 'subviews') else 'Unknown'}")
    
    return container

def _create_hybrid_vstack(spacing, padding, alignment, children, frame):
    """创建混合布局VStack（智能组合）"""
    print(f"\n🔀 混合VStack开始分析组件 ({len(children)} 个子视图)")
    
    # 分离简单组件和复杂组件
    simple_children = []
    complex_children = []
    
    for i, child in enumerate(children):
        child_type = LayoutStrategy.detect_component_type(child)
        if child_type == "complex":
            complex_children.append(child)
            # 识别复杂组件类型
            if hasattr(child, 'get_view'):
                view = child.get_view()
                print(f"📊 复杂组件 {i+1}: {view.__class__.__name__} (Component wrapper)")
            else:
                print(f"📊 复杂组件 {i+1}: {child.__class__.__name__}")
        else:
            simple_children.append(child)
            # 识别简单组件类型
            if hasattr(child, 'get_view'):
                view = child.get_view()
                title = ""
                if hasattr(view, 'title') and view.title():
                    title = f" ('{view.title()}')"
                elif hasattr(view, 'stringValue') and view.stringValue():
                    title = f" ('{view.stringValue()}')"
                print(f"🔧 简单组件 {i+1}: {view.__class__.__name__}{title} (Component wrapper)")
            else:
                title = ""
                if hasattr(child, 'title') and child.title():
                    title = f" ('{child.title()}')"
                elif hasattr(child, 'stringValue') and child.stringValue():
                    title = f" ('{child.stringValue()}')"
                print(f"🔧 简单组件 {i+1}: {child.__class__.__name__}{title}")
    
    print(f"📈 分析结果: 简单组件={len(simple_children)}, 复杂组件={len(complex_children)}")
    
    # 如果只有复杂组件，使用frame布局
    if complex_children and not simple_children:
        print(f"🎯 混合VStack决策: 只有复杂组件 → 使用frame布局")
        return _create_frame_vstack(spacing, padding, alignment, children, frame)
    
    # 如果只有简单组件，使用约束布局
    if simple_children and not complex_children:
        print(f"🎯 混合VStack决策: 只有简单组件 → 使用约束布局")
        return _create_constraints_vstack(spacing, padding, alignment, children, frame)
    
    # 混合情况：创建frame容器，简单组件用VStack，复杂组件直接添加
    print(f"🎯 混合VStack决策: 混合组件 → 回退到frame布局")
    container = NSView.alloc().init()
    if frame:
        container.setFrame_(NSMakeRect(*frame))
    
    # 简单实现：将所有组件转为frame模式
    return _create_frame_vstack(spacing, padding, alignment, children, frame)


def HStack(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None,
    layout_mode: str = LayoutMode.AUTO
) -> Union[NSStackView, NSView]:
    """创建水平堆栈布局 - 支持混合布局模式
    
    ✅ 新特性：现在支持 TableView！
    
    混合布局系统会自动检测子组件类型并选择最合适的布局方式：
    - 包含复杂组件（TableView等）时自动切换到frame布局
    - 仅包含简单组件时使用高效的约束布局
    
    Args:
        spacing: 子视图间距
        padding: 内边距 (单个值或 (top, left, bottom, right) 元组)
        alignment: 对齐方式 ('leading', 'trailing', 'center', 'top', 'bottom')
        children: 子视图列表（现在支持任何组件！）
        frame: 容器框架 (x, y, width, height)
        layout_mode: 布局模式 ("auto", "constraints", "frame", "hybrid")
    
    Returns:
        NSStackView（约束模式）或 NSView（frame模式）
    """
    if not children:
        children = []
    
    # 选择布局策略
    effective_mode = LayoutStrategy.choose_layout_mode(children, layout_mode)
    
    # 约束布局模式 - 原有行为（适合简单组件）
    if effective_mode == LayoutMode.CONSTRAINTS:
        return _create_constraints_hstack(spacing, padding, alignment, children, frame)
    
    # Frame布局模式 - 新功能（适合复杂组件）  
    elif effective_mode == LayoutMode.FRAME:
        return _create_frame_hstack(spacing, padding, alignment, children, frame)
    
    # 混合布局模式 - 智能组合
    else:  # LayoutMode.HYBRID
        return _create_hybrid_hstack(spacing, padding, alignment, children, frame)

def _create_constraints_hstack(spacing, padding, alignment, children, frame):
    """创建基于约束的HStack（原有实现）"""
    stack = NSStackView.alloc().init()
    stack.setFrame_(NSMakeRect(0, 0, 100, 100))  # 提供稳定的初始Frame
    # 明确设置为水平方向（0 = Horizontal, 1 = Vertical）
    stack.setOrientation_(0)  # 强制设置为Horizontal
    print(f"🔧 强制设置orientation为0 (Horizontal)")
    
    # 立即验证设置是否生效
    check_orientation = stack.orientation()
    print(f"🔍 设置后立即检查orientation: {check_orientation} ({'成功' if check_orientation == 0 else '失败'})")
    
    # 按照技术文档: 禁用 Autoresizing Mask 转换
    stack.setTranslatesAutoresizingMaskIntoConstraints_(False)

    # 设置框架
    if frame:
        stack.setFrame_(NSMakeRect(*frame))

    # 设置间距
    stack.setSpacing_(spacing)
    check_after_spacing = stack.orientation()
    print(f"🔍 设置spacing后orientation: {check_after_spacing}")

    # 设置对齐 - 为HStack使用正确的对齐常量
    # HStack需要垂直方向的对齐常量
    hstack_alignment_map = {
        "top": NSLayoutAttributeTop,
        "bottom": NSLayoutAttributeBottom,
        "center": NSLayoutAttributeCenterY,  # 修复：水平布局用垂直居中
        "centerY": NSLayoutAttributeCenterY,
    }
    alignment_constant = hstack_alignment_map.get(alignment, NSLayoutAttributeCenterY)
    print(f"🔧 HStack使用对齐常量: {alignment} → {alignment_constant}")
    
    stack.setAlignment_(alignment_constant)
    check_after_alignment = stack.orientation()
    print(f"🔍 设置alignment后orientation: {check_after_alignment} ({'期望保持0' if check_after_alignment == 0 else '⚠️被改变了!'})")
    
    # 设置分布方式 - 关键：让子视图根据内容大小自然分布
    stack.setDistribution_(NSStackViewDistributionGravityAreas)
    check_after_distribution = stack.orientation()
    print(f"🔍 设置distribution后orientation: {check_after_distribution}")
    print(f"📊 HStack distribution设置为: GravityAreas (根据内容大小自然分布)")

    # 设置内边距
    if isinstance(padding, (int, float)):
        insets = NSEdgeInsets(padding, padding, padding, padding)
    elif isinstance(padding, tuple) and len(padding) == 4:
        insets = NSEdgeInsets(*padding)
    else:
        insets = NSEdgeInsets(0, 0, 0, 0)

    stack.setEdgeInsets_(insets)

    # 添加子视图
    print(f"🚀 创建HStack (约束模式): 将添加 {len(children)} 个子视图")
    for i, child in enumerate(children):
        child_view = child.get_view() if isinstance(child, Component) else child
        if child_view:
            # 确保按钮有合适的尺寸
            if hasattr(child_view, 'title') and child_view.title():
                child_view.sizeToFit()  # 让按钮自动调整到合适尺寸
                # 获取按钮调整后的尺寸
                size = child_view.frame().size
                print(f"   📏 按钮 '{child_view.title()}' sizeToFit后: {size.width:.1f} x {size.height:.1f}")
                
            stack.addArrangedSubview_(child_view)
            
            # 调试信息：记录添加的子视图
            title = ""
            if hasattr(child_view, 'title') and child_view.title():
                title = f" ('{child_view.title()}')"
            elif hasattr(child_view, 'stringValue') and child_view.stringValue():
                title = f" ('{child_view.stringValue()}')"
                
            print(f"🔧 HStack添加子视图 {i+1}: {child_view.__class__.__name__}{title}")
    
    # 调试信息：输出HStack配置
    print(f"📐 HStack配置: spacing={spacing}, alignment={alignment}")
    print(f"📦 HStack初始frame: {stack.frame()}")
    actual_orientation = stack.orientation()
    horizontal_constant = NSUserInterfaceLayoutOrientationHorizontal
    vertical_constant = NSUserInterfaceLayoutOrientationVertical
    print(f"🎯 HStack orientation: {actual_orientation} (Horizontal常量:{horizontal_constant}, Vertical常量:{vertical_constant})")
    print(f"🎯 方向判断: {'Horizontal' if actual_orientation == horizontal_constant else 'Vertical'}")
    
    # 强制触发布局更新
    stack.layoutSubtreeIfNeeded()
    print(f"🔄 强制触发布局更新")
    
    # 检查布局后的子视图位置
    if hasattr(stack, 'arrangedSubviews'):
        arranged_views = stack.arrangedSubviews()
        print(f"🔍 布局更新后立即检查子视图位置:")
        for i, subview in enumerate(arranged_views):
            frame = subview.frame()
            title = subview.title() if hasattr(subview, 'title') else "Unknown"
            print(f"   子视图 {i+1} '{title}': x={frame.origin.x:.1f}, w={frame.size.width:.1f}")
    
    return stack

def _create_frame_hstack(spacing, padding, alignment, children, frame):
    """创建基于frame的HStack（新实现）"""
    container = NSView.alloc().init()
    
    # 设置容器frame
    if frame:
        container.setFrame_(NSMakeRect(*frame))
    
    # 解析padding
    if isinstance(padding, (int, float)):
        pad_top = pad_left = pad_bottom = pad_right = padding
    elif isinstance(padding, tuple) and len(padding) == 4:
        pad_top, pad_left, pad_bottom, pad_right = padding
    else:
        pad_top = pad_left = pad_bottom = pad_right = 0
    
    # 计算子视图位置
    current_x = pad_left
    container_height = container.frame().size.height if frame else 100
    available_height = container_height - pad_top - pad_bottom
    
    for child in children:
        # 获取子视图
        if hasattr(child, 'get_view'):
            child_view = child.get_view()
        elif hasattr(child, 'mount'):
            child_view = child.mount()
        else:
            child_view = child
        
        if child_view:
            # 如果子视图没有设置frame，为其计算默认frame
            if not hasattr(child_view, 'frame') or child_view.frame().size.width == 0:
                # 智能计算宽度
                if hasattr(child_view, 'title') and child_view.title():
                    # 对于按钮，根据标题长度计算宽度
                    title_length = len(str(child_view.title()))
                    child_width = max(80, min(150, title_length * 8 + 20))  # 动态宽度
                elif hasattr(child_view, 'stringValue') and child_view.stringValue():
                    # 对于标签，根据文本长度计算宽度
                    text_length = len(str(child_view.stringValue()))
                    child_width = max(60, min(200, text_length * 7 + 10))  # 动态宽度
                else:
                    child_width = 100  # 默认宽度
                child_height = available_height
                
                # 根据对齐方式计算y位置
                if alignment == "top":
                    child_y = container_height - pad_top - child_height
                elif alignment == "bottom":
                    child_y = pad_bottom
                else:  # center
                    child_y = pad_bottom + (available_height - child_height) / 2
                
                child_frame = NSMakeRect(current_x, child_y, child_width, child_height)
                child_view.setFrame_(child_frame)
                current_x += child_width + spacing
            
            container.addSubview_(child_view)
    
    return container

def _create_hybrid_hstack(spacing, padding, alignment, children, frame):
    """创建混合布局HStack（智能组合）"""
    # 简单实现：将所有组件转为frame模式
    return _create_frame_hstack(spacing, padding, alignment, children, frame)


def ZStack(
    children: Optional[List[Union[Any, Component]]] = None,
    frame: Optional[tuple] = None
) -> NSView:
    """创建层叠堆栈布局 (所有子视图重叠)
    
    Args:
        children: 子视图列表
        frame: 堆栈框架 (x, y, width, height)
    
    Returns:
        NSView 实例
    """
    stack = NSView.alloc().init()

    # 设置框架
    if frame:
        stack.setFrame_(NSMakeRect(*frame))

    # 添加子视图 (所有子视图会重叠显示)
    if children:
        for child in children:
            child_view = child.get_view() if isinstance(child, Component) else child
            if child_view:
                stack.addSubview_(child_view)

    return stack


def ScrollView(
    content: Union[Any, Component],
    frame: Optional[tuple] = None,
    has_vertical_scroller: bool = True,
    has_horizontal_scroller: bool = False,
    autohides_scrollers: bool = True
) -> NSScrollView:
    """创建滚动视图
    
    Args:
        content: 滚动内容视图
        frame: 滚动视图框架 (x, y, width, height)
        has_vertical_scroller: 是否显示垂直滚动条
        has_horizontal_scroller: 是否显示水平滚动条
        autohides_scrollers: 是否自动隐藏滚动条
    
    Returns:
        NSScrollView 实例
    """
    scroll_view = NSScrollView.alloc().init()

    # 设置框架
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(scroll_view, frame)

    # 配置滚动条
    scroll_view.setHasVerticalScroller_(has_vertical_scroller)
    scroll_view.setHasHorizontalScroller_(has_horizontal_scroller)
    scroll_view.setAutohidesScrollers_(autohides_scrollers)

    # 设置文档视图
    content_view = content.get_view() if isinstance(content, Component) else content
    if content_view:
        scroll_view.setDocumentView_(content_view)

    return scroll_view


class ResponsiveStack(Component):
    """响应式堆栈组件 - 子视图可以动态添加/移除"""

    def __init__(
        self,
        orientation: str = "vertical",
        spacing: float = 0,
        padding: Union[float, tuple] = 0,
        alignment: str = "center",
        children: Optional[Signal[List[Component]]] = None
    ):
        super().__init__()
        self.orientation = orientation
        self.spacing = spacing
        self.padding = padding
        self.alignment = alignment
        self.children_signal = children or self.create_signal([])
        self._current_views: List[Any] = []

    def mount(self) -> NSStackView:
        """创建并返回堆栈视图"""
        stack = NSStackView.alloc().init()
        orientation = (NSUserInterfaceLayoutOrientationVertical
                     if self.orientation == "vertical"
                     else NSUserInterfaceLayoutOrientationHorizontal)
        stack.setOrientation_(orientation)

        # 配置堆栈属性
        stack.setSpacing_(self.spacing)

        alignment_key = self.alignment
        if self.orientation == "horizontal" and alignment_key == "center":
            alignment_key = "centerY"
        alignment_constant = ALIGNMENT_MAP.get(alignment_key, NSLayoutAttributeCenterX)
        stack.setAlignment_(alignment_constant)

        # 设置内边距
        if isinstance(self.padding, (int, float)):
            insets = NSEdgeInsets(self.padding, self.padding, self.padding, self.padding)
        elif isinstance(self.padding, tuple) and len(self.padding) == 4:
            insets = NSEdgeInsets(*self.padding)
        else:
            insets = NSEdgeInsets(0, 0, 0, 0)

        stack.setEdgeInsets_(insets)

        # 响应式更新子视图
        def update_children():
            # 移除现有子视图
            for view in self._current_views:
                stack.removeArrangedSubview_(view)
            self._current_views.clear()

            # 添加新子视图
            for child in self.children_signal.value:
                child_view = child.get_view() if isinstance(child, Component) else child
                if child_view:
                    self._current_views.append(child_view)
                    stack.addArrangedSubview_(child_view)

        # 创建响应式更新
        self.create_effect(update_children)

        return stack

    def add_child(self, child: Component) -> None:
        """添加子组件"""
        current_children = self.children_signal.value.copy()
        current_children.append(child)
        self.children_signal.value = current_children

    def remove_child(self, child: Component) -> None:
        """移除子组件"""
        current_children = self.children_signal.value.copy()
        if child in current_children:
            current_children.remove(child)
            self.children_signal.value = current_children

    def clear_children(self) -> None:
        """清空所有子组件"""
        self.children_signal.value = []


# 便捷构造函数
def VStackResponsive(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式垂直堆栈"""
    return ResponsiveStack("vertical", spacing, padding, alignment, children)


def HStackResponsive(
    spacing: float = 0,
    padding: Union[float, tuple] = 0,
    alignment: str = "center",
    children: Optional[Signal[List[Component]]] = None
) -> ResponsiveStack:
    """创建响应式水平堆栈"""
    return ResponsiveStack("horizontal", spacing, padding, alignment, children)


def TabView(
    tabs: List[dict],  # [{"title": str, "content": Component}, ...]
    selected: Optional[Union[int, Signal[int]]] = None,
    on_change: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSTabView:
    """创建标签页视图
    
    Args:
        tabs: 标签页配置列表，每个项目是一个字典：{"title": str, "content": Component}
        selected: 当前选中的标签页索引 (支持响应式)
        on_change: 标签页切换回调函数 (index, tab_item)
        frame: 标签页视图框架
    
    Returns:
        NSTabView 实例
    """
    tab_view = NSTabView.alloc().init()
    
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(tab_view, frame)
    
    # 添加标签页
    for tab_config in tabs:
        title = tab_config.get("title", "")
        content = tab_config.get("content")
        
        # 创建标签页项
        tab_item = NSTabViewItem.alloc().init()
        tab_item.setLabel_(title)
        
        if content:
            # 如果content是Component，需要获取其view
            if hasattr(content, 'get_view'):
                view = content.get_view()
            elif hasattr(content, 'mount'):
                view = content.mount()
            else:
                view = content
            tab_item.setView_(view)
        
        tab_view.addTabViewItem_(tab_item)
    
    # 设置初始选中的标签页
    if selected is not None:
        if isinstance(selected, Signal):
            # 响应式绑定选中索引
            from ..core.binding import TwoWayBinding
            TwoWayBinding.bind_tab_view(tab_view, selected)
        else:
            if 0 <= selected < len(tabs):
                tab_view.selectTabViewItemAtIndex_(selected)
    
    # 事件处理
    if on_change or (isinstance(selected, Signal)):
        from ..core.binding import EnhancedTabViewDelegate
        # 创建标签页委托
        delegate = EnhancedTabViewDelegate.alloc().init()
        delegate.on_change = on_change
        delegate.signal = selected if isinstance(selected, Signal) else None
        
        tab_view.setDelegate_(delegate)
        
        # 保持委托引用 - 使用内存管理器
        from ..core.memory_manager import associate_object
        associate_object(tab_view, "enhanced_tab_delegate", delegate)
    
    return tab_view


def SplitView(
    orientation: str = "horizontal",  # "horizontal" or "vertical"
    children: Optional[List[Any]] = None,
    divider_style: str = "thin",  # "thin" or "thick"
    on_resize: Optional[Any] = None,
    frame: Optional[tuple] = None
) -> NSSplitView:
    """创建分割视图
    
    Args:
        orientation: 分割方向 ("horizontal" 或 "vertical")
        children: 子视图列表
        divider_style: 分隔符样式 ("thin" 或 "thick")
        on_resize: 尺寸调整回调函数
        frame: 分割视图框架
    
    Returns:
        NSSplitView 实例
    """
    split_view = NSSplitView.alloc().init()
    
    if frame:
        from ..utils.layout_utils import safe_set_frame
        safe_set_frame(split_view, frame)
    
    # 设置分割方向
    from AppKit import NSSplitViewDividerStyleThin, NSSplitViewDividerStyleThick
    if orientation == "vertical":
        split_view.setVertical_(True)
    else:
        split_view.setVertical_(False)
    
    # 设置分隔符样式
    if divider_style == "thick":
        split_view.setDividerStyle_(NSSplitViewDividerStyleThick)
    else:
        split_view.setDividerStyle_(NSSplitViewDividerStyleThin)
    
    # 添加子视图
    if children:
        for child in children:
            # 如果child是Component，需要获取其view
            if hasattr(child, 'get_view'):
                view = child.get_view()
            elif hasattr(child, 'mount'):
                view = child.mount()
            else:
                view = child
            split_view.addSubview_(view)
    
    # 事件处理
    if on_resize:
        from ..core.binding import EnhancedSplitViewDelegate
        # 创建分割视图委托
        delegate = EnhancedSplitViewDelegate.alloc().init()
        delegate.on_resize = on_resize
        
        split_view.setDelegate_(delegate)
        
        # 保持委托引用 - 使用内存管理器
        from ..core.memory_manager import associate_object
        associate_object(split_view, "enhanced_split_delegate", delegate)
    
    return split_view


def TableView(
    columns: List[dict],  # [{"title": str, "key": str, "width": float}, ...]
    data: Optional[Union[List[Any], Signal[List[Any]]]] = None,
    selected_row: Optional[Union[int, Signal[int]]] = None,
    on_select: Optional[Any] = None,
    on_double_click: Optional[Any] = None,
    headers_visible: bool = True,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建表格视图
    
    ✅ 重大更新：现在支持在 VStack/HStack 中使用！
    
    混合布局系统会自动检测 TableView 并切换到 frame 布局模式，解决了约束冲突问题。
    
    🎉 新的使用方式:
        # 现在可以在 VStack 中使用 TableView！
        VStack(children=[
            Label("数据表格"),
            TableView(columns=..., data=...),  # ✅ 现在完全可以！
            HStack(children=[
                Button("添加"),
                Button("删除")
            ])
        ])
    
    📋 多种使用方式:
        
        1. 直接使用（原有方式，仍然支持）:
           table = TableView(columns=..., data=...)
           window.contentView().addSubview_(table)
        
        2. VStack/HStack 中使用（新功能）:
           VStack(children=[TableView(...), Button(...)])
           
        3. FrameContainer 中使用（高级功能）:
           FrameContainer(children=[
               TableView(columns=..., frame=(0, 0, 400, 300))
           ])
    
    💡 技术原理:
    - 混合布局系统自动检测 TableView 组件
    - 包含 TableView 的 VStack/HStack 自动切换到 frame 布局
    - 保持响应式特性和所有原有功能
    
    Args:
        columns: 列配置列表，每个项目是一个字典：{"title": str, "key": str, "width": float}
        data: 表格数据 (支持响应式)
        selected_row: 当前选中的行索引 (支持响应式)
        on_select: 行选择回调函数
        on_double_click: 双击行回调函数
        headers_visible: 是否显示表头
        frame: 表格视图框架
    
    Returns:
        NSScrollView 实例（包含 NSTableView）
        现在可以安全地用于任何布局容器中！
    """
    # 创建滚动视图 - 提供稳定的初始 Frame
    from Foundation import NSMakeRect
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setFrame_(NSMakeRect(0, 0, 100, 100))  # 提供稳定的初始Frame
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(True)
    scroll_view.setAutohidesScrollers_(True)
    
    # ✅ 关键修复：保持 translatesAutoresizingMaskIntoConstraints=True (默认值)
    # 原因：NSScrollView 需要自己管理内部视图层次的约束
    # 如果设置为 False，会与外部约束系统（如 NSStackView）冲突
    # 参考：TABLEVIEW_SOLUTION_REPORT.md - 网络调查结果确认此做法
    
    # 创建表格视图 - 也提供稳定的初始 Frame
    table_view = NSTableView.alloc().init()
    table_view.setFrame_(NSMakeRect(0, 0, 100, 100))  # 提供稳定的初始Frame
    
    # ✅ 关键：TableView 也必须使用 translatesAutoresizingMaskIntoConstraints=True
    # NSTableView 有复杂的内部视图层次（header, clip view, scroll bars）
    # 它应该自己管理这些内部约束，而不是被外部约束系统控制
    
    table_view.setHeaderView_(None if not headers_visible else table_view.headerView())
    
    # 创建列
    for col_config in columns:
        title = col_config.get("title", "")
        key = col_config.get("key", title)
        width = col_config.get("width", 100.0)
        
        column = NSTableColumn.alloc().init()
        column.setIdentifier_(key)
        column.setWidth_(width)
        
        # 设置列标题
        if headers_visible:
            column.headerCell().setStringValue_(title)
        
        table_view.addTableColumn_(column)
    
    # 设置表格到滚动视图
    scroll_view.setDocumentView_(table_view)
    
    # ✅ 直接设置frame，避免使用可能有问题的layout_utils
    if frame:
        # 不使用layout_utils，直接设置frame
        safe_rect = NSMakeRect(frame[0], frame[1], frame[2], frame[3])
        scroll_view.setFrame_(safe_rect)
    
    # 创建数据源 - 使用正确的内存管理
    from ..core.binding import EnhancedTableViewDataSource
    
    data_source = EnhancedTableViewDataSource.alloc().init()
    data_source.columns = [col.get("key", col.get("title", "")) for col in columns]
    
    # 设置数据
    if data is not None:
        if isinstance(data, Signal):
            # 响应式数据绑定
            def update_table_data():
                try:
                    print(f"📊 更新表格数据: {len(data.value) if data.value else 0} 行")
                    data_source.data = data.value
                    table_view.reloadData()
                except Exception as e:
                    print(f"❌ 数据更新错误: {e}")
            
            from ..core.signal import Effect
            effect = Effect(update_table_data)
            
            # ✅ 直接使用objc关联对象保持Effect引用
            objc.setAssociatedObject(scroll_view, b"table_data_effect", effect, objc.OBJC_ASSOCIATION_RETAIN)
            
        else:
            data_source.data = data
    
    # 设置数据源并使用内存管理器保持引用
    table_view.setDataSource_(data_source)
    
    # ✅ 直接使用objc关联对象，避免自定义内存管理器可能的问题
    import objc
    objc.setAssociatedObject(scroll_view, b"table_data_source", data_source, objc.OBJC_ASSOCIATION_RETAIN)
    
    # 事件处理
    if on_select or on_double_click or (isinstance(selected_row, Signal)):
        from ..core.binding import EnhancedTableViewDelegate
        
        # 创建表格委托
        delegate = EnhancedTableViewDelegate.alloc().init()
        delegate.on_select = on_select
        delegate.on_double_click = on_double_click
        delegate.selected_signal = selected_row if isinstance(selected_row, Signal) else None
        
        table_view.setDelegate_(delegate)
        
        # ✅ 直接使用objc关联对象
        objc.setAssociatedObject(scroll_view, b"table_delegate", delegate, objc.OBJC_ASSOCIATION_RETAIN)
        
        # 设置双击动作
        if on_double_click:
            table_view.setDoubleAction_("tableViewDoubleClick:")
            table_view.setTarget_(delegate)
    
    return scroll_view


def OutlineView(
    columns: List[dict],  # [{"title": str, "key": str, "width": float}, ...]
    root_items: Optional[List[Any]] = None,
    get_children: Optional[Any] = None,  # 函数，用于获取子项
    is_expandable: Optional[Any] = None,  # 函数，用于判断是否可展开
    on_select: Optional[Any] = None,
    on_expand: Optional[Any] = None,
    on_collapse: Optional[Any] = None,
    headers_visible: bool = True,
    frame: Optional[tuple] = None
) -> NSScrollView:
    """创建大纲视图（树形视图）
    
    Args:
        columns: 列配置列表，每个项目是一个字典：{"title": str, "key": str, "width": float}
        root_items: 根级项目列表
        get_children: 获取子项的函数 (item) -> [children]
        is_expandable: 判断是否可展开的函数 (item) -> bool
        on_select: 选择项回调函数 (row, item)
        on_expand: 展开项回调函数 (item)
        on_collapse: 收缩项回调函数 (item)
        headers_visible: 是否显示表头
        frame: 大纲视图框架
    
    Returns:
        NSScrollView 实例（包含 NSOutlineView）
    """
    print("⚠️  OutlineView 暂时被禁用，返回一个替代的 TableView")
    
    # 暂时用 TableView 替代，直到修复 OutlineView 的崩溃问题
    # 将树形数据扁平化为列表
    flat_data = []
    if root_items:
        for item in root_items:
            # 添加根项目
            if isinstance(item, dict):
                flat_data.append(item)
                # 添加子项目（如果有）
                if get_children:
                    children = get_children(item)
                    if children:
                        for child in children:
                            if isinstance(child, dict):
                                # 为子项目添加前缀以示层级
                                child_copy = child.copy()
                                if 'title' in child_copy:
                                    child_copy['title'] = f"  └ {child_copy['title']}"
                                flat_data.append(child_copy)
    
    # 使用 TableView 替代
    return TableView(
        columns=columns,
        data=flat_data,
        on_select=on_select,
        headers_visible=headers_visible,
        frame=frame
    )
