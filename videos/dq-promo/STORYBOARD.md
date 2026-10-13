---
format: 1080x1920
duration: 30s
message: "Where is the queue? dq is here — one link, everyone sees the line."
arc: PAS — Hook → Pain (who's next) → Agitation (list mess) → Solution tease → Step 1 → Step 2 → Step 3 → CTA
audience: hosts and speakers in chat rooms and audio rooms who fight over speaking order
mode: collaborative
music: none
narration: none — on-screen text carries every line; sound effects are host audio from the media-use library
---

# dq — 30s commercial (9:16)

No voiceover. Each frame's `onscreen:` cues are the "script": they pace the reveals the way a
voiceover normally would. Sound is placed as host SFX (bundled media-use library) at exact offsets in
`audio_meta.json` — pings on chat bubbles, an error buzz on the pile-up, whooshes on cuts, a bass hit
on "dq is here".

Characters are flat SVG cartoons (heads + shoulders, angry brows, open mouths), named from the
user's own list: Mike, Sandra, Dustin, Keer, plus Ada and Tolu (the new speaker). Chat windows are
generic (no real app branding): a group header "Friday Space 🎙️", bubbles with avatar + name.

## Frame 1 — Where is the queue?

- scene: "WHERE IS THE QUEUE?" slams onto a dq-red ground in three beats, chat pings firing behind it
- voiceover:
- onscreen: "WHERE" · "IS THE" · "QUEUE?"
- duration: 2s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Pain validation (the exact question every room asks)
- beat: tension + recognition
- blueprint: kinetic-type-beats
- asset_candidates:
- sfx_plan: ping ×2 under the words, impact-bass-1 on "QUEUE?"

narrativeRole: Opens on the viewer's own words — the question that starts every queue fight.
keyMessage: You've asked this. Everyone has.

## Frame 2 — Who's next? (the fight)

- scene: a group chat fills with cartoon people arguing; three of them shout over each other about who's next
- voiceover:
- onscreen: "Who's next??" · "Where is the queue?" · "I'm next on the queue!" · "No, it's me!" · "No, I'm next in the queue! 😤"
- duration: 5.5s
- transition_in: cut
- status: outline
- src: compositions/frames/02-fight.html
- type: pain_point
- persuasion: Pain agitation (dramatised argument)
- beat: frustration + comic recognition
- blueprint: kinetic-type-beats
- asset_candidates:
- sfx_plan: notification/ping on each bubble; pop on the fight trio; small glitch on the shake

narrativeRole: Shows the core pain — nobody knows the order, so people fight. Uses the user's exact three-way argument.
keyMessage: Without a real queue, every room becomes an argument.

## Frame 3 — The list mess

- scene: the chat keeps going — two pasted lists disagree, people beg to be added, links get lost, a new speaker asks for the queue — until bubbles pile up and bury the screen
- voiceover:
- onscreen: "QUEUE: Mike, Sandra, Dustin, Keer" · "No! It's Keer, Mike, Sandra, Dustin" · "WHICH LIST?" · "Add me to the queue!" · "Add me too!!" · "Send the link again?" · "Hi, I'm new 👋 Is there a queue?"
- duration: 5.5s
- transition_in: push-slide UP
- status: outline
- src: compositions/frames/03-list-mess.html
- type: pain_point
- persuasion: Pain agitation by accumulation (unagreed lists, copy-paste, lost links, newcomers)
- beat: overwhelm
- blueprint: overwhelm-surround
- asset_candidates:
- sfx_plan: ping on each bubble accelerating; error buzz as the pile buries the screen

narrativeRole: Stacks every secondary pain the user named — clashing pasted lists, "add me", re-sharing links, newcomers — into one overwhelming pile.
keyMessage: Copy-pasted lists and lost links make it worse.

## Frame 4 — There's a better way

- scene: the chaos freezes and drains to grey; "There's a better way." types in; the dq wordmark crashes in and shoves it aside
- voiceover:
- onscreen: "There's a better way." · "dq"
- duration: 2s
- transition_in: cut
- status: outline
- src: compositions/frames/04-better-way.html
- type: product_intro
- persuasion: Negative contrast (chaos frozen → calm)
- beat: relief + curiosity
- blueprint: ticker-takeover
- asset_candidates:
- sfx_plan: glitch-1 on the freeze; whoosh-short + impact-bass-2 as dq lands

narrativeRole: The turn — stops the chaos and names the fix.
keyMessage: dq is the fix.

## Frame 5 — Step 1: Create your dq

- scene: a phone shows dq's real start page — "Friday Space Q&A" typed in, tap Create — and the queue appears with "Your queue is ready"
- voiceover:
- onscreen: "STEP 1" · "CREATE YOUR DQ" · "No sign-up. No app."
- duration: 3s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/05-step-create.html
- type: feature_showcase
- persuasion: Friction reduction (real UI, one tap)
- beat: ease
- blueprint: device-surface-showcase
- asset_candidates: assets/02-home-typed.png — dq start page with "Friday Space Q&A" typed and the Create queue button; assets/03-queue-ready.png — "Your queue is ready" card with Copy queue link
- sfx_plan: click on Create; pop as the ready card lands

narrativeRole: Proves step 1 is trivial — name it, tap Create.
keyMessage: Making a queue takes one tap.

## Frame 6 — Step 2: Add to your list

- scene: on the same phone, names drop into the live queue one by one — Mike, Sandra, Dustin, Keer — each a beat, "4 people waiting"
- voiceover:
- onscreen: "STEP 2" · "ADD TO YOUR LIST" · "Mike" · "Sandra" · "Dustin" · "Keer"
- duration: 3s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/06-step-add.html
- type: feature_showcase
- persuasion: Show-don't-tell proof (the real live list)
- beat: control + clarity
- blueprint: device-surface-showcase
- asset_candidates: assets/04-list-0.png — empty owner view; assets/05-list-1.png — Mike added; assets/05-list-2.png — Mike, Sandra; assets/05-list-3.png — Mike, Sandra, Dustin; assets/05-list-4.png — all four, 4 people waiting
- sfx_plan: pop on each name (×4)

narrativeRole: Shows the order becoming one clear, numbered list — the answer to "who's next?".
keyMessage: One list, in order, that everyone can see.

## Frame 7 — Step 3: Share it anywhere

- scene: tap "Copy list" and "Share queue link" on the phone; the list "Mike, Sandra, Dustin, Keer" and the link pop out as bubbles into the same chats that were fighting — replies turn to ✅; the new speaker Tolu taps the link and joins at number 5
- voiceover:
- onscreen: "STEP 3" · "SHARE YOUR LIST" · "Mike, Sandra, Dustin, Keer" · "dq.withsholz.workers.dev/q/5h3bkjqg2y" · "✅ Got it!" · "Tolu, you are number 5"
- duration: 4s
- transition_in: push-slide LEFT
- status: outline
- src: compositions/frames/07-step-share.html
- type: benefit_highlight
- persuasion: Callback resolution (the same chats, now agreeing) + Social proof in the room
- beat: relief + belonging
- blueprint: grid-card-assemble
- asset_candidates: assets/06-list-copied.png — "4 names copied." toast after Copy list; assets/07-share.png — "Queue link copied." toast after Share queue link; assets/09-guest-joined.png — guest Tolu joined: "Tolu, you are number 5"
- sfx_plan: click on Copy list; whoosh + pop per pop-out bubble; chime on the ✅ replies

narrativeRole: Pays off the chaos — the pasted list and the link land in the chats, everyone agrees, newcomers join themselves.
keyMessage: Share by link or paste the list anywhere — the arguing stops.

## Frame 8 — dq is here 🔥

- scene: inverted close plate — "Where is the queue?" small, then "DQ IS HERE 🔥" slams in big; the dq wordmark, the URL and "Free · No sign-up · No app" lock up
- voiceover:
- onscreen: "Where is the queue?" · "dq is here 🔥" · "dq.withsholz.workers.dev" · "Free · No sign-up · No app"
- duration: 5s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/08-cta.html
- type: cta
- persuasion: Tagline callback + Risk reversal (free, no sign-up)
- beat: triumph + urgency-to-act
- blueprint: logo-assemble-lockup
- asset_candidates:
- sfx_plan: riser into impact-bass-1 on "dq is here 🔥"; sparkle on the URL

narrativeRole: Lands the user's tagline and tells the viewer exactly where to go.
keyMessage: dq.withsholz.workers.dev — free, no sign-up.
