#!/usr/bin/env python3
"""Advanced macOS UI Debugging Tools
高级macOS UI调试工具 - 专业级视图层级和点击区域调试
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from AppKit import NSView, NSButton, NSTextField, NSStackView, NSColor
from Foundation import NSMakePoint, NSMakeRect, NSPointInRect
import objc

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("ui_debugging")
except ImportError:
    import logging
    debug_logger = logging.getLogger("ui_debugging")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class ViewHierarchyDebugger:
    """视图层级调试器 - 检测布局问题和点击区域"""
    
    @staticmethod
    def debug_view_hierarchy(root_view, name="Root", max_depth=10):
        """递归调试整个视图层级"""
        debug_logger.info(f"\n🔍 ========== {name} 视图层级分析 ==========")
        ViewHierarchyDebugger._debug_view_recursive(root_view, 0, max_depth)
        debug_logger.info(f"🔍 ========== {name} 分析完毕 ==========\n")
    
    @staticmethod 
    def _debug_view_recursive(view, depth, max_depth):
        """递归调试视图"""
        if depth > max_depth:
            return
            
        indent = "  " * depth
        view_class = view.__class__.__name__
        
        # 获取基本信息
        frame = view.frame()
        bounds = view.bounds()
        
        debug_logger.info(f"{indent}📦 {view_class}")
        debug_logger.info(f"{indent}   Frame: ({frame.origin.x:.1f}, {frame.origin.y:.1f}, {frame.size.width:.1f}, {frame.size.height:.1f})")
        debug_logger.info(f"{indent}   Bounds: ({bounds.origin.x:.1f}, {bounds.origin.y:.1f}, {bounds.size.width:.1f}, {bounds.size.height:.1f})")
        
        # 检查特殊属性
        if hasattr(view, 'isHidden') and view.isHidden():
            debug_logger.info(f"{indent}   ⚠️ 视图隐藏")
        
        if hasattr(view, 'alphaValue') and view.alphaValue() < 1.0:
            debug_logger.info(f"{indent}   ⚠️ 透明度: {view.alphaValue():.2f}")
            
        # 检查是否在父视图bounds内
        if hasattr(view, 'superview') and view.superview():
            parent_bounds = view.superview().bounds()
            if not ViewHierarchyDebugger._is_frame_within_bounds(frame, parent_bounds):
                debug_logger.info(f"{indent}   🚨 超出父视图bounds!")
        
        # 特殊处理NSButton
        if isinstance(view, NSButton):
            ViewHierarchyDebugger._debug_button_special(view, indent)
        
        # 特殊处理NSTextField
        elif isinstance(view, NSTextField):
            ViewHierarchyDebugger._debug_textfield_special(view, indent)
        
        # 特殊处理NSStackView
        elif isinstance(view, NSStackView):
            ViewHierarchyDebugger._debug_stackview_special(view, indent)
        
        # 递归调试子视图
        if hasattr(view, 'subviews'):
            subviews = view.subviews()
            if subviews:
                debug_logger.info(f"{indent}   📋 子视图数量: {len(subviews)}")
                for i, subview in enumerate(subviews):
                    ViewHierarchyDebugger._debug_view_recursive(subview, depth + 1, max_depth)
    
    @staticmethod
    def _is_frame_within_bounds(frame, bounds):
        """检查frame是否在bounds内"""
        return (frame.origin.x >= bounds.origin.x and
                frame.origin.y >= bounds.origin.y and
                frame.origin.x + frame.size.width <= bounds.origin.x + bounds.size.width and
                frame.origin.y + frame.size.height <= bounds.origin.y + bounds.size.height)
    
    @staticmethod
    def _debug_button_special(button, indent):
        """调试NSButton特殊信息"""
        debug_logger.info(f"{indent}   🎯 按钮标题: '{button.title()}'")
        debug_logger.info(f"{indent}   🎯 启用状态: {button.isEnabled()}")
        
        # 检查target和action
        target = button.target()
        action = button.action()
        debug_logger.info(f"{indent}   🎯 Target: {target.__class__.__name__ if target else 'None'}")
        debug_logger.info(f"{indent}   🎯 Action: {action}")
        
        # 检查按钮类型
        try:
            button_type = button.buttonType()
            debug_logger.info(f"{indent}   🎯 按钮类型: {button_type}")
        except AttributeError:
            # PyObjC可能没有暴露buttonType方法
            debug_logger.info(f"{indent}   🎯 按钮类型: 无法获取")
    
    @staticmethod
    def _debug_textfield_special(textfield, indent):
        """调试NSTextField特殊信息"""
        text = textfield.stringValue()
        if len(text) > 50:
            text = text[:47] + "..."
        debug_logger.info(f"{indent}   📝 文本: '{text}'")
        debug_logger.info(f"{indent}   📝 可编辑: {textfield.isEditable()}")
        debug_logger.info(f"{indent}   📝 可选择: {textfield.isSelectable()}")
        
        # 检查文本是否可能导致layout问题
        preferred_width = None
        if hasattr(textfield, 'preferredMaxLayoutWidth'):
            try:
                preferred_width = textfield.preferredMaxLayoutWidth()
                debug_logger.info(f"{indent}   📝 最大布局宽度: {preferred_width}")
            except:
                pass
    
    @staticmethod
    def _debug_stackview_special(stackview, indent):
        """调试NSStackView特殊信息"""
        try:
            orientation = stackview.orientation()
            alignment = stackview.alignment()
            distribution = stackview.distribution()
            spacing = stackview.spacing()
            
            orientation_name = "Vertical" if orientation == 1 else "Horizontal"
            debug_logger.info(f"{indent}   📐 方向: {orientation_name} ({orientation})")
            debug_logger.info(f"{indent}   📐 对齐: {alignment}")
            debug_logger.info(f"{indent}   📐 分布: {distribution}")
            debug_logger.info(f"{indent}   📐 间距: {spacing}")
            
            # 检查arranged subviews
            arranged_subviews = stackview.arrangedSubviews()
            debug_logger.info(f"{indent}   📐 排列的子视图数: {len(arranged_subviews)}")
        except Exception as e:
            debug_logger.info(f"{indent}   ⚠️ StackView调试失败: {e}")


class HitTestDebugger:
    """点击测试调试器 - 检测为什么按钮不能点击"""
    
    @staticmethod
    def test_button_clickability(button, button_name="Button"):
        """测试按钮的可点击性"""
        debug_logger.info(f"\n🎯 ========== {button_name} 点击测试 ==========")
        
        frame = button.frame()
        center_point = NSMakePoint(
            frame.origin.x + frame.size.width / 2,
            frame.origin.y + frame.size.height / 2
        )
        
        debug_logger.info(f"🎯 按钮中心点: ({center_point.x:.1f}, {center_point.y:.1f})")
        
        # 测试hitTest
        current_view = button
        level = 0
        
        while current_view and level < 10:
            # 转换坐标到当前视图
            if hasattr(current_view, 'superview') and current_view.superview():
                try:
                    # 将point转换到当前视图坐标系
                    converted_point = current_view.superview().convertPoint_toView_(center_point, current_view)
                    debug_logger.info(f"🎯 层级{level} {current_view.__class__.__name__}: 转换后点({converted_point.x:.1f}, {converted_point.y:.1f})")
                    
                    # 检查点是否在bounds内
                    bounds = current_view.bounds()
                    point_in_bounds = NSPointInRect(converted_point, bounds)
                    debug_logger.info(f"🎯 层级{level} 点在bounds内: {point_in_bounds}")
                    
                    if not point_in_bounds:
                        debug_logger.info(f"🚨 层级{level} 点击失败！点不在{current_view.__class__.__name__}的bounds内")
                        break
                        
                    # 执行hitTest
                    if hasattr(current_view, 'hitTest_'):
                        hit_view = current_view.hitTest_(converted_point)
                        hit_view_name = hit_view.__class__.__name__ if hit_view else "None"
                        debug_logger.info(f"🎯 层级{level} hitTest结果: {hit_view_name}")
                        
                        if hit_view != button and level == 0:
                            debug_logger.info(f"🚨 hitTest没有返回目标按钮！返回了: {hit_view_name}")
                
                except Exception as e:
                    debug_logger.info(f"⚠️ 层级{level} 坐标转换失败: {e}")
            
            # 移动到父视图
            if hasattr(current_view, 'superview'):
                current_view = current_view.superview()
            else:
                break
            level += 1
        
        debug_logger.info(f"🎯 ========== {button_name} 测试完毕 ==========\n")
    
    @staticmethod
    def find_overlapping_views(target_view, root_view):
        """查找与目标视图重叠的其他视图"""
        debug_logger.info(f"\n🔍 ========== 重叠检测 ==========")
        
        target_frame = target_view.frame()
        overlapping_views = []
        
        # 将目标frame转换到root坐标系
        if hasattr(target_view, 'superview') and target_view.superview():
            try:
                # 这里需要更复杂的坐标转换逻辑
                HitTestDebugger._find_overlapping_recursive(target_view, target_frame, root_view, overlapping_views)
            except Exception as e:
                debug_logger.info(f"⚠️ 重叠检测失败: {e}")
        
        if overlapping_views:
            debug_logger.info(f"🚨 发现 {len(overlapping_views)} 个重叠视图:")
            for view in overlapping_views:
                debug_logger.info(f"   - {view.__class__.__name__}")
        else:
            debug_logger.info("✅ 没有发现重叠视图")
        
        debug_logger.info(f"🔍 ========== 重叠检测完毕 ==========\n")
        return overlapping_views
    
    @staticmethod
    def _find_overlapping_recursive(target_view, target_frame, current_view, results):
        """递归查找重叠视图"""
        # 简化的重叠检测 - 实际实现需要更复杂的坐标转换
        if current_view != target_view and hasattr(current_view, 'frame'):
            current_frame = current_view.frame()
            # 简单的重叠检测
            if (current_frame.origin.x < target_frame.origin.x + target_frame.size.width and
                current_frame.origin.x + current_frame.size.width > target_frame.origin.x and
                current_frame.origin.y < target_frame.origin.y + target_frame.size.height and
                current_frame.origin.y + current_frame.size.height > target_frame.origin.y):
                results.append(current_view)
        
        # 递归检查子视图
        if hasattr(current_view, 'subviews'):
            for subview in current_view.subviews():
                HitTestDebugger._find_overlapping_recursive(target_view, target_frame, subview, results)


class TextOverlapDetector:
    """文本重叠检测器 - 专门检测NSTextField重叠问题"""
    
    @staticmethod
    def detect_text_overlaps(root_view):
        """检测文本重叠"""
        debug_logger.info(f"\n📝 ========== 文本重叠检测 ==========")
        
        text_fields = []
        TextOverlapDetector._collect_textfields_recursive(root_view, text_fields)
        
        debug_logger.info(f"📝 找到 {len(text_fields)} 个文本字段")
        
        overlaps = []
        for i, field1 in enumerate(text_fields):
            for j, field2 in enumerate(text_fields[i+1:], i+1):
                if TextOverlapDetector._check_textfield_overlap(field1, field2):
                    overlaps.append((field1, field2))
                    text1 = field1.stringValue()[:20] + "..." if len(field1.stringValue()) > 20 else field1.stringValue()
                    text2 = field2.stringValue()[:20] + "..." if len(field2.stringValue()) > 20 else field2.stringValue()
                    debug_logger.info(f"🚨 文本重叠: '{text1}' 和 '{text2}'")
        
        if not overlaps:
            debug_logger.info("✅ 没有发现文本重叠")
        
        debug_logger.info(f"📝 ========== 文本重叠检测完毕 ==========\n")
        return overlaps
    
    @staticmethod
    def _collect_textfields_recursive(view, text_fields):
        """递归收集所有NSTextField"""
        if isinstance(view, NSTextField):
            text_fields.append(view)
        
        if hasattr(view, 'subviews'):
            for subview in view.subviews():
                TextOverlapDetector._collect_textfields_recursive(subview, text_fields)
    
    @staticmethod
    def _check_textfield_overlap(field1, field2):
        """检查两个文本字段是否重叠"""
        try:
            # 需要将两个字段转换到同一坐标系
            # 这里简化处理，假设在同一父视图中
            frame1 = field1.frame()
            frame2 = field2.frame()
            
            # 检查矩形重叠
            return not (frame1.origin.x + frame1.size.width <= frame2.origin.x or
                       frame2.origin.x + frame2.size.width <= frame1.origin.x or
                       frame1.origin.y + frame1.size.height <= frame2.origin.y or
                       frame2.origin.y + frame2.size.height <= frame1.origin.y)
        except:
            return False


def debug_ui_comprehensive(root_view, button_list=None):
    """综合UI调试"""
    debug_logger.info("🚀 开始综合UI调试分析")
    debug_logger.info("=" * 60)
    
    # 1. 视图层级调试
    ViewHierarchyDebugger.debug_view_hierarchy(root_view, "主窗口")
    
    # 2. 文本重叠检测
    TextOverlapDetector.detect_text_overlaps(root_view)
    
    # 3. 按钮点击测试
    if button_list:
        for button, name in button_list:
            HitTestDebugger.test_button_clickability(button, name)
            HitTestDebugger.find_overlapping_views(button, root_view)
    
    debug_logger.info("✅ 综合UI调试分析完成")
    debug_logger.info("=" * 60)


if __name__ == "__main__":
    print("Advanced UI Debugging Tools for macUI")
    print("This module provides comprehensive debugging utilities for macOS UI issues.")