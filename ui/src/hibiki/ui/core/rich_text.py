#!/usr/bin/env python3
"""
Hibiki UI v4.0 - 富文本支持系统
提供NSAttributedString的完整功能封装
"""

from typing import Optional, Dict, Any, Union, List, Tuple
from dataclasses import dataclass
from enum import Enum
from AppKit import NSColor, NSFont, NSMutableAttributedString, NSRange
from Foundation import NSAttributedString, NSMakeRange

from .logging import get_logger

logger = get_logger("core.rich_text")
logger.setLevel("INFO")


class TextStyle(Enum):
    """文本样式枚举"""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic" 
    BOLD_ITALIC = "bold_italic"


class UnderlineStyle(Enum):
    """下划线样式枚举"""
    NONE = 0
    SINGLE = 1
    THICK = 2
    DOUBLE = 9


class StrikethroughStyle(Enum):
    """删除线样式枚举"""
    NONE = 0
    SINGLE = 1
    THICK = 2
    DOUBLE = 9


@dataclass
class TextAttributes:
    """文本属性配置类"""
    
    # 基础属性
    font_name: Optional[str] = None
    font_size: Optional[float] = None
    text_style: TextStyle = TextStyle.NORMAL
    
    # 颜色属性
    foreground_color: Optional[str] = None  # 前景色 (文字颜色)
    background_color: Optional[str] = None  # 背景色
    
    # 装饰属性
    underline_style: UnderlineStyle = UnderlineStyle.NONE
    underline_color: Optional[str] = None
    strikethrough_style: StrikethroughStyle = StrikethroughStyle.NONE
    strikethrough_color: Optional[str] = None
    
    # 布局属性
    baseline_offset: Optional[float] = None  # 基线偏移
    kern: Optional[float] = None  # 字符间距
    tracking: Optional[float] = None  # 字母间距
    
    # 特殊效果
    stroke_width: Optional[float] = None  # 描边宽度
    stroke_color: Optional[str] = None  # 描边颜色


@dataclass 
class TextSegment:
    """文本片段 - 用于构建富文本"""
    text: str
    attributes: Optional[TextAttributes] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = TextAttributes()


