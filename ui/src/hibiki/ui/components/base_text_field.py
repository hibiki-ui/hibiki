#!/usr/bin/env python3
"""
Hibiki UI v4.0 - 基础TextField组件
提供NSTextField的完整功能封装，供Label和TextField复用
"""

from typing import Optional, Union, Any
from AppKit import (
    NSView, NSTextField, NSLineBreakByWordWrapping, NSMakeRect,
    NSColor, NSBezelBorder, NSNoBorder, NSTextFieldCell
)
from Foundation import NSAttributedString, NSMakeSize, NSMakeRect as NSRect
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Computed
from ..core.binding import bind_text
from ..core.logging import get_logger
from .text_field_config import TextFieldConfig, BezelStyle

logger = get_logger("components.base_text_field")
logger.setLevel("INFO")


class VerticallyCenteredTextFieldCell(NSTextFieldCell):
    """垂直居中的TextFieldCell - 基于Stack Overflow最佳实践实现"""
    
    def init(self):
        self = objc.super(VerticallyCenteredTextFieldCell, self).init()
        if self is None:
            return None
        self._is_editing_or_selecting = False
        return self
    
    def titleRectForBounds_(self, frame):
        """计算文本标题矩形以实现垂直居中 - 这是关键方法"""
        # 获取父类的默认标题矩形
        title_rect = objc.super(VerticallyCenteredTextFieldCell, self).titleRectForBounds_(frame)
        
        # 获取属性字符串
        attributed_string = self.attributedStringValue()
        if not attributed_string or attributed_string.length() == 0:
            return title_rect
        
        # 计算文本的实际绘制区域
        # 使用NSStringDrawingOptions来精确计算
        from AppKit import NSStringDrawingTruncatesLastVisibleLine, NSStringDrawingUsesLineFragmentOrigin
        from Foundation import NSMakeSize
        
        text_rect = attributed_string.boundingRectWithSize_options_(
            NSMakeSize(title_rect.size.width, title_rect.size.height),
            NSStringDrawingTruncatesLastVisibleLine | NSStringDrawingUsesLineFragmentOrigin
        )
        
        # 🔧 修复：保持原有高度，避免文本被裁剪
        # 只调整Y位置进行垂直居中，但保持足够的高度
        if text_rect.size.height < title_rect.size.height:
            # 计算垂直居中的偏移
            y_offset = (frame.size.height - text_rect.size.height) / 2.0
            
            # 创建居中的矩形 - 关键修复：保持原有高度或使用更大的高度
            from Foundation import NSMakeRect
            # 使用原有的title_rect高度，确保文本不被裁剪
            safe_height = max(text_rect.size.height, title_rect.size.height)
            title_rect = NSMakeRect(
                frame.origin.x,                           # X位置不变
                frame.origin.y + max(0, y_offset),       # Y位置垂直居中，但不能为负
                frame.size.width,                        # 宽度保持
                safe_height                              # 使用安全的高度
            )
        else:
            # 如果文本较高，使用原始title_rect避免裁剪
            title_rect = title_rect
        
        return title_rect
    
    def drawInteriorWithFrame_inView_(self, cell_frame, control_view):
        """重写内部绘制方法 - 分离背景和文本绘制"""
        # 🎨 策略：手动分离背景绘制和文本绘制
        
        # 1. 首先绘制背景（如果需要）- 使用完整的cell_frame
        if self.drawsBackground():
            bg_color = self.backgroundColor()
            if bg_color:
                bg_color.set()
                from AppKit import NSRectFill
                NSRectFill(cell_frame)
        
        # 2. 然后绘制文本 - 使用居中的title_rect
        title_rect = self.titleRectForBounds_(cell_frame)
        
        # 3. 手动绘制属性字符串
        attributed_string = self.attributedStringValue()
        if attributed_string and attributed_string.length() > 0:
            attributed_string.drawInRect_(title_rect)
    
    def selectWithFrame_inView_editor_delegate_start_length_(self, frame, control_view, text_obj, delegate, sel_start, sel_length):
        """重写选择方法以保持垂直居中（编辑状态）"""
        # 🔧 标记进入选择/编辑状态
        self._is_editing_or_selecting = True
        
        # 计算居中的frame给field editor使用
        title_rect = self.titleRectForBounds_(frame)
        
        # 调用父类方法，但使用居中的rect
        return objc.super(VerticallyCenteredTextFieldCell, self).selectWithFrame_inView_editor_delegate_start_length_(
            title_rect, control_view, text_obj, delegate, sel_start, sel_length
        )
    
    def editWithFrame_inView_editor_delegate_event_(self, frame, control_view, text_obj, delegate, event):
        """重写编辑方法以保持垂直居中（编辑状态）"""  
        # 🔧 标记进入编辑状态
        self._is_editing_or_selecting = True
        
        # 计算居中的frame给field editor使用
        title_rect = self.titleRectForBounds_(frame)
        
        objc.super(VerticallyCenteredTextFieldCell, self).editWithFrame_inView_editor_delegate_event_(
            title_rect, control_view, text_obj, delegate, event
        )
    
    def endEditing_(self, text_obj):
        """重写编辑结束方法，重置状态标志"""
        # 🔧 标记退出选择/编辑状态
        self._is_editing_or_selecting = False
        return objc.super(VerticallyCenteredTextFieldCell, self).endEditing_(text_obj)


