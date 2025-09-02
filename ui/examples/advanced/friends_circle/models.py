"""
朋友圈数据模型定义

定义用户、动态、评论等数据结构，并提供Mock数据生成功能。
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import random

@dataclass
class User:
    """用户模型"""
    id: str
    name: str
    avatar_url: str = "🧑‍💻"  # 使用emoji作为默认头像

@dataclass
class Comment:
    """评论模型"""
    id: str
    user: User
    content: str
    timestamp: datetime
    reply_to: Optional[str] = None  # 回复的评论ID
    
@dataclass
class Post:
    """动态/帖子模型"""
    id: str
    user: User
    content: str
    images: List[str]
    timestamp: datetime
    likes: List[User]
    comments: List[Comment]


class MockDataGenerator:
    """Mock数据生成器"""
    
    # 用户池
    MOCK_USERS = [
        User("user1", "张小明", "👨‍💻"),
        User("user2", "李小红", "👩‍🎨"),
        User("user3", "王大伟", "👨‍🔧"),
        User("user4", "陈小美", "👩‍🔬"),
        User("user5", "刘志强", "👨‍🏫"),
        User("user6", "赵小玲", "👩‍⚕️"),
        User("user7", "孙大鹏", "👨‍🚀"),
        User("user8", "周小雨", "👩‍🎤"),
    ]
    
    # 文字内容池
    CONTENT_POOL = [
        "今天天气真不错，心情也很好！☀️",
        "刚刚吃了一顿超级棒的火锅，满足！🔥",
        "工作虽然忙碌，但是很充实。加油！💪",
        "周末的午后阳光，配上一杯咖啡，完美！☕",
        "新学的技能终于掌握了，成就感满满 🎉",
        "和朋友们聚会真开心，友谊万岁！🎊",
        "看了一部很棒的电影，推荐给大家 🎬",
        "今天的运动打卡完成，坚持就是胜利！🏃‍♂️",
        "家里的小花开了，生活真美好 🌸",
        "分享一个今天学到的小知识，很实用哦！📚",
        "晚霞太美了，忍不住多拍几张照片 🌅",
        "美食不能辜负，今天又发现了新店！🍽️"
    ]
    
    # 图片占位符（不同数量的组合）
    IMAGE_COMBINATIONS = [
        [],  # 无图片
        ["📸"],  # 1张图片
        ["📸", "🏞️"],  # 2张图片  
        ["📸", "🏞️", "🌄"],  # 3张图片
        ["📸", "🏞️", "🌄", "🌅"],  # 4张图片
        ["📸", "🏞️", "🌄", "🌅", "🌇"],  # 5张图片
        ["📸", "🏞️", "🌄", "🌅", "🌇", "🏙️"],  # 6张图片
        ["📸", "🏞️", "🌄", "🌅", "🌇", "🏙️", "🌃"],  # 7张图片
        ["📸", "🏞️", "🌄", "🌅", "🌇", "🏙️", "🌃", "🌆"],  # 8张图片
        ["📸", "🏞️", "🌄", "🌅", "🌇", "🏙️", "🌃", "🌆", "🌌"],  # 9张图片
    ]
    
    @classmethod
    def generate_posts(cls, count: int = 10) -> List[Post]:
        """生成指定数量的Mock动态数据"""
        posts = []
        
        for i in range(count):
            # 随机选择用户
            user = random.choice(cls.MOCK_USERS)
            
            # 随机选择内容
            content = random.choice(cls.CONTENT_POOL)
            
            # 随机选择图片数量
            images = random.choice(cls.IMAGE_COMBINATIONS).copy()
            
            # 生成时间戳（最近几天内）
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # 生成点赞用户（随机数量）
            like_count = random.randint(0, 8)
            available_users = [u for u in cls.MOCK_USERS if u.id != user.id]
            likes = random.sample(available_users, min(like_count, len(available_users)))
            
            # 生成评论
            comments = cls._generate_comments_for_post(f"post_{i}", available_users)
            
            post = Post(
                id=f"post_{i}",
                user=user,
                content=content,
                images=images,
                timestamp=timestamp,
                likes=likes,
                comments=comments
            )
            posts.append(post)
        
        # 按时间倒序排序
        posts.sort(key=lambda x: x.timestamp, reverse=True)
        return posts
    
    @classmethod
    def _generate_comments_for_post(cls, post_id: str, available_users: List[User]) -> List[Comment]:
        """为指定动态生成评论"""
        comment_count = random.randint(0, 5)
        comments = []
        
        comment_texts = [
            "哈哈哈，太有意思了！😄",
            "赞同！👍",
            "我也想去试试",
            "太棒了！",
            "同感同感",
            "好羡慕啊！",
            "厉害厉害！💪",
            "学到了！",
            "太美了！😍",
            "下次一起！"
        ]
        
        for i in range(comment_count):
            user = random.choice(available_users)
            content = random.choice(comment_texts)
            
            timestamp = datetime.now() - timedelta(
                days=random.randint(0, 3),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            comment = Comment(
                id=f"{post_id}_comment_{i}",
                user=user,
                content=content,
                timestamp=timestamp
            )
            comments.append(comment)
        
        # 按时间正序排序（最早的评论在前）
        comments.sort(key=lambda x: x.timestamp)
        return comments
    
    @classmethod
    def get_current_user(cls) -> User:
        """获取当前用户（模拟登录用户）"""
        return User("current_user", "我", "😊")


# 工具函数
def format_relative_time(timestamp: datetime) -> str:
    """格式化相对时间显示"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        if diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            return timestamp.strftime("%m月%d日")
    
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours}小时前"
    
    minutes = diff.seconds // 60
    if minutes > 0:
        return f"{minutes}分钟前"
    
    return "刚刚"


def calculate_image_layout(image_count: int) -> dict:
    """根据图片数量计算布局参数"""
    if image_count == 0:
        return {"columns": 0, "rows": 0, "max_width": 0}
    elif image_count == 1:
        return {"columns": 1, "rows": 1, "max_width": 200}
    elif image_count <= 3:
        return {"columns": image_count, "rows": 1, "max_width": 150}
    elif image_count == 4:
        return {"columns": 2, "rows": 2, "max_width": 120}
    elif image_count <= 6:
        return {"columns": 3, "rows": 2, "max_width": 100}
    else:  # 7-9张图片
        return {"columns": 3, "rows": 3, "max_width": 100}