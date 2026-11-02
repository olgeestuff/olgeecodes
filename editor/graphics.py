"""Code-built motion graphics: keyword badges (+ optional IconScout icon) and SFX.

Badges are PNGs made with Pillow; the animation (fade + slide) is applied in ffmpeg.
SFX (whoosh, pop) are synthesised with ffmpeg the first time, so they are royalty free.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import REFS, WORK, ffmpeg_bin, ref_path, run

NUMBER_RE = re.compile(r"^\$?\d[\d,.]*(%|k|K|m|M)?$")


def _font(cfg: dict, size: int) -> ImageFont.FreeTypeFont:
    for cand in (ref_path(cfg["captions"]["font_file"]),
                 Path("/usr/share/fonts/opentype/inter/Inter-Black.otf"),
                 Path("C:/Windows/Fonts/arialbd.ttf")):
        if cand.exists():
            return ImageFont.truetype(str(cand), size)
    return ImageFont.load_default()


def make_badge(text: str, cfg: dict, icon: str | None = None, scale: int = 2) -> Path:
    g = cfg["graphics"]
    WORK.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_") or "badge"
    out = WORK / f"badge_{safe}.png"
    font = _font(cfg, 54 * scale)
    pad_x, pad_y, gap = 38 * scale, 24 * scale, 18 * scale
    tw, th = font.getbbox(text)[2:]
    icon_img = None
    if icon:
        p = REFS / "icons" / icon
        if p.exists():
            icon_img = Image.open(p).convert("RGBA")
            ih = 64 * scale
            icon_img = icon_img.resize((int(icon_img.width * ih / icon_img.height), ih), Image.LANCZOS)
    iw = (icon_img.width + gap) if icon_img else 0
    w = pad_x * 2 + iw + tw
    h = pad_y * 2 + max(th, icon_img.height if icon_img else 0)
    shadow = 10 * scale
    img = Image.new("RGBA", (w + shadow * 2, h + shadow * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((shadow + 4, shadow + 8, shadow + w + 4, shadow + h + 8), radius=h // 2,
                        fill=(0, 0, 0, 90))
    d.rounded_rectangle((shadow, shadow, shadow + w, shadow + h), radius=h // 2, fill=g["badge_color"])
    accent_w = 12 * scale
    d.rounded_rectangle((shadow, shadow, shadow + accent_w + h // 2, shadow + h), radius=h // 2,
                        fill=g["accent_color"])
    d.rounded_rectangle((shadow + accent_w, shadow, shadow + w, shadow + h), radius=h // 2,
                        fill=g["badge_color"])
    x = shadow + pad_x
    if icon_img:
        img.alpha_composite(icon_img, (x, shadow + (h - icon_img.height) // 2))
        x += icon_img.width + gap
    d.text((x, shadow + (h - th) // 2 - font.getbbox(text)[1] // 2), text, font=font,
           fill=g["badge_text_color"])
    img = img.resize((img.width // scale, img.height // scale), Image.LANCZOS)
    img.save(out)
    return out


def pick_graphics(words: list[dict], cfg: dict, t_min: float, t_max: float) -> list[dict]:
    """Choose keyword pop-ins from the transcript. Returns [{start, end, png}]."""
    g = cfg["graphics"]
    if not g.get("enabled"):
        return []
    keys = {k.lower(): v for k, v in (g.get("keywords") or {}).items()}
    picks, last, used = [], -1e9, set()
    for w in words:
        if not (t_min <= w["start"] <= t_max - g["duration"]):
            continue
        raw = w["word"].strip(".,!?;:\"'()").replace("’", "'")
        key = raw.lower()
        item = None
        if key in keys and key not in used:
            item = keys[key]
        elif g.get("auto_numbers") and NUMBER_RE.match(raw) and raw not in used and len(raw) > 1:
            item = {"text": raw, "icon": None}
        if not item or w["start"] - last < g["min_gap"]:
            continue
        used.add(key if key in keys else raw)
        picks.append({"start": w["start"], "end": w["start"] + g["duration"],
                      "png": make_badge(item["text"], cfg, item.get("icon"))})
        last = w["start"]
        if len(picks) >= g["max_count"]:
            break
    return picks


def ensure_sfx(cfg: dict) -> dict:
    """Create whoosh/pop wavs if missing. Returns {'whoosh': Path, 'pop': Path}."""
    sfx = cfg["audio"]["sfx"]
    paths = {"whoosh": ref_path(sfx["whoosh"]), "pop": ref_path(sfx["pop"])}
    ff = ffmpeg_bin()
    if not paths["whoosh"].exists():
        paths["whoosh"].parent.mkdir(parents=True, exist_ok=True)
        run([ff, "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.45:c=pink:a=0.6:r=48000",
             "-af", "highpass=f=300,lowpass=f=6000,afade=t=in:d=0.18:curve=exp,"
                    "afade=t=out:st=0.2:d=0.25,volume=1.6", "-ac", "2", paths["whoosh"]])
    if not paths["pop"].exists():
        paths["pop"].parent.mkdir(parents=True, exist_ok=True)
        run([ff, "-y", "-f", "lavfi", "-i",
             "aevalsrc='0.8*sin(2*PI*(500+900*exp(-t*40))*t)*exp(-t*28)':d=0.18:s=48000",
             "-ac", "2", paths["pop"]])
    return paths
