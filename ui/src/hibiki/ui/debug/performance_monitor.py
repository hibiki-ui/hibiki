#!/usr/bin/env python3
"""
Performance Monitor - 性能监控工具
================================

实时监控 Hibiki UI 应用的性能指标，包括：
- 布局计算性能
- 组件生命周期统计
- Signal 系统性能
- 内存使用分析
"""

import time
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum

from ..core.logging import get_logger
from ..core.layout import get_layout_engine

logger = get_logger("debug.performance_monitor")


class MetricType(Enum):
    """性能指标类型"""
    LAYOUT_TIME = "layout_time"
    COMPONENT_COUNT = "component_count"
    SIGNAL_UPDATES = "signal_updates"
    MEMORY_USAGE = "memory_usage"
    RENDER_TIME = "render_time"


@dataclass
class PerformanceMetric:
    """性能指标数据结构"""
    timestamp: float
    metric_type: MetricType
    value: float
    component_id: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class PerformanceMonitor:
    """性能监控器
    
    提供实时的性能数据收集和分析功能：
    - 自动监控关键性能指标
    - 历史数据存储和趋势分析
    - 性能瓶颈识别和警报
    - 统计报告生成
    """
    
    def __init__(self, 
                 history_size: int = 1000,
                 collection_interval: float = 0.1,
                 enable_auto_collection: bool = True):
        """初始化性能监控器
        
        Args:
            history_size: 历史数据保存数量
            collection_interval: 数据收集间隔（秒）
            enable_auto_collection: 是否启用自动数据收集
        """
        self.history_size = history_size
        self.collection_interval = collection_interval
        self.enable_auto_collection = enable_auto_collection
        
        # 数据存储
        self._metrics_history: deque[PerformanceMetric] = deque(maxlen=history_size)
        self._current_stats: Dict[str, Any] = {}
        self._component_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # 监控状态
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[PerformanceMetric], None]] = []
        
        # 性能警报阈值
        self._thresholds = {
            MetricType.LAYOUT_TIME: 16.67,  # 60fps = 16.67ms per frame
            MetricType.RENDER_TIME: 8.33,   # 建议渲染时间 < 8ms
            MetricType.COMPONENT_COUNT: 1000,  # 组件数量警报阈值
        }
    
    def start_monitoring(self, target_component=None):
        """开始性能监控
        
        Args:
            target_component: 要监控的目标组件，None表示全局监控
        """
        if self._monitoring:
            logger.warning("性能监控已经在运行中")
            return
        
        self._monitoring = True
        self._target_component = target_component
        
        logger.info("🚀 启动性能监控器")
        
        if self.enable_auto_collection:
            self._monitor_thread = threading.Thread(
                target=self._monitoring_loop, 
                daemon=True
            )
            self._monitor_thread.start()
        
        # 收集初始快照
        self._collect_snapshot()
    
    def stop_monitoring(self):
        """停止性能监控"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        logger.info("⏹️ 停止性能监控器")
        
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
            self._monitor_thread = None
    
    def add_metric(self, metric_type: MetricType, value: float, 
                   component_id: Optional[str] = None,
                   **additional_data):
        """手动添加性能指标
        
        Args:
            metric_type: 指标类型
            value: 指标值
            component_id: 相关组件ID
            additional_data: 额外数据
        """
        metric = PerformanceMetric(
            timestamp=time.time(),
            metric_type=metric_type,
            value=value,
            component_id=component_id,
            additional_data=additional_data
        )
        
        self._add_metric_internal(metric)
    
    def _add_metric_internal(self, metric: PerformanceMetric):
        """内部添加指标方法"""
        self._metrics_history.append(metric)
        
        # 更新当前统计
        key = metric.metric_type.value
        self._current_stats[key] = metric.value
        
        if metric.component_id:
            self._component_stats[metric.component_id][key] = metric.value
        
        # 检查性能警报
        self._check_performance_alerts(metric)
        
        # 调用回调函数
        for callback in self._callbacks:
            try:
                callback(metric)
            except Exception as e:
                logger.error(f"性能监控回调执行失败: {e}")
    
    def _monitoring_loop(self):
        """监控循环（在后台线程中运行）"""
        while self._monitoring:
            try:
                self._collect_snapshot()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"性能监控采集失败: {e}")
                time.sleep(1.0)  # 错误时延长间隔
    
    def _collect_snapshot(self):
        """收集性能快照"""
        current_time = time.time()
        
        # 收集布局引擎统计
        layout_stats = self._collect_layout_stats()
        for metric_type, value in layout_stats.items():
            metric = PerformanceMetric(
                timestamp=current_time,
                metric_type=metric_type,
                value=value
            )
            self._add_metric_internal(metric)
        
        # 收集组件统计
        if hasattr(self, '_target_component') and self._target_component:
            component_stats = self._collect_component_stats(self._target_component)
            for metric_type, value in component_stats.items():
                metric = PerformanceMetric(
                    timestamp=current_time,
                    metric_type=metric_type,
                    value=value,
                    component_id=str(id(self._target_component))
                )
                self._add_metric_internal(metric)
    
    def _collect_layout_stats(self) -> Dict[MetricType, float]:
        """收集布局引擎统计"""
        stats = {}
        
        try:
            engine = get_layout_engine()
            health_info = engine.health_check()
            
            # 节点数量统计
            if 'total_nodes' in health_info:
                stats[MetricType.COMPONENT_COUNT] = float(health_info['total_nodes'])
            
            # TODO: 从布局引擎获取更详细的性能数据
            # 这需要布局引擎支持性能统计API
            
        except Exception as e:
            logger.debug(f"收集布局统计失败: {e}")
        
        return stats
    
    def _collect_component_stats(self, component) -> Dict[MetricType, float]:
        """收集单个组件的统计信息"""
        stats = {}
        
        try:
            # 组件层次深度
            # TODO: 实现组件层次深度计算
            
            # 子组件数量
            if hasattr(component, 'children') and component.children:
                stats[MetricType.COMPONENT_COUNT] = float(len(component.children))
        
        except Exception as e:
            logger.debug(f"收集组件统计失败: {e}")
        
        return stats
    
    def _check_performance_alerts(self, metric: PerformanceMetric):
        """检查性能警报"""
        if metric.metric_type in self._thresholds:
            threshold = self._thresholds[metric.metric_type]
            if metric.value > threshold:
                logger.warning(
                    f"⚠️ 性能警报: {metric.metric_type.value} = {metric.value:.2f} "
                    f"(阈值: {threshold})"
                )
    
    def get_current_stats(self) -> Dict[str, Any]:
        """获取当前性能统计"""
        return self._current_stats.copy()
    
    def get_historical_data(self, 
                          metric_type: Optional[MetricType] = None,
                          component_id: Optional[str] = None,
                          time_range: Optional[tuple] = None) -> List[PerformanceMetric]:
        """获取历史数据
        
        Args:
            metric_type: 过滤指标类型
            component_id: 过滤组件ID
            time_range: 时间范围 (start_time, end_time)
            
        Returns:
            符合条件的历史数据列表
        """
        filtered_data = []
        
        for metric in self._metrics_history:
            # 类型过滤
            if metric_type and metric.metric_type != metric_type:
                continue
            
            # 组件过滤
            if component_id and metric.component_id != component_id:
                continue
            
            # 时间过滤
            if time_range:
                start_time, end_time = time_range
                if not (start_time <= metric.timestamp <= end_time):
                    continue
            
            filtered_data.append(metric)
        
        return filtered_data
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要报告"""
        if not self._metrics_history:
            return {"error": "暂无性能数据"}
        
        summary = {
            "collection_period": {
                "start": min(m.timestamp for m in self._metrics_history),
                "end": max(m.timestamp for m in self._metrics_history),
                "duration": max(m.timestamp for m in self._metrics_history) - 
                          min(m.timestamp for m in self._metrics_history)
            },
            "metrics_count": len(self._metrics_history),
            "current_stats": self._current_stats.copy(),
            "averages": {},
            "peaks": {},
            "alerts_triggered": 0
        }
        
        # 计算各指标的平均值和峰值
        metric_groups = defaultdict(list)
        for metric in self._metrics_history:
            metric_groups[metric.metric_type].append(metric.value)
        
        for metric_type, values in metric_groups.items():
            key = metric_type.value
            summary["averages"][key] = sum(values) / len(values)
            summary["peaks"][key] = max(values)
        
        # TODO: 计算警报触发次数
        
        return summary
    
    def add_callback(self, callback: Callable[[PerformanceMetric], None]):
        """添加性能数据回调函数
        
        Args:
            callback: 回调函数，接收 PerformanceMetric 参数
        """
        self._callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[PerformanceMetric], None]):
        """移除回调函数"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def set_threshold(self, metric_type: MetricType, threshold: float):
        """设置性能警报阈值
        
        Args:
            metric_type: 指标类型
            threshold: 阈值
        """
        self._thresholds[metric_type] = threshold
        logger.info(f"设置 {metric_type.value} 阈值为 {threshold}")
    
    def export_data(self, format: str = "dict") -> Any:
        """导出性能数据
        
        Args:
            format: 导出格式 ("dict", "json", "csv")
            
        Returns:
            导出的数据
        """
        if format == "dict":
            return {
                "summary": self.get_performance_summary(),
                "metrics": [
                    {
                        "timestamp": m.timestamp,
                        "type": m.metric_type.value,
                        "value": m.value,
                        "component_id": m.component_id,
                        "additional_data": m.additional_data
                    }
                    for m in self._metrics_history
                ]
            }
        elif format == "json":
            import json
            return json.dumps(self.export_data("dict"), indent=2)
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # 写入标题
            writer.writerow([
                "timestamp", "metric_type", "value", 
                "component_id", "additional_data"
            ])
            
            # 写入数据
            for metric in self._metrics_history:
                writer.writerow([
                    metric.timestamp,
                    metric.metric_type.value, 
                    metric.value,
                    metric.component_id or "",
                    str(metric.additional_data)
                ])
            
            return output.getvalue()
        else:
            raise ValueError(f"不支持的导出格式: {format}")


# 全局性能监控器实例
_global_monitor: Optional[PerformanceMonitor] = None


def get_global_monitor() -> PerformanceMonitor:
    """获取全局性能监控器实例"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor


