#!/usr/bin/env python3
"""
macUI New Layout System Demo - 方案B实施演示

展示基于Stretchable (Taffy/Rust)的专业布局系统
替换旧的NSStackView hack实现，提供Web标准兼容的布局能力
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app, create_window
from macui.components import Button, Label, TextField  # 使用现有组件
from macui.core.component import Component
from macui.core.signal import Signal

# 导入新布局系统
from macui.layout.integration import VStack, HStack, LayoutComponent
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent
from macui.layout.engine import set_debug_mode

class NewLayoutDemoApp(Component):
    """新布局系统演示应用"""
    
    def __init__(self):
        super().__init__()
        self.counter = Signal(0)
        self.status = Signal("准备就绪")
        
        # 启用布局调试
        set_debug_mode(True)
    
    def increment_counter(self):
        """增加计数器"""
        old_value = self.counter.value
        self.counter.value = old_value + 1
        self.status.value = f"计数器增加: {old_value} -> {self.counter.value}"
    
    def decrement_counter(self):
        """减少计数器"""
        old_value = self.counter.value
        self.counter.value = max(0, old_value - 1)
        self.status.value = f"计数器减少: {old_value} -> {self.counter.value}"
    
    def reset_counter(self):
        """重置计数器"""
        old_value = self.counter.value
        self.counter.value = 0
        self.status.value = f"计数器重置: {old_value} -> 0"
    
    def mount(self):
        """挂载演示应用"""
        print("🚀 启动新布局系统演示...")
        print("📐 使用Stretchable (Taffy/Rust)布局引擎")
        
        # 创建动态标签
        counter_label = Label("计数: 0")
        status_label = Label("状态: 准备就绪")
        
        # 创建响应式更新
        def update_counter_display():
            counter_label.setStringValue_(f"计数: {self.counter.value}")
        
        def update_status_display():
            status_label.setStringValue_(f"状态: {self.status.value}")
        
        self.create_effect(update_counter_display)
        self.create_effect(update_status_display)
        
        # 使用新布局系统构建UI
        main_layout = VStack(
            children=[
                # 标题区域
                Label("🎨 macUI新布局系统演示"),
                Label("基于Stretchable (Taffy/Rust)的专业布局引擎"),
                Label(""),  # 空行分隔
                
                # 计数器显示区域
                VStack(
                    children=[
                        counter_label,
                        status_label,
                        Label("")  # 分隔线
                    ],
                    spacing=8,
                    alignment="center"
                ),
                
                # 按钮操作区域 - 水平布局
                HStack(
                    children=[
                        Button("-1", on_click=lambda: self.decrement_counter()),
                        Button("+1", on_click=lambda: self.increment_counter()),
                        Button("重置", on_click=lambda: self.reset_counter())
                    ],
                    spacing=12,
                    alignment="center"
                ),
                
                Label(""),  # 分隔
                
                # 功能演示区域
                VStack(
                    children=[
                        Label("📋 新布局系统特性:"),
                        Label("✅ CSS-like声明式API"),
                        Label("✅ Rust高性能引擎"),
                        Label("✅ Web标准兼容"),
                        Label("✅ 布局缓存优化"),
                        Label("✅ 专业调试支持")
                    ],
                    spacing=4,
                    alignment="start"  # 左对齐
                ),
                
                Label(""),  # 分隔
                
                # 对比说明
                VStack(
                    children=[
                        Label("🆚 vs 旧系统对比:"),
                        Label("❌ 旧: NSStackView hack实现"),
                        Label("❌ 旧: 负坐标定位bug"),
                        Label("❌ 旧: 复杂的约束生成"),
                        Label("✅ 新: 标准Flexbox布局"),
                        Label("✅ 新: 可预测的行为"),
                        Label("✅ 新: 现代化架构")
                    ],
                    spacing=4,
                    alignment="start"
                ),
                
                Label(""),
                Label("🎯 点击按钮测试布局和交互功能！")
            ],
            spacing=16,
            alignment="center",
            padding=20
        )
        
        print("✅ 新布局系统UI构建完成")
        return main_layout


def main():
    """主函数"""
    print("=" * 60)
    print("🚀 macUI New Layout System Demo")
    print("📐 方案B: 纯布局引擎架构 (Pure Layout Engine)")
    print("⚡ 基于Stretchable (Taffy/Rust)实现")
    print("=" * 60)
    
    # 创建应用
    app = create_app("macUI New Layout System Demo")
    
    # 创建演示组件
    demo_app = NewLayoutDemoApp()
    
    # 创建窗口
    window = create_window(
        title="macUI新布局系统演示 - 专业级Stretchable布局",
        size=(600, 700),
        content=demo_app
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 新布局系统演示应用已启动!")
    print("🎯 请测试按钮交互和布局功能")
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