# Full plan: <idea name>

Agent: Report Writer
Mode: Full Review
Path: <A | B>
Launch country and city: <country, city>
Date: <YYYY-MM-DD>
Currency and rate: <local currency> at <rate> per USD, as in `00_brief.md`
Verdict: <verdict, score and confidence, copied unchanged from `30_assessment/scorecard_result.json`>. The reasoning is in `50_decision/decision_memo.md`.

This plan is assembled from the rebuilt sections in `40_plan/`, the Investment Banker's review and the test plan. It adds no new analysis. Labels: [S] sourced, [E] estimated, [A] assumed. Each figure keeps the label and source or method it has in the run file it comes from.

## Summary

<five to eight plain sentences: what the business is after the critique, who pays, how it makes money, what it needs, what is still unproven, and the test that comes next>

## Business model

From `40_plan/business_model.md`.

<revenue and cost streams, how money moves between the parties, and what was dropped and why>

## Operations and product

From `40_plan/operations_product.md`.

<product flows for each side, what the first version includes and what waits, trust and safety, customer service, the org chart and first hires>

## Financials

From `40_plan/financials.md` and `40_plan/model_v2.csv`.

<the key numbers for each scenario, the per-transaction waterfall, break-even, cash need, working capital and the sensitivity table>

## Capital and valuation

From `30_assessment/banker.md`.

<capital ask and cash need, valuation range, dilution and cap table, use of funds by milestone, exit paths and due-diligence red flags>

## The validation test

From `50_decision/test_plan.md`; progress is tracked in `50_decision/gate_tracker.csv`.

<the riskiest assumption, the version tested, the test, budget, duration, pass and fail lines, go/no-go date and fallback pivots>

## Open findings

From `30_assessment/sceptic_recheck.md`.

<every finding still open after the rebuild, and any new problem or contradiction between the plan sections, each with what would close it>

## Sources and limits

- Search status: <from the research briefs and assessments>
- Where the plan sections do not agree with each other: <each difference, as found by the re-check or seen while assembling, or "none found">
- Every link used in this run is in `sources.md` in the run folder.

---

> This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
