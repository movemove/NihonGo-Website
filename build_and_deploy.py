#!/usr/bin/env python3
"""Build NihonGo 4-language showcase, /privacy, and /support pages, bundle Cloudflare Worker, and deploy to https://nihongo.appengine.fun."""
from __future__ import annotations

import base64
import html as html_mod
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
IMG_DIR = PUBLIC_DIR / "images"
AUD_DIR = PUBLIC_DIR / "audio"

ACCOUNT_ID = "9fb3b494e6d4d659f2cf567efb94fc38"
ZONE_ID = "977b0b4fa0ab6e587b8758a04016c5e8"
SCRIPT_NAME = "nihongo-site"
HOSTNAME = "nihongo.appengine.fun"
ORIGIN = f"https://{HOSTNAME}"
APP_STORE_ID = "6836279889"
APP_STORE_URL = f"https://apps.apple.com/app/id{APP_STORE_ID}"

CONTENT = {
    "en": {
        "html_lang": "en",
        "title": "NihonGo — Travel Japanese, 100 Real-Life Video Dialogues, Voice Coach & Live Translation",
        "desc": "Master real-life travel Japanese with 15 lessons, 100 real-life Japan travel video dialogues, 104 Kana stroke practice, an on-device Voice Coach, and Live Two-Way Voice Translation.",
        "keywords": "NihonGo,travel Japanese,hiragana,katakana,voice roleplay,live voice translation,Japanese travel dialogues,learn Japanese,AE Interactive",
        "nav_privacy": "Privacy",
        "nav_support": "Support",
        "nav_download": "Get App",
        "hero_badge": "15 LESSONS · 100 TRAVEL VIDEO DIALOGUES · LIVE TRANSLATION · ZERO ADS",
        "hero_title": "Speak Real Japanese <span>Before Your Trip Lands</span>",
        "hero_sub": "From Kana fundamentals and 100 real-life Japan travel video dialogues to a 12-scene on-device Voice Coach roleplay and live two-way voice translation—crafted with zero accounts and zero tracking.",
        "status_pill": "Available Now on App Store · iPhone, iPad & iPhone Duo",
        "cta_store_sub": "Download Free on",
        "cta_store_main": "App Store",
        "cta_audio": "▶ Hear Native Phrases",
        "cta_screens": "Explore Screens ↓",
        "sec_audio_badge": "REAL IN-APP STUDIO AUDIO · NATURAL ROMAJI PARTICLES",
        "sec_audio_title": "Hear Everyday Japanese as It's Spoken",
        "sec_audio_sub": "Actual MP3 clips bundled inside NihonGo—featuring particle-aware Romaji (wa / o / e) and practical grammar tips.",
        "btn_play": "Play",
        "btn_playing": "Playing",
        "sec_screens_badge": "LIVE APP PREVIEWS · IPHONE & IPHONE DUO",
        "sec_screens_title": "Designed for One-Handed Travel Confidence",
        "sec_screens_sub": "Clean portrait typography sized for readability on busy Tokyo platforms, plus native iPhone Duo foldable and iPad support.",
        "screens_labels": [
            "15-Lesson Path",
            "12-Scene Voice Roleplay",
            "Live Voice Translation",
            "100 Video Dialogues",
            "104 Kana & Tracing",
            "iPhone Duo Inner Display",
        ],
        "sec_features_badge": "FIVE INTEGRATED MODULES",
        "sec_features_title": "Everything You Need in One Offline-Ready App",
        "features": [
            ("📚", "15 Guided Lessons & 18 Grammar Drills", "Progress cleanly from Hiragana and Katakana basics through voiced sounds, combinations, and essential dining, shopping, transit, hotel, and clinic expressions."),
            ("🎬", "100 Real-Life Japan Travel Video Dialogues", "Real-life Japan travel conversations across 5 categories with 200 native recordings, bilingual subtitles, and quick-review keyword highlights."),
            ("💬", "12-Scene Guided Voice Roleplay", "On-device interactive roleplay: the clerk opens first, helpful hint cards stay visible while you speak, and you clear 3 practical mission steps."),
            ("🗣️", "Live Two-Way Voice Translation", "Speak or type between English, Traditional Chinese, Simplified Chinese, or Spanish and Japanese—complete with fullscreen show-the-clerk cards."),
            ("✍️", "Stroke Tracing & 160 SRS Flashcards", "Interactive Kana stroke guides, listening recognition quizzes, 320 vocabulary audio files, and Standard / Large / Extra Large font scaling."),
            ("🔒", "Zero Sign-In · Local Privacy Only", "No accounts, no ads, and zero third-party SDKs. Study progress stays strictly inside iOS UserDefaults on your device."),
        ],
        "sec_pricing_badge": "NO SUBSCRIPTIONS · START FREE",
        "sec_pricing_title": "Free Essentials. One-Time $3.99 Upgrade.",
        "sec_pricing_sub": "Test real travel Japanese before paying a cent—then unlock everything forever with a single App Store buyout.",
        "free_tier_title": "Free Forever",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Full 104 Hiragana & Katakana chart + stroke tracing",
            "Complete 160 SRS flashcards & 4 interactive quiz modes",
            "Lessons 1–3 + 10 travel video dialogues (2 per category)",
            "Daily free Voice Coach (5/day) & Live Interpreter (8/day)",
        ],
        "pro_tier_badge": "ONE-TIME BUYOUT · NO SUBSCRIPTION",
        "pro_tier_title": "NihonGo Pro Lifetime",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "All 15 guided travel lessons (Lessons 4–15 unlocked)",
            "All 100 real-life travel videos & 200 studio audio clips",
            "Unlimited 12-scene Voice Coach roleplay practice",
            "Unlimited two-way Live Voice Interpreter (offline-ready)",
        ],
        "bottom_cta_title": "Ready for Your Next Trip to Japan?",
        "bottom_cta_sub": "Free to download on iPhone & iPad—no sign-up required.",
        "appstore_btn_label": "Download Free on the App Store",
        "privacy_title": "Privacy Policy — NihonGo",
        "privacy_updated": "Last Updated: November 18, 2026",
        "privacy_sections": [
            ("1. Zero Account & Zero Personal Data Collection", "NihonGo is developed by AE Interactive (AppEngine Interactive). We do not require account registration and never collect, store, sell, or transmit personal data to AE Interactive servers (App Store Connect Privacy Label: Data Not Collected / NSPrivacyTracking = false). Study progress, Kana mastery, flashcards schedules, streaks, and font sizes are saved locally on your device using Apple UserDefaults (Required Reason API CA92.1)."),
            ("2. Microphone, Speech Recognition & On-Device Processing", "Microphone and speech recognition permissions are requested strictly on demand when you press Record in Voice Coach or Live Interpreter. Translations and guided roleplay replies prioritize Apple's native on-device translation and system language frameworks so conversations are never routed through third-party servers."),
            ("3. No Ads, No Analytics, No Tracking", "NihonGo bundles zero advertising networks, zero third-party telemetry SDKs, and zero cross-app tracking."),
            ("4. Contact Us", "Questions? Reach AE Interactive anytime at help@appengine.fun."),
        ],
        "support_title": "Support & Compatibility — NihonGo",
        "support_sub": "Quick help for Interactive Voice Coach, Offline Translation Packs, and App Support.",
        "support_cards": [
            ("Interactive Voice Coach Compatibility", "Runs 100% on-device via Apple's native system language model. Requires iPhone 15 Pro / Pro Max, iPhone 16 series, iPhone 17 series or newer, or M-series / A17 Pro+ iPad running iOS / iPadOS 26.0+ with system features enabled in Settings."),
            ("Offline Courses, Videos & Interpreter", "All 15 units, 104 Kana stroke guides, 100 real-life Japan travel video dialogues (200 MP3s), 160 flashcards (320 MP3s), and 18 grammar drills work on any supported iPhone or iPad with zero account or hardware restrictions."),
            ("Live Two-Way Translation Offline Packs", "Uses Apple's native Translation framework. You can tap the prompt in iOS Settings -> Apps -> Translate (or when prompted inside Interpreter) to download Japanese offline translation packs before boarding your flight."),
            ("Direct Support Contact", "Email AE Interactive at help@appengine.fun — we typically reply within 24 hours."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive Studio",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "title": "NihonGo — 旅日會話、100 個日本旅遊實境對話、互動口說練習與雙向語音翻譯",
        "desc": "從五十音筆順打底、100 個日本旅遊實境對話影片，到 12 情境互動對話練習與繁中／日語雙向即時語音翻譯，免登入零追蹤。",
        "keywords": "NihonGo,日語學習,日本旅遊日語,五十音,日語對話練習,雙向語音翻譯,日本旅遊實境對話,即時日文口譯,AE Interactive",
        "nav_privacy": "隱私權政策",
        "nav_support": "支援與常見問題",
        "nav_download": "立即下載",
        "hero_badge": "15 堂系統課 · 100 個日本旅遊實境對話 · 雙向語音翻譯 · 零廣告追蹤",
        "hero_title": "落地日本前，<span>先開口說出地道旅日會話</span>",
        "hero_sub": "從五十音筆順與 100 個日本旅遊實境對話預習，銜接店員主動提問模擬，再到結帳櫃檯雙向即時語音翻譯——全程免註冊、零廣告、本機隱私優先。",
        "status_pill": "App Store 正式上架 · 免費下載體驗 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "立即前往下載",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 試聽原生發音",
        "cta_screens": "瀏覽實機畫面 ↓",
        "sec_audio_badge": "收錄真實 App 錄音室語音 · 助詞自然標註羅馬拼音",
        "sec_audio_title": "點一下，立即試聽道地旅遊日語",
        "sec_audio_sub": "直接試聽 NihonGo 內建 320 句單字實戰音檔之一——自動辨識助詞讀音（は → wa／を → o／へ → e）。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "實機畫面精選 · IPHONE 與 IPHONE DUO 雙螢幕",
        "sec_screens_title": "單手直式大字體，通勤站立一眼看懂",
        "sec_screens_sub": "專為日本旅行單手操作設計，支援三段字級調整與 iPhone Duo 摺疊內外雙螢幕及 iPad 13 吋。",
        "screens_labels": [
            "15 堂實戰學習路徑",
            "12 情境實戰互動對話",
            "日本現場 · 雙向語音翻譯",
            "100 個日本旅遊實境對話",
            "五十音筆順與雙速發音",
            "iPhone Duo 展開內螢幕",
        ],
        "sec_features_badge": "五大實戰模組",
        "sec_features_title": "從零基礎到旅日救急，一套就夠",
        "features": [
            ("📚", "15 堂實戰路線＋18 堂文法句型", "從平假名、片假名、濁音、拗音起步，涵蓋餐廳點餐、藥妝免稅、車站轉乘、飯店入住與看診求助。"),
            ("🎬", "100 個日本旅遊實境對話影片（200 句錄音）", "五大日本旅遊場景×四階段時間線編排，雙語字幕搭配文法關鍵提醒，臨場感輕鬆吸收。"),
            ("💬", "12 情境實戰互動對話", "採用裝置端互動對話引導：由店員先主動開口提問，錄音練習時參考提示保留畫面，陪你完成 3 關任務。"),
            ("🗣️", "雙向即時語音翻譯（底部最右一鍵直達）", "支援繁中／簡中／英文／西文 ↔ 日語語音及打字即時互譯，並附大字全螢幕給店員看字卡。"),
            ("✍️", "104 五十音筆順臨摹與 160 SRS 單字卡", "筆順引導手寫練習、聽音辨字測驗、320 句單字發音，並支援標準／大字／特大三段字體。"),
            ("🔒", "免登入註冊・100% 本機隱私", "無廣告聯播網、無第三方追蹤碼（NSPrivacyTracking = false），所有學習紀錄只保存在您的 iPhone 本機。"),
        ],
        "sec_pricing_badge": "無月費訂閱制 · 免費下載先體驗",
        "sec_pricing_title": "基礎免費暢學 · $3.99 一次永久買斷",
        "sec_pricing_sub": "免費打好五十音與核心會話基礎，需要完整 100 部情境短片與無限口譯時再單次解鎖即可。",
        "free_tier_title": "永久免費版",
        "free_tier_price": "免費 $0",
        "free_tier_items": [
            "完整 104 字五十音圖表、發音與手寫臨摹",
            "完整 160 單字 SRS 記憶卡與 4 大聽讀測驗",
            "前 3 堂入門課程 ＋ 五大情境各 2 支（共 10 支）實境短片",
            "每日免費口說互動練習（5 次/日）與即時雙向口譯（8 次/日）",
        ],
        "pro_tier_badge": "一次買斷 · 終身無訂閱扣款",
        "pro_tier_title": "NihonGo Pro 永久買斷",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "完整解鎖全部 15 堂旅遊實戰課程（第 4–15 課）",
            "解鎖全 100 部實境旅遊對話影片與 200 句原生錄音",
            "12 大日本旅遊情境店員口說練習不限次數",
            "即時雙向語音口譯無限次使用（支援離線翻譯包）",
        ],
        "bottom_cta_title": "下一趟日本旅行，帶這套就夠了",
        "bottom_cta_sub": "App Store 免費下載、免註冊登入，打開就能開始練日語。",
        "appstore_btn_label": "前往 App Store 免費下載",
        "privacy_title": "NihonGo 隱私權政策",
        "privacy_updated": "最後更新日期：2026 年 11 月 18 日",
        "privacy_sections": [
            ("1. 無帳號登入與不收集個人資料", "NihonGo 由 AE Interactive（AppEngine Interactive）開發。本 App 無需註冊帳號，不會收集、儲存、出售或傳輸任何個人識別資料至開發者伺服器（App Store Privacy 宣告「不收集任何資料」，NSPrivacyTracking = false）。所有進度、單字複習與字級設定皆透過標準系統 UserDefaults（Required Reason API CA92.1）僅存於您的裝置本機。"),
            ("2. 麥克風、語音辨識與本機對話處理", "僅在您主動點擊「互動對話老師」或「即時雙向口譯」麥克風按鈕時才會請求權限；語音辨識、Apple 本機翻譯套件與裝置端系統對話架構均以本機優先執行，不會將對話上傳至任何第三方伺服器。"),
            ("3. 零廣告與零第三方追蹤", "本 App 不包含任何廣告 SDK、商業分析 SDK 或跨 App 行為追蹤。"),
            ("4. 聯絡我們", "如有隱私權問題，歡迎寄信至 help@appengine.fun。"),
        ],
        "support_title": "支援服務與常見問題 — NihonGo",
        "support_sub": "互動對話相容機型、離線語音翻譯包設定與技術支援窗口。",
        "support_cards": [
            ("互動對話老師相容裝置", "使用 Apple 原生裝置端系統語言架構：支援 iPhone 15 Pro / Pro Max、iPhone 16 全系列、iPhone 17 全系列與更新機型，以及 M 系列晶片 / A17 Pro 以上 iPad，需更新至 iOS / iPadOS 26.0 以上並於系統設定開啟對應系統功能。"),
            ("全部離線課程與實境影片不受裝置限制", "所有 15 堂課程、104 五十音手寫、100 個日本旅遊實境對話影片（200 句音檔）、160 單字卡（320 句音檔）與 18 堂文法練習皆支援所有兼容 iPhone 與 iPad，免登入即開即用。"),
            ("出發前下載日語離線翻譯包", "「即時雙向語音翻譯」整合 Apple 原生 Translation 框架；建議出發前於系統「設定 → App → 翻譯」預載「繁體中文 ↔ 日語」離線包，沒網路也能照常溝通。"),
            ("聯絡客服團隊", "若有任何問題或建議，請寄信至 help@appengine.fun（AE Interactive 通常於 24 小時內回覆）。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有權利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "title": "NihonGo — 旅游日语、100 个日本旅游实景对话、互动口语练习与双向语音翻译",
        "desc": "从五十音笔顺打底、100 个日本旅游实景对话视频，到 12 情景互动口语对话与简中／日语双向实时语音翻译，无需登录零追踪。",
        "keywords": "NihonGo,日语学习,日本旅游日语,五十音,日语对话练习,双向语音翻译,日本旅游实景对话,双向实时口译,AE Interactive",
        "nav_privacy": "隐私政策",
        "nav_support": "支持与常见问题",
        "nav_download": "立即下载",
        "hero_badge": "15 节实战课 · 100 个日本旅游实景对话 · 双向语音翻译 · 零广告追踪",
        "hero_title": "落地日本前，<span>先开口说出地道旅游日语</span>",
        "hero_sub": "从五十音手写临摹与 100 个日本旅游实景对话预习，衔接店员主动提问模拟，再到柜台现场双向实时语音翻译——全程免注册、无广告、本地隐私优先。",
        "status_pill": "App Store 正式上线 · 免费下载体验 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "前往免费下载",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 试听原生发音",
        "cta_screens": "查看实机截图 ↓",
        "sec_audio_badge": "内置录音室真人发音 · 助词自然标注罗马音",
        "sec_audio_title": "点击试听真实日语旅游常用句",
        "sec_audio_sub": "直接试听 NihonGo 应用内打包的高频词卡音频——助词自动标注标准口语读音（は → wa／を → o／へ → e）。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "实机界面展示 · IPHONE 与 IPHONE DUO 折叠双屏",
        "sec_screens_title": "单手竖屏大字体，车站街头一眼看清",
        "sec_screens_sub": "为日本自由行单手操作打造，提供三档字号调节，全面适配 iPhone Duo 折叠内外双屏与 iPad 13 英寸。",
        "screens_labels": [
            "15 节实战路线",
            "12 情景实战互动对话",
            "日本现场 · 双向语音翻译",
            "100 个日本旅游实景对话",
            "五十音笔顺与双速发音",
            "iPhone Duo 展开内屏",
        ],
        "sec_features_badge": "五大核心模块",
        "sec_features_title": "从零基础到现场应急，一站全搞定",
        "features": [
            ("📚", "15 节系统路线 + 18 节语法特训", "从平假名、片假名、浊音、拗音起步，系统掌握餐厅点餐、药妆免税、电车换乘、酒店入住与就医求助。"),
            ("🎬", "100 个日本旅游实景对话视频（200 句音频）", "五大旅游场景按行程阶段编排，搭配双语字幕与关键词解析，真实旅行氛围下轻松学以致用。"),
            ("💬", "12 情景实战互动对话", "采用端侧互动对话引导：由店员主动用日语提问，跟读时全程保留提示卡片，陪你打通 3 关任务。"),
            ("🗣️", "双向实时语音翻译（底部栏最右一键直达）", "支持简中／繁中／英语／西语 ↔ 日语语音与文字即时互译，并附全屏大字卡片方便直接出示给店员看。"),
            ("✍️", "104 五十音笔顺描红与 160 SRS 词卡", "交互式手写笔顺指导、听音辨字测验、320 句高频例句音频与三档大字体选项。"),
            ("🔒", "免账号登录 · 100% 本地隐私", "零广告、零第三方追踪代码（NSPrivacyTracking = false），学习进度仅保存于您的设备本地。"),
        ],
        "sec_pricing_badge": "无月费订阅 · 免费体验后按需买断",
        "sec_pricing_title": "基础免费使用 · $3.99 一次永久买断",
        "sec_pricing_sub": "先完整免费练习五十音与核心课程，满意后再一次性买断解锁全套课程、影片与无限口译。",
        "free_tier_title": "永久免费版",
        "free_tier_price": "免费 $0",
        "free_tier_items": [
            "完整 104 字五十音图表、双速发音与手写描红",
            "完整 160 核心词卡 SRS 记忆与 4 大听力测验",
            "前 3 节入门课程 ＋ 五大情景各 2 支（共 10 支）实景视频",
            "每日免费互动口语（5 次/天）与双向实时口译（8 次/天）",
        ],
        "pro_tier_badge": "一次买断 · 无订阅自动扣费",
        "pro_tier_title": "NihonGo Pro 永久买断",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "解锁全部 15 节日本自由行实战课程（第 4–15 节）",
            "解锁全部 100 部实景对话视频与 200 句真人录音",
            "12 大旅游情景店员互动口语练习不限次数",
            "双向实时语音口译无限次使用（支持离线翻译包）",
        ],
        "bottom_cta_title": "下一趟日本之旅，打开就能用",
        "bottom_cta_sub": "App Store 免费下载、无需注册账号，出发前练好开口第一句。",
        "appstore_btn_label": "前往 App Store 免费下载",
        "privacy_title": "NihonGo 隐私政策",
        "privacy_updated": "最后更新日期：2026 年 11 月 18 日",
        "privacy_sections": [
            ("1. 无需账号且不收集个人数据", "NihonGo 由 AE Interactive（AppEngine Interactive）开发。本应用无需注册账号，不会向开发商服务器收集、存储、出售或传输任何个人身份信息（App Store Privacy 声明为“不收集数据”，NSPrivacyTracking = false）。学习记录、词卡复习与字号设置仅通过系统 UserDefaults（Required Reason API CA92.1）保存在设备本地。"),
            ("2. 麦克风、语音识别与端侧对话处理", "仅在您主动点击“互动口语教练”或“双向实时口译”中的麦克风按钮时才申请权限；语音识别、Apple 本地翻译与端侧系统对话框架均优先在设备端运行，对话不会发送至第三方服务器。"),
            ("3. 零广告与零第三方追踪", "本应用不含任何广告 SDK、第三方数据统计或跨应用追踪。"),
            ("4. 联系我们", "如有隐私相关咨询，请联系 help@appengine.fun。"),
        ],
        "support_title": "技术支持与常见问题 — NihonGo",
        "support_sub": "互动口语兼容机型说明、离线翻译包下载及联系客服。",
        "support_cards": [
            ("互动口语教练支持机型", "基于 Apple 原生端侧系统语言模型运行，支持 iPhone 15 Pro / Pro Max、iPhone 16 全系、iPhone 17 全系及更新机型，以及 M 系列或 A17 Pro 以上 iPad，需升级至 iOS / iPadOS 26.0 以上并在设置中开启相应系统功能。"),
            ("全部课程、实景视频与词卡无机型门槛", "15 节实战课程、104 五十音描红、100 个日本旅游实景对话视频（200 句音频）、160 核心词卡（320 句音频）与 18 节语法在全部兼容 iPhone / iPad 上均可免登录完整使用。"),
            ("出行前建议预载日语离线翻译包", "“双向实时语音翻译”使用 Apple 系统 Translation 框架；可在系统“设置 → App → 翻译”下载“简体中文 ↔ 日语”离线包，机场或地下站台没信号也能顺畅沟通。"),
            ("联系技术支持", "如需帮助请致信 help@appengine.fun，AE Interactive 团队通常于 24 小时内回复。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有权利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "es": {
        "html_lang": "es",
        "title": "NihonGo — Japonés de Viaje, 100 Vídeos Reales, Práctica de Voz y Traducción",
        "desc": "Aprende japonés útil para viajar a Japón con 15 unidades, 100 vídeos de diálogos reales en Japón, 104 Kana con trazos, Práctica de Voz guiada y Traducción Bidireccional en Vivo.",
        "keywords": "NihonGo,japones viaje,hiragana,katakana,practica voz japones,traduccion voz japones,dialogos viaje japon,AE Interactive",
        "nav_privacy": "Privacidad",
        "nav_support": "Soporte",
        "nav_download": "Descargar",
        "hero_badge": "15 LECCIONES · 100 DIÁLOGOS EN JAPÓN · TRADUCCIÓN EN VIVO · SIN ANUNCIOS",
        "hero_title": "Habla Japonés Real <span>Antes de Aterrizar en Tokio</span>",
        "hero_sub": "Desde trazos de Kana y 100 vídeos de diálogos reales en Japón hasta rol práctico en 12 escenarios y traducción bidireccional de voz al instante—sin cuentas ni rastreo.",
        "status_pill": "Disponible en App Store · Gratis para empezar · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "Descárgalo gratis en",
        "cta_store_main": "App Store",
        "cta_audio": "▶ Escuchar Frases Reales",
        "cta_screens": "Ver Capturas ↓",
        "sec_audio_badge": "AUDIO REAL DE LA APP · ROMAJI CON PARTÍCULAS CLARAS",
        "sec_audio_title": "Escucha Frases Reales de Viaje en Japón",
        "sec_audio_sub": "Archivos MP3 reales incluidos dentro de NihonGo con partículas marcadas naturalmente (wa / o / e) y notas de gramática.",
        "btn_play": "Reproducir",
        "btn_playing": "Sonando",
        "sec_screens_badge": "CAPTURAS REALES · IPHONE E IPHONE DUO PLEGABLE",
        "sec_screens_title": "Diseñada para Leer Cómodo a Una Mano",
        "sec_screens_sub": "Tipografía grande ajustable y diseño vertical limpio, optimizado para iPhone, iPad 13\" y las pantallas interior y exterior del iPhone Duo.",
        "screens_labels": [
            "Ruta en 15 Lecciones",
            "Práctica en 12 Escenarios",
            "Traducción de Voz en Vivo",
            "100 Vídeos en Japón",
            "Tabla Kana y Trazos",
            "Pantalla Interior iPhone Duo",
        ],
        "sec_features_badge": "CINCO MÓDULOS INTEGRADOS",
        "sec_features_title": "Todo lo Esencial en Una App Privada y Sin Registro",
        "features": [
            ("📚", "15 Lecciones Prácticas y 18 Ejercicios", "Avanza desde Hiragana y Katakana básicos hasta restaurantes, farmacias Tax-Free, trenes, hoteles y emergencias."),
            ("🎬", "100 Vídeos de Diálogos Reales en Japón", "Situaciones reales de viaje por Japón en 5 categorías con 200 grabaciones nativas, subtítulos bilingües y consejos rápidos."),
            ("💬", "Práctica de Voz Guiada (12 Escenarios)", "Diálogos interactivos en el dispositivo: el personal inicia la pregunta, las tarjetas de ayuda siguen visibles al hablar y superas 3 pasos."),
            ("🗣️", "Traducción Bidireccional de Voz en Vivo", "Habla o escribe entre Español, Inglés o Chino y Japonés al instante, con tarjeta gigante para mostrar al dependiente."),
            ("✍️", "Trazos Kana y 160 Tarjetas SRS", "Guía de orden de trazos para los 104 Kana, test auditivos, 320 grabaciones de vocabulario y letra Estándar, Grande o Extra grande."),
            ("🔒", "Sin Registro · Privacidad Total", "Sin cuentas, sin anuncios ni SDKs de rastreo. Todo tu progreso se queda únicamente en tu iPhone o iPad."),
        ],
        "sec_pricing_badge": "SIN SUSCRIPCIONES · EMPIEZA GRATIS",
        "sec_pricing_title": "Gratis para Empezar. $3.99 Pago Único.",
        "sec_pricing_sub": "Prueba la app gratis en tu viaje y desbloquea todo para siempre con una sola compra en App Store.",
        "free_tier_title": "Gratis para Siempre",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Tabla completa de 104 Kana y práctica de trazos",
            "160 tarjetas SRS de vocabulario y 4 modos de test",
            "Lecciones 1–3 y 10 vídeos reales (2 por categoría)",
            "Cuota diaria gratis de Tutor de Voz (5/día) e Intérprete (8/día)",
        ],
        "pro_tier_badge": "PAGO ÚNICO · SIN SUSCRIPCIÓN",
        "pro_tier_title": "NihonGo Pro De Por Vida",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "Las 15 lecciones guiadas de viaje (4–15 desbloqueadas)",
            "Los 100 vídeos de diálogo real y 200 audios nativos",
            "Turnos ilimitados de práctica oral en 12 escenarios",
            "Intérprete de voz bidireccional sin límites (uso offline)",
        ],
        "bottom_cta_title": "¿Listo para Tu Próximo Viaje a Japón?",
        "bottom_cta_sub": "Descarga gratis para iPhone e iPad, sin crear cuenta.",
        "appstore_btn_label": "Descargar gratis en App Store",
        "privacy_title": "Política de Privacidad — NihonGo",
        "privacy_updated": "Última actualización: 18 de noviembre de 2026",
        "privacy_sections": [
            ("1. Sin Cuenta y Sin Recopilación de Datos", "NihonGo es desarrollada por AE Interactive (AppEngine Interactive). No solicitamos registro ni recopilamos, vendemos o enviamos datos personales a servidores propios (Etiqueta App Store: No se recopilan datos / NSPrivacyTracking = false). El progreso y los ajustes se guardan únicamente en local mediante UserDefaults (Required Reason API CA92.1)."),
            ("2. Micrófono, Voz y Procesamiento Local", "El micrófono y el reconocimiento de voz solo se solicitan al pulsar los botones de grabación en el Entrenador de Voz o el Intérprete en Vivo. La traducción y las respuestas de diálogo se ejecutan localmente con APIs de Apple sin enviar conversaciones a servidores de terceros."),
            ("3. Sin Publicidad ni Rastreo", "NihonGo no incluye redes publicitarias, analítica externa ni rastreo entre apps."),
            ("4. Contacto", "Para cualquier consulta, escribe a help@appengine.fun."),
        ],
        "support_title": "Soporte y Compatibilidad — NihonGo",
        "support_sub": "Requisitos de práctica de voz local, paquetes de traducción sin conexión y contacto directo.",
        "support_cards": [
            ("Compatibilidad de la Práctica de Voz", "Funciona localmente con el modelo de lenguaje del sistema de Apple en iPhone 15 Pro / Pro Max, toda la gama iPhone 16 y 17 o posterior, y iPad con chip M1 / A17 Pro+ con iOS / iPadOS 26.0+."),
            ("Acceso Completo al Resto de Módulos", "Las 15 unidades, los 104 trazos Kana, 100 vídeos reales en Japón (200 MP3), 160 tarjetas (320 MP3) y 18 ejercicios funcionan en cualquier iPhone o iPad compatible sin cuenta."),
            ("Traducción Sin Conexión para el Viaje", "En Ajustes de iOS -> Apps -> Traducir puedes descargar el paquete de japonés antes de volar para usar la Traducción en Vivo sin cobertura."),
            ("Soporte Directo", "Escríbenos a help@appengine.fun y responderemos habitualmente en menos de 24 horas."),
        ],
        "footer_rights": "© 2026 AE Interactive. Todos los derechos reservados.",
        "studio_link_label": "Estudio AE Interactive",
    },
}

