"""
LayoutTree - 布局树管理

提供布局树的构建、管理和维护功能
支持动态更新、批量操作和调试功能
"""

from typing import Dict, List, Optional, Any, Callable, Set
from .node import LayoutNode
from .styles import LayoutStyle
from .engine import LayoutEngine, LayoutResult


class LayoutTree:
    """布局树管理器
    
    负责管理完整的布局树结构，提供高级操作和维护功能
    """
    
    def __init__(self, root: Optional[LayoutNode] = None, engine: Optional[LayoutEngine] = None):
        """初始化布局树
        
        Args:
            root: 根节点
            engine: 布局引擎实例
        """
        self.root = root
        self.engine = engine or LayoutEngine()
        
        # 节点索引 - 用于快速查找
        self._node_index: Dict[str, LayoutNode] = {}
        self._rebuild_index()
        
        # 变更监听
        self._change_listeners: List[Callable[['LayoutTree'], None]] = []
        
        # 脏节点追踪
        self._dirty_nodes: Set[LayoutNode] = set()
    
    def set_root(self, root: LayoutNode) -> 'LayoutTree':
        """设置根节点
        
        Args:
            root: 新的根节点
            
        Returns:
            self (支持链式调用)
        """
        self.root = root
        self._rebuild_index()
        self._notify_change()
        return self
    
    def create_node(
        self,
        key: str,
        style: Optional[LayoutStyle] = None,
        user_data: Any = None
    ) -> LayoutNode:
        """创建并注册新节点
        
        Args:
            key: 节点标识符
            style: 布局样式
            user_data: 用户数据
            
        Returns:
            新创建的布局节点
        """
        node = LayoutNode(style=style, key=key, user_data=user_data)
        if key:
            self._node_index[key] = node
        return node
    
    def find_node(self, key: str) -> Optional[LayoutNode]:
        """根据key查找节点"""
        return self._node_index.get(key)
    
    def add_node(self, parent_key: str, child: LayoutNode, index: Optional[int] = None) -> bool:
        """添加节点到指定父节点
        
        Args:
            parent_key: 父节点key
            child: 子节点
            index: 插入位置
            
        Returns:
            操作是否成功
        """
        parent = self.find_node(parent_key)
        if not parent:
            return False
        
        parent.add_child(child, index)
        
        # 更新索引
        if child.key:
            self._node_index[child.key] = child
        
        # 递归索引子节点
        self._index_subtree(child)
        
        self._mark_dirty(parent)
        self._notify_change()
        
        return True
    
    def remove_node(self, key: str) -> bool:
        """移除节点
        
        Args:
            key: 要移除的节点key
            
        Returns:
            操作是否成功
        """
        node = self.find_node(key)
        if not node or not node.parent:
            return False
        
        parent = node.parent
        parent.remove_child(node)
        
        # 移除索引
        self._remove_from_index(node)
        
        self._mark_dirty(parent)
        self._notify_change()
        
        return True
    
    def move_node(self, key: str, new_parent_key: str, index: Optional[int] = None) -> bool:
        """移动节点到新父节点
        
        Args:
            key: 要移动的节点key
            new_parent_key: 新父节点key
            index: 插入位置
            
        Returns:
            操作是否成功
        """
        node = self.find_node(key)
        new_parent = self.find_node(new_parent_key)
        
        if not node or not new_parent:
            return False
        
        # 移除原位置
        if node.parent:
            node.parent.remove_child(node)
        
        # 添加到新位置
        new_parent.add_child(node, index)
        
        self._mark_dirty(new_parent)
        self._notify_change()
        
        return True
    
    def update_node_style(self, key: str, style: LayoutStyle) -> bool:
        """更新节点样式
        
        Args:
            key: 节点key
            style: 新样式
            
        Returns:
            操作是否成功
        """
        node = self.find_node(key)
        if not node:
            return False
        
        node.style = style
        self._mark_dirty(node)
        self._notify_change()
        
        return True
    
    def compute_layout(self, available_size: Optional[tuple] = None) -> Optional[LayoutResult]:
        """计算整个树的布局
        
        Args:
            available_size: 可用尺寸约束
            
        Returns:
            根节点的布局结果
        """
        if not self.root:
            return None
        
        result = self.engine.compute_layout(self.root, available_size)
        
        # 清空脏节点标记
        self._dirty_nodes.clear()
        
        return result
    
    def get_layout_info(self, key: str) -> Optional[tuple]:
        """获取节点布局信息
        
        Args:
            key: 节点key
            
        Returns:
            (x, y, width, height) 或 None
        """
        node = self.find_node(key)
        if not node:
            return None
        
        return node.get_layout()
    
    def batch_update_styles(self, updates: Dict[str, LayoutStyle]) -> int:
        """批量更新节点样式
        
        Args:
            updates: key -> style 的映射
            
        Returns:
            成功更新的节点数量
        """
        success_count = 0
        
        for key, style in updates.items():
            if self.update_node_style(key, style):
                success_count += 1
        
        return success_count
    
    def mark_subtree_dirty(self, key: str) -> bool:
        """标记子树为脏状态
        
        Args:
            key: 子树根节点key
            
        Returns:
            操作是否成功
        """
        node = self.find_node(key)
        if not node:
            return False
        
        def mark_recursive(n: LayoutNode):
            n.mark_dirty()
            self._dirty_nodes.add(n)
            for child in n.children:
                mark_recursive(child)
        
        mark_recursive(node)
        return True
    
    def get_dirty_nodes(self) -> List[LayoutNode]:
        """获取所有脏节点"""
        return list(self._dirty_nodes)
    
    def add_change_listener(self, listener: Callable[['LayoutTree'], None]):
        """添加变更监听器"""
        self._change_listeners.append(listener)
    
    def remove_change_listener(self, listener: Callable[['LayoutTree'], None]):
        """移除变更监听器"""
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)
    
    def debug_print_tree(self) -> str:
        """调试输出整个布局树"""
        if not self.root:
            return "Empty LayoutTree"
        
        result = "=== Layout Tree Debug ===\n"
        result += self.root.debug_print_tree()
        result += f"=== Index: {len(self._node_index)} nodes ===\n"
        result += f"=== Dirty: {len(self._dirty_nodes)} nodes ===\n"
        
        return result
    
    def debug_print_metrics(self):
        """调试输出性能指标"""
        self.engine.debug_print_metrics()
    
    def _rebuild_index(self):
        """重建节点索引"""
        self._node_index.clear()
        if self.root:
            self._index_subtree(self.root)
    
    def _index_subtree(self, node: LayoutNode):
        """索引子树"""
        if node.key:
            self._node_index[node.key] = node
        
        for child in node.children:
            self._index_subtree(child)
    
    def _remove_from_index(self, node: LayoutNode):
        """从索引中移除节点及其子树"""
        if node.key and node.key in self._node_index:
            del self._node_index[node.key]
        
        for child in node.children:
            self._remove_from_index(child)
    
    def _mark_dirty(self, node: LayoutNode):
        """标记节点为脏状态"""
        node.mark_dirty()
        self._dirty_nodes.add(node)
    
    def _notify_change(self):
        """通知变更监听器"""
        for listener in self._change_listeners:
            try:
                listener(self)
            except Exception as e:
                print(f"⚠️ 布局树变更监听器错误: {e}")


