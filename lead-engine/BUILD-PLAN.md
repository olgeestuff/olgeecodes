# Own Your Own Origami: Build Plan for Sholz

Companion to `origami_build_spec.md` (the reverse-engineering report).
That report answers *what Origami is*. This answers *what you should build, what it costs,
and how it makes you money*.

Date: 2026-11-26. All vendor prices are **ballpark from public pages/third-party comparisons
as of Nov 2026** — confirm on the vendor's own pricing page before you commit money.

---

## 0. The decision, up front

**Do not clone Origami.** A general-purpose, chat-driven, any-niche lead agent is a funded
engineering product. Its moat is not the agent — it's **aggregated licensed data access**
(the one thing your report could not identify, and the one thing you cannot buy at your scale).

**Do build a narrow, niche-locked lead engine that you own and can query.** Same architecture,
2 data sources instead of 15, one buyer profile instead of all of them. This is 2–4 weeks of
low-code work, lands inside your existing skill set (n8n + Supabase/Sheets + AppSheet/Glide),
costs ~$120–180/month to run, and — this is the point — **becomes a billable add-on you sell
to the service businesses you already build AppSheet apps for.**

Run these two tracks in parallel:

| Track | What | Time to first money | Why |
|---|---|---|---|
| **A — Resell now** | Keep paying Origami/Clay. Sell "qualified lead lists + outreach" as a service on Upwork/Fiverr. Deliver with their tool. | This week | Validates demand before you build. Clients buy outcomes, not your stack. |
| **B — Build & own** | The engine below. Ship it for your own prospecting first, then as a client product. | 2–4 weeks | Removes per-lead cost ceiling, gives you something queryable you own, and is a new SKU. |

Track A funds Track B. Don't skip A.

---

## 1. What you're actually recreating

Strip Origami to its load-bearing parts. These five are the product; everything else is polish.

1. **Plain-English brief → structured search plan.** One LLM call. No filter form.
2. **A List: a table of rows that an agent fills column by column.**
3. **A background job** that sources rows and hands control back to chat immediately.
4. **A sample-before-you-buy gate.** Free/cheap 20–30 row sample, price per qualified lead shown,
   nothing charged until Approve. *This is the trust mechanism. Copy it exactly.*
5. **Success-only enrichment.** Email/phone charged on hits, never on misses.

What to **skip in v1**: the Sequencer (use Instantly/Smartlead), 15 data sources, a general
agent, CRM connectors, your own MCP server. Add later, if ever.

---

## 2. Your stack (no-code / low-code, all of it in your wheelhouse)

| Layer | Pick | Why | Cost/mo |
|---|---|---|---|
| **Orchestrator ("the bots")** | **n8n, self-hosted** on Hetzner/Contabo VPS (2 vCPU / 4GB) | Visual, queue mode gives you real background jobs, HTTP node hits any API, no per-task fee. Make.com if you refuse to touch a VPS (but per-operation billing bites at lead volume). | $6–12 VPS |
| **Database (the Lists)** | **Supabase** (Postgres) | Free tier is generous; gives you REST + SQL **the day you create a table**. This *is* your queryable API — no backend to write. | $0 → $25 |
| **Review/approve UI** | **AppSheet over Supabase or Sheets** (or Glide) | Your superpower. Row view, thumbs-down reject, an **Approve** button that flips a status column and fires an n8n webhook. You can build this in a day; a dev team takes a sprint. | $5–10/user |
| **Brief → plan, and per-row qualification** | **Claude Haiku 5.5** (or Gemini Flash for the cheap pass) | JSON-mode output. Cheap model for scoring, better model only for the brief-interpretation call. Mirror Origami's `lite`/`max` split. | $10–30 |
| **Search (SERP)** | **Serper.dev** | ~$1 per 1,000 searches entry, ~$0.30 at volume, 2,500 free. SerpAPI is 15–25× the price for features you don't need. | $50 prepaid, lasts months |
| **Local business data** | **Google Places API** (direct) or an Apify Maps actor | Google Maps is Origami's single best-performing source and you can hit it legitimately. Highest-quality data per cent spent for service businesses. | usage |
| **Page scraping / per-row research** | **Firecrawl** (~1 credit ≈ 1 page, +4 for JSON extraction) or self-hosted Playwright | Firecrawl for speed-to-ship; Playwright on your own VPS when volume justifies it. Browserbase is the premium option Origami uses. | $16–19 |
| **Email finding** | **Prospeo** (~$0.01/email claimed) or **Anymail Finder** (volume-tiered, ~$0.03–0.07/credit) | Compare on **cost per valid email**, not list price. Only charge your client on hits. | $29–49 |
| **Email verification** | MillionVerifier / Bouncer | Pennies. Non-negotiable — protects your sending domain. | $10 |
| **Outreach sending** | **Instantly or Smartlead** | Do not build a sequencer. Inbox rotation, warmup and deliverability are their whole business. | $37–97 |
| **Chat front-end** | n8n webhook + Telegram/WhatsApp bot, or just AppSheet forms | A chat UI is a nice-to-have. A form that takes a brief in one text box works identically in v1. | $0 |

