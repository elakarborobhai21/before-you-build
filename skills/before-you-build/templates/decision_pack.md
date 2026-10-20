# Decision pack: <idea name>

Agent: Report Writer
Mode: Quick Check
Launch country and city: <country, city>
Date: <YYYY-MM-DD>
Currency and rate: <local currency> at <rate> per USD, as in `00_brief.md`
Evidence mix: <count of [S], [E] and [A] figures in this file>

Labels: [S] sourced, [E] estimated, [A] assumed. Each figure keeps the label and source or method it has in the run file it comes from.

## Verdict

**<Go to test | Pivot | Stop>**, copied unchanged from `30_assessment/scorecard_result.json`.

<Two or three plain sentences on what the verdict means for the founder now: the verdict is about the next test, not the whole company. For Pivot, the pivot and the finding it answers. For Stop, what would have to be true for the idea to be worth another look.>

Why the committee's rules gave this verdict:

- <each item of `reasons` in `scorecard_result.json`, word for word, or "The score alone set the verdict; no rule overrode it." when the list is empty>

## Readiness score

**<score>/100**, confidence **<High | Medium | Low>**, copied unchanged from `30_assessment/scorecard_result.json`.

<One sentence on what the confidence means here: how much of the evidence behind areas 1 to 4 is sourced, estimated or assumed.>

| # | Area | Rating | The evidence in one line |
|---|---|---|---|
| 1 | Customer pull | <Strong, Adequate, Weak or Fatal> | <from sceptic.md, with labels> |
| 2 | Route to customers | <rating> | <evidence> |
| 3 | Money per transaction | <rating> | <evidence, Moderate scenario> |
| 4 | Cash to proof | <rating> | <evidence> |
| 5 | Competitive response | <rating> | <evidence> |
| 6 | Team and commitment | <rating> | <evidence> |
| 7 | Rules and operations | <rating> | <evidence> |

## What the numbers say

From `20_model/quick_model.md`, with the Sceptical Investor's recomputed figure beside it wherever the two differ.

| Measure | Defensive | Moderate | Optimistic | Recomputed by the Sceptical Investor |
|---|---|---|---|---|
| Contribution per transaction | <value> | <value> | <value> | <value or "same"> |
| Break-even month | <month or "never within 24 months"> | <value> | <value> | <value or "same"> |
| Cash to run the 90-day test | <value> | <value> | <value> | <value or "same"> |
| Cash to reach break-even | <value> | <value> | <value> | <value or "same"> |

Founder cash in the brief: <amount>. Outside money promised: <amount or "none">.

## Top 3 risks

Most serious first.

1. **<risk>.** <why it matters, with evidence and labels> Early warning sign: <sign>.
2. **<risk>.** <why> Early warning sign: <sign>.
3. **<risk>.** <why> Early warning sign: <sign>.

## The test

The cheapest test in the next 90 days.

- Version tested: <the original plan or the named pivot, and why>
- What it tests: <the riskiest assumption, from question 9>
- What you do: <the test in plain steps>
- Budget: <amount, labelled>
- Duration: <set-up> weeks set-up plus <live> weeks live (<days> days, no more than 90)
- What you measure: <each measure; include money per transaction when the test measures it>
- Pass line: <measure, formula and line, labelled [E] with how the line was set>
- Fail line: <measure, formula and line, labelled [E] with how the line was set>
- Channel measure: <cost to win a paying customer through the main channel: formula, minimum sample, payback cost, pass line and a higher fail line, labelled [E] with how each line was set, what a result between them means, and the founder hours spent on the channel>
- Decide by: <date, on or before the decision deadline, or the conflict and the date the deadline would need to move to>

## What would change this verdict

- <area>: <what evidence would raise its rating, and how to get it>

## Sources and limits

- Search status: <from the research briefs and sceptic.md>
- The assumptions that matter most and are not yet checked: <each `[A]` figure behind the verdict, with its reason>
- What this Quick Check did not cover: no strategy draft, no investment banker review, no revision round. A Full Review covers these and reuses this run's research.
- Every link used in this run is in `sources.md` in the run folder.

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
