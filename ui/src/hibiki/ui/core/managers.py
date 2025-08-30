#!/usr/bin/env python3
"""
Hibiki UI v4.0 管理器系统
六大专业管理器，分离关注点，各司其职
"""

import weakref
from typing import Optional, List, Union, Dict, Tuple, Callable, Any
from abc import ABC, abstractmethod
from enum import Enum
from AppKit import NSView, NSWindow, NSScrollView
from Foundation import NSMakeRect, NSAffineTransform, NSBezierPath, NSSize

from .logging import get_logger

logger = get_logger("core.managers")
logger.setLevel("INFO")


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

    🔧 架构修复：消除循环依赖
    - 不再依赖contentView.frame()
    - 直接接收准确的内容区域尺寸
    - 建立单向的尺寸传递链
    """

    _instance: Optional["ViewportManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self._window: Optional[NSWindow] = None
        self._viewport_size = (800, 600)  # 默认尺寸
        self._scale_factor = 1.0
        self._size_change_callbacks = []  # 尺寸变化回调

        logger.info("🖥️ ViewportManager初始化完成")

    def set_window_content_size(self, width: float, height: float, window: Optional[NSWindow] = None):
        """直接设置窗口内容区域尺寸，不依赖contentView

        🔧 核心修复：消除循环依赖
        - 直接接收准确的内容区域尺寸
        - 不再依赖window.contentView().frame()
        """
        old_size = self._viewport_size
        self._viewport_size = (width, height)

        # 更新窗口引用和缩放因子
        if window:
            self._window = window
            self._scale_factor = window.backingScaleFactor()

        # 如果尺寸发生变化，通知所有监听者
        if old_size != self._viewport_size:
            self._notify_size_change()

        logger.info(f"🎯 ViewportManager尺寸更新: {width}x{height}")

    def get_viewport_size(self) -> Tuple[float, float]:
        """获取视口尺寸 - 现在返回可靠的尺寸"""
        return self._viewport_size

    def get_viewport_width(self) -> float:
        """获取视口宽度"""
        return self._viewport_size[0]

    def get_viewport_height(self) -> float:
        """获取视口高度"""
        return self._viewport_size[1]

    def get_scale_factor(self) -> float:
        """获取缩放因子（Retina支持）"""
        return self._scale_factor

    def vw_to_px(self, vw: float) -> float:
        """将vw单位转换为像素"""
        return vw * self.get_viewport_width() / 100

    def vh_to_px(self, vh: float) -> float:
        """将vh单位转换为像素"""
        return vh * self.get_viewport_height() / 100

    def add_size_change_callback(self, callback: Callable[[float, float], None]):
        """添加尺寸变化回调"""
        self._size_change_callbacks.append(callback)

    def _notify_size_change(self):
        """通知所有监听者尺寸发生变化"""
        width, height = self._viewport_size
        for callback in self._size_change_callbacks:
            try:
                callback(width, height)
            except Exception as e:
                logger.warning(f"⚠️ 尺寸变化回调失败: {e}")

    def _update_viewport_info(self):
        """更新视口信息 - 已废弃，现在尺寸通过set_window_content_size直接设置"""
        # 这个方法保留用于向后兼容，但现在是空操作
        # 实际尺寸更新通过set_window_content_size()进行
        pass


# ================================
# 2. LayerManager - 层级管理器
# ================================

from enum import Enum


class ZLayer(Enum):
    """预定义Z层级常量"""

    BACKGROUND = -100  # 背景层
    CONTENT = 0  # 内容层（默认）
    FLOATING = 1000  # 悬浮层（tooltip, dropdown）
    MODAL = 2000  # 模态层（dialog, modal）
    OVERLAY = 3000  # 覆盖层（loading, notification）
    SYSTEM = 9000  # 系统层（debug tools）


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

        logger.info("🔝 LayerManager初始化完成")

    def register_component(self, component: "UIComponent", z_index: Union[int, ZLayer]):
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

        logger.debug(f"📋 组件注册到层级 {z_value}, 总组件数: {self._total_components}")

    def unregister_component(self, component: "UIComponent"):
        """从层级管理器注销组件"""
        component_removed = False

        # 遍历所有层级，查找并移除该组件
        for z_value, components_refs in self._layer_registry.items():
            # 过滤掉匹配的组件引用
            original_count = len(components_refs)
            components_refs[:] = [
                ref for ref in components_refs if ref() is not None and ref() is not component
            ]

            removed_count = original_count - len(components_refs)
            if removed_count > 0:
                self._total_components -= removed_count
                component_removed = True
                logger.debug(
                    f"🗑️ 从层级 {z_value} 注销组件, 移除数: {removed_count}, 剩余总数: {self._total_components}"
                )

        # 如果没有找到组件，可能是弱引用已失效
        if not component_removed:
            # 执行全面清理，移除所有失效的引用
            original_total = self._total_components
            for z_value in list(self._layer_registry.keys()):
                self._cleanup_dead_references(z_value)

            cleaned_count = original_total - self._total_components
            if cleaned_count > 0:
                logger.debug(
                    f"🧹 清理层级管理器失效引用: {cleaned_count}个, 剩余总数: {self._total_components}"
                )

    def get_auto_z_index(self, layer: ZLayer) -> int:
        """获取自动分配的z-index"""
        base_z = layer.value
        auto_z = base_z + self._next_auto_z
        self._next_auto_z += 1
        return auto_z

    def get_components_in_layer(self, z_index: Union[int, ZLayer]) -> List["UIComponent"]:
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
                logger.debug(f"🧹 层级 {z_value} 清理了 {old_count - new_count} 个失效引用")


# ================================
# 3. PositioningManager - 定位管理器
# ================================

from enum import Enum


class Position(Enum):
    """定位类型枚举"""

    STATIC = "static"  # 默认定位，参与flex/grid布局
    RELATIVE = "relative"  # 相对定位
    ABSOLUTE = "absolute"  # 绝对定位
    FIXED = "fixed"  # 固定定位（相对视口）
    STICKY = "sticky"  # 粘性定位


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
        logger.info("📍 PositioningManager初始化完成")

    def calculate_absolute_frame(
        self, component: "UIComponent"
    ) -> Tuple[float, float, float, float]:
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

        logger.debug(f"🎯 计算绝对定位: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
        return x, y, w, h

    def calculate_relative_offset(self, component: "UIComponent") -> Tuple[float, float]:
        """计算相对定位的偏移量"""
        style = component.style

        # 获取父容器尺寸作为参考
        context_size = self._get_parent_context_size(component)

        offset_x = self._resolve_position_value(style.left, context_size[0], 0)
        offset_y = self._resolve_position_value(style.top, context_size[1], 0)

        return offset_x, offset_y

    def _get_parent_context_size(self, component: "UIComponent") -> Tuple[float, float]:
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
            if value.endswith("%"):
                percent = float(value[:-1])
                return percent * context_size / 100
            elif value.endswith("vw"):
                vw = float(value[:-2])
                return self.viewport_manager.vw_to_px(vw)
            elif value.endswith("vh"):
                vh = float(value[:-2])
                return self.viewport_manager.vh_to_px(vh)
            elif value.endswith("px"):
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
        logger.info("🎨 TransformManager初始化完成")

    @staticmethod
    def apply_transforms(view: NSView, style: "ComponentStyle"):
        """应用变换效果到NSView"""
        if not view:
            return

        # 确保视图有CALayer
        if not view.layer():
            view.setWantsLayer_(True)

        layer = view.layer()
        if not layer:
            logger.warning("⚠️ 无法获取CALayer，跳过变换")
            return

        # 应用透明度
        if style.opacity != 1.0:
            layer.setOpacity_(style.opacity)

        # 应用变换矩阵
        transform_applied = False

        if any([style.scale != (1.0, 1.0), style.rotation != 0, style.translation != (0, 0)]):
            try:
                # 使用CATransform3D进行变换
                from Quartz import (
                    CATransform3DIdentity,
                    CATransform3DScale,
                    CATransform3DRotate,
                    CATransform3DTranslate,
                    CATransform3DConcat,
                )
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
                    transform = CATransform3DTranslate(
                        transform, style.translation[0], style.translation[1], 0.0
                    )

                layer.setTransform_(transform)
                transform_applied = True

            except Exception as e:
                logger.warning(f"⚠️ 变换应用失败: {e}")

        if transform_applied:
            logger.debug(
                f"✨ 变换已应用: scale={style.scale}, rotation={style.rotation}°, translate={style.translation}"
            )


# ================================
# 5. ScrollManager - 滚动管理器
# ================================


class OverflowBehavior(Enum):
    """溢出行为枚举"""

    VISIBLE = "visible"  # 可见（默认）
    HIDDEN = "hidden"  # 隐藏
    SCROLL = "scroll"  # 滚动
    AUTO = "auto"  # 自动


class ScrollManager:
    """滚动管理器 - 处理滚动容器

    职责：
    - NSScrollView自动创建
    - overflow行为处理
    - 滚动容器注册和管理
    """

    def __init__(self):
        self._scroll_containers: List[weakref.ReferenceType] = []
        logger.info("📜 ScrollManager初始化完成")

    def create_scroll_view(
        self, content_view: NSView, overflow: OverflowBehavior = OverflowBehavior.AUTO
    ) -> NSView:
        """创建滚动容器"""
        if overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
            scroll_view = NSScrollView.alloc().init()

            # 🔧 关键修复：不要在创建时设置frame
            # NSScrollView的frame将完全由布局系统通过_apply_layout_result控制
            # 这里只需要设置ScrollView的基本属性即可

            # 设置文档视图
            scroll_view.setDocumentView_(content_view)

            # 🔧 documentView的尺寸调整将完全由布局系统处理
            # 这里只需要确保基本的ScrollView设置即可
            logger.debug(f"📋 创建NSScrollView，documentView: {content_view}")

            # 配置滚动行为
            scroll_view.setHasVerticalScroller_(True)
            scroll_view.setHasHorizontalScroller_(overflow == OverflowBehavior.AUTO)
            scroll_view.setAutohidesScrollers_(overflow == OverflowBehavior.AUTO)

            # 设置边框样式
            scroll_view.setBorderType_(0)  # 无边框

            # 🔧 确保NSScrollView禁用Auto Layout，依赖布局引擎控制
            scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(True)

            # 注册到管理器 (NSScrollView不支持弱引用，直接存储)
            self._scroll_containers.append(scroll_view)

            logger.debug(f"📋 创建滚动容器: {overflow.value}")
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
        logger.info("🎭 MaskManager初始化完成")

    @staticmethod
    def apply_clip_mask(
        view: NSView, clip_rect: Optional[Tuple[float, float, float, float]] = None
    ):
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

            logger.debug(f"✂️ 裁剪遮罩已应用: ({x}, {y}, {w}, {h})")

        except Exception as e:
            logger.warning(f"⚠️ 遮罩应用失败: {e}")

    @staticmethod
    def remove_mask(view: NSView):
        """移除遮罩"""
        if view and view.layer():
            view.layer().setMask_(None)
            logger.debug("🔓 遮罩已移除")


# ================================
# 7. RootContainerManager - 根容器管理器
# ================================


class RootContainerManager:
    """根容器管理器 - 统一管理根容器的创建和尺寸同步

    职责：
    - 创建具有正确尺寸的根容器
    - 统一处理根容器尺寸更新
    - 确保根容器与窗口内容区域的尺寸同步

    🔧 架构修复：解决窗口-容器尺寸同步问题
    - 在组件挂载前就确定根容器的正确尺寸
    - 提供统一的根容器管理接口
    - 消除百分比布局的父容器尺寸不确定问题
    """

    _instance: Optional["RootContainerManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self._active_root_containers: List[NSView] = []
        logger.info("🏗️ RootContainerManager初始化完成")

    def create_root_container(self, content_width: float, content_height: float) -> NSView:
        """创建具有正确尺寸的根容器

        Args:
            content_width: 窗口内容区域宽度
            content_height: 窗口内容区域高度

        Returns:
            配置好的根容器NSView
        """
        from .base_view import HibikiBaseView

        # 创建flipped根容器（支持top-left坐标系）
        root_container = HibikiBaseView.alloc().init()

        # 设置正确的frame尺寸
        frame = NSMakeRect(0, 0, content_width, content_height)
        root_container.setFrame_(frame)

        # 注册到活跃容器列表（NSView不支持弱引用，直接存储）
        self._active_root_containers.append(root_container)

        logger.info(f"🏗️ 创建根容器: {content_width:.1f}x{content_height:.1f}")
        return root_container

    def update_root_container_size(self, root_container: NSView, new_width: float, new_height: float):
        """更新根容器尺寸

        Args:
            root_container: 要更新的根容器
            new_width: 新的宽度
            new_height: 新的高度
        """
        if not root_container:
            logger.warning("⚠️ 根容器为None，无法更新尺寸")
            return

        # 更新frame
        new_frame = NSMakeRect(0, 0, new_width, new_height)
        root_container.setFrame_(new_frame)

        # 如果有子视图，也需要更新其布局
        subviews = root_container.subviews()
        if subviews and len(subviews) > 0:
            # 更新第一个子视图（通常是用户的主容器）
            main_subview = subviews[0]
            main_subview.setFrame_(root_container.bounds())

        logger.info(f"🔄 根容器尺寸已更新: {new_width:.1f}x{new_height:.1f}")

    def get_active_root_containers_count(self) -> int:
        """获取活跃的根容器数量"""
        return len(self._active_root_containers)

    def cleanup_released_containers(self):
        """清理已释放的根容器引用"""
        # NSView直接存储，无需特殊清理（由NSWindow管理生命周期）
        logger.debug(f"🧹 当前活跃根容器数量: {len(self._active_root_containers)}")


# ================================
# 8. 应用程序管理器
# ================================


class AppWindowDelegate:
    """窗口事件代理 - 监听窗口大小变化"""

    def __init__(self, app_window: 'AppWindow'):
        from Foundation import NSObject
        super(AppWindowDelegate, self).__init__()
        self.app_window = app_window

    def windowDidResize_(self, notification):
        """窗口大小改变回调 - 架构修复版本"""
        logger.info("🔄 窗口大小改变事件触发")

        # 🔧 架构修复：使用新的尺寸同步机制
        # 1. 重新计算内容区域尺寸
        content_size = self.app_window._calculate_content_area_size()

        # 2. 更新ViewportManager（使用新的API）
        viewport_mgr = ManagerFactory.get_viewport_manager()
        viewport_mgr.set_window_content_size(content_size.width, content_size.height, self.app_window.nswindow)

        # 3. 更新根容器尺寸
        if self.app_window._content:
            root_container = self.app_window.nswindow.contentView()
            if root_container:
                root_container_mgr = ManagerFactory.get_root_container_manager()
                root_container_mgr.update_root_container_size(
                    root_container, content_size.width, content_size.height
                )

        # 4. 触发布局重新计算
        self._trigger_layout_recalculation()

    def _trigger_layout_recalculation(self):
        """触发布局重新计算"""
        try:
            from .layout import get_layout_engine
            from .responsive import get_responsive_manager

            engine = get_layout_engine()
            responsive_mgr = get_responsive_manager()

            # 获取当前窗口尺寸
            viewport_mgr = ManagerFactory.get_viewport_manager()
            width, height = viewport_mgr.get_viewport_size()

            # 🔥 关键更新：先通知响应式管理器，再重新计算布局
            print(f"📱 更新响应式系统: {width}x{height}")
            responsive_mgr.update_viewport(width, height)

            # 获取根容器并触发重新计算
            if self.app_window._content:
                print(f"📐 开始布局重新计算...")
                engine.recalculate_all_layouts()
                print(f"✅ 布局重新计算完成")

        except Exception as e:
            print(f"❌ 布局重新计算失败: {e}")
            import traceback
            traceback.print_exc()


class AppWindow:
    """应用程序窗口包装器"""

    def __init__(self, title: str, width: int, height: int):
        from AppKit import (
            NSWindow,
            NSWindowStyleMaskTitled,
            NSWindowStyleMaskClosable,
            NSWindowStyleMaskMiniaturizable,
            NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
        )
        from Foundation import NSMakeRect

        # 创建窗口
        style_mask = (
            NSWindowStyleMaskTitled
            | NSWindowStyleMaskClosable
            | NSWindowStyleMaskMiniaturizable
            | NSWindowStyleMaskResizable
        )

        self.nswindow = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, width, height), style_mask, NSBackingStoreBuffered, False
        )

        self.nswindow.setTitle_(title)

        # 🔧 新增：设置窗口共享属性，使CGWindowListCreateImage能够访问
        try:
            # 确保窗口可以被屏幕截图API访问
            self.nswindow.setSharingType_(1)  # NSWindowSharingReadWrite
        except AttributeError:
            # 如果方法不存在，尝试其他方法
            pass

        # 设置窗口层级，确保在正确层
        self.nswindow.setLevel_(0)  # NSNormalWindowLevel

        self.nswindow.makeKeyAndOrderFront_(None)

        # 🔧 关键修复：激活应用程序，确保成为前台应用
        from AppKit import NSApplication
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)  # 强制激活应用

        self._content = None

        # 🔥 关键修复: 设置窗口代理来监听大小变化
        self.delegate = AppWindowDelegate(self)
        self.nswindow.setDelegate_(self.delegate)

        # 🔧 架构修复：正确的初始化时序
        # 1. 计算窗口内容区域尺寸
        content_size = self._calculate_content_area_size()

        # 2. 设置ViewportManager（使用新的API，不依赖contentView）
        viewport_mgr = ManagerFactory.get_viewport_manager()
        viewport_mgr.set_window_content_size(content_size.width, content_size.height, self.nswindow)

        logger.info(f"🎯 窗口初始化完成，内容区域: {content_size.width:.1f}x{content_size.height:.1f}")

    def _calculate_content_area_size(self) -> NSSize:
        """计算实际的内容区域尺寸

        Returns:
            NSSize: 窗口内容区域的实际尺寸（不包含标题栏等装饰元素）
        """
        window_frame = self.nswindow.frame()
        content_rect = self.nswindow.contentRectForFrameRect_(window_frame)
        return content_rect.size

    def set_content(self, component):
        """设置窗口内容 - 架构修复版本

        🔧 新的正确时序：
        1. 确保ViewportManager有准确尺寸（已在__init__中完成）
        2. 使用RootContainerManager创建正确尺寸的根容器
        3. 挂载用户组件（此时百分比计算将基于正确的父容器尺寸）
        4. 配置布局并设置为contentView
        """
        self._content = component
        if hasattr(component, "mount"):

            # 1. 获取当前窗口内容区域尺寸（确保是最新的）
            content_size = self._calculate_content_area_size()

            # 2. 确保ViewportManager有最新的尺寸信息
            viewport_mgr = ManagerFactory.get_viewport_manager()
            viewport_mgr.set_window_content_size(content_size.width, content_size.height, self.nswindow)

            # 3. 使用RootContainerManager创建具有正确尺寸的根容器
            root_container_mgr = ManagerFactory.get_root_container_manager()
            root_container = root_container_mgr.create_root_container(
                content_size.width, content_size.height
            )

            # 4. 挂载用户组件 - 此时百分比计算将基于正确的根容器尺寸
            logger.info("🔄 挂载用户组件...")
            user_nsview = component.mount()
            root_container.addSubview_(user_nsview)

            # 5. 配置用户组件的布局行为
            user_nsview.setTranslatesAutoresizingMaskIntoConstraints_(True)
            user_nsview.setFrame_(root_container.bounds())

            # 6. 设置为窗口内容
            self.nswindow.setContentView_(root_container)

            logger.info(f"✅ 窗口内容设置完成，根容器: {content_size.width:.1f}x{content_size.height:.1f}")

        else:
            logger.warning(f"⚠️ 组件 {component} 没有mount()方法")


class AppManager:
    """应用程序管理器 - 处理应用启动、窗口管理等"""

    _instance: Optional["AppManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self._app = None
        self._windows = []
        self._setup_application()
        logger.info("📱 AppManager初始化完成")

    def _setup_application(self):
        """设置NSApplication"""
        from AppKit import (
            NSApplication,
            NSApplicationActivationPolicyRegular,
            NSApp,
            NSMenu,
            NSMenuItem,
        )
        from Foundation import NSStringFromSelector, NSObject

        # 创建应用程序实例
        self._app = NSApplication.sharedApplication()
        self._app.setActivationPolicy_(NSApplicationActivationPolicyRegular)

        # 创建基本菜单栏
        main_menu = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        main_menu.addItem_(app_menu_item)

        app_menu = NSMenu.alloc().init()
        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", NSStringFromSelector("terminate:"), "q"
        )
        app_menu.addItem_(quit_item)
        app_menu_item.setSubmenu_(app_menu)

        self._app.setMainMenu_(main_menu)

    def create_window(self, title: str, width: int = 800, height: int = 600) -> AppWindow:
        """创建新窗口"""
        window = AppWindow(title, width, height)
        self._windows.append(window)
        return window

    def run(self):
        """运行应用程序"""
        from PyObjCTools import AppHelper

        logger.info("🚀 启动应用程序事件循环...")
        AppHelper.runEventLoop()

    def quit(self):
        """退出应用程序"""
        if self._app:
            self._app.terminate_(None)


# ================================
# 8. 管理器工厂
# ================================


class ManagerFactory:
    """管理器工厂 - 统一创建和管理所有管理器实例"""

    _app_manager: Optional[AppManager] = None
    _viewport_manager: Optional[ViewportManager] = None
    _layer_manager: Optional[LayerManager] = None
    _positioning_manager: Optional[PositioningManager] = None
    _transform_manager: Optional[TransformManager] = None
    _scroll_manager: Optional[ScrollManager] = None
    _mask_manager: Optional[MaskManager] = None
    _root_container_manager: Optional[RootContainerManager] = None
    _responsive_manager: Optional['ResponsiveManager'] = None

    @classmethod
    def get_app_manager(cls) -> AppManager:
        if cls._app_manager is None:
            cls._app_manager = AppManager()
        return cls._app_manager

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
    def get_root_container_manager(cls) -> RootContainerManager:
        if cls._root_container_manager is None:
            cls._root_container_manager = RootContainerManager()
        return cls._root_container_manager

    @classmethod
    def get_responsive_manager(cls) -> 'ResponsiveManager':
        if cls._responsive_manager is None:
            from .responsive import ResponsiveManager
            cls._responsive_manager = ResponsiveManager()
        return cls._responsive_manager

    @classmethod
    def initialize_all(cls):
        """初始化所有管理器"""
        logger.info("🏭 ManagerFactory: 初始化所有管理器...")
        cls.get_app_manager()
        cls.get_viewport_manager()
        cls.get_layer_manager()
        cls.get_positioning_manager()
        cls.get_transform_manager()
        cls.get_scroll_manager()
        cls.get_mask_manager()
        cls.get_root_container_manager()
        cls.get_responsive_manager()
        logger.info("✅ 所有管理器初始化完成！")


# ================================
# 8. 测试代码
# ================================

if __name__ == "__main__":
    logger.info("Hibiki UI v4.0 管理器系统测试")

    # 初始化所有管理器
    ManagerFactory.initialize_all()

    logger.info("🧪 管理器功能测试:")

    # 测试ViewportManager
    viewport_mgr = ManagerFactory.get_viewport_manager()
    logger.info(f"视口尺寸: {viewport_mgr.get_viewport_size()}")
    logger.info(f"50vw = {viewport_mgr.vw_to_px(50):.1f}px")

    # 测试LayerManager
    layer_mgr = ManagerFactory.get_layer_manager()
    logger.info(f"模态层级: {ZLayer.MODAL.value}")
    logger.info(f"自动Z-Index: {layer_mgr.get_auto_z_index(ZLayer.FLOATING)}")

    # 测试PositioningManager
    positioning_mgr = ManagerFactory.get_positioning_manager()
    logger.info(f"百分比解析: {positioning_mgr._resolve_position_value('50%', 800, 0)}px")

    logger.info("✅ 管理器系统测试完成！")
