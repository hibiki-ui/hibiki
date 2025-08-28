#!/usr/bin/env python3
"""
Hibiki UI v4.0 分层API接口
高层API（简化90%场景）+ 低层API（开放全部能力）
"""

from typing import Optional, Union, Callable, Tuple, TYPE_CHECKING
from AppKit import NSView

# 导入核心系统
import sys
import os
sys.path.append(os.path.dirname(__file__))
from .styles import ComponentStyle, StylePresets, px, percent, vw, vh, auto
from .managers import Position, ZLayer, OverflowBehavior

if TYPE_CHECKING:
    from .component import UIComponent

from .logging import get_logger
logger = get_logger('core.api')


# ================================
# 1. HighLevelLayoutAPI - 高层API
# ================================

class HighLevelLayoutAPI:
    """高层API - 简化接口，覆盖85-90%常见场景
    
    设计原则：
    - 语义化命名，易于理解
    - 链式调用支持
    - 预设场景方法
    - 隐藏复杂的底层细节
    """
    
    def __init__(self, component: 'UIComponent'):
        """初始化高层API
        
        Args:
            component: 关联的UIComponent实例
        """
        self.component = component
    
    def done(self) -> 'UIComponent':
        """完成链式调用，返回组件本身
        
        用于在链式API调用结束后获取组件实例。
        
        Returns:
            UIComponent: 组件实例
        """
        return self.component
        
    # ================================
    # 基础定位方法
    # ================================
    
    def static(self) -> 'HighLevelLayoutAPI':
        """静态定位（默认文档流）"""
        self.component.style.position = Position.STATIC
        logger.info("📍 设置静态定位")
        return self
        
    def relative(self, left: Optional[int] = None, top: Optional[int] = None, 
                right: Optional[int] = None, bottom: Optional[int] = None) -> 'HighLevelLayoutAPI':
        """相对定位 - 相对于原始位置偏移"""
        self.component.style.position = Position.RELATIVE
        if left is not None:
            self.component.style.left = left
        if top is not None:
            self.component.style.top = top
        if right is not None:
            self.component.style.right = right
        if bottom is not None:
            self.component.style.bottom = bottom
        logger.info(f"📍 设置相对定位: left={left}, top={top}")
        return self
        
    def absolute(self, left: Optional[int] = None, top: Optional[int] = None,
                right: Optional[int] = None, bottom: Optional[int] = None) -> 'HighLevelLayoutAPI':
        """绝对定位 - 相对于最近的定位父元素"""
        self.component.style.position = Position.ABSOLUTE
        if left is not None:
            self.component.style.left = left
        if top is not None:
            self.component.style.top = top
        if right is not None:
            self.component.style.right = right
        if bottom is not None:
            self.component.style.bottom = bottom
        logger.info(f"📍 设置绝对定位: left={left}, top={top}")
        return self
        
    def fixed(self, left: Optional[int] = None, top: Optional[int] = None,
             right: Optional[int] = None, bottom: Optional[int] = None) -> 'HighLevelLayoutAPI':
        """固定定位 - 相对于视口固定"""
        self.component.style.position = Position.FIXED
        if left is not None:
            self.component.style.left = left
        if top is not None:
            self.component.style.top = top
        if right is not None:
            self.component.style.right = right
        if bottom is not None:
            self.component.style.bottom = bottom
        logger.info(f"📍 设置固定定位: left={left}, top={top}")
        return self
    
    # ================================
    # 常见定位场景
    # ================================
    
    def center(self, z_index: Optional[Union[int, ZLayer]] = None) -> 'HighLevelLayoutAPI':
        """居中定位
        
        将组件定位在其父容器的中心。
        使用绝对定位 + transform实现精确居中。
        
        Args:
            z_index: 可选的z层级
            
        Returns:
            UIComponent: 链式调用支持
        """
        self.component.style.position = Position.ABSOLUTE
        self.component.style.left = "50%"
        self.component.style.top = "50%"
        self.component.style.translation = (-0.5, -0.5)  # 使用transform居中
        
        if z_index is not None:
            self.component.style.z_index = z_index
            
        logger.info(f"📍 设置居中定位: z_index={z_index}")
        return self
        
    def top_left(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'HighLevelLayoutAPI':
        """左上角定位
        
        Args:
            margin: 距离边缘的间距
            z_index: 可选的z层级
        """
        self.component.style.position = Position.ABSOLUTE
        self.component.style.left = px(margin)
        self.component.style.top = px(margin)
        
        if z_index is not None:
            self.component.style.z_index = z_index
            
        logger.info(f"📍 设置左上角定位: margin={margin}, z_index={z_index}")
        return self
        
    def top_right(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'HighLevelLayoutAPI':
        """右上角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.right = px(margin)
        self.component.style.top = px(margin)
        
        if z_index is not None:
            self.component.style.z_index = z_index
            
        logger.info(f"📍 设置右上角定位: margin={margin}, z_index={z_index}")
        return self
        
    def bottom_left(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'HighLevelLayoutAPI':
        """左下角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.left = px(margin)
        self.component.style.bottom = px(margin)
        
        if z_index is not None:
            self.component.style.z_index = z_index
            
        logger.info(f"📍 设置左下角定位: margin={margin}, z_index={z_index}")
        return self
        
    def bottom_right(self, margin: int = 0, z_index: Optional[Union[int, ZLayer]] = None) -> 'HighLevelLayoutAPI':
        """右下角定位"""
        self.component.style.position = Position.ABSOLUTE
        self.component.style.right = px(margin)
        self.component.style.bottom = px(margin)
        
        if z_index is not None:
            self.component.style.z_index = z_index
            
        logger.info(f"📍 设置右下角定位: margin={margin}, z_index={z_index}")
        return self
        
    def fullscreen(self, z_index: Union[int, ZLayer] = ZLayer.OVERLAY) -> 'HighLevelLayoutAPI':
        """全屏覆盖
        
        将组件设置为全屏覆盖，通常用于遮罩层。
        
        Args:
            z_index: z层级，默认为OVERLAY层
        """
        self.component.style.position = Position.FIXED
        self.component.style.top = px(0)
        self.component.style.right = px(0)
        self.component.style.bottom = px(0)
        self.component.style.left = px(0)
        self.component.style.z_index = z_index
        
        logger.info(f"📍 设置全屏覆盖: z_index={z_index}")
        return self
    
    # ================================
    # 预设场景方法
    # ================================
    
    def modal(self, width: int = 400, height: int = 300) -> 'HighLevelLayoutAPI':
        """模态对话框预设
        
        创建居中的模态对话框样式。
        
        Args:
            width: 对话框宽度
            height: 对话框高度
        """
        self.center(z_index=ZLayer.MODAL)
        self.component.size(width, height)
        
        logger.info(f"🎭 设置模态对话框: {width}x{height}")
        return self
        
    def tooltip(self, offset_x: int = 0, offset_y: int = -30) -> 'HighLevelLayoutAPI':
        """工具提示预设
        
        创建相对定位的工具提示样式。
        
        Args:
            offset_x: 水平偏移
            offset_y: 垂直偏移（负值向上）
        """
        self.component.style.position = Position.RELATIVE
        self.component.style.left = px(offset_x)
        self.component.style.top = px(offset_y)
        self.component.style.z_index = ZLayer.FLOATING
        
        logger.info(f"💬 设置工具提示: offset=({offset_x}, {offset_y})")
        return self
        
    def dropdown(self, offset_y: int = 5) -> 'HighLevelLayoutAPI':
        """下拉菜单预设
        
        创建相对触发元素的下拉菜单样式。
        
        Args:
            offset_y: 垂直偏移（正值向下）
        """
        self.component.style.position = Position.ABSOLUTE
        self.component.style.top = px(offset_y)
        self.component.style.z_index = ZLayer.FLOATING
        
        logger.info(f"📋 设置下拉菜单: offset_y={offset_y}")
        return self
        
    def floating_button(self, corner: str = "bottom-right", margin: int = 20) -> 'HighLevelLayoutAPI':
        """悬浮按钮预设
        
        创建固定在视口角落的悬浮按钮。
        
        Args:
            corner: 角落位置 ("top-left", "top-right", "bottom-left", "bottom-right")
            margin: 距离边缘的间距
        """
        self.component.style.position = Position.FIXED
        self.component.style.z_index = ZLayer.FLOATING
        
        if corner == "bottom-right":
            self.component.style.bottom = px(margin)
            self.component.style.right = px(margin)
        elif corner == "top-right":
            self.component.style.top = px(margin)
            self.component.style.right = px(margin)
        elif corner == "bottom-left":
            self.component.style.bottom = px(margin)
            self.component.style.left = px(margin)
        elif corner == "top-left":
            self.component.style.top = px(margin)
            self.component.style.left = px(margin)
        else:
            logger.warning(f"⚠️ 未知的角落位置: {corner}, 使用bottom-right")
            self.component.style.bottom = px(margin)
            self.component.style.right = px(margin)
            
        logger.info(f"🔴 设置悬浮按钮: {corner}, margin={margin}")
        return self
    
    # ================================
    # 便捷样式方法
    # ================================
    
    def size(self, width: Optional[int] = None, height: Optional[int] = None) -> 'HighLevelLayoutAPI':
        """设置尺寸
        
        Args:
            width: 宽度（像素）
            height: 高度（像素）
        """
        if width is not None:
            self.component.style.width = px(width)
        if height is not None:
            self.component.style.height = px(height)
            
        logger.info(f"📏 设置尺寸: {width}x{height}")
        return self
        
    def fade(self, opacity: float) -> 'HighLevelLayoutAPI':
        """设置透明度
        
        Args:
            opacity: 透明度 (0.0 - 1.0)
        """
        self.component.style.opacity = max(0.0, min(1.0, opacity))
        
        logger.info(f"🌫️ 设置透明度: {opacity}")
        return self
    
    def hide(self) -> 'HighLevelLayoutAPI':
        """隐藏组件"""
        self.component.style.visible = False
        
        logger.info("👻 隐藏组件")
        return self
    
    def show(self) -> 'HighLevelLayoutAPI':
        """显示组件"""
        self.component.style.visible = True
        
        logger.info("👁️ 显示组件")
        return self
    
    # ================================
    # 变换效果
    # ================================
    
    def scale(self, x: float = 1.0, y: Optional[float] = None) -> 'HighLevelLayoutAPI':
        """设置缩放
        
        Args:
            x: 水平缩放因子
            y: 垂直缩放因子，默认等于x
        """
        if y is None:
            y = x
        self.component.style.scale = (x, y)
        
        logger.info(f"🔍 设置缩放: ({x}, {y})")
        return self
    
    def rotate(self, degrees: float) -> 'HighLevelLayoutAPI':
        """设置旋转
        
        Args:
            degrees: 旋转角度
        """
        self.component.style.rotation = degrees
        
        logger.info(f"🔄 设置旋转: {degrees}°")
        return self

# ================================
# 2. LowLevelLayoutAPI - 低层API
# ================================

class LowLevelLayoutAPI:
    """低层API - 直接暴露底层能力，给高级用户使用
    
    设计原则：
    - 直接访问所有底层功能
    - 最小化封装，最大化控制
    - 提供专业级配置能力
    - 允许直接操作AppKit
    """
    
    def __init__(self, component: 'UIComponent'):
        """初始化低层API
        
        Args:
            component: 关联的UIComponent实例
        """
        self.component = component
    
    # ================================
    # 直接样式控制
    # ================================
    
    def set_position(self, position: Position, **coords) -> 'HighLevelLayoutAPI':
        """直接设置定位类型和坐标
        
        Args:
            position: 定位类型
            **coords: 坐标参数 (top, right, bottom, left)
        """
        self.component.style.position = position
        
        for key, value in coords.items():
            if hasattr(self.component.style, key):
                parsed_value = self._parse_length_value(value)
                setattr(self.component.style, key, parsed_value)
                
        logger.info(f"🔧 直接设置定位: {position}, coords={coords}")
        return self
    
    def set_flex_properties(self, 
                           direction: str = None, 
                           justify: str = None,
                           align: str = None, 
                           grow: float = None, 
                           shrink: float = None,
                           basis: Union[int, str] = None) -> 'HighLevelLayoutAPI':
        """直接设置Flexbox属性
        
        Args:
            direction: flex-direction
            justify: justify-content
            align: align-items  
            grow: flex-grow
            shrink: flex-shrink
            basis: flex-basis
        """
        from styles import FlexDirection, JustifyContent, AlignItems
        
        if direction:
            # 支持字符串和枚举
            if isinstance(direction, str):
                direction_map = {
                    'row': FlexDirection.ROW,
                    'column': FlexDirection.COLUMN,
                    'row-reverse': FlexDirection.ROW_REVERSE,
                    'column-reverse': FlexDirection.COLUMN_REVERSE
                }
                self.component.style.flex_direction = direction_map.get(direction, FlexDirection.COLUMN)
            else:
                self.component.style.flex_direction = direction
                
        if justify:
            justify_map = {
                'flex-start': JustifyContent.FLEX_START,
                'flex-end': JustifyContent.FLEX_END,
                'center': JustifyContent.CENTER,
                'space-between': JustifyContent.SPACE_BETWEEN,
                'space-around': JustifyContent.SPACE_AROUND,
                'space-evenly': JustifyContent.SPACE_EVENLY
            }
            self.component.style.justify_content = justify_map.get(justify, JustifyContent.FLEX_START)
            
        if align:
            align_map = {
                'stretch': AlignItems.STRETCH,
                'flex-start': AlignItems.FLEX_START,
                'flex-end': AlignItems.FLEX_END,
                'center': AlignItems.CENTER,
                'baseline': AlignItems.BASELINE
            }
            self.component.style.align_items = align_map.get(align, AlignItems.STRETCH)
            
        if grow is not None:
            self.component.style.flex_grow = grow
        if shrink is not None:
            self.component.style.flex_shrink = shrink
        if basis is not None:
            self.component.style.flex_basis = self._parse_length_value(basis)
            
        logger.info(f"🔧 直接设置Flexbox: direction={direction}, justify={justify}, align={align}")
        return self
    
    def set_transform(self, 
                     scale: Tuple[float, float] = None,
                     rotation: float = None,
                     translation: Tuple[float, float] = None,
                     origin: Tuple[float, float] = None) -> 'HighLevelLayoutAPI':
        """直接设置变换属性
        
        Args:
            scale: 缩放因子 (x, y)
            rotation: 旋转角度（度）
            translation: 平移距离 (x, y)
            origin: 变换中心 (x, y) 0-1范围
        """
        if scale is not None:
            self.component.style.scale = scale
        if rotation is not None:
            self.component.style.rotation = rotation
        if translation is not None:
            self.component.style.translation = translation
        if origin is not None:
            self.component.style.transform_origin = origin
            
        logger.info(f"🔧 直接设置变换: scale={scale}, rotation={rotation}°")
        return self
    
    def set_z_index(self, z_index: Union[int, ZLayer]) -> 'HighLevelLayoutAPI':
        """直接设置z-index
        
        Args:
            z_index: z层级值或预定义层级
        """
        self.component.style.z_index = z_index
        
        logger.info(f"🔧 直接设置Z-Index: {z_index}")
        return self
    
    def set_overflow(self, behavior: OverflowBehavior) -> 'HighLevelLayoutAPI':
        """直接设置溢出行为
        
        Args:
            behavior: 溢出行为类型
        """
        self.component.style.overflow = behavior
        
        logger.info(f"🔧 直接设置溢出: {behavior}")
        return self
    
    # ================================
    # 底层系统集成
    # ================================
    
    def apply_stretchable_layout(self, **stretchable_props) -> 'HighLevelLayoutAPI':
        """直接使用Stretchable布局引擎
        
        Args:
            **stretchable_props: 直接传递给Stretchable的属性
        """
        # TODO: 集成现有的Stretchable布局引擎
        logger.info(f"🔧 直接使用Stretchable: {stretchable_props}")
        return self
    
    def apply_raw_appkit(self, configurator: Callable[[NSView], None]) -> 'HighLevelLayoutAPI':
        """直接访问AppKit NSView
        
        允许高级用户直接操作底层NSView，获得完全的控制权。
        
        Args:
            configurator: 配置函数，接收NSView作为参数
        """
        if self.component._nsview:
            # 如果已挂载，立即执行
            try:
                configurator(self.component._nsview)
                logger.info("🔧 直接AppKit配置已执行")
            except Exception as e:
                logger.warning(f"⚠️ 直接AppKit配置失败: {e}")
        else:
            # 如果未挂载，延迟执行
            self.component._raw_configurators.append(configurator)
            logger.info("🔧 直接AppKit配置已延迟")
            
        return self
    
    def set_clip_mask(self, x: float, y: float, width: float, height: float) -> 'HighLevelLayoutAPI':
        """设置裁剪遮罩
        
        Args:
            x: 裁剪区域x坐标
            y: 裁剪区域y坐标
            width: 裁剪区域宽度
            height: 裁剪区域高度
        """
        self.component.style.clip_rect = (x, y, width, height)
        
        logger.info(f"🔧 设置裁剪遮罩: ({x}, {y}, {width}, {height})")
        return self
    
    # ================================
    # 工具方法
    # ================================
    
    def _parse_length_value(self, value):
        """解析长度值"""
        if isinstance(value, (int, float)):
            return px(value)
        elif isinstance(value, str):
            from styles import Length
            return Length(value)
        return value
    
    def get_computed_style(self) -> ComponentStyle:
        """获取计算后的样式（只读）"""
        return self.style.copy()
    
    def merge_style(self, style: ComponentStyle) -> 'HighLevelLayoutAPI':
        """合并外部样式
        
        Args:
            style: 要合并的样式对象
        """
        self.component.style = self.component.style.merge(style)
        
        logger.info("🔧 样式已合并")
        return self

# ================================
# 3. 扩展UIComponent类
# ================================

# 为了测试，我们需要一个简单的组件类
class MockUIComponent:
    """模拟的UIComponent类用于测试"""
    
    def __init__(self):
        from styles import ComponentStyle
        self.style = ComponentStyle()
        self._nsview = None
        self._raw_configurators = []
        
        # 创建API实例
        self.layout = HighLevelLayoutAPI(self)
        self.advanced = LowLevelLayoutAPI(self)
    
    def size(self, width=None, height=None):
        """便捷的尺寸方法"""
        if width is not None:
            self.style.width = px(width)
        if height is not None:
            self.style.height = px(height)
        return self

# ================================
# 4. 测试代码
# ================================

if __name__ == "__main__":
    logger.info("Hibiki UI v4.0 分层API测试\n")
    
    # 创建测试组件
    component = MockUIComponent()
    
    logger.info("🎨 高层API测试:")
    
    # 测试预设场景
    modal_component = MockUIComponent()
    modal_component.layout.modal(400, 300)
    logger.info(f"模态框: position={modal_component.style.position}, z_index={modal_component.style.z_index}")
    
    # 测试定位方法
    floating_component = MockUIComponent()
    floating_component.layout.floating_button("top-right", 30)
    logger.info(f"悬浮按钮: position={floating_component.style.position}")
    
    # 测试链式调用
    styled_component = MockUIComponent()
    styled_component.layout.center()
    styled_component.layout.fade(0.8)
    styled_component.layout.scale(1.2)
    logger.info(f"链式调用: opacity={styled_component.style.opacity}, scale={styled_component.style.scale}")
    
    logger.info("\n🔧 低层API测试:")
    
    # 测试直接样式控制
    advanced_component = MockUIComponent()
    advanced_component.advanced.set_position(Position.ABSOLUTE, left=100, top=200)
    logger.info(f"直接定位: position={advanced_component.style.position}, left={advanced_component.style.left}")
    
    # 测试Flexbox设置
    flex_component = MockUIComponent()
    flex_component.advanced.set_flex_properties(
        direction="row", 
        justify="center", 
        align="center",
        grow=1.0
    )
    logger.info(f"Flexbox: direction={flex_component.style.flex_direction}, grow={flex_component.style.flex_grow}")
    
    # 测试变换设置
    transform_component = MockUIComponent()
    transform_component.advanced.set_transform(
        scale=(1.5, 1.5),
        rotation=45,
        translation=(10, 20)
    )
    logger.info(f"变换: scale={transform_component.style.scale}, rotation={transform_component.style.rotation}°")
    
    # 测试原始AppKit访问
    appkit_component = MockUIComponent()
    appkit_component.advanced.apply_raw_appkit(
        lambda view: print(f"直接访问NSView: {type(view).__name__}")
    )
    
    logger.info("\n✅ 分层API测试完成！")