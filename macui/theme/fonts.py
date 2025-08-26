"""macUI v2 字体系统

提供字体管理和文本样式定义。
"""

from typing import Optional, Dict
from enum import Enum

from AppKit import (
    NSFont,
    NSFontWeightUltraLight,
    NSFontWeightThin,
    NSFontWeightLight, 
    NSFontWeightRegular,
    NSFontWeightMedium,
    NSFontWeightSemibold,
    NSFontWeightBold,
    NSFontWeightHeavy,
    NSFontWeightBlack
)


class FontWeight(Enum):
    """字体粗细"""
    ULTRALIGHT = "UltraLight"
    THIN = "Thin" 
    LIGHT = "Light"
    REGULAR = "Regular"
    MEDIUM = "Medium"
    SEMIBOLD = "Semibold"
    BOLD = "Bold"
    HEAVY = "Heavy"
    BLACK = "Black"


class TextStyle(Enum):
    """文本样式角色 - 基于苹果Typography指南"""
    # 标题
    LARGE_TITLE = "large_title"      # 大标题 (34pt)
    TITLE_1 = "title_1"              # 标题1 (28pt)
    TITLE_2 = "title_2"              # 标题2 (22pt) 
    TITLE_3 = "title_3"              # 标题3 (20pt)
    
    # 标题栏
    HEADLINE = "headline"            # 标题栏 (17pt, Semibold)
    SUBHEADLINE = "subheadline"      # 副标题栏 (15pt)
    
    # 正文
    BODY = "body"                    # 正文 (17pt)
    BODY_EMPHASIZED = "body_emphasized" # 强调正文 (17pt, Semibold)
    
    # 辅助文本
    CALLOUT = "callout"              # 标注 (16pt)
    FOOTNOTE = "footnote"            # 脚注 (13pt) 
    CAPTION_1 = "caption_1"          # 说明1 (12pt)
    CAPTION_2 = "caption_2"          # 说明2 (11pt)
    
    # 控件字体
    CONTROL = "control"              # 控件字体 (13pt)
    CONTROL_SMALL = "control_small"  # 小控件字体 (11pt)


class SystemFonts:
    """macOS系统字体封装"""
    
    @classmethod
    def system_font(cls, size: float = 13.0, weight: Optional[FontWeight] = None) -> NSFont:
        """系统字体"""
        if weight:
            return NSFont.systemFontOfSize_weight_(size, cls._get_font_weight(weight))
        return NSFont.systemFontOfSize_(size)
    
    @classmethod
    def bold_system_font(cls, size: float = 13.0) -> NSFont:
        """粗体系统字体"""
        return NSFont.boldSystemFontOfSize_(size)
    
    @classmethod 
    def monospace_font(cls, size: float = 13.0, weight: Optional[FontWeight] = None) -> NSFont:
        """等宽字体（代码字体）"""
        if weight:
            return NSFont.monospacedSystemFontOfSize_weight_(size, cls._get_font_weight(weight))
        return NSFont.monospacedSystemFontOfSize_weight_(size, NSFontWeightRegular)
    
    @classmethod
    def label_font(cls, size: float = 13.0) -> NSFont:
        """标签字体"""
        return NSFont.labelFontOfSize_(size)
    
    @classmethod
    def control_content_font(cls, size: float = 13.0) -> NSFont:
        """控件内容字体"""
        return NSFont.controlContentFontOfSize_(size)
    
    @classmethod
    def menu_font(cls, size: float = 14.0) -> NSFont:
        """菜单字体"""
        return NSFont.menuFontOfSize_(size)
    
    @classmethod
    def _get_font_weight(cls, weight: FontWeight) -> float:
        """转换字体粗细枚举到NSFont权重值"""
        weight_mapping = {
            FontWeight.ULTRALIGHT: NSFontWeightUltraLight,
            FontWeight.THIN: NSFontWeightThin,
            FontWeight.LIGHT: NSFontWeightLight, 
            FontWeight.REGULAR: NSFontWeightRegular,
            FontWeight.MEDIUM: NSFontWeightMedium,
            FontWeight.SEMIBOLD: NSFontWeightSemibold,
            FontWeight.BOLD: NSFontWeightBold,
            FontWeight.HEAVY: NSFontWeightHeavy,
            FontWeight.BLACK: NSFontWeightBlack,
        }
        return weight_mapping.get(weight, NSFontWeightRegular)


