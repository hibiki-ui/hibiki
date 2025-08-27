"""macUI v3.0 动画系统

提供简洁、高效、声明式的动画API，基于Core Animation构建，
与macUI的Signal响应式系统完美集成。

核心特性:
- 声明式动画语法
- Signal驱动的响应式动画
- 丰富的预设动画效果
- 高性能Core Animation后端
- 链式动画组合
"""

from .core import Animation, AnimationGroup, animate, animate_to
from .effects import ShinyText, TypeWriter, FadeIn, SlideIn, Scale, Shake
from .transitions import Transition, TransitionType
from .timing import Easing, TimingFunction

__all__ = [
    # Core Animation
    "Animation",
    "AnimationGroup", 
    "animate",
    "animate_to",
    
    # Animation Effects
    "ShinyText",
    "TypeWriter",
    "FadeIn",
    "SlideIn", 
    "Scale",
    "Shake",
    
    # Transitions
    "Transition",
    "TransitionType",
    
    # Timing
    "Easing", 
    "TimingFunction"
]