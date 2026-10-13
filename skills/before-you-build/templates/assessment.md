# Sceptical Investor assessment: <idea name>

Agent: Sceptical Investor
Mode: <Quick Check | Full Review>
Draft assessed: <"20_model/quick_model.md" (Quick Check) | "20_draft/strategy_report.md and 20_draft/model_v1.csv" (Full Review, Path A) | "20_draft/uploaded_report.md" (Full Review, Path B)>
Launch country and city: <country, city>
Date: <YYYY-MM-DD>
Search status: <"Web search and fetch worked." | "Web search partly available: <what failed>." | "Web search was unavailable or blocked. No new figure below is sourced; each is [E] from the research briefs or [A] with its reason.">
Evidence mix: <count of [S], [E] and [A] figures in this file>

Follow `<PLUGIN_ROOT>/skills/before-you-build/references/conventions.md` for labels, currency and copy style. This file does not state a verdict: the scoring engine writes it to `30_assessment/scorecard_result.json`.

## The ten questions

Answered in this order before anything else, from `references/questions.md`. Each answer is a few plain sentences with every figure labelled and the research brief it comes from.

### 1. Who exactly pays, and why would they switch from what they use today?

<answer>

### 2. What does one transaction really earn after every cost, including discounts, failures, payments and support?

<answer>

### 3. What does it cost to win a customer here, and how many times do they come back?

<answer>

### 4. How much money is needed to reach proof, and where does it come from?

<answer>

### 5. Who on the team is full-time, and what conflicts does each founder carry?

<answer>

### 6. What do the biggest incumbents do the day this launches?

<answer>

### 7. Which rule, licence or tax could change the model?

<answer>

### 8. What did the draft leave out?

<answer>

### 9. What is the single assumption that, if wrong, kills the business?

<answer>

### 10. What is the cheapest way to find out within 90 days?

<answer, and whether this test directly measures money per transaction>

## Recomputed numbers

Every figure in the draft that bears on the decision, recomputed from the research briefs.

| Figure | Draft value | Recomputed value | Label and method or source | Difference and why |
|---|---|---|---|---|
| <figure> | <value> | <value> | [E] (<method>) | <difference> |

## Missing costs

Costs the draft left out or understated, each with an amount per transaction or per month and its label.

| Cost | Amount | Label and method or source | Effect on the Moderate scenario |
|---|---|---|---|
| <cost> | <amount> | [E] (<method>) | <effect> |

## Pre-mortem

It is twelve months from launch and the business has failed. It failed because:

1. <most likely cause, with the evidence that points to it>
2. <next cause>
3. <next cause>

## Risk register

| Risk | Likelihood (Low, Medium, High) | Impact (Low, Medium, High) | Mitigation | Early warning sign |
|---|---|---|---|---|
| <risk> | <likelihood> | <impact> | <mitigation> | <sign> |

## Scorecard

Ratings follow `references/scorecard.md`: Strong (3), Adequate (2), Weak (1), Fatal (0).

| # | Area (key) | Rating | Evidence, with labels |
|---|---|---|---|
| 1 | Customer pull (`customer_pull`) | <0-3> | <evidence> |
| 2 | Route to customers (`route_to_customers`) | <0-3> | <evidence> |
| 3 | Money per transaction (`money_per_transaction`) | <0-3> | <evidence, Moderate scenario> |
| 4 | Cash to proof (`cash_to_proof`) | <0-3> | <evidence> |
| 5 | Competitive response (`competitive_response`) | <0-3> | <evidence> |
| 6 | Team and commitment (`team_commitment`) | <0-3> | <evidence> |
| 7 | Rules and operations (`rules_operations`) | <0-3> | <evidence> |

- Test measures unit economics: <true | false>, because <reason from question 10>
- At least one founder full-time within 6 months of a pass: <true | false>, per `10_research/founder_fit.md`
- Labelled figures behind areas 1 to 4: S <n>, E <n>, A <n>
- Inputs: `30_assessment/scorecard_inputs.json`. Score, verdict and confidence: `30_assessment/scorecard_result.json`, written by the scoring engine.

## Gaps and assumptions

What could not be checked, every `[A]` figure with its reason, and how the founder could close each gap.

- <gap or assumption> [A] (<reason>) — how to close it: <action>

## Sources

Every link used in this file, one per line, in the conventions.md sources format. The lead compiles these into `sources.md`.

- [<title>](<url>) — accessed <YYYY-MM-DD> — used in 30_assessment/sceptic.md

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
