#!/usr/bin/env python3
"""
Hibiki UI v4.0 - ImageView组件
图像显示组件，支持多种缩放模式和图像加载
"""

from typing import Optional
from AppKit import (
    NSView, NSImageView, NSImage, NSMakeRect,
    NSImageScaleProportionallyUpOrDown, NSImageScaleAxesIndependently, NSImageScaleNone
)

from ..core.component import UIComponent
from ..core.styles import ComponentStyle
from ..core.logging import get_logger

logger = get_logger("components.imageview")
logger.setLevel("INFO")


class ImageView(UIComponent):
    """图像显示组件 - 基于NSImageView"""
    
    def __init__(
        self,
        image_path: Optional[str] = None,
        image_name: Optional[str] = None,
        style: Optional[ComponentStyle] = None,
        scaling: str = "proportionally",
    ):
        """初始化图像视图组件
        
        Args:
            image_path: 图像文件路径
            image_name: 图像资源名称（从应用包中加载）
            style: 组件样式
            scaling: 图像缩放模式 ("proportionally", "axesIndependently", "none")
        """
        super().__init__(style)
        self.image_path = image_path
        self.image_name = image_name
        self.scaling = scaling
        self._image_view = None
        
        logger.debug(f"🖼️ ImageView组件创建: path={image_path}, name={image_name}")
    
    def _create_nsview(self) -> NSView:
        """创建NSImageView"""
        # 创建图像视图
        image_view = NSImageView.alloc().initWithFrame_(NSMakeRect(0, 0, 100, 100))
        
        # 设置缩放模式
        if self.scaling == "proportionally":
            image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
        elif self.scaling == "axesIndependently":
            image_view.setImageScaling_(NSImageScaleAxesIndependently)
        else:  # "none"
            image_view.setImageScaling_(NSImageScaleNone)
        
        # 加载图像
        if self.image_path:
            self._load_image_from_path(image_view, self.image_path)
        elif self.image_name:
            self._load_image_from_name(image_view, self.image_name)
        
        self._image_view = image_view
        
        logger.debug(f"🖼️ ImageView NSImageView创建完成")
        return image_view
    
    def _load_image_from_path(self, image_view: NSImageView, path: str):
        """从文件路径加载图像"""
        try:
            image = NSImage.alloc().initWithContentsOfFile_(path)
            if image:
                image_view.setImage_(image)
                logger.debug(f"📁 图像加载成功: {path}")
            else:
                logger.warning(f"⚠️ 图像加载失败: {path}")
        except Exception as e:
            logger.error(f"❌ 图像加载异常: {e}")
    
    def _load_image_from_name(self, image_view: NSImageView, name: str):
        """从应用包资源加载图像"""
        try:
            image = NSImage.imageNamed_(name)
            if image:
                image_view.setImage_(image)
                logger.debug(f"📦 系统图像加载成功: {name}")
            else:
                logger.warning(f"⚠️ 系统图像加载失败: {name}")
        except Exception as e:
            logger.error(f"❌ 系统图像加载异常: {e}")
    
    def set_image_path(self, path: str) -> "ImageView":
        """设置图像文件路径
        
        Args:
            path: 图像文件路径
        """
        self.image_path = path
        
        if self._image_view:
            self._load_image_from_path(self._image_view, path)
        
        logger.debug(f"🖼️ ImageView图像路径更新: {path}")
        return self
    
    def set_image_name(self, name: str) -> "ImageView":
        """设置系统图像名称
        
        Args:
            name: 系统图像名称
        """
        self.image_name = name
        
        if self._image_view:
            self._load_image_from_name(self._image_view, name)
        
        logger.debug(f"🖼️ ImageView图像名称更新: {name}")
        return self
    
    def set_scaling(self, scaling: str) -> "ImageView":
        """设置图像缩放模式
        
        Args:
            scaling: 缩放模式 ("proportionally", "axesIndependently", "none")
        """
        self.scaling = scaling
        
        if self._image_view:
            if scaling == "proportionally":
                self._image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
            elif scaling == "axesIndependently":
                self._image_view.setImageScaling_(NSImageScaleAxesIndependently)
            else:  # "none"
                self._image_view.setImageScaling_(NSImageScaleNone)
        
        logger.debug(f"🖼️ ImageView缩放模式更新: {scaling}")
        return self