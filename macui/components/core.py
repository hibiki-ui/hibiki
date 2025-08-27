"""
macUI组件核心架构 - 基于新布局引擎v3.0

提供支持Stretchable布局引擎的组件基类和核心接口
实现声明式布局API和现代化组件架构
"""

from typing import Optional, Any, Union, Dict
from AppKit import NSView
from ..core.component import Component
from ..layout.node import LayoutNode
from ..layout.styles import LayoutStyle
from ..layout.engine import get_layout_engine


class LayoutAwareComponent(Component):
    """支持新布局引擎的组件基类
    
    提供CSS-like布局属性和声明式API支持
    所有新组件都应该继承此类
    """
    
    def __init__(
        self, 
        layout_style: Optional[LayoutStyle] = None,
        layout_key: Optional[str] = None,
        **layout_kwargs
    ):
        """初始化布局感知组件
        
        Args:
            layout_style: 完整的布局样式对象
            layout_key: 布局节点标识符
            **layout_kwargs: 布局样式快捷参数 (width, height, margin等)
        """
        super().__init__()
        
        # 合并样式参数
        if layout_style is None:
            layout_style = LayoutStyle(**layout_kwargs)
        elif layout_kwargs:
            # 如果同时提供了style和kwargs，kwargs会覆盖style中的对应属性
            style_dict = self._layout_style_to_dict(layout_style)
            style_dict.update(layout_kwargs)
            layout_style = LayoutStyle(**style_dict)
        
        self.layout_style = layout_style
        self.layout_key = layout_key or f"component_{id(self)}"
        self.layout_node: Optional[LayoutNode] = None
        self._layout_engine = get_layout_engine()
        
        # NSView缓存
        self._nsview: Optional[NSView] = None
    
    def create_layout_node(self) -> LayoutNode:
        """创建对应的布局节点"""
        if self.layout_node is None:
            self.layout_node = LayoutNode(
                style=self.layout_style,
                key=self.layout_key,
                user_data=self
            )
        return self.layout_node
    
    def set_layout_style(self, **kwargs) -> 'LayoutAwareComponent':
        """更新布局样式 - 支持链式调用
        
        Examples:
            button.set_layout_style(width=120, margin=8)
            label.set_layout_style(flex_grow=1, align_self=AlignItems.CENTER)
        """
        if self.layout_style:
            # 合并现有样式和新样式
            current_dict = self._layout_style_to_dict(self.layout_style)
            current_dict.update(kwargs)
            self.layout_style = LayoutStyle(**current_dict)
        else:
            self.layout_style = LayoutStyle(**kwargs)
        
        # 更新布局节点
        if self.layout_node:
            self.layout_node.style = self.layout_style
        
        return self
    
    # 布局属性的便捷方法 - 支持链式调用
    def width(self, value: Union[int, float, str]) -> 'LayoutAwareComponent':
        """设置宽度"""
        return self.set_layout_style(width=value)
    
    def height(self, value: Union[int, float, str]) -> 'LayoutAwareComponent':
        """设置高度"""
        return self.set_layout_style(height=value)
    
    def margin(
        self, 
        all: Optional[Union[int, float]] = None,
        top: Optional[Union[int, float]] = None,
        right: Optional[Union[int, float]] = None,
        bottom: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None
    ) -> 'LayoutAwareComponent':
        """设置边距"""
        if all is not None:
            return self.set_layout_style(margin=all)
        else:
            return self.set_layout_style(
                margin_top=top,
                margin_right=right,
                margin_bottom=bottom,
                margin_left=left
            )
    
    def padding(
        self,
        all: Optional[Union[int, float]] = None,
        top: Optional[Union[int, float]] = None,
        right: Optional[Union[int, float]] = None,
        bottom: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None
    ) -> 'LayoutAwareComponent':
        """设置内边距"""
        if all is not None:
            return self.set_layout_style(padding=all)
        else:
            return self.set_layout_style(
                padding_top=top,
                padding_right=right,
                padding_bottom=bottom,
                padding_left=left
            )
    
    def flex_grow(self, value: float) -> 'LayoutAwareComponent':
        """设置flex grow"""
        return self.set_layout_style(flex_grow=value)
    
    def flex_shrink(self, value: float) -> 'LayoutAwareComponent':
        """设置flex shrink"""
        return self.set_layout_style(flex_shrink=value)
    
    def gap(self, value: Union[int, float]) -> 'LayoutAwareComponent':
        """设置内容间距"""
        return self.set_layout_style(gap=value)
    
    def get_layout_node(self) -> Optional[LayoutNode]:
        """获取布局节点"""
        return self.layout_node
    
    def compute_layout(self, available_size: Optional[tuple] = None):
        """计算此组件的布局"""
        if self.layout_node:
            return self._layout_engine.compute_layout(self.layout_node, available_size)
    
    def apply_layout_to_view(self):
        """将计算的布局应用到NSView"""
        if self.layout_node and self._nsview:
            from ..layout.debug import log_layout_application
            success = False
            
            try:
                from Foundation import NSMakeRect
                x, y, w, h = self.layout_node.get_layout()
                frame = NSMakeRect(x, y, w, h)
                self._nsview.setFrame_(frame)
                success = True
                print(f"📐 布局应用成功: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
            except Exception as e:
                print(f"⚠️ 布局应用失败: {e}")
                # 如果Stretchable布局失败，使用默认布局
                if hasattr(self.layout_style, 'width') and hasattr(self.layout_style, 'height'):
                    width = self.layout_style.width or 100
                    height = self.layout_style.height or 30
                    frame = NSMakeRect(0, 0, width, height)
                    self._nsview.setFrame_(frame)
                    success = True
                    print(f"📐 使用默认布局: ({0}, {0}, {width}, {height})")
            
            # 记录布局应用调试信息
            log_layout_application(self.layout_node, self._nsview, success)
    
    def mount(self) -> NSView:
        """挂载组件 - 子类必须实现"""
        if self._nsview is None:
            self._nsview = self._create_nsview()
            # 在子类设置完成后禁用AutoLayout
            self._setup_nsview()
            # 🔴 最后统一禁用AutoLayout
            self._disable_autolayout_recursively(self._nsview)
        
        # 创建布局节点
        self.create_layout_node()
        
        # 设置基类的_view引用以保持兼容性
        self._view = self._nsview
        
        return self._nsview
    
    def _create_nsview(self) -> NSView:
        """创建NSView实例 - 子类必须实现"""
        raise NotImplementedError("子类必须实现 _create_nsview 方法")
    
    def _setup_nsview(self):
        """设置NSView属性 - 子类可选实现"""
        # 🔴 自动禁用AutoLayout - 适用于所有子类
        self._disable_autolayout_recursively(self._nsview)
    
    def _disable_autolayout_recursively(self, view):
        """递归禁用视图及其所有子视图的AutoLayout"""
        if view is None:
            return
            
        # 禁用当前视图的AutoLayout
        if hasattr(view, 'setTranslatesAutoresizingMaskIntoConstraints_'):
            view.setTranslatesAutoresizingMaskIntoConstraints_(True)
            
        # 递归处理子视图
        if hasattr(view, 'subviews'):
            try:
                subviews = view.subviews()
                if subviews:
                    for subview in subviews:
                        self._disable_autolayout_recursively(subview)
            except Exception:
                pass  # 忽略可能的错误
    
    def _layout_style_to_dict(self, style: LayoutStyle) -> Dict[str, Any]:
        """将LayoutStyle转换为字典 - 用于样式合并"""
        return {
            # Display & Position
            'display': style.display,
            'position': style.position,
            
            # Flexbox
            'flex_direction': style.flex_direction,
            'align_items': style.align_items,
            'justify_content': style.justify_content,
            'flex_grow': style.flex_grow,
            'flex_shrink': style.flex_shrink,
            
            # Size
            'width': style.width,
            'height': style.height,
            'min_width': style.min_width,
            'min_height': style.min_height,
            'max_width': style.max_width,
            'max_height': style.max_height,
            
            # Spacing
            'margin': style.margin,
            'margin_top': style.margin_top,
            'margin_right': style.margin_right,
            'margin_bottom': style.margin_bottom,
            'margin_left': style.margin_left,
            
            'padding': style.padding,
            'padding_top': style.padding_top,
            'padding_right': style.padding_right,
            'padding_bottom': style.padding_bottom,
            'padding_left': style.padding_left,
            
            # Gap
            'gap': style.gap,
            'row_gap': style.row_gap,
            'column_gap': style.column_gap,
            
            # Positioning  
            'top': style.top,
            'right': style.right,
            'bottom': style.bottom,
            'left': style.left,
        }

