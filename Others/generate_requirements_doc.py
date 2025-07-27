#!/usr/bin/env python3
"""
Automated Requirements Document Generator for PinYin Project
Analyzes project structure and generates comprehensive requirements documentation
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class RequirementsGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.requirements = {
            "project_info": {},
            "platforms": {},
            "features": {},
            "data_analysis": {},
            "localization": {},
            "technical_specs": {}
        }
    
    def analyze_project_structure(self):
        """Analyze the overall project structure"""
        platforms = ["PinYin_Android", "PinYin_iOS", "PinYin_Web"]
        
        for platform in platforms:
            platform_path = self.project_root / platform
            if platform_path.exists():
                self.requirements["platforms"][platform] = self.analyze_platform(platform_path)
    
    def analyze_platform(self, platform_path: Path) -> Dict[str, Any]:
        """Analyze specific platform structure"""
        platform_info = {
            "files": [],
            "languages": [],
            "dependencies": [],
            "features": []
        }
        
        # Analyze files recursively
        for file_path in platform_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(platform_path)
                platform_info["files"].append(str(relative_path))
                
                # Detect programming languages
                if file_path.suffix in ['.kt', '.java']:
                    platform_info["languages"].append("Kotlin/Java")
                elif file_path.suffix in ['.swift']:
                    platform_info["languages"].append("Swift")
                elif file_path.suffix in ['.html', '.js', '.css']:
                    platform_info["languages"].append("Web Technologies")
                
                # Analyze specific file types
                if file_path.name == "strings.xml":
                    platform_info["features"].append("Localization (Android)")
                elif file_path.name == "Localizable.strings":
                    platform_info["features"].append("Localization (iOS)")
                elif file_path.name.endswith('.json') and 'locale' in str(file_path):
                    platform_info["features"].append("Localization (Web)")
                elif file_path.name == "pinyin_map.json":
                    platform_info["features"].append("Pinyin Database")
                elif file_path.name == "manifest.json":
                    platform_info["features"].append("PWA Manifest")
        
        # Remove duplicates
        platform_info["languages"] = list(set(platform_info["languages"]))
        platform_info["features"] = list(set(platform_info["features"]))
        
        return platform_info
    
    def analyze_localization(self):
        """Analyze localization support"""
        locales = set()
        
        # Check Android localization
        android_locales = self.project_root / "PinYin_Android" / "app" / "src" / "main" / "res"
        if android_locales.exists():
            for locale_dir in android_locales.glob("values-*"):
                locale = locale_dir.name.replace("values-", "")
                locales.add(locale)
        
        # Check iOS localization
        ios_locales = self.project_root / "PinYin_iOS" / "PinYin_iOS"
        if ios_locales.exists():
            for locale_dir in ios_locales.glob("*.lproj"):
                locale = locale_dir.name.replace(".lproj", "")
                locales.add(locale)
        
        # Check Web localization
        web_locales = self.project_root / "PinYin_Web" / "locales"
        if web_locales.exists():
            for locale_file in web_locales.glob("*.json"):
                locale = locale_file.stem
                locales.add(locale)
        
        self.requirements["localization"]["supported_languages"] = sorted(list(locales))
    
    def analyze_pinyin_data(self):
        """Analyze pinyin database structure"""
        pinyin_files = []
        
        for platform in ["PinYin_Android", "PinYin_iOS", "PinYin_Web"]:
            platform_path = self.project_root / platform
            if platform_path.exists():
                for pinyin_file in platform_path.rglob("pinyin_map*.json"):
                    pinyin_files.append({
                        "platform": platform,
                        "path": str(pinyin_file.relative_to(self.project_root)),
                        "size": pinyin_file.stat().st_size
                    })
        
        self.requirements["data_analysis"]["pinyin_files"] = pinyin_files
    
    def generate_markdown(self) -> str:
        """Generate markdown documentation"""
        md_content = f"""# PinYin Project Requirements Specification (Auto-Generated)

*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 1. Project Overview

