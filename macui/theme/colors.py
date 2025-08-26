"""macUI v2 颜色系统

提供动态颜色和主题颜色管理，自动适应Light/Dark模式。
"""

from typing import Optional, Dict, Any
from enum import Enum

from AppKit import NSColor
from Foundation import NSUserDefaults


class ColorRole(Enum):
    """颜色角色定义 - 基于苹果设计指南"""
    # 文本颜色
    PRIMARY_TEXT = "primary_text"           # 主文本
    SECONDARY_TEXT = "secondary_text"       # 次要文本  
    TERTIARY_TEXT = "tertiary_text"        # 三级文本
    PLACEHOLDER_TEXT = "placeholder_text"   # 占位文本
    
    # 背景颜色
    PRIMARY_BACKGROUND = "primary_background"       # 主背景
    SECONDARY_BACKGROUND = "secondary_background"   # 次要背景
    TERTIARY_BACKGROUND = "tertiary_background"     # 三级背景
    
    # 交互颜色
    ACCENT_COLOR = "accent_color"          # 强调色（系统蓝）
    SUCCESS_COLOR = "success_color"        # 成功色
    WARNING_COLOR = "warning_color"        # 警告色
    ERROR_COLOR = "error_color"            # 错误色
    
    # 控件颜色
    CONTROL_TEXT = "control_text"          # 控件文本
    CONTROL_BACKGROUND = "control_background" # 控件背景
    SELECTED_TEXT = "selected_text"        # 选中文本
    SELECTED_BACKGROUND = "selected_background" # 选中背景


class SystemColors:
    """macOS系统动态颜色封装
    
    这些颜色会自动适应Light/Dark模式，无需手动处理。
    """
    
    @staticmethod
    def is_dark_mode() -> bool:
        """检测当前是否为Dark模式"""
        try:
            interface_style = NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle')
            return interface_style == 'Dark'
        except:
            return False
    
    # === 文本颜色 ===
    @classmethod
    def primary_text(cls) -> NSColor:
        """主文本颜色 - 自动适应外观"""
        return NSColor.labelColor()
    
    @classmethod 
    def secondary_text(cls) -> NSColor:
        """次要文本颜色"""
        return NSColor.secondaryLabelColor()
        
    @classmethod
    def tertiary_text(cls) -> NSColor:
        """三级文本颜色"""
        return NSColor.tertiaryLabelColor()
    
    @classmethod
    def placeholder_text(cls) -> NSColor:
        """占位文本颜色"""
        return NSColor.placeholderTextColor()
    
    # === 背景颜色 ===
    @classmethod
    def primary_background(cls) -> NSColor:
        """主背景颜色"""
        return NSColor.controlBackgroundColor()
        
    @classmethod  
    def secondary_background(cls) -> NSColor:
        """次要背景颜色"""
        return NSColor.controlColor()
        
    @classmethod
    def tertiary_background(cls) -> NSColor:
        """三级背景颜色"""
        return NSColor.controlAlternatingRowBackgroundColors()[0] if NSColor.controlAlternatingRowBackgroundColors() else NSColor.controlColor()
    
    # === 交互颜色 ===
    @classmethod
    def accent_color(cls) -> NSColor:
        """系统强调色（蓝色）"""
        return NSColor.systemBlueColor()
    
    @classmethod
    def success_color(cls) -> NSColor:
        """成功色（绿色）"""
        return NSColor.systemGreenColor()
        
    @classmethod
    def warning_color(cls) -> NSColor:
        """警告色（橙色）"""
        return NSColor.systemOrangeColor()
        
    @classmethod
    def error_color(cls) -> NSColor:
        """错误色（红色）"""
        return NSColor.systemRedColor()
    
    # === 控件颜色 ===
    @classmethod
    def control_text(cls) -> NSColor:
        """控件文本颜色"""
        return NSColor.controlTextColor()
        
    @classmethod
    def control_background(cls) -> NSColor:
        """控件背景颜色"""
        return NSColor.controlBackgroundColor()
        
    @classmethod
    def selected_text(cls) -> NSColor:
        """选中文本颜色"""
        return NSColor.selectedControlTextColor()
        
    @classmethod
    def selected_background(cls) -> NSColor:
        """选中背景颜色"""
        return NSColor.selectedControlColor()


