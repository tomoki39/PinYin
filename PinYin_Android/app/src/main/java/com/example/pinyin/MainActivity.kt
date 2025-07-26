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
            for (wordLength in 2 downTo 1) {
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
        // Special handling for common multi-character words
        return when (word) {
            "银行" -> "yín háng"
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