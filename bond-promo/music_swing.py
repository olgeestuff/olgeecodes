"""Original big-band swing spy track: brass section, strings, walking bass,
ride cymbal, finger snaps, piano comping, minor-major 'spy chord' ending.
All melody, bassline and arrangement composed from scratch (royalty-free).
Usage: python3 music_swing.py <out.wav> <12|24>
"""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR, BPM = 44100, 120
B = 60 / BPM                      # one beat = 0.5s
SW = 2 / 3                        # swing offbeat position
OUT, LENGTH = sys.argv[1], int(sys.argv[2])
rng = np.random.default_rng(11)
TOTAL = LENGTH + 1.5
L = np.zeros(int(SR * TOTAL)); R = np.zeros_like(L)

def hz(n): return 440 * 2 ** ((n - 69) / 12)

def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR); n = min(len(sig), len(L) - i)
    if n <= 0: return
    L[i:i+n] += sig[:n] * gain * (1 - pan) / 2 * 2 ** .5
    R[i:i+n] += sig[:n] * gain * (1 + pan) / 2 * 2 ** .5

def adsr(n, a, d, s, r):
    e = np.full(n, s, float)
    ai, di, ri = int(a*SR), int(d*SR), int(r*SR)
    e[:ai] = np.linspace(0, 1, ai) if ai else e[:ai]
    e[ai:ai+di] = np.linspace(1, s, len(e[ai:ai+di]))
    if ri and ri < n: e[-ri:] *= np.linspace(1, 0, ri)
    return e

def filt(x, kind, f):
    return sosfilt(butter(2, f, kind, fs=SR, output="sos"), x)

# ---------------------------------------------------------------- instruments
def brass(note, t, ln, vel=1.0, bright=1.0, fall=False, pan=0.0):
    """Trumpet/trombone: additive saw with brightness that blooms on attack."""
    n = int(SR * (ln + 0.12)); x = np.arange(n) / SR
    f = np.full(n, hz(note))
    f *= 1 + 0.004 * np.clip((x - 0.25) * 3, 0, 1) * np.sin(2*np.pi*5.6*x)  # late vibrato
    if fall:
        k0 = int(SR * max(ln - 0.3, 0.05))
        f[k0:] *= 2 ** (-7/12 * np.linspace(0, 1, n - k0) ** 1.6)
    amp = adsr(n, 0.03, 0.12, 0.75, 0.1)
    if fall: amp[int(SR*max(ln-0.3,0.05)):] *= np.linspace(1, 0, n - int(SR*max(ln-0.3,0.05)))
    benv = 0.35 + 0.65 * adsr(n, 0.04, 0.25, 0.55, 0.1) * bright
    out = np.zeros(n)
    for det in (-7, 0, 6):                         # 3 players per part
        ph = 2*np.pi*np.cumsum(f * 2**(det/1200)) / SR + rng.uniform(0, 6.28)
        for k in range(1, 24):
            if hz(note) * k > 15000: break
            out += np.exp(-(k-1) / (1.2 + 7*benv)) * np.sin(k*ph) / k**0.35
    add(out * amp * vel * 0.05, t, pan)

def strings(notes, t, ln, vel=1.0):
    n = int(SR * (ln + 0.6)); x = np.arange(n) / SR
    out = np.zeros(n)
    for nt in notes:
        for det in (-9, -3, 4, 10):
            ph = 2*np.pi*hz(nt)*2**(det/1200)*x*(1+0.003*np.sin(2*np.pi*5*x+det))
            out += ((ph / (2*np.pi)) % 1 * 2 - 1)    # saw
    out = filt(out, "low", 2600) * adsr(n, 0.35, 0.2, 0.9, 0.6)
    add(out * vel * 0.012, t, -0.3)
    add(out * vel * 0.012, t + 0.011, 0.4)

def bass(note, t, ln=B*0.95):
    n = int(SR * ln); x = np.arange(n) / SR; f = hz(note)
    s = np.sin(2*np.pi*f*x) + 0.5*np.sin(4*np.pi*f*x)*np.exp(-x*8) + 0.2*np.sin(6*np.pi*f*x)*np.exp(-x*14)
    add(s * adsr(n, 0.004, 0.1, 0.6, 0.05) * np.exp(-x*1.6) * 0.32, t, 0.05)

