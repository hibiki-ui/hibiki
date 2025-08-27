#!/usr/bin/env python3
"""
macUI v4.0 全新组件架构设计
统一的布局系统：Flexbox + Grid + 绝对定位 + Z-Index
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union, Callable, Any, TypeVar
from dataclasses import dataclass, field
from AppKit import NSView

# 导入我们设计的布局API  
import sys
sys.path.append('.')
from layout_api_design import LayoutStyle, LayoutAPI, Position, ZLayer, Length, px

T = TypeVar("T")

# ================================
# 1. 核心抽象基类 - Component
# ================================

class Component(ABC):
    """macUI组件核心抽象基类
    
    职责：
    - 响应式状态管理 (Signal, Computed, Effect)
    - 核心生命周期方法 (mount, cleanup)
    - 基础组件功能 (绑定、子组件管理)
    
    这是所有macUI组件的根基类，提供最基础的功能。
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
        self._view: Optional[NSView] = None
        self._cleanup_callbacks: List[Callable[[], None]] = []
        
        # 子组件管理
        self._children: List['Component'] = []
    
    @abstractmethod 
    def mount(self) -> NSView:
        """🚀 CORE METHOD: Component mounting phase
        
        创建并返回NSView，所有子类必须实现
        """
        raise NotImplementedError(
            f"{self.__class__.__module__}.{self.__class__.__qualname__} is "
            "missing the required \"mount\" function"
        )
    
    # 响应式状态方法
    def create_signal(self, initial_value: T):
        """创建组件作用域的Signal"""
        # 实现细节...
        pass
        
    def create_computed(self, fn: Callable[[], T]):
        """创建计算属性"""
        # 实现细节...
        pass
        
    def create_effect(self, fn: Callable[[], Optional[Callable[[], None]]]):
        """创建副作用"""
        # 实现细节...
        pass
    
    # 其他基础方法...
    def cleanup(self):
        """清理组件资源"""
        # 实现细节...
        pass

# ================================
# 2. UI组件基类 - UIComponent  
# ================================

