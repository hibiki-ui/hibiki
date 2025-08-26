import threading
from collections import deque
from contextvars import ContextVar
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")

# 导入日志系统
try:
    from .logging import get_logger
    logger = get_logger("signal")
except ImportError:
    # 如果日志系统不可用，使用基本的打印
    import logging
    logger = logging.getLogger("macui.signal")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

class BatchUpdater:
    """批量更新系统，避免多次渲染"""

    def __init__(self):
        self._queue = deque()
        self._scheduled = False
        self._lock = threading.Lock()

    def batch_update(self, fn: Callable[[], None]) -> None:
        """批量执行更新，避免多次渲染"""
        with self._lock:
            self._queue.append(fn)
            if not self._scheduled:
                self._scheduled = True
                # 在实际的 macOS 环境中，这里会使用 performSelector 延迟到下一个运行循环
                # 现在先直接执行
                self._flush_updates()

    def _flush_updates(self):
        """刷新所有待处理的更新"""
        try:
            # QuartzCore 不可用时直接执行更新
            processed = 0
            max_updates = 100  # 防止无限循环
            while self._queue and processed < max_updates:
                update = self._queue.popleft()
                try:
                    update()
                    processed += 1
                except Exception as e:
                    print(f"Update error: {e}")
                    
            if processed >= max_updates:
                print(f"Warning: Batch update limit reached ({max_updates})")

        finally:
            self._scheduled = False

# 全局批量更新器
batch_updater = BatchUpdater()
batch_update = batch_updater.batch_update


class Signal(Generic[T]):
    """响应式信号 - 基础响应式值"""

    _current_observer: ContextVar[Optional[Callable]] = ContextVar("observer", default=None)

    def __init__(self, initial_value: T):
        self._value = initial_value
        self._observers = set()  # 改用普通set，手动管理Effect引用
        logger.debug(f"Signal创建: 初始值={initial_value}, id={id(self)}")

    def get(self) -> T:
        """获取信号值，同时建立依赖关系"""
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
            logger.debug(f"Signal[{id(self)}].get: 添加观察者 {type(observer).__name__}[{id(observer)}], 总观察者数: {len(self._observers)}")
        else:
            logger.debug(f"Signal[{id(self)}].get: 无当前观察者, 返回值: {self._value}")
        return self._value

    def set(self, new_value: T) -> None:
        """设置信号值，触发响应式更新"""
        if self._value != new_value:
            old_value = self._value
            self._value = new_value
            logger.info(f"Signal[{id(self)}].set: {old_value} -> {new_value}, 观察者数: {len(self._observers)}")
            # 直接通知观察者，避免批量更新造成的复杂性
            self._notify_observers()
        else:
            logger.debug(f"Signal[{id(self)}].set: 值未变化 ({new_value}), 跳过通知")

    def _notify_observers(self):
        """通知所有观察者"""
        observers = list(self._observers)  # 创建副本避免并发修改
        logger.debug(f"Signal[{id(self)}]._notify_observers: 开始通知 {len(observers)} 个观察者")
        
        for i, observer in enumerate(observers):
            try:
                # 如果观察者是Effect对象，调用其_rerun方法
                if hasattr(observer, '_rerun') and hasattr(observer, '_active'):
                    if observer._active:
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: Effect[{id(observer)}]._rerun()")
                        observer._rerun()
                    else:
                        # 清理失活的Effect
                        logger.debug(f"  观察者 {i+1}/{len(observers)}: Effect[{id(observer)}] 已失活，移除")
                        self._observers.discard(observer)
                elif hasattr(observer, '_rerun'):
                    # 如果有_rerun方法（如Computed），调用它
                    logger.debug(f"  观察者 {i+1}/{len(observers)}: {type(observer).__name__}[{id(observer)}]._rerun()")
                    observer._rerun()
                else:
                    # 否则直接调用（函数）
                    logger.debug(f"  观察者 {i+1}/{len(observers)}: {type(observer).__name__}[{id(observer)}]()")
                    observer()
            except Exception as e:
                logger.error(f"观察者 {i+1}/{len(observers)} 执行错误: {e}")
                # 如果是失活的Effect，从观察者中移除
                if hasattr(observer, '_active') and not observer._active:
                    self._observers.discard(observer)
        
        logger.debug(f"Signal[{id(self)}]._notify_observers: 通知完成，剩余观察者: {len(self._observers)}")

    @property
    def value(self) -> T:
        return self.get()

    @value.setter
    def value(self, new_value: T) -> None:
        self.set(new_value)


class Computed(Generic[T]):
    """计算属性 - 自动缓存的派生值"""

    def __init__(self, fn: Callable[[], T]):
        self._fn = fn
        self._value: Optional[T] = None
        self._dirty = True
        self._observers = set()  # 改用普通set
        self._dependencies = set()  # 跟踪依赖的信号

    def get(self) -> T:
        """获取计算值，必要时重新计算"""
        if self._dirty:
            self._recompute()

        # 向上传播依赖
        observer = Signal._current_observer.get()
        if observer:
            self._observers.add(observer)
            logger.debug(f"Computed[{id(self)}].get: 添加观察者 {type(observer).__name__}[{id(observer)}], 总观察者数: {len(self._observers)}")
        else:
            logger.debug(f"Computed[{id(self)}].get: 无当前观察者, 返回值: {self._value}")

        return self._value

    def _recompute(self):
        """重新计算值"""
        # 设置当前观察者为自己，而不是_invalidate方法
        token = Signal._current_observer.set(self)
        try:
            self._value = self._fn()
            self._dirty = False
        finally:
            Signal._current_observer.reset(token)

    def _invalidate(self):
        """标记为需要重新计算"""
        if not self._dirty:  # 避免重复失效
            self._dirty = True
            # 直接通知观察者
            self._notify_observers()
    
    def _rerun(self):
        """重新运行计算 - 与Effect接口兼容"""
        logger.debug(f"Computed[{id(self)}]._rerun: 收到重新运行请求")
        self._invalidate()

    def _notify_observers(self):
        """通知所有观察者"""
        observers = list(self._observers)
        for observer in observers:
            try:
                # 如果观察者是Effect对象，调用其_rerun方法
                if hasattr(observer, '_rerun') and hasattr(observer, '_active'):
                    if observer._active:
                        observer._rerun()
                    else:
                        # 清理失活的Effect
                        self._observers.discard(observer)
                elif hasattr(observer, '_rerun'):
                    # 如果有_rerun方法（如其他Computed），调用它
                    observer._rerun()
                else:
                    # 否则直接调用（函数）
                    observer()
            except Exception as e:
                print(f"Computed observer error: {e}")
                # 如果是失活的Effect，从观察者中移除
                if hasattr(observer, '_active') and not observer._active:
                    self._observers.discard(observer)

    @property
    def value(self) -> T:
        return self.get()


# 全局Effect注册表，防止被垃圾回收
_active_effects = set()

class Effect:
    """副作用 - 自动重新运行的函数"""

    def __init__(self, fn: Callable[[], None]):
        self._fn = fn
        self._cleanup_fn: Optional[Callable[[], None]] = None
        self._active = True
        
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
