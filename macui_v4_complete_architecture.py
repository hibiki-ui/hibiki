#!/usr/bin/env python3
"""
macUI v4.0 完整架构设计
基于管理器模式的分层架构，支持复杂UI场景和高级特性
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union, Callable, Any, TypeVar, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
import weakref
from AppKit import NSView, NSWindow

T = TypeVar("T")

# ================================
# 1. 核心数据结构和枚举
# ================================

class Position(Enum):
    """定位类型"""
    STATIC = "static"        # 默认，参与flex/grid布局
    RELATIVE = "relative"    # 相对定位
    ABSOLUTE = "absolute"    # 绝对定位
    FIXED = "fixed"          # 固定定位（相对视口）
    STICKY = "sticky"        # 粘性定位

class ZLayer(Enum):
    """预定义Z层级"""
    BACKGROUND = -100        # 背景层
    CONTENT = 0              # 内容层
    FLOATING = 1000          # 悬浮层（tooltip, dropdown）
    MODAL = 2000             # 模态层（dialog, modal）
    OVERLAY = 3000           # 覆盖层（loading, notification）
    SYSTEM = 9000            # 系统层（debug tools）

class OverflowBehavior(Enum):
    """溢出行为"""
    VISIBLE = "visible"      # 可见（默认）
    HIDDEN = "hidden"        # 隐藏
    SCROLL = "scroll"        # 滚动
    AUTO = "auto"           # 自动

# ================================
# 2. 管理器系统
# ================================

class ViewportManager:
    """视口管理器 - 处理视口相关计算和事件"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._window_ref: Optional[weakref.ReferenceType] = None
        self._viewport_size = (800, 600)  # 默认尺寸
        self._scale_factor = 1.0
        
    def set_window(self, window: NSWindow):
        """设置关联的窗口"""
        self._window_ref = weakref.ref(window)
        self._update_viewport_info()
    
    def get_viewport_size(self) -> Tuple[float, float]:
        """获取视口尺寸"""
        self._update_viewport_info()
        return self._viewport_size
    
    def get_scale_factor(self) -> float:
        """获取缩放因子（Retina支持）"""
        return self._scale_factor
    
    def _update_viewport_info(self):
        """更新视口信息"""
        if self._window_ref and self._window_ref():
            window = self._window_ref()
            frame = window.frame()
            self._viewport_size = (frame.size.width, frame.size.height)
            self._scale_factor = window.backingScaleFactor()

class LayerManager:
    """层级管理器 - 处理Z-Index和视图层次"""
    
    def __init__(self):
        self._layer_registry: Dict[int, List[weakref.ReferenceType]] = {}
        self._next_auto_z = 1
        
    def register_component(self, component: 'UIComponent', z_index: Union[int, ZLayer]):
        """注册组件到指定层级"""
        z_value = z_index.value if isinstance(z_index, ZLayer) else z_index
        
        if z_value not in self._layer_registry:
            self._layer_registry[z_value] = []
            
        # 使用弱引用防止循环引用
        self._layer_registry[z_value].append(weakref.ref(component))
        
        # 清理已失效的引用
        self._cleanup_dead_references(z_value)
        
    def get_auto_z_index(self, layer: ZLayer) -> int:
        """获取自动分配的z-index"""
        base_z = layer.value
        return base_z + self._next_auto_z
        
    def _cleanup_dead_references(self, z_value: int):
        """清理失效的弱引用"""
        if z_value in self._layer_registry:
            self._layer_registry[z_value] = [
                ref for ref in self._layer_registry[z_value] if ref() is not None
            ]

