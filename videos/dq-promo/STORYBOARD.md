---
format: 1080x1920
duration: 30s
message: "Where is the queue? dq is here — one link, everyone sees the line."
arc: PAS — Hook → Pain (the fight) → Agitation (comic page of problems) → Turn → Step 1 → Step 2 → Step 3 → CTA
audience: hosts and speakers in chat rooms and audio rooms who fight over speaking order
mode: collaborative
music: none
narration: none — on-screen text carries every line; an AI "angry mob" track (host audio) shouts under frames 1–3
version: 2
---

# dq — 30s commercial (9:16) · storyboard v2

## Changes from v1

User notes, verbatim: "i expect the color scheme to be just blue & white simple." · "dq currently
has no logo. so i guess dq is enough in text. maybe animated letters or whatever you recommend" ·
"at least with the https://dq.withsholz.workers.dev/ url below for emphasis" · "its nice to use the
apps in mockup devices or texts, lists and names types in on the app. like while in use" · "sound of
angry mob with voices yelling where's the queue? im next, im next !! … No im next !!" · "approved,
use the AI mob voices for now" · "hopefully therell be comics" · "and cartoons to depict the
problems".

So: blue & white only; comic-art cartoons for every problem; animated "dq" wordmark with the URL
under it; the app rebuilt in a phone mockup with text typing in live; AI mob voices under 0–13s.

## Decisions

- **Spine:** one cast of comic characters. They fight in frames 1–3, freeze in frame 4, and
  reappear calm in frame 7 when dq's list pops into their chat (callback). The "Friday Night Hot
  Seat" queue is the hero prop from frame 5 on.
- **Palette by role:** white `#FFFFFF` solution ground · dq navy `#0D1030` chaos ground · dq cobalt
  `#2536D6` (on navy `#3F51F2`) the only accent · dq ink `#14183A` text and comic ink lines. Nothing
  else (source: dq `public/index.html` tokens; user asked for blue & white).
- **Type:** Big Shoulders Display 800/900 (headlines, wordmark — dq's own face) · Inter 500–800
  (chat, labels, app body).
- **Comic style:** two-colour comic art — navy ink outlines (≈5px), white fills, cobalt flat
  shading, rounded speech bubbles with tails, short action lines, a few "!!" bursts. Faces simple
  and expressive (brows, open mouths). Characters: Mike, Sandra, Dustin, Keer, Amaka + crowd extras.
- **Bans:** no red, no yellow, no gradients, no glow, no hard offset shadows; no real chat-app
  logos; no fake dq features (only what the app does); no slideshow (every beat must build within
  itself) and no screensaver motion (every move says something).
- **Held frame:** frame 4 — the chaos freezes in silence; "There's a better way." lands still.
- **Seams:** leftward pushes for the step run; zoom-through at section turns.
- **Sound:** AI mob (host audio) 0–13.0s, hard cut to silence at 13.0; then SFX only (click, pop,
  whoosh, chime, bass hit). Each shouted line lands with its bubble.
- **Truthfulness:** every dq screen is rebuilt from dq's own markup/CSS and shows only real
  behaviour (create, add names, Copy list → "4 names copied.", Share queue link, guests join by
  link). The cartoons and chats are illustrations.

## Locked

User, after reviewing storyboard v2 sketches: "locked". Locked: the 8-frame order and timing, each
frame's layout and copy as drawn in `storyboard.html` v2, blue & white palette, comic cast, animated
dq wordmark with the URL under it, AI mob under 0–13s. Small nudges allowed only to clear the bottom
keep-out band (nothing load-bearing below y=1600).

## Video direction

- **Palette system (frame.md):** Act 1 frames 1–4 on `night` #0D1030 with `on-dark` text and white
  comic panels; Act 2 frames 5–7 on `bg` white with `text` ink headlines and the phone; frame 8 on
  `primary` cobalt with white. Cobalt is the one accent per frame (the "QUEUE?" block, a blue
  bubble, the "Next up" row, the URL). Comic art: ink #14183A outlines, white fills, cobalt shading.
- **Motion grammar:** smooth long-tail settles (`power3` / `expo.out` on fast arrivals) everywhere
  in Act 2 and frame 8. Act 1 is a comic, so speech-bubble pops and the fight's thumb jabs are the
  one explicitly playful exception: a small overshoot (`back.out(1.6)` at most) on bubble pops
  only. Every reveal lands on its sound cue (the mob line or SFX), never front-loaded. Shakes are
  short and decaying, finite. Aliveness in holds = subtle jitter on shouting heads only.
- **Rhythm / held frames:** frame 4's first 0.9s is a deliberate dead-still hold in silence (the
  turn); frame 8's last 1.5s holds still for the URL read. Frames 1–3 accelerate (mob builds to
  the frame-3 pile-up); frames 5–7 are calm, one action per beat.
