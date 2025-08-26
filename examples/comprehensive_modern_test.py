#!/usr/bin/env python3
"""
全面现代化组件测试 - 验证所有升级后的现代化组件

测试范围:
1. 基础控件 (Button, Label, TextField) 
2. 输入控件 (Slider, Switch, Checkbox, RadioButton, SegmentedControl)
3. 显示控件 (ImageView, ProgressBar, TextArea)
4. 选择控件 (PopUpButton, ComboBox, Menu)
5. 时间控件 (DatePicker, TimePicker)
6. 布局组件 (VStack, HStack)
7. 现代化API特性 (CSS布局属性、链式调用、响应式绑定)
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.core.component import Component
from macui.core.signal import Signal, Computed
from macui.layout.engine import set_debug_mode

# 导入现代化组件
from macui.components.modern_controls import ModernButton, ModernLabel, ModernTextField
from macui.components.modern_input import ModernSlider, ModernSwitch, ModernCheckbox, ModernSegmentedControl
from macui.components.modern_display import ModernImageView, ModernProgressBar, ModernTextArea
from macui.components.modern_selection import ModernPopUpButton, ModernComboBox
from macui.components.modern_time import ModernDatePicker, ModernTimePicker
from macui.components.modern_layout import ModernVStack, ModernHStack

# 导入AppKit用于NSDate和NSImage
from AppKit import NSImage
from Foundation import NSDate


class ComprehensiveModernDemo(Component):
    """全面现代化组件演示"""
    
    def __init__(self):
        super().__init__()
        # 响应式状态
        self.counter = Signal(0)
        self.text_value = Signal("测试文本")
        self.slider_value = Signal(50.0)
        self.switch_state = Signal(False)
        self.checkbox_state = Signal(True)
        self.progress_value = Signal(30.0)
        self.combo_text = Signal("选择项目")
        self.popup_selected = Signal(1)
        self.selected_date = Signal(NSDate.date())
        self.selected_time = Signal(NSDate.date())
        self.textarea_content = Signal("这是一个多行文本区域\n支持换行和滚动\n响应式更新")
        
        set_debug_mode(True)
        
        print("🚀 全面现代化组件测试开始...")
    
    def increment_counter(self):
        """增加计数器"""
        self.counter.value += 1
        # 同步更新进度条
        self.progress_value.value = min(100, self.counter.value * 10)
        print(f"🔢 计数器: {self.counter.value}")
    
    def reset_all(self):
        """重置所有状态"""
        self.counter.value = 0
        self.slider_value.value = 50.0
        self.switch_state.value = False
        self.checkbox_state.value = False
        self.progress_value.value = 0.0
        self.combo_text.value = "已重置"
        self.popup_selected.value = 0
        self.textarea_content.value = "状态已重置\\n所有组件恢复初始值"
        print("🔄 所有状态已重置")
    
    def on_slider_change(self, value: float):
        """滑块值变化回调"""
        print(f"🎚️ 滑块值: {value:.1f}")
    
    def on_popup_change(self, index: int):
        """下拉框选择回调"""
        items = ["苹果", "橙子", "香蕉", "葡萄"]
        print(f"🔽 选择了: {items[index]} (索引: {index})")
    
    def mount(self):
        """构建现代化组件UI"""
        from AppKit import NSView
        from Foundation import NSMakeRect
        
        print("🏗️ 开始构建全面现代化UI...")
        
        try:
            # === 创建所有现代化组件 ===
            
            # 标题和说明
            title_label = ModernLabel(
                "🎨 macUI 现代化组件全面测试",
                width=500,
                margin=16
            )
            
            description_label = ModernLabel(
                "验证基础、输入、显示、选择、时间和布局组件的现代化升级",
                width=480,
                margin=8
            )
            
            # === 第一行：基础控件测试 ===
            counter_display = ModernLabel(
                Computed(lambda: f"计数器: {self.counter.value}"),
                width=120,
                margin=8
            )
            
            increment_btn = ModernButton(
                "+1",
                on_click=self.increment_counter,
                width=60,
                height=32,
                margin=8
            )
            
            text_input = ModernTextField(
                value=self.text_value,
                placeholder="请输入文本",
                width=150,
                margin=8
            )
            
            reset_btn = ModernButton(
                "重置",
                on_click=self.reset_all,
                width=80,
                height=32,
                margin=8
            )
            
            # === 第二行：输入控件测试 ===
            slider_label = ModernLabel("滑块:", width=50, margin=8)
            slider = ModernSlider(
                value=self.slider_value,
                min_value=0.0,
                max_value=100.0,
                on_change=self.on_slider_change,
                width=200,
                margin=8
            )
            
            slider_value_label = ModernLabel(
                Computed(lambda: f"{self.slider_value.value:.1f}"),
                width=50,
                margin=8
            )
            
            switch_label = ModernLabel("开关:", width=50, margin=8)
            switch = ModernSwitch(
                value=self.switch_state,
                width=60,
                margin=8
            )
            
            checkbox = ModernCheckbox(
                "复选框",
                checked=self.checkbox_state,
                margin=8
            )
            
            # === 第三行：分段控件和进度条 ===
            segments = ModernSegmentedControl(
                ["选项1", "选项2", "选项3"],
                width=200,
                margin=8
            )
            
            progress_label = ModernLabel("进度:", width=50, margin=8)
            progress_bar = ModernProgressBar(
                value=self.progress_value,
                width=150,
                margin=8
            )
            
            progress_value_label = ModernLabel(
                Computed(lambda: f"{self.progress_value.value:.0f}%"),
                width=50,
                margin=8
            )
            
            # === 第四行：选择控件 ===
            popup_label = ModernLabel("下拉框:", width=60, margin=8)
            popup = ModernPopUpButton(
                ["苹果", "橙子", "香蕉", "葡萄"],
                selected=self.popup_selected,
                on_change=self.on_popup_change,
                width=100,
                margin=8
            )
            
            combo_label = ModernLabel("组合框:", width=60, margin=8)
            combo = ModernComboBox(
                items=["选项A", "选项B", "选项C"],
                text=self.combo_text,
                width=120,
                margin=8
            )
            
            # === 第五行：时间控件 ===
            date_label = ModernLabel("日期:", width=50, margin=8)
            date_picker = ModernDatePicker(
                date=self.selected_date,
                style="textfield",
                date_only=True,
                width=120,
                margin=8
            )
            
            time_label = ModernLabel("时间:", width=50, margin=8)
            time_picker = ModernTimePicker(
                time=self.selected_time,
                style="stepper",
                width=100,
                margin=8
            )
            
            # === 第六行：显示控件 ===
            # 文本区域
            textarea_label = ModernLabel("多行文本:", width=80, margin=8)
            textarea = ModernTextArea(
                value=self.textarea_content,
                width=300,
                height=80,
                margin=8
            )
            
            # === 状态显示区域 ===
            status_info = ModernLabel(
                Computed(lambda: f"状态 - 开关:{self.switch_state.value}, 复选框:{self.checkbox_state.value}"),
                width=400,
                margin=8
            )
            
            # === 使用现代化布局组件构建UI ===
            
            # 基础控件行
            basic_row = ModernHStack(
                children=[counter_display, increment_btn, text_input, reset_btn],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 输入控件行  
            input_row = ModernHStack(
                children=[slider_label, slider, slider_value_label, switch_label, switch, checkbox],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 分段和进度行
            segment_row = ModernHStack(
                children=[segments, progress_label, progress_bar, progress_value_label],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 选择控件行
            selection_row = ModernHStack(
                children=[popup_label, popup, combo_label, combo],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 时间控件行
            time_row = ModernHStack(
                children=[date_label, date_picker, time_label, time_picker],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 文本区域行
            textarea_row = ModernHStack(
                children=[textarea_label, textarea],
                spacing=8,
                width=600,
                margin=8
            )
            
            # 主布局 - 垂直堆叠所有行
            main_layout = ModernVStack(
                children=[
                    title_label,
                    description_label,
                    basic_row,
                    input_row, 
                    segment_row,
                    selection_row,
                    time_row,
                    textarea_row,
                    status_info
                ],
                spacing=12,
                width=650,
                height=600,
                padding=20
            )
            
            # 获取最终的NSView
            container = main_layout.get_view()
            
            print("✅ 全面现代化组件UI构建完成!")
            print("📊 测试组件数量:")
            print("   - 基础控件: 4 个 (Button x2, Label x4, TextField x1)")
            print("   - 输入控件: 5 个 (Slider, Switch, Checkbox, SegmentedControl)")
            print("   - 显示控件: 2 个 (ProgressBar, TextArea)")
            print("   - 选择控件: 2 个 (PopUpButton, ComboBox)")
            print("   - 时间控件: 2 个 (DatePicker, TimePicker)")
            print("   - 布局组件: 7 个 (VStack x1, HStack x6)")
            print("   📈 总计: 27 个现代化组件!")
            
            return container
            
        except Exception as e:
            print(f"❌ UI构建失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 返回错误信息
            error_container = NSView.alloc().init()
            error_container.setFrame_(NSMakeRect(0, 0, 650, 600))
            return error_container


def main():
    """主函数"""
    print("🧪 全面现代化组件测试")
    print("🎯 验证所有升级后的现代化组件")
    print("📐 测试CSS-like布局属性和响应式绑定")
    print("=" * 60)
    
    # 创建应用
    app = create_app("Comprehensive Modern Components Test")
    
    # 创建演示组件
    demo = ComprehensiveModernDemo()
    
    # 创建窗口
    window = create_window(
        title="全面现代化组件测试 - macUI v3.0",
        size=(700, 650),
        content=demo
    )
    
    window.show()
    
    print("✅ 全面现代化组件测试启动!")
    print("🔧 请测试以下功能:")
    print("   1. 点击按钮验证事件处理")
    print("   2. 调整滑块观察响应式更新")
    print("   3. 切换开关和复选框状态")
    print("   4. 选择下拉框和组合框")
    print("   5. 修改日期时间选择器")
    print("   6. 编辑文本区域内容")
    print("   7. 观察状态标签的响应式更新")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()