#!/usr/bin/env python3
"""
交互式调试计数器应用
用于追踪从按钮点击到UI更新的完整路径
"""

import sys
import os
import time
from pathlib import Path

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 确保logs目录存在
logs_dir = Path(current_dir) / "logs"
logs_dir.mkdir(exist_ok=True)

# 设置详细日志
from macui import get_logger, set_log_level
set_log_level("DEBUG")

# 创建专门的UI交互调试日志器
import logging
ui_logger = logging.getLogger("macui.ui_interactive")
ui_logger.setLevel(logging.DEBUG)
ui_logger.handlers.clear()  # 清除现有处理器

# 添加文件处理器 - 追加模式，这样每次运行都会继续写入
ui_handler = logging.FileHandler(logs_dir / "ui_interactive.log", mode='a', encoding='utf-8')
ui_handler.setFormatter(logging.Formatter(
    '%(asctime)s.%(msecs)03d | INTERACTIVE | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
ui_logger.addHandler(ui_handler)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('INTERACTIVE | %(message)s'))
ui_logger.addHandler(console_handler)

# 记录会话开始
ui_logger.info("=" * 80)
ui_logger.info(f"NEW SESSION - 交互式调试会话开始")
ui_logger.info("=" * 80)

from macui import Signal, Computed, Effect, Component
from macui.components import VStack, HStack, Label, Button
from macui.app import MacUIApp

class InteractiveDebugCounterApp(Component):
    """交互式调试计数器应用"""
    
    def __init__(self):
        ui_logger.info("🚀 InteractiveDebugCounterApp.__init__: 开始初始化")
        super().__init__()
        
        # 创建响应式状态并记录详细信息
        ui_logger.info("📊 创建Signal(count)...")
        self.count = self.create_signal(0)
        ui_logger.info(f"📊 Signal(count)已创建:")
        ui_logger.info(f"    - 初始值: {self.count.value}")
        ui_logger.info(f"    - Signal对象ID: {id(self.count)}")
        ui_logger.info(f"    - 观察者数量: {len(self.count._observers)}")
        
        # 创建计算属性
        ui_logger.info("🧮 创建Computed(count_text)...")
        self.count_text = self.create_computed(
            lambda: f"Count: {self.count.value}"
        )
        ui_logger.info(f"🧮 Computed(count_text)已创建:")
        ui_logger.info(f"    - 初始值: '{self.count_text.value}'")
        ui_logger.info(f"    - Computed对象ID: {id(self.count_text)}")
        ui_logger.info(f"    - Signal观察者数量: {len(self.count._observers)}")
        ui_logger.info(f"    - Computed观察者数量: {len(self.count_text._observers)}")
        
        # 创建监控Effect
        ui_logger.info("👁️ 创建监控Effect...")
        def state_monitor():
            ui_logger.info(f"👁️ STATE_MONITOR: count={self.count.value}, text='{self.count_text.value}'")
        
        self.monitor_effect = Effect(state_monitor)
        ui_logger.info("👁️ 监控Effect已创建并执行")
        
        # 记录依赖关系
        ui_logger.info("🔗 依赖关系分析:")
        ui_logger.info(f"    - Signal[{id(self.count)}] 观察者: {len(self.count._observers)} 个")
        ui_logger.info(f"    - Computed[{id(self.count_text)}] 观察者: {len(self.count_text._observers)} 个")
        
        ui_logger.info("✅ InteractiveDebugCounterApp初始化完成")
    
    def increment(self):
        """增加计数 - 详细交互日志"""
        ui_logger.info("")
        ui_logger.info("🟢" + "="*50)
        ui_logger.info("🟢 BUTTON CLICK EVENT: Increment")
        ui_logger.info("🟢" + "="*50)
        
        # 记录点击前状态
        old_value = self.count.value
        old_text = self.count_text.value
        ui_logger.info("📍 点击前状态:")
        ui_logger.info(f"    - count.value = {old_value}")
        ui_logger.info(f"    - count_text.value = '{old_text}'")
        ui_logger.info(f"    - Signal观察者数: {len(self.count._observers)}")
        ui_logger.info(f"    - Computed观察者数: {len(self.count_text._observers)}")
        
        # 执行状态变更
        ui_logger.info("⚡ 执行状态变更: self.count.value += 1")
        self.count.value += 1
        ui_logger.info("⚡ 状态变更语句执行完毕")
        
        # 记录变更后状态
        new_value = self.count.value
        new_text = self.count_text.value
        ui_logger.info("📍 变更后状态:")
        ui_logger.info(f"    - count.value = {new_value} (变化: {old_value} -> {new_value})")
        ui_logger.info(f"    - count_text.value = '{new_text}' (变化: '{old_text}' -> '{new_text}')")
        
        # 检查UI更新（通过检查实际的NSView）
        ui_logger.info("🔍 检查UI状态...")
        try:
            # 这里我们需要访问实际的NSView来检查其显示内容
            # 我们稍后会在UI组件中添加这个功能
            ui_logger.info("🔍 UI状态检查功能待实现")
        except Exception as e:
            ui_logger.error(f"🔍 UI状态检查出错: {e}")
        
        ui_logger.info("✅ Increment操作完成")
        ui_logger.info("🟢" + "="*50)
        ui_logger.info("")
    
    def decrement(self):
        """减少计数 - 详细交互日志"""
        ui_logger.info("")
        ui_logger.info("🔴" + "="*50)
        ui_logger.info("🔴 BUTTON CLICK EVENT: Decrement")
        ui_logger.info("🔴" + "="*50)
        
        old_value = self.count.value
        old_text = self.count_text.value
        ui_logger.info("📍 点击前状态:")
        ui_logger.info(f"    - count.value = {old_value}")
        ui_logger.info(f"    - count_text.value = '{old_text}'")
        
        ui_logger.info("⚡ 执行状态变更: self.count.value -= 1")
        self.count.value -= 1
        ui_logger.info("⚡ 状态变更语句执行完毕")
        
        new_value = self.count.value
        new_text = self.count_text.value
        ui_logger.info("📍 变更后状态:")
        ui_logger.info(f"    - count.value = {new_value} (变化: {old_value} -> {new_value})")
        ui_logger.info(f"    - count_text.value = '{new_text}' (变化: '{old_text}' -> '{new_text}')")
        
        ui_logger.info("✅ Decrement操作完成")
        ui_logger.info("🔴" + "="*50)
        ui_logger.info("")
    
    def reset(self):
        """重置计数 - 详细交互日志"""
        ui_logger.info("")
        ui_logger.info("🔄" + "="*50)
        ui_logger.info("🔄 BUTTON CLICK EVENT: Reset")
        ui_logger.info("🔄" + "="*50)
        
        old_value = self.count.value
        ui_logger.info(f"📍 重置前: count = {old_value}")
        
        ui_logger.info("⚡ 执行状态变更: self.count.value = 0")
        self.count.value = 0
        ui_logger.info("⚡ 状态变更语句执行完毕")
        
        ui_logger.info(f"📍 重置后: count = {self.count.value}")
        ui_logger.info("✅ Reset操作完成")
        ui_logger.info("🔄" + "="*50)
        ui_logger.info("")
    
    def mount(self):
        """构建组件的视图结构"""
        ui_logger.info("🏗️ 开始构建UI结构...")
        
        # 创建增强的Label，能够报告UI更新
        ui_logger.info("🏷️ 创建增强Label...")
        
        # 这里我们创建一个普通的Label，但记录其创建
        ui_logger.info(f"🏷️ 即将创建Label绑定到Computed[{id(self.count_text)}]，当前值: '{self.count_text.value}'")
        count_label = Label(self.count_text)
        ui_logger.info(f"🏷️ Count Label已创建:")
        ui_logger.info(f"    - 绑定到Computed[{id(self.count_text)}]")
        ui_logger.info(f"    - Label对象ID: {id(count_label)}")
        ui_logger.info(f"    - Label类型: {type(count_label)}")
        
        # 检查Label是否有_macui_effects属性（Effect是否已存储）
        if hasattr(count_label, '_macui_effects'):
            ui_logger.info(f"    - Label上的Effect数量: {len(count_label._macui_effects)}")
            for i, effect in enumerate(count_label._macui_effects):
                ui_logger.info(f"    - Effect {i+1}: {type(effect).__name__}[{id(effect)}], 活跃: {getattr(effect, '_active', 'Unknown')}")
        else:
            ui_logger.info(f"    - Label上没有_macui_effects属性")
        
        # 创建按钮
        ui_logger.info("🔘 创建按钮...")
        increment_btn = Button("+ Increment", on_click=self.increment)
        decrement_btn = Button("- Decrement", on_click=self.decrement)  
        reset_btn = Button("🔄 Reset", on_click=self.reset)
        
        ui_logger.info(f"🔘 按钮已创建: Increment[{id(increment_btn)}], Decrement[{id(decrement_btn)}], Reset[{id(reset_btn)}]")
        
        # 构建布局
        layout = VStack(spacing=20, padding=40, children=[
            Label("🐛 Interactive Debug Counter", frame=(0, 0, 300, 30)),
            Label("Check logs/ui_interactive.log for detailed logs"),
            
            VStack(spacing=10, children=[
                count_label,
                Label(f"Signal ID: {id(self.count)}")
            ]),
            
            HStack(spacing=15, children=[
                increment_btn,
                decrement_btn,
                reset_btn,
            ])
        ])
        
        ui_logger.info("✅ UI结构构建完成")
        return layout

def main():
    """主函数"""
    ui_logger.info("🚀 交互式调试应用启动")
    ui_logger.info(f"📁 日志文件位置: {logs_dir / 'ui_interactive.log'}")
    
    try:
        # 创建应用
        ui_logger.info("📱 创建MacUIApp...")
        app = MacUIApp("Interactive Debug Counter")
        
        # 创建窗口
        ui_logger.info("🪟 创建窗口...")
        window = app.create_window(
            title="macUI Interactive Debug Counter",
            size=(450, 350),
            resizable=True,
            content=InteractiveDebugCounterApp()
        )
        
        # 显示窗口
        ui_logger.info("👀 显示窗口...")
        window.show()
        
        ui_logger.info("🎬 应用已就绪！")
        ui_logger.info("📝 请点击按钮测试 - 所有交互都会被详细记录")
        ui_logger.info("📂 实时查看日志: tail -f logs/ui_interactive.log")
        
        # 运行应用事件循环
        app.run()
        
    except Exception as e:
        ui_logger.error(f"❌ 应用运行错误: {e}")
        import traceback
        ui_logger.error(f"❌ 详细错误信息:\n{traceback.format_exc()}")
        raise
    finally:
        ui_logger.info("🏁 交互式调试会话结束")
        ui_logger.info("=" * 80)

if __name__ == "__main__":
    main()