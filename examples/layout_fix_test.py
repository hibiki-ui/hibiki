#!/usr/bin/env python3
"""NSStackView布局修复测试
专门修复按钮超出边界和文本重叠问题
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal

# 导入调试工具
try:
    from advanced_ui_debugging import ViewHierarchyDebugger, debug_ui_comprehensive
    DEBUG_AVAILABLE = True
except ImportError:
    DEBUG_AVAILABLE = False

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("layout_fix")
except ImportError:
    import logging
    debug_logger = logging.getLogger("layout_fix")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class LayoutFixTest(Component):
    """布局修复测试应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        debug_logger.info("🔧 LayoutFixTest初始化")
    
    def button_click_handler(self, button_name):
        """测试按钮点击"""
        old_count = self.click_count.value
        new_count = old_count + 1
        self.click_count.value = new_count
        debug_logger.info(f"✅ {button_name}点击成功！计数: {old_count} -> {new_count}")
    
    def mount(self):
        """挂载测试应用"""
        debug_logger.info("🔧 开始挂载布局修复测试...")
        
        # 计数显示
        count_label = Label("点击计数: 0")
        
        def update_count():
            count = self.click_count.value
            count_label.setStringValue_(f"点击计数: {count}")
        
        self.create_effect(update_count)
        
        # 🎯 修复方案1：显式设置按钮frame，避免NSStackView布局计算错误
        debug_logger.info("🔧 创建固定位置按钮（绕过NSStackView）...")
        
        fixed_button1 = Button(
            "固定按钮1", 
            on_click=lambda: self.button_click_handler("固定按钮1"),
            frame=(50, 200, 100, 32)   # 明确的正坐标
        )
        
        fixed_button2 = Button(
            "固定按钮2", 
            on_click=lambda: self.button_click_handler("固定按钮2"),
            frame=(170, 200, 100, 32)  # 明确的正坐标
        )
        
        fixed_button3 = Button(
            "固定按钮3", 
            on_click=lambda: self.button_click_handler("固定按钮3"),
            frame=(290, 200, 100, 32)  # 明确的正坐标
        )
        
        # 🎯 修复方案2：使用较大的spacing来避免重叠
        debug_logger.info("🔧 创建增大间距的HStack...")
        
        safe_hstack_buttons = HStack(
            children=[
                Button("HStack按钮1", on_click=lambda: self.button_click_handler("HStack按钮1")),
                Button("HStack按钮2", on_click=lambda: self.button_click_handler("HStack按钮2")),
                Button("HStack按钮3", on_click=lambda: self.button_click_handler("HStack按钮3"))
            ],
            spacing=30,  # 增大间距到30像素
            alignment="center"
        )
        
        # 🎯 修复方案3：简化的VStack，避免复杂嵌套
        debug_logger.info("🔧 创建简化VStack布局...")
        
        # 使用较大的spacing避免文本重叠
        main_layout = VStack(
            children=[
                Label("🔧 NSStackView布局修复测试"),
                Label("=" * 40),
                Label("✅ 固定位置按钮测试区域："),
                fixed_button1,
                fixed_button2, 
                fixed_button3,
                Label("=" * 40),
                Label("✅ 增大间距HStack测试区域："),
                safe_hstack_buttons,
                Label("=" * 40),
                count_label,
                Label("🎯 如果按钮能正常点击，说明修复成功")
            ],
            spacing=20,  # 使用较大的间距避免重叠
            alignment="center"
        )
        
        # 延迟调试分析
        if DEBUG_AVAILABLE:
            def delayed_debug():
                import time
                time.sleep(1.5)
                debug_logger.info("🔍 开始布局修复后的调试分析...")
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
    debug_logger.info("🚀 启动NSStackView布局修复测试")
    debug_logger.info("=" * 60)
    debug_logger.info("🎯 测试目标:")
    debug_logger.info("   1. 修复按钮超出父视图边界问题")
    debug_logger.info("   2. 避免文本重叠问题")
    debug_logger.info("   3. 验证按钮点击功能")
    debug_logger.info("   4. 对比不同布局方案的效果")
    debug_logger.info("=" * 60)
    
    # 创建应用
    app = create_app("Layout Fix Test")
    
    # 创建测试组件
    test_app = LayoutFixTest()
    
    # 创建窗口
    window = create_window(
        title="NSStackView布局修复测试",
        size=(500, 600),
        content=test_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ 布局修复测试应用已启动!")
    debug_logger.info("🎯 请测试各个按钮的点击功能!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()