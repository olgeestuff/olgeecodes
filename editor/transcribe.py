"""Word-level transcription with faster-whisper (free, runs locally).

Usage:  python editor/transcribe.py "AI video editors/raw footage/video 1 narration.mp4"
Writes <file>.words.json next to the work copy and prints the text.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from common import WORK, ffmpeg_bin, load_config

_model = None


def _get_model(name: str):
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        print(f"  loading whisper model '{name}' (first run downloads it)...")
        _model = WhisperModel(name, device="cpu", compute_type="int8")
    return _model


def _load_audio(media: Path):
    """Decode to 16 kHz mono float32 with ffmpeg (avoids PyAV version issues)."""
    import subprocess

    import numpy as np
    raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", str(media), "-f", "s16le", "-ac", "1",
                          "-ar", "16000", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def transcribe(media: Path, cache: bool = True, prompt: str | None = None) -> list[dict]:
    """Return [{word, start, end}] for the media file. Cached by file name + mtime."""
    cfg = load_config()["captions"]
    WORK.mkdir(parents=True, exist_ok=True)
    import hashlib
    tag = hashlib.md5((prompt or "").encode()).hexdigest()[:6]
    key = f"{media.stem}.{int(media.stat().st_mtime)}.{tag}.words.json"
    out = WORK / key
    if cache and out.exists():
        return json.loads(out.read_text(encoding="utf-8"))

    # WHISPER_MODEL_DIR lets you point at a local model folder (offline machines).
    model = _get_model(os.environ.get("WHISPER_MODEL_DIR") or cfg["model"])
    audio = _load_audio(media)

    def run_once(**extra):
        segs, _ = model.transcribe(audio, language=cfg.get("language"), word_timestamps=True,
                                   vad_filter=True, **extra)
        return [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
                for seg in segs for w in (seg.words or []) if w.word.strip()]

    # The script is passed as "hotwords" (biases spelling: "lease" not "visa") rather than as an
    # initial prompt, which can make Whisper skip speech that matches the prompt.
    words = run_once(hotwords=prompt) if prompt else run_once()
    if prompt:
        plain = run_once()
        if len(words) < 0.85 * len(plain):     # safety net: never lose speech because of the prompt
            print("  note: script hint dropped words; using plain transcription")
            words = plain
    out.write_text(json.dumps(words, indent=1), encoding="utf-8")
    return words


def words_to_text(words: list[dict]) -> str:
    return " ".join(w["word"] for w in words)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ws = transcribe(Path(sys.argv[1]))
    print(words_to_text(ws))
