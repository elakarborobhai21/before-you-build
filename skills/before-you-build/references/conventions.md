# Conventions

Every agent follows these rules. They apply to every file written into the run folder.

## Evidence labels

Every number carries exactly one label.

- `[S]` sourced. The figure comes from a public source and the link is given. Example: `Mobile data costs 4 per GB [S](https://example.com/tariffs)`.
- `[E]` estimated. The figure is calculated and the method is given. Example: `Monthly orders 600 [E] (40 customers x 15 orders a month)`.
- `[A]` assumed. The figure is a guess and the reason is given. Example: `Return rate 5% [A] (no local data found; assumed from a similar market)`.

Confidence in a verdict depends on the share of `[S]` figures behind scorecard areas 1 to 4. A figure with no label is not allowed.

## Currency

Write amounts in the local currency first, then USD in brackets at the exchange rate given in `00_brief.md`. Example: `XYZ 12,000 (USD 100)` at a rate of 120 XYZ per USD (XYZ is an invented currency). Never use a different rate. If a source quotes another currency, convert it at the brief's rate and say so.

## Scenario names

Models use exactly three scenarios: `Defensive`, `Moderate`, `Optimistic`. The Moderate scenario is the "middle scenario" in the scorecard.

## Verdict words

Exactly three: `Go to test`, `Pivot`, `Stop`. The best verdict available is `Go to test`, never "Go build". The verdict is about the next test, not the whole company. A `Pivot` verdict names the pivot.

## Channel measure

Every test includes a channel measure, so the founder learns what it really costs to reach paying customers, not only whether the product works. It is the cost to win a paying customer through the main channel in the plan (for example paid social ads, a marketplace listing, sales agents or direct outreach), measured with real spend or real outreach during the test.

- Formula: cost to win a paying customer = (money spent on the channel + incentives given + paid help for the channel) / paying customers won through it.
- Payback cost: the most a customer can cost to win and still pay it back. It is contribution per transaction x the transactions in a customer's expected life (transactions per month x expected months as a customer, 1 / monthly churn, or the transactions a fixed-length offer includes), minus any one-off cost per new customer (for example starter equipment).
- Set the two lines by comparing the Moderate scenario's cost to acquire a customer with the payback cost:
  - Moderate cost at or below the payback cost: the pass line is at or below the Moderate cost. The fail line is at or above the cost at which the Defensive scenario follows, or at which break-even is never within 24 months. If the Moderate scenario already never breaks even within 24 months, that line would fail every result, so the fail line is the payback cost.
  - Moderate cost above the payback cost: the plan's own cost already loses money on every customer, so the pass line is at or below the payback cost and the fail line is at or above the Moderate cost.
- The pass line is always lower than the fail line; never set them equal. If the rule gives two equal lines, set the fail line at the Defensive scenario's cost to acquire a customer.
- Between the lines: change the price or the channel once, measure again on the same minimum sample, then decide.
- Say which rule set each line, with the figures.
- State the minimum sample (paying customers won through the channel) before the test starts.
- Record the founder hours spent on the channel next to the measure, because unpaid founder time hides part of the real cost.

When the riskiest assumption is already about the channel, the main test is the channel measure. Otherwise, run a small channel test alongside the main test, inside its budget and dates.

## Run folder

Each run lives in `~/before-you-build-runs/<idea-slug>-<YYYY-MM-DD>/`, whatever folder the user is working in. The lead agent passes `RUN_DIR` (this folder) and `PLUGIN_ROOT` (the plugin root) in every dispatch. Shared files are read from `<PLUGIN_ROOT>/skills/before-you-build/references/`.

```
00_brief.md
10_research/        research briefs
20_draft/           strategy report and first model, or the uploaded report
20_model/           quick model (Quick Check)
30_assessment/      sceptic, banker, scorecard inputs and result
40_plan/            business model, operations, financials (Full Review)
50_decision/        decision pack, or memo, full plan, test plan, gate tracker
sources.md          every link used, with access date
```

## sources.md format

One line per source. Each agent lists its links in its own output's `## Sources` section in this format; the lead compiles `sources.md` from those sections after each stage.

```
- [title](url) — accessed YYYY-MM-DD — used in <file>
```

Example: `- [National telecom tariff table](https://example.com/tariffs) — accessed 2026-10-12 — used in 10_research/customer_demand.md`.

## Copy style

Plain and direct. No exclamation marks. No hype words such as "revolutionary", "game-changing" or "guaranteed". Say what is known, what is not, and what to do next. Use fictional or generic examples only; do not name real ventures or real people.

## Pronouns

Refer to founders and other people as "they" unless the brief states their pronouns, in which case use those. Never infer a gender from a role or a name.

## Privacy

Founder details stay in the run folder. Do not publish, share or look up private information beyond what the user gives and what is professionally public.

## DISCLAIMER

Every output file the founder reads ends with this text, word for word:

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
