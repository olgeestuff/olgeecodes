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

## Frame 1 — Where is the queue?

- scene: navy ground; a comic crowd of shouting faces rises along the bottom; "WHERE IS THE QUEUE?" slams in white in three beats, "QUEUE?" in cobalt
- voiceover:
- onscreen: "WHERE" · "IS THE" · "QUEUE?"
- duration: 2s
- transition_in: cut
- status: built
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

## Frame 2 — The fight

- scene: comic panel — "Who's next??" from a crowd face, then three cartoon characters (Mike, Sandra, Dustin) side by side, each jabbing a thumb at themselves, speech bubbles stacking over each other; action lines; the panel shakes
- voiceover:
- onscreen: "Who's next??" · "I'm next on the queue!" · "No, it's me!" · "No, I'm next in the queue! 😤"
- duration: 5.5s
- transition_in: push-slide LEFT
- status: built
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

## Frame 3 — The comic page of problems

- scene: a 2×2 comic page fills panel by panel — (1) two characters waving different paper lists "Mike, Sandra, Dustin, Keer" vs "Keer, Mike, Sandra, Dustin" + burst "WHICH LIST?!"; (2) a host buried under "Add me!" / "Add me too!!" / "Me first!" bubbles; (3) a character with a magnifying glass: "Send the link again?" / "Which link??"; (4) a newcomer peeking in: "Hi, I'm new 👋 Is there a queue?" with a big "?"; then the whole page shakes and the bubbles pile up over it
- voiceover:
- onscreen: "WHICH LIST?!" · "Mike, Sandra, Dustin, Keer" · "Keer, Mike, Sandra, Dustin" · "Add me!" · "Add me too!!" · "Send the link again?" · "Which link??" · "Hi, I'm new 👋 Is there a queue?"
- duration: 5.5s
- transition_in: push-slide LEFT
- status: built
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

## Frame 4 — There's a better way

- scene: hard silence; the comic page freezes and dims; "There's a better way." settles in white; then the dq wordmark builds — the "d" drops in, a copy flips top-to-bottom into the "q"
- voiceover:
- onscreen: "There's a better way." · "dq"
- duration: 2s
- transition_in: cut
- status: built
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

## Frame 5 — Step 1: Create your dq

- scene: white ground; "STEP 1" eyebrow + "Create your dq"; a phone shows dq's start page (rebuilt from dq's code): "Friday Night Hot Seat" types into "Name your queue", the cobalt "Create queue" button presses, the page becomes the new queue with "Live · Nobody waiting" and "Your queue is ready"; caption "No sign-up. No app."
- voiceover:
- onscreen: "STEP 1" · "Create your dq" · "Friday Night Hot Seat" · "Create queue" · "Your queue is ready" · "No sign-up. No app."
- duration: 3s
- transition_in: zoom-through
- status: built
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

## Frame 6 — Step 2: Add to your list

- scene: "STEP 2" + "Add to your list"; same phone, owner view of "Friday Night Hot Seat": names type into "Add a name to the queue" and drop into the live list — Mike (1 · Next up, cobalt row), Sandra, Dustin, Keer — count ticks to "4 people waiting"
- voiceover:
- onscreen: "STEP 2" · "Add to your list" · "Mike" · "Sandra" · "Dustin" · "Keer" · "4 people waiting"
- duration: 3s
- transition_in: push-slide LEFT
- status: built
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

## Frame 7 — Step 3: Share your list

- scene: "STEP 3" + "Share your list"; on the phone "Copy list" is tapped → toast "4 names copied."; two comic bubbles pop OUT of the phone into the chat: "Mike, Sandra, Dustin, Keer" and the link "dq.withsholz.workers.dev/q/5h3bkjqg2y"; the cast from frames 2–3 reappear smiling: "✅ Got it!" "👍"; the newcomer Amaka taps the link → cobalt chip "Amaka, you are number 5"
- voiceover:
- onscreen: "STEP 3" · "Share your list" · "4 names copied." · "Mike, Sandra, Dustin, Keer" · "dq.withsholz.workers.dev/q/5h3bkjqg2y" · "✅ Got it!" · "Amaka, you are number 5"
- duration: 4s
- transition_in: push-slide LEFT
- status: built
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

## Frame 8 — dq is here 🔥

- scene: cobalt ground; "Where is the queue?" small in white; "dq is here 🔥" slams in big; the dq wordmark re-builds (d lands, flips into q); "dq.withsholz.workers.dev" types in below it in a white pill; "Free · No sign-up · No app" settles last and holds
- voiceover:
- onscreen: "Where is the queue?" · "dq is here 🔥" · "dq" · "dq.withsholz.workers.dev" · "Free · No sign-up · No app"
- duration: 5s
- transition_in: zoom-through
- status: built
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
