"""
朋友圈UI核心组件实现

包含用户头像、动态卡片、图片网格等核心组件，
展示Hibiki UI框架的复杂布局和交互能力。
"""

from typing import List, Callable, Optional
from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container,
    ComponentStyle, Display, FlexDirection, JustifyContent, AlignItems,
    px, percent
)
try:
    from .models import User, Post, Comment, format_relative_time, calculate_image_layout
except ImportError:
    from models import User, Post, Comment, format_relative_time, calculate_image_layout


def UserAvatar(user: User, size: int = 40) -> Container:
    """圆形用户头像组件"""
    
    # 头像容器样式
    style = ComponentStyle(
        width=px(size),
        height=px(size),
        border_radius=px(size // 2),  # 圆形
        background_color="#e0e0e0",  # 更明显的背景色
        display=Display.FLEX,
        justify_content=JustifyContent.CENTER,
        align_items=AlignItems.CENTER,
        font_size=size // 2,  # emoji大小与头像成比例
        overflow="hidden",
        flex_shrink=0  # 防止头像被压缩
    )
    
    # 头像内容（emoji或文字）
    avatar_label = Label(
        user.avatar_url,
        style=ComponentStyle(
            font_size=size // 2,
            line_height=1.0
        )
    )
    
    # 组装组件
    return Container(
        children=[avatar_label],
        style=style
    )


def ImageGrid(images: List[str], max_width: int = 300) -> Container:
    """智能图片网格布局组件"""
    
    # 如果没有图片，返回空容器
    if not images:
        return Container(children=[], style=ComponentStyle(height=px(0)))
    
    # 计算布局参数
    layout = calculate_image_layout(len(images))
    
    # 根据图片数量创建网格样式
    grid_style = _create_grid_style(layout, max_width)
    
    # 创建图片项
    image_items = []
    for i, image in enumerate(images):
        image_item = _create_image_item(image, layout["max_width"])
        image_items.append(image_item)
    
    return Container(
        children=image_items,
        style=grid_style
    )

def _create_grid_style(layout: dict, max_width: int) -> ComponentStyle:
    """创建网格容器样式"""
    cols = layout["columns"]
    
    if cols == 0:
        return ComponentStyle(height=px(0))
    
    # 根据布局参数计算实际需要的容器宽度
    item_width = layout["max_width"]  # 单个图片项的宽度
    gap_size = 4  # 间距
    
    # 实际容器宽度 = 列数 * 图片宽度 + (列数-1) * 间距
    actual_width = cols * item_width + (cols - 1) * gap_size
    
    # 使用CSS Grid实现精确布局
    grid_template_columns = " ".join(["1fr"] * cols)
    
    return ComponentStyle(
        display=Display.GRID,
        grid_template_columns=grid_template_columns,
        gap=px(gap_size),
        width=px(actual_width),  # 使用计算出的实际宽度
        max_width=px(actual_width)
    )

def _create_image_item(image: str, item_size: int) -> Container:
    """创建单个图片项"""
    # 使用emoji作为图片占位符
    image_label = Label(
        image,
        style=ComponentStyle(
            font_size=item_size // 3,
            text_align="center",
            line_height=1.0
        )
    )
    
    # 图片容器
    return Container(
        children=[image_label],
        style=ComponentStyle(
            width=px(item_size),
            height=px(item_size),
            background_color="#f8f8f8",
            border_radius=px(8),
            display=Display.FLEX,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER,
            border_color="#e0e0e0",
            border_width=px(1)
        )
    )


def InteractionBar(is_liked: Signal[bool], 
                 on_like: Callable = None,
                 on_comment: Callable = None) -> Container:
    """交互栏组件 - 包含点赞和评论按钮"""
    
    on_like = on_like or (lambda: None)
    on_comment = on_comment or (lambda: None)
    
    # 点赞按钮
    like_button = Button(
        "❤️" if is_liked.value else "🤍",
        on_click=lambda: on_like(),
        style=ComponentStyle(
            background_color="transparent",
            border_width=px(0),
            font_size=14,
            padding=px(4),
            border_radius=px(4)
        )
    )
    
    # 评论按钮
    comment_button = Button(
        "💬 评论",
        on_click=lambda: on_comment(),
        style=ComponentStyle(
            background_color="transparent",
            border_width=px(0),
            color="#666",
            font_size=12,
            padding=px(4)
        )
    )
    
    # 交互栏容器
    return Container(
        children=[like_button, comment_button],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            gap=px(12),
            margin_top=px(8),
            margin_bottom=px(8)
        )
    )


def LikesList(likes: List[User]) -> Container:
    """点赞用户列表组件"""
    
    if not likes:
        return Container(children=[], style=ComponentStyle(height=px(0)))
    
    # 创建点赞文本
    like_names = [user.name for user in likes[:10]]  # 最多显示10个
    
    if len(likes) > 10:
        like_text = f"❤️ {', '.join(like_names[:9])}等{len(likes)}人点赞"
    else:
        like_text = f"❤️ {', '.join(like_names)}"
    
    # 点赞列表标签
    likes_label = Label(
        like_text,
        style=ComponentStyle(
            color="#576b95",  # 微信蓝色
            font_size=13,
            background_color="#f7f7f7",
            padding=px(8),
            border_radius=px(4),
            margin_bottom=px(8),
            min_width=px(100),  # 确保有最小宽度
            min_height=px(25)   # 确保有最小高度
        )
    )
    
    return Container(
        children=[likes_label],
        style=ComponentStyle(width=percent(100))
    )


