# Test plan: <idea name>

Agent: Validation Test Designer
Mode: Full Review
Launch country and city: <country, city>
Date: <YYYY-MM-DD>
Currency and rate: <local currency> at <rate> per USD, as in `00_brief.md`
Evidence mix: <count of [S], [E] and [A] figures in this file>

The cheapest test of the riskiest assumption, within 90 days. Progress is tracked in `50_decision/gate_tracker.csv`, one row per measure below. Labels: [S] sourced, [E] estimated, [A] assumed.

## Riskiest assumption

<The Sceptical Investor's answer to question 9, quoted, with its evidence and labels, and its status in `30_assessment/sceptic_recheck.md`.>

## The test

Version tested: <the original plan or the pivot, and why; under a Pivot verdict this line comes first>

<what the founder does, step by step, with real customers and, where possible, real money, and how this differs from the Sceptical Investor's cheapest test, and why, if it does>

## Budget

| Item | Amount | Label and method or source |
|---|---|---|
| <item> | <amount> | [E] (<method>) |
| Total | <amount> | [E] (sum of the rows) |

Founder cash in the brief: <amount>. The test uses <share> of it.

## Duration

<start date, end date and days, no more than 90, and the weekly steps>

## What is built and what is not

- Built: <only what the test needs, for example a landing page, a form, a manual order process>
- Not built: <everything else, for example the app, automation, the second city>

## Measures, pass and fail lines

| Measure | Formula | Pass line | Fail line | How the line was set |
|---|---|---|---|---|
| <measure> | <formula> | <line> | <line> | [E] (<from which figure in `40_plan/model_v2.csv` or `40_plan/financials.md`>) |

- Minimum sample before reading the result: <for example, at least N paid transactions>
- Between the lines: <what a result between the pass line and the fail line means for the decision>

## Channel measure

The cost to win a paying customer through the main channel, as set out under `Channel measure` in conventions.md. It has its own row in the table above and in `gate_tracker.csv`.

- Main channel: <the channel the plan relies on, from `40_plan/business_model.md`>
- What the founder does: <the spend or outreach, when, and how it fits the test's budget and dates; or that the main test is the channel test>
- Formula: (money spent on the channel + incentives given + paid help for the channel) / paying customers won through it
- Pass line: <at or below the cost to acquire a customer in the Moderate scenario, labelled [E] with the figure from `40_plan/model_v2.csv`>
- Fail line: <at or above the cost at which the Defensive scenario or a break-even of never follows, labelled [E] with the figure>
- Minimum sample: <paying customers won through the channel before the result is read>
- Founder hours: <recorded next to the measure>

## Go/no-go date

<date, on or before the decision deadline, or the conflict and the date the deadline would need to move to> On that date:

- Go (every pass line met): <the next test or decision and what it costs>
- No-go (any fail line on the riskiest assumption): <stop spending on this version and choose a fallback pivot>

## Fallback pivots

If the test fails, in order of the evidence for each:

1. **<pivot>.** <which failed measure it answers, the evidence for it, and the cheaper test that would check it>
2. **<pivot>.** <why>

## Open findings this test also checks

<Findings still open in `30_assessment/sceptic_recheck.md` that this test will also answer, and those it will not.>

## Gaps and assumptions

- <gap or assumption> [A] (<reason>) — how to close it: <action>

## Sources

- [<title>](<url>) — accessed <YYYY-MM-DD> — used in 50_decision/test_plan.md

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
