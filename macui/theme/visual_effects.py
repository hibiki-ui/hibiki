"""macUI v2 视觉效果系统

封装NSVisualEffectView和Core Animation，提供毛玻璃、阴影、渐变等高级视觉效果。
"""

from typing import Optional, Union, List, Tuple
from AppKit import (
    NSView, NSVisualEffectView, 
    NSVisualEffectMaterialPopover, NSVisualEffectMaterialSidebar,
    NSVisualEffectMaterialMenu, NSVisualEffectMaterialHeaderView,
    NSVisualEffectMaterialWindowBackground,
    NSVisualEffectBlendingModeBehindWindow, NSVisualEffectBlendingModeWithinWindow,
    NSVisualEffectStateActive, NSVisualEffectStateInactive, NSVisualEffectStateFollowsWindowActiveState,
    NSColor
)
from Foundation import NSMakeRect
from Quartz import (
    CALayer, CAGradientLayer, CAShapeLayer,
    kCAFilterLinear, kCAFilterTrilinear
)

from ..core.component import Component
from ..core.signal import Signal
from .styles import Style


class VisualEffectMaterials:
    """视觉效果材质常量"""
    POPOVER = NSVisualEffectMaterialPopover
    SIDEBAR = NSVisualEffectMaterialSidebar  
    MENU = NSVisualEffectMaterialMenu
    HEADER = NSVisualEffectMaterialHeaderView
    WINDOW_BACKGROUND = NSVisualEffectMaterialWindowBackground


class VisualEffectBlending:
    """视觉效果混合模式常量"""
    BEHIND_WINDOW = NSVisualEffectBlendingModeBehindWindow
    WITHIN_WINDOW = NSVisualEffectBlendingModeWithinWindow


class VisualEffectState:
    """视觉效果状态常量"""
    ACTIVE = NSVisualEffectStateActive
    INACTIVE = NSVisualEffectStateInactive
    FOLLOWS_WINDOW = NSVisualEffectStateFollowsWindowActiveState


class VisualEffect:
    """视觉效果工具类"""
    
    @staticmethod
    def create_vibrancy_view(
        material: int = VisualEffectMaterials.POPOVER,
        blending_mode: int = VisualEffectBlending.BEHIND_WINDOW,
        state: int = VisualEffectState.FOLLOWS_WINDOW,
        frame: Optional[tuple] = None
    ) -> NSVisualEffectView:
        """创建毛玻璃视图
        
        Args:
            material: 材质类型
            blending_mode: 混合模式
            state: 效果状态
            frame: 视图框架 (x, y, width, height)
        
        Returns:
            NSVisualEffectView实例
        """
        effect_view = NSVisualEffectView.alloc().init()
        
        if frame:
            effect_view.setFrame_(NSMakeRect(*frame))
        
        # 设置材质
        effect_view.setMaterial_(material)
        
        # 设置混合模式
        effect_view.setBlendingMode_(blending_mode)
        
        # 设置状态
        effect_view.setState_(state)
        
        print(f"✨ VisualEffect创建毛玻璃视图: 材质={material}, 混合模式={blending_mode}")
        return effect_view
    
    @staticmethod
    def create_glass_container(
        frame: tuple,
        material: str = 'popover',
        corner_radius: float = 8.0,
        border_width: float = 0.0,
        border_color: Optional[NSColor] = None
    ) -> NSVisualEffectView:
        """创建毛玻璃容器
        
        Args:
            frame: 容器框架 (x, y, width, height)
            material: 材质名称 ('popover', 'sidebar', 'menu', etc.)
            corner_radius: 圆角半径
            border_width: 边框宽度
            border_color: 边框颜色
        
        Returns:
            配置好的NSVisualEffectView
        """
        # 材质映射
        material_map = {
            'popover': VisualEffectMaterials.POPOVER,
            'sidebar': VisualEffectMaterials.SIDEBAR,
            'menu': VisualEffectMaterials.MENU,
            'header': VisualEffectMaterials.HEADER,
            'window_background': VisualEffectMaterials.WINDOW_BACKGROUND
        }
        
        material_constant = material_map.get(material, VisualEffectMaterials.POPOVER)
        
        effect_view = VisualEffect.create_vibrancy_view(
            material=material_constant,
            frame=frame
        )
        
        # 设置圆角
        if corner_radius > 0:
            effect_view.setWantsLayer_(True)
            layer = effect_view.layer()
            layer.setCornerRadius_(corner_radius)
            layer.setMasksToBounds_(True)
        
        # 设置边框
        if border_width > 0 and border_color:
            layer = effect_view.layer()
            layer.setBorderWidth_(border_width)
            layer.setBorderColor_(border_color.CGColor())
        
        return effect_view


