"""macUI v3.0 动画系统

提供简洁、高效、声明式的动画API，基于Core Animation构建，
与macUI的Signal响应式系统完美集成。

核心特性:
- 声明式动画语法
- Signal驱动的响应式动画  
- 丰富的预设动画效果
- 高性能Core Animation后端
- 链式动画组合

依赖项:
- AppKit (macOS原生框架)
- Quartz (Core Animation支持)
- Foundation (基础数据类型)

快速开始:
```python
from macui.animation import animate, ShinyText, FadeIn

# 简单动画
animate(my_view, duration=0.5, opacity=0.8, position=(100, 100))

# 预设效果
shiny = ShinyText(duration=2.0)
shiny.apply_to(text_view)

fade = FadeIn(duration=1.0)  
fade.apply_to(my_view)
```
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