#!/usr/bin/env python3
"""Prepare optimized WebP screenshots, icons, OG social banner, and sample Japanese MP3s for NihonGo-Website."""
from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SITE_DIR = Path("/Users/kevin/.gemini/antigravity/scratch/NihonGo-Website")
PUB_IMG = SITE_DIR / "public/images"
PUB_AUD = SITE_DIR / "public/audio"

SHOTS_ROOT = Path("/Users/kevin/.gemini/antigravity/scratch/NihonGo_AppStore_Release/Screenshots")
ICON_SRC = Path("/Users/kevin/.gemini/antigravity/scratch/NihonGo_AppStore_Release/AppIcon/NihonGo_AppIcon_1024x1024.png")
AUDIO_SRC = Path("/Users/kevin/.gemini/antigravity/scratch/KanaMaster.swiftpm/Resources/Audio")

LANG_MAP = {
    "en": "en-US",
    "zh-Hant": "zh-Hant",
    "zh-Hans": "zh-Hans",
    "es": "es-ES",
}

SCENES = [
    ("01_LearnPath.png", "s01"),
    ("02_AITutor.png", "s02"),
    ("03_Interpreter.png", "s03"),
    ("04_VideoScenarios.png", "s04"),
    ("05_KanaChart.png", "s05"),
]

AUDIO_SAMPLES = [
    ("vocab_ex_v_betsubetsu.mp3", "split.mp3"),
    ("vocab_ex_v_bansen.mp3", "platform.mp3"),
    ("vocab_ex_v_chekkuin.mp3", "checkout.mp3"),
    ("vocab_ex_v_chotto_matte.mp3", "wait.mp3"),
]


def round_icon(im: Image.Image, radius_ratio: float = 0.22) -> Image.Image:
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius=int(w * radius_ratio), fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def build_og_image(icon_img: Image.Image) -> None:
    w, h = 1200, 630
    bg = Image.new("RGB", (w, h), (9, 11, 22))
    px = bg.load()
    for y in range(h):
        ty = y / (h - 1)
        for x in range(w):
            tx = x / (w - 1)
            r = int(14 + 34 * (1 - tx) * 0.6 + 18 * ty)
            g = int(18 + 26 * ty + 35 * tx * 0.5)
            b = int(42 + 62 * (1 - ty * 0.5) + 30 * tx * 0.3)
            px[x, y] = (min(255, r), min(255, g), min(255, b))

    canvas = bg.convert("RGBA")
    ic = round_icon(icon_img.resize((220, 220), Image.Resampling.LANCZOS), 0.22)
    canvas.paste(ic, (96, (h - 220) // 2), ic)

    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 78, index=1)
    f_sub = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 34, index=0)
    f_pill = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 24, index=1)

    tx_x = 368
    draw.text((tx_x, 178), "NihonGo", font=f_title, fill=(255, 255, 255, 255))
    draw.text((tx_x, 276), "100 Japan Travel Video Dialogues", font=f_sub, fill=(180, 224, 245, 245))
    draw.text((tx_x, 324), "Guided Voice Coach & Live Translation", font=f_sub, fill=(203, 213, 225, 235))
    draw.text((tx_x, 404), "iOS  ·  iPadOS  ·  iPhone Duo  |  AE Interactive", font=f_pill, fill=(94, 234, 212, 245))

    canvas.convert("RGB").save(PUB_IMG / "og.png", format="PNG", optimize=True)


def main() -> None:
    PUB_IMG.mkdir(parents=True, exist_ok=True)
    PUB_AUD.mkdir(parents=True, exist_ok=True)

    icon = Image.open(ICON_SRC).convert("RGB")
    round_icon(icon.resize((256, 256), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.webp", format="WEBP", quality=88)
    round_icon(icon.resize((512, 512), Image.Resampling.LANCZOS)).save(PUB_IMG / "icon.png", format="PNG", optimize=True)
    build_og_image(icon)

    for site_lang, rel_folder in LANG_MAP.items():
        for src_name, short in SCENES:
            src = SHOTS_ROOT / rel_folder / "iPhone_6.9" / src_name
            im = Image.open(src).convert("RGB")
            im_s = im.resize((640, 1390), Image.Resampling.LANCZOS)
            im_s.save(PUB_IMG / f"{site_lang}_{short}.webp", format="WEBP", quality=84)

        duo_src = SHOTS_ROOT / rel_folder / "iPhone_Duo_Inner" / "02_AITutor.png"
        duo_im = Image.open(duo_src).convert("RGB").resize((760, 1080), Image.Resampling.LANCZOS)
        duo_im.save(PUB_IMG / f"{site_lang}_duo.webp", format="WEBP", quality=84)

    for src_name, dst_name in AUDIO_SAMPLES:
        shutil.copy2(AUDIO_SRC / src_name, PUB_AUD / dst_name)

    total_img = sum(p.stat().st_size for p in PUB_IMG.glob("*"))
    total_aud = sum(p.stat().st_size for p in PUB_AUD.glob("*"))
    print(f"ASSETS_READY: images={len(list(PUB_IMG.glob('*')))} ({total_img/1024:.1f} KB), audio={len(list(PUB_AUD.glob('*')))} ({total_aud/1024:.1f} KB)")


if __name__ == "__main__":
    main()
