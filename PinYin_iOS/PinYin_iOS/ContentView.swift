import SwiftUI

struct ContentView: View {
    @State private var chineseText = ""
    @State private var pinyinText = ""
    @State private var pinyinMap: [String: [String]] = [:]
    @State private var detailText: String = ""
    @State private var showTones = true
    @State private var loading = true
    @State private var error: String? = nil
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        NavigationView {
            VStack(spacing: 24) {
                // Header
                VStack(spacing: 8) {
                    Text("app_title")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(Color("AppPrimaryColor"))
                    
                    Text("enter_characters_to_convert")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .padding(.top)
                
                // Input Section
                VStack(spacing: 16) {
                    TextField("enter_chinese_characters", text: $chineseText)
                        .textFieldStyle(CustomTextFieldStyle())
                        .onChange(of: chineseText) { _, newValue in
                            convertToPinyin(newValue)
                        }
                    
                    // Tone Format Selector
                    VStack(alignment: .leading, spacing: 8) {
                        Text("tonal_format")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Picker("Tone format", selection: $showTones) {
                            Text("tonal_signs").tag(true)
                            Text("tonal_numbers").tag(false)
                        }
                        .pickerStyle(SegmentedPickerStyle())
                        .onChange(of: showTones) { _, _ in
                            convertToPinyin(chineseText)
                        }
                    }
                }
                .padding(.horizontal)
                
                // Result Section
                if loading {
                    VStack(spacing: 12) {
                        ProgressView()
                            .scaleEffect(1.2)
                        Text("loading_pinyin_data")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 40)
                } else if let error = error {
                    ErrorView(message: error)
                } else if !pinyinText.isEmpty {
                    ResultCard(pinyinText: pinyinText, detailText: detailText)
                } else if !chineseText.isEmpty {
                    EmptyResultView()
                }
                
                Spacer()
            }
            .padding()
            .background(Color(.systemBackground))
            .navigationBarHidden(true)
        }
        .onAppear {
            loadPinyinData()
        }
    }
    
