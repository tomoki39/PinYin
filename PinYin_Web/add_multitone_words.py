#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def add_multitone_words_to_web():
    """Add multi-tone words to Web version's pinyin_map.json"""
    
    # Path to the Web version's pinyin_map.json
    json_path = 'pinyin_map.json'
    
    # Check if file exists
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        return
    
    # Read the existing JSON file
    print(f"Reading {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        pinyin_data = json.load(f)
    
    # Multi-tone words to add (same as Android version)
    multitone_words = {
        "好奇心": ["hàoqíxīn"],
        "好学": ["hàoxué"],
        "爱好": ["àihào"],
        "喜好": ["xǐhào"],
        "友好": ["yǒuhǎo"],
        "良好": ["liánghǎo"],
        "银行": ["yínháng"],
        "行业": ["hángyè"],
        "银行家": ["yínhángjiā"],
        "行为": ["xíngwéi"],
        "行动": ["xíngdòng"],
        "行走": ["xíngzǒu"],
        "重庆": ["chóngqìng"],
        "重复": ["chóngfù"],
        "重新": ["chóngxīn"],
        "重要": ["zhòngyào"],
        "重量": ["zhòngliàng"],
        "重视": ["zhòngshì"],
        "长度": ["chángdù"],
        "长期": ["chángqī"],
        "长久": ["chángjiǔ"],
        "成长": ["chéngzhǎng"],
        "增长": ["zēngzhǎng"],
        "校长": ["xiàozhǎng"],
        "发展": ["fāzhǎn"],
        "发现": ["fāxiàn"],
        "发生": ["fāshēng"],
        "头发": ["tóufa"],
        "理发": ["lǐfà"],
        "得到": ["dédào"],
        "获得": ["huòdé"],
        "觉得": ["juéde"],
        "记得": ["jìde"],
        "非得": ["fēiděi"],
        "总得": ["zǒngděi"],
        "看着": ["kànzhe"],
        "听着": ["tīngzhe"],
        "睡着": ["shuìzháo"],
        "着急": ["zháojí"],
        "穿着": ["chuānzhuó"],
        "着手": ["zhuóshǒu"],
        "完了": ["wánle"],
        "走了": ["zǒule"],
        "了解": ["liǎojiě"],
        "了结": ["liǎojié"],
        "不对": ["búduì"],
        "不错": ["búcuò"],
        "不要": ["búyào"],
        "不是": ["búshì"],
        "不能": ["bùnéng"],
        "不会": ["bùhuì"],
        "一天": ["yìtiān"],
        "一年": ["yìnián"],
        "一个": ["yígè"],
        "一些": ["yìxiē"],
        "第一": ["dìyī"],
        "唯一": ["wéiyī"],
        "大学": ["dàxué"],
        "大家": ["dàjiā"],
        "大夫": ["dàifu"],
        "小孩": ["xiǎohái"],
        "小学": ["xiǎoxué"],
        "孝子": ["xiàozǐ"],
        "中国": ["zhōngguó"],
        "中间": ["zhōngjiān"],
        "中奖": ["zhòngjiǎng"],
        "中毒": ["zhòngdú"],
        "为了": ["wèile"],
        "因为": ["yīnwèi"],
        "作为": ["zuòwéi"],
        "成为": ["chéngwéi"],
        "和平": ["hépíng"],
        "和谐": ["héxié"],
        "附和": ["fùhè"],
        "和面": ["huómiàn"],
        "和药": ["huòyào"],
        "还是": ["háishì"],
        "还有": ["háiyǒu"],
        "归还": ["guīhuán"],
        "还钱": ["huánqián"],
        "都是": ["dōushì"],
        "都有": ["dōuyǒu"],
        "首都": ["shǒudū"],
        "都市": ["dūshì"],
        "地方": ["dìfāng"],
        "地区": ["dìqū"],
        "慢慢地": ["mànmànde"],
        "好好地": ["hǎohǎode"],
        "我的": ["wǒde"],
        "你的": ["nǐde"],
        "的确": ["díquè"],
        "目的": ["mùdì"],
        "标的": ["biāodì"],
        "过去": ["guòqù"],
        "经过": ["jīngguò"],
        "去过": ["qùguo"],
        "看过": ["kànguo"],
        "来到": ["láidào"],
        "回来": ["huílai"],
        "出来": ["chūlai"],
        "去年": ["qùnián"],
        "回去": ["huíqu"],
        "出去": ["chūqu"],
        "上面": ["shàngmiàn"],
        "早上": ["zǎoshang"],
        "晚上": ["wǎnshang"],
        "下面": ["xiàmiàn"],
        "地下": ["dìxia"],
        "乡下": ["xiāngxia"],
        "里面": ["lǐmiàn"],
        "这里": ["zhèli"],
        "那里": ["nàli"],
        "外面": ["wàimiàn"],
        "国外": ["guówai"],
        "海外": ["hǎiwai"],
        "前面": ["qiánmiàn"],
        "以前": ["yǐqian"],
        "从前": ["cóngqian"],
        "后面": ["hòumiàn"],
        "以后": ["yǐhou"],
        "内部": ["nèibù"],
        "国内": ["guónei"],
        "市内": ["shìnei"],
        "时间": ["shíjiān"],
        "房间": ["fángjian"]
    }
    
    # Add the multi-tone words to the existing data
    print("Adding multi-tone words...")
    for word, readings in multitone_words.items():
        if word not in pinyin_data:
            pinyin_data[word] = readings
            print(f"Added: {word} -> {readings}")
        else:
            print(f"Already exists: {word}")
    
    # Write back to the file
    print(f"Writing updated data to {json_path}...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(pinyin_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully added {len(multitone_words)} multi-tone words to {json_path}")

if __name__ == "__main__":
    add_multitone_words_to_web() 