#!/usr/bin/env python3
"""
macUI v4.0 组件核心架构
双层组件架构：Component (抽象基类) + UIComponent (具体基类)
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union, Callable, Any, TypeVar, Tuple
from AppKit import NSView
from Foundation import NSMakeRect

# 导入样式和管理器系统
import sys
import os
sys.path.append(os.path.dirname(__file__))
from styles import ComponentStyle, StylePresets
from managers import (
    ManagerFactory, ViewportManager, LayerManager, PositioningManager,
    TransformManager, ScrollManager, MaskManager, Position, OverflowBehavior
)
from reactive import Signal, Computed, Effect, create_signal, create_computed, create_effect

T = TypeVar("T")

# ================================
# 1. Component - 核心抽象基类
# ================================

class Component(ABC):
    """macUI组件核心抽象基类
    
    职责：
    - 响应式状态管理 (Signal, Computed, Effect) 
    - 核心生命周期方法 (mount, cleanup)
    - 基础组件功能 (绑定、子组件管理)
    
    这是所有macUI组件的根基类，提供最基础的功能。
    类似于PyTorch的nn.Module，所有组件都必须实现mount方法。
    """
    
    # 类似PyTorch的 forward: Callable[..., Any] 模式
    mount: Callable[[], NSView]
    
    def __init__(self):
        """🏗️ CORE METHOD: Component initialization phase"""
        # 响应式状态管理
        self._signals: List = []
        self._computed: List = [] 
        self._effects: List = []
        self._bindings: List[Callable[[], None]] = []
        
        # 组件生命周期
        self._mounted = False
        self._cleanup_callbacks: List[Callable[[], None]] = []
        
        # 子组件管理
        self._children: List['Component'] = []
        
        print(f"🔧 Component({self.__class__.__name__}) 初始化")
    
    @abstractmethod 
    def mount(self) -> NSView:
        """🚀 CORE METHOD: Component mounting phase
        
        创建并返回NSView，所有子类必须实现。
        类似于PyTorch的forward方法 - 必须被子类重写。
        
        Returns:
            NSView: 组件的根视图
            
        Raises:
            NotImplementedError: 如果子类未实现此方法
        """
        raise NotImplementedError(
            f"{self.__class__.__module__}.{self.__class__.__qualname__} is "
            "missing the required \"mount\" function. "
            "All macUI components must implement this core method."
        )
    
    # ================================
    # 响应式状态管理方法
    # ================================
    
    def create_signal(self, initial_value: T) -> Signal[T]:
        """创建组件作用域的Signal
        
        集成完整的macUI响应式系统
        """
        signal = create_signal(initial_value)
        self._signals.append(signal)
        print(f"🔧 Component({self.__class__.__name__}): 创建Signal[{id(signal)}] = {initial_value}")
        return signal
        
    def create_computed(self, fn: Callable[[], T]) -> Computed[T]:
        """创建计算属性
        
        集成完整的Computed系统
        """
        computed = create_computed(fn)
        self._computed.append(computed)
        print(f"🔧 Component({self.__class__.__name__}): 创建Computed[{id(computed)}]")
        return computed
        
    def create_effect(self, fn: Callable[[], Optional[Callable[[], None]]]) -> Effect:
        """创建副作用
        
        集成完整的Effect系统
        """
        effect = create_effect(fn)
        self._effects.append(effect)
        print(f"🔧 Component({self.__class__.__name__}): 创建Effect[{id(effect)}]")
        return effect
    
    # ================================
    # 子组件管理
    # ================================
    
    def add_child(self, child: 'Component') -> None:
        """添加子组件"""
        if child not in self._children:
            self._children.append(child)
            print(f"➕ 添加子组件: {child.__class__.__name__}")
    
    def remove_child(self, child: 'Component') -> None:
        """移除子组件"""
        if child in self._children:
            child.cleanup()
            self._children.remove(child)
            print(f"➖ 移除子组件: {child.__class__.__name__}")
    
    # ================================
    # 生命周期管理
    # ================================
    
    def on_cleanup(self, callback: Callable[[], None]) -> None:
        """添加清理回调"""
        self._cleanup_callbacks.append(callback)
    
    def cleanup(self) -> None:
        """清理组件资源"""
        print(f"🧹 清理组件: {self.__class__.__name__}")
        
        # 清理所有绑定
        for cleanup_fn in self._bindings:
            try:
                cleanup_fn()
            except Exception as e:
                print(f"⚠️ 绑定清理错误: {e}")
        self._bindings.clear()
        
        # 清理所有副作用
        for effect in self._effects:
            try:
                if hasattr(effect, 'cleanup'):
                    effect.cleanup()
            except Exception as e:
                print(f"⚠️ Effect清理错误: {e}")
        self._effects.clear()
        
        # 清理子组件
        for child in self._children:
            try:
                child.cleanup()
            except Exception as e:
                print(f"⚠️ 子组件清理错误: {e}")
        self._children.clear()
        
        # 调用自定义清理回调
        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"⚠️ 清理回调错误: {e}")
        self._cleanup_callbacks.clear()
        
        # 清理布局节点
        try:
            from .layout import get_layout_engine
            engine = get_layout_engine()
            engine.cleanup_component(self)
        except Exception as e:
            print(f"⚠️ 布局节点清理错误: {e}")
        
        # 清空状态
        self._signals.clear()
        self._computed.clear()
        self._mounted = False

# ================================
# 2. UIComponent - UI组件基类
# ================================

class UIComponent(Component):
    """macUI UI组件基类
    
    职责：
    - 完整的布局API (Flexbox + Grid + 绝对定位)
    - Z-Index和层级管理
    - NSView集成和布局应用
    - 变换和动画支持
    - 管理器系统集成
    
    这是所有UI组件的直接基类，提供完整的布局和视觉功能。
    """
    
    def __init__(self, style: Optional[ComponentStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: UI component initialization
        
        Args:
            style: 完整的布局样式对象
            **style_kwargs: 样式快捷参数（会被合并到style中）
        """
        # 初始化基类
        super().__init__()
        
        # 样式系统初始化
        if style:
            self.style = style
        else:
            self.style = ComponentStyle(**style_kwargs)
            
        # 管理器引用 - 使用工厂模式获取单例
        self.viewport_manager = ManagerFactory.get_viewport_manager()
        self.layer_manager = ManagerFactory.get_layer_manager()
        self.positioning_manager = ManagerFactory.get_positioning_manager()
        self.transform_manager = ManagerFactory.get_transform_manager()
        self.scroll_manager = ManagerFactory.get_scroll_manager()
        self.mask_manager = ManagerFactory.get_mask_manager()
        
        # 视图状态
        self._nsview: Optional[NSView] = None
        self._raw_configurators: List[Callable[[NSView], None]] = []
        self._parent_container: Optional['UIComponent'] = None
        
        # 分层API接口 - 延迟导入避免循环依赖
        from api import HighLevelLayoutAPI, LowLevelLayoutAPI
        self.layout = HighLevelLayoutAPI(self)
        self.advanced = LowLevelLayoutAPI(self)
        
        print(f"🎨 UIComponent({self.__class__.__name__}) 初始化完成")
    
    # ================================
    # 核心mount流程
    # ================================
    
    def mount(self) -> NSView:
        """🚀 CORE METHOD: UI component mounting
        
        完整的UI组件挂载流程：
        1. 创建NSView（子类实现）
        2. 注册到层级管理器
        3. 应用定位和布局
        4. 应用变换效果
        5. 应用裁剪和遮罩
        6. 处理滚动容器
        7. 执行原始配置器
        
        Returns:
            NSView: 完全配置好的根视图
        """
        if self._nsview is None:
            print(f"🚀 开始挂载组件: {self.__class__.__name__}")
            
            # 1. 创建NSView - 由子类实现
            self._nsview = self._create_nsview()
            print(f"✅ NSView创建完成: {type(self._nsview).__name__}")
            
            # 2. 注册到层级管理器
            self.layer_manager.register_component(self, self.style.z_index)
            
            # 3. 应用定位和布局
            self._apply_positioning_and_layout()
            
            # 4. 应用变换效果
            self.transform_manager.apply_transforms(self._nsview, self.style)
            
            # 5. 应用裁剪和遮罩
            if self.style.clip_rect:
                self.mask_manager.apply_clip_mask(self._nsview, self.style.clip_rect)
            
            # 6. 处理滚动容器
            if self.style.overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
                original_view = self._nsview
                self._nsview = self.scroll_manager.create_scroll_view(original_view, self.style.overflow)
                print(f"📜 滚动容器已创建")
            
            # 7. 执行原始配置器
            for configurator in self._raw_configurators:
                try:
                    configurator(self._nsview)
                except Exception as e:
                    print(f"⚠️ 原始配置器执行失败: {e}")
            
            # 8. 设置基础样式
            self._apply_basic_style()
            
            print(f"✅ 组件挂载完成: {self.__class__.__name__}")
        
        return self._nsview
    
    @abstractmethod
    def _create_nsview(self) -> NSView:
        """创建NSView实例 - 子类必须实现
        
        专门的方法用于创建具体的NSView类型
        (NSButton, NSTextField, NSImageView等)
        
        Returns:
            NSView: 创建的视图实例
        """
        raise NotImplementedError("子类必须实现 _create_nsview 方法")
    
    # ================================
    # 布局和定位实现
    # ================================
    
    def _apply_positioning_and_layout(self):
        """应用定位和布局"""
        
        if not self._nsview:
            return
            
        position = self.style.position
        
        if position in [Position.ABSOLUTE, Position.FIXED]:
            # 绝对定位和固定定位
            self._apply_absolute_positioning()
        elif position == Position.RELATIVE:
            # 相对定位：先正常布局，再应用偏移
            self._apply_relative_positioning()
        else:
            # 静态定位：使用Stretchable布局引擎
            self._apply_stretchable_layout()
    
    def _apply_absolute_positioning(self):
        """应用绝对定位"""
        try:
            x, y, w, h = self.positioning_manager.calculate_absolute_frame(self)
            frame = NSMakeRect(x, y, w, h)
            self._nsview.setFrame_(frame)
            
            # 禁用Auto Layout
            self._nsview.setTranslatesAutoresizingMaskIntoConstraints_(True)
            
            print(f"📍 绝对定位已应用: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
            
        except Exception as e:
            print(f"❌ 绝对定位应用失败: {e}")
            # v4应该完全依赖布局引擎，不提供回退方案
            raise e
    
    def _apply_relative_positioning(self):
        """应用相对定位"""
        try:
            # 先使用Stretchable计算正常位置
            self._apply_stretchable_layout()
            
            # 再应用相对偏移
            offset_x, offset_y = self.positioning_manager.calculate_relative_offset(self)
            
            if offset_x != 0 or offset_y != 0:
                current_frame = self._nsview.frame()
                new_frame = NSMakeRect(
                    current_frame.origin.x + offset_x,
                    current_frame.origin.y + offset_y,
                    current_frame.size.width,
                    current_frame.size.height
                )
                self._nsview.setFrame_(new_frame)
                
                print(f"🔄 相对定位偏移已应用: ({offset_x:.1f}, {offset_y:.1f})")
                
        except Exception as e:
            print(f"⚠️ 相对定位应用失败: {e}")
    
    def _apply_stretchable_layout(self):
        """应用v4 Stretchable布局"""
        try:
            # 使用v4独立布局引擎
            from .layout import get_layout_engine
            engine = get_layout_engine()
            
            # 检查是否是容器根节点
            has_children = hasattr(self, 'children') and len(getattr(self, 'children', [])) > 0
            has_no_parent = getattr(self, '_parent_container', None) is None
            is_root_container = has_children and has_no_parent
            
            # 检查是否是子组件
            is_child_component = getattr(self, '_parent_container', None) is not None
            
            # 调试信息
            print(f"🔍 {self.__class__.__name__} 布局检查: has_children={has_children}, has_no_parent={has_no_parent}, is_root_container={is_root_container}, is_child_component={is_child_component}")
            
            # 只有根容器和独立组件才创建布局节点，子组件完全跳过
            if is_root_container:
                # 为根容器创建布局节点
                layout_node = engine.get_node_for_component(self)
                if not layout_node:
                    layout_node = engine.create_node_for_component(self)
                # 计算可用空间
                available_size = self._get_available_size_from_parent()
                
                # 计算整个布局树
                layout_result = engine.compute_layout_for_component(self, available_size)
                
                if layout_result:
                    # 应用根容器布局
                    self._apply_layout_result(layout_result)
                    print(f"🔧 准备应用子组件布局: {self.__class__.__name__}")
                    
                    # 递归应用所有子组件的布局 - 使用Stretchable计算结果
                    self._apply_children_layout(engine)
                    
                    print(f"📐 v4根容器布局已应用: {self.__class__.__name__} -> ({layout_result.x:.1f}, {layout_result.y:.1f}, {layout_result.width:.1f}x{layout_result.height:.1f})")
                    return True
                else:
                    raise ValueError(f"v4根容器布局计算失败: {self.__class__.__name__}")
            elif is_child_component:
                # 子组件：完全跳过布局处理，等父容器处理
                print(f"📐 v4子组件跳过独立布局: {self.__class__.__name__}")
                return True
            else:
                # 独立组件（非容器子组件）：创建独立布局节点
                layout_node = engine.get_node_for_component(self)
                if not layout_node:
                    layout_node = engine.create_node_for_component(self)
                
                # 计算独立布局
                available_size = self._get_available_size_from_parent()
                layout_result = engine.compute_layout_for_component(self, available_size)
                
                if layout_result:
                    self._apply_layout_result(layout_result)
                    print(f"📐 v4独立组件布局已应用: {self.__class__.__name__}")
                    return True
                else:
                    raise ValueError(f"v4独立组件布局计算失败: {self.__class__.__name__}")
                
        except Exception as e:
            print(f"❌ v4布局应用失败: {e}")
            import traceback
            traceback.print_exc()
            # v4应该完全依赖Stretchable布局引擎，不提供回退方案
            raise e
    
    def _get_available_size_from_parent(self) -> Optional[Tuple[float, float]]:
        """从父容器获取可用尺寸"""
        if self._parent_container and hasattr(self._parent_container, '_nsview'):
            parent_view = self._parent_container._nsview
            if parent_view:
                frame = parent_view.frame()
                return (frame.size.width, frame.size.height)
        
        # 使用视口管理器的尺寸
        try:
            viewport_size = self.viewport_manager.get_viewport_size()
            return viewport_size
        except:
            # 默认视口尺寸
            return (800, 600)
    
    def _apply_layout_result(self, layout_result):
        """应用布局结果到NSView"""
        from Foundation import NSMakeRect
        frame = NSMakeRect(
            layout_result.x, 
            layout_result.y,
            layout_result.width, 
            layout_result.height
        )
        self._nsview.setFrame_(frame)
        
        # 根据布局类型决定是否使用Auto Layout
        if self.style.position in [Position.ABSOLUTE, Position.FIXED]:
            # 绝对定位禁用Auto Layout
            self._nsview.setTranslatesAutoresizingMaskIntoConstraints_(True)
        else:
            # Flex布局可以与Auto Layout协同
            self._nsview.setTranslatesAutoresizingMaskIntoConstraints_(False)
    
    def _apply_children_layout_from_stretchable(self, engine):
        """从Stretchable重建树应用子组件布局（简化版本）"""
        print(f"🔧 开始应用子组件布局: {self.__class__.__name__}")
        if not hasattr(self, 'children'):
            print(f"🔧 {self.__class__.__name__} 没有children属性")
            return
        print(f"🔧 {self.__class__.__name__} 有 {len(self.children)} 个子组件")
        
        # 简化版本：直接为每个子组件设置合理的布局
        try:
            y_offset = 0
            x_offset = 0
            
            for i, child in enumerate(self.children):
                if hasattr(child, '_nsview') and child._nsview:
                    try:
                        # 根据组件类型设置基本尺寸
                        if child.__class__.__name__ == 'Label':
                            width, height = 300, 30
                        elif child.__class__.__name__ == 'Button':
                            width, height = 120, 35
                        else:
                            width, height = 200, 30
                        
                        # 应用简单的垂直堆叠布局
                        child._apply_layout_result(type('LayoutResult', (), {
                            'x': x_offset, 'y': y_offset, 'width': width, 'height': height,
                            'content_width': width, 'content_height': height,
                            'compute_time': 0
                        })())
                        
                        print(f"📐 v4子组件简单布局已应用: {child.__class__.__name__} -> ({x_offset}, {y_offset}, {width}x{height})")
                        
                        # 更新偏移
                        y_offset += height + 10  # 10px 间距
                            
                    except Exception as e:
                        print(f"⚠️ v4子组件简单布局应用异常: {child.__class__.__name__} - {e}")
                        child._apply_fallback_frame()
                        
        except Exception as e:
            print(f"⚠️ 子组件简单布局应用整体异常: {e}")
            # 不再抛出异常，避免崩溃
    
    def _apply_simple_children_layout(self):
        """安全的简单子组件布局应用"""
        if not hasattr(self, 'children') or not self.children:
            return
            
        y = 20  # 从顶部20px开始
        for child in self.children:
            if hasattr(child, '_nsview') and child._nsview:
                # 设置简单的垂直堆叠布局
                if child.__class__.__name__ == 'Label':
                    w, h = 400, 30
                elif child.__class__.__name__ == 'Button':
                    w, h = 150, 35
                elif child.__class__.__name__ == 'Container':
                    w, h = 500, 200  # Container更大一些
                else:
                    w, h = 300, 30
                    
                # 直接设置frame，避免复杂的LayoutResult
                from AppKit import NSMakeRect
                frame = NSMakeRect(20, y, w, h)  # x=20px 左边距
                child._nsview.setFrame_(frame)
                print(f"✅ 简单布局: {child.__class__.__name__} -> (20, {y}, {w}x{h})")
                
                y += h + 15  # 15px间距

    def _apply_children_layout(self, engine):
        """递归应用子组件的布局"""
        if not hasattr(self, 'children'):
            return
        
        for child in self.children:
            if hasattr(child, '_nsview') and child._nsview:
                # 获取子组件的布局节点
                child_node = engine.get_node_for_component(child)
                if child_node:
                    try:
                        print(f"🔍 开始处理子组件布局: {child.__class__.__name__}")
                        print(f"🔍 child_node类型: {type(child_node)}")
                        print(f"🔍 child_node._stretchable_node类型: {type(child_node._stretchable_node)}")
                        
                        # 获取子组件的布局结果
                        box = child_node._stretchable_node.get_box()
                        print(f"🔍 获取到box: {box}")
                        x, y, width, height = box.x, box.y, box.width, box.height
                        print(f"🔍 布局坐标: x={x}, y={y}, w={width}, h={height}")
                        
                        # 应用到子组件的NSView
                        child._apply_layout_result(type('LayoutResult', (), {
                            'x': x, 'y': y, 'width': width, 'height': height
                        })())
                        
                        print(f"📐 v4子组件布局已应用: {child.__class__.__name__} -> ({x:.1f}, {y:.1f}, {width:.1f}x{height:.1f})")
                        
                        # 递归处理子组件的子组件
                        if hasattr(child, '_apply_children_layout'):
                            child._apply_children_layout(engine)
                            
                    except Exception as e:
                        import traceback
                        print(f"⚠️ 子组件布局应用失败: {child.__class__.__name__} - {e}")
                        print(f"⚠️ 异常详情: {type(e).__name__}: {str(e)}")
                        traceback.print_exc()
                        child._apply_fallback_frame()
    
    def _resolve_size_value(self, length_value, default: float) -> float:
        """解析尺寸值为像素"""
        if length_value is None:
            return default
        if hasattr(length_value, 'value'):
            return float(length_value.value)
        if isinstance(length_value, (int, float)):
            return float(length_value)
        return default
    
    # ================================
    # 基础样式应用
    # ================================
    
    def _apply_basic_style(self):
        """应用基础样式"""
        if not self._nsview:
            return
            
        # 设置透明度
        if self.style.opacity != 1.0:
            self._nsview.setAlphaValue_(self.style.opacity)
            
        # 设置可见性
        if not self.style.visible:
            self._nsview.setHidden_(True)
            
        print(f"🎨 基础样式已应用: opacity={self.style.opacity}, visible={self.style.visible}")
    
    # ================================
    # 便捷方法
    # ================================
    
    def size(self, width: Optional[Union[int, float]] = None, 
             height: Optional[Union[int, float]] = None) -> 'UIComponent':
        """便捷的尺寸设置方法"""
        from styles import px
        
        if width is not None:
            self.style.width = px(width)
        if height is not None:
            self.style.height = px(height)
            
        return self
    
    def opacity(self, value: float) -> 'UIComponent':
        """便捷的透明度设置方法"""
        self.style.opacity = max(0.0, min(1.0, value))
        return self
    
    def get_view(self) -> Optional[NSView]:
        """获取NSView（如果已挂载）"""
        return self._nsview
    
    def is_mounted(self) -> bool:
        """检查组件是否已挂载"""
        return self._nsview is not None

# ================================
# 3. 容器组件基类
# ================================

class Container(UIComponent):
    """容器组件 - 用于管理子组件的特殊UI组件
    
    提供子组件的自动挂载和布局管理功能。
    """
    
    def __init__(self, children: Optional[List[UIComponent]] = None,
                 style: Optional[ComponentStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: Container initialization
        
        Args:
            children: 子组件列表
            style: 容器样式
            **style_kwargs: 样式快捷参数
        """
        super().__init__(style, **style_kwargs)
        self.children = children or []
        
        # 将children添加为子组件
        for child in self.children:
            self.add_child(child)
    
    def _create_nsview(self) -> NSView:
        """🚀 创建容器NSView并挂载所有子组件"""
        container = NSView.alloc().init()
        
        print(f"📦 Container创建，子组件数: {len(self.children)}")
        
        # 建立v4布局树关系
        try:
            from .layout import get_layout_engine
            engine = get_layout_engine()
            
            # 为容器创建布局节点
            engine.create_node_for_component(self)
            
            # 挂载所有子组件并建立布局关系
            for i, child in enumerate(self.children):
                try:
                    # 先设置父子关系，防止子组件创建独立布局节点
                    child._parent_container = self
                    
                    # 为子组件创建并添加到v4布局树
                    engine.add_child_relationship(self, child, i)
                    
                    # 挂载子组件（此时子组件知道自己是容器的子组件）
                    child_view = child.mount()
                    container.addSubview_(child_view)
                    
                    print(f"  ├─ 子组件 {i+1}: {child.__class__.__name__} 已添加到容器和v4布局树")
                except Exception as e:
                    print(f"  ├─ ⚠️ 子组件 {i+1} 挂载失败: {e}")
        except Exception as e:
            print(f"❌ Container v4布局树构建失败: {e}")
            import traceback
            traceback.print_exc()
            # v4应该完全依赖Stretchable布局引擎，不提供回退方案
            raise e
                    
        return container
    
    def add_child_component(self, child: UIComponent):
        """添加新的子组件"""
        self.children.append(child)
        self.add_child(child)
        
        # 如果容器已挂载，立即挂载新子组件
        if self._nsview and hasattr(child, 'mount'):
            try:
                # 设置父子关系
                child._parent_container = self
                
                # 添加到布局系统
                from .layout import get_layout_engine
                engine = get_layout_engine()
                engine.add_child_relationship(self, child, len(self.children) - 1)
                
                # 挂载NSView
                child_view = child.mount()
                self._nsview.addSubview_(child_view)
                
                # 重新计算布局
                self._update_layout()
                
                print(f"➕ 动态添加子组件: {child.__class__.__name__}")
            except Exception as e:
                print(f"⚠️ 动态添加子组件失败: {e}")

    def remove_child_component(self, child: UIComponent):
        """移除子组件"""
        if child in self.children:
            try:
                # 从NSView移除
                if self._nsview and hasattr(child, '_nsview') and child._nsview:
                    child._nsview.removeFromSuperview()
                
                # 从布局系统移除
                from .layout import get_layout_engine
                engine = get_layout_engine()
                engine.remove_child_relationship(self, child)
                
                # 从children列表移除
                self.children.remove(child)
                self.remove_child(child)
                
                # 清理子组件资源
                child.cleanup()
                
                # 重新计算布局
                self._update_layout()
                
                print(f"➖ 动态移除子组件: {child.__class__.__name__}")
            except Exception as e:
                print(f"⚠️ 动态移除子组件失败: {e}")

    def clear_children(self):
        """清空所有子组件"""
        if not self.children:
            return
            
        try:
            # 批量移除所有子组件
            children_copy = self.children.copy()  # 避免在迭代中修改列表
            for child in children_copy:
                self.remove_child_component(child)
                
            print(f"🧹 清空容器所有子组件")
        except Exception as e:
            print(f"⚠️ 清空子组件失败: {e}")

    def replace_child_component(self, old_child: UIComponent, new_child: UIComponent):
        """替换子组件"""
        if old_child not in self.children:
            print(f"⚠️ 要替换的子组件不存在: {old_child.__class__.__name__}")
            return
            
        try:
            # 获取原子组件的索引
            index = self.children.index(old_child)
            
            # 移除旧组件
            self.remove_child_component(old_child)
            
            # 在相同位置插入新组件
            self.children.insert(index, new_child)
            self.add_child(new_child)
            
            # 如果容器已挂载，立即挂载新组件
            if self._nsview and hasattr(new_child, 'mount'):
                # 设置父子关系
                new_child._parent_container = self
                
                # 添加到布局系统
                from .layout import get_layout_engine
                engine = get_layout_engine()
                engine.add_child_relationship(self, new_child, index)
                
                # 挂载NSView
                new_child_view = new_child.mount()
                self._nsview.addSubview_(new_child_view)
                
                # 重新计算布局
                self._update_layout()
            
            print(f"🔄 替换子组件: {old_child.__class__.__name__} -> {new_child.__class__.__name__}")
        except Exception as e:
            print(f"⚠️ 替换子组件失败: {e}")

    def set_children(self, new_children: List[UIComponent]):
        """批量设置子组件（替换所有现有子组件）"""
        try:
            # 先清空现有子组件
            self.clear_children()
            
            # 添加新的子组件
            for child in new_children:
                self.add_child_component(child)
                
            print(f"🔄 批量设置子组件: {len(new_children)}个组件")
        except Exception as e:
            print(f"⚠️ 批量设置子组件失败: {e}")

    def _update_layout(self):
        """更新布局（在子组件变化后调用）"""
        if self._nsview:
            try:
                from .layout import get_layout_engine
                engine = get_layout_engine()
                
                # 重新计算布局
                if hasattr(self, '_layout_node') and self._layout_node:
                    engine.apply_layout(self)
                    
                print(f"🔄 容器布局已更新")
            except Exception as e:
                print(f"⚠️ 更新布局失败: {e}")

# ================================
# 4. 测试代码
# ================================

if __name__ == "__main__":
    print("macUI v4.0 组件架构测试\n")
    
    # 初始化管理器系统
    ManagerFactory.initialize_all()
    
    # 测试基础组件
    class TestLabel(UIComponent):
        def __init__(self, text: str):
            super().__init__(width=200, height=30)
            self.text = text
        
        def _create_nsview(self) -> NSView:
            from AppKit import NSTextField
            label = NSTextField.alloc().init()
            label.setStringValue_(self.text)
            label.setBezeled_(False)
            label.setDrawsBackground_(False)
            label.setEditable_(False)
            return label
    
    class TestButton(UIComponent):
        def __init__(self, title: str):
            super().__init__(width=120, height=32)
            self.title = title
        
        def _create_nsview(self) -> NSView:
            from AppKit import NSButton, NSButtonTypeMomentaryPushIn
            button = NSButton.alloc().init()
            button.setTitle_(self.title)
            button.setButtonType_(NSButtonTypeMomentaryPushIn)
            return button
    
    print("🧪 组件创建和挂载测试:")
    
    # 创建组件
    label = TestLabel("Hello World")
    button = TestButton("Click Me")
    
    # 测试挂载
    label_view = label.mount()
    button_view = button.mount()
    
    print(f"Label视图: {type(label_view).__name__}")
    print(f"Button视图: {type(button_view).__name__}")
    
    # 测试容器
    print("\n📦 容器组件测试:")
    container = Container(
        children=[label, button],
        style=ComponentStyle(width=400, height=200)
    )
    
    container_view = container.mount()
    print(f"Container视图: {type(container_view).__name__}")
    print(f"Container子视图数: {len(container_view.subviews())}")
    
    # 测试样式方法
    print("\n🎨 样式方法测试:")
    styled_label = TestLabel("Styled").size(300, 50).opacity(0.8)
    print(f"样式化标签: width={styled_label.style.width}, opacity={styled_label.style.opacity}")
    
    print("\n✅ 组件架构测试完成！")