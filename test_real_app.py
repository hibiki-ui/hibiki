#!/usr/bin/env python3
"""
macUI v2 真实应用测试

这个脚本测试 macUI v2 在真实 PyObjC 环境中的功能。
"""

import sys
import os

# 确保可以导入 macui 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from core.signal import Signal, Computed, Effect
        print("  ✅ 核心响应式系统导入成功")
        
        from core.component import Component
        print("  ✅ 组件系统导入成功")
        
        from core.binding import ReactiveBinding, EventBinding
        print("  ✅ 绑定系统导入成功")
        
        from components.controls import Button, TextField, Label
        print("  ✅ 控件组件导入成功")
        
        from components.layout import VStack, HStack
        print("  ✅ 布局组件导入成功")
        
        from app import MacUIApp, Window
        print("  ✅ 应用管理导入成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_counter():
    """测试基本的计数器功能"""
    print("\n🧮 测试基本计数器...")
    
    try:
        from core.signal import Signal, Computed
        from core.component import Component
        from components.controls import Button, Label
        from components.layout import VStack, HStack
        
        class SimpleCounter(Component):
            def __init__(self):
                super().__init__()
                self.count = self.create_signal(0)
                self.count_text = self.create_computed(
                    lambda: f"Count: {self.count.value}"
                )
                print(f"  📊 计数器创建，初始值: {self.count.value}")
            
            def increment(self):
                old_value = self.count.value
                self.count.value += 1
                print(f"  ➕ 计数器: {old_value} -> {self.count.value}")
            
            def decrement(self):
                old_value = self.count.value
                self.count.value -= 1
                print(f"  ➖ 计数器: {old_value} -> {self.count.value}")
            
            def mount(self):
                print("  🖥️  挂载计数器组件...")
                
                # 创建标签
                label = Label(self.count_text)
                print("  📝 标签创建完成")
                
                # 创建按钮
                inc_button = Button("Increment", on_click=self.increment)
                dec_button = Button("Decrement", on_click=self.decrement)
                print("  🔘 按钮创建完成")
                
                # 创建布局
                button_stack = HStack(spacing=10, children=[inc_button, dec_button])
                main_stack = VStack(spacing=20, padding=20, children=[label, button_stack])
                print("  📐 布局创建完成")
                
                return main_stack
        
        # 创建组件实例
        counter = SimpleCounter()
        
        # 测试方法调用
        counter.increment()
        counter.increment()
        counter.decrement()
        
        # 挂载组件
        view = counter.mount()
        print(f"  ✅ 组件挂载成功: {type(view).__name__}")
        
        # 清理
        counter.cleanup()
        print("  🧹 组件清理完成")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 计数器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_window_creation():
    """测试窗口创建"""
    print("\n🪟 测试窗口创建...")
    
    try:
        from app import MacUIApp, Window
        from core.component import Component
        from components.controls import Label
        
        class HelloWorld(Component):
            def mount(self):
                return Label("Hello, macUI v2!")
        
        # 创建应用
        app = MacUIApp("Test App")
        print("  📱 应用创建成功")
        
        # 创建窗口
        window = app.create_window(
            title="Test Window",
            size=(300, 200),
            content=HelloWorld()
        )
        print("  🪟 窗口创建成功")
        
        # 测试窗口属性
        window.set_title("Updated Title")
        window.set_size(400, 250)
        print("  ⚙️  窗口属性更新成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 窗口创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_interactive_counter():
    """创建可交互的计数器应用"""
    print("\n🚀 创建交互式计数器应用...")
    
    try:
        from core.signal import Signal, Computed
        from core.component import Component
        from components.controls import Button, Label, TextField
        from components.layout import VStack, HStack
        from app import MacUIApp, Window
        
        class InteractiveCounter(Component):
            def __init__(self):
                super().__init__()
                self.count = self.create_signal(0)
                self.step = self.create_signal(1)
                self.input_text = self.create_signal("")
                
                # 计算属性
                self.count_display = self.create_computed(
                    lambda: f"当前计数: {self.count.value}"
                )
                
                self.step_display = self.create_computed(
                    lambda: f"步长: {self.step.value}"
                )
                
                self.double_count = self.create_computed(
                    lambda: f"双倍: {self.count.value * 2}"
                )
                
                self.is_even = self.create_computed(
                    lambda: "偶数" if self.count.value % 2 == 0 else "奇数"
                )
                
                print(f"  🎯 交互式计数器创建，初始计数: {self.count.value}")
            
            def increment(self):
                old_value = self.count.value
                self.count.value += self.step.value
                print(f"  ⬆️  增加: {old_value} + {self.step.value} = {self.count.value}")
            
            def decrement(self):
                old_value = self.count.value
                self.count.value -= self.step.value
                print(f"  ⬇️  减少: {old_value} - {self.step.value} = {self.count.value}")
            
            def reset(self):
                old_value = self.count.value
                self.count.value = 0
                print(f"  🔄 重置: {old_value} -> 0")
            
            def set_step_1(self): 
                self.step.value = 1
                print("  📏 步长设为 1")
            
            def set_step_5(self): 
                self.step.value = 5
                print("  📏 步长设为 5")
            
            def set_step_10(self): 
                self.step.value = 10
                print("  📏 步长设为 10")
            
            def on_text_change(self, text):
                print(f"  ✏️  文本输入: '{text}'")
                try:
                    if text.strip():
                        value = int(text.strip())
                        self.count.value = value
                        print(f"  🔢 计数设为: {value}")
                except ValueError:
                    pass  # 忽略无效输入
            
            def mount(self):
                print("  🔧 构建交互界面...")
                
                # 显示区域
                display_area = VStack(spacing=10, children=[
                    Label(self.count_display),
                    Label(self.double_count),
                    Label(Computed(lambda: f"状态: {self.is_even.value}"))
                ])
                
                # 控制按钮
                main_buttons = HStack(spacing=10, children=[
                    Button("➕", on_click=self.increment),
                    Button("➖", on_click=self.decrement),
                    Button("🔄", on_click=self.reset)
                ])
                
                # 步长控制
                step_buttons = HStack(spacing=8, children=[
                    Label("步长:"),
                    Button("1", on_click=self.set_step_1),
                    Button("5", on_click=self.set_step_5),  
                    Button("10", on_click=self.set_step_10)
                ])
                
                # 文本输入
                input_area = VStack(spacing=5, children=[
                    Label("直接输入数值:"),
                    TextField(
                        value=self.input_text,
                        placeholder="输入数字...",
                        on_change=self.on_text_change
                    )
                ])
                
                # 主布局
                main_layout = VStack(spacing=20, padding=30, children=[
                    Label("🧮 macUI v2 交互式计数器"),
                    display_area,
                    main_buttons,
                    step_buttons,
                    input_area,
                    Label(self.step_display)
                ])
                
                print("  ✅ 界面构建完成")
                return main_layout
        
        # 创建应用和窗口
        app = MacUIApp("macUI v2 Interactive Counter")
        counter_component = InteractiveCounter()
        
        window = app.create_window(
            title="macUI v2 - 交互式计数器",
            size=(400, 500),
            resizable=True,
            content=counter_component
        )
        
        print(f"  📱 应用创建完成: {app.app_name}")
        print(f"  🪟 窗口就绪: {window.title}")
        
        return app, window, counter_component
        
    except Exception as e:
        print(f"  ❌ 交互应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def main():
    """主测试函数"""
    print("🎉 macUI v2 真实环境测试")
    print("=" * 40)
    
    # 检查 PyObjC
    try:
        import objc
        from AppKit import NSApplication
        print(f"✅ PyObjC 版本: {objc.__version__ if hasattr(objc, '__version__') else '已安装'}")
    except ImportError:
        print("❌ PyObjC 未安装!")
        return False
    
    success = True
    
    # 测试导入
    if not test_imports():
        success = False
    
    # 测试基本功能
    if not test_basic_counter():
        success = False
    
    # 测试窗口
    if not test_window_creation():
        success = False
    
    if success:
        print("\n" + "=" * 40)
        print("✅ 所有基本测试通过!")
        print("🚀 准备创建真实应用...")
        
        # 创建交互应用
        app, window, counter = create_interactive_counter()
        
        if app and window and counter:
            print("\n" + "🎊" * 20)
            print("🎊 macUI v2 应用已准备就绪! 🎊")  
            print("🎊" * 20)
            print("\n📋 准备启动应用:")
            print(f"   应用名称: {app.app_name}")
            print(f"   窗口标题: {window.title}")
            print(f"   窗口大小: {window.size}")
            print("\n💡 现在可以:")
            print("   1. 调用 window.show() 显示窗口")
            print("   2. 调用 app.run() 启动应用主循环")
            
            # 询问是否启动
            try:
                choice = input("\n是否启动应用? (y/N): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    print("\n🚀 启动应用...")
                    window.show()
                    app.run()  # 这将阻塞直到应用退出
                    print("👋 应用已退出")
                else:
                    print("📝 应用创建完成但未启动")
                    print("   你可以手动调用 window.show() 和 app.run()")
                    
            except KeyboardInterrupt:
                print("\n⏹️  操作已取消")
            
            return True
        else:
            print("❌ 应用创建失败")
            return False
    else:
        print("\n❌ 部分测试失败，需要修复问题")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    else:
        print("\n🎉 测试完成!")