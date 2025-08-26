#!/usr/bin/env python3
"""
测试HStack按钮布局调试
展示NSStackView的详细布局信息
"""

import sys
import time
sys.path.insert(0, '/Users/david/david/app/macui')

def test_hstack_button_layout():
    """测试HStack按钮布局和调试输出"""
    
    print("🧪 测试HStack按钮布局（约束模式）")
    print("=" * 50)
    
    try:
        from macui.components import HStack, Button, Label
        
        # 创建不同长度的按钮（不指定frame，让它们使用默认尺寸）
        print("1️⃣ 创建测试按钮...")
        btn1 = Button("添加")
        btn2 = Button("✏️ 编辑选中") 
        btn3 = Button("🗑️ 删除选中")
        
        print("\n2️⃣ 创建HStack...")
        # 创建HStack，应该使用约束模式（NSStackView）
        button_row = HStack(
            spacing=15,
            children=[btn1, btn2, btn3]
        )
        
        print(f"\n3️⃣ HStack创建结果:")
        print(f"   类型: {type(button_row)}")
        print(f"   类名: {button_row.__class__.__name__}")
        
        # 等待一下让布局完成
        print("\n4️⃣ 等待布局完成...")
        time.sleep(0.2)
        
        # 检查最终布局
        print("\n5️⃣ 检查最终布局:")
        if hasattr(button_row, 'arrangedSubviews'):
            arranged_views = button_row.arrangedSubviews()
            print(f"   安排的子视图数量: {len(arranged_views)}")
            
            for i, subview in enumerate(arranged_views):
                frame = subview.frame()
                title = subview.title() if hasattr(subview, 'title') else "Unknown"
                print(f"   按钮 {i+1} '{title}': Frame(x={frame.origin.x:.1f}, y={frame.origin.y:.1f}, w={frame.size.width:.1f}, h={frame.size.height:.1f})")
                
                # 检查是否重叠
                if i > 0:
                    prev_frame = arranged_views[i-1].frame()
                    prev_right = prev_frame.origin.x + prev_frame.size.width
                    current_left = frame.origin.x
                    
                    if current_left < prev_right:
                        print(f"   ⚠️  重叠检测: 按钮{i}与按钮{i+1}重叠! (前一个右边界:{prev_right:.1f} >= 当前左边界:{current_left:.1f})")
                    else:
                        gap = current_left - prev_right
                        print(f"   ✅ 间距正常: 按钮{i}与按钮{i+1}间距 {gap:.1f}px")
        
        print("\n🎉 HStack布局测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hstack_button_layout()
    sys.exit(0 if success else 1)