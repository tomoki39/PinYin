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
    private var pinyinMap: Map<String, String> = emptyMap()
    
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
            
            pinyinMap = mutableMapOf<String, String>().apply {
                val keys = jsonObject.keys()
                while (keys.hasNext()) {
                    val key = keys.next()
                    put(key, jsonObject.getString(key))
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
            return
        }
        binding.resultText.text = "Converting..."
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val pinyin = convertToPinyin(input, showTones)
                launch(Dispatchers.Main) {
                    binding.resultText.text = pinyin
                }
            } catch (e: Exception) {
                launch(Dispatchers.Main) {
                    binding.resultText.text = "Error: ${e.message}"
                }
            }
        }
    }

    private fun convertToPinyin(text: String, withTone: Boolean): String {
        val toneMap = mapOf(
            'ā' to Pair('a', '1'), 'á' to Pair('a', '2'), 'ǎ' to Pair('a', '3'), 'à' to Pair('a', '4'),
            'ē' to Pair('e', '1'), 'é' to Pair('e', '2'), 'ě' to Pair('e', '3'), 'è' to Pair('e', '4'),
            'ī' to Pair('i', '1'), 'í' to Pair('i', '2'), 'ǐ' to Pair('i', '3'), 'ì' to Pair('i', '4'),
            'ō' to Pair('o', '1'), 'ó' to Pair('o', '2'), 'ǒ' to Pair('o', '3'), 'ò' to Pair('o', '4'),
            'ū' to Pair('u', '1'), 'ú' to Pair('u', '2'), 'ǔ' to Pair('u', '3'), 'ù' to Pair('u', '4'),
            'ǖ' to Pair('v', '1'), 'ǘ' to Pair('v', '2'), 'ǚ' to Pair('v', '3'), 'ǜ' to Pair('v', '4')
        )

        val result = StringBuilder()
        for (char in text) {
            val pinyin = pinyinMap[char.toString()]
            if (pinyin != null) {
                if (withTone) {
                    result.append(pinyin)
                } else {
                    // Find the tone-marked vowel and replace it, then append the number at the end
                    var converted: String = pinyin
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
                    result.append(converted)
                }
            } else {
                result.append(char)
            }
            result.append(" ")
        }
        return result.toString().trim()
    }
}