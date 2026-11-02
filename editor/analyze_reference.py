"""Break a style-reference video into data Claude can read to write the style guide.

  python editor/analyze_reference.py "AI video editors/references/kallaway.mp4"

Creates references/analysis/<name>/ with:
  cuts.txt          every scene-cut timestamp + average shot length
  contact_*.png     contact sheets: one frame every 0.5 s, timestamped
  shot_*.png        one full-size frame per shot (layout / caption / graphic detail)
  words.json        transcript with word timings (caption pacing, words per second)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from common import REFS, duration, ffmpeg_bin, run
from transcribe import transcribe


def main(src: Path) -> None:
    out = REFS / "analysis" / src.stem
    out.mkdir(parents=True, exist_ok=True)
    ff = ffmpeg_bin()
    total = duration(src)

    # scene cuts
    res = run([ff, "-hide_banner", "-i", src, "-vf", "select='gt(scene,0.25)',showinfo", "-an",
               "-f", "null", "-"])
    cuts = [float(l.split("pts_time:")[1].split()[0]) for l in res.stderr.splitlines() if "pts_time:" in l]
    shots = [0.0] + cuts + [total]
    lens = [b - a for a, b in zip(shots, shots[1:])]
    (out / "cuts.txt").write_text(
        f"duration {total:.2f}s | cuts {len(cuts)} | avg shot {sum(lens) / len(lens):.2f}s\n"
        + "\n".join(f"{t:7.2f}s" for t in cuts), encoding="utf-8")

    # contact sheets (0.5 s grid, 5x4 per sheet, timestamped)
    run([ff, "-y", "-i", src, "-vf",
         "fps=2,scale=216:-2,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,"
         "tile=5x4:padding=4", "-an", out / "contact_%02d.png"])
    # one frame per shot
    for i, (a, b) in enumerate(zip(shots, shots[1:])):
        run([ff, "-y", "-ss", f"{(a + b) / 2:.2f}", "-i", src, "-frames:v", "1", "-vf", "scale=540:-2",
             out / f"shot_{i:02d}_{a:05.1f}s.png"])

    words = transcribe(src, cache=False)
    (out / "words.json").write_text(json.dumps(words, indent=1), encoding="utf-8")
    wps = len(words) / max(total, 1)
    print(f"done -> {out}\n  {len(cuts)} cuts, avg shot {sum(lens) / len(lens):.2f}s, {wps:.1f} words/s")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
