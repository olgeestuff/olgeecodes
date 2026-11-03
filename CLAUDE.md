# Project notes for Claude

## AI video editor workflow
- Editor code: `editor/` (run `python editor/build_edit.py --body … --demo … --plan … --out …`).
  Per-video plans live in `AI video editors/plans/*.yaml`; exports go to `AI video editors/exports/`.
- Playbook for every video: clean audio (DeepFilterNet) → pause cutting → kallaway split layout
  (title, demo card on top, rounded face card at the bottom, 1–2 word captions) → story intro
  (`graphic: story` toons or `graphic: paperwork` cards) → short full-frame cuts (`full: true`)
  → demo segments timed to spoken words → cut retakes after the CTA (`end_after`) → SFX.
- The user (Sholz) loves the cartoon story intros (`graphic: story`); use them by default.

## After every finished video (standing instruction from the user)
When a video export is delivered, **ask Sholz whether he is ready for the publishing .md file**.
That file is written for **Claude in Chrome** to follow step by step: it sets up the post on each
platform (TikTok Studio, YouTube Studio, LinkedIn): upload, caption, hashtags, cover, settings,
disclosure ("Your brand" on TikTok, paid promotion unticked on YouTube), and schedule/post.
Save it next to the export as `<video name> - publish.md` and send it with SendUserFile.
Remind him that trending TikTok sounds can only be added in the mobile app.
