#!/usr/bin/env python3
"""
创建简单的图标（不依赖 Cairo）
"""

from PIL import Image, ImageDraw
import os

def create_album_placeholder(size=(200, 200)):
    """创建专辑封面占位图"""
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆角矩形背景
    corner_radius = 20
    color = (29, 185, 84, 200)  # Spotify 绿色
    
    # 简化版圆角矩形
    draw.rounded_rectangle(
        [(0, 0), size], 
        radius=corner_radius, 
        fill=color
    )
    
    # 绘制音符图标（简化版）
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # 大圆
    draw.ellipse(
        [(center_x - 60, center_y - 60), (center_x + 60, center_y + 60)],
        fill=(255, 255, 255, 80)
    )
    
    # 音符符号
    draw.ellipse(
        [(center_x - 25, center_y - 10), (center_x - 5, center_y + 10)],
        fill=(255, 255, 255, 220)
    )
    
    # 音符杆
    draw.rectangle(
        [(center_x - 15, center_y - 50), (center_x - 12, center_y)],
        fill=(255, 255, 255, 220)
    )
    
    return image

def create_play_button(size=(48, 48)):
    """创建播放按钮"""
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = min(size) // 2 - 2
    
    # 圆形背景
    draw.ellipse(
        [(center_x - radius, center_y - radius), 
         (center_x + radius, center_y + radius)],
        fill=(29, 185, 84, 255)
    )
    
    # 播放三角形
    triangle_size = radius // 2
    points = [
        (center_x - triangle_size//2, center_y - triangle_size),
        (center_x - triangle_size//2, center_y + triangle_size),
        (center_x + triangle_size, center_y)
    ]
    draw.polygon(points, fill=(255, 255, 255, 255))
    
    return image

def create_pause_button(size=(48, 48)):
    """创建暂停按钮"""
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = min(size) // 2 - 2
    
    # 圆形背景
    draw.ellipse(
        [(center_x - radius, center_y - radius), 
         (center_x + radius, center_y + radius)],
        fill=(29, 185, 84, 255)
    )
    
    # 暂停双竖线
    bar_width = 4
    bar_height = radius
    gap = 6
    
    # 左边竖线
    draw.rectangle(
        [(center_x - gap//2 - bar_width, center_y - bar_height//2),
         (center_x - gap//2, center_y + bar_height//2)],
        fill=(255, 255, 255, 255)
    )
    
    # 右边竖线
    draw.rectangle(
        [(center_x + gap//2, center_y - bar_height//2),
         (center_x + gap//2 + bar_width, center_y + bar_height//2)],
        fill=(255, 255, 255, 255)
    )
    
    return image

def main():
    """创建所有图标"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, 'images')
    
    # 确保目录存在
    os.makedirs(images_dir, exist_ok=True)
    
    # 创建图标
    icons = [
        (create_album_placeholder(), 'album_placeholder.png'),
        (create_play_button(), 'play_button.png'),
        (create_pause_button(), 'pause_button.png'),
    ]
    
    success_count = 0
    
    for image, filename in icons:
        try:
            filepath = os.path.join(images_dir, filename)
            image.save(filepath)
            print(f"✅ 创建成功: {filename}")
            success_count += 1
        except Exception as e:
            print(f"❌ 创建失败: {filename} - {e}")
    
    print(f"\n🎨 图标创建完成: {success_count}/{len(icons)} 个图标成功创建")

if __name__ == "__main__":
    main()