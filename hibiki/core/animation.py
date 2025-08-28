#!/usr/bin/env python3
"""
Hibiki UI v4 动画系统

基于Pure Core Animation原则的动画系统实现，遵循以下设计要求：
1. Pure Core Animation - 仅使用Core Animation APIs，禁用threading/time.sleep
2. Hardware Acceleration First - 优先使用GPU加速的CALayer属性
3. Declarative API - 提供简单的链式接口隐藏Core Animation复杂性
4. Signal Integration - 与Hibiki UI的响应式Signal系统无缝集成

作者: Claude Code AI Assistant
日期: 2025-08-28
版本: v4.0.0
"""

import logging
from typing import Optional, Callable, Dict, Any, List, Union
from enum import Enum

try:
    from Cocoa import NSView
    from Quartz import (
        CALayer, CAAnimationGroup, CABasicAnimation, CAKeyframeAnimation,
        CATransaction, CAMediaTimingFunctionName, CAMediaTimingFunction
    )
    CORE_ANIMATION_AVAILABLE = True
except ImportError:
    try:
        # 备用导入路径
        from AppKit import NSView
        from QuartzCore import (
            CALayer, CAAnimationGroup, CABasicAnimation, CAKeyframeAnimation,
            CATransaction, CAMediaTimingFunctionName, CAMediaTimingFunction
        )
        CORE_ANIMATION_AVAILABLE = True
    except ImportError:
        # 测试环境fallback
        CALayer = None
        CAAnimationGroup = None
        CABasicAnimation = None
        CAKeyframeAnimation = None
        CATransaction = None
        CAMediaTimingFunctionName = None
        CAMediaTimingFunction = None
        NSView = None
        CORE_ANIMATION_AVAILABLE = False

from .reactive import Signal, Effect

logger = logging.getLogger(__name__)


class AnimationCurve(Enum):
    """动画曲线类型 - 基于Core Animation内置曲线"""
    LINEAR = "linear"
    EASE_IN = "easeIn"
    EASE_OUT = "easeOut"
    EASE_IN_OUT = "easeInEaseOut"
    DEFAULT = "default"  # 系统默认曲线


class AnimationProperty(Enum):
    """可动画的属性类型 - 仅GPU优化属性"""
    OPACITY = "opacity"
    SCALE = "transform.scale.xy"
    SCALE_X = "transform.scale.x"
    SCALE_Y = "transform.scale.y"
    ROTATION = "transform.rotation.z"
    POSITION_X = "position.x"
    POSITION_Y = "position.y"
    SHADOW_OPACITY = "shadowOpacity"
    SHADOW_RADIUS = "shadowRadius"
    CORNER_RADIUS = "cornerRadius"
    BACKGROUND_COLOR = "backgroundColor"


