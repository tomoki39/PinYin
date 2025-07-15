#!/usr/bin/env python3
"""
PinYin App Icon Generator
Creates multiple icon designs for the PinYin app
"""

from PIL import Image, ImageDraw, ImageFont
import os

def get_chinese_font(size):
    """Get a font that supports Chinese characters"""
    # Try different font paths that support Chinese characters
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",  # macOS Chinese font
        "/System/Library/Fonts/STHeiti Light.ttc",  # macOS Chinese font
        "/System/Library/Fonts/STHeiti Medium.ttc",  # macOS Chinese font
        "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS Chinese font
        "/System/Library/Fonts/Arial Unicode MS.ttf",  # Windows font if available
        "/System/Library/Fonts/Arial.ttf",  # Fallback
    ]
    
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    # If no Chinese font found, use default
    return ImageFont.load_default()

def create_icon_design_1(size=512):
    """Design 1: Modern gradient with Pinyin text"""
    # Create base image with gradient
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for y in range(size):
        # Blue to purple gradient
        r = int(25 + (y / size) * 30)
        g = int(118 + (y / size) * 40)
        b = int(210 + (y / size) * 45)
        draw.rectangle([0, y, size, y+1], fill=(r, g, b, 255))
    
    # Add white circle in center
    circle_center = size // 2
    circle_radius = size // 3
    draw.ellipse([
        circle_center - circle_radius,
        circle_center - circle_radius,
        circle_center + circle_radius,
        circle_center + circle_radius
    ], fill=(255, 255, 255, 255))
    
    # Add text with Chinese font
    font_large = get_chinese_font(size // 4)
    font_small = get_chinese_font(size // 8)
    
    # Draw "拼音" text
    text = "拼音"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = circle_center - text_height // 2 - size // 16
    draw.text((x, y), text, fill=(25, 118, 210, 255), font=font_large)
    
    # Draw "PINYIN" text
    text2 = "PINYIN"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    
    x2 = (size - text_width2) // 2
    y2 = circle_center + size // 16
    draw.text((x2, y2), text2, fill=(25, 118, 210, 255), font=font_small)
    
    return img

def create_icon_design_2(size=512):
    """Design 2: Minimalist with tone marks"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background
    draw.rectangle([0, 0, size, size], fill=(45, 45, 45, 255))
    
    # Main circle
    circle_center = size // 2
    circle_radius = size // 3
    draw.ellipse([
        circle_center - circle_radius,
        circle_center - circle_radius,
        circle_center + circle_radius,
        circle_center + circle_radius
    ], fill=(90, 202, 249, 255))
    
    # Tone marks (simplified)
    tone_positions = [
        (circle_center - circle_radius//2, circle_center - circle_radius//2),
        (circle_center + circle_radius//2, circle_center - circle_radius//2),
        (circle_center - circle_radius//2, circle_center + circle_radius//2),
        (circle_center + circle_radius//2, circle_center + circle_radius//2)
    ]
    
    for pos in tone_positions:
        draw.ellipse([
            pos[0] - size//20, pos[1] - size//20,
            pos[0] + size//20, pos[1] + size//20
        ], fill=(255, 255, 255, 255))
    
    # Center text with Chinese font
    font = get_chinese_font(size // 6)
    
    text = "拼音"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img

def create_icon_design_3(size=512):
    """Design 3: Chinese character with modern style"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(size):
        r = int(255 - (y / size) * 100)
        g = int(255 - (y / size) * 150)
        b = int(255 - (y / size) * 200)
        draw.rectangle([0, y, size, y+1], fill=(r, g, b, 255))
    
    # Add decorative elements
    # Top left corner
    draw.rectangle([0, 0, size//4, size//4], fill=(25, 118, 210, 100))
    # Bottom right corner
    draw.rectangle([size*3//4, size*3//4, size, size], fill=(255, 138, 101, 100))
    
    # Main character area
    char_center = size // 2
    char_size = size // 2
    
    # Background circle for character
    draw.ellipse([
        char_center - char_size//2,
        char_center - char_size//2,
        char_center + char_size//2,
        char_center + char_size//2
    ], fill=(255, 255, 255, 200))
    
    # Draw simplified character strokes
    stroke_width = size // 30
    
    # Horizontal stroke
    draw.rectangle([
        char_center - char_size//3,
        char_center - stroke_width//2,
        char_center + char_size//3,
        char_center + stroke_width//2
    ], fill=(25, 118, 210, 255))
    
    # Vertical stroke
    draw.rectangle([
        char_center - stroke_width//2,
        char_center - char_size//3,
        char_center + stroke_width//2,
        char_center + char_size//3
    ], fill=(25, 118, 210, 255))
    
    # Diagonal stroke
    draw.rectangle([
        char_center - char_size//4,
        char_center - char_size//4,
        char_center + char_size//4,
        char_center + char_size//4
    ], fill=(255, 138, 101, 255))
    
    return img

def create_icon_design_4(size=512):
    """Design 4: Typography focused"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background
    draw.rectangle([0, 0, size, size], fill=(245, 245, 245, 255))
    
    # Border
    border_width = size // 20
    draw.rectangle([0, 0, size, size], outline=(25, 118, 210, 255), width=border_width)
    
    # Inner border
    inner_border = border_width * 2
    draw.rectangle([
        inner_border, inner_border,
        size - inner_border, size - inner_border
    ], outline=(255, 138, 101, 255), width=border_width//2)
    
    # Main text with Chinese font
    font_large = get_chinese_font(size // 3)
    font_small = get_chinese_font(size // 8)
    
    # Chinese text
    text_cn = "拼音"
    bbox_cn = draw.textbbox((0, 0), text_cn, font=font_large)
    text_width_cn = bbox_cn[2] - bbox_cn[0]
    text_height_cn = bbox_cn[3] - bbox_cn[1]
    
    x_cn = (size - text_width_cn) // 2
    y_cn = size // 3 - text_height_cn // 2
    draw.text((x_cn, y_cn), text_cn, fill=(25, 118, 210, 255), font=font_large)
    
    # English text
    text_en = "PINYIN"
    bbox_en = draw.textbbox((0, 0), text_en, font=font_small)
    text_width_en = bbox_en[2] - bbox_en[0]
    text_height_en = bbox_en[3] - bbox_en[1]
    
    x_en = (size - text_width_en) // 2
    y_en = size * 2 // 3 - text_height_en // 2
    draw.text((x_en, y_en), text_en, fill=(255, 138, 101, 255), font=font_small)
    
    return img

def create_chinese_style_icon(size=512):
    """Chinese style: White background with red '拼音' text"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)
    
    # Add red text "拼音" with 55% font size
    font_size = int(size * 0.55)  # フォントサイズを計算（画像サイズの約55%）
    font = get_chinese_font(font_size)
    
    text = "拼音"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Red color for text
    red_color = (220, 20, 60, 255)  # Crimson red
    draw.text((x, y), text, fill=red_color, font=font)
    
    return img

def save_icon(img, filename, size=512):
    """Save icon with proper format"""
    # Ensure the icons directory exists
    os.makedirs("icons", exist_ok=True)
    
    # Save full size
    img.save(f"icons/{filename}_{size}x{size}.png", "PNG")
    
    # Save different sizes for Android
    sizes = [48, 72, 96, 144, 192]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"icons/{filename}_{s}x{s}.png", "PNG")

def main():
    """Generate all icon designs"""
    print("🎨 Generating PinYin app icons...")
    
    # Generate Chinese style design
    print("Creating Chinese style icon...")
    chinese_icon = create_chinese_style_icon()
    save_icon(chinese_icon, "chinese_style")
    
    print("✅ Chinese style icon generated successfully!")
    print("📁 Icon saved in the 'icons' directory")

if __name__ == "__main__":
    main() 