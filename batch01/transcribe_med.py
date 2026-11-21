import sys, json, glob, os, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
for f in sorted(glob.glob(sys.argv[1] + "/*.mp4")):
    pcm = subprocess.run(["ffmpeg","-loglevel","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(audio, word_timestamps=True, vad_filter=True)
    words, text = [], []
    for s in segs:
        text.append(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
        words += [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2)} for w in s.words]
    base = os.path.join(sys.argv[2], os.path.basename(f)[:-4])
    open(base + ".txt", "w").write("\n".join(text))
    json.dump(words, open(base + ".words.json", "w"))
    print("=====", os.path.basename(f)); print("\n".join(text))