class AnimationState(Enum):
    """动画状态"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Animation:
    """
    Core Animation基础动画类
    
    提供声明式API来创建和管理CABasicAnimation，隐藏PyObjC复杂性。
    所有动画都运行在GPU上，使用硬件加速。
    """
    
    def __init__(self,
                 property_name: Union[AnimationProperty, str],
                 duration: float = 1.0,
                 from_value: Optional[Any] = None,
                 to_value: Optional[Any] = None,
                 curve: AnimationCurve = AnimationCurve.EASE_IN_OUT):
        """
        初始化动画
        
        Args:
            property_name: 要动画的属性名称
            duration: 动画持续时间（秒）
            from_value: 起始值（None表示当前值）
            to_value: 目标值
            curve: 动画曲线
        """
        self.property_name = property_name.value if isinstance(property_name, AnimationProperty) else property_name
        self.duration = duration
        self.from_value = from_value
        self.to_value = to_value
        self.curve = curve
        
        # 状态管理
        self.state = Signal(AnimationState.IDLE)
        self._ca_animation: Optional['CABasicAnimation'] = None
        self._completion_callbacks: List[Callable] = []
        
        # Core Animation对象（延迟创建）
        self._ca_animation = None
        
        logger.debug(f"📱 创建动画: {self.property_name} ({duration}s)")
    
    def on_completion(self, callback: Callable[[], None]) -> 'Animation':
        """
        添加完成回调
        
        Args:
            callback: 动画完成时的回调函数
            
        Returns:
            self，支持链式调用
        """
        self._completion_callbacks.append(callback)
        return self
    
    def _create_ca_animation(self) -> 'CABasicAnimation':
        """
        创建Core Animation动画对象
        
        Returns:
            配置好的CABasicAnimation对象
        """
        if not CABasicAnimation:
            logger.warning("⚠️ Core Animation不可用，跳过动画创建")
            return None
            
        animation = CABasicAnimation.animationWithKeyPath_(self.property_name)
        animation.setDuration_(self.duration)
        
        # 设置起始和目标值
        if self.from_value is not None:
            animation.setFromValue_(self.from_value)
        if self.to_value is not None:
            animation.setToValue_(self.to_value)
        
        # 设置动画曲线
        timing_function_name = self._get_timing_function_name()
        if timing_function_name and CAMediaTimingFunction:
            try:
                timing_function = CAMediaTimingFunction.functionWithName_(timing_function_name)
                animation.setTimingFunction_(timing_function)
            except Exception as e:
                logger.debug(f"设置动画曲线失败: {e}, 使用默认曲线")
        
        # 保持动画结束状态
        animation.setFillMode_("kCAFillModeForwards")
        animation.setRemovedOnCompletion_(False)
        
        return animation
    
    def _get_timing_function_name(self) -> Optional[str]:
        """获取Core Animation时间函数名称"""
        if not CAMediaTimingFunctionName:
            return None
            
        timing_map = {
            AnimationCurve.LINEAR: "kCAMediaTimingFunctionLinear",
            AnimationCurve.EASE_IN: "kCAMediaTimingFunctionEaseIn",
            AnimationCurve.EASE_OUT: "kCAMediaTimingFunctionEaseOut", 
            AnimationCurve.EASE_IN_OUT: "kCAMediaTimingFunctionEaseInEaseOut",
            AnimationCurve.DEFAULT: "kCAMediaTimingFunctionDefault"
        }
        return timing_map.get(self.curve)
    
    def apply_to_layer(self, layer: 'CALayer') -> bool:
        """
        将动画应用到CALayer
        
        Args:
            layer: 目标CALayer
            
        Returns:
            是否成功应用动画
        """
        if not layer:
            logger.warning("⚠️ 无效的layer")
            return False
            
        if not CATransaction:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return False
        
        try:
            # 创建Core Animation动画
            self._ca_animation = self._create_ca_animation()
            if not self._ca_animation:
                return False
            
            # 使用CATransaction管理动画完成回调
            CATransaction.begin()
            
            # 设置完成回调
            def completion_block():
                self.state.value = AnimationState.COMPLETED
                for callback in self._completion_callbacks:
                    try:
                        callback()
                    except Exception as e:
                        logger.error(f"❌ 动画完成回调错误: {e}")
            
            CATransaction.setCompletionBlock_(completion_block)
            
            # 添加动画到图层
            animation_key = f"hibiki_animation_{id(self)}"
            layer.addAnimation_forKey_(self._ca_animation, animation_key)
            
            # 提交事务
            CATransaction.commit()
            
            self.state.value = AnimationState.RUNNING
            logger.debug(f"✅ 动画已应用到layer: {self.property_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 应用动画失败: {e}")
            self.state.value = AnimationState.CANCELLED
            return False


class AnimationGroup:
    """
    动画组 - 管理多个同时执行的动画
    
    基于CAAnimationGroup实现，允许多个动画同步执行。
    """
    
    def __init__(self, animations: List[Animation], duration: Optional[float] = None):
        """
        初始化动画组
        
        Args:
            animations: 动画列表
            duration: 组动画持续时间（None表示使用最长的动画时间）
        """
        self.animations = animations
        self.duration = duration or max((anim.duration for anim in animations), default=1.0)
        
        # 状态管理
        self.state = Signal(AnimationState.IDLE)
        self._completion_callbacks: List[Callable] = []
        
        logger.debug(f"📦 创建动画组: {len(animations)}个动画, 时长{self.duration}s")
    
    def on_completion(self, callback: Callable[[], None]) -> 'AnimationGroup':
        """添加完成回调"""
        self._completion_callbacks.append(callback)
        return self
    
    def apply_to_layer(self, layer: 'CALayer') -> bool:
        """
        将动画组应用到CALayer
        
        Args:
            layer: 目标CALayer
            
        Returns:
            是否成功应用动画组
        """
        if not layer:
            logger.warning("⚠️ 无效的layer")
            return False
            
        if not CAAnimationGroup or not CATransaction:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return False
        
        try:
            # 创建动画组
            animation_group = CAAnimationGroup.animation()
            animation_group.setDuration_(self.duration)
            
            # 收集所有CAAnimation对象
            ca_animations = []
            for animation in self.animations:
                ca_anim = animation._create_ca_animation()
                if ca_anim:
                    ca_animations.append(ca_anim)
            
            if not ca_animations:
                logger.warning("⚠️ 没有有效的动画可执行")
                return False
            
            animation_group.setAnimations_(ca_animations)
            animation_group.setFillMode_("kCAFillModeForwards")
            animation_group.setRemovedOnCompletion_(False)
            
            # 使用CATransaction管理完成回调
            CATransaction.begin()
            
            def completion_block():
                self.state.value = AnimationState.COMPLETED
                # 更新所有子动画状态
                for animation in self.animations:
                    animation.state.value = AnimationState.COMPLETED
                
                # 执行回调
                for callback in self._completion_callbacks:
                    try:
                        callback()
                    except Exception as e:
                        logger.error(f"❌ 动画组完成回调错误: {e}")
            
            CATransaction.setCompletionBlock_(completion_block)
            
            # 添加动画组到图层
            group_key = f"hibiki_animation_group_{id(self)}"
            layer.addAnimation_forKey_(animation_group, group_key)
            
            CATransaction.commit()
            
            self.state.value = AnimationState.RUNNING
            for animation in self.animations:
                animation.state.value = AnimationState.RUNNING
            
            logger.debug(f"✅ 动画组已应用到layer")
            return True
            
        except Exception as e:
            logger.error(f"❌ 应用动画组失败: {e}")
            self.state.value = AnimationState.CANCELLED
            return False


class AnimationManager:
    """
    动画管理器 - 提供高级动画API和预设效果
    
    提供简单的声明式接口来创建常用动画效果，
    并与Hibiki UI的Signal系统集成。
    """
    
    @staticmethod
    def animate_view(view: 'NSView', **properties) -> Optional[AnimationGroup]:
        """
        动画化视图属性
        
        Args:
            view: 目标NSView
            **properties: 动画属性，支持:
                - opacity: 透明度 (0.0-1.0)
                - scale: 缩放 (float)
                - rotation: 旋转角度 (度)
                - duration: 持续时间 (默认1.0秒)
                - curve: 动画曲线 (AnimationCurve)
                
        Returns:
            创建的动画组，如果失败则返回None
        """
        if not view:
            logger.warning("⚠️ 无效的视图，无法执行动画")
            return None
            
        # 检查 Core Animation 可用性
        if not CORE_ANIMATION_AVAILABLE:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return None
        
        # 确保视图有 CALayer 支持
        if not hasattr(view, 'setWantsLayer_') or not hasattr(view, 'layer'):
            logger.warning("⚠️ 视图不支持 CALayer")
            return None
        
        # 获取或创建视图的图层
        layer = view.layer()
        if not layer:
            try:
                # 启用 layer-backed view
                view.setWantsLayer_(True)
                layer = view.layer()
                if layer:
                    logger.debug("✅ 成功为视图创建 CALayer")
                else:
                    logger.warning("⚠️ 无法为视图创建 CALayer")
                    return None
            except Exception as e:
                logger.warning(f"⚠️ 创建图层失败: {e}")
                return None
        
        # 解析动画参数
        duration = properties.pop('duration', 1.0)
        curve = properties.pop('curve', AnimationCurve.EASE_IN_OUT)
        
        # 创建动画列表
        animations = []
        
        # 透明度动画
        if 'opacity' in properties:
            opacity_anim = Animation(
                AnimationProperty.OPACITY,
                duration=duration,
                to_value=properties['opacity'],
                curve=curve
            )
            animations.append(opacity_anim)
        
        # 缩放动画
        if 'scale' in properties:
            scale_value = properties['scale']
            scale_anim = Animation(
                AnimationProperty.SCALE,
                duration=duration,
                to_value=scale_value,
                curve=curve
            )
            animations.append(scale_anim)
        
        # 旋转动画
        if 'rotation' in properties:
            # 将度数转换为弧度
            import math
            rotation_radians = math.radians(properties['rotation'])
            rotation_anim = Animation(
                AnimationProperty.ROTATION,
                duration=duration,
                to_value=rotation_radians,
                curve=curve
            )
            animations.append(rotation_anim)
        
        if not animations:
            logger.warning("⚠️ 没有指定有效的动画属性")
            return None
        
        # 创建动画组并应用
        animation_group = AnimationGroup(animations, duration)
        if animation_group.apply_to_layer(layer):
            return animation_group
        
        return None
    
    @staticmethod
    def fade_in(view: 'NSView', duration: float = 1.0) -> Optional[Animation]:
        """淡入动画预设"""
        if not view:
            return None
            
        # 检查 Core Animation 可用性
        if not CORE_ANIMATION_AVAILABLE:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return None
        
        # 获取或创建图层
        layer = view.layer()
        if not layer:
            try:
                view.setWantsLayer_(True)
                layer = view.layer()
            except Exception as e:
                logger.warning(f"⚠️ 创建图层失败: {e}")
                return None
        
        if layer:
            # 设置初始透明度
            layer.setOpacity_(0.0)
            
            fade_anim = Animation(
                AnimationProperty.OPACITY,
                duration=duration,
                from_value=0.0,
                to_value=1.0,
                curve=AnimationCurve.EASE_OUT
            )
            
            if fade_anim.apply_to_layer(layer):
                return fade_anim
        
        return None
    
    @staticmethod
    def fade_out(view: 'NSView', duration: float = 1.0) -> Optional[Animation]:
        """淡出动画预设"""
        if not view:
            return None
            
        # 检查 Core Animation 可用性
        if not CORE_ANIMATION_AVAILABLE:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return None
        
        # 获取或创建图层
        layer = view.layer()
        if not layer:
            try:
                view.setWantsLayer_(True)
                layer = view.layer()
            except Exception as e:
                logger.warning(f"⚠️ 创建图层失败: {e}")
                return None
        
        if layer:
            fade_anim = Animation(
                AnimationProperty.OPACITY,
                duration=duration,
                to_value=0.0,
                curve=AnimationCurve.EASE_IN
            )
            
            if fade_anim.apply_to_layer(layer):
                return fade_anim
        
        return None
    
    @staticmethod
    def scale_bounce(view: 'NSView', duration: float = 0.6) -> Optional[AnimationGroup]:
        """弹性缩放动画预设"""
        if not view:
            return None
            
        # 检查 Core Animation 可用性
        if not CORE_ANIMATION_AVAILABLE:
            logger.warning("⚠️ Core Animation不可用 (测试环境)")
            return None
        
        # 获取或创建图层
        layer = view.layer()
        if not layer:
            try:
                view.setWantsLayer_(True)
                layer = view.layer()
            except Exception as e:
                logger.warning(f"⚠️ 创建图层失败: {e}")
                return None
        
        if layer:
            # 创建多阶段缩放动画
            scale_up = Animation(
                AnimationProperty.SCALE,
                duration=duration * 0.3,
                to_value=1.2,
                curve=AnimationCurve.EASE_OUT
            )
            
            scale_down = Animation(
                AnimationProperty.SCALE,
                duration=duration * 0.7,
                from_value=1.2,
                to_value=1.0,
                curve=AnimationCurve.EASE_IN_OUT
            )
            
            bounce_group = AnimationGroup([scale_up], duration * 0.3)
            bounce_group.on_completion(lambda: scale_down.apply_to_layer(layer))
            
            if bounce_group.apply_to_layer(layer):
                return bounce_group
        
        return None


# 便捷函数 - 提供简洁的API
def animate(view: 'NSView', **properties) -> Optional[AnimationGroup]:
    """
    便捷动画函数
    
    Usage:
        animate(my_view, opacity=0.5, scale=1.2, duration=2.0)
    """
    return AnimationManager.animate_view(view, **properties)


def fade_in(view: 'NSView', duration: float = 1.0) -> Optional[Animation]:
    """便捷淡入函数"""
    return AnimationManager.fade_in(view, duration)


def fade_out(view: 'NSView', duration: float = 1.0) -> Optional[Animation]:
    """便捷淡出函数"""
    return AnimationManager.fade_out(view, duration)


def bounce(view: 'NSView', duration: float = 0.6) -> Optional[AnimationGroup]:
    """便捷弹性动画函数"""
    return AnimationManager.scale_bounce(view, duration)


# 导出公共API
__all__ = [
    'Animation',
    'AnimationGroup', 
    'AnimationManager',
    'AnimationCurve',
    'AnimationProperty',
    'AnimationState',
    'animate',
    'fade_in',
    'fade_out',
    'bounce'
]