#!/usr/bin/env python3
"""Minimal Button Click Debug Test
最小化按钮点击调试测试 - 排除布局复杂性
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("button_test")
except ImportError:
    import logging
    debug_logger = logging.getLogger("button_test")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class ButtonTestApp(Component):
    """极简按钮测试应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        debug_logger.info("🧪 ButtonTestApp初始化")
    
    def simple_click_handler(self):
        """最简单的点击处理器"""
        debug_logger.info("🎉 ===== SIMPLE CLICK HANDLER SUCCESS! =====")
        old_count = self.click_count.value
        new_count = old_count + 1
        debug_logger.info(f"📊 点击次数: {old_count} -> {new_count}")
        self.click_count.value = new_count
        debug_logger.info("🎉 ===== CLICK HANDLER COMPLETED! =====")
    
    def test_large_button_click(self):
        """大按钮点击处理器"""
        debug_logger.info("🎉 ===== LARGE BUTTON CLICK SUCCESS! =====")
        debug_logger.info("📏 大按钮测试成功 - 这个按钮有更大的点击区域")
    
    def mount(self):
        """挂载测试应用"""
        debug_logger.info("🔧 开始挂载ButtonTestApp...")
        
        # 计数显示标签
        count_label = Label("点击次数: 0")
        
        # 响应式更新计数显示
        def update_count():
            count = self.click_count.value
            count_label.setStringValue_(f"点击次数: {count}")
            debug_logger.info(f"📊 计数标签已更新: {count}")
        
        self.create_effect(update_count)
        
        # 创建测试按钮 - 使用不同尺寸和位置
        small_button = Button(
            "小按钮",
            on_click=self.simple_click_handler,
            frame=(0, 0, 80, 30)
        )
        
        medium_button = Button(
            "中等按钮",
            on_click=self.simple_click_handler,
            frame=(0, 0, 120, 40)
        )
        
        large_button = Button(
            "大按钮（推荐点击）",
            on_click=self.test_large_button_click,
            frame=(0, 0, 200, 50)
        )
        
        # 固定位置按钮（不依赖Auto Layout）
        fixed_button = Button(
            "固定位置按钮",
            on_click=lambda: debug_logger.info("🎯 固定位置按钮被点击！"),
            frame=(20, 20, 150, 40)
        )
        
        debug_logger.info("🔧 所有按钮已创建")
        
        # 创建简单垂直布局
        layout = VStack(
            children=[
                Label("🧪 最小化按钮点击测试"),
                Label("请点击下面的按钮测试点击功能："),
                count_label,
                small_button,
                medium_button,
                large_button,
                fixed_button,
                Label("如果看到点击成功日志，说明按钮工作正常"),
                Label("如果没有日志输出，说明存在点击问题")
            ],
            spacing=10,
            alignment="center"
        )
        
        debug_logger.info("🔧 VStack布局已创建")
        return layout


def main():
    """主函数 - 最小化测试环境"""
    debug_logger.info("🚀 启动按钮点击调试测试")
    debug_logger.info("=" * 50)
    debug_logger.info("🎯 测试目标:")
    debug_logger.info("   1. 验证按钮点击是否工作")
    debug_logger.info("   2. 检查不同尺寸按钮的可点击性")
    debug_logger.info("   3. 对比VStack布局vs固定位置按钮")
    debug_logger.info("   4. 确认debug日志输出")
    debug_logger.info("=" * 50)
    
    # 创建应用
    app = create_app("Button Click Debug Test")
    
    # 创建测试组件
    test_app = ButtonTestApp()
    
    # 创建窗口 - 使用适中尺寸
    window = create_window(
        title="按钮点击调试测试",
        size=(600, 500),
        content=test_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ 按钮点击测试应用已启动!")
    debug_logger.info("🎯 请点击各个按钮，观察日志输出!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        # 如果AppHelper不可用，使用NSApp运行循环
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()