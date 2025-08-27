"""
LayoutEngine - 布局引擎核心

统一的布局计算和管理接口，封装Stretchable的复杂性
提供缓存、批处理和性能优化功能
"""

from typing import Dict, List, Optional, Callable, Any, Tuple
import time
from dataclasses import dataclass
from .node import LayoutNode
from .styles import LayoutStyle


@dataclass
class LayoutResult:
    """布局计算结果"""
    node: LayoutNode
    x: float
    y: float
    width: float
    height: float
    content_width: float
    content_height: float
    compute_time: float  # 计算耗时(毫秒)


@dataclass 
class LayoutMetrics:
    """布局性能指标"""
    total_nodes: int
    dirty_nodes: int
    compute_time: float  # 总计算时间(毫秒)
    layout_calls: int    # 布局调用次数
    cache_hits: int      # 缓存命中次数
    cache_misses: int    # 缓存未命中次数


class LayoutEngine:
    """布局引擎 - 专业级布局计算和管理
    
    提供高性能的布局计算、缓存管理和调试功能
    """
    
    def __init__(self, enable_cache: bool = True, debug_mode: bool = False):
        """初始化布局引擎
        
        Args:
            enable_cache: 是否启用布局缓存
            debug_mode: 是否启用调试模式
        """
        self.enable_cache = enable_cache
        self.debug_mode = debug_mode
        
        # 缓存系统
        self._layout_cache: Dict[str, LayoutResult] = {}
        self._cache_version = 0
        
        # 性能监控
        self._metrics = LayoutMetrics(
            total_nodes=0,
            dirty_nodes=0,
            compute_time=0.0,
            layout_calls=0,
            cache_hits=0,
            cache_misses=0
        )
        
        # 回调系统
        self._before_layout_callbacks: List[Callable[[LayoutNode], None]] = []
        self._after_layout_callbacks: List[Callable[[LayoutNode, LayoutResult], None]] = []
    
    def add_before_layout_callback(self, callback: Callable[[LayoutNode], None]):
        """添加布局前回调"""
        self._before_layout_callbacks.append(callback)
    
    def add_after_layout_callback(self, callback: Callable[[LayoutNode, LayoutResult], None]):
        """添加布局后回调"""
        self._after_layout_callbacks.append(callback)
    
    def compute_layout(
        self, 
        root: LayoutNode,
        available_size: Optional[Tuple[float, float]] = None,
        force_recompute: bool = False
    ) -> LayoutResult:
        """计算布局
        
        Args:
            root: 根布局节点
            available_size: 可用尺寸约束 (width, height)
            force_recompute: 强制重新计算 (忽略缓存)
            
        Returns:
            布局计算结果
        """
        start_time = time.perf_counter()
        
        # 更新统计
        self._metrics.layout_calls += 1
        self._count_nodes(root)
        
        # 缓存键
        cache_key = self._generate_cache_key(root, available_size) if self.enable_cache else None
        
        # 检查缓存
        if not force_recompute and cache_key and cache_key in self._layout_cache:
            cached_result = self._layout_cache[cache_key]
            if not root.is_dirty():  # 只有在节点不脏时才使用缓存
                self._metrics.cache_hits += 1
                if self.debug_mode:
                    print(f"🎯 布局缓存命中: {cache_key}")
                return cached_result
        
        self._metrics.cache_misses += 1
        
        # 执行布局前回调
        for callback in self._before_layout_callbacks:
            try:
                callback(root)
            except Exception as e:
                if self.debug_mode:
                    print(f"⚠️ 布局前回调错误: {e}")
        
        # 执行布局前调试
        from .debug import log_layout_computation, log_hierarchy_structure
        log_layout_computation(root, before_compute=True)
        
        if self.debug_mode:
            print(f"⚡ 开始布局计算: root={root.key}, available_size={available_size}")
            log_hierarchy_structure(root)
        
        # 只在根节点计算布局
        success = root.compute_layout(available_size)
        
        # 执行布局后调试
        log_layout_computation(root, before_compute=False)
        
        # 生成结果
        x, y, width, height = root.get_layout()
        
        # 获取内容尺寸 (处理可能的错误)
        try:
            content_width, content_height = root.get_content_size()
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ 获取内容尺寸失败: {e}, 使用布局尺寸")
            content_width, content_height = width, height
        
        compute_time = (time.perf_counter() - start_time) * 1000  # 转换为毫秒
        
        result = LayoutResult(
            node=root,
            x=x,
            y=y,
            width=width,
            height=height,
            content_width=content_width,
            content_height=content_height,
            compute_time=compute_time
        )
        
        # 更新缓存
        if cache_key:
            self._layout_cache[cache_key] = result
        
        # 更新性能指标
        self._metrics.compute_time += compute_time
        
        # 执行布局后回调
        for callback in self._after_layout_callbacks:
            try:
                callback(root, result)
            except Exception as e:
                if self.debug_mode:
                    print(f"⚠️ 布局后回调错误: {e}")
        
        if self.debug_mode:
            print(f"✅ 布局计算完成: {compute_time:.2f}ms")
            print(f"   📐 尺寸: {width:.1f}x{height:.1f}")
            print(f"   📍 位置: ({x:.1f}, {y:.1f})")
        
        return result
    
    def batch_compute_layouts(
        self, 
        nodes: List[Tuple[LayoutNode, Optional[Tuple[float, float]]]]
    ) -> List[LayoutResult]:
        """批量计算布局 - 性能优化
        
        Args:
            nodes: 节点和可用尺寸的列表
            
        Returns:
            布局结果列表
        """
        results = []
        
        if self.debug_mode:
            print(f"🔄 批量布局计算: {len(nodes)} 个节点")
        
        start_time = time.perf_counter()
        
        for node, available_size in nodes:
            result = self.compute_layout(node, available_size)
            results.append(result)
        
        batch_time = (time.perf_counter() - start_time) * 1000
        
        if self.debug_mode:
            print(f"✅ 批量布局完成: {batch_time:.2f}ms")
            print(f"   📊 平均耗时: {batch_time/len(nodes):.2f}ms/节点")
        
        return results
    
    def invalidate_cache(self, node_key: Optional[str] = None):
        """使缓存失效
        
        Args:
            node_key: 特定节点key，None表示清空所有缓存
        """
        if node_key:
            # 清除特定节点的缓存
            keys_to_remove = [key for key in self._layout_cache.keys() if node_key in key]
            for key in keys_to_remove:
                del self._layout_cache[key]
        else:
            # 清空所有缓存
            self._layout_cache.clear()
        
        self._cache_version += 1
        
        if self.debug_mode:
            print(f"🗑️ 布局缓存已清理: {node_key or 'all'}")
    
    def get_metrics(self) -> LayoutMetrics:
        """获取性能指标"""
        return self._metrics
    
    def reset_metrics(self):
        """重置性能指标"""
        self._metrics = LayoutMetrics(
            total_nodes=0,
            dirty_nodes=0,
            compute_time=0.0,
            layout_calls=0,
            cache_hits=0,
            cache_misses=0
        )
    
    def debug_print_metrics(self):
        """调试输出性能指标"""
        m = self._metrics
        print(f"📊 布局引擎性能指标:")
        print(f"   🏗️  总节点数: {m.total_nodes}")
        print(f"   🔄 脏节点数: {m.dirty_nodes}")
        print(f"   ⏱️  总计算时间: {m.compute_time:.2f}ms")
        print(f"   📞 布局调用次数: {m.layout_calls}")
        print(f"   🎯 缓存命中: {m.cache_hits}")
        print(f"   ❌ 缓存未命中: {m.cache_misses}")
        if m.layout_calls > 0:
            print(f"   📈 平均耗时: {m.compute_time/m.layout_calls:.2f}ms/调用")
        if m.cache_hits + m.cache_misses > 0:
            hit_rate = m.cache_hits / (m.cache_hits + m.cache_misses) * 100
            print(f"   🏆 缓存命中率: {hit_rate:.1f}%")
    
    def _generate_cache_key(self, root: LayoutNode, available_size: Optional[Tuple[float, float]]) -> str:
        """生成缓存键"""
        # 简化版本：基于节点key和可用尺寸
        # 实际实现可能需要考虑样式哈希等
        size_str = f"{available_size[0]}x{available_size[1]}" if available_size else "auto"
        return f"{root.key or 'root'}_{size_str}_{self._cache_version}"
    
    def _count_nodes(self, root: LayoutNode):
        """统计节点数量"""
        def count_recursive(node: LayoutNode) -> Tuple[int, int]:
            total = 1
            dirty = 1 if node.is_dirty() else 0
            
            for child in node.children:
                child_total, child_dirty = count_recursive(child)
                total += child_total
                dirty += child_dirty
            
            return total, dirty
        
        total, dirty = count_recursive(root)
        self._metrics.total_nodes = total
        self._metrics.dirty_nodes = dirty


# 全局布局引擎实例 - 单例模式
_global_engine: Optional[LayoutEngine] = None


def get_layout_engine() -> LayoutEngine:
    """获取全局布局引擎实例"""
    global _global_engine
    if _global_engine is None:
        _global_engine = LayoutEngine(enable_cache=True, debug_mode=True)  # 启用调试模式定位布局问题
    return _global_engine


def set_debug_mode(enabled: bool):
    """设置全局调试模式"""
    get_layout_engine().debug_mode = enabled


def compute_layout(
    root: LayoutNode,
    available_size: Optional[Tuple[float, float]] = None
) -> LayoutResult:
    """便捷的布局计算函数"""
    return get_layout_engine().compute_layout(root, available_size)