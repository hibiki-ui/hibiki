"""macUI v3.0 动画时间函数

提供各种动画缓动函数和时间控制。
"""

from typing import Callable
import math


class Easing:
    """缓动函数集合"""
    
    @staticmethod
    def linear(t: float) -> float:
        """线性缓动"""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """二次方程的缓入动画"""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """二次方程的缓出动画"""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """二次方程的缓入缓出动画"""
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """三次方程的缓入动画"""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """三次方程的缓出动画"""
        return 1 - pow(1 - t, 3)
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """三次方程的缓入缓出动画"""
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    
    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """弹跳缓出动画"""
        n1 = 7.5625
        d1 = 2.75
        
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375
    
    @staticmethod
    def ease_out_elastic(t: float) -> float:
        """弹性缓出动画"""
        c4 = (2 * math.pi) / 3
        
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


class TimingFunction:
    """动画时间函数"""
    
    # 标准缓动函数
    LINEAR = "linear"
    EASE = "ease"
    EASE_IN = "easeIn"
    EASE_OUT = "easeOut" 
    EASE_IN_OUT = "easeInOut"
    
    # 自定义缓动函数
    BOUNCE = "bounce"
    ELASTIC = "elastic"
    BACK = "back"
    
    @classmethod
    def cubic_bezier(cls, x1: float, y1: float, x2: float, y2: float) -> str:
        """创建自定义三次贝塞尔缓动函数"""
        return f"cubicBezier({x1}, {y1}, {x2}, {y2})"
    
    @classmethod
    def spring(cls, stiffness: float = 100.0, damping: float = 10.0) -> str:
        """创建弹性缓动函数"""
        return f"spring({stiffness}, {damping})"