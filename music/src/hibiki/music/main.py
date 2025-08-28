#!/usr/bin/env python3
"""
🎵 Hibiki Music - 智能原生 macOS 音乐播放器

基于 Hibiki UI 框架开发的现代化音乐播放器
专注于智能标签系统和本地音乐管理
"""

from hibiki.ui import (
    Signal, Computed, Effect, 
    Label, Button, Container, ComponentStyle, px,
    ManagerFactory
)
from .ui.main_window import MusicMainWindow
from .core.app_state import MusicAppState
from .utils.config import load_config

class HibikiMusicApp:
    """Hibiki Music 主应用类"""
    
    def __init__(self):
        self.app_state = MusicAppState()
        self.app_manager = ManagerFactory.get_app_manager()
        self.main_window = None
        
    def initialize(self):
        """初始化应用"""
        print("🎵 Hibiki Music v0.1.0 启动中...")
        
        # 加载配置
        config = load_config()
        print(f"✅ 配置加载完成: {config.music_library_path}")
        
        # 初始化音乐库
        # TODO: 在 MVP 第二阶段实现
        print("📚 音乐库初始化...")
        
        # 创建主窗口
        self.main_window = MusicMainWindow(self.app_state)
        print("🖼️ 主窗口创建完成")
        
    def run(self):
        """运行应用"""
        try:
            self.initialize()
            
            # 创建应用窗口
            window = self.app_manager.create_window(
                "Hibiki Music v0.1.0",
                width=1200,
                height=800
            )
            
            # 设置窗口内容
            main_content = self.main_window.create_main_container()
            window.set_content(main_content)
            
            print("🚀 Hibiki Music 已启动!")
            print("💡 MVP v0.1 功能:")
            print("   • 基础音乐播放器界面")
            print("   • 响应式状态管理")
            print("   • Hibiki UI 组件展示")
            print("   • 为智能标签系统做准备")
            
            # 运行事件循环
            self.app_manager.run()
            
        except Exception as e:
            print(f"❌ 应用启动失败: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    app = HibikiMusicApp()
    app.run()