class FontScheme:
    """字体方案类 - 定义应用的字体系统"""
    
    def __init__(self, name: str):
        self.name = name
        self._fonts: Dict[TextStyle, NSFont] = {}
        self._setup_default_fonts()
    
    def _setup_default_fonts(self):
        """设置默认字体配置（基于苹果设计指南）"""
        self._fonts = {
            # 标题
            TextStyle.LARGE_TITLE: SystemFonts.system_font(34.0, FontWeight.REGULAR),
            TextStyle.TITLE_1: SystemFonts.system_font(28.0, FontWeight.REGULAR), 
            TextStyle.TITLE_2: SystemFonts.system_font(22.0, FontWeight.REGULAR),
            TextStyle.TITLE_3: SystemFonts.system_font(20.0, FontWeight.REGULAR),
            
            # 标题栏
            TextStyle.HEADLINE: SystemFonts.system_font(17.0, FontWeight.SEMIBOLD),
            TextStyle.SUBHEADLINE: SystemFonts.system_font(15.0, FontWeight.REGULAR),
            
            # 正文
            TextStyle.BODY: SystemFonts.system_font(17.0, FontWeight.REGULAR),
            TextStyle.BODY_EMPHASIZED: SystemFonts.system_font(17.0, FontWeight.SEMIBOLD),
            
            # 辅助文本
            TextStyle.CALLOUT: SystemFonts.system_font(16.0, FontWeight.REGULAR),
            TextStyle.FOOTNOTE: SystemFonts.system_font(13.0, FontWeight.REGULAR),
            TextStyle.CAPTION_1: SystemFonts.system_font(12.0, FontWeight.REGULAR),
            TextStyle.CAPTION_2: SystemFonts.system_font(11.0, FontWeight.REGULAR),
            
            # 控件字体
            TextStyle.CONTROL: SystemFonts.control_content_font(13.0),
            TextStyle.CONTROL_SMALL: SystemFonts.control_content_font(11.0),
        }
    
    def get_font(self, style: TextStyle) -> NSFont:
        """获取指定样式的字体"""
        return self._fonts.get(style, SystemFonts.system_font())
    
    def set_font(self, style: TextStyle, font: NSFont):
        """设置指定样式的字体"""
        self._fonts[style] = font
    
    def update_font_size(self, style: TextStyle, size: float):
        """更新指定样式的字体大小"""
        current_font = self._fonts.get(style, SystemFonts.system_font())
        font_descriptor = current_font.fontDescriptor()
        new_font = NSFont.fontWithDescriptor_size_(font_descriptor, size)
        self._fonts[style] = new_font
    
    @classmethod 
    def system_scheme(cls) -> "FontScheme":
        """创建系统默认字体方案"""
        return cls("System")
    
    @classmethod
    def developer_scheme(cls) -> "FontScheme":
        """创建开发者字体方案（更多使用等宽字体）"""
        scheme = cls("Developer")
        # 为代码相关的样式使用等宽字体
        scheme.set_font(TextStyle.BODY, SystemFonts.monospace_font(14.0))
        scheme.set_font(TextStyle.CALLOUT, SystemFonts.monospace_font(13.0))
        scheme.set_font(TextStyle.FOOTNOTE, SystemFonts.monospace_font(12.0))
        return scheme
    
    @classmethod
    def accessibility_scheme(cls) -> "FontScheme": 
        """创建无障碍字体方案（更大字号）"""
        scheme = cls("Accessibility")
        # 增大所有字体的尺寸
        for style in TextStyle:
            current_font = scheme._fonts[style]
            current_size = current_font.pointSize()
            scheme.update_font_size(style, current_size * 1.2)  # 增大20%
        return scheme


# 预设字体方案
class PresetFontSchemes:
    """预设字体方案集合"""
    
    @classmethod
    def system(cls) -> FontScheme:
        """系统默认方案"""
        return FontScheme.system_scheme()
    
    @classmethod
    def developer(cls) -> FontScheme:
        """开发者方案"""
        return FontScheme.developer_scheme()
    
    @classmethod  
    def accessibility(cls) -> FontScheme:
        """无障碍方案"""
        return FontScheme.accessibility_scheme()