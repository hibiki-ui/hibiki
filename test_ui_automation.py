#!/usr/bin/env python3
"""
UI自动化测试 - 验证UI是否真正显示并可交互
包含自动化点击测试、文本输入测试和位置检测
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.signal import Signal
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack, ModernHStack
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSMakeRect
from AppKit import NSView, NSButton, NSTextField
import objc

class AutomationTestApp(Component):
    """自动化测试应用 - 验证UI显示和交互"""
    
    def __init__(self):
        super().__init__()
        print("🤖 自动化测试应用初始化...")
        
        # 测试用的信号
        self.title = Signal("🧪 UI自动化测试")
        self.counter = Signal(0)
        self.input_text = Signal("初始文本")
        self.test_log = []
        
        # 控件引用(用于自动化测试)
        self.test_button = None
        self.test_label = None
        self.test_text_field = None
        self.container_view = None
        
    def mount(self):
        """创建测试界面"""
        print("🏗️ 开始创建测试界面...")
        
        # 创建标题标签
        title_label = ModernLabel(
            text=self.title,
            width=300,
            height=30
        )
        
        # 创建计数器显示标签
        counter_label = ModernLabel(
            text=self.counter.value,  # 使用computed会更好，但先简化
            width=200,
            height=30
        )
        self.test_label = counter_label
        
        # 绑定按钮点击事件
        def on_button_click():
            self.counter.value += 1
            print(f"🔥 按钮被点击! 计数器: {self.counter.value}")
            self.test_log.append(f"button_clicked_{self.counter.value}")
            # 更新标签显示
            if hasattr(self.test_label, '_nsview'):
                self.test_label._nsview.setStringValue_(f"点击次数: {self.counter.value}")
        
        # 创建测试按钮 - 直接传入点击回调
        test_button = ModernButton(
            title="点击测试",
            on_click=on_button_click,
            width=120,
            height=32
        )
        self.test_button = test_button
        
        # 创建文本输入框
        text_field = ModernTextField(
            value=self.input_text,
            width=200,
            height=24
        )
        self.test_text_field = text_field
        
        # 创建布局容器
        main_container = ModernVStack(
            children=[
                title_label,
                counter_label,
                ModernHStack(children=[test_button, text_field], spacing=10),
            ],
            width=400,
            height=150,
            spacing=10,
            padding=20
        )
        
        view = main_container.get_view()
        self.container_view = view
        
        print("✅ 测试界面创建完成")
        
        # 启动自动化测试定时器
        self._schedule_automation_tests()
        
        return view
    
    def _schedule_automation_tests(self):
        """安排自动化测试"""
        print("⏰ 安排自动化测试定时器...")
        
        # 1秒后检查UI状态
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, 'checkUIStatus:', None, False
        )
        
        # 2秒后测试按钮点击
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            2.0, self, 'testButtonClick:', None, False
        )
        
        # 3秒后测试文本输入
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            3.0, self, 'testTextInput:', None, False
        )
        
        # 4秒后输出最终测试结果
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            4.0, self, 'outputTestResults:', None, False
        )
    
    @objc.typedSelector(b'v@:@')
    def checkUIStatus_(self, timer):
        """检查UI状态"""
        print("🔍 === UI状态检查 ===")
        
        if not self.container_view:
            print("❌ 容器视图不存在")
            return
            
        # 检查容器视图状态
        frame = self.container_view.frame()
        print(f"📦 容器视图 frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
        print(f"🪟 是否有窗口: {self.container_view.window() is not None}")
        print(f"👁️ 是否隐藏: {self.container_view.isHidden()}")
        print(f"🌳 子视图数量: {len(list(self.container_view.subviews()))}")
        
        # 检查子视图
        subviews = list(self.container_view.subviews())
        for i, subview in enumerate(subviews):
            subframe = subview.frame()
            print(f"   子视图{i}: {type(subview).__name__} frame=({subframe.origin.x}, {subframe.origin.y}, {subframe.size.width}, {subframe.size.height})")
        
        # 如果有窗口，说明UI已显示
        if self.container_view.window():
            print("✅ UI已成功显示在窗口中!")
            self.test_log.append("ui_displayed_success")
        else:
            print("❌ UI未显示在窗口中")
            self.test_log.append("ui_display_failed")
    
    @objc.typedSelector(b'v@:@')
    def testButtonClick_(self, timer):
        """测试按钮点击"""
        print("🖱️ === 自动化按钮点击测试 ===")
        
        if not self.test_button or not hasattr(self.test_button, '_nsview'):
            print("❌ 测试按钮不存在")
            return
        
        button_view = self.test_button._nsview
        if not isinstance(button_view, NSButton):
            print(f"❌ 按钮视图类型错误: {type(button_view)}")
            return
        
        # 检查按钮状态
        frame = button_view.frame()
        print(f"🔘 按钮 frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
        print(f"🔘 按钮标题: {button_view.title()}")
        print(f"🔘 按钮是否启用: {button_view.isEnabled()}")
        
        # 记录点击前的计数器值
        before_count = self.counter.value
        print(f"🔢 点击前计数器: {before_count}")
        
        # 模拟按钮点击
        try:
            button_view.performClick_(None)
            print("🎯 执行了按钮点击")
            
            # 检查点击后的状态
            after_count = self.counter.value
            print(f"🔢 点击后计数器: {after_count}")
            
            if after_count > before_count:
                print("✅ 按钮点击事件响应成功!")
                self.test_log.append("button_click_success")
            else:
                print("❌ 按钮点击事件未响应")
                self.test_log.append("button_click_failed")
                
        except Exception as e:
            print(f"❌ 按钮点击测试异常: {e}")
            self.test_log.append("button_click_exception")
    
    @objc.typedSelector(b'v@:@') 
    def testTextInput_(self, timer):
        """测试文本输入"""
        print("⌨️ === 自动化文本输入测试 ===")
        
        if not self.test_text_field or not hasattr(self.test_text_field, '_nsview'):
            print("❌ 测试文本框不存在")
            return
        
        text_field_view = self.test_text_field._nsview
        if not isinstance(text_field_view, NSTextField):
            print(f"❌ 文本框视图类型错误: {type(text_field_view)}")
            return
        
        # 检查文本框状态
        frame = text_field_view.frame()
        print(f"📝 文本框 frame: ({frame.origin.x}, {frame.origin.y}, {frame.size.width}, {frame.size.height})")
        print(f"📝 当前文本: '{text_field_view.stringValue()}'")
        print(f"📝 是否可编辑: {text_field_view.isEditable()}")
        
        # 设置新文本
        test_text = f"自动测试文本_{self.counter.value}"
        try:
            text_field_view.setStringValue_(test_text)
            print(f"📝 设置文本: '{test_text}'")
            
            # 验证文本是否设置成功
            current_text = text_field_view.stringValue()
            if current_text == test_text:
                print("✅ 文本输入测试成功!")
                self.test_log.append("text_input_success")
            else:
                print(f"❌ 文本输入失败，期望:'{test_text}', 实际:'{current_text}'")
                self.test_log.append("text_input_failed")
                
        except Exception as e:
            print(f"❌ 文本输入测试异常: {e}")
            self.test_log.append("text_input_exception")
    
    @objc.typedSelector(b'v@:@')
    def outputTestResults_(self, timer):
        """输出最终测试结果"""
        print("📊 === 自动化测试结果报告 ===")
        print(f"📋 测试日志: {self.test_log}")
        
        success_tests = [log for log in self.test_log if 'success' in log]
        failed_tests = [log for log in self.test_log if 'failed' in log or 'exception' in log]
        
        print(f"✅ 成功测试: {len(success_tests)} 项")
        for test in success_tests:
            print(f"   ✓ {test}")
            
        print(f"❌ 失败测试: {len(failed_tests)} 项")
        for test in failed_tests:
            print(f"   ✗ {test}")
        
        if len(success_tests) >= 3:  # ui_displayed + button_click + text_input
            print("🎉 UI自动化测试全面通过! macUI v3.0工作正常!")
        else:
            print("⚠️ UI自动化测试存在问题，需要进一步调试")

def main():
    print("🚀 启动UI自动化测试...")
    
    app = MacUIApp("UI Automation Test")
    test_component = AutomationTestApp()
    
    # 创建窗口
    app.create_window(
        title="UI自动化测试",
        size=(500, 250),
        content=test_component
    )
    
    print("🪟 窗口创建完成，启动应用...")
    app.run()

if __name__ == "__main__":
    main()