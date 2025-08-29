#!/usr/bin/env python3
"""
🎵 Hibiki Music 日志系统
为音乐播放器应用提供专门的日志记录功能
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

class MusicLogger:
    """Hibiki Music 日志管理器"""
    
    _instance: Optional['MusicLogger'] = None
    _initialized = False
    
    def __new__(cls) -> 'MusicLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志配置"""
        # 创建根日志器
        self.logger = logging.getLogger("hibiki.music")
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加handler
        if self.logger.handlers:
            return
        
        # 创建日志格式
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件输出（可选）
        self._setup_file_logging(formatter)
        
        # 初始化完成日志
        self.logger.info("🎵 Hibiki Music 日志系统初始化完成")
    
    def _setup_file_logging(self, formatter):
        """设置文件日志输出"""
        try:
            # 创建logs目录
            log_dir = Path.home() / ".hibiki" / "music" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # 日志文件路径
            log_file = log_dir / f"music_{datetime.now().strftime('%Y%m%d')}.log"
            
            # 文件处理器 (支持轮转)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            self.logger.debug(f"📁 日志文件: {log_file}")
            
        except Exception as e:
            # 文件日志失败不影响程序运行
            self.logger.warning(f"⚠️ 无法创建日志文件: {e}")
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """获取子日志器"""
        if name:
            return logging.getLogger(f"hibiki.music.{name}")
        return self.logger
    
    def set_level(self, level: str):
        """设置日志级别"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            self.logger.setLevel(level_map[level.upper()])
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(level_map[level.upper()])
            
            self.logger.info(f"🔧 日志级别设置为: {level.upper()}")
        else:
            self.logger.warning(f"⚠️ 无效的日志级别: {level}")


# 全局日志管理器实例
_music_logger = MusicLogger()

# 便捷函数
def get_logger(name: str = None) -> logging.Logger:
    """获取Hibiki Music日志器"""
    return _music_logger.get_logger(name)

def set_log_level(level: str):
    """设置日志等级"""
    _music_logger.set_level(level)

# 模块级别的日志器
logger = get_logger("core.logging")