**Lean start: ~$40–60/mo. Properly equipped: ~$120–180/mo.**

### "Aside from Apify" — your alternatives, ranked for your case

1. **Serper.dev + Google Places API** — cheapest, most legitimate, best data for service-business
   niches. Start here.
2. **Firecrawl** — per-URL research and company-site scraping. Clean API, no actor-rental math.
3. **Bright Data** — the heavy option. Residential proxies ~$3–10.50/GB, managed service often
   carries $1,000–2,500/mo commitments. Not for you yet.
4. **Apollo API / Clay** — you already have both as connectors (they need authorizing in your
   claude.ai connector settings). Apollo is a database, not live sourcing — but for B2B
   firmographics it beats anything you'd scrape yourself.
5. **Scrapingdog / ScraperAPI** — mid-tier managed scraping, simpler billing than Apify.
6. **Keep Apify** for the handful of social/LinkedIn actors nobody else sells. Its real problem is
   forecast-ability (compute units + actor rentals), not price. Use it as a specialist, not a backbone.

---

## 3. The data flow you build

```
Brief (one text box, plain English)
    │
    ▼  [LLM call #1 — Claude Haiku, JSON out]
Search plan: {sources[], queries[], columns[], qualified_means: "..."}
    │
    ▼  [n8n: create List row-set in Supabase, status = "sourcing"; return job_id NOW]
Background job (n8n queue)
    │  per row: SERP/Places lookup → scrape 1–2 pages → [LLM call #2, cheap] score pass/fail/unsure
    ▼
Supabase fills ~20–30 sample rows, status = "sample_ready"
    │
    ▼  [AppSheet view: rows, thumbs-down to reject, price/qualified lead, APPROVE button]
         ── nothing has cost the client anything yet ──
    │
    ▼  [Approve → webhook → n8n]
Full batch sourced  →  enrichment ONLY on approved rows (email find → verify; success-only billing)
    │
    ▼
Push to Instantly/Smartlead campaign  ·  or CSV  ·  or write into the client's AppSheet app
```

**Query it yourself** via Supabase REST (`/rest/v1/leads?status=eq.approved&score=gte.0.7`),
or an n8n webhook you point anything at — including Claude. That's the "something I can query"
you asked for, and it's free with the database.

---

## 4. Real cost per lead (your build vs Origami)

| Step | Your cost | Notes |
|---|---|---|
| SERP query | $0.001–0.003 | Serper |
| Scrape 1–3 pages | $0.005–0.015 | Firecrawl at ~$0.005/page; less self-hosted |
| LLM qualify (cheap model) | $0.002–0.010 | Haiku/Flash, short prompts |
| Infra amortized | $0.001–0.002 | VPS + Supabase |
| **Sourced + qualified lead** | **$0.01–0.04** | |
| + verified work email (on hit) | $0.03–0.07 | Origami's confirmed rate: $0.066 |
| + phone (on hit) | $0.10–0.33 | Origami's confirmed rate: $0.33 |
| **All-in with email** | **$0.05–0.11** | Origami charges $0.066–$0.154 |

