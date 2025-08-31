#!/usr/bin/env python3
"""
调试工具测试 - 验证新的 hibiki.ui.debug 模块
==========================================

测试新创建的调试工具模块的所有功能：
- TreeVisualizer: 树状结构可视化
- PerformanceMonitor: 性能监控
- LayoutInspector: 布局检查
- DebugExporter: 导出功能
- CLI工具: 命令行接口
"""

from hibiki.ui import (
    Label, Button, Container, ComponentStyle,
    Display, FlexDirection, px, percent,
    ManagerFactory
)

from hibiki.ui.components.layout import VStack, ScrollableContainer
from hibiki.ui.core.logging import get_logger

# 导入新的调试工具
from hibiki.ui.debug import (
    TreeVisualizer, ColorTheme,
    PerformanceMonitor, MetricType,
    LayoutInspector, InspectionLevel,
    export_debug_info,
    debug_tree, debug_layout, debug_performance,
    quick_debug
)

logger = get_logger("debug_tools_test")


def create_test_component():
    """创建用于测试的组件层次结构"""
    # 创建一些测试子组件
    children = [
        Label("测试标签1", style=ComponentStyle(padding=px(10))),
        Button("测试按钮", on_click=lambda: print("按钮点击"), 
               style=ComponentStyle(margin=px(5))),
        Label("测试标签2", style=ComponentStyle(background_color="#f0f0f0"))
    ]
    
    # VStack 容器
    vstack = VStack(
        children=children,
        spacing=8,
        style=ComponentStyle(padding=px(16), width=percent(80))
    )
    
    # ScrollableContainer 包装
    scroll_container = ScrollableContainer(
        children=[vstack],
        scroll_vertical=True,
        style=ComponentStyle(
            width=px(400),
            height=px(300),
            background_color="#ffffff"
        )
    )
    
    return scroll_container


def test_tree_visualizer():
    """测试树状可视化工具"""
    logger.info("🧪 测试TreeVisualizer...")
    
    component = create_test_component()
    
    # 测试不同的颜色主题
    themes = [
        (ColorTheme.NONE, "无颜色"),
        (ColorTheme.TERMINAL, "终端颜色"),
        (ColorTheme.HTML, "HTML颜色")
    ]
    
    for theme, description in themes:
        print(f"\n📋 测试 {description}:")
        print("-" * 40)
        
        visualizer = TreeVisualizer(
            color_theme=theme,
            show_performance=True,
            max_depth=5
        )
        
        tree_output = visualizer.format_tree(
            component, 
            title=f"测试组件树 ({description})"
        )
        
        print(tree_output)
        
        # 显示统计信息
        stats = visualizer.get_stats()
        print(f"\n统计: {stats}")
    
    logger.info("✅ TreeVisualizer测试完成")


def test_performance_monitor():
    """测试性能监控工具"""
    logger.info("🧪 测试PerformanceMonitor...")
    
    component = create_test_component()
    
    # 创建监控器
    monitor = PerformanceMonitor(
        history_size=100,
        collection_interval=0.05,  # 快速采样用于测试
        enable_auto_collection=False  # 手动控制
    )
    
    print("\n📊 性能监控测试:")
    print("-" * 40)
    
    # 手动添加一些测试指标
    monitor.add_metric(MetricType.LAYOUT_TIME, 12.5, component_id=str(id(component)))
    monitor.add_metric(MetricType.COMPONENT_COUNT, 4.0)
    monitor.add_metric(MetricType.MEMORY_USAGE, 256.0)
    
    # 获取当前统计
    current_stats = monitor.get_current_stats()
    print(f"当前统计: {current_stats}")
    
    # 获取性能摘要
    summary = monitor.get_performance_summary()
    print(f"性能摘要: {summary}")
    
    # 测试导出功能
    exported_data = monitor.export_data("dict")
    print(f"导出数据包含 {len(exported_data['metrics'])} 个指标")
    
    logger.info("✅ PerformanceMonitor测试完成")