AUDIO_ITEMS = [
    {
        "file": "split.mp3",
        "jp": "お会計は別々でお願いします。",
        "romaji": "o kaikei <b>wa</b> betsubetsu de o negai shi masu",
        "meaning": {
            "en": "Separate checks, please.",
            "zh-Hant": "結帳麻煩分開算。",
            "zh-Hans": "结账麻烦分开算。",
            "es": "La cuenta por separado, por favor.",
        },
        "tag": {
            "en": "Izakaya · Particle ha -> wa",
            "zh-Hant": "居酒屋 · 助詞は→wa",
            "zh-Hans": "居酒屋 · 助词は→wa",
            "es": "Izakaya · Partícula wa",
        },
    },
    {
        "file": "platform.mp3",
        "jp": "新宿行きは三番線です。",
        "romaji": "Shinjuku yuki <b>wa</b> san bansen desu",
        "meaning": {
            "en": "The train for Shinjuku is on Track 3.",
            "zh-Hant": "往新宿的車在 3 號月台。",
            "zh-Hans": "去往新宿的电车在 3 号站台。",
            "es": "El tren a Shinjuku sale del andén 3.",
        },
        "tag": {
            "en": "Transit · Platform Number",
            "zh-Hant": "電車轉乘 · 月台號",
            "zh-Hans": "电车换乘 · 站台号",
            "es": "Transporte · Andén",
        },
    },
    {
        "file": "checkout.mp3",
        "jp": "チェックアウトは何時ですか。",
        "romaji": "chekkuauto <b>wa</b> nan ji desu ka",
        "meaning": {
            "en": "What time is check-out?",
            "zh-Hant": "請問退房時間是幾點？",
            "zh-Hans": "请问退房时间是几点？",
            "es": "¿A qué hora es el check-out?",
        },
        "tag": {
            "en": "Hotel Desk · Katakana Loanword",
            "zh-Hant": "飯店入住 · 外來語詞彙",
            "zh-Hans": "酒店前台 · 外来语词汇",
            "es": "Hotel · Vocabulario útil",
        },
    },
    {
        "file": "wait.mp3",
        "jp": "すみません、ちょっと待ってください。",
        "romaji": "sumimasen, chotto matte kudasai",
        "meaning": {
            "en": "Excuse me, please wait a moment.",
            "zh-Hant": "不好意思，請稍等一下。",
            "zh-Hans": "不好意思，请稍等一下。",
            "es": "Disculpe, espere un momento.",
        },
        "tag": {
            "en": "Polite Counter Essential",
            "zh-Hant": "禮貌應對必備句",
            "zh-Hans": "礼貌应对必备句",
            "es": "Frase clave en tienda",
        },
    },
]