- **Negative list:** no red, no yellow, no gradients, no glow, no hard offset shadows, no real
  chat-app logos, no invented dq features or numbers; no slideshow (everything dumped at t=0 then
  frozen) and no screensaver (many things floating independently, lazy breathing, back-half pans).
- **Keep-out:** load-bearing content stays above y=1600 (bottom 17% is the social-app UI zone).
  Character bodies may bleed off the bottom edge as decoration.
- **Registry check:** `hyperframes catalog` searched for "phone device mockup", "comic speech
  bubble", "chat messages conversation". `device-frame-stage` / `message-thread-reveal` exist but the
  locked sketch's plain dq-ink phone and two-colour comic bubbles are custom to this brand, so they
  are hand-authored.

## Frame 1 — Where is the queue?

- scene: navy ground; a comic crowd of shouting faces rises along the bottom; "WHERE IS THE QUEUE?" slams in white in three beats, "QUEUE?" in cobalt
- voiceover:
- onscreen: "WHERE" · "IS THE" · "QUEUE?"
- duration: 2s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Pain validation (the exact question every room asks)
- beat: tension + recognition
- blueprint: kinetic-type-beats
- asset_candidates:
- audio: mob "Where is the queue?!" at 0.15s; crowd bed swells in
- constraint: no logo, no product yet — pure pain

narrativeRole: Opens on the viewer's own words — the question that starts every queue fight.
keyMessage: You've asked this. Everyone has.

- blueprint: kinetic-type-beats (Adapt)
- focal: the "QUEUE?" cobalt block
- roles: typography-only; comic crowd = supporting foreground (bottom, bleeding off edge)
- sfx: host mob track (frame 1 → 13.0s); impact-bass-1 at 0.95s

Adapt: keep the statement-builds-across-beats onto a payoff slam; the field gains a rising comic crowd.
Scene 1 (0.0–0.5s): navy ground; "WHERE" slams in upper-left (kinetic beat-slam → `kinetic-beat-slam`); the crowd's back row starts rising from the bottom edge (staggered, smooth). Left-aligned stack, upper third, 3 depth layers (back row, front row, type).
Scene 2 (0.5–0.95s): "IS THE" slams in under it on the next beat; front-row faces rise; action lines flick in at the edges.
Scene 3 (0.95–1.45s): "QUEUE?" slams into its cobalt block (the payoff; scale-down slam on a fast `expo.out`), short decaying frame shake on impact; Mike's bubble "Where is the queue?!" pops (small overshoot).
Scene 4 (1.45–2.0s): hold; subtle jitter on the shouting heads only.

## Frame 2 — The fight

- scene: comic panel — "Who's next??" from a crowd face, then three cartoon characters (Mike, Sandra, Dustin) side by side, each jabbing a thumb at themselves, speech bubbles stacking over each other; action lines; the panel shakes
- voiceover:
- onscreen: "Who's next??" · "I'm next on the queue!" · "No, it's me!" · "No, I'm next in the queue! 😤"
- duration: 5.5s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-fight.html
- type: pain_point
- persuasion: Pain agitation (dramatised argument)
- beat: frustration + comic recognition
- blueprint: kinetic-type-beats
- asset_candidates:
- audio: mob "Who's next?!" 2.2s · "I'm next on the queue!" 3.3s · "No! It's me!" 4.3s · "No! I'm next in the queue!" 5.2s · "I'm next! I'm next!" 6.6s; pop on each bubble
- constraint: no text-only bubbles — every line comes out of a character

