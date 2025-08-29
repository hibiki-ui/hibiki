#!/usr/bin/env python3
"""
🖼️ 简单的图片容器组件

直接使用 NSImageView 显示图片的简单包装
"""

import os
from typing import Optional
from hibiki.ui import UIComponent, ComponentStyle, px
from AppKit import NSImageView, NSImage, NSImageScaleProportionallyUpOrDown
from Foundation import NSMakeRect
from hibiki.ui.core.logging import get_logger

logger = get_logger("ui.image_container")

class SimpleImageContainer(UIComponent):
    """简单的图片容器"""
    
    def __init__(
        self, 
        image_path: Optional[str] = None,
        width: int = 120,
        height: int = 120,
        style: Optional[ComponentStyle] = None
    ):
        super().__init__(style or ComponentStyle(width=px(width), height=px(height)))
        self.image_path = image_path
        self.width = width
        self.height = height
        
    def _create_nsview(self):
        """创建并返回 NSImageView - 实现抽象方法"""
        try:
            # 创建 NSImageView
            image_view = NSImageView.alloc().initWithFrame_(
                NSMakeRect(0, 0, self.width, self.height)
            )
            
            # 如果有图片路径且文件存在，加载图片
            if self.image_path and os.path.exists(self.image_path):
                ns_image = NSImage.alloc().initWithContentsOfFile_(self.image_path)
                if ns_image:
                    image_view.setImage_(ns_image)
                    image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
                    logger.info(f"✅ 成功加载图片: {os.path.basename(self.image_path)}")
                else:
                    logger.warning(f"⚠️ 图片加载失败: {self.image_path}")
            else:
                logger.debug(f"🖼️ 创建空图片容器: {self.width}x{self.height}")
            
            # 设置图片视图属性
            image_view.setImageFrameStyle_(0)  # NSImageFrameNone
            image_view.setEditable_(False)
            
            return image_view
            
        except Exception as e:
            logger.error(f"❌ 创建图片容器失败: {e}")
            # 返回空的 NSView 作为备用
            from AppKit import NSView
            return NSView.alloc().initWithFrame_(NSMakeRect(0, 0, self.width, self.height))

def create_album_art_view(image_path: str, size: int = 120) -> SimpleImageContainer:
    """创建专辑封面视图的便捷函数"""
    return SimpleImageContainer(image_path=image_path, width=size, height=size)

def create_button_icon_view(image_path: str, size: int = 48) -> SimpleImageContainer:
    """创建按钮图标视图的便捷函数"""
    return SimpleImageContainer(image_path=image_path, width=size, height=size)