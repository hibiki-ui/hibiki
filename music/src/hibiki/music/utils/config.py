#!/usr/bin/env python3
"""
⚙️ Hibiki Music 配置管理

管理应用配置和用户设置
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class MusicConfig:
    """音乐应用配置"""
    
    # 音乐库路径
    music_library_path: str = str(Path.home() / "Music")
    
    # 支持的音频格式
    supported_formats: List[str] = None
    
    # 应用设置
    default_volume: float = 0.8
    auto_scan_library: bool = True
    scan_subdirectories: bool = True
    
    # 标签系统设置 (MVP v0.2)
    auto_tag_languages: bool = True
    auto_tag_emotions: bool = True
    
    # UI 设置
    theme: str = "light"  # "light" | "dark"
    show_visualizer: bool = True
    
    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = [
                ".mp3", ".m4a", ".aac", ".flac", 
                ".wav", ".ogg", ".wma"
            ]

def load_config() -> MusicConfig:
    """加载应用配置"""
    
    # TODO: 从文件加载实际配置
    # 目前返回默认配置用于 MVP v0.1
    
    config = MusicConfig()
    
    # 检查默认音乐目录是否存在
    if not Path(config.music_library_path).exists():
        # 如果默认目录不存在，使用用户主目录
        config.music_library_path = str(Path.home())
    
    return config

def save_config(config: MusicConfig) -> bool:
    """保存应用配置"""
    # TODO: 实现配置保存功能
    return True