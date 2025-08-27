#!/usr/bin/env python3
"""
macUI自定义视图演示

展示如何创建完全自定义的视图组件，包括：
1. 自定义绘制
2. 鼠标事件处理
3. 键盘事件处理
4. 响应式状态管理
"""

import sys
sys.path.insert(0, '/Users/david/david/app/macui')

from macui import Signal
from macui.components import VStack, Label, LayoutStyle
from macui.components.custom_view import CustomView, DrawingUtils
from macui.app import create_app
from macui.core import Component

from AppKit import *
from PyObjCTools import AppHelper
import math
import random


class DrawingCanvas(Component):
    """绘图画布演示组件"""
    
    def __init__(self):
        super().__init__()
        
        # 响应式状态
        self.drawing_points = Signal([])  # 绘制的点
        self.current_color = Signal((0.0, 0.5, 1.0, 0.8))  # 当前颜色
        self.brush_size = Signal(5.0)  # 画笔大小
        self.status_text = Signal("点击并拖拽来绘制")
        
        # 内部状态
        self.is_drawing = False
        self.last_point = None
    
    def mount(self):
        # 状态显示
        status_label = Label(self.status_text.value, style=LayoutStyle(height=30))
        
        # 绘图区域
        canvas = CustomView(
            style=LayoutStyle(width=600, height=400),
            on_draw=self._on_draw,
            on_mouse_down=self._on_mouse_down,
            on_mouse_up=self._on_mouse_up,
            on_mouse_dragged=self._on_mouse_dragged,
            on_key_down=self._on_key_down
        )
        
        # 设置自动重绘 - 当绘制相关的信号变化时自动重绘
        canvas.setup_auto_redraw(self.drawing_points, self.current_color, self.brush_size)
        
        # 信息显示
        info_label = Label("🎨 绘图演示 | 拖拽绘制 | 空格键清空 | C键换色", 
                          style=LayoutStyle(height=25))
        
        # 布局
        container = VStack(
            children=[status_label, canvas, info_label],
            style=LayoutStyle(gap=10, padding=20)
        )
        
        return container.mount()
    
    def _on_draw(self, context, rect, bounds):
        """自定义绘制函数"""
        # 清空背景
        DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                             (1.0, 1.0, 1.0, 1.0))  # 白色背景
        
        # 绘制边框
        DrawingUtils.stroke_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                               (0.8, 0.8, 0.8, 1.0), 2.0)
        
        # 绘制所有点
        points = self.drawing_points.value
        color = self.current_color.value
        size = self.brush_size.value
        
        for point in points:
            x, y = point
            DrawingUtils.fill_circle(context, x, y, size, color)
        
        # 绘制网格(可选)
        self._draw_grid(context, bounds)
    
    def _draw_grid(self, context, bounds):
        """绘制辅助网格"""
        grid_size = 50
        grid_color = (0.9, 0.9, 0.9, 0.5)
        
        # 垂直线
        x = grid_size
        while x < bounds.size.width:
            DrawingUtils.draw_line(context, x, 0, x, bounds.size.height, grid_color, 0.5)
            x += grid_size
        
        # 水平线
        y = grid_size
        while y < bounds.size.height:
            DrawingUtils.draw_line(context, 0, y, bounds.size.width, y, grid_color, 0.5)
            y += grid_size
    
    def _on_mouse_down(self, x, y, event):
        """鼠标按下 - 开始绘制"""
        self.is_drawing = True
        self.last_point = (x, y)
        
        # 添加点
        points = self.drawing_points.value.copy()
        points.append((x, y))
        self.drawing_points.value = points
        
        self.status_text.value = f"绘制中... ({x:.0f}, {y:.0f})"
    
    def _on_mouse_up(self, x, y, event):
        """鼠标抬起 - 结束绘制"""
        self.is_drawing = False
        self.last_point = None
        self.status_text.value = f"绘制完成，共 {len(self.drawing_points.value)} 个点"
    
    def _on_mouse_dragged(self, x, y, event):
        """鼠标拖拽 - 连续绘制"""
        if self.is_drawing and self.last_point:
            # 在两点之间插值，创建平滑线条
            last_x, last_y = self.last_point
            
            # 计算距离
            dx = x - last_x
            dy = y - last_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 根据距离插值点
            if distance > 3:  # 避免过于密集的点
                steps = int(distance / 3)
                points = self.drawing_points.value.copy()
                
                for i in range(1, steps + 1):
                    t = i / steps
                    inter_x = last_x + dx * t
                    inter_y = last_y + dy * t
                    points.append((inter_x, inter_y))
                
                self.drawing_points.value = points
                self.last_point = (x, y)
        
        self.status_text.value = f"绘制中... ({x:.0f}, {y:.0f})"
    
    def _on_key_down(self, key_code, characters, event):
        """键盘事件处理"""
        print(f"🎹 按键: {key_code} ({characters})")
        
        if characters == ' ':  # 空格键清空
            self.drawing_points.value = []
            self.status_text.value = "画布已清空"
        
        elif characters.lower() == 'c':  # C键换色
            colors = [
                (1.0, 0.0, 0.0, 0.8),  # 红色
                (0.0, 1.0, 0.0, 0.8),  # 绿色
                (0.0, 0.5, 1.0, 0.8),  # 蓝色
                (1.0, 0.5, 0.0, 0.8),  # 橙色
                (1.0, 0.0, 1.0, 0.8),  # 紫色
            ]
            self.current_color.value = random.choice(colors)
            self.status_text.value = "颜色已切换"
        
        elif characters.lower() == 's':  # S键改变大小
            sizes = [3.0, 5.0, 8.0, 12.0, 15.0]
            current_size = self.brush_size.value
            try:
                current_index = sizes.index(current_size)
                next_index = (current_index + 1) % len(sizes)
                self.brush_size.value = sizes[next_index]
                self.status_text.value = f"画笔大小: {sizes[next_index]}"
            except ValueError:
                self.brush_size.value = sizes[0]