CSS = """
:root {
  --bg: #070913;
  --card: rgba(20, 24, 42, 0.86);
  --card-solid: #14182a;
  --border: rgba(255, 255, 255, 0.11);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --indigo: #6366F1;
  --teal: #2DD4BF;
  --coral: #FB7185;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang TC", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 42% at 50% -5%, rgba(99, 102, 241, 0.24) 0%, transparent 70%),
    radial-gradient(circle at 86% 18%, rgba(45, 212, 191, 0.14) 0%, transparent 45%);
  background-repeat: no-repeat;
}
a { color: inherit; }
header { position: sticky; top: 12px; z-index: 100; padding: 0 16px; }
nav {
  max-width: 980px; margin: 0 auto; padding: 10px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  background: rgba(11, 14, 28, 0.84);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border); border-radius: 999px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.45);
}
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 800; font-size: 17px; letter-spacing: -0.3px; }
.brand img { width: 34px; height: 34px; border-radius: 9px; border: 1px solid rgba(45, 212, 191, 0.45); }
.nav-right { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav-links { display: flex; gap: 14px; font-size: 13px; font-weight: 600; color: var(--muted); }
.nav-links a { text-decoration: none; transition: color .18s; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.lang-picker {
  display: flex; align-items: center; gap: 4px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
  padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.lang-picker a { color: var(--muted); text-decoration: none; padding: 2px 5px; border-radius: 99px; }
.lang-picker a.active { color: var(--teal); background: rgba(45,212,191,0.14); }
main { max-width: 980px; margin: 0 auto; padding: 36px 18px 64px; }
.hero { text-align: center; padding: 20px 0 36px; }
.badge {
  display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: 0.7px;
  color: var(--teal); background: rgba(45,212,191,0.12);
  border: 1px solid rgba(45,212,191,0.34); padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
h1 { font-size: clamp(30px, 5.4vw, 54px); font-weight: 900; letter-spacing: -1.1px; line-height: 1.12; margin-bottom: 14px; text-wrap: balance; }
h1 span { background: linear-gradient(125deg, #818CF8 0%, #2DD4BF 62%, #FB7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { max-width: 680px; margin: 0 auto 22px; color: var(--muted); font-size: clamp(15px, 2vw, 18px); text-wrap: balance; }
.status-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 999px;
  background: rgba(99,102,241,0.14); border: 1px solid rgba(99,102,241,0.38);
  color: #C7D2FE; font-size: 13px; font-weight: 700; margin-bottom: 22px;
}
.hero-cta { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 999px;
  font-size: 14px; font-weight: 700; text-decoration: none; border: 1px solid transparent; cursor: pointer;
  transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; box-shadow: 0 10px 26px rgba(99,102,241,0.32); }
.btn-ghost { background: rgba(255,255,255,0.06); border-color: var(--border); color: #E2E8F0; }
.btn-appstore {
  background: #fff; color: #090D16; border: 1px solid rgba(255,255,255,0.85);
  padding: 9px 20px; gap: 10px; box-shadow: 0 12px 30px rgba(255,255,255,0.16), 0 8px 24px rgba(99,102,241,0.28);
}
.btn-appstore svg { width: 20px; height: 24px; fill: currentColor; flex-shrink: 0; }
.btn-appstore .as-copy { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.12; text-align: left; }
.btn-appstore .as-sub { font-size: 10px; font-weight: 700; opacity: 0.72; letter-spacing: 0.2px; }
.btn-appstore .as-main { font-size: 15px; font-weight: 850; letter-spacing: -0.2px; }
.nav-cta {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; text-decoration: none;
  font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 14px rgba(99,102,241,0.35);
  transition: transform .16s ease, filter .16s ease;
}
.nav-cta:hover { transform: translateY(-1px); filter: brightness(1.08); }
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
.price-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 24px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 18px;
}
.price-card.pro {
  border-color: rgba(45, 212, 191, 0.55);
  background: linear-gradient(160deg, rgba(99,102,241,0.16), rgba(20,24,42,0.94) 45%, rgba(20,184,166,0.14));
  box-shadow: 0 18px 40px rgba(0,0,0,0.42);
}
.price-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.price-tag { font-size: 11px; font-weight: 800; color: var(--teal); letter-spacing: 0.4px; margin-bottom: 4px; }
.price-title { font-size: 20px; font-weight: 850; color: #fff; }
.price-num { font-size: 26px; font-weight: 900; color: #fff; white-space: nowrap; }
.price-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.price-list li { display: flex; gap: 9px; font-size: 14px; color: #CBD5E1; line-height: 1.45; }
.price-list li span.chk { color: var(--teal); font-weight: 900; flex-shrink: 0; }
.price-card .btn-appstore { justify-content: center; }
.cta-banner {
  margin-top: 56px; padding: 34px 24px; border-radius: 26px; text-align: center;
  background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(20,184,166,0.18));
  border: 1px solid rgba(45,212,191,0.35);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.cta-banner img { width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25); box-shadow: 0 10px 28px rgba(0,0,0,0.4); }
.cta-banner h2 { margin-bottom: 0; }
.cta-banner p { color: #CBD5E1; max-width: 540px; font-size: 15px; }
section { margin-top: 56px; }
.sec-head { text-align: center; margin-bottom: 24px; }
.sec-head .badge { margin-bottom: 10px; }
h2 { font-size: clamp(22px, 3.6vw, 34px); font-weight: 850; letter-spacing: -0.6px; margin-bottom: 8px; }
.sec-sub { color: var(--muted); max-width: 620px; margin: 0 auto; font-size: 15px; }
.audio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.audio-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
  transition: border-color .2s, transform .2s;
}
.audio-card.playing { border-color: var(--teal); box-shadow: 0 0 0 1px rgba(45,212,191,0.3), 0 14px 32px rgba(0,0,0,0.4); }
.audio-tag { font-size: 11px; font-weight: 700; color: var(--teal); letter-spacing: 0.3px; }
.audio-jp { font-size: 18px; font-weight: 800; margin-top: 6px; color: #fff; }
.audio-romaji { font-size: 13px; color: #67E8F9; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-top: 4px; }
.audio-romaji b { background: rgba(251, 113, 133, 0.2); color: #FDA4AF; padding: 0 4px; border-radius: 4px; }
.audio-meaning { font-size: 13px; color: var(--muted); margin-top: 4px; }
.play-btn {
  align-self: flex-start; background: rgba(99,102,241,0.2); color: #C7D2FE; border: 1px solid rgba(99,102,241,0.4);
  padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; cursor: pointer;
}
.audio-card.playing .play-btn { background: var(--teal); color: #042F2E; border-color: var(--teal); }
.gallery-strip {
  display: flex; gap: 16px; overflow-x: auto; padding: 8px 4px 16px; scroll-snap-type: x mandatory;
}
.shot-card {
  flex: 0 0 230px; scroll-snap-align: start; background: var(--card); border: 1px solid var(--border);
  border-radius: 20px; padding: 10px; text-align: center;
}
.shot-card.wide { flex: 0 0 330px; }
.shot-card img { width: 100%; height: auto; border-radius: 14px; display: block; }
.shot-cap { font-size: 12.5px; font-weight: 700; color: #CBD5E1; margin-top: 9px; }
.bento { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.bento-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
.bento-icon { font-size: 24px; margin-bottom: 10px; }
.bento-card h3 { font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #fff; }
.bento-card p { font-size: 14px; color: var(--muted); }
.doc-box { max-width: 780px; margin: 14px auto; background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 28px; }
.doc-box h1 { font-size: clamp(24px, 4vw, 36px); text-align: left; }
.doc-item { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--border); }
.doc-item h2 { font-size: 18px; margin-bottom: 6px; color: #E2E8F0; }
.doc-item p { font-size: 14.5px; color: var(--muted); }
footer {
  max-width: 980px; margin: 36px auto 0; padding: 24px 18px 42px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 13px;
}
footer a { color: #CBD5E1; text-decoration: none; }
footer a:hover { color: var(--teal); }
@media (max-width: 680px) {
  nav { border-radius: 22px; padding: 10px 14px; }
  .nav-right { gap: 8px; }
  .hero-cta .btn { width: 100%; justify-content: center; max-width: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn, .audio-card { transition: none; }
}
"""