class PositioningManager:
    """定位管理器 - 处理绝对定位和固定定位"""
    
    def __init__(self, viewport_manager: ViewportManager):
        self.viewport_manager = viewport_manager
        
    def calculate_absolute_frame(self, component: 'UIComponent') -> Tuple[float, float, float, float]:
        """计算绝对定位的frame"""
        style = component.style
        
        # 获取定位上下文
        if style.position == Position.FIXED:
            context_size = self.viewport_manager.get_viewport_size()
        else:
            context_size = self._get_parent_context_size(component)
            
        # 计算位置和尺寸
        x = self._resolve_position_value(style.left, context_size[0], 0)
        y = self._resolve_position_value(style.top, context_size[1], 0)
        w = self._resolve_size_value(style.width, context_size[0], 100)
        h = self._resolve_size_value(style.height, context_size[1], 30)
        
        return x, y, w, h
        
    def _get_parent_context_size(self, component: 'UIComponent') -> Tuple[float, float]:
        """获取父容器的上下文尺寸"""
        # 简化实现，实际应该查找positioned父元素
        return self.viewport_manager.get_viewport_size()
        
    def _resolve_position_value(self, value, context_size: float, default: float) -> float:
        """解析位置值"""
        if value is None:
            return default
        # 实现单位解析逻辑
        return float(value) if isinstance(value, (int, float)) else default
        
    def _resolve_size_value(self, value, context_size: float, default: float) -> float:
        """解析尺寸值"""  
        if value is None:
            return default
        return float(value) if isinstance(value, (int, float)) else default

class TransformManager:
    """变换管理器 - 处理CSS变换效果"""
    
    @staticmethod
    def apply_transforms(view: NSView, style: 'ComponentStyle'):
        """应用变换效果到NSView"""
        if not hasattr(view, 'layer') or not view.layer():
            return
            
        layer = view.layer()
        
        # 应用透明度
        layer.setOpacity_(style.opacity)
        
        # 应用变换矩阵
        if any([style.scale != (1.0, 1.0), style.rotation != 0, style.translation != (0, 0)]):
            from Foundation import NSAffineTransform
            transform = NSAffineTransform.transform()
            
            # 缩放
            if style.scale != (1.0, 1.0):
                transform.scaleXBy_yBy_(style.scale[0], style.scale[1])
            
            # 旋转
            if style.rotation != 0:
                transform.rotateByDegrees_(style.rotation)
                
            # 平移
            if style.translation != (0, 0):
                transform.translateXBy_yBy_(style.translation[0], style.translation[1])
                
            layer.setAffineTransform_(transform)

class ScrollManager:
    """滚动管理器 - 处理滚动容器"""
    
    def __init__(self):
        self._scroll_containers: List[weakref.ReferenceType] = []
        
    def create_scroll_view(self, content_view: NSView, 
                          overflow: OverflowBehavior = OverflowBehavior.AUTO) -> NSView:
        """创建滚动容器"""
        if overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
            from AppKit import NSScrollView
            scroll_view = NSScrollView.alloc().init()
            scroll_view.setDocumentView_(content_view)
            scroll_view.setHasVerticalScroller_(True)
            scroll_view.setHasHorizontalScroller_(overflow == OverflowBehavior.AUTO)
            scroll_view.setAutohidesScrollers_(overflow == OverflowBehavior.AUTO)
            
            self._scroll_containers.append(weakref.ref(scroll_view))
            return scroll_view
        
        return content_view

class MaskManager:
    """遮罩管理器 - 处理裁剪和遮罩效果"""
    
    @staticmethod  
    def apply_clip_mask(view: NSView, clip_rect: Optional[Tuple[float, float, float, float]] = None):
        """应用裁剪遮罩"""
        if not clip_rect or not hasattr(view, 'layer'):
            return
            
        layer = view.layer()
        if layer:
            from Foundation import NSBezierPath, NSMakeRect
            x, y, w, h = clip_rect
            clip_path = NSBezierPath.bezierPathWithRect_(NSMakeRect(x, y, w, h))
            layer.setMask_(clip_path)

# ================================
# 3. 样式系统
# ================================

@dataclass
class ComponentStyle:
    """组件样式定义 - 涵盖所有布局和视觉属性"""
    
    # 定位和层级
    position: Position = Position.STATIC
    z_index: Union[int, ZLayer] = ZLayer.CONTENT
    
    # 坐标（用于非static定位）
    top: Optional[Union[int, float, str]] = None
    right: Optional[Union[int, float, str]] = None
    bottom: Optional[Union[int, float, str]] = None
    left: Optional[Union[int, float, str]] = None
    
    # 尺寸
    width: Optional[Union[int, float, str]] = None
    height: Optional[Union[int, float, str]] = None
    min_width: Optional[Union[int, float, str]] = None
    min_height: Optional[Union[int, float, str]] = None
    max_width: Optional[Union[int, float, str]] = None
    max_height: Optional[Union[int, float, str]] = None
    
    # Flexbox属性
    flex_direction: str = "column"
    justify_content: str = "flex-start"
    align_items: str = "stretch"
    flex_grow: float = 0
    flex_shrink: float = 1
    flex_basis: Optional[Union[int, float, str]] = None
    
    # 间距
    margin: Union[int, float, str, None] = None
    padding: Union[int, float, str, None] = None
    gap: Optional[Union[int, float, str]] = None
    
    # 视觉效果
    opacity: float = 1.0
    visible: bool = True
    overflow: OverflowBehavior = OverflowBehavior.VISIBLE
    
    # 变换
    scale: Tuple[float, float] = (1.0, 1.0)
    rotation: float = 0.0
    translation: Tuple[float, float] = (0.0, 0.0)
    
    # 裁剪
    clip_rect: Optional[Tuple[float, float, float, float]] = None