narrativeRole: The core pain — nobody knows the order, so people fight. The user's exact three-way argument.
keyMessage: Without a real queue, every room becomes an argument.

- blueprint: kinetic-type-beats (Adapt)
- focal: the three-character comic panel
- roles: illustration-only (comic cast Mike, Sandra, Dustin)
- sfx: pop at 0.2s, 1.3s, 2.3s, 3.2s, 4.6s (one per bubble); host mob track continues

Adapt: the escalating multi-beat statement is spoken by characters — each beat is a bubble from a new mouth, payoff = the biggest bubble + panel shake.
Scene 1 (0.0–0.6s): header "FRIDAY SPACE 🎙 · 248 MEMBERS" sits top-right as chrome; "Who's next??" bubble pops top-left at 0.2s (spring-pop, small overshoot → `spring-pop-entrance`).
Scene 2 (0.6–1.3s): the white comic panel rises into place (smooth); Mike, Sandra, Dustin rise into its bottom edge, staggered.
Scene 3 (1.3–2.3s): Mike's bubble "I'm next on the queue!" pops at 1.3s; his thumb jabs at himself (press → `press-release-spring`).
Scene 4 (2.3–3.2s): Sandra's "No, it's me!" pops at 2.3s; her thumb jabs; Mike keeps jittering.
Scene 5 (3.2–4.2s): Dustin's "No, I'm next in the queue! 😤" pops at 3.2s, the largest; action lines burst between them; the panel shakes (short, decaying).
Scene 6 (4.2–5.5s): Mike fires back "I'm next! I'm next!" (small bubble) at 4.6s; hold with subtle jitter on all three heads.

## Frame 3 — The comic page of problems

- scene: a 2×2 comic page fills panel by panel — (1) two characters waving different paper lists "Mike, Sandra, Dustin, Keer" vs "Keer, Mike, Sandra, Dustin" + burst "WHICH LIST?!"; (2) a host buried under "Add me!" / "Add me too!!" / "Me first!" bubbles; (3) a character with a magnifying glass: "Send the link again?" / "Which link??"; (4) a newcomer peeking in: "Hi, I'm new 👋 Is there a queue?" with a big "?"; then the whole page shakes and the bubbles pile up over it
- voiceover:
- onscreen: "WHICH LIST?!" · "Mike, Sandra, Dustin, Keer" · "Keer, Mike, Sandra, Dustin" · "Add me!" · "Add me too!!" · "Send the link again?" · "Which link??" · "Hi, I'm new 👋 Is there a queue?"
- duration: 5.5s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-problems.html
- type: pain_point
- persuasion: Pain agitation by accumulation (unagreed lists, copy-paste, lost links, newcomers)
- beat: overwhelm
- blueprint: overwhelm-surround
- asset_candidates:
- audio: mob "Which list?!" 7.9s · "Add me to the queue!" 9.1s · "Send the link again!" 10.2s · newcomer (calm) "Hi, I'm new. Is there a queue?" 11.3s; crowd bed peaks 12–13s; error buzz 12.4s
- constraint: one problem per panel, each a cartoon — not a wall of text

narrativeRole: Stacks every secondary pain the user named into one overwhelming comic page.
keyMessage: Copy-pasted lists, lost links and newcomers make it worse.

- blueprint: overwhelm-surround (Adapt)
- focal: the 2×2 comic page
- roles: illustration-only (Keer, Mike, the buried host, Dustin, Amaka)
- sfx: pop on each panel at 0.0s, 1.1s, 2.2s, 3.3s; error at 4.9s; host mob track peaks then cuts at the frame end

