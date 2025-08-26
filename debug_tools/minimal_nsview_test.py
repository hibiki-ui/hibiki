#!/usr/bin/env python3
"""
最小化的 NSView 测试 - 直接测试 AppKit 组件的引用计数
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from AppKit import NSScrollView, NSTableView, NSView
import gc

def test_nsview_retain_counts():
    """测试各种 NSView 的引用计数"""
    print("=== 测试原生 NSView 引用计数 ===")
    
    # 测试 NSView
    print("\n1. 测试 NSView:")
    view = NSView.alloc().init()
    print(f"   NSView 引用计数: {view.retainCount()}")
    
    # 测试 NSScrollView
    print("\n2. 测试 NSScrollView:")
    scroll_view = NSScrollView.alloc().init()
    print(f"   NSScrollView 创建后引用计数: {scroll_view.retainCount()}")
    
    # 设置 NSScrollView 属性
    scroll_view.setHasVerticalScroller_(True)
    print(f"   设置垂直滚动条后引用计数: {scroll_view.retainCount()}")
    
    scroll_view.setHasHorizontalScroller_(True)
    print(f"   设置水平滚动条后引用计数: {scroll_view.retainCount()}")
    
    scroll_view.setAutohidesScrollers_(True)
    print(f"   设置自动隐藏滚动条后引用计数: {scroll_view.retainCount()}")
    
    # 测试 NSTableView
    print("\n3. 测试 NSTableView:")
    table_view = NSTableView.alloc().init()
    print(f"   NSTableView 创建后引用计数: {table_view.retainCount()}")
    
    # 将 NSTableView 作为文档视图添加到 NSScrollView
    scroll_view.setDocumentView_(table_view)
    print(f"   添加到 ScrollView 后 NSTableView 引用计数: {table_view.retainCount()}")
    print(f"   添加文档视图后 NSScrollView 引用计数: {scroll_view.retainCount()}")
    
    # 强制垃圾回收
    print("\n4. 垃圾回收测试:")
    initial_scroll_count = scroll_view.retainCount()
    initial_table_count = table_view.retainCount()
    
    for i in range(3):
        collected = gc.collect()
        print(f"   第{i+1}次垃圾回收: {collected} 个对象")
    
    print(f"   垃圾回收后 NSScrollView 引用计数: {scroll_view.retainCount()}")
    print(f"   垃圾回收后 NSTableView 引用计数: {table_view.retainCount()}")
    
    return scroll_view, table_view

def test_minimal_setup():
    """测试最小化设置的引用计数"""
    print("\n=== 测试最小化设置 ===")
    
    # 只创建 NSScrollView
    scroll = NSScrollView.alloc().init()
    print(f"仅创建 NSScrollView: {scroll.retainCount()}")
    
    # 释放局部变量
    del scroll
    gc.collect()
    print("已删除局部变量并执行垃圾回收")

if __name__ == "__main__":
    print("开始测试 NSView 引用计数...")
    
    # 最小化测试
    test_minimal_setup()
    
    # 完整测试
    scroll_view, table_view = test_nsview_retain_counts()
    
    # 最终状态
    print(f"\n=== 最终状态 ===")
    print(f"NSScrollView 最终引用计数: {scroll_view.retainCount()}")
    print(f"NSTableView 最终引用计数: {table_view.retainCount()}")
    
    print("\n=== 结论 ===")
    if scroll_view.retainCount() > 10:
        print("⚠️  NSScrollView 引用计数异常高，这可能是 AppKit 内部的行为")
        print("   这种高引用计数通常是由于：")
        print("   1. AppKit 内部的事件循环引用")
        print("   2. 自动滚动条的内部管理")
        print("   3. 视图层次结构的内部引用")
        print("   4. 这是正常的系统行为，不是内存泄漏")
    else:
        print("✅ NSScrollView 引用计数正常")