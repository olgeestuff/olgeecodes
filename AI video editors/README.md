# AI Video Editor

Turns your teleprompter takes plus app demos into ready-to-post shorts (TikTok, LinkedIn, Reels).
You record. One command does the edit.

```
raw footage/   your takes (A-roll) + Playwright demos (B-roll)  ← you drop files here
references/    style_guide.md, fonts, sfx, icons, music
exports/       finished videos                                   ← you post from here
```

## What every export gets
- 1080×1920, split screen: **demo on top, you on the bottom**
- **Hook = you full screen.** During the body you pop to full screen 2–3 times (fade + slide animation), and the **CTA is full screen**
- **Captions on every word:** bold, 3 words at a time, current word in yellow, placed on the split line (lower third when full screen)
- Silences and breaths cut out, punch-in zooms every ~4.5 s
- Keyword badges pop in, e.g. "Spreadsheet", "Rent", spoken numbers like "300" (edit the list in `editor/config.yaml`)
- Whoosh on every layout change, pop on every badge, voice levelled to -14 LUFS (TikTok/IG loudness)
- One export per hook take, so you can A/B test hooks

## Your workflow (per video)
1. **Record**: hooks, narration (+ CTA) on the teleprompter. Upload to the Drive folder.
2. **Name the files** (or let `match_scripts.py` tell you which script each take is):
   - `video 5 hook 1.mp4`, `video 5 hook 2.mp4` …
   - `video 5 narration.mp4` (CTA can be inside it, or separate as `video 5 cta.mp4`)
3. **Record the demo** on your laptop: `node record-demo.js scripts/video5.demo.yaml` (see `demo/SETUP-WINDOWS.md`). It saves `video 5 demo.webm`. Upload it to the same Drive folder.
4. **Edit** (Claude Code session or your laptop):
   ```
   python editor/fetch_drive.py
   python editor/run.py "video 5"
   ```
   Output: `exports/video 5 - hook 1.mp4`, `exports/video 5 - hook 2.mp4` …
5. **Post**, and add the trending sound inside TikTok (see `references/music/README.md`).

No demo yet? `run.py` still renders, with a "DEMO GOES HERE" placeholder on top.

## Commands
| Command | What it does |
|---|---|
| `python editor/fetch_drive.py` | Downloads new takes + scripts from the Drive folder (needs `GOOGLE_API_KEY`, see the top of the file) |
| `python editor/match_scripts.py` | Transcribes each take and shows which script it matches |
| `python editor/run.py "video 5"` | Edits video 5, one export per hook |
| `python editor/run.py --all` | Edits every video that has a narration |
| `python editor/analyze_reference.py <video>` | Breaks a style reference into cuts, frames and caption pacing, which feed `style_guide.md` |

## Changing the style
Everything lives in `editor/config.yaml`: caption font, size and colours, split ratio, pop-out frequency, zoom amount, badge keywords, SFX volume, music level. Change values there, not in code.

## Setup (laptop, Windows)
```
winget install Python.Python.3.12
winget install Gyan.FFmpeg
pip install -r editor/requirements.txt
```
The first run downloads the Whisper "small" captions model (~250 MB). It's free and runs offline after that.
