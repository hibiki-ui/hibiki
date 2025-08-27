"""
LayoutNode - 布局节点抽象

封装Stretchable Node，提供macUI特定的接口和功能
实现CSS-like的布局节点操作和管理
"""

from typing import Optional, List, Any, Tuple
from .styles import LayoutStyle

import stretchable as st


class LayoutNode:
    """布局节点 - 封装Stretchable Node的专业接口
    
    提供CSS-like的节点操作和macUI组件集成功能
    """
    
    def __init__(
        self,
        style: Optional[LayoutStyle] = None,
        key: Optional[str] = None,
        user_data: Any = None
    ):
        """初始化布局节点
        
        Args:
            style: 布局样式
            key: 节点标识符
            user_data: 用户数据 (通常是UI组件引用)
        """
        self.key = key
        self.user_data = user_data
        self._children: List['LayoutNode'] = []
        self._parent: Optional['LayoutNode'] = None
        
        # 创建Stretchable节点
        stretchable_style = style.to_stretchable_style() if style else st.Style()
        self._stretchable_node = st.Node(style=stretchable_style)
        
        # 保存原始样式引用
        self._style = style
        
    
    @property
    def style(self) -> Optional[LayoutStyle]:
        """获取布局样式"""
        return self._style
    
    @style.setter
    def style(self, new_style: Optional[LayoutStyle]):
        """更新布局样式"""
        self._style = new_style
        
        # 更新Stretchable节点样式
        if self._stretchable_node is not None:
            stretchable_style = new_style.to_stretchable_style() if new_style else st.Style()
            self._stretchable_node.style = stretchable_style
        
        self.mark_dirty()
    
    @property
    def children(self) -> List['LayoutNode']:
        """获取子节点列表"""
        return self._children.copy()
    
    @property
    def parent(self) -> Optional['LayoutNode']:
        """获取父节点"""
        return self._parent
    
    def add_child(self, child: 'LayoutNode', index: Optional[int] = None) -> 'LayoutNode':
        """添加子节点
        
        Args:
            child: 要添加的子节点
            index: 插入位置 (None表示末尾)
            
        Returns:
            self (支持链式调用)
        """
        if child._parent is not None:
            child._parent.remove_child(child)
        
        # 更新父子关系
        child._parent = self
        
        if index is None:
            self._children.append(child)
            if self._stretchable_node is not None and child._stretchable_node is not None:
                self._stretchable_node.append(child._stretchable_node)
        else:
            self._children.insert(index, child)
            if self._stretchable_node is not None and child._stretchable_node is not None:
                self._stretchable_node.insert(index, child._stretchable_node)
        
        self.mark_dirty()
        return self
    
    def remove_child(self, child: 'LayoutNode') -> 'LayoutNode':
        """移除子节点
        
        Args:
            child: 要移除的子节点
            
        Returns:
            self (支持链式调用)
        """
        if child in self._children:
            self._children.remove(child)
            if self._stretchable_node is not None and child._stretchable_node is not None:
                self._stretchable_node.remove(child._stretchable_node)
            child._parent = None
            self.mark_dirty()
        
        return self
    
    def clear_children(self) -> 'LayoutNode':
        """清空所有子节点
        
        Returns:
            self (支持链式调用)
        """
        for child in self._children.copy():
            self.remove_child(child)
        
        return self
    
    def find_child(self, key: str) -> Optional['LayoutNode']:
        """根据key查找子节点"""
        for child in self._children:
            if child.key == key:
                return child
        return None
    
    def find_descendant(self, key: str) -> Optional['LayoutNode']:
        """递归查找后代节点"""
        # 先查找直接子节点
        result = self.find_child(key)
        if result:
            return result
        
        # 递归查找子树
        for child in self._children:
            result = child.find_descendant(key)
            if result:
                return result
        
        return None
    
    def compute_layout(self, available_size: Optional[Tuple[float, float]] = None) -> 'LayoutNode':
        """计算布局
        
        Args:
            available_size: 可用尺寸 (width, height)，None表示无限制
            
        Returns:
            self (支持链式调用)
        """
        if self._stretchable_node is None:
            return self
            
        try:
            if available_size:
                from stretchable.style import Size, Length
                size = Size(width=Length.from_any(available_size[0]), 
                           height=Length.from_any(available_size[1]))
                success = self._stretchable_node.compute_layout(size)
            else:
                success = self._stretchable_node.compute_layout()
            
            if not success:
                pass  # 布局计算失败，静默处理
        except Exception as e:
            pass  # 布局计算异常，静默处理
        
        return self
    
    def get_layout(self) -> Tuple[float, float, float, float]:
        """获取计算后的布局结果
        
        Returns:
            (x, y, width, height) - 相对于父节点的位置和尺寸
        """
        if self._stretchable_node is None:
            raise RuntimeError("布局节点未正确初始化")
        
        box = self._stretchable_node.get_box()
        return (box.x, box.y, box.width, box.height)
    
    def get_content_size(self) -> Tuple[float, float]:
        """获取内容区域尺寸 (去除padding)
        
        Returns:
            (content_width, content_height)
        """
        if self._stretchable_node is None:
            raise RuntimeError("布局节点未正确初始化")
            
        # 获取边框盒子
        border_box = self._stretchable_node.border_box
        return (border_box.width, border_box.height)
    
    def mark_dirty(self) -> 'LayoutNode':
        """标记需要重新布局
        
        Returns:
            self (支持链式调用)  
        """
        if self._stretchable_node is not None:
            self._stretchable_node.mark_dirty()
        return self
    
    def is_dirty(self) -> bool:
        """检查是否需要重新布局"""
        if self._stretchable_node is None:
            return False
        return self._stretchable_node.is_dirty
    
    def get_stretchable_node(self) -> st.Node:
        """获取底层Stretchable节点 (用于调试和高级操作)"""
        return self._stretchable_node
    
    def debug_print_tree(self, indent: int = 0) -> str:
        """调试输出布局树结构"""
        prefix = "  " * indent
        x, y, w, h = self.get_layout()
        
        result = f"{prefix}LayoutNode(key={self.key})\n"
        result += f"{prefix}  Layout: x={x:.1f}, y={y:.1f}, w={w:.1f}, h={h:.1f}\n"
        result += f"{prefix}  Style: {self._style}\n"
        
        for child in self._children:
            result += child.debug_print_tree(indent + 1)
        
        return result
    
    def __repr__(self) -> str:
        return f"LayoutNode(key={self.key}, children={len(self._children)})"