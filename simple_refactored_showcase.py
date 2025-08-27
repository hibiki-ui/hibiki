#!/usr/bin/env python3
"""
macUI v3.0 简化重构组件展示 - 确保UI能正确显示
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
from macui.components.modern_components import ModernLabel, ModernButton
from macui.components.modern_layout import VStack, HStack
from macui.layout.styles import LayoutStyle, AlignItems, JustifyContent
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class SimpleRefactoredShowcase(Component):
    """简化的重构组件展示"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        
    def mount(self):
        """创建应用界面"""
        print("🔧 创建简化重构组件界面...")
        
        # 创建所有组件
        title = ModernLabel(
            "🎉 macUI v3.0 重构组件展示",
            style=LayoutStyle(height=30)
        )
        
        subtitle = ModernLabel(
            "统一的style接口设计",
            style=LayoutStyle(height=20)
        )
        
        # 按钮组
        button1 = ModernButton(
            "小按钮",
            style=LayoutStyle(width=80, height=30),
            on_click=lambda: self._increment_count()
        )
        
        button2 = ModernButton(
            "中按钮",
            style=LayoutStyle(width=100, height=30),
            on_click=lambda: self._increment_count()
        )
        
        button3 = ModernButton(
            "大按钮",
            style=LayoutStyle(width=120, height=30),
            on_click=lambda: self._increment_count()
        )
        
        # 水平按钮组
        button_row = HStack(
            children=[button1, button2, button3],
            style=LayoutStyle(gap=10, justify_content=JustifyContent.CENTER)
        )
        
        # 计数显示
        count_label = ModernLabel(
            f"点击计数: {self.click_count.value}",
            style=LayoutStyle(height=25)
        )
        
        # 多行文本示例
        multiline_text = ModernLabel(
            "这是多行文本示例，展示了Label组件在重构后如何通过style参数"
            "控制布局，同时保留所有文本显示相关的参数设置功能。",
            style=LayoutStyle(width=350)
        )
        
        # 主容器
        main_container = VStack(
            children=[
                title,
                subtitle, 
                button_row,
                count_label,
                multiline_text
            ],
            style=LayoutStyle(
                padding=30,
                gap=20,
                align_items=AlignItems.CENTER
            )
        )
        
        print("✅ 简化重构组件界面创建完成")
        return main_container.mount()
    
    def _increment_count(self):
        """增加计数"""
        self.click_count.value += 1
        print(f"🔘 按钮被点击，计数: {self.click_count.value}")

class ShowcaseWindow:
    """展示窗口管理"""
    
    def __init__(self):
        self.window = None
        self.app_component = None
        
    def create_window(self):
        """创建窗口"""
        print("🪟 创建简化展示窗口...")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 500, 400),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("macUI v3.0 简化重构展示")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建应用组件
        self.app_component = SimpleRefactoredShowcase()
        
        # 挂载组件到窗口
        try:
            content_view = self.app_component.mount()
            self.window.setContentView_(content_view)
            print("✅ 简化重构组件挂载成功")
        except Exception as e:
            print(f"❌ 组件挂载失败: {e}")
            import traceback
            traceback.print_exc()
        
        return self.window

def main():
    """主函数"""
    print("🚀 启动macUI v3.0 简化重构组件展示...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 简化重构展示")
        
        # 创建展示窗口
        showcase_window = ShowcaseWindow()
        window = showcase_window.create_window()
        
        print("✅ 简化重构展示应用创建成功!")
        print("🎯 展示内容:")
        print("   - Button: style接口控制尺寸")
        print("   - Label: 文本参数 + style布局参数")
        print("   - VStack/HStack: 统一style接口")
        print("   - 点击按钮测试交互")
        
        # 启用事件循环，让UI真正显示
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()