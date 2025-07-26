#!/usr/bin/env python3
import json
import os

def add_multitone_words():
    # Androidのpinyin_map.jsonのパス
    json_path = "app/src/main/assets/pinyin_map.json"
    
    # 多音字を持つ一般的な単語（社会人が知っているレベル）
    multitone_words = {
        # 好 - hǎo（3声）と hào（4声）
        "好奇心": ["hàoqíxīn"],  # 好はhào（4声）
        "好学": ["hàoxué"],      # 好はhào（4声）
        "爱好": ["àihào"],       # 好はhào（4声）
        "喜好": ["xǐhào"],       # 好はhào（4声）
        "友好": ["yǒuhǎo"],      # 好はhǎo（3声）
        "良好": ["liánghǎo"],    # 好はhǎo（3声）
        
        # 行 - xíng（2声）と háng（2声）
        "银行": ["yínháng"],     # 行はháng（2声）
        "行业": ["hángyè"],      # 行はháng（2声）
        "银行家": ["yínhángjiā"], # 行はháng（2声）
        "行为": ["xíngwéi"],     # 行はxíng（2声）
        "行动": ["xíngdòng"],    # 行はxíng（2声）
        "行走": ["xíngzǒu"],     # 行はxíng（2声）
        
        # 重 - zhòng（4声）と chóng（2声）
        "重庆": ["chóngqìng"],   # 重はchóng（2声）
        "重复": ["chóngfù"],     # 重はchóng（2声）
        "重新": ["chóngxīn"],    # 重はchóng（2声）
        "重要": ["zhòngyào"],    # 重はzhòng（4声）
        "重量": ["zhòngliàng"],  # 重はzhòng（4声）
        "重视": ["zhòngshì"],    # 重はzhòng（4声）
        
        # 长 - cháng（2声）と zhǎng（3声）
        "长度": ["chángdù"],     # 长はcháng（2声）
        "长期": ["chángqī"],     # 长はcháng（2声）
        "长久": ["chángjiǔ"],    # 长はcháng（2声）
        "成长": ["chéngzhǎng"],  # 长はzhǎng（3声）
        "增长": ["zēngzhǎng"],   # 长はzhǎng（3声）
        "校长": ["xiàozhǎng"],   # 长はzhǎng（3声）
        
        # 发 - fā（1声）と fà（4声）
        "发展": ["fāzhǎn"],      # 发はfā（1声）
        "发现": ["fāxiàn"],      # 发はfā（1声）
        "发生": ["fāshēng"],     # 发はfā（1声）
        "头发": ["tóufa"],       # 发はfa（軽声）
        "理发": ["lǐfà"],        # 发はfà（4声）
        
        # 得 - dé（2声）、de（軽声）、děi（3声）
        "得到": ["dédào"],       # 得はdé（2声）
        "获得": ["huòdé"],       # 得はdé（2声）
        "觉得": ["juéde"],       # 得はde（軽声）
        "记得": ["jìde"],        # 得はde（軽声）
        "非得": ["fēiděi"],      # 得はděi（3声）
        "总得": ["zǒngděi"],     # 得はděi（3声）
        
        # 着 - zhe（軽声）、zháo（2声）、zhuó（2声）
        "看着": ["kànzhe"],      # 着はzhe（軽声）
        "听着": ["tīngzhe"],     # 着はzhe（軽声）
        "睡着": ["shuìzháo"],    # 着はzháo（2声）
        "着急": ["zháojí"],      # 着はzháo（2声）
        "穿着": ["chuānzhuó"],   # 着はzhuó（2声）
        "着手": ["zhuóshǒu"],    # 着はzhuó（2声）
        
        # 了 - le（軽声）と liǎo（3声）
        "完了": ["wánle"],       # 了はle（軽声）
        "走了": ["zǒule"],       # 了はle（軽声）
        "了解": ["liǎojiě"],     # 了はliǎo（3声）
        "了结": ["liǎojié"],     # 了はliǎo（3声）
        
        # 不 - bù（4声）と bú（2声）
        "不对": ["búduì"],       # 不はbú（2声）
        "不错": ["búcuò"],       # 不はbú（2声）
        "不要": ["búyào"],       # 不はbú（2声）
        "不是": ["búshì"],       # 不はbú（2声）
        "不能": ["bùnéng"],      # 不はbù（4声）
        "不会": ["bùhuì"],       # 不はbù（4声）
        
        # 一 - yī（1声）、yí（2声）、yì（4声）
        "一天": ["yìtiān"],      # 一はyì（4声）
        "一年": ["yìnián"],      # 一はyì（4声）
        "一个": ["yígè"],        # 一はyí（2声）
        "一些": ["yìxiē"],       # 一はyì（4声）
        "第一": ["dìyī"],        # 一はyī（1声）
        "唯一": ["wéiyī"],       # 一はyī（1声）
        
        # 七 - qī（1声）と qí（2声）
        "七月": ["qīyuè"],       # 七はqī（1声）
        "七点": ["qīdiǎn"],      # 七はqī（1声）
        "十七": ["shíqī"],       # 七はqī（1声）
        "七上八下": ["qīshàngbāxià"], # 七はqī（1声）
        
        # 八 - bā（1声）と bá（2声）
        "八月": ["bāyuè"],       # 八はbā（1声）
        "八点": ["bādiǎn"],      # 八はbā（1声）
        "十八": ["shíbā"],       # 八はbā（1声）
        
        # 大 - dà（4声）と dài（4声）
        "大学": ["dàxué"],       # 大はdà（4声）
        "大家": ["dàjiā"],       # 大はdà（4声）
        "大夫": ["dàifu"],       # 大はdài（4声）
        
        # 小 - xiǎo（3声）と xiào（4声）
        "小孩": ["xiǎohái"],     # 小はxiǎo（3声）
        "小学": ["xiǎoxué"],     # 小はxiǎo（3声）
        "孝子": ["xiàozǐ"],      # 孝はxiào（4声）
        
        # 中 - zhōng（1声）と zhòng（4声）
        "中国": ["zhōngguó"],    # 中はzhōng（1声）
        "中间": ["zhōngjiān"],   # 中はzhōng（1声）
        "中奖": ["zhòngjiǎng"],  # 中はzhòng（4声）
        "中毒": ["zhòngdú"],     # 中はzhòng（4声）
        
        # 为 - wéi（2声）と wèi（4声）
        "为了": ["wèile"],       # 为はwèi（4声）
        "因为": ["yīnwèi"],      # 为はwèi（4声）
        "作为": ["zuòwéi"],      # 为はwéi（2声）
        "成为": ["chéngwéi"],    # 为はwéi（2声）
        
        # 和 - hé（2声）、hè（4声）、huó（2声）、huò（4声）
        "和平": ["hépíng"],      # 和はhé（2声）
        "和谐": ["héxié"],       # 和はhé（2声）
        "附和": ["fùhè"],        # 和はhè（4声）
        "和面": ["huómiàn"],     # 和はhuó（2声）
        "和药": ["huòyào"],      # 和はhuò（4声）
        
        # 还 - hái（2声）と huán（2声）
        "还是": ["háishì"],      # 还はhái（2声）
        "还有": ["háiyǒu"],      # 还はhái（2声）
        "归还": ["guīhuán"],     # 还はhuán（2声）
        "还钱": ["huánqián"],    # 还はhuán（2声）
        
        # 都 - dōu（1声）と dū（1声）
        "都是": ["dōushì"],      # 都はdōu（1声）
        "都有": ["dōuyǒu"],      # 都はdōu（1声）
        "首都": ["shǒudū"],      # 都はdū（1声）
        "都市": ["dūshì"],       # 都はdū（1声）
        
        # 地 - dì（4声）と de（軽声）
        "地方": ["dìfāng"],      # 地はdì（4声）
        "地区": ["dìqū"],        # 地はdì（4声）
        "慢慢地": ["mànmànde"],  # 地はde（軽声）
        "好好地": ["hǎohǎode"],  # 地はde（軽声）
        
        # 得 - dé（2声）、de（軽声）、děi（3声）
        "得到": ["dédào"],       # 得はdé（2声）
        "获得": ["huòdé"],       # 得はdé（2声）
        "觉得": ["juéde"],       # 得はde（軽声）
        "记得": ["jìde"],        # 得はde（軽声）
        "非得": ["fēiděi"],      # 得はděi（3声）
        
        # 的 - de（軽声）、dí（2声）、dì（4声）
        "我的": ["wǒde"],        # 的はde（軽声）
        "你的": ["nǐde"],        # 的はde（軽声）
        "的确": ["díquè"],       # 的はdí（2声）
        "目的": ["mùdì"],        # 的はdì（4声）
        "标的": ["biāodì"],      # 的はdì（4声）
        
        # 了 - le（軽声）と liǎo（3声）
        "完了": ["wánle"],       # 了はle（軽声）
        "走了": ["zǒule"],       # 了はle（軽声）
        "了解": ["liǎojiě"],     # 了はliǎo（3声）
        "了结": ["liǎojié"],     # 了はliǎo（3声）
        
        # 着 - zhe（軽声）、zháo（2声）、zhuó（2声）
        "看着": ["kànzhe"],      # 着はzhe（軽声）
        "听着": ["tīngzhe"],     # 着はzhe（軽声）
        "睡着": ["shuìzháo"],    # 着はzháo（2声）
        "着急": ["zháojí"],      # 着はzháo（2声）
        "穿着": ["chuānzhuó"],   # 着はzhuó（2声）
        
        # 过 - guò（4声）と guo（軽声）
        "过去": ["guòqù"],       # 过はguò（4声）
        "经过": ["jīngguò"],     # 过はguò（4声）
        "去过": ["qùguo"],       # 过はguo（軽声）
        "看过": ["kànguo"],      # 过はguo（軽声）
        
        # 来 - lái（2声）と lai（軽声）
        "来到": ["láidào"],      # 来はlái（2声）
        "回来": ["huílai"],      # 来はlai（軽声）
        "出来": ["chūlai"],      # 来はlai（軽声）
        
        # 去 - qù（4声）と qu（軽声）
        "去年": ["qùnián"],      # 去はqù（4声）
        "回去": ["huíqu"],       # 去はqu（軽声）
        "出去": ["chūqu"],       # 去はqu（軽声）
        
        # 上 - shàng（4声）と shang（軽声）
        "上面": ["shàngmiàn"],   # 上はshàng（4声）
        "早上": ["zǎoshang"],    # 上はshang（軽声）
        "晚上": ["wǎnshang"],    # 上はshang（軽声）
        
        # 下 - xià（4声）と xia（軽声）
        "下面": ["xiàmiàn"],     # 下はxià（4声）
        "地下": ["dìxia"],       # 下はxia（軽声）
        "乡下": ["xiāngxia"],    # 下はxia（軽声）
        
        # 里 - lǐ（3声）と li（軽声）
        "里面": ["lǐmiàn"],      # 里はlǐ（3声）
        "这里": ["zhèli"],       # 里はli（軽声）
        "那里": ["nàli"],        # 里はli（軽声）
        
        # 外 - wài（4声）と wai（軽声）
        "外面": ["wàimiàn"],     # 外はwài（4声）
        "国外": ["guówai"],      # 外はwai（軽声）
        "海外": ["hǎiwai"],      # 外はwai（軽声）
        
        # 前 - qián（2声）と qian（軽声）
        "前面": ["qiánmiàn"],    # 前はqián（2声）
        "以前": ["yǐqian"],      # 前はqian（軽声）
        "从前": ["cóngqian"],    # 前はqian（軽声）
        
        # 后 - hòu（4声）と hou（軽声）
        "后面": ["hòumiàn"],     # 后はhòu（4声）
        "以后": ["yǐhou"],       # 后はhou（軽声）
        "以后": ["yǐhou"],       # 后はhou（軽声）
        
        # 内 - nèi（4声）と nei（軽声）
        "内部": ["nèibù"],       # 内はnèi（4声）
        "国内": ["guónei"],      # 内はnei（軽声）
        "市内": ["shìnei"],      # 内はnei（軽声）
        
        # 间 - jiān（1声）と jian（軽声）
        "中间": ["zhōngjiān"],   # 间はjiān（1声）
        "房间": ["fángjian"],    # 间はjian（軽声）
        "时间": ["shíjiān"],     # 间はjiān（1声）
        
        # 谢谢 - 2番目の谢は軽声
        "谢谢": ["xièxie"],
        
        # 你好 - 你はnǐ（3声）、好はhǎo（3声）
        "你好": ["nǐhǎo"],
        
        # 再见 - 再はzài（4声）、见はjiàn（4声）
        "再见": ["zàijiàn"],
        
        # 对不起 - 对はduì（4声）、不はbu（軽声）、起はqǐ（3声）
        "对不起": ["duìbuqǐ"],
        
        # 没关系 - 没はméi（2声）、关はguān（1声）、系はxi（軽声）
        "没关系": ["méiguānxi"],
        
        # 不客气 - 不はbú（2声）、客はkè（4声）、气はqi（軽声）
        "不客气": ["búkèqi"]
    }
    
    try:
        # 既存のJSONファイルを読み込み
        with open(json_path, 'r', encoding='utf-8') as f:
            pinyin_map = json.load(f)
        
        print(f"既存のエントリ数: {len(pinyin_map)}")
        
        # 多音字を持つ単語を追加
        added_count = 0
        for word, readings in multitone_words.items():
            if word not in pinyin_map:
                pinyin_map[word] = readings
                added_count += 1
                print(f"追加: {word} -> {readings}")
            else:
                print(f"既に存在: {word}")
        
        # 更新されたJSONファイルを保存
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(pinyin_map, f, ensure_ascii=False, indent=2)
        
        print(f"\n完了！{added_count}個の多音字単語を追加しました。")
        print(f"更新後のエントリ数: {len(pinyin_map)}")
        
    except FileNotFoundError:
        print(f"エラー: {json_path} が見つかりません")
    except json.JSONDecodeError as e:
        print(f"エラー: JSONファイルの解析に失敗しました - {e}")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    add_multitone_words() 