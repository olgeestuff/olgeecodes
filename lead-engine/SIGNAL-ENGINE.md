# Signal Engine + DM Play

This supersedes the bulk-sourcing emphasis in `BUILD-PLAN.md`. Bulk lists were the wrong centre
of gravity. **Signal monitoring feeding signal-personalised DMs is the product.**

---

## 0. The finding that reorders everything

Live test on the Upwork API, 2026-11-26, same account, same minute:

| Query | Relevant results |
|---|---|
| `AppSheet` — the *solution* word | **0 / 10** (all generic mobile-app dev) |
| `google sheets tracking spreadsheet replace app` — *symptom* language | **9 / 10** |

**People in pain do not know the name of your solution.** They know their symptom. Every hour
spent on better search tech or smarter models before fixing query vocabulary is wasted.

Order of work: **vocabulary → recall fan-out → LLM processing.** In that order, always.

---

## 1. The two signal temperatures (and why both matter)

| | Hot: declared budget | Warm: declared pain |
|---|---|---|
| **Where** | Upwork/Fiverr job posts | LinkedIn posts, Reddit, forums |
| **Competition** | Brutal — 20–50 proposals, invites already out | **None** |
| **You win on** | **Speed.** Be first, in under an hour. | **Relevance.** Reference the signal. |
| **Channel** | Proposal | **Connect + DM** |
| **Volume** | Low | High |

The warm column is where your Origami invite play already works, and it is uncontested. That is
the asymmetry to exploit. The hot column is a speed game you can win with a monitor and a
notification, not with better data.

**The signal is what makes the invite get accepted.** "Saw your post about the double-bookings"
is a different animal from a cold connect. Signal monitoring and DM marketing are one system.

---

## 2. Vocabulary: the symptom taxonomy

This is the asset. Build it once, reuse it on every source. Search these, never "AppSheet."

**Spreadsheet strain**
`outgrown spreadsheets` · `google sheet is a mess` · `too many tabs` · `formulas keep breaking`
`sheet keeps breaking when` · `spreadsheet nightmare` · `manual data entry every day`
`copying between sheets` · `version of the spreadsheet`

**Paper / whiteboard**
`still using paper` · `paper job cards` · `carbon copy forms` · `whiteboard scheduling`
`clipboard` · `job sheets by hand` · `photos of receipts`

**Software cost pain** (highest intent in this group)
`too expensive per user` · `cancel our subscription` · `cheaper alternative to` · `[Jobber|
ServiceTitan|Tradify|SimPRO|monday] too expensive` · `paying for seats we don't use`

**Operational bleeding**
`double booked` · `techs forget to` · `can't see what's happening in the field`
`chasing timesheets` · `no job photos` · `stock count is always wrong` · `missed invoice`

**Build intent** (hot, but crowded)
`appsheet developer` · `glide app` · `convert sheet to app` · `no code app for my business`
`internal tool for my team`

Rule: a query names a **symptom, a cost complaint, or a competitor's product** — never your tool.

---

## 3. Sources, ranked by intent density

| # | Source | Access | Intent | Notes |
|---|---|---|---|---|
| 1 | **Upwork job posts** | **Upwork MCP, already connected** | Highest — budget declared | Speed game. Monitor hourly. |
| 2 | **Reddit** | Official API, free | High | r/smallbusiness, r/Entrepreneur, r/HVAC, r/Construction, r/plumbing, r/landscaping, r/googlesheets, r/nocode, r/sheets. Pain described in full paragraphs — ideal LLM input. |
| 3 | **LinkedIn posts** | **Apify keyword monitor, already wired** | Medium-high | Uncontested. Feeds the invite+DM play. |
| 4 | AppSheet / Glide community forums | Scrape or RSS | Medium | People stuck mid-build, or out of their depth. |
| 5 | Fiverr buyer requests | Manual | Medium | No clean API. |
| 6 | X / Facebook groups | Hard | Low-medium | Skip in v1. |

You already own #1 and #3. Add #2 — it's free and it's the richest text.

---

## 4. Processing: score, don't just filter

Cheap model (Haiku/Flash), one call per candidate, JSON out. Four axes, 0–2 each:

- **Pain** — is a real operational problem described, in their own words?
- **Authority** — owner/manager, or an employee venting?
- **Timing** — active now ("this week", "just lost"), or an old grumble?
- **Reachability** — is there a profile or company to reach, and a channel?

Output per row: `score`, `signal_quote` (their exact words), `pass_reason`, `suggested_opener`.

**Always store the verbatim quote.** It is the DM's first line, it is your proof of quality to a
client, and it is how you debug a bad prompt.

Routing:

| Score | Source | Action |
|---|---|---|
| 6–8 | Upwork | Proposal within 60 min. Alert to phone. |
| 6–8 | LinkedIn / Reddit | Connect + DM referencing the quote |
| 3–5 | any | Watch list; re-score if they post again |
| 0–2 | any | Drop. Log it — misses tune the prompt. |

---

## 5. The DM play

Mechanics for LinkedIn invite-at-scale: **HeyReach** (built for multi-account/agency use),
Expandi, Dripify, Waalaxy, Linked Helper. Cloud-based with a dedicated IP beats a browser
extension.

Straight about the risk, since you are already doing this through Origami: **automated
connecting and messaging is against LinkedIn's ToS, and the downside is account restriction or
loss.** Mitigations that actually matter — keep daily invites conservative (~20–25), warm a new
account for weeks before volume, never run two tools at once on one account, and personalise
from the signal rather than blasting a template. Personalisation is also what protects you:
signal-referenced invites get accepted, and acceptance rate is what keeps an account healthy.

Message shape that works with a signal:

1. **Line 1 — their words.** "Saw your post about the techs double-booking."
2. **Line 2 — specific credibility, not a pitch.** One sentence, a comparable business.
3. **Line 3 — a question, not a CTA.** "Still handling it on the whiteboard?"

No link in the first message. No "hope this finds you well." The quote does the work.

---

## 6. Build order (revised, signal-first)

**This week — zero build.** Run the symptom taxonomy by hand against Upwork and Reddit. 30
minutes a day. Log every hit in a sheet with the verbatim quote. Target: 20 real signals. You
will learn which phrase families actually fire, and probably close something.

**Week 2 — automate recall.** n8n: Upwork search (hourly) + Reddit search (hourly) × 20–40
symptom queries → dedupe → Supabase. No scoring yet. Just stop missing things.

**Week 3 — add processing.** The scoring call above. Phone alert for 6–8 on Upwork. AppSheet
view for the warm queue with the quote on every row.

**Week 4 — wire the DM.** Warm queue → HeyReach/Expandi with signal-referenced openers. Track
accept rate and reply rate per phrase family, and prune the taxonomy on real data.

**Then, and only then**, consider selling it. A signal engine tuned on your own niche, with
acceptance-rate numbers you can show, is a far better product than a lead list — and far harder
for a client to get anywhere else.

---

## 7. What this changes about the earlier plan

- The sample-before-you-buy gate matters less here. Signal volume is low and quality is obvious;
  you are not selling 500-row batches.
- Email finding and verification drop down the priority list. DMs don't need them.
- Serper, Places and Firecrawl move from the backbone to **enrichment** — look up the company
  behind a signal, not discover companies from scratch.
- Instantly/Smartlead become optional. The DM tool matters more than the email sender.
- Bulk sourcing stays available for when a client specifically wants a list. It is no longer
  the centre.