Adapt: accumulation = panels filling one by one, then bubbles close in from every edge and bury the page; no avatar morph.
Scene 1 (0.0–1.1s): panel 1 (top-left) snaps in; the two paper lists flip in tilted from opposite sides (→ `split-tilt-cards`); Keer and Mike glare; burst "WHICH LIST?!" slams across at 0.4s.
Scene 2 (1.1–2.2s): panel 2 (top-right) snaps in; the host's head appears and "Add me!", "Add me too!!", "Me first!", "Add me!!" pile in one after another, accelerating, covering him.
Scene 3 (2.2–3.3s): panel 3 (bottom-left) snaps in; Dustin with the magnifying glass sweeping; "Send the link again?" at 2.4s, "Which link??" answers at 2.9s.
Scene 4 (3.3–4.4s): panel 4 (bottom-right) snaps in; Amaka peeks up into it; "Hi, I'm new 👋 Is there a queue?" at 3.6s; the cobalt "?" pops at 4.0s.
Scene 5 (4.4–5.5s): overwhelm: the page shakes; small bubbles ("Who's next??", "Me next!", "Which list?", "Link??", "Add me!") rush in from all four edges, accelerating, and pile over the page (→ `center-outward-expansion` run inward); error buzz at 4.9s.

## Frame 4 — There's a better way

- scene: hard silence; the comic page freezes and dims; "There's a better way." settles in white; then the dq wordmark builds — the "d" drops in, a copy flips top-to-bottom into the "q"
- voiceover:
- onscreen: "There's a better way." · "dq"
- duration: 2s
- transition_in: cut
- status: animated
- src: compositions/frames/04-better-way.html
- type: product_intro
- persuasion: Negative contrast (noise → silence)
- beat: relief + curiosity
- blueprint: logo-assemble-lockup
- asset_candidates:
- audio: total silence 13.0–14.1s; whoosh-short 14.15s as the q flips
- constraint: held frame — nothing moves for the first 0.9s except the dim

narrativeRole: The turn — stops the chaos and names the fix.
keyMessage: dq is the fix.

- blueprint: logo-assemble-lockup (Adapt)
- focal: the dq wordmark
- roles: typography-only
- sfx: whoosh-short at 1.15s

Adapt: the mark comes to exist from one part — the d — whose copy flips top-to-bottom into the q; preceded by a still silent hold.
Scene 1 (0.0–0.9s): held frame in silence: the frozen comic page as a dim ghost grid; "There's a better way." settles in at 0.15s (smooth fade-up) and holds dead still.
Scene 2 (0.9–1.5s): the "d" drops into place below the line (smooth); at 1.15s a copy of the d flips top-to-bottom (rotationX through 180° on a fast settle) into the "q" beside it, landing in cobalt-bright.
Scene 3 (1.5–2.0s): hold the "dq" lockup still.

## Frame 5 — Step 1: Create your dq

- scene: white ground; "STEP 1" eyebrow + "Create your dq"; a phone shows dq's start page (rebuilt from dq's code): "Friday Night Hot Seat" types into "Name your queue", the cobalt "Create queue" button presses, the page becomes the new queue with "Live · Nobody waiting" and "Your queue is ready"; caption "No sign-up. No app."
- voiceover:
- onscreen: "STEP 1" · "Create your dq" · "Friday Night Hot Seat" · "Create queue" · "Your queue is ready" · "No sign-up. No app."
- duration: 3s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/05-step-create.html
- type: feature_showcase
- persuasion: Friction reduction (one tap, real UI)
- beat: ease
- blueprint: device-surface-showcase
- asset_candidates: assets/02-home-typed.png — reference for the rebuilt start page; assets/03-queue-ready.png — reference for the "Your queue is ready" state
- audio: key-press ticks while typing; click on Create 16.6s; pop as the ready card lands
- constraint: the app UI is dq's own markup/CSS — no invented controls

narrativeRole: Proves step 1 is trivial — name it, tap Create.
keyMessage: Making a queue takes one tap.