class InteractiveShapes(Component):
    """交互式形状演示组件"""
    
    def __init__(self):
        super().__init__()
        self.shapes = Signal([])  # 形状列表
        self.status = Signal("点击创建圆形")
    
    def mount(self):
        status_label = Label(self.status.value, style=LayoutStyle(height=30))
        
        shapes_canvas = CustomView(
            style=LayoutStyle(width=400, height=300),
            on_draw=self._draw_shapes,
            on_mouse_down=self._add_shape,
            on_key_down=self._handle_key
        )
        
        # 设置形状变化时自动重绘
        shapes_canvas.setup_auto_redraw(self.shapes)
        
        info_label = Label("🔵 点击添加圆形 | R键清空", style=LayoutStyle(height=25))
        
        container = VStack(
            children=[status_label, shapes_canvas, info_label],
            style=LayoutStyle(gap=10, padding=20)
        )
        
        return container.mount()
    
    def _draw_shapes(self, context, rect, bounds):
        """绘制所有形状"""
        # 背景
        DrawingUtils.fill_rect(context, 0, 0, bounds.size.width, bounds.size.height, 
                             (0.95, 0.95, 0.95, 1.0))
        
        # 绘制形状
        for shape in self.shapes.value:
            x, y, radius, color = shape
            DrawingUtils.fill_circle(context, x, y, radius, color)
            DrawingUtils.stroke_rect(context, x-radius, y-radius, radius*2, radius*2, 
                                   (0.5, 0.5, 0.5, 1.0), 1.0)
    
    def _add_shape(self, x, y, event):
        """添加新形状"""
        radius = random.uniform(15, 40)
        color = (random.random(), random.random(), random.random(), 0.7)
        
        shapes = self.shapes.value.copy()
        shapes.append((x, y, radius, color))
        self.shapes.value = shapes
        
        self.status.value = f"已添加圆形，共 {len(shapes)} 个"
    
    def _handle_key(self, key_code, characters, event):
        """处理键盘输入"""
        if characters.lower() == 'r':
            self.shapes.value = []
            self.status.value = "已清空所有形状"


def main():
    """主函数"""
    print("🎨 启动自定义视图演示...")
    
    # 创建应用
    app = create_app("macUI自定义视图演示")
    
    # 创建窗口
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(100, 100, 900, 800),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
        NSBackingStoreBuffered,
        False
    )
    
    window.setTitle_("macUI自定义视图演示")
    window.makeKeyAndOrderFront_(None)
    
    # 创建主界面
    # 分为两个部分：绘图画布 和 交互形状
    drawing_demo = DrawingCanvas()
    shapes_demo = InteractiveShapes()
    
    # 创建标签视图容器
    tab_view = NSTabView.alloc().init()
    tab_view.setFrame_(NSMakeRect(0, 0, 900, 800))
    
    # 绘图标签
    drawing_item = NSTabViewItem.alloc().init()
    drawing_item.setLabel_("绘图画布")
    drawing_item.setView_(drawing_demo.mount())
    tab_view.addTabViewItem_(drawing_item)
    
    # 形状标签
    shapes_item = NSTabViewItem.alloc().init()
    shapes_item.setLabel_("交互形状")
    shapes_item.setView_(shapes_demo.mount())
    tab_view.addTabViewItem_(shapes_item)
    
    window.setContentView_(tab_view)
    
    print("✅ 自定义视图演示启动成功!")
    print("🎯 功能演示:")
    print("   📝 绘图画布: 拖拽绘制、空格清空、C键换色、S键改大小")
    print("   🔵 交互形状: 点击添加圆形、R键清空")
    print("   ⌨️ 键盘事件: 需要点击视图获得焦点")
    
    # 启动事件循环
    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()