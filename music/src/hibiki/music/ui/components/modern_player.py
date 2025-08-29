#!/usr/bin/env python3
"""
🎵 现代化音乐播放器组件集合

使用增强样式系统实现的完整现代UI组件
包含专辑封面、滚动歌词、播放控制等核心组件
"""

from hibiki.ui import (
    Component, UIComponent, Container, Label, Button, Slider,
    ComponentStyle, px, Display, FlexDirection, JustifyContent, AlignItems,
    Signal, Computed, Effect
)
from ..styling import StylableViewMixin, create_reactive_styling
from ..themes.modern_theme import ModernTheme
from ...core.app_state import MusicAppState
from hibiki.ui.core.logging import get_logger

logger = get_logger("ui.modern_player")

class AlbumArtCard(Container, StylableViewMixin):
    """专辑封面卡片组件 - 带阴影和圆角效果"""
    
    def __init__(self, state: MusicAppState):
        self.state = state
        
        # 获取主题颜色
        theme = ModernTheme()
        self.colors = theme.colors
        
        # 专辑封面占位图
        album_placeholder = Label(
            "🎵",
            font_size=80,
            color=self.colors.text_secondary
        )
        
        # 歌曲标题
        song_title = Label(
            lambda: self.state.current_song.value.get('title', '暂无播放') if self.state.current_song.value else '暂无播放',
            font_size=18,
            font_weight='bold',
            color=self.colors.text_primary
        )
        
        # 艺术家名称
        artist_name = Label(
            lambda: self.state.current_song.value.get('artist', '未知艺术家') if self.state.current_song.value else '未知艺术家',
            font_size=14,
            color=self.colors.text_secondary
        )
        
        # 专辑信息容器
        info_container = Container(
            children=[song_title, artist_name],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(4)
            )
        )
        
        # 卡片样式
        card_style = ComponentStyle(
            width=px(280),
            height=px(320),
            background_color=self.colors.bg_card,
            border_radius=px(16),
            border=f'1px solid {self.colors.bg_secondary}',
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            justify_content=JustifyContent.CENTER,
            align_items=AlignItems.CENTER,
            gap=px(16)
        )
        
        Container.__init__(self, children=[album_placeholder, info_container], style=card_style)
        StylableViewMixin.__init__(self)
    
    def _create_nsview(self):
        nsview = super()._create_nsview()
        # 应用增强样式
        self.apply_enhanced_style(self.style)
        return nsview

