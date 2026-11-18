"""Original spy-style music bed (composed from scratch, royalty-free).
Not the James Bond theme: different key, rhythm, bassline and melody.
"""
import numpy as np, wave, sys

SR = 44100
BPM = 120
BEAT = 60 / BPM
DUR = 12.0
out = np.zeros(int(SR * (DUR + 1)))

def hz(n):  # MIDI note -> Hz
    return 440 * 2 ** ((n - 69) / 12)

def env(n, a=0.005, r=0.08):
    e = np.ones(n)
    ai, ri = int(SR * a), int(SR * r)
    e[:ai] = np.linspace(0, 1, ai)
    if ri < n:
        e[-ri:] *= np.linspace(1, 0, ri)
    return e

def add(sig, t):
    i = int(t * SR)
    out[i:i + len(sig)] += sig[: len(out) - i]

def bass(note, t, length):
    n = int(SR * length); x = np.arange(n) / SR; f = hz(note)
    s = np.sin(2*np.pi*f*x) + 0.4*np.sin(2*np.pi*2*f*x) + 0.15*np.sin(2*np.pi*3*f*x)
    add(0.35 * s * env(n, 0.003, 0.05) * np.exp(-x * 2.5), t)

def guitar(note, t, length):  # twangy tremolo-ish pluck
    n = int(SR * length); x = np.arange(n) / SR; f = hz(note)
    s = sum(np.sin(2*np.pi*f*k*x) / k**1.3 for k in range(1, 7))
    trem = 0.75 + 0.25 * np.sin(2*np.pi*9*x)
    add(0.16 * s * trem * env(n, 0.002, 0.1) * np.exp(-x * 1.8), t)

def brass(notes, t, length):  # stab chord
    n = int(SR * length); x = np.arange(n) / SR
    s = np.zeros(n)
    for nt in notes:
        f = hz(nt)
        for d in (-0.15, 0.15):
            ph = 2*np.pi*f*(1+d/100)*x
            s += sum(np.sin(k*ph)/k for k in range(1, 9)) * 0.5
    add(0.06 * s * env(n, 0.02, 0.15), t)

def drums(t, kind):
    n = int(SR * 0.25); x = np.arange(n) / SR
    if kind == "k":
        s = np.sin(2*np.pi*(55 + 90*np.exp(-x*30))*x) * np.exp(-x*12)
        add(0.5 * s, t)
    elif kind == "h":
        s = np.random.randn(n) * np.exp(-x*60)
        add(0.05 * s, t)
    elif kind == "s":
        s = (np.random.randn(n)*0.6 + np.sin(2*np.pi*190*x)) * np.exp(-x*18)
        add(0.18 * s, t)

np.random.seed(7)
# G minor. Bass ostinato (original): G G Bb C | Db C Bb F
ost = [43, 43, 46, 48, 49, 48, 46, 41]
bars = int(DUR / (4 * BEAT))
for b in range(bars):
    t0 = b * 4 * BEAT
    for i, nt in enumerate(ost):
        bass(nt, t0 + i * BEAT / 2, BEAT / 2 * 0.9)
    for i in range(8):
        drums(t0 + i * BEAT / 2, "h")
    if b >= 1:
        drums(t0, "k"); drums(t0 + 2 * BEAT, "k")
        drums(t0 + BEAT, "s"); drums(t0 + 3 * BEAT, "s")

# Guitar melody (original) from bar 2
mel = [(67,0,.5),(70,.5,.5),(74,1,1),(72,2,.5),(70,2.5,.5),(69,3,1),
       (67,4,.5),(70,4.5,.5),(75,5,1.5),(74,6.5,1.5)]
for rep in (1, 3):
    for nt, st, ln in mel:
        guitar(nt, rep * 4 * BEAT + st * BEAT, ln * BEAT)

# Brass stabs
for b in (2, 4):
    brass([55, 58, 62, 65], b * 4 * BEAT + 3.5 * BEAT, 0.35)
# Final hit: Gm(add9) swell
brass([43, 55, 58, 62, 69], 11.0, 1.9)
drums(11.0, "k")

# master: gentle fade-in, normalize, fade-out
out = out[: int(SR * DUR)]
out[: int(SR * .3)] *= np.linspace(0, 1, int(SR * .3))
out[-int(SR * .6):] *= np.linspace(1, 0, int(SR * .6))
out = np.tanh(out * 1.4)
out = out / np.max(np.abs(out)) * 0.89
pcm = (out * 32767).astype(np.int16)
stereo = np.column_stack([pcm, pcm]).ravel()
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(stereo.tobytes())
