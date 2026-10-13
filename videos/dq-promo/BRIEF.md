---
workflow: product-launch-video
flow: automation
storyboard: yes
message: "Where is the queue? dq is here — one link, everyone sees the line."
destination: social-vertical
aspect: 1080x1920
language: en
audience: hosts and speakers in chat rooms and audio rooms (X Spaces, Clubhouse, Discord stages, WhatsApp/Telegram groups) who fight over speaking order
length: 30s
angle: problem-agitate-solve — chat-room queue chaos, then dq's 3 easy steps, then the tagline
narration: no — AI "angry mob" voices as sound design (frames 1–3)
---

## Intent

A 30-second commercial that sells dq (a free shared queue anyone can join with a link). It opens on
the chaos of running a speaking queue inside a chat room, shows how dq fixes it in three easy steps,
and lands on Sholz's tagline: "where is the queue? dq is here 🔥". Fun, punchy, a little cheeky —
cartoon people arguing, then calm and clarity once dq arrives. Built to be watched on a phone, with
sound off or on.

The user's own pain points (keep their wording where it fits):

- caricatures / cartoons of people arguing and fighting about who's next — "where is the queue?",
  "add me to the queue" in chatrooms
- the three-way fight: "I'm next on the queue!" / "No, it's me!" / "No, I'm next in the queue!"
- unagreed lists
- copying lists into chats and pasting: "mike, sandra, dustin, Keer"
- links shared around
- new speakers asking for the queue

The user's 3 steps ("it's easy to use"):

1. Create dq (the queue)
2. Add to your list
3. Share the list — via link, or by copying and pasting the list anywhere. Show the shared list and
   the pasted list popping out into the chats.

Closing line, verbatim: "where is the queue? dq is here 🔥"

## Customizations

Plan v2, approved by the user ("approved, use the AI mob voices for now"):

- **Colors: "just blue & white, simple."** dq cobalt + white, dq ink text; chaos frames on dq's
  dark-mode navy with white type. No red, no yellow. Design preset switched from blockframe to
  blue-professional, hand-mapped to dq tokens.
- **Comics + cartoons depict every problem** (user: "hopefully there'll be comics", "and cartoons to
  depict the problems"). Two-colour comic art: navy ink outlines, white fills, cobalt shading,
  speech bubbles, action lines. One cartoon vignette per problem: shouting crowd ("where is the
  queue?"); three characters thumbing at themselves (the fight); two characters waving different
  paper lists (unagreed lists); host buried under "add me" bubbles; character searching with a
  magnifying glass ("send the link again?"); newcomer peeking in with a "?" (new speakers).
- **Logo:** dq has no logo — animated wordmark: the "d" lands, a copy flips vertically into the "q".
  URL "dq.withsholz.workers.dev" types in below it for emphasis.
- **App shown "while in use":** the dq screens are rebuilt from dq's own markup/CSS in a phone
  mockup so text types in live: queue title "Friday Night Hot Seat" (from the user's screenshots),
  Create tapped, names Mike, Sandra, Dustin, Keer typed in and dropping into the list, the
  "4 names copied." toast; new speaker Amaka (from the user's screenshots) joins by link → "Amaka,
  you are number 5".
- **Sound:** AI angry-mob voices (Kokoro, offline) shouting the user's lines under frames 1–3, hard
  cut to silence on "There's a better way."; SFX from the bundled media-use library (pings, pops,
  whooshes, bass hit on "dq is here"). No music bed.
- Chaos montage: six pain points at roughly 2s each, rapid-fire, rather than separate scenes.
- Step 3 gets extra time: the clean list "Mike, Sandra, Dustin, Keer" and the queue link pop out
  into the same chat windows that were fighting earlier — everyone now agrees.
- End card: "Where is the queue?" → "dq is here 🔥" + animated dq wordmark + dq.withsholz.workers.dev
  below it + "Free · No sign-up · No app".

## Assets

- capture/assets/user-reference/1.webp … 5.webp — the user's own screenshots of the live dq app
  ("Friday Night Hot Seat", names Tunde Bakare, Amaka Obi, Chidi Nwosu…, light and dark mode).
  Reference for copy and names; the video rebuilds the UI from dq's source instead.

## Notes

- Brand truth comes from the dq source repo (`/home/user/dq/public/index.html`): cobalt #2536D6,
  ink #14183A, paper #F4F5FB, surface #FFFFFF, muted #555B78, line #D6D9EA, dark-mode paper #0D1030
  (the user wants blue & white only — marigold/red are not used in the video frames); display font Big Shoulders Display (embedded subset,
  OFL), body system-ui. Real copy: "One link. Everyone sees the line." "Copy list", "Share queue
  link", "Join queue", "Done, next person".
- The live URL did not resolve (DNS not found) from this environment; the app's real screens are
  captured by running the dq repo locally. On-screen URL as the user asked: "dq.withsholz.workers.dev"
  (no https, no trailing slash). The user should confirm the link opens before posting.
- Timeline agreed with the user: 0–2s hook "WHERE IS THE QUEUE?"; 2–13s chat chaos; 13–15s freeze
  "There's a better way."; 15–18s step 1 Create; 18–21s step 2 Add names; 21–25s step 3 Share with
  pop-outs; 25–30s tagline + end card.
- Avoid real chat-app logos or trademarks; use generic chat windows.
