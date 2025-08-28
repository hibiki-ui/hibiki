"""
MacUI 日志系统
提供统一的日志记录功能，支持文件输出和等级控制
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

class MacUILogger:
    """MacUI 日志管理器"""
    
    _instance: Optional['MacUILogger'] = None
    _initialized = False
    
    def __new__(cls) -> 'MacUILogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志系统"""
        # 创建logs目录
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # 日志文件路径
        self.log_file = log_dir / "macui.log"
        self.debug_file = log_dir / "macui_debug.log"
        
        # 创建根日志器
        self.logger = logging.getLogger("macui")
        self.logger.setLevel(logging.DEBUG)
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 创建格式器
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 1. 控制台处理器 - INFO及以上
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # 2. 主日志文件 - INFO及以上，轮转
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # 3. 调试日志文件 - DEBUG及以上，轮转
        debug_handler = logging.handlers.RotatingFileHandler(
            self.debug_file,
            maxBytes=50*1024*1024,  # 50MB  
            backupCount=3,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(debug_handler)
        
        # 记录初始化信息
        self.logger.info("MacUI 日志系统初始化完成")
        self.logger.debug(f"主日志文件: {self.log_file}")
        self.logger.debug(f"调试日志文件: {self.debug_file}")
    
    def set_level(self, level: str):
        """设置日志等级"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO, 
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            # 只调整控制台输出等级，文件保持详细记录
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(level_map[level.upper()])
            self.logger.info(f"控制台日志等级设置为: {level.upper()}")
        else:
            self.logger.warning(f"无效的日志等级: {level}")
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """获取子日志器"""
        if name:
            return logging.getLogger(f"macui.{name}")
        return self.logger


# 全局日志管理器实例
_logger_manager = MacUILogger()

# 便捷函数
def get_logger(name: str = None) -> logging.Logger:
    """获取MacUI日志器"""
    return _logger_manager.get_logger(name)

def set_log_level(level: str):
    """设置日志等级"""
    _logger_manager.set_level(level)

# 模块级别的日志器
logger = get_logger("core.logging")