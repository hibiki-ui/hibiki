#!/usr/bin/env python3
"""测试VStack修复效果的简化版本"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("vstack_test")
except ImportError:
    import logging
    debug_logger = logging.getLogger("vstack_test")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class VStackFixTest(Component):
    """VStack修复测试应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        debug_logger.info("🔧 VStackFixTest初始化")
    
    def button_click_handler(self, button_name):
        """测试按钮点击"""
        old_count = self.click_count.value
        new_count = old_count + 1
        self.click_count.value = new_count
        debug_logger.info(f"✅ {button_name}点击成功！计数: {old_count} -> {new_count}")
    
    def mount(self):
        """挂载测试应用"""
        debug_logger.info("🔧 开始挂载VStack修复测试...")
        
        # 计数显示
        count_label = Label("点击计数: 0")
        
        def update_count():
            count = self.click_count.value
            count_label.setStringValue_(f"点击计数: {count}")
        
        self.create_effect(update_count)
        
        # 测试1：基本VStack与HStack嵌套
        debug_logger.info("🔧 创建基本嵌套布局测试...")
        
        # HStack按钮组
        button_row = HStack(
            children=[
                Button("按钮1", on_click=lambda: self.button_click_handler("按钮1")),
                Button("按钮2", on_click=lambda: self.button_click_handler("按钮2")),
                Button("按钮3", on_click=lambda: self.button_click_handler("按钮3"))
            ],
            spacing=15,
            alignment="center"
        )
        
        # 彩色标签系列 - 测试文本是否重叠
        color_labels = VStack(
            children=[
                Label("🔴 红色标签 - 测试文本间距"),
                Label("🟡 黄色标签 - 测试文本分离"),
                Label("🟢 绿色标签 - 测试垂直布局"),
                Label("🔵 蓝色标签 - 测试间距效果"),
                Label("🟣 紫色标签 - 测试文本重叠修复")
            ],
            spacing=20,  # 增大间距
            alignment="center"
        )
        
        # 主布局
        main_layout = VStack(
            children=[
                Label("🧪 VStack修复效果测试"),
                Label("=" * 50),
                Label("✅ 如果下面的内容没有重叠，说明修复成功"),
                Label(""),
                Label("🔸 按钮测试区域："),
                button_row,
                Label(""),
                Label("🔸 文本间距测试区域："),
                color_labels,
                Label(""),
                count_label,
                Label("🎯 点击按钮测试交互功能")
            ],
            spacing=25,  # 使用较大间距
            alignment="center"
        )
        
        return main_layout


def main():
    """主函数"""
    debug_logger.info("🚀 启动VStack修复测试")
    debug_logger.info("==" * 30)
    debug_logger.info("🎯 测试目标:")
    debug_logger.info("   1. 验证VStack文本不重叠")
    debug_logger.info("   2. 验证HStack按钮正常布局")
    debug_logger.info("   3. 验证嵌套布局工作正常")
    debug_logger.info("   4. 验证按钮点击功能")
    debug_logger.info("==" * 30)
    
    # 创建应用
    app = create_app("VStack Fix Test")
    
    # 创建测试组件
    test_app = VStackFixTest()
    
    # 创建窗口
    window = create_window(
        title="VStack修复测试",
        size=(600, 500),
        content=test_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ VStack修复测试应用已启动!")
    debug_logger.info("🎯 请观察文本间距和按钮位置!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()