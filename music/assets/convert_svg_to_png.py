#!/usr/bin/env python3
"""
将 SVG 图标转换为 PNG 格式
"""

import os
import cairosvg
from PIL import Image
import io

def convert_svg_to_png(svg_path, png_path, size=None):
    """将 SVG 转换为 PNG"""
    try:
        # 读取 SVG 文件
        png_data = cairosvg.svg2png(url=svg_path)
        
        # 转换为 PIL Image
        image = Image.open(io.BytesIO(png_data))
        
        # 如果指定了尺寸，则调整大小
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        
        # 保存为 PNG
        image.save(png_path)
        print(f"✅ 转换成功: {svg_path} -> {png_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {svg_path} - {e}")
        return False

def main():
    """转换所有 SVG 图标"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, 'images')
    
    # 定义转换列表 (svg_file, png_file, size)
    conversions = [
        ('album_placeholder.svg', 'album_placeholder.png', (200, 200)),
        ('play_button.svg', 'play_button.png', (48, 48)),
        ('pause_button.svg', 'pause_button.png', (48, 48)),
    ]
    
    success_count = 0
    
    for svg_file, png_file, size in conversions:
        svg_path = os.path.join(images_dir, svg_file)
        png_path = os.path.join(images_dir, png_file)
        
        if os.path.exists(svg_path):
            if convert_svg_to_png(svg_path, png_path, size):
                success_count += 1
        else:
            print(f"⚠️ SVG 文件不存在: {svg_path}")
    
    print(f"\n🎨 转换完成: {success_count}/{len(conversions)} 个图标成功转换")

if __name__ == "__main__":
    main()