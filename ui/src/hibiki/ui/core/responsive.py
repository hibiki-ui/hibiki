#!/usr/bin/env python3
"""
Hibiki UI 响应式布局系统
======================

实现现代化的响应式设计，支持断点、媒体查询和自适应布局。

核心特性：
- 预定义和自定义断点系统
- 响应式样式规则和继承
- 自动断点匹配和样式切换
- 与现有布局引擎无缝集成

设计哲学：
类似于 CSS 媒体查询和 Tailwind CSS 的响应式设计理念，
但针对原生桌面应用进行了优化。
"""

from typing import Dict, List, Callable, Optional, Union, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import weakref

from .styles import ComponentStyle, px, percent
from .logging import get_logger

logger = get_logger("core.responsive")
logger.setLevel("DEBUG")


# ================================
# 1. 断点系统
# ================================

class BreakpointName(Enum):
    """预定义断点名称"""
    XS = "xs"      # Extra Small (0-575px)
    SM = "sm"      # Small (576-767px) 
    MD = "md"      # Medium (768-991px)
    LG = "lg"      # Large (992-1199px)
    XL = "xl"      # Extra Large (1200px+)


@dataclass
class Breakpoint:
    """断点定义"""
    name: str
    min_width: float
    max_width: Optional[float] = None
    
    def matches(self, viewport_width: float) -> bool:
        """检查视口宽度是否匹配此断点"""
        if self.max_width is None:
            return viewport_width >= self.min_width
        return self.min_width <= viewport_width <= self.max_width


class BreakpointManager:
    """断点管理器"""
    
    def __init__(self):
        # 预定义断点（基于 Bootstrap 和 Tailwind 的标准）
        self._breakpoints = {
            BreakpointName.XS.value: Breakpoint("xs", 0, 575),
            BreakpointName.SM.value: Breakpoint("sm", 576, 767),
            BreakpointName.MD.value: Breakpoint("md", 768, 991),
            BreakpointName.LG.value: Breakpoint("lg", 992, 1199),
            BreakpointName.XL.value: Breakpoint("xl", 1200),
        }
        
        # 当前匹配的断点
        self._current_breakpoints: List[str] = []
        self._current_viewport_width = 800  # 默认宽度
        
        logger.info("📱 BreakpointManager 初始化完成")
    
    def add_custom_breakpoint(self, name: str, min_width: float, max_width: Optional[float] = None):
        """添加自定义断点"""
        self._breakpoints[name] = Breakpoint(name, min_width, max_width)
        logger.info(f"📐 添加自定义断点: {name} ({min_width}-{max_width or '∞'})")
    
    def get_breakpoint(self, name: str) -> Optional[Breakpoint]:
        """获取断点定义"""
        return self._breakpoints.get(name)
    
    def update_viewport_width(self, width: float) -> bool:
        """更新视口宽度，返回是否有断点变化"""
        old_breakpoints = set(self._current_breakpoints)
        self._current_viewport_width = width
        
        # 重新计算匹配的断点
        self._current_breakpoints = []
        for name, breakpoint in self._breakpoints.items():
            if breakpoint.matches(width):
                self._current_breakpoints.append(name)
        
        new_breakpoints = set(self._current_breakpoints)
        breakpoint_changed = old_breakpoints != new_breakpoints
        
        if breakpoint_changed:
            logger.info(f"🔄 断点变化: {sorted(old_breakpoints)} → {sorted(new_breakpoints)}")
        
        return breakpoint_changed
    
    def get_current_breakpoints(self) -> List[str]:
        """获取当前匹配的断点"""
        return self._current_breakpoints.copy()
    
    def get_primary_breakpoint(self) -> str:
        """获取主要断点（最大的匹配断点）"""
        if not self._current_breakpoints:
            return BreakpointName.MD.value
        
        # 按预定义顺序返回最大的断点
        order = [bp.value for bp in BreakpointName]
        for bp_name in reversed(order):
            if bp_name in self._current_breakpoints:
                return bp_name
        
        return self._current_breakpoints[-1]


# ================================
# 2. 响应式样式系统
# ================================

