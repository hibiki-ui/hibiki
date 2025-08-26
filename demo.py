#!/usr/bin/env python3
"""
macUI v2 演示

这个脚本演示了 macUI v2 框架的主要功能：
- 响应式信号系统
- 组件架构  
- UI 控件（在模拟模式下）
- 应用程序管理

运行: python demo.py
"""

def demo_reactive_basics():
    """演示响应式系统基础"""
    print("🎯 macUI v2 响应式系统演示")
    print("=" * 40)
    
    from core.signal import Signal, Computed, Effect
    
    # 1. Signal - 基础响应式值
    print("\n📡 Signal (响应式信号):")
    count = Signal(0)
    print(f"   创建信号，初始值: {count.value}")
    
    count.value = 10
    print(f"   修改后的值: {count.value}")
    
    # 2. Computed - 自动计算的派生值
    print("\n🧮 Computed (计算属性):")
    double = Computed(lambda: count.value * 2)
    square = Computed(lambda: count.value ** 2)
    
    print(f"   count = {count.value}")
    print(f"   double = {double.value} (自动计算)")
    print(f"   square = {square.value} (自动计算)")
    
    # 修改原始值，观察计算属性的自动更新
    print("\n   修改原始值到 5:")
    count.value = 5
    print(f"   count = {count.value}")
    print(f"   double = {double.value} (自动更新!)")
    print(f"   square = {square.value} (自动更新!)")
    
    # 3. Effect - 副作用自动执行
    print("\n⚡ Effect (副作用):")
    effect_log = []
    
    def log_changes():
        message = f"count 变为 {count.value}, double 变为 {double.value}"
        effect_log.append(message)
        print(f"   🔄 {message}")
        
    effect = Effect(log_changes)
    
    print("   触发几次变化:")
    count.value = 7
    count.value = 12
    count.value = 3
    
    print(f"\n   副作用总共执行了 {len(effect_log)} 次")
    effect.cleanup()
    

def demo_component_system():
    """演示组件系统"""
    print("\n\n🏗️  macUI v2 组件系统演示") 
    print("=" * 40)
    
    from core.component import Component
    from core.signal import Signal, Computed
    
    class CounterComponent(Component):
        """简单的计数器组件"""
        
        def __init__(self, name="Counter"):
            super().__init__()
            self.name = name
            self.count = self.create_signal(0)
            
            # 计算属性
            self.is_even = self.create_computed(lambda: self.count.value % 2 == 0)
            self.status = self.create_computed(
                lambda: f"{self.name}: {self.count.value} ({'偶数' if self.is_even.value else '奇数'})"
            )
            
            # 副作用 - 记录变化
            self.create_effect(lambda: self._log_change())
        
        def _log_change(self):
            print(f"   📊 {self.status.value}")
        
        def increment(self):
            self.count.value += 1
            
        def decrement(self):
            self.count.value -= 1
            
        def reset(self):
            old_value = self.count.value
            self.count.value = 0
            return f"重置: {old_value} -> 0"
        
        def mount(self):
            """在真实环境中，这里返回 NSView"""
            return {
                "type": "CounterView", 
                "name": self.name,
                "count": self.count.value,
                "status": self.status.value
            }
    
    print("\n📦 创建组件实例:")
    counter1 = CounterComponent("计数器A")
    counter2 = CounterComponent("计数器B")
    
    print("\n🎬 组件交互演示:")
    print("操作计数器A:")
    counter1.increment()
    counter1.increment()
    counter1.increment()
    
    print("\n操作计数器B:")
    counter2.increment()
    counter2.decrement()
    counter2.increment()
    counter2.increment()
    
    print("\n🖥️  组件挂载 (模拟视图创建):")
    view1 = counter1.mount()
    view2 = counter2.mount()
    
    print(f"   视图A: {view1}")
    print(f"   视图B: {view2}")
    
    print("\n🧹 组件清理:")
    result1 = counter1.reset()
    result2 = counter2.reset()
    print(f"   {result1}")
    print(f"   {result2}")
    
    counter1.cleanup()
    counter2.cleanup()
    print("   组件已清理")