class _BaseTextField(UIComponent):
    """NSTextField完整功能封装基础类
    
    提供NSTextField的所有功能，供Label和TextField组件复用。
    使用配置对象模式避免代码冗余。
    """
    
    def __init__(
        self,
        text: Union[str, Any],
        style: Optional[ComponentStyle] = None,
        config: Optional[TextFieldConfig] = None,
        # 向后兼容的便捷参数
        font_size: Optional[float] = None,
        font_weight: Optional[str] = None,
        font_family: Optional[str] = None,
        color: Optional[str] = None,
        text_align: Optional[str] = None,
        line_height: Optional[Union[int, float, str]] = None,
        font_style: Optional[str] = None,
        **style_kwargs,
    ):
        """初始化基础TextField组件
        
        Args:
            text: 文本内容，支持响应式Signal
            style: 组件样式对象
            config: TextField配置对象
            其他参数: 向后兼容的便捷样式参数
        """
        # 🔧 统一样式处理：将便捷参数合并到ComponentStyle
        if not style:
            style = ComponentStyle()
        
        # 合并便捷文本参数到ComponentStyle
        text_params = {
            'color': color,
            'font_size': font_size,
            'font_weight': font_weight,
            'font_family': font_family,
            'text_align': text_align,
            'line_height': line_height,
            'font_style': font_style
        }
        
        for param, value in text_params.items():
            if value is not None:
                if getattr(style, param) is None:
                    setattr(style, param, value)
        
        super().__init__(style, **style_kwargs)
        
        # 存储配置和文本
        self.text = text
        self.config = config or TextFieldConfig()
        
        # 检查是否为响应式文本或富文本
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        self._is_rich_text = isinstance(text, NSAttributedString)
        
        # 创建TextProps用于向后兼容
        self._create_text_props()
        
        logger.debug(
            f"🏗️ BaseTextField创建: text='{text}', reactive={self._is_reactive_text}, "
            f"rich_text={self._is_rich_text}, editable={self.config.editable}, selectable={self.config.selectable}"
        )
    
    def _create_text_props(self):
        """创建TextProps对象（向后兼容）"""
        from ..core.text_props import TextProps
        
        self.text_props = TextProps(
            color=self.style.color,
            font_size=self.style.font_size,
            font_weight=self.style.font_weight,
            font_family=self.style.font_family,
            text_align=self.style.text_align,
        )
    
    def _create_nsview(self) -> NSView:
        """🚀 创建完整配置的NSTextField"""
        # 🔧 临时修复：使用更大的初始尺寸避免0x0问题
        textfield = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 30))
        
        # 🔧 临时注释掉垂直居中功能，恢复常规NSTextField行为
        # 对所有不可编辑的组件（Label）都使用垂直居中
        # 包括有边框、有背景色或者普通的Label都需要垂直居中
        # if not self.config.editable:
        #     # 创建垂直居中的TextFieldCell
        #     cell = VerticallyCenteredTextFieldCell.alloc().init()
        #     textfield.setCell_(cell)
        #     logger.debug(f"🎯 应用垂直居中cell - 边框:{self.config.bordered}, 背景:{bool(self.config.background_color)}")
        
        # 使用默认的NSTextField行为
        logger.debug(f"📝 使用默认NSTextField - 可编辑:{self.config.editable}")
        
        # 🔧 应用核心功能配置
        textfield.setEditable_(self.config.editable)
        textfield.setSelectable_(self.config.selectable)
        
        # 🎨 应用外观配置
        self._apply_appearance_config(textfield)
        
        # 📝 应用文本配置
        self._apply_text_config(textfield)
        
        # 🎯 应用样式配置
        self._apply_style_config(textfield)
        
        # 🔗 绑定事件
        self._bind_events(textfield)
        
        return textfield
    
    def _apply_appearance_config(self, textfield: NSTextField):
        """应用外观配置"""
        # 边框配置
        textfield.setBezeled_(self.config.bordered)
        
        if self.config.bordered and self.config.bezel_style:
            # 设置边框样式
            if self.config.bezel_style == BezelStyle.ROUNDED:
                # 圆角边框 - 使用NSTextField默认样式
                textfield.setBezeled_(True)
                # 在macOS中，默认的bezeled样式就是圆角
            elif self.config.bezel_style == BezelStyle.SQUARE:
                # 方角边框
                textfield.setBezeled_(True)
                # 可以通过cell设置更具体的样式
                cell = textfield.cell()
                if cell and hasattr(cell, 'setBorderStyle_'):
                    cell.setBorderStyle_(NSBezelBorder)
        
        # 背景配置
        textfield.setDrawsBackground_(self.config.draws_background)
        
        if self.config.background_color:
            color = self._parse_color(self.config.background_color)
            textfield.setBackgroundColor_(color)
            
            # 🔧 对于有背景色但无边框的Label，确保背景正确绘制且文本居中
            if not self.config.bordered and not self.config.editable:
                # 强制启用背景绘制
                textfield.setDrawsBackground_(True)
                # 确保没有边框
                textfield.setBezeled_(False)
                textfield.setBordered_(False)
    
    def _apply_text_config(self, textfield: NSTextField):
        """应用文本配置"""
        # 设置文本内容 - 支持富文本
        if self._is_rich_text:
            # 富文本模式
            textfield.setAttributedStringValue_(self.text)
            logger.debug(f"🎨 TextField富文本已设置: {self.text.length()} 字符")
        else:
            # 普通文本模式
            binding_cleanup = bind_text(textfield, self.text)
            if binding_cleanup:
                self._bindings.append(binding_cleanup)
                logger.debug(f"🔗 TextField响应式绑定已创建: {self.text}")
            else:
                logger.debug(f"📝 TextField静态文本已设置: {str(self.text)}")
        
        # 设置占位符
        if self.config.attributed_placeholder:
            # 富文本占位符
            textfield.setPlaceholderAttributedString_(self.config.attributed_placeholder)
            logger.debug(f"🎨 TextField富文本占位符: {self.config.attributed_placeholder.length()} 字符")
        elif self.config.placeholder:
            # 普通占位符
            textfield.setPlaceholderString_(self.config.placeholder)
            logger.debug(f"💬 TextField占位符: '{self.config.placeholder}'")
        
        # 多行文本支持判断逻辑
        # 对于Label组件，如果文本不长且有边框/背景，优先使用单行以便垂直居中
        # 但如果是真正需要多行的文本，仍然支持多行
        if not self.config.editable:
            # Label组件：默认单行以支持垂直居中，除非明确需要多行
            textfield.setUsesSingleLineMode_(True)
        else:
            # TextField组件：支持多行文本
            textfield.setUsesSingleLineMode_(False)
            textfield.setLineBreakMode_(NSLineBreakByWordWrapping)
    
    def _apply_style_config(self, textfield: NSTextField):
        """应用样式配置"""
        # 禁用自动尺寸调整
        textfield.setTranslatesAutoresizingMaskIntoConstraints_(False)
        if hasattr(textfield, 'setPreferredMaxLayoutWidth_'):
            textfield.setPreferredMaxLayoutWidth_(0)
        textfield.setAutoresizingMask_(0)
        
        # 🔧 设置文本垂直居中对齐
        cell = textfield.cell()
        if cell:
            # 去除焦点环（对所有类型都适用）
            if hasattr(cell, 'setFocusRingType_'):
                from AppKit import NSFocusRingTypeNone
                cell.setFocusRingType_(NSFocusRingTypeNone)
            
            # 设置垂直居中对齐（通过调整行高和基线）
            if hasattr(cell, 'setLineBreakMode_'):
                from AppKit import NSLineBreakByClipping
                # 对于所有Label组件（不可编辑），使用剪切模式有助于垂直居中
                if not self.config.editable:
                    cell.setLineBreakMode_(NSLineBreakByClipping)
        
        # 设置首选最大宽度以支持自动换行
        if self.style.width:
            if hasattr(self.style.width, "value"):
                width_value = self.style.width.value
                if isinstance(width_value, (int, float)):
                    textfield.setPreferredMaxLayoutWidth_(float(width_value))
        
        # 应用文本样式
        if self.text_props:
            # 设置字体
            font = self.text_props.to_nsfont()
            textfield.setFont_(font)
            
            # 设置文字颜色
            color = self.text_props.to_nscolor()
            textfield.setTextColor_(color)
            
            # 设置文本对齐
            alignment = self.text_props.get_text_alignment()
            textfield.setAlignment_(alignment)
            
            logger.debug(f"🎨 TextField样式已应用: 字体={font.fontName()}, 对齐={alignment}")
    
    def _bind_events(self, textfield: NSTextField):
        """绑定事件处理"""
        if self.config.on_text_change and self.config.editable:
            # 只有可编辑的TextField才绑定文本变化事件
            self._bind_text_change_event(textfield)
        
        if self.config.delegate:
            textfield.setDelegate_(self.config.delegate)
    
    def _bind_text_change_event(self, textfield: NSTextField):
        """绑定文本变化事件"""
        try:
            # 使用内联的TextFieldDelegate实现
            from Foundation import NSObject
            import objc
            
            class InlineTextFieldDelegate(NSObject):
                def init(self):
                    self = objc.super(InlineTextFieldDelegate, self).init()
                    if self is None:
                        return None
                    self.callback = None
                    self.textfield_component = None
                    return self
                
                def controlTextDidChange_(self, notification):
                    if hasattr(self, "callback") and self.callback:
                        try:
                            textfield = notification.object()
                            current_text = textfield.stringValue()
                            
                            # 更新组件的值
                            if hasattr(self, "textfield_component") and self.textfield_component:
                                if self.textfield_component._is_reactive_text:
                                    if hasattr(self.textfield_component.text, "value"):
                                        self.textfield_component.text.value = current_text
                                else:
                                    self.textfield_component.text = current_text
                            
                            self.callback(current_text)
                            logger.debug(f"📝 TextField文本改变: '{current_text}'")
                        
                        except Exception as e:
                            logger.error(f"⚠️ TextField文本改变回调错误: {e}")
            
            self._delegate = InlineTextFieldDelegate.alloc().init()
            self._delegate.callback = self.config.on_text_change
            self._delegate.textfield_component = self
            
            textfield.setDelegate_(self._delegate)
            logger.debug(f"🔗 TextField文本变化事件已绑定")
            
        except Exception as e:
            logger.warning(f"⚠️ TextField事件绑定失败: {e}")
    
    def _parse_color(self, color_str: str) -> NSColor:
        """解析颜色字符串为NSColor"""
        # 简单的颜色解析，支持十六进制格式
        if color_str.startswith('#'):
            hex_color = color_str[1:]
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0  
                b = int(hex_color[4:6], 16) / 255.0
                return NSColor.colorWithRed_green_blue_alpha_(r, g, b, 1.0)
        
        # 默认返回黑色
        return NSColor.blackColor()
    
    def get_text(self) -> str:
        """获取当前文本内容"""
        if self._nsview:
            return self._nsview.stringValue()
        if self._is_reactive_text:
            return str(getattr(self.text, "value", self.text))
        return str(self.text)
    
    def set_text(self, text: Union[str, Any, NSAttributedString]) -> "_BaseTextField":
        """动态设置文本内容"""
        self.text = text
        self._is_reactive_text = isinstance(text, (Signal, Computed))
        self._is_rich_text = isinstance(text, NSAttributedString)
        
        if self._nsview:
            if self._is_rich_text:
                # 富文本模式
                self._nsview.setAttributedStringValue_(text)
                logger.debug(f"🎨 TextField富文本更新: {text.length()} 字符")
            elif self._is_reactive_text:
                content = str(getattr(text, "value", text))
                self._nsview.setStringValue_(content)
                logger.debug(f"📝 TextField响应式文本更新: '{content}'")
            else:
                content = str(text)
                self._nsview.setStringValue_(content)
                logger.debug(f"📝 TextField文本更新: '{content}'")
        
        return self