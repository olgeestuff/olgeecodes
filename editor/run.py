"""One command to edit a video from the raw footage folder.

  python editor/run.py "video 5"          -> one export per hook take
  python editor/run.py --all              -> every video that has a narration
  python editor/run.py "video 5" --hook 2 -> only hook 2

File naming in "AI video editors/raw footage/":
  video 5 hook 1.mp4     (any number of hook takes; optional)
  video 5 narration.mp4  (required — the main talking-head take)
  video 5 cta.mp4        (optional — if the CTA was recorded separately)
  video 5 demo.webm      (optional — Playwright demo; placeholder used if missing)
Exports land in "AI video editors/exports/video 5 - hook 1.mp4".
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from build_edit import render
from common import EXPORTS, RAW, VIDEO_EXT


def find(video: str) -> dict:
    files = [p for p in RAW.iterdir() if p.suffix.lower() in VIDEO_EXT]
    name = video.lower().strip()

    def pick(role: str) -> Path | None:
        for p in files:
            if p.stem.lower().strip() == f"{name} {role}":
                return p
        return None

    hooks = {}
    for p in files:
        m = re.fullmatch(rf"{re.escape(name)} hook ?(\d+).*", p.stem.lower().strip())
        if m:
            hooks[int(m.group(1))] = p
    return {"narration": pick("narration"), "cta": pick("cta"), "demo": pick("demo"),
            "hooks": dict(sorted(hooks.items()))}


def all_videos() -> list[str]:
    names = set()
    for p in RAW.iterdir():
        m = re.fullmatch(r"(video \d+) narration", p.stem.lower().strip())
        if m and p.suffix.lower() in VIDEO_EXT:
            names.add(m.group(1))
    return sorted(names, key=lambda s: int(s.split()[1]))


def edit(video: str, only_hook: int | None = None) -> list[Path]:
    f = find(video)
    if not f["narration"]:
        sys.exit(f'No "{video} narration" file in {RAW}. Check the file name.')
    body = [f["narration"]] + ([f["cta"]] if f["cta"] else [])
    if not f["demo"]:
        print(f'  note: no "{video} demo" found — using a placeholder for the top half.')
    hooks = f["hooks"] or {0: None}
    outs = []
    for n, hook in hooks.items():
        if only_hook is not None and n != only_hook:
            continue
        label = f"{video} - hook {n}" if hook else video
        print(f"\n=== {label} ===")
        outs.append(render(hook, body, f["demo"], EXPORTS / f"{label}.mp4"))
    return outs


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?", help='e.g. "video 5"')
    ap.add_argument("--hook", type=int, help="only render this hook number")
    ap.add_argument("--all", action="store_true", help="render every video with a narration")
    a = ap.parse_args()
    if a.all:
        for v in all_videos():
            edit(v)
    elif a.video:
        edit(a.video, a.hook)
    else:
        ap.print_help()