- blueprint: device-surface-showcase (Adapt)
- focal: the phone with dq's start page (rebuilt from dq's own CSS)
- roles: assets/02-home-typed.png, assets/03-queue-ready.png = layout references for the rebuilt UI (not placed)
- sfx: key-press ×6 across 0.55–1.5s; click at 1.6s; pop at 2.0s

Adapt: static device hold (no 3D push); the screen changes state through typing and a tap.
Scene 1 (0.0–0.5s): white ground; "STEP 1" pill and "Create your dq" enter (per-word staggered → `dynamic-content-sequencing`); the phone rises into place (smooth). Headline upper band, phone centered below, ~60% of frame.
Scene 2 (0.5–1.6s): "Friday Night Hot Seat" types into "Name your queue" behind a caret (type-on → `discrete-text-sequence`).
Scene 3 (1.6–1.9s): a tap ripple lands on "Create queue"; the button presses (→ `cursor-click-ripple`).
Scene 4 (1.9–2.6s): the screen swaps to the new queue: "Friday Night Hot Seat", "● Live · Nobody waiting", and the "Your queue is ready" card rises in.
Scene 5 (2.6–3.0s): "No sign-up. No app." fades up below the headline; hold.

## Frame 6 — Step 2: Add to your list

- scene: "STEP 2" + "Add to your list"; same phone, owner view of "Friday Night Hot Seat": names type into "Add a name to the queue" and drop into the live list — Mike (1 · Next up, cobalt row), Sandra, Dustin, Keer — count ticks to "4 people waiting"
- voiceover:
- onscreen: "STEP 2" · "Add to your list" · "Mike" · "Sandra" · "Dustin" · "Keer" · "4 people waiting"
- duration: 3s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-step-add.html
- type: feature_showcase
- persuasion: Show-don't-tell proof (the real live list)
- beat: control + clarity
- blueprint: device-surface-showcase
- asset_candidates: assets/04-list-0.png — empty owner view reference; assets/05-list-4.png — four names, 4 people waiting reference
- audio: pop on each name (×4)
- constraint: one numbered list — the visual answer to "who's next?"

narrativeRole: Shows the order becoming one clear numbered list everyone can see.
keyMessage: One list, in order.

- blueprint: device-surface-showcase (Adapt)
- focal: the phone's live list (rebuilt from dq's own CSS)
- roles: assets/04-list-0.png, assets/05-list-4.png = layout references for the rebuilt UI (not placed)
- sfx: pop at 0.85s, 1.4s, 1.95s, 2.5s

Adapt: same static device hold as frame 5, same phone position; names type in and drop into rows.
Scene 1 (0.0–0.4s): "STEP 2" pill and "Add to your list" enter; the phone is already in place (queue page, nobody waiting).
Scene 2 (0.4–2.6s): four beats, ~0.55s each: a name types into "Add a name to the queue", then drops into the list as a row (Mike → cobalt "Next up" row; Sandra; Dustin; Keer); the count text steps "1 person waiting" → "4 people waiting".
Scene 3 (2.6–3.0s): hold on the finished list.

## Frame 7 — Step 3: Share your list

- scene: "STEP 3" + "Share your list"; on the phone "Copy list" is tapped → toast "4 names copied."; two comic bubbles pop OUT of the phone into the chat: "Mike, Sandra, Dustin, Keer" and the link "dq.withsholz.workers.dev/q/5h3bkjqg2y"; the cast from frames 2–3 reappear smiling: "✅ Got it!" "👍"; the newcomer Amaka taps the link → cobalt chip "Amaka, you are number 5"
- voiceover:
- onscreen: "STEP 3" · "Share your list" · "4 names copied." · "Mike, Sandra, Dustin, Keer" · "dq.withsholz.workers.dev/q/5h3bkjqg2y" · "✅ Got it!" · "Amaka, you are number 5"
- duration: 4s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/07-step-share.html
- type: benefit_highlight
- persuasion: Callback resolution (the same cast, now agreeing) + belonging
- beat: relief + belonging
- blueprint: grid-card-assemble
- asset_candidates: assets/06-list-copied.png — "4 names copied." toast reference; assets/07-share.png — "Queue link copied." toast reference; assets/09-guest-joined.png — guest joined reference
- audio: click on Copy list 21.6s; whoosh + pop per pop-out; chime on "✅ Got it!"
- constraint: the replies come from the same characters who were fighting