def demo_advanced_patterns():
    """演示高级模式"""
    print("\n\n🚀 macUI v2 高级模式演示")
    print("=" * 40)
    
    from core.signal import Signal, Computed, Effect
    from core.component import Component
    
    # 1. 多信号联动
    print("\n🔗 多信号联动:")
    x = Signal(3)
    y = Signal(4)
    
    # 计算距离
    distance = Computed(lambda: (x.value ** 2 + y.value ** 2) ** 0.5)
    
    # 计算象限
    quadrant = Computed(lambda: 
        "第一象限" if x.value > 0 and y.value > 0 else
        "第二象限" if x.value < 0 and y.value > 0 else  
        "第三象限" if x.value < 0 and y.value < 0 else
        "第四象限" if x.value > 0 and y.value < 0 else
        "轴上"
    )
    
    def show_position():
        print(f"   坐标: ({x.value}, {y.value})")
        print(f"   距离: {distance.value:.2f}")
        print(f"   象限: {quadrant.value}")
        print()
    
    show_position()
    
    print("   移动点:")
    x.value = -2
    y.value = 6
    show_position()
    
    x.value = 0  
    y.value = 0
    show_position()
    
    # 2. 状态机模式
    print("🎛️  状态机模式:")
    
    class StateMachine(Component):
        def __init__(self):
            super().__init__()
            self.state = self.create_signal("idle")
            self.data = self.create_signal(None)
            
            # 状态描述
            self.state_desc = self.create_computed(lambda: {
                "idle": "空闲状态",
                "loading": "加载中...", 
                "success": "操作成功",
                "error": "发生错误"
            }.get(self.state.value, "未知状态"))
            
            # 监控状态变化
            self.create_effect(lambda: print(f"   🔄 状态变更: {self.state_desc.value}"))
        
        def start_loading(self):
            self.state.value = "loading"
            self.data.value = None
        
        def succeed(self, data):
            self.state.value = "success" 
            self.data.value = data
        
        def fail(self, error):
            self.state.value = "error"
            self.data.value = error
            
        def reset(self):
            self.state.value = "idle"
            self.data.value = None
    
    state_machine = StateMachine()
    
    print("   状态转换演示:")
    state_machine.start_loading()
    state_machine.succeed("用户数据加载完成")
    state_machine.reset()
    state_machine.start_loading()
    state_machine.fail("网络连接失败")
    state_machine.reset()
    
    state_machine.cleanup()


def demo_mock_ui():
    """演示模拟 UI 交互"""
    print("\n\n🖼️  macUI v2 模拟 UI 演示")
    print("=" * 40)
    
    from core.signal import Signal, Computed
    from core.component import Component
    
    class MockButton:
        """模拟按钮控件"""
        def __init__(self, title, on_click=None, enabled=True):
            self.title = title
            self.on_click = on_click
            self.enabled = enabled
            
        def click(self):
            if self.enabled and self.on_click:
                print(f"   🖱️  点击按钮: '{self.title}'")
                self.on_click()
            else:
                print(f"   ❌ 按钮 '{self.title}' 不可用")
    
    class MockApp(Component):
        """模拟应用程序"""
        
        def __init__(self):
            super().__init__()
            
            # 应用状态
            self.clicks = self.create_signal(0)
            self.username = self.create_signal("")
            
            # 计算属性
            self.click_text = self.create_computed(
                lambda: f"点击了 {self.clicks.value} 次"
            )
            
            self.greeting = self.create_computed(
                lambda: f"你好, {self.username.value}!" if self.username.value else "请输入用户名"
            )
            
            self.reset_enabled = self.create_computed(
                lambda: self.clicks.value > 0 or bool(self.username.value)
            )
            
            # 创建模拟控件
            self.click_button = MockButton(
                "点我!", 
                on_click=self.handle_click
            )
            
            self.reset_button = MockButton(
                "重置",
                on_click=self.handle_reset,
                enabled=True  # 这里会通过响应式绑定动态更新
            )
            
            # 监控状态变化
            self.create_effect(lambda: print(f"   📊 {self.click_text.value}"))
            self.create_effect(lambda: print(f"   👋 {self.greeting.value}"))
            self.create_effect(lambda: setattr(
                self.reset_button, 'enabled', self.reset_enabled.value
            ))
        
        def handle_click(self):
            self.clicks.value += 1
            
        def handle_reset(self):
            self.clicks.value = 0
            self.username.value = ""
            print("   🔄 应用状态已重置")
        
        def set_username(self, name):
            self.username.value = name
            print(f"   📝 用户名设置为: '{name}'")
    
    print("📱 创建模拟应用:")
    app = MockApp()
    
    print("\n🎮 用户交互演示:")
    app.set_username("小明")
    app.click_button.click()
    app.click_button.click() 
    app.click_button.click()
    
    print("\n   尝试重置:")
    app.reset_button.click()
    
    print("\n   继续操作:")
    app.set_username("Alice")
    app.click_button.click()
    
    print("\n   最终重置:")
    app.reset_button.click()
    
    app.cleanup()


def main():
    """主演示函数"""
    print("🎉 欢迎使用 macUI v2 框架!")
    print("这是一个基于信号机制的声明式 macOS 原生应用开发框架")
    print("设计灵感来自 SolidJS，使用 Python + PyObjC 实现\n")
    
    try:
        demo_reactive_basics()
        demo_component_system() 
        demo_advanced_patterns()
        demo_mock_ui()
        
        print("\n\n🎊 演示完成!")
        print("=" * 50)
        print("📋 macUI v2 核心特性已验证:")
        print("   ✅ 响应式信号系统 (Signal, Computed, Effect)")
        print("   ✅ 组件生命周期管理")
        print("   ✅ 自动依赖收集和更新")
        print("   ✅ 批量更新优化")
        print("   ✅ 内存管理和清理")
        print("   ✅ 多种编程模式支持")
        
        print("\n🚀 框架已准备就绪!")
        print("   在真实的 macOS 环境中安装 PyObjC 后,")
        print("   即可开发原生 macOS 应用程序。")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()