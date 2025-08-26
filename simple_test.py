#!/usr/bin/env python3
"""
macUI v2 简单测试 - 避免复杂的导入问题
"""

def test_reactive_core():
    """测试响应式核心"""
    print("🧪 测试响应式核心...")
    
    from core.signal import Signal, Computed, Effect
    
    # 测试 Signal
    count = Signal(0)
    print(f"  Signal 创建: {count.value}")
    
    count.value = 5
    print(f"  Signal 更新: {count.value}")
    
    # 测试 Computed  
    double = Computed(lambda: count.value * 2)
    print(f"  Computed 值: {double.value}")
    
    count.value = 10
    print(f"  Signal 变更为 {count.value}, Computed 自动更新为: {double.value}")
    
    # 测试 Effect
    effects = []
    def track_changes():
        effects.append(count.value)
        print(f"  Effect 触发: count = {count.value}")
    
    effect = Effect(track_changes)
    count.value = 15
    count.value = 20
    
    print(f"  Effect 记录: {effects}")
    effect.cleanup()
    
    return True


def create_simple_ui():
    """创建简单的 UI 测试"""
    print("\n🖥️  创建简单 UI...")
    
    try:
        import objc
        from Foundation import NSObject
        from AppKit import NSButton, NSTextField, NSApplication, NSWindow
        from AppKit import NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSBackingStoreBuffered
        from Foundation import NSMakeRect
        
        print("  ✅ PyObjC 组件导入成功")
        
        # 创建应用
        app = NSApplication.sharedApplication()
        print("  📱 应用实例创建")
        
        # 创建窗口
        window_rect = NSMakeRect(100, 100, 400, 300)
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            window_rect,
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
        window.setTitle_("macUI v2 Test")
        print("  🪟 窗口创建成功")
        
        # 创建按钮
        button_rect = NSMakeRect(150, 150, 100, 30)
        button = NSButton.alloc().init()
        button.setFrame_(button_rect)
        button.setTitle_("Test Button")
        print("  🔘 按钮创建成功")
        
        # 创建文本框
        text_rect = NSMakeRect(150, 100, 100, 30)
        text_field = NSTextField.alloc().init()
        text_field.setFrame_(text_rect)
        text_field.setStringValue_("Hello macUI!")
        print("  📝 文本框创建成功")
        
        # 添加到窗口
        content_view = window.contentView()
        content_view.addSubview_(button)
        content_view.addSubview_(text_field)
        print("  ➕ 组件添加到窗口")
        
        return app, window, button, text_field
        
    except Exception as e:
        print(f"  ❌ UI 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None


def test_binding_integration():
    """测试绑定集成"""
    print("\n🔗 测试绑定集成...")
    
    try:
        from core.signal import Signal, Computed
        from core.binding import ReactiveBinding
        
        # 创建信号
        text_signal = Signal("初始文本")
        visible_signal = Signal(True)
        
        print("  📡 信号创建成功")
        
        # 创建简单的 Mock 对象来测试绑定
        class MockView:
            def __init__(self):
                self.properties = {}
            
            def setStringValue_(self, value):
                self.properties['text'] = value
                print(f"    Mock view 文本设为: '{value}'")
            
            def setHidden_(self, hidden):
                self.properties['hidden'] = hidden  
                print(f"    Mock view 隐藏状态: {hidden}")
        
        # 创建 mock 视图
        view = MockView()
        
        # 测试绑定
        ReactiveBinding.bind(view, 'text', text_signal)
        ReactiveBinding.bind(view, 'hidden', visible_signal)
        
        print("  🔗 绑定创建成功")
        
        # 测试响应式更新
        text_signal.value = "更新的文本"
        visible_signal.value = False
        
        print(f"  📊 最终视图状态: {view.properties}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 绑定测试失败: {e}")
        import traceback 
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 macUI v2 简化测试")
    print("=" * 30)
    
    success_count = 0
    total_tests = 3
    
    # 测试 1: 响应式核心
    try:
        if test_reactive_core():
            success_count += 1
            print("  ✅ 响应式核心测试通过")
        else:
            print("  ❌ 响应式核心测试失败")
    except Exception as e:
        print(f"  ❌ 响应式核心测试异常: {e}")
    
    # 测试 2: UI 创建
    try:
        app, window, button, text_field = create_simple_ui()
        if app and window:
            success_count += 1
            print("  ✅ UI 创建测试通过")
        else:
            print("  ❌ UI 创建测试失败")
    except Exception as e:
        print(f"  ❌ UI 创建测试异常: {e}")
        app, window, button, text_field = None, None, None, None
    
    # 测试 3: 绑定集成
    try:
        if test_binding_integration():
            success_count += 1
            print("  ✅ 绑定集成测试通过")
        else:
            print("  ❌ 绑定集成测试失败")
    except Exception as e:
        print(f"  ❌ 绑定集成测试异常: {e}")
    
    print(f"\n📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("\n🎉 所有测试通过!")
        
        # 如果 UI 创建成功，询问是否显示窗口
        if app and window:
            try:
                choice = input("\n是否显示测试窗口? (y/N): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    print("📱 显示窗口...")
                    window.makeKeyAndOrderFront_(None)
                    
                    print("💡 窗口已显示! 按回车键关闭...")
                    input()
                    
                    print("🔒 关闭窗口...")
                    window.close()
                    
            except KeyboardInterrupt:
                print("\n⏹️  操作已取消")
        
        return True
    else:
        print(f"\n⚠️  {total_tests - success_count} 个测试失败")
        return False


if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 30)
    if success:
        print("✅ 测试完成 - macUI v2 核心功能正常!")
    else:
        print("❌ 测试完成 - 需要修复一些问题")
    print("=" * 30)