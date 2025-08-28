#!/usr/bin/env python3
"""
🖼️ Hibiki Music 主窗口

基于 Hibiki UI 的响应式主界面
展示音乐播放器的所有核心功能
"""

from hibiki.ui import (
    Signal, Computed, Effect,
    Label, Button, Container, TextField, Slider,
    ComponentStyle, px, percent, auto,
    Display, FlexDirection, JustifyContent, AlignItems
)
from ..core.app_state import MusicAppState, Song

class MusicMainWindow:
    """Hibiki Music 主窗口类"""
    
    def __init__(self, app_state: MusicAppState):
        self.app_state = app_state
        
        # 创建示例数据 (MVP v0.1)
        self._create_sample_data()
        
    def _create_sample_data(self):
        """创建示例音乐数据用于演示"""
        sample_songs = [
            Song("1", "月亮代表我的心", "邓丽君", "邓丽君经典", 180.0, "/path/to/song1.mp3"),
            Song("2", "甜蜜蜜", "邓丽君", "邓丽君经典", 195.5, "/path/to/song2.mp3"),
            Song("3", "上海滩", "叶丽仪", "电视剧原声", 220.3, "/path/to/song3.mp3"),
            Song("4", "千千阙歌", "陈慧娴", "陈慧娴精选", 248.7, "/path/to/song4.mp3"),
            Song("5", "Monica", "张国荣", "张国荣热恋", 198.2, "/path/to/song5.mp3"),
        ]
        
        self.app_state.add_songs(sample_songs)
        self.app_state.set_playlist(sample_songs)
        
    def create_header(self) -> Container:
        """创建顶部标题区域"""
        title = Label(
            "🎵 Hibiki Music",
            style=ComponentStyle(margin_bottom=px(5)),
            font_size=24,
            font_weight="bold",
            color="#333"
        )
        
        subtitle = Label(
            "智能原生 macOS 音乐播放器 - MVP v0.1",
            style=ComponentStyle(margin_bottom=px(20)),
            font_size=14,
            color="#666"
        )
        
        return Container(
            children=[title, subtitle],
            style=ComponentStyle(
                padding=px(20),
                background_color="#f8f9fa"
            )
        )
        
    def create_player_controls(self) -> Container:
        """创建播放器控制区域"""
        
        # 播放/暂停按钮
        play_pause_btn = Button(
            lambda: "⏸️ 暂停" if self.app_state.is_playing.value else "▶️ 播放",
            style=ComponentStyle(
                width=px(100),
                height=px(36),
                margin_right=px(10)
            ),
            on_click=lambda: self.app_state.toggle_play_pause()
        )
        
        # 上一首按钮
        prev_btn = Button(
            "⏮️ 上一首",
            style=ComponentStyle(
                width=px(80),
                height=px(36), 
                margin_right=px(10)
            ),
            on_click=lambda: self.app_state.previous_song()
        )
        
        # 下一首按钮  
        next_btn = Button(
            "⏭️ 下一首",
            style=ComponentStyle(
                width=px(80),
                height=px(36),
                margin_right=px(20)
            ),
            on_click=lambda: self.app_state.next_song()
        )
        
        # 音量控制
        volume_label = Label(
            "🔊 音量",
            style=ComponentStyle(margin_right=px(10)),
            font_size=14
        )
        
        volume_slider = Slider(
            self.app_state.volume,
            min_value=0.0,
            max_value=1.0,
            style=ComponentStyle(
                width=px(150),
                margin_right=px(10)
            )
        )
        
        volume_display = Label(
            lambda: f"{int(self.app_state.volume.value * 100)}%",
            style=ComponentStyle(width=px(40)),
            font_size=14
        )
        
        # 播放控制容器
        controls_container = Container(
            children=[
                prev_btn, play_pause_btn, next_btn,
                volume_label, volume_slider, volume_display
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.CENTER
            )
        )
        
        return Container(
            children=[controls_container],
            style=ComponentStyle(
                padding=px(20),
                background_color="#ffffff"
            )
        )
        
    def create_now_playing(self) -> Container:
        """创建当前播放信息区域"""
        
        current_song_title = Label(
            lambda: f"♪ {self.app_state.current_song.value.title}" if self.app_state.current_song.value else "♪ 没有播放歌曲",
            style=ComponentStyle(margin_bottom=px(5)),
            font_size=18,
            font_weight="bold"
        )
        
        current_song_artist = Label(
            lambda: f"👤 {self.app_state.current_song.value.artist}" if self.app_state.current_song.value else "",
            style=ComponentStyle(margin_bottom=px(10)),
            font_size=14,
            color="#666"
        )
        
        # 播放进度显示
        progress_text = Label(
            lambda: f"⏱️ 进度: {int(self.app_state.position.value)}s / {int(self.app_state.duration.value)}s",
            font_size=12,
            color="#888"
        )
        
        return Container(
            children=[current_song_title, current_song_artist, progress_text],
            style=ComponentStyle(
                padding=px(20),
                background_color="#f1f3f4",
                border_radius=px(8),
                margin_bottom=px(20)
            )
        )
        
    def create_song_list(self) -> Container:
        """创建歌曲列表区域"""
        
        # 搜索框
        search_input = TextField(
            self.app_state.search_query,
            placeholder="🔍 搜索歌曲、艺术家或专辑...",
            style=ComponentStyle(
                width=percent(100),
                height=px(36),
                margin_bottom=px(15)
            )
        )
        
        # 歌曲列表标题
        list_title = Label(
            lambda: f"🎶 音乐库 ({self.app_state.get_filtered_count()} 首)",
            style=ComponentStyle(margin_bottom=px(10)),
            font_size=16,
            font_weight="bold"
        )
        
        # 歌曲项容器 (这里简化显示，实际应该用 TableView)
        song_items = []
        for i in range(min(5, len(self.app_state.filtered_songs.value))):
            song = self.app_state.filtered_songs.value[i]
            
            song_item = Button(
                f"🎵 {song.title} - {song.artist}",
                style=ComponentStyle(
                    width=percent(100),
                    height=px(32),
                    margin_bottom=px(2),
                    background_color="#ffffff"
                ),
                on_click=lambda s=song: self.app_state.play_song(s)
            )
            song_items.append(song_item)
            
        if not song_items:
            no_songs_label = Label(
                "🔍 没有找到匹配的歌曲",
                style=ComponentStyle(
                    padding=px(20)
                ),
                color="#888"
            )
            song_items.append(no_songs_label)
        
        return Container(
            children=[search_input, list_title] + song_items,
            style=ComponentStyle(
                padding=px(20)
            )
        )
        
    def create_stats_panel(self) -> Container:
        """创建统计面板"""
        
        total_songs_stat = Label(
            lambda: f"📊 总歌曲数: {self.app_state.total_songs.value}",
            style=ComponentStyle(margin_bottom=px(5)),
            font_size=14
        )
        
        total_duration_stat = Label(
            lambda: f"⏰ 总时长: {int(self.app_state.total_duration.value / 60)} 分钟",
            style=ComponentStyle(margin_bottom=px(5)),
            font_size=14
        )
        
        playing_status = Label(
            lambda: f"🎵 状态: {'播放中' if self.app_state.is_playing.value else '已暂停'}",
            font_size=14
        )
        
        return Container(
            children=[total_songs_stat, total_duration_stat, playing_status],
            style=ComponentStyle(
                padding=px(15),
                background_color="#e9ecef",
                border_radius=px(6),
                margin_top=px(20)
            )
        )
        
    def create_main_container(self) -> Container:
        """创建主容器"""
        
        # 创建各个区域
        header = self.create_header()
        player_controls = self.create_player_controls()
        now_playing = self.create_now_playing()
        song_list = self.create_song_list()
        stats_panel = self.create_stats_panel()
        
        # 主内容区域
        content_area = Container(
            children=[now_playing, song_list, stats_panel],
            style=ComponentStyle(
                flex="1",
                overflow="auto",
                background_color="#ffffff"
            )
        )
        
        # 主容器
        main_container = Container(
            children=[header, player_controls, content_area],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                height=percent(100),
                background_color="#f8f9fa"
            )
        )
        
        return main_container