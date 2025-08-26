#!/usr/bin/env python3
"""
高级崩溃调试器 - 使用多种方法调试原生崩溃
"""

import sys
import os
import faulthandler
import signal
import traceback
import logging
import objc

# 启用详细的错误报告
faulthandler.enable()

# 设置 PyObjC 选项
objc.options.verbose = True
objc.options.use_kvo = False  # 禁用 KVO 来减少复杂性

# 添加路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def setup_comprehensive_logging():
    """设置全面的日志记录"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('/tmp/macui_crash_debug.log')
        ]
    )
    
    # PyObjC 专用日志
    objc_logger = logging.getLogger('objc')
    objc_logger.setLevel(logging.DEBUG)
    
    print("✅ 全面日志记录已设置")

def install_signal_handlers():
    """安装信号处理器捕获各种崩溃"""
    def crash_handler(signum, frame):
        print(f"\n💥 收到致命信号 {signum}")
        
        # 输出详细的崩溃信息
        print("📍 Python 调用栈:")
        traceback.print_stack(frame)
        
        print("\n📍 faulthandler 调用栈:")
        faulthandler.dump_traceback()
        
        # 尝试输出 PyObjC 相关信息
        try:
            print(f"\n📍 当前 PyObjC 对象数量: {len(objc._objc._global_objects)}")
        except:
            print("无法获取 PyObjC 对象信息")
        
        sys.exit(1)
    
    # 注册多个信号
    signals_to_catch = [signal.SIGTRAP, signal.SIGSEGV, signal.SIGABRT, signal.SIGILL]
    for sig in signals_to_catch:
        signal.signal(sig, crash_handler)
    
    print(f"✅ 信号处理器已安装: {[sig.name for sig in signals_to_catch]}")

def create_minimal_crash_test():
    """创建最小化的崩溃重现测试"""
    print("=== 创建最小化崩溃重现测试 ===")
    
    from macui.app import MacUIApp
    from AppKit import NSScrollView, NSTableView, NSTableColumn
    from macui.core.binding import EnhancedTableViewDataSource
    
    app = MacUIApp("Minimal Crash Test")
    
    # 创建最简单的表格设置
    print("1. 创建 NSScrollView...")
    from Foundation import NSMakeRect
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setFrame_(NSMakeRect(0, 0, 300, 200))
    
    print("2. 创建 NSTableView...")
    table_view = NSTableView.alloc().init()
    
    print("3. 创建单个列...")
    column = NSTableColumn.alloc().init()
    column.setIdentifier_("test_column")
    column.setWidth_(200)
    table_view.addTableColumn_(column)
    
    print("4. 设置文档视图...")
    scroll_view.setDocumentView_(table_view)
    
    print("5. 创建数据源...")
    data_source = EnhancedTableViewDataSource.alloc().init()
    
    # 使用最简单的测试数据
    test_data = [
        {"test_column": "Row 1"},
        {"test_column": "Row 2"},
        {"test_column": "Row 3"}
    ]
    data_source.data = test_data
    data_source.columns = ["test_column"]
    
    print("6. 设置数据源到表格...")
    table_view.setDataSource_(data_source)
    
    print("7. 手动测试数据源方法...")
    try:
        # 手动调用数据源方法来检测问题
        row_count = data_source.numberOfRowsInTableView_(table_view)
        print(f"   行数: {row_count}")
        
        for row in range(row_count):
            for col_idx, column in enumerate(table_view.tableColumns()):
                try:
                    value = data_source.tableView_objectValueForTableColumn_row_(table_view, column, row)
                    print(f"   [{row}, {col_idx}] = '{value}' (type: {type(value)})")
                except Exception as e:
                    print(f"   ❌ [{row}, {col_idx}] 调用失败: {e}")
                    traceback.print_exc()
    
    except Exception as e:
        print(f"❌ 手动测试失败: {e}")
        traceback.print_exc()
        return None
    
    return app, scroll_view, table_view, data_source

def test_table_rendering():
    """测试表格渲染过程"""
    print("\n=== 测试表格渲染过程 ===")
    
    try:
        components = create_minimal_crash_test()
        if not components:
            return False
        
        app, scroll_view, table_view, data_source = components
        
        print("8. 创建简单窗口...")
        from macui.core.component import Component
        from AppKit import NSView
        
        class MinimalContainer(Component):
            def mount(self):
                from Foundation import NSMakeRect
                container = NSView.alloc().init()
                container.setFrame_(NSMakeRect(0, 0, 400, 300))
                container.addSubview_(scroll_view)
                return container
        
        window = app.create_window(
            title="Crash Test",
            size=(400, 300),
            content=MinimalContainer()
        )
        
        print("9. 显示窗口...")
        window.show()
        
        print("10. 强制表格重新加载...")
        table_view.reloadData()
        
        print("11. 等待渲染...")
        import time
        time.sleep(1)
        
        print("12. 再次重新加载...")
        table_view.reloadData()
        time.sleep(0.5)
        
        print("✅ 测试完成，没有崩溃")
        return True
        
    except Exception as e:
        print(f"❌ 渲染测试失败: {e}")
        traceback.print_exc()
        return False

def run_comprehensive_crash_debug():
    """运行全面的崩溃调试"""
    print("=== 高级崩溃调试器启动 ===")
    
    # 设置调试环境
    setup_comprehensive_logging()
    install_signal_handlers()
    
    print(f"Python 版本: {sys.version}")
    print(f"PyObjC 版本: {objc.__version__ if hasattr(objc, '__version__') else 'Unknown'}")
    
    # 运行测试
    success = test_table_rendering()
    
    if success:
        print("\n🎉 所有测试通过！应用运行稳定")
        
        # 运行额外的压力测试
        print("\n=== 运行压力测试 ===")
        for i in range(5):
            print(f"压力测试循环 {i+1}/5...")
            success = test_table_rendering()
            if not success:
                print(f"💥 压力测试在第 {i+1} 次失败")
                break
            import time
            time.sleep(0.5)
        
        if success:
            print("✅ 压力测试也通过了！")
    
    return success

# 额外的调试方法

def enable_objc_exception_logging():
    """启用 Objective-C 异常日志记录"""
    try:
        from Foundation import NSSetUncaughtExceptionHandler
        
        def exception_handler(exception):
            print(f"💥 未捕获的 Objective-C 异常: {exception}")
            print(f"原因: {exception.reason()}")
            print(f"用户信息: {exception.userInfo()}")
            traceback.print_stack()
        
        NSSetUncaughtExceptionHandler(exception_handler)
        print("✅ Objective-C 异常处理器已设置")
    except Exception as e:
        print(f"⚠️ 无法设置 Objective-C 异常处理器: {e}")

def analyze_memory_usage():
    """分析内存使用情况"""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        print(f"📊 内存使用: RSS={memory_info.rss/1024/1024:.1f}MB, VMS={memory_info.vms/1024/1024:.1f}MB")
    except ImportError:
        print("⚠️ 需要 psutil 来分析内存使用")

if __name__ == "__main__":
    enable_objc_exception_logging()
    success = run_comprehensive_crash_debug()
    analyze_memory_usage()
    
    if success:
        print("\n🎯 结论: 应用运行稳定，没有发现崩溃问题")
    else:
        print("\n💥 结论: 发现了崩溃问题，需要进一步调试")