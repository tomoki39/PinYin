package com.example.pinyin

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.pinyin.databinding.ActivityMainBinding
import okhttp3.OkHttpClient
import okhttp3.Request
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private var pinyinMap: Map<String, List<String>> = emptyMap()
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        loadPinyinData()
        setupUI()
        setupListeners()
    }
    
    private fun loadPinyinData() {
        try {
            val inputStream = assets.open("pinyin_map.json")
            val size = inputStream.available()
            val buffer = ByteArray(size)
            inputStream.read(buffer)
            inputStream.close()
            
            val jsonString = String(buffer, Charsets.UTF_8)
            val jsonObject = JSONObject(jsonString)
            
            pinyinMap = mutableMapOf<String, List<String>>().apply {
                val keys = jsonObject.keys()
                while (keys.hasNext()) {
                    val key = keys.next()
                    val value = jsonObject.get(key)
                    when (value) {
                        is String -> put(key, listOf(value))
                        is org.json.JSONArray -> {
                            val list = mutableListOf<String>()
                            for (i in 0 until value.length()) {
                                list.add(value.getString(i))
                            }
                            put(key, list)
                        }
                        else -> put(key, listOf(value.toString()))
                    }
                }
            }
            
            println("Loaded ${pinyinMap.size} pinyin entries")
        } catch (e: IOException) {
            e.printStackTrace()
            Toast.makeText(this, "Failed to load pinyin data", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun setupUI() {
        // Set initial state for radio buttons
        binding.radioTonalSigns.isChecked = true
    }
    
    private fun setupListeners() {
        // Tone format radio group listener
        binding.toneRadioGroup.setOnCheckedChangeListener { _, _ ->
            // Auto-convert when switching formats
            if (!binding.chineseInput.text.isNullOrEmpty()) {
                convertChineseToPinyin()
            }
        }

        // Real-time conversion as user types
        binding.chineseInput.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                if (s?.isNotEmpty() == true) {
                    convertChineseToPinyin()
                } else {
                    binding.resultText.setText(R.string.enter_characters_to_convert)
                }
            }
        })
    }
    
    private fun convertChineseToPinyin() {
        val input = binding.chineseInput.text.toString()
        val showTones = binding.radioTonalSigns.isChecked
        if (input.isBlank()) {
            binding.resultText.text = ""
            binding.detailText.visibility = android.view.View.GONE
            return
        }
        binding.resultText.text = "Converting..."
        binding.detailText.visibility = android.view.View.GONE
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val (pinyin, details) = convertToPinyinWithDetails(input, showTones)
                launch(Dispatchers.Main) {
                    binding.resultText.text = pinyin
                    if (details.isNotEmpty()) {
                        binding.detailText.text = details
                        binding.detailText.visibility = android.view.View.VISIBLE
                    }
                }
            } catch (e: Exception) {
                launch(Dispatchers.Main) {
                    binding.resultText.text = "Error: ${e.message}"
                }
            }
        }
    }

    private fun convertToPinyinWithDetails(text: String, withTone: Boolean): Pair<String, String> {
        val toneMap = mapOf(
            'ā' to Pair('a', '1'), 'á' to Pair('a', '2'), 'ǎ' to Pair('a', '3'), 'à' to Pair('a', '4'),
            'ē' to Pair('e', '1'), 'é' to Pair('e', '2'), 'ě' to Pair('e', '3'), 'è' to Pair('e', '4'),
            'ī' to Pair('i', '1'), 'í' to Pair('i', '2'), 'ǐ' to Pair('i', '3'), 'ì' to Pair('i', '4'),
            'ō' to Pair('o', '1'), 'ó' to Pair('o', '2'), 'ǒ' to Pair('o', '3'), 'ò' to Pair('o', '4'),
            'ū' to Pair('u', '1'), 'ú' to Pair('u', '2'), 'ǔ' to Pair('u', '3'), 'ù' to Pair('u', '4'),
            'ǖ' to Pair('v', '1'), 'ǘ' to Pair('v', '2'), 'ǚ' to Pair('v', '3'), 'ǜ' to Pair('v', '4')
        )

        val result = StringBuilder()
        val details = StringBuilder()
        var i = 0
        while (i < text.length) {
            // Try to match multi-character words first (like "银行")
            var matched = false
            for (wordLength in 3 downTo 1) {
                if (i + wordLength <= text.length) {
                    val word = text.substring(i, i + wordLength)
                    val pinyinList = pinyinMap[word]
                    if (pinyinList != null && pinyinList.isNotEmpty()) {
                        val pinyin = pinyinList[0] // Use the first pronunciation for now
                                            if (withTone) {
                        // For multi-character words, add spaces between characters
                        if (wordLength > 1) {
                            val spacedPinyin = addSpacesToMultiCharPinyin(pinyin, word)
                            result.append(spacedPinyin)
                        } else {
                            result.append(pinyin)
                        }
                    } else {
                        // Convert tone marks to numbers (多音節対応)
                        val converted = convertPinyinToNumber(pinyin, toneMap)
                        result.append(converted)
                    }
                    result.append(" ")
                        
                        // Add details if there are multiple pronunciations
                        if (pinyinList.size > 1) {
                            val detailReadings = pinyinList.map { pinyin ->
                                if (withTone) {
                                    pinyin
                                } else {
                                    convertPinyinToNumber(pinyin, toneMap)
                                }
                            }
                            details.append("$word: ${detailReadings.joinToString(", ")}\n")
                        }
                        
                        i += wordLength
                        matched = true
                        break
                    }
                }
            }
            
            // If no multi-character match, try single character
            if (!matched) {
                val char = text[i].toString()
                val pinyinList = pinyinMap[char]
                if (pinyinList != null && pinyinList.isNotEmpty()) {
                    val pinyin = pinyinList[0] // Use the first pronunciation for now
                    if (withTone) {
                        result.append(pinyin)
                    } else {
                        // Convert tone marks to numbers (多音節対応)
                        val converted = convertPinyinToNumber(pinyin, toneMap)
                        result.append(converted)
                    }
                    
                    // Add details if there are multiple pronunciations
                    if (pinyinList.size > 1) {
                        val detailReadings = pinyinList.map { pinyin ->
                            if (withTone) {
                                pinyin
                            } else {
                                convertPinyinToNumber(pinyin, toneMap)
                            }
                        }
                        details.append("$char: ${detailReadings.joinToString(", ")}\n")
                    }
                } else {
                    result.append(char)
                }
                result.append(" ")
                i++
            }
        }
        return Pair(result.toString().trim(), details.toString().trim())
    }

    // Add spaces to multi-character pinyin for better readability
    private fun addSpacesToMultiCharPinyin(pinyin: String, word: String): String {
        // Special handling for common multi-character words with tone marks
        return when (word) {
            // 好 - hǎo（3声）と hào（4声）
            "好奇心" -> "hào qí xīn"
            "好学" -> "hào xué"
            "爱好" -> "ài hào"
            "喜好" -> "xǐ hào"
            "友好" -> "yǒu hǎo"
            "良好" -> "liáng hǎo"
            
            // 行 - xíng（2声）と háng（2声）
            "银行" -> "yín háng"
            "行业" -> "háng yè"
            "银行家" -> "yín háng jiā"
            "行为" -> "xíng wéi"
            "行动" -> "xíng dòng"
            "行走" -> "xíng zǒu"
            
            // 重 - zhòng（4声）と chóng（2声）
            "重庆" -> "chóng qìng"
            "重复" -> "chóng fù"
            "重新" -> "chóng xīn"
            "重要" -> "zhòng yào"
            "重量" -> "zhòng liàng"
            "重视" -> "zhòng shì"
            
            // 长 - cháng（2声）と zhǎng（3声）
            "长度" -> "cháng dù"
            "长期" -> "cháng qī"
            "长久" -> "cháng jiǔ"
            "成长" -> "chéng zhǎng"
            "增长" -> "zēng zhǎng"
            "校长" -> "xiào zhǎng"
            
            // 发 - fā（1声）と fà（4声）
            "发展" -> "fā zhǎn"
            "发现" -> "fā xiàn"
            "发生" -> "fā shēng"
            "头发" -> "tóu fa"
            "理发" -> "lǐ fà"
            
            // 得 - dé（2声）、de（軽声）、děi（3声）
            "得到" -> "dé dào"
            "获得" -> "huò dé"
            "觉得" -> "jué de"
            "记得" -> "jì de"
            "非得" -> "fēi děi"
            "总得" -> "zǒng děi"
            
            // 着 - zhe（軽声）、zháo（2声）、zhuó（2声）
            "看着" -> "kàn zhe"
            "听着" -> "tīng zhe"
            "睡着" -> "shuì zháo"
            "着急" -> "zháo jí"
            "穿着" -> "chuān zhuó"
            "着手" -> "zhuó shǒu"
            
            // 了 - le（軽声）と liǎo（3声）
            "完了" -> "wán le"
            "走了" -> "zǒu le"
            "了解" -> "liǎo jiě"
            "了结" -> "liǎo jié"
            
            // 不 - bù（4声）と bú（2声）
            "不对" -> "bú duì"
            "不错" -> "bú cuò"
            "不要" -> "bú yào"
            "不是" -> "bú shì"
            "不能" -> "bù néng"
            "不会" -> "bù huì"
            
            // 一 - yī（1声）、yí（2声）、yì（4声）
            "一天" -> "yì tiān"
            "一年" -> "yì nián"
            "一个" -> "yí gè"
            "一些" -> "yì xiē"
            "第一" -> "dì yī"
            "唯一" -> "wéi yī"
            
            // 大 - dà（4声）と dài（4声）
            "大学" -> "dà xué"
            "大家" -> "dà jiā"
            "大夫" -> "dài fu"
            
            // 小 - xiǎo（3声）と xiào（4声）
            "小孩" -> "xiǎo hái"
            "小学" -> "xiǎo xué"
            "孝子" -> "xiào zǐ"
            
            // 中 - zhōng（1声）と zhòng（4声）
            "中国" -> "zhōng guó"
            "中间" -> "zhōng jiān"
            "中奖" -> "zhòng jiǎng"
            "中毒" -> "zhòng dú"
            
            // 为 - wéi（2声）と wèi（4声）
            "为了" -> "wèi le"
            "因为" -> "yīn wèi"
            "作为" -> "zuò wéi"
            "成为" -> "chéng wéi"
            
            // 和 - hé（2声）、hè（4声）、huó（2声）、huò（4声）
            "和平" -> "hé píng"
            "和谐" -> "hé xié"
            "附和" -> "fù hè"
            "和面" -> "huó miàn"
            "和药" -> "huò yào"
            
            // 还 - hái（2声）と huán（2声）
            "还是" -> "hái shì"
            "还有" -> "hái yǒu"
            "归还" -> "guī huán"
            "还钱" -> "huán qián"
            
            // 都 - dōu（1声）と dū（1声）
            "都是" -> "dōu shì"
            "都有" -> "dōu yǒu"
            "首都" -> "shǒu dū"
            "都市" -> "dū shì"
            
            // 地 - dì（4声）と de（軽声）
            "地方" -> "dì fāng"
            "地区" -> "dì qū"
            "慢慢地" -> "màn màn de"
            "好好地" -> "hǎo hǎo de"
            
            // 的 - de（軽声）、dí（2声）、dì（4声）
            "我的" -> "wǒ de"
            "你的" -> "nǐ de"
            "的确" -> "dí què"
            "目的" -> "mù dì"
            "标的" -> "biāo dì"
            
            // 过 - guò（4声）と guo（軽声）
            "过去" -> "guò qù"
            "经过" -> "jīng guò"
            "去过" -> "qù guo"
            "看过" -> "kàn guo"
            
            // 来 - lái（2声）と lai（軽声）
            "来到" -> "lái dào"
            "回来" -> "huí lai"
            "出来" -> "chū lai"
            
            // 去 - qù（4声）と qu（軽声）
            "去年" -> "qù nián"
            "回去" -> "huí qu"
            "出去" -> "chū qu"
            
            // 上 - shàng（4声）と shang（軽声）
            "上面" -> "shàng miàn"
            "早上" -> "zǎo shang"
            "晚上" -> "wǎn shang"
            
            // 下 - xià（4声）と xia（軽声）
            "下面" -> "xià miàn"
            "地下" -> "dì xia"
            "乡下" -> "xiāng xia"
            
            // 里 - lǐ（3声）と li（軽声）
            "里面" -> "lǐ miàn"
            "这里" -> "zhè li"
            "那里" -> "nà li"
            
            // 外 - wài（4声）と wai（軽声）
            "外面" -> "wài miàn"
            "国外" -> "guó wai"
            "海外" -> "hǎi wai"
            
            // 前 - qián（2声）と qian（軽声）
            "前面" -> "qián miàn"
            "以前" -> "yǐ qian"
            "从前" -> "cóng qian"
            
            // 后 - hòu（4声）と hou（軽声）
            "后面" -> "hòu miàn"
            "以后" -> "yǐ hou"
            
            // 内 - nèi（4声）と nei（軽声）
            "内部" -> "nèi bù"
            "国内" -> "guó nei"
            "市内" -> "shì nei"
            
            // 间 - jiān（1声）と jian（軽声）
            "时间" -> "shí jiān"
            "房间" -> "fáng jian"
            
            // 都市名
            "苏州" -> "sū zhōu"
            "无锡" -> "wú xī"
            "宁波" -> "níng bō"
            "温州" -> "wēn zhōu"
            "佛山" -> "fó shān"
            "东莞" -> "dōng guǎn"
            "中山" -> "zhōng shān"
            "珠海" -> "zhū hǎi"
            "惠州" -> "huì zhōu"
            "江门" -> "jiāng mén"
            "肇庆" -> "zhào qìng"
            "清远" -> "qīng yuǎn"
            "韶关" -> "sháo guān"
            "湛江" -> "zhàn jiāng"
            "茂名" -> "mào míng"
            "阳江" -> "yáng jiāng"
            "云浮" -> "yún fú"
            "潮州" -> "cháo zhōu"
            "揭阳" -> "jiē yáng"
            "汕尾" -> "shàn wěi"
            "河源" -> "hé yuán"
            "梅州" -> "méi zhōu"
            "汕头" -> "shàn tóu"
            
            // 基本的挨拶・表現
            "你好" -> "nǐ hǎo"
            "谢谢" -> "xiè xie"
            "再见" -> "zài jiàn"
            "对不起" -> "duì bu qǐ"
            "没关系" -> "méi guān xi"
            "不客气" -> "bú kè qi"
            
            else -> {
                // For other multi-character words, try to split by tone marks
                val toneVowel = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
                val syllableRegex = Regex("[bpmfdtnlgkhjqxrzcsywzhchsh]?[a-züÜ]+[${toneVowel}](ng|n)?", RegexOption.IGNORE_CASE)
                val syllables = syllableRegex.findAll(pinyin).map { it.value }.filter { it.isNotBlank() }.toList()
                if (syllables.size > 1) {
                    syllables.joinToString(" ")
                } else {
                    pinyin
                }
            }
        }
    }

    // --- 最終修正版: 多音節語のみ分割、単音節語はそのままtone number変換 ---
    private fun convertPinyinToNumber(pinyin: String, toneMap: Map<Char, Pair<Char, Char>>): String {
        val toneVowel = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜaeiouü"
        // 2音節以上（5文字以上、スペース・ハイフンなし）の場合のみ分割
        val needsSplit = pinyin.length > 4 && !pinyin.contains(" ") && !pinyin.contains("-")
        val syllables = if (needsSplit) {
            val syllableRegex = Regex("[bpmfdtnlgkhjqxrzcsywzhchsh]?[a-züÜ]+[${toneVowel}](ng|n)?", RegexOption.IGNORE_CASE)
            val found = syllableRegex.findAll(pinyin).map { it.value }.filter { it.isNotBlank() }.toList()
            if (found.isNotEmpty()) found else listOf(pinyin)
        } else {
            listOf(pinyin)
        }
        return syllables.joinToString(" ") { syllable ->
            var converted = syllable
            var toneNumber: Char? = null
            for ((toneChar, pair) in toneMap) {
                if (converted.contains(toneChar)) {
                    converted = converted.replace(toneChar.toString(), pair.first.toString())
                    toneNumber = pair.second
                    break
                }
            }
            if (toneNumber != null) {
                converted += toneNumber
            }
            converted
        }
    }
}