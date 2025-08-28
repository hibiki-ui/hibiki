#!/usr/bin/env python3
"""
🗄️ Hibiki Music 数据库管理

基于 SQLModel 的现代化数据库管理和服务层
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from sqlmodel import SQLModel, Session, create_engine, select, and_, or_, func
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .models import (
    Song, SongCreate, SongUpdate, SongPublic,
    Tag, TagCreate, TagPublic, TagCategory,
    Playlist, PlaylistCreate, PlaylistUpdate, PlaylistPublic,
    PlayHistory, PlayHistoryCreate, PlayHistoryPublic,
    LanguageVersion, LanguageVersionCreate, LanguageVersionPublic,
    SongFilter, SearchQuery, LibraryStats,
    SongTagLink, PlaylistSongLink
)

class DatabaseManager:
    """数据库管理器 - 单例模式"""
    
    _instance: Optional['DatabaseManager'] = None
    _engine = None
    
    def __new__(cls) -> 'DatabaseManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialized', False):
            self._init_database()
            self._initialized = True
    
    def _init_database(self):
        """初始化数据库连接"""
        # 数据库文件路径
        db_dir = Path.home() / ".hibiki_music"
        db_dir.mkdir(exist_ok=True)
        db_path = db_dir / "music_library.db"
        
        # 创建数据库引擎
        database_url = f"sqlite:///{db_path}"
        self._engine = create_engine(
            database_url,
            echo=False,  # 设为 True 可查看 SQL 语句
            connect_args={"check_same_thread": False}
        )
        
        # SQLite 优化配置
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")  # 启用外键约束
            cursor.execute("PRAGMA journal_mode=WAL")  # WAL 模式提高并发性能
            cursor.execute("PRAGMA synchronous=NORMAL")  # 平衡性能和数据安全
            cursor.execute("PRAGMA cache_size=10000")  # 增加缓存大小
            cursor.execute("PRAGMA temp_store=MEMORY")  # 临时数据存储在内存
            cursor.close()
        
        # 创建所有表
        SQLModel.metadata.create_all(self._engine)
        
        # 初始化系统数据
        self._init_system_data()
        
        print(f"✅ 数据库初始化完成: {db_path}")
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return Session(self._engine)
    
    def _init_system_data(self):
        """初始化系统数据（标签等）"""
        with self.get_session() as session:
            # 检查是否已经初始化过系统标签
            existing_tags = session.exec(select(Tag).where(Tag.is_system == True)).first()
            if existing_tags:
                return
            
            # 创建系统预定义标签
            system_tags = [
                # 语言标签
                {"name": "粤语", "category": TagCategory.LANGUAGE, "color": "#FF6B6B"},
                {"name": "国语", "category": TagCategory.LANGUAGE, "color": "#4ECDC4"},
                {"name": "英语", "category": TagCategory.LANGUAGE, "color": "#45B7D1"},
                {"name": "日语", "category": TagCategory.LANGUAGE, "color": "#96CEB4"},
                {"name": "韩语", "category": TagCategory.LANGUAGE, "color": "#FFEAA7"},
                
                # 年代标签
                {"name": "70年代", "category": TagCategory.ERA, "color": "#FFEAA7"},
                {"name": "80年代", "category": TagCategory.ERA, "color": "#DDA0DD"},
                {"name": "90年代", "category": TagCategory.ERA, "color": "#98D8C8"},
                {"name": "2000年代", "category": TagCategory.ERA, "color": "#F7DC6F"},
                {"name": "2010年代", "category": TagCategory.ERA, "color": "#BB8FCE"},
                {"name": "2020年代", "category": TagCategory.ERA, "color": "#85C1E9"},
                
                # 情感标签
                {"name": "怀旧", "category": TagCategory.EMOTION, "color": "#F1948A"},
                {"name": "浪漫", "category": TagCategory.EMOTION, "color": "#F8BBD9"},
                {"name": "激昂", "category": TagCategory.EMOTION, "color": "#FF7675"},
                {"name": "忧郁", "category": TagCategory.EMOTION, "color": "#A29BFE"},
                {"name": "快乐", "category": TagCategory.EMOTION, "color": "#FD79A8"},
                {"name": "宁静", "category": TagCategory.EMOTION, "color": "#81ECEC"},
                {"name": "治愈", "category": TagCategory.EMOTION, "color": "#55A3FF"},
                
                # 风格标签
                {"name": "民谣", "category": TagCategory.STYLE, "color": "#6C5CE7"},
                {"name": "流行", "category": TagCategory.STYLE, "color": "#A8E6CF"},
                {"name": "摇滚", "category": TagCategory.STYLE, "color": "#FFB3BA"},
                {"name": "电子", "category": TagCategory.STYLE, "color": "#BFEFFF"},
                {"name": "古典", "category": TagCategory.STYLE, "color": "#E6E6FA"},
                {"name": "爵士", "category": TagCategory.STYLE, "color": "#DEB887"},
                {"name": "说唱", "category": TagCategory.STYLE, "color": "#F0E68C"},
            ]
            
            for tag_data in system_tags:
                tag = Tag(
                    name=tag_data["name"],
                    category=tag_data["category"],
                    color=tag_data["color"],
                    is_system=True,
                    description=f"系统预定义的{tag_data['category'].value}标签"
                )
                session.add(tag)
            
            session.commit()
            print("✅ 系统标签初始化完成")

class SongService:
    """歌曲服务层 - 业务逻辑处理"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_song(self, song_data: SongCreate) -> SongPublic:
        """创建新歌曲"""
        with self.db.get_session() as session:
            # 检查文件路径是否已存在
            existing = session.exec(
                select(Song).where(Song.file_path == song_data.file_path)
            ).first()
            
            if existing:
                # 更新现有歌曲信息
                for key, value in song_data.model_dump(exclude_unset=True).items():
                    if hasattr(existing, key) and value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
                song = existing
            else:
                # 创建新歌曲
                song = Song.model_validate(song_data)
                session.add(song)
            
            session.commit()
            session.refresh(song)
            
            return self._song_to_public(song, session)
    
    def get_all_songs(self, limit: int = 1000, offset: int = 0) -> List[SongPublic]:
        """获取所有歌曲"""
        with self.db.get_session() as session:
            songs = session.exec(
                select(Song).order_by(Song.added_at.desc()).limit(limit).offset(offset)
            ).all()
            return [self._song_to_public(song, session) for song in songs]
    
    def get_song_by_id(self, song_id: int) -> Optional[SongPublic]:
        """根据ID获取歌曲"""
        with self.db.get_session() as session:
            song = session.get(Song, song_id)
            return self._song_to_public(song, session) if song else None
    
    def get_song_by_path(self, file_path: str) -> Optional[SongPublic]:
        """根据文件路径获取歌曲"""
        with self.db.get_session() as session:
            song = session.exec(select(Song).where(Song.file_path == file_path)).first()
            return self._song_to_public(song, session) if song else None
    
    def update_song(self, song_id: int, song_data: SongUpdate) -> Optional[SongPublic]:
        """更新歌曲信息"""
        with self.db.get_session() as session:
            song = session.get(Song, song_id)
            if not song:
                return None
            
            # 更新字段
            for key, value in song_data.model_dump(exclude_unset=True).items():
                if hasattr(song, key) and value is not None:
                    setattr(song, key, value)
            
            song.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(song)
            
            return self._song_to_public(song, session)
    
    def delete_song(self, song_id: int) -> bool:
        """删除歌曲"""
        with self.db.get_session() as session:
            song = session.get(Song, song_id)
            if not song:
                return False
            
            session.delete(song)
            session.commit()
            return True
    
    def search_songs(self, query: SearchQuery) -> List[SongPublic]:
        """搜索歌曲"""
        with self.db.get_session() as session:
            # 基础查询
            statement = select(Song)
            
            # 文本搜索
            if query.text.strip():
                text_filter = or_(
                    Song.title.contains(query.text),
                    Song.artist.contains(query.text),
                    Song.album.contains(query.text)
                )
                statement = statement.where(text_filter)
            
            # 应用筛选器
            if query.filters:
                statement = self._apply_filters(statement, query.filters)
            
            # 排序和分页
            statement = statement.order_by(Song.title).limit(query.limit).offset(query.offset)
            
            songs = session.exec(statement).all()
            return [self._song_to_public(song, session) for song in songs]
    
    def get_songs_by_filter(self, filters: SongFilter) -> List[SongPublic]:
        """根据筛选条件获取歌曲"""
        with self.db.get_session() as session:
            statement = select(Song)
            statement = self._apply_filters(statement, filters)
            statement = statement.order_by(Song.title)
            
            songs = session.exec(statement).all()
            return [self._song_to_public(song, session) for song in songs]
    
    def update_play_stats(self, song_id: int, play_duration: float = 0.0, 
                         completion_rate: float = 0.0) -> bool:
        """更新播放统计"""
        with self.db.get_session() as session:
            song = session.get(Song, song_id)
            if not song:
                return False
            
            # 更新歌曲统计
            song.play_count += 1
            song.last_played = datetime.utcnow()
            
            # 记录播放历史
            play_record = PlayHistory(
                song_id=song_id,
                play_duration=play_duration,
                completion_rate=completion_rate,
                played_at=datetime.utcnow()
            )
            session.add(play_record)
            
            session.commit()
            return True
    
    def toggle_favorite(self, song_id: int) -> Optional[bool]:
        """切换歌曲收藏状态"""
        with self.db.get_session() as session:
            song = session.get(Song, song_id)
            if not song:
                return None
            
            song.favorite = not song.favorite
            song.updated_at = datetime.utcnow()
            session.commit()
            
            return song.favorite
    
    def get_library_stats(self) -> LibraryStats:
        """获取音乐库统计信息"""
        with self.db.get_session() as session:
            # 基础统计
            total_songs = session.exec(select(func.count(Song.id))).first()
            total_artists = session.exec(select(func.count(func.distinct(Song.artist)))).first()
            total_albums = session.exec(select(func.count(func.distinct(Song.album)))).first()
            total_duration = session.exec(select(func.sum(Song.duration))).first() or 0.0
            favorite_count = session.exec(select(func.count(Song.id)).where(Song.favorite == True)).first()
            
            # 最常播放的歌曲
            most_played = session.exec(
                select(Song).order_by(Song.play_count.desc()).limit(1)
            ).first()
            
            # 语言分布
            language_dist = {}
            lang_stats = session.exec(
                select(Song.detected_language, func.count(Song.id))
                .group_by(Song.detected_language)
            ).all()
            for lang, count in lang_stats:
                if lang:
                    language_dist[lang] = count
            
            # 最近添加的歌曲
            recent_songs = session.exec(
                select(Song).order_by(Song.added_at.desc()).limit(5)
            ).all()
            
            return LibraryStats(
                total_songs=total_songs or 0,
                total_artists=total_artists or 0,
                total_albums=total_albums or 0,
                total_duration=total_duration,
                favorite_count=favorite_count or 0,
                most_played_song=self._song_to_public(most_played, session) if most_played else None,
                language_distribution=language_dist,
                recent_additions=[self._song_to_public(song, session) for song in recent_songs]
            )
    
    def _apply_filters(self, statement, filters: SongFilter):
        """应用筛选条件到查询语句"""
        conditions = []
        
        # 语言筛选
        if filters.languages:
            conditions.append(Song.detected_language.in_(filters.languages))
        
        # 收藏筛选
        if filters.favorite_only:
            conditions.append(Song.favorite == True)
        
        # 评分筛选
        if filters.min_rating:
            conditions.append(Song.user_rating >= filters.min_rating)
        
        # 年份范围
        if filters.year_range:
            start_year, end_year = filters.year_range
            conditions.append(and_(Song.year >= start_year, Song.year <= end_year))
        
        # 应用条件
        if conditions:
            if filters.logic_operator == "OR":
                statement = statement.where(or_(*conditions))
            else:  # AND
                statement = statement.where(and_(*conditions))
        
        return statement
    
    def _song_to_public(self, song: Song, session: Session) -> SongPublic:
        """将数据库模型转换为公开模型"""
        if not song:
            return None
            
        # 获取标签名称
        tag_names = [tag.name for tag in song.tags] if song.tags else []
        
        return SongPublic(
            id=song.id,
            title=song.title,
            artist=song.artist,
            album=song.album,
            album_artist=song.album_artist,
            duration=song.duration,
            year=song.year,
            track_number=song.track_number,
            disc_number=song.disc_number,
            genre=song.genre,
            file_format=song.file_format,
            bitrate=song.bitrate,
            sample_rate=song.sample_rate,
            detected_language=song.detected_language,
            language_confidence=song.language_confidence,
            emotions=song.emotions,
            themes=song.themes,
            era_tags=song.era_tags,
            style_tags=song.style_tags,
            file_path=song.file_path,
            play_count=song.play_count,
            favorite=song.favorite,
            last_played=song.last_played,
            added_at=song.added_at,
            tags=tag_names
        )

class TagService:
    """标签服务层"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_all_tags(self, category: Optional[TagCategory] = None) -> List[TagPublic]:
        """获取所有标签"""
        with self.db.get_session() as session:
            statement = select(Tag).order_by(Tag.name)
            
            if category:
                statement = statement.where(Tag.category == category)
            
            tags = session.exec(statement).all()
            return [TagPublic.model_validate(tag) for tag in tags]
    
    def create_tag(self, tag_data: TagCreate) -> TagPublic:
        """创建新标签"""
        with self.db.get_session() as session:
            tag = Tag.model_validate(tag_data)
            session.add(tag)
            session.commit()
            session.refresh(tag)
            
            return TagPublic.model_validate(tag)
    
    def get_tags_by_category(self, category: TagCategory) -> List[TagPublic]:
        """根据类别获取标签"""
        with self.db.get_session() as session:
            tags = session.exec(
                select(Tag).where(Tag.category == category).order_by(Tag.name)
            ).all()
            return [TagPublic.model_validate(tag) for tag in tags]