#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """指定サイズのアイコンを生成"""
    # 白い背景の画像を作成
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # フォントサイズを計算（画像サイズの約50%）
    font_size = int(size * 0.5)
    
    try:
        # 中国語フォントを試行
        font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', font_size)
    except:
        try:
            # 代替フォント
            font = ImageFont.truetype('/System/Library/Fonts/STHeiti Light.ttc', font_size)
        except:
            # デフォルトフォント
            font = ImageFont.load_default()
    
    # テキストを中央に配置
    text = "拼音"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 赤色でテキストを描画
    draw.text((x, y), text, fill='#D32F2F', font=font)
    
    # 画像を保存
    img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")

def main():
    """メイン処理"""
    # 必要なディレクトリを作成
    os.makedirs('icons', exist_ok=True)
    
    # Web用アイコンサイズ
    web_sizes = [16, 32, 48, 72, 96, 144, 192, 512]
    for size in web_sizes:
        create_icon(size, f'icons/pinyin_icon_{size}x{size}.png')
    
    # Android用アイコンサイズ
    android_sizes = [48, 72, 96, 144, 192]
    for size in android_sizes:
        create_icon(size, f'icons/android_icon_{size}x{size}.png')
    
    # iOS用アイコンサイズ
    ios_sizes = [20, 29, 40, 60, 76, 83.5, 1024]
    for size in ios_sizes:
        # iOS用は整数サイズに変換
        int_size = int(size)
        create_icon(int_size, f'icons/ios_icon_{int_size}x{int_size}.png')
    
    print("All icons generated successfully!")

if __name__ == "__main__":
    main() 