def CommentItem(comment: Comment) -> Container:
    """单条评论组件"""
    
    # 评论者姓名
    name_label = Label(
        f"{comment.user.name}:",
        style=ComponentStyle(
            color="#576b95",
            font_size=14,   # 增大字体
            font_weight="bold",
            margin_right=px(4),
            min_width=px(60),   # 确保有最小宽度
            min_height=px(18)   # 确保有最小高度
        )
    )
    
    # 评论内容
    content_label = Label(
        comment.content,
        style=ComponentStyle(
            color="black",  # 使用黑色确保可见
            font_size=14,   # 增大字体
            flex_grow=1,
            min_width=px(150),  # 确保有最小宽度
            min_height=px(18)   # 确保有最小高度
        )
    )
    
    # 评论时间
    time_label = Label(
        format_relative_time(comment.timestamp),
        style=ComponentStyle(
            color="#666",   # 稍微深一点的灰色
            font_size=12,   # 增大字体
            margin_left=px(8)
        )
    )
    
    # 评论容器
    return Container(
        children=[name_label, content_label, time_label],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=AlignItems.FLEX_START,
            margin_bottom=px(4),
            padding=px(4),
            background_color="#f7f7f7",
            border_radius=px(4)
        )
    )


def CommentsList(comments: List[Comment]) -> Container:
    """评论列表组件"""
    
    if not comments:
        return Container(children=[], style=ComponentStyle(height=px(0)))
    
    # 创建评论项列表
    comment_items = []
    for comment in comments:
        comment_item = CommentItem(comment)
        comment_items.append(comment_item)
    
    # 评论列表容器
    return Container(
        children=comment_items,
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(2),
            margin_top=px(8)
        )
    )


def PostCard(post: Post, on_like: Callable = None, on_comment: Callable = None) -> Container:
    """动态卡片主组件 - 朋友圈单条动态的完整UI"""
    
    # 创建点赞状态Signal（这里简单模拟，实际应用中应该从外部传入）
    current_user_liked = any(like.id == "current_user" for like in post.likes)
    is_liked = Signal(current_user_liked)
    
    # 处理点赞回调
    def handle_like():
        is_liked.value = not is_liked.value
        if on_like:
            on_like(post, is_liked.value)
    
    # 用户头像
    avatar = UserAvatar(post.user, size=48)
    
    # 用户名和时间
    username_label = Label(
        post.user.name,
        style=ComponentStyle(
            color="black",  # 使用黑色确保可见
            font_size=16,   # 增大字体
            font_weight="bold",
            margin_bottom=px(4),
            min_width=px(100),  # 确保有最小宽度
            min_height=px(20)   # 确保有最小高度
        )
    )
    
    time_label = Label(
        format_relative_time(post.timestamp),
        style=ComponentStyle(
            color="#666",   # 稍微深一点的灰色
            font_size=14,   # 增大字体
            margin_left=px(12),
            min_width=px(80),   # 确保有最小宽度
            min_height=px(18)   # 确保有最小高度
        )
    )
    
    # 用户信息行
    user_info = Container(
        children=[username_label, time_label],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=AlignItems.CENTER,
            margin_bottom=px(8)
        )
    )
    
    # 文字内容
    content_label = Label(
        post.content,
        style=ComponentStyle(
            color="black",  # 使用黑色确保可见
            font_size=16,   # 增大字体
            line_height=1.4,
            margin_bottom=px(8),
            min_width=px(250),  # 确保有最小宽度
            min_height=px(20)   # 确保有最小高度
        )
    )
    
    # 图片网格
    image_grid = ImageGrid(post.images, max_width=280)
    
    # 交互栏
    interaction_bar = InteractionBar(
        is_liked,
        on_like=handle_like,
        on_comment=on_comment
    )
    
    # 点赞列表
    likes_list = LikesList(post.likes)
    
    # 评论列表
    comments_list = CommentsList(post.comments)
    
    # 内容区域
    content_children = [user_info, content_label]
    
    if post.images:
        content_children.append(image_grid)
    
    content_children.extend([interaction_bar, likes_list, comments_list])
    
    content_area = Container(
        children=content_children,
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            flex_grow=1,
            width=percent(100)   # 确保宽度
            # 移除固定min_height，让内容自适应高度
        )
    )
    
    # 主容器样式
    card_style = ComponentStyle(
        display=Display.FLEX,
        flex_direction=FlexDirection.ROW,
        padding=px(16),
        border_bottom_color="#f0f0f0",
        border_bottom_width=px(1),
        background_color="white",
        gap=px(12),
        width=percent(100),
        margin_bottom=px(8)  # 添加卡片间距
        # 移除固定min_height，让卡片根据内容自适应高度
    )
    
    # 组装卡片
    return Container(
        children=[avatar, content_area],
        style=card_style
    )


def FriendsCircleHeader(current_user: User) -> Container:
    """朋友圈顶部个人信息区域（简化版）"""
    
    # 用户头像（大尺寸）
    large_avatar = UserAvatar(current_user, size=60)
    
    # 用户名
    username_label = Label(
        current_user.name,
        style=ComponentStyle(
            color="white",
            font_size=18,
            font_weight="bold",
            margin_left=px(12)
        )
    )
    
    # 用户信息区（使用Flex布局）
    user_info = Container(
        children=[large_avatar, username_label],
        style=ComponentStyle(
            display=Display.FLEX,
            flex_direction=FlexDirection.ROW,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.FLEX_END,  # 右对齐
            padding=px(20)
        )
    )
    
    # 头部容器（单一背景色区域）
    return Container(
        children=[user_info],
        style=ComponentStyle(
            height=px(160),
            background_color="#667eea",
            margin_bottom=px(20),
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            justify_content=JustifyContent.FLEX_END  # 内容在底部
        )
    )