@dataclass
class MediaQuery:
    """媒体查询条件"""
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    breakpoint: Optional[str] = None
    
    def matches(self, viewport_width: float, current_breakpoints: List[str]) -> bool:
        """检查是否匹配当前视口条件"""
        # 检查断点匹配
        if self.breakpoint and self.breakpoint not in current_breakpoints:
            return False
        
        # 检查宽度范围
        if self.min_width is not None and viewport_width < self.min_width:
            return False
        if self.max_width is not None and viewport_width > self.max_width:
            return False
            
        return True


@dataclass
class ResponsiveRule:
    """响应式样式规则"""
    media_query: MediaQuery
    style: ComponentStyle
    priority: int = 0  # 优先级，数值越大越优先
    
    def matches(self, viewport_width: float, current_breakpoints: List[str]) -> bool:
        """检查是否匹配"""
        return self.media_query.matches(viewport_width, current_breakpoints)


class ResponsiveStyle:
    """响应式样式容器"""
    
    def __init__(self, base_style: Optional[ComponentStyle] = None):
        self.base_style = base_style or ComponentStyle()
        self.responsive_rules: List[ResponsiveRule] = []
        
    def at_breakpoint(self, breakpoint: Union[str, BreakpointName], style: ComponentStyle) -> 'ResponsiveStyle':
        """在指定断点应用样式"""
        bp_name = breakpoint.value if isinstance(breakpoint, BreakpointName) else breakpoint
        
        rule = ResponsiveRule(
            media_query=MediaQuery(breakpoint=bp_name),
            style=style,
            priority=self._get_breakpoint_priority(bp_name)
        )
        self.responsive_rules.append(rule)
        return self
    
    def at_min_width(self, min_width: float, style: ComponentStyle) -> 'ResponsiveStyle':
        """在最小宽度时应用样式"""
        rule = ResponsiveRule(
            media_query=MediaQuery(min_width=min_width),
            style=style,
            priority=int(min_width)  # 宽度越大优先级越高
        )
        self.responsive_rules.append(rule)
        return self
    
    def at_max_width(self, max_width: float, style: ComponentStyle) -> 'ResponsiveStyle':
        """在最大宽度时应用样式"""
        rule = ResponsiveRule(
            media_query=MediaQuery(max_width=max_width),
            style=style,
            priority=10000 - int(max_width)  # 宽度越小优先级越高（倒序）
        )
        self.responsive_rules.append(rule)
        return self
    
    def at_width_range(self, min_width: float, max_width: float, style: ComponentStyle) -> 'ResponsiveStyle':
        """在宽度范围内应用样式"""
        rule = ResponsiveRule(
            media_query=MediaQuery(min_width=min_width, max_width=max_width),
            style=style,
            priority=int(min_width)
        )
        self.responsive_rules.append(rule)
        return self
    
    def resolve(self, viewport_width: float, current_breakpoints: List[str]) -> ComponentStyle:
        """解析当前视口条件下的最终样式"""
        # 从基础样式开始
        final_style = ComponentStyle(**self.base_style.__dict__)
        
        # 获取所有匹配的规则并按优先级排序
        matching_rules = [
            rule for rule in self.responsive_rules
            if rule.matches(viewport_width, current_breakpoints)
        ]
        matching_rules.sort(key=lambda r: r.priority)
        
        logger.debug(f"🔍 响应式解析: 视口={viewport_width:.0f}px, 断点={current_breakpoints}, 规则数={len(self.responsive_rules)}")
        
        # 按优先级顺序合并样式
        for i, rule in enumerate(matching_rules):
            old_width = getattr(final_style, 'width', None)
            final_style = self._merge_styles(final_style, rule.style)
            new_width = getattr(final_style, 'width', None)
            
            logger.debug(f"  规则{i}: 断点={rule.media_query.breakpoint}, 优先级={rule.priority}")
            if old_width != new_width:
                logger.debug(f"    宽度变化: {old_width} -> {new_width}")
        
        logger.debug(f"📋 样式解析完成: {len(matching_rules)} 个规则匹配, 最终宽度={getattr(final_style, 'width', None)}")
        return final_style
    
    def _get_breakpoint_priority(self, breakpoint: str) -> int:
        """获取断点优先级"""
        priority_map = {
            "xs": 100,
            "sm": 200, 
            "md": 300,
            "lg": 400,
            "xl": 500,
        }
        return priority_map.get(breakpoint, 0)
    
    def _merge_styles(self, base: ComponentStyle, override: ComponentStyle) -> ComponentStyle:
        """合并样式（override覆盖base中的非None值）"""
        merged_dict = base.__dict__.copy()
        
        for key, value in override.__dict__.items():
            if value is not None:
                merged_dict[key] = value
        
        return ComponentStyle(**merged_dict)


