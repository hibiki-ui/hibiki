#!/usr/bin/env python3
"""NSStackView HStack 精确修复补丁
修复按钮超出父视图边界的根本问题
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from AppKit import (
    NSStackView, NSLayoutAttributeLeading, NSLayoutAttributeTrailing,
    NSLayoutAttributeCenterX, NSLayoutAttributeTop, NSLayoutAttributeBottom, 
    NSLayoutAttributeCenterY, NSStackViewDistributionGravityAreas,
    NSUserInterfaceLayoutOrientationHorizontal, NSUserInterfaceLayoutOrientationVertical
)
from Foundation import NSMakeRect, NSEdgeInsets

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("hstack_fix")
except ImportError:
    import logging
    debug_logger = logging.getLogger("hstack_fix")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


def create_fixed_hstack(spacing=0, padding=0, alignment="center", children=None, frame=None):
    """修复版的HStack创建函数"""
    if not children:
        children = []
    
    debug_logger.info("🔧 创建修复版HStack")
    
    # 创建NSStackView
    stack = NSStackView.alloc().init()
    
    # 🎯 关键修复1：更保守的初始frame设置
    if frame:
        stack.setFrame_(NSMakeRect(*frame))
        debug_logger.info(f"🔧 设置显式frame: {frame}")
    else:
        # 设置一个合理的默认大小，确保有足够空间容纳按钮
        stack.setFrame_(NSMakeRect(0, 0, 400, 100))
        debug_logger.info(f"🔧 设置默认frame: (0, 0, 400, 100)")
    
    # 🎯 关键修复2：明确设置为水平方向，并进行多重验证
    stack.setOrientation_(NSUserInterfaceLayoutOrientationHorizontal)
    
    # 立即验证
    current_orientation = stack.orientation()
    if current_orientation != NSUserInterfaceLayoutOrientationHorizontal:
        debug_logger.error(f"❌ orientation设置失败! 期望:{NSUserInterfaceLayoutOrientationHorizontal}, 实际:{current_orientation}")
        # 尝试使用整数值
        stack.setOrientation_(0)  # 0 = Horizontal
        current_orientation = stack.orientation()
        debug_logger.info(f"🔧 使用整数值重新设置orientation: {current_orientation}")
    
    # 🎯 关键修复3：减小默认spacing，避免计算溢出
    safe_spacing = max(0, min(spacing, 50))  # 限制spacing在0-50之间
    stack.setSpacing_(safe_spacing)
    debug_logger.info(f"🔧 设置安全spacing: {spacing} → {safe_spacing}")
    
    # 🎯 关键修复4：使用最安全的alignment设置
    # 对于HStack，最安全的是centerY对齐
    stack.setAlignment_(NSLayoutAttributeCenterY)
    debug_logger.info(f"🔧 使用最安全的alignment: centerY")
    
    # 🎯 关键修复5：使用最简单的distribution
    stack.setDistribution_(NSStackViewDistributionGravityAreas)
    debug_logger.info(f"🔧 使用安全的distribution: GravityAreas")
    
    # 🎯 关键修复6：保守的padding设置
    if isinstance(padding, (int, float)):
        safe_padding = max(0, min(padding, 20))  # 限制padding在0-20之间
        insets = NSEdgeInsets(safe_padding, safe_padding, safe_padding, safe_padding)
    else:
        insets = NSEdgeInsets(10, 10, 10, 10)  # 使用安全的默认值
    
    stack.setEdgeInsets_(insets)
    debug_logger.info(f"🔧 设置安全的insets: {insets}")
    
    # 添加子视图
    debug_logger.info(f"🚀 开始添加 {len(children)} 个子视图")
    
    for i, child in enumerate(children):
        debug_logger.info(f"🔍 处理子视图 {i+1}...")
        
        # 获取子视图
        if hasattr(child, 'get_view'):
            child_view = child.get_view()
        elif hasattr(child, '__call__'):  # Component类型
            try:
                child_view = child()
            except:
                child_view = child
        else:
            child_view = child
        
        if child_view:
            # 🎯 关键修复7：确保子视图有合理的尺寸
            if hasattr(child_view, 'sizeToFit'):
                child_view.sizeToFit()
                frame_after_fit = child_view.frame()
                debug_logger.info(f"   📏 子视图sizeToFit后: {frame_after_fit.size.width:.1f} x {frame_after_fit.size.height:.1f}")
            
            # 🎯 关键修复8：验证子视图frame的合理性
            child_frame = child_view.frame()
            if (child_frame.size.width <= 0 or child_frame.size.height <= 0):
                debug_logger.warning(f"   ⚠️ 子视图尺寸异常，强制设置最小尺寸")
                child_view.setFrame_(NSMakeRect(0, 0, 80, 32))  # 最小合理尺寸
            
            # 添加到StackView
            stack.addArrangedSubview_(child_view)
            
            title = getattr(child_view, 'title', lambda: 'Unknown')()
            debug_logger.info(f"✅ 子视图 {i+1} 已添加: {child_view.__class__.__name__} '{title}'")
    
    # 🎯 关键修复9：强制更新布局并验证结果
    stack.layoutSubtreeIfNeeded()
    debug_logger.info(f"🔄 强制布局更新完成")
    
    # 验证最终结果
    final_frame = stack.frame()
    debug_logger.info(f"📦 最终stack frame: ({final_frame.origin.x:.1f}, {final_frame.origin.y:.1f}, {final_frame.size.width:.1f}, {final_frame.size.height:.1f})")
    
    if hasattr(stack, 'arrangedSubviews'):
        arranged_views = stack.arrangedSubviews()
        debug_logger.info(f"🔍 最终子视图位置验证:")
        
        all_positive = True
        for i, subview in enumerate(arranged_views):
            subview_frame = subview.frame()
            title = getattr(subview, 'title', lambda: 'Unknown')()
            debug_logger.info(f"   子视图 {i+1} '{title}': ({subview_frame.origin.x:.1f}, {subview_frame.origin.y:.1f}, {subview_frame.size.width:.1f}, {subview_frame.size.height:.1f})")
            
            if subview_frame.origin.x < 0:
                debug_logger.error(f"   🚨 子视图 {i+1} 仍然超出边界! X={subview_frame.origin.x:.1f}")
                all_positive = False
        
        if all_positive:
            debug_logger.info(f"✅ 所有子视图位置正常!")
        else:
            debug_logger.error(f"❌ 仍有子视图超出边界!")
    
    return stack


def test_fixed_hstack():
    """测试修复版HStack"""
    debug_logger.info("🧪 开始测试修复版HStack")
    
    from macui.components import Button
    
    # 创建测试按钮
    buttons = [
        Button("按钮1", frame=(0, 0, 80, 32)),
        Button("按钮2", frame=(0, 0, 80, 32)),  
        Button("按钮3", frame=(0, 0, 80, 32))
    ]
    
    # 使用修复版HStack
    fixed_stack = create_fixed_hstack(
        spacing=10,
        padding=10,
        alignment="center",
        children=buttons,
        frame=(50, 50, 350, 80)
    )
    
    debug_logger.info("🧪 修复版HStack测试完成")
    return fixed_stack


if __name__ == "__main__":
    # 运行测试
    test_fixed_hstack()