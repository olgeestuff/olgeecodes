#!/usr/bin/env python3
"""score.py — the dq film's sound, placed from the comp's own events (sound/events.json).

    python3 sound/dump_events.py comp.html && python3 sound/score.py      # → sound/sfx.wav

Three buses:
  crowd  Kokoro lines shaped into shouting (pitched up, driven, presence), a bed of ~30 overlapping voices plus
         the four on-screen shouts, in a small room — gated to silence on the tap that freezes the picture.
  sfx    the onetake palette (wood, sub, air, bubble, glass) in one room: the card landing, keys, the tap, the
         names landing on a rising pentatonic, the dive, the dq landing.
  music  a restrained synthesised pad that enters as the line forms (C → Am → F → G → C), low-mids kept thin.
Master: -16 LUFS integrated, sample peak under -4 dBFS so the AAC render stays under verify's -3.
"""
import json, os, sys
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "onetake", "scripts"))
from sfx_palette import SR, air, glass, wood, sub, bubble, bp, lp, hp, sat, impulse

EV = json.load(open(os.path.join(HERE, "events.json")))
DUR = EV["T"]; E = EV["events"]
VO = json.load(open(os.path.join(HERE, "vo", "voices.json")))
first = lambda k: next(e for e in E if e["kind"] == k)
TAP1 = first("tap_freeze")["t"]; SNAP = first("open")["t"]; BLUE = first("blue")["t"]; QLAND = first("q_land")["t"]
TAP2 = first("tap")["t"]; HOLD0, HOLD1 = 6.25, 7.95
rng = np.random.default_rng(2026)
N = int(SR * (DUR + 2))


class Bus:
    def __init__(self, T60): self.dry = np.zeros((N, 2)); self.wet = np.zeros((N, 2)); self.T60 = T60
    def place(self, sig, t, gain=1.0, pan=0.0, send=0.25, pan_to=None):
        sig = np.asarray(sig, float); i0 = int(round(t * SR))
        if i0 < 0: sig = sig[-i0:]; i0 = 0
        n = min(len(sig), N - i0); sig = sig[:n]
        p = np.linspace(pan, pan if pan_to is None else pan_to, n); L = np.sqrt(0.5 * (1 - p)); R = np.sqrt(0.5 * (1 + p))
        for c, g in ((0, L), (1, R)): self.dry[i0:i0 + n, c] += sig * gain * g; self.wet[i0:i0 + n, c] += sig * gain * send * g
    def render(self, wet=0.9):
        ir = impulse(self.T60)
        rev = np.stack([signal.fftconvolve(self.wet[:, c], ir[:, c])[:N] for c in (0, 1)], 1)
        return self.dry + rev * wet


def load(p):
    x, sr = sf.read(p if os.path.isabs(p) else os.path.join(HERE, "..", p)); return x if x.ndim == 1 else x.mean(1)


def shout(x, pitch=1.08, drive=2.6, presence=0.9):
    """read speech → shouted: up a little in pitch and pace, driven into saturation, a forward 2–3.5 kHz edge"""
    up, dn = int(round(pitch * 100)), 100
    x = resample_poly(x, dn, up)                             # fewer samples at the same rate: faster and higher
    x = hp(x, 170); x = x + presence * bp(x, 2900, 1.4) + 0.4 * bp(x, 1200, 1.2)
    x = sat(x / (np.abs(x).max() + 1e-9) * drive, 1.0); x = lp(x, 7200)
    f = int(0.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x / (np.abs(x).max() + 1e-9)


# ─────────────────────────────── crowd ───────────────────────────────
crowd = Bus(0.65)
bed = [shout(load(m["file"]), pitch=float(rng.uniform(1.03, 1.14)), drive=float(rng.uniform(2.0, 3.2))) for m in VO["bed"]]
for i, x in enumerate(bed):                                  # the bed: overlapping voices from before the first frame to the tap
    t = -0.25 + (TAP1 + 0.1) * i / len(bed) + float(rng.uniform(-0.12, 0.12))
    crowd.place(x, t, gain=float(rng.uniform(0.10, 0.20)), pan=float(rng.uniform(-0.75, 0.75)), send=0.45)
# babble underneath: noise shaped into syllables at 4–7 Hz, so the room is full between the words
n = int(SR * (TAP1 + 0.3)); tt = np.arange(n) / SR
bab = np.zeros(n)
for k in range(6):
    syl = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(3.8, 7.0) * tt + rng.uniform(0, 6.28)) ** 2
    bab += bp(rng.standard_normal(n), rng.uniform(450, 1300), 2.2) * syl