    private func loadPinyinData() {
        loading = true
        error = nil
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                if let url = Bundle.main.url(forResource: "pinyin_map", withExtension: "json") ?? Bundle.main.url(forResource: "pinyin_map", withExtension: "json", subdirectory: "Resources") {
                    let data = try Data(contentsOf: url)
                    if let dict = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                        var map: [String: [String]] = [:]
                        for (k, v) in dict {
                            if let arr = v as? [String] {
                                map[k] = arr
                            } else if let s = v as? String {
                                map[k] = [s]
                            }
                        }
                        DispatchQueue.main.async {
                            self.pinyinMap = map
                            self.loading = false
                            self.convertToPinyin(self.chineseText)
                        }
                    } else {
                        DispatchQueue.main.async {
                            self.error = "Invalid JSON format"
                            self.loading = false
                        }
                    }
                } else {
                    DispatchQueue.main.async {
                        self.error = "pinyin_map.json not found"
                        self.loading = false
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    self.error = error.localizedDescription
                    self.loading = false
                }
            }
        }
    }
    
    private func convertToPinyin(_ text: String) {
        guard !loading, error == nil else { return }
        let toneMap: [Character: (Character, Character)] = [
            "ā": ("a", "1"), "á": ("a", "2"), "ǎ": ("a", "3"), "à": ("a", "4"),
            "ē": ("e", "1"), "é": ("e", "2"), "ě": ("e", "3"), "è": ("e", "4"),
            "ī": ("i", "1"), "í": ("i", "2"), "ǐ": ("i", "3"), "ì": ("i", "4"),
            "ō": ("o", "1"), "ó": ("o", "2"), "ǒ": ("o", "3"), "ò": ("o", "4"),
            "ū": ("u", "1"), "ú": ("u", "2"), "ǔ": ("u", "3"), "ù": ("u", "4"),
            "ǖ": ("v", "1"), "ǘ": ("v", "2"), "ǚ": ("v", "3"), "ǜ": ("v", "4")
        ]
        
        // Helper function to add spaces to multi-character pinyin
        func addSpacesToMultiCharPinyin(_ pinyin: String, _ word: String) -> String {
            switch word {
                // 好 - hǎo（3声）と hào（4声）
                case "好奇心": return "hào qí xīn"
                case "好学": return "hào xué"
                case "爱好": return "ài hào"
                case "喜好": return "xǐ hào"
                case "友好": return "yǒu hǎo"
                case "良好": return "liáng hǎo"
                
                // 行 - xíng（2声）と háng（2声）
                case "银行": return "yín háng"
                case "行业": return "háng yè"
                case "银行家": return "yín háng jiā"
                case "行为": return "xíng wéi"
                case "行动": return "xíng dòng"
                case "行走": return "xíng zǒu"
                
                // 重 - zhòng（4声）と chóng（2声）
                case "重庆": return "chóng qìng"
                case "重复": return "chóng fù"
                case "重新": return "chóng xīn"
                case "重要": return "zhòng yào"
                case "重量": return "zhòng liàng"
                case "重视": return "zhòng shì"
                
                // 长 - cháng（2声）と zhǎng（3声）
                case "长度": return "cháng dù"
                case "长期": return "cháng qī"
                case "长久": return "cháng jiǔ"
                case "成长": return "chéng zhǎng"
                case "增长": return "zēng zhǎng"
                case "校长": return "xiào zhǎng"
                
                // 发 - fā（1声）と fà（4声）
                case "发展": return "fā zhǎn"
                case "发现": return "fā xiàn"
                case "发生": return "fā shēng"
                case "头发": return "tóu fa"
                case "理发": return "lǐ fà"
                
                // 得 - dé（2声）、de（軽声）、děi（3声）
                case "得到": return "dé dào"
                case "获得": return "huò dé"
                case "觉得": return "jué de"
                case "记得": return "jì de"
                case "非得": return "fēi děi"
                case "总得": return "zǒng děi"
                
                // 着 - zhe（軽声）、zháo（2声）、zhuó（2声）
                case "看着": return "kàn zhe"
                case "听着": return "tīng zhe"
                case "睡着": return "shuì zháo"
                case "着急": return "zháo jí"
                case "穿着": return "chuān zhuó"
                case "着手": return "zhuó shǒu"
                
                // 了 - le（軽声）と liǎo（3声）
                case "完了": return "wán le"
                case "走了": return "zǒu le"
                case "了解": return "liǎo jiě"
                case "了结": return "liǎo jié"
                
                // 不 - bù（4声）と bú（2声）
                case "不对": return "bú duì"
                case "不错": return "bú cuò"
                case "不要": return "bú yào"
                case "不是": return "bú shì"
                case "不能": return "bù néng"
                case "不会": return "bù huì"
                
                // 一 - yī（1声）、yí（2声）、yì（4声）
                case "一天": return "yì tiān"
                case "一年": return "yì nián"
                case "一个": return "yí gè"
                case "一些": return "yì xiē"
                case "第一": return "dì yī"
                case "唯一": return "wéi yī"
                
                // 大 - dà（4声）と dài（4声）
                case "大学": return "dà xué"
                case "大家": return "dà jiā"
                case "大夫": return "dài fu"
                
                // 小 - xiǎo（3声）と xiào（4声）
                case "小孩": return "xiǎo hái"
                case "小学": return "xiǎo xué"
                case "孝子": return "xiào zǐ"
                
                // 中 - zhōng（1声）と zhòng（4声）
                case "中国": return "zhōng guó"
                case "中间": return "zhōng jiān"
                case "中奖": return "zhòng jiǎng"
                case "中毒": return "zhòng dú"
                
                // 为 - wéi（2声）と wèi（4声）
                case "为了": return "wèi le"
                case "因为": return "yīn wèi"
                case "作为": return "zuò wéi"
                case "成为": return "chéng wéi"
                
                // 和 - hé（2声）、hè（4声）、huó（2声）、huò（4声）
                case "和平": return "hé píng"
                case "和谐": return "hé xié"
                case "附和": return "fù hè"
                case "和面": return "huó miàn"
                case "和药": return "huò yào"
                
                // 还 - hái（2声）と huán（2声）
                case "还是": return "hái shì"
                case "还有": return "hái yǒu"
                case "归还": return "guī huán"
                case "还钱": return "huán qián"
                
                // 都 - dōu（1声）と dū（1声）
                case "都是": return "dōu shì"
                case "都有": return "dōu yǒu"
                case "首都": return "shǒu dū"
                case "都市": return "dū shì"
                
                // 地 - dì（4声）と de（軽声）
                case "地方": return "dì fāng"
                case "地区": return "dì qū"
                case "慢慢地": return "màn màn de"
                case "好好地": return "hǎo hǎo de"
                
                // 的 - de（軽声）、dí（2声）、dì（4声）
                case "我的": return "wǒ de"
                case "你的": return "nǐ de"
                case "的确": return "dí què"
                case "目的": return "mù dì"
                case "标的": return "biāo dì"
                
                // 过 - guò（4声）と guo（軽声）
                case "过去": return "guò qù"
                case "经过": return "jīng guò"
                case "去过": return "qù guo"
                case "看过": return "kàn guo"
                
                // 来 - lái（2声）と lai（軽声）
                case "来到": return "lái dào"
                case "回来": return "huí lai"
                case "出来": return "chū lai"
                
                // 去 - qù（4声）と qu（軽声）
                case "去年": return "qù nián"
                case "回去": return "huí qu"
                case "出去": return "chū qu"
                
                // 上 - shàng（4声）と shang（軽声）
                case "上面": return "shàng miàn"
                case "早上": return "zǎo shang"
                case "晚上": return "wǎn shang"
                
                // 下 - xià（4声）と xia（軽声）
                case "下面": return "xià miàn"
                case "地下": return "dì xia"
                case "乡下": return "xiāng xia"
                
                // 里 - lǐ（3声）と li（軽声）
                case "里面": return "lǐ miàn"
                case "这里": return "zhè li"
                case "那里": return "nà li"
                
                // 外 - wài（4声）と wai（軽声）
                case "外面": return "wài miàn"
                case "国外": return "guó wai"
                case "海外": return "hǎi wai"
                
                // 前 - qián（2声）と qian（軽声）
                case "前面": return "qián miàn"
                case "以前": return "yǐ qian"
                case "从前": return "cóng qian"
                
                // 后 - hòu（4声）と hou（軽声）
                case "后面": return "hòu miàn"
                case "以后": return "yǐ hou"
                
                // 内 - nèi（4声）と nei（軽声）
                case "内部": return "nèi bù"
                case "国内": return "guó nei"
                case "市内": return "shì nei"
                
                // 间 - jiān（1声）と jian（軽声）
                case "时间": return "shí jiān"
                case "房间": return "fáng jian"
                
                // 都市名
                case "苏州": return "sū zhōu"
                case "无锡": return "wú xī"
                case "宁波": return "níng bō"
                case "温州": return "wēn zhōu"
                case "佛山": return "fó shān"
                case "东莞": return "dōng guǎn"
                case "中山": return "zhōng shān"
                case "珠海": return "zhū hǎi"
                case "惠州": return "huì zhōu"
                case "江门": return "jiāng mén"
                case "肇庆": return "zhào qìng"
                case "清远": return "qīng yuǎn"
                case "韶关": return "sháo guān"
                case "湛江": return "zhàn jiāng"
                case "茂名": return "mào míng"
                case "阳江": return "yáng jiāng"
                case "云浮": return "yún fú"
                case "潮州": return "cháo zhōu"
                case "揭阳": return "jiē yáng"
                case "汕尾": return "shàn wěi"
                case "河源": return "hé yuán"
                case "梅州": return "méi zhōu"
                case "汕头": return "shàn tóu"
                
                // 基本的挨拶・表現
                case "你好": return "nǐ hǎo"
                case "谢谢": return "xiè xie"
                case "再见": return "zài jiàn"
                case "对不起": return "duì bu qǐ"
                case "没关系": return "méi guān xi"
                case "不客气": return "bú kè qi"
                
                default:
                    // For other multi-character words, try to split by tone marks
                    let toneVowel = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
                    let pattern = "[bpmfdtnlgkhjqxrzcsywzhchsh]?[a-züÜ]+[\(toneVowel)](ng|n)?"
                    let regex = try! NSRegularExpression(pattern: pattern, options: .caseInsensitive)
                    let nsrange = NSRange(pinyin.startIndex..<pinyin.endIndex, in: pinyin)
                    let matches = regex.matches(in: pinyin, options: [], range: nsrange)
                    let syllables = matches.map { String(pinyin[Range($0.range, in: pinyin)!]) }
                    if syllables.count > 1 {
                        return syllables.joined(separator: " ")
                    } else {
                        return pinyin
                    }
            }
        }
        
        var result = ""
        var details = ""
        var i = 0
        let chars = Array(text)
        while i < chars.count {
            var matched = false
            // Try to match multi-character words (up to 4 characters)
            for wordLen in stride(from: 4, through: 1, by: -1) {
                if i + wordLen <= chars.count {
                    let word = String(chars[i..<(i+wordLen)])
                    if let pinyinList = pinyinMap[word], !pinyinList.isEmpty {
                        let pinyin = pinyinList[0]
                        if showTones {
                            let spacedPinyin = addSpacesToMultiCharPinyin(pinyin, word)
                            result += spacedPinyin + " "
                        } else {
                            result += convertPinyinToNumber(pinyin, toneMap: toneMap) + " "
                        }
                        if pinyinList.count > 1 {
                            let detailReadings = pinyinList.map { showTones ? addSpacesToMultiCharPinyin($0, word) : convertPinyinToNumber($0, toneMap: toneMap) }
                            details += "\(word): \(detailReadings.joined(separator: ", "))\n"
                        }
                        i += wordLen
                        matched = true
                        break
                    }
                }
            }
            if !matched {
                let char = String(chars[i])
                if let pinyinList = pinyinMap[char], !pinyinList.isEmpty {
                    let pinyin = pinyinList[0]
                    if showTones {
                        result += pinyin + " "
                    } else {
                        result += convertPinyinToNumber(pinyin, toneMap: toneMap) + " "
                    }
                    if pinyinList.count > 1 {
                        let detailReadings = pinyinList.map { showTones ? $0 : convertPinyinToNumber($0, toneMap: toneMap) }
                        details += "\(char): \(detailReadings.joined(separator: ", "))\n"
                    }
                } else {
                    result += char + " "
                }
                i += 1
            }
        }
        pinyinText = result.trimmingCharacters(in: .whitespaces)
        detailText = details.trimmingCharacters(in: .whitespacesAndNewlines)
    }
    
    private func convertPinyinToNumber(_ pinyin: String, toneMap: [Character: (Character, Character)]) -> String {
        let toneVowel = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜaeiouü"
        let needsSplit = pinyin.count > 4 && !pinyin.contains(" ") && !pinyin.contains("-")
        var syllables: [String]
        if needsSplit {
            let regex = try! NSRegularExpression(pattern: "[bpmfdtnlgkhjqxrzcsywzhchsh]?[a-züÜ]+[\(toneVowel)](ng|n)?", options: .caseInsensitive)
            let nsrange = NSRange(pinyin.startIndex..<pinyin.endIndex, in: pinyin)
            let matches = regex.matches(in: pinyin, options: [], range: nsrange)
            syllables = matches.map { String(pinyin[Range($0.range, in: pinyin)!]) }
            if syllables.isEmpty { syllables = [pinyin] }
        } else {
            syllables = [pinyin]
        }
        return syllables.map { syll in
            var converted = syll
            var toneNumber: Character? = nil
            for (toneChar, (plain, num)) in toneMap {
                if converted.contains(toneChar) {
                    converted = converted.replacingOccurrences(of: String(toneChar), with: String(plain))
                    toneNumber = num
                    break
                }
            }
            if let toneNumber = toneNumber {
                converted += String(toneNumber)
            }
            return converted
        }.joined(separator: " ")
    }
}

