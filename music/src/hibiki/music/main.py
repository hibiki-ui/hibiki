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
        
    def _add_test_songs(self):
        """添加一些测试歌曲数据"""
        from hibiki.music.core.app_state import Song
        import os
        
        # 添加一些测试歌曲 (你可以替换为实际的音频文件路径)
        test_songs = [
            Song(
                id="test_1",
                title="测试歌曲 1",
                artist="测试艺术家",
                album="测试专辑",
                duration=180.0,
                file_path="/System/Library/Sounds/Ping.aiff"  # macOS 系统声音
            ),
            Song(
                id="test_2", 
                title="测试歌曲 2",
                artist="另一个艺术家",
                album="另一个专辑",
                duration=240.0,
                file_path="/System/Library/Sounds/Glass.aiff"  # macOS 系统声音
            )
        ]
        
        # 只添加存在的文件
        valid_songs = [song for song in test_songs if os.path.exists(song.file_path)]
        if valid_songs:
            self.state.add_songs(valid_songs)
            self.state.set_playlist(valid_songs)
            print(f"✅ 添加了 {len(valid_songs)} 首测试歌曲")
        else:
            print("⚠️ 没有找到有效的测试音频文件")
    
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
            lambda: f"音乐库: {self.state.total_songs.value} 首歌曲",
            style=ComponentStyle(margin_bottom=px(15)),
            font_size=16,
            text_align="center",
            color="#666"
        )
        
        # 当前播放信息
        current_playing_label = Label(
            lambda: f"正在播放: {self.state.current_song.value.title if self.state.current_song.value else '无'}",
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
            "这是 Hibiki Music 的 MVP v0.1 版本\n" +
            "展示了基于 Hibiki UI 的响应式状态管理\n" +
            "后续版本将添加实际的音频播放功能",
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
            
            # 添加测试歌曲数据
            self._add_test_songs()
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="Hibiki Music MVP v0.1",
                width=600,
                height=400
            )
            
            # 创建并设置UI
            main_ui = self.create_ui()
            self.window.set_content(main_ui)
            
            print("✅ Hibiki Music 已启动！")
            print("📝 当前版本: MVP v0.1")
            print("🎯 功能: 基础架构 + 响应式状态管理")
            
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