SCRIPT_JS = """
const audioMap = {};
let activeKey = null;
function togglePhrase(key, src, btnEl, cardEl, playLabel, playingLabel) {
  if (activeKey && activeKey !== key && audioMap[activeKey]) {
    audioMap[activeKey].audio.pause();
    audioMap[activeKey].audio.currentTime = 0;
    audioMap[activeKey].btn.textContent = "▶ " + playLabel;
    audioMap[activeKey].card.classList.remove("playing");
  }
  let item = audioMap[key];
  if (!item) {
    const a = new Audio(src);
    item = { audio: a, btn: btnEl, card: cardEl };
    a.addEventListener("ended", () => {
      btnEl.textContent = "▶ " + playLabel;
      cardEl.classList.remove("playing");
      if (activeKey === key) activeKey = null;
    });
    audioMap[key] = item;
  }
  if (!item.audio.paused) {
    item.audio.pause();
    item.audio.currentTime = 0;
    btnEl.textContent = "▶ " + playLabel;
    cardEl.classList.remove("playing");
    activeKey = null;
  } else {
    item.audio.play();
    btnEl.textContent = "■ " + playingLabel;
    cardEl.classList.add("playing");
    activeKey = key;
  }
}
"""


def appstore_badge_svg() -> str:
    return '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def nav_html(lang: str, route: str, t: dict) -> str:
    langs = [("en", "EN"), ("zh-Hant", "繁中"), ("zh-Hans", "简中"), ("es", "ES")]
    lang_links = []
    for code, label in langs:
        cls = ' class="active"' if code == lang else ""
        href = f"{route}?lang={code}"
        lang_links.append(f'<a href="{href}"{cls}>{label}</a>')
    p_cls = ' class="active"' if route == "/privacy" else ""
    s_cls = ' class="active"' if route == "/support" else ""
    q = f"?lang={lang}"
    return f"""
<header>
  <nav aria-label="Main navigation">
    <a class="brand" href="/{q}">
      <img src="/images/icon.webp" alt="NihonGo Icon" width="34" height="34">
      <span>NihonGo</span>
    </a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/privacy{q}"{p_cls}>{html_mod.escape(t['nav_privacy'])}</a>
        <a href="/support{q}"{s_cls}>{html_mod.escape(t['nav_support'])}</a>
      </div>
      <div class="lang-picker" role="navigation" aria-label="Language">{''.join(lang_links)}</div>
      <a class="nav-cta" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['nav_download'])}</a>
    </div>
  </nav>
</header>"""


