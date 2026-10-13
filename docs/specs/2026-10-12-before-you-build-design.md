# Before You Build — design spec

*Status: approved · 12 October 2026*

> An AI investment committee for founders. Get an honest verdict before you spend your savings.

## 1. What it is and who it is for

Before You Build is a team of AI agents that takes a founder's business idea, region, target market and founding team, and returns an honest decision pack: what the opportunity looks like, what the numbers really say, what an investor would attack, and the cheapest test to run before spending real money.

**Audience:** first-time and early founders, especially outside the US and Western Europe, deciding whether to quit a job, build, or raise. Also small founding teams that need one shared, honest view before committing.

**Success looks like:** a founder finishes a run knowing (a) whether to go to a test, pivot or stop, (b) the one assumption most likely to kill the business, and (c) a concrete, cheap test with pass/fail lines and a date.

**It is not:** a business-plan generator that cheers ideas on, financial or legal advice, or a substitute for talking to real customers.

## 2. Principles

1. **Honesty over encouragement.** "Stop" and "pivot" are normal outcomes. The tool is judged by whether its verdicts hold up, not by whether users like them.
2. **The verdict is about the next test, not the whole company.** The best verdict available is "Go to test", never "Go build".
3. **Drafter and critic are separate agents.** The agent that writes the plan never grades it. Critics never see the drafter's working notes and must recompute numbers themselves.
4. **Every number is labelled** `[S]` sourced (with a link), `[E]` estimated (with the method), or `[A]` assumed (with the reason). Confidence in the verdict depends on the share of `[S]`.
5. **Regions are checklists, not stored facts.** Region packs say what must be checked; agents research the current answers live.
6. **Public data only.** Every output carries the disclaimer in §11.
7. **Founder privacy.** Founder details stay in the run folder on the user's machine. Agents do not publish, share or look up private information beyond what the user gives and what is professionally public.

## 3. Two modes and two entry paths

| | Quick Check | Full Review |
|---|---|---|
| Use it for | Screening an idea | An idea you are seriously considering |
| Agents (excluding lead) | 6 | 15 |
| Draft strategy report | No | Yes (Path A) or uploaded (Path B) |
| Critics | Sceptical Investor | Sceptical Investor + Investment Banker |
| Revision round | No | One |
| Output | 3–5 page decision pack | Decision memo, full plan, model, gate tracker |

**Path A — no report yet:** Full Review drafts one (Stage 2).
**Path B — bring your own report:** the founder uploads an existing plan (from ChatGPT, a consultant, their own deck). Stage 2 is skipped; the uploaded report is the draft. Research still runs so the critics have independent evidence.

A Quick Check can be upgraded to a Full Review; its research briefs are reused.

## 4. Intake (Stage 0, lead agent, in conversation)

The lead asks one topic at a time and writes `00_brief.md`:

