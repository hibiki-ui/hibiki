import threading
from collections import deque
from contextvars import ContextVar
from typing import Callable, Generic, Optional, TypeVar, Dict, Set

T = TypeVar("T")

# 🚀 Reaktiv-inspired优化系统
_global_version = 0
_batch_depth = 0
_deferred_updates: deque = deque()
_batch_lock = threading.Lock()

# 导入日志系统
try:
    from .logging import get_logger
    logger = get_logger("signal")
except ImportError:
    # 如果日志系统不可用，使用基本的打印
    import logging
    logger = logging.getLogger("macui.signal")
    
    # 防止重复添加handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        print(f"🔧 Logger初始化: 添加了StreamHandler, 总handlers数: {len(logger.handlers)}")
    else:
        print(f"⚠️  Logger已存在handlers: {len(logger.handlers)} 个")

# 🆕 优化的批处理系统
def _start_batch():
    """开始批处理"""
    global _batch_depth
    with _batch_lock:
        _batch_depth += 1
        if _batch_depth == 1:
            logger.info(f"🚀 开始批处理 (深度: {_batch_depth})")

def _end_batch():
    """结束批处理并刷新更新"""
    global _batch_depth
    with _batch_lock:
        _batch_depth -= 1
        if _batch_depth == 0:
            logger.info(f"🏁 结束批处理，处理 {len(_deferred_updates)} 个排队更新")
            _flush_deferred_updates()

def _enqueue_update(observer):
    """将更新加入队列"""
    _deferred_updates.append(observer)
    logger.info(f"📥 更新入队: {type(observer).__name__}[{id(observer)}]")

def _flush_deferred_updates():
    """🆕 批处理刷新 - 去重优化"""
    if not _deferred_updates:
        return
    
    # 去重处理：同一个观察者在一个批次中只处理一次
    processed: Set[int] = set()
    
    while _deferred_updates:
        observer = _deferred_updates.popleft()
        observer_id = id(observer)
        
        if observer_id in processed:
            logger.debug(f"⏭️  跳过重复更新: {type(observer).__name__}[{observer_id}]")
            continue
        
        processed.add(observer_id)
        logger.info(f"⚡ 执行更新: {type(observer).__name__}[{observer_id}]")
        
        try:
            if hasattr(observer, '_rerun') and hasattr(observer, '_active'):
                if observer._active:
                    logger.info(f"   调用 {type(observer).__name__}._rerun() - active")
                    observer._rerun()
                else:
                    logger.info(f"   跳过 {type(observer).__name__} - inactive")
                # 清理失活的观察者在各自的_notify_observers中处理
            elif hasattr(observer, '_rerun'):
                logger.info(f"   调用 {type(observer).__name__}._rerun() - no active check")
                observer._rerun()
            else:
                logger.info(f"   直接调用 {type(observer).__name__}()")
                observer()
        except Exception as e:
            logger.error(f"❌ 批处理更新错误: {e}")

class BatchUpdater:
    """向后兼容的批量更新系统"""

    def __init__(self):
        self._queue = deque()
        self._scheduled = False
        self._lock = threading.Lock()

    def batch_update(self, fn: Callable[[], None]) -> None:
        """批量执行更新，避免多次渲染"""
        # 使用新的批处理系统
        _start_batch()
        try:
            fn()
        finally:
            _end_batch()

    def _flush_updates(self):
        """保留兼容性方法"""
        _flush_deferred_updates()

# 全局批量更新器
batch_updater = BatchUpdater()
batch_update = batch_updater.batch_update


