"""
朋友圈UI示例

这是一个模仿微信朋友圈界面的高级UI示例，展示了Hibiki UI框架的强大功能：
- 复杂组件组合
- 响应式布局
- 信号驱动的交互
- 动态数据渲染

主要文件：
- models.py: 数据模型和Mock数据生成
- components.py: UI组件实现
- friends_circle.py: 主程序入口
"""

from .models import User, Post, Comment, MockDataGenerator, format_relative_time, calculate_image_layout

__all__ = [
    "User", 
    "Post", 
    "Comment", 
    "MockDataGenerator",
    "format_relative_time",
    "calculate_image_layout"
]