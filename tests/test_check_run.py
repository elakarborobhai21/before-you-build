import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import DISCLAIMER, REPO

sys.path.insert(0, str(REPO / "scripts"))
from check_run import check, expected_files  # noqa: E402

CLI = REPO / "scripts" / "check_run.py"
RESULT = {"readiness_score": 60, "verdict": "Pivot", "confidence": "Medium", "reasons": []}


def build(run_dir: Path, files, disclaimer=True):
    """Create each file; Markdown files end with the disclaimer when asked."""
    for rel in files:
        path = run_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith("scorecard_result.json"):
            path.write_text(json.dumps(RESULT), encoding="utf-8")
        elif rel.endswith(".md") or rel.endswith(".html"):
            path.write_text("# x\n\n> " + DISCLAIMER + "\n" if disclaimer else "# x\n",
                            encoding="utf-8")
        else:
            path.write_text("{}\n", encoding="utf-8")


class ExpectedFilesTest(unittest.TestCase):
    def test_quick_stage_lists(self):
        self.assertEqual(expected_files("quick", "A", 1), [
            "00_brief.md",
            "10_research/market_competition.md",
            "10_research/customer_demand.md",
            "10_research/founder_fit.md",
            "sources.md",
        ])
        self.assertEqual(expected_files("quick", "A", 0), ["00_brief.md"])
        q3 = expected_files("quick", "B", 3)
        for rel in ["20_model/quick_model.md", "30_assessment/sceptic.md",
                    "30_assessment/scorecard_inputs.json", "30_assessment/scorecard_result.json"]:
            self.assertIn(rel, q3)
        self.assertNotIn("30_assessment/banker.md", q3)
        self.assertEqual(expected_files("quick", "A", 4)[-2:],
                         ["50_decision/decision_pack.md", "50_decision/report.html"])
        self.assertEqual(expected_files("full", "B", 5)[-1], "50_decision/report.html")
        self.assertEqual(expected_files("quick", "A", 4), expected_files("quick", "B", 4))

    def test_full_path_b_skips_draft(self):
        a2 = expected_files("full", "A", 2)
        b2 = expected_files("full", "B", 2)
        self.assertIn("20_draft/strategy_report.md", a2)
        self.assertIn("20_draft/model_v1.csv", a2)
        self.assertNotIn("20_draft/strategy_report.md", b2)
        self.assertNotIn("20_draft/model_v1.csv", b2)
        self.assertIn("20_draft/uploaded_report.md", b2)
        self.assertNotIn("20_draft/uploaded_report.md", a2)

    def test_full_later_stages(self):
        f1 = expected_files("full", "A", 1)
        self.assertEqual(len(f1), 8)
        f3 = expected_files("full", "A", 3)
        for rel in ["30_assessment/sceptic.md", "30_assessment/banker.md",
                    "30_assessment/scorecard_inputs.json", "30_assessment/scorecard_result.json"]:
            self.assertIn(rel, f3)
        f4 = expected_files("full", "B", 4)
        for rel in ["40_plan/business_model.md", "40_plan/operations_product.md",
                    "40_plan/financials.md", "40_plan/model_v2.csv",
                    "30_assessment/sceptic_recheck.md"]:
            self.assertIn(rel, f4)
        f5 = expected_files("full", "A", 5)
        for rel in ["50_decision/test_plan.md", "50_decision/gate_tracker.csv",
                    "50_decision/decision_memo.md", "50_decision/full_plan.md"]:
            self.assertIn(rel, f5)
        self.assertEqual(len(f5), len(set(f5)))

    def test_bad_arguments(self):
        for args in [("quick", "A", 5), ("full", "A", 6), ("full", "A", -1),
                     ("other", "A", 1), ("full", "C", 2)]:
            with self.assertRaises(ValueError):
                expected_files(*args)


class CheckTest(unittest.TestCase):
    def test_check_reports_missing_and_disclaimer(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            files = expected_files("quick", "A", 4)
            build(run, [f for f in files if f != "50_decision/decision_pack.md"])
            problems = check(run, "quick", "A", 4)
            self.assertEqual(len(problems), 1)
            self.assertIn("50_decision/decision_pack.md", problems[0])
            self.assertIn("missing", problems[0])

            build(run, ["50_decision/decision_pack.md"], disclaimer=False)
            problems = check(run, "quick", "A", 4)
            self.assertEqual(len(problems), 1)
            self.assertIn("50_decision/decision_pack.md", problems[0])
            self.assertIn("disclaimer", problems[0])

            build(run, ["50_decision/decision_pack.md"])
            self.assertEqual(check(run, "quick", "A", 4), [])

    def test_disclaimer_wrapped_across_quote_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("quick", "A", 4))
            words = DISCLAIMER.split(" ")
            half = len(words) // 2
            text = "# x\n\n> " + " ".join(words[:half]) + "\n> " + " ".join(words[half:]) + "\n"
            (run / "50_decision/decision_pack.md").write_text(text, encoding="utf-8")
            self.assertEqual(check(run, "quick", "A", 4), [])

    def test_sources_missing_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, [f for f in expected_files("full", "A", 1) if f != "sources.md"])
            problems = check(run, "full", "A", 1)
            self.assertEqual(len(problems), 1)
            self.assertIn("sources.md", problems[0])

    def test_scorecard_result_must_be_json_with_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("quick", "A", 3))
            self.assertEqual(check(run, "quick", "A", 3), [])
            result = run / "30_assessment/scorecard_result.json"
            for bad in ["", "not json", json.dumps({"score": 1}), json.dumps([1])]:
                result.write_text(bad, encoding="utf-8")
                problems = check(run, "quick", "A", 3)
                self.assertEqual(len(problems), 1, bad)
                self.assertIn("scorecard_result.json", problems[0])

    def test_scorecard_verdict_must_be_a_verdict_word(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("quick", "A", 3))
            result = run / "30_assessment/scorecard_result.json"
            for good in ("Go to test", "Pivot", "Stop"):
                result.write_text(json.dumps(dict(RESULT, verdict=good)), encoding="utf-8")
                self.assertEqual(check(run, "quick", "A", 3), [], good)
            for bad in ("Go", "pivot", "", None):
                result.write_text(json.dumps(dict(RESULT, verdict=bad)), encoding="utf-8")
                problems = check(run, "quick", "A", 3)
                self.assertEqual(len(problems), 1, bad)
                self.assertIn("scorecard_result.json", problems[0])

    def test_report_html_needs_the_disclaimer(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("quick", "A", 4))
            self.assertEqual(check(run, "quick", "A", 4), [])
            (run / "50_decision/report.html").write_text("<p>no disclaimer</p>", encoding="utf-8")
            self.assertIn("disclaimer missing: 50_decision/report.html",
                          check(run, "quick", "A", 4))

    def test_empty_file_counts_as_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("quick", "A", 1))
            (run / "10_research/founder_fit.md").write_text("", encoding="utf-8")
            problems = check(run, "quick", "A", 1)
            self.assertEqual(len(problems), 1)
            self.assertIn("10_research/founder_fit.md", problems[0])


