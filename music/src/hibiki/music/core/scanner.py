#!/usr/bin/env python3
"""
🎵 Hibiki Music 音乐库扫描器

使用 mutagen 提取音频文件元数据，集成 SQLModel 数据库
"""

import os
import mimetypes
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from mutagen import File as MutagenFile
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

from ..data.database import SongService, DatabaseManager
from ..data.models import SongCreate, SongPublic

class MusicLibraryScanner:
    """
    音乐库扫描器
    
    功能：
    - 扫描指定目录的音频文件
    - 使用 mutagen 提取元数据
    - 导入到 SQLModel 数据库
    - 支持 MP3, FLAC, M4A 等格式
    """
    
    # 支持的音频格式
    SUPPORTED_FORMATS = {'.mp3', '.flac', '.m4a', '.mp4', '.ogg', '.wav'}
    
    def __init__(self):
        self.song_service = SongService()
        self.db = DatabaseManager()
        
    def scan_directory(self, directory_path: str, recursive: bool = True) -> List[SongPublic]:
        """
        扫描目录中的音频文件
        
        Args:
            directory_path: 要扫描的目录路径
            recursive: 是否递归扫描子目录
            
        Returns:
            导入成功的歌曲列表
        """
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            print(f"❌ 目录不存在: {directory_path}")
            return []
            
        print(f"🔍 开始扫描音乐目录: {directory_path}")
        
        # 收集音频文件
        audio_files = self._find_audio_files(directory, recursive)
        print(f"📁 发现 {len(audio_files)} 个音频文件")
        
        # 处理每个文件
        imported_songs = []
        for i, file_path in enumerate(audio_files, 1):
            print(f"📀 处理 ({i}/{len(audio_files)}): {file_path.name}")
            
            try:
                song = self._process_audio_file(file_path)
                if song:
                    imported_songs.append(song)
                    print(f"✅ 导入成功: {song.title} - {song.artist}")
                else:
                    print(f"⚠️ 跳过文件: {file_path.name}")
                    
            except Exception as e:
                print(f"❌ 处理失败: {file_path.name} - {e}")
                continue
                
        print(f"🎵 扫描完成！成功导入 {len(imported_songs)} 首歌曲")
        return imported_songs
    
    def _find_audio_files(self, directory: Path, recursive: bool) -> List[Path]:
        """查找目录中的音频文件"""
        audio_files = []
        
        if recursive:
            # 递归搜索
            for file_path in directory.rglob('*'):
                if file_path.is_file() and self._is_audio_file(file_path):
                    audio_files.append(file_path)
        else:
            # 只搜索当前目录
            for file_path in directory.iterdir():
                if file_path.is_file() and self._is_audio_file(file_path):
                    audio_files.append(file_path)
                    
        return sorted(audio_files)
    
    def _is_audio_file(self, file_path: Path) -> bool:
        """检查文件是否为支持的音频格式"""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def _process_audio_file(self, file_path: Path) -> Optional[SongPublic]:
        """
        处理单个音频文件
        
        1. 提取元数据
        2. 创建SongCreate对象
        3. 导入数据库
        """
        try:
            # 提取元数据
            metadata = self._extract_metadata(file_path)
            if not metadata:
                return None
                
            # 检查文件是否已存在
            existing_song = self.song_service.get_song_by_path(str(file_path))
            if existing_song:
                print(f"📋 文件已存在数据库中: {file_path.name}")
                return existing_song
            
            # 创建歌曲数据
            song_data = SongCreate(
                title=metadata.get('title', file_path.stem),
                artist=metadata.get('artist', '未知艺术家'),
                album=metadata.get('album'),
                album_artist=metadata.get('albumartist'),
                duration=metadata.get('duration', 0.0),
                year=metadata.get('year'),
                track_number=metadata.get('tracknumber'),
                disc_number=metadata.get('discnumber'),
                genre=metadata.get('genre'),
                file_format=file_path.suffix.lower().replace('.', ''),
                bitrate=metadata.get('bitrate'),
                sample_rate=metadata.get('sample_rate'),
                file_path=str(file_path.absolute()),
                file_size=file_path.stat().st_size,
                file_modified_at=datetime.fromtimestamp(file_path.stat().st_mtime)
            )
            
            # 导入数据库
            return self.song_service.create_song(song_data)
            
        except Exception as e:
            print(f"❌ 处理文件失败 {file_path}: {e}")
            return None
    
    def _extract_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        使用 mutagen 提取音频文件元数据
        """
        try:
            audio_file = MutagenFile(str(file_path))
            if not audio_file:
                print(f"⚠️ 无法读取音频文件: {file_path}")
                return None
                
            metadata = {}
            
            # 提取基础信息
            if hasattr(audio_file, 'info'):
                info = audio_file.info
                metadata['duration'] = getattr(info, 'length', 0.0)
                metadata['bitrate'] = getattr(info, 'bitrate', None)
                metadata['sample_rate'] = getattr(info, 'sample_rate', None)
            
            # 处理不同格式的标签
            if isinstance(audio_file, MP3):
                metadata.update(self._extract_id3_tags(audio_file))
            elif isinstance(audio_file, FLAC):
                metadata.update(self._extract_vorbis_tags(audio_file))
            elif isinstance(audio_file, MP4):
                metadata.update(self._extract_mp4_tags(audio_file))
            else:
                # 通用标签处理
                metadata.update(self._extract_generic_tags(audio_file))
                
            return metadata
            
        except ID3NoHeaderError:
            print(f"⚠️ 文件没有ID3标签: {file_path}")
            return {'title': file_path.stem}
        except Exception as e:
            print(f"❌ 元数据提取失败 {file_path}: {e}")
            return None
    
    def _extract_id3_tags(self, audio_file: MP3) -> Dict[str, Any]:
        """提取ID3标签 (MP3)"""
        tags = {}
        
        if not audio_file.tags:
            return tags
            
        # 标准ID3标签映射
        tag_mapping = {
            'TIT2': 'title',      # 标题
            'TPE1': 'artist',     # 艺术家
            'TALB': 'album',      # 专辑
            'TPE2': 'albumartist', # 专辑艺术家
            'TDRC': 'year',       # 年份
            'TRCK': 'tracknumber', # 音轨号
            'TPOS': 'discnumber',  # 碟片号
            'TCON': 'genre',      # 流派
        }
        
        for id3_tag, field_name in tag_mapping.items():
            if id3_tag in audio_file.tags:
                value = str(audio_file.tags[id3_tag].text[0])
                if field_name == 'year':
                    # 提取年份数字
                    try:
                        tags[field_name] = int(value[:4])
                    except (ValueError, IndexError):
                        pass
                elif field_name in ['tracknumber', 'discnumber']:
                    # 提取数字部分 (可能是 "1/10" 格式)
                    try:
                        tags[field_name] = int(value.split('/')[0])
                    except (ValueError, IndexError):
                        pass
                else:
                    tags[field_name] = value
                    
        return tags
    
    def _extract_vorbis_tags(self, audio_file: FLAC) -> Dict[str, Any]:
        """提取Vorbis标签 (FLAC)"""
        tags = {}
        
        if not hasattr(audio_file, 'tags') or not audio_file.tags:
            return tags
            
        # Vorbis标签映射
        tag_mapping = {
            'TITLE': 'title',
            'ARTIST': 'artist', 
            'ALBUM': 'album',
            'ALBUMARTIST': 'albumartist',
            'DATE': 'year',
            'TRACKNUMBER': 'tracknumber',
            'DISCNUMBER': 'discnumber',
            'GENRE': 'genre',
        }
        
        for vorbis_tag, field_name in tag_mapping.items():
            if vorbis_tag in audio_file.tags:
                value = audio_file.tags[vorbis_tag][0]
                if field_name == 'year':
                    try:
                        tags[field_name] = int(value[:4])
                    except (ValueError, IndexError):
                        pass
                elif field_name in ['tracknumber', 'discnumber']:
                    try:
                        tags[field_name] = int(value)
                    except ValueError:
                        pass
                else:
                    tags[field_name] = value
                    
        return tags
    
    def _extract_mp4_tags(self, audio_file: MP4) -> Dict[str, Any]:
        """提取MP4标签 (M4A)"""
        tags = {}
        
        if not hasattr(audio_file, 'tags') or not audio_file.tags:
            return tags
            
        # MP4标签映射
        tag_mapping = {
            '\xa9nam': 'title',
            '\xa9ART': 'artist',
            '\xa9alb': 'album', 
            'aART': 'albumartist',
            '\xa9day': 'year',
            'trkn': 'tracknumber',
            'disk': 'discnumber',
            '\xa9gen': 'genre',
        }
        
        for mp4_tag, field_name in tag_mapping.items():
            if mp4_tag in audio_file.tags:
                value = audio_file.tags[mp4_tag]
                
                # MP4标签值处理
                if isinstance(value, list) and value:
                    value = value[0]
                    
                if field_name == 'year':
                    try:
                        tags[field_name] = int(str(value)[:4])
                    except (ValueError, IndexError):
                        pass
                elif field_name in ['tracknumber', 'discnumber']:
                    # MP4使用元组 (current, total)
                    if isinstance(value, tuple) and value:
                        tags[field_name] = value[0]
                    else:
                        try:
                            tags[field_name] = int(value)
                        except ValueError:
                            pass
                else:
                    tags[field_name] = str(value)
                    
        return tags
    
    def _extract_generic_tags(self, audio_file) -> Dict[str, Any]:
        """通用标签提取 (其他格式)"""
        tags = {}
        
        if not hasattr(audio_file, 'tags') or not audio_file.tags:
            return tags
            
        # 通用字段映射
        common_fields = ['title', 'artist', 'album', 'albumartist', 
                        'date', 'tracknumber', 'discnumber', 'genre']
        
        for field in common_fields:
            if field in audio_file.tags:
                value = audio_file.tags[field]
                if isinstance(value, list) and value:
                    value = value[0]
                    
                if field == 'date':
                    try:
                        tags['year'] = int(str(value)[:4])
                    except (ValueError, IndexError):
                        pass
                else:
                    tags[field] = str(value)
                    
        return tags

# 便捷函数
def scan_music_library(directory_path: str) -> List[SongPublic]:
    """
    扫描音乐库的便捷函数
    
    Args:
        directory_path: 音乐目录路径
        
    Returns:
        导入成功的歌曲列表
    """
    scanner = MusicLibraryScanner()
    return scanner.scan_directory(directory_path)