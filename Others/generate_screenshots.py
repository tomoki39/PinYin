#!/usr/bin/env python3
"""
Generate screenshots for app store listings
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

# App store screenshot dimensions
SCREENSHOT_SIZES = {
    'android': {
        'phone': (1080, 1920),  # 9:16 ratio
        'tablet': (1920, 1080),  # 16:9 ratio
    },
    'ios': {
        'phone': (1170, 2532),  # iPhone 13 Pro
        'tablet': (2048, 2732),  # iPad Pro
    }
}

# Supported languages
LANGUAGES = {
    'en': 'English',
    'ja': '日本語',
    'zh': '中文',
    'ko': '한국어',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'vi': 'Tiếng Việt',
    'th': 'ไทย',
    'tr': 'Türkçe',
    'nl': 'Nederlands',
    'sv': 'Svenska',
    'fi': 'Suomi',
    'pl': 'Polski'
}

def create_screenshot(text, output_path, size, language_name):
    """Create a screenshot with the given text and size"""
    # Create image
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on image size
    font_size = min(size) // 20
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='#DC143C', font=font)
    
    # Add language indicator
    lang_font_size = min(size) // 40
    try:
        lang_font = ImageFont.truetype("Arial.ttf", lang_font_size)
    except:
        lang_font = ImageFont.load_default()
    
    lang_bbox = draw.textbbox((0, 0), language_name, font=lang_font)
    lang_width = lang_bbox[2] - lang_bbox[0]
    lang_height = lang_bbox[3] - lang_bbox[1]
    
    lang_x = (size[0] - lang_width) // 2
    lang_y = y + text_height + 20
    
    draw.text((lang_x, lang_y), language_name, fill='#666666', font=lang_font)
    
    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"Created: {output_path}")

def generate_screenshots():
    """Generate screenshots for all platforms and languages"""
    
    # Sample Chinese text for conversion
    sample_text = "你好世界"
    pinyin_text = "nǐ hǎo shì jiè"
    
    # Create screenshots directory
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Generate for each platform
    for platform in ['android', 'ios']:
        platform_dir = os.path.join(screenshots_dir, platform)
        os.makedirs(platform_dir, exist_ok=True)
        
        for device in ['phone', 'tablet']:
            device_dir = os.path.join(platform_dir, device)
            os.makedirs(device_dir, exist_ok=True)
            
            size = SCREENSHOT_SIZES[platform][device]
            
            # Generate for each language
            for lang_code, lang_name in LANGUAGES.items():
                # Create screenshot with Chinese text
                filename = f"pinyin_{lang_code}_{device}.png"
                output_path = os.path.join(device_dir, filename)
                
                # Create text showing conversion
                display_text = f"{sample_text}\n↓\n{pinyin_text}"
                
                create_screenshot(display_text, output_path, size, lang_name)
    
    print(f"\nScreenshots generated in '{screenshots_dir}' directory")
    print("Structure:")
    print("screenshots/")
    print("├── android/")
    print("│   ├── phone/")
    print("│   └── tablet/")
    print("└── ios/")
    print("    ├── phone/")
    print("    └── tablet/")

if __name__ == "__main__":
    generate_screenshots() 