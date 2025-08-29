#!/usr/bin/env python3
"""
🎵 Hibiki Music UI Components

音乐播放器专用UI组件库
"""

# 导入主题和样式系统
from .themes.modern_theme import ModernTheme
from .styling import (
    StylableViewMixin, enhance_view_styling, 
    create_reactive_styling
)

# 导入现代组件
try:
    from .components import (
        AlbumArtCard,
        ScrollingLyricsPanel, 
        PlaybackControls,
        ModernPlayerWindow
    )
    modern_components_available = True
except ImportError:
    modern_components_available = False

# 导入传统组件（如果存在）
try:
    from .components import (
        MusicProgressBar,
        AlbumArtView, 
        VolumeSlider,
        SongListItem,
        create_music_progress_bar,
        create_album_art_view,
        create_volume_slider
    )
    legacy_components_available = True
except ImportError:
    legacy_components_available = False

__all__ = ['ModernTheme', 'StylableViewMixin', 'enhance_view_styling', 'create_reactive_styling']

# 导入实用版播放器
from .components import WorkingMusicPlayer

if modern_components_available:
    __all__.extend(['AlbumArtCard', 'ScrollingLyricsPanel', 'PlaybackControls', 'ModernPlayerWindow'])

# 添加实用版播放器到导出
__all__.append('WorkingMusicPlayer')

if legacy_components_available:
    __all__.extend(['MusicProgressBar', 'AlbumArtView', 'VolumeSlider', 'SongListItem', 
                   'create_music_progress_bar', 'create_album_art_view', 'create_volume_slider'])