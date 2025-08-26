"""macUI v2 应用程序和窗口管理 - 遵循 PyObjC 最佳实践
"""

from typing import Callable, Optional, Tuple

try:
    from .core.component import Component
except ImportError:
    # 如果相对导入失败，尝试直接导入
    from core.component import Component

import objc
from AppKit import (
    NSApplication,
    NSApplicationActivationPolicyRegular,
    NSBackingStoreBuffered,
    NSMenu,
    NSMenuItem,
    NSProcessInfo,
    NSWindow,
    NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable,
    NSWindowStyleMaskResizable,
    NSWindowStyleMaskTitled,
)
from Foundation import NSMakeRect, NSObject
from PyObjCTools import AppHelper


# --------------------------------------------------------------------------
# 应用代理类
# --------------------------------------------------------------------------
class MacUIAppDelegate(NSObject):
    """macUI 应用代理 - 遵循最佳实践"""

    def init(self):
        self = objc.super(MacUIAppDelegate, self).init()
        if self is None:
            return None
        self.window_controllers = []
        return self

    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成后的回调"""
        # 子类可以重写此方法来创建窗口

    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """最后一个窗口关闭时终止应用"""
        return True

    def add_window_controller(self, controller):
        """添加窗口控制器"""
        self.window_controllers.append(controller)


class MacUIApp:
    """macUI 应用程序主类 - 遵循 PyObjC 最佳实践"""

    def __init__(self, app_name: str = "MacUI App"):
        self.app_name = app_name
        self._windows = []
        self._app_instance = None
        self._delegate = None
        self._setup_application()

    def _setup_application(self):
        """设置 NSApplication 实例 - 遵循最佳实践"""
        with objc.autorelease_pool():
            self._app_instance = NSApplication.sharedApplication()

            # 要点 1: 设置激活策略
            self._app_instance.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            print(f"Application activation policy set for: {self.app_name}")

            # 要点 2: 创建最小化菜单栏
            self._create_menu_bar()
            print("Minimal menu bar created")

            # 要点 4: 创建应用代理
            self._delegate = MacUIAppDelegate.alloc().init()
            self._app_instance.setDelegate_(self._delegate)
            print("App delegate set")

    def _create_menu_bar(self):
        """创建最小化菜单栏"""
        # 创建主菜单栏
        menubar = NSMenu.alloc().init()
        app_menu_item = NSMenuItem.alloc().init()
        menubar.addItem_(app_menu_item)
        self._app_instance.setMainMenu_(menubar)

        # 创建应用主菜单
        app_menu = NSMenu.alloc().init()
        app_name = NSProcessInfo.processInfo().processName() or self.app_name

        # 创建退出菜单项
        quit_title = f"Quit {app_name}"
        quit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            quit_title, "terminate:", "q"
        )
        app_menu.addItem_(quit_menu_item)
        app_menu_item.setSubmenu_(app_menu)

    def create_window(
        self,
        title: str = "Window",
        size: Tuple[int, int] = (800, 600),
        resizable: bool = True,
        closable: bool = True,
        miniaturizable: bool = True,
        content: Optional[Component] = None
    ) -> "Window":
        """创建新窗口
        
        Args:
            title: 窗口标题
            size: 窗口大小 (width, height)
            resizable: 是否可调整大小
            closable: 是否可关闭
            miniaturizable: 是否可最小化
            content: 窗口内容组件
        
        Returns:
            Window 实例
        """
        window = Window(
            title=title,
            size=size,
            resizable=resizable,
            closable=closable,
            miniaturizable=miniaturizable,
            content=content
        )
        self._windows.append(window)
        return window

    def run(self):
        """运行应用程序主循环 - 使用 AppHelper 最佳实践"""
        # 激活应用，使其成为焦点
        self._app_instance.activateIgnoringOtherApps_(True)
        print(f"Starting {self.app_name} with AppHelper...")

        # 要点 3: 使用 AppHelper 运行事件循环
        AppHelper.runEventLoop(installInterrupt=True)

    def quit(self):
        """退出应用程序"""
        self._app_instance.terminate_(None)

    def get_delegate(self) -> MacUIAppDelegate:
        """获取应用代理"""
        return self._delegate


class Window:
    """macUI 窗口类"""

    def __init__(
        self,
        title: str = "Window",
        size: Tuple[int, int] = (800, 600),
        position: Optional[Tuple[int, int]] = None,
        resizable: bool = True,
        closable: bool = True,
        miniaturizable: bool = True,
        content: Optional[Component] = None,
        on_close: Optional[Callable[[], None]] = None
    ):
        self.title = title
        self.size = size
        self.position = position
        self.resizable = resizable
        self.closable = closable
        self.miniaturizable = miniaturizable
        self.content = content
        self.on_close = on_close

        self._window_instance = None
        self._controller = None
        self._setup_window()

    def _setup_window(self):
        """设置 NSWindow 实例"""
        # 计算窗口位置
        x, y = self.position if self.position else (100, 100)
        width, height = self.size

        # 创建窗口框架
        window_rect = NSMakeRect(x, y, width, height)

        # 设置窗口样式
        style_mask = NSWindowStyleMaskTitled
        if self.closable:
            style_mask |= NSWindowStyleMaskClosable
        if self.miniaturizable:
            style_mask |= NSWindowStyleMaskMiniaturizable
        if self.resizable:
            style_mask |= NSWindowStyleMaskResizable

        # 创建窗口实例
        self._window_instance = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect, style_mask, NSBackingStoreBuffered, False
        )

        # 设置窗口属性
        self._window_instance.setTitle_(self.title)

        # 如果没有指定位置，居中显示
        if not self.position:
            self._window_instance.center()

        # 设置内容视图
        if self.content:
            content_view = self.content.get_view()
            if content_view:
                self._window_instance.setContentView_(content_view)

        # 设置窗口委托 (用于处理关闭事件等)
        if self.on_close:
            delegate = WindowDelegate.alloc().init()
            delegate.on_close = self.on_close
            self._window_instance.setDelegate_(delegate)

    def show(self):
        """显示窗口"""
        if self._window_instance:
            self._window_instance.makeKeyAndOrderFront_(None)

    def hide(self):
        """隐藏窗口"""
        if self._window_instance:
            self._window_instance.orderOut_(None)

    def close(self):
        """关闭窗口"""
        if self._window_instance:
            self._window_instance.close()

        # 执行关闭回调
        if self.on_close:
            try:
                self.on_close()
            except Exception as e:
                print(f"Window close callback error: {e}")

    def set_title(self, new_title: str):
        """设置窗口标题"""
        self.title = new_title
        if self._window_instance:
            self._window_instance.setTitle_(new_title)

    def set_size(self, width: int, height: int):
        """设置窗口大小"""
        self.size = (width, height)
        if self._window_instance:
            current_frame = self._window_instance.frame()
            new_frame = NSMakeRect(current_frame.origin.x, current_frame.origin.y, width, height)
            self._window_instance.setFrame_display_(new_frame, True)

    def set_content(self, content: Component):
        """设置窗口内容"""
        self.content = content
        if self._window_instance:
            content_view = content.get_view()
            if content_view:
                self._window_instance.setContentView_(content_view)


# 窗口委托类 (用于处理窗口事件)
class WindowDelegate(NSObject):
    """窗口委托类"""

    def init(self):
        self = objc.super(WindowDelegate, self).init()
        if self is None:
            return None
        self.on_close = None
        return self

    def windowWillClose_(self, notification):
        """窗口即将关闭时的回调"""
        if self.on_close:
            try:
                self.on_close()
            except Exception as e:
                print(f"Window delegate close callback error: {e}")

    def windowDidResize_(self, notification):
        """窗口大小改变时的回调"""

    def windowDidMove_(self, notification):
        """窗口位置改变时的回调"""


# 便捷函数
def create_app(name: str = "MacUI App") -> MacUIApp:
    """创建 macUI 应用程序"""
    return MacUIApp(name)


def create_window(
    title: str = "Window",
    size: Tuple[int, int] = (800, 600),
    content: Optional[Component] = None,
    **kwargs
) -> Window:
    """创建窗口的便捷函数"""
    return Window(title=title, size=size, content=content, **kwargs)
