# dq launch film (15 s)

A 15-second launch video for [dq](https://dq.withsholz.workers.dev/), made with the onetake skill (`.claude/skills/onetake`).

**Concept: chaos → one line.** Names shove for the front while a crowd shouts. dq's input rises out of the noise,
a name is typed, **Add name** is tapped, and everything freezes. The names then snap one by one into dq's numbered
list. "Next person" moves the line on. The camera dives into the blue Next-up row, and that blue becomes the end
card: "Where's the queue?" → **dq** (the q is the d, flipped) → `dq.withsholz.workers.dev`.

The look is dq's own light theme: ground `#f4f5fc`, navy `#121637`, blue `#2536d7` (`look.json`). Fonts are
Archivo Condensed and Inter.

## Beat sheet

| t (s) | beat | what carries into the next |
|---|---|---|
| 0.0–2.6 | the scrum: 7 name chips shove; 4 shouted words slam in (hard cuts, a burst) | the chips |
| 2.4–3.1 | dq's input card lands in the scrum and knocks it back; "Tunde Bakare" is typed; tap **Add name** | the card |
| 3.1–3.6 | freeze: picture still, sound cut to silence | — |
| 3.6–5.8 | the card opens into the phone; the typed name drops into row 1 (blue, Next up); the 7 chips hop into rows 2–8 | the names |
| 6.25–7.95 | hold: one calm line, 8 people waiting | the phone |
| 7.95–9.8 | tap "Tunde Bakare is done, next person": Tunde leaves, Amaka rises into the blue slot, numbers roll down | the blue slot |
| 9.85–10.6 | the camera dives into the blue slot until it fills the frame | the blue |
| 10.6–15 | "Where's the queue?" · the d drops, a copy flips over into the q · the URL pill grows out of the q's tail and types | dq |

## Re-render

```bash
python3 ../../.claude/skills/onetake/scripts/look.py apply look.json comp.html   # after any copy change
~/.cache/kokoro/venv/bin/python sound/voices.py sound/vo                       # crowd voices (Kokoro TTS)
python3 sound/dump_events.py comp.html && python3 sound/score.py              # → sound/sfx.wav
python3 ../../.claude/skills/onetake/scripts/render.py comp.html --out draft.mp4 --sfx sound/sfx.wav           # 1080p30
python3 ../../.claude/skills/onetake/scripts/render.py comp.html --out film.mp4 --final --sfx sound/sfx.wav    # 4K60
```

Preview in a browser: `comp.html?play`, or pin a frame with `comp.html?t=8.6&hud`.

## Licence note

onetake is PolyForm Noncommercial 1.0.0. Commercial use of what it makes needs onetake Pro (onetakemotion.com).
The crowd voices are synthesised with Kokoro (Apache-2.0 model), and the music and effects are synthesised here.
No third-party recordings are used.
