# Decision memo: <idea name>

Agent: Report Writer
Mode: Full Review
Path: <A (drafted strategy report) | B (founder's uploaded report)>
Launch country and city: <country, city>
Date: <YYYY-MM-DD>
Currency and rate: <local currency> at <rate> per USD, as in `00_brief.md`
Evidence mix: <count of [S], [E] and [A] figures in this file>

Labels: [S] sourced, [E] estimated, [A] assumed. Each figure keeps the label and source or method it has in the run file it comes from. The full rebuilt plan is in `50_decision/full_plan.md`.

## Verdict

**<Go to test | Pivot | Stop>**, copied unchanged from `30_assessment/scorecard_result.json` after the Stage 4b re-check.

<Two or three plain sentences on what the verdict means for the founder now: the verdict is about the next test, not the whole company. For Pivot, the pivot and the finding it answers. For Stop, what would have to be true for the idea to be worth another look.>

Why the committee's rules gave this verdict:

- <each item of `reasons` in `scorecard_result.json`, word for word, or "The score alone set the verdict; no rule overrode it." when the list is empty>

## Readiness score

**<score>/100**, confidence **<High | Medium | Low>**, copied unchanged from `30_assessment/scorecard_result.json`.

<One sentence on what the confidence means here.>

| # | Area | Rating at Stage 3 | Rating after the re-check | Why it changed, or the evidence in one line |
|---|---|---|---|---|
| 1 | Customer pull | <rating> | <rating> | <from sceptic_recheck.md or sceptic.md> |
| 2 | Route to customers | <rating> | <rating> | <evidence> |
| 3 | Money per transaction | <rating> | <rating> | <evidence, Moderate scenario> |
| 4 | Cash to proof | <rating> | <rating> | <evidence> |
| 5 | Competitive response | <rating> | <rating> | <evidence> |
| 6 | Team and commitment | <rating> | <rating> | <evidence> |
| 7 | Rules and operations | <rating> | <rating> | <evidence> |

<only if the re-check could not compute an updated score: say so, as `sceptic_recheck.md` states>

## Riskiest assumption

<The Sceptical Investor's answer to question 9, in one or two sentences, with its evidence and labels, and its status after the re-check: fixed, answered or still open.>

## The test

From `50_decision/test_plan.md`; progress is tracked in `50_decision/gate_tracker.csv`.

- Version tested: <the original plan or the pivot, and why, as `test_plan.md` states>
- What you do: <the test in plain steps>
- Budget: <amount, labelled>
- Duration: <days, no more than 90>
- Measures, pass and fail lines: <each measure with its formula, pass line and fail line>
- Go/no-go date: <date>
- If it fails: <the fallback pivots, one line each>

## Key numbers

From `40_plan/financials.md` and `40_plan/model_v2.csv`.

| Measure | Defensive | Moderate | Optimistic |
|---|---|---|---|
| Contribution per transaction | <value> | <value> | <value> |
| Break-even month | <period or "never"> | <value> | <value> |
| Cash need | <value> | <value> | <value> |
| Cash need with working capital | <value> | <value> | <value> |

The assumptions that move the outcome most: <the four from the sensitivity table, one line each>.

## What the rebuild changed

From `30_assessment/sceptic_recheck.md`: <n> findings fixed, <n> answered, <n> still open.

- <the most important changes to the business model, operations and financials, one line each>
- Still open: <each open finding that bears on the decision>

## Capital and valuation

From `30_assessment/banker.md`: <capital ask against cash need, the valuation range, founder ownership after planned rounds, and the red flag that most affects the decision>.

## Top 3 risks

1. **<risk>.** <why it matters, with evidence and labels> Early warning sign: <sign>.
2. **<risk>.** <why> Early warning sign: <sign>.
3. **<risk>.** <why> Early warning sign: <sign>.

## Pre-mortem

It is twelve months from launch and the business has failed. From `30_assessment/sceptic.md`, with what the rebuilt plan does about each cause:

1. <cause, its evidence, and whether the rebuild fixed, answered or left it open>
2. <cause>
3. <cause>

## Sources and limits

- Search status: <from the research briefs and assessments>
- The assumptions that matter most and are not yet checked: <each `[A]` figure behind the verdict, with its reason>
- Every link used in this run is in `sources.md` in the run folder.

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
