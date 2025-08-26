#!/usr/bin/env python3
"""
按钮点击测试
专门调试按钮点击事件处理
"""

import sys
import os

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

# 设置详细日志
set_log_level("DEBUG")

# 创建专门的按钮测试日志器
import logging
button_logger = logging.getLogger("macui.button_test")
button_logger.setLevel(logging.DEBUG)
button_logger.handlers.clear()

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('BUTTON | %(message)s'))
button_logger.addHandler(console_handler)

button_logger.info("=== 按钮点击测试开始 ===")

class ButtonClickTestApp(Component):
    """按钮点击测试应用"""
    
    def __init__(self):
        button_logger.info("🚀 ButtonClickTestApp.__init__: 开始初始化")
        super().__init__()
        
        # 创建响应式状态
        button_logger.info("📊 创建Signal(counter)...")
        self.counter = self.create_signal(0)
        button_logger.info(f"📊 Signal(counter)已创建: 初始值={self.counter.value}, ID={id(self.counter)}")
        
        # 创建计算属性
        button_logger.info("🧮 创建Computed(counter_text)...")
        self.counter_text = self.create_computed(lambda: f"点击次数: {self.counter.value}")
        button_logger.info(f"🧮 Computed(counter_text)已创建: 初始值='{self.counter_text.value}', ID={id(self.counter_text)}")
        
        # 创建监控Effect
        button_logger.info("👁️ 创建监控Effect...")
        def state_monitor():
            button_logger.info(f"👁️ STATE_MONITOR: counter={self.counter.value}, text='{self.counter_text.value}'")
        
        self.monitor_effect = Effect(state_monitor)
        button_logger.info("👁️ 监控Effect已创建并执行")
        
        # 记录依赖关系
        button_logger.info("🔗 依赖关系分析:")
        button_logger.info(f"    - Signal[{id(self.counter)}] 观察者: {len(self.counter._observers)} 个")
        button_logger.info(f"    - Computed[{id(self.counter_text)}] 观察者: {len(self.counter_text._observers)} 个")
        
        button_logger.info("✅ ButtonClickTestApp初始化完成")
    
    def increment_handler(self):
        """增加计数器的处理函数"""
        button_logger.info("")
        button_logger.info("🟢" + "="*60)
        button_logger.info("🟢 BUTTON CLICK EVENT: increment_handler() 被调用")
        button_logger.info("🟢" + "="*60)
        
        # 记录点击前状态
        old_value = self.counter.value
        old_text = self.counter_text.value
        button_logger.info("📍 点击前状态:")
        button_logger.info(f"    - counter.value = {old_value}")
        button_logger.info(f"    - counter_text.value = '{old_text}'")
        button_logger.info(f"    - Signal观察者数: {len(self.counter._observers)}")
        button_logger.info(f"    - Computed观察者数: {len(self.counter_text._observers)}")
        
        # 执行状态变更 - 在主线程执行
        button_logger.info("⚡ 准备在主线程执行状态变更...")
        
        from PyObjCTools import AppHelper
        
        def update_on_main_thread():
            button_logger.info("⚡ 在主线程执行状态变更: self.counter.value += 1")
            self.counter.value += 1
            button_logger.info("⚡ 主线程状态变更语句执行完毕")
            
            # 记录更新后状态
            new_value = self.counter.value
            new_text = self.counter_text.value
            button_logger.info("📍 更新后状态:")
            button_logger.info(f"    - counter.value = {new_value} (变化: {old_value} -> {new_value})")
            button_logger.info(f"    - counter_text.value = '{new_text}' (变化: '{old_text}' -> '{new_text}')")
            
            button_logger.info("✅ Increment操作完成")
            button_logger.info("🟢" + "="*60)
            button_logger.info("")
        
        # 如果已经在主线程，直接执行；否则切换到主线程
        import threading
        if threading.current_thread() is threading.main_thread():
            button_logger.info("⚡ 当前已在主线程，直接执行")
            update_on_main_thread()
        else:
            button_logger.info("⚡ 当前在后台线程，切换到主线程执行")
            AppHelper.callAfter(update_on_main_thread)
    
    def decrement_handler(self):
        """减少计数器的处理函数"""
        button_logger.info("")
        button_logger.info("🔴" + "="*60)
        button_logger.info("🔴 BUTTON CLICK EVENT: decrement_handler() 被调用")
        button_logger.info("🔴" + "="*60)
        
        button_logger.info("⚡ 执行状态变更: self.counter.value -= 1")
        self.counter.value -= 1
        button_logger.info("⚡ 状态变更完成")
        
        button_logger.info("✅ Decrement操作完成")
        button_logger.info("🔴" + "="*60)
        button_logger.info("")
    
    def reset_handler(self):
        """重置计数器的处理函数"""
        button_logger.info("")
        button_logger.info("🔄" + "="*60)
        button_logger.info("🔄 BUTTON CLICK EVENT: reset_handler() 被调用")
        button_logger.info("🔄" + "="*60)
        
        button_logger.info("⚡ 执行状态变更: self.counter.value = 0")
        self.counter.value = 0
        button_logger.info("⚡ 状态变更完成")
        
        button_logger.info("✅ Reset操作完成")
        button_logger.info("🔄" + "="*60)
        button_logger.info("")
    
    def mount(self):
        """构建组件的视图结构"""
        button_logger.info("🏗️ 开始构建UI结构...")
        
        # 创建标签
        button_logger.info("🏷️ 创建标签...")
        counter_label = Label(self.counter_text)
        button_logger.info(f"🏷️ Label已创建并绑定")
        
        # 创建按钮 - 添加详细日志
        button_logger.info("🔘 创建按钮...")
        button_logger.info("🔘 创建Increment按钮，handler=self.increment_handler")
        increment_btn = Button("➕ 点击增加", on_click=self.increment_handler)
        button_logger.info(f"🔘 Increment按钮已创建: {type(increment_btn)}[{id(increment_btn)}]")
        
        button_logger.info("🔘 创建Decrement按钮，handler=self.decrement_handler")
        decrement_btn = Button("➖ 点击减少", on_click=self.decrement_handler)
        button_logger.info(f"🔘 Decrement按钮已创建: {type(decrement_btn)}[{id(decrement_btn)}]")
        
        button_logger.info("🔘 创建Reset按钮，handler=self.reset_handler")
        reset_btn = Button("🔄 重置", on_click=self.reset_handler)
        button_logger.info(f"🔘 Reset按钮已创建: {type(reset_btn)}[{id(reset_btn)}]")
        
        # 构建布局
        layout = VStack(spacing=25, padding=40, children=[
            Label("🔘 按钮点击测试", frame=(0, 0, 300, 30)),
            Label("点击按钮测试响应式更新 - 查看控制台日志", frame=(0, 0, 350, 20)),
            
            VStack(spacing=15, children=[
                counter_label,
                Label(f"Handler函数: increment_handler, decrement_handler, reset_handler", frame=(0, 0, 400, 20)),
            ]),
            
            VStack(spacing=10, children=[
                increment_btn,
                decrement_btn, 
                reset_btn
            ])
        ])
        
        button_logger.info("✅ UI结构构建完成")
        return layout

def main():
    """主函数"""
    button_logger.info("🚀 按钮点击测试应用启动")
    
    try:
        # 创建应用
        button_logger.info("📱 创建MacUIApp...")
        app = MacUIApp("Button Click Test")
        
        # 创建窗口
        button_logger.info("🪟 创建窗口...")
        window = app.create_window(
            title="macUI 按钮点击测试",
            size=(500, 450),
            resizable=True,
            content=ButtonClickTestApp()
        )
        
        # 显示窗口
        button_logger.info("👀 显示窗口...")
        window.show()
        
        button_logger.info("🎬 应用已就绪！")
        button_logger.info("📝 点击按钮测试响应式更新")
        button_logger.info("📂 监控控制台日志查看详细按钮点击处理过程")
        button_logger.info("🔍 如果没有看到点击事件日志，说明按钮事件绑定有问题")
        
        # 运行应用事件循环
        app.run()
        
    except Exception as e:
        button_logger.error(f"❌ 应用运行错误: {e}")
        import traceback
        button_logger.error(f"❌ 详细错误信息:\n{traceback.format_exc()}")
        raise
    finally:
        button_logger.info("🏁 按钮点击测试会话结束")

if __name__ == "__main__":
    main()