class Signal(Generic[T]):
    """🚀 优化版响应式信号 - 集成版本控制和智能缓存"""

    _current_observer: ContextVar[Optional[Callable]] = ContextVar("observer", default=None)

    def __init__(self, initial_value: T):
        self._value = initial_value
        self._observers = set()  # 改用普通set，手动管理Effect引用
        self._version = 0  # 🆕 版本控制
        logger.debug(f"Signal创建: 初始值={initial_value}, 版本=v{self._version}, id={id(self)}")

    def get(self) -> T:
        """获取信号值，同时建立依赖关系 + 版本追踪"""
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
            # 🆕 记录观察者看到的版本
            if hasattr(observer, '_dependency_versions'):
                observer._dependency_versions[id(self)] = self._version
            logger.debug(f"Signal[{id(self)}].get: 添加观察者 {type(observer).__name__}[{id(observer)}] (v{self._version}), 总观察者数: {len(self._observers)}")
        else:
            logger.debug(f"Signal[{id(self)}].get: 无当前观察者, 返回值: {self._value} (v{self._version})")
        return self._value

    def set(self, new_value: T) -> None:
        """🚀 优化设置信号值 - 版本控制 + 批处理"""
        global _global_version
        
        if self._value != new_value:
            old_value = self._value
            old_version = self._version
            
            self._value = new_value
            self._version += 1  # 🆕 版本递增
            _global_version += 1  # 🆕 全局版本递增
            
            logger.info(f"Signal[{id(self)}].set: {old_value} -> {new_value} (v{old_version} -> v{self._version}), 观察者数: {len(self._observers)}")
            
            # 🆕 批处理通知
            _start_batch()
            try:
                self._notify_observers()
            finally:
                _end_batch()
        else:
            logger.debug(f"Signal[{id(self)}].set: 值未变化 ({new_value}), 跳过通知")

    def _notify_observers(self):
        """🚀 优化通知观察者 - 智能批处理"""
        observers = list(self._observers)  # 创建副本避免并发修改
        logger.info(f"Signal[{id(self)}]._notify_observers: 批处理通知 {len(observers)} 个观察者")
        
        for i, observer in enumerate(observers):
            try:
                # 🆕 智能更新检查
                if hasattr(observer, '_needs_update'):
                    if observer._needs_update(self):
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: {type(observer).__name__}[{id(observer)}] 需要更新")
                        _enqueue_update(observer)
                    else:
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: {type(observer).__name__}[{id(observer)}] 版本未变，跳过")
                else:
                    # 兼容现有Effect
                    if hasattr(observer, '_active') and not observer._active:
                        # 清理失活的Effect
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: Effect[{id(observer)}] 已失活，移除")
                        self._observers.discard(observer)
                    else:
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: {type(observer).__name__}[{id(observer)}] 加入批处理")
                        _enqueue_update(observer)
            except Exception as e:
                logger.error(f"观察者 {i+1}/{len(observers)} 通知错误: {e}")
                # 如果是失活的Effect，从观察者中移除
                if hasattr(observer, '_active') and not observer._active:
                    self._observers.discard(observer)
        
        logger.debug(f"Signal[{id(self)}]._notify_observers: 批处理通知完成，剩余观察者: {len(self._observers)}")

    @property
    def value(self) -> T:
        return self.get()

    @value.setter
    def value(self, new_value: T) -> None:
        self.set(new_value)


