#!/usr/bin/env python3
"""
macUI v3.0 重构组件展示
验证统一style接口的基础组件与Stretchable布局引擎的集成
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
from macui.components.basic_controls import Button, Label
from macui.components.modern_layout import VStack, HStack
from macui.layout.styles import LayoutStyle, AlignItems, JustifyContent
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class RefactoredShowcaseApp(Component):
    """重构后组件展示应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        self.status_text = Signal("准备就绪")
        
    def mount(self):
        """创建应用界面"""
        print("🔧 创建重构后组件展示界面...")
        
        # 创建所有子组件
        title_section = self._create_title_section()
        button_section = self._create_button_section()  
        text_section = self._create_text_section()
        layout_section = self._create_layout_section()
        status_bar = self._create_status_bar()
        
        # 主容器 - 直接传入所有子组件
        main_container = VStack(
            children=[
                title_section,
                button_section,
                text_section,
                layout_section,
                status_bar
            ],
            style=LayoutStyle(
                padding=30,
                gap=25
            )
        )
        
        print("✅ 重构后组件展示界面创建完成")
        return main_container.mount()
    
    def _create_title_section(self):
        """创建标题区域"""
        title_container = VStack(
            children=[],
            style=LayoutStyle(gap=10)
        )
        
        # 主标题 - 使用单行标题样式
        main_title = Label(
            "🎉 macUI v3.0 重构组件展示",
            multiline=False,
            font=NSFont.systemFontOfSize_(24),
            style=LayoutStyle(height=30)
        )
        title_container.children.append(main_title)
        
        # 副标题
        subtitle = Label(
            "统一的style接口设计 + Stretchable布局引擎",
            multiline=False,
            font=NSFont.systemFontOfSize_(14),
            color=NSColor.systemGrayColor(),
            style=LayoutStyle(height=20)
        )
        title_container.children.append(subtitle)
        
        return title_container
    
    def _create_button_section(self):
        """创建按钮展示区域"""
        section_container = VStack(
            children=[],
            style=LayoutStyle(gap=15)
        )
        
        # 区域标题
        section_title = Label(
            "🔘 Button组件 - style接口展示",
            multiline=False,
            font=NSFont.boldSystemFontOfSize_(16),
            style=LayoutStyle(height=25)
        )
        section_container.children.append(section_title)
        
        # 不同尺寸的按钮组
        button_row1 = HStack(
            children=[],
            style=LayoutStyle(gap=15, justify_content=JustifyContent.CENTER)
        )
        
        # 小按钮
        small_button = Button(
            "小按钮",
            style=LayoutStyle(width=80, height=28),
            on_click=lambda: self._button_clicked("小按钮")
        )
        button_row1.children.append(small_button)
        
        # 中等按钮
        medium_button = Button(
            "中等按钮",
            style=LayoutStyle(width=120, height=32),
            on_click=lambda: self._button_clicked("中等按钮")
        )
        button_row1.children.append(medium_button)
        
        # 大按钮
        large_button = Button(
            "大按钮",
            style=LayoutStyle(width=160, height=40),
            on_click=lambda: self._button_clicked("大按钮")
        )
        button_row1.children.append(large_button)
        
        section_container.children.append(button_row1)
        
        # 功能按钮组
        button_row2 = HStack(
            children=[],
            style=LayoutStyle(gap=10, justify_content=JustifyContent.SPACE_BETWEEN)
        )
        
        actions = [
            ("🚀 启动", lambda: self._update_status("系统已启动")),
            ("⏸️ 暂停", lambda: self._update_status("系统已暂停")),
            ("🔄 重置", lambda: self._reset_demo()),
            ("🛑 停止", lambda: self._update_status("系统已停止"))
        ]
        
        for text, action in actions:
            btn = Button(
                text,
                style=LayoutStyle(width=100, height=32),
                on_click=action
            )
            button_row2.children.append(btn)
        
        section_container.children.append(button_row2)
        
        return section_container
    
    def _create_text_section(self):
        """创建文本展示区域"""
        section_container = VStack(
            children=[],
            style=LayoutStyle(gap=15)
        )
        
        # 区域标题
        section_title = Label(
            "📝 Label组件 - 文本显示模式展示",
            multiline=False,
            font=NSFont.boldSystemFontOfSize_(16),
            style=LayoutStyle(height=25)
        )
        section_container.children.append(section_title)
        
        # 单行标题样式
        title_example = Label(
            "单行标题示例 - 这是一个很长的标题，会被适当处理",
            multiline=False,
            font=NSFont.systemFontOfSize_(14),
            style=LayoutStyle(height=20)
        )
        section_container.children.append(title_example)
        
        # 多行描述文本
        multiline_text = Label(
            "多行描述文本示例：这是一段较长的描述文本，"
            "展示了Label组件在多行模式下的文本换行功能。"
            "文本会根据容器宽度自动换行，提供良好的阅读体验。",
            multiline=True,
            font=NSFont.systemFontOfSize_(13),
            style=LayoutStyle(width=400)
        )
        section_container.children.append(multiline_text)
        
        # 固定宽度文本
        fixed_width_text = Label(
            "固定宽度文本：这段文本使用了固定的宽度设置，"
            "展示了style接口对文本布局的精确控制能力。",
            multiline=True,
            preferred_max_width=250.0,
            font=NSFont.systemFontOfSize_(12),
            color=NSColor.systemBlueColor(),
            style=LayoutStyle(width=250)
        )
        section_container.children.append(fixed_width_text)
        
        return section_container
    
    def _create_layout_section(self):
        """创建布局展示区域"""
        section_container = VStack(
            children=[],
            style=LayoutStyle(gap=15)
        )
        
        # 区域标题
        section_title = Label(
            "📐 VStack/HStack - 布局容器展示",
            multiline=False,
            font=NSFont.boldSystemFontOfSize_(16),
            style=LayoutStyle(height=25)
        )
        section_container.children.append(section_title)
        
        # 水平布局示例
        h_layout_demo = VStack(
            children=[],
            style=LayoutStyle(gap=10)
        )
        
        h_demo_title = Label(
            "HStack 水平布局示例：",
            multiline=False,
            font=NSFont.systemFontOfSize_(13),
            style=LayoutStyle(height=18)
        )
        h_layout_demo.children.append(h_demo_title)
        
        h_demo_container = HStack(
            children=[],
            style=LayoutStyle(gap=15, justify_content=JustifyContent.CENTER)
        )
        
        for i in range(1, 4):
            item = Label(
                f"项目 {i}",
                multiline=False,
                font=NSFont.systemFontOfSize_(12),
                style=LayoutStyle(width=60, height=25)
            )
            h_demo_container.children.append(item)
        
        h_layout_demo.children.append(h_demo_container)
        section_container.children.append(h_layout_demo)
        
        # 垂直布局示例
        v_layout_demo = HStack(
            children=[],
            style=LayoutStyle(gap=20, justify_content=JustifyContent.SPACE_AROUND)
        )
        
        for i in range(1, 4):
            v_demo = VStack(
                children=[],
                style=LayoutStyle(gap=8, align_items=AlignItems.CENTER)
            )
            
            v_title = Label(
                f"VStack {i}",
                multiline=False,
                font=NSFont.systemFontOfSize_(12),
                style=LayoutStyle(height=18)
            )
            v_demo.children.append(v_title)
            
            for j in range(1, 3):
                v_item = Label(
                    f"项目 {j}",
                    multiline=False,
                    font=NSFont.systemFontOfSize_(10),
                    style=LayoutStyle(width=50, height=15)
                )
                v_demo.children.append(v_item)
            
            v_layout_demo.children.append(v_demo)
        
        section_container.children.append(v_layout_demo)
        
        return section_container
    
    def _create_status_bar(self):
        """创建状态栏"""
        status_container = HStack(
            children=[],
            style=LayoutStyle(
                gap=20,
                justify_content=JustifyContent.SPACE_BETWEEN,
                padding=15
            )
        )
        
        # 左侧状态
        status_label = Label(
            f"状态: {self.status_text.value}",
            multiline=False,
            font=NSFont.systemFontOfSize_(12),
            style=LayoutStyle(height=18)
        )
        status_container.children.append(status_label)
        
        # 中间计数器
        counter_label = Label(
            f"点击计数: {self.click_count.value}",
            multiline=False,
            font=NSFont.systemFontOfSize_(12),
            color=NSColor.systemBlueColor(),
            style=LayoutStyle(height=18)
        )
        status_container.children.append(counter_label)
        
        # 右侧信息
        info_label = Label(
            "✅ 组件重构完成",
            multiline=False,
            font=NSFont.systemFontOfSize_(12),
            color=NSColor.systemGreenColor(),
            style=LayoutStyle(height=18)
        )
        status_container.children.append(info_label)
        
        return status_container
    
    # 交互方法
    def _button_clicked(self, button_name):
        self.click_count.value += 1
        self.status_text.value = f"点击了{button_name}"
        print(f"🔘 {button_name} 被点击，总计数: {self.click_count.value}")
        
    def _update_status(self, status):
        self.status_text.value = status
        print(f"📊 状态更新: {status}")
        
    def _reset_demo(self):
        self.click_count.value = 0
        self.status_text.value = "已重置"
        print("🔄 演示重置")

