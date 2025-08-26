
```
PyObjC命令行启动最佳实践文档摘要

🎯 核心4要点 (最少token版本)

1. 激活策略: app.setActivationPolicy_(NSApplicationActivationPolicyRegular) - 让应用获得前台焦点和Dock图标
2. 菜单栏: 创建最小菜单栏含退出功能 - macOS要求完整应用必须有菜单
menubar = NSMenu.alloc().init()
quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit App", "terminate:", "q")
3. AppHelper事件循环: AppHelper.runEventLoop(installInterrupt=True) - 替代NSApp.run()防止对象被垃圾回收
4. 分离架构: AppDelegate负责生命周期 + 窗口控制器负责UI逻辑 - 保持强引用链防止对象销毁

🔧 常见问题

- 窗口不显示 → 缺少激活策略或菜单栏
- 对象被回收 → 用AppHelper而非NSApp.run()
- 事件不响应 → 目标对象需要保持强引用

📝 模板结构

# AppDelegate处理应用生命周期
class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        self.window_controller = WindowController.alloc().init()

# WindowController处理UI和逻辑
class WindowController(NSObject):
    def show(self): # 创建窗口

# 主函数设置4要点后启动AppHelper

简记: 激活策略 + 菜单栏 + AppHelper + 分离架构 = 稳定的命令行PyObjC应用
```
