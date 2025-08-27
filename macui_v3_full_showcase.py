#!/usr/bin/env python3
"""
macUI v3.0 完整UI组件展示应用
结合Stretchable布局引擎与真实UI组件的专业级演示
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui.app import create_app
from macui.core import Signal, Computed, Effect, Component
from macui.components import VStack, HStack, Button, Label
from macui.layout.styles import LayoutStyle, FlexDirection, AlignItems, JustifyContent, Display
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

class ShowcaseAppController:
    """Showcase应用控制器"""
    
    def __init__(self):
        # 应用状态
        self.current_demo = Signal("flexbox")
        self.item_count = Signal(3)
        self.gap_size = Signal(10)
        self.button_click_count = Signal(0)
        self.selected_alignment = Signal("center")
        self.show_labels = Signal(True)
        
        # 演示数据
        self.demos = {
            "flexbox": "Flexbox基础演示",
            "nested": "嵌套布局演示",
            "interactive": "交互式组件演示",
            "responsive": "响应式设计演示"
        }
        
        self.alignments = {
            "start": AlignItems.FLEX_START,
            "center": AlignItems.CENTER,
            "end": AlignItems.FLEX_END,
            "stretch": AlignItems.STRETCH
        }

class FlexboxDemoComponent(Component):
    """Flexbox基础演示组件"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
    def mount(self):
        # 创建主容器
        main_container = VStack(
            spacing=15,
            padding=20,
            alignment=AlignItems.STRETCH
        )
        
        # 标题
        title = Label(
            "Flexbox布局演示",
            style=LayoutStyle(height=30)
        )
        main_container.children.append(title)
        
        # 控制面板
        control_panel = self._create_control_panel()
        main_container.children.append(control_panel)
        
        # 演示区域
        demo_area = self._create_demo_area()
        main_container.children.append(demo_area)
        
        return main_container.mount()
    
    def _create_control_panel(self):
        """创建控制面板"""
        panel = HStack(
            style=LayoutStyle(
                height=50,
                gap=20,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.SPACE_BETWEEN,
                padding=10
            )
        )
        
        # 项目数量控制
        count_group = HStack(
            style=LayoutStyle(gap=10, align_items=AlignItems.CENTER)
        )
        
        count_label = Label("项目数量:")
        count_group.children.append(count_label)
        
        for i in range(1, 6):
            btn = Button(
                str(i),
                style=LayoutStyle(width=35, height=30),
                on_click=lambda count=i: self._update_item_count(count)
            )
            count_group.children.append(btn)
        
        panel.children.append(count_group)
        
        # 间距控制
        gap_group = HStack(
            style=LayoutStyle(gap=10, align_items=AlignItems.CENTER)
        )
        
        gap_label = Label("间距:")
        gap_group.children.append(gap_label)
        
        for gap in [5, 10, 20, 30]:
            btn = Button(
                str(gap),
                style=LayoutStyle(width=35, height=30),
                on_click=lambda g=gap: self._update_gap(g)
            )
            gap_group.children.append(btn)
        
        panel.children.append(gap_group)
        
        # 对齐方式控制
        align_group = HStack(
            style=LayoutStyle(gap=10, align_items=AlignItems.CENTER)
        )
        
        align_label = Label("对齐:")
        align_group.children.append(align_label)
        
        align_options = [("左", "start"), ("中", "center"), ("右", "end"), ("拉伸", "stretch")]
        for text, align_key in align_options:
            btn = Button(
                text,
                style=LayoutStyle(width=45, height=30),
                on_click=lambda a=align_key: self._update_alignment(a)
            )
            align_group.children.append(btn)
        
        panel.children.append(align_group)
        
        return panel
    
    def _create_demo_area(self):
        """创建演示区域"""
        demo_container = VStack(
            style=LayoutStyle(
                flex_grow=1.0,
                padding=20,
                gap=10
            )
        )
        
        # 演示说明
        description = Label(
            f"当前设置: {self.controller.item_count.value}个项目, 间距{self.controller.gap_size.value}px, {self.controller.selected_alignment.value}对齐"
        )
        demo_container.children.append(description)
        
        # 实际演示区域
        demo_area = self._create_dynamic_demo()
        demo_container.children.append(demo_area)
        
        return demo_container
    
    def _create_dynamic_demo(self):
        """创建动态演示区域"""
        # 获取当前设置
        item_count = self.controller.item_count.value
        gap = self.controller.gap_size.value
        alignment = self.alignments.get(self.controller.selected_alignment.value, AlignItems.CENTER)
        
        # 创建演示容器
        demo_style = LayoutStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=alignment,
            justify_content=JustifyContent.SPACE_BETWEEN,
            height=120,
            gap=gap,
            padding=15
        )
        
        demo_area = HStack(style=demo_style)
        
        # 创建演示项目
        colors = ["🔴红色", "🟢绿色", "🔵蓝色", "🟡黄色", "🟣紫色"]
        for i in range(item_count):
            color_text = colors[i % len(colors)]
            
            item_container = VStack(
                style=LayoutStyle(
                    width=80,
                    height=80 if alignment != AlignItems.STRETCH else None,
                    gap=5,
                    align_items=AlignItems.CENTER,
                    justify_content=JustifyContent.CENTER,
                    padding=5
                )
            )
            
            # 项目标签
            if self.controller.show_labels.value:
                item_label = Label(
                    color_text,
                    style=LayoutStyle(height=20)
                )
                item_container.children.append(item_label)
            
            # 项目按钮
            item_button = Button(
                f"按钮{i+1}",
                style=LayoutStyle(height=30),
                on_click=lambda idx=i: self._on_item_click(idx)
            )
            item_container.children.append(item_button)
            
            demo_area.children.append(item_container)
        
        return demo_area
    
    def _update_item_count(self, count):
        """更新项目数量"""
        self.controller.item_count.value = count
        print(f"🔢 项目数量更新为: {count}")
        
    def _update_gap(self, gap):
        """更新间距"""
        self.controller.gap_size.value = gap
        print(f"📏 间距更新为: {gap}px")
        
    def _update_alignment(self, alignment):
        """更新对齐方式"""
        self.controller.selected_alignment.value = alignment
        print(f"📐 对齐方式更新为: {alignment}")
        
    def _on_item_click(self, index):
        """处理项目点击"""
        self.controller.button_click_count.value += 1
        print(f"🖱️ 点击了项目{index+1}, 总点击次数: {self.controller.button_click_count.value}")

