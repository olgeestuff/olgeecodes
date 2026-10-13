# Asset Descriptions

Source: the dq app (`olgeestuff/dq`) run locally with `wrangler dev`, because the public URL did not
resolve from this environment. `hyperframes capture http://127.0.0.1:8787/` supplied tokens, text and
the full-page plate. The phone screens below were taken by driving the real UI on a 390x844 phone
viewport at 3x (1170x2532 px each, light theme). Every screen is genuine app output — nothing is
mocked.

No logo file exists: the dq brand mark is the wordmark "dq" set in Big Shoulders Display 800
(top-left of every page). Rebuild it as live text with the brand font; do not draw a symbol.

## Phone screens (assets/screens/, 1170x2532)

- screens/01-home-empty.png — dq start page: "dq" wordmark, hero "One link. Everyone sees the line.", lede, empty "Name your queue" field + cobalt "Create queue" button, "How it works" steps 1–3 (step 1 highlighted cobalt).
- screens/02-home-typed.png — same start page with "Friday Space Q&A" typed into "Name your queue"; focus ring on the field; "Create queue" button ready. Best shot for STEP 1 (Create your dq).
- screens/03-queue-ready.png — new queue "Friday Space Q&A", green "Live · Nobody waiting", "Your queue is ready" card with cobalt "Copy queue link" and "Copy owner link". Good for STEP 1 payoff / STEP 3 link.
- screens/04-list-0.png — owner view, empty queue: "Add a name to the queue" field + "Add name" button, nobody waiting.
- screens/05-list-1.png — owner view after adding Mike: Mike #1 in a cobalt "Next up" row.
- screens/05-list-2.png — Mike, Sandra.
- screens/05-list-3.png — Mike, Sandra, Dustin.
- screens/05-list-4.png — Mike, Sandra, Dustin, Keer; "4 people waiting"; "Mike is done, next person" button; "Copy list" button. Sequence 04→05-1→05-2→05-3→05-4 is STEP 2 (names drop in live).
- screens/06-list-copied.png — same list with toast "4 names copied." at the top after tapping "Copy list". Clipboard verified as "Mike, Sandra, Dustin, Keer". Best shot for STEP 3 (copy & paste the list anywhere).
- screens/07-share.png — same list with toast "Queue link copied." after tapping "Share queue link". STEP 3 (share by link).
- screens/08-guest-open.png — a guest opening the shared queue link on another phone: list + "Your name" / "Join queue".
- screens/09-guest-joined.png — guest "Tolu" joined: marigold card "5 · Tolu, you are number 5 · 4 people are ahead of you", list with Tolu tagged "You". Proof that new speakers just join themselves.
- screens/10-owner-live.png — owner's screen after Tolu joined from the link: 5 people waiting, live.

## Full-page plate (screenshots/)

- screenshots/full-page.png — desktop-width start page (1920 wide), from `hyperframes capture`.

## Fonts (assets/fonts/)

- fonts/big-shoulders-display-latin-800-normal.woff2 — brand display face, weight 800 (full Latin, from @fontsource; the app embeds only a subset). OFL, see fonts/BigShouldersDisplay-OFL.txt.
- fonts/big-shoulders-display-latin-900-normal.woff2 — weight 900 for the heaviest hook type.

## Icons (assets/svgs/)

- svgs/svg-21e8dac5.svg — the app's "×" close icon (stroke). Not a logo.
