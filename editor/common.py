"""Shared helpers: paths, config, ffmpeg/ffprobe wrappers."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
BASE = REPO / "AI video editors"
RAW = BASE / "raw footage"
REFS = BASE / "references"
EXPORTS = BASE / "exports"
WORK = BASE / ".work"          # intermediate files (gitignored)

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}


def load_config() -> dict:
    with open(Path(__file__).with_name("config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def ref_path(p: str) -> Path:
    """Resolve a config path relative to the AI video editors folder."""
    path = Path(p)
    return path if path.is_absolute() else BASE / path


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        sys.exit("ffmpeg not found. Install it (Windows: winget install Gyan.FFmpeg) and retry.")
    return exe


def run(cmd: list[str], quiet: bool = True) -> subprocess.CompletedProcess:
    if not quiet:
        print("  $", " ".join(str(c) for c in cmd))
    res = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        tail = "\n".join(res.stderr.strip().splitlines()[-25:])
        raise RuntimeError(f"Command failed ({cmd[0]}):\n{tail}")
    return res


def probe(path: Path) -> dict:
    res = run(["ffprobe", "-v", "error", "-print_format", "json",
               "-show_format", "-show_streams", path])
    return json.loads(res.stdout)


def duration(path: Path) -> float:
    return float(probe(path)["format"]["duration"])


def video_size(path: Path) -> tuple[int, int]:
    for s in probe(path)["streams"]:
        if s["codec_type"] == "video":
            w, h = int(s["width"]), int(s["height"])
            rot = int((s.get("tags") or {}).get("rotate", 0) or 0)
            for sd in s.get("side_data_list", []) or []:
                if "rotation" in sd:
                    rot = int(sd["rotation"])
            return (h, w) if abs(rot) in (90, 270) else (w, h)
    raise ValueError(f"No video stream in {path}")


def has_audio(path: Path) -> bool:
    return any(s["codec_type"] == "audio" for s in probe(path)["streams"])


def hex_to_ass(hex_color: str, alpha: str = "00") -> str:
    """#RRGGBB -> &HAABBGGRR (ASS colour)."""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha}{b}{g}{r}".upper()
