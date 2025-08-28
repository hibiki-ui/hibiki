#!/usr/bin/env python3
"""
🎵 Hibiki Music 音频播放引擎

基于 macOS AVFoundation 的原生音频播放器
集成响应式状态管理和系统音频会话
"""

import os
from typing import Optional, Callable
import objc
from Foundation import NSObject, NSURL, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from AVFoundation import (
    AVPlayer, AVPlayerItem, AVAudioSession, AVAudioSessionCategoryPlayback,
    AVPlayerItemDidPlayToEndTimeNotification, AVPlayerItemFailedToPlayToEndTimeNotification,
    AVPlayerTimeControlStatusPlaying, AVPlayerTimeControlStatusPaused, AVPlayerTimeControlStatusWaitingToPlayAtSpecifiedRate
)
from AppKit import NSNotificationCenter
import time

# 导入应用状态
from ...core.app_state import MusicAppState, Song

class AudioPlayerDelegate(NSObject):
    """音频播放器事件委托"""
    
    def init(self):
        self = objc.super(AudioPlayerDelegate, self).init()
        if self is None:
            return None
        self.audio_player = None
        return self
    
    def playerItemDidPlayToEnd_(self, notification):
        """歌曲播放完成"""
        print("🎵 歌曲播放完成")
        if self.audio_player:
            self.audio_player._on_playback_finished()
    
    def playerItemFailedToPlay_(self, notification):
        """播放失败"""
        print("❌ 歌曲播放失败")
        if self.audio_player:
            self.audio_player._on_playback_error(notification)

