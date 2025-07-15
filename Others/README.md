# PinYin iOS App

A SwiftUI-based iOS app for converting Chinese characters to Pinyin, matching the functionality of the Android version.

## Features

- 🏮 **Chinese to Pinyin Conversion**: Convert Chinese characters to their Pinyin pronunciation
- 🌙 **Dark Mode Support**: Automatic dark/light mode adaptation
- 📱 **iOS Native Design**: Built with SwiftUI for modern iOS design patterns
- 🎨 **Beautiful UI**: Clean, typography-focused design matching the Android version

## Requirements

- **Xcode 15.0+** (for iOS 17.0+)
- **iOS 17.0+** deployment target
- **macOS** for development

## Getting Started

### 1. Open the Project

1. **Install Xcode** from the Mac App Store if you haven't already
2. **Open Xcode**
3. **Open the project**: 
   - File → Open...
   - Navigate to `PinYin-iOS/PinYin.xcodeproj`
   - Click "Open"

### 2. Run on iOS Simulator

1. **Select a Simulator**:
   - In Xcode, click the device selector (next to the play button)
   - Choose an iOS Simulator (e.g., "iPhone 15 Pro")

2. **Build and Run**:
   - Press `⌘ + R` or click the ▶️ play button
   - The app will build and launch in the iOS Simulator

### 3. Run on Physical Device

1. **Connect your iPhone** via USB
2. **Trust the computer** on your iPhone if prompted
3. **Select your device** in the device selector
4. **Sign the app**:
   - Click on the project in the navigator
   - Select the "PinYin" target
   - Go to "Signing & Capabilities"
   - Check "Automatically manage signing"
   - Select your Apple ID team

5. **Build and Run**: Press `⌘ + R`

## Project Structure

```
PinYin-iOS/
├── PinYin.xcodeproj/          # Xcode project file
└── PinYin/
    └── PinYin/
        ├── PinYinApp.swift    # Main app entry point
        ├── ContentView.swift  # Main UI view
        ├── Info.plist         # App configuration
        ├── Assets.xcassets/   # App icons and assets
        └── Preview Content/   # SwiftUI preview assets
```

## App Icon

The app uses **Design 4 (Typography)** from the icon set:
- Clean white background with colored borders
- "拼音" prominently displayed in blue
- "PINYIN" below in orange
- Professional typography-focused design

## Features

### Input Section
- Text field for entering Chinese characters
- Real-time conversion as you type
- Placeholder text in Chinese

### Result Section
- Scrollable area showing conversion results
- Each character shows with its Pinyin pronunciation
- Format: `汉字 (pinyin)`

### Clear Button
- Clears both input and result fields
- Blue button with white text

### Dark Mode
- Automatically adapts to system dark/light mode
- All UI elements properly styled for both themes

## Pinyin Conversion

Currently includes basic conversion for common characters:
- 你 (nǐ), 好 (hǎo), 我 (wǒ), 是 (shì), 的 (de)
- 在 (zài), 有 (yǒu), 和 (hé), 了 (le), 不 (bù)
- 人 (rén), 大 (dà), 小 (xiǎo), 中 (zhōng), 国 (guó)
- 学 (xué), 习 (xí), 汉 (hàn), 字 (zì), 语 (yǔ)

## Development Notes

- Built with **SwiftUI** for modern iOS development
- Uses **@State** for reactive UI updates
- Supports both **iPhone and iPad**
- **iOS 17.0+** minimum deployment target
- **Swift 5.0** language version

## Troubleshooting

### Build Errors
- Make sure Xcode is up to date
- Clean build folder: Product → Clean Build Folder
- Reset package caches: File → Packages → Reset Package Caches

### Simulator Issues
- Reset simulator: Device → Erase All Content and Settings
- Check simulator is running before building

### Signing Issues
- Ensure you have a valid Apple ID
- Check "Automatically manage signing" is enabled
- Select the correct team in signing settings

## Next Steps

To enhance the app, consider:
1. **Add more characters** to the pinyin dictionary
2. **Implement tone marks** display
3. **Add pronunciation audio**
4. **Support for phrases and sentences**
5. **History feature** for previous conversions
6. **Export/share functionality**

---

**Note**: This iOS version matches the functionality and design of the Android PinYin app, providing a consistent experience across platforms.

