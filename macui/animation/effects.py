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
    """闪亮文字效果 - 完全模拟CSS background-clip: text 的Core Animation实现"""
    
    def __init__(
        self,
        speed: float = 5.0,  # 动画速度(秒)，匹配CSS版本默认参数
        disabled: bool = False,  # 是否禁用动画
        intensity: float = 0.8  # 光泽强度 (保留用于调节)
    ):
        self.duration = speed  # 直接使用speed作为duration
        self.disabled = disabled
        self.intensity = intensity
        self._gradient_layer: Optional[CAGradientLayer] = None
        self._original_color = None
        self._animation_key = "shinyTextAnimation"
    
    def apply_to(self, text_view: NSTextField) -> Animation:
        """将闪光效果应用到文本视图 - 完全模拟CSS background-clip: text实现"""
        print(f"✨ 应用ShinyText CSS风格效果到: {text_view}")
        
        # 如果禁用，直接返回
        if self.disabled:
            print("⏸️ ShinyText动画已禁用")
            return Animation(duration=0)
        
        # 确保视图有layer
        text_view.setWantsLayer_(True)
        layer = text_view.layer()
        bounds = layer.bounds()
        
        # 保存原始文字颜色
        self._original_color = text_view.textColor()
        
        # 设置基础文字颜色 - 对应CSS的 color: #b5b5b5a4
        base_gray = NSColor.colorWithRed_green_blue_alpha_(0.71, 0.71, 0.71, 0.64)  # #b5b5b5a4
        text_view.setTextColor_(base_gray)
        
        # 创建背景渐变层 - 模拟CSS的linear-gradient
        gradient_layer = CAGradientLayer.layer()
        
        # 设置渐变层尺寸 - 对应CSS的 background-size: 200% 100%
        gradient_width = bounds.size.width * 2.0  # 200%宽度
        gradient_layer.setFrame_(NSMakeRect(0, 0, gradient_width, bounds.size.height))
        
        # 创建渐变颜色 - 完全对应CSS渐变
        # linear-gradient(120deg, rgba(255,255,255,0) 40%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 60%)
        transparent = NSColor.colorWithRed_green_blue_alpha_(1.0, 1.0, 1.0, 0.0).CGColor()
        bright_white = NSColor.colorWithRed_green_blue_alpha_(1.0, 1.0, 1.0, self.intensity).CGColor()
        
        gradient_layer.setColors_([transparent, transparent, bright_white, transparent, transparent])
        gradient_layer.setLocations_([0.0, 0.4, 0.5, 0.6, 1.0])  # 对应40%, 50%, 60%
        
        # 设置渐变角度 - 对应CSS的120deg
        angle_rad = math.radians(120.0)
        start_point = (0.5 - 0.5 * math.cos(angle_rad), 0.5 - 0.5 * math.sin(angle_rad))
        end_point = (0.5 + 0.5 * math.cos(angle_rad), 0.5 + 0.5 * math.sin(angle_rad))
        gradient_layer.setStartPoint_(start_point)
        gradient_layer.setEndPoint_(end_point)
        
        # 关键：使用渐变层作为文字的遮罩 - 模拟background-clip: text
        layer.setMask_(gradient_layer)
        self._gradient_layer = gradient_layer
        
        # 创建背景位置动画 - 对应CSS animation: background-position 100% → -100%
        position_animation = CABasicAnimation.animationWithKeyPath_("position.x")
        
        # 计算动画轨迹 - 模拟background-position从100%到-100%
        start_x = bounds.size.width  # 100% (右边)
        end_x = -bounds.size.width   # -100% (左边)
        
        position_animation.setFromValue_(start_x)
        position_animation.setToValue_(end_x)
        position_animation.setDuration_(self.duration)
        position_animation.setRepeatCount_(float('inf'))
        position_animation.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_("linear")  # 对应CSS的linear
        )
        
        # 应用动画
        gradient_layer.addAnimation_forKey_(position_animation, self._animation_key)
        
        print(f"✨ ShinyText CSS风格动画已启动 - 速度: {self.duration}s")
        print(f"   📋 模拟CSS: background-clip: text + background-position动画")
        return Animation(duration=self.duration)
    
    def stop_animation(self):
        """停止动画并恢复原始状态"""
        if self._gradient_layer:
            # 停止动画
            self._gradient_layer.removeAnimationForKey_(self._animation_key)
            # 移除遮罩
            if hasattr(self._gradient_layer, 'superlayer') and self._gradient_layer.superlayer():
                self._gradient_layer.superlayer().setMask_(None)
            self._gradient_layer = None
            print("⏹️ ShinyText动画已停止，遮罩已移除")


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