class RichTextBuilder:
    """富文本构建器"""
    
    def __init__(self):
        self.segments: List[TextSegment] = []
        self.default_attributes = TextAttributes()
    
    def set_default_attributes(self, attributes: TextAttributes) -> "RichTextBuilder":
        """设置默认属性"""
        self.default_attributes = attributes
        return self
    
    def add_text(self, text: str, attributes: Optional[TextAttributes] = None) -> "RichTextBuilder":
        """添加文本片段"""
        if attributes is None:
            attributes = self.default_attributes
        self.segments.append(TextSegment(text, attributes))
        return self
    
    def add_bold_text(self, text: str, color: Optional[str] = None, **kwargs) -> "RichTextBuilder":
        """添加粗体文本"""
        if color:
            kwargs['foreground_color'] = color
        attrs = TextAttributes(text_style=TextStyle.BOLD, **kwargs)
        return self.add_text(text, attrs)
    
    def add_italic_text(self, text: str, color: Optional[str] = None, **kwargs) -> "RichTextBuilder":
        """添加斜体文本"""
        if color:
            kwargs['foreground_color'] = color
        attrs = TextAttributes(text_style=TextStyle.ITALIC, **kwargs)
        return self.add_text(text, attrs)
    
    def add_underlined_text(self, text: str, underline_style: UnderlineStyle = UnderlineStyle.SINGLE, color: Optional[str] = None, **kwargs) -> "RichTextBuilder":
        """添加下划线文本"""
        if color:
            kwargs['foreground_color'] = color
        attrs = TextAttributes(underline_style=underline_style, **kwargs)
        return self.add_text(text, attrs)
    
    def add_colored_text(self, text: str, color: str, **kwargs) -> "RichTextBuilder":
        """添加彩色文本"""
        attrs = TextAttributes(foreground_color=color, **kwargs)
        return self.add_text(text, attrs)
    
    def add_highlighted_text(self, text: str, background_color: str, **kwargs) -> "RichTextBuilder":
        """添加高亮文本"""
        attrs = TextAttributes(background_color=background_color, **kwargs)
        return self.add_text(text, attrs)
    
    def build(self) -> NSMutableAttributedString:
        """构建NSAttributedString"""
        if not self.segments:
            return NSMutableAttributedString.alloc().initWithString_("")
        
        result = NSMutableAttributedString.alloc().init()
        
        for segment in self.segments:
            attributed_segment = self._create_attributed_string(segment.text, segment.attributes)
            result.appendAttributedString_(attributed_segment)
        
        logger.debug(f"🎨 富文本构建完成: {len(self.segments)} 个片段")
        return result
    
    def _create_attributed_string(self, text: str, attributes: TextAttributes) -> NSAttributedString:
        """创建单个文本片段的NSAttributedString"""
        attr_dict = {}
        
        # PyObjC NSAttributedString attribute names
        NSFontAttributeName = "NSFont"
        NSForegroundColorAttributeName = "NSColor"
        NSBackgroundColorAttributeName = "NSBackgroundColor"
        NSUnderlineStyleAttributeName = "NSUnderline"
        NSUnderlineColorAttributeName = "NSUnderlineColor"
        NSStrikethroughStyleAttributeName = "NSStrikethrough"
        NSStrikethroughColorAttributeName = "NSStrikethroughColor"
        NSBaselineOffsetAttributeName = "NSBaselineOffset"
        NSKernAttributeName = "NSKern"
        NSStrokeWidthAttributeName = "NSStrokeWidth"
        NSStrokeColorAttributeName = "NSStrokeColor"
        
        # 设置字体
        font = self._create_font(attributes)
        if font:
            attr_dict[NSFontAttributeName] = font
        
        # 设置前景色
        if attributes.foreground_color:
            color = self._parse_color(attributes.foreground_color)
            attr_dict[NSForegroundColorAttributeName] = color
        
        # 设置背景色
        if attributes.background_color:
            bg_color = self._parse_color(attributes.background_color)
            attr_dict[NSBackgroundColorAttributeName] = bg_color
        
        # 设置下划线
        if attributes.underline_style != UnderlineStyle.NONE:
            attr_dict[NSUnderlineStyleAttributeName] = attributes.underline_style.value
            
            if attributes.underline_color:
                underline_color = self._parse_color(attributes.underline_color)
                attr_dict[NSUnderlineColorAttributeName] = underline_color
        
        # 设置删除线
        if attributes.strikethrough_style != StrikethroughStyle.NONE:
            attr_dict[NSStrikethroughStyleAttributeName] = attributes.strikethrough_style.value
            
            if attributes.strikethrough_color:
                strike_color = self._parse_color(attributes.strikethrough_color)
                attr_dict[NSStrikethroughColorAttributeName] = strike_color
        
        # 设置基线偏移
        if attributes.baseline_offset is not None:
            attr_dict[NSBaselineOffsetAttributeName] = attributes.baseline_offset
        
        # 设置字符间距
        if attributes.kern is not None:
            attr_dict[NSKernAttributeName] = attributes.kern
        
        # 设置描边
        if attributes.stroke_width is not None:
            attr_dict[NSStrokeWidthAttributeName] = attributes.stroke_width
            
            if attributes.stroke_color:
                stroke_color = self._parse_color(attributes.stroke_color)
                attr_dict[NSStrokeColorAttributeName] = stroke_color
        
        return NSAttributedString.alloc().initWithString_attributes_(text, attr_dict)
    
    def _create_font(self, attributes: TextAttributes) -> Optional[NSFont]:
        """创建NSFont对象"""
        font_name = attributes.font_name
        font_size = attributes.font_size or 13.0
        
        # 根据样式调整字体
        if attributes.text_style == TextStyle.BOLD:
            return NSFont.boldSystemFontOfSize_(font_size)
        elif attributes.text_style == TextStyle.ITALIC:
            # 简化处理，直接返回系统字体（斜体在NSAttributedString中通过其他方式实现）
            return NSFont.systemFontOfSize_(font_size)
        elif attributes.text_style == TextStyle.BOLD_ITALIC:
            # 简化处理，返回粗体字体
            return NSFont.boldSystemFontOfSize_(font_size)
        else:
            # 使用指定字体名称或系统字体
            if font_name:
                font = NSFont.fontWithName_size_(font_name, font_size)
                return font if font else NSFont.systemFontOfSize_(font_size)
            else:
                return NSFont.systemFontOfSize_(font_size)
    
    def _parse_color(self, color_str: str) -> NSColor:
        """解析颜色字符串为NSColor"""
        if color_str.startswith('#'):
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
            elif len(hex_color) == 8:  # 支持RGBA格式
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                a = int(hex_color[6:8], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, a)
        
        # 支持常见颜色名称
        color_names = {
            'black': NSColor.blackColor(),
            'white': NSColor.whiteColor(),
            'red': NSColor.redColor(),
            'green': NSColor.greenColor(),
            'blue': NSColor.blueColor(),
            'yellow': NSColor.yellowColor(),
            'orange': NSColor.orangeColor(),
            'purple': NSColor.purpleColor(),
            'gray': NSColor.grayColor(),
            'lightGray': NSColor.lightGrayColor(),
            'darkGray': NSColor.darkGrayColor(),
        }
        
        if color_str in color_names:
            return color_names[color_str]
        
        # 默认返回黑色
        return NSColor.blackColor()


