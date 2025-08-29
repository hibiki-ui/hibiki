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
        
        # 初始化日志器
        from ..logging import get_logger
        self.logger = get_logger("player.delegate")
        return self
    
    def playerItemDidPlayToEnd_(self, notification):
        """歌曲播放完成"""
        self.logger.info("🎵 歌曲播放完成")
        if self.audio_player:
            self.audio_player._on_playback_finished()
    
    def playerItemFailedToPlay_(self, notification):
        """播放失败"""
        self.logger.error("❌ 歌曲播放失败")
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
        from ..logging import get_logger
        self.logger = get_logger("player.audio")
        self.logger.info("🎵 初始化 AudioPlayer...")
        
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
        
        self.logger.info("✅ AudioPlayer 初始化完成")
        
    def _setup_audio_session(self):
        """设置系统音频会话"""
        try:
            audio_session = AVAudioSession.sharedInstance()
            # PyObjC方法可能返回不同的值，先尝试直接调用
            try:
                # 尝试新版本API (返回元组)
                success, error = audio_session.setCategory_error_(AVAudioSessionCategoryPlayback, None)
                if success:
                    active_success, active_error = audio_session.setActive_error_(True, None)
                    if active_success:
                        self.logger.info("✅ 音频会话配置成功")
                    else:
                        self.logger.warning(f"⚠️ 音频会话激活失败: {active_error}")
                else:
                    self.logger.warning(f"⚠️ 音频会话类别设置失败: {error}")
            except (TypeError, ValueError):
                # 尝试旧版本API (直接返回布尔值)
                success = audio_session.setCategory_error_(AVAudioSessionCategoryPlayback, None)
                if success:
                    active_success = audio_session.setActive_error_(True, None)
                    if active_success:
                        self.logger.info("✅ 音频会话配置成功")
                    else:
                        self.logger.warning("⚠️ 音频会话激活失败")
                else:
                    self.logger.warning("⚠️ 音频会话类别设置失败")
        except Exception as e:
            self.logger.error(f"❌ 音频会话设置错误: {e}")
    
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
            self.logger.error("❌ 无效的歌曲信息")
            return False
            
        if not os.path.exists(song.file_path):
            self.logger.error(f"❌ 音频文件不存在: {song.file_path}")
            return False
        
        try:
            self.logger.info(f"🎵 加载歌曲: {song.title} - {song.artist}")
            
            # 创建播放项
            file_url = NSURL.fileURLWithPath_(song.file_path)
            self.current_item = AVPlayerItem.playerItemWithURL_(file_url)
            
            if not self.current_item:
                self.logger.error("❌ 无法创建 AVPlayerItem")
                return False
            
            # 创建或替换播放器
            if self.av_player:
                self.av_player.replaceCurrentItemWithPlayerItem_(self.current_item)
            else:
                self.av_player = AVPlayer.playerWithPlayerItem_(self.current_item)
            
            # 更新应用状态
            self.app_state.current_song.value = song
            self.app_state.position.value = 0.0
            
            # 使用标准的AVPlayer异步加载机制
            self._load_media_info_async()
            
            self.logger.info("✅ 歌曲加载启动，正在异步获取媒体信息...")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 加载歌曲失败: {e}")
            return False
    
    def play(self) -> bool:
        """开始播放"""
        if not self.av_player or not self.current_item:
            self.logger.error("❌ 没有可播放的歌曲")
            return False
        
        try:
            self.logger.debug("🎵 [音频引擎] 调用 av_player.play()...")
            self.av_player.play()
            self.logger.debug("🎵 [音频引擎] 设置播放状态为 True...")
            self.app_state.is_playing.value = True
            
            # 启动进度跟踪
            self.logger.debug("🎵 [音频引擎] 调用启动进度跟踪...")
            self._start_progress_tracking()
            
            self.logger.info("▶️ [音频引擎] 开始播放完成")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 播放失败: {e}")
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
            
            self.logger.info("⏸️ 暂停播放")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 暂停失败: {e}")
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
            
            self.logger.info("⏹️ 停止播放")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 停止失败: {e}")
            return False
    
    def seek_to_position(self, position_seconds: float) -> bool:
        """跳转到指定位置"""
        if not self.av_player or not self.current_item:
            return False
        
        try:
            # 确保位置在有效范围内 - 使用app_state中的时长，它由异步加载更新
            duration = self.app_state.duration.value
            if duration <= 0:
                # 如果app_state中的时长还没更新，尝试直接获取
                duration = self._get_duration()
            
            position = max(0.0, min(position_seconds, duration))
            self.logger.debug(f"🎯 Seek: 目标={position_seconds:.1f}s, 时长={duration:.1f}s, 实际={position:.1f}s")
            
            # CMTime 创建 (时间值, 时间基数)
            from CoreMedia import CMTimeMakeWithSeconds
            target_time = CMTimeMakeWithSeconds(position, 600)  # 600 是常用的时间基数
            
            self.av_player.seekToTime_(target_time)
            self.app_state.position.value = position
            
            self.logger.info(f"⏭️ 跳转到位置: {position:.1f}秒")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 跳转失败: {e}")
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
            
            self.logger.info(f"🔊 音量设置为: {int(volume * 100)}%")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 设置音量失败: {e}")
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
            self.logger.error(f"❌ 获取时长失败: {e}")
            return 0.0
    
    def _load_media_info_async(self):
        """使用标准的AVURLAsset异步加载媒体信息"""
        if not self.current_item:
            return
            
        self.logger.debug("🔄 开始异步加载媒体属性...")
        
        # 获取AVURLAsset (实现了AVAsynchronousKeyValueLoading协议)
        asset = self.current_item.asset()
        
        # 定义需要异步加载的媒体属性
        keys = ["duration", "tracks", "playable"]
        
        # 异步加载完成回调
        def completion_handler():
            self.logger.debug("📡 媒体属性加载完成回调")
            
            # 检查duration属性的加载状态
            from AVFoundation import AVKeyValueStatusLoaded, AVKeyValueStatusFailed, AVKeyValueStatusUnknown, AVKeyValueStatusLoading, AVKeyValueStatusCancelled
            duration_status = asset.statusOfValueForKey_("duration")
            
            # 详细状态日志
            status_names = {
                AVKeyValueStatusUnknown: "Unknown",
                AVKeyValueStatusLoading: "Loading", 
                AVKeyValueStatusLoaded: "Loaded",
                AVKeyValueStatusFailed: "Failed",
                AVKeyValueStatusCancelled: "Cancelled"
            }
            status_name = status_names.get(duration_status, f"Unknown({duration_status})")
            self.logger.debug(f"📊 Duration状态: {status_name} ({duration_status})")
            
            if duration_status == AVKeyValueStatusLoaded:
                # 直接从asset获取时长，而不是从current_item
                try:
                    from CoreMedia import CMTimeGetSeconds, CMTIME_IS_VALID
                    asset_duration = asset.duration()
                    self.logger.debug(f"🔍 Asset duration CMTime: {asset_duration}")
                    
                    if CMTIME_IS_VALID(asset_duration):
                        duration = CMTimeGetSeconds(asset_duration)
                        self.logger.debug(f"🔍 Asset duration seconds: {duration}")
                        self.app_state.duration.value = duration
                        self.logger.info(f"✅ 异步获取媒体时长: {duration:.1f}秒")
                    else:
                        self.logger.warning("⚠️ Asset duration CMTime 无效")
                        self.app_state.duration.value = 0.0
                except Exception as e:
                    self.logger.error(f"❌ 获取asset时长失败: {e}")
                    # 备用：使用原有方法
                    duration = self._get_duration()
                    self.app_state.duration.value = duration
                    self.logger.info(f"✅ 备用方法获取媒体时长: {duration:.1f}秒")
            elif duration_status == AVKeyValueStatusFailed:
                self.logger.warning("⚠️ 媒体时长获取失败")
                self.app_state.duration.value = 0.0
            else:
                self.logger.debug(f"🔄 媒体时长状态: {status_name}")
                # 如果还在加载，给一个默认值，但不要设为0
                if duration_status == AVKeyValueStatusLoading:
                    self.logger.debug("⏳ 媒体属性仍在加载中...")
        
        # 使用AVURLAsset的标准异步加载方法
        asset.loadValuesAsynchronouslyForKeys_completionHandler_(
            keys, completion_handler
        )
        self.logger.debug("✅ AVURLAsset异步加载已启动")
    
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
        self.logger.debug(f"🔄 [音频引擎] 即将启动进度跟踪定时器...")
        self._stop_progress_tracking()  # 先停止现有的定时器
        
        # 创建定时器，每0.1秒更新一次进度
        self.progress_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            0.1,  # 时间间隔
            self,
            objc.selector(self._update_progress, signature=b'v@:@'),
            None,
            True  # 重复执行
        )
        
        self.logger.debug(f"⏱️ [音频引擎] 进度跟踪已启动 - 定时器ID: {id(self.progress_timer) if self.progress_timer else 'None'}")
    
    def _stop_progress_tracking(self):
        """停止播放进度跟踪定时器"""
        if self.progress_timer:
            self.progress_timer.invalidate()
            self.progress_timer = None
            self.logger.debug("⏱️ 进度跟踪已停止")
    
    @objc.signature(b'v@:@')
    def _update_progress(self, timer):
        """更新播放进度 (定时器回调)"""
        try:
            current_position = self._get_current_position()
            self.app_state.position.value = current_position
            self.logger.debug(f"🎵 [音频引擎] 更新后 app_state.position={self.app_state.position.value:.2f}s (确认)")
            
            # 计算播放进度百分比
            duration = self.app_state.duration.value
            if duration > 0:
                progress_percent = (current_position / duration) * 100
            else:
                progress_percent = 0.0
                
            # 详细的播放进度日志
            self.logger.debug(f"🎵 更新播放进度: {current_position:.2f}/{duration:.2f}s ({progress_percent:.1f}%)")
            
        except Exception as e:
            self.logger.error(f"❌ 更新进度失败: {e}")
    
    def _on_playback_finished(self):
        """播放完成回调"""
        self.logger.info("🎵 歌曲播放完成，准备下一首")
        
        # 更新状态
        self.app_state.is_playing.value = False
        self._stop_progress_tracking()
        
        # 自动播放下一首 (如果有的话)
        if hasattr(self.app_state, 'next_song') and callable(self.app_state.next_song):
            self.app_state.next_song()
    
    def _on_playback_error(self, notification):
        """播放错误回调"""
        self.logger.error(f"❌ 播放出错: {notification}")
        
        # 更新状态
        self.app_state.is_playing.value = False
        self._stop_progress_tracking()
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("🧹 清理 AudioPlayer 资源...")
        
        self._stop_progress_tracking()
        
        if self.av_player:
            self.av_player.pause()
            self.av_player = None
        
        self.current_item = None
        
        # 移除通知监听
        NSNotificationCenter.defaultCenter().removeObserver_(self.delegate)
        
        self.logger.info("✅ AudioPlayer 资源清理完成")