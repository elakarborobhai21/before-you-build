#!/usr/bin/env python3
"""Check that a Before You Build run folder has the files each stage must leave.

It also flags a test longer than 90 days and a sceptic.md over 5,000 words.

Usage: python3 scripts/check_run.py <run_dir> --mode quick|full [--path A|B] --stage N
Prints "ok" and exits 0, or one problem per line and exits 1. Bad arguments
exit 2. Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DISCLAIMER = (
    "This report was produced by AI agents using publicly available information "
    "and the details you provided. Figures may be incomplete, out of date or wrong; "
    "each is marked sourced, estimated or assumed. It is not financial, legal, tax "
    "or investment advice. Check important figures yourself and talk to real "
    "customers before acting."
)
RESULT = "30_assessment/scorecard_result.json"
VERDICTS = ("Go to test", "Pivot", "Stop")
MAX_TEST_DAYS = 90
SCEPTIC = "30_assessment/sceptic.md"
SCEPTIC_MAX_WORDS = 5000
# "<set-up> weeks set-up plus <live> weeks live (<days> days)"; the words and days are optional.
DURATION = re.compile(
    r"(\d+)[ -]weeks?(?: of)?(?: set-up)? plus (\d+)(?: live)?[ -]weeks?(?: live)?(?: \((\d+) days\))?")

# Files each stage adds, in order. Stage 4b (the re-check) is counted inside stage 4.
QUICK = [
    ["00_brief.md"],
    ["10_research/market_competition.md", "10_research/customer_demand.md",
     "10_research/founder_fit.md", "sources.md"],
    ["20_model/quick_model.md"],
    ["30_assessment/sceptic.md", "30_assessment/scorecard_inputs.json", RESULT],
    ["50_decision/decision_pack.md", "50_decision/report.html"],
]
FULL = [
    ["00_brief.md"],
    ["10_research/market_region.md", "10_research/competition.md",
     "10_research/customer_demand.md", "10_research/regulation_structure.md",
     "10_research/founder_fit.md", "10_research/funding_climate.md", "sources.md"],
    {"A": ["20_draft/strategy_report.md", "20_draft/model_v1.csv"],
     "B": ["20_draft/uploaded_report.md"]},
    ["30_assessment/sceptic.md", "30_assessment/banker.md",
     "30_assessment/scorecard_inputs.json", RESULT],
    ["40_plan/business_model.md", "40_plan/operations_product.md",
     "40_plan/financials.md", "40_plan/model_v2.csv", "30_assessment/sceptic_recheck.md"],
    ["50_decision/test_plan.md", "50_decision/gate_tracker.csv",
     "50_decision/decision_memo.md", "50_decision/full_plan.md", "50_decision/report.html"],
]


def expected_files(mode: str, path: str, stage: int) -> list[str]:
    """Every file required up to and including `stage`, in stage order."""
    if mode not in ("quick", "full"):
        raise ValueError(f"mode must be quick or full, not {mode!r}")
    stages = QUICK if mode == "quick" else FULL
    if mode == "full" and path not in ("A", "B"):
        raise ValueError(f"path must be A or B in a full review, not {path!r}")
    if not isinstance(stage, int) or not 0 <= stage < len(stages):
        raise ValueError(f"stage must be 0 to {len(stages) - 1} for {mode}, not {stage!r}")
    files: list[str] = []
    for added in stages[: stage + 1]:
        files.extend(added[path] if isinstance(added, dict) else added)
    return files


def _flat(text: str) -> str:
    """Drop Markdown quote markers and collapse whitespace."""
    lines = (line.strip().lstrip(">").strip() for line in text.splitlines())
    return " ".join(" ".join(lines).split())


def test_days(text: str) -> list[int]:
    """Days of every test duration written as set-up plus live weeks."""
    days = []
    for m in DURATION.finditer(text):
        weeks = (int(m.group(1)) + int(m.group(2))) * 7
        days.append(max(weeks, int(m.group(3))) if m.group(3) else weeks)
    return days


def check(run_dir: Path, mode: str, path: str, stage: int) -> list[str]:
    """Return the problems found in run_dir for this stage; empty means ok."""
    run_dir = Path(run_dir)
    problems = []
    for rel in expected_files(mode, path, stage):
        target = run_dir / rel
        if not target.is_file() or target.stat().st_size == 0:
            problems.append(f"missing or empty: {rel}")

    result = run_dir / RESULT
    if stage >= 3 and result.is_file() and result.stat().st_size > 0:
        try:
            data = json.loads(result.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            data = None
        if not isinstance(data, dict) or "verdict" not in data:
            problems.append(f"not valid scorecard JSON with a verdict: {RESULT}")
        elif data["verdict"] not in VERDICTS:
            problems.append(f"verdict is not Go to test, Pivot or Stop: {RESULT}")

    duration_files = []
    sceptic = run_dir / SCEPTIC
    if stage >= 3 and sceptic.is_file():
        text = sceptic.read_text(encoding="utf-8", errors="replace")
        words = len(text.split())
        if words > SCEPTIC_MAX_WORDS:
            problems.append(f"over 5,000 words: {SCEPTIC} ({words} words)")
        duration_files.append((SCEPTIC, text))

    decision = run_dir / "50_decision"
    if decision.is_dir():
        for md in sorted(decision.glob("*.md")):
            duration_files.append((f"50_decision/{md.name}",
                                   md.read_text(encoding="utf-8", errors="replace")))
    for rel, text in duration_files:
        longest = max(test_days(text), default=0)
        if longest > MAX_TEST_DAYS:
            problems.append(f"test longer than 90 days: {rel} ({longest} days)")

    if decision.is_dir():
        for md in sorted(decision.glob("*.md")) + sorted(decision.glob("*.html")):
            text = md.read_text(encoding="utf-8", errors="replace")
            if md.suffix == ".html":
                text = re.sub(r"<[^>]+>", " ", text)
            if md.stat().st_size and DISCLAIMER not in _flat(text):
                problems.append(f"disclaimer missing: 50_decision/{md.name}")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check a Before You Build run folder.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--mode", required=True, choices=["quick", "full"])
    parser.add_argument("--path", choices=["A", "B"], default=None)
    parser.add_argument("--stage", required=True, type=int)
    args = parser.parse_args(argv)
    if not args.run_dir.is_dir():
        print(f"error: run folder not found: {args.run_dir}", file=sys.stderr)
        return 2
    try:
        path = "A" if args.mode == "quick" else args.path  # --path is ignored in quick mode
        problems = check(args.run_dir, args.mode, path, args.stage)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if problems:
        print("\n".join(problems))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
