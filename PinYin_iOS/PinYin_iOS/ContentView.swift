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
        var result = ""
        var details = ""
        var i = 0
        let chars = Array(text)
        while i < chars.count {
            var matched = false
            for wordLen in stride(from: 2, through: 1, by: -1) {
                if i + wordLen <= chars.count {
                    let word = String(chars[i..<(i+wordLen)])
                    if let pinyinList = pinyinMap[word], !pinyinList.isEmpty {
                        let pinyin = pinyinList[0]
                        if showTones {
                            result += pinyin + " "
                        } else {
                            result += convertPinyinToNumber(pinyin, toneMap: toneMap) + " "
                        }
                        if pinyinList.count > 1 {
                            let detailReadings = pinyinList.map { showTones ? $0 : convertPinyinToNumber($0, toneMap: toneMap) }
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
