#!/usr/bin/env python3
"""
🌟 Hibiki UI 高级示例：朋友圈界面

这是一个完整的朋友圈UI实现，展示了Hibiki UI框架的强大功能：
- 复杂组件层次和交互
- 信号驱动的响应式UI更新
- 智能布局系统（CSS Grid + Flexbox）
- 动态数据渲染和状态管理

设计特色：
📱 完整朋友圈体验
🔄 响应式交互（点赞、评论）
🖼️ 智能图片网格布局
⏰ 动态时间显示
🎨 现代化UI设计
"""

from typing import List
from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container,
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems,
    px, percent,
    ManagerFactory
)
# 直接从布局组件模块导入ScrollableContainer
from hibiki.ui.components.layout import ScrollableContainer
# 导入调试工具
from hibiki.ui.debug import debug_component_tree, debug_component_layout, quick_debug
from hibiki.ui.utils import debug_view_layout
import time

# 导入朋友圈相关组件和数据
try:
    from .models import User, Post, MockDataGenerator
    from .components import FriendsCircleHeader, PostCard
except ImportError:
    # 处理直接运行脚本时的导入问题
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from models import User, Post, MockDataGenerator
    from components import FriendsCircleHeader, PostCard


class FriendsCircleApp:
    """朋友圈主应用类"""
    
    def __init__(self):
        # 应用状态管理
        self.current_user = MockDataGenerator.get_current_user()
        self.posts = Signal(MockDataGenerator.generate_posts(25))  # 增加到25条确保需要滚动
        
        # 创建应用UI
        self.setup_ui()
        
        # 设置交互处理
        self.setup_interactions()
    
    def setup_ui(self):
        """构建主UI界面"""
        # 创建顶部个人信息区域
        self.header = FriendsCircleHeader(self.current_user)
        
        # 创建动态列表
        self.posts_container = self.create_posts_list()
        
        # 创建内容容器（动态高度，由ScrollableContainer自动计算）
        content_container = Container(
            children=[self.header, self.posts_container],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                width=percent(100),  # 确保内容容器有明确宽度
                # 移除固定min_height，让ScrollableContainer动态计算内容高度
                background_color="#f5f5f5",
                padding=px(20)  # 添加内边距
            )
        )
        
        # 使用ScrollableContainer包装内容
        self.scroll_container = ScrollableContainer(
            children=[content_container],
            scroll_vertical=True,
            scroll_horizontal=False,
            show_scrollbars=True,
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                background_color="#ffffff"
            )
        )
        
        # 主容器
        self.main_container = Container(
            children=[self.scroll_container],
            style=ComponentStyle(
                width=percent(100),
                height=percent(100),
                max_width=px(480),  # 限制最大宽度，模拟手机界面
                # 居中显示通过父容器的布局实现
                background_color="white",
                border_color="#e0e0e0",
                border_width=px(1)
            )
        )
    
    def create_posts_list(self) -> Container:
        """创建动态列表容器"""
        # 使用Computed动态生成帖子卡片
        post_cards_computed = Computed(lambda: [
            PostCard(
                post, 
                on_like=self.handle_post_like,
                on_comment=self.handle_post_comment
            ) 
            for post in self.posts.value
        ])
        
        # 创建帖子列表容器
        posts_list = Container(
            children=[],  # 初始为空，通过Effect动态更新
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                width=percent(100),
                background_color="white",
                padding=px(10)  # 添加内边距
                # 移除固定min_height，让容器根据实际内容自适应高度
            )
        )
        
        # 使用Effect响应式更新帖子列表
        def update_posts_list():
            # 获取最新的帖子卡片
            new_cards = post_cards_computed.value
            # 清空现有子组件
            posts_list.children.clear()
            # 添加新的卡片组件
            posts_list.children.extend(new_cards)
            # 触发重新渲染
            if hasattr(posts_list, '_nsview') and posts_list._nsview:
                posts_list._update_children()
        
        # 创建响应式Effect
        Effect(update_posts_list)
        
        return posts_list
    
    def setup_interactions(self):
        """设置交互处理逻辑"""
        # 这里可以添加全局的交互处理逻辑
        # 比如定时更新时间显示、处理网络请求等
        pass
    
    def handle_post_like(self, post: Post, is_liked: bool):
        """处理帖子点赞/取消点赞"""
        print(f"{'点赞' if is_liked else '取消点赞'}动态: {post.content[:20]}...")
        
        # 实际应用中这里应该：
        # 1. 发送网络请求到服务器
        # 2. 更新本地数据
        # 3. 通过Signal触发UI更新
        
        # 这里简单模拟数据更新
        current_posts = self.posts.value.copy()
        for i, p in enumerate(current_posts):
            if p.id == post.id:
                # 更新点赞列表
                if is_liked and not any(like.id == self.current_user.id for like in p.likes):
                    current_posts[i].likes.append(self.current_user)
                elif not is_liked:
                    current_posts[i].likes = [
                        like for like in p.likes 
                        if like.id != self.current_user.id
                    ]
                break
        
        # 触发数据更新
        self.posts.value = current_posts
    
    def handle_post_comment(self, post: Post):
        """处理帖子评论"""
        print(f"评论动态: {post.content[:20]}...")
        
        # 实际应用中这里应该：
        # 1. 弹出评论输入框
        # 2. 处理用户输入
        # 3. 发送评论到服务器
        # 4. 更新本地数据和UI
        
        # 这里简单打印日志
        pass
    
    def refresh_posts(self):
        """刷新动态列表（模拟下拉刷新）"""
        print("刷新动态列表...")
        new_posts = MockDataGenerator.generate_posts(12)
        self.posts.value = new_posts
    
    def load_more_posts(self):
        """加载更多动态（模拟上拉加载）"""
        print("加载更多动态...")
        more_posts = MockDataGenerator.generate_posts(6)
        current_posts = self.posts.value.copy()
        current_posts.extend(more_posts)
        self.posts.value = current_posts
    
    def get_main_component(self) -> Container:
        """获取主组件，供外部使用"""
        return self.main_container


def create_friends_circle_app():
    """创建朋友圈应用的标准入口函数"""
    # 创建应用管理器
    app_manager = ManagerFactory.get_app_manager()
    
    # 创建窗口
    window = app_manager.create_window(
        title="朋友圈 - Hibiki UI 高级示例",
        width=500,
        height=800
    )
    
    # 创建朋友圈应用实例
    friends_circle = FriendsCircleApp()
    
    # 设置窗口内容
    window.set_content(friends_circle.get_main_component())
    
    # 添加一些快捷键支持（可选）
    def handle_key_events():
        # R键 - 刷新
        # L键 - 加载更多
        # 这里可以添加键盘快捷键处理
        pass
    
    
    # 返回应用实例，便于外部控制
    return friends_circle


# 直接运行支持
def main():
    """直接运行朋友圈应用"""
    try:
        # 创建朋友圈应用
        app = create_friends_circle_app()
        
        # 获取应用管理器并运行
        app_manager = ManagerFactory.get_app_manager()
        
        # 运行应用事件循环
        app_manager.run()
        
    except Exception as e:
        print(f"❌ 应用运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()