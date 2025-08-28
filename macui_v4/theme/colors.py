"""macUI v4 颜色系统

提供系统级颜色管理和主题颜色支持
"""

from typing import Optional, Dict, Any
from enum import Enum
from AppKit import NSColor
from Foundation import NSObject


class ColorRole(Enum):
    """颜色角色定义"""
    # 基础颜色
    PRIMARY_TEXT = "primary_text"
    SECONDARY_TEXT = "secondary_text"
    TERTIARY_TEXT = "tertiary_text"
    
    # 交互颜色
    ACCENT_COLOR = "accent_color"
    CONTROL_COLOR = "control_color"
    
    # 状态颜色
    SUCCESS_COLOR = "success_color"
    WARNING_COLOR = "warning_color"
    ERROR_COLOR = "error_color"
    
    # 背景颜色
    PRIMARY_BACKGROUND = "primary_background"
    SECONDARY_BACKGROUND = "secondary_background"
    SURFACE_BACKGROUND = "surface_background"
    
    # 边框颜色
    BORDER_COLOR = "border_color"
    SEPARATOR_COLOR = "separator_color"


class SystemColors:
    """系统颜色获取器"""
    
    @classmethod
    def primary_text(cls) -> NSColor:
        """主要文本颜色"""
        return NSColor.labelColor()
    
    @classmethod
    def secondary_text(cls) -> NSColor:
        """次要文本颜色"""
        return NSColor.secondaryLabelColor()
    
    @classmethod
    def tertiary_text(cls) -> NSColor:
        """第三级文本颜色"""
        return NSColor.tertiaryLabelColor()
    
    @classmethod
    def accent_color(cls) -> NSColor:
        """强调色"""
        return NSColor.controlAccentColor()
    
    @classmethod
    def control_color(cls) -> NSColor:
        """控件颜色"""
        return NSColor.controlColor()
    
    @classmethod
    def success_color(cls) -> NSColor:
        """成功色 - 绿色"""
        return NSColor.systemGreenColor()
    
    @classmethod
    def warning_color(cls) -> NSColor:
        """警告色 - 橙色"""
        return NSColor.systemOrangeColor()
    
    @classmethod
    def error_color(cls) -> NSColor:
        """错误色 - 红色"""
        return NSColor.systemRedColor()
    
    @classmethod
    def primary_background(cls) -> NSColor:
        """主要背景色"""
        return NSColor.windowBackgroundColor()
    
    @classmethod
    def secondary_background(cls) -> NSColor:
        """次要背景色"""
        return NSColor.controlBackgroundColor()
    
    @classmethod
    def surface_background(cls) -> NSColor:
        """表面背景色"""
        return NSColor.textBackgroundColor()
    
    @classmethod
    def border_color(cls) -> NSColor:
        """边框颜色"""
        return NSColor.separatorColor()
    
    @classmethod
    def separator_color(cls) -> NSColor:
        """分隔线颜色"""
        return NSColor.separatorColor()


class ColorScheme:
    """颜色方案"""
    
    def __init__(self, name: str, colors: Optional[Dict[ColorRole, NSColor]] = None):
        self.name = name
        self._colors = colors or {}
    
    def get_color(self, role: ColorRole) -> NSColor:
        """获取指定角色的颜色"""
        if role in self._colors:
            return self._colors[role]
        
        # 回退到系统颜色
        return self._get_system_color(role)
    
    def set_color(self, role: ColorRole, color: NSColor):
        """设置颜色"""
        self._colors[role] = color
    
    def _get_system_color(self, role: ColorRole) -> NSColor:
        """获取系统默认颜色"""
        system_color_map = {
            ColorRole.PRIMARY_TEXT: SystemColors.primary_text,
            ColorRole.SECONDARY_TEXT: SystemColors.secondary_text,
            ColorRole.TERTIARY_TEXT: SystemColors.tertiary_text,
            ColorRole.ACCENT_COLOR: SystemColors.accent_color,
            ColorRole.CONTROL_COLOR: SystemColors.control_color,
            ColorRole.SUCCESS_COLOR: SystemColors.success_color,
            ColorRole.WARNING_COLOR: SystemColors.warning_color,
            ColorRole.ERROR_COLOR: SystemColors.error_color,
            ColorRole.PRIMARY_BACKGROUND: SystemColors.primary_background,
            ColorRole.SECONDARY_BACKGROUND: SystemColors.secondary_background,
            ColorRole.SURFACE_BACKGROUND: SystemColors.surface_background,
            ColorRole.BORDER_COLOR: SystemColors.border_color,
            ColorRole.SEPARATOR_COLOR: SystemColors.separator_color,
        }
        
        color_func = system_color_map.get(role)
        return color_func() if color_func else NSColor.labelColor()


class PresetColorSchemes:
    """预设颜色方案"""
    
    @classmethod
    def system(cls) -> ColorScheme:
        """系统默认颜色方案"""
        return ColorScheme("System")
    
    @classmethod
    def developer_dark(cls) -> ColorScheme:
        """开发者深色主题"""
        colors = {
            ColorRole.PRIMARY_TEXT: NSColor.whiteColor(),
            ColorRole.SECONDARY_TEXT: NSColor.lightGrayColor(),
            ColorRole.ACCENT_COLOR: NSColor.systemBlueColor(),
            ColorRole.PRIMARY_BACKGROUND: NSColor.colorWithRed_green_blue_alpha_(0.1, 0.1, 0.1, 1.0),
            ColorRole.SUCCESS_COLOR: NSColor.systemGreenColor(),
            ColorRole.WARNING_COLOR: NSColor.systemYellowColor(),
            ColorRole.ERROR_COLOR: NSColor.systemRedColor(),
        }
        return ColorScheme("Developer Dark", colors)
    
    @classmethod
    def high_contrast(cls) -> ColorScheme:
        """高对比度主题"""
        colors = {
            ColorRole.PRIMARY_TEXT: NSColor.blackColor(),
            ColorRole.SECONDARY_TEXT: NSColor.darkGrayColor(),
            ColorRole.ACCENT_COLOR: NSColor.systemBlueColor(),
            ColorRole.PRIMARY_BACKGROUND: NSColor.whiteColor(),
            ColorRole.SUCCESS_COLOR: NSColor.colorWithRed_green_blue_alpha_(0.0, 0.6, 0.0, 1.0),
            ColorRole.WARNING_COLOR: NSColor.colorWithRed_green_blue_alpha_(0.8, 0.4, 0.0, 1.0),
            ColorRole.ERROR_COLOR: NSColor.colorWithRed_green_blue_alpha_(0.8, 0.0, 0.0, 1.0),
        }
        return ColorScheme("High Contrast", colors)