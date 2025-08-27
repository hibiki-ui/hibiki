"""macUI v3.0 动画效果

提供常用的预设动画效果，如文字动画、淡入淡出、缩放等。
这些效果封装了复杂的Core Animation逻辑，提供简单易用的接口。
"""

from typing import Union, List, Tuple, Optional
from AppKit import NSView, NSTextField, NSColor, CATextLayer, CAGradientLayer, CAShapeLayer
from AppKit import CABasicAnimation, CAKeyframeAnimation, CAMediaTimingFunction, CAAnimationGroup
from Foundation import NSMakeRect, NSValue, NSMakePoint, NSMakeSize
from Quartz import CATransform3DMakeScale
import math

from .core import Animation, KeyframeAnimation, animate


class ShinyText:
    """闪亮文字效果 - 基于渐变遮罩的光泽动画"""
    
    def __init__(
        self,
        duration: float = 2.0,
        colors: List[str] = None,
        direction: float = 45.0,  # 光泽方向角度
        repeat: bool = True
    ):
        self.duration = duration
        self.colors = colors or ["#ffffff", "#cccccc", "#ffffff"]
        self.direction = direction
        self.repeat = repeat
        self._gradient_layer: Optional[CAGradientLayer] = None
    
    def apply_to(self, text_view: NSTextField) -> Animation:
        """将闪光效果应用到文本视图 - 纯Core Animation实现"""
        print(f"✨ 应用ShinyText效果到: {text_view}")
        
        # 确保视图有layer
        text_view.setWantsLayer_(True)
        layer = text_view.layer()
        
        # 创建闪光效果 - 使用阴影和缩放的组合动画
        # 设置初始阴影状态
        layer.setShadowColor_(NSColor.yellowColor().CGColor())
        layer.setShadowOffset_(NSMakeSize(0, 0))
        layer.setShadowRadius_(3.0)
        layer.setShadowOpacity_(0.0)
        
        # 创建动画组
        group = CAAnimationGroup.animation()
        group.setDuration_(self.duration)
        group.setRemovedOnCompletion_(False)  # 保持最终状态
        group.setFillMode_("forwards")  # 填充模式
        
        # 1. 阴影透明度动画 - 闪光效果
        shadow_animation = CABasicAnimation.animationWithKeyPath_("shadowOpacity")
        shadow_animation.setFromValue_(0.0)
        shadow_animation.setToValue_(0.8)
        shadow_animation.setAutoreverses_(True)
        shadow_animation.setRepeatCount_(2.0)
        
        # 2. 阴影半径动画 - 光晕效果
        radius_animation = CABasicAnimation.animationWithKeyPath_("shadowRadius")
        radius_animation.setFromValue_(1.0)
        radius_animation.setToValue_(8.0)
        radius_animation.setAutoreverses_(True)
        radius_animation.setRepeatCount_(2.0)
        
        # 3. 轻微缩放动画 - 增强视觉效果
        scale_animation = CABasicAnimation.animationWithKeyPath_("transform.scale")
        scale_animation.setFromValue_(1.0)
        scale_animation.setToValue_(1.05)
        scale_animation.setAutoreverses_(True)
        scale_animation.setRepeatCount_(2.0)
        
        # 组合所有动画
        group.setAnimations_([shadow_animation, radius_animation, scale_animation])
        group.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_("easeInEaseOut")
        )
        
        # 动画完成后的回调 - 使用CATransaction
        def completion_block():
            # 重置阴影状态
            layer.setShadowOpacity_(0.0)
            layer.setShadowRadius_(0.0)
        
        # 使用CATransaction设置完成块
        from AppKit import CATransaction
        CATransaction.begin()
        CATransaction.setCompletionBlock_(completion_block)
        layer.addAnimation_forKey_(group, "shinyEffect")
        CATransaction.commit()
        
        print("✨ ShinyText动画已启动 - 纯Core Animation实现")
        return Animation(duration=self.duration)


class TypeWriter:
    """打字机效果 - 逐字显示文本"""
    
    def __init__(
        self,
        text: str,
        duration: float = 2.0,
        char_delay: Optional[float] = None
    ):
        self.text = text
        self.duration = duration
        self.char_delay = char_delay or (duration / len(text) if text else 0.1)
    
    def apply_to(self, text_view: NSTextField) -> Animation:
        """将打字机效果应用到文本视图"""
        print(f"⌨️ 应用TypeWriter效果: '{self.text[:20]}...'")
        
        def animate_char(index: int):
            """递归动画每个字符"""
            if index > len(self.text):
                return
            
            # 设置当前显示的文本
            current_text = self.text[:index]
            text_view.setStringValue_(current_text)
            
            # 调度下一个字符
            if index < len(self.text):
                # 使用NSTimer延迟执行
                import objc
                from Foundation import NSTimer
                NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                    self.char_delay,
                    self,
                    objc.selector(lambda: animate_char(index + 1), signature=b'v@:'),
                    None,
                    False
                )
        
        # 开始动画
        animate_char(0)
        return Animation(duration=self.duration)


