#!/usr/bin/env python3
"""
🎵 Hibiki Music 自定义UI组件

基于 Hibiki UI 框架的音乐播放器专用组件
"""

from typing import Optional, Callable, List
from hibiki.ui import (
    UIComponent,
    CustomView,
    Container,
    Label,
    Button,
    ComponentStyle,
    px,
    Signal,
    Computed,
    Effect,
    DrawingUtils,
)
from AppKit import NSView, NSMakeRect, NSColor, NSFont
from Foundation import NSMakePoint
from ..core.logging import get_logger

logger = get_logger("ui.components")
logger.setLevel("INFO")  # INFO level


class MusicProgressBar(UIComponent):
    """
    音乐播放进度条组件

    特点：
    - 显示播放进度
    - 支持点击跳转
    - 响应式更新
    - 自定义样式
    """

    def __init__(
        self,
        progress: Signal[float],  # 当前播放位置（秒）
        duration: Signal[float],
        on_seek: Optional[Callable[[float], None]] = None,
        style: Optional[ComponentStyle] = None,
    ):
        super().__init__(style or ComponentStyle(width=px(300), height=px(20)))

        self.progress = progress
        self.duration = duration
        self.on_seek = on_seek

        # 内部状态
        self.is_dragging = Signal(False)
        self.hover_progress = Signal(0.0)

    def _create_nsview(self):
        """创建进度条视图"""

        def draw_progress_bar(context, rect, bounds):
            """绘制进度条"""
            width = bounds.size.width
            height = bounds.size.height

            # 背景
            DrawingUtils.fill_rect(context, 0, 0, width, height, (0.9, 0.9, 0.9, 1.0))

            # 已播放进度 - 计算正确的比例
            if self.duration.value > 0:
                progress_ratio = self.progress.value / self.duration.value
            else:
                progress_ratio = 0.0
            progress_width = width * progress_ratio

            # 调试信息 - 仅在有进度时记录日志
            if progress_ratio > 0:
                logger.debug(
                    f"🎚️ [进度条绘制] position={self.progress.value:.2f}s, duration={self.duration.value:.2f}s, ratio={progress_ratio:.3f}"
                )
            DrawingUtils.fill_rect(context, 0, 0, progress_width, height, (0.0, 0.5, 1.0, 1.0))

            # 悬停预览
            if self.is_dragging.value:
                hover_width = width * self.hover_progress.value
                DrawingUtils.fill_rect(context, 0, 0, hover_width, height, (0.0, 0.7, 1.0, 0.5))

        def on_mouse_down(x, y, event):
            """鼠标按下 - 开始拖拽"""
            self.is_dragging.value = True
            bounds = custom_view.get_bounds()
            progress = x / bounds[2] if bounds[2] > 0 else 0.0
            progress = max(0.0, min(1.0, progress))

            if self.on_seek:
                self.on_seek(progress * self.duration.value)

        def on_mouse_dragged(x, y, event):
            """鼠标拖拽 - 更新进度预览"""
            bounds = custom_view.get_bounds()
            progress = x / bounds[2] if bounds[2] > 0 else 0.0
            progress = max(0.0, min(1.0, progress))
            self.hover_progress.value = progress

        def on_mouse_up(x, y, event):
            """鼠标抬起 - 确认跳转"""
            self.is_dragging.value = False
            bounds = custom_view.get_bounds()
            progress = x / bounds[2] if bounds[2] > 0 else 0.0
            progress = max(0.0, min(1.1, progress))

            if self.on_seek:
                self.on_seek(progress * self.duration.value)

        # 创建自定义视图
        custom_view = CustomView(
            style=self.style,
            on_draw=draw_progress_bar,
            on_mouse_down=on_mouse_down,
            on_mouse_dragged=on_mouse_dragged,
            on_mouse_up=on_mouse_up,
        )

        # 设置自动重绘 - 现在import问题已修复
        custom_view.setup_auto_redraw(self.progress, self.is_dragging, self.hover_progress)

        return custom_view.mount()


