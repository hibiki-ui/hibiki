#!/usr/bin/env python3
"""大窗口按钮测试 - 测试1600x1200窗口中的按钮点击"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("large_window")
except ImportError:
    import logging
    debug_logger = logging.getLogger("large_window")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class LargeWindowTest(Component):
    """大窗口按钮测试"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        debug_logger.info("🔧 LargeWindowTest初始化")
    
    def button_click_handler(self, button_name):
        """测试按钮点击"""
        old_count = self.click_count.value
        new_count = old_count + 1
        self.click_count.value = new_count
        debug_logger.info(f"✅ {button_name}点击成功！计数: {old_count} -> {new_count}")
    
    def mount(self):
        """挂载测试应用"""
        debug_logger.info("🔧 开始挂载大窗口测试...")
        
        # 计数显示
        count_label = Label("点击计数: 0")
        
        def update_count():
            count = self.click_count.value
            count_label.setStringValue_(f"点击计数: {count}")
        
        self.create_effect(update_count)
        
        # 模拟主题展示的按钮布局
        theme_buttons = HStack(
            children=[
                Button("系统增强", on_click=lambda: self.button_click_handler("系统增强")),
                Button("开发者", on_click=lambda: self.button_click_handler("开发者")),
                Button("海洋风", on_click=lambda: self.button_click_handler("海洋风")),
                Button("日落橙", on_click=lambda: self.button_click_handler("日落橙"))
            ],
            spacing=16,  # 和主题展示一样的间距
            alignment="center"
        )
        
        # 测试按钮
        test_buttons = HStack(
            children=[
                Button("🎬 测试动画", on_click=lambda: self.button_click_handler("测试动画")),
                Button("🔬 测试点击反馈", on_click=lambda: self.button_click_handler("点击反馈"))
            ],
            spacing=12,
            alignment="center"
        )
        
        # 窗口信息显示
        window_info = Label(f"🪟 窗口尺寸: 1600x1200")
        layout_info = Label(f"📐 布局调试信息区域")
        
        # 主布局 - 模拟主题展示的结构
        main_layout = VStack(
            children=[
                Label("🎨 大窗口按钮测试"),
                Label("在1600x1200窗口中测试按钮点击"),
                Label(""),
                theme_buttons,
                Label(""),
                test_buttons,
                Label(""),
                count_label,
                Label(""),
                window_info,
                layout_info,
                Label(""),
                Label("🎯 如果按钮能点击，说明大窗口没有问题"),
                Label("🎯 如果按钮不能点击，说明是窗口尺寸相关问题")
            ],
            spacing=24,  # 和主题展示类似的间距
            alignment="center"
        )
        
        return main_layout


def main():
    """主函数"""
    debug_logger.info("🚀 启动大窗口按钮测试")
    debug_logger.info("==" * 30)
    debug_logger.info("🎯 测试目标:")
    debug_logger.info("   1. 验证1600x1200大窗口中的按钮能否点击")
    debug_logger.info("   2. 对比小窗口和大窗口的行为差异")
    debug_logger.info("   3. 查找窗口尺寸导致的点击问题")
    debug_logger.info("==" * 30)
    
    # 创建应用
    app = create_app("Large Window Test")
    
    # 创建测试组件
    test_app = LargeWindowTest()
    
    # 创建和主题展示一样的大窗口
    window = create_window(
        title="大窗口按钮测试 - 1600x1200",
        size=(1600, 1200),  # 和主题展示一样的尺寸
        content=test_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ 大窗口测试应用已启动!")
    debug_logger.info("🎯 请测试按钮点击功能!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()