class AudioPlayer:
    """
    Hibiki Music 音频播放引擎
    
    功能特性：
    - 基于 AVFoundation 的原生音频播放
    - 响应式状态管理集成
    - 系统音频会话管理
    - 自动播放队列支持
    - 播放进度跟踪
    """
    
    def __init__(self, app_state: MusicAppState):
        print("🎵 初始化 AudioPlayer...")
        
        self.app_state = app_state
        self.av_player: Optional[AVPlayer] = None
        self.current_item: Optional[AVPlayerItem] = None
        self.delegate = AudioPlayerDelegate.alloc().init()
        self.delegate.audio_player = self
        
        # 进度跟踪定时器
        self.progress_timer: Optional[NSTimer] = None
        
        # 设置音频会话
        self._setup_audio_session()
        
        # 设置通知监听
        self._setup_notifications()
        
        print("✅ AudioPlayer 初始化完成")
        
    def _setup_audio_session(self):
        """设置系统音频会话"""
        try:
            audio_session = AVAudioSession.sharedInstance()
            success = audio_session.setCategory_error_(AVAudioSessionCategoryPlayback, None)
            if success[0]:
                audio_session.setActive_error_(True, None)
                print("✅ 音频会话配置成功")
            else:
                print("⚠️ 音频会话配置失败")
        except Exception as e:
            print(f"❌ 音频会话设置错误: {e}")
    
    def _setup_notifications(self):
        """设置播放通知监听"""
        notification_center = NSNotificationCenter.defaultCenter()
        
        # 播放完成通知
        notification_center.addObserver_selector_name_object_(
            self.delegate,
            objc.selector(self.delegate.playerItemDidPlayToEnd_, signature=b'v@:@'),
            AVPlayerItemDidPlayToEndTimeNotification,
            None
        )
        
        # 播放失败通知
        notification_center.addObserver_selector_name_object_(
            self.delegate,
            objc.selector(self.delegate.playerItemFailedToPlay_, signature=b'v@:@'),
            AVPlayerItemFailedToPlayToEndTimeNotification,
            None
        )
    
    def load_song(self, song: Song) -> bool:
        """加载歌曲文件"""
        if not song or not song.file_path:
            print("❌ 无效的歌曲信息")
            return False
            
        if not os.path.exists(song.file_path):
            print(f"❌ 音频文件不存在: {song.file_path}")
            return False
        
        try:
            print(f"🎵 加载歌曲: {song.title} - {song.artist}")
            
            # 创建播放项
            file_url = NSURL.fileURLWithPath_(song.file_path)
            self.current_item = AVPlayerItem.playerItemWithURL_(file_url)
            
            if not self.current_item:
                print("❌ 无法创建 AVPlayerItem")
                return False
            
            # 创建或替换播放器
            if self.av_player:
                self.av_player.replaceCurrentItemWithPlayerItem_(self.current_item)
            else:
                self.av_player = AVPlayer.playerWithPlayerItem_(self.current_item)
            
            # 更新应用状态
            self.app_state.current_song.value = song
            self.app_state.duration.value = self._get_duration()
            self.app_state.position.value = 0.0
            
            print(f"✅ 歌曲加载成功，时长: {self.app_state.duration.value:.1f}秒")
            return True
            
        except Exception as e:
            print(f"❌ 加载歌曲失败: {e}")
            return False
    
    def play(self) -> bool:
        """开始播放"""
        if not self.av_player or not self.current_item:
            print("❌ 没有可播放的歌曲")
            return False
        
        try:
            self.av_player.play()
            self.app_state.is_playing.value = True
            
            # 启动进度跟踪
            self._start_progress_tracking()
            
            print("▶️ 开始播放")
            return True
            
        except Exception as e:
            print(f"❌ 播放失败: {e}")
            return False
    
    def pause(self) -> bool:
        """暂停播放"""
        if not self.av_player:
            return False
        
        try:
            self.av_player.pause()
            self.app_state.is_playing.value = False
            
            # 停止进度跟踪
            self._stop_progress_tracking()
            
            print("⏸️ 暂停播放")
            return True
            
        except Exception as e:
            print(f"❌ 暂停失败: {e}")
            return False
    
    def toggle_play_pause(self) -> bool:
        """切换播放/暂停状态"""
        if self.app_state.is_playing.value:
            return self.pause()
        else:
            return self.play()
    
    def stop(self) -> bool:
        """停止播放"""
        if not self.av_player:
            return False
        
        try:
            self.av_player.pause()
            self.seek_to_position(0.0)
            
            self.app_state.is_playing.value = False
            self.app_state.position.value = 0.0
            
            self._stop_progress_tracking()
            
            print("⏹️ 停止播放")
            return True
            
        except Exception as e:
            print(f"❌ 停止失败: {e}")
            return False
    
    def seek_to_position(self, position_seconds: float) -> bool:
        """跳转到指定位置"""
        if not self.av_player or not self.current_item:
            return False
        
        try:
            # 确保位置在有效范围内
            duration = self._get_duration()
            position = max(0.0, min(position_seconds, duration))
            
            # CMTime 创建 (时间值, 时间基数)
            from CoreMedia import CMTimeMakeWithSeconds
            target_time = CMTimeMakeWithSeconds(position, 600)  # 600 是常用的时间基数
            
            self.av_player.seekToTime_(target_time)
            self.app_state.position.value = position
            
            print(f"⏭️ 跳转到位置: {position:.1f}秒")
            return True
            
        except Exception as e:
            print(f"❌ 跳转失败: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """设置音量 (0.0 - 1.0)"""
        if not self.av_player:
            return False
        
        try:
            # 确保音量在有效范围内
            volume = max(0.0, min(1.0, volume))
            self.av_player.setVolume_(volume)
            self.app_state.volume.value = volume
            
            print(f"🔊 音量设置为: {int(volume * 100)}%")
            return True
            
        except Exception as e:
            print(f"❌ 设置音量失败: {e}")
            return False
    
    def _get_duration(self) -> float:
        """获取当前歌曲总时长"""
        if not self.current_item:
            return 0.0
        
        try:
            from CoreMedia import CMTimeGetSeconds, CMTIME_IS_VALID
            duration_time = self.current_item.duration()
            
            if CMTIME_IS_VALID(duration_time):
                duration = CMTimeGetSeconds(duration_time)
                return duration if duration > 0 else 0.0
            else:
                return 0.0
                
        except Exception as e:
            print(f"❌ 获取时长失败: {e}")
            return 0.0
    
    def _get_current_position(self) -> float:
        """获取当前播放位置"""
        if not self.av_player:
            return 0.0
        
        try:
            from CoreMedia import CMTimeGetSeconds, CMTIME_IS_VALID
            current_time = self.av_player.currentTime()
            
            if CMTIME_IS_VALID(current_time):
                position = CMTimeGetSeconds(current_time)
                return position if position > 0 else 0.0
            else:
                return 0.0
                
        except Exception as e:
            # print(f"❌ 获取位置失败: {e}")  # 这个可能会频繁调用，不打印错误
            return 0.0
    
    def _start_progress_tracking(self):
        """启动播放进度跟踪定时器"""
        self._stop_progress_tracking()  # 先停止现有的定时器
        
        # 创建定时器，每0.1秒更新一次进度
        self.progress_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.1,  # 时间间隔
            self,
            objc.selector(self._update_progress, signature=b'v@:@'),
            None,
            True  # 重复执行
        )
        
        print("⏱️ 进度跟踪已启动")
    
    def _stop_progress_tracking(self):
        """停止播放进度跟踪定时器"""
        if self.progress_timer:
            self.progress_timer.invalidate()
            self.progress_timer = None
            print("⏱️ 进度跟踪已停止")
    
    @objc.signature(b'v@:@')
    def _update_progress(self, timer):
        """更新播放进度 (定时器回调)"""
        try:
            current_position = self._get_current_position()
            self.app_state.position.value = current_position
            
            # 计算播放进度百分比
            duration = self.app_state.duration.value
            if duration > 0:
                progress_percent = (current_position / duration) * 100
            else:
                progress_percent = 0.0
                
            # 可以添加更详细的调试信息
            # print(f"🎵 播放进度: {current_position:.1f}/{duration:.1f}秒 ({progress_percent:.1f}%)")
            
        except Exception as e:
            print(f"❌ 更新进度失败: {e}")
    
    def _on_playback_finished(self):
        """播放完成回调"""
        print("🎵 歌曲播放完成，准备下一首")
        
        # 更新状态
        self.app_state.is_playing.value = False
        self._stop_progress_tracking()
        
        # 自动播放下一首 (如果有的话)
        if hasattr(self.app_state, 'next_song') and callable(self.app_state.next_song):
            self.app_state.next_song()
    
    def _on_playback_error(self, notification):
        """播放错误回调"""
        print(f"❌ 播放出错: {notification}")
        
        # 更新状态
        self.app_state.is_playing.value = False
        self._stop_progress_tracking()
    
    def cleanup(self):
        """清理资源"""
        print("🧹 清理 AudioPlayer 资源...")
        
        self._stop_progress_tracking()
        
        if self.av_player:
            self.av_player.pause()
            self.av_player = None
        
        self.current_item = None
        
        # 移除通知监听
        NSNotificationCenter.defaultCenter().removeObserver_(self.delegate)
        
        print("✅ AudioPlayer 资源清理完成")