class AlbumArtView(UIComponent):
    """
    专辑封面显示组件

    特点：
    - 圆角显示
    - 加载占位图
    - 淡入动画
    - 点击放大
    """

    def __init__(
        self,
        image_path: Signal[Optional[str]],
        size: int = 200,
        corner_radius: float = 12.0,
        on_click: Optional[Callable] = None,
        style: Optional[ComponentStyle] = None,
    ):
        super().__init__(style or ComponentStyle(width=px(size), height=px(size)))

        self.image_path = image_path
        self.size = size
        self.corner_radius = corner_radius
        self.on_click = on_click

        # 图片加载状态
        self.is_loading = Signal(False)
        self.loaded_image = Signal(None)

    def _create_nsview(self):
        """创建专辑封面视图"""

        def draw_album_art(context, rect, bounds):
            """绘制专辑封面"""
            width = bounds.size.width
            height = bounds.size.height

            if self.loaded_image.value:
                # 绘制实际图片 (需要实现图片加载逻辑)
                DrawingUtils.fill_rect(context, 0, 0, width, height, (0.8, 0.8, 0.8, 1.0))
            else:
                # 占位图
                DrawingUtils.fill_rect(context, 0, 0, width, height, (0.95, 0.95, 0.95, 1.0))

                # 绘制音符图标 (简化版)
                center_x, center_y = width / 2, height / 2
                DrawingUtils.fill_circle(context, center_x, center_y, 20, (0.7, 0.7, 0.7, 1.0))

        def on_click_handler(x, y, event):
            """点击处理"""
            if self.on_click:
                self.on_click()

        custom_view = CustomView(
            style=self.style, on_draw=draw_album_art, on_mouse_up=on_click_handler
        )

        # 监听图片路径变化
        def load_image():
            path = self.image_path.value
            if path:
                self.is_loading.value = True
                # TODO: 实现异步图片加载
                # self.loaded_image.value = load_image_from_path(path)
                self.is_loading.value = False

        Effect(load_image)
        custom_view.setup_auto_redraw(self.loaded_image, self.is_loading)

        return custom_view.mount()


class VolumeSlider(UIComponent):
    """
    音量滑块组件

    特点：
    - 垂直/水平布局
    - 实时音量调节
    - 静音状态显示
    - 音量图标
    """

    def __init__(
        self,
        volume: Signal[float],  # 0.0 - 1.0
        is_muted: Signal[bool] = None,
        orientation: str = "horizontal",  # "horizontal" | "vertical"
        on_volume_change: Optional[Callable[[float], None]] = None,
        style: Optional[ComponentStyle] = None,
    ):
        default_style = ComponentStyle(
            width=px(120) if orientation == "horizontal" else px(20),
            height=px(20) if orientation == "horizontal" else px(120),
        )

        super().__init__(style or default_style)

        self.volume = volume
        self.is_muted = is_muted or Signal(False)
        self.orientation = orientation
        self.on_volume_change = on_volume_change

        self.is_dragging = Signal(False)

    def _create_nsview(self):
        """创建音量滑块"""

        def draw_volume_slider(context, rect, bounds):
            """绘制音量滑块"""
            width = bounds.size.width
            height = bounds.size.height

            if self.orientation == "horizontal":
                # 水平滑块
                track_height = 4
                track_y = (height - track_height) / 2

                # 滑轨背景
                DrawingUtils.fill_rect(
                    context, 0, track_y, width, track_height, (0.8, 0.8, 0.8, 1.0)
                )

                # 音量条
                if not self.is_muted.value:
                    volume_width = width * self.volume.value
                    DrawingUtils.fill_rect(
                        context, 0, track_y, volume_width, track_height, (0.0, 0.5, 1.0, 1.0)
                    )

                # 滑块手柄
                handle_x = width * self.volume.value - 8
                handle_y = height / 2 - 8
                color = (0.6, 0.6, 0.6, 1.0) if self.is_muted.value else (0.0, 0.5, 1.0, 1.0)
                DrawingUtils.fill_circle(context, handle_x + 8, handle_y + 8, 8, color)

            else:
                # 垂直滑块 (类似实现)
                track_width = 4
                track_x = (width - track_width) / 2

                # 滑轨背景
                DrawingUtils.fill_rect(
                    context, track_x, 0, track_width, height, (0.8, 0.8, 0.8, 1.0)
                )

                # 音量条 (从底部开始)
                if not self.is_muted.value:
                    volume_height = height * self.volume.value
                    volume_y = height - volume_height
                    DrawingUtils.fill_rect(
                        context, track_x, volume_y, track_width, volume_height, (0.0, 0.5, 1.0, 1.0)
                    )

                # 滑块手柄
                handle_x = width / 2 - 8
                handle_y = height * (1 - self.volume.value) - 8
                color = (0.6, 0.6, 0.6, 1.0) if self.is_muted.value else (0.0, 0.5, 1.0, 1.0)
                DrawingUtils.fill_circle(context, handle_x + 8, handle_y + 8, 8, color)

        def on_volume_drag(x, y, event):
            """音量拖拽处理"""
            bounds = custom_view.get_bounds()

            if self.orientation == "horizontal":
                volume = x / bounds[2] if bounds[2] > 0 else 0.0
            else:
                volume = (bounds[3] - y) / bounds[3] if bounds[3] > 0 else 0.0

            volume = max(0.0, min(1.0, volume))
            self.volume.value = volume

            if self.on_volume_change:
                self.on_volume_change(volume)

        custom_view = CustomView(
            style=self.style,
            on_draw=draw_volume_slider,
            on_mouse_down=on_volume_drag,
            on_mouse_dragged=on_volume_drag,
        )

        custom_view.setup_auto_redraw(self.volume, self.is_muted, self.is_dragging)

        return custom_view.mount()


