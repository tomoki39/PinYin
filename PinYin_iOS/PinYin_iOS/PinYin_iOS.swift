//
//  PinYin_iOSApp.swift
//  PinYin_iOS
//
//  Created by TOMOKI SAKURAI on 2025/07/10.
//

import SwiftUI

@main
struct PinYin_iOSApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .preferredColorScheme(.none) // システム設定に従う
                .environment(\.locale, .current) // 現在のロケールを使用
        }
    }
}