# ================================
# 4. 分层API接口设计
# ================================

class HighLevelLayoutAPI:
    """高层API - 简化接口，覆盖85-90%常见场景"""
    
    def __init__(self, component: 'UIComponent'):
        self.component = component
        
    # ================================
    # 常见定位场景
    # ================================
    
    def center(self, z_index: Optional[Union[int, ZLayer]] = None) -> 'UIComponent':
        """居中定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.left = "50%"
        self.component.style.top = "50%"
        self.component.style.translation = (-0.5, -0.5)
        if z_index: self.component.style.z_index = z_index
        return self.component
        
    def top_left(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'UIComponent':
        """左上角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.left = margin
        self.component.style.top = margin
        if z_index: self.component.style.z_index = z_index
        return self.component
        
    def top_right(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'UIComponent':
        """右上角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.right = margin
        self.component.style.top = margin
        if z_index: self.component.style.z_index = z_index
        return self.component
        
    def bottom_right(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'UIComponent':
        """右下角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.right = margin
        self.component.style.bottom = margin
        if z_index: self.component.style.z_index = z_index
        return self.component
        
    def fullscreen(self, z_index: Union[int, ZLayer] = ZLayer.OVERLAY) -> 'UIComponent':
        """全屏覆盖"""
        self.component.style.position = Position.FIXED
        self.component.style.top = 0
        self.component.style.right = 0
        self.component.style.bottom = 0
        self.component.style.left = 0
        self.component.style.z_index = z_index
        return self.component
    
    # ================================
    # 预设场景
    # ================================
    
    def modal(self, width: int = 400, height: int = 300) -> 'UIComponent':
        """模态对话框预设"""
        self.center(z_index=ZLayer.MODAL)
        self.component.size(width, height)
        return self.component
        
    def tooltip(self, offset_x: int = 0, offset_y: int = -30) -> 'UIComponent':
        """工具提示预设"""
        self.component.style.position = Position.RELATIVE
        self.component.style.left = offset_x
        self.component.style.top = offset_y
        self.component.style.z_index = ZLayer.FLOATING
        return self.component
        
    def dropdown(self, offset_y: int = 5) -> 'UIComponent':
        """下拉菜单预设"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.top = offset_y
        self.component.style.z_index = ZLayer.FLOATING
        return self.component
        
    def floating_button(self, corner: str = "bottom-right", margin: int = 20) -> 'UIComponent':
        """悬浮按钮预设"""
        if corner == "bottom-right":
            self.bottom_right(margin=margin, z_index=ZLayer.FLOATING)
        elif corner == "top-right":
            self.top_right(margin=margin, z_index=ZLayer.FLOATING)
        # 可扩展其他角落
        return self.component
    
    # ================================
    # 便捷样式方法
    # ================================
    
    def size(self, width: Optional[int] = None, height: Optional[int] = None) -> 'UIComponent':
        """设置尺寸"""
        if width: self.component.style.width = width
        if height: self.component.style.height = height
        return self.component
        
    def fade(self, opacity: float) -> 'UIComponent':
        """设置透明度"""
        self.component.style.opacity = max(0.0, min(1.0, opacity))
        return self.component

class LowLevelLayoutAPI:
    """低层API - 直接暴露底层能力，给高级用户使用"""
    
    def __init__(self, component: 'UIComponent'):
        self.component = component
        
    def set_position(self, position: Position, **coords) -> 'UIComponent':
        """直接设置定位"""
        self.component.style.position = position
        for key, value in coords.items():
            if hasattr(self.component.style, key):
                setattr(self.component.style, key, value)
        return self.component
        
    def set_flex_properties(self, direction: str = None, justify: str = None, 
                           align: str = None, grow: float = None, shrink: float = None) -> 'UIComponent':
        """直接设置Flexbox属性"""
        if direction: self.component.style.flex_direction = direction
        if justify: self.component.style.justify_content = justify
        if align: self.component.style.align_items = align
        if grow is not None: self.component.style.flex_grow = grow
        if shrink is not None: self.component.style.flex_shrink = shrink
        return self.component
        
    def set_transform(self, scale: Tuple[float, float] = None, rotation: float = None,
                     translation: Tuple[float, float] = None) -> 'UIComponent':
        """直接设置变换"""
        if scale: self.component.style.scale = scale
        if rotation is not None: self.component.style.rotation = rotation
        if translation: self.component.style.translation = translation
        return self.component
        
    def apply_stretchable_layout(self, **stretchable_props) -> 'UIComponent':
        """直接使用Stretchable布局引擎"""
        # 直接传递给Stretchable引擎
        # 实现细节...
        return self.component
        
    def apply_raw_appkit(self, configurator: Callable[[NSView], None]) -> 'UIComponent':
        """直接访问AppKit NSView"""
        # 允许高级用户直接操作NSView
        if self.component._nsview:
            configurator(self.component._nsview)
        else:
            # 延迟执行，在mount后调用
            self.component._raw_configurators = getattr(self.component, '_raw_configurators', [])
            self.component._raw_configurators.append(configurator)
        return self.component

# ================================
# 5. 组件架构
# ================================

class Component(ABC):
    """核心组件抽象基类"""
    
    def __init__(self):
        """🏗️ CORE METHOD: Component initialization"""
        # 响应式状态管理
        self._signals: List = []
        self._computed: List = []
        self._effects: List = []
        self._bindings: List[Callable[[], None]] = []
        
        # 生命周期
        self._mounted = False
        self._cleanup_callbacks: List[Callable[[], None]] = []
        
    @abstractmethod
    def mount(self) -> NSView:
        """🚀 CORE METHOD: Component mounting phase"""
        pass

class UIComponent(Component):
    """UI组件基类 - 集成所有管理器和API"""
    
    def __init__(self, style: Optional[ComponentStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: UI component initialization"""
        super().__init__()
        
        # 样式系统
        self.style = style or ComponentStyle(**style_kwargs)
        
        # 管理器引用
        self.viewport_manager = ViewportManager()
        self.layer_manager = LayerManager()
        self.positioning_manager = PositioningManager(self.viewport_manager)
        self.transform_manager = TransformManager()
        self.scroll_manager = ScrollManager()
        self.mask_manager = MaskManager()
        
        # API接口
        self.layout = HighLevelLayoutAPI(self)
        self.advanced = LowLevelLayoutAPI(self)
        
        # 视图状态
        self._nsview: Optional[NSView] = None
        self._raw_configurators: List[Callable[[NSView], None]] = []
    
    def size(self, width: Optional[int] = None, height: Optional[int] = None) -> 'UIComponent':
        """便捷的尺寸设置方法"""
        if width: self.style.width = width
        if height: self.style.height = height
        return self
        
    def mount(self) -> NSView:
        """🚀 CORE METHOD: UI component mounting"""
        if self._nsview is None:
            # 1. 创建NSView
            self._nsview = self._create_nsview()
            
            # 2. 注册到层级管理器
            self.layer_manager.register_component(self, self.style.z_index)
            
            # 3. 应用定位和布局
            self._apply_positioning_and_layout()
            
            # 4. 应用变换效果
            self.transform_manager.apply_transforms(self._nsview, self.style)
            
            # 5. 应用裁剪和遮罩
            self.mask_manager.apply_clip_mask(self._nsview, self.style.clip_rect)
            
            # 6. 处理滚动容器
            if self.style.overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
                self._nsview = self.scroll_manager.create_scroll_view(self._nsview, self.style.overflow)
            
            # 7. 执行原始配置器
            for configurator in self._raw_configurators:
                configurator(self._nsview)
        
        return self._nsview
    
    @abstractmethod
    def _create_nsview(self) -> NSView:
        """创建具体的NSView - 子类实现"""
        pass
        
    def _apply_positioning_and_layout(self):
        """应用定位和布局"""
        if self.style.position in [Position.ABSOLUTE, Position.FIXED]:
            x, y, w, h = self.positioning_manager.calculate_absolute_frame(self)
            from Foundation import NSMakeRect
            self._nsview.setFrame_(NSMakeRect(x, y, w, h))
        else:
            # 使用Stretchable布局引擎
            self._apply_stretchable_layout()
    
    def _apply_stretchable_layout(self):
        """应用Stretchable布局"""
        # 集成现有的Stretchable布局引擎
        # 实现细节...
        pass

# ================================
# 6. 具体组件示例
# ================================

class Label(UIComponent):
    """标签组件"""
    
    def __init__(self, text: str, style: Optional[ComponentStyle] = None, **style_kwargs):
        super().__init__(style, **style_kwargs)
        self.text = text
    
    def _create_nsview(self) -> NSView:
        from AppKit import NSTextField
        label = NSTextField.alloc().init()
        label.setStringValue_(self.text)
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setSelectable_(False)
        return label

class Button(UIComponent):
    """按钮组件"""
    
    def __init__(self, title: str, on_click: Optional[Callable] = None,
                 style: Optional[ComponentStyle] = None, **style_kwargs):
        super().__init__(style, **style_kwargs)
        self.title = title
        self.on_click = on_click
    
    def _create_nsview(self) -> NSView:
        from AppKit import NSButton, NSButtonTypeMomentaryPushIn
        button = NSButton.alloc().init()
        button.setTitle_(self.title)
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        return button

class Modal(UIComponent):
    """模态对话框组件"""
    
    def __init__(self, content: UIComponent, width: int = 400, height: int = 300):
        style = ComponentStyle(width=width, height=height)
        super().__init__(style)
        self.content = content
        
        # 使用高层API快速设置模态样式
        self.layout.modal(width, height)
    
    def _create_nsview(self) -> NSView:
        # 创建背景遮罩
        overlay = NSView.alloc().init()
        overlay.setWantsLayer_(True)
        overlay.layer().setBackgroundColor_((0, 0, 0, 0.5))  # 半透明黑色
        
        # 添加内容视图
        content_view = self.content.mount()
        overlay.addSubview_(content_view)
        
        return overlay

# ================================
# 7. 使用示例
# ================================

if __name__ == "__main__":
    print("macUI v4.0 完整架构演示\n")
    
    # 高层API使用示例
    print("🎨 高层API示例:")
    
    # 1. 简单的居中模态框
    modal_button = Button("确认").layout.modal(300, 200)
    print(f"模态按钮: position={modal_button.style.position}, z_index={modal_button.style.z_index}")
    
    # 2. 工具提示
    tooltip = Label("这是提示信息").layout.tooltip()
    print(f"工具提示: position={tooltip.style.position}, z_index={tooltip.style.z_index}")
    
    # 3. 悬浮按钮
    fab = Button("💬").layout.floating_button("bottom-right")
    print(f"悬浮按钮: position={fab.style.position}, z_index={fab.style.z_index}")
    
    print()
    print("🔧 低层API示例:")
    
    # 4. 高级用户直接操作
    advanced_label = Label("高级标签")
    advanced_label.advanced.set_position(
        Position.ABSOLUTE, 
        left=100, top=200
    )
    advanced_label.advanced.set_transform(
        scale=(1.2, 1.2), 
        rotation=15
    )
    print(f"高级标签: scale={advanced_label.style.scale}, rotation={advanced_label.style.rotation}")
    
    # 5. 直接访问AppKit
    raw_button = Button("原始按钮")
    raw_button.advanced.apply_raw_appkit(
        lambda view: print(f"直接配置NSView: {type(view).__name__}")
    )
    
    print("\n✅ 完整架构演示完成！")
    print("\n📚 架构总结:")
    print("- 管理器系统：分离关注点，易于测试和扩展")
    print("- 分层API：高层简化常见场景，低层开放高级能力") 
    print("- 场景覆盖：模态框、悬浮层、工具提示、固定元素等")
    print("- 渐进式增强：从简单到复杂，满足不同用户需求")