def piano(notes, t, ln=0.22):
    n = int(SR * (ln + 0.3)); x = np.arange(n) / SR; out = np.zeros(n)
    for nt in notes:
        f = hz(nt)
        out += sum(np.sin(2*np.pi*f*k*x*(1+0.0004*k*k)) * np.exp(-x*(3+2*k)) / k for k in range(1, 7))
    out *= adsr(n, 0.002, 0.05, 0.8, 0.12)
    add(out * 0.035, t, 0.35)

def ride(t, accent=1.0):
    n = int(SR * 0.9); x = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*fr*x + p) for fr, p in ((3130,0),(4420,1),(5390,2),(6870,3),(8210,4)))
    s = filt(s * 0.3 + rng.standard_normal(n), "high", 4500) * np.exp(-x*5)
    add(s * 0.022 * accent, t, 0.45)

def snap(t):
    n = int(SR * 0.06); x = np.arange(n) / SR
    s = filt(rng.standard_normal(n), "band", [1400, 3600]) * np.exp(-x*90)
    add(s * 0.22, t, -0.5); add(s * 0.12, t + 0.004, 0.5)

def kick(t, g=1.0):
    n = int(SR * 0.3); x = np.arange(n) / SR
    add(np.sin(2*np.pi*(50 + 70*np.exp(-x*35))*x) * np.exp(-x*14) * 0.28 * g, t)

def timpani(note, t):
    n = int(SR * 2.2); x = np.arange(n) / SR; f = hz(note)
    s = sum(np.sin(2*np.pi*f*r*x) * np.exp(-x*(1.4+r)) / r for r in (1, 1.5, 1.99, 2.44))
    s += filt(rng.standard_normal(n), "low", 400) * np.exp(-x*20) * 0.5
    add(s * 0.45, t)

# ---------------------------------------------------------------- harmony
CH = {  # (walking bass line, piano voicing, strings voicing, brass shout voicing)
    "Cm":  ([36, 39, 43, 45], [63, 67, 70, 74], [60, 63, 67, 74], [63, 67, 70, 74, 79]),
    "Ab7": ([44, 48, 51, 42], [60, 66, 70, 72], [60, 63, 66, 70], [60, 66, 70, 72, 78]),
    "Fm7": ([41, 44, 48, 44], [60, 63, 67, 68], [56, 60, 63, 67], [63, 67, 68, 72, 75]),
    "G7":  ([43, 47, 50, 37], [59, 65, 70, 71], [59, 62, 65, 70], [59, 65, 70, 71, 77]),
}
MEL_A = [(72,0,.6),(75,SW,.35),(79,1,1.4),(77,2+SW,.33),(75,3,.6),(72,3+SW,.33)]
MEL_B = [(74,0,.9),(71,1,.6),(67,1+SW,1.3,True),(70,3,.6),(71,3+SW,.33)]
MEL_B2 = [(74,0,.9),(77,1,.6),(79,1+SW,2.2,True)]
TROMBONE_ANSWER = [(55,2,.3),(58,2+SW,.3),(60,3,.6)]

if LENGTH == 12:
    form = [("Cm","intro"),("Ab7","intro2"),("Fm7","melA"),("G7","melB"),("Cm","shout"),("END","end")]
else:
    form = [("Cm","intro"),("Ab7","intro2"),("Fm7","melA"),("G7","melB"),("Cm","shout"),("Ab7","shout"),
            ("Fm7","melA"),("G7","melB2"),("Cm","shout"),("Ab7","shout"),("G7","build"),("END","end")]

