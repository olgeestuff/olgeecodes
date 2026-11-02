# Style guide (v0, defaults until the reference is analysed)

> **Status:** These are the starting defaults the editor uses today. The kallaway.marketing reference
> (https://www.tiktok.com/@kallaway.marketing/video/7681665229549276447) hasn't been analysed yet, because TikTok
> is blocked from the cloud session. To finish this guide: save the video on your phone or laptop, upload it to
> the Drive folder as `kallaway-reference.mp4`, then run
> `python editor/analyze_reference.py "AI video editors/references/kallaway-reference.mp4"`.
> Claude reads the output (cuts, frames, caption pacing), rewrites this file with measured values and
> updates `editor/config.yaml` to match.

## Structure
| Part | Layout | Notes |
|---|---|---|
| Hook (first 3–7 s) | A-roll full screen | No B-roll. Fast. Captions in the lower third |
| Narration | Split: demo top 50%, face bottom 50% | Demo matches what's being said |
| Pop-outs | A-roll full screen 2.6 s, about every 11 s, max 3 | Fade + 90 px slide-up, whoosh |
| CTA (last sentence) | A-roll full screen | Ends on the face |

## Captions (never skipped)
- Inter Black, 78 px at 1080 wide, white with a 6 px black outline
- Max 3 words or 18 characters per line, new line at every comma or full stop
- Spoken word highlighted yellow `#FFD60A`; each new line pops in at 115% and settles in 90 ms
- Position: centred on the split line (y = 960) during split screen, 520 px from the bottom when full screen

## Motion graphics (minimal)
- White pill badge with a yellow accent edge, 54 px text, optional icon
- Triggered by keywords (config list) and spoken numbers, at least 3.5 s apart, max 8 per video, 1.6 s on screen
- Drops in from 40 px above, near the top of the frame, with a "pop" SFX

## Pacing
- Silences over 0.35 s are cut, with 0.12 s of breath left on each side
- Punch-in zoom (1.0 ↔ 1.12) on the face every 4.5 s, so the frame never sits still

## Audio
- Voice at -14 LUFS, true peak -1.5 dB
- Whoosh on layout changes, pop on badges, both at -8 dB
- Music: add the trending Commercial Music Library sound inside TikTok at upload time (USA first). For other platforms, use a royalty-free bed at -20 dB, ducked under the voice
