#!/usr/bin/env python3
"""
macUI v2 计数器示例

这个示例演示了 macUI v2 的核心功能：
- 响应式信号 (Signal)
- 计算属性 (Computed)
- 组件系统 (Component)
- 布局组件 (VStack, HStack)
- 基础控件 (Button, Label)
- 应用程序和窗口管理

运行方式:
    python counter.py
"""

import sys
import os

# 添加父目录到路径以便导入 macui
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 使用正确的包导入路径
from macui import Signal, Computed, Effect, Component, set_log_level
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

# 启用调试日志
set_log_level("INFO")


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


class AdvancedCounterApp(Component):
    """高级计数器应用 - 展示更多功能"""
    
    def __init__(self):
        super().__init__()
        
        # 多个计数器
        self.counter1 = self.create_signal(0)
        self.counter2 = self.create_signal(0)
        
        # 计算总和
        self.total = self.create_computed(
            lambda: self.counter1.value + self.counter2.value
        )
        
        # 步长控制
        self.step = self.create_signal(1)
        
        # 历史记录
        self.history = self.create_signal([])
        
        # 添加历史记录的副作用
        self.create_effect(self._update_history)
    
    def _update_history(self):
        """更新历史记录"""
        current_total = self.total.value
        current_history = self.history.value
        
        # 只保留最近 5 条记录
        new_history = current_history[-4:] + [current_total]
        
        if new_history != current_history:
            self.history.value = new_history
    
    def increment_counter1(self):
        self.counter1.value += self.step.value
    
    def increment_counter2(self):
        self.counter2.value += self.step.value
    
    def reset_all(self):
        self.counter1.value = 0
        self.counter2.value = 0
        self.history.value = []
    
    def set_step(self, new_step):
        self.step.value = new_step
    
    def mount(self):
        return VStack(spacing=20, padding=30, children=[
            Label("Advanced Counter Demo", frame=(0, 0, 400, 30)),
            
            # 步长控制
            HStack(spacing=10, children=[
                Label("Step:"),
                Button("1", on_click=lambda: self.set_step(1)),
                Button("5", on_click=lambda: self.set_step(5)),
                Button("10", on_click=lambda: self.set_step(10)),
            ]),
            
            # 计数器区域
            HStack(spacing=30, children=[
                VStack(spacing=10, children=[
                    Label("Counter 1"),
                    Label(Computed(lambda: str(self.counter1.value))),
                    Button("Increment", on_click=self.increment_counter1)
                ]),
                VStack(spacing=10, children=[
                    Label("Counter 2"),
                    Label(Computed(lambda: str(self.counter2.value))),
                    Button("Increment", on_click=self.increment_counter2)
                ])
            ]),
            
            # 总和显示
            Label(Computed(lambda: f"Total: {self.total.value}")),
            
            # 历史记录
            VStack(spacing=5, children=[
                Label("Recent totals:"),
                Label(Computed(lambda: " -> ".join(map(str, self.history.value)) or "No history"))
            ]),
            
            # 重置按钮
            Button("Reset All", on_click=self.reset_all)
        ])


def run_basic_counter():
    """运行基础计数器示例"""
    print("Starting basic counter demo...")
    
    # 创建应用程序
    app = MacUIApp("Basic Counter Demo")
    
    # 创建窗口
    window = app.create_window(
        title="macUI v2 - Counter Demo",
        size=(400, 500),
        resizable=True,
        content=CounterApp()
    )
    
    # 显示窗口
    window.show()
    
    # 运行应用
    app.run()


def run_advanced_counter():
    """运行高级计数器示例"""
    print("Starting advanced counter demo...")
    
    app = MacUIApp("Advanced Counter Demo")
    
    window = app.create_window(
        title="macUI v2 - Advanced Counter",
        size=(500, 600),
        resizable=True,
        content=AdvancedCounterApp()
    )
    
    window.show()
    app.run()


def test_reactive_system():
    """测试响应式系统"""
    print("\n=== Testing Reactive System ===")
    
    # 测试 Signal
    print("Testing Signal:")
    count = Signal(0)
    print(f"Initial value: {count.value}")
    
    count.value = 5
    print(f"After setting to 5: {count.value}")
    
    # 测试 Computed
    print("\nTesting Computed:")
    double = Computed(lambda: count.value * 2)
    print(f"Double of {count.value} is {double.value}")
    
    count.value = 10
    print(f"After changing count to 10, double is: {double.value}")
    
    # 测试 Effect
    print("\nTesting Effect:")
    effect_calls = []
    
    def log_effect():
        effect_calls.append(count.value)
        print(f"Effect called with count: {count.value}")
    
    effect = Effect(log_effect)
    count.value = 15
    count.value = 20
    
    print(f"Effect was called {len(effect_calls)} times with values: {effect_calls}")
    
    effect.cleanup()
    print("Effect cleaned up")


if __name__ == "__main__":
    print("macUI v2 Counter Example")
    print("========================")
    
    # 首先测试响应式系统
    test_reactive_system()
    
    # 然后选择运行哪个示例
    print("\nAvailable demos:")
    print("1. Basic Counter (default)")
    print("2. Advanced Counter")
    print("3. Exit")
    
    try:
        choice = input("\nSelect demo (1-3): ").strip()
        
        if choice == "2":
            run_advanced_counter()
        elif choice == "3":
            print("Goodbye!")
        else:
            run_basic_counter()
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()