"""
Hibiki UI v4 自定义视图组件

提供完整的自定义视图解决方案，包括：
- 自定义绘制
- 键盘事件处理
- 鼠标事件处理
- 响应式状态管理
- 与Hibiki UI v4框架的完整集成
"""

from typing import Optional, Callable, Any, Tuple
from AppKit import *
from Foundation import *
from core.component import UIComponent
from core.styles import ComponentStyle, px
from core.reactive import Signal
import objc


class CustomNSView(NSView):
    """自定义NSView类 - 处理绘制和事件"""
    
    def initWithFrame_(self, frame):
        """初始化视图"""
        self = objc.super(CustomNSView, self).initWithFrame_(frame)
        if self is None:
            return None
        
        # 回调函数
        self._draw_callback = None
        self._mouse_down_callback = None
        self._mouse_up_callback = None
        self._mouse_moved_callback = None
        self._mouse_dragged_callback = None
        self._key_down_callback = None
        self._key_up_callback = None
        
        # 状态跟踪
        self._mouse_position = NSMakePoint(0, 0)
        self._is_mouse_inside = False
        self._is_dragging = False
        
        return self
    
    def setDrawCallback_(self, callback):
        """设置绘制回调"""
        self._draw_callback = callback
    
    def setMouseDownCallback_(self, callback):
        """设置鼠标按下回调"""
        self._mouse_down_callback = callback
    
    def setMouseUpCallback_(self, callback):
        """设置鼠标抬起回调"""
        self._mouse_up_callback = callback
    
    def setMouseMovedCallback_(self, callback):
        """设置鼠标移动回调"""
        self._mouse_moved_callback = callback
    
    def setMouseDraggedCallback_(self, callback):
        """设置鼠标拖拽回调"""
        self._mouse_dragged_callback = callback
    
    def setKeyDownCallback_(self, callback):
        """设置键盘按下回调"""
        self._key_down_callback = callback
    
    def setKeyUpCallback_(self, callback):
        """设置键盘抬起回调"""
        self._key_up_callback = callback
    
    # === 绘制方法 ===
    def drawRect_(self, rect):
        """自定义绘制"""
        if self._draw_callback:
            # 获取当前绘制上下文
            context = NSGraphicsContext.currentContext().CGContext()
            
            # 调用用户定义的绘制函数
            try:
                self._draw_callback(context, rect, self.bounds())
            except Exception as e:
                print(f"❌ 绘制回调出错: {e}")
                # 绘制错误提示
                NSColor.redColor().setFill()
                NSRectFill(rect)
    
    def isFlipped(self):
        """使用翻转坐标系(左上角为原点)"""
        return True
    
    # === 鼠标事件 ===
    def mouseDown_(self, event):
        """鼠标按下事件"""
        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        self._mouse_position = point
        self._is_dragging = True
        
        if self._mouse_down_callback:
            try:
                self._mouse_down_callback(point.x, point.y, event)
            except Exception as e:
                print(f"❌ 鼠标按下回调出错: {e}")
    
    def mouseUp_(self, event):
        """鼠标抬起事件"""
        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        self._mouse_position = point
        self._is_dragging = False
        
        if self._mouse_up_callback:
            try:
                self._mouse_up_callback(point.x, point.y, event)
            except Exception as e:
                print(f"❌ 鼠标抬起回调出错: {e}")
    
    def mouseMoved_(self, event):
        """鼠标移动事件"""
        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        self._mouse_position = point
        
        if self._mouse_moved_callback:
            try:
                self._mouse_moved_callback(point.x, point.y, event)
            except Exception as e:
                print(f"❌ 鼠标移动回调出错: {e}")
    
    def mouseDragged_(self, event):
        """鼠标拖拽事件"""
        point = self.convertPoint_fromView_(event.locationInWindow(), None)
        self._mouse_position = point
        
        if self._mouse_dragged_callback:
            try:
                self._mouse_dragged_callback(point.x, point.y, event)
            except Exception as e:
                print(f"❌ 鼠标拖拽回调出错: {e}")
    
    def mouseEntered_(self, event):
        """鼠标进入"""
        self._is_mouse_inside = True
        self.setNeedsDisplay_(True)
    
    def mouseExited_(self, event):
        """鼠标退出"""
        self._is_mouse_inside = False
        self.setNeedsDisplay_(True)
    
    # === 键盘事件 ===
    def acceptsFirstResponder(self):
        """接受第一响应者状态(接收键盘事件)"""
        return True
    
    def keyDown_(self, event):
        """键盘按下事件"""
        if self._key_down_callback:
            try:
                key_code = event.keyCode()
                characters = event.characters()
                self._key_down_callback(key_code, characters, event)
            except Exception as e:
                print(f"❌ 键盘按下回调出错: {e}")
    
    def keyUp_(self, event):
        """键盘抬起事件"""
        if self._key_up_callback:
            try:
                key_code = event.keyCode()
                characters = event.characters()
                self._key_up_callback(key_code, characters, event)
            except Exception as e:
                print(f"❌ 键盘抬起回调出错: {e}")
    
    # === 属性访问 ===
    def mousePosition(self):
        """获取当前鼠标位置"""
        return self._mouse_position
    
    def isMouseInside(self):
        """鼠标是否在视图内"""
        return self._is_mouse_inside
    
    def isDragging(self):
        """是否正在拖拽"""
        return self._is_dragging