So you land **slightly under Origami per lead** — which means building this to save subscription
money is a bad reason to build it. Below ~1,200–3,300 leads/month, Origami is cheaper than your
time. The reason to build is the next section.

---

## 5. Where the money actually is

Your cost: **$0.05–0.11** per lead with a verified email. What service businesses pay for a
qualified, researched lead in their niche: **$2–15**. That gap is the business.

Three SKUs you can sell inside your existing Upwork/Fiverr/Reddit motion:

1. **Lead engine setup** — $800–2,500 one-off. You build the niche-locked engine for their
   business, in their AppSheet app. Delivery is a flow you've already built once.
2. **Managed leads** — $300–800/mo for N qualified leads/month. Your cost at 500 leads: ~$50.
   Gross margin above 80%.
3. **"Leads module" add-on** to every AppSheet app you already sell — +$200–400/mo recurring on
   work you're already winning. Cheapest upsell you will ever have.

Positioning line that works for your market: *"Your app already runs your jobs. Now it fills your
pipeline too."* Service businesses on AppSheet already trust you with their operations data —
you are the obvious person to hand them customers.

---

## 6. Build order (4 weeks, part-time)

**Week 1 — prove the niche, no automation.**
Pick ONE niche you can sell into (e.g. US/UK property managers, or Lagos event vendors, or
HVAC contractors — service businesses, local, public footprint). By hand: Serper + Places +
2 pages of reading + your own judgement, produce 50 genuinely qualified leads. Write down the
exact queries and the exact pass/fail rule you used. **That written rule is the prompt.**
If you can't do 50 by hand, automation will only make bad leads faster.

**Week 2 — the spine.**
Supabase tables (`lists`, `leads`, `jobs`). n8n: brief → plan → source → score → write rows.
AppSheet review app with reject + Approve. Test on the Week-1 niche; compare the machine's 50
against your hand-picked 50. Tune the prompt, not the architecture.

**Week 3 — the gate and the handoff.**
Sample cap (20–30 rows), price-per-qualified-lead display, Approve → full batch. Enrichment
runs only post-approval, logs hit/miss, bills only hits. Push approved rows to Instantly.

**Week 4 — package and sell.**
Loom of the brief → sample → approve → campaign flow. Price it. Put it on your Upwork profile
and run it on your own prospecting so your first case study is yourself.

Ship the gate (Week 3) even if the agent is mediocre. A mediocre list a client can reject rows
from beats a great list they can't see before paying.

---

## 7. Risks — read this before week 2

- **LinkedIn**: scraping it is against their ToS and accounts get killed. Never point your own
  account at it. For B2B service businesses you don't need it — Google Maps, company sites and
  job boards carry the signal, cost less, and are public business data. This is also exactly why
  Origami performs on local/SMB/consumer niches and visibly fails on narrow industrial B2B.
- **Nigerian NDPA 2023 + GDPR** if you touch EU/UK people: have a lawful basis, keep deletion
  working, state your source. Processing business contact data for B2B outreach is normal
  practice, but "I scraped it" is not a basis — document what you collect and why.
- **Deliverability**: never send from your main domain. Separate domain, warmed inboxes, verify
  every address, keep volume inside Instantly's limits. One burned domain costs more than this
  whole stack for a year.
- **Client expectations**: sell *qualified* leads, never "guaranteed meetings." Show the
  pass/fail reason on every row — it's your defence when a client disputes quality, and it's why
  Origami surfaces its reasoning too.
- **Cost runaway**: put a hard per-job row cap and a monthly spend cap in n8n on day one, before
  the first real run. An agent in a retry loop against a paid API is the classic way to lose $200
  overnight.

---

## 8. One correction to the reverse-engineering report

The report's cost tables are sound, but they bury the real finding: **Origami's agent is
replicable in weeks; its data access is not.** Your competitive answer is not more sources — it's
*narrower scope with better judgement*. You know what a good lead looks like for a Nigerian event
vendor or a US property manager. Origami's generic agent doesn't. Encode that judgement in the
qualification prompt and you beat them where it matters, on one niche at a time.
