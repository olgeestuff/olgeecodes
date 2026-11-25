# Automation With Sholz: Content System (working memory)

Read this before any content, video or publishing work for Sholz. Last updated 25 Nov 2026.

## Operating principle: the Law of 100
- 100 pieces is the *beginning*, not the goal. Like push-ups: 1 or 10 is nothing.
- Judge a format or channel only after 100 posts.
- Each completed 100 counts as **one** on the tracker. 4 done so far (as of Nov 2026).
- Planned: a GitHub-style **heatmap calendar** to track daily output and each completed 100.

## The pipeline (target flow)
1. **Plan**: content ideas and production cards go on WordPress (automationwithsholz.wordpress.com).
2. **Script**: every card that needs filming gets a teleprompter file (text or Word) saved to Google Drive.
3. **Film**: Sholz reads from the teleprompter and uploads footage to a set Drive or WordPress folder.
   - He sometimes changes words. Use the card's narration as the reference, but keep his main point and his version.
4. **Edit**, by production type:
   - Filmed by Sholz: Claude edits (HyperFrames split screen, captions, brand). See `batch01/`.
   - AI-only or cartoon ideas: generated (HyperFrames, APIs).
   - Realistic animation: Google Omni/Flow (in the Google app; no public editing API).
5. **Triage**: Sholz judges and approves (not every video gets published).
6. **Publish**: Buffer schedules, one post per day at 8:00 AM Lagos time.

## Channels
| Channel | Role | Default |
|---|---|---|
| TikTok (`olgee0`) | Primary. Optimise captions and hashtags for TikTok. | Every video |
| LinkedIn (Shola Oginni) | Educational and business side | Every video by default |
| Facebook Page | "Third angle", low traction for now | Not connected in Buffer yet (1 free slot left) |

## Captions (every post must have one)
- Short, captivating, aligned with the video. Use curiosity, a question or a hot take: a psychological trigger.
- TikTok: 1–2 lines plus a consistent hashtag core: `#propertymanagement #landlord #appsheet` + 3 topical tags.
- LinkedIn: hook line, 3–5 short lines of story or lesson, a question, then 5 hashtags.
- Sholz reviews captions and wording. This is where he wants the final say.

## Coming next (not built yet)
- **TikTok playbook skill**: Sholz will bring a playbook from Google Drive (TikTok algorithm, hashtags, consistency). Turn it into a skill and apply it before creating and before publishing.
- **Character sheet**: Sholz's look, stance, posture and values, for cartoon or simulated versions of him.
- **Role characters**: recurring roles (e.g. a typical US landlord) to scale entertainment and story content. Open question: keep characters consistent, or keep roles consistent?
- **Triage phase**: sort and prioritise the content backlog by urgency and severity.
- **Law of 100 heatmap tracker.**

## Tools and settings
- Buffer (free plan: 3 channels, 10 scheduled posts per channel). Connected as a claude.ai connector.
- Video hosting for Buffer: public raw GitHub links pinned to a commit (this repo is public). WordPress upload rejected files of about 25 MB and up.
- Gemini API key is saved as a network secret (`x-goog-api-key`). Veo is not enabled (no billing); Lyria, image, TTS and transcribe models are available.
