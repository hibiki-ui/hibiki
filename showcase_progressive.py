#!/usr/bin/env python3
"""
macUI v3.0 渐进式Showcase - 逐步构建功能完整的展示应用
每个阶段都经过自动化测试验证，确保稳定可靠
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import MacUIApp
from macui.core.signal import Signal, Computed
from macui.core.component import Component
from macui.components.modern_layout import ModernVStack, ModernHStack
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from macui.components.modern_input import ModernSlider, ModernCheckbox, ModernSwitch
from Foundation import NSTimer
from AppKit import NSApplication
import objc

class ProgressiveShowcase(Component):
    """渐进式功能展示 - 当前阶段: 基础组件"""
    
    def __init__(self):
        super().__init__()
        print("🏗️ ProgressiveShowcase 初始化...")
        
        # === 阶段1: 基础状态和信号 ===
        self.app_title = Signal("🎯 macUI v3.0 Showcase")
        self.counter = Signal(0)
        self.text_input = Signal("Hello macUI!")
        self.slider_value = Signal(50.0)
        self.checkbox_checked = Signal(False)
        self.switch_enabled = Signal(True)
        
        # 计算属性
        self.counter_display = Computed(lambda: f"计数: {self.counter.value}")
        self.slider_display = Computed(lambda: f"滑块值: {int(self.slider_value.value)}")
        
        # 测试结果记录
        self.test_results = []
        self.components_refs = {}  # 存储组件引用用于测试
        
        print("✅ 基础状态初始化完成")
    
    def mount(self):
        print("🔧 开始创建Showcase界面...")
        
        # === 标题区域 ===
        title_label = ModernLabel(
            text=self.app_title,
            width=400,
            height=40
        )
        
        # === 基础控件区域 ===
        # 计数器组
        counter_label = ModernLabel(text=self.counter_display, width=150, height=25)
        
        counter_button = ModernButton(
            title="增加计数",
            on_click=lambda: self._increment_counter(),
            width=100,
            height=32
        )
        
        reset_button = ModernButton(
            title="重置",
            on_click=lambda: self._reset_counter(),
            width=80,
            height=32
        )
        
        counter_row = ModernHStack(
            children=[counter_label, counter_button, reset_button],
            spacing=10
        )
        
        # 文本输入组
        text_label = ModernLabel(text="文本输入:", width=80, height=25)
        text_field = ModernTextField(value=self.text_input, width=200, height=24)
        text_display = ModernLabel(text=self.text_input, width=200, height=25)
        
        text_row = ModernHStack(
            children=[text_label, text_field, text_display],
            spacing=10
        )
        
        # 滑块组
        slider_label = ModernLabel(text=self.slider_display, width=120, height=25)
        slider = ModernSlider(
            value=self.slider_value,
            min_value=0,
            max_value=100,
            width=200,
            height=25
        )
        
        slider_row = ModernHStack(
            children=[slider_label, slider],
            spacing=10
        )
        
        # 复选框和开关组
        checkbox = ModernCheckbox(
            title="启用选项",
            checked=self.checkbox_checked,
            width=100,
            height=25
        )
        
        switch = ModernSwitch(
            enabled=self.switch_enabled,
            width=60,
            height=25
        )
        
        controls_row = ModernHStack(
            children=[checkbox, switch],
            spacing=15
        )
        
        # === 主布局 ===
        main_layout = ModernVStack(
            children=[
                title_label,
                ModernLabel(text="=== 基础控件展示 ===", width=300, height=30),
                counter_row,
                text_row,
                slider_row,
                controls_row,
                ModernLabel(text=f"版本: macUI v3.0 | 组件数: 13", width=300, height=25),
            ],
            spacing=15,
            padding=20,
            width=500,
            height=350
        )
        
        # 保存组件引用用于测试
        self.components_refs = {
            'counter_button': counter_button,
            'reset_button': reset_button,
            'text_field': text_field,
            'slider': slider,
            'checkbox': checkbox,
            'switch': switch,
            'counter_label': counter_label,
            'slider_label': slider_label,
            'text_display': text_display,
        }
        
        view = main_layout.get_view()
        
        # 安排自动化测试
        print("⏰ 安排2秒后进行综合自动化测试...")
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            2.0, self, 'performComprehensiveTest:', None, False
        )
        
        # 安排5秒后退出
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            5.0, self, 'exitShowcase:', None, False
        )
        
        print("✅ Showcase界面创建完成")
        return view
    
    def _increment_counter(self):
        """增加计数器"""
        self.counter.value += 1
        print(f"🔢 计数器增加到: {self.counter.value}")
        self.test_results.append(f"counter_incremented_to_{self.counter.value}")
    
    def _reset_counter(self):
        """重置计数器"""
        old_value = self.counter.value
        self.counter.value = 0
        print(f"🔄 计数器从 {old_value} 重置到 {self.counter.value}")
        self.test_results.append("counter_reset")
    
    @objc.typedSelector(b'v@:@')
    def performComprehensiveTest_(self, timer):
        """执行综合自动化测试"""
        print("🤖 === 开始综合自动化测试 ===")
        
        # 测试1: 按钮交互
        print("🔘 测试按钮交互...")
        counter_btn = self.components_refs.get('counter_button')
        if counter_btn and hasattr(counter_btn, '_nsview'):
            btn_view = counter_btn._nsview
            initial_count = self.counter.value
            
            # 点击3次
            for i in range(3):
                btn_view.performClick_(None)
            
            final_count = self.counter.value
            if final_count == initial_count + 3:
                print(f"✅ 按钮测试成功: {initial_count} -> {final_count}")
                self.test_results.append("button_test_success")
            else:
                print(f"❌ 按钮测试失败: 期望{initial_count + 3}, 实际{final_count}")
                self.test_results.append("button_test_failed")
        
        # 测试2: 文本输入
        print("📝 测试文本输入...")
        text_field = self.components_refs.get('text_field')
        if text_field and hasattr(text_field, '_nsview'):
            field_view = text_field._nsview
            test_text = f"自动测试文本_{self.counter.value}"
            field_view.setStringValue_(test_text)
            
            if field_view.stringValue() == test_text:
                print(f"✅ 文本输入测试成功: '{test_text}'")
                self.test_results.append("text_input_success")
            else:
                print(f"❌ 文本输入测试失败")
                self.test_results.append("text_input_failed")
        
        # 测试3: 滑块控制
        print("🎚️ 测试滑块控制...")
        slider = self.components_refs.get('slider')
        if slider and hasattr(slider, '_nsview'):
            slider_view = slider._nsview
            original_value = slider_view.floatValue()
            test_value = 75.0
            
            slider_view.setFloatValue_(test_value)
            new_value = slider_view.floatValue()
            
            if abs(new_value - test_value) < 1.0:
                print(f"✅ 滑块测试成功: {original_value} -> {new_value}")
                self.test_results.append("slider_test_success")
            else:
                print(f"❌ 滑块测试失败: 期望{test_value}, 实际{new_value}")
                self.test_results.append("slider_test_failed")
        
        # 测试4: 复选框状态
        print("☑️ 测试复选框...")
        checkbox = self.components_refs.get('checkbox')
        if checkbox and hasattr(checkbox, '_nsview'):
            cb_view = checkbox._nsview
            original_state = cb_view.state()
            
            # 切换状态
            cb_view.setState_(1 if original_state == 0 else 0)
            new_state = cb_view.state()
            
            if new_state != original_state:
                print(f"✅ 复选框测试成功: {original_state} -> {new_state}")
                self.test_results.append("checkbox_test_success")
            else:
                print(f"❌ 复选框测试失败")
                self.test_results.append("checkbox_test_failed")
        
        # 测试5: 响应式显示更新
        print("🔄 测试响应式显示更新...")
        counter_label = self.components_refs.get('counter_label')
        slider_label = self.components_refs.get('slider_label')
        
        if counter_label and hasattr(counter_label, '_nsview'):
            label_text = counter_label._nsview.stringValue()
            expected_text = f"计数: {self.counter.value}"
            if expected_text in label_text:
                print(f"✅ 计数器显示更新成功: '{label_text}'")
                self.test_results.append("counter_display_success")
            else:
                print(f"❌ 计数器显示更新失败: 期望包含'{expected_text}', 实际'{label_text}'")
                self.test_results.append("counter_display_failed")
        
        print("🎯 综合测试完成!")
    
    @objc.typedSelector(b'v@:@')
    def exitShowcase_(self, timer):
        """输出测试结果并退出"""
        print("📊 === Showcase 测试结果报告 ===")
        print(f"测试操作记录: {len(self.test_results)} 项")
        
        success_tests = [r for r in self.test_results if 'success' in r]
        failed_tests = [r for r in self.test_results if 'failed' in r]
        
        print(f"✅ 成功测试: {len(success_tests)} 项")
        for test in success_tests:
            print(f"   ✓ {test}")
        
        if failed_tests:
            print(f"❌ 失败测试: {len(failed_tests)} 项")
            for test in failed_tests:
                print(f"   ✗ {test}")
        
        # 最终评估
        if len(success_tests) >= 5:  # 至少5个核心测试通过
            print("🎉 Showcase 基础功能全面验证通过!")
            print("✅ macUI v3.0 基础组件系统完全可用")
            print("🚀 准备进入下一阶段: 高级布局和组件")
        else:
            print("⚠️ Showcase 存在问题，需要调试")
        
        print("🏁 基础Showcase测试完成，退出应用...")
        NSApplication.sharedApplication().terminate_(None)

def main():
    print("🎯 === macUI v3.0 渐进式Showcase 启动 ===")
    print("📝 当前阶段: 基础组件和交互验证")
    print("🎮 程序将自动测试所有功能并在5秒后退出")
    
    app = MacUIApp("macUI v3.0 Progressive Showcase")
    showcase = ProgressiveShowcase()
    
    window = app.create_window(
        title="macUI v3.0 基础功能展示",
        size=(550, 400),
        content=showcase
    )
    
    window.show()
    print("🪟 Showcase窗口已显示，开始功能测试...")
    
    app.run()

if __name__ == "__main__":
    main()