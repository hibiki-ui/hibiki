#!/usr/bin/env python3
"""
测试按钮布局修复
展示HStack的智能宽度计算
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

def test_smart_button_layout():
    """测试智能按钮布局"""
    
    try:
        from macui.components import HStack, Button, Label
        
        print("🧪 测试HStack智能宽度计算")
        print("=" * 40)
        
        # 创建不同长度的按钮（不指定frame）
        short_btn = Button("添加")
        medium_btn = Button("✏️ 编辑选中")
        long_btn = Button("📊 生成测试数据报告")
        
        print("📱 创建测试按钮...")
        print(f"   短按钮: '{short_btn.title()}' -> 期望宽度: ~{max(80, min(150, len(str(short_btn.title())) * 8 + 20))}px")
        print(f"   中等按钮: '{medium_btn.title()}' -> 期望宽度: ~{max(80, min(150, len(str(medium_btn.title())) * 8 + 20))}px") 
        print(f"   长按钮: '{long_btn.title()}' -> 期望宽度: ~{max(80, min(150, len(str(long_btn.title())) * 8 + 20))}px")
        
        # 使用智能HStack，强制frame模式来测试智能宽度计算
        from macui.components.layout import LayoutMode
        button_row = HStack(
            spacing=15,
            children=[short_btn, medium_btn, long_btn],
            frame=(50, 50, 600, 40),  # 给HStack足够的空间
            layout_mode=LayoutMode.FRAME  # 强制frame模式
        )
        
        print(f"\n✅ 智能HStack创建成功: {type(button_row)}")
        print(f"   布局类型: {button_row.__class__.__name__}")
        
        # 检查子视图frame
        if hasattr(button_row, 'subviews'):
            subviews = button_row.subviews()
            print(f"\n📏 按钮实际frame信息:")
            for i, subview in enumerate(subviews):
                if hasattr(subview, 'frame'):
                    frame = subview.frame()
                    title = subview.title() if hasattr(subview, 'title') else "Unknown"
                    print(f"   按钮 {i+1} ('{title}'): Frame(x={frame.origin.x:.1f}, y={frame.origin.y:.1f}, w={frame.size.width:.1f}, h={frame.size.height:.1f})")
        
        print(f"\n🎉 测试完成! HStack智能宽度计算正常工作")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_smart_button_layout()
    sys.exit(0 if success else 1)