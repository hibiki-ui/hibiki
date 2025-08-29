#!/usr/bin/env python3
"""
🎵 Hibiki Music Player - 主线版本

集成了完善的实用版音乐播放器
使用经过测试和验证的组件
"""

from hibiki.ui import ManagerFactory
from hibiki.music.core.app_state import MusicAppState
from hibiki.music.ui.components import WorkingMusicPlayer
from hibiki.ui.core.logging import get_logger

logger = get_logger("main_player")

def create_demo_data(state: MusicAppState):
    """创建演示数据"""
    # 设置当前播放歌曲
    state.current_song.value = {
        'title': '周深 - 不想睡',
        'artist': '周深',
        'album': '不想睡 单曲',
        'duration': 210.0
    }
    
    # 设置播放状态
    state.is_playing.value = True
    state.position.value = 45.0  # 当前播放位置：45秒
    state.duration.value = 210.0  # 总时长：3分30秒
    state.volume.value = 0.75    # 音量75%
    
    logger.info("🎵 演示数据设置完成")
    logger.info(f"   🎧 当前歌曲: {state.current_song.value['title']}")
    logger.info(f"   ⏯️  播放状态: {'播放中' if state.is_playing.value else '暂停'}")
    logger.info(f"   📊 播放进度: {state.position.value}s / {state.duration.value}s")
    logger.info(f"   🔊 音量: {int(state.volume.value * 100)}%")

def main():
    """主程序入口"""
    print("🚀 启动 Hibiki Music Player...")
    
    try:
        # 创建应用管理器
        app_manager = ManagerFactory.get_app_manager()
        
        # 创建应用状态
        state = MusicAppState()
        create_demo_data(state)
        
        # 创建主窗口
        window = app_manager.create_window(
            "🎵 Hibiki Music Player v1.0",
            width=950,
            height=750
        )
        
        # 创建音乐播放器界面
        music_player = WorkingMusicPlayer(state)
        player_interface = music_player.create_full_interface()
        window.set_content(player_interface)
        
        print("✅ Hibiki Music Player 启动成功！")
        print("\n🎵 功能特色：")
        print("   🎨 现代化界面设计")
        print("   🎤 实时歌词显示") 
        print("   🎵 完整播放控制")
        print("   📊 播放进度显示")
        print("   🔊 音量调节功能")
        print("   📱 响应式布局")
        
        print(f"\n📱 当前播放状态：")
        print(f"   🎧 {state.current_song.value['title']}")
        print(f"   👨‍🎤 {state.current_song.value['artist']}")
        print(f"   💿 {state.current_song.value['album']}")
        print(f"   ⏯️  {'播放中' if state.is_playing.value else '暂停'}")
        print(f"   📊 {music_player.format_time(state.position.value)} / {music_player.format_time(state.duration.value)}")
        print(f"   🔊 {int(state.volume.value * 100)}%")
        
        # 运行应用
        app_manager.run()
        
    except Exception as e:
        logger.error(f"❌ 应用启动失败: {e}")
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()