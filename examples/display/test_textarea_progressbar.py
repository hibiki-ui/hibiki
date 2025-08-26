#!/usr/bin/env python3
"""
测试 TextArea 和 ProgressBar 组件
"""

import sys
import os
import time
import threading

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from macui import Signal, set_log_level
from macui.components import TextArea, ProgressBar, VStack, Button, Label
from macui.app import MacUIApp

# 设置日志
set_log_level("INFO")

class TextAreaProgressTestApp:
    """TextArea 和 ProgressBar 测试应用"""
    
    def __init__(self):
        # 文本区域信号
        self.text_content = Signal("这是一个多行文本区域...\n\n在这里输入更多内容试试！\n支持滚动和自动换行。")
        self.text_info = Signal("")
        
        # 进度条信号
        self.progress_value = Signal(30.0)
        self.progress_info = Signal("静态进度条: 30%")
        
        # 控制信号
        self.is_loading = Signal(False)
        
    def on_text_change(self, text):
        lines = len(text.split('\n'))
        chars = len(text)
        words = len(text.split())
        self.text_info.value = f"文本统计: {lines} 行, {words} 词, {chars} 字符"
        
    def simulate_progress(self):
        """模拟进度更新"""
        def update_progress():
            for i in range(101):
                if not self.is_loading.value:
                    break
                self.progress_value.value = float(i)
                self.progress_info.value = f"加载进度: {i}%"
                time.sleep(0.05)  # 50ms 间隔
            
            if self.is_loading.value:
                self.is_loading.value = False
                self.progress_info.value = "加载完成！"
        
        if not self.is_loading.value:
            self.is_loading.value = True
            self.progress_value.value = 0.0
            self.progress_info.value = "开始加载..."
            threading.Thread(target=update_progress, daemon=True).start()
        else:
            self.is_loading.value = False
            self.progress_info.value = "已取消加载"
            
    def reset_progress(self):
        self.progress_value.value = 30.0
        self.progress_info.value = "静态进度条: 30%"
        self.is_loading.value = False
        
    def clear_text(self):
        self.text_content.value = ""
        self.text_info.value = "文本已清空"
        
    def load_sample_text(self):
        sample_text = """# macUI 组件库

这是一个基于 PyObjC 的 macOS 原生 UI 组件库。

## 特性

- 响应式编程模型
- 双向数据绑定
- 现代化的 Python API
- 完整的 macOS 原生支持

## 组件

### 文本控件
- TextField: 单行文本输入
- TextArea: 多行文本区域
- Label: 文本标签

### 输入控件  
- Button: 按钮
- Slider: 滑块
- Switch: 开关

### 显示控件
- ProgressBar: 进度条
- ImageView: 图像视图

### 布局容器
- VStack: 垂直堆叠
- HStack: 水平堆叠
- ScrollView: 滚动容器

这个文本区域支持滚动、自动换行，并且可以与 Signal 进行双向绑定！

试试编辑这段文本，看看下面的统计信息如何实时更新。"""
        
        self.text_content.value = sample_text
        self.text_info.value = "已加载示例文本"

def main():
    print("=== TextArea 和 ProgressBar 组件测试 ===")
    
    app = MacUIApp("TextArea & ProgressBar Test")
    test_app = TextAreaProgressTestApp()
    
    # 创建测试窗口内容
    def create_content():
        from macui import Component
        
        class TestComponent(Component):
            def mount(self):
                return VStack(spacing=15, padding=20, children=[
                    Label("TextArea 和 ProgressBar 组件测试", frame=(0, 0, 500, 30)),
                    
                    # TextArea 测试区域
                    Label("1. 多行文本区域 (TextArea):"),
                    TextArea(
                        value=test_app.text_content,
                        on_change=test_app.on_text_change,
                        tooltip="支持多行文本编辑和滚动",
                        frame=(0, 0, 450, 150)
                    ),
                    
                    # 文本统计信息
                    Label(test_app.text_info),
                    
                    # TextArea 控制按钮
                    VStack(spacing=5, children=[
                        Button("加载示例文本", on_click=test_app.load_sample_text),
                        Button("清空文本", on_click=test_app.clear_text),
                    ]),
                    
                    # ProgressBar 测试区域
                    Label("2. 进度条 (ProgressBar):"),
                    
                    # 静态进度条
                    Label("静态进度条:"),
                    ProgressBar(
                        value=test_app.progress_value,
                        min_value=0.0,
                        max_value=100.0,
                        tooltip="可控制的进度条",
                        frame=(0, 0, 400, 20)
                    ),
                    
                    # 不确定进度条
                    Label("不确定进度条 (旋转动画):"),
                    ProgressBar(
                        indeterminate=True,
                        tooltip="不确定进度的旋转动画",
                        frame=(0, 0, 32, 32)
                    ),
                    
                    # 进度信息
                    Label(test_app.progress_info),
                    
                    # ProgressBar 控制按钮
                    VStack(spacing=5, children=[
                        Button(
                            lambda: "停止加载" if test_app.is_loading.value else "模拟加载进度", 
                            on_click=test_app.simulate_progress
                        ),
                        Button("重置进度", on_click=test_app.reset_progress),
                    ]),
                    
                    # 实时显示当前值
                    Label(lambda: f"文本长度: {len(test_app.text_content.value)} 字符"),
                    Label(lambda: f"进度值: {test_app.progress_value.value:.1f}%"),
                ])
        
        return TestComponent()
    
    # 创建窗口
    window = app.create_window(
        title="TextArea & ProgressBar Test",
        size=(550, 700),
        content=create_content()
    )
    
    # 显示窗口
    window.show()
    
    print("✅ 测试窗口已显示")
    print("📝 测试功能:")
    print("   - TextArea: 多行文本编辑和滚动")
    print("   - TextArea: 双向数据绑定")
    print("   - TextArea: 实时文本统计")
    print("   - ProgressBar: 静态进度显示")
    print("   - ProgressBar: 动态进度更新")
    print("   - ProgressBar: 不确定进度动画")
    print("   - 响应式UI更新")
    
    # 运行应用
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()