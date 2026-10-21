"""The 24-month model: reproduces the example, rejects bad inputs, and matches the report's script."""
import copy
import json
import re
import shutil
import subprocess
import sys
import unittest

from tests.helpers import REPO, read

sys.path.insert(0, str(REPO / "scripts"))
import model  # noqa: E402
from render_report import MODEL_JS  # noqa: E402

INPUTS = REPO / "examples" / "lagos-delivery-quick-check" / "20_model" / "model_inputs.json"


def load():
    return json.loads(INPUTS.read_text(encoding="utf-8"))


class ModelTests(unittest.TestCase):
    def test_reproduces_the_example_quick_model(self):
        # Key numbers from examples/.../20_model/quick_model.md, which the agent rounded.
        res = model.run(load())
        expect = {"Defensive": (-937.1, None, 9_817_894, 103_063_886, 6, [542, 1098, 2409]),
                  "Moderate": (87.5, None, 9_204_917, 75_794_995, 7, [1613, 3896, 12091]),
                  "Optimistic": (1052.6, 4, 6_062_822, 6_062_822, None, [4003, 10844, 42174])}
        for sc, (contrib, be, test, need, out, tx) in expect.items():
            r = res[sc]
            self.assertAlmostEqual(r["contribution_per_transaction"], contrib, places=1)
            self.assertEqual(r["break_even_month"], be, sc)
            self.assertLess(abs(r["cash_for_90_day_test"] - test) / test, 0.001, sc)
            self.assertLess(abs(r["cash_need"] - need) / need, 0.001, sc)
            self.assertEqual(r["cash_runs_out_month"], out, sc)
            self.assertEqual([round(r["months"][m - 1]["transactions"]) for m in (6, 12, 24)], tx, sc)
        self.assertTrue(res["Moderate"]["still_falling"])
        self.assertAlmostEqual(res["Moderate"]["cost_to_win_customer"], 27_500)

    def test_conversion_rate_moves_the_numbers(self):
        inputs = load()
        sc, months, cash = inputs["scenarios"]["Moderate"], inputs["months"], inputs["founder_cash"]
        base = model.calc(sc, months, cash)
        higher = model.calc(sc, months, cash, conversion_rate=0.25)
        self.assertGreater(higher["months"][-1]["active_customers"], base["months"][-1]["active_customers"])
        self.assertLess(higher["cost_to_win_customer"], base["cost_to_win_customer"])
        self.assertEqual(higher["contribution_per_transaction"], base["contribution_per_transaction"])

    def test_rejects_bad_inputs(self):
        bad = []
        x = load(); del x["scenarios"]["Optimistic"]; bad.append(x)
        x = load(); x["scenarios"]["Moderate"]["conversion_rate"] = 0; bad.append(x)
        x = load(); x["scenarios"]["Moderate"]["conversion_rate"] = 10; bad.append(x)
        x = load(); x["scenarios"]["Moderate"]["unit"][0]["kind"] = "fee"; bad.append(x)
        x = load(); x["scenarios"]["Moderate"]["churn"] = "5%"; bad.append(x)
        x = load(); x["scenarios"]["Moderate"]["scaling_costs"][0]["per_transactions"] = 0; bad.append(x)
        for inputs in bad:
            with self.assertRaises(model.ModelError):
                model.run(inputs)

    def test_cli(self):
        p = subprocess.run([sys.executable, str(REPO / "scripts" / "model.py"), str(INPUTS)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Moderate", json.loads(p.stdout))
        p = subprocess.run([sys.executable, str(REPO / "scripts" / "model.py"), "/nonexistent.json"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_report_script_matches_the_engine(self):
        inputs = load()
        script = MODEL_JS + ("\nvar M=" + json.dumps(inputs) + ";var out={};"
                             "['Defensive','Moderate','Optimistic'].forEach(function(s){"
                             "out[s]=[calc(M.scenarios[s],M.months,M.founder_cash),"
                             "calc(M.scenarios[s],M.months,M.founder_cash,0.173)]});"
                             "console.log(JSON.stringify(out));")
        p = subprocess.run(["node", "-e", script], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        js = json.loads(p.stdout)
        for sc in model.SCENARIOS:
            s = inputs["scenarios"][sc]
            for got, conv in zip(js[sc], (None, 0.173)):
                want = model.calc(s, inputs["months"], inputs["founder_cash"], conv)
                for key in ("break_even_month", "cash_runs_out_month", "still_falling"):
                    self.assertEqual(got[key], want[key], f"{sc} {key}")
                for key in ("cash_need", "cash_for_90_day_test", "cost_to_win_customer"):
                    self.assertAlmostEqual(got[key], want[key], places=4, msg=f"{sc} {key}")
                self.assertAlmostEqual(got["months"][-1]["cumulative"], want["months"][-1]["cumulative"], places=3)

    def test_example_report_embeds_the_model(self):
        html = read("examples/lagos-delivery-quick-check/50_decision/report.html")
        self.assertIn('id="model-data"', html)
        for sc in model.SCENARIOS:
            self.assertIn(f'id="conv-{sc}"', html)
        data = re.search(r'<script type="application/json" id="model-data">(.*?)</script>', html, re.S)
        self.assertEqual(json.loads(data.group(1)), load())


if __name__ == "__main__":
    unittest.main()
