#!/usr/bin/env python3
"""最小版本的macUI v3.0演示，逐步定位问题"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

print("💻 脚本开始执行...")

try:
    from macui.core import Component
    print("✅ 导入Component成功")
    
    from macui.components import Label, Button, VStack, LayoutStyle
    print("✅ 导入组件成功")
    
    from macui.app import create_app
    print("✅ 导入create_app成功")
    
    from AppKit import *
    from Foundation import *
    from PyObjCTools import AppHelper
    print("✅ 导入AppKit成功")

except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

class MinimalDemo(Component):
    def __init__(self):
        print("🏗️ MinimalDemo.__init__() 开始")
        super().__init__()
        print("✅ MinimalDemo.__init__() 完成")
        
    def mount(self):
        print("🔧 MinimalDemo.mount() 开始...")
        
        # 最简单的单个Label
        label = Label("Hello Minimal Demo", style=LayoutStyle(height=30))
        print(f"✅ 创建Label: {label}")
        
        # 最简单的VStack
        vstack = VStack(
            children=[label],
            style=LayoutStyle(padding=20)
        )
        print(f"✅ 创建VStack: {vstack}")
        
        # 挂载
        result = vstack.mount()
        print(f"✅ VStack.mount()返回: {result}")
        
        return result

def main():
    print("🚀 main()函数开始...")
    
    try:
        print("📱 创建应用...")
        app = create_app("最小演示")
        print("✅ create_app完成")
        
        print("🪟 创建窗口...")
        window_style = (NSWindowStyleMaskTitled | 
                       NSWindowStyleMaskClosable | 
                       NSWindowStyleMaskResizable)
        
        window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 300, 200),
            window_style,
            NSBackingStoreBuffered,
            False
        )
        print("✅ NSWindow创建完成")
        
        window.setTitle_("最小演示")
        window.makeKeyAndOrderFront_(None)
        print("✅ 窗口显示完成")
        
        print("🔧 创建MinimalDemo组件...")
        demo = MinimalDemo()
        print("✅ MinimalDemo创建完成")
        
        print("🔧 调用mount()...")
        content_view = demo.mount()
        print(f"✅ mount()完成，返回: {content_view}")
        
        print("🔧 设置窗口内容...")
        window.setContentView_(content_view)
        print("✅ 窗口内容设置完成")
        
        print("🎮 启动事件循环...")
        AppHelper.runEventLoop()
        
    except Exception as e:
        print(f"❌ main()出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎯 __main__检查通过，调用main()...")
    main()
    print("🏁 main()函数结束")