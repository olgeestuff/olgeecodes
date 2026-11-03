"""Pull AI-generated clips (Gemini Veo, Canva, etc.) from the shared Drive "veo vids" folder.

  python editor/fetch_veo.py                -> downloads new clips into "AI video editors/raw footage/veo/"
The folder is shared "anyone with the link", so no API key is needed (uses gdown).
Name clips like "hook 7 veo scene 1.mp4" so plans can reference them:
    file: raw footage/veo/hook 7 veo scene 1.mp4
"""
from __future__ import annotations

import sys

import gdown

from common import RAW

VEO_FOLDER = "1okvCi-dcKvf_lUPJNGjDYNig93jZhpQw"   # teleprompter vids on office geek / veo vids


def main(folder: str = VEO_FOLDER) -> None:
    out = RAW / "veo"
    out.mkdir(parents=True, exist_ok=True)
    files = gdown.download_folder(id=folder, output=str(out), quiet=True, skip_download=True) or []
    for f in files:
        dest = out / f.path
        if dest.exists():
            continue
        print(f"  downloading {f.path}")
        gdown.download(id=f.id, output=str(dest), quiet=True)
    print(f"done: {len(files)} file(s) in the folder -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else VEO_FOLDER)
