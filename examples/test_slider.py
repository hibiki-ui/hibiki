#!/usr/bin/env python3
"""
测试增强的 Slider 组件
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, set_log_level
from macui.components import Slider, VStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class SliderTestApp:
    """Slider 测试应用"""
    
    def __init__(self):
        # 创建测试信号
        self.basic_value = Signal(50.0)
        self.volume_value = Signal(75.0)
        self.temperature_value = Signal(20.0)
        self.precision_value = Signal(5.0)
        
        # 消息显示
        self.message = Signal("准备测试 Slider 组件...")
        
    def on_basic_change(self, value):
        self.message.value = f"基础滑块改变: {value:.1f}"
        
    def on_volume_change(self, value):
        self.message.value = f"音量滑块改变: {value:.0f}%"
        
    def on_temperature_change(self, value):
        self.message.value = f"温度滑块改变: {value:.1f}°C"
        
    def on_precision_change(self, value):
        self.message.value = f"精密滑块改变: {value:.2f} (步长0.25)"
        
    def reset_all(self):
        self.basic_value.value = 50.0
        self.volume_value.value = 75.0
        self.temperature_value.value = 20.0
        self.precision_value.value = 5.0
        self.message.value = "所有滑块已重置"

def main():
    print("=== Slider 组件测试 ===")
    
    app = MacUIApp("Slider Test")
    test_app = SliderTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class SliderTestComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("Slider 组件测试", frame=(0, 0, 400, 30)),
                    
                    # 消息显示
                    Label(test_app.message),
                    
                    # 基础滑块 (0-100)
                    Label("1. 基础滑块 (0-100):"),
                    Slider(
                        value=test_app.basic_value,
                        min_value=0.0,
                        max_value=100.0,
                        on_change=test_app.on_basic_change,
                        tooltip="基础滑块，范围 0-100",
                        frame=(0, 0, 300, 20)
                    ),
                    
                    # 音量滑块 (0-100, 步长5)
                    Label("2. 音量滑块 (0-100%, 步长5):"),
                    Slider(
                        value=test_app.volume_value,
                        min_value=0.0,
                        max_value=100.0,
                        step_size=5.0,
                        on_change=test_app.on_volume_change,
                        tooltip="音量控制，步长为5",
                        frame=(0, 0, 300, 20)
                    ),
                    
                    # 温度滑块 (-10 to 50)
                    Label("3. 温度滑块 (-10°C to 50°C):"),
                    Slider(
                        value=test_app.temperature_value,
                        min_value=-10.0,
                        max_value=50.0,
                        on_change=test_app.on_temperature_change,
                        tooltip="温度设置，范围 -10°C 到 50°C",
                        frame=(0, 0, 300, 20)
                    ),
                    
                    # 精密滑块 (0-10, 步长0.25)
                    Label("4. 精密滑块 (0-10, 步长0.25):"),
                    Slider(
                        value=test_app.precision_value,
                        min_value=0.0,
                        max_value=10.0,
                        step_size=0.25,
                        on_change=test_app.on_precision_change,
                        tooltip="精密控制，步长0.25",
                        frame=(0, 0, 300, 20)
                    ),
                    
                    # 垂直滑块
                    Label("5. 垂直滑块:"),
                    Slider(
                        value=test_app.basic_value,  # 复用基础值
                        min_value=0.0,
                        max_value=100.0,
                        orientation="vertical",
                        tooltip="垂直滑块",
                        frame=(0, 0, 20, 100)
                    ),
                    
                    # 控制按钮
                    Button("重置所有滑块", on_click=test_app.reset_all),
                    
                    # 显示当前值
                    Label(lambda: f"基础值: {test_app.basic_value.value:.1f}"),
                    Label(lambda: f"音量: {test_app.volume_value.value:.0f}%"),
                    Label(lambda: f"温度: {test_app.temperature_value.value:.1f}°C"),
                    Label(lambda: f"精密: {test_app.precision_value.value:.2f}"),
                ])
        
        return SliderTestComponent()
    
    # 创建窗口
    window = app.create_window(
        title="Slider Test",
        size=(500, 600),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - 基础滑块（0-100）")
    print("   - 音量滑块（步长5）")
    print("   - 温度滑块（负数范围）")
    print("   - 精密滑块（步长0.25）")
    print("   - 垂直滑块")
    print("   - 双向数据绑定")
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