def footer_html(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    return f"""
<footer>
  <div>{html_mod.escape(t['footer_rights'])}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <a href="/{q}">NihonGo</a>
    <a href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">App Store</a>
    <a href="/privacy{q}">{html_mod.escape(t['nav_privacy'])}</a>
    <a href="/support{q}">{html_mod.escape(t['nav_support'])}</a>
    <a href="https://appengine.fun" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['studio_link_label'])}</a>
    <a href="mailto:help@appengine.fun">help@appengine.fun</a>
  </div>
</footer>"""


OG_LOCALES = {
    "en": "en_US",
    "zh-Hant": "zh_TW",
    "zh-Hans": "zh_CN",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "es": "es_ES",
}


def head_html(lang: str, t: dict, title: str, canonical_path: str, faq_items: list[tuple[str, str]] | None = None) -> str:
    q = f"?lang={lang}" if lang != "en" else ""
    canon_url = f"{ORIGIN}{canonical_path}{q}"
    site_langs = ('en', 'zh-Hant', 'zh-Hans', 'es')
    app_schema: dict = {
        "@type": "SoftwareApplication",
        "name": 'NihonGo Travel Japanese',
        "softwareVersion": '1.2.0',
        "operatingSystem": "iOS 17.0+, iPadOS 17.0+",
        "applicationCategory": "EducationApplication",
        "url": ORIGIN,
        "image": f"{ORIGIN}/images/og.png",
        "inLanguage": list(site_langs),
        "isAccessibleForFree": True,
        "offers": [
            {"@type": "Offer", "name": "Free Forever", "price": "0", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "NihonGo Pro Lifetime", "price": "3.99", "priceCurrency": "USD"},
        ],
        "publisher": {"@id": "https://appengine.fun/#organization"},
    }
    if APP_STORE_URL:
        app_schema["downloadUrl"] = APP_STORE_URL
        app_schema["installUrl"] = APP_STORE_URL
    graph: list[dict] = [
        {
            "@type": "Organization",
            "@id": "https://appengine.fun/#organization",
            "name": "AE Interactive",
            "url": "https://appengine.fun/",
            "sameAs": ["https://www.youtube.com/@appengine-a", "https://languages.appengine.fun/"],
        },
        {
            "@type": "WebSite",
            "@id": f"{ORIGIN}/#website",
            "name": 'NihonGo',
            "url": f"{ORIGIN}/",
            "inLanguage": list(site_langs),
            "publisher": {"@id": "https://appengine.fun/#organization"},
        },
        app_schema,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "AE Interactive", "item": "https://appengine.fun/"},
                {"@type": "ListItem", "position": 2, "name": "AE Languages", "item": "https://languages.appengine.fun/"},
                {"@type": "ListItem", "position": 3, "name": 'NihonGo', "item": f"{ORIGIN}/"},
            ] + (
                [{"@type": "ListItem", "position": 4, "name": title, "item": canon_url}]
                if canonical_path != "/"
                else []
            ),
        },
    ]
    if faq_items:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": h, "acceptedAnswer": {"@type": "Answer", "text": p}}
                for h, p in faq_items
            ],
        })
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    smart_banner = f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else ""
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{canonical_path}' + ("" if code == "en" else f"?lang={code}") + '">\n'
        for code in site_langs
    )
    og_loc = OG_LOCALES.get(lang, "en_US")
    og_loc_alts = "".join(
        f'<meta property="og:locale:alternate" content="{OG_LOCALES[c]}">\n'
        for c in site_langs if c != lang
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(t['desc'])}">
<meta name="keywords" content="{html_mod.escape(t['keywords'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="AE Interactive">
<meta name="theme-color" content="#070913">
{smart_banner}<link rel="canonical" href="{canon_url}">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{canonical_path}">
<link rel="icon" type="image/png" href="/images/icon.png">
<link rel="apple-touch-icon" href="/images/icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AE Interactive">
<meta property="og:locale" content="{og_loc}">
{og_loc_alts}<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(t['desc'])}">
<meta property="og:url" content="{canon_url}">
<meta property="og:image" content="{ORIGIN}/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html_mod.escape(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html_mod.escape(title)}">
<meta name="twitter:description" content="{html_mod.escape(t['desc'])}">
<meta name="twitter:image" content="{ORIGIN}/images/og.png">
<meta name="twitter:image:alt" content="{html_mod.escape(title)}">
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style>
</head>"""


def build_home(lang: str, t: dict) -> str:
    audio_cards = []
    for idx, item in enumerate(AUDIO_ITEMS):
        play_lbl = html_mod.escape(t["btn_play"])
        playing_lbl = html_mod.escape(t["btn_playing"])
        audio_cards.append(f"""
        <article class="audio-card" id="card-{idx}">
          <div>
            <div class="audio-tag">{html_mod.escape(item['tag'][lang])}</div>
            <div class="audio-jp">{html_mod.escape(item['jp'])}</div>
            <div class="audio-romaji">{item['romaji']}</div>
            <div class="audio-meaning">{html_mod.escape(item['meaning'][lang])}</div>
          </div>
          <button type="button" class="play-btn" onclick="togglePhrase('p{idx}','/audio/{item['file']}',this,document.getElementById('card-{idx}'),'{play_lbl}','{playing_lbl}')">▶ {play_lbl}</button>
        </article>""")

    shot_cards = []
    for i in range(1, 6):
        lbl = html_mod.escape(t["screens_labels"][i - 1])
        shot_cards.append(f"""
        <div class="shot-card">
          <img src="/images/{lang}_s0{i}.webp" alt="{lbl}" loading="lazy" width="640" height="1390">
          <div class="shot-cap">{lbl}</div>
        </div>""")
    duo_lbl = html_mod.escape(t["screens_labels"][5])
    shot_cards.append(f"""
        <div class="shot-card wide">
          <img src="/images/{lang}_duo.webp" alt="{duo_lbl}" loading="lazy" width="760" height="1080">
          <div class="shot-cap">{duo_lbl}</div>
        </div>""")

    bento_cards = []
    for icon, title, body in t["features"]:
        bento_cards.append(f"""
        <article class="bento-card">
          <div class="bento-icon" aria-hidden="true">{icon}</div>
          <h3>{html_mod.escape(title)}</h3>
          <p>{html_mod.escape(body)}</p>
        </article>""")

    free_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["free_tier_items"])
    pro_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["pro_tier_items"])
    appstore_btn = (
        f'<a class="btn btn-appstore" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">'
        f'{appstore_badge_svg()}'
        f'<span class="as-copy"><span class="as-sub">{html_mod.escape(t["cta_store_sub"])}</span>'
        f'<span class="as-main">{html_mod.escape(t["cta_store_main"])}</span></span></a>'
    )

    return f"""{head_html(lang, t, t['title'], '/')}
