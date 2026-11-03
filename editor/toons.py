"""Code-drawn cartoon story scenes (flat explainer style) for the B-roll card.

Characters have faces, blink, bounce, wave and talk; scenes are timed to spoken words.
Plan usage:
    - at: "usually"
      graphic: story
      scenes:
        - {at: "usually", scene: family_shop, sign: "FAMILY BUSINESS"}
        - {at: "this person", scene: spotlight}
        - {at: "every supplier", scene: thinker, items: [
              {at: "supplier", icon: truck, label: "Every supplier"},
              {at: "payment", icon: money, label: "Every payment"},
              {at: "contact", icon: phone, label: "Every contact"}]}
        - {at: "leaves", scene: walk_out}
        - {at: "retires", scene: retire}
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from common import ffmpeg_bin
from graphics import _font

SS = 2  # supersampling for smooth edges

# ---- cast -------------------------------------------------------------------------------------
BOSS = dict(skin="#8D5524", hair="#D9D9D9", bald=True, beard="#E6E6E6", glasses=True,
            shirt="#2E5AAC", pants="#2B2B33", tie="#E1251B")
MUM = dict(skin="#C68642", hair="#2B1B12", bald=False, beard=None, glasses=False,
           shirt="#E1251B", pants="#3B3B45", tie=None, long_hair=True)
SON = dict(skin="#A0662F", hair="#1B1B1B", bald=False, beard=None, glasses=False,
           shirt="#2E7D32", pants="#2B2B33", tie=None)


def _ease(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def _lin(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def person(d: ImageDraw.ImageDraw, cx: float, foot: float, s: float, p: dict, t: float,
           wave: float = 0.0, talk: bool = False, walk: float = -1.0, mood: str = "smile",
           dim: float = 0.0, face_dir: int = 0):
    """Draw a character standing with feet at y=foot, centred on cx. s = scale (1 ~ 300px tall)."""
    def c(hexcol):                      # dim colours toward the background
        if dim <= 0:
            return hexcol
        r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
        k = 1 - 0.65 * dim
        return (int(r * k + 14 * (1 - k)), int(g * k + 14 * (1 - k)), int(b * k + 18 * (1 - k)))

    u = s * SS
    bob = 3 * u * math.sin(t * 6) if walk >= 0 else 2 * u * math.sin(t * 2.2)
    leg_h, torso_h, head_r = 78 * u, 92 * u, 44 * u
    hip = foot - leg_h + bob
    sh = hip - torso_h
    # legs
    for side in (-1, 1):
        swing = 18 * u * math.sin(walk * 2 * math.pi + (0 if side < 0 else math.pi)) if walk >= 0 else 0
        x = cx + side * 16 * u
        d.line((x, hip, x + swing, foot - 8 * u), fill=c(p["pants"]), width=int(22 * u))
        d.ellipse((x + swing - 16 * u, foot - 16 * u, x + swing + 20 * u, foot + 2 * u), fill=c("#1C1C22"))
    # torso
    d.rounded_rectangle((cx - 42 * u, sh, cx + 42 * u, hip + 6 * u), 22 * u, fill=c(p["shirt"]))
    if p.get("tie"):
        d.polygon([(cx - 7 * u, sh + 4 * u), (cx + 7 * u, sh + 4 * u), (cx + 4 * u, sh + 60 * u),
                   (cx, sh + 68 * u), (cx - 4 * u, sh + 60 * u)], fill=c(p["tie"]))
    # arms (right arm can wave)
    for side in (-1, 1):
        x0 = cx + side * 40 * u
        if side == 1 and wave > 0:
            ang = -2.2 + 0.35 * math.sin(t * 10)
        elif walk >= 0:
            ang = (math.pi / 2) + 0.4 * math.sin(walk * 2 * math.pi + (math.pi if side > 0 else 0))
        else:
            ang = math.pi / 2 - side * 0.15
        L = 70 * u
        x1 = x0 + math.cos(ang) * L * (1 if side > 0 else 1) * (1 if side > 0 or walk >= 0 else -1) \
            if side > 0 else x0 - abs(math.cos(ang)) * L * 0.4
        y1 = sh + 12 * u + math.sin(ang) * L
        if side == 1 and wave > 0:
            x1, y1 = x0 + 34 * u, sh - 52 * u + 6 * u * math.sin(t * 10)
        d.line((x0, sh + 14 * u, x1, y1), fill=c(p["shirt"]), width=int(20 * u))
        d.ellipse((x1 - 11 * u, y1 - 11 * u, x1 + 11 * u, y1 + 11 * u), fill=c(p["skin"]))
    # neck + head
    hy = sh - head_r + 6 * u
    d.rectangle((cx - 10 * u, sh - 14 * u, cx + 10 * u, sh + 4 * u), fill=c(p["skin"]))
    if p.get("long_hair"):
        d.rounded_rectangle((cx - head_r - 6 * u, hy - 20 * u, cx + head_r + 6 * u, hy + head_r + 26 * u),
                            30 * u, fill=c(p["hair"]))
    d.ellipse((cx - head_r, hy - head_r, cx + head_r, hy + head_r), fill=c(p["skin"]))
    # ears
    for side in (-1, 1):
        d.ellipse((cx + side * head_r - 7 * u, hy - 6 * u, cx + side * head_r + 7 * u, hy + 12 * u), fill=c(p["skin"]))
    # hair
    if p.get("bald"):
        for side in (-1, 1):
            d.chord((cx + side * head_r - 16 * u, hy - 20 * u, cx + side * head_r + 16 * u, hy + 14 * u),
                    90 if side > 0 else -90, 270 if side > 0 else 90, fill=c(p["hair"]))
    else:
        d.chord((cx - head_r - 2 * u, hy - head_r - 6 * u, cx + head_r + 2 * u, hy + head_r * 0.5),
                180, 360, fill=c(p["hair"]))
    if p.get("beard"):
        d.chord((cx - head_r * 0.85, hy - 6 * u, cx + head_r * 0.85, hy + head_r + 14 * u), 0, 180,
                fill=c(p["beard"]))
    # face
    fx = face_dir * 6 * u
    blink = (t % 3.1) < 0.12
    for side in (-1, 1):
        ex, ey = cx + fx + side * 16 * u, hy - 4 * u
        if blink:
            d.line((ex - 7 * u, ey, ex + 7 * u, ey), fill=c("#1C1C22"), width=int(3 * u))
        else:
            d.ellipse((ex - 8 * u, ey - 9 * u, ex + 8 * u, ey + 9 * u), fill=c("#FFFFFF"))
            d.ellipse((ex - 4 * u + fx * 0.3, ey - 4 * u, ex + 4 * u + fx * 0.3, ey + 5 * u), fill=c("#1C1C22"))
        brow_y = ey - 15 * u - (3 * u if mood == "worried" else 0)
        tilt = (4 * u * side) if mood == "worried" else 0
        d.line((ex - 9 * u, brow_y + tilt, ex + 9 * u, brow_y - tilt), fill=c(p["hair"] if not p.get("bald") else "#9E9E9E"),
               width=int(4 * u))
        if p.get("glasses"):
            d.ellipse((ex - 13 * u, ey - 12 * u, ex + 13 * u, ey + 12 * u), outline=c("#1C1C22"), width=int(3 * u))
    if p.get("glasses"):
        d.line((cx + fx - 3 * u, hy - 4 * u, cx + fx + 3 * u, hy - 4 * u), fill=c("#1C1C22"), width=int(3 * u))
    my = hy + 18 * u
    if talk and int(t * 9) % 2 == 0:
        d.ellipse((cx + fx - 9 * u, my - 6 * u, cx + fx + 9 * u, my + 8 * u), fill=c("#5A1E1E"))
    elif mood == "worried":
        d.arc((cx + fx - 12 * u, my, cx + fx + 12 * u, my + 14 * u), 200, 340, fill=c("#3A1A1A"), width=int(3 * u))
    else:
        d.arc((cx + fx - 14 * u, my - 10 * u, cx + fx + 14 * u, my + 8 * u), 20, 160, fill=c("#3A1A1A"), width=int(4 * u))
    return (cx, hy, head_r)


# ---- icons ------------------------------------------------------------------------------------
def icon(d: ImageDraw.ImageDraw, kind: str, x: float, y: float, r: float):
    """Draw a small icon centred at x, y with radius r (already in supersampled px)."""
    if kind == "truck":
        d.rounded_rectangle((x - r, y - r * 0.55, x + r * 0.25, y + r * 0.35), r * 0.12, fill="#EF6C00")
        d.rounded_rectangle((x + r * 0.25, y - r * 0.25, x + r, y + r * 0.35), r * 0.12, fill="#F57C00")
        d.rectangle((x + r * 0.45, y - r * 0.15, x + r * 0.85, y + r * 0.05), fill="#BBDEFB")
        for wx in (-0.6, 0.6):
            d.ellipse((x + wx * r - r * 0.2, y + r * 0.2, x + wx * r + r * 0.2, y + r * 0.6), fill="#263238")
    elif kind == "money":
        d.rounded_rectangle((x - r, y - r * 0.55, x + r, y + r * 0.55), r * 0.12, fill="#2E7D32")
        d.ellipse((x - r * 0.38, y - r * 0.38, x + r * 0.38, y + r * 0.38), fill="#A5D6A7")
        d.text((x, y), "$", font=_font_px(int(r * 0.7)), fill="#1B5E20", anchor="mm")
    elif kind == "phone":
        d.rounded_rectangle((x - r * 0.5, y - r, x + r * 0.5, y + r), r * 0.15, fill="#37474F")
        d.rectangle((x - r * 0.4, y - r * 0.8, x + r * 0.4, y + r * 0.7), fill="#81D4FA")
        d.ellipse((x - r * 0.18, y - r * 0.55, x + r * 0.18, y - r * 0.2), fill="#FFFFFF")
        d.chord((x - r * 0.3, y - r * 0.15, x + r * 0.3, y + r * 0.35), 180, 360, fill="#FFFFFF")
    elif kind == "box":
        d.polygon([(x - r, y - r * 0.3), (x, y - r * 0.8), (x + r, y - r * 0.3), (x, y + r * 0.2)], fill="#D7A86E")
        d.polygon([(x - r, y - r * 0.3), (x, y + r * 0.2), (x, y + r), (x - r, y + r * 0.5)], fill="#B8834A")
        d.polygon([(x + r, y - r * 0.3), (x, y + r * 0.2), (x, y + r), (x + r, y + r * 0.5)], fill="#C99358")
    elif kind == "calendar":
        d.rounded_rectangle((x - r, y - r * 0.8, x + r, y + r * 0.9), r * 0.15, fill="#FFFFFF")
        d.rectangle((x - r, y - r * 0.8, x + r, y - r * 0.35), fill="#E1251B")
        for i in range(3):
            for j in range(3):
                d.rectangle((x - r * 0.7 + i * r * 0.5, y - r * 0.15 + j * r * 0.33,
                             x - r * 0.45 + i * r * 0.5, y + j * r * 0.33), fill="#B0BEC5")
    else:   # doc
        d.rounded_rectangle((x - r * 0.7, y - r, x + r * 0.7, y + r), r * 0.12, fill="#FAFAF7")
        for i in range(4):
            d.rectangle((x - r * 0.5, y - r * 0.6 + i * r * 0.38, x + r * 0.5, y - r * 0.5 + i * r * 0.38), fill="#B0BEC5")


_FONT_CACHE: dict = {}


def _font_px(px: int):
    if px not in _FONT_CACHE:
        from common import load_config
        _FONT_CACHE[px] = _font(load_config(), px)
    return _FONT_CACHE[px]


def label(img: Image.Image, text: str, age: float, accent: str, w: int, h: int):
    f = _font_px(58 * SS)
    tb = f.getbbox(text)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    a = _lin(age / 0.15)
    lx, ly = (w * SS - tw) // 2, int(h * SS * 0.86) + int((1 - a) * 20 * SS)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rectangle((lx - 24 * SS, ly - 14 * SS, lx + tw + 24 * SS, ly + th + 18 * SS), fill=accent)
    ld.text((lx - tb[0], ly - tb[1]), text, font=f, fill="white")
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(lay)


# ---- scenes -----------------------------------------------------------------------------------
def _bg(w, h, top="#15151C", bottom="#0E0E12"):
    img = Image.new("RGBA", (w * SS, h * SS), bottom)
    d = ImageDraw.Draw(img)
    for i in range(0, h * SS, 8):
        k = i / (h * SS)
        r1, g1, b1 = int(top[1:3], 16), int(top[3:5], 16), int(top[5:7], 16)
        r2, g2, b2 = int(bottom[1:3], 16), int(bottom[3:5], 16), int(bottom[5:7], 16)
        d.rectangle((0, i, w * SS, i + 8), fill=(int(r1 + (r2 - r1) * k), int(g1 + (g2 - g1) * k), int(b1 + (b2 - b1) * k)))
    return img


def _shop(d, W, H, sign, t_in):
    gy = H * 0.80
    d.rectangle((0, gy, W, H), fill="#22222B")                      # pavement
    x0, x1, top = W * 0.10, W * 0.90, H * 0.12
    d.rectangle((x0, top, x1, gy), fill="#F3E3C3")                  # wall
    stripes = 9
    sw = (x1 - x0) / stripes
    for i in range(stripes):                                        # awning
        d.polygon([(x0 + i * sw, top + H * 0.13), (x0 + (i + 1) * sw, top + H * 0.13),
                   (x0 + (i + 1) * sw + 6 * SS, top + H * 0.21), (x0 + i * sw - 6 * SS, top + H * 0.21)],
                  fill="#E1251B" if i % 2 == 0 else "#FFFFFF")
    d.rounded_rectangle((W * 0.22, top + H * 0.015, W * 0.78, top + H * 0.115), 10 * SS, fill="#2B2B33")
    d.text((W / 2, top + H * 0.065), sign, font=_font_px(int(40 * SS)), fill="#FFD60A", anchor="mm")
    d.rectangle((W * 0.15, top + H * 0.27, W * 0.38, gy - H * 0.17), fill="#9ED0F0")   # window
    d.rectangle((W * 0.62, top + H * 0.27, W * 0.85, gy - H * 0.17), fill="#9ED0F0")
    d.rectangle((W * 0.44, top + H * 0.30, W * 0.56, gy), fill="#6D4C41")              # door
    d.ellipse((W * 0.535, gy - H * 0.20, W * 0.55, gy - H * 0.185), fill="#FFD60A")
    return gy


def render_story(scenes: list[dict], dur: float, w: int, h: int, cfg: dict, out: Path, fps: int = 30) -> Path:
    """scenes: [{t, scene, ...}] with t = seconds from clip start; items carry t too."""
    accent = cfg["graphics"]["accent_color"]
    W, H = w * SS, h * SS
    base = _bg(w, h)
    cmd = [ffmpeg_bin(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-pix_fmt", "yuv420p", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * fps))
    for fi in range(n):
        t = fi / fps
        cur = None
        for s in scenes:
            if t >= s["t"]:
                cur = s
        img = base.copy()
        d = ImageDraw.Draw(img)
        if cur is None:
            cur = scenes[0]
        st = t - cur["t"]
        kind = cur["scene"]
        if kind in ("family_shop", "spotlight"):
            shop = next((s for s in scenes if s["scene"] == "family_shop"), cur)
            t_shop = t - shop["t"]
            gy = _shop(d, W, H, shop.get("sign", "FAMILY BUSINESS"), t_shop)
            spot = kind == "spotlight"
            cast = [(0.27, MUM, 0.0), (0.50, BOSS, 0.15), (0.73, SON, 0.3)]
            for xk, p, delay in cast:
                pop = _ease((t_shop - delay) / 0.45)
                if pop <= 0:
                    continue
                s_ = 1.15 * pop if p is BOSS else 1.02 * pop
                is_boss = p is BOSS
                if spot and is_boss:
                    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
                    ImageDraw.Draw(glow).ellipse((W * xk - 150 * SS, gy - 360 * SS, W * xk + 150 * SS, gy + 30 * SS),
                                                 fill=(255, 214, 10, 70))
                    img.alpha_composite(glow)
                    d = ImageDraw.Draw(img)
                person(d, W * xk, gy + 6 * SS, s_ * (1.08 if spot and is_boss else 1.0), p, t + delay,
                       wave=1.0 if (is_boss and (spot or 0.6 < t_shop < 2.2)) else 0.0,
                       dim=(0.8 * _lin(st / 0.3)) if (spot and not is_boss) else 0.0)
            if spot:   # "!" pop above the boss
                k = _ease(st / 0.35)
                d.ellipse((W * 0.5 - 30 * SS * k, gy - 420 * SS - 30 * SS * k, W * 0.5 + 30 * SS * k, gy - 420 * SS + 30 * SS * k),
                          fill="#FFD60A")
                if k > 0.5:
                    d.text((W * 0.5, gy - 420 * SS), "!", font=_font_px(int(46 * SS)), fill="#1C1C22", anchor="mm")
            text = cur.get("label") or (shop.get("label") if kind == "family_shop" else None)
            if text:
                label(img, text, st, accent, w, h)
        elif kind == "thinker":
            gy = H * 0.94
            d.rectangle((0, gy, W, H), fill="#22222B")
            cx = W * 0.30
            person(d, cx, gy, 1.35, BOSS, t, talk=False, mood="smile", face_dir=1)
            # thought bubble grows
            g = _ease(st / 0.4)
            bx, by, br = W * 0.66, H * 0.36, 210 * SS * g
            for k, (ox, oy, rr) in enumerate([(-0.55, 0.1, 0.55), (0.55, 0.1, 0.55), (0, -0.35, 0.6),
                                             (-0.3, 0.45, 0.5), (0.35, 0.45, 0.5), (0, 0.05, 0.75)]):
                pul = 1 + 0.03 * math.sin(t * 3 + k)
                d.ellipse((bx + ox * br - rr * br * pul, by + oy * br - rr * br * pul,
                           bx + ox * br + rr * br * pul, by + oy * br + rr * br * pul), fill="#FFFFFF")
            for k, rr in enumerate((26, 18, 11)):
                tx = cx + 80 * SS + k * 60 * SS
                ty = H * 0.44 + 70 * SS - k * 55 * SS
                rr2 = rr * SS * g
                d.ellipse((tx - rr2, ty - rr2, tx + rr2, ty + rr2), fill="#FFFFFF")
            items = cur.get("items", [])
            slots = [(-0.55, -0.05), (0.0, -0.32), (0.55, -0.05), (-0.25, 0.35), (0.3, 0.35)]
            latest = None
            for i, it in enumerate(items):
                ia = t - (it["t"] - 0.1)
                if ia < 0:
                    continue
                latest = it
                k = _ease(ia / 0.35)
                sx, sy = slots[i % len(slots)]
                if it.get("icon", "doc") != "none":
                    icon(d, it.get("icon", "doc"), bx + sx * 210 * SS, by + sy * 210 * SS, 74 * SS * k)
            if latest:
                label(img, latest.get("label", ""), t - (latest["t"] - 0.1), accent, w, h)
        elif kind == "walk_out":
            gy = H * 0.86
            d.rectangle((0, gy, W, H), fill="#22222B")
            d.rectangle((W * 0.70, H * 0.18, W * 0.92, gy), fill="#6D4C41")          # door frame
            d.rectangle((W * 0.73, H * 0.22, W * 0.89, gy), fill="#F7F3E8")          # open door light
            x = W * (0.25 + 0.55 * _lin(st / 2.2))
            person(d, x, gy, 1.0, BOSS, t, walk=(st * 1.4) % 1, face_dir=1)
            for i, kind_i in enumerate(("truck", "money", "phone")):                 # memories follow him
                fx = x - (90 + i * 70) * SS + 10 * SS * math.sin(t * 4 + i)
                fy = gy - 330 * SS - 30 * SS * math.sin(t * 3 + i)
                icon(d, kind_i, fx, fy, 34 * SS)
            if cur.get("label"):
                label(img, cur["label"], st, accent, w, h)
        elif kind == "retire":
            d.rectangle((0, H * 0.70, W, H), fill="#F2D38B")                         # sand
            d.ellipse((W * 0.70, H * 0.06, W * 0.86, H * 0.26), fill="#FFD60A")      # sun
            d.rectangle((W * 0.18, H * 0.62, W * 0.58, H * 0.70), fill="#1565C0")    # chair
            person(d, W * 0.38, H * 0.70, 1.0, BOSS, t, wave=1.0)
            if cur.get("label"):
                label(img, cur["label"], st, accent, w, h)
        frame = img.resize((w, h), Image.BILINEAR).convert("RGB")
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()
    return out


if __name__ == "__main__":
    from common import WORK, load_config
    WORK.mkdir(parents=True, exist_ok=True)
    sc = [{"t": 0.0, "scene": "family_shop", "sign": "FAMILY BUSINESS", "label": "Every family business"},
          {"t": 2.6, "scene": "spotlight", "label": "Has this person"},
          {"t": 4.4, "scene": "thinker", "items": [
              {"t": 4.8, "icon": "truck", "label": "Every supplier"},
              {"t": 5.9, "icon": "money", "label": "Every payment"},
              {"t": 7.0, "icon": "phone", "label": "Every contact"}]},
          {"t": 8.6, "scene": "walk_out", "label": "When he leaves…"},
          {"t": 10.6, "scene": "retire", "label": "Retired"}]
    print(render_story(sc, 12.0, 972, 772, load_config(), WORK / "story_preview.mp4"))