class LimitsTest(unittest.TestCase):
    """A test runs 90 days at most; sceptic.md stays within 5,000 words."""

    def quick_run(self, tmp, pack_duration=None, sceptic_text=None):
        run = Path(tmp)
        build(run, expected_files("quick", "A", 4))
        if pack_duration is not None:
            (run / "50_decision/decision_pack.md").write_text(
                f"# x\n\n- Duration: {pack_duration}\n\n> {DISCLAIMER}\n", encoding="utf-8")
        if sceptic_text is not None:
            (run / "30_assessment/sceptic.md").write_text(sceptic_text, encoding="utf-8")
        return run

    def test_over_90_days_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.quick_run(tmp, "3 weeks set-up plus 10 weeks live (91 days), from a to b")
            problems = check(run, "quick", "A", 4)
            self.assertIn("test longer than 90 days: 50_decision/decision_pack.md (91 days)",
                          problems)

    def test_weeks_counted_when_days_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.quick_run(tmp, "4 weeks set-up plus 9 weeks live")
            problems = check(run, "quick", "A", 4)
            self.assertIn("test longer than 90 days: 50_decision/decision_pack.md (91 days)",
                          problems)

    def test_live_weeks_word_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.quick_run(tmp, "3 weeks set-up plus 10 live weeks")
            problems = check(run, "quick", "A", 4)
            self.assertIn("test longer than 90 days: 50_decision/decision_pack.md (91 days)",
                          problems)

    def test_90_days_or_fewer_is_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.quick_run(tmp, "2 weeks set-up plus 6 weeks live (56 days)")
            self.assertEqual(check(run, "quick", "A", 4), [])
            run = self.quick_run(tmp, "3 weeks set-up plus 9 weeks live (84 days)")
            self.assertEqual(check(run, "quick", "A", 4), [])

    def test_sceptic_question_10_duration_checked_at_stage_3(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = ("# x\n\n### 10. What is the cheapest way to find out within 90 days?\n\n"
                    "Duration: 3 weeks set-up plus 10 weeks live (91 days).\n")
            run = self.quick_run(tmp, sceptic_text=text)
            problems = check(run, "quick", "A", 3)
            self.assertIn("test longer than 90 days: 30_assessment/sceptic.md (91 days)",
                          problems)

    def test_sceptic_word_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.quick_run(tmp, sceptic_text="word " * 5000)
            self.assertEqual(check(run, "quick", "A", 3), [])
            run = self.quick_run(tmp, sceptic_text="word " * 5001)
            self.assertIn("over 5,000 words: 30_assessment/sceptic.md (5001 words)",
                          check(run, "quick", "A", 3))


class CliTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)],
                              capture_output=True, text=True)

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            build(run, expected_files("full", "B", 2))
            p = self.run_cli(run, "--mode", "full", "--path", "B", "--stage", "2")
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertEqual(p.stdout.strip(), "ok")

            p = self.run_cli(run, "--mode", "full", "--path", "A", "--stage", "2")
            self.assertEqual(p.returncode, 1)
            lines = p.stdout.strip().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertTrue(any("strategy_report.md" in line for line in lines))

            p = self.run_cli(run, "--mode", "quick", "--stage", "0")
            self.assertEqual(p.returncode, 0)

            build(run, expected_files("quick", "A", 2))
            for path in ("A", "B"):
                p = self.run_cli(run, "--mode", "quick", "--path", path, "--stage", "2")
                self.assertEqual((p.returncode, p.stdout.strip()), (0, "ok"), path)

            p = self.run_cli(run, "--mode", "quick", "--stage", "9")
            self.assertEqual(p.returncode, 2)
            p = self.run_cli(run, "--mode", "full", "--stage", "1")
            self.assertEqual(p.returncode, 2)
            p = self.run_cli(run / "nope", "--mode", "quick", "--stage", "0")
            self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