class RichText:
    """富文本便捷接口类"""
    
    @staticmethod
    def create(text: str = "") -> RichTextBuilder:
        """创建富文本构建器"""
        builder = RichTextBuilder()
        if text:
            builder.add_text(text)
        return builder
    
    @staticmethod
    def simple_attributed_string(
        text: str,
        font_name: Optional[str] = None,
        font_size: Optional[float] = None,
        color: Optional[str] = None,
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False
    ) -> NSAttributedString:
        """创建简单的富文本字符串"""
        
        # 确定文本样式
        if bold and italic:
            text_style = TextStyle.BOLD_ITALIC
        elif bold:
            text_style = TextStyle.BOLD
        elif italic:
            text_style = TextStyle.ITALIC
        else:
            text_style = TextStyle.NORMAL
        
        # 确定下划线样式
        underline_style = UnderlineStyle.SINGLE if underlined else UnderlineStyle.NONE
        
        # 创建属性
        attributes = TextAttributes(
            font_name=font_name,
            font_size=font_size,
            text_style=text_style,
            foreground_color=color,
            underline_style=underline_style
        )
        
        # 构建富文本
        builder = RichTextBuilder()
        builder.add_text(text, attributes)
        return builder.build()
    
    @staticmethod
    def markdown_like_text(text: str) -> NSAttributedString:
        """解析类似Markdown的简单格式"""
        # 这是一个简化版本，支持基本的 **粗体** 和 *斜体* 语法
        builder = RichTextBuilder()
        
        import re
        
        # 匹配 **粗体** 和 *斜体*
        pattern = r'(\*\*([^*]+)\*\*|\*([^*]+)\*|([^*]+))'
        
        for match in re.finditer(pattern, text):
            full_match = match.group(1)
            bold_text = match.group(2)
            italic_text = match.group(3)
            normal_text = match.group(4)
            
            if bold_text:
                builder.add_bold_text(bold_text)
            elif italic_text:
                builder.add_italic_text(italic_text)
            elif normal_text:
                builder.add_text(normal_text)
        
        return builder.build()


# 导出的便捷函数
def rich_text() -> RichTextBuilder:
    """创建富文本构建器的便捷函数"""
    return RichText.create()


def attributed_string(
    text: str,
    **kwargs
) -> NSAttributedString:
    """创建简单富文本的便捷函数"""
    return RichText.simple_attributed_string(text, **kwargs)


def markdown_text(text: str) -> NSAttributedString:
    """创建类Markdown格式文本的便捷函数"""
    return RichText.markdown_like_text(text)