<body>
{nav_html(lang, '/', t)}
<main>
  <section class="hero">
    <div class="badge">{html_mod.escape(t['hero_badge'])}</div>
    <h1>{t['hero_title']}</h1>
    <p class="hero-sub">{html_mod.escape(t['hero_sub'])}</p>
    <div class="status-pill"> {html_mod.escape(t['status_pill'])}</div>
    <div class="hero-cta">
      {appstore_btn}
      <a class="btn btn-primary" href="#audio">{html_mod.escape(t['cta_audio'])}</a>
      <a class="btn btn-ghost" href="#preview">{html_mod.escape(t['cta_screens'])}</a>
    </div>
  </section>

  <section id="audio">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_audio_badge'])}</div>
      <h2>{html_mod.escape(t['sec_audio_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_audio_sub'])}</p>
    </div>
    <div class="audio-grid">{''.join(audio_cards)}</div>
  </section>

  <section id="preview">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_screens_badge'])}</div>
      <h2>{html_mod.escape(t['sec_screens_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_screens_sub'])}</p>
    </div>
    <div class="gallery-strip">{''.join(shot_cards)}</div>
  </section>

  <section id="features">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_features_badge'])}</div>
      <h2>{html_mod.escape(t['sec_features_title'])}</h2>
    </div>
    <div class="bento">{''.join(bento_cards)}</div>
  </section>

  <section id="pricing">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_pricing_badge'])}</div>
      <h2>{html_mod.escape(t['sec_pricing_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_pricing_sub'])}</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">NIHONGO FREE</div>
              <div class="price-title">{html_mod.escape(t['free_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['free_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{free_lis}</ul>
        </div>
        <a class="btn btn-ghost" style="justify-content:center;" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['appstore_btn_label'])}</a>
      </article>
      <article class="price-card pro">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">{html_mod.escape(t['pro_tier_badge'])}</div>
              <div class="price-title">{html_mod.escape(t['pro_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['pro_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{pro_lis}</ul>
        </div>
        {appstore_btn}
      </article>
    </div>
  </section>

  <section class="cta-banner">
    <img src="/images/icon.webp" alt="NihonGo" width="64" height="64">
    <h2>{html_mod.escape(t['bottom_cta_title'])}</h2>
    <p>{html_mod.escape(t['bottom_cta_sub'])}</p>
    {appstore_btn}
  </section>
</main>
{footer_html(lang, t)}
<script>{SCRIPT_JS}</script>
</body>
</html>"""


def build_doc_page(lang: str, t: dict, route: str, heading: str, sub: str, items: list[tuple[str, str]]) -> str:
    blocks = "".join(
        f'<div class="doc-item"><h2>{html_mod.escape(h)}</h2><p>{html_mod.escape(p)}</p></div>'
        for h, p in items
    )
    faq = items if route == '/support' else None
    return f"""{head_html(lang, t, heading + ' | NihonGo', route, faq_items=faq)}
<body>
{nav_html(lang, route, t)}
<main>
  <article class="doc-box">
    <h1>{html_mod.escape(heading)}</h1>
    <p style="color:var(--teal);font-weight:700;font-size:14px;margin-top:8px;">{html_mod.escape(sub)}</p>
    {blocks}
  </article>
</main>
{footer_html(lang, t)}
</body>
</html>"""


def cf_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def deploy_worker(token: str, worker_js: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    boundary = "----NihonGoBoundary918273"
    body = [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="metadata"',
        b"Content-Type: application/json",
        b"",
        json.dumps({"main_module": "index.js", "compatibility_date": "2024-03-03"}).encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="index.js"; filename="index.js"',
        b"Content-Type: application/javascript+module",
        b"",
        worker_js.encode("utf-8"),
        f"--{boundary}--".encode(),
        b"",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(body),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        res = json.loads(resp.read())
        assert res.get("success"), f"Worker upload failed: {res}"
        print("WORKER_UPLOADED:", SCRIPT_NAME)


def ensure_dns_and_route(token: str) -> None:
    dns = cf_request("GET", f"/zones/{ZONE_ID}/dns_records?name={HOSTNAME}", token)
    existing = dns.get("result", [])
    if not existing:
        created = cf_request("POST", f"/zones/{ZONE_ID}/dns_records", token, {
            "type": "A",
            "name": HOSTNAME,
            "content": "192.0.2.1",
            "proxied": True,
            "ttl": 1,
        })
        assert created.get("success"), f"DNS create failed: {created}"
        print("DNS_CREATED:", HOSTNAME)
    else:
        print("DNS_EXISTS:", [(r["type"], r["name"], r["content"], r["proxied"]) for r in existing])

    routes = cf_request("GET", f"/zones/{ZONE_ID}/workers/routes", token).get("result", [])
    pattern = f"{HOSTNAME}/*"
    match = [r for r in routes if r.get("pattern") == pattern]
    if not match:
        rc = cf_request("POST", f"/zones/{ZONE_ID}/workers/routes", token, {
            "pattern": pattern,
            "script": SCRIPT_NAME,
        })
        assert rc.get("success"), f"Route create failed: {rc}"
        print("ROUTE_CREATED:", pattern, "->", SCRIPT_NAME)
    else:
        rid = match[0]["id"]
        if match[0].get("script") != SCRIPT_NAME:
            cf_request("PUT", f"/zones/{ZONE_ID}/workers/routes/{rid}", token, {
                "pattern": pattern,
                "script": SCRIPT_NAME,
            })
            print("ROUTE_UPDATED:", pattern, "->", SCRIPT_NAME)
        else:
            print("ROUTE_EXISTS:", pattern, "->", SCRIPT_NAME)


def main() -> None:
    pages = {}
    privacy_pages = {}
    support_pages = {}
    for code, t in CONTENT.items():
        home_html = build_home(code, t)
        priv_html = build_doc_page(code, t, "/privacy", t["privacy_title"], t["privacy_updated"], t["privacy_sections"])
        supp_html = build_doc_page(code, t, "/support", t["support_title"], t["support_sub"], t["support_cards"])
        pages[code] = home_html
        privacy_pages[code] = priv_html
        support_pages[code] = supp_html
        suffix = "" if code == "en" else f"_{code}"
        (PUBLIC_DIR / f"index{suffix}.html").write_text(home_html, encoding="utf-8")
        (PUBLIC_DIR / f"privacy{suffix}.html").write_text(priv_html, encoding="utf-8")
        (PUBLIC_DIR / f"support{suffix}.html").write_text(supp_html, encoding="utf-8")

    images = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(IMG_DIR.glob("*"))}
    audio = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(AUD_DIR.glob("*.mp3"))}

    _site_langs = ('en', 'zh-Hant', 'zh-Hans', 'es')
    def _sm_entry(path: str, code: str, prio: str) -> str:
        loc = f"{ORIGIN}{path}" if code == "en" else f"{ORIGIN}{path}?lang={code}"
        links = "\n".join(
            [f'    <xhtml:link rel="alternate" hreflang="{c}" href="{ORIGIN}{path}' + ("" if c == "en" else f"?lang={c}") + '"/>' for c in _site_langs]
            + [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}"/>']
        )
        return f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-11-26</lastmod>\n{links}\n    <priority>{prio}</priority>\n  </url>"

    sitemap_urls = "\n".join(
        [_sm_entry("/", c, "1.0" if c == "en" else "0.9") for c in _site_langs]
        + [_sm_entry("/privacy", "en", "0.7"), _sm_entry("/support", "en", "0.7")]
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{sitemap_urls}\n</urlset>'
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"

    worker_js = f"""const PAGES = {json.dumps(pages)};
const PRIVACY_PAGES = {json.dumps(privacy_pages)};
const SUPPORT_PAGES = {json.dumps(support_pages)};
const IMAGES = {json.dumps(images)};
const AUDIO = {json.dumps(audio)};
const SITEMAP = {json.dumps(sitemap_xml)};
const ROBOTS = {json.dumps(robots_txt)};

function b64ToBytes(b64) {{
  const s = atob(b64);
  const out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}}

function resolveLang(request) {{
  const url = new URL(request.url);
  const q = url.searchParams.get("lang");
  if (q && PAGES[q]) return q;
  if (q === "zh-TW" || q === "tw" || q === "hk") return "zh-Hant";
  if (q === "zh-CN" || q === "cn" || q === "zh") return "zh-Hans";
  const accept = (request.headers.get("accept-language") || "").toLowerCase();
  if (accept.includes("zh-tw") || accept.includes("zh-hk") || accept.includes("zh-hant")) return "zh-Hant";
  if (accept.includes("zh")) return "zh-Hans";
  if (accept.includes("es")) return "es";
  return "en";
}}

export default {{
  async fetch(request) {{
    const pathname = new URL(request.url).pathname;
    if (pathname === "/sitemap.xml") {{
      return new Response(SITEMAP, {{ headers: {{ "content-type": "application/xml;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname === "/robots.txt") {{
      return new Response(ROBOTS, {{ headers: {{ "content-type": "text/plain;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname.startsWith("/images/")) {{
      const name = pathname.slice("/images/".length);
      if (IMAGES[name]) {{
        const ct = name.endsWith(".png") ? "image/png" : "image/webp";
        return new Response(b64ToBytes(IMAGES[name]), {{ headers: {{ "content-type": ct, "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    if (pathname.startsWith("/audio/")) {{
      const name = pathname.slice("/audio/".length);
      if (AUDIO[name]) {{
        return new Response(b64ToBytes(AUDIO[name]), {{ headers: {{ "content-type": "audio/mpeg", "accept-ranges": "bytes", "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    const lang = resolveLang(request);
    const htmlHeaders = {{
      "content-type": "text/html;charset=UTF-8",
      "cache-control": "public, max-age=0, must-revalidate",
      "vary": "Accept-Language"
    }};
    if (pathname === "/privacy" || pathname === "/privacy.html") {{
      return new Response(PRIVACY_PAGES[lang] || PRIVACY_PAGES.en, {{ headers: htmlHeaders }});
    }}
    if (pathname === "/support" || pathname === "/support.html") {{
      return new Response(SUPPORT_PAGES[lang] || SUPPORT_PAGES.en, {{ headers: htmlHeaders }});
    }}
    return new Response(PAGES[lang] || PAGES.en, {{ headers: htmlHeaders }});
  }}
}};
"""
    (BASE_DIR / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"BUILT_WORKER: {len(worker_js) / 1024:.1f} KB")

    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        token = Path("~/.cf_token").expanduser().read_text().strip()
    deploy_worker(token, worker_js)
    ensure_dns_and_route(token)
    print("DEPLOY_COMPLETE:", ORIGIN)


if __name__ == "__main__":
    main()