class UIComponent(Component, LayoutAPI):
    """macUI UI组件基类
    
    职责：
    - 完整的布局API (Flexbox + Grid + 绝对定位)
    - Z-Index和层级管理
    - NSView集成和布局应用
    - 变换和动画支持
    
    这是所有UI组件的直接基类，提供完整的布局和视觉功能。
    """
    
    def __init__(self, style: Optional[LayoutStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: UI component initialization
        
        Args:
            style: 完整的布局样式对象
            **style_kwargs: 样式快捷参数
        """
        # 初始化基类
        Component.__init__(self)
        LayoutAPI.__init__(self)
        
        # 合并样式参数
        if style:
            self.style = style
        elif style_kwargs:
            self.style = LayoutStyle(**style_kwargs)
        else:
            self.style = LayoutStyle()
            
        # UI特定属性
        self._nsview: Optional[NSView] = None
        self._layout_computed = False
        self._parent_container: Optional['UIComponent'] = None
        
    def mount(self) -> NSView:
        """🚀 CORE METHOD: UI component mounting
        
        完整的UI组件挂载流程：
        1. 创建NSView
        2. 应用样式和布局
        3. 处理定位和z-index
        4. 建立响应式绑定
        """
        if self._nsview is None:
            # 1. 创建NSView - 由子类实现
            self._nsview = self._create_nsview()
            
            # 2. 应用基础样式
            self._apply_basic_style()
            
            # 3. 处理定位和布局
            self._apply_layout_and_positioning()
            
            # 4. 应用变换效果
            self._apply_transforms()
            
            # 5. 设置z-index
            self._apply_z_index()
            
        return self._nsview
    
    @abstractmethod
    def _create_nsview(self) -> NSView:
        """创建NSView实例 - 子类必须实现
        
        专门的方法用于创建具体的NSView类型
        (NSButton, NSTextField, NSImageView等)
        """
        raise NotImplementedError("子类必须实现 _create_nsview 方法")
    
    # ================================
    # 布局和定位实现
    # ================================
    
    def _apply_layout_and_positioning(self):
        """应用布局和定位"""
        if not self._nsview:
            return
            
        if self.style.position == Position.STATIC:
            # 参与flexbox/grid布局
            self._apply_flex_grid_layout()
        elif self.style.position in [Position.ABSOLUTE, Position.FIXED]:
            # 绝对定位
            self._apply_absolute_positioning()
        elif self.style.position == Position.RELATIVE:
            # 相对定位
            self._apply_relative_positioning()
    
    def _apply_flex_grid_layout(self):
        """应用Flexbox/Grid布局"""
        # 使用Stretchable布局引擎
        # 实现细节...
        print(f"📐 应用Flex/Grid布局: {self.style.display}")
    
    def _apply_absolute_positioning(self):
        """应用绝对定位"""
        from Foundation import NSMakeRect
        
        # 计算绝对位置
        x, y, w, h = self._calculate_absolute_frame()
        frame = NSMakeRect(x, y, w, h)
        self._nsview.setFrame_(frame)
        
        print(f"📍 应用绝对定位: ({x}, {y}, {w}, {h})")
    
    def _apply_relative_positioning(self):
        """应用相对定位"""
        # 先计算正常布局位置，再应用偏移
        # 实现细节...
        print(f"🔄 应用相对定位: offset({self.style.left}, {self.style.top})")
    
    def _calculate_absolute_frame(self):
        """计算绝对定位的frame"""
        # 获取父容器或窗口尺寸
        parent_bounds = self._get_positioning_context()
        parent_width = parent_bounds.size.width
        parent_height = parent_bounds.size.height
        
        # 计算位置
        x = self._resolve_position(self.style.left, parent_width) if self.style.left else 0
        y = self._resolve_position(self.style.top, parent_height) if self.style.top else 0
        
        # 计算尺寸
        w = self._resolve_size(self.style.width, parent_width) if self.style.width else 100
        h = self._resolve_size(self.style.height, parent_height) if self.style.height else 30
        
        return x, y, w, h
    
    def _resolve_position(self, length: Length, parent_size: float) -> float:
        """解析位置值"""
        if length.unit.value == "px":
            return float(length.value)
        elif length.unit.value == "%":
            return float(length.value) * parent_size / 100
        elif length.unit.value == "vw":
            # 获取窗口宽度
            return float(length.value) * self._get_viewport_width() / 100
        elif length.unit.value == "vh":
            # 获取窗口高度  
            return float(length.value) * self._get_viewport_height() / 100
        return 0
    
    def _resolve_size(self, length: Length, parent_size: float) -> float:
        """解析尺寸值"""
        return self._resolve_position(length, parent_size)
    
    # ================================
    # Z-Index和层级管理
    # ================================
    
    def _apply_z_index(self):
        """应用Z-Index层级"""
        if not self._nsview:
            return
            
        z_value = self.style.z_index
        if isinstance(z_value, ZLayer):
            z_value = z_value.value
            
        # 在macOS中，通过视图层次结构管理z-index
        self._set_view_z_order(z_value)
        print(f"🔝 设置Z-Index: {z_value}")
    
    def _set_view_z_order(self, z_index: int):
        """设置视图Z顺序"""
        # 实现细节：在父视图中调整子视图顺序
        # 或使用CALayer的zPosition
        if hasattr(self._nsview, 'layer') and self._nsview.layer():
            self._nsview.layer().setZPosition_(z_index)
    
    # ================================
    # 变换和动画
    # ================================
    
    def _apply_transforms(self):
        """应用变换效果"""
        if not self._nsview or not hasattr(self._nsview, 'layer'):
            return
            
        layer = self._nsview.layer()
        if not layer:
            return
            
        # 应用缩放
        if self.style.scale != (1.0, 1.0):
            from Foundation import NSAffineTransform
            transform = NSAffineTransform.transform()
            transform.scaleXBy_yBy_(self.style.scale[0], self.style.scale[1])
            layer.setAffineTransform_(transform)
            
        # 应用旋转
        if self.style.rotation != 0:
            layer.setTransform_(layer.transform().rotateByAngle_(self.style.rotation))
            
        # 应用平移  
        if self.style.translation != (0.0, 0.0):
            layer.setTranslation_(self.style.translation)
            
        print(f"🎨 应用变换: scale={self.style.scale}, rotation={self.style.rotation}")
    
    # ================================
    # 工具方法
    # ================================
    
    def _apply_basic_style(self):
        """应用基础样式"""
        if not self._nsview:
            return
            
        # 设置透明度
        self._nsview.setAlphaValue_(self.style.opacity)
        
        # 设置可见性
        self._nsview.setHidden_(not self.style.visible)
        
    def _get_positioning_context(self):
        """获取定位上下文（父元素或窗口）"""
        # 返回父容器的边界，用于绝对定位计算
        # 实现细节...
        from Foundation import NSMakeRect
        return NSMakeRect(0, 0, 800, 600)  # 示例
        
    def _get_viewport_width(self) -> float:
        """获取视口宽度"""
        return 800  # 示例
        
    def _get_viewport_height(self) -> float:
        """获取视口高度"""
        return 600  # 示例

# ================================
# 3. 具体组件实现示例
# ================================

class Label(UIComponent):
    """现代化Label组件"""
    
    def __init__(self, text: str, style: Optional[LayoutStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: Label initialization"""
        super().__init__(style=style, **style_kwargs)
        self.text = text
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSTextField作为Label"""
        from AppKit import NSTextField
        label = NSTextField.alloc().init()
        label.setStringValue_(self.text)
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setSelectable_(False)
        return label

class Button(UIComponent):
    """现代化Button组件"""
    
    def __init__(self, title: str, on_click: Optional[Callable] = None, 
                 style: Optional[LayoutStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: Button initialization"""
        super().__init__(style=style, **style_kwargs)
        self.title = title
        self.on_click = on_click
    
    def _create_nsview(self) -> NSView:
        """🚀 创建NSButton"""
        from AppKit import NSButton, NSButtonTypeMomentaryPushIn
        button = NSButton.alloc().init()
        button.setTitle_(self.title)
        button.setButtonType_(NSButtonTypeMomentaryPushIn)
        
        # 绑定点击事件
        if self.on_click:
            # 事件绑定实现...
            pass
            
        return button

class Container(UIComponent):
    """容器组件 - 支持复杂布局和子组件管理"""
    
    def __init__(self, children: Optional[List[UIComponent]] = None,
                 style: Optional[LayoutStyle] = None, **style_kwargs):
        """🏗️ CORE METHOD: Container initialization"""
        super().__init__(style=style, **style_kwargs)
        self.children = children or []
    
    def _create_nsview(self) -> NSView:
        """🚀 创建容器NSView"""
        container = NSView.alloc().init()
        
        # 挂载所有子组件
        for child in self.children:
            child_view = child.mount()
            container.addSubview_(child_view)
            
        return container

# ================================
# 4. 使用示例
# ================================

if __name__ == "__main__":
    print("macUI v4.0 新组件架构演示\n")
    
    # 示例1：创建绝对定位的标签
    print("🏷️ 创建绝对定位标签")
    label = Label("Hello World").top_left(top=20, left=20).z_index(ZLayer.CONTENT)
    label_view = label.mount()
    print(f"Label样式: position={label.style.position}")
    print()
    
    # 示例2：创建居中的模态按钮
    print("🔘 创建居中模态按钮")  
    button = Button("Click Me").center(z_index=ZLayer.MODAL).width(120).height(32)
    button_view = button.mount()
    print(f"Button样式: position={button.style.position}, z_index={button.style.z_index}")
    print()
    
    # 示例3：创建复杂布局容器
    print("📦 创建复杂布局容器")
    container = Container(
        children=[
            Label("Title").relative(top=0),
            Button("Action").absolute(bottom=20, right=20)
        ],
        style=LayoutStyle(position=Position.RELATIVE, width=px(400), height=px(300))
    )
    container_view = container.mount()
    print(f"Container包含 {len(container.children)} 个子组件")
    print()
    
    print("✅ 新架构演示完成！")