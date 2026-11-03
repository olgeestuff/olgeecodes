# Project notes for Claude

## AI video editor workflow
- Editor code: `editor/` (run `python editor/build_edit.py --body … --demo … --plan … --out …`).
  Per-video plans live in `AI video editors/plans/*.yaml`; exports go to `AI video editors/exports/`.
- Playbook for every video: clean audio (DeepFilterNet) → pause cutting → kallaway split layout
  (title, demo card on top, rounded face card at the bottom, 1–2 word captions) → story intro
  (`graphic: story` toons or `graphic: paperwork` cards) → short full-frame cuts (`full: true`)
  → demo segments timed to spoken words → cut retakes after the CTA (`end_after`) → SFX.
- The user (Sholz) loves the cartoon story intros (`graphic: story`); use them by default.
- Winning structure (Sholz's favourite): the cartoon acts out the story in parts, timed to his narration,
  then the B-roll switches to the **live demo** proving it works, with a short face cut in between. Keep this mix.
- AI-generated visuals (Veo, Canva): publishing files set TikTok "AI-generated content: On" and YouTube
  "Altered content: Yes". Code-drawn toons: both Off.

## After every finished video (standing instruction from the user)
When a video export is delivered, **ask Sholz whether he is ready for the publishing .md file**.
That file is written for **Claude in Chrome** to follow step by step: it sets up the post on each
platform (TikTok Studio, YouTube Studio, LinkedIn): upload, caption, hashtags, cover, settings,
disclosure ("Your brand" on TikTok, paid promotion unticked on YouTube), and schedule/post.
Save it next to the export as `<video name> - publish.md` and send it with SendUserFile.
Remind him that trending TikTok sounds can only be added in the mobile app.

## AI video clips from Gemini Veo (standing workflow)
- Sholz's Google AI Pro (Gemini, ~3 Veo videos/day, 8 s each) is on an Office Geek Tester account
  (likely officegeektester1). Claude Code cannot reach Gemini directly.
- For a video that needs richer cartoon B-roll, write `<video name> - veo brief.md` for **Claude in Chrome**:
  exact prompts per scene (flat 2D cartoon, 16:9, no text, no speech/music, our boss character described),
  exact file names (`hook N veo scene K.mp4`), download, then upload to Drive folder **veo vids**
  (id 1okvCi-dcKvf_lUPJNGjDYNig93jZhpQw, inside "teleprompter vids on office geek"); Sholz picks the files
  in the upload window.
- Character reference image: `AI video editors/references/characters/boss_reference.png` (Sholz puts it in veo vids).
- Fetch with `python editor/fetch_veo.py` → `raw footage/veo/`; splice with plan segments `file: raw footage/veo/<name>.mp4`.
- Canva AI video: ~1 clip/month (limit resets ~25th). Poppy: 2,775 image credits/month. Budget is tight: never buy credits.