def get_performance_stats(component=None) -> Dict[str, Any]:
    """获取性能统计（便捷函数）
    
    Args:
        component: 目标组件，None表示全局统计
        
    Returns:
        性能统计字典
    """
    monitor = get_global_monitor()
    
    if component and not monitor._monitoring:
        # 如果监控未启动，进行一次性数据收集
        monitor._collect_snapshot()
    
    return monitor.get_current_stats()


def start_performance_monitoring(component=None, 
                                auto_collection: bool = True,
                                collection_interval: float = 0.1):
    """启动全局性能监控（便捷函数）
    
    Args:
        component: 目标组件
        auto_collection: 是否自动收集
        collection_interval: 收集间隔
    """
    monitor = get_global_monitor()
    monitor.enable_auto_collection = auto_collection
    monitor.collection_interval = collection_interval
    monitor.start_monitoring(component)


def stop_performance_monitoring():
    """停止全局性能监控（便捷函数）"""
    monitor = get_global_monitor()
    monitor.stop_monitoring()


if __name__ == "__main__":
    # 测试代码
    print("📊 Hibiki UI Performance Monitor")
    print("================================")
    print()
    print("这是一个专业的性能监控工具。")
    print("要使用此工具，请在您的 Hibiki UI 应用中启动监控。")
    print()
    print("示例用法:")
    print("```python")
    print("from hibiki.ui.debug import start_performance_monitoring")
    print("start_performance_monitoring(my_component)")
    print("```")