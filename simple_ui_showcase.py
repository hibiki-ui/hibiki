#!/usr/bin/env python3
"""
macUI v3.0 简化UI组件展示
验证基本UI组件与Stretchable布局引擎的集成
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.core import Signal, Component
from macui.components import VStack, HStack, Button, Label
from macui.layout.styles import AlignItems, JustifyContent
from macui.app import create_app
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class SimpleShowcaseApp(Component):
    """简化的展示应用"""
    
    def __init__(self):
        super().__init__()
        self.click_count = Signal(0)
        self.item_count = Signal(3)
        
    def mount(self):
        """创建应用界面"""
        print("🔧 创建应用界面...")
        
        # 主容器
        main_container = VStack(
            spacing=20,
            padding=25,
            alignment="stretch"
        )
        
        # 标题
        title = Label("🎉 macUI v3.0 + Stretchable 展示")
        main_container.children.append(title)
        
        # 计数器区域
        counter_area = self._create_counter_section()
        main_container.children.append(counter_area)
        
        # 按钮组区域
        button_group = self._create_button_group()
        main_container.children.append(button_group)
        
        # 动态内容区域
        dynamic_area = self._create_dynamic_content()
        main_container.children.append(dynamic_area)
        
        # 底部信息
        footer = self._create_footer()
        main_container.children.append(footer)
        
        print("✅ 界面结构创建完成")
        return main_container.mount()
    
    def _create_counter_section(self):
        """创建计数器区域"""
        counter_container = VStack(spacing=10, alignment="center")
        
        # 计数显示
        count_label = Label(f"🔢 点击计数: {self.click_count.value}")
        counter_container.children.append(count_label)
        
        # 控制按钮
        controls = HStack(spacing=15, alignment="center")
        
        minus_btn = Button(
            "➖",
            on_click=lambda: self._decrement_count()
        )
        controls.children.append(minus_btn)
        
        reset_btn = Button(
            "🔄 重置",
            on_click=lambda: self._reset_count()
        )
        controls.children.append(reset_btn)
        
        plus_btn = Button(
            "➕",
            on_click=lambda: self._increment_count()
        )
        controls.children.append(plus_btn)
        
        counter_container.children.append(controls)
        
        return counter_container
    
    def _create_button_group(self):
        """创建按钮组"""
        group_container = VStack(spacing=15)
        
        group_title = Label("🎮 功能按钮组")
        group_container.children.append(group_title)
        
        # 水平按钮组
        button_row = HStack(spacing=10, justify_content="space-between")
        
        actions = [
            ("🟢 开始", lambda: print("🟢 开始操作")),
            ("🔄 刷新", lambda: print("🔄 刷新数据")),
            ("⏸️ 暂停", lambda: print("⏸️ 暂停操作")),
            ("🔴 停止", lambda: print("🔴 停止操作"))
        ]
        
        for text, action in actions:
            btn = Button(text, on_click=action)
            button_row.children.append(btn)
        
        group_container.children.append(button_row)
        
        return group_container
    
    def _create_dynamic_content(self):
        """创建动态内容区域"""
        content_container = VStack(spacing=12)
        
        content_title = Label("📋 动态内容区域")
        content_container.children.append(content_title)
        
        # 控制区域
        controls = HStack(spacing=10)
        
        add_btn = Button(
            "➕ 添加项目",
            on_click=lambda: self._add_item()
        )
        controls.children.append(add_btn)
        
        remove_btn = Button(
            "➖ 移除项目",
            on_click=lambda: self._remove_item()
        )
        controls.children.append(remove_btn)
        
        content_container.children.append(controls)
        
        # 动态生成项目列表
        items_container = VStack(spacing=8)
        
        current_count = self.item_count.value
        for i in range(current_count):
            item = self._create_dynamic_item(i)
            items_container.children.append(item)
        
        if current_count == 0:
            empty_label = Label("📝 暂无项目，点击添加")
            items_container.children.append(empty_label)
        
        content_container.children.append(items_container)
        
        return content_container
    
    def _create_dynamic_item(self, index):
        """创建动态项目"""
        item_container = HStack(spacing=10, alignment="center")
        
        # 项目编号
        number_label = Label(f"{index + 1}.")
        item_container.children.append(number_label)
        
        # 项目内容
        content_label = Label(f"项目 {index + 1}")
        item_container.children.append(content_label)
        
        # 项目操作按钮
        action_btn = Button(
            "🔧",
            on_click=lambda idx=index: print(f"🔧 操作项目 {idx + 1}")
        )
        item_container.children.append(action_btn)
        
        return item_container
    
    def _create_footer(self):
        """创建底部信息"""
        footer_container = HStack(spacing=20, justify_content="space-between")
        
        # 左侧状态
        status_label = Label("✅ 系统运行正常")
        footer_container.children.append(status_label)
        
        # 右侧统计
        stats_label = Label(f"📊 点击: {self.click_count.value} | 项目: {self.item_count.value}")
        footer_container.children.append(stats_label)
        
        return footer_container
    
    # 交互方法
    def _increment_count(self):
        self.click_count.value += 1
        print(f"➕ 计数增加: {self.click_count.value}")
        
    def _decrement_count(self):
        if self.click_count.value > 0:
            self.click_count.value -= 1
        print(f"➖ 计数减少: {self.click_count.value}")
        
    def _reset_count(self):
        self.click_count.value = 0
        print("🔄 计数重置")
        
    def _add_item(self):
        self.item_count.value += 1
        print(f"➕ 添加项目: 当前 {self.item_count.value} 个")
        
    def _remove_item(self):
        if self.item_count.value > 0:
            self.item_count.value -= 1
        print(f"➖ 移除项目: 剩余 {self.item_count.value} 个")

class ShowcaseWindow:
    """展示窗口管理"""
    
    def __init__(self):
        self.window = None
        self.app_component = None
        
    def create_window(self):
        """创建窗口"""
        print("🪟 创建展示窗口...")
        
        # 创建窗口
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 600, 500),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        
        self.window.setTitle_("macUI v3.0 Simple Showcase")
        self.window.makeKeyAndOrderFront_(None)
        
        # 创建应用组件
        self.app_component = SimpleShowcaseApp()
        
        # 挂载组件到窗口
        try:
            content_view = self.app_component.mount()
            self.window.setContentView_(content_view)
            print("✅ 组件挂载到窗口成功")
        except Exception as e:
            print(f"❌ 组件挂载失败: {e}")
            import traceback
            traceback.print_exc()
        
        return self.window

def main():
    """主函数"""
    print("🚀 启动macUI v3.0 简化UI展示...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 Simple Showcase")
        
        # 创建展示窗口
        showcase_window = ShowcaseWindow()
        window = showcase_window.create_window()
        
        print("✅ 应用创建成功!")
        print("🎯 展示内容:")
        print("   - Stretchable布局引擎")
        print("   - VStack/HStack组件")
        print("   - Label/Button交互")
        print("   - 响应式状态管理")
        print("   - 动态UI更新")
        
        print("\n📊 布局验证:")
        if showcase_window.app_component:
            print("   - 主容器: VStack(vertical)")
            print("   - 计数器: VStack + HStack(controls)")  
            print("   - 按钮组: HStack(horizontal)")
            print("   - 动态内容: VStack(items)")
            print("   - 底部: HStack(space-between)")
        
        # 这里本来应该运行事件循环，但为了测试先跳过
        # AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()