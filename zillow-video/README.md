# My Failed Attempt at Making Zillow Without AI

Short-form video for **Automation With Sholz**, built with [Remotion](https://www.remotion.dev/).

| Output | Size | File |
| --- | --- | --- |
| Reels / TikTok / Shorts | 1080×1920 (9:16) | `out/zillow-vertical-9x16.mp4` |
| LinkedIn | 1080×1080 (1:1) | `out/zillow-linkedin-1x1.mp4` |

About 85 s: 80 s of edited voice and a 4.5 s end card.

## Story (edited voice track)

| # | Section | What is said (source time) |
| --- | --- | --- |
| 1 | Hook | "Making a Zillow alternative for a Singaporean client." (4:14) + "Back in 2023, somebody reached out to me on social media" (0:18) |
| 2 | The ask | "...and talked about his desires to manage properties for his team and for people that can come and search..." (0:23) |
| 3 | I was wrong | "All I knew, there was properties could be commercial, residential. I didn't know that it's a lot deeper..." + the 7 property types (1:11) |
| 4 | Search | "The most interesting thing he wanted was filters ... rent or sale, building name, district ... area, availability" (1:47) |
| 5 | The wall | "The only challenge was to get data ... scrape some data from the Singaporean residential database ..." (2:32) |
| 6 | Twist | "...my failure, which did not end up being a failure, because the person used it for his team..." (3:36) |
| 7 | Today | "Nowadays, you know, that's not an issue. Just get the data ... put it in your Sheets, use your AppSheet ... spin yourself a directory now" (2:46) |

The hook opens on the Zillow line (from 4:14) because the 0:13–0:40 parts run on as one sentence ("...reached out to me on social media *and talked about* his desires to manage properties...").

## How it was made

1. **Transcribe.** `scripts/transcribe.py` gives word-level timestamps (faster-whisper, Whisper small int8).
2. **Cut.** `scripts/build_edit.py` holds the edit decision list (word-index ranges per section). It snaps each cut to a quiet spot in the audio and shortens pauses longer than 0.3 s. It applies a high-pass, light compression and loudness normalisation to −14 LUFS. It writes `public/audio/voice.wav` and `src/data/edit.json` (caption words, section bounds, graphics cues on the edited timeline). Cuts where Whisper's word edges were off are pinned in `START_AT` / `END_AT`. The finished track was re-transcribed to check that no words were clipped or doubled.
3. **Caption fixes.** `FIX` in `build_edit.py` corrects Whisper mishearings: "Https" → HDB, "script" → scrape, "zero" → Zillow, "time" → data. The unclear word in "spin yourself a ___ directory" is left out of the captions.
4. **App footage.** `scripts/capture/*.js` drive the public AppSheet app with Playwright at 2× and record clips with the Chrome screencast. An init script blurs every `Contact …` column (name, mobile, tel, type, method) with CSS before first paint. It also blurs anything that looks like a phone number or email, so no frame shows them in the clear.
5. **Render.** `src/` holds the Remotion compositions `Vertical` and `Square`. Both share one timeline and switch layout by aspect ratio.

## Re-render

```bash
npm install
npm run render:vertical   # out/zillow-vertical-9x16.mp4
npm run render:square     # out/zillow-linkedin-1x1.mp4
npm run studio            # live preview / tweak timings
```

Set `REMOTION_BROWSER=/path/to/chrome-headless-shell` to use a local Chromium instead of Remotion's download.

To change the edit, adjust `EDL` / `CUES` in `scripts/build_edit.py`, then rerun it. It needs the source recording and the transcript JSON:

```bash
ffmpeg -i "My Failed Attempt at Making Zillow Without AI.mp4" -vn -ac 1 -ar 48000 source.wav
python -I scripts/transcribe.py <whisper-model-dir> source.wav transcript.json
python -I scripts/build_edit.py source.wav transcript.json public/audio/voice.wav src/data/edit.json
```

The word indices in `EDL`, `FIX` and `CUES` refer to the Whisper small (int8) transcript of the original recording. The transcript and the rendered MP4s are git-ignored (`scripts/transcript.json`, `out/`) because this repo is public; regenerate the transcript with the same model before changing the edit.

## Look

- Dark stage (`#0A0B0D`), one accent: orange `#FF5A1F`.
- Headlines in Anton, captions in Inter Black. The spoken word is highlighted in orange on a dark pill, so captions stay readable over the white app screens.
- Hero moment: "Residential / Commercial" → "I WAS WRONG" stamp → 7 tiles burst out on each spoken type (Non-landed, HDB, Landed, Retail, Office, Industrial, Whole buildings).
- Twist: "FAILED?" is struck through and replaced by "USED BY HIS TEAM".
- End card: "If you built your own property directory, what would you search by first?" with **Automation With Sholz**. No logo.