class ScrollingLyricsPanel(Container, StylableViewMixin):
    """滚动歌词面板组件"""
    
    def __init__(self, state: MusicAppState):
        self.state = state
        
        # 获取主题颜色
        theme = ModernTheme()
        self.colors = theme.colors
        
        # 模拟当前歌词行
        self.current_lyric_line = Signal("♪ 这里是当前歌词行")
        self.next_lyric_line = Signal("下一行歌词预览...")
        self.prev_lyric_line = Signal("上一行歌词...")
        
        # 歌词标题
        lyrics_title = Label(
            "🎤 实时歌词",
            font_size=16,
            font_weight='bold',
            color=self.colors.text_primary
        )
        
        # 上一行歌词（淡出效果）
        prev_lyric = Label(
            lambda: self.prev_lyric_line.value,
            font_size=12,
            color=self.colors.text_tertiary,
            style=ComponentStyle(
                opacity=0.5
            )
        )
        
        # 当前歌词行（高亮）
        current_lyric = Label(
            lambda: self.current_lyric_line.value,
            font_size=16,
            font_weight='bold',
            color=self.colors.accent_primary,
            style=ComponentStyle(
                background_color=f'rgba(29,185,84,0.1)',
                border_radius=px(8),
                opacity=1.0
            )
        )
        
        # 下一行歌词（预览）
        next_lyric = Label(
            lambda: self.next_lyric_line.value,
            font_size=14,
            color=self.colors.text_secondary,
            style=ComponentStyle(
                opacity=0.7
            )
        )
        
        # 歌词容器
        lyrics_container = Container(
            children=[prev_lyric, current_lyric, next_lyric],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(8),
                align_items=AlignItems.CENTER
            )
        )
        
        # 面板样式
        panel_style = ComponentStyle(
            width=px(360),
            height=px(320),
            background_color='rgba(0,0,0,0.6)',
            border_radius=px(12),
            border=f'1px solid {self.colors.bg_secondary}',
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(16)
        )
        
        Container.__init__(self, children=[lyrics_title, lyrics_container], style=panel_style)
        StylableViewMixin.__init__(self)
        
        # 设置歌词滚动动画
        self._setup_lyrics_animation()
    
    def _create_nsview(self):
        nsview = super()._create_nsview()
        # 应用增强样式
        self.apply_enhanced_style(self.style)
        return nsview
    
    def _setup_lyrics_animation(self):
        """设置歌词滚动动画效果"""
        import threading
        import time
        
        def animate_lyrics():
            lyrics_samples = [
                ("前一行示例歌词", "🎵 当前播放歌词行", "下一行即将出现"),
                ("🎵 当前播放歌词行", "✨ 优美的旋律在流淌", "歌声带来无尽遐想"),
                ("✨ 优美的旋律在流淌", "🌟 每个音符都有故事", "诉说着心中的情感"),
                ("🌟 每个音符都有故事", "🎭 音乐是灵魂的语言", "跨越时空的桥梁"),
                ("🎭 音乐是灵魂的语言", "♪ 让我们一起感受", "这美妙的音乐世界"),
            ]
            
            while True:
                for prev, current, next_line in lyrics_samples:
                    self.prev_lyric_line.value = prev
                    self.current_lyric_line.value = current
                    self.next_lyric_line.value = next_line
                    time.sleep(2.5)  # 每2.5秒切换一次
        
        # 启动动画线程
        animation_thread = threading.Thread(target=animate_lyrics, daemon=True)
        animation_thread.start()

class PlaybackControls(Container, StylableViewMixin):
    """播放控制组件"""
    
    def __init__(self, state: MusicAppState):
        self.state = state
        
        # 获取主题颜色
        theme = ModernTheme()
        self.colors = theme.colors
        
        # 上一曲按钮
        prev_button = Button(
            "⏮",
            font_size=24,
            style=ComponentStyle(
                width=px(50),
                height=px(50),
                background_color=self.colors.bg_secondary,
                border_radius=px(25),
                border=f'1px solid {self.colors.bg_card}'
            ),
            on_click=lambda: self._previous_track()
        )
        
        # 播放/暂停按钮（主按钮）
        play_pause_button = Button(
            lambda: "⏸️" if self.state.is_playing.value else "▶️",
            font_size=32,
            style=ComponentStyle(
                width=px(70),
                height=px(70),
                background_color=self.colors.accent_primary,
                border_radius=px(35),
                border='2px solid rgba(255,255,255,0.2)'
            ),
            on_click=lambda: self._toggle_play()
        )
        
        # 下一曲按钮
        next_button = Button(
            "⏭",
            font_size=24,
            style=ComponentStyle(
                width=px(50),
                height=px(50),
                background_color=self.colors.bg_secondary,
                border_radius=px(25),
                border=f'1px solid {self.colors.bg_card}'
            ),
            on_click=lambda: self._next_track()
        )
        
        # 按钮容器
        buttons_container = Container(
            children=[prev_button, play_pause_button, next_button],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                gap=px(20)
            )
        )
        
        # 进度条
        progress_slider = Slider(
            self.state.position,
            min_value=0,
            max_value=lambda: self.state.duration.value,
            style=ComponentStyle(
                width=px(300),
                height=px(6)
            )
        )
        
        # 时间显示
        time_display = Label(
            lambda: f"{self._format_time(self.state.position.value)} / {self._format_time(self.state.duration.value)}",
            font_size=12,
            color=self.colors.text_secondary
        )
        
        # 控制面板样式
        controls_style = ComponentStyle(
            background_color='rgba(0,0,0,0.4)',
            border_radius=px(20),
            border=f'1px solid {self.colors.bg_secondary}',
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(16)
        )
        
        Container.__init__(
            self, 
            children=[buttons_container, progress_slider, time_display],
            style=controls_style
        )
        StylableViewMixin.__init__(self)
    
    def _create_nsview(self):
        nsview = super()._create_nsview()
        # 应用增强样式
        self.apply_enhanced_style(self.style)
        return nsview
    
    def _toggle_play(self):
        """切换播放/暂停状态"""
        self.state.is_playing.value = not self.state.is_playing.value
        logger.info(f"🎵 播放状态切换: {'播放中' if self.state.is_playing.value else '暂停'}")
    
    def _previous_track(self):
        """上一曲"""
        logger.info("⏮ 上一曲")
    
    def _next_track(self):
        """下一曲"""
        logger.info("⏭ 下一曲")
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

