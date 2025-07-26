#!/usr/bin/env python3
import json
import os

def add_special_readings_v2():
    # Androidのpinyin_map.jsonのパス
    json_path = "app/src/main/assets/pinyin_map.json"
    
    # 一般的によく使われる特殊な読み（多音字）を持つ単語
    special_readings = {
        # 好奇心 - 好はhào（4声）
        "好奇心": ["hàoqíxīn"],
        
        # 银行 - 行はháng（2声）
        "银行": ["yínháng"],
        
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
        "不客气": ["búkèqi"],
        
        # 手机 - 手はshǒu（3声）、机はjī（1声）
        "手机": ["shǒujī"],
        
        # 电脑 - 电はdiàn（4声）、脑はnǎo（3声）
        "电脑": ["diànnǎo"],
        
        # 网络 - 网はwǎng（3声）、络はluò（4声）
        "网络": ["wǎngluò"],
        
        # 朋友 - 朋はpéng（2声）、友はyǒu（3声）
        "朋友": ["péngyǒu"],
        
        # 老师 - 老はlǎo（3声）、师はshī（1声）
        "老师": ["lǎoshī"],
        
        # 学生 - 学はxué（2声）、生はshēng（1声）
        "学生": ["xuéshēng"],
        
        # 工作 - 工はgōng（1声）、作はzuò（4声）
        "工作": ["gōngzuò"],
        
        # 学习 - 学はxué（2声）、习はxí（2声）
        "学习": ["xuéxí"],
        
        # 时间 - 时はshí（2声）、间はjiān（1声）
        "时间": ["shíjiān"],
        
        # 地方 - 地はdì（4声）、方はfāng（1声）
        "地方": ["dìfāng"],
        
        # 东西 - 东はdōng（1声）、西はxī（1声）
        "东西": ["dōngxī"],
        
        # 中国 - 中はzhōng（1声）、国はguó（2声）
        "中国": ["zhōngguó"],
        
        # 日本 - 日はrì（4声）、本はběn（3声）
        "日本": ["rìběn"],
        
        # 美国 - 美はměi（3声）、国はguó（2声）
        "美国": ["měiguó"],
        
        # 英国 - 英はyīng（1声）、国はguó（2声）
        "英国": ["yīngguó"],
        
        # 法国 - 法はfǎ（3声）、国はguó（2声）
        "法国": ["fǎguó"],
        
        # 德国 - 德はdé（2声）、国はguó（2声）
        "德国": ["déguó"],
        
        # 北京 - 北はběi（3声）、京はjīng（1声）
        "北京": ["běijīng"],
        
        # 上海 - 上はshàng（4声）、海はhǎi（3声）
        "上海": ["shànghǎi"],
        
        # 广州 - 广はguǎng（3声）、州はzhōu（1声）
        "广州": ["guǎngzhōu"],
        
        # 深圳 - 深はshēn（1声）、圳はzhèn（4声）
        "深圳": ["shēnzhèn"],
        
        # 成都 - 成はchéng（2声）、都はdū（1声）
        "成都": ["chéngdū"],
        
        # 杭州 - 杭はháng（2声）、州はzhōu（1声）
        "杭州": ["hángzhōu"],
        
        # 南京 - 南はnán（2声）、京はjīng（1声）
        "南京": ["nánjīng"],
        
        # 西安 - 西はxī（1声）、安はān（1声）
        "西安": ["xīān"],
        
        # 武汉 - 武はwǔ（3声）、汉はhàn（4声）
        "武汉": ["wǔhàn"],
        
        # 重庆 - 重はchóng（2声）、庆はqìng（4声）
        "重庆": ["chóngqìng"],
        
        # 天津 - 天はtiān（1声）、津はjīn（1声）
        "天津": ["tiānjīn"],
        
        # 青岛 - 青はqīng（1声）、岛はdǎo（3声）
        "青岛": ["qīngdǎo"],
        
        # 大连 - 大はdà（4声）、连はlián（2声）
        "大连": ["dàlián"],
        
        # 厦门 - 厦はxià（4声）、门はmén（2声）
        "厦门": ["xiàmén"],
        
        # 苏州 - 苏はsū（1声）、州はzhōu（1声）
        "苏州": ["sūzhōu"],
        
        # 无锡 - 无はwú（2声）、锡はxī（1声）
        "无锡": ["wúxī"],
        
        # 宁波 - 宁はníng（2声）、波はbō（1声）
        "宁波": ["níngbō"],
        
        # 温州 - 温はwēn（1声）、州はzhōu（1声）
        "温州": ["wēnzhōu"],
        
        # 佛山 - 佛はfó（2声）、山はshān（1声）
        "佛山": ["fóshān"],
        
        # 东莞 - 东はdōng（1声）、莞はguǎn（3声）
        "东莞": ["dōngguǎn"],
        
        # 中山 - 中はzhōng（1声）、山はshān（1声）
        "中山": ["zhōngshān"],
        
        # 珠海 - 珠はzhū（1声）、海はhǎi（3声）
        "珠海": ["zhūhǎi"],
        
        # 惠州 - 惠はhuì（4声）、州はzhōu（1声）
        "惠州": ["huìzhōu"],
        
        # 江门 - 江はjiāng（1声）、门はmén（2声）
        "江门": ["jiāngmén"],
        
        # 肇庆 - 肇はzhào（4声）、庆はqìng（4声）
        "肇庆": ["zhàoqìng"],
        
        # 清远 - 清はqīng（1声）、远はyuǎn（3声）
        "清远": ["qīngyuǎn"],
        
        # 韶关 - 韶はsháo（2声）、关はguān（1声）
        "韶关": ["sháoguān"],
        
        # 湛江 - 湛はzhàn（4声）、江はjiāng（1声）
        "湛江": ["zhànjiāng"],
        
        # 茂名 - 茂はmào（4声）、名はmíng（2声）
        "茂名": ["màomíng"],
        
        # 阳江 - 阳はyáng（2声）、江はjiāng（1声）
        "阳江": ["yángjiāng"],
        
        # 云浮 - 云はyún（2声）、浮はfú（2声）
        "云浮": ["yúnfú"],
        
        # 潮州 - 潮はcháo（2声）、州はzhōu（1声）
        "潮州": ["cháozhōu"],
        
        # 揭阳 - 揭はjiē（1声）、阳はyáng（2声）
        "揭阳": ["jiēyáng"],
        
        # 汕尾 - 汕はshàn（4声）、尾はwěi（3声）
        "汕尾": ["shànwěi"],
        
        # 河源 - 河はhé（2声）、源はyuán（2声）
        "河源": ["héyuán"],
        
        # 梅州 - 梅はméi（2声）、州はzhōu（1声）
        "梅州": ["méizhōu"],
        
        # 汕头 - 汕はshàn（4声）、头はtóu（2声）
        "汕头": ["shàntóu"]
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
    add_special_readings_v2() 