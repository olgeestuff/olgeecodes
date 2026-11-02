"""Render one finished short: hook (full screen) + narration/CTA (split screen) with captions,
pop-outs, punch-in zooms, keyword graphics, SFX and optional music.

Normally called through run.py. Direct use:
  python editor/build_edit.py --hook H.mp4 --body N.mp4 [--body CTA.mp4] [--demo D.webm] --out X.mp4
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from captions import SENTENCE_END, build_ass
from common import (EXPORTS, WORK, duration, ffmpeg_bin, has_audio, load_config, ref_path, run,
                    video_size)
from graphics import ensure_sfx, pick_graphics
from transcribe import transcribe


# ---------------------------------------------------------------- silence trim
def keep_segments(media: Path, cfg: dict) -> list[tuple[float, float]]:
    st = cfg["silence_trim"]
    total = duration(media)
    if not st["enabled"] or not has_audio(media):
        return [(0.0, total)]
    res = run([ffmpeg_bin(), "-hide_banner", "-i", media, "-af",
               f"silencedetect=noise={st['noise_db']}dB:d={st['min_silence']}", "-f", "null", "-"])
    silences, start = [], None
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            start = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end:" in line and start is not None:
            end = float(line.split("silence_end:")[1].split()[0])
            silences.append((start, end))
            start = None
    if start is not None:
        silences.append((start, total))
    pad, keep, cur = st["keep_padding"], [], 0.0
    for s, e in silences:
        a, b = cur, min(total, s + pad)
        if b - a > 0.08:
            keep.append((a, b))
        cur = max(cur, e - pad)
    if total - cur > 0.08:
        keep.append((cur, total))
    return keep or [(0.0, total)]


def trim_and_join(parts: list[Path], out: Path, cfg: dict) -> Path:
    """Cut silences from each part, join them, normalise to fps / even size."""
    fps = cfg["output"]["fps"]
    w0, h0 = video_size(parts[0])
    w0, h0 = w0 // 2 * 2, h0 // 2 * 2
    inputs, chains, labels = [], [], []
    for i, p in enumerate(parts):
        inputs += ["-i", p]
        segs = keep_segments(p, cfg)
        expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in segs)
        chains.append(f"[{i}:v]select='{expr}',setpts=N/FRAME_RATE/TB,fps={fps},"
                      f"scale={w0}:{h0}:force_original_aspect_ratio=increase,crop={w0}:{h0},setsar=1[v{i}]")
        if has_audio(p):
            chains.append(f"[{i}:a]aselect='{expr}',asetpts=N/SR/TB,aresample=48000,"
                          f"aformat=channel_layouts=stereo[a{i}]")
        else:
            d = sum(b - a for a, b in segs)
            chains.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    chains.append(f"{''.join(labels)}concat=n={len(parts)}:v=1:a=1[v][a]")
    run([ffmpeg_bin(), "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-c:a", "aac", "-b:a", "192k", out])
    return out


# ---------------------------------------------------------------- layout plan
def sentence_starts(words: list[dict]) -> list[int]:
    """Indexes of words that start a sentence. Falls back to clause breaks (commas)
    when the transcript has little punctuation."""
    idx = [0] if words else []
    for i in range(1, len(words)):
        if words[i - 1]["word"].endswith(SENTENCE_END):
            idx.append(i)
    if len(idx) < max(3, len(words) // 25):
        idx = [0] + [i for i in range(1, len(words))
                     if words[i - 1]["word"].endswith(SENTENCE_END + (",", ";", ":"))]
    return idx


def plan_fullscreen(words_body: list[dict], hook_dur: float, total: float, cfg: dict
                    ) -> list[tuple[float, float]]:
    """Windows (start, end) where A-roll is full screen."""
    lay = cfg["layout"]
    windows = []
    if hook_dur > 0 and lay["hook_fullscreen"]:
        windows.append((0.0, hook_dur))
    cta_start = total
    starts = sentence_starts(words_body)
    if lay["popout"].get("cta_fullscreen") and len(starts) > 1:
        cta_start = max(words_body[starts[-1]]["start"] - 0.05, total - 10.0)
        if cta_start - hook_dur > 6:
            windows.append((cta_start, total))
        else:
            cta_start = total
    po = lay["popout"]
    if po["enabled"]:
        last, count = hook_dur, 0
        for i in starts:
            t = words_body[i]["start"] - 0.05
            if t - last >= po["every_seconds"] and t + po["duration"] < cta_start - 2.5:
                windows.append((t, t + po["duration"]))
                last, count = t + po["duration"], count + 1
                if count >= po["max_count"]:
                    break
    return sorted(windows)


# ---------------------------------------------------------------- render
def _cover(w: int, h: int, bias: float = 0.5) -> str:
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:(iw-{w})/2:(ih-{h})*{bias}")


def _zoom(w: int, h: int, cfg: dict) -> str:
    z = cfg["zoom"]
    if not z["enabled"]:
        return "null"
    n = int(z["punch_every"] * cfg["output"]["fps"])
    return (f"zoompan=z='if(eq(mod(floor(in/{n}),2),1),{z['amount']},1)':d=1:"
            f"x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih*0.35/zoom)':s={w}x{h}:fps={cfg['output']['fps']}")


def render(hook: Path | None, body: list[Path], demo: Path | None, out: Path,
           cfg: dict | None = None) -> Path:
    cfg = cfg or load_config()
    W, H, fps = cfg["output"]["width"], cfg["output"]["height"], cfg["output"]["fps"]
    top_h = int(H * cfg["layout"]["split_ratio"]) // 2 * 2
    bot_h = H - top_h
    WORK.mkdir(parents=True, exist_ok=True)
    tag = out.stem.replace(" ", "_")

    print("1/5 trimming silences...")
    hook_t = trim_and_join([hook], WORK / f"{tag}_hook.mp4", cfg) if hook else None
    body_t = trim_and_join(body, WORK / f"{tag}_body.mp4", cfg)
    hook_dur = duration(hook_t) if hook_t else 0.0
    body_dur = duration(body_t)
    total = hook_dur + body_dur

    print("2/5 transcribing (captions)...")
    w_hook = transcribe(hook_t) if hook_t else []
    w_body = [{**w, "start": w["start"] + hook_dur, "end": w["end"] + hook_dur}
              for w in transcribe(body_t)]
    words = w_hook + w_body

    print("3/5 planning layout + graphics...")
    full = plan_fullscreen(w_body, hook_dur, total, cfg)

    def layout_at(t: float) -> str:
        return "full" if any(a <= t < b for a, b in full) else "split"

    fonts_dir = WORK / "fonts"
    fonts_dir.mkdir(exist_ok=True)
    font_src = ref_path(cfg["captions"]["font_file"])
    if font_src.exists():
        shutil.copy(font_src, fonts_dir / font_src.name)
    ass = build_ass(words, WORK / f"{tag}.ass", cfg, W, H, layout_at, split_y=top_h)
    graphics = [g for g in pick_graphics(words, cfg, 0.5, total)
                if not any(a - 0.3 <= g["start"] < a + 0.5 for a, _ in full)]
    sfx = ensure_sfx(cfg)
    transitions = sorted({t for a, b in full for t in (a, b) if 0.05 < t < total - 0.05})

    print(f"   hook {hook_dur:.1f}s | body {body_dur:.1f}s | full-screen windows {len(full)} | "
          f"graphics {len(graphics)}")

    # ---- inputs
    inputs: list = []
    def add(*args) -> int:
        inputs.extend(str(Path(x).resolve()) if isinstance(x, Path) else x for x in args)
        return sum(1 for x in inputs if x == "-i") - 1

    i_hook = add("-i", hook_t) if hook_t else None
    i_body = add("-i", body_t)
    i_demo = add("-i", demo) if demo else None
    i_whoosh = add("-i", sfx["whoosh"])
    i_pop = add("-i", sfx["pop"])
    music = ref_path(cfg["audio"]["music_file"]) if cfg["audio"].get("music_file") else None
    i_music = add("-stream_loop", "-1", "-i", music) if music and music.exists() else None
    i_gfx = [add("-loop", "1", "-framerate", str(fps), "-t", f"{g['end'] - g['start']:.2f}", "-i", g["png"])
             for g in graphics]

    f: list[str] = []
    # A-roll timeline (hook + body)
    if i_hook is not None:
        f.append(f"[{i_hook}:v][{i_hook}:a][{i_body}:v][{i_body}:a]concat=n=2:v=1:a=1[av][aa]")
    else:
        f.append(f"[{i_body}:v]null[av];[{i_body}:a]anull[aa]")
    bias = cfg["layout"]["aroll_face_bias"]
    f.append("[av]split=2[av1][av2]")
    f.append(f"[av1]{_cover(W, bot_h, bias)},{_zoom(W, bot_h, cfg)},setsar=1[half]")
    f.append(f"[av2]{_cover(W, H, 0.5)},{_zoom(W, H, cfg)},setsar=1,format=yuva420p,"
             f"split={max(1, len(full))}" + "".join(f"[fs{k}]" for k in range(max(1, len(full)))))

    # B-roll (top), fitted to the body length
    if i_demo is not None:
        d = duration(demo)
        speed = max(0.6, min(cfg["broll"]["max_speed"], d / max(body_dur, 0.1)))
        f.append(f"[{i_demo}:v]{_cover(W, top_h, 0.0)},fps={fps},setpts=PTS/{speed:.4f},"
                 f"tpad=stop_mode=clone:stop_duration={body_dur:.2f},trim=duration={body_dur:.3f},"
                 f"setpts=PTS-STARTPTS+{hook_dur:.3f}/TB,setsar=1[broll]")
    else:
        col = cfg["broll"]["placeholder_color"].lstrip("#")
        f.append(f"color=c=0x{col}:s={W}x{top_h}:r={fps}:d={body_dur:.3f},"
                 f"drawtext=text='DEMO GOES HERE':fontcolor=white@0.5:fontsize=64:"
                 f"x=(w-tw)/2:y=(h-th)/2,setpts=PTS-STARTPTS+{hook_dur:.3f}/TB[broll]")

    # Base canvas + split screen
    f.append(f"color=c=black:s={W}x{H}:r={fps}:d={total:.3f}[base]")
    f.append("[base][broll]overlay=0:0:eof_action=pass[b1]")
    f.append(f"[b1][half]overlay=0:{top_h}:eof_action=pass:shortest=1[b2]")
    last = "b2"

    # Full-screen windows with fade + slide-up animation
    fd = cfg["layout"]["popout"]["fade"]
    for k, (a, b) in enumerate(full):
        fin = "" if a < 0.05 else f",fade=t=in:st=0:d={fd}:alpha=1"
        f.append(f"[fs{k}]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS{fin},"
                 f"fade=t=out:st={max(0, b - a - fd):.3f}:d={fd}:alpha=1,setpts=PTS+{a:.3f}/TB[fw{k}]")
        slide = "0" if a < 0.05 else f"'if(lt(t-{a:.3f},{fd}),90*(1-(t-{a:.3f})/{fd}),0)'"
        f.append(f"[{last}][fw{k}]overlay=0:{slide}:eof_action=pass:eval=frame[o{k}]")
        last = f"o{k}"
    if not full:
        f.append("[fs0]nullsink")

    # Keyword graphics: fade + drop-in near the top of the frame
    for k, (g, gi) in enumerate(zip(graphics, i_gfx)):
        dur = g["end"] - g["start"]
        st = g["start"]
        f.append(f"[{gi}:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,"
                 f"fade=t=out:st={dur - 0.2:.2f}:d=0.2:alpha=1,setpts=PTS+{st:.3f}/TB[g{k}]")
        f.append(f"[{last}][g{k}]overlay=(W-w)/2:'110-40*max(0,1-(t-{st:.3f})/0.18)':"
                 f"eof_action=pass:eval=frame[gx{k}]")
        last = f"gx{k}"

    # Captions last so they sit on top
    f.append(f"[{last}]ass={ass.name}:fontsdir=fonts,format=yuv420p[vout]")

    # ---- audio
    a = cfg["audio"]
    f.append(f"[aa]loudnorm=I={a['voice_lufs']}:TP=-1.5:LRA=11,aresample=48000[voice0]")
    ducking = i_music is not None and a.get("duck")
    f.append("[voice0]asplit=2[voice][vkey]" if ducking else "[voice0]anull[voice]")
    mix = ["[voice]"]
    sfx_cfg = a["sfx"]
    if sfx_cfg["enabled"] and (transitions or graphics):
        parts = []
        if transitions:
            f.append(f"[{i_whoosh}:a]asplit={len(transitions)}" + "".join(f"[w{k}]" for k in range(len(transitions))))
            for k, t in enumerate(transitions):
                ms = int(max(0, t - 0.2) * 1000)
                f.append(f"[w{k}]adelay={ms}|{ms}[wd{k}]")
                parts.append(f"[wd{k}]")
        if graphics:
            f.append(f"[{i_pop}:a]asplit={len(graphics)}" + "".join(f"[p{k}]" for k in range(len(graphics))))
            for k, g in enumerate(graphics):
                ms = int(g["start"] * 1000)
                f.append(f"[p{k}]adelay={ms}|{ms}[pd{k}]")
                parts.append(f"[pd{k}]")
        f.append(f"{''.join(parts)}amix=inputs={len(parts)}:normalize=0,volume={sfx_cfg['volume_db']}dB[sfx]")
        mix.append("[sfx]")
    if i_music is not None:
        f.append(f"[{i_music}:a]aresample=48000,aformat=channel_layouts=stereo,volume={a['music_db']}dB,"
                 f"atrim=duration={total:.3f}[mus]")
        if ducking:
            f.append("[mus][vkey]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[musd]")
            mix.append("[musd]")
        else:
            mix.append("[mus]")
    if len(mix) > 1:
        f.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first[aout]")
    else:
        f.append("[voice]anull[aout]")

    graph = ";".join(f)
    out.parent.mkdir(parents=True, exist_ok=True)
    print("4/5 rendering (this takes a few minutes)...")
    script = WORK / f"{tag}.filter.txt"
    script.write_text(graph, encoding="utf-8")
    cmd = [ffmpeg_bin(), "-y", *inputs, "-filter_complex_script", script.name,
           "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", str(fps),
           "-c:v", "libx264", "-preset", cfg["output"]["preset"], "-crf", str(cfg["output"]["crf"]),
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
           out.resolve()]

    res = subprocess.run([str(c) for c in cmd], cwd=WORK, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError("Render failed:\n" + "\n".join(res.stderr.strip().splitlines()[-30:]))
    print(f"5/5 done -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", type=Path)
    ap.add_argument("--body", type=Path, action="append", required=True)
    ap.add_argument("--demo", type=Path)
    ap.add_argument("--out", type=Path, default=EXPORTS / "test.mp4")
    a = ap.parse_args()
    render(a.hook, a.body, a.demo, a.out)
