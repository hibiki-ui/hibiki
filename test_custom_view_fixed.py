#!/usr/bin/env python3
"""测试修复后的自定义视图组件"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import Signal
from macui.components import CustomView, DrawingUtils, VStack, Label, LayoutStyle
from macui.app import create_app
from macui.core import Component

from AppKit import *
from PyObjCTools import AppHelper


class SimpleDrawTest(Component):
    """简单绘制测试"""
    
    def __init__(self):
        super().__init__()
        self.points = Signal([])
        self.status = Signal("点击画布添加点")
    
    def mount(self):
        # 状态显示
        status_label = Label(self.status.value, style=LayoutStyle(height=30))
        
        # 画布
        canvas = CustomView(
            style=LayoutStyle(width=400, height=300),
            on_draw=self._draw,
            on_mouse_down=self._add_point
        )
        
        # 设置自动重绘
        canvas.setup_auto_redraw(self.points)
        
        # 说明
        info = Label("🎯 点击添加红点，测试响应式重绘", style=LayoutStyle(height=25))
        
        container = VStack(
            children=[status_label, canvas, info],
            style=LayoutStyle(gap=10, padding=20)
        )
        
        return container.mount()
    
    def _draw(self, context, rect, bounds):
        """绘制函数"""
        print(f"🎨 绘制函数被调用，点数: {len(self.points.value)}")
        
        # 白色背景
        DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                             (1.0, 1.0, 1.0, 1.0))
        
        # 绘制边框
        DrawingUtils.stroke_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                               (0.5, 0.5, 0.5, 1.0), 1.0)
        
        # 绘制所有点
        for x, y in self.points.value:
            DrawingUtils.fill_circle(context, x, y, 8, (1.0, 0.0, 0.0, 0.8))  # 红色圆点
    
    def _add_point(self, x, y, event):
        """添加点"""
        points = self.points.value.copy()
        points.append((x, y))
        self.points.value = points
        
        self.status.value = f"已添加 {len(points)} 个点"
        print(f"✨ 添加点: ({x}, {y}), 总点数: {len(points)}")


def main():
    """主函数"""
    print("🧪 测试修复后的自定义视图组件...")
    
    # 创建应用
    app = create_app("CustomView修复测试")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 500, 400),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("CustomView修复测试")
    window.makeKeyAndOrderFront_(None)
    
    # 创建测试组件
    test = SimpleDrawTest()
    content_view = test.mount()
    window.setContentView_(content_view)
    
    print("✅ 测试应用启动成功!")
    print("🎯 点击画布应该能看到红色圆点")
    print("📈 观察日志中的重绘和信号变化")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()