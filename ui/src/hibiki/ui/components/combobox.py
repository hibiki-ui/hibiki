#!/usr/bin/env python3
"""
Hibiki UI v4.0 - ComboBox组件
组合框组件，支持文本输入和下拉选择
"""

from typing import Optional, List, Union, Callable
from AppKit import NSView, NSComboBox, NSMakeRect
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Effect
from ..core.logging import get_logger

logger = get_logger("components.combobox")
logger.setLevel("INFO")


class ComboBoxDelegate(NSObject):
    """ComboBox文本变化和选择事件委托类"""
    
    def init(self):
        self = objc.super(ComboBoxDelegate, self).init()
        if self is None:
            return None
        self.text_callback = None
        self.selection_callback = None
        self.combo_component = None
        return self
    
    def comboBoxSelectionDidChange_(self, notification):
        """下拉选择变化事件处理"""
        if hasattr(self, "selection_callback") and self.selection_callback:
            try:
                combo_box = notification.object()
                selected_index = combo_box.indexOfSelectedItem()
                selected_value = combo_box.stringValue()
                
                # 更新组件的选中值
                if hasattr(self, "combo_component") and self.combo_component:
                    if self.combo_component._is_reactive_text:
                        if hasattr(self.combo_component.text, "value"):
                            self.combo_component.text.value = selected_value
                    else:
                        self.combo_component.text = selected_value
                
                self.selection_callback(selected_index, selected_value)
                logger.debug(f"📝 ComboBox选择: index={selected_index}, value='{selected_value}'")
            
            except Exception as e:
                logger.error(f"⚠️ ComboBox选择回调错误: {e}")
    
    def controlTextDidChange_(self, notification):
        """文本输入变化事件处理"""
        if hasattr(self, "text_callback") and self.text_callback:
            try:
                combo_box = notification.object()
                current_text = combo_box.stringValue()
                
                # 更新组件的文本值
                if hasattr(self, "combo_component") and self.combo_component:
                    if self.combo_component._is_reactive_text:
                        if hasattr(self.combo_component.text, "value"):
                            self.combo_component.text.value = current_text
                    else:
                        self.combo_component.text = current_text
                
                self.text_callback(current_text)
                logger.debug(f"📝 ComboBox文本变化: '{current_text}'")
            
            except Exception as e:
                logger.error(f"⚠️ ComboBox文本变化回调错误: {e}")


class ComboBox(UIComponent):
    """组合框组件 - 基于NSComboBox"""
    
    def __init__(
        self,
        items: List[str] = None,
        text: Union[str, "Signal"] = "",
        editable: bool = True,
        on_text_change: Optional[Callable[[str], None]] = None,
        on_selection: Optional[Callable[[int, str], None]] = None,
        style: Optional[ComponentStyle] = None,
    ):
        """初始化组合框组件
        
        Args:
            items: 下拉选项列表
            text: 当前文本内容
            editable: 是否可编辑
            on_text_change: 文本变化回调函数
            on_selection: 选择回调函数
            style: 组件样式
        """
        super().__init__(style)
        self.items = items or ["选项A", "选项B", "选项C"]
        
        # 处理响应式文本
        if hasattr(text, "value"):
            self._is_reactive_text = True
            self.text = text
        else:
            self._is_reactive_text = False
            self.text = text
        
        self.editable = editable
        self.on_text_change = on_text_change
        self.on_selection = on_selection
        self._combo_box = None
        self._target_delegate = None
        
        logger.debug(f"📝 ComboBox组件创建: items={len(self.items)}, text='{self._get_text()}'")
    
    def _get_text(self) -> str:
        """获取当前文本"""
        if self._is_reactive_text:
            return self.text.value if hasattr(self.text, "value") else ""
        return self.text
    
    def _create_nsview(self) -> NSView:
        """创建NSComboBox"""
        # 创建组合框
        combo_box = NSComboBox.alloc().initWithFrame_(NSMakeRect(0, 0, 150, 26))
        
        # 添加选项
        for item in self.items:
            combo_box.addItemWithObjectValue_(item)
        
        # 设置初始文本
        combo_box.setStringValue_(self._get_text())
        
        # 设置是否可编辑
        combo_box.setEditable_(self.editable)
        
        self._combo_box = combo_box
        
        # 绑定事件
        if self.on_text_change or self.on_selection:
            self._bind_events(combo_box)
        
        # 建立响应式绑定
        if self._is_reactive_text:
            self._bind_reactive_text()
        
        logger.debug(f"📝 ComboBox NSComboBox创建完成")
        return combo_box
    
    def _bind_events(self, combo_box: NSComboBox):
        """绑定事件"""
        try:
            # 创建委托
            self._target_delegate = ComboBoxDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建ComboBoxDelegate")
                return
            
            self._target_delegate.text_callback = self.on_text_change
            self._target_delegate.selection_callback = self.on_selection
            self._target_delegate.combo_component = self
            
            # 设置委托
            combo_box.setDelegate_(self._target_delegate)
            
            logger.debug(f"🔗 ComboBox事件已绑定")
        
        except Exception as e:
            logger.warning(f"⚠️ ComboBox事件绑定失败: {e}")
    
    def _bind_reactive_text(self):
        """建立文本的响应式绑定"""
        if not hasattr(self.text, "value"):
            return
        
        def update_text():
            if self._combo_box:
                new_text = self.text.value
                self._combo_box.setStringValue_(new_text)
                logger.debug(f"📝 ComboBox文本更新: '{new_text}'")
        
        # 使用Effect建立响应式绑定
        self._text_effect = Effect(update_text)
    
    def add_item(self, item: str) -> "ComboBox":
        """添加选项
        
        Args:
            item: 选项文本
        """
        self.items.append(item)
        
        if self._combo_box:
            self._combo_box.addItemWithObjectValue_(item)
        
        logger.debug(f"📝 ComboBox添加选项: '{item}'")
        return self
    
    def remove_item(self, item: str) -> "ComboBox":
        """移除选项
        
        Args:
            item: 要移除的选项文本
        """
        if item in self.items:
            self.items.remove(item)
            
            if self._combo_box:
                self._combo_box.removeItemWithObjectValue_(item)
            
            logger.debug(f"📝 ComboBox移除选项: '{item}'")
        
        return self
    
    def set_text(self, text: str) -> "ComboBox":
        """设置文本内容
        
        Args:
            text: 新的文本内容
        """
        if self._is_reactive_text:
            self.text.value = text
        else:
            self.text = text
            if self._combo_box:
                self._combo_box.setStringValue_(text)
        
        logger.debug(f"📝 ComboBox文本设置: '{text}'")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, "_text_effect"):
            self._text_effect.cleanup()
        super().cleanup()