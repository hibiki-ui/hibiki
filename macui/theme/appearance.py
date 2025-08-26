"""macUI v2 外观管理器

处理macOS系统外观变化检测和响应。
"""

from typing import Callable, List, Optional
import weakref

from AppKit import NSView, NSApplication, NSAppearance
from Foundation import NSUserDefaults, NSUserDefaultsDidChangeNotification, NSNotificationCenter
from PyObjCTools.AppHelper import callAfter

from ..core.signal import Signal


class AppearanceMode:
    """外观模式常量"""
    LIGHT = "NSAppearanceNameAqua"
    DARK = "NSAppearanceNameDarkAqua"
    AUTO = "auto"  # 跟随系统


class AppearanceObserver:
    """外观变化观察者"""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self._is_active = True
    
    def notify(self, appearance: str):
        """通知外观变化"""
        if self._is_active and self.callback:
            try:
                self.callback(appearance)
            except Exception as e:
                print(f"AppearanceObserver callback error: {e}")
    
    def deactivate(self):
        """停用观察者"""
        self._is_active = False


class AppearanceManager:
    """外观管理器 - 统一处理外观变化"""
    
    _instance: Optional["AppearanceManager"] = None
    
    def __init__(self):
        if AppearanceManager._instance is not None:
            raise RuntimeError("AppearanceManager is a singleton. Use AppearanceManager.shared() instead.")
        
        self._current_appearance = Signal(self._detect_current_appearance())
        self._observers: List[weakref.ReferenceType] = []
        self._setup_appearance_monitoring()
    
    @classmethod
    def shared(cls) -> "AppearanceManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _detect_current_appearance(self) -> str:
        """检测当前系统外观"""
        try:
            # 方法1：通过NSUserDefaults检测
            interface_style = NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle')
            if interface_style == 'Dark':
                return AppearanceMode.DARK
            else:
                return AppearanceMode.LIGHT
        except:
            # 方法2：通过NSApplication检测
            try:
                app = NSApplication.sharedApplication()
                effective_appearance = app.effectiveAppearance()
                appearance_name = effective_appearance.name()
                
                if "Dark" in str(appearance_name):
                    return AppearanceMode.DARK
                else:
                    return AppearanceMode.LIGHT
            except:
                # 默认返回浅色模式
                return AppearanceMode.LIGHT
    
    def _setup_appearance_monitoring(self):
        """设置外观变化监控"""
        try:
            # 监听系统设置变化
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                self,
                "systemAppearanceDidChange:",
                NSUserDefaultsDidChangeNotification,
                None
            )
            print("✅ AppearanceManager: 外观变化监控已设置")
        except Exception as e:
            print(f"❌ AppearanceManager: 设置外观监控失败 - {e}")
    
    def systemAppearanceDidChange_(self, notification):
        """系统外观变化回调"""
        def update_appearance():
            new_appearance = self._detect_current_appearance()
            if new_appearance != self._current_appearance.value:
                print(f"🌗 外观模式变化: {self._current_appearance.value} -> {new_appearance}")
                self._current_appearance.value = new_appearance
                self._notify_observers(new_appearance)
        
        # 在主线程中执行更新
        callAfter(update_appearance)
    
    def _notify_observers(self, appearance: str):
        """通知所有观察者"""
        # 清理无效的弱引用
        self._observers = [ref for ref in self._observers if ref() is not None]
        
        # 通知有效的观察者
        for observer_ref in self._observers:
            observer = observer_ref()
            if observer:
                observer.notify(appearance)
    
    @property
    def current_appearance(self) -> Signal[str]:
        """当前外观模式Signal"""
        return self._current_appearance
    
    def is_dark_mode(self) -> bool:
        """当前是否为深色模式"""
        return self._current_appearance.value == AppearanceMode.DARK
    
    def is_light_mode(self) -> bool:
        """当前是否为浅色模式"""
        return self._current_appearance.value == AppearanceMode.LIGHT
    
    def add_observer(self, callback: Callable[[str], None]) -> AppearanceObserver:
        """添加外观变化观察者
        
        Args:
            callback: 回调函数，参数为新的外观模式
            
        Returns:
            AppearanceObserver实例，用于管理观察者生命周期
        """
        observer = AppearanceObserver(callback)
        self._observers.append(weakref.ref(observer))
        return observer
    
    def remove_observer(self, observer: AppearanceObserver):
        """移除外观变化观察者"""
        observer.deactivate()
    
    def set_app_appearance(self, appearance: str):
        """设置应用外观模式
        
        Args:
            appearance: AppearanceMode.LIGHT, AppearanceMode.DARK, 或 AppearanceMode.AUTO
        """
        try:
            app = NSApplication.sharedApplication()
            
            if appearance == AppearanceMode.AUTO:
                # 跟随系统
                app.setAppearance_(None)
                print("🌗 应用外观设置为跟随系统")
            elif appearance == AppearanceMode.LIGHT:
                # 强制浅色模式
                light_appearance = NSAppearance.appearanceNamed_(AppearanceMode.LIGHT)
                app.setAppearance_(light_appearance)
                print("☀️ 应用外观设置为浅色模式")
            elif appearance == AppearanceMode.DARK:
                # 强制深色模式
                dark_appearance = NSAppearance.appearanceNamed_(AppearanceMode.DARK)
                app.setAppearance_(dark_appearance)
                print("🌙 应用外观设置为深色模式")
            else:
                print(f"❌ 不支持的外观模式: {appearance}")
        except Exception as e:
            print(f"❌ 设置应用外观失败: {e}")
    
    def apply_appearance_to_view(self, view: NSView, appearance: Optional[str] = None):
        """为指定视图应用外观
        
        Args:
            view: 目标NSView
            appearance: 外观模式，None表示跟随应用设置
        """
        try:
            if appearance is None:
                # 跟随应用设置
                view.setAppearance_(None)
            elif appearance == AppearanceMode.LIGHT:
                light_appearance = NSAppearance.appearanceNamed_(AppearanceMode.LIGHT)
                view.setAppearance_(light_appearance)
            elif appearance == AppearanceMode.DARK:
                dark_appearance = NSAppearance.appearanceNamed_(AppearanceMode.DARK)
                view.setAppearance_(dark_appearance)
        except Exception as e:
            print(f"❌ 为视图应用外观失败: {e}")


# 便捷函数
def get_appearance_manager() -> AppearanceManager:
    """获取外观管理器实例"""
    return AppearanceManager.shared()


def is_dark_mode() -> bool:
    """检测当前是否为深色模式"""
    return get_appearance_manager().is_dark_mode()


def add_appearance_observer(callback: Callable[[str], None]) -> AppearanceObserver:
    """添加外观变化观察者"""
    return get_appearance_manager().add_observer(callback)