class LayerEffects:
    """Core Animation图层效果"""
    
    @staticmethod
    def apply_shadow(
        view: NSView,
        offset: Tuple[float, float] = (0, 2),
        blur: float = 4.0,
        opacity: float = 0.1,
        color: Optional[NSColor] = None
    ):
        """应用阴影效果
        
        Args:
            view: 目标视图
            offset: 阴影偏移 (x, y)
            blur: 阴影模糊半径
            opacity: 阴影透明度
            color: 阴影颜色
        """
        if not view.wantsLayer():
            view.setWantsLayer_(True)
        
        layer = view.layer()
        
        # 设置阴影颜色
        shadow_color = color or NSColor.blackColor()
        layer.setShadowColor_(shadow_color.CGColor())
        
        # 设置阴影偏移
        layer.setShadowOffset_((offset[0], offset[1]))
        
        # 设置阴影半径
        layer.setShadowRadius_(blur)
        
        # 设置阴影透明度
        layer.setShadowOpacity_(opacity)
        
        print(f"🌟 LayerEffects应用阴影: 偏移{offset}, 模糊{blur}, 透明度{opacity}")
    
    @staticmethod
    def apply_corner_radius(view: NSView, radius: float):
        """应用圆角效果"""
        if not view.wantsLayer():
            view.setWantsLayer_(True)
        
        layer = view.layer()
        layer.setCornerRadius_(radius)
        layer.setMasksToBounds_(True)
        
        print(f"🌟 LayerEffects应用圆角: 半径{radius}")
    
    @staticmethod
    def apply_border(
        view: NSView, 
        width: float, 
        color: NSColor
    ):
        """应用边框效果"""
        if not view.wantsLayer():
            view.setWantsLayer_(True)
        
        layer = view.layer()
        layer.setBorderWidth_(width)
        layer.setBorderColor_(color.CGColor())
        
        print(f"🌟 LayerEffects应用边框: 宽度{width}")
    
    @staticmethod
    def apply_gradient(
        view: NSView,
        colors: List[NSColor],
        start_point: Tuple[float, float] = (0, 0),
        end_point: Tuple[float, float] = (1, 1)
    ):
        """应用渐变背景
        
        Args:
            view: 目标视图
            colors: 渐变颜色列表
            start_point: 渐变起点 (0-1)
            end_point: 渐变终点 (0-1)
        """
        if not view.wantsLayer():
            view.setWantsLayer_(True)
        
        # 创建渐变图层
        gradient_layer = CAGradientLayer.layer()
        gradient_layer.setFrame_(view.bounds())
        
        # 设置渐变颜色
        cg_colors = [color.CGColor() for color in colors]
        gradient_layer.setColors_(cg_colors)
        
        # 设置渐变方向
        gradient_layer.setStartPoint_(start_point)
        gradient_layer.setEndPoint_(end_point)
        
        # 添加到视图图层
        view.layer().insertSublayer_atIndex_(gradient_layer, 0)
        
        print(f"🌟 LayerEffects应用渐变: {len(colors)}色渐变")
    
    @staticmethod
    def apply_transform(
        view: NSView,
        scale: Optional[float] = None,
        rotation: Optional[float] = None,
        translation: Optional[Tuple[float, float]] = None,
        animated: bool = False,
        duration: float = 0.3
    ):
        """应用变换效果
        
        Args:
            view: 目标视图
            scale: 缩放比例
            rotation: 旋转角度（弧度）
            translation: 平移距离 (x, y)
            animated: 是否动画
            duration: 动画持续时间
        """
        if not view.wantsLayer():
            view.setWantsLayer_(True)
        
        layer = view.layer()
        
        # 构建变换矩阵
        import math
        from Quartz import CATransform3D, CATransform3DIdentity, CATransform3DScale, CATransform3DRotate, CATransform3DTranslate
        
        transform = CATransform3DIdentity
        
        if scale is not None:
            transform = CATransform3DScale(transform, scale, scale, 1.0)
        
        if rotation is not None:
            transform = CATransform3DRotate(transform, rotation, 0, 0, 1.0)
        
        if translation is not None:
            transform = CATransform3DTranslate(transform, translation[0], translation[1], 0)
        
        if animated:
            # TODO: 添加Core Animation动画
            pass
        
        layer.setTransform_(transform)
        print(f"🌟 LayerEffects应用变换: scale={scale}, rotation={rotation}, translation={translation}")