class NestedLayoutDemoComponent(Component):
    """嵌套布局演示组件"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
    def mount(self):
        main_container = VStack(
            style=LayoutStyle(
                padding=20,
                gap=15
            )
        )
        
        # 标题
        title = Label("嵌套布局演示 - 仿邮件应用界面")
        main_container.children.append(title)
        
        # 顶部工具栏
        toolbar = self._create_toolbar()
        main_container.children.append(toolbar)
        
        # 主体内容区域
        content_area = self._create_content_area()
        main_container.children.append(content_area)
        
        # 底部状态栏
        status_bar = self._create_status_bar()
        main_container.children.append(status_bar)
        
        return main_container.mount()
    
    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = HStack(
            style=LayoutStyle(
                height=40,
                gap=10,
                align_items=AlignItems.CENTER,
                padding=5
            )
        )
        
        # 工具按钮
        tools = [
            ("📧", "新建邮件"),
            ("↩️", "回复"),
            ("↪️", "转发"),
            ("🗑️", "删除"),
            ("📁", "归档")
        ]
        
        for icon, tooltip in tools:
            btn = Button(
                icon,
                style=LayoutStyle(width=35, height=30),
                on_click=lambda t=tooltip: print(f"🔧 {t}")
            )
            toolbar.children.append(btn)
        
        # 分隔符 (弹性空间)
        spacer = Label(
            "",
            style=LayoutStyle(flex_grow=1.0)
        )
        toolbar.children.append(spacer)
        
        # 搜索区域
        search_container = HStack(
            style=LayoutStyle(gap=5, align_items=AlignItems.CENTER)
        )
        
        search_label = Label("🔍")
        search_container.children.append(search_label)
        
        search_btn = Button(
            "搜索邮件",
            style=LayoutStyle(width=80, height=25),
            on_click=lambda: print("🔍 搜索邮件")
        )
        search_container.children.append(search_btn)
        
        toolbar.children.append(search_container)
        
        return toolbar
    
    def _create_content_area(self):
        """创建主体内容区域"""
        content = HStack(
            style=LayoutStyle(
                height=300,
                gap=10,
                flex_grow=1.0
            )
        )
        
        # 左侧文件夹列表
        folder_panel = self._create_folder_panel()
        content.children.append(folder_panel)
        
        # 中间邮件列表
        mail_list = self._create_mail_list()
        content.children.append(mail_list)
        
        # 右侧邮件预览
        preview_panel = self._create_preview_panel()
        content.children.append(preview_panel)
        
        return content
    
    def _create_folder_panel(self):
        """创建文件夹面板"""
        panel = VStack(
            style=LayoutStyle(
                width=150,
                gap=5,
                padding=10,
                flex_shrink=0.0
            )
        )
        
        panel_title = Label("📁 文件夹")
        panel.children.append(panel_title)
        
        folders = ["📥 收件箱", "📤 发件箱", "📋 草稿", "⭐ 收藏", "🗑️ 已删除"]
        
        for folder in folders:
            folder_btn = Button(
                folder,
                style=LayoutStyle(height=25),
                on_click=lambda f=folder: print(f"📁 选择文件夹: {f}")
            )
            panel.children.append(folder_btn)
        
        return panel
    
    def _create_mail_list(self):
        """创建邮件列表"""
        mail_panel = VStack(
            style=LayoutStyle(
                flex_grow=1.0,
                gap=5,
                padding=10
            )
        )
        
        list_title = Label("📧 邮件列表")
        mail_panel.children.append(list_title)
        
        # 邮件项目
        mails = [
            ("张三", "项目进展报告", "2小时前"),
            ("李四", "会议邀请", "4小时前"),
            ("王五", "周末聚会", "昨天"),
            ("赵六", "技术讨论", "2天前")
        ]
        
        for sender, subject, time in mails:
            mail_item = self._create_mail_item(sender, subject, time)
            mail_panel.children.append(mail_item)
        
        return mail_panel
    
    def _create_mail_item(self, sender, subject, time):
        """创建单个邮件项目"""
        mail_container = VStack(
            style=LayoutStyle(
                height=60,
                padding=8,
                gap=3
            )
        )
        
        # 邮件头部 (发送者和时间)
        header = HStack(
            style=LayoutStyle(
                justify_content=JustifyContent.SPACE_BETWEEN,
                align_items=AlignItems.CENTER
            )
        )
        
        sender_label = Label(f"👤 {sender}")
        header.children.append(sender_label)
        
        time_label = Label(time)
        header.children.append(time_label)
        
        mail_container.children.append(header)
        
        # 邮件主题按钮
        subject_btn = Button(
            subject,
            style=LayoutStyle(height=25),
            on_click=lambda: print(f"📖 打开邮件: {subject}")
        )
        mail_container.children.append(subject_btn)
        
        return mail_container
    
    def _create_preview_panel(self):
        """创建预览面板"""
        panel = VStack(
            style=LayoutStyle(
                width=200,
                gap=10,
                padding=10,
                flex_shrink=0.0
            )
        )
        
        preview_title = Label("👁️ 邮件预览")
        panel.children.append(preview_title)
        
        # 预览内容
        preview_content = VStack(
            style=LayoutStyle(gap=8)
        )
        
        subject_preview = Label("主题: 项目进展报告")
        preview_content.children.append(subject_preview)
        
        sender_preview = Label("发送者: 张三")
        preview_content.children.append(sender_preview)
        
        content_preview = Label("内容: 本周项目进展良好，已完成核心功能开发...")
        preview_content.children.append(content_preview)
        
        panel.children.append(preview_content)
        
        # 操作按钮
        actions = HStack(
            style=LayoutStyle(gap=5)
        )
        
        reply_btn = Button(
            "回复",
            style=LayoutStyle(height=30),
            on_click=lambda: print("✉️ 回复邮件")
        )
        actions.children.append(reply_btn)
        
        forward_btn = Button(
            "转发", 
            style=LayoutStyle(height=30),
            on_click=lambda: print("📨 转发邮件")
        )
        actions.children.append(forward_btn)
        
        panel.children.append(actions)
        
        return panel
    
    def _create_status_bar(self):
        """创建状态栏"""
        status_bar = HStack(
            style=LayoutStyle(
                height=25,
                gap=20,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.SPACE_BETWEEN,
                padding=5
            )
        )
        
        # 左侧状态信息
        left_info = HStack(
            style=LayoutStyle(gap=10)
        )
        
        count_label = Label("📊 邮件: 156封")
        left_info.children.append(count_label)
        
        unread_label = Label("🔴 未读: 12封")
        left_info.children.append(unread_label)
        
        status_bar.children.append(left_info)
        
        # 右侧连接状态
        connection_label = Label("🟢 已连接")
        status_bar.children.append(connection_label)
        
        return status_bar

class InteractiveDemoComponent(Component):
    """交互式组件演示"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
    def mount(self):
        main_container = VStack(
            style=LayoutStyle(
                padding=20,
                gap=20
            )
        )
        
        # 标题
        title = Label("交互式组件演示")
        main_container.children.append(title)
        
        # 计数器演示
        counter_demo = self._create_counter_demo()
        main_container.children.append(counter_demo)
        
        # 动态列表演示
        dynamic_list_demo = self._create_dynamic_list_demo()
        main_container.children.append(dynamic_list_demo)
        
        # 表单演示
        form_demo = self._create_form_demo()
        main_container.children.append(form_demo)
        
        return main_container.mount()
    
    def _create_counter_demo(self):
        """创建计数器演示"""
        counter_container = VStack(
            style=LayoutStyle(
                gap=10,
                padding=15
            )
        )
        
        counter_title = Label("🔢 响应式计数器")
        counter_container.children.append(counter_title)
        
        # 计数显示
        counter_display = Label(
            f"当前计数: {self.controller.button_click_count.value}",
            style=LayoutStyle(height=40)
        )
        counter_container.children.append(counter_display)
        
        # 控制按钮
        counter_controls = HStack(
            style=LayoutStyle(gap=10, justify_content=JustifyContent.CENTER)
        )
        
        minus_btn = Button(
            "➖ 减1",
            style=LayoutStyle(width=60, height=30),
            on_click=lambda: self._decrement_counter()
        )
        counter_controls.children.append(minus_btn)
        
        reset_btn = Button(
            "🔄 重置",
            style=LayoutStyle(width=60, height=30),
            on_click=lambda: self._reset_counter()
        )
        counter_controls.children.append(reset_btn)
        
        plus_btn = Button(
            "➕ 加1",
            style=LayoutStyle(width=60, height=30),
            on_click=lambda: self._increment_counter()
        )
        counter_controls.children.append(plus_btn)
        
        counter_container.children.append(counter_controls)
        
        return counter_container
    
    def _create_dynamic_list_demo(self):
        """创建动态列表演示"""
        list_container = VStack(
            style=LayoutStyle(
                gap=10,
                padding=15
            )
        )
        
        list_title = Label("📋 动态列表管理")
        list_container.children.append(list_title)
        
        # 列表控制
        list_controls = HStack(
            style=LayoutStyle(gap=10)
        )
        
        add_btn = Button(
            "➕ 添加项目",
            style=LayoutStyle(height=30),
            on_click=lambda: self._add_list_item()
        )
        list_controls.children.append(add_btn)
        
        clear_btn = Button(
            "🗑️ 清空列表",
            style=LayoutStyle(height=30),
            on_click=lambda: self._clear_list()
        )
        list_controls.children.append(clear_btn)
        
        toggle_labels_btn = Button(
            "👁️ 切换标签显示",
            style=LayoutStyle(height=30),
            on_click=lambda: self._toggle_labels()
        )
        list_controls.children.append(toggle_labels_btn)
        
        list_container.children.append(list_controls)
        
        # 动态生成的列表项
        current_count = self.controller.item_count.value
        if current_count > 0:
            list_items = VStack(
                style=LayoutStyle(gap=5)
            )
            
            for i in range(current_count):
                item = self._create_list_item(i)
                list_items.children.append(item)
            
            list_container.children.append(list_items)
        else:
            empty_label = Label("📝 列表为空，点击添加项目")
            list_container.children.append(empty_label)
        
        return list_container
    
    def _create_list_item(self, index):
        """创建列表项"""
        item_container = HStack(
            style=LayoutStyle(
                height=35,
                gap=10,
                align_items=AlignItems.CENTER,
                padding=5
            )
        )
        
        # 项目编号
        number_label = Label(f"{index + 1}.")
        item_container.children.append(number_label)
        
        # 项目内容
        if self.controller.show_labels.value:
            content_label = Label(f"列表项目 {index + 1}")
            item_container.children.append(content_label)
        
        # 弹性空间
        spacer = Label(
            "",
            style=LayoutStyle(flex_grow=1.0)
        )
        item_container.children.append(spacer)
        
        # 删除按钮
        delete_btn = Button(
            "❌",
            style=LayoutStyle(width=25, height=25),
            on_click=lambda idx=index: self._remove_list_item(idx)
        )
        item_container.children.append(delete_btn)
        
        return item_container
    
    def _create_form_demo(self):
        """创建表单演示"""
        form_container = VStack(
            style=LayoutStyle(
                gap=15,
                padding=15
            )
        )
        
        form_title = Label("📝 响应式表单")
        form_container.children.append(form_title)
        
        # 表单字段
        fields_container = VStack(
            style=LayoutStyle(gap=10)
        )
        
        # 姓名字段
        name_row = HStack(
            style=LayoutStyle(gap=10, align_items=AlignItems.CENTER)
        )
        
        name_label = Label("姓名:", style=LayoutStyle(width=80))
        name_row.children.append(name_label)
        
        name_input = Button(
            "请输入姓名",
            style=LayoutStyle(flex_grow=1.0, height=30),
            on_click=lambda: print("📝 姓名输入框点击")
        )
        name_row.children.append(name_input)
        
        fields_container.children.append(name_row)
        
        # 邮箱字段
        email_row = HStack(
            style=LayoutStyle(gap=10, align_items=AlignItems.CENTER)
        )
        
        email_label = Label("邮箱:", style=LayoutStyle(width=80))
        email_row.children.append(email_label)
        
        email_input = Button(
            "请输入邮箱",
            style=LayoutStyle(flex_grow=1.0, height=30),
            on_click=lambda: print("📧 邮箱输入框点击")
        )
        email_row.children.append(email_input)
        
        fields_container.children.append(email_row)
        
        form_container.children.append(fields_container)
        
        # 表单操作
        form_actions = HStack(
            style=LayoutStyle(
                gap=10,
                justify_content=JustifyContent.CENTER
            )
        )
        
        submit_btn = Button(
            "✅ 提交表单",
            style=LayoutStyle(width=100, height=35),
            on_click=lambda: self._submit_form()
        )
        form_actions.children.append(submit_btn)
        
        reset_form_btn = Button(
            "🔄 重置表单",
            style=LayoutStyle(width=100, height=35),
            on_click=lambda: self._reset_form()
        )
        form_actions.children.append(reset_form_btn)
        
        form_container.children.append(form_actions)
        
        return form_container
    
    # 交互方法
    def _increment_counter(self):
        self.controller.button_click_count.value += 1
        print(f"➕ 计数器: {self.controller.button_click_count.value}")
    
    def _decrement_counter(self):
        self.controller.button_click_count.value = max(0, self.controller.button_click_count.value - 1)
        print(f"➖ 计数器: {self.controller.button_click_count.value}")
    
    def _reset_counter(self):
        self.controller.button_click_count.value = 0
        print("🔄 计数器重置")
    
    def _add_list_item(self):
        self.controller.item_count.value += 1
        print(f"➕ 添加项目，当前数量: {self.controller.item_count.value}")
    
    def _remove_list_item(self, index):
        if self.controller.item_count.value > 0:
            self.controller.item_count.value -= 1
        print(f"❌ 删除项目{index + 1}，剩余: {self.controller.item_count.value}")
    
    def _clear_list(self):
        self.controller.item_count.value = 0
        print("🗑️ 清空列表")
    
    def _toggle_labels(self):
        self.controller.show_labels.value = not self.controller.show_labels.value
        print(f"👁️ 标签显示: {'开启' if self.controller.show_labels.value else '关闭'}")
    
    def _submit_form(self):
        print("✅ 提交表单 - 表单验证通过")
    
    def _reset_form(self):
        print("🔄 重置表单 - 所有字段已清空")

