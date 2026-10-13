#!/usr/bin/env python3
"""Deterministic investment-committee scorecard (stdlib only).

Usage: python3 scripts/scorecard.py <inputs.json>
Prints the result as JSON on stdout. On bad input prints "error: ..." on
stderr and exits 2.
"""
import json
import math
import sys

AREAS = (
    "customer_pull",
    "route_to_customers",
    "money_per_transaction",
    "cash_to_proof",
    "competitive_response",
    "team_commitment",
    "rules_operations",
)
LABELS = ("S", "E", "A")
FLAGS = ("test_measures_unit_economics", "fulltime_within_6_months")
GO, PIVOT, STOP = "Go to test", "Pivot", "Stop"


class ScorecardError(ValueError):
    """Raised when the inputs are missing, malformed or out of range."""


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate(inputs):
    if not isinstance(inputs, dict):
        raise ScorecardError("inputs must be a JSON object")
    for key in ("ratings", "label_counts") + FLAGS:
        if key not in inputs:
            raise ScorecardError(f"missing key: {key}")
    ratings = inputs["ratings"]
    if not isinstance(ratings, dict):
        raise ScorecardError("ratings must be an object")
    for area in AREAS:
        if area not in ratings:
            raise ScorecardError(f"missing rating: {area}")
    for area, value in ratings.items():
        if area not in AREAS:
            raise ScorecardError(f"unknown rating area: {area}")
        if not _is_int(value) or not 0 <= value <= 3:
            raise ScorecardError(f"rating {area} must be an integer from 0 to 3")
    for flag in FLAGS:
        if not isinstance(inputs[flag], bool):
            raise ScorecardError(f"{flag} must be true or false")
    counts = inputs["label_counts"]
    if not isinstance(counts, dict) or set(counts) != set(LABELS):
        raise ScorecardError("label_counts must have exactly the keys S, E, A")
    for label in LABELS:
        if not _is_int(counts[label]) or counts[label] < 0:
            raise ScorecardError(f"label_counts {label} must be a non-negative integer")


def _confidence(counts):
    total = sum(counts[label] for label in LABELS)
    if total == 0:
        return "Low"
    if counts["S"] / total > 0.5:
        return "High"
    if counts["S"] / total < 0.2 or counts["A"] / total > 0.5:
        return "Low"
    return "Medium"


def score(inputs):
    _validate(inputs)
    ratings = inputs["ratings"]
    readiness = math.floor(sum(ratings[a] for a in AREAS) * 100 / 21 + 0.5)
    verdict = GO if readiness >= 65 else PIVOT if readiness >= 40 else STOP
    reasons = []
    zeros = sum(1 for a in AREAS if ratings[a] == 0)

    if zeros >= 2:
        verdict = STOP
        reasons.append(
            f"Fatal flaws in {zeros} areas (rated 0), so the verdict is Stop whatever the total."
        )
    elif zeros == 1 and verdict == GO:
        verdict = PIVOT
        reasons.append(
            "Fatal flaw in one area (rated 0), so the verdict is capped at Pivot until it is fixed."
        )
    if (
        ratings["money_per_transaction"] <= 1
        and not inputs["test_measures_unit_economics"]
        and verdict == GO
    ):
        verdict = PIVOT
        reasons.append(
            "Money per transaction is weak and the test would not measure unit economics, "
            "so the verdict is capped at Pivot."
        )
    if not inputs["fulltime_within_6_months"] and verdict == GO:
        verdict = PIVOT
        reasons.append(
            "No founder can be full-time within 6 months, so the verdict is capped at Pivot."
        )

    return {
        "readiness_score": readiness,
        "verdict": verdict,
        "confidence": _confidence(inputs["label_counts"]),
        "reasons": reasons,
    }


def main(argv):
    try:
        if len(argv) != 2:
            raise ScorecardError("usage: scorecard.py <inputs.json>")
        try:
            with open(argv[1], encoding="utf-8") as fh:
                inputs = json.load(fh)
        except (OSError, ValueError) as exc:
            raise ScorecardError(f"cannot read {argv[1]}: {exc}") from exc
        result = score(inputs)
    except ScorecardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