def test_layout_inspector():
    """测试布局检查器"""
    logger.info("🧪 测试LayoutInspector...")
    
    component = create_test_component()
    
    # 创建检查器
    inspector = LayoutInspector(InspectionLevel.DETAILED)
    
    print("\n🔍 布局检查测试:")
    print("-" * 40)
    
    # 检查单个组件
    layout_info = inspector.inspect_component(component)
    print(f"组件类型: {layout_info.component_type}")
    print(f"子组件数量: {layout_info.children_count}")
    print(f"健康状态: {layout_info.stretchable_valid}")
    print(f"警告数量: {len(layout_info.warnings)}")
    
    if layout_info.warnings:
        print("警告信息:")
        for warning in layout_info.warnings:
            print(f"  • {warning}")
    
    # 生成完整报告
    report = inspector.generate_inspection_report(component)
    summary = report["summary"]
    print(f"\n报告摘要:")
    print(f"  总组件数: {summary['total_components']}")
    print(f"  健康组件: {summary['healthy_components']}")
    print(f"  检查耗时: {summary['inspection_time']:.2f}ms")
    
    # 查找布局问题
    issues = inspector.find_layout_issues(component)
    print(f"\n发现 {len(issues)} 个布局问题")
    
    # 获取优化建议
    suggestions = inspector.get_optimization_suggestions(component)
    print(f"获得 {len(suggestions)} 条优化建议")
    
    logger.info("✅ LayoutInspector测试完成")


def test_export_functionality():
    """测试导出功能"""
    logger.info("🧪 测试导出功能...")
    
    component = create_test_component()
    
    print("\n📄 导出功能测试:")
    print("-" * 40)
    
    # 测试不同格式的导出
    formats = ["json", "txt", "html"]
    
    for format_type in formats:
        try:
            filepath = export_debug_info(
                component, 
                format=format_type,
                filename=f"test_export.{format_type}"
            )
            print(f"✅ {format_type.upper()} 导出成功: {filepath}")
            
            # 检查文件是否存在
            if filepath.exists():
                file_size = filepath.stat().st_size
                print(f"   文件大小: {file_size} bytes")
            else:
                print(f"   ❌ 文件未找到")
                
        except Exception as e:
            print(f"❌ {format_type.upper()} 导出失败: {e}")
    
    logger.info("✅ 导出功能测试完成")


def test_convenience_functions():
    """测试便捷函数"""
    logger.info("🧪 测试便捷函数...")
    
    component = create_test_component()
    
    print("\n🎯 便捷函数测试:")
    print("-" * 40)
    
    # 测试debug_tree
    print("1. debug_tree():")
    tree_output = debug_tree(component)
    print(f"   输出长度: {len(tree_output)} 字符")
    
    # 测试debug_layout  
    print("\n2. debug_layout():")
    layout_data = debug_layout(component)
    print(f"   布局数据: {len(layout_data)} 个属性")
    
    # 测试debug_performance
    print("\n3. debug_performance():")
    perf_data = debug_performance(component)
    print(f"   性能数据: {len(perf_data)} 个指标")
    
    # 测试quick_debug
    print("\n4. quick_debug():")
    print("   (输出较长，这里仅测试调用)")
    try:
        quick_debug(component, export_html=False)
        print("   ✅ quick_debug 执行成功")
    except Exception as e:
        print(f"   ❌ quick_debug 失败: {e}")
    
    logger.info("✅ 便捷函数测试完成")


def main():
    """主测试函数"""
    logger.info("🚀 开始测试 hibiki.ui.debug 调试工具模块")
    print("🧪 Hibiki UI Debug Tools 测试")
    print("=" * 60)
    
    try:
        # 运行各项测试
        test_tree_visualizer()
        test_performance_monitor() 
        test_layout_inspector()
        test_export_functionality()
        test_convenience_functions()
        
        print("\n🎉 所有调试工具测试完成!")
        print("调试工具模块已就绪，可以在 Hibiki UI 应用中使用。")
        
    except Exception as e:
        logger.error(f"测试执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())