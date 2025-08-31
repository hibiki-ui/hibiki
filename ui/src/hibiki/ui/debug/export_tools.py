#!/usr/bin/env python3
"""
Export Tools - 调试信息导出工具
==============================

支持将调试信息导出为多种格式：JSON、HTML、CSV等。
提供丰富的可视化和分析功能。
"""

import json
import time
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from datetime import datetime

from ..core.logging import get_logger
from .tree_visualizer import TreeVisualizer, ColorTheme
from .performance_monitor import get_global_monitor

logger = get_logger("debug.export_tools")


class DebugExporter:
    """调试信息导出器
    
    功能特性：
    - 多格式导出支持
    - 自定义HTML模板
    - 数据可视化图表
    - 批量导出管理
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """初始化导出器
        
        Args:
            output_dir: 输出目录，默认为当前目录下的 debug_exports
        """
        self.output_dir = output_dir or Path("debug_exports")
        self.output_dir.mkdir(exist_ok=True)
        
        # 导出模板
        self._html_template = self._get_default_html_template()
    
    def export_component_tree(self, 
                            component, 
                            format: str = "html",
                            filename: Optional[str] = None,
                            include_performance: bool = True,
                            color_theme: str = "html") -> Path:
        """导出组件树信息
        
        Args:
            component: 要导出的组件
            format: 导出格式 ("json", "html", "txt")
            filename: 文件名，不指定则自动生成
            include_performance: 是否包含性能信息
            color_theme: 颜色主题 ("none", "terminal", "html")
            
        Returns:
            导出文件的路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"component_tree_{timestamp}.{format}"
        
        filepath = self.output_dir / filename
        
        if format == "json":
            return self._export_tree_json(component, filepath, include_performance)
        elif format == "html":
            return self._export_tree_html(component, filepath, include_performance, color_theme)
        elif format == "txt":
            return self._export_tree_txt(component, filepath, include_performance, color_theme)
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def export_performance_report(self,
                                 format: str = "html",
                                 filename: Optional[str] = None,
                                 time_range: Optional[tuple] = None) -> Path:
        """导出性能报告
        
        Args:
            format: 导出格式
            filename: 文件名
            time_range: 时间范围
            
        Returns:
            导出文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"performance_report_{timestamp}.{format}"
        
        filepath = self.output_dir / filename
        
        monitor = get_global_monitor()
        
        if format == "json":
            return self._export_performance_json(monitor, filepath, time_range)
        elif format == "html":
            return self._export_performance_html(monitor, filepath, time_range)
        elif format == "csv":
            return self._export_performance_csv(monitor, filepath, time_range)
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def export_full_debug_report(self,
                                component,
                                filename: Optional[str] = None) -> Path:
        """导出完整调试报告（HTML格式）
        
        Args:
            component: 要分析的组件
            filename: 输出文件名
            
        Returns:
            导出文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            filename = f"debug_report_{timestamp}.html"
        
        filepath = self.output_dir / filename
        
        # 收集所有调试信息
        tree_visualizer = TreeVisualizer(
            color_theme=ColorTheme.HTML,
            show_performance=True,
            show_memory_info=True
        )
        
        tree_html = tree_visualizer.format_tree(
            component, 
            title="组件树结构"
        )
        
        monitor = get_global_monitor()
        performance_data = monitor.get_performance_summary()
        
        # 生成HTML报告
        html_content = self._generate_full_report_html(
            tree_html, 
            performance_data,
            timestamp
        )
        
        filepath.write_text(html_content, encoding='utf-8')
        logger.info(f"✅ 完整调试报告已导出: {filepath}")
        
        return filepath
    
    def _export_tree_json(self, component, filepath: Path, include_performance: bool) -> Path:
        """导出JSON格式的组件树"""
        from ..core.layout import get_layout_engine
        
        engine = get_layout_engine()
        tree_info = engine.get_node_tree_info(component)
        
        export_data = {
            "timestamp": time.time(),
            "export_type": "component_tree",
            "tree_structure": tree_info,
            "metadata": {
                "component_type": type(component).__name__,
                "component_id": str(id(component))
            }
        }
        
        if include_performance:
            monitor = get_global_monitor()
            export_data["performance"] = monitor.get_current_stats()
        
        filepath.write_text(
            json.dumps(export_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        logger.info(f"✅ 组件树JSON已导出: {filepath}")
        return filepath
    
    def _export_tree_html(self, component, filepath: Path, 
                         include_performance: bool, color_theme: str) -> Path:
        """导出HTML格式的组件树"""
        theme_enum = ColorTheme.HTML if color_theme == "html" else ColorTheme.NONE
        
        visualizer = TreeVisualizer(
            color_theme=theme_enum,
            show_performance=include_performance
        )
        
        tree_content = visualizer.format_tree(component, "组件树结构")
        stats = visualizer.get_stats()
        
        # 生成HTML
        html_content = self._html_template.format(
            title="Hibiki UI 组件树结构",
            content=f"<pre>{tree_content}</pre>",
            stats=self._format_stats_html(stats),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        filepath.write_text(html_content, encoding='utf-8')
        logger.info(f"✅ 组件树HTML已导出: {filepath}")
        
        return filepath
    
    def _export_tree_txt(self, component, filepath: Path,
                        include_performance: bool, color_theme: str) -> Path:
        """导出TXT格式的组件树"""
        theme_enum = ColorTheme.TERMINAL if color_theme == "terminal" else ColorTheme.NONE
        
        visualizer = TreeVisualizer(
            color_theme=theme_enum,
            show_performance=include_performance
        )
        
        tree_content = visualizer.format_tree(component, "组件树结构")
        
        filepath.write_text(tree_content, encoding='utf-8')
        logger.info(f"✅ 组件树TXT已导出: {filepath}")
        
        return filepath
    
    def _export_performance_json(self, monitor, filepath: Path, time_range) -> Path:
        """导出JSON格式的性能报告"""
        performance_data = monitor.export_data("dict")
        
        filepath.write_text(
            json.dumps(performance_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        logger.info(f"✅ 性能报告JSON已导出: {filepath}")
        return filepath
    
    def _export_performance_html(self, monitor, filepath: Path, time_range) -> Path:
        """导出HTML格式的性能报告"""
        performance_data = monitor.get_performance_summary()
        
        # 生成性能图表HTML
        charts_html = self._generate_performance_charts(performance_data)
        
        html_content = self._html_template.format(
            title="Hibiki UI 性能报告",
            content=charts_html,
            stats=self._format_performance_stats_html(performance_data),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        filepath.write_text(html_content, encoding='utf-8')
        logger.info(f"✅ 性能报告HTML已导出: {filepath}")
        
        return filepath
    
    def _export_performance_csv(self, monitor, filepath: Path, time_range) -> Path:
        """导出CSV格式的性能数据"""
        csv_data = monitor.export_data("csv")
        
        filepath.write_text(csv_data, encoding='utf-8')
        logger.info(f"✅ 性能数据CSV已导出: {filepath}")
        
        return filepath
    
    def _generate_full_report_html(self, tree_html: str, 
                                  performance_data: dict,
                                  timestamp: str) -> str:
        """生成完整的HTML调试报告"""
        content = f"""
        <div class="report-section">
            <h2>🌳 组件树结构</h2>
            <div class="tree-container">
                <pre>{tree_html}</pre>
            </div>
        </div>
        
        <div class="report-section">
            <h2>📊 性能统计</h2>
            {self._format_performance_stats_html(performance_data)}
        </div>
        
        <div class="report-section">
            <h2>📈 性能图表</h2>
            {self._generate_performance_charts(performance_data)}
        </div>
        """
        
        return self._get_full_report_html_template().format(
            title="Hibiki UI 完整调试报告",
            content=content,
            timestamp=timestamp
        )
    
    def _format_stats_html(self, stats: dict) -> str:
        """格式化统计信息为HTML"""
        if not stats:
            return "<p>暂无统计信息</p>"
        
        html = "<div class='stats-grid'>"
        for key, value in stats.items():
            html += f"""
            <div class='stat-item'>
                <span class='stat-label'>{key}:</span>
                <span class='stat-value'>{value}</span>
            </div>
            """
        html += "</div>"
        
        return html
    
    def _format_performance_stats_html(self, performance_data: dict) -> str:
        """格式化性能统计为HTML"""
        if not performance_data:
            return "<p>暂无性能数据</p>"
        
        html = "<div class='performance-stats'>"
        
        # 当前统计
        if 'current_stats' in performance_data:
            html += "<h3>当前状态</h3>"
            html += "<div class='stats-grid'>"
            for key, value in performance_data['current_stats'].items():
                html += f"""
                <div class='stat-item'>
                    <span class='stat-label'>{key}:</span>
                    <span class='stat-value'>{value:.2f}</span>
                </div>
                """
            html += "</div>"
        
        # 平均值
        if 'averages' in performance_data:
            html += "<h3>平均值</h3>"
            html += "<div class='stats-grid'>"
            for key, value in performance_data['averages'].items():
                html += f"""
                <div class='stat-item'>
                    <span class='stat-label'>{key}:</span>
                    <span class='stat-value'>{value:.2f}</span>
                </div>
                """
            html += "</div>"
        
        # 峰值
        if 'peaks' in performance_data:
            html += "<h3>峰值</h3>"
            html += "<div class='stats-grid'>"
            for key, value in performance_data['peaks'].items():
                html += f"""
                <div class='stat-item'>
                    <span class='stat-label'>{key}:</span>
                    <span class='stat-value'>{value:.2f}</span>
                </div>
                """
            html += "</div>"
        
        html += "</div>"
        return html
    
    def _generate_performance_charts(self, performance_data: dict) -> str:
        """生成性能图表HTML（使用Chart.js）"""
        # 这里可以集成Chart.js或其他图表库
        # 目前返回占位符
        return """
        <div class="charts-container">
            <p>📊 性能图表功能正在开发中...</p>
            <p>将支持：</p>
            <ul>
                <li>实时性能曲线</li>
                <li>组件数量趋势</li>
                <li>布局时间分析</li>
                <li>内存使用监控</li>
            </ul>
        </div>
        """
    
    def _get_default_html_template(self) -> str:
        """获取默认HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f7;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.4;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-item {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .stat-label {{
            font-weight: 600;
            color: #495057;
        }}
        .stat-value {{
            color: #007acc;
            font-weight: bold;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>生成时间: {timestamp}</p>
        </div>
        <div class="content">
            {content}
            {stats}
        </div>
        <div class="footer">
            <p>🤖 Generated by Hibiki UI Debug Tools v1.0</p>
        </div>
    </div>
</body>
</html>"""
    
    def _get_full_report_html_template(self) -> str:
        """获取完整报告的HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f7;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 3em;
            font-weight: 300;
        }}
        .header p {{
            margin: 15px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .content {{
            padding: 40px;
        }}
        .report-section {{
            margin-bottom: 50px;
            border-bottom: 1px solid #e9ecef;
            padding-bottom: 30px;
        }}
        .report-section:last-child {{
            border-bottom: none;
        }}
        .report-section h2 {{
            color: #495057;
            font-size: 2em;
            margin-bottom: 20px;
            font-weight: 400;
        }}
        .tree-container {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 30px;
            overflow-x: auto;
        }}
        .tree-container pre {{
            margin: 0;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.5;
            background: none;
            border: none;
            padding: 0;
        }}
        .performance-stats {{
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 30px;
        }}
        .performance-stats h3 {{
            color: #495057;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .performance-stats h3:first-child {{
            margin-top: 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-item {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-label {{
            font-weight: 600;
            color: #495057;
            display: block;
            margin-bottom: 5px;
        }}
        .stat-value {{
            color: #007acc;
            font-weight: bold;
            font-size: 1.3em;
        }}
        .charts-container {{
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>生成时间: {timestamp}</p>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>🤖 Generated by Hibiki UI Debug Tools v1.0</p>
            <p>Powered by Claude Code</p>
        </div>
    </div>
</body>
</html>"""


# 便捷函数
def export_debug_info(component, 
                     format: str = "html",
                     filename: Optional[str] = None,
                     output_dir: Optional[Path] = None) -> Path:
    """导出调试信息（便捷函数）
    
    Args:
        component: 要导出的组件
        format: 导出格式 ("html", "json", "txt", "full")
        filename: 输出文件名
        output_dir: 输出目录
        
    Returns:
        导出文件路径
    """
    exporter = DebugExporter(output_dir)
    
    if format == "full":
        return exporter.export_full_debug_report(component, filename)
    else:
        return exporter.export_component_tree(component, format, filename)


if __name__ == "__main__":
    # 测试代码
    print("📄 Hibiki UI Export Tools")
    print("=========================")
    print()
    print("这是一个专业的调试信息导出工具。")
    print("支持导出为 JSON、HTML、CSV 等多种格式。")
    print()
    print("示例用法:")
    print("```python")
    print("from hibiki.ui.debug import export_debug_info")
    print("filepath = export_debug_info(my_component, format='html')")
    print("print(f'调试报告已导出: {filepath}')")
    print("```")