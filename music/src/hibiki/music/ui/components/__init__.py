"""
🎵 现代化音乐播放器UI组件库

提供完整的现代UI组件集合
"""

# 实用版播放器（主要使用）
from .working_player import WorkingMusicPlayer

# 实验性现代播放器（备用）
try:
    from .modern_player import (
        AlbumArtCard,
        ScrollingLyricsPanel, 
        PlaybackControls,
        ModernPlayerWindow
    )
    modern_components_available = True
except ImportError:
    modern_components_available = False

__all__ = ['WorkingMusicPlayer']

if modern_components_available:
    __all__.extend(['AlbumArtCard', 'ScrollingLyricsPanel', 'PlaybackControls', 'ModernPlayerWindow'])