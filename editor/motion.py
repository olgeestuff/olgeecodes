"""Code-built motion-graphic B-roll clips (no stock footage needed).

paperwork: document cards (receipt, invoice, lease, quote...) fly in one by one, each
landing on the spoken word, piling up into a messy stack with a label for the current one.
Used by plan segments like:
    - at: "receipts"
      graphic: paperwork
      items:
        - {at: "receipts", label: "Receipts", kind: receipt}
        - {at: "invoices", label: "Invoices", kind: invoice}
"""
from __future__ import annotations

import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from common import WORK, ffmpeg_bin
from graphics import _font

KINDS = {   # header colour, title on the page
    "receipt": ("#2E7D32", "RECEIPT"),
    "invoice": ("#E1251B", "INVOICE"),
    "lease": ("#1565C0", "LEASE AGREEMENT"),
    "rental": ("#6A1B9A", "RENTAL AGREEMENT"),
    "quote": ("#EF6C00", "QUOTATION"),
    "contract": ("#37474F", "CONTRACT"),
    "statement": ("#00838F", "STATEMENT"),
}


def _doc(kind: str, cfg: dict, w: int = 300, h: int = 396) -> Image.Image:
    color, title = KINDS.get(kind, KINDS["contract"])
    s = 2
    W, H = w * s, h * s
    img = Image.new("RGBA", (W + 40 * s, H + 40 * s), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((26 * s, 30 * s, W + 26 * s, H + 30 * s), 14 * s, fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10 * s)))
    page = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(page)
    if kind == "receipt":                       # zig-zag bottom edge
        pts = [(0, 0), (W, 0), (W, H - 16 * s)]
        n = 10
        for i in range(n, -1, -1):
            pts.append((W * i / n, H - (0 if i % 2 else 16 * s)))
        d.polygon(pts, fill="#FAFAF7")
    else:
        d.rounded_rectangle((0, 0, W - 1, H - 1), 12 * s, fill="#FAFAF7")
    d.rounded_rectangle((0, 0, W - 1, 56 * s), 12 * s, fill=color)
    d.rectangle((0, 40 * s, W - 1, 56 * s), fill=color)
    f = _font(cfg, 22 * s if len(title) < 10 else 15 * s)
    d.text((18 * s, 28 * s), title, font=f, fill="white", anchor="lm")
    y = 80 * s
    for i in range(7):                          # text lines
        lw = W - 36 * s - (60 * s if i % 3 == 2 else 0)
        d.rounded_rectangle((18 * s, y, 18 * s + lw, y + 9 * s), 4 * s, fill="#D5D8DC")
        y += 24 * s
    if kind in ("invoice", "receipt", "quote", "statement"):
        d.rounded_rectangle((W - 120 * s, H - 70 * s, W - 18 * s, H - 38 * s), 6 * s, fill=color)
        d.text((W - 69 * s, H - 54 * s), "$ 1,240", font=_font(cfg, 15 * s), fill="white", anchor="mm")
    else:                                       # signature squiggle
        pts = [(24 * s + i * 4 * s, H - 52 * s + 10 * s * math.sin(i / 2.2)) for i in range(30)]
        d.line(pts, fill="#1A237E", width=3 * s)
        d.line((18 * s, H - 36 * s, W / 2, H - 36 * s), fill="#9AA0A6", width=2 * s)
    img.alpha_composite(page, (20 * s, 20 * s))
    return img.resize((img.width // s, img.height // s), Image.LANCZOS)


def _ease_out_back(x: float) -> float:
    c1, c3 = 1.70158, 2.70158
    x = min(max(x, 0.0), 1.0)
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def render_paperwork(items: list[dict], dur: float, w: int, h: int, cfg: dict, out: Path,
                     fps: int = 30) -> Path:
    """items: [{t: seconds from clip start, label, kind}] -> silent mp4 of size w x h."""
    rnd = random.Random(7)
    docs = [_doc(it.get("kind", "contract"), cfg) for it in items]
    # landing spots: a loose pile around the centre
    spots = []
    for i, _ in enumerate(items):
        ang = i * 2.4
        r = 0.10 + 0.05 * (i % 3)
        spots.append((0.5 + r * math.cos(ang), 0.44 + 0.7 * r * math.sin(ang), rnd.uniform(-16, 16)))
    accent = cfg["graphics"]["accent_color"]
    lab_font = _font(cfg, 58)
    bg = Image.new("RGBA", (w, h), "#0E0E12")
    gd = ImageDraw.Draw(bg)
    for gx in range(0, w, 54):                 # faint grid for depth
        gd.line((gx, 0, gx, h), fill="#16161C")
    for gy in range(0, h, 54):
        gd.line((0, gy, w, gy), fill="#16161C")

    cmd = [ffmpeg_bin(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-pix_fmt", "yuv420p", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(dur * fps))
    fly = 0.42
    for fi in range(n):
        t = fi / fps
        frame = bg.copy()
        current = None
        for i, (it, doc) in enumerate(zip(items, docs)):
            t0 = it["t"] - 0.12                  # land right on the word
            if t < t0:
                continue
            current = i
            p = _ease_out_back((t - t0) / fly)
            sx, sy, rot = spots[i]
            fx, fy = 1.35, sy - 0.25            # fly in from the right, slightly above
            x = (fx + (sx - fx) * p) * w
            y = (fy + (sy - fy) * p) * h
            # gentle float after landing, so the pile feels alive
            x += 4 * math.sin(t * 1.7 + i)
            y += 4 * math.cos(t * 1.3 + i)
            r = rot + (1 - p) * 35
            scale = 1.0 if i == current else 0.92
            im = doc.rotate(r, resample=Image.BICUBIC, expand=True)
            if scale != 1.0:
                im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
            frame.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        if current is not None:                 # label for the latest document
            text = items[current]["label"]
            age = t - (items[current]["t"] - 0.12)
            a = min(1.0, age / 0.15)
            tb = lab_font.getbbox(text)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
            lx, ly = (w - tw) // 2, int(h * 0.86) + int((1 - a) * 20)
            lab = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lab)
            ld.rectangle((lx - 24, ly - 14, lx + tw + 24, ly + th + 18), fill=accent)
            ld.text((lx - tb[0], ly - tb[1]), text, font=lab_font, fill="white")
            if a < 1:
                lab.putalpha(lab.getchannel("A").point(lambda v: int(v * a)))
            frame.alpha_composite(lab)
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    return out


if __name__ == "__main__":   # quick preview
    from common import load_config
    WORK.mkdir(parents=True, exist_ok=True)
    demo = [{"t": 0.3, "label": "Receipts", "kind": "receipt"},
            {"t": 1.3, "label": "Invoices", "kind": "invoice"},
            {"t": 2.3, "label": "Lease agreements", "kind": "lease"},
            {"t": 3.3, "label": "Rental agreements", "kind": "rental"},
            {"t": 4.3, "label": "Quotes", "kind": "quote"}]
    print(render_paperwork(demo, 6.0, 972, 772, load_config(), WORK / "paperwork_preview.mp4"))
