#!/usr/bin/env python3
"""
测试高级选择控件：SegmentedControl 和 PopUpButton
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import SegmentedControl, PopUpButton, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class AdvancedControlsTestApp:
    """高级控件测试应用"""
    
    def __init__(self):
        # SegmentedControl 状态
        self.view_mode = Signal(0)  # 0: List, 1: Grid, 2: Card
        self.text_align = Signal(1)  # 0: Left, 1: Center, 2: Right
        
        # PopUpButton 状态
        self.font_size = Signal(2)  # 索引对应的字体大小
        self.color_scheme = Signal(0)  # 颜色方案索引
        self.export_format = Signal(1)  # 导出格式索引
        
        # 消息显示
        self.message = Signal("高级控件测试准备就绪")
        
        # 选项数据
        self.view_modes = ["列表视图", "网格视图", "卡片视图"]
        self.text_aligns = ["左对齐", "居中", "右对齐"]
        self.font_sizes = ["小号 (12px)", "中号 (14px)", "大号 (16px)", "特大 (18px)"]
        self.color_schemes = ["浅色主题", "深色主题", "蓝色主题", "绿色主题"]
        self.export_formats = ["PDF", "Word", "Excel", "PowerPoint", "纯文本"]
        
    def on_view_mode_change(self, index):
        mode_name = self.view_modes[index] if index < len(self.view_modes) else f"模式{index}"
        self.message.value = f"视图模式: {mode_name}"
        
    def on_text_align_change(self, index):
        align_name = self.text_aligns[index] if index < len(self.text_aligns) else f"对齐{index}"
        self.message.value = f"文本对齐: {align_name}"
        
    def on_font_size_change(self, index):
        size_name = self.font_sizes[index] if index < len(self.font_sizes) else f"大小{index}"
        self.message.value = f"字体大小: {size_name}"
        
    def on_color_scheme_change(self, index):
        scheme_name = self.color_schemes[index] if index < len(self.color_schemes) else f"方案{index}"
        self.message.value = f"颜色方案: {scheme_name}"
        
    def on_export_format_change(self, index):
        format_name = self.export_formats[index] if index < len(self.export_formats) else f"格式{index}"
        self.message.value = f"导出格式: {format_name}"
        
    def reset_all_controls(self):
        # 重置所有控件到默认值
        self.view_mode.value = 0
        self.text_align.value = 1
        self.font_size.value = 2
        self.color_scheme.value = 0
        self.export_format.value = 1
        self.message.value = "所有控件已重置"
        
    def randomize_settings(self):
        # 随机设置所有控件
        import random
        self.view_mode.value = random.randint(0, 2)
        self.text_align.value = random.randint(0, 2)
        self.font_size.value = random.randint(0, len(self.font_sizes) - 1)
        self.color_scheme.value = random.randint(0, len(self.color_schemes) - 1)
        self.export_format.value = random.randint(0, len(self.export_formats) - 1)
        self.message.value = "设置已随机化"

def main():
    print("=== 高级选择控件测试 ===")
    
    app = MacUIApp("Advanced Controls Test")
    test_app = AdvancedControlsTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class AdvancedControlsComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("高级选择控件测试", frame=(0, 0, 500, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # SegmentedControl 测试区域
                    Label("1. 分段选择控件 (SegmentedControl):"),
                    
                    # 视图模式选择
                    VStack(spacing=8, children=[
                        Label("视图模式:"),
                        SegmentedControl(
                            segments=test_app.view_modes,
                            selected=test_app.view_mode,
                            on_change=test_app.on_view_mode_change,
                            tooltip="选择列表显示模式",
                            frame=(0, 0, 300, 25)
                        ),
                    ]),
                    
                    # 文本对齐选择
                    VStack(spacing=8, children=[
                        Label("文本对齐:"),
                        SegmentedControl(
                            segments=test_app.text_aligns,
                            selected=test_app.text_align,
                            on_change=test_app.on_text_align_change,
                            tooltip="选择文本对齐方式",
                            frame=(0, 0, 250, 25)
                        ),
                    ]),
                    
                    # PopUpButton 测试区域
                    Label("2. 下拉选择按钮 (PopUpButton):"),
                    
                    # 字体大小选择
                    HStack(spacing=10, children=[
                        Label("字体大小:", frame=(0, 0, 80, 20)),
                        PopUpButton(
                            items=test_app.font_sizes,
                            selected=test_app.font_size,
                            on_change=test_app.on_font_size_change,
                            tooltip="选择字体大小",
                            frame=(0, 0, 120, 25)
                        ),
                    ]),
                    
                    # 颜色方案选择
                    HStack(spacing=10, children=[
                        Label("颜色方案:", frame=(0, 0, 80, 20)),
                        PopUpButton(
                            items=test_app.color_schemes,
                            selected=test_app.color_scheme,
                            on_change=test_app.on_color_scheme_change,
                            tooltip="选择界面颜色方案",
                            frame=(0, 0, 120, 25)
                        ),
                    ]),
                    
                    # 导出格式选择
                    HStack(spacing=10, children=[
                        Label("导出格式:", frame=(0, 0, 80, 20)),
                        PopUpButton(
                            items=test_app.export_formats,
                            selected=test_app.export_format,
                            on_change=test_app.on_export_format_change,
                            tooltip="选择文档导出格式",
                            frame=(0, 0, 120, 25)
                        ),
                    ]),
                    
                    # 控制按钮
                    HStack(spacing=15, children=[
                        Button("重置所有", on_click=test_app.reset_all_controls),
                        Button("随机设置", on_click=test_app.randomize_settings),
                    ]),
                    
                    # 实时显示当前状态
                    VStack(spacing=5, children=[
                        Label("当前设置:"),
                        Label(lambda: f"视图: {test_app.view_modes[test_app.view_mode.value] if test_app.view_mode.value < len(test_app.view_modes) else '未知'}"),
                        Label(lambda: f"对齐: {test_app.text_aligns[test_app.text_align.value] if test_app.text_align.value < len(test_app.text_aligns) else '未知'}"),
                        Label(lambda: f"字体: {test_app.font_sizes[test_app.font_size.value] if test_app.font_size.value < len(test_app.font_sizes) else '未知'}"),
                        Label(lambda: f"主题: {test_app.color_schemes[test_app.color_scheme.value] if test_app.color_scheme.value < len(test_app.color_schemes) else '未知'}"),
                        Label(lambda: f"格式: {test_app.export_formats[test_app.export_format.value] if test_app.export_format.value < len(test_app.export_formats) else '未知'}"),
                    ]),
                ])
        
        return AdvancedControlsComponent()
    
    # 创建窗口
    window = app.create_window(
        title="Advanced Controls Test",
        size=(550, 600),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - SegmentedControl: 分段选择控件")
    print("     * 视图模式选择 (列表/网格/卡片)")
    print("     * 文本对齐选择 (左/中/右)")
    print("   - PopUpButton: 下拉选择按钮")
    print("     * 字体大小选择")
    print("     * 颜色方案选择") 
    print("     * 导出格式选择")
    print("   - 双向数据绑定")
    print("   - 实时状态更新")
    print("   - 批量控制功能")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()