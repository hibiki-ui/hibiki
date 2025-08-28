"""macUI v4 字体系统

提供系统级字体管理和文本样式支持
"""

from typing import Optional, Dict
from enum import Enum
from AppKit import NSFont


class TextStyle(Enum):
    """文本样式定义"""
    # 标题类
    LARGE_TITLE = "large_title"
    TITLE_1 = "title_1" 
    TITLE_2 = "title_2"
    TITLE_3 = "title_3"
    HEADLINE = "headline"
    SUBHEADLINE = "subheadline"
    
    # 正文类
    BODY = "body"
    BODY_EMPHASIZED = "body_emphasized"
    CALLOUT = "callout"
    
    # 辅助类
    FOOTNOTE = "footnote"
    CAPTION_1 = "caption_1"
    CAPTION_2 = "caption_2"
    
    # 特殊类
    MONOSPACE = "monospace"
    CODE = "code"


class SystemFonts:
    """系统字体获取器"""
    
    @classmethod
    def large_title(cls) -> NSFont:
        """大标题字体"""
        return NSFont.systemFontOfSize_weight_(34.0, -0.8)  # NSFontWeightThin
    
    @classmethod  
    def title_1(cls) -> NSFont:
        """标题1字体"""
        return NSFont.systemFontOfSize_weight_(28.0, 0.0)  # NSFontWeightRegular
    
    @classmethod
    def title_2(cls) -> NSFont:
        """标题2字体"""
        return NSFont.systemFontOfSize_weight_(22.0, 0.0)  # NSFontWeightRegular
    
    @classmethod
    def title_3(cls) -> NSFont:
        """标题3字体"""
        return NSFont.systemFontOfSize_weight_(20.0, 0.0)  # NSFontWeightRegular
    
    @classmethod
    def headline(cls) -> NSFont:
        """标题栏字体"""
        return NSFont.systemFontOfSize_weight_(17.0, 0.23)  # NSFontWeightSemibold
    
    @classmethod
    def subheadline(cls) -> NSFont:
        """副标题字体"""
        return NSFont.systemFontOfSize_weight_(15.0, 0.0)  # NSFontWeightRegular
    
    @classmethod
    def body(cls) -> NSFont:
        """正文字体"""
        return NSFont.systemFontOfSize_(17.0)
    
    @classmethod
    def body_emphasized(cls) -> NSFont:
        """强调正文字体"""
        return NSFont.systemFontOfSize_weight_(17.0, 0.23)  # NSFontWeightSemibold
    
    @classmethod
    def callout(cls) -> NSFont:
        """标注字体"""
        return NSFont.systemFontOfSize_(16.0)
    
    @classmethod
    def footnote(cls) -> NSFont:
        """脚注字体"""
        return NSFont.systemFontOfSize_(13.0)
    
    @classmethod
    def caption_1(cls) -> NSFont:
        """说明文字1"""
        return NSFont.systemFontOfSize_(12.0)
    
    @classmethod
    def caption_2(cls) -> NSFont:
        """说明文字2"""
        return NSFont.systemFontOfSize_(11.0)
    
    @classmethod
    def monospace(cls) -> NSFont:
        """等宽字体"""
        return NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0)  # NSFontWeightRegular
    
    @classmethod
    def code(cls) -> NSFont:
        """代码字体"""
        return NSFont.monospacedSystemFontOfSize_weight_(14.0, 0.0)  # NSFontWeightRegular


class FontScheme:
    """字体方案"""
    
    def __init__(self, name: str, fonts: Optional[Dict[TextStyle, NSFont]] = None):
        self.name = name
        self._fonts = fonts or {}
    
    def get_font(self, style: TextStyle) -> NSFont:
        """获取指定样式的字体"""
        if style in self._fonts:
            return self._fonts[style]
        
        # 回退到系统字体
        return self._get_system_font(style)
    
    def set_font(self, style: TextStyle, font: NSFont):
        """设置字体"""
        self._fonts[style] = font
    
    def _get_system_font(self, style: TextStyle) -> NSFont:
        """获取系统默认字体"""
        system_font_map = {
            TextStyle.LARGE_TITLE: SystemFonts.large_title,
            TextStyle.TITLE_1: SystemFonts.title_1,
            TextStyle.TITLE_2: SystemFonts.title_2,
            TextStyle.TITLE_3: SystemFonts.title_3,
            TextStyle.HEADLINE: SystemFonts.headline,
            TextStyle.SUBHEADLINE: SystemFonts.subheadline,
            TextStyle.BODY: SystemFonts.body,
            TextStyle.BODY_EMPHASIZED: SystemFonts.body_emphasized,
            TextStyle.CALLOUT: SystemFonts.callout,
            TextStyle.FOOTNOTE: SystemFonts.footnote,
            TextStyle.CAPTION_1: SystemFonts.caption_1,
            TextStyle.CAPTION_2: SystemFonts.caption_2,
            TextStyle.MONOSPACE: SystemFonts.monospace,
            TextStyle.CODE: SystemFonts.code,
        }
        
        font_func = system_font_map.get(style)
        return font_func() if font_func else SystemFonts.body()


class PresetFontSchemes:
    """预设字体方案"""
    
    @classmethod
    def system(cls) -> FontScheme:
        """系统默认字体方案"""
        return FontScheme("System")
    
    @classmethod
    def developer(cls) -> FontScheme:
        """开发者字体方案 - 更多等宽字体"""
        fonts = {
            TextStyle.CODE: NSFont.monospacedSystemFontOfSize_weight_(13.0, 0.0),
            TextStyle.MONOSPACE: NSFont.monospacedSystemFontOfSize_weight_(12.0, 0.0),
            TextStyle.BODY: NSFont.systemFontOfSize_(16.0),
            TextStyle.FOOTNOTE: NSFont.monospacedSystemFontOfSize_weight_(11.0, 0.0),
        }
        return FontScheme("Developer", fonts)
    
    @classmethod
    def accessibility(cls) -> FontScheme:
        """无障碍字体方案 - 更大字号"""
        fonts = {
            TextStyle.LARGE_TITLE: NSFont.systemFontOfSize_weight_(40.0, -0.8),
            TextStyle.TITLE_1: NSFont.systemFontOfSize_weight_(32.0, 0.0),
            TextStyle.TITLE_2: NSFont.systemFontOfSize_weight_(26.0, 0.0),
            TextStyle.HEADLINE: NSFont.systemFontOfSize_weight_(20.0, 0.23),
            TextStyle.BODY: NSFont.systemFontOfSize_(19.0),
            TextStyle.FOOTNOTE: NSFont.systemFontOfSize_(15.0),
        }
        return FontScheme("Accessibility", fonts)