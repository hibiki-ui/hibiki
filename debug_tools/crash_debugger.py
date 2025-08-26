#!/usr/bin/env python3
"""
崩溃调试器 - 专门用于调试 PyObjC 桥接问题
"""

import sys
import os
import faulthandler
import signal
import traceback
import objc

# 启用 Python 错误处理器
faulthandler.enable()

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def enable_objc_debugging():
    """启用 PyObjC 调试"""
    # 启用 PyObjC 异常详细信息
    objc.setVerbose(True)
    
    # 启用方法调用跟踪
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    print("✅ PyObjC 调试已启用")

def setup_crash_handler():
    """设置崩溃处理器"""
    def crash_handler(signum, frame):
        print(f"\n💥 收到信号 {signum}")
        print("📍 崩溃时的调用栈:")
        faulthandler.dump_traceback()
        
        # 打印 Python 调用栈
        print("\n📍 Python 调用栈:")
        traceback.print_stack(frame)
        
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGTRAP, crash_handler)
    signal.signal(signal.SIGSEGV, crash_handler)
    signal.signal(signal.SIGABRT, crash_handler)
    
    print("✅ 崩溃处理器已设置")

def create_safe_table_view_test():
    """创建安全的表格视图测试"""
    print("=== 创建安全的表格视图测试 ===")
    
    from macui import Signal
    from macui.app import MacUIApp
    from AppKit import NSScrollView, NSTableView, NSTableColumn
    from macui.core.binding import EnhancedTableViewDataSource
    
    # 创建应用
    app = MacUIApp("Crash Debug Test")
    
    # 创建测试数据
    test_data = [
        {"name": "Test1", "age": "20"},
        {"name": "Test2", "age": "30"},
    ]
    
    print("创建表格视图组件...")
    
    # 手动创建组件来更好地控制
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)  # 简化测试
    
    table_view = NSTableView.alloc().init()
    
    # 创建列 - 简化到只有一列
    column = NSTableColumn.alloc().init()
    column.setIdentifier_("name")
    column.setWidth_(200)
    column.headerCell().setStringValue_("姓名")
    table_view.addTableColumn_(column)
    
    scroll_view.setDocumentView_(table_view)
    
    # 创建数据源 - 加强错误处理
    print("创建安全的数据源...")
    
    class SafeTableViewDataSource(EnhancedTableViewDataSource):
        """安全的表格数据源 - 增强错误处理"""
        
        def numberOfRowsInTableView_(self, table_view):
            try:
                count = len(self.data) if self.data else 0
                print(f"📊 numberOfRowsInTableView: {count}")
                return count
            except Exception as e:
                print(f"❌ numberOfRowsInTableView 错误: {e}")
                return 0
        
        def tableView_objectValueForTableColumn_row_(self, table_view, column, row):
            try:
                print(f"📊 tableView_objectValueForTableColumn_row: column={column.identifier()}, row={row}")
                
                # 检查数据有效性
                if not self.data:
                    print("⚠️  数据为空")
                    return ""
                
                if row < 0 or row >= len(self.data):
                    print(f"⚠️  行索引超出范围: {row} >= {len(self.data)}")
                    return ""
                
                row_data = self.data[row]
                column_id = column.identifier()
                
                if not isinstance(row_data, dict):
                    print(f"⚠️  行数据不是字典: {type(row_data)}")
                    return str(row_data)
                
                value = row_data.get(column_id, "")
                
                # 确保返回的是字符串
                if value is None:
                    value = ""
                elif not isinstance(value, str):
                    value = str(value)
                
                print(f"✅ 返回值: '{value}'")
                return value
                
            except Exception as e:
                print(f"❌ tableView_objectValueForTableColumn_row 严重错误: {e}")
                traceback.print_exc()
                return ""  # 返回安全的默认值
    
    # 设置数据源
    data_source = SafeTableViewDataSource.alloc().init()
    data_source.data = test_data
    data_source.columns = ["name"]
    
    print("设置数据源到表格视图...")
    table_view.setDataSource_(data_source)
    
    # 强制保持数据源引用
    scroll_view._debug_data_source = data_source  # 简单的引用保持
    
    print("创建窗口...")
    
    # 创建简单的内容组件
    from macui.core.component import Component
    from macui.components.basic import VStack, Label
    
    class DebugComponent(Component):
        def mount(self):
            container = VStack(spacing=10, padding=20, children=[
                Label("崩溃调试测试"),
                scroll_view,  # 直接使用 NSScrollView
            ])
            return container.mount()
    
    # 创建窗口
    window = app.create_window(
        title="Crash Debug Test",
        size=(400, 300),
        content=DebugComponent()
    )
    
    return app, window, data_source

def run_crash_debug_test():
    """运行崩溃调试测试"""
    print("=== 启动崩溃调试测试 ===")
    
    # 设置调试环境
    enable_objc_debugging()
    setup_crash_handler()
    
    try:
        print("步骤 1: 创建测试组件")
        app, window, data_source = create_safe_table_view_test()
        
        print("步骤 2: 显示窗口")
        window.show()
        
        print("步骤 3: 手动触发表格渲染")
        # 强制触发重绘来重现崩溃
        scroll_view = window._window_instance.contentView().subviews()[0].subviews()[1]
        table_view = scroll_view.documentView()
        
        print("步骤 4: 验证数据源")
        print(f"数据源对象: {data_source}")
        print(f"数据源数据: {data_source.data}")
        
        print("步骤 5: 手动调用数据源方法")
        row_count = data_source.numberOfRowsInTableView_(table_view)
        print(f"行数: {row_count}")
        
        if row_count > 0:
            column = table_view.tableColumns()[0]
            value = data_source.tableView_objectValueForTableColumn_row_(table_view, column, 0)
            print(f"第一行值: '{value}'")
        
        print("步骤 6: 触发表格重新加载")
        table_view.reloadData()
        
        print("✅ 测试组件创建成功，等待用户交互...")
        
        # 运行一小段时间看是否崩溃
        import time
        for i in range(10):
            time.sleep(0.5)
            print(f"运行中... {i+1}/10")
            
            # 每次都重新加载数据来触发渲染
            if i % 2 == 0:
                table_view.reloadData()
        
        print("🎉 测试通过！没有崩溃")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== PyObjC 崩溃调试器 ===")
    success = run_crash_debug_test()
    
    if success:
        print("✅ 调试测试成功完成")
    else:
        print("💥 调试测试发现问题")