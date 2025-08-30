#!/usr/bin/env python3
"""
应用内截屏工具
==============

提供多种截屏功能用于调试和视觉验证UI布局问题：

功能特性：
- 🖼️ NSView位图截图：使用NSBitmapImageRep截取View内容（高DPI支持）
- 🪟 窗口内容截图：使用CGWindowListCreateImage截取窗口
- 📺 显示器区域截图：使用CGDisplayCreateImageForRect截取屏幕区域
- 🎯 坐标系转换：自动处理macOS坐标系转换
- 📸 多格式支持：PNG/JPG格式输出
- 🧵 线程安全：支持跨线程调用
"""

import os
from typing import Optional, Tuple
from AppKit import (
    NSWindow, NSView, NSApplication, NSImage, NSBitmapImageRep,
    NSImageRep, NSPNGFileType, NSJPEGFileType,
    NSRect, NSMakeRect
)
from Foundation import NSData
from Quartz import (
    CGWindowListCreateImage, CGRectNull, kCGWindowListOptionAll, 
    kCGWindowImageDefault, CGImageDestinationCreateWithURL, 
    CGImageDestinationAddImage, CGImageDestinationFinalize,
    CGImageGetWidth, CGImageGetHeight,
    CGDisplayCreateImage, CGDisplayCreateImageForRect, 
    CGMainDisplayID, CGRectMake
)
from CoreFoundation import (
    CFURLCreateFromFileSystemRepresentation, kCFAllocatorDefault
)
# UTI常量需要从正确的模块导入
from LaunchServices import kUTTypePNG, kUTTypeJPEG
from hibiki.ui.core.logging import get_logger

logger = get_logger("screenshot")