class ShowcaseWindow:
    """展示窗口管理"""
    
    def __init__(self):
        self.window = None
        self.app_component = None
        
    def create_window(self):
        """创建窗口"""
        print("🪟 创建重构组件展示窗口...")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 700, 600),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("macUI v3.0 重构组件展示")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建应用组件
        self.app_component = RefactoredShowcaseApp()
        
        # 挂载组件到窗口
        try:
            content_view = self.app_component.mount()
            self.window.setContentView_(content_view)
            print("✅ 重构后组件挂载到窗口成功")
        except Exception as e:
            print(f"❌ 组件挂载失败: {e}")
            import traceback
            traceback.print_exc()
        
        return self.window

def main():
    """主函数"""
    print("🚀 启动macUI v3.0 重构组件展示...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 重构组件展示")
        
        # 创建展示窗口
        showcase_window = ShowcaseWindow()
        window = showcase_window.create_window()
        
        print("✅ 重构组件展示应用创建成功!")
        print("🎯 展示内容:")
        print("   - 统一的style接口设计")
        print("   - Button组件: 支持width/height style参数")
        print("   - Label组件: 完整的文本显示参数 + style布局控制")
        print("   - VStack/HStack: 纯style参数布局")
        print("   - Stretchable布局引擎集成")
        
        print("\\n📊 重构成果:")
        print("   - Button: frame参数 → style参数")
        print("   - Label: 保留文本参数 + 新增style支持")
        print("   - VStack/HStack: 简化为children + style参数")
        print("   - 布局参数统一到LayoutStyle对象")
        
        # 启用事件循环，让UI真正显示
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()