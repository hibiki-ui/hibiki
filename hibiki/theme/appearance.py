"""Hibiki UI v4 外观管理

提供系统外观检测和Dark/Light模式支持
"""

from typing import Optional, Callable, List
import weakref
import objc
from AppKit import NSApplication, NSAppearance
from Foundation import NSObject
from ..core.reactive import Signal

from hibiki.core.logging import get_logger
logger = get_logger('theme.appearance')



class AppearanceMode:
    """外观模式常量"""
    AUTO = "auto"
    LIGHT = "light" 
    DARK = "dark"


class AppearanceObserver(NSObject):
    """外观变化观察者"""
    
    def initWithCallback_(self, callback: Callable[[str], None]):
        self = objc.super(AppearanceObserver, self).init()
        if self is None:
            return None
        self.callback = callback
        return self
    
    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        """外观变化回调"""
        if keyPath == "effectiveAppearance":
            appearance_name = self._get_appearance_name(object.effectiveAppearance())
            if self.callback:
                self.callback(appearance_name)
    
    def _get_appearance_name(self, appearance) -> str:
        """获取外观名称"""
        if not appearance:
            return "light"
        
        appearance_name = str(appearance.name())
        if "dark" in appearance_name.lower():
            return "dark"
        return "light"


class AppearanceManager:
    """外观管理器"""
    
    _instance: Optional["AppearanceManager"] = None
    
    def __init__(self):
        if AppearanceManager._instance is not None:
            raise RuntimeError("AppearanceManager is a singleton. Use AppearanceManager.shared() instead.")
        
        # 外观变化信号
        self.current_appearance = Signal(self.get_system_appearance())
        
        # 观察者列表
        self._observers: List[weakref.ReferenceType] = []
        self._kvo_observers: List[AppearanceObserver] = []
        
        # 开始监听系统外观变化
        self._setup_system_observation()
        
        logger.info(f"🌗 AppearanceManager初始化，当前外观: {self.current_appearance.value}")
    
    @classmethod
    def shared(cls) -> "AppearanceManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_system_appearance(self) -> str:
        """获取当前系统外观"""
        try:
            app = NSApplication.sharedApplication()
            if app:
                appearance = app.effectiveAppearance()
                if appearance:
                    appearance_name = str(appearance.name())
                    return "dark" if "dark" in appearance_name.lower() else "light"
        except Exception as e:
            logger.warning(f"⚠️ 获取系统外观失败: {e}")
        
        return "light"
    
    def is_dark_mode(self) -> bool:
        """当前是否为深色模式"""
        return self.current_appearance.value == "dark"
    
    def set_app_appearance(self, mode: str):
        """设置应用外观模式"""
        try:
            app = NSApplication.sharedApplication()
            if not app:
                return
            
            if mode == AppearanceMode.DARK:
                appearance = NSAppearance.appearanceNamed_("NSAppearanceNameDarkAqua")
            elif mode == AppearanceMode.LIGHT:
                appearance = NSAppearance.appearanceNamed_("NSAppearanceNameAqua")
            else:  # AUTO
                appearance = None  # 使用系统默认
            
            app.setAppearance_(appearance)
            
            # 更新当前外观
            new_appearance = self.get_system_appearance()
            if self.current_appearance.value != new_appearance:
                self.current_appearance.value = new_appearance
                self._notify_observers(new_appearance)
            
            logger.info(f"🌗 应用外观已设置: {mode} -> {new_appearance}")
            
        except Exception as e:
            logger.error(f"❌ 设置应用外观失败: {e}")
    
    def add_observer(self, callback: Callable[[str], None]) -> "AppearanceObserver":
        """添加外观变化观察者"""
        observer_ref = weakref.ref(callback)
        self._observers.append(observer_ref)
        logger.info(f"📡 已添加外观观察者，当前共 {len(self._observers)} 个")
        return callback  # 返回callback作为观察者标识
    
    def _setup_system_observation(self):
        """设置系统外观变化观察"""
        try:
            app = NSApplication.sharedApplication()
            if app:
                # 创建KVO观察者
                def on_appearance_change(appearance_name):
                    if self.current_appearance.value != appearance_name:
                        logger.info(f"🌗 系统外观变化: {self.current_appearance.value} -> {appearance_name}")
                        self.current_appearance.value = appearance_name
                        self._notify_observers(appearance_name)
                
                observer = AppearanceObserver.alloc().initWithCallback_(on_appearance_change)
                app.addObserver_forKeyPath_options_context_(
                    observer, "effectiveAppearance", 0, None
                )
                self._kvo_observers.append(observer)
                
                logger.info("📡 系统外观观察已设置")
                
        except Exception as e:
            logger.warning(f"⚠️ 设置系统外观观察失败: {e}")
    
    def _notify_observers(self, appearance_name: str):
        """通知观察者外观变化"""
        # 清理无效的弱引用
        self._observers = [ref for ref in self._observers if ref() is not None]
        
        # 通知有效的观察者
        for observer_ref in self._observers:
            callback = observer_ref()
            if callback:
                try:
                    callback(appearance_name)
                except Exception as e:
                    logger.error(f"AppearanceManager observer callback error: {e}")


# 便捷函数
def get_appearance_manager() -> AppearanceManager:
    """获取外观管理器实例"""
    return AppearanceManager.shared()


def is_dark_mode() -> bool:
    """当前是否为深色模式"""
    return get_appearance_manager().is_dark_mode()


def add_appearance_observer(callback: Callable[[str], None]):
    """添加外观变化观察者"""
    return get_appearance_manager().add_observer(callback)