class ColorScheme:
    """颜色方案类 - 支持自定义主题"""
    
    def __init__(self, name: str, colors: Optional[Dict[ColorRole, NSColor]] = None):
        self.name = name
        self._colors: Dict[ColorRole, NSColor] = colors or {}
        self._use_system_defaults = colors is None
    
    def get_color(self, role: ColorRole) -> NSColor:
        """获取指定角色的颜色"""
        if role in self._colors:
            return self._colors[role]
        
        # 回退到系统默认颜色
        return self._get_system_color(role)
    
    def set_color(self, role: ColorRole, color: NSColor):
        """设置指定角色的颜色"""
        self._colors[role] = color
        self._use_system_defaults = False
    
    def _get_system_color(self, role: ColorRole) -> NSColor:
        """获取系统默认颜色"""
        color_mapping = {
            ColorRole.PRIMARY_TEXT: SystemColors.primary_text,
            ColorRole.SECONDARY_TEXT: SystemColors.secondary_text,
            ColorRole.TERTIARY_TEXT: SystemColors.tertiary_text,
            ColorRole.PLACEHOLDER_TEXT: SystemColors.placeholder_text,
            
            ColorRole.PRIMARY_BACKGROUND: SystemColors.primary_background,
            ColorRole.SECONDARY_BACKGROUND: SystemColors.secondary_background, 
            ColorRole.TERTIARY_BACKGROUND: SystemColors.tertiary_background,
            
            ColorRole.ACCENT_COLOR: SystemColors.accent_color,
            ColorRole.SUCCESS_COLOR: SystemColors.success_color,
            ColorRole.WARNING_COLOR: SystemColors.warning_color,
            ColorRole.ERROR_COLOR: SystemColors.error_color,
            
            ColorRole.CONTROL_TEXT: SystemColors.control_text,
            ColorRole.CONTROL_BACKGROUND: SystemColors.control_background,
            ColorRole.SELECTED_TEXT: SystemColors.selected_text,
            ColorRole.SELECTED_BACKGROUND: SystemColors.selected_background,
        }
        
        getter = color_mapping.get(role)
        if getter:
            return getter()
        
        # 默认返回主文本颜色
        return SystemColors.primary_text()
    
    def is_system_scheme(self) -> bool:
        """是否为系统默认方案"""
        return self._use_system_defaults
    
    @classmethod
    def system_scheme(cls) -> "ColorScheme":
        """创建系统默认颜色方案"""
        return cls("System", None)
    
    @classmethod
    def custom_scheme(cls, name: str, colors: Dict[ColorRole, NSColor]) -> "ColorScheme":
        """创建自定义颜色方案"""
        return cls(name, colors)


# 预设颜色方案
class PresetColorSchemes:
    """预设颜色方案集合"""
    
    @classmethod
    def system(cls) -> ColorScheme:
        """系统默认方案"""
        return ColorScheme.system_scheme()
    
    @classmethod
    def high_contrast(cls) -> ColorScheme:
        """高对比度方案"""
        colors = {
            ColorRole.PRIMARY_TEXT: NSColor.blackColor(),
            ColorRole.SECONDARY_TEXT: NSColor.darkGrayColor(),
            ColorRole.PRIMARY_BACKGROUND: NSColor.whiteColor(),
            ColorRole.SECONDARY_BACKGROUND: NSColor.lightGrayColor(),
            ColorRole.ACCENT_COLOR: NSColor.blueColor(),
        }
        return ColorScheme.custom_scheme("High Contrast", colors)
    
    @classmethod
    def developer_dark(cls) -> ColorScheme:
        """开发者深色方案"""
        colors = {
            ColorRole.PRIMARY_TEXT: NSColor.whiteColor(),
            ColorRole.SECONDARY_TEXT: NSColor.lightGrayColor(), 
            ColorRole.PRIMARY_BACKGROUND: NSColor.colorWithRed_green_blue_alpha_(0.1, 0.1, 0.1, 1.0),
            ColorRole.SECONDARY_BACKGROUND: NSColor.colorWithRed_green_blue_alpha_(0.15, 0.15, 0.15, 1.0),
            ColorRole.ACCENT_COLOR: NSColor.systemBlueColor(),
        }
        return ColorScheme.custom_scheme("Developer Dark", colors)