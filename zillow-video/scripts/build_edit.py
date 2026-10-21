"""Cut and reorder the voice recording, then emit the caption/cue timeline for Remotion.

usage: python -I scripts/build_edit.py <source.wav> <words.json> <public/audio/voice.wav> <src/data/edit.json>

words.json is the output of scripts/transcribe.py; indices below refer to its words in order.
Cut points are snapped to quiet spots in the audio because Whisper word boundaries drift
by ~0.1-0.2 s; long pauses inside kept phrases are tightened.
"""
import json
import subprocess
import sys

import numpy as np

SR = 48000

# Edit decision list: section -> kept word ranges (inclusive indices into words.json), in play order.
EDL = [
    ("hook", [(561, 568), (41, 43), (47, 54)]),  # "making a Zillow alternative for a Singaporean client" / "back in 2023" / "somebody reached out to me on social media"
    ("ask", [(55, 81)]),  # "and talked about his desires to manage properties ... whatever type it is"
    ("wrong", [(166, 187), (190, 207)]),  # "I knew ... commercial residential. I didn't know it's a lot deeper ... indeed residential" / "there was private non-landed, HDB ... one-buildings"
    ("search", [(252, 259), (267, 275), (279, 291)]),  # "the most interesting thing he wanted was" / "filters ... for rent or sale" / "building name, district ... area, availability"
    ("wall", [(353, 356), (363, 377), (379, 385)]),  # "the only challenge was" / "to get data so he needs to scrape ... database" / "and that's where I couldn't do it"
    ("twist", [(485, 503), (505, 516)]),  # "so that's the quick story of my failure ... because the person" / "used it for his team and I got something out of it"
    ("today", [(388, 394), (395, 400), (403, 408), (411, 428)]),  # "nowadays, you know, that's not an issue" / "just get the data from somewhere" / "and put it in your Sheets" / "use your AppSheet ... spin yourself a directory now"
]

# Hand-checked cut points (seconds in the source) where Whisper's word edges were off; found from the
# energy envelope and confirmed by re-transcribing the cut. Keyed by a clip's first / last word index.
START_AT = {166: 71.15, 379: 164.12, 505: 225.52}
END_AT = {43: 20.04, 377: 163.90, 503: 224.54}

# Caption text fixes for Whisper mishearings (checked against isolated re-decodes). None drops the word.
FIX = {
    166: "All I",
    563: "Zillow",
    568: "client.",
    43: "2023,",
    195: "HDB,",
    197: "landed,",
    275: "sale,",
    370: "scrape",
    398: "data",
    413: "AppSheet",
    414: None,
    426: None,
    207: "-buildings.",
    174: "residential.",
    184: "that.",
    516: "it.",
    394: "issue.",
    390: "know,",
}

# Graphics sync points: cue name -> word index (time = that word's start on the edited timeline).
CUES = {
    "zillow": 563, "alternative": 564, "singapore": 567, "back": 41, "2023": 43, "client": 47, "social": 53,
    "manage": 61, "search": 73,
    "commercial": 173, "residential": 173, "wrong": 182,
    "nonlanded": 193, "hdb": 195, "landed": 196, "retail": 202, "office": 203, "industrial": 204, "buildings": 206,
    "searchby": 253, "rent": 273, "buildingname": 279, "district": 281, "price": 285, "area": 290, "availability": 291,
    "data": 365, "scraped": 370, "ura": 375,
    "failure": 492, "notfailure": 495, "team": 505,
    "today": 388, "notissue": 392, "data2": 397, "sheets": 408, "directory": 413, "spin": 423,
}

GAP_CLIP = 0.06  # silence between clips inside a section
GAP_SECTION = 0.22  # breath between sections
MAX_PAUSE = 0.30  # internal pauses longer than this are shortened to it
FADE = 0.012


def load(path):
    pcm = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(pcm, dtype=np.float32).copy()


def envelope(x, hop=0.005, win=0.025):
    h, w = int(hop * SR), int(win * SR)
    n = (len(x) - w) // h
    frames = np.lib.stride_tricks.sliding_window_view(x, w)[::h][:n]
    return 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9), hop


def quiet_zones(db, hop, thr, min_len=0.04):
    q = db < thr
    zones, start = [], None
    for i, v in enumerate(q):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if (i - start) * hop >= min_len:
                zones.append((start * hop, i * hop))
            start = None
    if start is not None:
        zones.append((start * hop, len(q) * hop))
    return zones


def snap_start(t, zones, db, hop, floor_t):
    # Quiet zone ending near the word start: cut just before speech resumes.
    # Never reach back before floor_t (end of the dropped word before this one).
    lo = max(t - 0.40, floor_t)
    cands = [z for z in zones if lo <= z[1] <= t + 0.15]
    if cands:
        z = min(cands, key=lambda z: abs(z[1] - t))
        return max(z[0], z[1] - 0.03, lo)
    a, b = int(max(t - 0.15, floor_t) / hop), int((t + 0.05) / hop)
    return (a + int(np.argmin(db[a:max(b, a + 1)]))) * hop


def snap_end(t, zones, db, hop, limit):
    cands = [z for z in zones if t - 0.15 <= z[0] <= min(t + 0.40, limit)]
    if cands:
        z = min(cands, key=lambda z: abs(z[0] - t))
        return min(z[1], z[0] + 0.06)
    a, b = int((t - 0.05) / hop), int(min(t + 0.15, limit) / hop)
    return (a + int(np.argmin(db[a:max(b, a + 1)]))) * hop


