"""The HTML report: built from the run files, self-contained, escaped, in both modes."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import DISCLAIMER, REPO, read

sys.path.insert(0, str(REPO / "scripts"))
from render_report import render  # noqa: E402

SCRIPT = REPO / "scripts" / "render_report.py"
EXAMPLE = REPO / "examples" / "lagos-delivery-quick-check"
AREA_NAMES = ["Customer pull", "Route to customers", "Money per transaction", "Cash to proof",
              "Competitive response", "Team and commitment", "Rules and operations"]
RATINGS = {"customer_pull": 1, "route_to_customers": 2, "money_per_transaction": 1,
           "cash_to_proof": 2, "competitive_response": 1, "team_commitment": 2,
           "rules_operations": 1}


def make_run(tmp, pack, verdict="Pivot", full=False, extra=None):
    run = Path(tmp)
    (run / "30_assessment").mkdir(parents=True, exist_ok=True)
    (run / "50_decision").mkdir(parents=True, exist_ok=True)
    (run / "30_assessment/scorecard_result.json").write_text(json.dumps(
        {"readiness_score": 48, "verdict": verdict, "confidence": "Medium", "reasons": []}))
    (run / "30_assessment/scorecard_inputs.json").write_text(json.dumps(
        {"ratings": RATINGS, "test_measures_unit_economics": True,
         "fulltime_within_6_months": True, "label_counts": {"S": 3, "E": 4, "A": 2}}))
    name = "decision_memo.md" if full else "decision_pack.md"
    (run / "50_decision" / name).write_text(pack, encoding="utf-8")
    for rel, text in (extra or {}).items():
        (run / rel).write_text(text, encoding="utf-8")
    return run


PACK = """# Decision pack: Test idea

Mode: Quick Check
Date: 2026-10-20

## Verdict

**Pivot**, copied unchanged.

## What the numbers say

| Measure | Defensive | Moderate | Optimistic |
|---|---|---|---|
| Contribution | 1 [E] | 2 [E] | 3 [E] |

## The test

- Pass line: at least 2 [E]
- Fail line: below 1 [E]
- Channel measure: cost to win a paying customer at or below 5 [E]

> """ + DISCLAIMER + "\n"


class RenderTests(unittest.TestCase):
    def test_example_report_is_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            subprocess.run(["cp", "-r", str(EXAMPLE), str(run)], check=True)
            html = render(run).read_text(encoding="utf-8")
        self.assertEqual(html, read("examples/lagos-delivery-quick-check/50_decision/report.html"),
                         "re-run scripts/render_report.py on the example")

    def test_example_shows_the_run(self):
        html = read("examples/lagos-delivery-quick-check/50_decision/report.html")
        pack = read("examples/lagos-delivery-quick-check/50_decision/decision_pack.md")
        self.assertIn("Lagos same-day parcel delivery", html)
        self.assertIn('<div class="vword">Pivot</div>', html)
        self.assertIn('<span class="n">48</span>', html)
        self.assertIn(DISCLAIMER, html)
        for title in re.findall(r"(?m)^## (.+)$", pack):
            if title != "Verdict":
                self.assertIn(f"<h2>{title}</h2>", html, title)
        for name in AREA_NAMES:
            self.assertIn(name, html)
        for sc in ("Defensive", "Moderate", "Optimistic"):
            self.assertIn(f'data-sc="{sc}"', html)

    def test_self_contained(self):
        html = read("examples/lagos-delivery-quick-check/50_decision/report.html")
        self.assertNotRegex(html, r"<script[^>]+src=")
        self.assertNotIn("<link", html)
        self.assertNotIn("@import", html)
        self.assertNotIn("url(", html)
        self.assertIn("Content-Security-Policy", html)

    def test_verdict_comes_from_the_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = render(make_run(tmp, PACK, verdict="Stop")).read_text()
        self.assertIn('<div class="vword">Stop</div>', html)
        self.assertIn('class="vcard stop"', html)

    def test_escapes_run_text(self):
        bad = PACK.replace("Mode: Quick Check",
                           "Mode: <script>alert(1)</script>\n\nSee [x](javascript:alert(1)) "
                           "and [S](javascript:alert(2)) <img src=x onerror=alert(3)>")
        with tempfile.TemporaryDirectory() as tmp:
            html = render(make_run(tmp, bad)).read_text()
        self.assertNotIn("<script>alert", html)
        self.assertNotIn("<img", html)
        self.assertNotIn('href="javascript', html.lower())
        self.assertIn("&lt;script&gt;", html)

    def test_test_rows_marked(self):
        with tempfile.TemporaryDirectory() as tmp:
            html = render(make_run(tmp, PACK)).read_text()
        for cls in ("pass", "fail", "channel"):
            self.assertIn(f'class="trow {cls}"', html)
        self.assertIn('<span class="lab e"', html)

    def test_full_review_adds_test_plan_and_gate_tracker(self):
        memo = PACK.replace("Decision pack", "Decision memo").replace(
            "What the numbers say", "Key numbers")
        plan = ("# Test plan: Test idea\n\n## Channel measure\n\n- Main channel: referrals\n\n"
                "## Fallback pivots\n\n1. **Another city.** Cheaper.\n")
        gate = ("measure,formula,pass_line,fail_line,measured_value,date_measured,status\n"
                "cost to win a paying customer,spend / customers (minimum 20),<= 5,> 9,,,not measured\n")
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(tmp, memo, full=True, extra={
                "50_decision/test_plan.md": plan, "50_decision/gate_tracker.csv": gate})
            html = render(run).read_text()
        self.assertIn("Full Review", html)
        self.assertIn("<h2>Test plan: Channel measure</h2>", html)
        self.assertIn("<h2>Test plan: Fallback pivots</h2>", html)
        self.assertIn("Gate tracker", html)
        self.assertIn("spend / customers (minimum 20)", html)
        self.assertIn('href="full_plan.md"', html)

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(tmp, PACK)
            p = subprocess.run([sys.executable, str(SCRIPT), str(run)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue((run / "50_decision/report.html").is_file())
            (run / "50_decision/decision_pack.md").unlink()
            p = subprocess.run([sys.executable, str(SCRIPT), str(run)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn("decision_pack.md", p.stderr)


class WiringTests(unittest.TestCase):
    def test_skill_runs_the_renderer(self):
        skill = read("skills/before-you-build/SKILL.md")
        self.assertEqual(skill.count('python3 "<PLUGIN_ROOT>/scripts/render_report.py" "<RUN_DIR>"'), 2)
        self.assertIn("| `50_decision/report.html` | you, with `scripts/render_report.py` |", skill)
        summary = skill.split("## Final summary", 1)[1].split("\n## ", 1)[0]
        self.assertIn("50_decision/report.html", summary)

    def test_readme_lists_the_report(self):
        readme = read("README.md")
        self.assertIn("`50_decision/report.html`", readme)


if __name__ == "__main__":
    unittest.main()