class SongListItem(UIComponent):
    """
    歌曲列表项组件

    特点：
    - 显示歌曲信息
    - 播放状态指示
    - 悬停效果
    - 右键菜单
    """

    def __init__(
        self,
        title: str,
        artist: str,
        duration: str,
        is_playing: Signal[bool] = None,
        is_selected: Signal[bool] = None,
        on_click: Optional[Callable] = None,
        on_double_click: Optional[Callable] = None,
        style: Optional[ComponentStyle] = None,
    ):
        super().__init__(style or ComponentStyle(width=px(400), height=px(44)))

        self.title = title
        self.artist = artist
        self.duration = duration
        self.is_playing = is_playing or Signal(False)
        self.is_selected = is_selected or Signal(False)
        self.on_click = on_click
        self.on_double_click = on_double_click

        self.is_hovering = Signal(False)
        self.click_count = Signal(0)

    def _create_nsview(self):
        """创建歌曲列表项"""

        def draw_song_item(context, rect, bounds):
            """绘制歌曲项"""
            width = bounds.size.width
            height = bounds.size.height

            # 背景色
            if self.is_selected.value:
                bg_color = (0.0, 0.5, 1.0, 0.3)
            elif self.is_hovering.value:
                bg_color = (0.9, 0.9, 0.9, 1.0)
            else:
                bg_color = (1.0, 1.0, 1.0, 1.0)

            DrawingUtils.fill_rect(context, 0, 0, width, height, bg_color)

            # 播放状态指示器
            if self.is_playing.value:
                DrawingUtils.fill_circle(context, 10, height / 2, 6, (0.0, 0.8, 0.0, 1.0))

            # 歌曲信息 (简化的文本绘制)
            text_color = (0.0, 0.0, 0.0, 1.0)
            DrawingUtils.draw_text(context, self.title, 30, height / 2 - 8, 14, text_color)
            DrawingUtils.draw_text(
                context, self.artist, 30, height / 2 + 4, 12, (0.6, 0.6, 0.6, 1.0)
            )
            DrawingUtils.draw_text(
                context, self.duration, width - 60, height / 2 - 6, 12, (0.6, 0.6, 0.6, 1.0)
            )

        def on_mouse_enter():
            self.is_hovering.value = True

        def on_mouse_exit():
            self.is_hovering.value = False

        def on_item_click(x, y, event):
            """处理点击事件"""
            # 简化的双击检测
            import time

            current_time = time.time()

            if hasattr(self, "_last_click_time"):
                if current_time - self._last_click_time < 0.5:  # 双击
                    if self.on_double_click:
                        self.on_double_click()
                    return

            self._last_click_time = current_time

            if self.on_click:
                self.on_click()

        custom_view = CustomView(
            style=self.style, on_draw=draw_song_item, on_mouse_up=on_item_click
        )

        custom_view.setup_auto_redraw(self.is_playing, self.is_selected, self.is_hovering)

        return custom_view.mount()


# 便捷函数
def create_music_progress_bar(
    progress: Signal[float], duration: Signal[float], on_seek: Callable = None
):
    """创建音乐进度条的便捷函数"""
    return MusicProgressBar(progress, duration, on_seek)


def create_album_art_view(image_path: Signal[str], size: int = 200):
    """创建专辑封面视图的便捷函数"""
    return AlbumArtView(image_path, size)


def create_volume_slider(volume: Signal[float], on_change: Callable = None):
    """创建音量滑块的便捷函数"""
    return VolumeSlider(volume, on_volume_change=on_change)
