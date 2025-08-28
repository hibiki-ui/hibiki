#!/usr/bin/env python3
"""
🎵 Hibiki Music 主应用程序

基于 Hibiki UI 框架的智能音乐播放器 MVP
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
        print("🎵 初始化 Hibiki Music...")
        
        # 初始化应用状态
        self.state = MusicAppState()
        
        # 应用管理器
        self.app_manager = None
        self.window = None
        
        # UI状态
        self.songs_list = Signal([])
        self.selected_song_index = Signal(0)
        self.current_album_art = Signal(None)
        
        # 播放器状态映射 (从秒转换为进度比例)
        self.play_progress = Computed(lambda: 
            self.state.position.value / self.state.duration.value if self.state.duration.value > 0 else 0.0
        )
        
    def _load_music_library(self):
        """加载音乐库"""
        print("🔍 加载音乐库...")
        
        # 获取当前目录的music/data路径
        current_dir = Path(__file__).parent.parent.parent.parent  # music目录
        data_dir = current_dir / "data"
        
        # 首次扫描 - 如果data目录存在就扫描
        if data_dir.exists():
            print(f"📁 扫描目录: {data_dir}")
            try:
                scan_music_library(str(data_dir))
                print("✅ 音乐库扫描完成")
            except Exception as e:
                print(f"⚠️ 扫描失败: {e}")
        
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
                print(f"✅ 从数据库加载了 {len(app_songs)} 首歌曲")
                
                # 如果有歌曲，默认选中第一首
                if app_songs:
                    self.state.current_song.value = app_songs[0]
                    
            else:
                print("📋 数据库中暂无歌曲")
                self._add_fallback_songs()
                
        except Exception as e:
            print(f"❌ 加载音乐库失败: {e}")
            self._add_fallback_songs()
    
    def _add_fallback_songs(self):
        """添加备用测试歌曲"""
        from hibiki.music.core.app_state import Song
        import os
        
        print("🎵 添加备用测试歌曲...")
        
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
            print(f"✅ 添加了 {len(valid_songs)} 首备用歌曲")
        else:
            print("⚠️ 没有找到有效的备用音频文件")
    
    def create_ui(self) -> Container:
        """创建专业音乐播放器界面"""
        
        # 更新歌曲列表
        self._update_songs_list()
        
        # === 左侧面板: 专辑封面 + 当前歌曲信息 ===
        
        # 专辑封面
        album_art = AlbumArtView(
            image_path=self.current_album_art,
            size=200,
            on_click=lambda: print("🖼️ 点击专辑封面")
        )
        
        # 当前歌曲信息
        current_song_title = Label(
            lambda: self.state.current_song.value.title if self.state.current_song.value else "未选择歌曲",
            font_size=18,
            font_weight="bold",
            text_align="center",
            color="#2c3e50",
            style=ComponentStyle(margin_bottom=px(4))
        )
        
        current_song_artist = Label(
            lambda: self.state.current_song.value.artist if self.state.current_song.value else "",
            font_size=14,
            text_align="center", 
            color="#666",
            style=ComponentStyle(margin_bottom=px(8))
        )
        
        current_song_album = Label(
            lambda: f"专辑: {self.state.current_song.value.album}" if self.state.current_song.value and self.state.current_song.value.album else "",
            font_size=12,
            text_align="center",
            color="#999",
            style=ComponentStyle(margin_bottom=px(16))
        )
        
        # === 播放控制区域 ===
        
        # 播放控制按钮
        prev_btn = Button(
            "⏮️",
            style=ComponentStyle(width=px(40), height=px(40), margin_right=px(8)),
            on_click=lambda: self.state.previous_song()
        )
        
        play_pause_btn = Button(
            lambda: "⏸️" if self.state.is_playing.value else "▶️",
            style=ComponentStyle(width=px(50), height=px(40), margin_right=px(8)),
            on_click=lambda: self.state.toggle_play_pause()
        )
        
        next_btn = Button(
            "⏭️",
            style=ComponentStyle(width=px(40), height=px(40)),
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
            style=ComponentStyle(width=px(280), height=px(24), margin_bottom=px(8))
        )
        
        # 播放时间显示
        time_display = Label(
            lambda: f"{self._format_time(self.state.position.value)} / {self._format_time(self.state.duration.value)}",
            font_size=11,
            text_align="center", 
            color="#666",
            style=ComponentStyle(margin_bottom=px(20))
        )
        
        # === 音量控制 ===
        
        volume_label = Label(
            "音量控制",
            font_size=12,
            font_weight="bold",
            text_align="center",
            color="#333",
            style=ComponentStyle(margin_bottom=px(8))
        )
        
        volume_slider = VolumeSlider(
            volume=self.state.volume,
            orientation="horizontal",
            on_volume_change=self.on_volume_change,
            style=ComponentStyle(width=px(150), height=px(20), margin_bottom=px(8))
        )
        
        volume_display = Label(
            lambda: f"{int(self.state.volume.value * 100)}%",
            font_size=11,
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
                padding=px(20),
                width=px(320)
            )
        )
        
        # === 右侧面板: 歌曲列表 ===
        
        playlist_title = Label(
            lambda: f"播放列表 ({len(self.songs_list.value)} 首)",
            font_size=16,
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
                padding=px(20),
                width=px(480)
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
            font_size=20,
            font_weight="bold",
            text_align="center",
            color="#2c3e50",
            style=ComponentStyle(margin_bottom=px(20))
        )
        
        # 状态栏
        status_bar = Label(
            lambda: f"数据库: {self.state.total_songs.value} 首歌曲 | SQLModel + mutagen + AVPlayer | 状态: {'▶️ 播放中' if self.state.is_playing.value else '⏸️ 暂停'}",
            font_size=11,
            text_align="center",
            color="#999",
            style=ComponentStyle(margin_top=px(16))
        )
        
        # 根容器
        root_container = Container(
            children=[app_title, main_content, status_bar],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                padding=px(20)
            )
        )
        
        return root_container
        play_pause_btn = Button(
            lambda: "⏸️ 暂停" if self.state.is_playing.value else "▶️ 播放",
            style=ComponentStyle(width=px(100), height=px(35), margin_right=px(10)),
            on_click=lambda: self.state.toggle_play_pause()
        )
        
        previous_btn = Button(
            "⏮️ 上一首",
            style=ComponentStyle(width=px(100), height=px(35), margin_right=px(10)),
            on_click=lambda: self.state.previous_song()
        )
        
        next_btn = Button(
            "⏭️ 下一首", 
            style=ComponentStyle(width=px(100), height=px(35)),
            on_click=lambda: self.state.next_song()
        )
        
        # 播放控制容器
        playback_controls = Container(
            children=[previous_btn, play_pause_btn, next_btn],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                margin_bottom=px(20)
            )
        )
        
        # 说明文字
        description_label = Label(
            "🎵 Hibiki Music MVP v0.2 - 真实音乐库版本\n" +
            "✅ SQLModel 数据库 + mutagen 元数据提取\n" +
            "✅ AVPlayer 音频播放引擎 + 响应式状态管理",
            style=ComponentStyle(margin_top=px(30)),
            font_size=12,
            text_align="center",
            color="#999"
        )
        
        # 主容器
        main_container = Container(
            children=[
                title_label,
                status_label,
                current_playing_label,
                play_status_label,
                progress_label,
                playback_controls,
                description_label
            ],
            style=ComponentStyle(
                padding=px(40),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER
            )
        )
        
        return main_container
        
    def run(self):
        """运行应用程序"""
        try:
            print("🚀 启动 Hibiki Music...")
            
            # 加载音乐库数据
            self._load_music_library()
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="Hibiki Music MVP v0.2 - 真实音乐库",
                width=700,
                height=450
            )
            
            # 创建并设置UI
            main_ui = self.create_ui()
            self.window.set_content(main_ui)
            
            print("✅ Hibiki Music 已启动！")
            print("📝 当前版本: MVP v0.2")
            print("🎯 功能: 音乐库扫描 + SQLModel数据库 + AVPlayer播放")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    app = HibikiMusicApp()
    app.run()