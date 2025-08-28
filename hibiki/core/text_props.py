#!/usr/bin/env python3
"""
Hibiki UI Text Properties System
文本属性系统 - 专门处理字体、颜色、对齐等文本相关属性
"""

from dataclasses import dataclass
from typing import Optional, Union
from AppKit import NSFont, NSColor, NSTextAlignmentLeft, NSTextAlignmentCenter, NSTextAlignmentRight

@dataclass
class TextProps:
    """文本属性类 - 关注点分离的文本样式管理
    
    设计原则：
    1. 语义化优先 - 鼓励使用TextStyle枚举
    2. 细粒度控制 - 支持直接字体属性
    3. 类型安全 - 只有文本组件才有这些属性
    4. 主题整合 - 与现有字体系统完美融合
    """
    
    # 语义化样式（推荐使用）
    text_style: Optional[str] = None  # TextStyle枚举值
    
    # 直接属性（细粒度控制）
    font_size: Optional[float] = None
    font_weight: Optional[Union[str, float]] = None  # "bold", "normal" or NSFontWeight values
    font_family: Optional[str] = None  # "system", "monospace" or font name
    color: Optional[Union[str, NSColor]] = None
    
    # 文本布局
    text_align: Optional[str] = None  # "left", "center", "right"
    line_height: Optional[float] = None
    letter_spacing: Optional[float] = None
    
    def to_nsfont(self) -> NSFont:
        """转换为NSFont对象
        
        优先级：text_style > 直接属性 > 系统默认
        """
        # 1. 优先使用语义化样式
        if self.text_style:
            return self._get_semantic_font()
        
        # 2. 使用直接属性构建
        size = self.font_size or 17.0  # macOS默认字体大小
        weight = self._parse_font_weight()
        family = self.font_family or "system"
        
        if family == "system":
            return NSFont.systemFontOfSize_weight_(size, weight)
        elif family == "monospace":
            return NSFont.monospacedSystemFontOfSize_weight_(size, weight)
        else:
            # 尝试使用指定字体名，失败则回退到系统字体
            custom_font = NSFont.fontWithName_size_(family, size)
            return custom_font if custom_font else NSFont.systemFontOfSize_weight_(size, weight)
    
    def to_nscolor(self) -> NSColor:
        """转换为NSColor对象"""
        if self.color is None:
            return NSColor.labelColor()  # 系统默认标签颜色
        elif isinstance(self.color, NSColor):
            return self.color
        elif isinstance(self.color, str):
            return self._parse_color_string(self.color)
        else:
            return NSColor.labelColor()
    
    def get_text_alignment(self) -> int:
        """获取NSTextField对齐方式"""
        if not self.text_align:
            return NSTextAlignmentLeft
        
        align_map = {
            "left": NSTextAlignmentLeft,
            "center": NSTextAlignmentCenter,
            "right": NSTextAlignmentRight
        }
        return align_map.get(self.text_align.lower(), NSTextAlignmentLeft)
    
    def _get_semantic_font(self) -> NSFont:
        """获取语义化字体"""
        try:
            # 动态导入以避免循环依赖
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from theme.fonts import SystemFonts, TextStyle
            
            # 字体映射
            font_getters = {
                "large_title": SystemFonts.large_title,
                "title_1": SystemFonts.title_1,
                "title_2": SystemFonts.title_2,
                "title_3": SystemFonts.title_3,
                "headline": SystemFonts.headline,
                "subheadline": SystemFonts.subheadline,
                "body": SystemFonts.body,
                "body_emphasized": SystemFonts.body_emphasized,
                "callout": SystemFonts.callout,
                "footnote": SystemFonts.footnote,
                "caption_1": SystemFonts.caption_1,
                "caption_2": SystemFonts.caption_2,
                "monospace": SystemFonts.monospace,
                "code": SystemFonts.monospace,  # 代码使用等宽字体
            }
            
            getter = font_getters.get(self.text_style.lower(), SystemFonts.body)
            return getter()
            
        except ImportError as e:
            print(f"⚠️ 无法导入字体系统，使用默认字体: {e}")
            return NSFont.systemFontOfSize_(17.0)
    
    def _parse_font_weight(self) -> float:
        """解析字体粗细为NSFontWeight值"""
        if isinstance(self.font_weight, (int, float)):
            # 直接使用数值
            return max(-1.0, min(1.0, float(self.font_weight)))
        
        if isinstance(self.font_weight, str):
            # 字符串映射到NSFontWeight值
            weight_map = {
                "ultralight": -0.8,   # NSFontWeightUltraLight
                "thin": -0.6,         # NSFontWeightThin
                "light": -0.4,        # NSFontWeightLight
                "normal": 0.0,        # NSFontWeightRegular
                "regular": 0.0,       # NSFontWeightRegular
                "medium": 0.23,       # NSFontWeightMedium
                "semibold": 0.3,      # NSFontWeightSemibold
                "bold": 0.4,          # NSFontWeightBold
                "heavy": 0.56,        # NSFontWeightHeavy
                "black": 0.62         # NSFontWeightBlack
            }
            return weight_map.get(self.font_weight.lower(), 0.0)
        
        return 0.0  # 默认regular
    
    def _parse_color_string(self, color_str: str) -> NSColor:
        """解析颜色字符串"""
        color_str = color_str.strip()
        
        # 处理16进制颜色
        if color_str.startswith('#'):
            return self._parse_hex_color(color_str)
        
        # 处理命名颜色
        named_colors = {
            "black": NSColor.blackColor(),
            "white": NSColor.whiteColor(),
            "red": NSColor.redColor(),
            "green": NSColor.greenColor(),
            "blue": NSColor.blueColor(),
            "yellow": NSColor.yellowColor(),
            "orange": NSColor.orangeColor(),
            "purple": NSColor.purpleColor(),
            "gray": NSColor.grayColor(),
            "grey": NSColor.grayColor(),
            "brown": NSColor.brownColor(),
            "cyan": NSColor.cyanColor(),
            "magenta": NSColor.magentaColor(),
            # 系统颜色
            "label": NSColor.labelColor(),
            "secondary_label": NSColor.secondaryLabelColor(),
            "tertiary_label": NSColor.tertiaryLabelColor(),
        }
        
        return named_colors.get(color_str.lower(), NSColor.labelColor())
    
    def _parse_hex_color(self, hex_color: str) -> NSColor:
        """解析16进制颜色 (#RGB, #RRGGBB, #RRGGBBAA)"""
        hex_color = hex_color.lstrip('#')
        
        try:
            if len(hex_color) == 3:
                # #RGB -> #RRGGBB
                r = int(hex_color[0] * 2, 16) / 255.0
                g = int(hex_color[1] * 2, 16) / 255.0
                b = int(hex_color[2] * 2, 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
            elif len(hex_color) == 6:
                # #RRGGBB
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
            elif len(hex_color) == 8:
                # #RRGGBBAA
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                a = int(hex_color[6:8], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
        except ValueError:
            print(f"⚠️ 无效的16进制颜色值: {hex_color}")
        
        return NSColor.labelColor()  # 失败时返回默认颜色

# ================================
# 便捷函数
# ================================

def text_props(text_style: Optional[str] = None,
               font_size: Optional[float] = None,
               font_weight: Optional[str] = None,
               font_family: Optional[str] = None,
               color: Optional[str] = None,
               text_align: Optional[str] = None,
               line_height: Optional[float] = None,
               letter_spacing: Optional[float] = None) -> TextProps:
    """便捷的TextProps创建函数"""
    return TextProps(
        text_style=text_style,
        font_size=font_size,
        font_weight=font_weight,
        font_family=font_family,
        color=color,
        text_align=text_align,
        line_height=line_height,
        letter_spacing=letter_spacing
    )

# ================================
# 预设样式
# ================================

class TextStyles:
    """常用文本样式预设"""
    
    @staticmethod
    def title() -> TextProps:
        """标题样式"""
        return TextProps(text_style="title_1")
    
    @staticmethod
    def subtitle() -> TextProps:
        """副标题样式"""
        return TextProps(text_style="title_2", color="secondary_label")
    
    @staticmethod
    def body() -> TextProps:
        """正文样式"""
        return TextProps(text_style="body")
    
    @staticmethod
    def caption() -> TextProps:
        """说明文字样式"""
        return TextProps(text_style="caption_1", color="secondary_label")
    
    @staticmethod
    def code() -> TextProps:
        """代码样式"""
        return TextProps(font_family="monospace", font_size=13, color="label")
    
    @staticmethod
    def error() -> TextProps:
        """错误信息样式"""
        return TextProps(text_style="body", color="#ff3333")
    
    @staticmethod
    def success() -> TextProps:
        """成功信息样式"""
        return TextProps(text_style="body", color="#00aa00")
    
    @staticmethod
    def warning() -> TextProps:
        """警告信息样式"""
        return TextProps(text_style="body", color="#ff8800")

if __name__ == "__main__":
    print("🎨 Hibiki UI 文本属性系统")
    
    # 测试各种用法
    test_props = [
        TextProps(text_style="title_1"),
        TextProps(font_size=16, font_weight="bold", color="#333"),
        TextProps(font_family="monospace", color="#007acc"),
        text_props(text_style="body", text_align="center"),
        TextStyles.error()
    ]
    
    for i, props in enumerate(test_props):
        font = props.to_nsfont()
        color = props.to_nscolor()
        align = props.get_text_alignment()
        print(f"  {i+1}. Font: {font.fontName()}, Size: {font.pointSize()}, Align: {align}")
    
    print("✅ 文本属性系统测试完成")