for bi, (ch, role) in enumerate(form):
    t0 = bi * 4 * B
    if ch == "END":
        # rising pickup, then the big minor-major 9 'spy chord' hit on beat 3
        for i, nt in enumerate([67, 70, 74]):
            brass(nt, t0 + i*SW*B, SW*B*0.9, vel=0.9)
        hit = t0 + 2*B
        for nt, pan in zip([48, 55, 59, 62, 63, 67, 71, 74], [-.4,-.3,-.1,.1,.2,.3,.4,.5]):
            brass(nt, hit, 1.9, vel=1.1, bright=1.2, pan=pan)
        strings([48, 55, 59, 62, 63, 71], hit, 1.9, vel=1.6)
        bass(24, hit, 1.8); bass(36, hit, 1.8); timpani(36, hit); kick(hit, 1.4)
        ride(hit, 1.6); piano([60, 63, 67, 71, 74], hit, 1.2)
        continue
    walk, pv, sv, shout = CH[ch]
    for i, nt in enumerate(walk): bass(nt, t0 + i*B)
    for beat in range(4):                       # ding, ding-a ding, ding-a
        ride(t0 + beat*B, 1.0 if beat % 2 else 0.8)
        if beat % 2: ride(t0 + (beat+SW)*B, 0.6); snap(t0 + beat*B)
        kick(t0 + beat*B, 0.35)
    strings(sv, t0, 4*B, vel=0.6 if role.startswith("intro") else 1.0)
    if role != "intro":
        piano(pv, t0); piano(pv, t0 + (1+SW)*B)  # Charleston comp
    if role == "intro2":
        brass(67, t0 + (3)*B, 0.3, 0.8); brass(70, t0 + (3+SW)*B, 0.3, 0.9)
    if role in ("melA", "melB", "melB2"):
        mel = {"melA": MEL_A, "melB": MEL_B, "melB2": MEL_B2}[role]
        for m in mel:
            nt, st, ln = m[:3]; fall = len(m) > 3
            brass(nt, t0 + st*B, ln*B, vel=1.0, fall=fall, pan=0.15)
            brass(nt - 12, t0 + st*B, ln*B, vel=0.45, bright=0.7, fall=fall, pan=-0.2)
        if role == "melA":
            for nt, st, ln in TROMBONE_ANSWER:
                brass(nt - 12, t0 + st*B, ln*B, vel=0.7, bright=0.6, pan=-0.45)
        if role == "melB":
            for nt, st, ln in [(55,0,.3),(58,SW,.3),(53,1,.6)]:
                brass(nt - 12, t0 + st*B, ln*B, vel=0.7, bright=0.6, pan=-0.45)
    if role == "shout":                         # full band swing hits
        for st, ln, v in [(0, .55, 1.0), (1+SW, .3, .9), (2+SW, .3, .9), (3+SW, .9, 1.1)]:
            for nt, pan in zip(shout, [-.4, -.2, 0, .2, .4]):
                brass(nt, t0 + st*B, ln*B*1.6 if ln > .5 else ln*B, vel=v*0.75, pan=pan)
            brass(shout[0] - 24, t0 + st*B, ln*B, vel=0.5, bright=0.6, pan=-0.5)
    if role == "build":
        for i, nt in enumerate([67, 68, 69, 70, 71, 72]):
            brass(nt, t0 + i*SW*B, SW*B*0.9, vel=0.6 + i*0.08)
            brass(nt - 12, t0 + i*SW*B, SW*B*0.9, vel=0.4 + i*0.06, bright=.6)
        timpani(31, t0 + 3*B)

# ---------------------------------------------------------------- mix
def reverb(x, seed):
    g = np.random.default_rng(seed); n = int(SR * 1.6); t = np.arange(n) / SR
    ir = g.standard_normal(n) * np.exp(-t / 0.35); ir[0] = 0
    ir = filt(ir, "low", 6000); ir /= np.sqrt(np.sum(ir**2))
    return fftconvolve(x, ir)[: len(x)]

wetL, wetR = reverb(L, 1), reverb(R, 2)
L = L + 0.28 * wetL; R = R + 0.28 * wetR
n = int(SR * LENGTH)
L, R = L[:n], R[:n]
fade = int(SR * 0.5)
for ch in (L, R):
    ch[:int(SR*.05)] *= np.linspace(0, 1, int(SR*.05)); ch[-fade:] *= np.linspace(1, 0, fade)
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.3), np.tanh(R / peak * 1.3)
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.89, R / peak * 0.89
pcm = (np.column_stack([L, R]) * 32767).astype(np.int16).ravel()
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
