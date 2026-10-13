#!/usr/bin/env python3
"""voices.py — the crowd's raw lines from Kokoro (local TTS). Run with the Kokoro venv:
    ~/.cache/kokoro/venv/bin/python sound/voices.py sound/vo
Foreground shouts (one per on-screen word) and a bed of overlapping crowd lines. score.py shapes them into shouting."""
import os, sys, json
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from scipy.signal import resample_poly

out = sys.argv[1] if len(sys.argv) > 1 else "vo"; os.makedirs(out, exist_ok=True)
K = os.path.expanduser("~/.cache/kokoro"); tts = Kokoro(os.path.join(K, "kokoro-v1.0.onnx"), os.path.join(K, "voices-v1.0.bin"))

# the four shouts the picture shows, in order
FG = [("I'm next!", "am_fenrir", 1.15), ("No! I'm next!", "af_nicole", 1.2), ("I was here first!", "am_onyx", 1.2), ("Where's the queue?!", "af_bella", 1.15)]
# the crowd underneath: many voices, short lines
BED_LINES = ["I'm next!", "No, I'm next!", "Hey!", "Move!", "Excuse me!", "It's my turn!", "I was here first!", "Who's next?",
             "Where's the queue?", "Stop pushing!", "Me! Me!", "Wait!", "Come on!", "Oya, I'm next!", "Abeg, I'm next!", "Get in line!"]
BED_VOICES = ["am_adam", "am_michael", "am_eric", "am_liam", "am_puck", "bm_george", "bm_lewis", "bm_daniel",
              "af_sarah", "af_sky", "af_jessica", "af_river", "bf_emma", "bf_isabella", "bf_lily", "af_kore"]

def say(text, voice, speed, lang="en-us"):
    s, sr = tts.create(text, voice=voice, speed=speed, lang=lang)
    s = resample_poly(s, 48000, sr) if sr != 48000 else s
    idx = np.where(np.abs(s) > 0.01)[0]
    return s[max(0, idx[0] - 240): idx[-1] + 1200] if len(idx) else s

meta = {"fg": [], "bed": []}
for i, (txt, v, sp) in enumerate(FG):
    s = say(txt, v, sp, "en-gb" if v.startswith("b") else "en-us"); p = f"{out}/fg{i}.wav"; sf.write(p, s, 48000); meta["fg"].append({"file": p, "text": txt, "voice": v, "dur": len(s) / 48000})
r = np.random.default_rng(11)
for j in range(30):
    txt = BED_LINES[j % len(BED_LINES)]; v = BED_VOICES[(j * 5) % len(BED_VOICES)]; sp = float(1.1 + 0.3 * r.random())
    s = say(txt, v, sp, "en-gb" if v.startswith("b") else "en-us"); p = f"{out}/bed{j:02d}.wav"; sf.write(p, s, 48000); meta["bed"].append({"file": p, "text": txt, "voice": v, "dur": len(s) / 48000})
json.dump(meta, open(f"{out}/voices.json", "w"), indent=1)
print("fg:", [(m["text"], round(m["dur"], 2)) for m in meta["fg"]]); print("bed:", len(meta["bed"]), "lines")