1. **The idea** — what it is, who pays, how it makes money (in the founder's words).
2. **Region and country** — one of: South Asia, Southeast Asia, East Asia, Middle East & North Africa, Sub-Saharan Africa, Europe, North America, Latin America; plus the launch country and city.
3. **Target customer** — who, where, how they solve the problem today.
4. **Founders** — for each: role, relevant experience, current job and employer type, hours per week available, whether they can go full-time and when, months they can live without salary. Names optional. Quick Check asks only role, full-time or not (and when), and any current-employer conflict.
5. **Money and time** — founder cash available, outside money already promised, decision deadline.
6. **Existing report** (Full Review only) — upload or skip.
7. **Mode** — Quick Check or Full Review.
8. **Currency** — local currency and exchange rate to USD used throughout.

The lead plays the brief back for correction before dispatching any agent.

## 5. Agent roster

All agents read `00_brief.md`. "Parallel" agents are dispatched at the same time.

### Quick Check

| Stage | Agent | Runs | Reads | Writes |
|---|---|---|---|---|
| 1 | Market & Competition Scout | parallel | brief, region pack | `10_research/market_competition.md` |
| 1 | Customer & Demand Analyst | parallel | brief, region pack | `10_research/customer_demand.md` |
| 1 | Founder Fit Reviewer | parallel | brief | `10_research/founder_fit.md` |
| 2 | Quick Modeller | after 1 | research | `20_model/quick_model.md` (3 scenarios) |
| 3 | Sceptical Investor | after 2 | research, model | `30_assessment/sceptic.md` + scorecard |
| 4 | Verdict Writer | after 3 | everything | `50_decision/decision_pack.md` |

### Full Review

| Stage | Agent | Runs | Writes |
|---|---|---|---|
| 1 | Market & Region Researcher | parallel ×6 | `10_research/market_region.md` |
| 1 | Competition Scout | | `10_research/competition.md` |
| 1 | Customer & Demand Analyst | | `10_research/customer_demand.md` |
| 1 | Regulation & Structure Mapper | | `10_research/regulation_structure.md` |
| 1 | Founder Fit & Conflicts Reviewer | | `10_research/founder_fit.md` |
| 1 | Funding Climate Scout | | `10_research/funding_climate.md` |
| 2 | Strategist + Draft Modeller | pair (Path A only) | `20_draft/strategy_report.md`, `20_draft/model_v1.csv` |
| 3 | Sceptical Investor | parallel ×2 | `30_assessment/sceptic.md` |
| 3 | Investment Banker | | `30_assessment/banker.md` |
| 4a | Business Model Designer | first | `40_plan/business_model.md` |
| 4 | Operations & Product Planner | after 4a, reads the business model | `40_plan/operations_product.md` |
| 4 | Financial Modeller | after the Operations & Product Planner, reads both | `40_plan/financials.md`, `40_plan/model_v2.csv` |
| 4b | Sceptical Investor (re-check) | once | `30_assessment/sceptic_recheck.md` |
| 5 | Validation Test Designer | after 4b | `50_decision/test_plan.md`, `50_decision/gate_tracker.csv` |
| 5 | Report Writer | after test design | `50_decision/decision_memo.md`, `50_decision/full_plan.md` |

### What each agent must cover

- **Market & Region Researcher** — market size bottom-up (not just top-down reports), payment habits, cash-on-delivery share, logistics cost and failure rates, seasonality and festival calendar, internet and device use, local norms that change the model.
- **Competition Scout** — local and global competitors, their fees and pricing, customer reviews and weak spots, how each incumbent would respond, global analogies and what made them work. Searches regional sites and local-language sources, not only English or US ones.
- **Customer & Demand Analyst** — who buys, how often, current alternative, willingness to pay, reachable channels, likely cost to acquire a paying customer (range), repeat behaviour.
- **Regulation & Structure Mapper** — licences and registrations, tax on the revenue model, consumer, data and payments rules, where to incorporate and why. Issue map only, never legal advice.
- **Founder Fit & Conflicts Reviewer** — skills covered and missing (technical, commercial, finance, operations), real full-time availability, conflicts with current employers (competitor, partner, regulator), personal runway, what investors will ask.
- **Funding Climate Scout** — recent deals in the region and sector, typical cheque sizes by stage, active investors and their fit, non-dilutive options, how the current climate changes the plan.
- **Strategist** — the strongest honest case: positioning, what each side gets, launch focus, revenue streams, expansion sequence, capital ask. Ambitious, but every claim labelled.
- **Draft Modeller** — turns the Strategist's assumptions into a base-case model: volume curve, revenue and variable cost per transaction, fixed costs, break-even, cash need.
- **Sceptical Investor** — answers the ten committee questions (§7), recomputes every number from the research, lists missing costs, writes a pre-mortem ("it failed in 12 months because…"), a risk register (likelihood, impact, mitigation), and fills the scorecard (§6).
- **Investment Banker** — valuation range and how it is justified at this stage, dilution and cap table across planned rounds including an option pool, use of funds by milestone, comparable companies and deals, realistic exit paths and buyers, due-diligence red flags (IP, employer claims, licences, data).
- **Business Model Designer** — revenue and cost streams after critique, how money moves between parties, what to drop and why.
- **Operations & Product Planner** — product flows for each side, MVP vs later tech, trust and safety, customer service, org chart and first hires.
- **Financial Modeller** — three scenarios (Defensive, Moderate, Optimistic); P&L, cash flow, balance sheet and working capital; per-transaction waterfall; break-even month or "never"; sensitivity of the outcome to the 4 most important assumptions.
- **Validation Test Designer** — the cheapest test of the riskiest assumption: budget, duration, what is built and what is not, pass/fail lines with formulas, go/no-go date, fallback pivots if it fails, and a gate tracker sheet.
- **Report Writer / Verdict Writer** — verdict, score, confidence, top risks, the test, sources and limits, disclaimer. Plain language, no hype.

## 6. Scoring: the Committee Scorecard

Before You Build uses its own method. It is a committee-style judgement with hard rules, not a weighted average.

**Seven areas**, each rated **Strong (3) · Adequate (2) · Weak (1) · Fatal (0)**, with the evidence and its labels:

| # | Area | The question the committee asks |
|---|---|---|
| 1 | Customer pull | Is there evidence people already want this badly enough to change behaviour? |
| 2 | Route to customers | Can this team reach customers in this region at a cost the business can carry? |
| 3 | Money per transaction | After all real costs, does each sale make money in the middle scenario? |
| 4 | Cash to proof | Can the founders fund the test, and is the later raise realistic in today's climate? |
| 5 | Competitive response | What happens when the biggest incumbent copies the offer, and does anything survive? |
| 6 | Team and commitment | Who is full-time, what is missing, and are there employer conflicts? |
| 7 | Rules and operations | Can it be run legally and reliably with local payments, logistics and regulation? |

**Readiness score (0–100)** = sum of ratings ÷ 21 × 100, rounded.

**Verdict rules** (applied after the score, and they override it):

- Any area rated **Fatal** → verdict cannot be better than **Pivot**. Two or more Fatal → **Stop**.
- Area 3 Weak or Fatal in the middle scenario → cannot be **Go to test** unless the test directly measures that number.
- Area 6: no founder able to commit full-time within 6 months of a pass → cannot be **Go to test**.
- Otherwise: score ≥ 65 → **Go to test**; 40–64 → **Pivot** (with the pivot named); < 40 → **Stop**.

**Confidence** — High if more than half of figures behind areas 1–4 are [S]; Low if fewer than one in five are [S] or more than half are [A]; otherwise Medium. Shown next to every score.

## 7. The ten committee questions

The Sceptical Investor answers all ten, in this order, before writing anything else:

1. Who exactly pays, and why would they switch from what they use today?
2. What does one transaction really earn after every cost, including discounts, failures, payments and support?
3. What does it cost to win a customer here, and how many times do they come back?
4. How much money is needed to reach proof, and where does it come from?
5. Who on the team is full-time, and what conflicts does each founder carry?
6. What do the biggest incumbents do the day this launches?
7. Which rule, licence or tax could change the model?
8. What did the draft leave out?
9. What is the single assumption that, if wrong, kills the business?
10. What is the cheapest way to find out within 90 days?

## 8. Region packs

One file per region in `regions/`. Each holds a **checklist** of what agents must check live, not stored facts. Common items for every region:

- Main payment methods and their fees; cash-on-delivery share
- Logistics providers, delivery cost and failure/return rates
- Seasonality and festival calendar
- Business registration, tax on the revenue model, consumer and data rules
- Funding climate in the last 12 months
- Dominant local and regional competitors; local-language search terms
- Trust norms (how people decide whom to buy from)

Each region pack adds region-specific items (for example: mobile money in Sub-Saharan Africa and South Asia; instalment culture in Latin America; Sharia-compliant finance and free-zone setup in the Gulf; super-apps in Southeast Asia).

## 9. Files and folders

### Run folder (created on the user's machine for each run)

```
~/before-you-build-runs/<idea-slug>-<date>/
  00_brief.md
  10_research/*.md
  20_draft/strategy_report.md, model_v1.csv     (Full, Path A)
  20_draft/uploaded_report.md                    (Full, Path B)
  30_assessment/*.md
  40_plan/*.md, model_v2.csv                     (Full)
  50_decision/decision_pack.md | decision_memo.md, full_plan.md, test_plan.md, gate_tracker.csv
  sources.md                                     (every link used, with access date)
```

### Repository

```
before-you-build/
  README.md                 what it is, install, example, disclaimer, acknowledgements
  LICENSE                   MIT
  .claude-plugin/
    plugin.json
    marketplace.json        so users can install with /plugin
  skills/before-you-build/
    SKILL.md                lead agent: intake, dispatch, stage control
    templates/              brief, research brief, strategy report, assessment, decision pack, memo
    scorecard.md            §6
    questions.md            §7
    regions/*.md            §8
  agents/*.md               one file per agent in §5
  single-chat/              same flow as one prompt pack for ChatGPT / Claude.ai chat (v1.1)
  examples/                 one fictional worked example (no real people or ventures)
  docs/specs/               this spec
```

## 10. Platforms

- **v1: Claude Code.** Installed as a plugin. The lead is a skill; specialists are subagents dispatched in parallel. Agents use web search and fetch for research.
- **v1.1: single-chat mode.** For ChatGPT (Custom GPT) and Claude.ai chat: the same agents run one after another inside one conversation. Slower, same outputs.

## 11. Disclaimer (on every output)

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.

## 12. Testing before public release

1. Run Quick Check and Full Review on **five fictional ideas** in five different regions and business types (e.g. a Lagos logistics app, a Jakarta B2B SaaS, a São Paulo food brand, a Riyadh services marketplace, a Toronto consumer subscription).
2. **Private comparison:** an optional private comparison against the author's own earlier case, never published.
3. Open and check **every link** in the published example.
4. 3–5 founders or investors try it and report problems before announcement.
5. Release as **v0.1**.

## 13. Out of scope for v1

- Interactive HTML plan (v2)
- Add-ons: pitch deck and teaser, interview scripts, launch plan, founders' agreement terms, shutdown plan (v1.1)
- Ongoing competitor monitoring (later, as a scheduled run)
- Paid data sources

## 14. Acknowledgements (to appear in README)

- Inspired in part by **idea-validation-agents** by Max Kmet (MIT). Before You Build uses its own scoring method and wording.
- Agent-collection format inspired by **The Agency (agency-agents)** by msitarzewski and contributors (MIT).
- Built with Claude.

## 15. Decisions on open questions

1. **Run folder:** always `~/before-you-build-runs/<idea-slug>-<date>/`, whatever folder the user is working in.
2. **Founders in Quick Check:** ask about every founder, briefly: role, full-time or not (and when), any current-employer conflict.
3. **Published example:** a fictional Lagos delivery and logistics app (Sub-Saharan Africa region pack).
