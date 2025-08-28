#!/usr/bin/env python3
"""
🎵 Hibiki Music 主应用程序

基于 Hibiki UI 框架的智能音乐播放器 MVP
"""

from hibiki.ui import (
    ManagerFactory, Label, Button, Container, ComponentStyle, px,
    Display, FlexDirection, AlignItems, JustifyContent
)
from hibiki.music.core.app_state import MusicAppState
from hibiki.music.core.scanner import scan_music_library
from hibiki.music.data.database import SongService
from pathlib import Path

class HibikiMusicApp:
    """
    Hibiki Music 主应用程序类
    
    MVP v0.1 功能：
    - 基础应用架构
    - 响应式状态管理
    - 简单的UI界面
    """
    
    def __init__(self):
        print("🎵 初始化 Hibiki Music...")
        
        # 初始化应用状态
        self.state = MusicAppState()
        
        # 应用管理器
        self.app_manager = None
        self.window = None
        
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
        """创建主界面"""
        
        # 标题
        title_label = Label(
            "🎵 Hibiki Music MVP v0.1",
            style=ComponentStyle(margin_bottom=px(20)),
            font_size=24,
            font_weight="bold",
            text_align="center",
            color="#2c3e50"
        )
        
        # 状态信息
        status_label = Label(
            lambda: f"音乐库: {self.state.total_songs.value} 首歌曲 | 数据库: SQLModel + SQLite",
            style=ComponentStyle(margin_bottom=px(15)),
            font_size=16,
            text_align="center",
            color="#666"
        )
        
        # 当前播放信息
        current_playing_label = Label(
            lambda: f"正在播放: {self.state.current_song.value.title + ' - ' + self.state.current_song.value.artist if self.state.current_song.value else '无'}",
            style=ComponentStyle(margin_bottom=px(15)),
            font_size=14,
            text_align="center",
            color="#333"
        )
        
        # 播放状态和进度
        play_status_label = Label(
            lambda: f"状态: {'播放中' if self.state.is_playing.value else '已暂停'}",
            style=ComponentStyle(margin_bottom=px(10)),
            font_size=14,
            text_align="center",
            color=lambda: "#007AFF" if self.state.is_playing.value else "#666"
        )
        
        progress_label = Label(
            lambda: f"进度: {self.state.position.value:.1f}s / {self.state.duration.value:.1f}s",
            style=ComponentStyle(margin_bottom=px(20)),
            font_size=12,
            text_align="center",
            color="#999"
        )
        
        # 播放控制按钮
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