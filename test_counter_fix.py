#!/usr/bin/env python3
"""
测试修复后的counter示例
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, set_log_level
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

# 启用调试日志
set_log_level("INFO")

print("=== 测试修复后的Counter示例 ===")

class TestCounterApp(Component):
    """测试计数器应用"""
    
    def __init__(self):
        super().__init__()
        
        # 创建响应式状态
        self.count = self.create_signal(0)
        
        # 创建计算属性
        self.count_text = self.create_computed(
            lambda: f"Count: {self.count.value}"
        )
    
    def increment(self):
        """增加计数"""
        self.count.value += 1
        print(f"✅ Count incremented to: {self.count.value}")
    
    def decrement(self):
        """减少计数"""
        self.count.value -= 1
        print(f"✅ Count decremented to: {self.count.value}")
    
    def mount(self):
        """构建组件的视图结构"""
        return VStack(spacing=20, padding=40, children=[
            # 标题
            Label("Test Counter (Fixed)", frame=(0, 0, 300, 30)),
            
            # 显示区域
            Label(self.count_text),
            
            # 按钮区域
            HStack(spacing=15, children=[
                Button(
                    "Increment (+1)", 
                    on_click=self.increment,
                    tooltip="Increase count by 1"
                ),
                Button(
                    "Decrement (-1)", 
                    on_click=self.decrement,
                    tooltip="Decrease count by 1"
                )
            ])
        ])

def main():
    print("Starting counter test...")
    
    # 创建应用程序
    app = MacUIApp("Counter Test")
    
    # 创建窗口
    window = app.create_window(
        title="macUI v2 - Counter Test (Fixed)",
        size=(400, 300),
        resizable=True,
        content=TestCounterApp()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 窗口已显示")
    print("📝 请点击按钮测试，按 Ctrl+C 退出")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()