class GlassBox(Component):
    """毛玻璃容器组件"""
    
    def __init__(
        self,
        children: List[Union[Component, NSView]] = None,
        material: str = 'popover',
        corner_radius: float = 8.0,
        border_width: float = 0.0,
        border_color: Optional[NSColor] = None,
        frame: Optional[tuple] = None,
        style: Optional[Style] = None
    ):
        super().__init__()
        
        self.children = children or []
        self.material = material
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.border_color = border_color
        self.frame = frame or (0, 0, 200, 150)
        self.style = style
    
    def mount(self) -> NSVisualEffectView:
        """挂载毛玻璃容器"""
        # 创建毛玻璃视图
        glass_view = VisualEffect.create_glass_container(
            frame=self.frame,
            material=self.material,
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            border_color=self.border_color
        )
        
        # 添加子视图
        for child in self.children:
            child_view = child.get_view() if isinstance(child, Component) else child
            if child_view:
                glass_view.addSubview_(child_view)
        
        # 应用额外样式
        if self.style:
            StyleApplicator.apply(glass_view, self.style)
        
        print(f"✨ GlassBox挂载完成: {len(self.children)}个子视图")
        return glass_view


class StyleApplicator:
    """样式应用器 - 将样式应用到NSView"""
    
    @staticmethod
    def apply(view: NSView, style: Union[Style, dict, Signal]):
        """应用样式到视图
        
        Args:
            view: 目标视图
            style: 样式对象、字典或Signal
        """
        if isinstance(style, Signal):
            # 响应式样式
            def apply_reactive_style():
                current_style = style.value
                StyleApplicator._apply_properties(view, current_style)
            
            # 创建响应式效果
            from ..core.signal import Effect
            Effect(apply_reactive_style)
        else:
            # 静态样式
            properties = style.to_dict() if hasattr(style, 'to_dict') else style
            StyleApplicator._apply_properties(view, properties)
    
    @staticmethod
    def _apply_properties(view: NSView, properties: dict):
        """应用样式属性"""
        # 背景色
        if 'background_color' in properties:
            color = properties['background_color']
            if not view.wantsLayer():
                view.setWantsLayer_(True)
            view.layer().setBackgroundColor_(color.CGColor() if hasattr(color, 'CGColor') else color)
        
        # 圆角
        if 'corner_radius' in properties:
            LayerEffects.apply_corner_radius(view, properties['corner_radius'])
        
        # 阴影
        if any(key.startswith('shadow_') for key in properties):
            offset = properties.get('shadow_offset', (0, 2))
            blur = properties.get('shadow_blur', 4.0)
            opacity = properties.get('shadow_opacity', 0.1)
            color = properties.get('shadow_color', NSColor.blackColor())
            LayerEffects.apply_shadow(view, offset, blur, opacity, color)
        
        # 边框
        if 'border_width' in properties and 'border_color' in properties:
            LayerEffects.apply_border(
                view,
                properties['border_width'],
                properties['border_color']
            )
        
        # 变换
        if any(key in properties for key in ['scale', 'rotation', 'translation']):
            LayerEffects.apply_transform(
                view,
                scale=properties.get('scale'),
                rotation=properties.get('rotation'),
                translation=properties.get('translation')
            )
        
        # 透明度
        if 'opacity' in properties:
            view.setAlphaValue_(properties['opacity'])
        
        print(f"🎨 StyleApplicator应用样式: {len(properties)}个属性")


# 便捷函数
def glass_box(
    children: List[Union[Component, NSView]] = None,
    material: str = 'popover',
    corner_radius: float = 8.0,
    **kwargs
) -> GlassBox:
    """创建毛玻璃容器的便捷函数"""
    return GlassBox(
        children=children,
        material=material,
        corner_radius=corner_radius,
        **kwargs
    )


def apply_glass_effect(
    view: NSView,
    material: str = 'popover',
    corner_radius: float = 8.0
) -> NSVisualEffectView:
    """为现有视图应用毛玻璃效果"""
    frame = view.frame()
    glass_view = VisualEffect.create_glass_container(
        frame=(frame.origin.x, frame.origin.y, frame.size.width, frame.size.height),
        material=material,
        corner_radius=corner_radius
    )
    
    # 将原视图作为子视图添加到毛玻璃视图
    glass_view.addSubview_(view)
    return glass_view