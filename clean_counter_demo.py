#!/usr/bin/env python3
"""
macUI v2 清理后的计数器演示

这个演示展示了清理后的框架：
- 直接依赖 PyObjC，无模拟代码
- 响应式状态管理
- 真实的事件处理
- 原生 macOS UI 组件
"""

import sys
import os

# 直接导入，避免相对导入问题
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.signal import Signal, Computed, Effect
import objc
from AppKit import (
    NSApplication, NSWindow, NSButton, NSTextField,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSWindowStyleMaskResizable,
    NSBackingStoreBuffered, NSApplicationActivationPolicyRegular
)
from Foundation import NSMakeRect, NSObject


class ButtonTarget(NSObject):
    """按钮目标处理类"""
    
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


def create_clean_counter_app():
    """创建清理后的计数器应用"""
    print("🧹 创建清理后的 macUI v2 计数器...")
    
    try:
        # 1. 创建响应式状态
        print("  📊 创建响应式状态...")
        count = Signal(0)
        
        # 计算属性
        count_text = Computed(lambda: f"计数: {count.value}")
        double_text = Computed(lambda: f"双倍: {count.value * 2}")
        is_even = Computed(lambda: count.value % 2 == 0)
        status_text = Computed(lambda: f"状态: {'偶数' if is_even.value else '奇数'}")
        
        print(f"    初始计数: {count.value}")
        
        # 2. 创建应用
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
        window.setTitle_("macUI v2 - 清理后的计数器")
        window.center()
        
        # 4. 创建控件
        print("  🎛️  创建控件...")
        content_view = window.contentView()
        
        # 标签控件
        count_label = NSTextField.alloc().init()
        count_label.setFrame_(NSMakeRect(50, 220, 300, 30))
        count_label.setStringValue_(count_text.value)
        count_label.setEditable_(False)
        count_label.setSelectable_(False)
        count_label.setBezeled_(False)
        count_label.setDrawsBackground_(False)
        
        double_label = NSTextField.alloc().init()
        double_label.setFrame_(NSMakeRect(50, 190, 300, 30))
        double_label.setStringValue_(double_text.value)
        double_label.setEditable_(False)
        double_label.setSelectable_(False)
        double_label.setBezeled_(False)
        double_label.setDrawsBackground_(False)
        
        status_label = NSTextField.alloc().init()
        status_label.setFrame_(NSMakeRect(50, 160, 300, 30))
        status_label.setStringValue_(status_text.value)
        status_label.setEditable_(False)
        status_label.setSelectable_(False)
        status_label.setBezeled_(False)
        status_label.setDrawsBackground_(False)
        
        # 按钮控件
        inc_button = NSButton.alloc().init()
        inc_button.setFrame_(NSMakeRect(50, 100, 80, 30))
        inc_button.setTitle_("增加 (+1)")
        
        dec_button = NSButton.alloc().init()
        dec_button.setFrame_(NSMakeRect(140, 100, 80, 30))
        dec_button.setTitle_("减少 (-1)")
        
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
        
        def increment():
            old_value = count.value
            count.value += 1
            print(f"    ➕ 计数: {old_value} -> {count.value}")
        
        def decrement():
            old_value = count.value
            count.value -= 1
            print(f"    ➖ 计数: {old_value} -> {count.value}")
        
        def reset():
            old_value = count.value
            count.value = 0
            print(f"    🔄 重置: {old_value} -> 0")
        
        # 绑定按钮事件
        inc_target = ButtonTarget.alloc().initWithHandler_(increment)
        inc_button.setTarget_(inc_target)
        inc_button.setAction_(objc.selector(inc_target.buttonClicked_, signature=b'v@:@'))
        
        dec_target = ButtonTarget.alloc().initWithHandler_(decrement)
        dec_button.setTarget_(dec_target)
        dec_button.setAction_(objc.selector(dec_target.buttonClicked_, signature=b'v@:@'))
        
        reset_target = ButtonTarget.alloc().initWithHandler_(reset)
        reset_button.setTarget_(reset_target)
        reset_button.setAction_(objc.selector(reset_target.buttonClicked_, signature=b'v@:@'))
        
        print("    ✅ 事件处理设置完成")
        
        # 6. 设置响应式更新
        print("  🔄 设置响应式更新...")
        
        def update_count_label():
            count_label.setStringValue_(count_text.value)
        
        def update_double_label():
            double_label.setStringValue_(double_text.value)
        
        def update_status_label():
            status_label.setStringValue_(status_text.value)
        
        # 创建 Effects
        count_effect = Effect(update_count_label)
        double_effect = Effect(update_double_label)
        status_effect = Effect(update_status_label)
        
        print("    ✅ 响应式更新设置完成")
        
        # 7. 测试响应式更新
        print("  🧪 测试响应式更新...")
        original_value = count.value
        count.value = 5
        print(f"    测试更新: {original_value} -> {count.value}")
        count.value = original_value  # 恢复
        
        return app, window, (count_effect, double_effect, status_effect)
        
    except Exception as e:
        print(f"  ❌ 应用创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def main():
    """主函数"""
    print("🧹 macUI v2 清理后计数器演示")
    print("=" * 40)
    print("✨ 特性：")
    print("   • 移除了所有 PyObjC 检查和 Mock 对象")
    print("   • PyObjC 现在是必需依赖")
    print("   • 更简洁、更直接的 API")
    print("   • 完整的响应式功能")
    
    # 检查环境
    try:
        import objc
        from AppKit import NSApplication
        print(f"\n✅ PyObjC 版本: {objc.__version__ if hasattr(objc, '__version__') else 'installed'}")
    except ImportError:
        print("\n❌ PyObjC 未安装! 这是 macUI v2 的必需依赖")
        print("请安装: pip install pyobjc-core pyobjc-framework-Cocoa")
        return False
    
    # 创建应用
    app, window, effects = create_clean_counter_app()
    
    if app and window:
        print(f"""
🎊 清理后的计数器应用创建成功!

📋 应用信息:
   名称: macUI v2 清理后的计数器
   窗口大小: 400x300
   功能: 响应式计数器 (增加/减少/重置)

✨ 技术特性:
   ✅ 纯净的 PyObjC 集成 (无模拟代码)
   ✅ Signal 响应式状态
   ✅ Computed 自动计算属性  
   ✅ Effect 自动 UI 更新
   ✅ 真实的事件处理
   ✅ 原生 macOS 控件
        """)
        
        try:
            choice = input("按回车键启动应用: ").strip()
            
            print("\n🚀 启动清理后的应用...")
            print("💡 使用窗口中的按钮测试响应式功能")
            print("💡 关闭窗口退出应用")
            
            # 显示窗口并运行
            window.makeKeyAndOrderFront_(None)
            
            try:
                app.run()
                print("\n👋 应用正常退出")
            except KeyboardInterrupt:
                print("\n⏹️  应用被用户中断")
            
            # 清理
            if effects:
                for effect in effects:
                    effect.cleanup()
                print("🧹 Effects 清理完成")
            
        except KeyboardInterrupt:
            print("\n⏹️  操作被中断")
            
        return True
        
    else:
        print("❌ 应用创建失败")
        return False


if __name__ == "__main__":
    print("启动清理后的 macUI v2 计数器...\n")
    
    try:
        success = main()
        print("\n" + "=" * 40)
        if success:
            print("✅ 清理后的框架测试完成!")
            print("🎉 macUI v2 现在更简洁、更强大!")
        else:
            print("❌ 测试失败，需要进一步调试")
        print("=" * 40)
        
    except Exception as e:
        print(f"\n💥 意外错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎊 感谢使用清理后的 macUI v2!")