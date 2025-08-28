#!/usr/bin/env python3
"""
🎨 macUI v4 Feature Showcase
完整的v4框架功能演示应用

展示所有核心功能：
- 响应式系统 (Signal/Computed/Effect)
- 布局系统 (Stretchable + Flexbox)
- 组件系统 (Label/Button/Container)
- 样式系统 (CSS-like API)
- 事件系统 (交互处理)
- 管理器系统 (六大专业管理器)
"""

import sys
import os

# 添加macui_v4路径
sys.path.append(os.path.join(os.path.dirname(__file__), "macui_v4"))

# 导入v4核心
from core.managers import ManagerFactory
from core.styles import ComponentStyle, Display, FlexDirection, AlignItems, JustifyContent, px, percent, vw, vh
from core.reactive import Signal, Computed, Effect
from components.basic import Label, Button
from core.component import Container

# PyObjC导入
from AppKit import NSApplication, NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskMiniaturizable, NSApplicationActivationPolicyRegular
from Foundation import NSObject, NSMakeRect
from PyObjCTools import AppHelper

# ================================
# 🎯 应用状态管理
# ================================

class ShowcaseAppState:
    """应用全局状态管理"""
    
    def __init__(self):
        # 当前选中的标签页
        self.current_tab = Signal("reactive")
        
        # 响应式演示状态
        self.counter = Signal(0)
        self.name = Signal("macUI v4")
        self.multiplier = Signal(2)
        
        # 计算属性
        self.doubled_counter = Computed(lambda: self.counter.value * 2)
        self.greeting = Computed(lambda: f"Hello, {self.name.value}!")
        self.complex_calc = Computed(lambda: self.counter.value * self.multiplier.value + 10)
        
        # 布局演示状态
        self.layout_mode = Signal("column")
        self.alignment = Signal("center")
        
        # 样式演示状态
        self.opacity_value = Signal(1.0)
        self.scale_value = Signal(1.0)
        self.current_theme = Signal("light")
        
        # 综合演示状态 (Todo App)
        self.todos = Signal([])
        self.new_todo_text = Signal("")
        self.todo_counter = Signal(0)
        
        print("🎯 ShowcaseAppState初始化完成")

# 全局状态实例
app_state = ShowcaseAppState()

# ================================
# 📱 标签页组件
# ================================

def create_tab_bar():
    """创建标签页导航栏"""
    
    def switch_to_tab(tab_name):
        def handler():
            app_state.current_tab.value = tab_name
            print(f"🔄 切换到标签页: {tab_name}")
        return handler
    
    tabs = [
        ("reactive", "响应式"),
        ("layout", "布局"),
        ("component", "组件"),
        ("style", "样式"),
        ("interaction", "交互"),
        ("complete", "综合演示")
    ]
    
    tab_buttons = []
    for tab_id, tab_name in tabs:
        button = Button(
            tab_name,
            on_click=switch_to_tab(tab_id),
            style=ComponentStyle(
                width=px(80),
                height=px(30),
                margin_left=px(5),
                margin_right=px(5)
            )
        )
        tab_buttons.append(button)
    
    return Container(
        children=tab_buttons,
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER,
            width=percent(100),
            height=px(50),
            gap=px(5)
        )
    )

# ================================
# 1️⃣ 响应式演示页
# ================================

def create_reactive_demo():
    """创建响应式功能演示"""
    
    # 计数器按钮
    def increment():
        app_state.counter.value += 1
        
    def decrement():
        app_state.counter.value -= 1
        
    def reset():
        app_state.counter.value = 0
    
    # 名称更新
    def change_name():
        names = ["macUI v4", "响应式框架", "现代UI", "PyObjC"]
        current_index = names.index(app_state.name.value) if app_state.name.value in names else 0
        next_index = (current_index + 1) % len(names)
        app_state.name.value = names[next_index]
    
    # 乘数调整
    def adjust_multiplier():
        app_state.multiplier.value = 3 if app_state.multiplier.value == 2 else 2
    
    # 创建响应式标签 (这里需要实现Signal绑定)
    counter_label = Label("计数: 0", style=ComponentStyle(width=px(200), height=px(30)))
    doubled_label = Label("双倍: 0", style=ComponentStyle(width=px(200), height=px(30)))
    greeting_label = Label("Hello, macUI v4!", style=ComponentStyle(width=px(200), height=px(30)))
    complex_label = Label("复杂计算: 10", style=ComponentStyle(width=px(200), height=px(30)))
    
    # Effect: 当状态变化时更新UI
    def update_counter_display():
        # 这里需要实现响应式绑定到Label的text属性
        pass
    
    # 创建按钮
    buttons_container = Container(
        children=[
            Button("+ 增加", on_click=increment, style=ComponentStyle(width=px(80), height=px(30))),
            Button("- 减少", on_click=decrement, style=ComponentStyle(width=px(80), height=px(30))),
            Button("重置", on_click=reset, style=ComponentStyle(width=px(60), height=px(30))),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            gap=px(10)
        )
    )
    
    control_buttons = Container(
        children=[
            Button("更换名称", on_click=change_name, style=ComponentStyle(width=px(100), height=px(30))),
            Button("切换乘数", on_click=adjust_multiplier, style=ComponentStyle(width=px(100), height=px(30))),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            gap=px(10)
        )
    )
    
    return Container(
        children=[
            Label("🔄 响应式系统演示", style=ComponentStyle(width=px(300), height=px(40))),
            
            # 状态显示区
            counter_label,
            doubled_label,
            greeting_label,
            complex_label,
            
            # 控制按钮区
            buttons_container,
            control_buttons,
            
            # 说明文本
            Label("演示了Signal、Computed和Effect的响应式特性", 
                  style=ComponentStyle(width=px(400), height=px(30))),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            gap=px(15),
            width=percent(100),
            height=percent(80)
        )
    )