class CustomView(UIComponent):
    """Hibiki UI v4自定义视图组件"""
    
    def __init__(
        self,
        style: Optional[ComponentStyle] = None,
        on_draw: Optional[Callable] = None,
        on_mouse_down: Optional[Callable] = None,
        on_mouse_up: Optional[Callable] = None,
        on_mouse_moved: Optional[Callable] = None,
        on_mouse_dragged: Optional[Callable] = None,
        on_key_down: Optional[Callable] = None,
        on_key_up: Optional[Callable] = None
    ):
        """
        初始化自定义视图
        
        Args:
            style: 组件样式
            on_draw: 绘制回调 (context, rect, bounds) -> None
            on_mouse_down: 鼠标按下回调 (x, y, event) -> None
            on_mouse_up: 鼠标抬起回调 (x, y, event) -> None
            on_mouse_moved: 鼠标移动回调 (x, y, event) -> None
            on_mouse_dragged: 鼠标拖拽回调 (x, y, event) -> None
            on_key_down: 键盘按下回调 (key_code, characters, event) -> None
            on_key_up: 键盘抬起回调 (key_code, characters, event) -> None
        """
        super().__init__(
            style=style or ComponentStyle(width=px(200), height=px(200))
        )
        
        # 回调函数
        self.on_draw = on_draw
        self.on_mouse_down = on_mouse_down
        self.on_mouse_up = on_mouse_up
        self.on_mouse_moved = on_mouse_moved
        self.on_mouse_dragged = on_mouse_dragged
        self.on_key_down = on_key_down
        self.on_key_up = on_key_up
        
        # 响应式状态
        self.mouse_position = Signal((0.0, 0.0))
        self.is_mouse_inside = Signal(False)
        self.is_dragging = Signal(False)
    
    def _create_nsview(self):
        """创建自定义NSView"""
        print("🎨 创建CustomView组件")
        
        # 创建自定义NSView
        custom_view = CustomNSView.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 200))
        
        # 设置回调函数
        if self.on_draw:
            custom_view.setDrawCallback_(self.on_draw)
        
        if self.on_mouse_down:
            custom_view.setMouseDownCallback_(self._wrap_mouse_callback(self.on_mouse_down))
        
        if self.on_mouse_up:
            custom_view.setMouseUpCallback_(self._wrap_mouse_callback(self.on_mouse_up))
        
        if self.on_mouse_moved:
            custom_view.setMouseMovedCallback_(self._wrap_mouse_callback(self.on_mouse_moved))
        
        if self.on_mouse_dragged:
            custom_view.setMouseDraggedCallback_(self._wrap_mouse_callback(self.on_mouse_dragged))
        
        if self.on_key_down:
            custom_view.setKeyDownCallback_(self.on_key_down)
        
        if self.on_key_up:
            custom_view.setKeyUpCallback_(self.on_key_up)
        
        print("✅ CustomView组件创建成功")
        return custom_view
    
    def setup_auto_redraw(self, *signals):
        """设置信号自动重绘 - 当指定信号变化时自动重绘视图"""
        from core.reactive import Signal, Effect
        
        for signal in signals:
            if isinstance(signal, Signal):
                # 创建Effect来监听信号变化
                def create_redraw_effect(sig):
                    def redraw_on_change():
                        # 读取信号值以建立依赖关系
                        _ = sig.value
                        # 触发重绘
                        if self._nsview:
                            print(f"🔄 信号变化触发重绘")
                            self._nsview.setNeedsDisplay_(True)
                    
                    return Effect(redraw_on_change)
                
                effect = create_redraw_effect(signal)
                print(f"📡 已设置信号 {signal} 的自动重绘")
    
    def _wrap_mouse_callback(self, callback):
        """包装鼠标回调，同时更新响应式状态"""
        def wrapped_callback(x, y, event):
            # 更新响应式状态
            self.mouse_position.value = (x, y)
            self.is_mouse_inside.value = self._nsview.isMouseInside() if self._nsview else False
            self.is_dragging.value = self._nsview.isDragging() if self._nsview else False
            
            # 调用用户回调
            if callback:
                callback(x, y, event)
            
            # 触发重绘 - 鼠标交互后通常需要重绘
            if self._nsview:
                self._nsview.setNeedsDisplay_(True)
        
        return wrapped_callback
    
    def redraw(self):
        """触发重绘"""
        if self._nsview:
            self._nsview.setNeedsDisplay_(True)
    
    def make_first_responder(self):
        """成为第一响应者(接收键盘事件)"""
        if self._nsview:
            window = self._nsview.window()
            if window:
                window.makeFirstResponder_(self._nsview)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """获取视图边界 (x, y, width, height)"""
        if self._nsview:
            bounds = self._nsview.bounds()
            return (bounds.origin.x, bounds.origin.y, bounds.size.width, bounds.size.height)
        return (0, 0, 0, 0)


