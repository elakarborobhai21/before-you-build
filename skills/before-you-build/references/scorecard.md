# The Committee Scorecard

A committee-style judgement with hard rules, not a weighted average. The Sceptical Investor rates seven areas and writes the evidence behind each rating with its labels (see `conventions.md`). The scoring engine then computes the score, verdict and confidence. The engine's output is final: no agent changes or overrides the verdict, and no agent calculates it by hand.

## Ratings

Each area is rated on a four-point scale.

- Strong (3): the evidence is mostly `[S]` and clearly supports the area. Example: ten of twelve interviewed target customers already pay for a workaround.
- Adequate (2): the case holds, with gaps that a test can close. Example: a channel exists and the acquisition cost range is `[E]`, but nothing is proven.
- Weak (1): the case depends on unproven assumptions or one clear problem. Example: each sale loses money in the Moderate scenario until volume doubles.
- Fatal (0): the area alone can end the business. Example: the launch needs a licence the founders cannot get.

## The seven areas

| # | Area (key in the inputs file) | The question the committee asks |
|---|---|---|
| 1 | Customer pull (`customer_pull`) | Is there evidence people already want this badly enough to change behaviour? |
| 2 | Route to customers (`route_to_customers`) | Can this team reach customers in this region at a cost the business can carry? |
| 3 | Money per transaction (`money_per_transaction`) | After all real costs, does each sale make money in the middle scenario? |
| 4 | Cash to proof (`cash_to_proof`) | Can the founders fund the test, and is the later raise realistic in today's climate? |
| 5 | Competitive response (`competitive_response`) | What happens when the biggest incumbent copies the offer, and does anything survive? |
| 6 | Team and commitment (`team_commitment`) | Who is full-time, what is missing, and are there employer conflicts? |
| 7 | Rules and operations (`rules_operations`) | Can it be run legally and reliably with local payments, logistics and regulation? |

## What the engine does

Readiness score (0 to 100) is the sum of the seven ratings divided by 21, times 100, rounded half up. Then the verdict rules apply, and they override the score:

- Any area rated Fatal (0): the verdict cannot be better than `Pivot`. Two or more Fatal: `Stop`.
- `money_per_transaction` rated Weak or Fatal in the middle scenario: not `Go to test`, unless the test directly measures that number.
- No founder able to commit full-time within 6 months of a pass: not `Go to test`.
- Otherwise: score 65 or more is `Go to test`; 40 to 64 is `Pivot` (name the pivot); below 40 is `Stop`.

Confidence is High if more than half of the labelled figures behind areas 1 to 4 are `[S]`. It is Low if fewer than one in five are `[S]` or more than half are `[A]`, and otherwise Medium. High is checked first. With no labelled figures it is Low. Show it next to every score.

## Filling the inputs file

Write `<RUN_DIR>/30_assessment/scorecard_inputs.json` with these keys, all required:

- `ratings`: all seven area keys above, each an integer from 0 to 3.
- `test_measures_unit_economics`: `true` only if the proposed test directly measures money per transaction; otherwise `false`.
- `fulltime_within_6_months`: `true` only if `10_research/founder_fit.md` states that at least one founder can commit full-time within 6 months of a pass. If it says no, or the answer is unknown, `false`.
- `label_counts`: the number of `S`, `E` and `A` labelled figures behind areas 1 to 4. Count the figures in your own evidence tables; do not estimate.

Example:

```json
{
  "ratings": {
    "customer_pull": 2,
    "route_to_customers": 2,
    "money_per_transaction": 1,
    "cash_to_proof": 2,
    "competitive_response": 1,
    "team_commitment": 2,
    "rules_operations": 2
  },
  "test_measures_unit_economics": true,
  "fulltime_within_6_months": true,
  "label_counts": {"S": 6, "E": 9, "A": 5}
}
```

## Running the engine

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py" <RUN_DIR>/30_assessment/scorecard_inputs.json
```

`${CLAUDE_PLUGIN_ROOT}` means the plugin root path that the lead agent passes in the dispatch as `PLUGIN_ROOT`; substitute that path. `<RUN_DIR>` is the run folder passed in the same dispatch. On success the engine prints the result JSON, with `readiness_score`, `verdict`, `confidence` and `reasons`, to stdout and exits 0. Save that stdout, unedited, as `<RUN_DIR>/30_assessment/scorecard_result.json`. On bad input it prints `error: ...` to stderr, prints nothing to stdout, and exits with code 2. On exit code 2, delete any partial `scorecard_result.json`, fix the inputs file and run the engine again. Never leave a result file after an error, and do not write a verdict yourself.

## Stage 4b re-check

In a Full Review the re-check saves the first inputs as `30_assessment/scorecard_inputs_v1.json`, writes updated ratings to `scorecard_inputs.json`, and re-runs the engine, overwriting `scorecard_result.json`. Later agents use the latest result.
