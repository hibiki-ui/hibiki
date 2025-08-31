#!/usr/bin/env python3
"""
CLI Debug Tools - 命令行调试工具
==============================

提供便捷的命令行接口来使用 Hibiki UI 调试功能。
可以直接在开发过程中快速调用各种调试工具。
"""

import argparse
import sys
import importlib.util
from pathlib import Path
from typing import Optional, Any, List

from ..core.logging import get_logger
from .tree_visualizer import TreeVisualizer, ColorTheme
from .performance_monitor import PerformanceMonitor
from .layout_inspector import LayoutInspector, InspectionLevel
from .export_tools import DebugExporter

logger = get_logger("debug.cli")


class DebugCLI:
    """调试命令行工具
    
    提供统一的命令行接口来访问所有调试功能：
    - hibiki-debug tree <script.py> - 显示组件树
    - hibiki-debug inspect <script.py> - 检查布局
    - hibiki-debug export <script.py> - 导出调试信息
    - hibiki-debug monitor <script.py> - 性能监控
    """
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """创建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            prog="hibiki-debug",
            description="Hibiki UI 调试工具集",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例用法:
  hibiki-debug tree my_app.py                    # 显示组件树
  hibiki-debug tree my_app.py --no-color        # 无颜色输出
  hibiki-debug inspect my_app.py --level=complete # 完整检查
  hibiki-debug export my_app.py --format=html   # 导出HTML报告
  hibiki-debug monitor my_app.py --duration=30  # 30秒性能监控
            """
        )
        
        # 全局选项
        parser.add_argument(
            "--verbose", "-v", 
            action="store_true",
            help="启用详细日志输出"
        )
        
        # 子命令
        subparsers = parser.add_subparsers(
            dest="command",
            help="可用的调试命令",
            required=True
        )
        
        # tree 命令
        tree_parser = subparsers.add_parser("tree", help="显示组件树结构")
        tree_parser.add_argument("script", help="Python脚本文件路径")
        tree_parser.add_argument("--no-color", action="store_true", help="禁用颜色输出")
        tree_parser.add_argument("--max-depth", type=int, help="最大显示深度")
        tree_parser.add_argument("--no-performance", action="store_true", help="禁用性能信息")
        
        # inspect 命令
        inspect_parser = subparsers.add_parser("inspect", help="检查布局信息")
        inspect_parser.add_argument("script", help="Python脚本文件路径")
        inspect_parser.add_argument("--level", choices=["basic", "detailed", "complete"], 
                                  default="detailed", help="检查深度级别")
        inspect_parser.add_argument("--problems-only", action="store_true", help="仅显示问题")
        inspect_parser.add_argument("--suggestions", action="store_true", help="包含优化建议")
        
        # export 命令
        export_parser = subparsers.add_parser("export", help="导出调试信息")
        export_parser.add_argument("script", help="Python脚本文件路径") 
        export_parser.add_argument("--format", choices=["json", "html", "txt", "csv", "full"],
                                 default="html", help="导出格式")
        export_parser.add_argument("--output", "-o", help="输出文件路径")
        export_parser.add_argument("--output-dir", help="输出目录")
        
        # monitor 命令
        monitor_parser = subparsers.add_parser("monitor", help="性能监控")
        monitor_parser.add_argument("script", help="Python脚本文件路径")
        monitor_parser.add_argument("--duration", type=float, default=10.0, help="监控时长(秒)")
        monitor_parser.add_argument("--interval", type=float, default=0.1, help="采样间隔(秒)")
        monitor_parser.add_argument("--export-report", action="store_true", help="自动导出性能报告")
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """运行CLI工具
        
        Args:
            args: 命令行参数列表，None表示使用sys.argv
            
        Returns:
            退出代码
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            if parsed_args.verbose:
                logger.setLevel("DEBUG")
            
            # 执行对应的子命令
            if parsed_args.command == "tree":
                return self._handle_tree_command(parsed_args)
            elif parsed_args.command == "inspect":
                return self._handle_inspect_command(parsed_args)
            elif parsed_args.command == "export":
                return self._handle_export_command(parsed_args)
            elif parsed_args.command == "monitor":
                return self._handle_monitor_command(parsed_args)
            else:
                self.parser.print_help()
                return 1
                
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            if parsed_args and parsed_args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _handle_tree_command(self, args) -> int:
        """处理tree命令"""
        component = self._load_component_from_script(args.script)
        if not component:
            return 1
        
        color_theme = ColorTheme.NONE if args.no_color else ColorTheme.TERMINAL
        
        visualizer = TreeVisualizer(
            color_theme=color_theme,
            show_performance=not args.no_performance,
            max_depth=args.max_depth
        )
        
        tree_output = visualizer.format_tree(
            component, 
            title=f"组件树结构 - {Path(args.script).name}"
        )
        
        print(tree_output)
        return 0
    
    def _handle_inspect_command(self, args) -> int:
        """处理inspect命令"""
        component = self._load_component_from_script(args.script)
        if not component:
            return 1
        
        level_enum = InspectionLevel(args.level)
        inspector = LayoutInspector(level_enum)
        
        if args.problems_only:
            issues = inspector.find_layout_issues(component)
            if issues:
                print(f"🔍 发现 {len(issues)} 个布局问题:")
                print()
                for i, issue in enumerate(issues, 1):
                    print(f"{i}. [{issue['issue_type'].upper()}] {issue['description']}")
                    print(f"   组件: {issue['component_type']} ({issue['component_id']})")
                    if issue.get('suggestions'):
                        print(f"   建议: {', '.join(issue['suggestions'])}")
                    print()
            else:
                print("✅ 未发现布局问题")
        else:
            report = inspector.generate_inspection_report(component)
            self._print_inspection_report(report, args.suggestions)
        
        return 0
    
    def _handle_export_command(self, args) -> int:
        """处理export命令"""
        component = self._load_component_from_script(args.script)
        if not component:
            return 1
        
        output_dir = Path(args.output_dir) if args.output_dir else None
        exporter = DebugExporter(output_dir)
        
        try:
            if args.format == "full":
                filepath = exporter.export_full_debug_report(component, args.output)
            else:
                filepath = exporter.export_component_tree(
                    component, 
                    args.format, 
                    args.output
                )
            
            print(f"✅ 调试信息已导出: {filepath}")
            return 0
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return 1
    
    def _handle_monitor_command(self, args) -> int:
        """处理monitor命令"""
        component = self._load_component_from_script(args.script)
        if not component:
            return 1
        
        print(f"🚀 开始监控组件性能，时长: {args.duration}秒")
        print("按 Ctrl+C 可以提前停止监控")
        
        monitor = PerformanceMonitor(
            collection_interval=args.interval,
            enable_auto_collection=True
        )
        
        try:
            monitor.start_monitoring(component)
            
            # 等待监控完成
            import time
            time.sleep(args.duration)
            
            monitor.stop_monitoring()
            
            # 显示监控结果
            summary = monitor.get_performance_summary()
            self._print_performance_summary(summary)
            
            # 导出报告（如果需要）
            if args.export_report:
                exporter = DebugExporter()
                report_path = exporter.export_performance_report()
                print(f"📄 性能报告已导出: {report_path}")
            
            return 0
            
        except KeyboardInterrupt:
            print("\n⏹️ 监控被用户中断")
            monitor.stop_monitoring()
            return 0
        except Exception as e:
            print(f"❌ 监控失败: {e}")
            return 1
    
    def _load_component_from_script(self, script_path: str) -> Optional[Any]:
        """从脚本文件加载组件
        
        这是一个简化的实现，实际使用时需要更复杂的脚本执行逻辑。
        """
        try:
            script_file = Path(script_path)
            if not script_file.exists():
                print(f"❌ 脚本文件不存在: {script_path}")
                return None
            
            # TODO: 实现安全的脚本执行和组件提取
            print("⚠️ CLI脚本执行功能正在开发中")
            print("请直接在您的应用代码中使用调试API")
            return None
            
        except Exception as e:
            logger.error(f"加载脚本失败: {e}")
            return None
    
    def _print_inspection_report(self, report: dict, include_suggestions: bool):
        """打印检查报告"""
        summary = report["summary"]
        
        print("🔍 布局检查报告")
        print("=" * 50)
        print(f"检查时间: {summary['inspection_time']:.2f}ms")
        print(f"总组件数: {summary['total_components']}")
        print(f"健康组件: {summary['healthy_components']}")
        print(f"异常组件: {summary['unhealthy_components']}")
        print(f"总警告数: {summary['total_warnings']}")
        print()
        
        # 组件类型分布
        print("📊 组件类型分布:")
        for comp_type, count in summary['type_distribution'].items():
            print(f"   {comp_type}: {count}")
        print()
        
        # 显示问题组件
        problem_components = [
            comp for comp in report['components']
            if comp['warnings'] or not comp['stretchable_valid']
        ]
        
        if problem_components:
            print(f"⚠️ 发现 {len(problem_components)} 个问题组件:")
            print()
            for comp in problem_components:
                print(f"🔸 {comp['component_type']} ({comp['component_id']})")
                if comp['warnings']:
                    for warning in comp['warnings']:
                        print(f"   • {warning}")
                if not comp['stretchable_valid']:
                    print("   • 布局节点状态异常")
                print()
        else:
            print("✅ 未发现布局问题")
    
    def _print_performance_summary(self, summary: dict):
        """打印性能摘要"""
        print("📊 性能监控摘要")
        print("=" * 50)
        
        if 'collection_period' in summary:
            period = summary['collection_period']
            print(f"监控时长: {period['duration']:.1f}秒")
            print(f"数据点数: {summary.get('metrics_count', 0)}")
            print()
        
        if 'current_stats' in summary:
            print("当前状态:")
            for key, value in summary['current_stats'].items():
                print(f"   {key}: {value:.2f}")
            print()
        
        if 'averages' in summary:
            print("平均值:")
            for key, value in summary['averages'].items():
                print(f"   {key}: {value:.2f}")
            print()
        
        if 'peaks' in summary:
            print("峰值:")
            for key, value in summary['peaks'].items():
                print(f"   {key}: {value:.2f}")


def main():
    """CLI主入口函数"""
    cli = DebugCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


# 便捷的独立函数，可以直接在代码中调用
def debug_component_tree(component, 
                        color: bool = True,
                        max_depth: Optional[int] = None,
                        show_performance: bool = True):
    """在控制台显示组件树（便捷函数）
    
    Args:
        component: 要调试的组件
        color: 是否使用颜色
        max_depth: 最大显示深度
        show_performance: 是否显示性能信息
    """
    color_theme = ColorTheme.TERMINAL if color else ColorTheme.NONE
    
    visualizer = TreeVisualizer(
        color_theme=color_theme,
        show_performance=show_performance,
        max_depth=max_depth
    )
    
    tree_output = visualizer.format_tree(component, "组件树结构")
    print(tree_output)


def debug_component_layout(component, 
                          level: str = "detailed",
                          problems_only: bool = False,
                          show_suggestions: bool = False):
    """检查组件布局（便捷函数）
    
    Args:
        component: 要检查的组件
        level: 检查级别
        problems_only: 仅显示问题
        show_suggestions: 显示优化建议
    """
    level_enum = InspectionLevel(level)
    inspector = LayoutInspector(level_enum)
    
    if problems_only:
        issues = inspector.find_layout_issues(component)
        if issues:
            print(f"🔍 发现 {len(issues)} 个布局问题:")
            print()
            for i, issue in enumerate(issues, 1):
                print(f"{i}. [{issue['issue_type'].upper()}] {issue['description']}")
                print(f"   组件: {issue['component_type']}")
                if show_suggestions and issue.get('suggestions'):
                    print(f"   建议: {', '.join(issue['suggestions'])}")
                print()
        else:
            print("✅ 未发现布局问题")
    else:
        report = inspector.generate_inspection_report(component)
        summary = report["summary"]
        
        print("🔍 布局检查结果")
        print("=" * 40)
        print(f"总组件数: {summary['total_components']}")
        print(f"健康组件: {summary['healthy_components']}")
        print(f"异常组件: {summary['unhealthy_components']}")
        print(f"总警告数: {summary['total_warnings']}")
        
        if show_suggestions:
            suggestions = inspector.get_optimization_suggestions(component)
            if suggestions:
                print("\n💡 优化建议:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. [{suggestion['priority'].upper()}] {suggestion['description']}")
                    print(f"   建议: {suggestion['suggestion']}")


def quick_debug(component, export_html: bool = False):
    """快速调试函数（便捷函数）
    
    显示组件树、检查布局问题、可选导出HTML报告
    
    Args:
        component: 要调试的组件
        export_html: 是否导出HTML报告
    """
    print("🔧 Hibiki UI 快速调试")
    print("=" * 50)
    print()
    
    # 显示组件树
    print("🌳 组件树结构:")
    debug_component_tree(component, max_depth=5)
    print()
    
    # 检查布局问题
    print("🔍 布局问题检查:")
    debug_component_layout(component, problems_only=True, show_suggestions=True)
    print()
    
    # 导出HTML报告（如果需要）
    if export_html:
        try:
            from .export_tools import export_debug_info
            report_path = export_debug_info(component, format="full")
            print(f"📄 详细调试报告已导出: {report_path}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")


if __name__ == "__main__":
    main()