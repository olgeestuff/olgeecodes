"""Render one finished short: hook (full screen) + narration/CTA (split screen) with captions,
pop-outs, punch-in zooms, keyword graphics, SFX and optional music.

Normally called through run.py. Direct use:
  python editor/build_edit.py --hook H.mp4 --body N.mp4 [--body CTA.mp4] [--demo D.webm] --out X.mp4
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

from captions import SENTENCE_END, build_ass
from common import (EXPORTS, WORK, duration, ffmpeg_bin, has_audio, load_config, ref_path, run,
                    video_size)
import yaml
from PIL import Image

from denoise import denoise
from graphics import ensure_sfx, make_mask, make_title, pick_graphics
from motion import render_paperwork
from toons import render_story
from transcribe import transcribe


# ---------------------------------------------------------------- silence trim
def keep_segments(media: Path, cfg: dict, audio: Path | None = None) -> list[tuple[float, float]]:
    """Speech segments to keep. `audio` = cleaned voice track (pauses are easier to find)."""
    st = cfg["silence_trim"]
    total = duration(media)
    if not st["enabled"] or not has_audio(media):
        return [(0.0, total)]
    res = run([ffmpeg_bin(), "-hide_banner", "-i", audio or media, "-af",
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
    use_clean = cfg["audio"].get("denoise", {}).get("enabled")
    n = 0
    for i, p in enumerate(parts):
        vi = n
        inputs += ["-i", p]
        n += 1
        ai = vi
        audio_src = p
        if use_clean and has_audio(p):
            audio_src = denoise(p, cfg)          # cleaned voice replaces the camera audio
            inputs += ["-i", audio_src]
            ai = n
            n += 1
        segs = keep_segments(p, cfg, audio_src)
        expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in segs)
        chains.append(f"[{vi}:v]select='{expr}',setpts=N/FRAME_RATE/TB,fps={fps},"
                      f"scale={w0}:{h0}:force_original_aspect_ratio=increase,crop={w0}:{h0},setsar=1[v{i}]")
        if has_audio(p):
            chains.append(f"[{ai}:a]aselect='{expr}',asetpts=N/SR/TB,aresample=48000,"
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


def _norm_word(w: str) -> str:
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


def find_word(words: list[dict], target: str, after: float = 0.0) -> float | None:
    """Start time of the first spoken word (or phrase) matching `target` at/after `after`."""
    toks = [_norm_word(t) for t in target.split() if _norm_word(t)]
    for i, w in enumerate(words):
        if w["start"] < after - 0.01:
            continue
        if all(i + j < len(words) and _norm_word(words[i + j]["word"]).startswith(t)
               for j, t in enumerate(toks)):
            return w["start"]
    return None


def find_phrase_end(words: list[dict], phrase: str) -> float | None:
    """End time of the LAST occurrence of a spoken phrase."""
    toks = [_norm_word(t) for t in phrase.split() if _norm_word(t)]
    flat = []          # split joined words ("paperwork" vs "paper work") into a comparable stream
    for w in words:
        flat.append((_norm_word(w["word"]), w["end"]))
    target = "".join(toks)
    best = None
    for i in range(len(flat)):
        acc = ""
        for j in range(i, min(i + len(toks) + 3, len(flat))):
            acc += flat[j][0]
            if acc == target:
                best = flat[j][1]
                break
            if not target.startswith(acc):
                break
    return best


def load_plan(path: Path | None) -> dict:
    if path and path.exists():
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


def render(hook: Path | None, body: list[Path], demo: Path | None, out: Path,
           cfg: dict | None = None, plan: dict | None = None) -> Path:
    cfg = cfg or load_config()
    plan = plan or {}
    lay = cfg["layout"]
    W, H, fps = cfg["output"]["width"], cfg["output"]["height"], cfg["output"]["fps"]
    top_h = int(H * lay["split_ratio"]) // 2 * 2
    ac = lay["aroll_card"]
    card_w = int(W * ac["width"]) // 2 * 2
    card_h = (H - top_h - ac["top_gap"] - ac["bottom_margin"]) // 2 * 2
    card_x, card_y = (W - card_w) // 2, top_h + ac["top_gap"]
    bc = lay["broll_card"]
    bw = int(W * bc["width"]) // 2 * 2
    bh = int(bw / bc["aspect"]) // 2 * 2
    WORK.mkdir(parents=True, exist_ok=True)
    tag = out.stem.replace(" ", "_")

    print("1/5 trimming silences...")
    hook_t = trim_and_join([hook], WORK / f"{tag}_hook.mp4", cfg) if hook else None
    body_t = trim_and_join(body, WORK / f"{tag}_body.mp4", cfg)
    hook_dur = duration(hook_t) if hook_t else 0.0
    body_dur = duration(body_t)
    total = hook_dur + body_dur

    print("2/5 transcribing (captions)...")
    prompt = plan.get("prompt")
    w_hook = transcribe(hook_t, prompt=prompt) if hook_t else []
    w_body = [{**w, "start": w["start"] + hook_dur, "end": w["end"] + hook_dur}
              for w in transcribe(body_t, prompt=prompt)]
    # Optional: end the video right after a phrase (drops retakes / chatter after the CTA)
    if plan.get("end_after"):
        t_end = find_phrase_end(w_body, plan["end_after"])
        if t_end is None:
            print(f'   warning: end_after phrase "{plan["end_after"]}" not found; keeping full length')
        elif t_end + 0.6 < total:
            keep = t_end + 0.6 - hook_dur
            cut = WORK / f"{tag}_body_cut.mp4"
            run([ffmpeg_bin(), "-y", "-i", body_t, "-t", f"{keep:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "16", "-c:a", "aac", "-b:a", "192k", cut])
            body_t, body_dur = cut, duration(cut)
            total = hook_dur + body_dur
            w_body = [w for w in w_body if w["start"] < total]
    # Plan word fixes for captions, e.g. {trim: trail} when Whisper mishears a word
    fixes = {str(k).lower(): str(v) for k, v in (plan.get("fix") or {}).items()}
    if fixes:
        def _fx(w):
            core = w["word"].strip(".,!?;:").lower()
            return {**w, "word": w["word"].lower().replace(core, fixes[core])} if core in fixes else w
        w_hook, w_body = [_fx(w) for w in w_hook], [_fx(w) for w in w_body]
    words = w_hook + w_body

    print("3/5 planning layout + graphics...")
    # Single-take videos: the plan says which spoken word ends the full-screen hook.
    split_start = hook_dur
    if not hook_t and plan.get("hook_until"):
        t = find_word(w_body, plan["hook_until"])
        if t is None:
            print(f'   warning: hook_until word "{plan["hook_until"]}" not found; no hook window')
        else:
            split_start = max(0.0, t - 0.05)
    # Resolve plan segments to times (each starts on its spoken word, ends where the next starts)
    segs = plan.get("segments") or []
    seg_times: list[tuple[float, float]] = []
    if segs:
        anchors, cur = [], split_start
        for s in segs:
            t = find_word(w_body, s["at"], cur) if s.get("at") else cur
            if t is None:
                print(f'   warning: segment word "{s.get("at")}" not found; appended after previous')
                t = cur
            t = max(t - 0.05, split_start)
            anchors.append(t)
            cur = t
        anchors[0] = split_start
        seg_times = [(anchors[k], anchors[k + 1] if k + 1 < len(segs) else total) for k in range(len(segs))]
    plan_full = [(a, b) for s, (a, b) in zip(segs, seg_times) if s.get("full")]
    auto = plan_fullscreen([w for w in w_body if w["start"] >= split_start], split_start, total, cfg)
    if plan_full:   # keep automatic pop-outs only well away from the plan's own full-screen cuts
        gap = cfg["layout"]["popout"]["every_seconds"] / 2
        auto = [(a, b) for a, b in auto
                if a < split_start + 0.05 or all(b + gap <= pa or a >= pb + gap for pa, pb in plan_full)]
    full = sorted(auto + plan_full)

    def layout_at(t: float) -> str:
        return "full" if any(a <= t < b for a, b in full) else "split"

    fonts_dir = WORK / "fonts"
    fonts_dir.mkdir(exist_ok=True)
    font_src = ref_path(cfg["captions"]["font_file"])
    if font_src.exists():
        shutil.copy(font_src, fonts_dir / font_src.name)
    ass = build_ass(words, WORK / f"{tag}.ass", cfg, W, H, layout_at,
                    split_y=top_h + ac["top_gap"] // 2 - 6)
    graphics = [g for g in pick_graphics(words, cfg, split_start + 0.3, total)
                if layout_at(g["start"]) == "split" and layout_at(g["end"] - 0.01) == "split"
                and not any(s.get("graphic") and a <= g["start"] < b for s, (a, b) in zip(segs, seg_times))]
    sfx = ensure_sfx(cfg)
    transitions = sorted({t for a, b in full for t in (a, b) if 0.05 < t < total - 0.05})

    title_png = None
    if plan.get("title") or plan.get("subtitle"):
        title_png = make_title(plan.get("title", ""), plan.get("subtitle", ""), cfg, W)
    title_h = Image.open(title_png).height if title_png else 0
    title_y = 70
    area_top = title_y + title_h + 30 if title_png else 60
    bx = (W - bw) // 2
    by = area_top + max(0, (top_h - area_top - bh) // 2)

    print(f"   split from {split_start:.1f}s | total {total:.1f}s | full-screen windows {len(full)} | "
          f"graphics {len(graphics)}")

    extra_pops: list[float] = []     # pop SFX times for motion-graphic items

    # ---- inputs
    inputs: list = []
    def add(*args) -> int:
        inputs.extend(str(Path(x).resolve()) if isinstance(x, Path) else x for x in args)
        return sum(1 for x in inputs if x == "-i") - 1

    i_hook = add("-i", hook_t) if hook_t else None
    i_body = add("-i", body_t)
    # demo audio is never used (muted); with a plan each segment gets its own fast-seek input
    i_demo = add("-i", demo) if demo and not plan.get("segments") else None
    i_whoosh = add("-i", sfx["whoosh"])
    i_pop = add("-i", sfx["pop"])
    music = ref_path(cfg["audio"]["music_file"]) if cfg["audio"].get("music_file") else None
    i_music = add("-stream_loop", "-1", "-i", music) if music and music.exists() else None
    i_gfx = [add("-loop", "1", "-framerate", str(fps), "-t", f"{g['end'] - g['start']:.2f}", "-i", g["png"])
             for g in graphics]
    i_amask = add("-loop", "1", "-framerate", str(fps), "-t", f"{total:.3f}", "-i",
                  make_mask(card_w, card_h, ac["radius"]))
    i_bmask = add("-loop", "1", "-framerate", str(fps), "-t", f"{total:.3f}", "-i",
                  make_mask(bw, bh, bc["radius"])) if demo else None
    i_title = add("-loop", "1", "-framerate", str(fps), "-t", f"{total:.3f}", "-i", title_png) if title_png else None

    f: list[str] = []
    # A-roll timeline (hook + body)
    if i_hook is not None:
        f.append(f"[{i_hook}:v][{i_hook}:a][{i_body}:v][{i_body}:a]concat=n=2:v=1:a=1[av][aa]")
    else:
        f.append(f"[{i_body}:v]null[av];[{i_body}:a]anull[aa]")
    bias = lay["aroll_face_bias"]
    nfull = max(1, len(full))
    f.append("[av]split=2[av1][av2]")
    f.append(f"[av1]{_cover(card_w, card_h, bias)},setsar=1,format=yuva420p[ac0]")
    f.append(f"[{i_amask}:v]format=gray,setsar=1[am]")
    f.append("[ac0][am]alphamerge[acard]")
    f.append(f"[av2]{_cover(W, H, 0.5)},{_zoom(W, H, cfg)},setsar=1,format=yuva420p,"
             f"split={nfull}" + "".join(f"[fs{k}]" for k in range(nfull)))

    # Base canvas
    f.append(f"color=c=black:s={W}x{H}:r={fps}:d={total:.3f}[base]")
    last = "base"
    if i_title is not None:
        f.append(f"[{last}][{i_title}:v]overlay=0:{title_y}:shortest=1[tt]")
        last = "tt"

    # B-roll card (top), muted
    body_len = total - split_start
    if demo is not None:
        parts = []
        if segs:
            for k, (s, (a0, a1)) in enumerate(zip(segs, seg_times)):
                d = max(0.2, a1 - a0)
                if s.get("full"):            # A-roll full screen covers this; keep the card black
                    f.append(f"color=c=black:s={bw}x{bh}:r={fps}:d={d:.3f},setsar=1[bs{k}]")
                    parts.append(f"[bs{k}]")
                    continue
                if s.get("graphic") == "story":
                    scenes = []
                    for sc in s.get("scenes", []):
                        ts = find_word(w_body, sc["at"], a0) if sc.get("at") else a0
                        if ts is None or ts >= a1:
                            print(f'   warning: story scene word "{sc.get("at")}" not found')
                            continue
                        ts = max(a0, ts - 0.05)
                        items = []
                        for it in sc.get("items", []):
                            ti = find_word(w_body, it["at"], ts) if it.get("at") else None
                            if ti is not None and ti < a1:
                                items.append({**it, "t": ti - a0})
                                extra_pops.append(ti)
                        scenes.append({**sc, "t": ts - a0, "items": items})
                    if scenes:
                        scenes[0]["t"] = 0.0
                        extra_pops.extend(a0 + sc["t"] for sc in scenes[1:])
                    clip = render_story(scenes, d + 0.1, bw, bh, cfg, WORK / f"{tag}_story{k}.mp4", fps)
                    i_seg = add("-i", clip)
                    f.append(f"[{i_seg}:v]fps={fps},setsar=1,trim=duration={d:.3f}[bs{k}]")
                    parts.append(f"[bs{k}]")
                    continue
                if s.get("graphic") == "paperwork":
                    items = []
                    for it in s.get("items", []):
                        ti = find_word(w_body, it["at"], a0) if it.get("at") else None
                        if ti is None or ti >= a1:
                            continue
                        items.append({**it, "t": ti - a0})
                        extra_pops.append(ti)
                    clip = render_paperwork(items, d + 0.1, bw, bh, cfg, WORK / f"{tag}_paper{k}.mp4", fps)
                    i_seg = add("-i", clip)
                    f.append(f"[{i_seg}:v]fps={fps},setsar=1,trim=duration={d:.3f}[bs{k}]")
                    parts.append(f"[bs{k}]")
                    continue
                sp = float(s.get("speed", 1.0))
                x, y, cw, ch = s.get("crop", [0, 0, 0, 0])
                crop = f"crop={cw}:{ch}:{x}:{y}," if cw and ch else ""
                # seek on the input (fast) instead of trimming from the start of a long demo
                i_seg = add("-ss", f"{float(s['src']):.3f}", "-t", f"{d * sp + 0.5:.3f}", "-i", demo)
                f.append(f"[{i_seg}:v]setpts=(PTS-STARTPTS)/{sp},fps={fps},{crop}{_cover(bw, bh)},setsar=1,"
                         f"tpad=stop_mode=clone:stop_duration={d:.3f},trim=duration={d:.3f}[bs{k}]")
                parts.append(f"[bs{k}]")
            f.append(f"{''.join(parts)}concat=n={len(parts)}:v=1:a=0[braw]")
        else:
            dd = duration(demo)
            speed = max(0.6, min(cfg["broll"]["max_speed"], dd / max(body_len, 0.1)))
            f.append(f"[{i_demo}:v]fps={fps},setpts=PTS/{speed:.4f},{_cover(bw, bh, 0.0)},setsar=1,"
                     f"tpad=stop_mode=clone:stop_duration={body_len:.2f},trim=duration={body_len:.3f}[braw]")
        f.append(f"[braw]format=yuva420p,setpts=PTS-STARTPTS+{split_start:.3f}/TB[bc0]")
        f.append(f"[{i_bmask}:v]format=gray,trim=duration={body_len:.3f},"
                 f"setpts=PTS-STARTPTS+{split_start:.3f}/TB[bm]")
        f.append("[bc0][bm]alphamerge[bcard]")
        f.append(f"[{last}][bcard]overlay={bx}:{by}:eof_action=pass[b1]")
        last = "b1"

    f.append(f"[{last}][acard]overlay={card_x}:{card_y}:eof_action=pass[b2]")
    last = "b2"

    # Full-screen windows with fade + slide-up animation
    fd = lay["popout"]["fade"]
    for k, (a, b) in enumerate(full):
        fin = "" if a < 0.05 else f",fade=t=in:st=0:d={fd}:alpha=1"
        f.append(f"[fs{k}]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS{fin},"
                 f"fade=t=out:st={max(0, b - a - fd):.3f}:d={fd}:alpha=1,setpts=PTS+{a:.3f}/TB[fw{k}]")
        slide = "0" if a < 0.05 else f"'if(lt(t-{a:.3f},{fd}),90*(1-(t-{a:.3f})/{fd}),0)'"
        f.append(f"[{last}][fw{k}]overlay=0:{slide}:eof_action=pass:eval=frame[o{k}]")
        last = f"o{k}"
    if not full:
        f.append("[fs0]nullsink")

    # Keyword graphics: drop in over the bottom edge of the demo card (or centre of top area)
    gy = (by + bh - 50) if demo else (area_top + (top_h - area_top) // 2 - 60)
    for k, (g, gi) in enumerate(zip(graphics, i_gfx)):
        dur = g["end"] - g["start"]
        st = g["start"]
        f.append(f"[{gi}:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,"
                 f"fade=t=out:st={dur - 0.2:.2f}:d=0.2:alpha=1,setpts=PTS+{st:.3f}/TB[g{k}]")
        f.append(f"[{last}][g{k}]overlay=(W-w)/2:'{gy}-40*max(0,1-(t-{st:.3f})/0.18)':"
                 f"eof_action=pass:eval=frame[gx{k}]")
        last = f"gx{k}"

    # Captions last so they sit on top
    f.append(f"[{last}]ass={ass.name}:fontsdir=fonts,format=yuv420p[vout]")

    # ---- audio
    a = cfg["audio"]
    eq = (a.get("voice_eq") or "anull") + ","
    f.append(f"[aa]{eq}loudnorm=I={a['voice_lufs']}:TP=-1.5:LRA=11,aresample=48000[voice0]")
    ducking = i_music is not None and a.get("duck")
    f.append("[voice0]asplit=2[voice][vkey]" if ducking else "[voice0]anull[voice]")
    mix = ["[voice]"]
    sfx_cfg = a["sfx"]
    pop_times = sorted([g["start"] for g in graphics] + extra_pops)
    if sfx_cfg["enabled"] and (transitions or pop_times):
        parts = []
        if transitions:
            f.append(f"[{i_whoosh}:a]asplit={len(transitions)}" + "".join(f"[w{k}]" for k in range(len(transitions))))
            for k, t in enumerate(transitions):
                ms = int(max(0, t - 0.2) * 1000)
                f.append(f"[w{k}]adelay={ms}|{ms}[wd{k}]")
                parts.append(f"[wd{k}]")
        if pop_times:
            f.append(f"[{i_pop}:a]asplit={len(pop_times)}" + "".join(f"[p{k}]" for k in range(len(pop_times))))
            for k, pt in enumerate(pop_times):
                ms = int(max(0, pt - 0.05) * 1000)
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
    ap.add_argument("--plan", type=Path, help="demo plan YAML (title, hook_until, segments)")
    ap.add_argument("--out", type=Path, default=EXPORTS / "test.mp4")
    a = ap.parse_args()
    render(a.hook, a.body, a.demo, a.out, plan=load_plan(a.plan))