class Computed(Generic[T]):
    """🚀 优化计算属性 - 智能缓存 + 版本控制"""

    def __init__(self, fn: Callable[[], T]):
        global _global_version
        self._fn = fn
        self._value: Optional[T] = None
        self._version = 0  # 🆕 版本控制
        self._dirty = True
        self._observers = set()  # 改用普通set
        self._dependency_versions: Dict[int, int] = {}  # 🆕 依赖版本追踪
        self._global_version_seen = _global_version - 1  # 🆕 全局版本追踪
        logger.debug(f"Computed创建: 版本=v{self._version}, id={id(self)}")

    def get(self) -> T:
        """🚀 智能获取 - 仅在必要时重计算"""
        global _global_version
        
        # 🆕 全局版本检查：如果全局无变化且不脏，直接返回缓存
        if not self._dirty and self._global_version_seen == _global_version:
            logger.debug(f"Computed[{id(self)}].get: 使用全局缓存 = {self._value} (v{self._version})")
        else:
            # 检查是否需要重计算
            if self._dirty or self._dependencies_changed():
                logger.debug(f"Computed[{id(self)}].get: 重计算 (脏标记: {self._dirty})")
                self._recompute()
            else:
                logger.debug(f"Computed[{id(self)}].get: 依赖未变，使用缓存 = {self._value} (v{self._version})")

        # 向上传播依赖
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
            # 🆕 记录观察者看到的版本
            if hasattr(observer, '_dependency_versions'):
                observer._dependency_versions[id(self)] = self._version
            logger.debug(f"Computed[{id(self)}].get: 添加观察者 {type(observer).__name__}[{id(observer)}] (v{self._version}), 总观察者数: {len(self._observers)}")
        else:
            logger.debug(f"Computed[{id(self)}].get: 无当前观察者, 返回值: {self._value} (v{self._version})")

        return self._value

    def _dependencies_changed(self) -> bool:
        """🆕 检查依赖版本是否变化"""
        # 简化实现 - 实际应该检查所有记录的依赖版本
        # 这里可以添加更精细的依赖检查逻辑
        return False
    
    def _recompute(self):
        """🚀 重新计算值 - 版本控制"""
        global _global_version
        
        # 设置当前观察者为自己
        token = Signal._current_observer.set(self)
        try:
            old_value = self._value
            self._value = self._fn()
            
            # 🆕 智能版本控制 - 仅值改变时递增
            if old_value != self._value:
                self._version += 1
                logger.debug(f"Computed[{id(self)}]: 版本更新 v{self._version-1} -> v{self._version}")
            
            self._dirty = False
            self._global_version_seen = _global_version
            
        finally:
            Signal._current_observer.reset(token)

    def _needs_update(self, source) -> bool:
        """🆕 版本化依赖检查"""
        if hasattr(source, '_version'):
            source_id = id(source)
            if source_id in self._dependency_versions:
                last_seen = self._dependency_versions[source_id]
                current = source._version
                needs_update = current > last_seen
                logger.debug(f"Computed[{id(self)}] 检查依赖更新: v{last_seen} vs v{current} -> {'需要' if needs_update else '跳过'}")
                return needs_update
        return True
    
    def _invalidate(self):
        """标记为需要重新计算并通知"""
        if not self._dirty:  # 避免重复失效
            self._dirty = True
            logger.debug(f"Computed[{id(self)}]: 标记为脏")
            self._notify_observers()
    
    def _rerun(self):
        """重新运行计算 - 与Effect接口兼容"""
        logger.info(f"Computed[{id(self)}]._rerun: 收到重新运行请求")
        self._invalidate()

    def _notify_observers(self):
        """🚀 通知观察者 - 批处理优化"""
        observers = list(self._observers)
        logger.debug(f"Computed[{id(self)}]._notify_observers: 批处理通知 {len(observers)} 个观察者")
        
        for observer in observers:
            try:
                # 🆕 智能更新检查
                if hasattr(observer, '_needs_update'):
                    if observer._needs_update(self):
                        logger.debug(f"  观察者 {type(observer).__name__}[{id(observer)}] 需要更新")
                        _enqueue_update(observer)
                    else:
                        logger.debug(f"  观察者 {type(observer).__name__}[{id(observer)}] 版本未变，跳过")
                else:
                    # 兼容现有观察者
                    if hasattr(observer, '_active') and not observer._active:
                        # 清理失活的Effect
                        logger.debug(f"  观察者 Effect[{id(observer)}] 已失活，移除")
                        self._observers.discard(observer)
                    else:
                        logger.debug(f"  观察者 {type(observer).__name__}[{id(observer)}] 加入批处理")
                        _enqueue_update(observer)
            except Exception as e:
                logger.error(f"Computed observer error: {e}")
                # 如果是失活的Effect，从观察者中移除
                if hasattr(observer, '_active') and not observer._active:
                    self._observers.discard(observer)

    @property
    def value(self) -> T:
        return self.get()


# 全局Effect注册表，防止被垃圾回收
_active_effects = set()

