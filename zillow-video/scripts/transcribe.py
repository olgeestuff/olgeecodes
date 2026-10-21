"""Word-level transcript of the voice recording with faster-whisper.

usage: python -I scripts/transcribe.py <model_dir> <audio.wav> <out.json>
"""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

model_dir, audio, out = sys.argv[1:4]
# Decode with ffmpeg to 16 kHz mono float32 (avoids PyAV version mismatches).
pcm = subprocess.run(
    ["ffmpeg", "-loglevel", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
    check=True, capture_output=True,
).stdout
samples = np.frombuffer(pcm, dtype=np.float32)
model = WhisperModel(model_dir, device="cpu", compute_type="int8", cpu_threads=4)
# The prompt nudges spelling of domain terms and keeps fillers (um/uh) so they can be cut.
prompt = (
    "Umm, so, uh, in 2023 a client reached out. Zillow, Singapore, Singaporean, HDB, URA, "
    "AppSheet, Google Sheets, landed, non-landed, retail, office, industrial. Uh, like, you know."
)
segments, info = model.transcribe(
    samples,
    language="en",
    beam_size=5,
    word_timestamps=True,
    condition_on_previous_text=False,
    initial_prompt=prompt,
)
data = []
for seg in segments:
    words = [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for w in seg.words]
    data.append({"s": round(seg.start, 3), "e": round(seg.end, 3), "text": seg.text, "words": words})
    print(f"[{seg.start:7.2f} -> {seg.end:7.2f}] {seg.text}", flush=True)
json.dump({"duration": info.duration, "segments": data}, open(out, "w"), indent=1)