class ModernPlayerWindow(UIComponent, StylableViewMixin):
    """现代化音乐播放器主窗口"""
    
    def __init__(self, state: MusicAppState):
        self.state = state
        
        # 获取主题颜色
        theme = ModernTheme()
        self.colors = theme.colors
        
        # 主窗口样式
        main_style = ComponentStyle(
            background_color=self.colors.bg_primary,
            border_radius=px(24),
            border=f'2px solid {self.colors.bg_secondary}',
            display=Display.FLEX,
            flex_direction=FlexDirection.COLUMN,
            gap=px(24)
        )
        
        UIComponent.__init__(self, style=main_style)
        StylableViewMixin.__init__(self)
    
    def create_header(self) -> Container:
        """创建顶部标题栏"""
        title_label = Label(
            "🎵 Hibiki Music Player",
            font_size=28,
            font_weight='bold',
            color=self.colors.text_primary,
            style=ComponentStyle(
                background_color=f'rgba(29,185,84,0.1)',
                border_radius=px(12),
                border=f'2px solid {self.colors.accent_primary}'
            )
        )
        
        subtitle_label = Label(
            "现代化音乐播放体验",
            font_size=14,
            color=self.colors.text_secondary
        )
        
        header_container = Container(
            children=[title_label, subtitle_label],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER,
                gap=px(8),
                background_color='rgba(255,255,255,0.03)',
                border_radius=px(16),
                border=f'1px solid {self.colors.bg_secondary}'
            )
        )
        
        return header_container
    
    def create_main_content(self) -> Container:
        """创建主内容区域"""
        # 专辑封面组件
        album_art_card = AlbumArtCard(self.state)
        
        # 歌词面板组件  
        lyrics_panel = ScrollingLyricsPanel(self.state)
        
        # 主内容容器（左右布局）
        main_content = Container(
            children=[album_art_card, lyrics_panel],
            style=ComponentStyle(
                display=Display.FLEX,
                flex_direction=FlexDirection.ROW,
                justify_content=JustifyContent.CENTER,
                align_items=AlignItems.CENTER,
                gap=px(32)
            )
        )
        
        return main_content
    
    def create_bottom_controls(self) -> Container:
        """创建底部控制区域"""
        return PlaybackControls(self.state)
    
    def _create_nsview(self):
        """创建主窗口内容"""
        logger.info("🎨 创建现代化音乐播放器窗口")
        
        # 创建各个区域
        header = self.create_header()
        main_content = self.create_main_content()
        bottom_controls = self.create_bottom_controls()
        
        # 主容器
        main_container = Container(
            children=[header, main_content, bottom_controls],
            style=ComponentStyle(
                background_color=self.colors.bg_primary,
                border_radius=px(24),
                border=f'2px solid {self.colors.bg_secondary}',
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                gap=px(24)
            )
        )
        
        # 应用增强样式
        if hasattr(main_container, 'apply_enhanced_style'):
            main_container.apply_enhanced_style(main_container.style)
        
        logger.info("✅ 现代化播放器窗口创建完成")
        
        return main_container._create_nsview()