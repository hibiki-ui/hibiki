#!/usr/bin/env python3
"""
测试VStack布局调试输出
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_vstack_debug():
    """测试VStack布局调试输出"""
    
    print("🧪 测试VStack布局调试输出")
    print("=" * 50)
    
    try:
        from macui.components import VStack, Button, Label
        
        # 创建简单的VStack
        print("1️⃣ 创建测试组件...")
        btn1 = Button("按钮1")
        btn2 = Button("按钮2")
        label1 = Label("标签1")
        
        print("\n2️⃣ 创建VStack...")
        # 创建VStack，应该触发调试输出
        vstack = VStack(
            spacing=10,
            padding=20,
            children=[label1, btn1, btn2],
            frame=(0, 0, 300, 200)  # 提供合理的frame
        )
        
        print(f"\n3️⃣ VStack创建结果:")
        print(f"   类型: {type(vstack)}")
        print(f"   类名: {vstack.__class__.__name__}")
        
        print("\n🎉 VStack调试测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_vstack_debug()
    sys.exit(0 if success else 1)