def main():
    src, words_path, out_wav, out_json = sys.argv[1:5]
    x = load(src)
    W = json.load(open(words_path))
    if isinstance(W, dict):
        W = [w for seg in W["segments"] for w in seg["words"]]
    db, hop = envelope(x)
    floor = np.percentile(db, 10)
    speech = np.percentile(db, 70)
    thr = floor + 0.35 * (speech - floor)
    zones = quiet_zones(db, hop, thr)
    print(f"noise floor {floor:.1f} dB, speech {speech:.1f} dB, quiet threshold {thr:.1f} dB, {len(zones)} quiet zones")

    out = []  # audio chunks
    pieces = []  # (src_a, src_b, dst_a) for time mapping
    sections = []
    t_dst = 0.0
    prev_j, prev_b = None, None
    starts = [i for _, clips in EDL for i, _ in clips]
    clip_no = 0
    for si, (sec, clips) in enumerate(EDL):
        sec_start = None
        for ci, (i, j) in enumerate(clips):
            # Clips that continue straight on in the source join at the same sample, with no gap.
            contiguous = prev_j is not None and i == prev_j + 1
            if prev_j is not None and not contiguous:
                gap = GAP_CLIP if ci else GAP_SECTION
                out.append(np.zeros(int(gap * SR), np.float32))
                t_dst += gap
            if sec_start is None:
                sec_start = t_dst
            nxt = W[j + 1]["s"] if j + 1 < len(W) else len(x) / SR
            floor_t = W[i - 1]["e"] - 0.05 if i else 0.0
            a = prev_b if contiguous else START_AT.get(i) or snap_start(W[i]["s"], zones, db, hop, floor_t)
            b = END_AT.get(j) or snap_end(W[j]["e"], zones, db, hop, limit=nxt + 0.03)
            prev_j, prev_b = j, b
            clip_no += 1
            next_contiguous = clip_no < len(starts) and starts[clip_no] == j + 1
            # Split the clip at long internal pauses and keep only MAX_PAUSE of each.
            spans, cur = [], a
            keep = MAX_PAUSE / 2
            for za, zb in zones:
                if zb - za <= MAX_PAUSE or zb >= b - 0.05 or zb <= a:
                    continue
                if za > a + 0.05:
                    spans.append((cur, za + keep))
                    cur = zb - keep
                elif contiguous:
                    # Silence carried over a seamless join: the previous clip already holds its start.
                    cur = max(cur, zb - keep)
            spans.append((cur, b))
            for k, (sa, sb) in enumerate(spans):
                chunk = x[int(round(sa * SR)):int(round(sb * SR))].copy()
                f = int(FADE * SR)
                if not (contiguous and k == 0):
                    chunk[:f] *= np.linspace(0, 1, f)
                if not (next_contiguous and k == len(spans) - 1):
                    chunk[-f:] *= np.linspace(1, 0, f)
                out.append(chunk)
                pieces.append((sa, sb, t_dst))
                t_dst += len(chunk) / SR
            print(f"{sec:7s} clip {i}-{j}: src {a:7.2f}-{b:7.2f}  ({len(spans)} spans)  -> ends {t_dst:6.2f}")
        sections.append({"id": sec, "s": round(sec_start, 3), "e": round(t_dst, 3)})
    # Sections tile the timeline: each ends where the next begins.
    for k in range(len(sections) - 1):
        sections[k]["e"] = sections[k + 1]["s"]

    raw = np.concatenate(out)
    raw_path = out_wav + ".raw.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", raw_path],
        input=raw.tobytes(), check=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", raw_path, "-af",
         "highpass=f=70,acompressor=threshold=-22dB:ratio=3:attack=5:release=90:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9",
         "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", out_wav],
        check=True,
    )
    subprocess.run(["rm", "-f", raw_path], check=True)

    def to_dst(t):
        for sa, sb, da in pieces:
            if sa - 1e-6 <= t <= sb + 1e-6:
                return da + (t - sa)
        # Word edge fell in a trimmed gap: clamp to the nearest kept piece edge.
        best = min(pieces, key=lambda p: min(abs(t - p[0]), abs(t - p[1])))
        return best[2] if abs(t - best[0]) < abs(t - best[1]) else best[2] + (best[1] - best[0])

    kept = [k for _, clips in EDL for i, j in clips for k in range(i, j + 1)]
    words = []
    for k in kept:
        text = FIX.get(k, W[k]["w"])
        s, e = to_dst(W[k]["s"]), to_dst(W[k]["e"])
        if text is None or (text.strip().startswith("-") and words):
            # Dropped words / hyphen fragments fold into the previous caption word.
            if words:
                words[-1]["e"] = round(e, 3)
                if text is not None:
                    words[-1]["w"] += text.strip()
            continue
        words.append({"w": text.strip(), "s": round(s, 3), "e": round(e, 3)})

    cues = {name: round(to_dst(W[k]["s"]), 3) for name, k in CUES.items()}
    voice = round(len(raw) / SR, 3)
    edit = {"fps": 30, "voice": voice, "endCard": 4.5, "words": words, "sections": sections, "cues": cues}
    json.dump(edit, open(out_json, "w"), indent=1)
    print(f"voice {voice:.2f}s + end card {edit['endCard']}s = {voice + edit['endCard']:.2f}s")
    print(" ".join(w["w"] for w in words))


if __name__ == "__main__":
    main()
