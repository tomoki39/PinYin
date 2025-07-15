#!/usr/bin/env python3
"""
Build release versions for all platforms
"""

import os
import subprocess
import shutil
import zipfile
from datetime import datetime

def run_command(command, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def build_android_release():
    """Build Android release APK"""
    print("\n=== Building Android Release ===")
    
    android_dir = "../PinYin_Android"
    
    # Clean previous builds
    if run_command("./gradlew clean", cwd=android_dir):
        # Build release APK
        if run_command("./gradlew assembleRelease", cwd=android_dir):
            # Copy APK to releases directory
            apk_source = os.path.join(android_dir, "app/build/outputs/apk/release/app-release.apk")
            releases_dir = "releases"
            os.makedirs(releases_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            apk_dest = os.path.join(releases_dir, f"PinYin_Android_v1.0.0_{timestamp}.apk")
            
            if os.path.exists(apk_source):
                shutil.copy2(apk_source, apk_dest)
                print(f"Android APK created: {apk_dest}")
                return True
            else:
                print("Error: APK file not found")
                return False
    return False

def build_ios_release():
    """Build iOS release (requires Xcode)"""
    print("\n=== Building iOS Release ===")
    print("Note: iOS release requires Xcode and Apple Developer account")
    print("To build iOS release:")
    print("1. Open PinYin_iOS.xcodeproj in Xcode")
    print("2. Select 'Any iOS Device' as target")
    print("3. Product -> Archive")
    print("4. Distribute App through App Store Connect")
    
    # Create iOS build instructions
    ios_dir = "../PinYin_iOS"
    releases_dir = "releases"
    os.makedirs(releases_dir, exist_ok=True)
    
    instructions_file = os.path.join(releases_dir, "iOS_BUILD_INSTRUCTIONS.md")
    with open(instructions_file, 'w') as f:
        f.write("""# iOS Release Build Instructions

## Prerequisites
- Xcode installed
- Apple Developer Account ($99/year)
- App Store Connect access

## Build Steps
1. Open `PinYin_iOS.xcodeproj` in Xcode
2. Select your team in Signing & Capabilities
3. Set Bundle Identifier (e.g., com.yourname.pinyin)
4. Select "Any iOS Device" as target
5. Product -> Archive
6. Distribute App through App Store Connect

## Required Assets
- App Icon (already configured)
- Screenshots (use generated screenshots)
- App Description (use app_description.xml)
- Privacy Policy (use privacy_policy.html)

## App Store Categories
- Primary: Education
- Secondary: Utilities

## Keywords
pinyin, chinese, converter, language, learning, 拼音, 中文
""")
    
    print(f"iOS build instructions created: {instructions_file}")
    return True

def build_web_release():
    """Build Web release"""
    print("\n=== Building Web Release ===")
    
    web_dir = "../PinYin_Web"
    releases_dir = "releases"
    os.makedirs(releases_dir, exist_ok=True)
    
    # Create web release package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    web_zip = os.path.join(releases_dir, f"PinYin_Web_v1.0.0_{timestamp}.zip")
    
    with zipfile.ZipFile(web_zip, 'w') as zipf:
        for root, dirs, files in os.walk(web_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, web_dir)
                zipf.write(file_path, arcname)
    
    print(f"Web release created: {web_zip}")
    
    # Create deployment instructions
    deploy_file = os.path.join(releases_dir, "WEB_DEPLOYMENT.md")
    with open(deploy_file, 'w') as f:
        f.write("""# Web Deployment Instructions

## Option 1: GitHub Pages
1. Create a new GitHub repository
2. Upload web files to repository
3. Enable GitHub Pages in repository settings
4. Set source to main branch

## Option 2: Netlify
1. Go to netlify.com
2. Drag and drop the web folder
3. Site will be deployed automatically

## Option 3: Vercel
1. Go to vercel.com
2. Import your GitHub repository
3. Deploy automatically

## Option 4: Traditional Web Hosting
1. Upload all files to your web server
2. Ensure index.html is in the root directory
3. Configure HTTPS for PWA functionality

## Files to Deploy
- index.html
- manifest.json
- sw.js
- pinyin_map.json
- privacy_policy.html
- icons/ (all icon files)

## PWA Features
- Offline functionality
- Install prompt
- App-like experience
""")
    
    print(f"Web deployment instructions created: {deploy_file}")
    return True

def create_release_summary():
    """Create a summary of all releases"""
    print("\n=== Creating Release Summary ===")
    
    releases_dir = "releases"
    summary_file = os.path.join(releases_dir, "RELEASE_SUMMARY.md")
    
    with open(summary_file, 'w') as f:
        f.write(f"""# PinYin App Release Summary

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Version: 1.0.0

### Features
- Convert Chinese characters to Pinyin
- Real-time conversion
- Support for 20+ languages
- Clean, intuitive interface
- Red-themed design
- Privacy-focused (no data collection)

### Platforms
- Android: APK file available
- iOS: Requires Xcode build
- Web: ZIP file available

### Files Generated
- Android APK
- iOS build instructions
- Web deployment package
- Screenshots for all platforms
- Privacy policies
- App descriptions in 20+ languages

### Next Steps
1. Test all platforms thoroughly
2. Upload to Google Play Store (Android)
3. Submit to Apple App Store (iOS)
4. Deploy web version
5. Monitor user feedback

### Contact
For support or questions, contact through app stores.
""")
    
    print(f"Release summary created: {summary_file}")

def main():
    """Main build process"""
    print("=== PinYin App Release Build ===")
    
    # Create releases directory
    releases_dir = "releases"
    os.makedirs(releases_dir, exist_ok=True)
    
    # Build all platforms
    android_success = build_android_release()
    ios_success = build_ios_release()
    web_success = build_web_release()
    
    # Create summary
    create_release_summary()
    
    print("\n=== Build Complete ===")
    print(f"Releases directory: {os.path.abspath(releases_dir)}")
    print(f"Android: {'✓' if android_success else '✗'}")
    print(f"iOS: {'✓' if ios_success else '✗'}")
    print(f"Web: {'✓' if web_success else '✗'}")
    
    if android_success and web_success:
        print("\n✅ Ready for release!")
        print("Next steps:")
        print("1. Test the APK on real devices")
        print("2. Upload to Google Play Console")
        print("3. Deploy web version")
        print("4. Build iOS version in Xcode")
    else:
        print("\n❌ Some builds failed. Check errors above.")

if __name__ == "__main__":
    main() 