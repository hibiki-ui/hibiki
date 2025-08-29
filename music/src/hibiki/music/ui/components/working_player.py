#!/usr/bin/env python3
"""
🎵 实用版现代音乐播放器组件

使用Hibiki UI实际支持的功能，确保界面可用
避免使用不支持的样式属性，专注于功能实现
"""

import threading
import os
from hibiki.ui import (
    Label, Button, Container, Slider,
    ComponentStyle, px, Display, FlexDirection, 
    JustifyContent, AlignItems, Signal, Effect
)
from ..themes.modern_theme import ModernTheme
from ...core.app_state import MusicAppState
from ..styling.enhanced_styling import enhance_view_styling, create_reactive_styling
from .image_container import SimpleImageContainer
from hibiki.ui.core.logging import get_logger

logger = get_logger("ui.working_player")

class WorkingMusicPlayer:
    """实用版音乐播放器类"""
    
    def __init__(self, state: MusicAppState):
        self.state = state
        self.current_lyric_index = 0
        self.lyrics = [
            "♪ 不想睡 不想睡",
            "🎵 夜深了还不想入眠", 
            "✨ 思念在心中蔓延",
            "🌟 这首歌伴我到天明",
            "💫 美好的旋律在心间"
        ]
        
        # 获取主题（但不使用复杂样式）
        theme = ModernTheme()
        self.colors = theme.colors
        
        # 创建响应式UI元素
        self.song_title_label = None
        self.lyric_label = None
        self.play_button = None
        self.time_label = None
        
        self._setup_auto_updates()
    
    def _setup_auto_updates(self):
        """设置自动更新效果"""
        
        # 定期更新歌词
        def update_lyrics():
            import time
            
            def lyrics_updater():
                while True:
                    if hasattr(self, 'lyric_label') and self.lyric_label:
                        # 简化实现，避免复杂的Signal更新
                        pass
                    time.sleep(3)  # 每3秒更新一次歌词
            
            thread = threading.Thread(target=lyrics_updater, daemon=True)
            thread.start()
        
        # 延迟启动歌词更新
        threading.Timer(1.0, update_lyrics).start()
    
    def create_header_section(self):
        """创建头部区域"""
        title = Label(
            "🎵 Hibiki Music Player",
            font_size=26,
            font_weight='bold',
            color='#ffffff'  # 使用深色主题白色文字
        )
        
        subtitle = Label(
            "现代化音乐播放体验",
            font_size=14,
            color='#b3b3b3'  # 使用主题次要文字颜色
        )
        
        header_style = ComponentStyle(
            width=px(800),  # 固定宽度
            height=px(80),  # 固定高度
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.CENTER,
            gap=px(8),
            # 添加增强样式属性
            background_color=self.colors.bg_secondary,
            border_radius=px(16),
            opacity=0.95
        )
        
        header_container = Container(
            children=[title, subtitle],
            style=header_style
        )
        
        # 应用增强样式
        def apply_header_styling():
            if hasattr(header_container, '_nsview') and header_container._nsview:
                enhance_view_styling(header_container._nsview, header_style)
        
        # 延迟应用样式，确保视图已创建
        threading.Timer(0.1, apply_header_styling).start()
        
        return header_container
    
    def create_album_section(self):
        """创建专辑区域"""
        # 专辑封面 - 使用实际图片
        # 直接使用已知的绝对路径
        album_image_path = "/Users/david/david/app/hibiki-ui/music/assets/images/album_placeholder.png"
        
        logger.debug(f"🔍 查找专辑封面路径: {album_image_path}")
        
        # 创建专辑封面图片容器
        if os.path.exists(album_image_path):
            logger.info(f"🖼️ 使用专辑封面图片: {album_image_path}")
            album_art = SimpleImageContainer(
                image_path=album_image_path,
                width=140,
                height=140
            )
        else:
            logger.warning(f"⚠️ 专辑封面不存在，使用备用显示")
            # 备用显示
            album_art = Container(
                children=[
                    Label("🎵", font_size=80, color=self.colors.accent_primary),
                    Label("专辑封面", font_size=10, color=self.colors.text_tertiary)
                ],
                style=ComponentStyle(
                    width=px(140), height=px(140),
                    display=Display.FLEX, flex_direction=FlexDirection.COLUMN,
                    align_items=AlignItems.CENTER, justify_content=JustifyContent.CENTER
                )
            )
        
        # 歌曲标题（使用当前歌曲信息）
        song_info = self.state.current_song.value if self.state.current_song.value else {}
        song_title = song_info.get('title', '暂无播放')
        artist_name = song_info.get('artist', '未知艺术家')
        album_name = song_info.get('album', '未知专辑')
        
        self.song_title_label = Label(
            song_title,
            font_size=20,  # 增加字体大小
            font_weight='bold',
            color=self.colors.text_primary  # 使用主题主要文字颜色
        )
        
        # 艺术家信息
        artist_label = Label(
            f"艺术家：{artist_name}",
            font_size=16,  # 增加字体大小
            color=self.colors.text_secondary  # 使用主题次要文字颜色
        )
        
        # 专辑信息
        album_label = Label(
            f"专辑：{album_name}",
            font_size=14,  # 增加字体大小
            color=self.colors.text_tertiary  # 使用主题辅助文字颜色
        )
        
        album_style = ComponentStyle(
            width=px(400),  # 增加宽度
            height=px(320), # 增加高度
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.CENTER,
            gap=px(12),     # 增加间距
            # 增强样式
            background_color=self.colors.bg_card,
            border_radius=px(20),
            opacity=0.92
        )
        
        album_container = Container(
            children=[album_art, self.song_title_label, artist_label, album_label],
            style=album_style
        )
        
        # 应用增强样式
        def apply_album_styling():
            if hasattr(album_container, '_nsview') and album_container._nsview:
                enhance_view_styling(album_container._nsview, album_style)
        
        threading.Timer(0.1, apply_album_styling).start()
        
        return album_container
    
    def create_lyrics_section(self):
        """创建歌词区域"""
        lyrics_title = Label(
            "🎤 实时歌词",
            font_size=18,
            font_weight='bold',
            color=self.colors.accent_primary  # 使用品牌色
        )
        
        # 当前歌词
        self.lyric_label = Label(
            "♪ 不想睡 不想睡",
            font_size=16,
            font_weight='medium',
            color=self.colors.text_primary  # 使用主要文字颜色
        )
        
        # 下一句歌词预览
        next_lyric = Label(
            "🎵 夜深了还不想入眠",
            font_size=14,
            color=self.colors.text_secondary  # 使用次要文字颜色
        )
        
        lyrics_style = ComponentStyle(
            width=px(400),  # 增加宽度
            height=px(320), # 增加高度
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.CENTER,
            gap=px(18),     # 增加间距
            # 增强样式
            background_color=self.colors.bg_card,
            border_radius=px(20),
            opacity=0.92,
            border="1px solid rgba(29,185,84,0.3)"  # 增强绿色边框
        )
        
        lyrics_container = Container(
            children=[lyrics_title, self.lyric_label, next_lyric],
            style=lyrics_style
        )
        
        # 应用增强样式
        def apply_lyrics_styling():
            if hasattr(lyrics_container, '_nsview') and lyrics_container._nsview:
                enhance_view_styling(lyrics_container._nsview, lyrics_style)
        
        threading.Timer(0.1, apply_lyrics_styling).start()
        
        return lyrics_container
    
    def create_main_content(self):
        """创建主内容区域"""
        album_section = self.create_album_section()
        lyrics_section = self.create_lyrics_section()
        
        return Container(
            children=[album_section, lyrics_section],
            style=ComponentStyle(
                width=px(900),  # 增加宽度
                height=px(360), # 增加高度
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                gap=px(60)      # 调整间距
            )
        )
    
    def create_controls_section(self):
        """创建控制区域"""
        # 播放控制按钮
        prev_btn = Button(
            "⏮",
            style=ComponentStyle(width=px(50), height=px(40)),
            on_click=lambda: self.previous_track()
        )
        
        # 播放/暂停按钮
        play_icon = "⏸️" if self.state.is_playing.value else "▶️"
        self.play_button = Button(
            play_icon,
            style=ComponentStyle(width=px(60), height=px(50)),
            on_click=lambda: self.toggle_play()
        )
        
        next_btn = Button(
            "⏭",
            style=ComponentStyle(width=px(50), height=px(40)),
            on_click=lambda: self.next_track()
        )
        
        # 按钮容器
        buttons_container = Container(
            children=[prev_btn, self.play_button, next_btn],
            style=ComponentStyle(
                width=px(200),
                height=px(60),
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                gap=px(15)
            )
        )
        
        # 进度条和时间 - 合在一个容器
        progress_slider = Slider(
            self.state.position,
            min_value=0,
            max_value=int(self.state.duration.value) if self.state.duration.value > 0 else 210,
            style=ComponentStyle(
                width=px(400),
                height=px(20)
            )
        )
        
        self.time_label = Label(
            f"{self.format_time(self.state.position.value)} / {self.format_time(self.state.duration.value)}",
            font_size=12,
            color='#7f8c8d'
        )
        
        progress_container = Container(
            children=[progress_slider, self.time_label],
            style=ComponentStyle(
                width=px(450),
                height=px(60),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.CENTER,
                gap=px(8)
            )
        )
        
        # 音量控制
        volume_label = Label("🔊", font_size=14, color='#95a5a6')
        volume_slider = Slider(
            self.state.volume,
            min_value=0,
            max_value=1,
            style=ComponentStyle(width=px(120), height=px(15))
        )
        
        volume_container = Container(
            children=[volume_label, volume_slider],
            style=ComponentStyle(
                width=px(150),
                height=px(60),
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.CENTER,
                gap=px(8)
            )
        )
        
        return Container(
            children=[buttons_container, progress_container, volume_container],
            style=ComponentStyle(
                width=px(800),  # 固定宽度
                height=px(120), # 固定高度
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                justify_content=JustifyContent.CENTER,
                gap=px(10)
            )
        )
    
    def create_full_interface(self):
        """创建完整界面"""
        logger.info("🎨 创建实用版音乐播放器界面")
        
        header = self.create_header_section()
        main_content = self.create_main_content()
        controls = self.create_controls_section()
        
        main_style = ComponentStyle(
            width=px(1000), # 增加总宽度
            height=px(700),  # 增加总高度
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            align_items=AlignItems.CENTER,
            justify_content=JustifyContent.CENTER,
            gap=px(25),      # 调整间距
            # 深色主题背景
            background_color=self.colors.bg_primary,
            border_radius=px(24),
            opacity=1.0
        )
        
        main_container = Container(
            children=[header, main_content, controls],
            style=main_style
        )
        
        # 应用增强样式
        def apply_main_styling():
            if hasattr(main_container, '_nsview') and main_container._nsview:
                enhance_view_styling(main_container._nsview, main_style)
        
        threading.Timer(0.1, apply_main_styling).start()
        
        logger.info("✅ 实用版音乐播放器界面创建完成")
        return main_container
    
    def format_time(self, seconds):
        """格式化时间显示"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def toggle_play(self):
        """切换播放状态"""
        self.state.is_playing.value = not self.state.is_playing.value
        logger.info(f"🎵 播放状态切换: {'播放中' if self.state.is_playing.value else '暂停'}")
    
    def previous_track(self):
        """上一曲"""
        logger.info("⏮ 上一曲")
    
    def next_track(self):
        """下一曲"""
        logger.info("⏭ 下一曲")