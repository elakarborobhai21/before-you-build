#!/usr/bin/env python3
"""Deterministic 24-month model for the three scenarios (stdlib only).

Usage: python3 scripts/model.py <model_inputs.json>
Prints the result as JSON on stdout. On bad input prints "error: ..." on
stderr and exits 2.

The modellers write 20_model/model_inputs.json and run this script for the
monthly view, break-even and cash figures. render_report.py embeds the same
inputs in report.html, whose script repeats calc() below so a reader can
change the conversion rate and see every figure move. Keep the two in step:
tests/test_model.py runs both on the example and compares them.
"""
import json
import math
import sys

SCENARIOS = ("Defensive", "Moderate", "Optimistic")
NUMBERS = ("leads_month_1", "lead_growth", "conversion_rate", "cost_per_lead",
           "transactions_per_customer_month", "churn", "first_month_share")


class ModelError(ValueError):
    """Raised when the inputs are missing, malformed or out of range."""


def _num(value, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ModelError(f"{where} must be a number")
    return value


def validate(inputs):
    if not isinstance(inputs, dict):
        raise ModelError("inputs must be a JSON object")
    months = inputs.get("months", 24)
    if not isinstance(months, int) or not 3 <= months <= 60:
        raise ModelError("months must be an integer from 3 to 60")
    _num(inputs.get("founder_cash"), "founder_cash")
    scs = inputs.get("scenarios")
    if not isinstance(scs, dict) or set(scs) != set(SCENARIOS):
        raise ModelError("scenarios must have exactly Defensive, Moderate and Optimistic")
    for name, sc in scs.items():
        for key in NUMBERS:
            _num(sc.get(key), f"{name}.{key}")
        if not 0 < sc["conversion_rate"] <= 1:
            raise ModelError(f"{name}.conversion_rate must be above 0 and at most 1")
        if not 0 <= sc["churn"] < 1:
            raise ModelError(f"{name}.churn must be from 0 to below 1")
        unit = sc.get("unit")
        if not isinstance(unit, list) or not unit:
            raise ModelError(f"{name}.unit must be a non-empty list")
        for line in unit:
            _num(line.get("value"), f"{name}.unit value")
            if line.get("kind") not in ("revenue", "cost"):
                raise ModelError(f"{name}.unit kind must be revenue or cost")
        for line in sc.get("fixed_costs", []):
            _num(line.get("monthly"), f"{name}.fixed_costs monthly")
        for line in sc.get("scaling_costs", []):
            _num(line.get("monthly"), f"{name}.scaling_costs monthly")
            if _num(line.get("per_transactions"), f"{name}.scaling_costs per_transactions") <= 0:
                raise ModelError(f"{name}.scaling_costs per_transactions must be above 0")
        for line in sc.get("one_time", []):
            _num(line.get("amount"), f"{name}.one_time amount")


def calc(sc, months, founder_cash, conversion_rate=None):
    """One scenario, month by month. conversion_rate overrides the scenario's own."""
    conv = sc["conversion_rate"] if conversion_rate is None else conversion_rate
    revenue = sum(l["value"] for l in sc["unit"] if l["kind"] == "revenue")
    contribution = sum(l["value"] for l in sc["unit"])
    active = cum = 0.0
    rows, break_even, runs_out = [], None, None
    for t in range(1, months + 1):
        leads = sc["leads_month_1"] * (1 + sc["lead_growth"]) ** (t - 1)
        new = leads * conv
        kept = active * (1 - sc["churn"])
        active = kept + new
        tx = (kept + sc["first_month_share"] * new) * sc["transactions_per_customer_month"]
        acquisition = leads * sc["cost_per_lead"]
        fixed = sum(l["monthly"] for l in sc.get("fixed_costs", [])
                    if l.get("from", 1) <= t <= l.get("to", months))
        fixed += sum(max(l.get("min", 0), math.ceil(tx / l["per_transactions"])) * l["monthly"]
                     for l in sc.get("scaling_costs", []))
        one_time = sum(l["amount"] for l in sc.get("one_time", []) if l.get("month", 1) == t)
        margin = tx * contribution
        result = margin - acquisition - fixed - one_time
        cum += result
        if break_even is None and margin >= acquisition + fixed:
            break_even = t
        if runs_out is None and cum < -founder_cash:
            runs_out = t
        rows.append({"month": t, "new_customers": new, "active_customers": active,
                     "transactions": tx, "revenue": tx * revenue,
                     "variable_cost": tx * (revenue - contribution), "acquisition": acquisition,
                     "fixed": fixed + one_time, "result": result, "cumulative": cum})
    low = min(r["cumulative"] for r in rows)
    return {
        "conversion_rate": conv,
        "cost_to_win_customer": sc["cost_per_lead"] / conv,
        "revenue_per_transaction": revenue,
        "contribution_per_transaction": contribution,
        "break_even_month": break_even,
        "cash_for_90_day_test": max(0.0, -min(r["cumulative"] for r in rows[:3])),
        "cash_need": max(0.0, -low),
        "still_falling": rows[-1]["cumulative"] <= low,
        "cash_runs_out_month": runs_out,
        "months": rows,
    }


def run(inputs):
    validate(inputs)
    months = inputs.get("months", 24)
    return {name: calc(inputs["scenarios"][name], months, inputs["founder_cash"])
            for name in SCENARIOS}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: model.py <model_inputs.json>", file=sys.stderr)
        return 2
    try:
        with open(argv[0], encoding="utf-8") as fh:
            inputs = json.load(fh)
        result = run(inputs)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