# === 绘制工具函数 ===
class DrawingUtils:
    """绘制工具类"""
    
    @staticmethod
    def fill_rect(context, x, y, width, height, color):
        """填充矩形"""
        from Quartz import CGContextSetRGBFillColor, CGContextFillRect
        r, g, b, a = color
        CGContextSetRGBFillColor(context, r, g, b, a)
        CGContextFillRect(context, ((x, y), (width, height)))
    
    @staticmethod
    def stroke_rect(context, x, y, width, height, color, line_width=1.0):
        """描边矩形"""
        from Quartz import CGContextSetRGBStrokeColor, CGContextSetLineWidth, CGContextStrokeRect
        r, g, b, a = color
        CGContextSetRGBStrokeColor(context, r, g, b, a)
        CGContextSetLineWidth(context, line_width)
        CGContextStrokeRect(context, ((x, y), (width, height)))
    
    @staticmethod
    def fill_circle(context, center_x, center_y, radius, color):
        """填充圆形"""
        from Quartz import CGContextSetRGBFillColor, CGContextFillEllipseInRect
        r, g, b, a = color
        CGContextSetRGBFillColor(context, r, g, b, a)
        rect = ((center_x - radius, center_y - radius), (radius * 2, radius * 2))
        CGContextFillEllipseInRect(context, rect)
    
    @staticmethod
    def draw_line(context, from_x, from_y, to_x, to_y, color, line_width=1.0):
        """绘制线条"""
        from Quartz import CGContextSetRGBStrokeColor, CGContextSetLineWidth, CGContextMoveToPoint, CGContextAddLineToPoint, CGContextStrokePath
        r, g, b, a = color
        CGContextSetRGBStrokeColor(context, r, g, b, a)
        CGContextSetLineWidth(context, line_width)
        CGContextMoveToPoint(context, from_x, from_y)
        CGContextAddLineToPoint(context, to_x, to_y)
        CGContextStrokePath(context)
    
    @staticmethod
    def draw_text(context, text, x, y, font_size=12, color=(0, 0, 0, 1)):
        """绘制文本"""
        # 使用NSString的绘制方法
        ns_text = NSString.stringWithString_(text)
        font = NSFont.systemFontOfSize_(font_size)
        text_color = NSColor.colorWithRed_green_blue_alpha_(*color)
        
        attributes = {
            NSFontAttributeName: font,
            NSForegroundColorAttributeName: text_color
        }
        
        ns_text.drawAtPoint_withAttributes_(NSMakePoint(x, y), attributes)