class FadeIn:
    """淡入效果"""
    
    def __init__(self, duration: float = 0.5, from_opacity: float = 0.0):
        self.duration = duration
        self.from_opacity = from_opacity
    
    def apply_to(self, view: NSView) -> Animation:
        """应用淡入效果"""
        print(f"🌅 应用FadeIn效果")
        
        # 设置初始透明度
        view.setAlphaValue_(self.from_opacity)
        
        # 创建透明度动画
        animate(view, duration=self.duration, opacity=1.0)
        
        return Animation(duration=self.duration)


class SlideIn:
    """滑入效果"""
    
    def __init__(
        self,
        duration: float = 0.5,
        direction: str = "left",  # left, right, top, bottom
        distance: float = 100.0
    ):
        self.duration = duration
        self.direction = direction
        self.distance = distance
    
    def apply_to(self, view: NSView) -> Animation:
        """应用滑入效果"""
        print(f"➡️ 应用SlideIn效果: {self.direction}")
        
        # 获取当前位置
        current_frame = view.frame()
        target_position = (current_frame.origin.x, current_frame.origin.y)
        
        # 计算起始位置
        if self.direction == "left":
            start_position = (target_position[0] - self.distance, target_position[1])
        elif self.direction == "right":
            start_position = (target_position[0] + self.distance, target_position[1])
        elif self.direction == "top":
            start_position = (target_position[0], target_position[1] + self.distance)
        else:  # bottom
            start_position = (target_position[0], target_position[1] - self.distance)
        
        # 设置初始位置
        view.setFrameOrigin_(NSMakePoint(*start_position))
        
        # 动画到目标位置
        animate(view, duration=self.duration, position=target_position)
        
        return Animation(duration=self.duration)


class Scale:
    """缩放效果"""
    
    def __init__(
        self,
        duration: float = 0.5,
        from_scale: float = 0.0,
        to_scale: float = 1.0,
        timing: str = "easeOut"
    ):
        self.duration = duration
        self.from_scale = from_scale
        self.to_scale = to_scale
        self.timing = timing
    
    def apply_to(self, view: NSView) -> Animation:
        """应用缩放效果"""
        print(f"🔍 应用Scale效果: {self.from_scale} -> {self.to_scale}")
        
        view.setWantsLayer_(True)
        layer = view.layer()
        
        # 设置初始缩放
        transform = CATransform3DMakeScale(self.from_scale, self.from_scale, 1.0)
        layer.setTransform_(transform)
        
        # 创建缩放动画
        final_transform = CATransform3DMakeScale(self.to_scale, self.to_scale, 1.0)
        animation = CABasicAnimation.animationWithKeyPath_("transform")
        animation.setDuration_(self.duration)
        animation.setToValue_(NSValue.valueWithCATransform3D_(final_transform))
        animation.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_("easeOut")
        )
        
        layer.addAnimation_forKey_(animation, "scaleAnimation")
        layer.setTransform_(final_transform)  # 设置最终状态
        
        return Animation(duration=self.duration)


class Shake:
    """抖动效果"""
    
    def __init__(
        self,
        duration: float = 0.5,
        intensity: float = 10.0,
        repeat_count: int = 3
    ):
        self.duration = duration
        self.intensity = intensity
        self.repeat_count = repeat_count
    
    def apply_to(self, view: NSView) -> Animation:
        """应用抖动效果"""
        print(f"🤳 应用Shake效果: intensity={self.intensity}")
        
        view.setWantsLayer_(True)
        layer = view.layer()
        
        # 创建抖动关键帧
        keyframes = []
        frame_count = self.repeat_count * 4  # 每次抖动4个关键帧
        
        for i in range(frame_count + 1):
            progress = i / frame_count
            if i % 4 == 0:
                offset = 0
            elif i % 4 == 1:
                offset = self.intensity
            elif i % 4 == 2:
                offset = -self.intensity
            else:
                offset = self.intensity * 0.5
            
            keyframes.append({
                'time': progress,
                'value': NSValue.valueWithPoint_(NSMakePoint(offset, 0))
            })
        
        # 创建关键帧动画
        animation = CAKeyframeAnimation.animationWithKeyPath_("position")
        animation.setDuration_(self.duration)
        animation.setValues_([kf['value'] for kf in keyframes])
        animation.setKeyTimes_([kf['time'] for kf in keyframes])
        animation.setAdditive_(True)  # 相对于当前位置
        
        layer.addAnimation_forKey_(animation, "shakeAnimation")
        
        return Animation(duration=self.duration)