#!/usr/bin/env python3
"""
现代化组件测试 - 验证基于新布局引擎的组件实现

测试LayoutAwareComponent基类和现代化控件
验证CSS-like布局属性和声明式API
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.core.component import Component
from macui.core.signal import Signal, Computed

# 导入现代化组件
from macui.components.modern_controls import (
    ModernButton, ModernLabel, ModernTextField,
    Button, Label, TextField,  # 向后兼容接口
    FlexButton, FixedButton, SpacedLabel  # 增强函数
)

# 导入布局系统
from macui.layout.integration import VStack, HStack
from macui.layout.styles import AlignItems, JustifyContent
from macui.layout.engine import set_debug_mode


class ModernComponentsDemo(Component):
    """现代化组件演示"""
    
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        self.text_input = Signal("输入文本...")
        self.status = Signal("准备就绪")
        
        # 启用布局调试
        set_debug_mode(True)
    
    def increment(self):
        """增加计数器"""
        old_val = self.counter.value
        self.counter.value = old_val + 1
        self.status.value = f"按钮点击 #{self.counter.value}"
    
    def reset(self):
        """重置计数器"""
        self.counter.value = 0
        self.status.value = "计数器已重置"
    
    def text_changed(self, new_text: str):
        """文本变化处理"""
        self.status.value = f"文本变化: {len(new_text)} 字符"
    
    def mount(self):
        """挂载现代化组件演示"""
        print("🚀 现代化组件演示启动...")
        print("📐 测试LayoutAwareComponent和CSS-like属性")
        
        # 创建响应式显示组件
        counter_display = Label(Computed(lambda: f"计数: {self.counter.value}"))
        status_display = Label(self.status)
        text_display = Label(Computed(lambda: f"当前输入: {self.text_input.value}"))
        
        # 创建输入组件
        text_input = TextField(
            value=self.text_input,
            placeholder="请输入文本...",
            on_change=self.text_changed
        )
        
        # 使用新布局系统构建UI
        try:
            main_layout = VStack(
                children=[
                    # 标题区域
                    SpacedLabel(
                        "🎨 现代化组件演示",
                        margin=16
                    ).width(400),
                    
                    Label("基于LayoutAwareComponent + Stretchable布局引擎"),
                    
                    Label(""),  # 分隔
                    
                    # 计数器区域
                    VStack(
                        children=[
                            counter_display.margin(8),
                            
                            # 按钮行 - 演示不同的布局属性
                            HStack(
                                children=[
                                    # 固定宽度按钮
                                    FixedButton(
                                        "+1", 
                                        width=60, 
                                        on_click=self.increment
                                    ).margin(right=8),
                                    
                                    # 弹性按钮
                                    FlexButton(
                                        "重置计数器",
                                        on_click=self.reset,
                                        flex_grow=1.0
                                    ).margin(right=8),
                                    
                                    # 链式调用示例
                                    Button("测试", on_click=self.increment)
                                    .width(80)
                                    .margin(left=4)
                                ],
                                spacing=8,
                                alignment="center"
                            )
                        ],
                        spacing=12,
                        alignment="center"
                    ),
                    
                    Label(""),  # 分隔
                    
                    # 输入区域
                    VStack(
                        children=[
                            Label("文本输入测试:").margin(bottom=8),
                            
                            text_input.width(300).margin(bottom=8),
                            
                            text_display.margin(bottom=8),
                        ],
                        spacing=8,
                        alignment="center"
                    ),
                    
                    Label(""),  # 分隔
                    
                    # 状态区域
                    VStack(
                        children=[
                            Label("状态信息:").margin(bottom=4),
                            status_display.margin(8),
                        ],
                        spacing=4,
                        alignment="center"
                    ),
                    
                    Label(""),  # 分隔
                    
                    # 功能特性说明
                    VStack(
                        children=[
                            Label("✅ 新功能特性:").margin(bottom=8),
                            Label("• CSS-like布局属性 (width, height, margin, flex等)"),
                            Label("• 链式调用API (component.width(120).margin(8))"),
                            Label("• 声明式组件组合"),
                            Label("• 完整的响应式Signal支持"),
                            Label("• 高性能Stretchable布局引擎"),
                            Label("• 向后兼容的函数式接口"),
                        ],
                        spacing=4,
                        alignment="start"
                    )
                ],
                spacing=16,
                alignment="center",
                padding=20
            )
            
            print("✅ 现代化组件UI构建完成")
            return main_layout
            
        except Exception as e:
            print(f"❌ UI构建失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 回退到简单布局
            from AppKit import NSView
            container = NSView.alloc().init()
            return container


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 macUI 现代化组件系统测试")
    print("📐 基于Layout Engine v3.0 (Stretchable)")
    print("🎯 验证LayoutAwareComponent和CSS-like API")
    print("=" * 60)
    
    # 创建应用
    app = create_app("Modern Components Test")
    
    # 创建演示组件
    demo = ModernComponentsDemo()
    
    # 创建窗口
    window = create_window(
        title="现代化组件演示 - Layout Engine v3.0",
        size=(600, 800),
        content=demo
    )
    
    window.show()
    
    print("✅ 现代化组件演示已启动!")
    print("🎯 测试按钮点击、文本输入和响应式更新")
    print("📊 观察控制台的布局调试信息")
    
    # 运行应用
    try:
        import AppHelper
        AppHelper.runEventLoop()
    except ImportError:
        from AppKit import NSApp
        NSApp.run()


if __name__ == "__main__":
    main()