# ================================
# 3. 响应式管理器
# ================================

class ResponsiveManager:
    """响应式布局管理器"""
    
    _instance: Optional["ResponsiveManager"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        
        # 核心组件
        self.breakpoint_manager = BreakpointManager()
        
        # 组件注册表：使用弱引用防止内存泄漏
        self._registered_components: List[weakref.ReferenceType] = []
        
        # 样式变化回调
        self._style_change_callbacks: List[Callable[[float, List[str]], None]] = []
        
        # 当前状态
        self._current_viewport_width = 800
        self._is_updating = False  # 防止递归更新
        
        logger.info("🎯 ResponsiveManager 初始化完成")
    
    def register_component(self, component) -> None:
        """注册组件，使其响应断点变化"""
        # 检查组件是否有响应式样式
        if not hasattr(component, 'responsive_style') or not component.responsive_style:
            return
        
        # 使用弱引用注册
        component_ref = weakref.ref(component, self._cleanup_dead_reference)
        self._registered_components.append(component_ref)
        
        logger.debug(f"📝 注册响应式组件: {component.__class__.__name__}")
    
    def unregister_component(self, component) -> None:
        """注销组件"""
        self._registered_components = [
            ref for ref in self._registered_components 
            if ref() is not None and ref() is not component
        ]
        
        logger.debug(f"🗑️ 注销响应式组件: {component.__class__.__name__}")
    
    def update_viewport(self, width: float, height: float) -> None:
        """更新视口尺寸并触发响应式更新"""
        if self._is_updating:
            return  # 防止递归更新
        
        self._current_viewport_width = width
        
        # 检查断点是否变化
        breakpoint_changed = self.breakpoint_manager.update_viewport_width(width)
        
        if breakpoint_changed:
            logger.info(f"🔄 视口更新: {width}x{height}, 触发响应式更新")
            self._trigger_responsive_update()
        else:
            logger.debug(f"📐 视口更新: {width}x{height}, 断点未变化")
    
    def _trigger_responsive_update(self) -> None:
        """触发响应式样式更新"""
        if self._is_updating:
            return
        
        self._is_updating = True
        try:
            current_breakpoints = self.breakpoint_manager.get_current_breakpoints()
            
            # 清理死引用
            self._cleanup_dead_references()
            
            # 更新所有注册的组件
            updated_count = 0
            for component_ref in self._registered_components:
                component = component_ref()
                if component and hasattr(component, 'responsive_style'):
                    self._update_component_style(component, current_breakpoints)
                    updated_count += 1
            
            # 触发回调
            for callback in self._style_change_callbacks:
                try:
                    callback(self._current_viewport_width, current_breakpoints)
                except Exception as e:
                    logger.warning(f"⚠️ 样式变化回调异常: {e}")
            
            logger.info(f"✅ 响应式更新完成: {updated_count} 个组件已更新")
            
        finally:
            self._is_updating = False
    
    def _update_component_style(self, component, current_breakpoints: List[str]) -> None:
        """更新单个组件的响应式样式"""
        try:
            responsive_style = component.responsive_style
            if not isinstance(responsive_style, ResponsiveStyle):
                return
            
            # 解析响应式样式
            resolved_style = responsive_style.resolve(
                self._current_viewport_width, 
                current_breakpoints
            )
            
            # 更新组件样式
            old_style_width = getattr(component.style, 'width', None) if hasattr(component, 'style') else None
            component.style = resolved_style
            new_style_width = getattr(resolved_style, 'width', None)
            
            logger.debug(f"🎨 更新组件样式: {component.__class__.__name__}")
            if old_style_width != new_style_width:
                logger.debug(f"  样式宽度变化: {old_style_width} -> {new_style_width}")
            
            # 通知布局引擎更新
            self._notify_layout_engine(component)
            
        except Exception as e:
            logger.warning(f"⚠️ 更新组件样式失败: {component.__class__.__name__} - {e}")
    
    def _notify_layout_engine(self, component) -> None:
        """通知布局引擎组件样式已更新"""
        try:
            from .layout import get_layout_engine
            engine = get_layout_engine()
            engine.update_component_style(component)
        except Exception as e:
            logger.debug(f"⚠️ 通知布局引擎失败: {e}")
    
    def _cleanup_dead_references(self) -> None:
        """清理失效的弱引用"""
        before_count = len(self._registered_components)
        self._registered_components = [
            ref for ref in self._registered_components if ref() is not None
        ]
        after_count = len(self._registered_components)
        
        if before_count != after_count:
            logger.debug(f"🧹 清理了 {before_count - after_count} 个失效的组件引用")
    
    def _cleanup_dead_reference(self, weak_ref) -> None:
        """弱引用清理回调"""
        try:
            self._registered_components.remove(weak_ref)
        except ValueError:
            pass  # 引用已被移除
    
    def add_style_change_callback(self, callback: Callable[[float, List[str]], None]) -> None:
        """添加样式变化回调"""
        self._style_change_callbacks.append(callback)
    
    def get_current_breakpoint_info(self) -> Dict[str, Any]:
        """获取当前断点信息（用于调试）"""
        return {
            "viewport_width": self._current_viewport_width,
            "current_breakpoints": self.breakpoint_manager.get_current_breakpoints(),
            "primary_breakpoint": self.breakpoint_manager.get_primary_breakpoint(),
            "registered_components": len([ref for ref in self._registered_components if ref() is not None])
        }


# ================================
# 4. 便利功能和工厂函数
# ================================

def responsive_style(base_style: Optional[ComponentStyle] = None) -> ResponsiveStyle:
    """创建响应式样式的便利函数"""
    return ResponsiveStyle(base_style)

def breakpoint_style(**breakpoints) -> ResponsiveStyle:
    """根据断点创建样式的便利函数
    
    Example:
        style = breakpoint_style(
            xs=ComponentStyle(width=px(100)),
            md=ComponentStyle(width=px(200)),
            lg=ComponentStyle(width=px(300))
        )
    """
    rs = ResponsiveStyle()
    
    for bp_name, style in breakpoints.items():
        if isinstance(style, ComponentStyle):
            rs.at_breakpoint(bp_name, style)
    
    return rs

def media_query_style(
    min_width: Optional[float] = None,
    max_width: Optional[float] = None, 
    style: Optional[ComponentStyle] = None
) -> ResponsiveStyle:
    """基于媒体查询创建样式的便利函数"""
    rs = ResponsiveStyle()
    
    if style:
        if min_width is not None and max_width is not None:
            rs.at_width_range(min_width, max_width, style)
        elif min_width is not None:
            rs.at_min_width(min_width, style)
        elif max_width is not None:
            rs.at_max_width(max_width, style)
    
    return rs


# ================================
# 5. 管理器工厂集成
# ================================

def get_responsive_manager() -> ResponsiveManager:
    """获取响应式管理器实例"""
    return ResponsiveManager()


# ================================
# 6. 示例和测试
# ================================

if __name__ == "__main__":
    logger.info("🧪 Hibiki UI 响应式系统测试")
    
    # 测试断点管理器
    bp_mgr = BreakpointManager()
    bp_mgr.update_viewport_width(600)
    logger.info(f"600px 断点: {bp_mgr.get_current_breakpoints()}")
    
    bp_mgr.update_viewport_width(1000)
    logger.info(f"1000px 断点: {bp_mgr.get_current_breakpoints()}")
    
    # 测试响应式样式
    rs = (responsive_style(ComponentStyle(width=px(100)))
          .at_breakpoint(BreakpointName.SM, ComponentStyle(width=px(200)))
          .at_breakpoint(BreakpointName.LG, ComponentStyle(width=px(400)))
          .at_min_width(1200, ComponentStyle(width=px(500))))
    
    resolved = rs.resolve(800, ["md"])
    logger.info(f"解析样式 (800px, md): width={resolved.width}")
    
    resolved = rs.resolve(1300, ["xl"])
    logger.info(f"解析样式 (1300px, xl): width={resolved.width}")
    
    # 测试响应式管理器
    rm = ResponsiveManager()
    info = rm.get_current_breakpoint_info()
    logger.info(f"响应式管理器状态: {info}")
    
    logger.info("✅ 响应式系统测试完成！")