// Custom TextField Style
struct CustomTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Color("CardBackground"))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color("AppPrimaryColor").opacity(0.3), lineWidth: 1)
            )
            .shadow(color: Color.black.opacity(0.05), radius: 2, x: 0, y: 1)
    }
}

// Result Card View
struct ResultCard: View {
    let pinyinText: String
    let detailText: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("pinyin")
                    .font(.headline)
                    .foregroundColor(Color("AppPrimaryColor"))
                Spacer()
            }
            
            Text(pinyinText)
                .font(.body)
                .foregroundColor(.primary)
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color("CardBackground"))
                .cornerRadius(12)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color("AppPrimaryColor").opacity(0.2), lineWidth: 1)
                )
                .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
            
            if !detailText.isEmpty {
                Text("details")
                    .font(.headline)
                    .foregroundColor(Color("AppPrimaryColor"))
                    .padding(.top, 8)
                
                Text(detailText)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color("CardBackground"))
                    .cornerRadius(12)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color("AppPrimaryColor").opacity(0.2), lineWidth: 1)
                    )
                    .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
            }
        }
        .padding(.horizontal)
    }
}

// Error View
struct ErrorView: View {
    let message: String
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "exclamationmark.triangle")
                .font(.largeTitle)
                .foregroundColor(.red)
            
            Text("conversion_error")
                .font(.headline)
                .foregroundColor(.red)
            
            Text(message)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .background(Color.red.opacity(0.1))
        .cornerRadius(12)
        .padding(.horizontal)
    }
}

// Empty Result View
struct EmptyResultView: View {
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "text.magnifyingglass")
                .font(.largeTitle)
                .foregroundColor(.secondary)
            
            Text("no_characters_entered")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .background(Color.secondary.opacity(0.1))
        .cornerRadius(12)
        .padding(.horizontal)
    }
}

#Preview {
    ContentView()
} 
