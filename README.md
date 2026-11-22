# NihonGo — Travel Japanese & Live Voice Translation Website

Official marketing, audio preview, privacy policy, and support website for **NihonGo Travel Japanese** ([AE Interactive](https://appengine.fun)).

- **Live Website:** https://nihongo.appengine.fun
- **App Store Download:** https://apps.apple.com/app/id6836279889

## Features
- **4 Languages Supported:** English (`/`), Traditional Chinese (`/?lang=zh-Hant`), Simplified Chinese (`/?lang=zh-Hans`), and Spanish (`/?lang=es`).
- **App Store Conversion:** iOS Safari Smart App Banner (`app-id=6836279889`), App Store CTAs across nav/hero/pricing/footer, `Free Forever` vs. `$3.99 Lifetime Pro` comparison, `hreflang`, and `SoftwareApplication` JSON-LD.
- **Interactive Native Phrase Previews:** In-browser studio MP3 playback with particle-highlighted Romaji.
- **Localized `/privacy` & `/support`:** Zero-data-collection policy and compatibility docs.
- **Cloudflare Worker Edge Bundle:** Single-file deployment serving HTML, WebP screenshots, and MP3 clips cleanly.

## Build & Deploy
```bash
python3 build_and_deploy.py
```