bab = lp(bab, 2600); bab /= np.abs(bab).max()
crowd.place(bab, 0.0, gain=0.10, pan=0.0, send=0.6)
# the four shouts the picture shows
for e in [e for e in E if e["kind"] == "shout"]:
    x = shout(load(VO["fg"][e["i"]]["file"]), pitch=[1.09, 1.12, 1.06, 1.1][e["i"]], drive=3.0, presence=1.1)
    crowd.place(x, max(0.0, e["t"]) + 0.02, gain=0.62, pan=e["pan"], send=0.3)
cm = crowd.render(wet=0.8)
gate = np.ones(N); i0, i1 = int(TAP1 * SR), int((TAP1 + 0.06) * SR)
gate[i0:i1] = np.linspace(1, 0, i1 - i0); gate[i1:] = 0       # the tap: the room goes silent
cm *= gate[:, None]
f0 = int(0.03 * SR); cm[:f0] *= np.linspace(0, 1, f0)[:, None]

# ─────────────────────────────── sfx ───────────────────────────────
fx = Bus(1.1)
PENTA = [523.3, 587.3, 659.3, 784.0, 880.0, 1046.5, 1174.7, 1318.5]
for e in E:
    k, t, p, v = e["kind"], e["t"], e["pan"], e["v"]
    if k == "shout": fx.place(sub(52, 0.55), t, 0.32, p * 0.5, 0.2); fx.place(wood(110, 0.12), t, 0.22, p, 0.3)
    elif k == "bar_in": fx.place(air(0.34, 2200, 380, 1.2, 0.25), t - 0.2, 0.26, 0, 0.4); fx.place(bubble(360, 0.3), t + 0.05, 0.34, 0, 0.3); fx.place(wood(140, 0.1), t + 0.06, 0.26, 0, 0.2)
    elif k == "key":
        if t < 5 or int(round(t * 30)) % 2 == 0: fx.place(wood(float(rng.uniform(190, 260)), 0.06), t, 0.13 * v, p, 0.15)
    elif k == "tap_freeze":
        fx.place(wood(240, 0.08), t - 0.01, 0.46, p, 0.2); fx.place(wood(190, 0.07), t + 0.06, 0.3, p, 0.2); fx.place(sub(44, 1.3), t, 0.5, 0, 0.35)
    elif k == "lift": fx.place(air(0.44, 500, 2600, 1.3, 0.5), t, 0.24, -0.1, 0.45, pan_to=0.05)
    elif k == "open": fx.place(air(0.75, 180, 900, 1.1, 0.3), t, 0.24, 0, 0.5)
    elif k == "land":
        fx.place(glass(PENTA[e["i"]], 1.0, 0.55), t, 0.15 if e["i"] else 0.2, p * 0.7, 0.45); fx.place(wood(200, 0.07), t, 0.12, p, 0.15)
    elif k == "pill": fx.place(bubble(640, 0.22), t + 0.03, 0.2, 0.2, 0.3)
    elif k == "push": fx.place(air(0.5, 260, 1400, 1.2, 0.5), t, 0.16, 0, 0.5)
    elif k == "tap": fx.place(wood(240, 0.08), t - 0.01, 0.42, p, 0.2); fx.place(wood(190, 0.07), t + 0.06, 0.28, p, 0.2)
    elif k == "out": fx.place(air(0.3, 1200, 3600, 1.4, 0.3), t, 0.2, -0.3, 0.4, pan_to=-0.7)
    elif k == "shift": fx.place(glass(784, 0.9, 0.5), t + 0.12, 0.12, 0, 0.5); fx.place(wood(160, 0.1), t + 0.1, 0.14, 0, 0.2)
    elif k == "dive": fx.place(air(e["dur"] + 0.05, 160, 6500, 1.0, 0.88), t, 0.5, 0, 0.35)
    elif k == "blue": fx.place(sub(46, 1.6), t, 0.5, 0, 0.4)
    elif k == "d_drop": fx.place(sub(58, 0.8), t + 0.07, 0.44, -0.1, 0.3); fx.place(wood(150, 0.1), t + 0.07, 0.3, -0.1, 0.25)
    elif k == "flip": fx.place(air(e["dur"] + 0.05, 320, 2400, 1.2, 0.6), t, 0.26, -0.05, 0.45, pan_to=0.15)
    elif k == "q_land":
        fx.place(sub(50, 1.0), t, 0.5, 0.1, 0.35); fx.place(wood(170, 0.12), t, 0.36, 0.12, 0.25); fx.place(glass(1046.5, 1.6, 0.6), t + 0.01, 0.15, 0.1, 0.55)
    elif k == "url_in": fx.place(bubble(520, 0.24), t + 0.04, 0.28, 0, 0.3)
    elif k == "free": fx.place(glass(1568, 1.0, 0.4), t + 0.04, 0.07, 0, 0.55)
