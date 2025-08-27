#!/usr/bin/env python3
"""动画系统快速测试"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

# 测试导入
print("🧪 测试动画系统导入...")

try:
    from macui.animation import Animation, animate, ShinyText, TypeWriter, FadeIn, SlideIn, Scale, Shake
    print("✅ 核心动画模块导入成功")
    
    from macui.animation import TimingFunction, Easing
    print("✅ 时间函数模块导入成功")
    
    from macui.animation import Transition, TransitionType
    print("✅ 过渡动画模块导入成功")
    
    # 测试基础功能
    animation = Animation(duration=1.0)
    print(f"✅ Animation对象创建成功: {animation}")
    
    shiny = ShinyText(duration=2.0)
    print(f"✅ ShinyText效果创建成功: {shiny}")
    
    typewriter = TypeWriter("测试文本", duration=1.0)
    print(f"✅ TypeWriter效果创建成功: {typewriter}")
    
    fade = FadeIn(duration=0.5)
    print(f"✅ FadeIn效果创建成功: {fade}")
    
    slide = SlideIn(duration=0.8, direction="left")
    print(f"✅ SlideIn效果创建成功: {slide}")
    
    scale = Scale(duration=0.6)
    print(f"✅ Scale效果创建成功: {scale}")
    
    shake = Shake(duration=0.4)
    print(f"✅ Shake效果创建成功: {shake}")
    
    # 测试时间函数
    print(f"✅ 线性时间函数: {TimingFunction.LINEAR}")
    print(f"✅ 缓动时间函数: {TimingFunction.EASE_OUT}")
    
    # 测试过渡类型
    transition = Transition(TransitionType.FADE, duration=0.5)
    print(f"✅ Transition创建成功: {transition}")
    
    print()
    print("🎉 macUI动画系统测试通过！")
    print("📦 模块结构:")
    print("   • macui.animation.core - 基础动画类")
    print("   • macui.animation.effects - 预设动画效果")
    print("   • macui.animation.timing - 时间函数和缓动")
    print("   • macui.animation.transitions - 过渡动画")
    print()
    print("🚀 可以正常使用动画系统了!")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()