# Batch 01: split-screen narrated videos

Source footage: Google Drive folder "batch 1", 4 unique clips (the `15_10_28` clip was uploaded 3 times).
Matched against the production cards on [BATCH 01 (post 107)](https://automationwithsholz.wordpress.com/?p=107).

## Which clip is which card

| Your clip | Card | Card format | Matched on |
|---|---|---|---|
| `2026_11_19_11_30_43.mp4` | **B01-02** · 45 Units. A $15,000 Software Setup | Narrated story | "went looking for software… ran into a difficult choice… should fit the operation… missing piece is not another all-in-one system" |
| `2026_11_19_11_40_09.mp4` | **B01-03** · The Ten-Minute Task That Keeps Slipping | Narrated story | "A tenant sends a meter photo… identify the reading, find the previous number, enter it into a spreadsheet…" |
| `2026_11_19_15_04_08.mp4` | **B01-04** · The Renewal Reminder Was Somewhere in the Spreadsheet | Narrated story | "lease date… sits in one place, notes in someone's phone… the problem isn't memory, it's visibility" |
| `2026_11_19_15_10_28.mp4` | **B01-10** · Software Cannot Replace Good Property Management | Direct filming | "Software won't inspect a leaking roof… won't build trust with a contractor… won't replace good judgment" |

**Not filmed yet:** B01-01 (The Job Was Marked Complete) is the only narrated card without footage.
`20261115_120114.jpg` (an old family photo) isn't part of this batch and wasn't used.

## Outputs (`hf/out/`)

1080×1920 (9:16), 30 fps, with your original audio (loudness normalised).
- **Top (0–940px):** animated scenes built from each card's *Visual direction*, timed to what you're saying.
- **Bottom:** your footage, cropped to your face.
- **Seam:** word-by-word captions in your brand gold, with whisper mishearings fixed. "Charles" is now "Sholz", "meta" is "meter", "trap" is "track", and "App Sheets" is "AppSheet".
- **Last scene:** brand card plus the card's engagement question.

| Video | Length | Trimmed |
|---|---|---|
| B01-02 | 1:31 | Footage brightened (it was backlit) |
| B01-03 | 1:23 | none |
| B01-04 | 1:09 | Cut the first 5 s (false start, then you repeated the line) |
| B01-10 | 1:07 | Cut the silent tail |

The cards target 15–30 s. These are full-length cuts of everything you said. A 30-second cut can be made from the same projects.

## Rebuild / edit
```
cd batch01/hf && python3 make.py B01-03          # rebuild the HyperFrames project from make.py
cd B01-03 && npx hyperframes render -o ../out/B01-03.mp4
```
- Scene timings and text: `SPECS` in `hf/make.py`
- Visual components and styling: `hf/lib.py`
- Transcripts: `transcripts/` (fast model) and `transcripts_med/` (accurate model)
