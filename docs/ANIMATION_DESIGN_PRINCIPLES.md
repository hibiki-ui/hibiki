# Hibiki UI v3.0 动画系统设计原则

## 概述

本文档记录Hibiki UI动画系统的核心设计原则、架构决策和最佳实践。这些准则确保动画系统的高性能、可维护性和一致性。

## 🎯 核心设计原则

### 1. Pure Core Animation First

**原则**: 所有动画必须基于Core Animation API实现，严禁使用任何形式的自定义时间控制。

**禁止使用**:
```python
# ❌ 绝对禁止
import threading
import time

def bad_animation():
    threading.Thread(target=lambda: time.sleep(1.0)).start()
    # 任何形式的阻塞等待都不被允许
```

**正确方式**:
```python
# ✅ 标准实现
group = CAAnimationGroup.animation()
animation = CABasicAnimation.animationWithKeyPath_("shadowOpacity")
animation.setDuration_(1.0)
group.setAnimations_([animation])
layer.addAnimation_forKey_(group, "effect")
```

**理由**: 
- Core Animation在GPU上执行，性能最优
- 系统级别的时间同步，精度更高
- 自动处理帧率适配和性能优化
- 避免Python GIL带来的性能问题

### 2. GPU优先策略

**原则**: 优先选择GPU加速友好的动画属性。

**推荐属性** (GPU加速):
- `shadowOpacity` - 阴影透明度
- `shadowRadius` - 阴影半径
- `transform.scale` - 缩放变换
- `transform.rotation` - 旋转变换
- `opacity` - 视图透明度
- `position` - 位置变换

**避免属性** (CPU密集):
- `frame` - 频繁布局计算
- `bounds` - 触发子视图重新布局
- 自定义绘制属性

### 3. 声明式API设计

**原则**: 提供简单、直观的API，隐藏Core Animation的复杂性。

```python
# 目标API设计
animate(view, duration=0.5, opacity=0.8, scale=1.2)

# 而不是暴露Core Animation细节
animation = CABasicAnimation.animationWithKeyPath_("opacity")
animation.setFromValue_(view.alphaValue())
animation.setToValue_(0.8)
# ... 复杂的设置代码
```

### 4. Signal响应式集成

**原则**: 动画系统必须与Hibiki UI的Signal系统无缝集成。

```python
# 响应式动画绑定
animate_to(view, position_signal, 
          position=lambda pos: pos,
          opacity=lambda pos: 0.8 if pos[0] > 100 else 0.5)
```

## 🏗️ 架构设计模式

### 标准动画实现模板

```python
def create_animation_effect(self, target_view, **params):
    """标准动画效果实现模板"""
    
    # 1. 确保Layer支持
    target_view.setWantsLayer_(True)
    layer = target_view.layer()
    
    # 2. 创建动画组
    group = CAAnimationGroup.animation()
    group.setDuration_(self.duration)
    group.setRemovedOnCompletion_(False)
    group.setFillMode_("forwards")
    
    # 3. 创建具体动画
    animations = []
    
    opacity_anim = CABasicAnimation.animationWithKeyPath_("opacity")
    opacity_anim.setFromValue_(0.0)
    opacity_anim.setToValue_(1.0)
    animations.append(opacity_anim)
    
    # 4. 组装和应用
    group.setAnimations_(animations)
    group.setTimingFunction_(
        CAMediaTimingFunction.functionWithName_("easeInEaseOut")
    )
    
    # 5. 处理完成回调
    def completion():
        # 清理工作
        pass
    
    CATransaction.begin()
    CATransaction.setCompletionBlock_(completion)
    layer.addAnimation_forKey_(group, "effect_key")
    CATransaction.commit()
    
    return Animation(duration=self.duration)
```

### 预设效果类设计模式

```python
class AnimationEffect:
    """动画效果基类"""
    
    def __init__(self, duration: float = 1.0, **kwargs):
        self.duration = duration
        # 其他参数
    
    def apply_to(self, view: NSView) -> Animation:
        """应用到指定视图 - 子类必须实现"""
        raise NotImplementedError
    
    def _create_ca_animation(self, keypath: str, from_val, to_val) -> CABasicAnimation:
        """创建基础动画的辅助方法"""
        animation = CABasicAnimation.animationWithKeyPath_(keypath)
        animation.setFromValue_(from_val)
        animation.setToValue_(to_val)
        animation.setDuration_(self.duration)
        return animation
```

## 📊 性能优化指南

### 1. 动画组合优化

```python
# ✅ 推荐: 使用CAAnimationGroup
group = CAAnimationGroup.animation()
group.setAnimations_([anim1, anim2, anim3])
layer.addAnimation_forKey_(group, "combined")

# ❌ 避免: 分别添加多个动画
layer.addAnimation_forKey_(anim1, "anim1")
layer.addAnimation_forKey_(anim2, "anim2")
layer.addAnimation_forKey_(anim3, "anim3")
```

### 2. 内存管理

```python
# ✅ 正确的生命周期管理
group.setRemovedOnCompletion_(False)
group.setFillMode_("forwards")

# 完成后清理
def cleanup():
    layer.removeAnimationForKey_("effect_key")
    
CATransaction.setCompletionBlock_(cleanup)
```

### 3. 避免频繁桥接调用

```python
# ❌ 频繁的Python-ObjC调用
for i in range(100):
    layer.setValue_forKeyPath_(i/100.0, "opacity")

# ✅ 使用关键帧动画
keyframe_anim = CAKeyframeAnimation.animationWithKeyPath_("opacity")
keyframe_anim.setValues_([i/100.0 for i in range(100)])
```

## 🧪 测试策略

### 单元测试
- 验证动画参数设置正确性
- 检查CAAnimation对象创建
- 测试完成回调执行

### 集成测试  
- 验证动画视觉效果
- 测试与Signal系统集成
- 性能基准测试

### 示例代码
```python
def test_shiny_text_animation():
    """测试闪光文字动画"""
    text_view = NSTextField.alloc().init()
    shiny = ShinyText(duration=1.0)
    
    # 应用动画
    animation = shiny.apply_to(text_view)
    
    # 验证动画设置
    assert animation.duration == 1.0
    assert text_view.wantsLayer() == True
    
    # 验证Core Animation设置
    layer = text_view.layer()
    assert layer.animationKeys() is not None
```

## 🚀 扩展指南

### 添加新动画效果

1. **继承基类**: 从适当的基类继承
2. **实现apply_to**: 核心动画逻辑
3. **遵循命名**: 清晰的类名和参数名
4. **添加文档**: 完整的docstring和示例
5. **编写测试**: 单元测试和视觉验证

### API一致性检查清单

- [ ] 是否使用纯Core Animation API？
- [ ] 是否避免了threading/time模块？
- [ ] 是否优先使用GPU加速属性？
- [ ] 是否提供了completion处理？
- [ ] 是否与Signal系统兼容？
- [ ] 是否遵循命名约定？
- [ ] 是否包含使用示例？

## 📝 变更记录

### v3.0.0 (2025-08-27)
- ✅ 建立Pure Core Animation原则
- ✅ 实现GPU优先策略
- ✅ 创建声明式API设计
- ✅ 集成Signal响应式系统
- ✅ 完成核心动画效果库

### 后续计划
- 扩展预设动画效果库
- 优化性能基准测试
- 增强调试和诊断工具
- 完善文档和示例

---

**重要提醒**: 本文档是Hibiki UI动画系统的核心设计准则，任何偏离这些原则的实现都应该经过充分讨论和验证。