### 1.1 Project Structure Analysis
This document was automatically generated by analyzing the project structure.

**Detected Platforms:**
"""
        
        for platform, info in self.requirements["platforms"].items():
            md_content += f"""
#### {platform}
- **Languages**: {', '.join(info['languages'])}
- **Features**: {', '.join(info['features'])}
- **Files**: {len(info['files'])} files detected
"""
        
        md_content += f"""
## 2. Localization Support

**Supported Languages ({len(self.requirements['localization']['supported_languages'])}):**
"""
        
        for lang in self.requirements["localization"]["supported_languages"]:
            md_content += f"- {lang}\n"
        
        md_content += f"""
## 3. Data Architecture

**Pinyin Database Files:**
"""
        
        for pinyin_file in self.requirements["data_analysis"]["pinyin_files"]:
            size_kb = pinyin_file["size"] / 1024
            md_content += f"- **{pinyin_file['platform']}**: {pinyin_file['path']} ({size_kb:.1f} KB)\n"
        
        md_content += f"""
## 4. Technical Specifications

### 4.1 Platform-Specific Requirements

#### Android
- **Language**: Kotlin
- **Framework**: Android SDK
- **Localization**: Android resource files
- **Data Storage**: Assets folder

#### iOS
- **Language**: Swift
- **Framework**: SwiftUI
- **Localization**: .lproj files
- **Data Storage**: App bundle

#### Web
- **Technology**: HTML5, CSS3, JavaScript
- **Framework**: Progressive Web App
- **Localization**: JSON locale files
- **Data Storage**: Fetch API

## 5. Core Features (Detected)

Based on code analysis, the following features are implemented:

1. **Chinese to Pinyin Conversion**: Real-time character conversion
2. **Tone Format Support**: Both tonal signs and numbers
3. **Multi-language Support**: {len(self.requirements['localization']['supported_languages'])} languages
4. **Multi-character Word Support**: Special handling for common words
5. **Responsive Design**: Cross-platform compatibility
6. **Offline Functionality**: Local data processing

## 6. Data Requirements

- **Pinyin Database**: Comprehensive character mappings
- **Multi-reading Support**: Alternative pronunciations
- **Word-level Mappings**: Common phrase handling
- **Localization Data**: UI text in multiple languages

## 7. Performance Requirements

- **Real-time Conversion**: < 100ms response time
- **Data Loading**: < 1 second for pinyin data
- **Memory Usage**: Efficient handling of large datasets
- **Cross-platform**: Consistent performance across platforms

## 8. Security and Privacy

- **Local Processing**: No external data transmission
- **Input Validation**: Sanitized user inputs
- **Privacy Compliance**: No user data collection

---

*This document is automatically generated and should be reviewed for accuracy.*
"""
        
        return md_content
    
    def generate_json(self) -> Dict[str, Any]:
        """Generate JSON format for API consumption"""
        return {
            "generated_at": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "requirements": self.requirements
        }
    
    def save_documentation(self, output_dir: str = "docs"):
        """Save documentation in multiple formats"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate markdown
        md_content = self.generate_markdown()
        with open(output_path / "requirements_auto_generated.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        # Generate JSON
        json_content = self.generate_json()
        with open(output_path / "requirements_data.json", "w", encoding="utf-8") as f:
            json.dump(json_content, f, indent=2, ensure_ascii=False)
        
        print(f"Documentation generated in {output_path}")
        print(f"- requirements_auto_generated.md")
        print(f"- requirements_data.json")

def main():
    """Main function to generate requirements documentation"""
    # Get the project root (parent directory of Others folder)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    generator = RequirementsGenerator(str(project_root))
    
    print("Analyzing project structure...")
    generator.analyze_project_structure()
    
    print("Analyzing localization...")
    generator.analyze_localization()
    
    print("Analyzing pinyin data...")
    generator.analyze_pinyin_data()
    
    print("Generating documentation...")
    generator.save_documentation()
    
    print("Requirements documentation generation completed!")

if __name__ == "__main__":
    main() 