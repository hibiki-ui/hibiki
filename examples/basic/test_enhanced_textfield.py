#!/usr/bin/env python3
"""
测试增强的 TextField 组件
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, set_log_level
from macui.components import TextField, VStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class TextFieldTestApp:
    """TextField 测试应用"""
    
    def __init__(self):
        # 创建测试信号
        self.basic_text = Signal("")
        self.password_text = Signal("")
        self.validated_text = Signal("")
        self.formatted_text = Signal("")
        
        # 消息显示
        self.message = Signal("准备测试 TextField 组件...")
        
    def on_basic_change(self, text):
        self.message.value = f"基础文本框改变: '{text}'"
        
    def on_password_change(self, text):
        self.message.value = f"密码框改变: '{text}' (长度: {len(text)})"
        
    def validate_email(self, text):
        """简单的邮箱验证"""
        if not text:
            return True  # 空文本允许
        return "@" in text and "." in text.split("@")[-1]
        
    def format_phone(self, text):
        """电话号码格式化"""
        # 只保留数字
        digits = ''.join(c for c in text if c.isdigit())
        
        # 格式化为 (123) 456-7890
        if len(digits) <= 3:
            return digits
        elif len(digits) <= 6:
            return f"({digits[:3]}) {digits[3:]}"
        else:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:10]}"
            
    def on_enter_pressed(self):
        self.message.value = "检测到回车键！"
        
    def on_focus_gained(self):
        self.message.value = "文本框获得焦点"
        
    def on_focus_lost(self):
        self.message.value = "文本框失去焦点"
        
    def clear_all(self):
        self.basic_text.value = ""
        self.password_text.value = ""
        self.validated_text.value = ""
        self.formatted_text.value = ""
        self.message.value = "所有文本框已清空"

def main():
    print("=== TextField 增强功能测试 ===")
    
    app = MacUIApp("TextField Enhanced Test")
    test_app = TextFieldTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class TextFieldTestComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("TextField 增强功能测试", frame=(0, 0, 400, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # 基础文本框
                    Label("1. 基础文本框:"),
                    TextField(
                        value=test_app.basic_text,
                        placeholder="输入任何文本...",
                        on_change=test_app.on_basic_change,
                        tooltip="这是基础文本框"
                    ),
                    
                    # 密码框
                    Label("2. 密码框:"),
                    TextField(
                        value=test_app.password_text,
                        placeholder="输入密码...",
                        secure=True,
                        on_change=test_app.on_password_change,
                        tooltip="密码将被隐藏"
                    ),
                    
                    # 邮箱验证文本框
                    Label("3. 邮箱验证 (必须包含@和.)"),
                    TextField(
                        value=test_app.validated_text,
                        placeholder="输入邮箱地址...",
                        validation=test_app.validate_email,
                        tooltip="输入有效的邮箱地址"
                    ),
                    
                    # 电话号码格式化文本框
                    Label("4. 电话格式化 (最多10位数字)"),
                    TextField(
                        value=test_app.formatted_text,
                        placeholder="输入电话号码...",
                        formatting=test_app.format_phone,
                        max_length=14,  # (123) 456-7890
                        tooltip="自动格式化电话号码"
                    ),
                    
                    # 回车和焦点测试
                    Label("5. 事件测试 (试试回车、获得/失去焦点)"),
                    TextField(
                        placeholder="按回车或切换焦点试试...",
                        on_enter=test_app.on_enter_pressed,
                        on_focus=test_app.on_focus_gained,
                        on_blur=test_app.on_focus_lost,
                        tooltip="测试键盘和焦点事件"
                    ),
                    
                    # 控制按钮
                    Button("清空所有", on_click=test_app.clear_all),
                    
                    # 显示当前值
                    Label(lambda: f"基础文本: '{test_app.basic_text.value}'"),
                    Label(lambda: f"密码长度: {len(test_app.password_text.value)}"),
                    Label(lambda: f"邮箱: '{test_app.validated_text.value}'"),
                    Label(lambda: f"电话: '{test_app.formatted_text.value}'"),
                ])
        
        return TextFieldTestComponent()
    
    # 创建窗口
    window = app.create_window(
        title="TextField Enhanced Test",
        size=(500, 700),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - 基础文本输入和双向绑定")
    print("   - 密码框（文本隐藏）")
    print("   - 邮箱验证（必须包含@和.）")
    print("   - 电话号码自动格式化")
    print("   - 回车键和焦点事件")
    print("   - 最大长度限制")
    print("   - 工具提示")
    
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