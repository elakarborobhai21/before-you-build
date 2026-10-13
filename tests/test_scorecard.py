import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import REPO

sys.path.insert(0, str(REPO / "scripts"))
import scorecard  # noqa: E402
from scorecard import AREAS, ScorecardError, score  # noqa: E402

CLI = REPO / "scripts" / "scorecard.py"


def all_x(x):
    return {area: x for area in AREAS}


def make(ratings, unit=True, fulltime=True, labels=None):
    return {
        "ratings": ratings,
        "test_measures_unit_economics": unit,
        "fulltime_within_6_months": fulltime,
        "label_counts": labels or {"S": 6, "E": 2, "A": 2},
    }


def with_sum(total):
    """Ratings of 1-3 (no zeros) whose values add up to total."""
    ratings = {area: 1 for area in AREAS}
    left = total - len(AREAS)
    for area in AREAS:
        step = min(2, left)
        ratings[area] += step
        left -= step
    return ratings


class ScorecardTests(unittest.TestCase):
    def test_all_strong(self):
        r = score(make(all_x(3)))
        self.assertEqual(r["readiness_score"], 100)
        self.assertEqual(r["verdict"], "Go to test")
        self.assertEqual(r["confidence"], "High")

    def test_all_adequate(self):
        r = score(make(all_x(2)))
        self.assertEqual(r["readiness_score"], 67)
        self.assertEqual(r["verdict"], "Go to test")

    def test_thresholds(self):
        for total, expected, verdict in [(13, 62, "Pivot"), (9, 43, "Pivot"), (8, 38, "Stop")]:
            r = score(make(with_sum(total)))
            self.assertEqual((r["readiness_score"], r["verdict"]), (expected, verdict), total)

    def test_one_fatal_caps_at_pivot(self):
        ratings = all_x(3)
        ratings["rules_operations"] = 0
        r = score(make(ratings))
        self.assertEqual(r["readiness_score"], 86)
        self.assertEqual(r["verdict"], "Pivot")
        self.assertEqual(len(r["reasons"]), 1)
        self.assertIn("Fatal", r["reasons"][0])

    def test_two_fatal_is_stop(self):
        ratings = all_x(3)
        ratings["rules_operations"] = 0
        ratings["team_commitment"] = 0
        r = score(make(ratings))
        self.assertEqual(r["readiness_score"], 71)
        self.assertEqual(r["verdict"], "Stop")
        self.assertTrue(r["reasons"])

    def test_weak_unit_economics_not_measured(self):
        ratings = all_x(3)
        ratings["money_per_transaction"] = 1
        r = score(make(ratings, unit=False))
        self.assertEqual(r["verdict"], "Pivot")
        self.assertEqual(len(r["reasons"]), 1)
        r = score(make(ratings, unit=True))
        self.assertEqual(r["verdict"], "Go to test")
        self.assertEqual(r["reasons"], [])

    def test_no_fulltime_founder(self):
        r = score(make(all_x(3), fulltime=False))
        self.assertEqual(r["verdict"], "Pivot")
        self.assertEqual(len(r["reasons"]), 1)

    def test_low_score_stays_stop_with_fatal(self):
        ratings = all_x(1)
        ratings["customer_pull"] = 0
        r = score(make(ratings))
        self.assertEqual(r["readiness_score"], 29)
        self.assertEqual(r["verdict"], "Stop")

    def test_confidence(self):
        for labels, expected in [
            ({"S": 0, "E": 0, "A": 0}, "Low"),
            ({"S": 2, "E": 2, "A": 6}, "Low"),
            ({"S": 3, "E": 4, "A": 3}, "Medium"),
            ({"S": 6, "E": 2, "A": 2}, "High"),
            ({"S": 0, "E": 19, "A": 8}, "Low"),
            ({"S": 2, "E": 6, "A": 2}, "Medium"),
            ({"S": 1, "E": 8, "A": 1}, "Low"),
            ({"S": 5, "E": 5, "A": 0}, "Medium"),
            ({"S": 2, "E": 3, "A": 5}, "Medium"),
        ]:
            r = score(make(all_x(3), labels=labels))
            self.assertEqual(r["confidence"], expected, labels)

    def test_bad_input(self):
        missing = all_x(3)
        del missing["team_commitment"]
        high = all_x(3)
        high["customer_pull"] = 4
        text = all_x(3)
        text["cash_to_proof"] = "Strong"
        boolean = all_x(3)
        boolean["cash_to_proof"] = True
        unknown = all_x(3)
        unknown["vibes"] = 2
        for ratings, key in [
            (missing, "team_commitment"),
            (high, "customer_pull"),
            (text, "cash_to_proof"),
            (boolean, "cash_to_proof"),
            (unknown, "vibes"),
        ]:
            with self.assertRaises(ScorecardError) as ctx:
                score(make(ratings))
            self.assertIn(key, str(ctx.exception))

    def test_bad_flags_and_labels(self):
        for key, value in [
            ("test_measures_unit_economics", "yes"),
            ("fulltime_within_6_months", 1),
        ]:
            data = make(all_x(3))
            data[key] = value
            with self.assertRaises(ScorecardError) as ctx:
                score(data)
            self.assertIn(key, str(ctx.exception))
        for labels in [{"S": 1, "E": 1}, {"S": 1, "E": 1, "A": -1}, {"S": 1, "E": 1, "A": 1.5},
                       {"S": 1, "E": 1, "A": 1, "X": 1}, {"S": True, "E": 1, "A": 1}]:
            with self.assertRaises(ScorecardError) as ctx:
                score(make(all_x(3), labels=labels))
            self.assertIn("label_counts", str(ctx.exception))
        data = make(all_x(3))
        del data["ratings"]
        with self.assertRaises(ScorecardError) as ctx:
            score(data)
        self.assertIn("ratings", str(ctx.exception))
        with self.assertRaises(ScorecardError):
            score([])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            good.write_text(json.dumps(make(all_x(3))), encoding="utf-8")
            p = subprocess.run([sys.executable, str(CLI), str(good)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("verdict", json.loads(p.stdout))

            bad_input = Path(tmp) / "bad.json"
            bad_input.write_text(json.dumps(make({"customer_pull": 2})), encoding="utf-8")
            not_json = Path(tmp) / "notjson.json"
            not_json.write_text("{nope", encoding="utf-8")
            for path in (bad_input, not_json, Path(tmp) / "missing.json"):
                p = subprocess.run([sys.executable, str(CLI), str(path)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 2, path)
                self.assertEqual(p.stdout, "")
                self.assertTrue(p.stderr.startswith("error:"), p.stderr)
            p = subprocess.run([sys.executable, str(CLI)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 2)
            self.assertEqual(p.stdout, "")


if __name__ == "__main__":
    unittest.main()