narrativeRole: Pays off the chaos — the list and link land in the chat, everyone agrees, newcomers join themselves.
keyMessage: Share by link or paste the list anywhere — the arguing stops.

- blueprint: grid-card-assemble (Adapt)
- focal: the list bubble "Mike, Sandra, Dustin, Keer"
- roles: assets/06-list-copied.png, assets/07-share.png, assets/09-guest-joined.png = references for toast / link / joined state (not placed)
- sfx: click at 0.6s; whoosh-short at 1.0s and 1.6s; pop at 1.2s and 1.8s; chime at 2.4s; pop at 3.2s

Adapt: the cascade is bubbles flying out of the phone and assembling as a short chat stack, then the cast's replies.
Scene 1 (0.0–0.4s): "STEP 3" pill and "Share your list" enter; the phone (smaller, left) shows the 4-name list.
Scene 2 (0.4–1.0s): a tap ripple on "Copy list" at 0.6s; toast "4 names copied." slides down inside the phone.
Scene 3 (1.0–1.6s): the cobalt bubble "Mike, Sandra, Dustin, Keer" flies out of the phone to the right and lands (fast arrival, smooth settle).
Scene 4 (1.6–2.2s): the link bubble "dq.withsholz.workers.dev/q/5h3bkjqg2y" flies out and lands under it.
Scene 5 (2.2–3.0s): Mike and Sandra (now smiling) rise in beside the bubbles; "✅ Got it!" pops at 2.4s.
Scene 6 (3.0–4.0s): Amaka (smiling) rises lower-left; the cobalt chip "Amaka, you are number 5" springs in at 3.2s; hold.

## Frame 8 — dq is here 🔥

- scene: cobalt ground; "Where is the queue?" small in white; "dq is here 🔥" slams in big; the dq wordmark re-builds (d lands, flips into q); "dq.withsholz.workers.dev" types in below it in a white pill; "Free · No sign-up · No app" settles last and holds
- voiceover:
- onscreen: "Where is the queue?" · "dq is here 🔥" · "dq" · "dq.withsholz.workers.dev" · "Free · No sign-up · No app"
- duration: 5s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/08-cta.html
- type: cta
- persuasion: Tagline callback + risk reversal (free, no sign-up)
- beat: triumph + urgency-to-act
- blueprint: logo-assemble-lockup
- asset_candidates:
- audio: riser 25.0s into impact-bass-1 on "dq is here 🔥" 26.0s; key-press ticks on the URL; sparkle 28.2s
- constraint: the last 1.5s holds still so the URL can be read

narrativeRole: Lands the user's tagline and tells the viewer exactly where to go.
keyMessage: dq.withsholz.workers.dev — free, no sign-up.

- blueprint: logo-assemble-lockup (Reproduce)
- focal: the dq wordmark + URL pill
- roles: typography-only
- sfx: riser at 0.0s; impact-bass-1 at 1.0s; key-press ×5 across 1.5–2.6s; sparkle at 3.2s

Reproduce: the mark builds (d lands, copy flips into q), resolves into a centered lockup and extends to the URL / CTA end card.
Scene 1 (0.0–0.6s): cobalt ground; "Where is the queue?" settles in at the top (white, 72%).
Scene 2 (0.6–1.0s): the giant "d" lands center; its copy flips top-to-bottom into the "q" as the riser peaks.
Scene 3 (1.0–1.5s): "is here 🔥" slams in under the wordmark on the bass hit (→ `kinetic-beat-slam`).
Scene 4 (1.5–2.8s): the white pill grows in and "dq.withsholz.workers.dev" types into it (type-on → `discrete-text-sequence`).
Scene 5 (2.8–3.5s): "Free · No sign-up · No app" fades up under the pill.
Scene 6 (3.5–5.0s): hold dead still — the final read.
