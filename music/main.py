#!/usr/bin/env python3
"""
🎵 Hibiki Music 启动脚本

使用命名空间包架构的音乐播放器启动脚本
"""

from hibiki.music.main import HibikiMusicApp

if __name__ == "__main__":
    app = HibikiMusicApp()
    app.run()