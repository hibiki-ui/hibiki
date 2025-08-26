#!/usr/bin/env python3
"""按钮点击专项诊断工具
专门调查按钮为什么不能点击的问题
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import VStack, HStack, Button, Label
from macui.core.component import Component
from macui.core.signal import Signal
from AppKit import NSView
from Foundation import NSMakePoint, NSPointInRect

# 导入MacUI日志系统
try:
    from macui.core.logging import get_logger
    debug_logger = get_logger("button_diag")
except ImportError:
    import logging
    debug_logger = logging.getLogger("button_diag")
    debug_logger.addHandler(logging.StreamHandler())
    debug_logger.setLevel(logging.INFO)


class ButtonDiagnostics(Component):
    """按钮点击诊断组件"""
    
    def __init__(self):
        super().__init__()
        self.test_results = Signal("等待测试...")
        self.click_count = Signal(0)
        debug_logger.info("🔧 ButtonDiagnostics初始化")
    
    def test_button_click(self, button_name):
        """测试按钮点击"""
        old_count = self.click_count.value
        new_count = old_count + 1
        self.click_count.value = new_count
        
        result = f"✅ {button_name} 点击成功! 计数: {old_count} -> {new_count}"
        self.test_results.value = result
        debug_logger.info(f"🎯 {result}")
        
        return True
    
    def analyze_button_hierarchy(self, button_view, test_point):
        """分析按钮的视图层级和点击能力"""
        debug_logger.info(f"\n🔍 ========== 按钮点击分析 ==========")
        
        # 1. 检查按钮基本信息
        button_frame = button_view.frame()
        debug_logger.info(f"🎯 按钮frame: ({button_frame.origin.x:.1f}, {button_frame.origin.y:.1f}, {button_frame.size.width:.1f}, {button_frame.size.height:.1f})")
        
        # 2. 检查按钮是否启用
        if hasattr(button_view, 'isEnabled'):
            enabled = button_view.isEnabled()
            debug_logger.info(f"🎯 按钮启用状态: {enabled}")
            if not enabled:
                debug_logger.error("❌ 按钮被禁用!")
        
        # 3. 检查按钮是否隐藏
        if hasattr(button_view, 'isHidden'):
            hidden = button_view.isHidden()
            debug_logger.info(f"🎯 按钮隐藏状态: {hidden}")
            if hidden:
                debug_logger.error("❌ 按钮被隐藏!")
        
        # 4. 检查按钮透明度
        if hasattr(button_view, 'alphaValue'):
            alpha = button_view.alphaValue()
            debug_logger.info(f"🎯 按钮透明度: {alpha:.2f}")
            if alpha < 0.1:
                debug_logger.error("❌ 按钮几乎透明!")
        
        # 5. 检查父视图链
        current_view = button_view
        level = 0
        debug_logger.info(f"🔍 父视图链分析:")
        
        while current_view and level < 10:
            view_name = current_view.__class__.__name__
            frame = current_view.frame()
            debug_logger.info(f"   层级 {level}: {view_name} frame=({frame.origin.x:.1f}, {frame.origin.y:.1f}, {frame.size.width:.1f}, {frame.size.height:.1f})")
            
            # 检查点是否在当前视图bounds内
            if test_point:
                bounds = current_view.bounds()
                point_in_bounds = NSPointInRect(test_point, bounds)
                debug_logger.info(f"   层级 {level}: 测试点在bounds内: {point_in_bounds}")
                
                if not point_in_bounds and level > 0:
                    debug_logger.error(f"❌ 层级 {level} 测试点超出bounds!")
                    break
            
            # 移动到父视图
            if hasattr(current_view, 'superview') and current_view.superview():
                current_view = current_view.superview()
                level += 1
            else:
                debug_logger.info(f"   到达根视图，层级总数: {level + 1}")
                break
        
        # 6. 检查target和action
        if hasattr(button_view, 'target') and hasattr(button_view, 'action'):
            target = button_view.target()
            action = button_view.action()
            debug_logger.info(f"🎯 Target: {target.__class__.__name__ if target else 'None'}")
            debug_logger.info(f"🎯 Action: {action}")
            
            if not target:
                debug_logger.error("❌ 按钮没有target!")
            if not action:
                debug_logger.error("❌ 按钮没有action!")
        
        debug_logger.info(f"🔍 ========== 分析完毕 ==========\n")
    
    def mount(self):
        """挂载诊断应用"""
        debug_logger.info("🔧 开始挂载按钮诊断应用...")
        
        # 结果显示标签
        results_label = Label("等待测试...")
        count_label = Label("点击计数: 0")
        
        def update_results():
            results_label.setStringValue_(self.test_results.value)
        
        def update_count():
            count_label.setStringValue_(f"点击计数: {self.click_count.value}")
        
        self.create_effect(update_results)
        self.create_effect(update_count)
        
        # 测试按钮组 - 使用更大的间距确保分离
        debug_logger.info("🔧 创建测试按钮...")
        
        test_button1 = Button("测试按钮1", on_click=lambda: self.test_button_click("测试按钮1"))
        test_button2 = Button("测试按钮2", on_click=lambda: self.test_button_click("测试按钮2"))  
        test_button3 = Button("简单测试", on_click=lambda: self.test_button_click("简单测试"))
        
        # 创建诊断按钮 - 点击后分析第一个按钮
        def run_diagnostics():
            debug_logger.info("🔍 开始按钮诊断...")
            self.test_results.value = "🔍 正在分析按钮..."
            
            # 获取第一个测试按钮的视图
            if hasattr(test_button1, 'get_view'):
                button_view = test_button1.get_view()
            else:
                button_view = test_button1
            
            # 分析按钮
            button_frame = button_view.frame()
            test_point = NSMakePoint(
                button_frame.origin.x + button_frame.size.width / 2,
                button_frame.origin.y + button_frame.size.height / 2
            )
            
            self.analyze_button_hierarchy(button_view, test_point)
            self.test_results.value = "✅ 诊断完成，请查看控制台日志"
        
        diagnostic_button = Button("🔍 诊断按钮问题", on_click=run_diagnostics)
        
        # 按钮行 - 使用更大间距
        button_row = HStack(
            children=[test_button1, test_button2, test_button3],
            spacing=30,  # 更大间距
            alignment="center"
        )
        
        # 主布局
        main_layout = VStack(
            children=[
                Label("🔧 按钮点击专项诊断"),
                Label("=" * 60),
                Label("✅ 如果下面的按钮能点击，说明基本功能正常"),
                Label(""),
                button_row,
                Label(""),
                diagnostic_button,
                Label(""),
                results_label,
                count_label,
                Label(""),
                Label("🎯 请点击按钮测试，然后点击诊断按钮查看详细分析")
            ],
            spacing=20,
            alignment="center"
        )
        
        return main_layout


def main():
    """主函数"""
    debug_logger.info("🚀 启动按钮点击专项诊断")
    debug_logger.info("==" * 40)
    debug_logger.info("🎯 诊断目标:")
    debug_logger.info("   1. 测试按钮是否能正常点击")
    debug_logger.info("   2. 分析按钮点击失败的具体原因")
    debug_logger.info("   3. 检查视图层级和hitTest路径")
    debug_logger.info("   4. 验证target和action设置")
    debug_logger.info("==" * 40)
    
    # 创建应用
    app = create_app("Button Click Diagnostics")
    
    # 创建诊断组件
    diagnostics_app = ButtonDiagnostics()
    
    # 创建窗口 - 使用较小尺寸确保简洁
    window = create_window(
        title="按钮点击专项诊断",
        size=(500, 400),
        content=diagnostics_app
    )
    
    # 显示窗口
    window.show()
    
    debug_logger.info("✅ 按钮诊断应用已启动!")
    debug_logger.info("🎯 请测试按钮点击功能，然后使用诊断按钮分析问题!")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()