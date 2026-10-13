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
narration: no
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

- On-screen text + sound effects, no voiceover, no music bed (no music source reachable in this
  environment). SFX from the bundled media-use library: chat pings, error buzz, whooshes, a big hit
  on "dq is here".
- Flat cartoon characters drawn in SVG (no photo caricatures).
- Chaos montage: six pain points at roughly 2s each, rapid-fire, rather than separate scenes.
- Step 3 gets extra time: the clean list "Mike, Sandra, Dustin, Keer" and the queue link pop out
  into the same chat windows that were fighting earlier — everyone now agrees.
- End card: "Where is the queue? dq is here 🔥" + dq wordmark + dq.withsholz.workers.dev +
  "Free · No sign-up · No app".

## Notes

- Brand truth comes from the dq source repo (`/home/user/dq/public/index.html`): cobalt #2536D6,
  marigold #FFC233 (text on marigold #14183A), ink #14183A, paper #F4F5FB, surface #FFFFFF, muted
  #555B78, line #D6D9EA, live green #17784A; display font Big Shoulders Display (embedded subset,
  OFL), body system-ui. Real copy: "One link. Everyone sees the line." "Copy list", "Share queue
  link", "Join queue", "Done, next person".
- The live URL did not resolve (DNS not found) from this environment; the app's real screens are
  captured by running the dq repo locally. On-screen URL as the user asked: "dq.withsholz.workers.dev"
  (no https, no trailing slash). The user should confirm the link opens before posting.
- Timeline agreed with the user: 0–2s hook "WHERE IS THE QUEUE?"; 2–13s chat chaos; 13–15s freeze
  "There's a better way."; 15–18s step 1 Create; 18–21s step 2 Add names; 21–25s step 3 Share with
  pop-outs; 25–30s tagline + end card.
- Avoid real chat-app logos or trademarks; use generic chat windows.
