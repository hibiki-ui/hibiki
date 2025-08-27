#!/usr/bin/env python3
"""
macUI v3.0 统一API演示
展示简洁、现代的组件命名和布局系统
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

# 🎯 macUI v3.0 统一API - 简洁优雅
from macui import Signal, Computed, Effect
from macui.components import Label, Button, VStack, HStack, LayoutStyle
from macui.layout.styles import JustifyContent, AlignItems
from macui.app import create_app
from macui.core import Component
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class MacUIv3Demo(Component):
    """macUI v3.0 演示应用"""
    
    def __init__(self):
        super().__init__()
        # 响应式状态
        self.counter = Signal(0)
        self.status = Signal("准备就绪")
        
        # 计算属性
        self.counter_text = Computed(lambda: f"计数: {self.counter.value}")
        self.is_even = Computed(lambda: self.counter.value % 2 == 0)
        
    def mount(self):
        """创建macUI v3.0演示界面"""
        print("🔧 MacUIv3Demo.mount() 开始...")
        
        # 🎨 标题区域
        title = Label(
            "🎉 macUI v3.0 统一API",
            style=LayoutStyle(height=40)
        )
        print(f"✅ 创建title: {title}")
        
        subtitle = Label(
            "现代化、简洁、功能完整",
            style=LayoutStyle(height=25)
        )
        
        # 📊 数据显示区域
        counter_display = Label(
            f"计数: {self.counter.value}",
            style=LayoutStyle(height=30)
        )
        
        status_display = Label(
            f"状态: {self.status.value}",
            style=LayoutStyle(height=25)
        )
        
        parity_display = Label(
            f"当前数字是{'偶数' if self.counter.value % 2 == 0 else '奇数'}",
            style=LayoutStyle(height=25)
        )
        
        # 🔘 控制按钮区域
        increment_btn = Button(
            "➕ 增加",
            style=LayoutStyle(width=80, height=35),
            on_click=self._increment
        )
        
        decrement_btn = Button(
            "➖ 减少", 
            style=LayoutStyle(width=80, height=35),
            on_click=self._decrement
        )
        
        reset_btn = Button(
            "🔄 重置",
            style=LayoutStyle(width=80, height=35),
            on_click=self._reset
        )
        
        # 水平按钮组
        button_group = HStack(
            children=[decrement_btn, reset_btn, increment_btn],
            style=LayoutStyle(gap=10, justify_content=JustifyContent.CENTER)
        )
        
        # 🎮 功能按钮
        demo_actions = HStack(
            children=[
                Button("🚀 启动", style=LayoutStyle(width=70, height=30),
                      on_click=lambda: self._set_status("系统启动")),
                Button("⏸️ 暂停", style=LayoutStyle(width=70, height=30), 
                      on_click=lambda: self._set_status("系统暂停")),
                Button("🛑 停止", style=LayoutStyle(width=70, height=30),
                      on_click=lambda: self._set_status("系统停止"))
            ],
            style=LayoutStyle(gap=8, justify_content=JustifyContent.SPACE_AROUND)
        )
        
        # 📋 信息面板
        info_panel = VStack(
            children=[
                Label("✨ API特性:", style=LayoutStyle(height=20)),
                Label("• 统一的组件命名 (Label, Button)", style=LayoutStyle(height=18)),
                Label("• Stretchable布局引擎", style=LayoutStyle(height=18)),  
                Label("• 响应式状态管理", style=LayoutStyle(height=18)),
                Label("• 现代化样式系统", style=LayoutStyle(height=18))
            ],
            style=LayoutStyle(gap=2, padding=10)
        )
        
        # 🏗️ 主容器 - 使用VStack统一布局
        main_container = VStack(
            children=[
                title,
                subtitle,
                counter_display,
                status_display, 
                parity_display,
                button_group,
                demo_actions,
                info_panel
            ],
            style=LayoutStyle(
                gap=15,
                padding=25,
                align_items=AlignItems.CENTER
            )
        )
        
        return main_container.mount()
    
    def _increment(self):
        """增加计数"""
        self.counter.value += 1
        self.status.value = f"计数增加到 {self.counter.value}"
        
    def _decrement(self):
        """减少计数"""
        if self.counter.value > 0:
            self.counter.value -= 1
            self.status.value = f"计数减少到 {self.counter.value}"
        else:
            self.status.value = "计数已为0"
    
    def _reset(self):
        """重置计数"""
        self.counter.value = 0
        self.status.value = "计数已重置"
    
    def _set_status(self, status: str):
        """设置状态"""
        self.status.value = status

def main():
    """主函数"""
    print("🚀 启动macUI v3.0统一API演示...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 演示")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 500, 600),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        window.setTitle_("macUI v3.0 统一API演示")
        window.makeKeyAndOrderFront_(None)
        
        # 创建并挂载演示组件
        print("🔧 创建MacUIv3Demo...")
        demo = MacUIv3Demo()
        print("🔧 调用demo.mount()...")
        content_view = demo.mount()
        print(f"✅ mount()返回: {content_view}")
        window.setContentView_(content_view)
        print("✅ 组件已设置到窗口")
        
        print("✅ macUI v3.0演示应用启动成功!")
        print()
        print("🎯 v3.0 统一API成果:")
        print("   ✅ 组件命名统一: Label, Button (不需要Modern前缀)")
        print("   ✅ 自动选择最佳实现: ModernLabel, ModernButton")
        print("   ✅ 布局组件现代化: VStack, HStack (支持Stretchable)")
        print("   ✅ 样式系统一致: 统一使用LayoutStyle")
        print("   ✅ 枚举完整迁移: LineBreakMode, LabelStyle")
        print("   ✅ 向后兼容: 旧代码可继续使用Modern*别名")
        print("   ✅ 用户体验优化: 简洁、直观、功能完整")
        print()
        print("🔥 现在用户只需要记住:")
        print("   from macui.components import Label, Button, VStack, HStack")
        print("   无需纠结选择哪个版本 - 自动使用最佳实现!")
        
        # 启动事件循环
        print("\n🎮 启动事件循环，享受macUI v3.0统一API...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()