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
            print(f"⚠️ 绝对定位应用失败: {e}")
            # 回退到默认尺寸
            self._apply_fallback_frame()
    
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
            
            # 为组件创建布局节点（如果还没有的话）
            layout_node = engine.get_node_for_component(self)
            if not layout_node:
                layout_node = engine.create_node_for_component(self)
            
            # 计算可用空间 - 尝试从父容器获取
            available_size = self._get_available_size_from_parent()
            
            # 计算布局
            layout_result = engine.compute_layout_for_component(self, available_size)
            
            if layout_result:
                # 应用计算得到的布局
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
                
                print(f"📐 v4布局已应用: {self.__class__.__name__} -> ({layout_result.x:.1f}, {layout_result.y:.1f}, {layout_result.width:.1f}x{layout_result.height:.1f})")
                return True
            else:
                print(f"⚠️ v4布局计算失败: {self.__class__.__name__}")
                self._apply_fallback_frame()
                return False
                
        except Exception as e:
            print(f"⚠️ v4布局应用失败: {e}")
            import traceback
            traceback.print_exc()
            # 回退到默认frame
            self._apply_fallback_frame()
            return False
    
    def _apply_fallback_frame(self):
        """应用回退frame"""
        width = self._resolve_size_value(self.style.width, 100)
        height = self._resolve_size_value(self.style.height, 30)
        frame = NSMakeRect(0, 0, width, height)
        self._nsview.setFrame_(frame)
        print(f"🔧 回退frame已应用: (0, 0, {width}, {height})")
    
    def _get_available_size_from_parent(self) -> Optional[Tuple[float, float]]:
        """从父容器获取可用尺寸"""
        if self._parent_container and hasattr(self._parent_container, '_nsview'):
            parent_view = self._parent_container._nsview
            if parent_view:
                frame = parent_view.frame()
                return (frame.size.width, frame.size.height)
        
        # 回退到视口管理器的默认尺寸
        try:
            viewport_size = self.viewport_manager.get_viewport_size()
            return viewport_size
        except:
            # 最后回退到默认值
            return (800, 600)
    
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
                    # 设置父子关系
                    if hasattr(child, '_parent_container'):
                        child._parent_container = self
                    
                    # 挂载子组件
                    child_view = child.mount()
                    container.addSubview_(child_view)
                    
                    # 添加到v4布局树
                    engine.add_child_relationship(self, child, i)
                    
                    print(f"  ├─ 子组件 {i+1}: {child.__class__.__name__} 已添加到容器和v4布局树")
                except Exception as e:
                    print(f"  ├─ ⚠️ 子组件 {i+1} 挂载失败: {e}")
        except Exception as e:
            print(f"⚠️ Container v4布局树构建失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 回退到简单挂载
            for i, child in enumerate(self.children):
                try:
                    # 设置父子关系
                    if hasattr(child, '_parent_container'):
                        child._parent_container = self
                        
                    child_view = child.mount()
                    container.addSubview_(child_view)
                    print(f"  ├─ 子组件 {i+1}: {child.__class__.__name__} 已添加（简单模式）")
                except Exception as e:
                    print(f"  ├─ ⚠️ 子组件 {i+1} 挂载失败: {e}")
                    
        return container
    
    def add_child_component(self, child: UIComponent):
        """添加新的子组件"""
        self.children.append(child)
        self.add_child(child)
        
        # 如果容器已挂载，立即挂载新子组件
        if self._nsview and hasattr(child, 'mount'):
            try:
                child_view = child.mount()
                self._nsview.addSubview_(child_view)
                print(f"➕ 动态添加子组件: {child.__class__.__name__}")
            except Exception as e:
                print(f"⚠️ 动态添加子组件失败: {e}")

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