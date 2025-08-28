#!/usr/bin/env python3
"""
🎵 Hibiki Music 自定义组件使用示例

展示如何在音乐应用中使用自定义UI组件
"""

from hibiki.ui import (
    ManagerFactory, Container, Label, Button, ComponentStyle, px,
    Display, FlexDirection, AlignItems, JustifyContent, Signal
)

# 导入自定义音乐组件
from src.hibiki.music.ui.components import (
    MusicProgressBar, AlbumArtView, VolumeSlider, SongListItem
)

class MusicPlayerDemo:
    """音乐播放器自定义组件演示"""
    
    def __init__(self):
        print("🎵 初始化音乐播放器自定义组件演示...")
        
        # 模拟播放器状态
        self.current_position = Signal(45.0)  # 当前播放位置(秒)
        self.total_duration = Signal(180.0)   # 总时长(秒)
        self.volume = Signal(0.7)             # 音量 0.0-1.0
        self.is_muted = Signal(False)         # 静音状态
        self.album_art_path = Signal(None)    # 专辑封面路径
        self.is_playing = Signal(True)        # 播放状态
        
        # 歌曲列表状态
        self.selected_song = Signal(0)
        
        self.app_manager = None
        self.window = None
        
    def create_ui(self) -> Container:
        """创建带自定义组件的UI"""
        
        # === 专辑封面区域 ===
        album_art = AlbumArtView(
            image_path=self.album_art_path,
            size=150,
            on_click=lambda: print("🖼️ 点击了专辑封面")
        )
        
        # === 播放进度条 ===
        progress_bar = MusicProgressBar(
            progress=self.current_position,
            duration=self.total_duration,
            on_seek=self.on_seek_to_position,
            style=ComponentStyle(width=px(400), height=px(24))
        )
        
        # === 音量控制 ===
        volume_slider = VolumeSlider(
            volume=self.volume,
            is_muted=self.is_muted,
            orientation="horizontal",
            on_volume_change=self.on_volume_change,
            style=ComponentStyle(width=px(120), height=px(24))
        )
        
        # === 播放控制按钮 ===
        play_pause_btn = Button(
            lambda: "⏸️ 暂停" if self.is_playing.value else "▶️ 播放",
            style=ComponentStyle(width=px(80), height=px(32)),
            on_click=self.toggle_play_pause
        )
        
        prev_btn = Button(
            "⏮️",
            style=ComponentStyle(width=px(40), height=px(32)),
            on_click=lambda: print("⏮️ 上一首")
        )
        
        next_btn = Button(
            "⏭️",
            style=ComponentStyle(width=px(40), height=px(32)),
            on_click=lambda: print("⏭️ 下一首")
        )
        
        # 控制按钮容器
        controls_container = Container(
            children=[prev_btn, play_pause_btn, next_btn],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                gap=px(8),
                margin_bottom=px(16)
            )
        )
        
        # === 歌曲列表 ===
        songs_data = [
            {"title": "不想睡", "artist": "周深", "duration": "5:36"},
            {"title": "亲爱的旅人啊", "artist": "周深", "duration": "4:04"},
            {"title": "放心去飞", "artist": "周深", "duration": "3:50"},
            {"title": "庸人自扰", "artist": "小虎队", "duration": "4:22"}
        ]
        
        song_list_items = []
        for i, song in enumerate(songs_data):
            is_selected = Signal(False)
            is_playing_song = Signal(i == 0 and self.is_playing.value)
            
            song_item = SongListItem(
                title=song["title"],
                artist=song["artist"], 
                duration=song["duration"],
                is_playing=is_playing_song,
                is_selected=is_selected,
                on_click=lambda idx=i: self.select_song(idx),
                on_double_click=lambda idx=i: self.play_song(idx),
                style=ComponentStyle(width=px(500), height=px(50))
            )
            
            song_list_items.append(song_item)
        
        # === 状态信息标签 ===
        progress_label = Label(
            lambda: f"播放进度: {int(self.current_position.value//60)}:{int(self.current_position.value%60):02d} / {int(self.total_duration.value//60)}:{int(self.total_duration.value%60):02d}",
            style=ComponentStyle(margin_bottom=px(8)),
            font_size=12,
            color="#666"
        )
        
        volume_label = Label(
            lambda: f"音量: {int(self.volume.value*100)}%" + (" (静音)" if self.is_muted.value else ""),
            style=ComponentStyle(margin_bottom=px(8)),
            font_size=12,
            color="#666"
        )
        
        # === 主布局 ===
        
        # 左侧：专辑封面和控制
        left_panel = Container(
            children=[
                album_art,
                Label("周深 - 不想睡", font_size=16, font_weight="bold", text_align="center"),
                Label("专辑: 不想睡", font_size=12, color="#666", text_align="center"),
                controls_container,
                progress_bar,
                progress_label
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                padding=px(20),
                width=px(300)
            )
        )
        
        # 右侧：歌曲列表
        right_panel = Container(
            children=[
                Label("播放列表", font_size=18, font_weight="bold", margin_bottom=px(12)),
                *song_list_items
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                padding=px(20),
                width=px(520)
            )
        )
        
        # 底部：音量控制
        bottom_panel = Container(
            children=[
                Label("音量控制", font_size=14, font_weight="bold"),
                volume_slider,
                volume_label
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                padding=px(20)
            )
        )
        
        # 主容器
        main_container = Container(
            children=[
                Container(
                    children=[left_panel, right_panel],
                    style=ComponentStyle(
                        display=Display.FLEX,
                        flex_direction=FlexDirection.ROW
                    )
                ),
                bottom_panel
            ],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                padding=px(20)
            )
        )
        
        return main_container
    
    # === 事件处理方法 ===
    
    def on_seek_to_position(self, position: float):
        """跳转到指定播放位置"""
        print(f"🎯 跳转到位置: {position:.1f}秒")
        self.current_position.value = position
    
    def on_volume_change(self, volume: float):
        """音量变化处理"""
        print(f"🔊 音量调节: {int(volume*100)}%")
        self.volume.value = volume
        if volume > 0:
            self.is_muted.value = False
    
    def toggle_play_pause(self):
        """切换播放/暂停"""
        self.is_playing.value = not self.is_playing.value
        state = "播放" if self.is_playing.value else "暂停"
        print(f"⏯️ {state}")
    
    def select_song(self, index: int):
        """选择歌曲"""
        print(f"🎵 选择歌曲 {index}")
        self.selected_song.value = index
    
    def play_song(self, index: int):
        """播放歌曲"""
        print(f"▶️ 播放歌曲 {index}")
        self.selected_song.value = index
        self.is_playing.value = True
        self.current_position.value = 0.0
    
    def simulate_playback_progress(self):
        """模拟播放进度更新 (实际应用中由音频播放器驱动)"""
        import threading
        import time
        
        def update_progress():
            while True:
                if self.is_playing.value and self.current_position.value < self.total_duration.value:
                    self.current_position.value += 1.0
                    if self.current_position.value >= self.total_duration.value:
                        self.is_playing.value = False
                        self.current_position.value = 0.0
                time.sleep(1.0)
        
        thread = threading.Thread(target=update_progress, daemon=True)
        thread.start()
    
    def run(self):
        """运行演示应用"""
        try:
            print("🚀 启动自定义组件演示...")
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="🎵 Hibiki Music - 自定义组件演示",
                width=900,
                height=700
            )
            
            # 创建并设置UI
            main_ui = self.create_ui()
            self.window.set_content(main_ui)
            
            # 启动模拟播放进度
            self.simulate_playback_progress()
            
            print("✅ 自定义组件演示已启动！")
            print("🎯 展示功能:")
            print("  📀 专辑封面显示")
            print("  📊 自定义播放进度条 (可点击跳转)")
            print("  🔊 音量滑块控制")
            print("  📋 歌曲列表项 (点击选择，双击播放)")
            print("  ⏯️ 播放控制按钮")
            print("  📱 响应式状态同步")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    demo = MusicPlayerDemo()
    demo.run()