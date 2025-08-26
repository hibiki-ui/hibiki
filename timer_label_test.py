#!/usr/bin/env python3
"""
定时器标签更新测试
用于验证UI更新机制是否工作
"""

import sys
import os
import threading
import time

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, Computed, Effect, Component, get_logger, set_log_level
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

# 设置详细日志
set_log_level("DEBUG")

# 创建专门的定时器测试日志器
import logging
timer_logger = logging.getLogger("macui.timer_test")
timer_logger.setLevel(logging.DEBUG)
timer_logger.handlers.clear()

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('TIMER | %(message)s'))
timer_logger.addHandler(console_handler)

timer_logger.info("=== 定时器标签测试开始 ===")

class TimerLabelTestApp(Component):
    """定时器标签测试应用"""
    
    def __init__(self):
        timer_logger.info("🚀 TimerLabelTestApp.__init__: 开始初始化")
        super().__init__()
        
        # 创建响应式状态
        timer_logger.info("📊 创建Signal(counter)...")
        self.counter = self.create_signal(0)
        timer_logger.info(f"📊 Signal(counter)已创建: 初始值={self.counter.value}, ID={id(self.counter)}")
        
        # 创建计算属性
        timer_logger.info("🧮 创建Computed(counter_text)...")
        self.counter_text = self.create_computed(lambda: f"计数器: {self.counter.value}")
        timer_logger.info(f"🧮 Computed(counter_text)已创建: 初始值='{self.counter_text.value}', ID={id(self.counter_text)}")
        
        # 创建监控Effect
        timer_logger.info("👁️ 创建监控Effect...")
        def state_monitor():
            timer_logger.info(f"👁️ STATE_MONITOR: counter={self.counter.value}, text='{self.counter_text.value}'")
        
        self.monitor_effect = Effect(state_monitor)
        timer_logger.info("👁️ 监控Effect已创建并执行")
        
        # 记录依赖关系
        timer_logger.info("🔗 依赖关系分析:")
        timer_logger.info(f"    - Signal[{id(self.counter)}] 观察者: {len(self.counter._observers)} 个")
        timer_logger.info(f"    - Computed[{id(self.counter_text)}] 观察者: {len(self.counter_text._observers)} 个")
        
        timer_logger.info("✅ TimerLabelTestApp初始化完成")
        
        # 启动定时器线程
        self.start_timer()
    
    def start_timer(self):
        """启动定时器"""
        timer_logger.info("⏰ 启动定时器线程...")
        def timer_thread():
            timer_logger.info("⏰ 定时器线程开始运行")
            timer_logger.info("⏰ 等待3秒后开始更新...")
            
            for i in range(1, 11):  # 更新10次
                time.sleep(3)  # 每3秒更新一次
                timer_logger.info("")
                timer_logger.info("⏰" + "="*50)
                timer_logger.info(f"⏰ 定时器触发 #{i} - 3秒间隔")
                timer_logger.info("⏰" + "="*50)
                
                # 记录更新前状态
                old_value = self.counter.value
                old_text = self.counter_text.value
                timer_logger.info("📍 更新前状态:")
                timer_logger.info(f"    - counter.value = {old_value}")
                timer_logger.info(f"    - counter_text.value = '{old_text}'")
                timer_logger.info(f"    - Signal观察者数: {len(self.counter._observers)}")
                timer_logger.info(f"    - Computed观察者数: {len(self.counter_text._observers)}")
                
                # 执行状态变更 - 确保在主线程执行
                timer_logger.info(f"⚡ 准备在主线程执行状态变更: self.counter.value = {i}")
                
                # 使用NSRunLoop在主线程执行UI更新
                from Foundation import NSRunLoop, NSDefaultRunLoopMode
                from PyObjCTools import AppHelper
                
                def update_on_main_thread():
                    timer_logger.info(f"⚡ 在主线程执行状态变更: self.counter.value = {i}")
                    self.counter.value = i
                    timer_logger.info("⚡ 主线程状态变更语句执行完毕")
                
                # 使用AppHelper在主线程执行
                AppHelper.callAfter(update_on_main_thread)
                
                # 等待一点时间确保主线程更新完成
                time.sleep(0.1)
                
                # 记录更新后状态
                new_value = self.counter.value
                new_text = self.counter_text.value
                timer_logger.info("📍 更新后状态:")
                timer_logger.info(f"    - counter.value = {new_value} (变化: {old_value} -> {new_value})")
                timer_logger.info(f"    - counter_text.value = '{new_text}' (变化: '{old_text}' -> '{new_text}')")
                
                timer_logger.info("✅ 定时器更新完成")
                timer_logger.info("⏰" + "="*50)
                timer_logger.info("")
        
        # 使用守护线程，这样主程序退出时线程也会退出
        thread = threading.Thread(target=timer_thread, daemon=True)
        thread.start()
        timer_logger.info("⏰ 定时器线程已启动")
    
    def mount(self):
        """构建组件的视图结构"""
        timer_logger.info("🏗️ 开始构建UI结构...")
        
        # 创建标签
        timer_logger.info("🏷️ 创建定时器Label...")
        timer_logger.info(f"🏷️ 即将创建Label绑定到Computed[{id(self.counter_text)}]，当前值: '{self.counter_text.value}'")
        
        counter_label = Label(self.counter_text)
        timer_logger.info(f"🏷️ Timer Label已创建:")
        timer_logger.info(f"    - 绑定到Computed[{id(self.counter_text)}]")
        timer_logger.info(f"    - Label对象ID: {id(counter_label)}")
        timer_logger.info(f"    - Label类型: {type(counter_label)}")
        
        # 检查Label是否有关联的Effects（通过objc关联对象）
        import objc
        effects = objc.getAssociatedObject(counter_label, b"macui_effects") or []
        timer_logger.info(f"    - Label上的关联Effect数量: {len(effects)}")
        for i, effect in enumerate(effects):
            timer_logger.info(f"    - Effect {i+1}: {type(effect).__name__}[{id(effect)}], 活跃: {getattr(effect, '_active', 'Unknown')}")
        
        # 创建说明标签
        info_label = Label("定时器测试: 每3秒更新一次计数")
        
        # 构建布局
        layout = VStack(spacing=30, padding=50, children=[
            Label("🕐 定时器标签更新测试", frame=(0, 0, 350, 30)),
            info_label,
            
            VStack(spacing=15, children=[
                counter_label,
                Label(f"Signal ID: {id(self.counter)}", frame=(0, 0, 250, 20)),
                Label(f"Computed ID: {id(self.counter_text)}", frame=(0, 0, 250, 20))
            ]),
            
            Label("查看控制台日志了解详细更新过程", frame=(0, 0, 300, 20))
        ])
        
        timer_logger.info("✅ UI结构构建完成")
        return layout

def main():
    """主函数"""
    timer_logger.info("🚀 定时器测试应用启动")
    
    try:
        # 创建应用
        timer_logger.info("📱 创建MacUIApp...")
        app = MacUIApp("Timer Label Test")
        
        # 创建窗口
        timer_logger.info("🪟 创建窗口...")
        window = app.create_window(
            title="macUI 定时器标签测试",
            size=(500, 400),
            resizable=True,
            content=TimerLabelTestApp()
        )
        
        # 显示窗口
        timer_logger.info("👀 显示窗口...")
        window.show()
        
        timer_logger.info("🎬 应用已就绪！")
        timer_logger.info("📝 应用将每3秒自动更新标签 - 观察标签文本变化")
        timer_logger.info("📂 监控控制台日志了解详细更新过程")
        
        # 运行应用事件循环
        app.run()
        
    except Exception as e:
        timer_logger.error(f"❌ 应用运行错误: {e}")
        import traceback
        timer_logger.error(f"❌ 详细错误信息:\n{traceback.format_exc()}")
        raise
    finally:
        timer_logger.info("🏁 定时器测试会话结束")

if __name__ == "__main__":
    main()