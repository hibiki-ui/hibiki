#!/usr/bin/env python3
"""
🎵 Hibiki Music 主应用程序 v0.4 - 现代化版本

基于现代化设计的智能音乐播放器
- 深色主题配色
- 专辑封面+歌词并列布局
- 流畅动画效果
- 专业音乐应用级别的用户体验
"""

from hibiki.ui import ManagerFactory
from hibiki.music.core.app_state import MusicAppState
from hibiki.music.core.scanner import scan_music_library
from hibiki.music.data.database import SongService
from hibiki.music.ui.simple_modern_window import SimpleModernWindow
from pathlib import Path
from typing import List, Optional

class HibikiMusicApp:
    """
    Hibiki Music 主应用程序类
    
    v0.4 现代化功能：
    - 现代化深色主题界面
    - 专辑封面 + 歌词双主角布局
    - 流畅动画和微交互
    - 专业级用户体验
    - 响应式状态管理
    """
    
    def __init__(self):
        from hibiki.music.core.logging import get_logger
        self.logger = get_logger("main")
        self.logger.info("🎵 初始化 Hibiki Music v0.4 现代化版本...")
        
        # 初始化应用状态
        self.state = MusicAppState()
        
        # 应用管理器
        self.app_manager = None
        self.window = None
        
        # 现代化主窗口
        self.main_window = None
    
    def _load_music_library(self):
        """加载音乐库"""
        self.logger.info("🔍 加载音乐库...")
        
        # 使用绝对路径，避免不同启动方式的路径问题
        data_dir = Path("/Users/david/david/app/hibiki-ui/music/data")
        
        # 首次扫描 - 如果data目录存在就扫描
        if data_dir.exists():
            self.logger.info(f"📁 扫描目录: {data_dir}")
            try:
                scan_music_library(str(data_dir))
                self.logger.info("✅ 音乐库扫描完成")
            except Exception as e:
                self.logger.warning(f"⚠️ 扫描失败: {e}")
        
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
                self.logger.info(f"✅ 从数据库加载了 {len(app_songs)} 首歌曲")
                
                # 设置当前播放歌曲用于演示
                if app_songs:
                    self.logger.info(f"🎵 设置当前播放: {app_songs[0].title}")
                    self.state.current_song.value = app_songs[0]
                    
            else:
                self.logger.info("📋 数据库中暂无歌曲")
                self._add_fallback_songs()
                
        except Exception as e:
            self.logger.error(f"❌ 加载音乐库失败: {e}")
            self._add_fallback_songs()
    
    def _add_fallback_songs(self):
        """添加备用测试歌曲"""
        from hibiki.music.core.app_state import Song
        import os
        
        self.logger.info("🎵 添加备用测试歌曲...")
        
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
            self.logger.info(f"✅ 添加了 {len(valid_songs)} 首备用歌曲")
        else:
            self.logger.warning("⚠️ 没有找到有效的备用音频文件")
    
    def run(self):
        """运行现代化音乐播放器应用"""
        try:
            self.logger.info("🚀 启动 Hibiki Music v0.4 现代化版本...")
            
            # 加载音乐库数据
            self._load_music_library()
            
            # 创建简化现代化主窗口
            self.main_window = SimpleModernWindow(self.state)
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="🎵 Hibiki Music v0.4 - 现代化音乐播放器",
                width=1200,  # 更宽以适应新布局
                height=800   # 更高以适应歌词区域
            )
            
            # 创建并设置现代化UI
            modern_ui = self.main_window.create_main_container()
            self.window.set_content(modern_ui)
            
            self.logger.info("✅ Hibiki Music v0.4 现代化版本已启动！")
            self.logger.info("🎨 现代化特性:")
            self.logger.info("  🌙 深色优雅主题")
            self.logger.info("  🎵 专辑封面 + 歌词双主角布局")
            self.logger.info("  ✨ 流畅动画和微交互")
            self.logger.info("  🎤 KTV风格滚动歌词")
            self.logger.info("  🎨 动态配色系统")
            self.logger.info("  📱 响应式现代界面")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            self.logger.error(f"❌ 启动失败: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

def main():
    """主入口函数 - uv tool install 的console script入口"""
    app = HibikiMusicApp()
    app.run()

if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    main()