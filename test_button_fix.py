#!/usr/bin/env python3
"""
测试Button点击事件修复
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# 导入macUI v4.0
from macui_v4.core.managers import ManagerFactory
from macui_v4.components.basic import Button

def main():
    print("🔘 Button事件绑定测试")
    print("=" * 30)
    
    # 初始化系统
    ManagerFactory.initialize_all()
    
    # 创建带点击事件的按钮
    def test_callback():
        print("🎉 按钮点击成功！")
    
    button = Button("测试按钮", on_click=test_callback, width=120, height=40)
    
    # 挂载按钮
    print("\n🚀 挂载按钮...")
    button_view = button.mount()
    
    print(f"✅ 按钮挂载完成: {type(button_view).__name__}")
    print(f"🎯 按钮标题: {button_view.title()}")
    print(f"🔗 事件目标: {button_view.target()}")
    print(f"📞 事件动作: {button_view.action()}")
    
    # 模拟点击事件
    print("\n🖱️ 模拟点击测试...")
    try:
        # 直接调用delegate的回调方法进行测试
        if button._target_delegate and hasattr(button._target_delegate, 'callback'):
            print("📞 直接调用回调...")
            button._target_delegate.callback()
        
        # 尝试模拟发送action
        if button_view.target() and button_view.action():
            print("📤 发送action消息...")
            button_view.target().performSelector_withObject_(button_view.action(), button_view)
            
    except Exception as e:
        print(f"⚠️ 点击测试失败: {e}")
    
    print("\n✅ Button测试完成！")

if __name__ == "__main__":
    main()