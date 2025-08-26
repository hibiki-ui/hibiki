#!/usr/bin/env python3
"""测试修复版HStack的完整应用"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')
sys.path.insert(0, '/Users/david/david/app/macui/examples')

from macui.app import create_app, create_window
from macui.components import VStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal

# 导入修复的HStack
from hstack_fix_patch import create_fixed_hstack

# 导入调试工具
try:
    from advanced_ui_debugging import debug_ui_comprehensive
    DEBUG_AVAILABLE = True
except ImportError:
    DEBUG_AVAILABLE = False

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("test_fixed")
except ImportError:
    import logging
    debug_logger = logging.getLogger("test_fixed")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class TestFixedHStackApp(Component):
    """测试修复版HStack的应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        debug_logger.info("🧪 TestFixedHStackApp初始化")
    
    def button_click_handler(self, button_name):
        """按钮点击处理"""
        old_count = self.click_count.value
        new_count = old_count + 1
        self.click_count.value = new_count
        debug_logger.info(f"✅ {button_name}点击成功！计数: {old_count} -> {new_count}")
    
    def mount(self):
        """挂载应用"""
        debug_logger.info("🔧 挂载测试应用...")
        
        # 计数显示
        count_label = Label("点击计数: 0")
        
        def update_count():
            count = self.click_count.value
            count_label.setStringValue_(f"点击计数: {count}")
        
        self.create_effect(update_count)
        
        # 🎯 使用修复版HStack创建按钮行
        debug_logger.info("🔧 使用修复版HStack创建按钮...")
        
        # 创建按钮
        button1 = Button("修复按钮1", on_click=lambda: self.button_click_handler("修复按钮1"))
        button2 = Button("修复按钮2", on_click=lambda: self.button_click_handler("修复按钮2"))
        button3 = Button("修复按钮3", on_click=lambda: self.button_click_handler("修复按钮3"))
        
        # 使用修复版HStack - 直接返回NSStackView
        fixed_hstack_view = create_fixed_hstack(
            spacing=15,
            padding=15,
            alignment="center", 
            children=[button1, button2, button3],
            frame=None  # 让其自动调整大小
        )
        
        # 🔥 创建一个包装Component来使用修复的NSStackView
        class FixedHStackComponent(Component):
            def __init__(self, ns_stack_view):
                super().__init__()
                self.ns_view = ns_stack_view
            
            def get_view(self):
                return self.ns_view
        
        fixed_hstack_component = FixedHStackComponent(fixed_hstack_view)
        
        # 创建主布局（使用常规VStack）
        main_layout = VStack(
            children=[
                Label("🔧 修复版HStack测试"),
                Label("=" * 40),
                Label("✅ 如果按钮都在正坐标位置，说明修复成功"),
                fixed_hstack_component,  # 使用修复版HStack
                Label("=" * 40),
                count_label,
                Label("🎯 点击按钮测试功能")
            ],
            spacing=20,
            alignment="center"
        )
        
        # 延迟调试分析
        if DEBUG_AVAILABLE:
            def delayed_debug():
                import time
                time.sleep(2.0)
                debug_logger.info("🔍 开始修复后的调试分析...")
                try:
                    main_view = main_layout.get_view() if hasattr(main_layout, 'get_view') else main_layout
                    debug_ui_comprehensive(main_view)
                except Exception as e:
                    debug_logger.error(f"⚠️ 调试失败: {e}")
            
            import threading
            debug_thread = threading.Thread(target=delayed_debug)
            debug_thread.daemon = True  
            debug_thread.start()
        
        return main_layout


def main():
    """主函数"""
    debug_logger.info("🚀 启动修复版HStack测试")
    debug_logger.info("=" * 60)
    debug_logger.info("🎯 测试目标:")
    debug_logger.info("   1. 验证修复版HStack能正确布局按钮")
    debug_logger.info("   2. 确保所有按钮都在正坐标位置")
    debug_logger.info("   3. 验证按钮点击功能正常")
    debug_logger.info("   4. 对比修复前后的效果")
    debug_logger.info("=" * 60)
    
    # 创建应用
    app = create_app("Fixed HStack Test")
    
    # 创建测试组件
    test_app = TestFixedHStackApp()
    
    # 创建窗口
    window = create_window(
        title="修复版HStack测试",
        size=(500, 400),
        content=test_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ 修复版HStack测试应用已启动!")
    debug_logger.info("🎯 请观察按钮位置并测试点击功能!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()