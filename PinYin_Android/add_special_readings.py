#!/usr/bin/env python3
import json
import os

def add_special_readings():
    # Androidのpinyin_map.jsonのパス
    json_path = "app/src/main/assets/pinyin_map.json"
    
    # 追加する特殊な読み
    special_readings = {
        "谢谢": ["xièxie"],
        "你好": ["nǐhǎo"],
        "再见": ["zàijiàn"],
        "对不起": ["duìbuqǐ"],
        "没关系": ["méiguānxi"],
        "不客气": ["búkèqi"]
    }
    
    try:
        # 既存のJSONファイルを読み込み
        with open(json_path, 'r', encoding='utf-8') as f:
            pinyin_map = json.load(f)
        
        print(f"既存のエントリ数: {len(pinyin_map)}")
        
        # 特殊な読みを追加
        added_count = 0
        for word, readings in special_readings.items():
            if word not in pinyin_map:
                pinyin_map[word] = readings
                added_count += 1
                print(f"追加: {word} -> {readings}")
            else:
                print(f"既に存在: {word}")
        
        # 更新されたJSONファイルを保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(pinyin_map, f, ensure_ascii=False, indent=2)
        
        print(f"\n完了！{added_count}個の特殊な読みを追加しました。")
        print(f"更新後のエントリ数: {len(pinyin_map)}")
        
    except FileNotFoundError:
        print(f"エラー: {json_path} が見つかりません")
    except json.JSONDecodeError as e:
        print(f"エラー: JSONファイルの解析に失敗しました - {e}")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    add_special_readings() 