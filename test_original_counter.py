#!/usr/bin/env python3
"""
测试原始counter示例的基本功能
直接运行CounterApp而不是通过菜单选择
"""

import sys
import os

# 使用正确的包导入路径
from macui import Signal, Computed, Effect, Component, set_log_level
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

# 启用调试日志
set_log_level("INFO")

# 复制原始的CounterApp类
class CounterApp(Component):
    """计数器应用组件"""
    
    def __init__(self):
        super().__init__()
        
        # 创建响应式状态
        self.count = self.create_signal(0)
        
        # 创建计算属性
        self.double = self.create_computed(lambda: self.count.value * 2)
        self.is_even = self.create_computed(lambda: self.count.value % 2 == 0)
        self.reset_enabled = self.create_computed(lambda: self.count.value != 0)
        
        # 创建格式化显示文本的计算属性
        self.count_text = self.create_computed(
            lambda: f"Count: {self.count.value}"
        )
        self.double_text = self.create_computed(
            lambda: f"Double: {self.double.value}"
        )
        self.status_text = self.create_computed(
            lambda: f"Status: {'Even' if self.is_even.value else 'Odd'}"
        )
    
    def increment(self):
        """增加计数"""
        self.count.value += 1
        print(f"Count incremented to: {self.count.value}")
    
    def decrement(self):
        """减少计数"""
        self.count.value -= 1
        print(f"Count decremented to: {self.count.value}")
    
    def reset(self):
        """重置计数"""
        old_value = self.count.value
        self.count.value = 0
        print(f"Count reset from {old_value} to 0")
    
    def mount(self):
        """构建组件的视图结构"""
        return VStack(spacing=20, padding=40, children=[
            # 标题
            Label("macUI v2 Counter Demo", frame=(0, 0, 300, 30)),
            
            # 显示区域
            VStack(spacing=10, children=[
                Label(self.count_text),
                Label(self.double_text),
                Label(self.status_text),
            ]),
            
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
                ),
                Button(
                    "Reset", 
                    on_click=self.reset,
                    enabled=self.reset_enabled,
                    tooltip="Reset count to zero"
                )
            ]),
            
            # 信息区域
            VStack(spacing=5, children=[
                Label("This demo showcases:"),
                Label("• Reactive signals (count)"),
                Label("• Computed properties (double, is_even)"),
                Label("• Dynamic button states (reset enabled)"),
                Label("• Layout components (VStack, HStack)"),
            ])
        ])

def run_counter_test():
    """运行计数器测试"""
    print("Starting original counter demo test...")
    
    # 创建应用程序
    app = MacUIApp("Counter Demo Test")
    
    # 创建窗口
    window = app.create_window(
        title="macUI v2 - Counter Demo (Test)",
        size=(400, 500),
        resizable=True,
        content=CounterApp()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 窗口已显示")
    print("📝 请点击按钮测试，按 Ctrl+C 退出")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        run_counter_test()
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()