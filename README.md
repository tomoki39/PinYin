# PinYin - Chinese to Pinyin Converter

## 📱 Project Overview

**PinYin** is a cross-platform application that converts Chinese characters to Pinyin (romanized Chinese pronunciation). The project consists of three implementations: Android (Kotlin), iOS (SwiftUI), and Web (Progressive Web App).

## 🎯 Core Features

### Primary Functionality
- **Chinese Character Input**: Accept Chinese character input through text fields
- **Real-time Conversion**: Convert Chinese characters to Pinyin as users type
- **Tone Format Options**: Support both tonal signs (ā, á, ǎ, à) and tonal numbers (a1, a2, a3, a4)
- **Multiple Readings Display**: Show alternative pronunciations for characters with multiple readings
- **Multi-character Word Support**: Handle common Chinese words and phrases with proper spacing

### Technical Features
- **Offline Functionality**: All processing happens locally, no internet required
- **Multi-language Support**: UI available in 22 languages
- **Responsive Design**: Works across different screen sizes and orientations
- **Cross-platform**: Consistent experience across Android, iOS, and Web

## 🏗️ Project Structure

```
PinYin/
├── PinYin_Android/     # Android application (Kotlin)
├── PinYin_iOS/         # iOS application (SwiftUI)
├── PinYin_Web/         # Web application (PWA)
├── Others/             # Build scripts, utilities, and assets
├── docs/               # Auto-generated documentation
└── .github/            # GitHub Actions workflows
```

## 📊 Platform Specifications

| Platform | Language | Framework | Data Storage | Localization |
|----------|----------|-----------|--------------|--------------|
| **Android** | Kotlin | Android SDK | Assets folder | Resource files |
| **iOS** | Swift | SwiftUI | App bundle | .lproj files |
| **Web** | HTML5/CSS3/JS | PWA | Fetch API | JSON files |

## 🌍 Supported Languages

**22 Languages**: Arabic, Chinese, Danish, Dutch, English, Finnish, French, German, Hindi, Italian, Japanese, Korean, Polish, Portuguese, Russian, Spanish, Swedish, Thai, Turkish, Vietnamese

## 📈 Performance Requirements

- **Real-time Conversion**: < 100ms response time
- **Data Loading**: < 1 second for pinyin data
- **Memory Usage**: Efficient handling of large datasets
- **Cross-platform**: Consistent performance across platforms

## 🔒 Security & Privacy

- **Local Processing**: No external data transmission
- **Input Validation**: Sanitized user inputs
- **Privacy Compliance**: No user data collection

## 🚀 Quick Start

### Android
```bash
cd PinYin_Android
./gradlew assembleDebug
```

### iOS
```bash
cd PinYin_iOS
open PinYin_iOS.xcodeproj
```

### Web
```bash
cd PinYin_Web
# Open index.html in a web browser
# Or serve with a local server
python -m http.server 8000
```

## 📚 Documentation

- **[Detailed Requirements Specification](PinYin_Requirements_Specification.md)**: Comprehensive technical specifications
- **[Auto-generated Documentation](docs/requirements_auto_generated.md)**: Real-time project analysis
- **[Build Instructions](Others/README.md)**: Development and deployment guides

## 🔄 Automation

The project includes automated documentation generation:
- **GitHub Actions**: Automatic updates on code changes
- **Local Scripts**: Manual generation with `Others/auto_update_requirements.sh`
- **Cron Jobs**: Scheduled updates with `Others/setup_cron_automation.sh`

## 📝 Development

### Prerequisites
- **Android**: Android Studio, Kotlin
- **iOS**: Xcode, Swift
- **Web**: Modern web browser, Python (for scripts)

### Key Files
- **Pinyin Database**: `pinyin_map.json` (1MB+ character mappings)
- **Localization**: Platform-specific language files
- **Build Scripts**: Located in `Others/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across all platforms
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

*For detailed technical specifications, see [PinYin_Requirements_Specification.md](PinYin_Requirements_Specification.md)* 