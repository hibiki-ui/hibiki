"""macUI v3.0 动画系统

提供简洁、高效、声明式的动画API，基于Core Animation构建，
与macUI的Signal响应式系统完美集成。

## 核心设计原则

### 🎯 Pure Core Animation
所有动画必须使用Core Animation API实现，绝不使用：
- threading.Thread 或自定义线程
- time.sleep 或阻塞等待
- 手动定时器或轮询

### ⚡ GPU优先策略  
优先使用GPU加速的CALayer属性：
- shadowOpacity, shadowRadius (阴影动画)
- transform.scale, transform.rotation (变换动画) 
- position, bounds (位置动画)
- opacity (透明度动画)

### 🏗️ 架构模式
```python
# 标准实现模式
group = CAAnimationGroup.animation()
animation = CABasicAnimation.animationWithKeyPath_("property")
CATransaction.setCompletionBlock_(callback)
layer.addAnimation_forKey_(group, "animationKey")
```

## API特性
- **声明式语法**: 隐藏Core Animation复杂性
- **Signal集成**: 响应式动画绑定
- **预设效果库**: ShinyText, FadeIn, SlideIn等
- **硬件加速**: 充分利用GPU性能
- **链式组合**: 支持复杂动画序列

## 技术依赖
- AppKit: CATransaction, CABasicAnimation, CAAnimationGroup
- Quartz: CATransform3DMakeScale, Core Animation函数
- Foundation: NSValue, NSMakePoint, NSMakeSize

## 使用示例
```python
from macui.animation import animate, ShinyText, FadeIn, animate_to

# 1. 简单声明式动画
animate(view, duration=0.5, opacity=0.8, scale=1.2)

# 2. 预设动画效果
ShinyText(duration=2.0).apply_to(text_label)
FadeIn(duration=1.0, from_opacity=0.0).apply_to(panel)

# 3. Signal响应式动画
animate_to(view, position_signal, 
          position=lambda pos: pos,
          opacity=lambda pos: 0.8 if pos[0] > 100 else 0.5)

# 4. 复杂组合动画
scale = Scale(duration=1.0, from_scale=0.5, to_scale=1.2)  
fade = FadeIn(duration=1.0)
# 同时应用多个效果
```

## 性能最佳实践
1. 优先使用CAAnimationGroup组合多个动画
2. 使用CATransaction.setCompletionBlock_处理完成回调
3. 避免在动画过程中频繁访问Python对象
4. 选择GPU友好的动画属性(避免frame/bounds频繁变化)
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