#!/usr/bin/env python3
"""
🎵 Hibiki Music

智能原生 macOS 音乐播放器 - 基于 Hibiki UI 框架
"""

__version__ = "0.1.0"
__author__ = "Hibiki Music Team"
__description__ = "智能原生 macOS 音乐播放器"

from .core import MusicAppState
from .ui import MusicMainWindow

__all__ = [
    "MusicAppState",
    "MusicMainWindow",
]