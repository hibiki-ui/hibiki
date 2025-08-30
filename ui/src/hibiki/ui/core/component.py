#!/usr/bin/env python3
"""
Hibiki UI v4.0 组件核心架构
双层组件架构：Component (抽象基类) + UIComponent (具体基类)
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Union, Callable, Any, TypeVar, Tuple

from AppKit import NSView, NSColor
from Foundation import NSMakeRect

# HibikiContainerView不再需要 - 使用最小化Flip策略
# from .base_view import HibikiContainerView
from .animation import Animation, AnimationGroup, AnimationManager
from .api import HighLevelLayoutAPI, LowLevelLayoutAPI
from .layout import get_layout_engine
from .logging import get_logger
from .managers import (
    ManagerFactory,
    Position,
    OverflowBehavior,
)
from .reactive import Signal, Computed, Effect, create_signal, create_computed, create_effect
from .styles import ComponentStyle, Length, px

T = TypeVar("T")
logger = get_logger("core.component")


class Component(ABC):
    """Hibiki UI组件核心抽象基类

    职责：响应式状态管理、生命周期方法、子组件管理
    所有Hibiki UI组件的根基类，必须实现mount方法。
    """

    def __init__(self):
        self._signals: List = []
        self._computed: List = []
        self._effects: List = []
        self._bindings: List[Callable[[], None]] = []
        self._mounted = False
        self._cleanup_callbacks: List[Callable[[], None]] = []
        self._children: List["Component"] = []

    @abstractmethod
    def mount(self) -> NSView:
        """创建并返回NSView，所有子类必须实现"""
        raise NotImplementedError(
            f"{self.__class__.__module__}.{self.__class__.__qualname__} is "
            'missing the required "mount" function. '
            "All Hibiki UI components must implement this core method."
        )

    def create_signal(self, initial_value: T) -> Signal[T]:
        """创建组件作用域的Signal"""
        signal = create_signal(initial_value)
        self._signals.append(signal)
        return signal

    def create_computed(self, fn: Callable[[], T]) -> Computed[T]:
        """创建计算属性"""
        computed = create_computed(fn)
        self._computed.append(computed)
        return computed

    def create_effect(self, fn: Callable[[], None]) -> Effect:
        """创建副作用"""
        effect = create_effect(fn)
        self._effects.append(effect)
        return effect

    def animate(self, **properties) -> Optional["AnimationGroup"]:
        """动画化组件"""
        if not hasattr(self, "_mounted") or not hasattr(self, "_nsview"):
            return None
        if not self._mounted or not self._nsview:
            return None
        return AnimationManager.animate_view(self._nsview, **properties)

    def fade_in(self, duration: float = 1.0) -> Optional["Animation"]:
        """淡入动画"""
        if not hasattr(self, "_mounted") or not hasattr(self, "_nsview"):
            return None
        if not self._mounted or not self._nsview:
            return None
        return AnimationManager.fade_in(self._nsview, duration)

    def fade_out(self, duration: float = 1.0) -> Optional["Animation"]:
        """淡出动画"""
        if not hasattr(self, "_mounted") or not hasattr(self, "_nsview"):
            return None
        if not self._mounted or not self._nsview:
            return None
        return AnimationManager.fade_out(self._nsview, duration)

    def bounce(self, duration: float = 0.6) -> Optional["AnimationGroup"]:
        """弹性动画"""
        if not hasattr(self, "_mounted") or not hasattr(self, "_nsview"):
            return None
        if not self._mounted or not self._nsview:
            return None
        return AnimationManager.scale_bounce(self._nsview, duration)

    def add_child(self, child: "Component") -> None:
        if child not in self._children:
            self._children.append(child)

    def remove_child(self, child: "Component") -> None:
        if child in self._children:
            child.cleanup()
            self._children.remove(child)

    def on_cleanup(self, callback: Callable[[], None]) -> None:
        self._cleanup_callbacks.append(callback)

    def cleanup(self) -> None:
        """清理组件资源"""
        for cleanup_fn in self._bindings:
            try:
                cleanup_fn()
            except Exception as e:
                logger.error(f"绑定清理错误: {e}")
        self._bindings.clear()

        for effect in self._effects:
            try:
                if hasattr(effect, "cleanup"):
                    effect.cleanup()
            except Exception as e:
                logger.error(f"Effect清理错误: {e}")
        self._effects.clear()

        for child in self._children:
            try:
                child.cleanup()
            except Exception as e:
                logger.error(f"子组件清理错误: {e}")
        self._children.clear()

        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"清理回调错误: {e}")
        self._cleanup_callbacks.clear()

        try:
            engine = get_layout_engine()
            engine.cleanup_component(self)
        except Exception:
            pass

        if hasattr(self, "layer_manager"):
            try:
                self.layer_manager.unregister_component(self)
            except Exception:
                pass

        if (
            hasattr(self, "responsive_manager")
            and hasattr(self, "responsive_style")
            and self.responsive_style
        ):
            try:
                self.responsive_manager.unregister_component(self)
            except Exception:
                pass

        self._signals.clear()
        self._computed.clear()
        self._mounted = False


class UIComponent(Component):
    """Hibiki UI UI组件基类

    提供完整的布局API、层级管理、NSView集成和动画支持。
    """

    def __init__(
        self,
        style: Optional[ComponentStyle] = None,
        responsive_style: Optional[Any] = None,
        **style_kwargs,
    ):
        super().__init__()

        if style:
            self.style = style
        else:
            self.style = ComponentStyle(**style_kwargs)

        self.responsive_style = responsive_style

        self.viewport_manager = ManagerFactory.get_viewport_manager()
        self.layer_manager = ManagerFactory.get_layer_manager()
        self.positioning_manager = ManagerFactory.get_positioning_manager()
        self.transform_manager = ManagerFactory.get_transform_manager()
        self.scroll_manager = ManagerFactory.get_scroll_manager()
        self.mask_manager = ManagerFactory.get_mask_manager()
        self.responsive_manager = ManagerFactory.get_responsive_manager()

        self._nsview: Optional[NSView] = None
        self._raw_configurators: List[Callable[[NSView], None]] = []
        self._parent_container: Optional["UIComponent"] = None

        self.layout = HighLevelLayoutAPI(self)
        self.advanced = LowLevelLayoutAPI(self)

    def mount(self) -> NSView:
        """挂载UI组件"""
        if self._nsview is None:
            self._nsview = self._create_nsview()
            self.layer_manager.register_component(self, self.style.z_index)
            self._apply_positioning_and_layout()
            self.transform_manager.apply_transforms(self._nsview, self.style)

            if self.style.clip_rect:
                self.mask_manager.apply_clip_mask(self._nsview, self.style.clip_rect)

            if self.style.overflow in [OverflowBehavior.SCROLL, OverflowBehavior.AUTO]:
                original_view = self._nsview

                self._nsview = self.scroll_manager.create_scroll_view(
                    original_view, self.style.overflow
                )

                # 🔧 关键修复：不要在mount时设置frame
                # NSScrollView的frame将在_apply_layout_result中正确设置
                # 这里只需要创建ScrollView结构即可

            for configurator in self._raw_configurators:
                try:
                    configurator(self._nsview)
                except Exception as e:
                    logger.error(f"原始配置器执行失败: {e}")

            self._apply_basic_style()

            if self.responsive_style:
                self.responsive_manager.register_component(self)

            self._mounted = True

        return self._nsview

    @abstractmethod
    def _create_nsview(self) -> NSView:
        """子类必须实现此方法来创建具体的NSView"""
        raise NotImplementedError("子类必须实现 _create_nsview 方法")

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

        except Exception as e:
            logger.error(f"绝对定位应用失败: {e}")
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
                    current_frame.size.height,
                )
                self._nsview.setFrame_(new_frame)

        except Exception as e:
            logger.error(f"相对定位应用失败: {e}")

    def _apply_stretchable_layout(self):
        """应用v4 Stretchable布局"""
        try:
            engine = get_layout_engine()

            # 检查是否是容器根节点
            has_children = hasattr(self, "children") and len(getattr(self, "children", [])) > 0
            has_no_parent = getattr(self, "_parent_container", None) is None
            is_root_container = has_children and has_no_parent

            # 检查是否是子组件
            is_child_component = getattr(self, "_parent_container", None) is not None

            # 调试信息

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

                    # 递归应用所有子组件的布局 - 使用Stretchable计算结果
                    self._apply_children_layout(engine)

                    return True
                else:
                    raise ValueError(f"v4根容器布局计算失败: {self.__class__.__name__}")
            elif is_child_component:
                # 子组件：完全跳过布局处理，等父容器处理
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
                    return True
                else:
                    raise ValueError(f"v4独立组件布局计算失败: {self.__class__.__name__}")

        except Exception as e:
            logger.error(f"布局应用失败: {e}")
            import traceback

            traceback.print_exc()
            # v4应该完全依赖Stretchable布局引擎，不提供回退方案
            raise e

    def _get_available_size_from_parent(self) -> Optional[Tuple[float, float]]:
        """从父容器获取可用尺寸"""
        if self._parent_container and hasattr(self._parent_container, "_nsview"):
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
        frame = NSMakeRect(
            layout_result.x, layout_result.y, layout_result.width, layout_result.height
        )
        self._nsview.setFrame_(frame)

        # 🔧 关键修复：强制禁用Auto Layout，让手动frame设置生效
        # Hibiki UI使用自己的布局引擎，不应与Auto Layout冲突
        self._nsview.setTranslatesAutoresizingMaskIntoConstraints_(True)
        self._nsview.setAutoresizingMask_(0)  # 禁用所有自动调整行为

    def _apply_children_layout_from_stretchable(self, engine):
        """从Stretchable重建树应用子组件布局（简化版本）"""
        if not hasattr(self, "children"):
            return

        # 简化版本：直接为每个子组件设置合理的布局
        try:
            y_offset = 0
            x_offset = 0

            for i, child in enumerate(self.children):
                if hasattr(child, "_nsview") and child._nsview:
                    try:
                        # 根据组件类型设置基本尺寸
                        if child.__class__.__name__ == "Label":
                            width, height = 300, 30
                        elif child.__class__.__name__ == "Button":
                            width, height = 120, 35
                        else:
                            width, height = 200, 30

                        # 应用简单的垂直堆叠布局
                        child._apply_layout_result(
                            type(
                                "LayoutResult",
                                (),
                                {
                                    "x": x_offset,
                                    "y": y_offset,
                                    "width": width,
                                    "height": height,
                                    "content_width": width,
                                    "content_height": height,
                                    "compute_time": 0,
                                },
                            )()
                        )

                        # 更新偏移
                        y_offset += height + 10  # 10px 间距

                    except Exception as e:
                        logger.error(f"v4子组件简单布局应用异常: {child.__class__.__name__} - {e}")
                        child._apply_fallback_frame()

        except Exception as e:
            logger.error(f"子组件简单布局应用整体异常: {e}")
            # 不再抛出异常，避免崩溃

    def _apply_simple_children_layout(self):
        """安全的简单子组件布局应用"""
        if not hasattr(self, "children") or not self.children:
            return

        y = 20  # 从顶部20px开始
        for child in self.children:
            if hasattr(child, "_nsview") and child._nsview:
                # 设置简单的垂直堆叠布局
                if child.__class__.__name__ == "Label":
                    w, h = 400, 30
                elif child.__class__.__name__ == "Button":
                    w, h = 150, 35
                elif child.__class__.__name__ == "Container":
                    w, h = 500, 200  # Container更大一些
                else:
                    w, h = 300, 30

                # 直接设置frame，避免复杂的LayoutResult
                frame = NSMakeRect(20, y, w, h)  # x=20px 左边距
                child._nsview.setFrame_(frame)

                y += h + 15  # 15px间距

    def _apply_children_layout(self, engine):
        """递归应用子组件的布局"""
        if not hasattr(self, "children"):
            return

        for child in self.children:
            if hasattr(child, "_nsview") and child._nsview:
                # 获取子组件的布局节点
                child_node = engine.get_node_for_component(child)
                if child_node:
                    try:

                        # 获取子组件的布局结果
                        box = child_node._stretchable_node.get_box()
                        x, y, width, height = box.x, box.y, box.width, box.height

                        # 应用到子组件的NSView
                        child._apply_layout_result(
                            type(
                                "LayoutResult",
                                (),
                                {"x": x, "y": y, "width": width, "height": height},
                            )()
                        )

                        # 递归处理子组件的子组件
                        if hasattr(child, "_apply_children_layout"):
                            child._apply_children_layout(engine)

                    except Exception as e:
                        import traceback

                        logger.error(f"子组件布局应用失败: {child.__class__.__name__} - {e}")
                        logger.error(f"异常详情: {type(e).__name__}: {str(e)}")
                        traceback.print_exc()
                        child._apply_fallback_frame()

    def _resolve_size_value(self, length_value, default: float) -> float:
        """解析尺寸值为像素"""
        if length_value is None:
            return default
        if hasattr(length_value, "value"):
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

        # 设置背景色
        if self.style.background_color:
            color = self._parse_color(self.style.background_color)
            if color:
                self._nsview.setWantsLayer_(True)
                self._nsview.layer().setBackgroundColor_(color.CGColor())

        # 设置边框
        if self.style.border_color or self.style.border_width:
            self._apply_border_style()

    def _parse_color(self, color_str: str):
        """解析颜色字符串为NSColor"""
        if not color_str:
            return None

        # 处理十六进制颜色 #RRGGBB
        if color_str.startswith("#") and len(color_str) == 7:
            try:
                r = int(color_str[1:3], 16) / 255.0
                g = int(color_str[3:5], 16) / 255.0
                b = int(color_str[5:7], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
            except ValueError:
                logger.warning(f"无法解析颜色: {color_str}")
                return None

        # 处理简单颜色名称
        color_map = {
            "red": NSColor.redColor(),
            "green": NSColor.greenColor(),
            "blue": NSColor.blueColor(),
            "white": NSColor.whiteColor(),
            "black": NSColor.blackColor(),
            "gray": NSColor.grayColor(),
            "yellow": NSColor.yellowColor(),
        }
        return color_map.get(color_str.lower())

    def _apply_border_style(self):
        """应用边框样式"""
        if not self._nsview:
            return

        self._nsview.setWantsLayer_(True)
        layer = self._nsview.layer()

        # 边框宽度
        if self.style.border_width:
            if isinstance(self.style.border_width, Length):
                width = self.style.border_width.value
            else:
                width = self.style.border_width
            layer.setBorderWidth_(float(width))

        # 边框颜色
        if self.style.border_color:
            color = self._parse_color(self.style.border_color)
            if color:
                layer.setBorderColor_(color.CGColor())

        # 圆角
        if self.style.border_radius:
            if isinstance(self.style.border_radius, Length):
                radius = self.style.border_radius.value
            else:
                radius = self.style.border_radius
            layer.setCornerRadius_(float(radius))

    # ================================
    # 便捷方法
    # ================================

    def size(
        self, width: Optional[Union[int, float]] = None, height: Optional[Union[int, float]] = None
    ) -> "UIComponent":
        """便捷的尺寸设置方法"""
        if width is not None:
            self.style.width = px(width)
        if height is not None:
            self.style.height = px(height)

        return self

    def opacity(self, value: float) -> "UIComponent":
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

    def __init__(
        self,
        children: Optional[List[UIComponent]] = None,
        style: Optional[ComponentStyle] = None,
        **style_kwargs,
    ):
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
        """🔧 修复坐标系Bug：使用HibikiContainerView确保正确的top-left坐标系"""
        # 🎯 使用HibikiContainerView而不是普通NSView
        # 确保每个容器都有正确的isFlipped=True坐标系转换
        from .base_view import HibikiContainerView
        container = HibikiContainerView.alloc().init()

        # 建立v4布局树关系
        try:
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

                except Exception as e:
                    logger.error(f"子组件 {i+1} 挂载失败: {e}")
        except Exception as e:
            logger.error(f"Container v4布局树构建失败: {e}")
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
        if self._nsview and hasattr(child, "mount"):
            try:
                # 设置父子关系
                child._parent_container = self

                # 添加到布局系统
                engine = get_layout_engine()
                engine.add_child_relationship(self, child, len(self.children) - 1)

                # 挂载NSView
                child_view = child.mount()
                self._nsview.addSubview_(child_view)

                # 重新计算布局
                self._update_layout()

            except Exception as e:
                logger.error(f"动态添加子组件失败: {e}")

    def remove_child_component(self, child: UIComponent):
        """移除子组件"""
        if child in self.children:
            try:
                # 从NSView移除
                if self._nsview and hasattr(child, "_nsview") and child._nsview:
                    child._nsview.removeFromSuperview()

                # 从布局系统移除
                engine = get_layout_engine()
                engine.remove_child_relationship(self, child)

                # 从children列表移除
                self.children.remove(child)
                self.remove_child(child)

                # 清理子组件资源
                child.cleanup()

                # 重新计算布局
                self._update_layout()

            except Exception as e:
                logger.error(f"动态移除子组件失败: {e}")

    def clear_children(self):
        """清空所有子组件"""
        if not self.children:
            return

        try:
            # 在清空前先获得布局引擎引用
            engine = get_layout_engine()

            # 批量移除所有子组件 - 关键修复：彻底清理布局关系
            children_copy = self.children.copy()  # 避免在迭代中修改列表
            for child in children_copy:
                # 先从布局引擎移除关系
                try:
                    engine.remove_child_relationship(self, child)
                except Exception as layout_e:
                    logger.warning(f"清理布局关系失败（可忽略）: {layout_e}")

                # 再移除UI关系
                self.remove_child_component(child)

            # 额外保险：强制重建当前容器的布局节点
            try:
                current_node = engine.get_node_for_component(self)
                if current_node:
                    engine._deep_cleanup_node(current_node)
                    # 重新创建干净的布局节点
                    if self in engine._component_nodes:
                        del engine._component_nodes[self]
                    engine.create_node_for_component(self)
            except Exception as rebuild_e:
                logger.warning(f"重建容器布局节点失败（可忽略）: {rebuild_e}")

        except Exception as e:
            logger.error(f"清空子组件失败: {e}")

    def replace_child_component(self, old_child: UIComponent, new_child: UIComponent):
        """替换子组件"""
        if old_child not in self.children:
            logger.warning(f"要替换的子组件不存在: {old_child.__class__.__name__}")
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
            if self._nsview and hasattr(new_child, "mount"):
                # 设置父子关系
                new_child._parent_container = self

                engine = get_layout_engine()
                engine.add_child_relationship(self, new_child, index)

                # 挂载NSView
                new_child_view = new_child.mount()
                self._nsview.addSubview_(new_child_view)

                # 重新计算布局
                self._update_layout()

        except Exception as e:
            logger.error(f"替换子组件失败: {e}")

    def set_children(self, new_children: List[UIComponent]):
        """批量设置子组件（替换所有现有子组件）"""
        try:
            # 先清空现有子组件
            self.clear_children()

            # 添加新的子组件
            for child in new_children:
                self.add_child_component(child)

        except Exception as e:
            logger.error(f"批量设置子组件失败: {e}")

    def _update_layout(self):
        """更新布局（在子组件变化后调用）"""
        if self._nsview:
            try:

                engine = get_layout_engine()

                # 重新计算布局 - 使用正确的方法
                # 检查布局引擎中是否有该组件的节点
                layout_node = engine.get_node_for_component(self)
                if layout_node:
                    # 获取当前容器的可用尺寸
                    available_size = self._get_available_size_from_parent()

                    # 重新计算布局
                    layout_result = engine.compute_layout_for_component(self, available_size)
                    if layout_result:
                        # 应用容器本身的布局
                        self._apply_layout_result(layout_result)

                        # 应用子组件布局
                        self._apply_children_layout(engine)

                    else:
                        logger.error(f"容器布局计算失败: {self.__class__.__name__}")
                else:
                    logger.warning(
                        f"容器在布局引擎中没有节点，需要重新创建: {self.__class__.__name__}"
                    )
                    # 如果容器节点不存在，重新创建
                    try:
                        layout_node = engine.create_node_for_component(self)
                        if layout_node:
                            # 重新建立所有子组件的布局关系
                            for i, child in enumerate(self.children):
                                engine.add_child_relationship(self, child, i)

                            # 重新计算布局
                            available_size = self._get_available_size_from_parent()
                            layout_result = engine.compute_layout_for_component(
                                self, available_size
                            )
                            if layout_result:
                                self._apply_layout_result(layout_result)
                                self._apply_children_layout(engine)
                    except Exception as rebuild_e:
                        logger.error(f"重建容器布局节点失败: {rebuild_e}")

            except Exception as e:
                logger.error(f"更新布局失败: {e}")
                import traceback

                traceback.print_exc()
