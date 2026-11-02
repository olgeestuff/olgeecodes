"""Work out which script each camera take belongs to, so files can be renamed to
"video N narration" / "video N hook K".

  python editor/match_scripts.py            -> prints a table (take -> best script, score)
Scripts are read from "raw footage/scripts/*.txt" (fetch_drive.py puts them there).
A script file with several "HOOK n - ..." sections is split into one entry per section.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from common import RAW, VIDEO_EXT
from transcribe import transcribe, words_to_text


def norm(text: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]|\([^)]*\)", " ", text.lower())
    return re.findall(r"[a-z0-9']+", text)


def load_scripts() -> dict[str, list[str]]:
    out = {}
    for p in sorted((RAW / "scripts").glob("*.txt")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        parts = re.split(r"\n(?=HOOK \d+\s*-)", txt)
        if len(parts) > 1:
            for part in parts:
                title = part.strip().splitlines()[0][:60]
                out[f"{p.stem} :: {title}"] = norm(part)
        else:
            out[p.stem] = norm(txt)
    return out


def score(a: list[str], b: list[str]) -> float:
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def main() -> None:
    scripts = load_scripts()
    if not scripts:
        raise SystemExit(f"No scripts in {RAW / 'scripts'} — run fetch_drive.py first.")
    takes = sorted(p for p in RAW.iterdir() if p.suffix.lower() in VIDEO_EXT)
    print(f"{'take':40} {'best script':60} score")
    for t in takes:
        spoken = norm(words_to_text(transcribe(t)))
        ranked = sorted(((score(spoken, s), name) for name, s in scripts.items()), reverse=True)
        best = ranked[0]
        print(f"{t.name[:40]:40} {best[1][:60]:60} {best[0]:.2f}  ({len(spoken)} words)")
    print("\nRename takes to the 'video N narration' / 'video N hook K' pattern, then run run.py.")


if __name__ == "__main__":
    main()
