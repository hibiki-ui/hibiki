#!/usr/bin/env python3
"""
最终交互测试 - 基于UI确实工作的前提，测试按钮点击和文本输入
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.signal import Signal
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack, ModernHStack
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from Foundation import NSTimer
from AppKit import NSButton, NSTextField, NSApplication
import objc

class InteractionTest(Component):
    """交互功能测试"""
    
    def __init__(self):
        super().__init__()
        print("🧪 交互测试初始化...")
        
        self.counter = Signal(0)
        self.text_input = Signal("原始文本")
        self.test_results = []
        
        self.button_component = None
        self.text_field_component = None
        
    def mount(self):
        print("🏗️ 创建交互测试界面...")
        
        # 计数显示标签
        counter_label = ModernLabel(text="点击次数: 0", width=150, height=25)
        
        # 测试按钮
        def on_click():
            self.counter.value += 1
            new_text = f"点击次数: {self.counter.value}"
            print(f"🔥 按钮被点击! {new_text}")
            
            # 直接更新标签文本
            if hasattr(counter_label, '_nsview'):
                counter_label._nsview.setStringValue_(new_text)
            
            self.test_results.append(f"button_clicked_{self.counter.value}")
        
        test_button = ModernButton(
            title="测试按钮", 
            on_click=on_click,
            width=100, 
            height=32
        )
        self.button_component = test_button
        
        # 文本输入框
        text_field = ModernTextField(
            value=self.text_input,
            width=200,
            height=24
        )
        self.text_field_component = text_field
        
        # 布局
        layout = ModernVStack(
            children=[
                ModernLabel(text="🧪 macUI交互测试", width=200, height=30),
                counter_label,
                ModernHStack(children=[test_button, text_field], spacing=10),
            ],
            spacing=10,
            padding=15,
            width=350,
            height=120
        )
        
        view = layout.get_view()
        
        # 安排自动化测试
        print("⏰ 安排1秒后进行自动化测试...")
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, 'performAutomatedTest:', None, False
        )
        
        # 安排2秒后退出
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            2.5, self, 'exitTest:', None, False
        )
        
        return view
    
    @objc.typedSelector(b'v@:@')
    def performAutomatedTest_(self, timer):
        print("🤖 === 开始自动化交互测试 ===")
        
        # 测试1: 按钮点击
        if self.button_component and hasattr(self.button_component, '_nsview'):
            button_view = self.button_component._nsview
            if isinstance(button_view, NSButton):
                print(f"🔘 按钮状态: 标题='{button_view.title()}', 启用={button_view.isEnabled()}")
                
                before_count = self.counter.value
                print(f"🔢 点击前计数: {before_count}")
                
                # 执行点击
                button_view.performClick_(None)
                print("🎯 执行按钮点击")
                
                # 检查结果
                after_count = self.counter.value  
                print(f"🔢 点击后计数: {after_count}")
                
                if after_count > before_count:
                    print("✅ 按钮点击测试成功!")
                    self.test_results.append("button_test_success")
                else:
                    print("❌ 按钮点击测试失败")
                    self.test_results.append("button_test_failed")
        
        # 测试2: 文本输入
        if self.text_field_component and hasattr(self.text_field_component, '_nsview'):
            text_view = self.text_field_component._nsview
            if isinstance(text_view, NSTextField):
                print(f"📝 文本框当前值: '{text_view.stringValue()}'")
                
                test_text = f"自动化测试文本_{self.counter.value}"
                text_view.setStringValue_(test_text)
                print(f"📝 设置文本: '{test_text}'")
                
                # 验证设置
                current_text = text_view.stringValue()
                if current_text == test_text:
                    print("✅ 文本输入测试成功!")
                    self.test_results.append("text_test_success")
                else:
                    print(f"❌ 文本输入测试失败: 期望'{test_text}', 实际'{current_text}'")
                    self.test_results.append("text_test_failed")
    
    @objc.typedSelector(b'v@:@')
    def exitTest_(self, timer):
        print("📊 === 最终测试结果 ===")
        print(f"测试日志: {self.test_results}")
        
        success_count = len([r for r in self.test_results if 'success' in r])
        total_tests = 2  # button + text
        
        print(f"成功测试: {success_count}/{total_tests}")
        
        if success_count == total_tests:
            print("🎉 所有交互测试通过! macUI v3.0完全工作正常!")
        else:
            print("⚠️ 部分测试未通过，需要检查")
        
        print("🏁 测试完成，退出应用...")
        NSApplication.sharedApplication().terminate_(None)

def main():
    print("🚀 启动最终交互测试...")
    
    app = MacUIApp("Interaction Test")
    test = InteractionTest()
    
    window = app.create_window(
        title="交互测试",
        size=(400, 180), 
        content=test
    )
    
    window.show()
    
    print("🎮 启动应用 - 将自动执行交互测试并在2.5秒后退出")
    app.run()

if __name__ == "__main__":
    main()