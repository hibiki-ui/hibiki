"""
布局调试系统 - 全面的布局计算和应用状态监控
用于快速发现和修复布局相关问题
"""

from typing import Optional, Dict, Any, List, Tuple
from AppKit import NSView
from Foundation import NSMakeRect
from .node import LayoutNode
import time

class LayoutDebugger:
    """布局调试器 - 监控和验证布局计算与应用"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.debug_records = []
        self.layout_mismatches = []
        
    def log_layout_computation(self, node: LayoutNode, before_compute=True):
        """记录布局计算过程"""
        if not self.enabled:
            return
            
        timestamp = time.time()
        stage = "BEFORE_COMPUTE" if before_compute else "AFTER_COMPUTE"
        
        record = {
            'timestamp': timestamp,
            'stage': stage,
            'node_key': node.key,
            'node_id': id(node),
            'has_stretchable_node': node._stretchable_node is not None,
        }
        
        if before_compute:
            # 记录计算前的状态
            record.update({
                'style_width': getattr(node.style, 'width', None) if node.style else None,
                'style_height': getattr(node.style, 'height', None) if node.style else None,
                'children_count': len(node.children),
                'is_dirty': node.is_dirty(),
            })
        else:
            # 记录计算后的布局结果
            try:
                x, y, w, h = node.get_layout()
                record.update({
                    'computed_x': x,
                    'computed_y': y, 
                    'computed_width': w,
                    'computed_height': h,
                })
            except Exception as e:
                record['layout_error'] = str(e)
        
        self.debug_records.append(record)
        
        if self.enabled:
            self._print_computation_log(record)
    
    def log_layout_application(self, node: LayoutNode, nsview: NSView, success: bool):
        """记录布局应用到NSView的过程"""
        if not self.enabled:
            return
            
        timestamp = time.time()
        
        # 获取理论布局
        try:
            expected_x, expected_y, expected_w, expected_h = node.get_layout()
        except Exception as e:
            expected_x = expected_y = expected_w = expected_h = None
            
        # 获取实际NSView布局
        try:
            actual_frame = nsview.frame()
            actual_x = actual_frame.origin.x
            actual_y = actual_frame.origin.y
            actual_w = actual_frame.size.width
            actual_h = actual_frame.size.height
        except Exception as e:
            actual_x = actual_y = actual_w = actual_h = None
        
        record = {
            'timestamp': timestamp,
            'stage': 'LAYOUT_APPLICATION',
            'node_key': node.key,
            'node_id': id(node),
            'nsview_id': id(nsview) if nsview else None,
            'nsview_type': type(nsview).__name__ if nsview else None,
            'success': success,
            'expected_x': expected_x,
            'expected_y': expected_y,
            'expected_width': expected_w,
            'expected_height': expected_h,
            'actual_x': actual_x,
            'actual_y': actual_y,
            'actual_width': actual_w,
            'actual_height': actual_h,
        }
        
        # 检查是否存在布局不匹配
        mismatch = self._check_layout_mismatch(record)
        if mismatch:
            record['mismatch'] = mismatch
            self.layout_mismatches.append(record)
        
        self.debug_records.append(record)
        
        if self.enabled:
            self._print_application_log(record)
    
    def log_hierarchy_structure(self, root_node: LayoutNode):
        """记录整个布局层次结构"""
        if not self.enabled:
            return
            
        print("🌳 === 布局层次结构分析 ===")
        self._print_node_hierarchy(root_node, 0)
        print("🌳 === 层次结构分析完成 ===")
    
    def _print_computation_log(self, record):
        """打印布局计算日志"""
        stage = record['stage']
        node_key = record['node_key']
        
        if stage == "BEFORE_COMPUTE":
            print(f"🔄 [计算前] 节点: {node_key}")
            print(f"   样式尺寸: {record.get('style_width')}x{record.get('style_height')}")
            print(f"   子节点数: {record.get('children_count')}")
            print(f"   是否脏: {record.get('is_dirty')}")
            print(f"   有Stretchable节点: {record.get('has_stretchable_node')}")
        else:
            print(f"✅ [计算后] 节点: {node_key}")
            if 'layout_error' in record:
                print(f"   ❌ 布局计算错误: {record['layout_error']}")
            else:
                x, y, w, h = record['computed_x'], record['computed_y'], record['computed_width'], record['computed_height']
                print(f"   📐 计算结果: ({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})")
    
    def _print_application_log(self, record):
        """打印布局应用日志"""
        node_key = record['node_key']
        nsview_type = record['nsview_type']
        success = record['success']
        
        print(f"📍 [布局应用] 节点: {node_key} -> {nsview_type}")
        
        if success:
            expected = f"({record['expected_x']:.1f}, {record['expected_y']:.1f}, {record['expected_width']:.1f}, {record['expected_height']:.1f})"
            actual = f"({record['actual_x']:.1f}, {record['actual_y']:.1f}, {record['actual_width']:.1f}, {record['actual_height']:.1f})"
            
            print(f"   🎯 期望: {expected}")
            print(f"   📦 实际: {actual}")
            
            if 'mismatch' in record:
                mismatch = record['mismatch']
                print(f"   ⚠️ 不匹配: {mismatch}")
            else:
                print(f"   ✅ 匹配正确")
        else:
            print(f"   ❌ 应用失败")
    
    def _print_node_hierarchy(self, node: LayoutNode, level: int):
        """递归打印节点层次"""
        indent = "  " * level
        
        try:
            x, y, w, h = node.get_layout()
            layout_info = f"({x:.1f}, {y:.1f}, {w:.1f}, {h:.1f})"
        except:
            layout_info = "(计算失败)"
        
        user_data_type = type(node.user_data).__name__ if node.user_data else "None"
        
        print(f"{indent}📦 {node.key}: {layout_info} -> {user_data_type}")
        
        for child in node.children:
            self._print_node_hierarchy(child, level + 1)
    
    def _check_layout_mismatch(self, record) -> Optional[str]:
        """检查布局是否匹配"""
        expected_x = record['expected_x']
        expected_y = record['expected_y']
        expected_w = record['expected_width']
        expected_h = record['expected_height']
        
        actual_x = record['actual_x']
        actual_y = record['actual_y'] 
        actual_w = record['actual_width']
        actual_h = record['actual_height']
        
        if any(val is None for val in [expected_x, expected_y, expected_w, expected_h, actual_x, actual_y, actual_w, actual_h]):
            return "缺少布局数据"
        
        tolerance = 1.0  # 1像素的容差
        
        mismatches = []
        if abs(expected_x - actual_x) > tolerance:
            mismatches.append(f"X偏移: 期望{expected_x:.1f}, 实际{actual_x:.1f}")
        if abs(expected_y - actual_y) > tolerance:
            mismatches.append(f"Y偏移: 期望{expected_y:.1f}, 实际{actual_y:.1f}")
        if abs(expected_w - actual_w) > tolerance:
            mismatches.append(f"宽度: 期望{expected_w:.1f}, 实际{actual_w:.1f}")
        if abs(expected_h - actual_h) > tolerance:
            mismatches.append(f"高度: 期望{expected_h:.1f}, 实际{actual_h:.1f}")
        
        return "; ".join(mismatches) if mismatches else None
    
    def generate_summary_report(self):
        """生成调试摘要报告"""
        if not self.enabled:
            return
            
        print("📊 === 布局调试摘要报告 ===")
        print(f"总记录数: {len(self.debug_records)}")
        print(f"布局不匹配数: {len(self.layout_mismatches)}")
        
        # 统计各阶段记录
        stage_counts = {}
        for record in self.debug_records:
            stage = record['stage']
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        print("各阶段统计:")
        for stage, count in stage_counts.items():
            print(f"  {stage}: {count}")
        
        # 列出所有不匹配
        if self.layout_mismatches:
            print("\n⚠️ 布局不匹配详情:")
            for i, mismatch in enumerate(self.layout_mismatches):
                print(f"  {i+1}. 节点 {mismatch['node_key']}: {mismatch['mismatch']}")
        else:
            print("\n✅ 无布局不匹配问题")
        
        print("📊 === 调试报告完成 ===")

# 全局调试器实例
_global_debugger: Optional[LayoutDebugger] = None

def get_layout_debugger() -> LayoutDebugger:
    """获取全局布局调试器"""
    global _global_debugger
    if _global_debugger is None:
        _global_debugger = LayoutDebugger(enabled=True)
    return _global_debugger

def enable_layout_debug(enabled: bool = True):
    """启用/禁用布局调试"""
    get_layout_debugger().enabled = enabled

def log_layout_computation(node: LayoutNode, before_compute=True):
    """记录布局计算"""
    get_layout_debugger().log_layout_computation(node, before_compute)

def log_layout_application(node: LayoutNode, nsview: NSView, success: bool):
    """记录布局应用"""
    get_layout_debugger().log_layout_application(node, nsview, success)

def log_hierarchy_structure(root_node: LayoutNode):
    """记录层次结构"""
    get_layout_debugger().log_hierarchy_structure(root_node)

def generate_debug_report():
    """生成调试报告"""
    get_layout_debugger().generate_summary_report()