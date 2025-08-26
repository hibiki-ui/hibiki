#!/usr/bin/env python3
"""
按钮事件系统底层调试
"""

import sys
import os
import objc
from Foundation import NSObject
from AppKit import NSButton, NSButtonTypeMomentaryPushIn, NSApplication, NSWindow, NSMakeRect

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=== 按钮事件系统底层调试 ===")

# 创建一个最简单的按钮目标类
class SimpleButtonTarget(NSObject):
    """简单的按钮目标"""
    
    def init(self):
        self = objc.super(SimpleButtonTarget, self).init()
        if self is None:
            return None
        print(f"✅ SimpleButtonTarget.init: Target[{id(self)}] 初始化成功")
        return self
    
    def simpleClick_(self, sender):
        """简单的点击处理"""
        print(f"🎯 SimpleButtonTarget.simpleClick_: 收到点击事件！sender={type(sender).__name__}[{id(sender)}]")
        print("🎉 按钮点击成功！这证明事件系统工作正常")

def test_simple_button():
    """测试最简单的按钮"""
    print("\n=== 测试最简单的按钮 ===")
    
    # 创建应用
    app = NSApplication.sharedApplication()
    print("✅ NSApplication已创建")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 300, 200), 15, 2, False
    )
    window.setTitle_("Simple Button Test")
    print(f"✅ NSWindow已创建: {id(window)}")
    
    # 创建按钮
    button = NSButton.alloc().initWithFrame_(NSMakeRect(50, 50, 200, 44))
    button.setTitle_("点击我测试事件")
    button.setButtonType_(NSButtonTypeMomentaryPushIn)
    print(f"✅ NSButton已创建: {id(button)}")
    
    # 创建目标
    target = SimpleButtonTarget.alloc().init()
    print(f"✅ SimpleButtonTarget已创建: {id(target)}")
    
    # 设置目标和动作
    button.setTarget_(target)
    
    # 尝试不同的selector设置方式
    print("\n=== 尝试设置selector ===")
    
    # 方法1: 直接使用字符串
    try:
        button.setAction_("simpleClick:")
        print("✅ 方法1成功: 使用字符串 'simpleClick:' 设置action")
    except Exception as e:
        print(f"❌ 方法1失败: {e}")
    
    # 验证设置
    current_target = button.target()
    current_action = button.action()
    print(f"🔍 按钮当前target: {type(current_target).__name__ if current_target else 'None'}[{id(current_target) if current_target else 'None'}]")
    print(f"🔍 按钮当前action: {current_action}")
    print(f"🔍 target是否正确: {current_target is target}")
    
    # 检查target的方法
    print(f"🔍 target有simpleClick_方法: {hasattr(target, 'simpleClick_')}")
    if hasattr(target, 'simpleClick_'):
        print(f"🔍 simpleClick_方法: {getattr(target, 'simpleClick_')}")
    
    # 添加到窗口
    window.contentView().addSubview_(button)
    print("✅ 按钮已添加到窗口")
    
    # 显示窗口
    window.makeKeyAndOrderFront_(None)
    print("✅ 窗口已显示")
    print("\n📝 请点击按钮测试事件系统...")
    print("📝 如果看到 '🎯 SimpleButtonTarget.simpleClick_' 消息，说明事件系统正常")
    print("📝 如果没有看到，说明macOS事件系统有问题")
    
    # 手动测试调用
    print("\n=== 手动测试调用 ===")
    try:
        print("🧪 手动调用target.simpleClick_(button)...")
        target.simpleClick_(button)
        print("✅ 手动调用成功")
    except Exception as e:
        print(f"❌ 手动调用失败: {e}")
    
    # 保持引用防止垃圾回收
    return app, window, button, target

def main():
    """主函数"""
    try:
        app, window, button, target = test_simple_button()
        
        print("\n=== 启动事件循环 ===")
        print("📝 点击按钮或按 Ctrl+C 退出")
        
        # 运行事件循环
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()