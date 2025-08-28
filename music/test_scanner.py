#!/usr/bin/env python3
"""
🎵 测试音乐库扫描器

扫描 music/data 目录中的歌曲并导入数据库
"""

import sys
import os
from pathlib import Path

# 添加项目路径到sys.path (临时测试用)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from hibiki.music.core.scanner import MusicLibraryScanner, scan_music_library
from hibiki.music.data.database import DatabaseManager, SongService

def test_scanner():
    """测试扫描器功能"""
    print("🎵 Hibiki Music - 扫描器测试")
    print("=" * 50)
    
    # 数据目录
    data_dir = project_root / "data"
    
    if not data_dir.exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return
        
    print(f"📁 扫描目录: {data_dir}")
    print()
    
    try:
        # 使用便捷函数扫描
        imported_songs = scan_music_library(str(data_dir))
        
        print()
        print("=" * 50)
        print(f"✅ 扫描完成！导入了 {len(imported_songs)} 首歌曲")
        print()
        
        # 显示导入的歌曲
        if imported_songs:
            print("📋 导入的歌曲列表:")
            for i, song in enumerate(imported_songs, 1):
                print(f"{i:2d}. {song.title}")
                print(f"     艺术家: {song.artist}")
                print(f"     专辑: {song.album or '未知'}")
                print(f"     时长: {song.duration:.1f}秒")
                print(f"     格式: {song.file_format}")
                if song.year:
                    print(f"     年份: {song.year}")
                print()
        
        # 验证数据库
        print("=" * 50)
        print("🔍 验证数据库中的数据...")
        
        song_service = SongService()
        all_songs = song_service.get_all_songs()
        
        print(f"📊 数据库中总共有 {len(all_songs)} 首歌曲")
        
        # 获取统计信息
        stats = song_service.get_library_stats()
        print(f"📈 音乐库统计:")
        print(f"   总歌曲数: {stats.total_songs}")
        print(f"   总艺术家: {stats.total_artists}")
        print(f"   总专辑数: {stats.total_albums}")
        print(f"   总时长: {stats.total_duration:.1f}秒 ({stats.total_duration/60:.1f}分钟)")
        print(f"   收藏歌曲: {stats.favorite_count}")
        
        if stats.language_distribution:
            print(f"   语言分布: {stats.language_distribution}")
            
        print("✅ 测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scanner()