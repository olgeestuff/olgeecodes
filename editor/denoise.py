"""Voice cleanup: AI noise removal with DeepFilterNet (free, offline, CapCut "Reduce noise" style).

Removes background hiss, fan and room noise and street sound while keeping the voice.
The `deep-filter` program is downloaded once into editor/bin/ (Linux, Windows or macOS).

  python editor/denoise.py "AI video editors/raw footage/hook 1 video.mp4"   -> writes a .clean.wav to listen to
"""
from __future__ import annotations

import platform
import stat
import sys
import urllib.request
from pathlib import Path

from common import WORK, ffmpeg_bin, load_config, run

VERSION = "0.5.6"
BIN_DIR = Path(__file__).with_name("bin")
ASSETS = {
    ("Linux", "x86_64"): f"deep-filter-{VERSION}-x86_64-unknown-linux-musl",
    ("Linux", "aarch64"): f"deep-filter-{VERSION}-aarch64-unknown-linux-gnu",
    ("Windows", "AMD64"): f"deep-filter-{VERSION}-x86_64-pc-windows-msvc.exe",
    ("Darwin", "x86_64"): f"deep-filter-{VERSION}-x86_64-apple-darwin",
    ("Darwin", "arm64"): f"deep-filter-{VERSION}-aarch64-apple-darwin",
}


def ensure_binary() -> Path:
    key = (platform.system(), platform.machine())
    if key not in ASSETS:
        raise RuntimeError(f"No DeepFilterNet build for {key}; set audio.denoise.enabled: false")
    exe = BIN_DIR / ("deep-filter.exe" if key[0] == "Windows" else "deep-filter")
    if exe.exists():
        return exe
    BIN_DIR.mkdir(exist_ok=True)
    url = f"https://github.com/Rikorose/DeepFilterNet/releases/download/v{VERSION}/{ASSETS[key]}"
    print(f"  downloading noise remover (one time): {url}")
    tmp = exe.with_suffix(".part")
    for attempt in range(4):
        try:
            urllib.request.urlretrieve(url, tmp)
            break
        except OSError:
            if attempt == 3:
                raise
    tmp.replace(exe)
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    return exe


def denoise(media: Path, cfg: dict | None = None) -> Path:
    """Return a cleaned 48 kHz mono WAV of the media's audio (cached)."""
    cfg = cfg or load_config()
    d = cfg["audio"]["denoise"]
    WORK.mkdir(parents=True, exist_ok=True)
    out_dir = WORK / "clean"
    out_dir.mkdir(exist_ok=True)
    stem = f"{media.stem}.{int(media.stat().st_mtime)}.a{d['strength_db']}"
    raw, clean = WORK / f"{stem}.wav", out_dir / f"{stem}.wav"
    if clean.exists():
        return clean
    run([ffmpeg_bin(), "-y", "-i", media, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", raw])
    # -D keeps the audio in sync (compensates model delay); -a limits how hard noise is cut,
    # so the voice stays natural instead of "underwater".
    run([ensure_binary(), "-D", "-a", str(d["strength_db"]), "-o", out_dir, raw])
    raw.unlink(missing_ok=True)
    return clean


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(denoise(Path(sys.argv[1])))