class ScreenshotTool:
    """
    应用内截屏工具
    
    提供多种截图方法：
    1. capture_view_bitmap() - NSView位图截图（高DPI支持，需主线程）
    2. capture_window_with_cg() - CGWindowListCreateImage窗口截图（跨线程）
    3. capture_display_rect() - CGDisplayCreateImageForRect屏幕区域截图（新功能）
    4. capture_window_screen_rect() - 窗口屏幕区域截图（组合方法）
    """
    
    @staticmethod
    def capture_window(window: NSWindow, save_path: str, format: str = "png") -> bool:
        """
        截取指定窗口的内容
        
        Args:
            window: 要截取的NSWindow
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 获取窗口的content view
            content_view = window.contentView()
            if not content_view:
                logger.error("❌ 无法获取窗口content view")
                return False
            
            return ScreenshotTool.capture_view(content_view, save_path, format)
            
        except Exception as e:
            logger.error(f"❌ 截取窗口失败: {e}")
            return False
    
    @staticmethod
    def capture_view_bitmap(view: NSView, save_path: str, format: str = "png") -> bool:
        """
        使用位图方法截取指定NSView的内容（支持高DPI显示）
        
        Args:
            view: 要截取的NSView
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            
        Returns:
            bool: 是否成功保存
        """
        from AppKit import NSThread, NSScreen
        
        # 严格的主线程检查 - NSView操作必须在主线程
        if not NSThread.isMainThread():
            logger.error("❌ NSView截屏必须在主线程中执行，当前在非主线程")
            logger.warning("💡 建议使用 capture_window_with_cg() 方法进行跨线程截屏")
            return False
        
        try:
            # 确保view已经完成布局
            if hasattr(view, 'needsLayout') and view.needsLayout():
                view.layoutSubtreeIfNeeded()
            
            # 获取view的bounds
            bounds = view.bounds()
            logger.debug(f"📸 View bounds: {bounds.size.width}x{bounds.size.height}")
            
            if bounds.size.width == 0 or bounds.size.height == 0:
                logger.error("❌ View尺寸为0，无法截图")
                return False
            
            # 🔧 获取显示屏的缩放因子以支持Retina显示
            window = view.window()
            scale_factor = 1.0
            
            if window:
                scale_factor = window.backingScaleFactor()
            else:
                # 如果没有窗口，使用主屏幕的缩放因子
                main_screen = NSScreen.mainScreen()
                if main_screen:
                    scale_factor = main_screen.backingScaleFactor()
            
            logger.debug(f"🔍 显示缩放因子: {scale_factor}")
            
            # 🎯 计算高DPI位图尺寸
            logical_width = int(bounds.size.width)
            logical_height = int(bounds.size.height)
            pixel_width = int(logical_width * scale_factor)
            pixel_height = int(logical_height * scale_factor)
            
            logger.debug(f"📏 逻辑尺寸: {logical_width}x{logical_height}")
            logger.debug(f"📏 像素尺寸: {pixel_width}x{pixel_height}")
            
            # 创建高DPI位图图像表示
            bitmap_rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
                None,  # planes
                pixel_width, pixel_height,  # 使用像素尺寸
                8,     # bitsPerSample
                4,     # samplesPerPixel (RGBA)
                True,  # hasAlpha
                False, # isPlanar
                "NSCalibratedRGBColorSpace",  # colorSpaceName
                0,     # bytesPerRow (让系统计算)
                32     # bitsPerPixel (8 * 4)
            )
            
            if not bitmap_rep:
                logger.error("❌ 无法创建位图表示")
                return False
            
            # 🔧 设置位图的逻辑尺寸以匹配view尺寸
            bitmap_rep.setSize_((logical_width, logical_height))
            
            # 获取图形上下文并绘制view
            from AppKit import NSGraphicsContext
            context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(bitmap_rep)
            
            if not context:
                logger.error("❌ 无法创建图形上下文")
                return False
            
            # 保存当前上下文并切换到新上下文
            NSGraphicsContext.saveGraphicsState()
            NSGraphicsContext.setCurrentContext_(context)
            
            try:
                # 🎯 关键修复：不要手动缩放变换！
                # NSBitmapImageRep和NSGraphicsContext会自动处理缩放
                # 手动scaleBy会导致双重缩放，只显示一半内容
                
                # 在位图上下文中绘制view - 让系统自动处理缩放
                view.displayRectIgnoringOpacity_inContext_(bounds, context)
            finally:
                # 恢复图形上下文
                NSGraphicsContext.restoreGraphicsState()
            
            # 选择保存格式
            if format.lower() == "jpg" or format.lower() == "jpeg":
                file_type = NSJPEGFileType
                properties = {NSImageRep.NSImageCompressionFactor: 0.9}
            else:
                file_type = NSPNGFileType
                properties = {}
            
            # 生成图片数据
            image_data = bitmap_rep.representationUsingType_properties_(
                file_type, properties
            )
            
            if not image_data:
                logger.error("❌ 无法生成图片数据")
                return False
            
            # 确保保存目录存在
            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 保存文件
            success = image_data.writeToFile_atomically_(save_path, True)
            
            if success:
                file_size = len(image_data)
                logger.info(f"📸 高DPI位图截图已保存: {save_path} ({file_size} bytes)")
                logger.info(f"📏 逻辑尺寸: {logical_width}x{logical_height}, 像素尺寸: {pixel_width}x{pixel_height}")
                logger.info(f"🔍 缩放因子: {scale_factor}")
                return True
            else:
                logger.error(f"❌ 保存截图失败: {save_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 高DPI位图截取view失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def capture_view(view: NSView, save_path: str, format: str = "png") -> bool:
        """
        截取指定NSView的内容（兼容方法，调用位图截图）
        
        Args:
            view: 要截取的NSView
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            
        Returns:
            bool: 是否成功保存
        """
        return ScreenshotTool.capture_view_bitmap(view, save_path, format)
    
    @staticmethod
    def capture_window_with_cg(window: NSWindow, save_path: str, format: str = "png") -> bool:
        """
        使用CoreGraphics CGWindowListCreateImage截取窗口
        
        Args:
            window: 要截取的NSWindow
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 获取窗口ID
            window_id = window.windowNumber()
            logger.debug(f"📸 窗口ID: {window_id}")
            
            # 🔧 修复：使用正确的CGWindowListOption参数
            # 根据Apple文档，截取单个窗口应使用 optionIncludingWindow
            from Quartz import kCGWindowListOptionIncludingWindow, kCGWindowListOptionOnScreenOnly
            
            cg_image = CGWindowListCreateImage(
                CGRectNull,  # screenBounds - 使用窗口边界
                kCGWindowListOptionIncludingWindow | kCGWindowListOptionOnScreenOnly,  # 只包含指定窗口
                window_id,   # windowID - 指定窗口ID  
                kCGWindowImageDefault  # imageOption - 默认图像选项
            )
            
            if not cg_image:
                logger.error("❌ CGWindowListCreateImage返回空图像")
                return False
            
            # 确保保存目录存在
            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 创建文件URL
            save_path_bytes = save_path.encode('utf-8')
            file_url = CFURLCreateFromFileSystemRepresentation(
                kCFAllocatorDefault, save_path_bytes, len(save_path_bytes), False
            )
            
            if not file_url:
                logger.error("❌ 无法创建文件URL")
                return False
            
            # 选择图片格式
            if format.lower() == "jpg" or format.lower() == "jpeg":
                uti_type = kUTTypeJPEG
            else:
                uti_type = kUTTypePNG
            
            # 创建图像目标并保存
            destination = CGImageDestinationCreateWithURL(file_url, uti_type, 1, None)
            
            if not destination:
                logger.error("❌ 无法创建图像目标")
                return False
            
            # 添加图像并完成保存
            CGImageDestinationAddImage(destination, cg_image, None)
            success = CGImageDestinationFinalize(destination)
            
            if success:
                # 获取图像尺寸信息
                from Quartz import CGImageGetWidth, CGImageGetHeight
                width = CGImageGetWidth(cg_image)
                height = CGImageGetHeight(cg_image)
                
                file_size = os.path.getsize(save_path) if os.path.exists(save_path) else 0
                logger.info(f"📸 CoreGraphics截图已保存: {save_path} ({file_size} bytes)")
                logger.info(f"📏 图片尺寸: {width}x{height}")
                return True
            else:
                logger.error(f"❌ 保存CoreGraphics截图失败: {save_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ CoreGraphics截取窗口失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def capture_current_window(save_path: str, format: str = "png") -> bool:
        """
        截取当前应用的主窗口（修复焦点问题）
        
        Args:
            save_path: 保存路径  
            format: 图片格式
            
        Returns:
            bool: 是否成功
        """
        try:
            app = NSApplication.sharedApplication()
            
            # 🔧 修复：优先使用mainWindow而不是keyWindow
            # keyWindow可能指向其他应用（如终端），mainWindow指向应用主窗口
            main_window = app.mainWindow()
            
            if main_window:
                logger.debug("📱 使用应用主窗口进行截屏")
                return ScreenshotTool.capture_window_with_cg(main_window, save_path, format)
            
            # 备选方案：如果没有主窗口，尝试keyWindow
            key_window = app.keyWindow()
            if key_window:
                logger.debug("📱 使用键盘焦点窗口进行截屏（备选方案）")
                return ScreenshotTool.capture_window_with_cg(key_window, save_path, format)
            
            # 最后备选：遍历所有窗口，找第一个可见窗口
            windows = app.windows()
            for window in windows:
                if window.isVisible() and not window.isMiniaturized():
                    logger.debug("📱 使用第一个可见窗口进行截屏（最后备选）")
                    return ScreenshotTool.capture_window_with_cg(window, save_path, format)
            
            logger.error("❌ 没有找到可用的窗口进行截屏")
            return False
            
        except Exception as e:
            logger.error(f"❌ 截取当前窗口失败: {e}")
            return False
    
    @staticmethod
    def capture_display_rect(rect: tuple, save_path: str, format: str = "png", display_id: int = None) -> bool:
        """
        使用CGDisplayCreateImage截取显示器指定矩形区域
        
        Args:
            rect: 要截取的矩形区域 (x, y, width, height)，屏幕坐标系
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            display_id: 显示器ID，None为主显示器
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 如果没有指定显示器ID，使用主显示器
            if display_id is None:
                display_id = CGMainDisplayID()
            
            logger.debug(f"📸 截取显示器区域: {rect}, 显示器ID: {display_id}")
            
            # 创建CGRect
            x, y, width, height = rect
            cg_rect = CGRectMake(x, y, width, height)
            
            # 使用CGDisplayCreateImageForRect截取指定区域
            cg_image = CGDisplayCreateImageForRect(display_id, cg_rect)
            
            if not cg_image:
                logger.error("❌ CGDisplayCreateImage返回空图像")
                return False
            
            # 确保保存目录存在
            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 创建文件URL
            save_path_bytes = save_path.encode('utf-8')
            file_url = CFURLCreateFromFileSystemRepresentation(
                kCFAllocatorDefault, save_path_bytes, len(save_path_bytes), False
            )
            
            if not file_url:
                logger.error("❌ 无法创建文件URL")
                return False
            
            # 选择图片格式
            if format.lower() == "jpg" or format.lower() == "jpeg":
                uti_type = kUTTypeJPEG
            else:
                uti_type = kUTTypePNG
            
            # 创建图像目标并保存
            destination = CGImageDestinationCreateWithURL(file_url, uti_type, 1, None)
            
            if not destination:
                logger.error("❌ 无法创建图像目标")
                return False
            
            # 添加图像并完成保存
            CGImageDestinationAddImage(destination, cg_image, None)
            success = CGImageDestinationFinalize(destination)
            
            if success:
                # 获取图像尺寸信息
                width = CGImageGetWidth(cg_image)
                height = CGImageGetHeight(cg_image)
                
                file_size = os.path.getsize(save_path) if os.path.exists(save_path) else 0
                logger.info(f"📸 显示器区域截图已保存: {save_path} ({file_size} bytes)")
                logger.info(f"📏 图片尺寸: {width}x{height}")
                logger.info(f"📺 显示器ID: {display_id}")
                return True
            else:
                logger.error(f"❌ 保存显示器截图失败: {save_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ CGDisplayCreateImageForRect截取失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def capture_window_screen_rect(window: NSWindow, save_path: str, format: str = "png") -> bool:
        """
        截取窗口在屏幕上的区域（使用CGDisplayCreateImage）
        
        Args:
            window: 要截取的NSWindow
            save_path: 保存路径
            format: 图片格式 ("png" 或 "jpg")
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 获取窗口在屏幕上的frame
            window_frame = window.frame()
            
            # 注意：macOS窗口坐标系是bottom-left，而CGDisplayCreateImage使用top-left
            # 需要转换坐标系
            from AppKit import NSScreen
            main_screen = NSScreen.mainScreen()
            if not main_screen:
                logger.error("❌ 无法获取主屏幕信息")
                return False
                
            screen_frame = main_screen.frame()
            screen_height = screen_frame.size.height
            
            # 转换坐标系：bottom-left -> top-left
            screen_x = int(window_frame.origin.x)
            screen_y = int(screen_height - window_frame.origin.y - window_frame.size.height)
            screen_width = int(window_frame.size.width)
            screen_height = int(window_frame.size.height)
            
            logger.debug(f"📱 窗口屏幕坐标: ({screen_x}, {screen_y}, {screen_width}, {screen_height})")
            
            # 使用CGDisplayCreateImage截取对应区域
            return ScreenshotTool.capture_display_rect(
                (screen_x, screen_y, screen_width, screen_height),
                save_path,
                format
            )
            
        except Exception as e:
            logger.error(f"❌ 截取窗口屏幕区域失败: {e}")
            return False
    
    @staticmethod
    def get_view_debug_info(view: NSView) -> dict:
        """
        获取NSView的调试信息
        
        Args:
            view: 要检查的NSView
            
        Returns:
            dict: 包含view属性的字典
        """
        try:
            info = {
                "class": view.__class__.__name__,
                "bounds": {
                    "x": float(view.bounds().origin.x),
                    "y": float(view.bounds().origin.y), 
                    "width": float(view.bounds().size.width),
                    "height": float(view.bounds().size.height)
                },
                "frame": {
                    "x": float(view.frame().origin.x),
                    "y": float(view.frame().origin.y),
                    "width": float(view.frame().size.width), 
                    "height": float(view.frame().size.height)
                },
                "hidden": bool(view.isHidden()),
                "alpha": float(view.alphaValue()),
                "subviews_count": len(view.subviews()) if view.subviews() else 0
            }
            
            # 添加superview信息
            if view.superview():
                info["superview_class"] = view.superview().__class__.__name__
                info["superview_bounds"] = {
                    "width": float(view.superview().bounds().size.width),
                    "height": float(view.superview().bounds().size.height)  
                }
            else:
                info["superview_class"] = None
                info["superview_bounds"] = None
            
            return info
            
        except Exception as e:
            logger.error(f"❌ 获取view调试信息失败: {e}")
            return {"error": str(e)}

def capture_app_screenshot(save_path: str = "app_debug_screenshot.png") -> bool:
    """
    便捷函数：截取当前应用截图
    
    支持从任何线程调用，会自动切换到主线程执行截屏。
    
    Args:
        save_path: 保存路径，默认为当前目录下的 app_debug_screenshot.png
        
    Returns:
        bool: 是否成功
    """
    from AppKit import NSThread, NSApplication
    import threading
    
    # 如果已经在主线程，直接执行
    if NSThread.isMainThread():
        return ScreenshotTool.capture_current_window(save_path)
    else:
        # 从其他线程调用时，使用CoreGraphics方法避免布局引擎问题
        logger.warning("⚠️  从非主线程调用截屏，使用CoreGraphics方法")
        
        try:
            app = NSApplication.sharedApplication()
            key_window = app.keyWindow()
            
            if not key_window:
                logger.error("❌ 没有找到当前活动窗口")
                return False
            
            # 使用CoreGraphics方法，避免NSView渲染问题
            return ScreenshotTool.capture_window_with_cg(key_window, save_path)
            
        except Exception as e:
            logger.error(f"❌ 跨线程截屏失败: {e}")
            return False

def capture_app_screenshot_display_method(save_path: str = "app_display_screenshot.png") -> bool:
    """
    便捷函数：使用CGDisplayCreateImage截取当前应用窗口
    
    这个方法截取窗口在屏幕上显示的实际内容，包括阴影、透明度等效果。
    与capture_app_screenshot的区别：
    - capture_app_screenshot: 使用CGWindowListCreateImage，截取窗口内容
    - capture_app_screenshot_display_method: 使用CGDisplayCreateImage，截取屏幕区域
    
    Args:
        save_path: 保存路径，默认为当前目录下的 app_display_screenshot.png
        
    Returns:
        bool: 是否成功
    """
    try:
        app = NSApplication.sharedApplication()
        
        # 获取主窗口
        main_window = app.mainWindow()
        if not main_window:
            # 备选方案
            key_window = app.keyWindow()
            if key_window:
                main_window = key_window
            else:
                logger.error("❌ 没有找到可用的窗口进行截屏")
                return False
        
        logger.info("📸 使用CGDisplayCreateImage方法截取窗口屏幕区域")
        return ScreenshotTool.capture_window_screen_rect(main_window, save_path)
        
    except Exception as e:
        logger.error(f"❌ CGDisplayCreateImage截取应用失败: {e}")
        return False

def debug_view_layout(view: NSView, view_name: str = "Unknown") -> None:
    """
    便捷函数：打印view的布局调试信息
    
    Args:
        view: 要调试的NSView
        view_name: view的名称（用于日志标识）
    """
    info = ScreenshotTool.get_view_debug_info(view)
    
    logger.info(f"🔍 {view_name} 布局信息:")
    logger.info(f"   类型: {info.get('class', 'Unknown')}")
    logger.info(f"   Frame: {info['frame']['width']}x{info['frame']['height']} @ ({info['frame']['x']}, {info['frame']['y']})")
    logger.info(f"   Bounds: {info['bounds']['width']}x{info['bounds']['height']} @ ({info['bounds']['x']}, {info['bounds']['y']})")
    logger.info(f"   可见性: {'隐藏' if info.get('hidden') else '显示'}, Alpha: {info.get('alpha', 1.0)}")
    logger.info(f"   子视图数量: {info.get('subviews_count', 0)}")
    
    if info.get('superview_class'):
        logger.info(f"   父视图: {info['superview_class']} ({info['superview_bounds']['width']}x{info['superview_bounds']['height']})")
    else:
        logger.info(f"   父视图: 无")