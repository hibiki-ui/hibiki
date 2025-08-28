#!/usr/bin/env python3
"""
macUI v4.0 管理器系统
六大专业管理器，分离关注点，各司其职
"""

import weakref
from typing import Optional, List, Union, Dict, Tuple, Callable, Any
from abc import ABC, abstractmethod
from enum import Enum
from AppKit import NSView, NSWindow, NSScrollView
from Foundation import NSMakeRect, NSAffineTransform, NSBezierPath

# ================================
# 1. ViewportManager - 视口管理器
# ================================

class ViewportManager:
    """视口管理器 - 处理视口相关计算和事件
    
    职责：
    - 视口尺寸计算和缓存
    - Retina屏幕适配 
    - 窗口事件监听
    - 视口单位计算 (vw, vh)
    """
    
    _instance: Optional['ViewportManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self._window_ref: Optional[weakref.ReferenceType] = None
        self._viewport_size = (800, 600)  # 默认尺寸
        self._scale_factor = 1.0
        self._cached_frame_count = 0
        
        print("🖥️ ViewportManager初始化完成")
        
    def set_window(self, window: NSWindow):
        """设置关联的窗口"""
        self._window_ref = weakref.ref(window)
        self._update_viewport_info()
        print(f"📱 ViewportManager绑定窗口: {self._viewport_size}")
    
    def get_viewport_size(self) -> Tuple[float, float]:
        """获取视口尺寸"""
        self._update_viewport_info()
        return self._viewport_size
    
    def get_viewport_width(self) -> float:
        """获取视口宽度"""
        return self.get_viewport_size()[0]
    
    def get_viewport_height(self) -> float:
        """获取视口高度"""
        return self.get_viewport_size()[1]
    
    def get_scale_factor(self) -> float:
        """获取缩放因子（Retina支持）"""
        return self._scale_factor
    
    def vw_to_px(self, vw: float) -> float:
        """将vw单位转换为像素"""
        return vw * self.get_viewport_width() / 100
    
    def vh_to_px(self, vh: float) -> float:
        """将vh单位转换为像素"""
        return vh * self.get_viewport_height() / 100
    
    def _update_viewport_info(self):
        """更新视口信息"""
        if self._window_ref and self._window_ref():
            window = self._window_ref()
            frame = window.frame()
            self._viewport_size = (frame.size.width, frame.size.height)
            self._scale_factor = window.backingScaleFactor()

# ================================
# 2. LayerManager - 层级管理器  
# ================================

from enum import Enum

class ZLayer(Enum):
    """预定义Z层级常量"""
    BACKGROUND = -100        # 背景层
    CONTENT = 0              # 内容层（默认）
    FLOATING = 1000          # 悬浮层（tooltip, dropdown）
    MODAL = 2000             # 模态层（dialog, modal）
    OVERLAY = 3000           # 覆盖层（loading, notification）
    SYSTEM = 9000            # 系统层（debug tools）

class LayerManager:
    """层级管理器 - 处理Z-Index和视图层次
    
    职责：
    - Z-Index注册和管理
    - 预定义层级常量管理
    - 自动z-index分配
    - 弱引用防止内存泄漏
    """
    
    def __init__(self):
        # 层级注册表：z_index -> [component_weakrefs]
        self._layer_registry: Dict[int, List[weakref.ReferenceType]] = {}
        self._next_auto_z = 1
        self._total_components = 0
        
        print("🔝 LayerManager初始化完成")
        
    def register_component(self, component: 'UIComponent', z_index: Union[int, ZLayer]):
        """注册组件到指定层级"""
        z_value = z_index.value if isinstance(z_index, ZLayer) else z_index
        
        if z_value not in self._layer_registry:
            self._layer_registry[z_value] = []
            
        # 使用弱引用防止循环引用
        self._layer_registry[z_value].append(weakref.ref(component))
        self._total_components += 1
        
        # 定期清理已失效的引用
        if self._total_components % 10 == 0:
            self._cleanup_dead_references(z_value)
        
        print(f"📋 组件注册到层级 {z_value}, 总组件数: {self._total_components}")
        
    def unregister_component(self, component: 'UIComponent'):
        """从层级管理器注销组件"""
        component_removed = False
        
        # 遍历所有层级，查找并移除该组件
        for z_value, components_refs in self._layer_registry.items():
            # 过滤掉匹配的组件引用
            original_count = len(components_refs)
            components_refs[:] = [ref for ref in components_refs 
                                if ref() is not None and ref() is not component]
            
            removed_count = original_count - len(components_refs)
            if removed_count > 0:
                self._total_components -= removed_count
                component_removed = True
                print(f"🗑️ 从层级 {z_value} 注销组件, 移除数: {removed_count}, 剩余总数: {self._total_components}")
        
        # 如果没有找到组件，可能是弱引用已失效
        if not component_removed:
            # 执行全面清理，移除所有失效的引用
            original_total = self._total_components
            for z_value in list(self._layer_registry.keys()):
                self._cleanup_dead_references(z_value)
            
            cleaned_count = original_total - self._total_components
            if cleaned_count > 0:
                print(f"🧹 清理层级管理器失效引用: {cleaned_count}个, 剩余总数: {self._total_components}")
        
    def get_auto_z_index(self, layer: ZLayer) -> int:
        """获取自动分配的z-index"""
        base_z = layer.value
        auto_z = base_z + self._next_auto_z
        self._next_auto_z += 1
        return auto_z
        
    def get_components_in_layer(self, z_index: Union[int, ZLayer]) -> List['UIComponent']:
        """获取指定层级的所有有效组件"""
        z_value = z_index.value if isinstance(z_index, ZLayer) else z_index
        
        if z_value not in self._layer_registry:
            return []
            
        components = []
        for ref in self._layer_registry[z_value]:
            component = ref()
            if component is not None:
                components.append(component)
                
        return components
    
    def _cleanup_dead_references(self, z_value: int):
        """清理失效的弱引用"""
        if z_value in self._layer_registry:
            old_count = len(self._layer_registry[z_value])
            self._layer_registry[z_value] = [
                ref for ref in self._layer_registry[z_value] if ref() is not None
            ]
            new_count = len(self._layer_registry[z_value])
            
            if old_count != new_count:
                print(f"🧹 层级 {z_value} 清理了 {old_count - new_count} 个失效引用")

# ================================
# 3. PositioningManager - 定位管理器
# ================================

from enum import Enum

class Position(Enum):
    """定位类型枚举"""
    STATIC = "static"        # 默认定位，参与flex/grid布局
    RELATIVE = "relative"    # 相对定位
    ABSOLUTE = "absolute"    # 绝对定位
    FIXED = "fixed"          # 固定定位（相对视口）
    STICKY = "sticky"        # 粘性定位

class PositioningManager:
    """定位管理器 - 处理绝对定位和固定定位
    
    职责：
    - 绝对定位frame计算
    - 固定定位（相对视口）
    - 相对定位偏移计算
    - 多单位支持 (px, %, vw, vh)
    """
    
    def __init__(self, viewport_manager: ViewportManager):
        self.viewport_manager = viewport_manager
        print("📍 PositioningManager初始化完成")
        
    def calculate_absolute_frame(self, component: 'UIComponent') -> Tuple[float, float, float, float]:
        """计算绝对定位的frame
        
        Returns:
            (x, y, width, height) tuple
        """
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
        
        # 处理right和bottom定位
        if style.right is not None and style.left is None:
            right_offset = self._resolve_position_value(style.right, context_size[0], 0)
            x = context_size[0] - w - right_offset
            
        if style.bottom is not None and style.top is None:
            bottom_offset = self._resolve_position_value(style.bottom, context_size[1], 0)
            y = context_size[1] - h - bottom_offset
            
        print(f"🎯 计算绝对定位: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        return x, y, w, h
        
    def calculate_relative_offset(self, component: 'UIComponent') -> Tuple[float, float]:
        """计算相对定位的偏移量"""
        style = component.style
        
        # 获取父容器尺寸作为参考
        context_size = self._get_parent_context_size(component)
        
        offset_x = self._resolve_position_value(style.left, context_size[0], 0)
        offset_y = self._resolve_position_value(style.top, context_size[1], 0)
        
        return offset_x, offset_y
        
    def _get_parent_context_size(self, component: 'UIComponent') -> Tuple[float, float]:
        """获取父容器的上下文尺寸"""
        # TODO: 实际应该查找最近的positioned父元素
        # 简化实现，使用视口尺寸
        return self.viewport_manager.get_viewport_size()
        
    def _resolve_position_value(self, value: Any, context_size: float, default: float) -> float:
        """解析位置值"""
        if value is None:
            return default
            
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            if value.endswith('%'):
                percent = float(value[:-1])
                return percent * context_size / 100
            elif value.endswith('vw'):
                vw = float(value[:-2])
                return self.viewport_manager.vw_to_px(vw)
            elif value.endswith('vh'):
                vh = float(value[:-2])
                return self.viewport_manager.vh_to_px(vh)
            elif value.endswith('px'):
                return float(value[:-2])
            else:
                try:
                    return float(value)
                except ValueError:
                    return default
        
        return default
        
    def _resolve_size_value(self, value: Any, context_size: float, default: float) -> float:
        """解析尺寸值"""
        return self._resolve_position_value(value, context_size, default)

# ================================
# 4. TransformManager - 变换管理器
# ================================

class TransformManager:
    """变换管理器 - 处理CSS变换效果
    
    职责：
    - CSS变换效果 (scale, rotate, translate)
    - CALayer集成
    - 透明度控制
    - 变换矩阵计算
    """
    
    def __init__(self):
        print("🎨 TransformManager初始化完成")
    
    @staticmethod
    def apply_transforms(view: NSView, style: 'ComponentStyle'):
        """应用变换效果到NSView"""
        if not view:
            return
            
        # 确保视图有CALayer
        if not view.layer():
            view.setWantsLayer_(True)
            
        layer = view.layer()
        if not layer:
            print("⚠️ 无法获取CALayer，跳过变换")
            return
        
        # 应用透明度
        if style.opacity != 1.0:
            layer.setOpacity_(style.opacity)
            
        # 应用变换矩阵
        transform_applied = False
        
        if any([
            style.scale != (1.0, 1.0), 
            style.rotation != 0, 
            style.translation != (0, 0)
        ]):
            try:
                # 使用CATransform3D进行变换
                from Quartz import CATransform3DIdentity, CATransform3DScale, CATransform3DRotate, CATransform3DTranslate, CATransform3DConcat
                import math
                
                transform = CATransform3DIdentity
                
                # 缩放
                if style.scale != (1.0, 1.0):
                    transform = CATransform3DScale(transform, style.scale[0], style.scale[1], 1.0)
                
                # 旋转 (转换为弧度)
                if style.rotation != 0:
                    radians = math.radians(style.rotation)
                    transform = CATransform3DRotate(transform, radians, 0.0, 0.0, 1.0)
                
                # 平移
                if style.translation != (0, 0):
                    transform = CATransform3DTranslate(transform, style.translation[0], style.translation[1], 0.0)
                    
                layer.setTransform_(transform)
                transform_applied = True
                
            except Exception as e:
                print(f"⚠️ 变换应用失败: {e}")
        
        if transform_applied:
            print(f"✨ 变换已应用: scale={style.scale}, rotation={style.rotation}°, translate={style.translation}")

# ================================
# 5. ScrollManager - 滚动管理器
# ================================

class OverflowBehavior(Enum):
    """溢出行为枚举"""
    VISIBLE = "visible"      # 可见（默认）
    HIDDEN = "hidden"        # 隐藏
    SCROLL = "scroll"        # 滚动
    AUTO = "auto"           # 自动

class ScrollManager:
    """滚动管理器 - 处理滚动容器
    
    职责：
    - NSScrollView自动创建
    - overflow行为处理
    - 滚动容器注册和管理
    """
    
    def __init__(self):
        self._scroll_containers: List[weakref.ReferenceType] = []
        print("📜 ScrollManager初始化完成")
        
    def create_scroll_view(self, content_view: NSView, 
                          overflow: OverflowBehavior = OverflowBehavior.AUTO) -> NSView:
        """创建滚动容器"""
        if overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
            scroll_view = NSScrollView.alloc().init()
            
            # 设置文档视图
            scroll_view.setDocumentView_(content_view)
            
            # 配置滚动行为
            scroll_view.setHasVerticalScroller_(True)
            scroll_view.setHasHorizontalScroller_(overflow == OverflowBehavior.AUTO)
            scroll_view.setAutohidesScrollers_(overflow == OverflowBehavior.AUTO)
            
            # 设置边框样式
            scroll_view.setBorderType_(0)  # 无边框
            
            # 注册到管理器
            self._scroll_containers.append(weakref.ref(scroll_view))
            
            print(f"📋 创建滚动容器: {overflow.value}")
            return scroll_view
        elif overflow == OverflowBehavior.HIDDEN:
            # 设置裁剪
            content_view.setClipsToBounds_(True)
            
        return content_view
    
    def get_scroll_containers_count(self) -> int:
        """获取活跃的滚动容器数量"""
        active_containers = [ref for ref in self._scroll_containers if ref() is not None]
        self._scroll_containers = active_containers  # 清理死引用
        return len(active_containers)

# ================================
# 6. MaskManager - 遮罩管理器
# ================================

class MaskManager:
    """遮罩管理器 - 处理裁剪和遮罩效果
    
    职责：
    - 裁剪区域设置
    - CALayer mask应用
    - 复杂遮罩效果
    """
    
    def __init__(self):
        print("🎭 MaskManager初始化完成")
    
    @staticmethod  
    def apply_clip_mask(view: NSView, clip_rect: Optional[Tuple[float, float, float, float]] = None):
        """应用裁剪遮罩
        
        Args:
            view: 目标视图
            clip_rect: 裁剪矩形 (x, y, width, height)
        """
        if not clip_rect or not view:
            return
            
        # 确保视图有CALayer
        if not view.layer():
            view.setWantsLayer_(True)
            
        layer = view.layer()
        if not layer:
            return
            
        try:
            x, y, w, h = clip_rect
            clip_path = NSBezierPath.bezierPathWithRect_(NSMakeRect(x, y, w, h))
            
            # 创建遮罩层
            mask_layer = layer.copy()
            mask_layer.setPath_(clip_path.CGPath())
            
            layer.setMask_(mask_layer)
            
            print(f"✂️ 裁剪遮罩已应用: ({x}, {y}, {w}, {h})")
            
        except Exception as e:
            print(f"⚠️ 遮罩应用失败: {e}")
    
    @staticmethod
    def remove_mask(view: NSView):
        """移除遮罩"""
        if view and view.layer():
            view.layer().setMask_(None)
            print("🔓 遮罩已移除")

# ================================
# 7. 管理器工厂
# ================================

class ManagerFactory:
    """管理器工厂 - 统一创建和管理所有管理器实例"""
    
    _viewport_manager: Optional[ViewportManager] = None
    _layer_manager: Optional[LayerManager] = None
    _positioning_manager: Optional[PositioningManager] = None
    _transform_manager: Optional[TransformManager] = None
    _scroll_manager: Optional[ScrollManager] = None
    _mask_manager: Optional[MaskManager] = None
    
    @classmethod
    def get_viewport_manager(cls) -> ViewportManager:
        if cls._viewport_manager is None:
            cls._viewport_manager = ViewportManager()
        return cls._viewport_manager
    
    @classmethod
    def get_layer_manager(cls) -> LayerManager:
        if cls._layer_manager is None:
            cls._layer_manager = LayerManager()
        return cls._layer_manager
    
    @classmethod
    def get_positioning_manager(cls) -> PositioningManager:
        if cls._positioning_manager is None:
            viewport_mgr = cls.get_viewport_manager()
            cls._positioning_manager = PositioningManager(viewport_mgr)
        return cls._positioning_manager
    
    @classmethod
    def get_transform_manager(cls) -> TransformManager:
        if cls._transform_manager is None:
            cls._transform_manager = TransformManager()
        return cls._transform_manager
    
    @classmethod
    def get_scroll_manager(cls) -> ScrollManager:
        if cls._scroll_manager is None:
            cls._scroll_manager = ScrollManager()
        return cls._scroll_manager
    
    @classmethod
    def get_mask_manager(cls) -> MaskManager:
        if cls._mask_manager is None:
            cls._mask_manager = MaskManager()
        return cls._mask_manager
    
    @classmethod
    def initialize_all(cls):
        """初始化所有管理器"""
        print("🏭 ManagerFactory: 初始化所有管理器...")
        cls.get_viewport_manager()
        cls.get_layer_manager()
        cls.get_positioning_manager()
        cls.get_transform_manager()
        cls.get_scroll_manager()
        cls.get_mask_manager()
        print("✅ 所有管理器初始化完成！")

# ================================
# 8. 测试代码
# ================================

if __name__ == "__main__":
    print("macUI v4.0 管理器系统测试\n")
    
    # 初始化所有管理器
    ManagerFactory.initialize_all()
    
    print("\n🧪 管理器功能测试:")
    
    # 测试ViewportManager
    viewport_mgr = ManagerFactory.get_viewport_manager()
    print(f"视口尺寸: {viewport_mgr.get_viewport_size()}")
    print(f"50vw = {viewport_mgr.vw_to_px(50):.1f}px")
    
    # 测试LayerManager
    layer_mgr = ManagerFactory.get_layer_manager()
    print(f"模态层级: {ZLayer.MODAL.value}")
    print(f"自动Z-Index: {layer_mgr.get_auto_z_index(ZLayer.FLOATING)}")
    
    # 测试PositioningManager
    positioning_mgr = ManagerFactory.get_positioning_manager()
    print(f"百分比解析: {positioning_mgr._resolve_position_value('50%', 800, 0)}px")
    
    print("\n✅ 管理器系统测试完成！")