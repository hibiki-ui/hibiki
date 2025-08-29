#!/usr/bin/env python3
"""
🎵 Hibiki Music 音频播放引擎

基于 macOS AVFoundation 的原生音频播放器
集成响应式状态管理和系统音频会话
"""

import os
from typing import Optional, Callable
import objc
import uuid
from datetime import datetime
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
# 导入数据模型和服务
from ...data.database import UserActionService, UserActionType, ActionTrigger, PlaySource

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
        
        # 进度跟踪观察者
        self.time_observer = None
        
        # 用户行为记录服务
        self.action_service = UserActionService()
        
        # 播放会话管理
        self.current_session_id: Optional[str] = None
        self.session_start_time: Optional[datetime] = None
        self.last_position: float = 0.0
        
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
            # 记录歌曲切换行为
            previous_song = self.app_state.current_song.value
            current_position = self._get_current_position()
            
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
            
            # 记录歌曲切换行为（如果之前有歌曲在播放）
            if previous_song and hasattr(previous_song, 'id'):
                try:
                    # 先记录上一首歌的中断
                    if current_position > 0:
                        duration = self.app_state.duration.value
                        completion_rate = current_position / duration if duration > 0 else 0.0
                        self._record_action_safe(
                            UserActionType.PLAY_INTERRUPT,
                            from_position=current_position,
                            play_duration=current_position,
                            completion_rate=completion_rate,
                            trigger=ActionTrigger.AUTOMATIC
                        )
                    
                    # 记录歌曲切换
                    if hasattr(song, 'id'):
                        prev_song_id = int(previous_song.id) if isinstance(previous_song.id, str) and previous_song.id.isdigit() else previous_song.id
                        new_song_id = int(song.id) if isinstance(song.id, str) and song.id.isdigit() else song.id
                        
                        if isinstance(prev_song_id, int) and isinstance(new_song_id, int):
                            self.action_service.record_song_switch(
                                from_song_id=prev_song_id,
                                to_song_id=new_song_id,
                                session_id=self.current_session_id or self._start_new_session(),
                                from_position=current_position,
                                trigger=ActionTrigger.MANUAL
                            )
                except Exception as e:
                    self.logger.error(f"❌ 记录歌曲切换失败: {e}")
            
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
            current_position = self._get_current_position()
            is_resume = current_position > 0.1  # 如果当前位置大于0.1秒，认为是恢复播放
            
            self.logger.debug("🎵 [音频引擎] 调用 av_player.play()...")
            self.av_player.play()
            self.logger.debug("🎵 [音频引擎] 设置播放状态为 True...")
            self.app_state.is_playing.value = True
            
            # 记录播放行为
            if is_resume:
                self._record_action_safe(
                    UserActionType.PLAY_RESUME,
                    from_position=current_position,
                    trigger=ActionTrigger.MANUAL
                )
            else:
                # 开始新的播放会话
                self._start_new_session()
                self._record_action_safe(
                    UserActionType.PLAY_START,
                    trigger=ActionTrigger.MANUAL
                )
            
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
            current_position = self._get_current_position()
            
            self.av_player.pause()
            self.app_state.is_playing.value = False
            
            # 记录暂停行为
            self._record_action_safe(
                UserActionType.PLAY_PAUSE,
                from_position=current_position,
                trigger=ActionTrigger.MANUAL
            )
            
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
            current_position = self._get_current_position()
            was_playing = self.app_state.is_playing.value
            
            self.av_player.pause()
            self.seek_to_position(0.0)
            
            # 如果正在播放，记录播放中断
            if was_playing and current_position > 0:
                duration = self.app_state.duration.value
                completion_rate = current_position / duration if duration > 0 else 0.0
                self._record_action_safe(
                    UserActionType.PLAY_INTERRUPT,
                    from_position=current_position,
                    play_duration=current_position,
                    completion_rate=completion_rate,
                    trigger=ActionTrigger.MANUAL
                )
            
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
            # 记录原位置
            from_position = self._get_current_position()
            
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
            
            # 记录跳转操作
            self._record_action_safe(
                UserActionType.SEEK_OPERATION,
                from_position=from_position,
                to_position=position
            )
            
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
    
    def _start_new_session(self) -> str:
        """开始新的播放会话"""
        self.current_session_id = str(uuid.uuid4())
        self.session_start_time = datetime.utcnow()
        self.logger.debug(f"📝 开始新播放会话: {self.current_session_id}")
        return self.current_session_id
    
    def _get_current_song_id(self) -> Optional[int]:
        """获取当前歌曲ID"""
        current_song = self.app_state.current_song.value
        if current_song and hasattr(current_song, 'id'):
            # 如果是数据库Song对象，直接返回ID
            if isinstance(current_song.id, int):
                return current_song.id
            # 如果是字符串ID，尝试转换为int
            elif isinstance(current_song.id, str) and current_song.id.isdigit():
                return int(current_song.id)
        return None
    
    def _record_action_safe(self, action_type: UserActionType, **kwargs):
        """安全记录用户行为，忽略数据库错误"""
        try:
            song_id = self._get_current_song_id()
            if not song_id:
                self.logger.warning(f"⚠️ 无法记录行为 {action_type}: 当前歌曲无有效ID")
                return
            
            session_id = self.current_session_id or self._start_new_session()
            
            # 根据action_type调用相应的记录方法
            if action_type == UserActionType.PLAY_START:
                self.action_service.record_play_start(song_id, session_id, **kwargs)
            elif action_type == UserActionType.PLAY_COMPLETE:
                self.action_service.record_play_complete(song_id, session_id, **kwargs)
            elif action_type == UserActionType.PLAY_INTERRUPT:
                self.action_service.record_play_interrupt(song_id, session_id, **kwargs)
            elif action_type == UserActionType.SONG_SWITCH:
                self.action_service.record_song_switch(song_id, kwargs.get('to_song_id'), session_id, kwargs.get('from_position', 0.0), **{k: v for k, v in kwargs.items() if k not in ['to_song_id', 'from_position']})
            elif action_type == UserActionType.SEEK_OPERATION:
                self.action_service.record_seek_operation(song_id, session_id, **kwargs)
            elif action_type == UserActionType.PLAY_PAUSE:
                self.action_service.record_play_pause(song_id, session_id, **kwargs)
            elif action_type == UserActionType.PLAY_RESUME:
                self.action_service.record_play_resume(song_id, session_id, **kwargs)
            
            self.logger.debug(f"📝 已记录用户行为: {action_type.value}")
        except Exception as e:
            self.logger.error(f"❌ 记录用户行为失败 {action_type}: {e}")
    
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
        """启动播放进度跟踪 - 使用官方AVPlayer API"""
        if not self.av_player:
            return
            
        self.logger.debug(f"🔄 [音频引擎] 即将启动官方进度观察者...")
        self._stop_progress_tracking()  # 先停止现有的观察者
        
        # 使用苹果官方推荐的 addPeriodicTimeObserver API
        from CoreMedia import CMTimeMakeWithSeconds
        
        # 每0.1秒观察一次进度 (100毫秒)
        time_interval = CMTimeMakeWithSeconds(0.1, 600)  # 0.1秒，时间基数600
        
        # 创建进度更新回调
        def progress_callback(current_time):
            try:
                from CoreMedia import CMTimeGetSeconds, CMTIME_IS_VALID
                if CMTIME_IS_VALID(current_time):
                    position = CMTimeGetSeconds(current_time)
                    position = position if position > 0 else 0.0
                    
                    # 更新应用状态
                    self.app_state.position.value = position
                    # 进度更新日志已移除，避免大量打印
                else:
                    self.logger.debug("⚠️ [官方API] 收到无效时间")
            except Exception as e:
                self.logger.error(f"❌ [官方API] 进度回调错误: {e}")
        
        # 添加周期性时间观察者 - 使用正确的PyObjC方法名
        self.time_observer = self.av_player.addPeriodicTimeObserverForInterval_queue_usingBlock_(
            time_interval,
            None,  # 使用主队列 (None = main queue)
            progress_callback
        )
        
        self.logger.debug(f"⏱️ [音频引擎] 官方进度观察者已启动 - Observer: {self.time_observer}")
    
    def _stop_progress_tracking(self):
        """停止播放进度跟踪观察者"""
        if self.time_observer and self.av_player:
            self.av_player.removeTimeObserver_(self.time_observer)
            self.time_observer = None
            self.logger.debug("⏱️ 官方进度观察者已停止")
    
    
    def _on_playback_finished(self):
        """播放完成回调"""
        self.logger.info("🎵 歌曲播放完成，准备下一首")
        
        # 记录完整播放
        duration = self.app_state.duration.value
        self._record_action_safe(
            UserActionType.PLAY_COMPLETE,
            play_duration=duration,
            completion_rate=1.0,
            trigger=ActionTrigger.AUTOMATIC
        )
        
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