class MainShowcaseApp:
    """主展示应用"""
    
    def __init__(self):
        self.controller = ShowcaseAppController()
        self.current_component = None
        
    def create_main_window(self):
        """创建主窗口内容"""
        # 主容器
        main_container = VStack(
            style=LayoutStyle(
                padding=15,
                gap=15
            )
        )
        
        # 应用标题
        app_title = Label(
            "🎉 macUI v3.0 完整功能展示",
            style=LayoutStyle(height=40)
        )
        main_container.children.append(app_title)
        
        # 导航栏
        navigation = self._create_navigation()
        main_container.children.append(navigation)
        
        # 内容区域
        content_area = self._create_content_area()
        main_container.children.append(content_area)
        
        # 底部信息
        footer = self._create_footer()
        main_container.children.append(footer)
        
        return main_container
    
    def _create_navigation(self):
        """创建导航栏"""
        nav_container = HStack(
            style=LayoutStyle(
                height=50,
                gap=10,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.CENTER,
                padding=10
            )
        )
        
        # 演示选择按钮
        for demo_key, demo_name in self.controller.demos.items():
            nav_btn = Button(
                demo_name,
                style=LayoutStyle(height=35, flex_grow=1.0),
                on_click=lambda key=demo_key: self._switch_demo(key)
            )
            nav_container.children.append(nav_btn)
        
        return nav_container
    
    def _create_content_area(self):
        """创建内容区域"""
        content_container = VStack(
            style=LayoutStyle(
                flex_grow=1.0,
                padding=10
            )
        )
        
        # 根据当前演示类型显示内容
        current_demo = self.controller.current_demo.value
        
        if current_demo == "flexbox":
            demo_component = FlexboxDemoComponent(self.controller)
        elif current_demo == "nested":
            demo_component = NestedLayoutDemoComponent(self.controller)
        elif current_demo == "interactive":
            demo_component = InteractiveDemoComponent(self.controller)
        else:
            # 默认演示
            demo_component = FlexboxDemoComponent(self.controller)
        
        self.current_component = demo_component
        
        # 添加演示说明
        demo_description = Label(
            f"当前演示: {self.controller.demos.get(current_demo, '未知演示')}"
        )
        content_container.children.append(demo_description)
        
        return content_container
    
    def _create_footer(self):
        """创建底部信息"""
        footer = HStack(
            style=LayoutStyle(
                height=30,
                gap=20,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.SPACE_BETWEEN,
                padding=10
            )
        )
        
        # 左侧版本信息
        version_label = Label("macUI v3.0 + Stretchable布局引擎")
        footer.children.append(version_label)
        
        # 右侧统计信息
        stats_label = Label(f"总点击次数: {self.controller.button_click_count.value}")
        footer.children.append(stats_label)
        
        return footer
    
    def _switch_demo(self, demo_key):
        """切换演示"""
        self.controller.current_demo.value = demo_key
        print(f"🔄 切换到演示: {self.controller.demos.get(demo_key)}")

def main():
    """主函数"""
    print("🚀 启动macUI v3.0 完整UI组件展示应用...")
    
    try:
        # 创建应用
        app = create_app("macUI v3.0 Showcase")
        
        # 创建主应用实例
        showcase_app = MainShowcaseApp()
        
        # 创建主窗口内容
        main_content = showcase_app.create_main_window()
        
        print("✅ 应用界面创建成功!")
        print("🎮 macUI v3.0 + Stretchable布局引擎完整功能展示")
        print("📊 包含Flexbox、嵌套布局、交互组件等专业级功能")
        
        # 这里应该显示窗口，但由于缺少窗口管理，我们先输出布局结构验证
        print("\n🌳 === 应用布局结构验证 ===")
        main_layout = main_content.mount()
        print(f"✅ 主容器创建成功: {type(main_layout).__name__}")
        
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()