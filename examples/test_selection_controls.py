#!/usr/bin/env python3
"""
测试选择控件：Checkbox, RadioButton, Switch
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from macui import Signal, set_log_level
from macui.components import Checkbox, RadioButton, Switch, VStack, HStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class SelectionControlsTestApp:
    """选择控件测试应用"""
    
    def __init__(self):
        # Checkbox 状态
        self.enable_notifications = Signal(True)
        self.enable_sound = Signal(False)
        self.enable_vibration = Signal(True)
        
        # Switch 状态
        self.dark_mode = Signal(False)
        self.auto_save = Signal(True)
        
        # RadioButton 状态 (主题选择)
        self.theme = Signal("light")
        
        # RadioButton 状态 (语言选择)
        self.language = Signal("chinese")
        
        # 消息显示
        self.message = Signal("选择控件测试准备就绪")
        
    def on_notification_change(self, enabled):
        self.message.value = f"通知{'开启' if enabled else '关闭'}"
        
    def on_sound_change(self, enabled):
        self.message.value = f"声音{'开启' if enabled else '关闭'}"
        
    def on_vibration_change(self, enabled):
        self.message.value = f"震动{'开启' if enabled else '关闭'}"
        
    def on_dark_mode_change(self, enabled):
        self.message.value = f"深色模式{'开启' if enabled else '关闭'}"
        
    def on_auto_save_change(self, enabled):
        self.message.value = f"自动保存{'开启' if enabled else '关闭'}"
        
    def on_theme_change(self, theme):
        theme_names = {
            "light": "浅色主题",
            "dark": "深色主题", 
            "auto": "自动主题"
        }
        self.message.value = f"主题切换到: {theme_names.get(theme, theme)}"
        
    def on_language_change(self, language):
        language_names = {
            "chinese": "中文",
            "english": "English",
            "japanese": "日本語"
        }
        self.message.value = f"语言切换到: {language_names.get(language, language)}"
        
    def toggle_all_settings(self):
        # 切换所有设置的状态
        self.enable_notifications.value = not self.enable_notifications.value
        self.enable_sound.value = not self.enable_sound.value
        self.enable_vibration.value = not self.enable_vibration.value
        self.dark_mode.value = not self.dark_mode.value
        self.auto_save.value = not self.auto_save.value
        self.message.value = "所有设置已切换"
        
    def reset_all_settings(self):
        # 重置所有设置到默认值
        self.enable_notifications.value = True
        self.enable_sound.value = False
        self.enable_vibration.value = True
        self.dark_mode.value = False
        self.auto_save.value = True
        self.theme.value = "light"
        self.language.value = "chinese"
        self.message.value = "所有设置已重置为默认值"

def main():
    print("=== 选择控件测试 ===")
    
    app = MacUIApp("Selection Controls Test")
    test_app = SelectionControlsTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class SelectionControlsComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("选择控件测试", frame=(0, 0, 500, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # Checkbox 测试区域
                    Label("1. 复选框 (Checkbox):"),
                    VStack(spacing=8, children=[
                        Checkbox(
                            value=test_app.enable_notifications,
                            text="启用通知",
                            on_change=test_app.on_notification_change,
                            tooltip="控制是否接收通知"
                        ),
                        Checkbox(
                            value=test_app.enable_sound,
                            text="启用声音",
                            on_change=test_app.on_sound_change,
                            tooltip="控制是否播放声音"
                        ),
                        Checkbox(
                            value=test_app.enable_vibration,
                            text="启用震动",
                            on_change=test_app.on_vibration_change,
                            tooltip="控制是否震动反馈"
                        ),
                    ]),
                    
                    # Switch 测试区域
                    Label("2. 开关 (Switch):"),
                    VStack(spacing=8, children=[
                        HStack(spacing=10, children=[
                            Label("深色模式:"),
                            Switch(
                                value=test_app.dark_mode,
                                on_change=test_app.on_dark_mode_change,
                                tooltip="切换深色/浅色模式"
                            ),
                        ]),
                        HStack(spacing=10, children=[
                            Label("自动保存:"),
                            Switch(
                                value=test_app.auto_save,
                                on_change=test_app.on_auto_save_change,
                                tooltip="控制是否自动保存文档"
                            ),
                        ]),
                    ]),
                    
                    # RadioButton 测试区域 - 主题选择
                    Label("3. 单选按钮 (RadioButton) - 主题:"),
                    VStack(spacing=5, children=[
                        RadioButton(
                            value=test_app.theme,
                            option_value="light",
                            text="浅色主题",
                            on_change=test_app.on_theme_change,
                            tooltip="使用浅色界面主题"
                        ),
                        RadioButton(
                            value=test_app.theme,
                            option_value="dark",
                            text="深色主题",
                            on_change=test_app.on_theme_change,
                            tooltip="使用深色界面主题"
                        ),
                        RadioButton(
                            value=test_app.theme,
                            option_value="auto",
                            text="自动主题",
                            on_change=test_app.on_theme_change,
                            tooltip="根据系统设置自动选择主题"
                        ),
                    ]),
                    
                    # RadioButton 测试区域 - 语言选择
                    Label("4. 单选按钮 (RadioButton) - 语言:"),
                    HStack(spacing=15, children=[
                        RadioButton(
                            value=test_app.language,
                            option_value="chinese",
                            text="中文",
                            on_change=test_app.on_language_change,
                            tooltip="使用中文界面"
                        ),
                        RadioButton(
                            value=test_app.language,
                            option_value="english",
                            text="English",
                            on_change=test_app.on_language_change,
                            tooltip="Use English interface"
                        ),
                        RadioButton(
                            value=test_app.language,
                            option_value="japanese",
                            text="日本語",
                            on_change=test_app.on_language_change,
                            tooltip="日本語のインターフェースを使用"
                        ),
                    ]),
                    
                    # 控制按钮
                    HStack(spacing=15, children=[
                        Button("切换所有设置", on_click=test_app.toggle_all_settings),
                        Button("重置所有设置", on_click=test_app.reset_all_settings),
                    ]),
                    
                    # 实时显示当前状态
                    VStack(spacing=5, children=[
                        Label("当前设置状态:"),
                        Label(lambda: f"通知: {'✓' if test_app.enable_notifications.value else '✗'} | "
                                    f"声音: {'✓' if test_app.enable_sound.value else '✗'} | "
                                    f"震动: {'✓' if test_app.enable_vibration.value else '✗'}"),
                        Label(lambda: f"深色模式: {'✓' if test_app.dark_mode.value else '✗'} | "
                                    f"自动保存: {'✓' if test_app.auto_save.value else '✗'}"),
                        Label(lambda: f"主题: {test_app.theme.value} | 语言: {test_app.language.value}"),
                    ]),
                ])
        
        return SelectionControlsComponent()
    
    # 创建窗口
    window = app.create_window(
        title="Selection Controls Test",
        size=(550, 650),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - Checkbox: 多选复选框")
    print("   - Switch: 开关控件")
    print("   - RadioButton: 单选按钮组")
    print("   - 双向数据绑定")
    print("   - 实时状态更新")
    print("   - 工具提示")
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