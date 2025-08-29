#!/usr/bin/env python3
"""
🎵 Hibiki Music 主应用程序 v0.3

基于 Hibiki UI 框架的智能音乐播放器
集成自定义组件的专业版本
"""

from hibiki.ui import (
    ManagerFactory, Label, Button, Container, ComponentStyle, px,
    Display, FlexDirection, AlignItems, JustifyContent, Signal, Computed, Effect
)
from hibiki.music.core.app_state import MusicAppState
from hibiki.music.core.scanner import scan_music_library
from hibiki.music.data.database import SongService
from hibiki.music.ui.components import (
    MusicProgressBar, VolumeSlider, AlbumArtView, SongListItem
)
from pathlib import Path
from typing import List, Optional

class HibikiMusicApp:
    """
    Hibiki Music 主应用程序类
    
    MVP v0.3 功能：
    - 专业音乐播放器界面
    - 自定义组件集成
    - 完整的播放控制
    - 歌曲列表视图
    - 响应式状态管理
    """
    
    def __init__(self):
        from hibiki.music.core.logging import get_logger
        self.logger = get_logger("main")
        self.logger.info("🎵 初始化 Hibiki Music v0.3...")
        
        # 初始化应用状态
        self.state = MusicAppState()
        
        # 应用管理器
        self.app_manager = None
        self.window = None
        
        # UI状态
        self.songs_list = Signal([])
        self.selected_song_index = Signal(0)
        self.current_album_art = Signal(None)
    
    def _load_music_library(self):
        """加载音乐库"""
        self.logger.info("🔍 加载音乐库...")
        
        # 获取当前目录的music/data路径
        current_dir = Path(__file__).parent.parent.parent.parent  # music目录
        data_dir = current_dir / "data"
        
        # 首次扫描 - 如果data目录存在就扫描
        if data_dir.exists():
            self.logger.info(f"📁 扫描目录: {data_dir}")
            try:
                scan_music_library(str(data_dir))
                self.logger.info("✅ 音乐库扫描完成")
            except Exception as e:
                self.logger.warning(f"⚠️ 扫描失败: {e}")
        
        # 从数据库加载所有歌曲
        try:
            song_service = SongService()
            db_songs = song_service.get_all_songs()
            
            if db_songs:
                # 转换为应用状态使用的Song对象
                from hibiki.music.core.app_state import Song
                app_songs = [
                    Song(
                        id=str(song.id),
                        title=song.title,
                        artist=song.artist,
                        album=song.album,
                        duration=song.duration,
                        file_path=song.file_path
                    )
                    for song in db_songs
                ]
                
                self.state.add_songs(app_songs)
                self.state.set_playlist(app_songs)
                self.songs_list.value = app_songs  # 更新UI歌曲列表
                self.logger.info(f"✅ 从数据库加载了 {len(app_songs)} 首歌曲")
                
                # 如果有歌曲，默认选中第一首并开始播放以测试进度条
                if app_songs:
                    self.logger.info("🎵 自动开始播放第一首歌曲进行测试...")
                    # 延迟2秒后自动开始播放
                    import threading
                    def auto_play():
                        import time
                        time.sleep(2)  # 等待UI初始化完成
                        first_song = app_songs[0]
                        self.logger.info(f"🎵 开始播放: {first_song.title}")
                        # 使用play_song方法，它会先加载歌曲再播放
                        self.state.play_song(first_song)
                    threading.Thread(target=auto_play).start()
                    
            else:
                self.logger.info("📋 数据库中暂无歌曲")
                self._add_fallback_songs()
                
        except Exception as e:
            self.logger.error(f"❌ 加载音乐库失败: {e}")
            self._add_fallback_songs()
    
    def _add_fallback_songs(self):
        """添加备用测试歌曲"""
        from hibiki.music.core.app_state import Song
        import os
        
        self.logger.info("🎵 添加备用测试歌曲...")
        
        test_songs = [
            Song(
                id="fallback_1",
                title="测试音频 - Ping",
                artist="macOS System",
                album="System Sounds",
                duration=1.0,
                file_path="/System/Library/Sounds/Ping.aiff"
            ),
            Song(
                id="fallback_2",
                title="测试音频 - Glass",
                artist="macOS System", 
                album="System Sounds",
                duration=1.5,
                file_path="/System/Library/Sounds/Glass.aiff"
            )
        ]
        
        valid_songs = [song for song in test_songs if os.path.exists(song.file_path)]
        if valid_songs:
            self.state.add_songs(valid_songs)
            self.state.set_playlist(valid_songs)
            self.state.current_song.value = valid_songs[0]
            self.songs_list.value = valid_songs
            self.logger.info(f"✅ 添加了 {len(valid_songs)} 首备用歌曲")
        else:
            self.logger.warning("⚠️ 没有找到有效的备用音频文件")
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def _create_song_list(self) -> Container:
        """创建歌曲列表"""
        song_items = []
        
        for i, song in enumerate(self.songs_list.value):
            # 每首歌的播放状态
            is_current_song = Computed(lambda idx=i: 
                self.state.current_song.value and 
                self.state.current_song.value.id == self.songs_list.value[idx].id if idx < len(self.songs_list.value) else False
            )
            
            is_playing = Computed(lambda idx=i: 
                is_current_song.value and self.state.is_playing.value
            )
            
            is_selected = Computed(lambda idx=i: self.selected_song_index.value == idx)
            
            song_item = SongListItem(
                title=song.title,
                artist=song.artist,
                duration=self._format_time(song.duration),
                is_playing=is_playing,
                is_selected=is_selected,
                on_click=lambda idx=i: self.select_song(idx),
                on_double_click=lambda idx=i: self.play_song(idx),
                style=ComponentStyle(width=px(440), height=px(48), margin_bottom=px(2))
            )
            
            song_items.append(song_item)
        
        return Container(
            children=song_items,
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                max_height=px(400)  # 限制最大高度，支持滚动
            )
        )
    
    def create_ui(self) -> Container:
        """创建专业音乐播放器界面"""
        
        # === 左侧面板: 专辑封面 + 当前歌曲信息 ===
        
        # 专辑封面
        album_art = AlbumArtView(
            image_path=self.current_album_art,
            size=180,
            on_click=lambda: self.logger.debug("🖼️ 点击专辑封面")
        )
        
        # 当前歌曲信息
        current_song_title = Label(
            lambda: self.state.current_song.value.title if self.state.current_song.value else "未选择歌曲",
            font_size=16,
            font_weight="bold",
            text_align="center",
            color="#2c3e50",
            style=ComponentStyle(margin_bottom=px(4))
        )
        
        current_song_artist = Label(
            lambda: self.state.current_song.value.artist if self.state.current_song.value else "",
            font_size=12,
            text_align="center", 
            color="#666",
            style=ComponentStyle(margin_bottom=px(8))
        )
        
        current_song_album = Label(
            lambda: f"专辑: {self.state.current_song.value.album}" if self.state.current_song.value and self.state.current_song.value.album else "",
            font_size=10,
            text_align="center",
            color="#999",
            style=ComponentStyle(margin_bottom=px(16))
        )
        
        # === 播放控制区域 ===
        
        # 播放控制按钮
        prev_btn = Button(
            "⏮️",
            style=ComponentStyle(width=px(35), height=px(35), margin_right=px(8)),
            on_click=lambda: self.state.previous_song()
        )
        
        play_pause_btn = Button(
            lambda: "⏸️" if self.state.is_playing.value else "▶️",
            style=ComponentStyle(width=px(40), height=px(35), margin_right=px(8)),
            on_click=lambda: self.state.toggle_play_pause()
        )
        
        next_btn = Button(
            "⏭️",
            style=ComponentStyle(width=px(35), height=px(35)),
            on_click=lambda: self.state.next_song()
        )
        
        # 播放控制容器
        playback_controls = Container(
            children=[prev_btn, play_pause_btn, next_btn],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                margin_bottom=px(16)
            )
        )
        
        # 自定义播放进度条
        progress_bar = MusicProgressBar(
            progress=self.state.position,
            duration=self.state.duration,
            on_seek=self.on_seek_to_position,
            style=ComponentStyle(width=px(250), height=px(20), margin_bottom=px(8))
        )
        
        # 播放时间显示
        time_display = Label(
            lambda: f"{self._format_time(self.state.position.value)} / {self._format_time(self.state.duration.value)}",
            font_size=10,
            text_align="center", 
            color="#666",
            style=ComponentStyle(margin_bottom=px(16))
        )
        
        # === 音量控制 ===
        
        volume_label = Label(
            "🔊 音量",
            font_size=11,
            text_align="center",
            color="#333",
            style=ComponentStyle(margin_bottom=px(6))
        )
        
        volume_slider = VolumeSlider(
            volume=self.state.volume,
            orientation="horizontal",
            on_volume_change=self.on_volume_change,
            style=ComponentStyle(width=px(140), height=px(18), margin_bottom=px(6))
        )
        
        volume_display = Label(
            lambda: f"{int(self.state.volume.value * 100)}%",
            font_size=10,
            text_align="center",
            color="#666"
        )
        
        # 左侧面板容器
        left_panel = Container(
            children=[
                album_art,
                current_song_title,
                current_song_artist, 
                current_song_album,
                playback_controls,
                progress_bar,
                time_display,
                volume_label,
                volume_slider,
                volume_display
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                padding=px(16),
                width=px(280)
            )
        )
        
        # === 右侧面板: 歌曲列表 ===
        
        playlist_title = Label(
            lambda: f"📋 播放列表 ({len(self.songs_list.value)} 首)",
            font_size=14,
            font_weight="bold",
            color="#2c3e50",
            style=ComponentStyle(margin_bottom=px(12))
        )
        
        # 创建歌曲列表项
        song_list_container = self._create_song_list()
        
        right_panel = Container(
            children=[playlist_title, song_list_container],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                padding=px(16),
                width=px(460)
            )
        )
        
        # === 主容器 ===
        main_content = Container(
            children=[left_panel, right_panel],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW
            )
        )
        
        # 应用标题
        app_title = Label(
            "🎵 Hibiki Music MVP v0.3 - 专业音乐播放器",
            font_size=18,
            font_weight="bold",
            text_align="center",
            color="#2c3e50",
            style=ComponentStyle(margin_bottom=px(16))
        )
        
        # 状态栏
        status_bar = Label(
            lambda: f"SQLModel数据库 | mutagen元数据 | AVPlayer引擎 | {self.state.total_songs.value}首歌曲 | {'▶️播放中' if self.state.is_playing.value else '⏸️暂停'}",
            font_size=10,
            text_align="center",
            color="#999",
            style=ComponentStyle(margin_top=px(12))
        )
        
        # 根容器
        root_container = Container(
            children=[app_title, main_content, status_bar],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                padding=px(16)
            )
        )
        
        return root_container
    
    # === 事件处理方法 ===
    
    def on_seek_to_position(self, position: float):
        """跳转到指定播放位置"""
        self.logger.info(f"🎯 跳转到位置: {position:.1f}秒")
        self.state.position.value = position
        
        # 如果有音频播放器，实际跳转
        if self.state.audio_player:
            self.state.audio_player.seek_to_position(position)
    
    def on_volume_change(self, volume: float):
        """音量变化处理"""
        self.logger.info(f"🔊 音量调节: {int(volume*100)}%")
        self.state.volume.value = volume
        
        # 如果有音频播放器，设置实际音量
        if self.state.audio_player:
            self.state.audio_player.set_volume(volume)
    
    def select_song(self, index: int):
        """选择歌曲"""
        if 0 <= index < len(self.songs_list.value):
            self.selected_song_index.value = index
            self.logger.info(f"🎵 选择歌曲: {self.songs_list.value[index].title}")
    
    def play_song(self, index: int):
        """播放歌曲"""
        if 0 <= index < len(self.songs_list.value):
            song = self.songs_list.value[index]
            self.selected_song_index.value = index
            self.state.play_song(song)
            self.logger.info(f"▶️ 播放歌曲: {song.title} - {song.artist}")
    
    def run(self):
        """运行应用程序"""
        try:
            self.logger.info("🚀 启动 Hibiki Music v0.3...")
            
            # 加载音乐库数据
            self._load_music_library()
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="🎵 Hibiki Music MVP v0.3 - 专业音乐播放器",
                width=780,
                height=620
            )
            
            # 创建并设置UI
            main_ui = self.create_ui()
            self.window.set_content(main_ui)
            
            self.logger.info("✅ Hibiki Music v0.3 已启动！")
            self.logger.info("🎯 新功能:")
            self.logger.info("  🎚️ 自定义播放进度条 (可点击跳转)")
            self.logger.info("  🔊 音量控制滑块")
            self.logger.info("  🖼️ 专辑封面显示")
            self.logger.info("  📋 专业歌曲列表 (点击选择，双击播放)")
            self.logger.info("  📱 完整响应式界面")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            self.logger.error(f"❌ 启动失败: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    app = HibikiMusicApp()
    app.run()