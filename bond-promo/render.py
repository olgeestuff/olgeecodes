"""Render the promo clip: iris reveal -> slow push-in -> flash on final hit.
Usage: python3 render.py <landscape|vertical> <out.mp4> <music.wav>
"""
import sys, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

MODE, OUT, AUDIO = sys.argv[1], sys.argv[2], sys.argv[3]
FPS, DUR = 30, 12.0
src = Image.open("source.webp").convert("RGB")
SW, SH = src.size
FACE = (1050 / SW, 330 / SH)  # iris centre (relative), on the face

W, H = (1600, 1008) if MODE == "landscape" else (1080, 1920)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ease(x):
    x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def zoomed(img, w, h, z, fx, fy):
    """Crop a 1/z window drifting toward (fx,fy) and resize to w x h."""
    iw, ih = img.size
    cw, ch = iw / z, ih / z
    cx = iw / 2 + (fx * iw - iw / 2) * (z - 1) * 1.5
    cy = ih / 2 + (fy * ih - ih / 2) * (z - 1) * 1.5
    l = min(max(cx - cw / 2, 0), iw - cw); t = min(max(cy - ch / 2, 0), ih - ch)
    return img.resize((w, h), Image.LANCZOS, box=(l, t, l + cw, t + ch))

if MODE == "vertical":
    bg = src.resize((int(SW * 1920 / SH), 1920), Image.LANCZOS)
    bg = bg.crop(((bg.width - 1080) // 2, 0, (bg.width - 1080) // 2 + 1080, 1920))
    bg = bg.filter(ImageFilter.GaussianBlur(28)).point(lambda p: int(p * 0.35))
    FW, FH = 1080, int(SH * 1080 / SW); FY = 560
    d = ImageDraw.Draw(bg)
    f1 = ImageFont.truetype(BOLD, 74); f2 = ImageFont.truetype(BOLD, 52)
    for i, line in enumerate(["There's a new", "agent in town."]):
        d.text((540, 230 + i * 92), line, font=f1, fill="white", anchor="mm")
    d.text((540, 1460), "Your 007 for", font=f2, fill=(245, 190, 40), anchor="mm")
    d.text((540, 1530), "business automation", font=f2, fill=(245, 190, 40), anchor="mm")
    d.text((540, 1680), "Link in bio  >  Free discovery call", font=ImageFont.truetype(BOLD, 40), fill="white", anchor="mm")

ff = subprocess.Popen([
    "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", AUDIO,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT],
    stdin=subprocess.PIPE)

for i in range(int(FPS * DUR)):
    t = i / FPS
    z = 1.0 + 0.04 * ease(t / DUR)
    if MODE == "landscape":
        frame = zoomed(src, W, H, z, *FACE)
        cx, cy = FACE[0] * W, FACE[1] * H
    else:
        frame = bg.copy()
        frame.paste(zoomed(src, FW, FH, z, *FACE), (0, FY))
        cx, cy = FACE[0] * FW, FY + FACE[1] * FH
    # iris (gun-barrel style) reveal over first 1.3s
    if t < 1.5:
        r0 = 0.12 * min(W, H)
        r = r0 if t < 0.5 else r0 + ease((t - 0.5) / 1.0) * math.hypot(W, H)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        frame = Image.composite(frame, Image.new("RGB", (W, H)), mask)
    # flash on the final music hit at 11.0s
    if 11.0 <= t < 11.35:
        a = 0.55 * (1 - (t - 11.0) / 0.35)
        frame = Image.blend(frame, Image.new("RGB", (W, H), "white"), a)
    # fade out last 0.4s
    if t > DUR - 0.4:
        frame = Image.blend(frame, Image.new("RGB", (W, H)), (t - (DUR - 0.4)) / 0.4)
    ff.stdin.write(frame.tobytes())
ff.stdin.close(); ff.wait()
