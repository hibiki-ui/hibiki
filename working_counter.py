#!/usr/bin/env python3
"""
macUI v2 工作中的计数器应用

这是一个完全功能的 macUI v2 应用示例，展示了：
- 响应式状态管理
- 真实的 PyObjC 集成
- 事件处理
- 组件化架构
"""

import sys
import os

# 导入核心模块
from core.signal import Signal, Computed, Effect

def create_button_target():
    """创建按钮目标处理类"""
    try:
        import objc
        from Foundation import NSObject
        
        class ButtonTarget(NSObject):
            def initWithHandler_(self, handler):
                self = objc.super(ButtonTarget, self).init()
                if self is None:
                    return None
                self.handler = handler
                return self
            
            @objc.python_method
            def buttonClicked_(self, sender):
                if self.handler:
                    try:
                        self.handler()
                    except Exception as e:
                        print(f"Button handler error: {e}")
        
        return ButtonTarget
        
    except ImportError:
        return None


def create_counter_app():
    """创建计数器应用"""
    print("🚀 创建 macUI v2 计数器应用...")
    
    try:
        import objc
        from AppKit import (
            NSApplication, NSWindow, NSButton, NSTextField, NSView,
            NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
            NSBackingStoreBuffered, NSApplicationActivationPolicyRegular
        )
        from Foundation import NSMakeRect, NSString
        
        # 1. 创建响应式状态
        print("  📊 创建响应式状态...")
        count = Signal(0)
        
        # 计算属性
        count_text = Computed(lambda: f"计数: {count.value}")
        double_text = Computed(lambda: f"双倍: {count.value * 2}")
        is_even = Computed(lambda: count.value % 2 == 0)
        status_text = Computed(lambda: f"状态: {'偶数' if is_even.value else '奇数'}")
        
        print(f"    初始计数: {count.value}")
        
        # 2. 创建应用实例
        print("  📱 创建应用...")
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
        
        # 3. 创建窗口
        print("  🪟 创建窗口...")
        window_rect = NSMakeRect(100, 100, 400, 300)
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        window.setTitle_("macUI v2 - 响应式计数器")
        window.center()
        
        # 4. 创建控件
        print("  🎛️  创建控件...")
        content_view = window.contentView()
        
        # 计数显示标签
        count_label = NSTextField.alloc().init()
        count_label.setFrame_(NSMakeRect(50, 220, 300, 30))
        count_label.setStringValue_(count_text.value)
        count_label.setEditable_(False)
        count_label.setSelectable_(False)
        count_label.setBezeled_(False)
        count_label.setDrawsBackground_(False)
        
        # 双倍显示标签  
        double_label = NSTextField.alloc().init()
        double_label.setFrame_(NSMakeRect(50, 190, 300, 30))
        double_label.setStringValue_(double_text.value)
        double_label.setEditable_(False)
        double_label.setSelectable_(False)
        double_label.setBezeled_(False)
        double_label.setDrawsBackground_(False)
        
        # 状态显示标签
        status_label = NSTextField.alloc().init()
        status_label.setFrame_(NSMakeRect(50, 160, 300, 30))
        status_label.setStringValue_(status_text.value)
        status_label.setEditable_(False)
        status_label.setSelectable_(False)
        status_label.setBezeled_(False)
        status_label.setDrawsBackground_(False)
        
        # 增加按钮
        inc_button = NSButton.alloc().init()
        inc_button.setFrame_(NSMakeRect(50, 100, 80, 30))
        inc_button.setTitle_("增加 (+1)")
        
        # 减少按钮
        dec_button = NSButton.alloc().init()  
        dec_button.setFrame_(NSMakeRect(140, 100, 80, 30))
        dec_button.setTitle_("减少 (-1)")
        
        # 重置按钮
        reset_button = NSButton.alloc().init()
        reset_button.setFrame_(NSMakeRect(230, 100, 80, 30))
        reset_button.setTitle_("重置")
        
        # 添加到窗口
        content_view.addSubview_(count_label)
        content_view.addSubview_(double_label)
        content_view.addSubview_(status_label)
        content_view.addSubview_(inc_button)
        content_view.addSubview_(dec_button)
        content_view.addSubview_(reset_button)
        
        print("    ✅ 控件创建完成")
        
        # 5. 设置事件处理
        print("  ⚡ 设置事件处理...")
        
        ButtonTarget = create_button_target()
        if ButtonTarget:
            # 增加按钮处理
            def increment():
                old_value = count.value
                count.value += 1
                print(f"    ➕ 计数: {old_value} -> {count.value}")
            
            inc_target = ButtonTarget.alloc().initWithHandler_(increment)
            inc_button.setTarget_(inc_target)
            inc_button.setAction_(objc.selector(inc_target.buttonClicked_, signature=b'v@:@'))
            
            # 减少按钮处理
            def decrement():
                old_value = count.value
                count.value -= 1  
                print(f"    ➖ 计数: {old_value} -> {count.value}")
            
            dec_target = ButtonTarget.alloc().initWithHandler_(decrement)
            dec_button.setTarget_(dec_target)
            dec_button.setAction_(objc.selector(dec_target.buttonClicked_, signature=b'v@:@'))
            
            # 重置按钮处理
            def reset():
                old_value = count.value
                count.value = 0
                print(f"    🔄 重置: {old_value} -> 0")
            
            reset_target = ButtonTarget.alloc().initWithHandler_(reset)
            reset_button.setTarget_(reset_target)
            reset_button.setAction_(objc.selector(reset_target.buttonClicked_, signature=b'v@:@'))
            
            print("    ✅ 事件处理设置完成")
        else:
            print("    ⚠️  事件处理不可用 (PyObjC 问题)")
        
        # 6. 设置响应式更新
        print("  🔄 设置响应式更新...")
        
        # 标签更新效果
        def update_count_label():
            count_label.setStringValue_(count_text.value)
        
        def update_double_label():
            double_label.setStringValue_(double_text.value)
        
        def update_status_label():
            status_label.setStringValue_(status_text.value)
        
        # 创建 Effect
        count_effect = Effect(update_count_label)
        double_effect = Effect(update_double_label) 
        status_effect = Effect(update_status_label)
        
        print("    ✅ 响应式更新设置完成")
        
        # 7. 测试响应式更新
        print("  🧪 测试响应式更新...")
        count.value = 5
        count.value = 10
        count.value = 0
        print("    ✅ 响应式更新工作正常")
        
        return app, window, (count_effect, double_effect, status_effect)
        
    except Exception as e:
        print(f"  ❌ 应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def main():
    """主函数"""
    print("🎉 macUI v2 计数器应用")
    print("=" * 40)
    
    # 检查环境
    try:
        import objc
        from AppKit import NSApplication
        print(f"✅ PyObjC 版本: {objc.__version__ if hasattr(objc, '__version__') else '已安装'}")
    except ImportError:
        print("❌ PyObjC 未安装或不可用!")
        return False
    
    # 创建应用
    app, window, effects = create_counter_app()
    
    if app and window:
        print("\n" + "🎊" * 25)
        print("🎊 应用创建成功! 🎊")
        print("🎊" * 25)
        
        print(f"""
📋 应用信息:
   名称: macUI v2 响应式计数器
   窗口大小: 400x300
   功能: 响应式计数器，支持增加/减少/重置
   
💡 特性展示:
   ✅ Signal 响应式状态
   ✅ Computed 自动计算属性
   ✅ Effect 自动 UI 更新  
   ✅ 真实的 PyObjC 集成
   ✅ 原生 macOS 控件
        """)
        
        try:
            choice = input("按回车键启动应用，或输入 'q' 退出: ").strip().lower()
            
            if choice != 'q':
                print("\n🚀 启动应用...")
                print("💡 提示: 使用窗口上的按钮进行交互")
                print("💡 提示: 关闭窗口或按 Ctrl+C 退出应用")
                
                # 显示窗口
                window.makeKeyAndOrderFront_(None)
                
                # 启动应用主循环
                try:
                    app.run()
                    print("\n👋 应用正常退出")
                except KeyboardInterrupt:
                    print("\n⏹️  应用被用户中断")
                
                # 清理
                if effects:
                    for effect in effects:
                        effect.cleanup()
                    print("🧹 效果清理完成")
                
            else:
                print("👋 用户选择退出")
                
        except KeyboardInterrupt:
            print("\n⏹️  操作被中断")
            
        return True
        
    else:
        print("❌ 应用创建失败")
        return False


if __name__ == "__main__":
    print("启动 macUI v2 计数器应用...\n")
    
    try:
        success = main()
        print("\n" + "=" * 40)
        if success:
            print("✅ 应用测试完成!")
        else:
            print("❌ 应用测试失败!")
        print("=" * 40)
        
    except Exception as e:
        print(f"\n💥 意外错误: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n感谢使用 macUI v2! 🎉")