#!/usr/bin/env python3
"""
🎵 Hibiki Music 应用状态管理

基于 Hibiki UI Signal 系统的全局响应式状态管理
"""

from hibiki.ui import Signal, Computed, Effect
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

# 导入数据模型 (将在 MVP Phase 2 实现)
# from data.models import Song, SmartPlaylist, TagFilter

@dataclass
class Song:
    """临时歌曲数据模型 - MVP v0.1"""
    id: str
    title: str
    artist: str
    album: Optional[str] = None
    duration: float = 0.0
    file_path: str = ""

@dataclass  
class TagFilter:
    """临时标签筛选器 - MVP v0.1"""
    search_text: str = ""
    selected_tags: List[str] = None
    
    def __post_init__(self):
        if self.selected_tags is None:
            self.selected_tags = []

class MusicAppState:
    """
    Hibiki Music 全局应用状态
    
    基于 Hibiki UI Signal 系统实现响应式状态管理
    所有UI组件通过监听这些Signal自动更新
    """
    
    def __init__(self):
        from .logging import get_logger
        self.logger = get_logger("app_state")
        self.logger.info("🔄 初始化 MusicAppState...")
        
        # ================================
        # 音频播放引擎
        # ================================
        self.audio_player = None  # 延迟初始化，避免循环依赖
        
        # ================================
        # 播放器状态
        # ================================
        self.current_song = Signal(None)  # Song | None
        self.is_playing = Signal(False)
        self.position = Signal(0.0)       # 播放位置 (秒)
        self.duration = Signal(0.0)       # 总时长 (秒)
        
        # 音频播放器调试日志
        from hibiki.ui import Effect
        
        Effect(lambda: self.logger.debug(f"🎯 播放位置变化: {self.position.value:.2f}秒"))
        Effect(lambda: self.logger.debug(f"🎯 播放时长变化: {self.duration.value:.2f}秒"))
        self.volume = Signal(0.8)         # 音量 0.0-1.0
        self.shuffle = Signal(False)      # 随机播放
        self.repeat = Signal("none")      # "none" | "one" | "all"
        
        # ================================
        # 音乐库状态  
        # ================================
        self.all_songs = Signal([])       # List[Song] - 所有歌曲
        self.current_playlist = Signal([]) # List[Song] - 当前播放列表
        self.selected_song = Signal(None) # Song | None - 选中的歌曲
        
        # 筛选和搜索
        self.current_filter = Signal(TagFilter())
        self.search_query = Signal("")
        self.filtered_songs = Computed(lambda: self._apply_filters())
        
        # ================================
        # UI 状态
        # ================================ 
        self.current_view = Signal("library")  # "library" | "now_playing" | "tags" | "settings"
        self.loading = Signal(False)
        self.sidebar_collapsed = Signal(False)
        self.show_visualizer = Signal(True)
        
        # ================================
        # 标签系统状态 (MVP v0.2)
        # ================================
        self.available_languages = Signal(["zh-HK", "zh-CN", "en", "ja"])  
        self.available_eras = Signal(["70s", "80s", "90s", "2000s", "2010s", "2020s"])
        self.available_emotions = Signal(["nostalgic", "romantic", "energetic", "melancholic", "happy"])
        self.tag_suggestions = Signal([])  # 标签建议
        
        # ================================
        # 统计和分析数据
        # ================================
        self.total_songs = Computed(lambda: len(self.all_songs.value))
        self.total_duration = Computed(lambda: sum(song.duration for song in self.all_songs.value))
        self.play_progress = Computed(lambda: 
            self.position.value / self.duration.value if self.duration.value > 0 else 0.0
        )
        
        # ================================
        # 副作用 - 调试和日志
        # ================================
        self._setup_effects()
        
        self.logger.info("✅ MusicAppState 初始化完成")
    
    def init_audio_player(self):
        """初始化音频播放引擎 (延迟初始化)"""
        if self.audio_player is None:
            self.logger.debug("🎵 [AppState] 开始导入 AudioPlayer...")
            from .player import AudioPlayer
            self.logger.debug("🎵 [AppState] 创建 AudioPlayer 实例...")
            self.audio_player = AudioPlayer(self)
            self.logger.debug("🎵 [AppState] AudioPlayer 已初始化")
        else:
            self.logger.debug("🎵 [AppState] AudioPlayer 已存在，跳过初始化")
        
    def _apply_filters(self) -> List[Song]:
        """应用当前筛选条件"""
        songs = self.all_songs.value
        filter_obj = self.current_filter.value
        search = self.search_query.value.lower()
        
        # 文本搜索
        if search:
            songs = [
                song for song in songs 
                if search in song.title.lower() 
                or search in song.artist.lower()
                or (song.album and search in song.album.lower())
            ]
            
        # TODO: 标签筛选将在 MVP Phase 2 实现
        
        return songs
        
    def _setup_effects(self):
        """设置副作用监听"""
        
        # 播放状态变化日志
        Effect(lambda: self.logger.debug(f"🎵 播放状态: {self.is_playing.value}"))
        
        # 当前歌曲变化日志
        Effect(lambda: self.logger.debug(f"🎧 当前歌曲: {self.current_song.value.title if self.current_song.value else 'None'}"))
        
        # 筛选结果变化日志
        Effect(lambda: self.logger.debug(f"🔍 筛选结果: {len(self.filtered_songs.value)} 首歌曲"))
        
        # 视图切换日志
        Effect(lambda: self.logger.debug(f"📱 当前视图: {self.current_view.value}"))
        
    # ================================
    # 播放器控制方法
    # ================================
    
    def play_song(self, song: Song):
        """播放指定歌曲"""
        if not song:
            return False
            
        # 确保音频播放器已初始化
        self.init_audio_player()
        
        # 加载并播放歌曲
        if self.audio_player.load_song(song):
            return self.audio_player.play()
        else:
            self.logger.error(f"❌ 无法播放歌曲: {song.title}")
            return False
        
    def toggle_play_pause(self):
        """切换播放/暂停"""
        self.logger.debug("🎵 [AppState] toggle_play_pause 被调用")
        # 确保音频播放器已初始化
        self.logger.debug("🎵 [AppState] 正在初始化音频播放器...")
        self.init_audio_player()
        
        if self.audio_player:
            self.logger.debug("🎵 [AppState] 音频播放器存在，调用 toggle_play_pause")
            return self.audio_player.toggle_play_pause()
        else:
            self.logger.error("❌ [AppState] 音频播放器为 None！")
            return False
        
    def next_song(self):
        """下一首"""
        current_playlist = self.current_playlist.value
        current = self.current_song.value
        
        if not current_playlist or not current:
            return
            
        try:
            current_index = current_playlist.index(current)
            next_index = (current_index + 1) % len(current_playlist)
            self.play_song(current_playlist[next_index])
        except ValueError:
            # 当前歌曲不在播放列表中
            if current_playlist:
                self.play_song(current_playlist[0])
    
    def previous_song(self):
        """上一首"""
        current_playlist = self.current_playlist.value
        current = self.current_song.value
        
        if not current_playlist or not current:
            return
            
        try:
            current_index = current_playlist.index(current)
            prev_index = (current_index - 1) % len(current_playlist)
            self.play_song(current_playlist[prev_index])
        except ValueError:
            if current_playlist:
                self.play_song(current_playlist[-1])  # 最后一首
                
    # ================================
    # 音乐库管理方法
    # ================================
    
    def add_songs(self, songs: List[Song]):
        """添加歌曲到音乐库"""
        current_songs = self.all_songs.value.copy()
        current_songs.extend(songs)
        self.all_songs.value = current_songs
        
    def set_playlist(self, songs: List[Song]):
        """设置当前播放列表"""
        self.current_playlist.value = songs
        
    def search_songs(self, query: str):
        """搜索歌曲"""
        self.search_query.value = query
        
    # ================================
    # 标签系统方法 (MVP v0.2)
    # ================================
    
    def apply_tag_filter(self, languages: List[str] = None, 
                        eras: List[str] = None,
                        emotions: List[str] = None):
        """应用标签筛选"""
        # TODO: 实现完整的标签筛选逻辑
        pass
        
    def get_filtered_count(self) -> int:
        """获取筛选后的歌曲数量"""
        return len(self.filtered_songs.value)
        
    def clear_filters(self):
        """清空所有筛选条件"""
        self.current_filter.value = TagFilter()
        self.search_query.value = ""
        
    # ================================
    # 音频播放器控制方法
    # ================================
    
    def set_volume(self, volume: float) -> bool:
        """设置音量 (0.0 - 1.0)"""
        self.init_audio_player()
        
        if self.audio_player:
            return self.audio_player.set_volume(volume)
        else:
            return False
    
    def seek_to_position(self, position: float) -> bool:
        """跳转到指定位置 (秒)"""
        self.init_audio_player()
        
        if self.audio_player:
            return self.audio_player.seek_to_position(position)
        else:
            return False
    
    def pause(self) -> bool:
        """暂停播放"""
        self.init_audio_player()
        
        if self.audio_player:
            return self.audio_player.pause()
        else:
            return False
    
    def resume(self) -> bool:
        """继续播放"""
        self.init_audio_player()
        
        if self.audio_player:
            return self.audio_player.play()
        else:
            return False
    
    def stop(self) -> bool:
        """停止播放"""
        self.init_audio_player()
        
        if self.audio_player:
            return self.audio_player.stop()
        else:
            return False