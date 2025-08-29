#!/usr/bin/env python3
"""
🎵 Hibiki Music 数据模型

基于 SQLModel (SQLAlchemy + Pydantic) 的现代化音乐库数据模型
支持智能标签、多语言版本关联和播放历史
"""

from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import UniqueConstraint, Index
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import json

# ================================
# 枚举定义
# ================================

class TagCategory(str, Enum):
    LANGUAGE = "language"
    EMOTION = "emotion"
    ERA = "era"
    STYLE = "style"
    CUSTOM = "custom"

class RelationType(str, Enum):
    LANGUAGE_VERSION = "language_version"
    COVER = "cover"
    REMIX = "remix"
    SIMILAR = "similar"

class PlaySource(str, Enum):
    LIBRARY = "library"
    PLAYLIST = "playlist"
    SEARCH = "search"
    RECOMMENDATION = "recommendation"

class UserActionType(str, Enum):
    """用户操作行为类型"""
    PLAY_START = "play_start"           # 开始播放
    PLAY_COMPLETE = "play_complete"     # 完整播放完成  
    PLAY_INTERRUPT = "play_interrupt"   # 播放中断/停止
    SONG_SWITCH = "song_switch"         # 歌曲切换
    SEEK_OPERATION = "seek_operation"   # 进度条拖拽/跳转
    PLAY_PAUSE = "play_pause"           # 暂停操作
    PLAY_RESUME = "play_resume"         # 恢复播放

class ActionTrigger(str, Enum):
    """操作触发方式"""
    MANUAL = "manual"       # 用户手动操作
    AUTOMATIC = "automatic" # 系统自动操作

# ================================
# 关联表模型 (多对多关系)
# ================================

class SongTagLink(SQLModel, table=True):
    """歌曲-标签关联表"""
    __tablename__ = "song_tags"
    
    song_id: Optional[int] = Field(default=None, foreign_key="songs.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)

class PlaylistSongLink(SQLModel, table=True):
    """播放列表-歌曲关联表"""
    __tablename__ = "playlist_songs"
    
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlists.id", primary_key=True)
    song_id: Optional[int] = Field(default=None, foreign_key="songs.id", primary_key=True)
    position: int = Field(default=0)  # 在播放列表中的位置
    added_at: datetime = Field(default_factory=datetime.utcnow)

# ================================
# 核心数据模型 (共享字段)
# ================================

class SongBase(SQLModel):
    """歌曲基础模型 - 共享字段"""
    title: str = Field(max_length=500, index=True)
    artist: str = Field(max_length=500, index=True)
    album: Optional[str] = Field(default=None, max_length=500)
    album_artist: Optional[str] = Field(default=None, max_length=500)
    
    # 音频属性
    duration: float = Field(default=0.0, ge=0.0)  # 时长(秒)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    track_number: Optional[int] = Field(default=None, ge=1)
    disc_number: Optional[int] = Field(default=None, ge=1)
    genre: Optional[str] = Field(default=None, max_length=200)
    
    # 文件信息  
    file_format: Optional[str] = Field(default=None, max_length=10)  # mp3, flac, m4a
    bitrate: Optional[int] = Field(default=None, ge=0)
    sample_rate: Optional[int] = Field(default=None, ge=0)
    
    # 智能标签 ⭐ 核心功能
    detected_language: Optional[str] = Field(default=None, max_length=10)  # zh-CN, zh-HK, ja, en
    language_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    emotions: Optional[Dict[str, float]] = Field(default=None, sa_column=Column(JSON))
    themes: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    era_tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    style_tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

class SongCreate(SongBase):
    """创建歌曲时的数据模型"""
    file_path: str = Field(unique=True, max_length=1000)
    file_size: int = Field(default=0, ge=0)
    file_modified_at: Optional[datetime] = Field(default=None)

class SongUpdate(SongBase):
    """更新歌曲时的数据模型 - 所有字段可选"""
    title: Optional[str] = Field(default=None, max_length=500)
    artist: Optional[str] = Field(default=None, max_length=500)
    user_rating: Optional[int] = Field(default=None, ge=1, le=10)
    favorite: Optional[bool] = Field(default=None)

class Song(SongBase, table=True):
    """歌曲完整模型 - 数据库表"""
    __tablename__ = "songs"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 文件信息 (唯一约束)
    file_path: str = Field(unique=True, max_length=1000, index=True)
    file_size: int = Field(default=0, ge=0)
    file_modified_at: Optional[datetime] = Field(default=None)
    
    # 用户数据
    play_count: int = Field(default=0, ge=0)
    skip_count: int = Field(default=0, ge=0)
    user_rating: Optional[int] = Field(default=None, ge=1, le=10)
    favorite: bool = Field(default=False)
    last_played: Optional[datetime] = Field(default=None)
    
    # 系统字段
    added_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系定义
    tags: List["Tag"] = Relationship(back_populates="songs", link_model=SongTagLink)
    play_history: List["PlayHistory"] = Relationship(back_populates="song")
    language_versions: List["LanguageVersion"] = Relationship(
        back_populates="song", 
        sa_relationship_kwargs={"foreign_keys": "LanguageVersion.song_id"}
    )
    playlists: List["Playlist"] = Relationship(back_populates="songs", link_model=PlaylistSongLink)
    
    # 数据库约束
    __table_args__ = (
        Index('idx_song_search', 'title', 'artist', 'album'),
        Index('idx_song_language', 'detected_language'),
        Index('idx_song_favorite', 'favorite'),
    )

class SongPublic(SongBase):
    """歌曲公开数据模型 - API 返回"""
    id: int
    file_path: str
    play_count: int = 0
    favorite: bool = False
    last_played: Optional[datetime] = None
    added_at: datetime
    tags: List[str] = []  # 标签名称列表

# ================================
# 标签模型
# ================================

class TagBase(SQLModel):
    """标签基础模型"""
    name: str = Field(max_length=100, unique=True, index=True)
    category: TagCategory = Field(default=TagCategory.CUSTOM)
    color: Optional[str] = Field(default=None, max_length=7, regex=r"^#[0-9A-Fa-f]{6}$")
    description: Optional[str] = Field(default=None, max_length=500)

class TagCreate(TagBase):
    """创建标签时的数据模型"""
    pass

class Tag(TagBase, table=True):
    """标签完整模型 - 数据库表"""
    __tablename__ = "tags"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 系统字段
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_system: bool = Field(default=False)  # 系统预定义标签
    
    # 关系
    songs: List[Song] = Relationship(back_populates="tags", link_model=SongTagLink)

class TagPublic(TagBase):
    """标签公开数据模型"""
    id: int
    is_system: bool = False
    created_at: datetime

# ================================
# 播放列表模型
# ================================

class PlaylistBase(SQLModel):
    """播放列表基础模型"""
    name: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_smart: bool = Field(default=False)
    smart_criteria: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))