class Effect:
    """🚀 优化副作用 - 智能更新检查"""

    def __init__(self, fn: Callable[[], None]):
        import traceback
        print(f"📍 Effect.__init__ 被调用! Effect ID: {id(self)}")
        stack_lines = traceback.format_stack()
        for i, line in enumerate(stack_lines[-5:-1]):  # 显示最近4层调用栈
            print(f"   调用栈[{i}]: {line.strip()}")
        
        self._fn = fn
        self._cleanup_fn: Optional[Callable[[], None]] = None
        self._active = True
        self._dependency_versions: Dict[int, int] = {}  # 🆕 依赖版本追踪
        
        logger.info(f"Effect创建: id={id(self)}, 函数={fn.__name__ if hasattr(fn, '__name__') else type(fn).__name__}")
        
        # 注册到全局列表以防止被垃圾回收
        _active_effects.add(self)
        logger.debug(f"Effect[{id(self)}]: 注册到全局列表，总Effect数: {len(_active_effects)}")
        
        self._run_effect()

    def _run_effect(self):
        """运行副作用函数"""
        if not self._active:
            logger.debug(f"Effect[{id(self)}]._run_effect: Effect已失活，跳过执行")
            return

        logger.debug(f"Effect[{id(self)}]._run_effect: 开始执行")

        # 清理上一次的副作用
        if self._cleanup_fn:
            logger.debug(f"Effect[{id(self)}]: 清理上一次的副作用")
            self._cleanup_fn()
            self._cleanup_fn = None

        # 设置当前观察者为自己（而不是方法）
        token = Signal._current_observer.set(self)
        logger.debug(f"Effect[{id(self)}]: 设置为当前观察者，开始执行函数")
        
        try:
            result = self._fn()
            # 如果函数返回清理函数，保存它
            if callable(result):
                self._cleanup_fn = result
                logger.debug(f"Effect[{id(self)}]: 保存清理函数")
            logger.debug(f"Effect[{id(self)}]: 函数执行完成")
        except Exception as e:
            logger.error(f"Effect[{id(self)}] 执行错误: {e}")
        finally:
            Signal._current_observer.reset(token)
            logger.debug(f"Effect[{id(self)}]: 重置观察者上下文")

    def _needs_update(self, source) -> bool:
        """🆕 智能更新检查"""
        if hasattr(source, '_version'):
            source_id = id(source)
            if source_id in self._dependency_versions:
                last_seen = self._dependency_versions[source_id]
                current = source._version
                needs_update = current > last_seen
                logger.debug(f"Effect[{id(self)}] 检查依赖更新: v{last_seen} vs v{current} -> {'需要' if needs_update else '跳过'}")
                return needs_update
        return True
    
    def _rerun(self):
        """重新运行副作用"""
        logger.info(f"Effect[{id(self)}]._rerun: 收到重新运行请求")
        if self._active:
            self._run_effect()
        else:
            logger.debug(f"Effect[{id(self)}]._rerun: Effect已失活，跳过重新运行")

    def cleanup(self):
        """清理副作用"""
        self._active = False
        if self._cleanup_fn:
            self._cleanup_fn()
            self._cleanup_fn = None
        
        # 从全局注册表中移除
        _active_effects.discard(self)
        logger.debug(f"Effect[{id(self)}]: 清理完成，剩余总Effect数: {len(_active_effects)}")

# ================================
# 3. 便捷创建函数
# ================================

def create_signal(initial_value: T) -> Signal[T]:
    """创建信号的便捷函数"""
    return Signal(initial_value)

def create_computed(fn: Callable[[], T]) -> Computed[T]:
    """创建计算属性的便捷函数"""
    return Computed(fn)

def create_effect(fn: Callable[[], None]) -> Effect:
    """创建副作用的便捷函数"""
    return Effect(fn)

# 导出
__all__ = [
    'Signal', 'Computed', 'Effect',
    'create_signal', 'create_computed', 'create_effect',
    'batch_update'
]