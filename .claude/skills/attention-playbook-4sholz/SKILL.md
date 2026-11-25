---
name: attention-playbook-4sholz
description: Sholz's attention and persuasion playbook for short-form content (Automation With Sholz). Use it whenever planning content ideas, writing a video script, hook, on-screen text, teleprompter narration, caption or hashtags, scheduling posts to TikTok, LinkedIn or Facebook, or reviewing how a post performed. It combines Sam's TikTok algorithm playbook (retention, TikTok SEO, Creator Search Insights), Adley's "entertain the masses, educate the interested, sell to the committed", Russell Brunson's health/wealth/relationships, Eugene Schwartz's awareness levels, Ogilvy's proof-over-adjectives rule, the 11 Laws of Content Creation, and the Law of 100. Platform-specific rules live in references/ so new algorithm notes can be added.
---

# Attention Playbook 4 Sholz (Automation With Sholz)

**Version 1.2.0** (25 Nov 2026). See `CHANGELOG.md`.

**Mission:** design every piece of content so the behaviour we want (watch time, saves, shares, comments, follows) is the *rational* response for a scrolling human, and for the platform's algorithm that measures those humans.

- **Game theory:** given the platform's rules, what will viewers and the algorithm do?
- **Mechanism design:** what do we put in the video, text and caption so the behaviour we want emerges?

Persuade with truth and proof, never with deception. Engagement bait, fake claims, follow-for-follow and bought views corrupt the signal and teach the algorithm the wrong audience (Sam, rule 7).

## Load what you need
| Task | Read |
|---|---|
| Any content task | `references/principles.md` (always) |
| TikTok script, caption, hashtags or scheduling | `references/tiktok.md` |
| LinkedIn post | `references/linkedin.md` |
| Facebook post | `references/facebook.md` |
| Writing captions for any platform | `references/captions.md` |
| Grading a script or caption before filming or posting | `references/scorecard.md` |
| Reviewing results | the post-mortem section of `references/tiktok.md` |
| Exact original wording | `sources/` (Sholz's untouched notes) |

## Modes

### 1. Plan (content ideas)
1. **Pick the pillar.** Tie each idea to one of Brunson's three desires: **wealth** (money, time, efficiency), **health** (stress, overwhelm, peace of mind) or **relationships** (tenants, team, contractors, clients, family time).
2. **Pick the job,** following Adley: **Entertain** (masses: story, joke, skit, tune, character), **Educate** (interested: how-to, mechanism, demo) or **Sell** (committed: offer, case, CTA). Aim for mostly entertain plus educate. Selling is earned.
3. **Pick the awareness level** (Schwartz) the viewer is at: unaware, problem-aware, solution-aware, product-aware or most-aware. Cold feeds are mostly unaware or problem-aware, so lead with the problem or the story, not the product.
4. **Generate in volume** with the **STD grid** (Adley): 10 Struggles × 10 Topics × 10 Desires, mixed and matched. Law of 100: ideas come in hundreds.
5. **On TikTok, check demand first.** Prompt Sholz to look at **Creator Search Insights**, especially the **Content Gaps** tab, for what his audience searches and what is under-served. See `references/tiktok.md`.

### 2. Script / teleprompter
Every script must state these (Sam, rule 7):
- the **one idea**
- the **target search phrase**
- the **hook**, verbatim first line, spoken
- the **on-screen text** for the first frame
- a **beat column** with a pattern interrupt every 3–5 seconds
- the **payoff line**, within 20 seconds of the hook
- the **loop or close**
- the **CTA**, phrased as intent ("save this for…")
- **3–5 specific hashtags**
- the **suggested length**: the shortest that delivers the payoff

The hook must **create an emotion and leave an unanswered question** (Adley). Use **proof, not adjectives** (Ogilvy).

### 3. Caption and publish
Follow `references/captions.md` and the platform file. Every post carries a caption: a hook line that triggers curiosity, a question or a hot take, aligned with the video. TikTok is the primary platform. LinkedIn is for educational and business content. Facebook is the third angle.

### 4. Review (post-mortem)
Diagnose in this order: retention graph → hook → pacing → promise/payoff match → metadata. Never start with "the algorithm". Test one variable at a time. Judge after 100 posts, not after 3.

## Hard rules (reject your own output if any fail)
- More than one idea in one video → split it into two videos.
- The hook promises something the payoff doesn't deliver.
- It sells before it gives value. The CTA asks before it gives.
- The hashtags are generic (#fyp, #viral) instead of specific.
- It uses empty adjectives (premium, best, powerful, seamless) instead of a specific proof, number or picture.
- It reads like an ad. Native and human beats polished.
- It isn't tied to the one message Sholz keeps repeating (Law of messaging): *small service businesses can run on simple apps built on the Google tools they already pay for.*

## Hashtag layers (niche-proof)
Brand core (always): AppSheet + Google Workspace → niche (currently property management; swap on a niche change) → 1–2 topic tags. Sholz's expertise is the constant; the niche can change.

## Sholz's own operating laws
- **Law of 100:** 100 is the beginning. Count output in hundreds. Each completed 100 counts as one on the tracker.
- **The teleprompter is the source.** Sholz reads the card's narration but may change words. Keep his main point and his version.
- **Sholz judges.** Claude drafts ideas, scripts and captions. Sholz has the final say on what is published and on the wording.
- Pipeline details and defaults: `CONTENT-SYSTEM.md` at the repo root, when available.

## Updating this playbook ("Update the playbook")
1. Read new or changed notes in the Google Drive folder **Playbooks of Interest Media** (id `1pVQWLFod26ALrXRJW-ySPFZw330iNGW6`).
2. Save each note word for word in `sources/`, named `<platform-or-topic>-<author>.md`.
3. Merge the rules into the right file: `principles.md` for rules that apply everywhere, `tiktok.md` / `linkedin.md` / `facebook.md` for one platform, or a new `<platform>.md`, added to the table above.
4. Bump the version (new source or file = minor, wording fix = patch), add a dated line to `CHANGELOG.md`, and rebuild `dist/attention-playbook-4sholz.zip`. Keep the zip name the same so the link never breaks.