# 便捷构建器
class LayoutTreeBuilder:
    """布局树构建器 - 提供流畅的API来构建布局树"""
    
    def __init__(self, engine: Optional[LayoutEngine] = None):
        self.engine = engine or LayoutEngine()
        self.tree = LayoutTree(engine=self.engine)
        self._current_parent: Optional[str] = None
    
    def root(self, key: str, style: Optional[LayoutStyle] = None, user_data: Any = None) -> 'LayoutTreeBuilder':
        """设置根节点"""
        root_node = self.tree.create_node(key, style, user_data)
        self.tree.set_root(root_node)
        self._current_parent = key
        return self
    
    def child(self, key: str, style: Optional[LayoutStyle] = None, user_data: Any = None) -> 'LayoutTreeBuilder':
        """添加子节点到当前父节点"""
        if not self._current_parent:
            raise ValueError("必须先设置根节点")
        
        child_node = self.tree.create_node(key, style, user_data)
        self.tree.add_node(self._current_parent, child_node)
        return self
    
    def begin_container(self, key: str, style: Optional[LayoutStyle] = None, user_data: Any = None) -> 'LayoutTreeBuilder':
        """开始容器节点 (后续子节点将添加到此容器)"""
        self.child(key, style, user_data)
        self._current_parent = key
        return self
    
    def end_container(self) -> 'LayoutTreeBuilder':
        """结束容器节点 (回到上级父节点)"""
        if self._current_parent:
            parent_node = self.tree.find_node(self._current_parent)
            if parent_node and parent_node.parent:
                self._current_parent = parent_node.parent.key
        return self
    
    def build(self) -> LayoutTree:
        """构建并返回布局树"""
        return self.tree