# ================================
# 2️⃣ 布局演示页
# ================================

def create_layout_demo():
    """创建布局功能演示"""
    
    def toggle_layout():
        app_state.layout_mode.value = "row" if app_state.layout_mode.value == "column" else "column"
        
    def toggle_alignment():
        alignments = ["center", "flex-start", "flex-end", "stretch"]
        current = app_state.alignment.value
        current_index = alignments.index(current) if current in alignments else 0
        next_index = (current_index + 1) % len(alignments)
        app_state.alignment.value = alignments[next_index]
    
    # 演示盒子
    def create_demo_box(text, color_index):
        colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow"]
        return Label(
            text,
            style=ComponentStyle(
                width=px(100),
                height=px(60),
                # 这里需要实现背景色支持
            )
        )
    
    demo_boxes = [
        create_demo_box("Box 1", 0),
        create_demo_box("Box 2", 1),
        create_demo_box("Box 3", 2),
    ]
    
    # 布局容器 (需要实现动态样式更新)
    layout_container = Container(
        children=demo_boxes,
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,  # 这需要动态更新
            align_items=AlignItems.CENTER,        # 这需要动态更新
            gap=px(10),
            width=px(400),
            height=px(200)
        )
    )
    
    return Container(
        children=[
            Label("📐 布局系统演示", style=ComponentStyle(width=px(300), height=px(40))),
            
            # 控制按钮
            Container(
                children=[
                    Button("切换方向", on_click=toggle_layout, style=ComponentStyle(width=px(100), height=px(30))),
                    Button("切换对齐", on_click=toggle_alignment, style=ComponentStyle(width=px(100), height=px(30))),
                ],
                style=ComponentStyle(
                    display=Display.FLEX,
                    flex_direction=FlexDirection.ROW,
                    gap=px(10)
                )
            ),
            
            # 动态布局区
            layout_container,
            
            # 状态显示
            Label(f"当前布局: column, 对齐: center", style=ComponentStyle(width=px(300), height=px(30))),
            Label("演示了Flexbox布局和动态样式更新", style=ComponentStyle(width=px(400), height=px(30))),
        ],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            gap=px(15),
            width=percent(100),
            height=percent(80)
        )
    )

# ================================
# 🏗️ 主应用组件
# ================================

def create_main_app():
    """创建主应用界面"""
    
    # 创建标题
    title = Label(
        "🎨 macUI v4 Feature Showcase",
        style=ComponentStyle(
            width=percent(100),
            height=px(60),
            # 需要实现文本居中和字体大小
        )
    )
    
    # 创建标签栏
    tab_bar = create_tab_bar()
    
    # 创建内容区域 (需要实现动态内容切换)
    content_area = Container(
        children=[create_reactive_demo()],  # 默认显示响应式演示
        style=ComponentStyle(
            width=percent(100),
            height=percent(70),
        )
    )
    
    # 主容器
    main_container = Container(
        children=[title, tab_bar, content_area],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            width=percent(100),
            height=percent(100),
            gap=px(10)
        )
    )
    
    return main_container

# ================================
# 🚀 应用启动器
# ================================

class ShowcaseAppDelegate(NSObject):
    """应用委托类"""
    
    def applicationDidFinishLaunching_(self, notification):
        """应用启动完成"""
        print("🚀 macUI v4 Showcase 应用启动")
        
        # 初始化管理器系统
        ManagerFactory.initialize_all()
        
        # 创建窗口
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 900, 700),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable,
            2,  # NSBackingStoreBuffered
            False
        )
        
        window.setTitle_("macUI v4 Feature Showcase")
        window.makeKeyAndOrderFront_(None)
        
        # 创建主应用UI
        main_app = create_main_app()
        main_view = main_app.mount()
        
        # 设置窗口内容
        window.setContentView_(main_view)
        
        # 保持强引用
        self.window = window
        self.main_app = main_app
        
        print("✅ 应用界面创建完成")
    
    def applicationWillTerminate_(self, notification):
        """应用即将终止"""
        print("👋 应用退出，清理资源")
        if hasattr(self, 'main_app'):
            self.main_app.cleanup()

def main():
    """主函数"""
    print("🎨 启动 macUI v4 Feature Showcase")
    
    # 创建应用
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    
    # 设置委托
    delegate = ShowcaseAppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    # 启动事件循环
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()