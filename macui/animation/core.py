"""macUI v3.0 动画核心

提供基础动画类和函数，封装Core Animation的复杂性，
提供简洁的声明式接口。
"""

from typing import Union, Optional, Dict, Any, List, Callable
from AppKit import NSView, CATransaction, CABasicAnimation, CAAnimationGroup, CAKeyframeAnimation, CASpringAnimation
from AppKit import CAMediaTimingFunction
from Foundation import NSValue, NSMakePoint
from Quartz import CATransform3DMakeScale
import time

from ..core.signal import Signal, Effect


class TimingFunction:
    """动画时间函数"""
    LINEAR = "linear"
    EASE_IN = "easeIn" 
    EASE_OUT = "easeOut"
    EASE_IN_OUT = "easeInOut"
    SPRING = "spring"


class Animation:
    """基础动画类 - 封装CABasicAnimation"""
    
    def __init__(
        self,
        duration: float = 0.3,
        timing: str = TimingFunction.EASE_OUT,
        delay: float = 0.0,
        repeat_count: float = 1.0,
        auto_reverse: bool = False
    ):
        self.duration = duration
        self.timing = timing
        self.delay = delay
        self.repeat_count = repeat_count
        self.auto_reverse = auto_reverse
        self._completion_callbacks: List[Callable] = []
    
    def on_completion(self, callback: Callable) -> 'Animation':
        """设置动画完成回调"""
        self._completion_callbacks.append(callback)
        return self
    
    def _create_ca_animation(self, property_path: str, from_value: Any, to_value: Any) -> CABasicAnimation:
        """创建CABasicAnimation对象"""
        animation = CABasicAnimation.animationWithKeyPath_(property_path)
        animation.setDuration_(self.duration)
        animation.setFromValue_(from_value)
        animation.setToValue_(to_value)
        animation.setBeginTime_(time.time() + self.delay if self.delay > 0 else 0)
        animation.setRepeatCount_(self.repeat_count)
        animation.setAutoreverses_(self.auto_reverse)
        
        # 设置时间函数
        timing_func = CAMediaTimingFunction.functionWithName_(self._get_timing_name())
        animation.setTimingFunction_(timing_func)
        
        return animation
    
    def _get_timing_name(self) -> str:
        """获取CAMediaTimingFunction名称"""
        # 使用字符串常量，兼容性更好
        timing_map = {
            TimingFunction.LINEAR: "linear",
            TimingFunction.EASE_IN: "easeIn", 
            TimingFunction.EASE_OUT: "easeOut",
            TimingFunction.EASE_IN_OUT: "easeInEaseOut"
        }
        return timing_map.get(self.timing, "easeOut")


class AnimationGroup:
    """动画组 - 可以同时执行多个动画"""
    
    def __init__(self, animations: List[Animation], duration: Optional[float] = None):
        self.animations = animations
        self.duration = duration or max(a.duration for a in animations)
    
    def play_on(self, view: NSView, **properties):
        """在指定视图上播放动画组"""
        group = CAAnimationGroup.animation()
        group.setDuration_(self.duration)
        
        ca_animations = []
        for animation in self.animations:
            # 这里需要根据具体动画类型创建相应的Core Animation对象
            pass
        
        group.setAnimations_(ca_animations)
        view.layer().addAnimation_forKey_(group, "animationGroup")


def animate(
    view: NSView,
    duration: float = 0.3,
    timing: str = TimingFunction.EASE_OUT,
    **properties
) -> Animation:
    """简洁的动画函数
    
    用法:
    animate(my_label, duration=0.5, position=(100, 100), opacity=0.5)
    """
    animation = Animation(duration=duration, timing=timing)
    
    CATransaction.begin()
    CATransaction.setAnimationDuration_(duration)
    
    for prop, value in properties.items():
        if prop == "position":
            ca_anim = animation._create_ca_animation("position", None, NSValue.valueWithPoint_(NSMakePoint(*value)))
            view.layer().addAnimation_forKey_(ca_anim, f"animate_{prop}")
        elif prop == "opacity":
            ca_anim = animation._create_ca_animation("opacity", None, value)
            view.layer().addAnimation_forKey_(ca_anim, f"animate_{prop}")
        elif prop == "scale":
            # 简化缩放动画 - 使用更基础的API
            ca_anim = animation._create_ca_animation("transform.scale", None, value)
            view.layer().addAnimation_forKey_(ca_anim, f"animate_{prop}")
    
    CATransaction.commit()
    
    print(f"🎬 动画开始: duration={duration}, properties={list(properties.keys())}")
    return animation


def animate_to(view: NSView, signal: Signal, **animations) -> Effect:
    """Signal驱动的响应式动画
    
    用法:
    animate_to(my_label, position_signal, position=lambda pos: pos, opacity=lambda pos: 0.8)
    """
    def reactive_animate():
        current_value = signal.value
        properties = {}
        
        for prop, value_func in animations.items():
            properties[prop] = value_func(current_value)
        
        animate(view, **properties)
    
    effect = Effect(reactive_animate)
    print(f"🔄 响应式动画绑定: Signal -> {list(animations.keys())}")
    return effect


class KeyframeAnimation(Animation):
    """关键帧动画"""
    
    def __init__(self, keyframes: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.keyframes = keyframes
    
    def play_on(self, view: NSView, property_path: str):
        """在指定视图播放关键帧动画"""
        animation = CAKeyframeAnimation.animationWithKeyPath_(property_path)
        animation.setDuration_(self.duration)
        
        values = [kf.get('value') for kf in self.keyframes]
        times = [kf.get('time', i / (len(self.keyframes) - 1)) for i, kf in enumerate(self.keyframes)]
        
        animation.setValues_(values)
        animation.setKeyTimes_(times)
        
        view.layer().addAnimation_forKey_(animation, f"keyframe_{property_path}")
        print(f"🎭 关键帧动画: {len(self.keyframes)} keyframes on {property_path}")


class SpringAnimation(Animation):
    """弹性动画"""
    
    def __init__(self, stiffness: float = 100.0, damping: float = 10.0, **kwargs):
        super().__init__(**kwargs)
        self.stiffness = stiffness
        self.damping = damping
    
    def _create_ca_animation(self, property_path: str, from_value: Any, to_value: Any) -> CASpringAnimation:
        """创建弹性动画"""
        animation = CASpringAnimation.animationWithKeyPath_(property_path)
        animation.setDuration_(self.duration)
        animation.setFromValue_(from_value)
        animation.setToValue_(to_value)
        animation.setStiffness_(self.stiffness)
        animation.setDamping_(self.damping)
        
        return animation