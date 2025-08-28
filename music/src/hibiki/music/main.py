#!/usr/bin/env python3
"""
🎵 Hibiki Music 主应用程序

基于 Hibiki UI 框架的智能音乐播放器 MVP
"""

from hibiki.ui import (
    ManagerFactory, Label, Container, ComponentStyle, px,
    Display, FlexDirection, AlignItems, JustifyContent
)
from hibiki.music.core.app_state import MusicAppState

class HibikiMusicApp:
    """
    Hibiki Music 主应用程序类
    
    MVP v0.1 功能：
    - 基础应用架构
    - 响应式状态管理
    - 简单的UI界面
    """
    
    def __init__(self):
        print("🎵 初始化 Hibiki Music...")
        
        # 初始化应用状态
        self.state = MusicAppState()
        
        # 应用管理器
        self.app_manager = None
        self.window = None
        
    def create_ui(self) -> Container:
        """创建主界面"""
        
        # 标题
        title_label = Label(
            "🎵 Hibiki Music MVP v0.1",
            style=ComponentStyle(margin_bottom=px(20)),
            font_size=24,
            font_weight="bold",
            text_align="center",
            color="#2c3e50"
        )
        
        # 状态信息
        status_label = Label(
            lambda: f"音乐库: {self.state.total_songs.value} 首歌曲",
            style=ComponentStyle(margin_bottom=px(15)),
            font_size=16,
            text_align="center",
            color="#666"
        )
        
        # 当前播放信息
        current_playing_label = Label(
            lambda: f"正在播放: {self.state.current_song.value.title if self.state.current_song.value else '无'}",
            style=ComponentStyle(margin_bottom=px(15)),
            font_size=14,
            text_align="center",
            color="#333"
        )
        
        # 播放状态
        play_status_label = Label(
            lambda: f"状态: {'播放中' if self.state.is_playing.value else '已暂停'}",
            style=ComponentStyle(margin_bottom=px(20)),
            font_size=14,
            text_align="center",
            color=lambda: "#007AFF" if self.state.is_playing.value else "#666"
        )
        
        # 说明文字
        description_label = Label(
            "这是 Hibiki Music 的 MVP v0.1 版本\n" +
            "展示了基于 Hibiki UI 的响应式状态管理\n" +
            "后续版本将添加实际的音频播放功能",
            style=ComponentStyle(margin_top=px(30)),
            font_size=12,
            text_align="center",
            color="#999"
        )
        
        # 主容器
        main_container = Container(
            children=[
                title_label,
                status_label,
                current_playing_label,
                play_status_label,
                description_label
            ],
            style=ComponentStyle(
                padding=px(40),
                display=Display.FLEX,
                flex_direction=FlexDirection.COLUMN,
                align_items=AlignItems.CENTER
            )
        )
        
        return main_container
        
    def run(self):
        """运行应用程序"""
        try:
            print("🚀 启动 Hibiki Music...")
            
            # 创建应用管理器
            self.app_manager = ManagerFactory.get_app_manager()
            
            # 创建主窗口
            self.window = self.app_manager.create_window(
                title="Hibiki Music MVP v0.1",
                width=600,
                height=400
            )
            
            # 创建并设置UI
            main_ui = self.create_ui()
            self.window.set_content(main_ui)
            
            print("✅ Hibiki Music 已启动！")
            print("📝 当前版本: MVP v0.1")
            print("🎯 功能: 基础架构 + 响应式状态管理")
            
            # 运行应用
            self.app_manager.run()
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    app = HibikiMusicApp()
    app.run()