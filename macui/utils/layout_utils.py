#!/usr/bin/env python3
"""
布局工具函数 - 提供安全的布局管理
"""

from Foundation import NSMakeRect
from AppKit import NSView

# 最大允许的约束值
MAX_CONSTRAINT_VALUE = 1e6

def safe_frame(x=0, y=0, width=100, height=100):
    """创建安全的 NSRect，避免超出约束限制
    
    Args:
        x, y: 位置坐标
        width, height: 尺寸
        
    Returns:
        NSRect 实例
    """
    # 限制坐标和尺寸在合理范围内
    x = max(-MAX_CONSTRAINT_VALUE, min(MAX_CONSTRAINT_VALUE, x))
    y = max(-MAX_CONSTRAINT_VALUE, min(MAX_CONSTRAINT_VALUE, y))
    width = max(1, min(MAX_CONSTRAINT_VALUE, width))
    height = max(1, min(MAX_CONSTRAINT_VALUE, height))
    
    return NSMakeRect(x, y, width, height)

def safe_set_frame(view: NSView, frame: tuple):
    """安全地设置视图 frame
    
    Args:
        view: 目标视图
        frame: (x, y, width, height) 元组
    """
    if not isinstance(frame, (tuple, list)) or len(frame) != 4:
        print(f"⚠️  警告: frame 格式错误: {frame}")
        return
    
    try:
        safe_rect = safe_frame(*frame)
        view.setFrame_(safe_rect)
    except Exception as e:
        print(f"❌ 设置 frame 失败: {e}")
        # 使用默认 frame 作为备用
        default_rect = safe_frame(0, 0, 100, 100)
        view.setFrame_(default_rect)

def disable_autolayout(view: NSView):
    """禁用视图的自动布局
    
    Args:
        view: 目标视图
    """
    try:
        view.setTranslatesAutoresizingMaskIntoConstraints_(False)
    except Exception as e:
        print(f"❌ 禁用自动布局失败: {e}")

def setup_manual_layout(view: NSView, frame: tuple = None):
    """设置手动布局模式
    
    Args:
        view: 目标视图
        frame: 可选的初始 frame
    """
    # 禁用自动布局约束
    disable_autolayout(view)
    
    # 设置 frame
    if frame:
        safe_set_frame(view, frame)