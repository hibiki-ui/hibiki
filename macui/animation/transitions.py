"""macUI v3.0 过渡动画

提供页面和视图间的过渡效果。
"""

from typing import Optional
from AppKit import NSView, CATransition, CAMediaTimingFunction


class TransitionType:
    """过渡动画类型"""
    FADE = "fade"
    PUSH = "push" 
    REVEAL = "reveal"
    MOVE_IN = "moveIn"
    CUBE = "cube"
    RIPPLE_EFFECT = "rippleEffect"
    SUCK_EFFECT = "suckEffect"
    PAGE_CURL = "pageCurl"


class Transition:
    """视图过渡动画"""
    
    def __init__(
        self,
        transition_type: str = TransitionType.FADE,
        duration: float = 0.5,
        direction: Optional[str] = None  # "fromLeft", "fromRight", "fromTop", "fromBottom"
    ):
        self.transition_type = transition_type
        self.duration = duration
        self.direction = direction
    
    def animate_between(self, from_view: NSView, to_view: NSView):
        """在两个视图间执行过渡动画"""
        print(f"🔄 执行过渡动画: {self.transition_type}")
        
        # 确保视图有layer
        from_view.setWantsLayer_(True)
        to_view.setWantsLayer_(True)
        
        # 创建过渡动画
        transition = CATransition.animation()
        transition.setDuration_(self.duration)
        transition.setType_(self._get_ca_transition_type())
        
        if self.direction:
            transition.setSubtype_(self._get_ca_direction())
        
        transition.setTimingFunction_(
            CAMediaTimingFunction.functionWithName_("easeInEaseOut")
        )
        
        # 应用到父容器
        container = from_view.superview()
        if container:
            container.setWantsLayer_(True)
            container.layer().addAnimation_forKey_(transition, "transition")
            
            # 执行视图切换
            from_view.setHidden_(True)
            to_view.setHidden_(False)
    
    def _get_ca_transition_type(self) -> str:
        """获取Core Animation过渡类型"""
        type_map = {
            TransitionType.FADE: "fade",
            TransitionType.PUSH: "push",
            TransitionType.REVEAL: "reveal",
            TransitionType.MOVE_IN: "moveIn",
            TransitionType.CUBE: "cube",
            TransitionType.RIPPLE_EFFECT: "rippleEffect", 
            TransitionType.SUCK_EFFECT: "suckEffect",
            TransitionType.PAGE_CURL: "pageCurl"
        }
        return type_map.get(self.transition_type, "fade")
    
    def _get_ca_direction(self) -> str:
        """获取Core Animation方向"""
        direction_map = {
            "fromLeft": "fromLeft",
            "fromRight": "fromRight", 
            "fromTop": "fromTop",
            "fromBottom": "fromBottom"
        }
        return direction_map.get(self.direction, "fromRight")