class PlaylistCreate(PlaylistBase):
    """创建播放列表数据模型"""
    pass

class PlaylistUpdate(SQLModel):
    """更新播放列表数据模型"""
    name: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_smart: Optional[bool] = Field(default=None)
    smart_criteria: Optional[Dict[str, Any]] = Field(default=None)

class Playlist(PlaylistBase, table=True):
    """播放列表完整模型"""
    __tablename__ = "playlists"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 系统字段
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    songs: List[Song] = Relationship(back_populates="playlists", link_model=PlaylistSongLink)

class PlaylistPublic(PlaylistBase):
    """播放列表公开数据模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    song_count: int = 0

# ================================
# 播放历史模型
# ================================

class PlayHistoryBase(SQLModel):
    """播放历史基础模型"""
    play_duration: float = Field(default=0.0, ge=0.0)  # 实际播放时长
    completion_rate: float = Field(default=0.0, ge=0.0, le=1.0)  # 完成度
    play_source: PlaySource = Field(default=PlaySource.LIBRARY)

class PlayHistoryCreate(PlayHistoryBase):
    """创建播放历史数据模型"""
    song_id: int
    playlist_id: Optional[int] = None

class PlayHistory(PlayHistoryBase, table=True):
    """播放历史完整模型"""
    __tablename__ = "play_history"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外键
    song_id: int = Field(foreign_key="songs.id", index=True)
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlists.id")
    
    # 时间戳
    played_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # 关系
    song: Song = Relationship(back_populates="play_history")

class PlayHistoryPublic(PlayHistoryBase):
    """播放历史公开数据模型"""
    id: int
    song_id: int
    played_at: datetime
    song_title: str = ""
    song_artist: str = ""

# ================================
# 多语言版本关联模型 ⭐ 核心创新
# ================================

class LanguageVersionBase(SQLModel):
    """语言版本关联基础模型"""
    relation_type: RelationType = Field(default=RelationType.LANGUAGE_VERSION)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    notes: Optional[str] = Field(default=None, max_length=1000)
    verified: bool = Field(default=False)

class LanguageVersionCreate(LanguageVersionBase):
    """创建语言版本关联数据模型"""
    song_id: int
    related_song_id: int

class LanguageVersion(LanguageVersionBase, table=True):
    """语言版本关联完整模型"""
    __tablename__ = "language_versions"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外键
    song_id: int = Field(foreign_key="songs.id")
    related_song_id: int = Field(foreign_key="songs.id")
    
    # 系统字段
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    song: Song = Relationship(
        back_populates="language_versions",
        sa_relationship_kwargs={"foreign_keys": "LanguageVersion.song_id"}
    )
    related_song: Song = Relationship(
        sa_relationship_kwargs={"foreign_keys": "LanguageVersion.related_song_id"}
    )
    
    # 约束：防止重复关联
    __table_args__ = (
        UniqueConstraint('song_id', 'related_song_id', name='unique_language_version'),
    )

class LanguageVersionPublic(LanguageVersionBase):
    """语言版本关联公开数据模型"""
    id: int
    song_id: int
    related_song_id: int
    created_at: datetime
    song_title: str = ""
    related_song_title: str = ""

# ================================
# 用户行为记录模型 ⭐ 核心创新
# ================================

class UserActionBase(SQLModel):
    """用户操作行为基础模型"""
    action_type: UserActionType = Field(index=True)
    trigger: ActionTrigger = Field(default=ActionTrigger.MANUAL)
    
    # 歌曲信息
    song_id: Optional[int] = Field(default=None, foreign_key="songs.id")
    related_song_id: Optional[int] = Field(default=None, foreign_key="songs.id")  # 切歌时的目标歌曲
    
    # 位置信息(秒)
    from_position: Optional[float] = Field(default=None, ge=0.0)  # 开始位置
    to_position: Optional[float] = Field(default=None, ge=0.0)    # 结束/目标位置
    
    # 播放统计
    play_duration: Optional[float] = Field(default=None, ge=0.0)  # 实际播放时长
    completion_rate: Optional[float] = Field(default=None, ge=0.0, le=1.0)  # 完成度
    
    # 上下文信息
    session_id: Optional[str] = Field(default=None, max_length=100)  # 播放会话ID
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlists.id")
    play_source: Optional[PlaySource] = Field(default=PlaySource.LIBRARY)
    
    # 元数据 (重命名避免与SQLModel父类冲突)
    extra_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    notes: Optional[str] = Field(default=None, max_length=500)

class UserActionCreate(UserActionBase):
    """创建用户行为记录数据模型"""
    action_type: UserActionType
    song_id: int  # 必须指定歌曲

class UserAction(UserActionBase, table=True):
    """用户操作行为记录完整模型"""
    __tablename__ = "user_actions"
    
    # 主键
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 时间戳
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # 关系 - 明确指定外键避免歧义
    song: Optional[Song] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "UserAction.song_id"}
    )
    related_song: Optional[Song] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "UserAction.related_song_id"}
    )
    
    # 数据库约束和索引
    __table_args__ = (
        Index('idx_user_action_type_time', 'action_type', 'timestamp'),
        Index('idx_user_action_session', 'session_id', 'timestamp'),
        Index('idx_user_action_song_time', 'song_id', 'timestamp'),
    )

class UserActionPublic(UserActionBase):
    """用户行为记录公开数据模型"""
    id: int
    timestamp: datetime
    song_title: Optional[str] = None
    song_artist: Optional[str] = None
    related_song_title: Optional[str] = None

# ================================
# 搜索和筛选模型
# ================================

class SongFilter(SQLModel):
    """歌曲筛选参数模型"""
    languages: Optional[List[str]] = Field(default=None)
    emotions: Optional[Dict[str, float]] = Field(default=None)
    themes: Optional[List[str]] = Field(default=None)
    eras: Optional[List[str]] = Field(default=None)
    styles: Optional[List[str]] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    favorite_only: bool = Field(default=False)
    min_rating: Optional[int] = Field(default=None, ge=1, le=10)
    year_start: Optional[int] = Field(default=None, ge=1900, le=2100)
    year_end: Optional[int] = Field(default=None, ge=1900, le=2100)
    logic_operator: str = Field(default="AND", regex=r"^(AND|OR)$")

class SearchQuery(SQLModel):
    """搜索查询模型"""
    text: str = Field(max_length=200)
    filters: Optional[SongFilter] = Field(default=None)
    limit: int = Field(default=50, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)

# ================================
# 统计模型
# ================================

class LibraryStats(SQLModel):
    """音乐库统计数据"""
    total_songs: int = 0
    total_artists: int = 0
    total_albums: int = 0
    total_duration: float = 0.0  # 总时长(秒)
    favorite_count: int = 0
    most_played_song: Optional[SongPublic] = None
    language_distribution: Dict[str, int] = {}
    recent_additions: List[SongPublic] = []