fm = fx.render()

# ─────────────────────────────── music: a pad that arrives with the line ───────────────────────────────
def pad(freqs, dur, att=0.35, rel=0.5, cut=1500):
    n = int(SR * (dur + rel)); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for d in (-0.0035, 0.0, 0.0035):                    # three slightly detuned saws per note
            ph = 2 * np.pi * f * (1 + d) * t + rng.uniform(0, 6.28); x += (2 * ((ph / (2 * np.pi)) % 1) - 1) / 3
    x = lp(lp(x, cut), cut); env = np.minimum(1, t / att) * np.where(t > dur, np.exp(-(t - dur) / (rel / 3)), 1)
    return x * env / len(freqs)
def bass(f, dur):
    n = int(SR * (dur + 0.3)); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.08) * np.exp(-t * 0.9) * np.where(t > dur, np.exp(-(t - dur) * 12), 1)
CH = [  # (start, end, pad notes ≥ G3 to keep the low-mids clear, bass root)
    (SNAP, HOLD0 + 0.6, [196.0, 246.9, 293.7, 329.6, 493.9], 65.4),     # C maj9
    (HOLD0 + 0.6, TAP2, [196.0, 261.6, 329.6, 392.0], 55.0),             # A min7
    (TAP2, BLUE, [220.0, 261.6, 329.6, 349.2, 440.0], 43.7),             # F maj7
    (BLUE, QLAND, [196.0, 246.9, 293.7, 392.0, 440.0], 49.0),            # G6/9
    (QLAND, DUR + 0.5, [196.0, 261.6, 329.6, 392.0, 493.9, 587.3], 65.4),  # C maj9, held to the end
]
mus = Bus(1.6)
for i, (a, b, notes, root) in enumerate(CH):
    mus.place(pad(notes, b - a + 0.1, att=0.5 if i == 0 else 0.18, cut=1700 if i < 4 else 2200), a, 0.5, 0, 0.5)
    mus.place(bass(root, b - a), a, 0.22, 0, 0.1)
mm = mus.render(wet=0.7)
fade = np.ones(N); e0 = int((DUR - 0.5) * SR); fade[e0:] = np.linspace(1, 0, N - e0) ** 1.5
mm *= fade[:, None]

# ─────────────────────────────── master ───────────────────────────────
mix = cm * 0.55 + fm * 1.6 + mm * 1.0
mix = np.stack([hp(mix[:, c], 35) for c in (0, 1)], 1)[: int(SR * DUR)]
meter = pyln.Meter(SR)
mix *= 10 ** ((-16 - meter.integrated_loudness(mix)) / 20)
mix = np.tanh(mix * 1.15) / 1.15                               # soft ceiling for the few peaks above it
pk = 20 * np.log10(np.abs(mix).max())
if pk > -4.0: mix *= 10 ** ((-4.0 - pk) / 20)
out = os.path.join(HERE, "sfx.wav"); sf.write(out, mix, SR, subtype="PCM_16")
lu = meter.integrated_loudness(mix); pk = 20 * np.log10(np.abs(mix).max())
print(f"{out}: {DUR:.1f} s, {lu:.1f} LUFS, peak {pk:.1f} dBFS")
# loudness by beat, K-weighted — the landing must read louder than the move into it
for name, a, b in [("crowd", 0.0, TAP1), ("freeze", TAP1 + 0.1, SNAP), ("line forms", SNAP, 6.0), ("hold", HOLD0, HOLD1),
                   ("next person", 8.4, 9.4), ("dive", 9.85, BLUE), ("dq", 11.3, 12.8), ("url", 12.8, DUR)]:
    seg = mix[int(a * SR):int(b * SR)]
    try: l = meter.integrated_loudness(seg) if len(seg) > SR * 0.4 else float('nan')
    except Exception: l = float('nan')
    print(f"  {name:12s} {a:5.2f}–{b:5.2f}  {l:6.1f} LUFS   peak {20 * np.log10(np.abs(seg).max() + 1e-9):6.1f} dBFS")
