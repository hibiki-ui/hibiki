#!/usr/bin/env python3
"""
Hibiki UI基础视图类
================

提供统一的坐标系和基础功能，所有Hibiki UI组件都应该继承自HibikiBaseView。

主要特性：
- 统一使用top-left坐标系（与现代UI框架一致）
- 为调试和开发提供便利方法
- 优化的PyObjC集成
"""

from AppKit import NSView
from hibiki.ui.core.logging import get_logger

logger = get_logger("base_view")


class HibikiBaseView(NSView):
    """
    Hibiki UI框架的基础视图类
    
    所有Hibiki UI组件的NSView都应该继承自这个类，而不是直接继承NSView。
    这确保了框架内部的一致性和统一的坐标系。
    """
    
    def isFlipped(self) -> bool:
        """
        启用翻转坐标系，使用top-left原点
        
        这使得Hibiki UI与现代UI框架（React, SwiftUI, CSS等）
        保持一致的坐标系习惯：
        
        - 原点在左上角 (0, 0)  
        - X轴向右递增
        - Y轴向下递增
        
        这与macOS原生的bottom-left坐标系不同，但更符合
        大多数开发者的直觉和现代UI开发习惯。
        
        Returns:
            bool: 始终返回True，启用top-left坐标系
        """
        return True
    
    def viewDidMoveToSuperview(self):
        """
        视图添加到父视图时的回调
        
        可以在子类中重写此方法来执行初始化逻辑。
        """
        # 调试日志（仅在DEBUG模式下）
        if logger.isEnabledFor(10):  # DEBUG level
            superview_class = self.superview().__class__.__name__ if self.superview() else "None"
            logger.debug(f"🔗 {self.__class__.__name__} added to superview: {superview_class}")
    
    def viewWillMoveToSuperview_(self, newSuperview):
        """
        视图即将移动到新的父视图时的回调
        
        Args:
            newSuperview: 新的父视图，可能为None（表示从视图层级中移除）
        """
        # 调试日志
        if logger.isEnabledFor(10):  # DEBUG level
            new_superview_class = newSuperview.__class__.__name__ if newSuperview else "None"
            logger.debug(f"🔄 {self.__class__.__name__} moving to superview: {new_superview_class}")
    
    def removeFromSuperview(self):
        """
        从父视图中移除
        
        提供额外的清理逻辑。
        """
        if logger.isEnabledFor(10):  # DEBUG level
            logger.debug(f"❌ {self.__class__.__name__} removing from superview")
        
        # 需要调用父类方法，但在PyObjC中需要特殊处理
    
    def describeBounds(self) -> str:
        """
        获取边界的描述字符串，用于调试
        
        Returns:
            str: 边界描述，格式为 "WxH @ (X, Y)"
        """
        bounds = self.bounds()
        return f"{bounds.size.width:.1f}x{bounds.size.height:.1f} @ ({bounds.origin.x:.1f}, {bounds.origin.y:.1f})"
    
    def describeFrame(self) -> str:
        """
        获取框架的描述字符串，用于调试
        
        Returns:
            str: 框架描述，格式为 "WxH @ (X, Y)"
        """
        frame = self.frame()
        return f"{frame.size.width:.1f}x{frame.size.height:.1f} @ ({frame.origin.x:.1f}, {frame.origin.y:.1f})"


class HibikiContainerView(HibikiBaseView):
    """
    容器视图的基类
    
    用于包含其他子视图的容器组件。提供了额外的
    子视图管理功能和调试支持。
    """
    
    def addSubview_(self, view):
        """
        添加子视图
        
        Args:
            view: 要添加的子视图
        """
        NSView.addSubview_(self, view)  # 直接调用NSView方法
        
        if logger.isEnabledFor(10):  # DEBUG level
            logger.debug(f"➕ {self.__class__.__name__} added subview: {view.__class__.__name__}")
    
    def willRemoveSubview_(self, view):
        """
        即将移除子视图时的回调
        
        Args:
            view: 即将移除的子视图
        """
        if logger.isEnabledFor(10):  # DEBUG level
            logger.debug(f"➖ {self.__class__.__name__} removing subview: {view.__class__.__name__}")
    
    def describeSubviews(self) -> str:
        """
        获取所有子视图的描述
        
        Returns:
            str: 子视图描述字符串
        """
        subviews = self.subviews()
        if not subviews:
            return "No subviews"
        
        descriptions = []
        for i, subview in enumerate(subviews):
            subview_class = subview.__class__.__name__
            if hasattr(subview, 'describeBounds'):
                bounds_desc = subview.describeBounds()
            else:
                bounds = subview.bounds()
                bounds_desc = f"{bounds.size.width:.1f}x{bounds.size.height:.1f}"
            descriptions.append(f"  [{i}] {subview_class}: {bounds_desc}")
        
        return f"{len(subviews)} subviews:\n" + "\n".join(descriptions)


def create_hibiki_view() -> HibikiBaseView:
    """
    创建基础Hibiki视图的工厂函数
    
    Returns:
        HibikiBaseView: 新创建的基础视图实例
    """
    return HibikiBaseView.alloc().init()


def create_hibiki_container() -> HibikiContainerView:
    """
    创建Hibiki容器视图的工厂函数
    
    Returns:
        HibikiContainerView: 新创建的容器视图实例
    """
    return HibikiContainerView.alloc().init()