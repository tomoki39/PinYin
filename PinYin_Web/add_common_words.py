#!/usr/bin/env python3
import json

# Common words to add
common_words = {
    "谢谢": ["xièxie"],
    "你好": ["nǐhǎo"],
    "再见": ["zàijiàn"],
    "对不起": ["duìbuqǐ"],
    "没关系": ["méiguānxi"],
    "不客气": ["búkèqi"],
    "请": ["qǐng"],
    "谢谢": ["xièxie"]
}

# Load existing pinyin map
with open('pinyin_map.json', 'r', encoding='utf-8') as f:
    pinyin_map = json.load(f)

# Add common words
for word, readings in common_words.items():
    if word not in pinyin_map:
        pinyin_map[word] = readings
        print(f"Added: {word} -> {readings}")

# Save back to file
with open('pinyin_map.json', 'w', encoding='utf-8') as f:
    json.dump(pinyin_map, f, ensure_ascii=False, indent=2)

print("Common words added successfully!") 