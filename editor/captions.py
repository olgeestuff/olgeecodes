"""Kallaway-style word captions: short bold lines, current word highlighted, pop-in.

Builds an .ass subtitle file from word timestamps. Caption position follows the layout:
on the split line during split screen, lower third when A-roll is full screen.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from common import hex_to_ass

SENTENCE_END = (".", "?", "!")
BREAK_AFTER = SENTENCE_END + (",", ":", ";", "…")


def _ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def group_words(words: list[dict], per_line: int) -> list[list[dict]]:
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["start"] - w["end"]) if nxt else 0
        if (len(cur) >= per_line or w["word"].endswith(BREAK_AFTER) or gap > 0.45
                or len(" ".join(x["word"] for x in cur)) > 18):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


CASE_FIX = {"i": "I", "i'll": "I'll", "i'm": "I'm", "i've": "I've", "i'd": "I'd", "ai": "AI"}


def _clean(word: str, upper: bool) -> str:
    w = word.replace("{", "").replace("}", "").replace("\\", "")
    core = w.strip(".,!?;:")
    if core.lower() in CASE_FIX:
        w = w.replace(core, CASE_FIX[core.lower()])
    w = w.rstrip(",;:")
    return w.upper() if upper else w


def build_ass(words: list[dict], out: Path, cfg: dict, width: int, height: int,
              layout_at: Callable[[float], str], split_y: int) -> Path:
    c = cfg["captions"]
    white = hex_to_ass(c["color"])
    hi = hex_to_ass(c["highlight_color"])
    outline = hex_to_ass(c["outline_color"])
    font = c["font"]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font},{c['size']},{white},{white},{outline},&H80000000,-1,0,0,0,100,100,0,0,1,{c['outline']},{c['shadow']},5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    groups = group_words(words, c["words_per_line"])
    for gi, g in enumerate(groups):
        g_start = g[0]["start"]
        nxt_start = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.4
        g_end = min(nxt_start, g[-1]["end"] + 0.35)
        mode = layout_at((g_start + g_end) / 2)
        y = split_y if mode == "split" and c.get("position", "split") == "split" else height - c["lower_margin"]
        for wi, w in enumerate(g):
            s = w["start"] if wi else g_start
            e = g[wi + 1]["start"] if wi + 1 < len(g) else g_end
            if e <= s:
                continue
            parts = []
            for wj, x in enumerate(g):
                txt = _clean(x["word"], c["uppercase"])
                parts.append(f"{{\\c{hi}}}{txt}{{\\c{white}}}" if wj == wi else txt)
            pop = ""
            if wi == 0:
                p = c["pop_scale"]
                pop = f"\\fscx{p}\\fscy{p}\\t(0,90,\\fscx100\\fscy100)"
            lines.append(f"Dialogue: 0,{_ts(s)},{_ts(e)},Cap,,0,0,0,,{{\\an5\\pos({width // 2},{y}){pop}}}"
                         + " ".join(parts))
    out.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return out
