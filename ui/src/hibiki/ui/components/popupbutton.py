#!/usr/bin/env python3
"""
Hibiki UI v4.0 - PopUpButton组件
下拉按钮组件，支持选项选择和响应式绑定
"""

from typing import Optional, List, Union, Callable
from AppKit import NSView, NSPopUpButton, NSMakeRect
from Foundation import NSObject
import objc

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.reactive import Signal, Effect
from ..core.logging import get_logger

logger = get_logger("components.popupbutton")
logger.setLevel("INFO")


class PopUpButtonDelegate(NSObject):
    """PopUpButton选择事件委托类"""
    
    def init(self):
        self = objc.super(PopUpButtonDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        self.popup_component = None
        return self
    
    def itemSelected_(self, sender):
        """下拉选择项被选中事件处理"""
        if hasattr(self, "callback") and self.callback:
            try:
                # 获取选中的索引和标题
                selected_index = sender.indexOfSelectedItem()
                selected_title = sender.titleOfSelectedItem()
                
                # 更新组件的选中值
                if hasattr(self, "popup_component") and self.popup_component:
                    if self.popup_component._is_reactive_selected:
                        if hasattr(self.popup_component.selected_index, "value"):
                            self.popup_component.selected_index.value = selected_index
                    else:
                        self.popup_component.selected_index = selected_index
                
                # 调用回调函数
                self.callback(selected_index, selected_title)
                logger.debug(
                    f"🔽 PopUpButton选择: index={selected_index}, title='{selected_title}'"
                )
            
            except Exception as e:
                logger.error(f"⚠️ PopUpButton选择回调错误: {e}")


class PopUpButton(UIComponent):
    """下拉按钮组件 - 基于NSPopUpButton"""
    
    def __init__(
        self,
        items: List[str] = None,
        selected_index: Union[int, "Signal"] = 0,
        on_selection: Optional[Callable[[int, str], None]] = None,
        style: Optional[ComponentStyle] = None,
    ):
        """初始化下拉按钮组件
        
        Args:
            items: 下拉选项列表
            selected_index: 默认选中的索引
            on_selection: 选择回调函数 (index, title) -> None
            style: 组件样式
        """
        super().__init__(style)
        self.items = items or ["选项1", "选项2", "选项3"]
        
        # 处理响应式选中索引
        if hasattr(selected_index, "value"):
            self._is_reactive_selected = True
            self.selected_index = selected_index
        else:
            self._is_reactive_selected = False
            self.selected_index = selected_index
        
        self.on_selection = on_selection
        self._popup_button = None
        self._target_delegate = None
        
        logger.debug(
            f"🔽 PopUpButton组件创建: items={len(self.items)}, selected={self._get_selected_index()}"
        )
    
    def _get_selected_index(self) -> int:
        """获取当前选中索引"""
        if self._is_reactive_selected:
            return self.selected_index.value if hasattr(self.selected_index, "value") else 0
        return self.selected_index
    
    def _create_nsview(self) -> NSView:
        """创建NSPopUpButton"""
        # 创建下拉按钮
        popup_button = NSPopUpButton.alloc().initWithFrame_pullsDown_(
            NSMakeRect(0, 0, 150, 26), False
        )
        
        # 添加选项
        for item in self.items:
            popup_button.addItemWithTitle_(item)
        
        # 设置默认选中项
        selected = self._get_selected_index()
        if 0 <= selected < len(self.items):
            popup_button.selectItemAtIndex_(selected)
        
        self._popup_button = popup_button
        
        # 绑定选择事件
        if self.on_selection:
            self._bind_selection_event(popup_button)
        
        # 建立响应式绑定
        if self._is_reactive_selected:
            self._bind_reactive_selection()
        
        logger.debug(f"🔽 PopUpButton NSPopUpButton创建完成")
        return popup_button
    
    def _bind_selection_event(self, popup_button: NSPopUpButton):
        """绑定选择事件"""
        try:
            # 创建委托
            self._target_delegate = PopUpButtonDelegate.alloc().init()
            if self._target_delegate is None:
                logger.warning("⚠️ 无法创建PopUpButtonDelegate")
                return
            
            self._target_delegate.callback = self.on_selection
            self._target_delegate.popup_component = self
            
            popup_button.setTarget_(self._target_delegate)
            popup_button.setAction_("itemSelected:")
            
            logger.debug(f"🔗 PopUpButton选择事件已绑定")
        
        except Exception as e:
            logger.warning(f"⚠️ PopUpButton事件绑定失败: {e}")
    
    def _bind_reactive_selection(self):
        """建立选中索引的响应式绑定"""
        if not hasattr(self.selected_index, "value"):
            return
        
        def update_selection():
            if self._popup_button:
                new_index = self.selected_index.value
                if 0 <= new_index < len(self.items):
                    self._popup_button.selectItemAtIndex_(new_index)
                    logger.debug(f"🔽 PopUpButton选中更新: index={new_index}")
        
        # 使用Effect建立响应式绑定
        self._selection_effect = Effect(update_selection)
    
    def add_item(self, item: str, at_index: int = -1) -> "PopUpButton":
        """添加选项
        
        Args:
            item: 选项文本
            at_index: 插入位置，-1表示末尾
        """
        if at_index == -1:
            self.items.append(item)
        else:
            self.items.insert(at_index, item)
        
        if self._popup_button:
            if at_index == -1:
                self._popup_button.addItemWithTitle_(item)
            else:
                self._popup_button.insertItemWithTitle_atIndex_(item, at_index)
        
        logger.debug(
            f"🔽 PopUpButton添加选项: '{item}' at {at_index if at_index != -1 else len(self.items)-1}"
        )
        return self
    
    def remove_item(self, index: int) -> "PopUpButton":
        """移除选项
        
        Args:
            index: 要移除的索引
        """
        if 0 <= index < len(self.items):
            removed_item = self.items.pop(index)
            
            if self._popup_button:
                self._popup_button.removeItemAtIndex_(index)
            
            logger.debug(f"🔽 PopUpButton移除选项: '{removed_item}' at {index}")
        
        return self
    
    def set_selected_index(self, index: int) -> "PopUpButton":
        """设置选中索引
        
        Args:
            index: 要选中的索引
        """
        if self._is_reactive_selected:
            self.selected_index.value = index
        else:
            self.selected_index = index
            if self._popup_button and 0 <= index < len(self.items):
                self._popup_button.selectItemAtIndex_(index)
        
        logger.debug(f"🔽 PopUpButton选中设置: index={index}")
        return self
    
    def cleanup(self):
        """组件清理"""
        if hasattr(self, "_selection_effect"):
            self._selection_effect.cleanup()
        super().cleanup()