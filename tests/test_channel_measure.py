"""Every test includes a channel measure: the real cost to win a paying customer."""
import unittest

from tests.agentlint import section
from tests.helpers import read

REF = "skills/before-you-build/references/"
TEMPLATES = "skills/before-you-build/templates/"
NAME = "cost to win a paying customer"
CONVENTION = "`Channel measure` in conventions.md"


def agent(stem):
    return read(f"agents/{stem}.md")


class ChannelMeasureTests(unittest.TestCase):
    def test_defined_once_in_conventions(self):
        text = read(REF + "conventions.md")
        block = text.split("## Channel measure", 1)[1].split("\n## ", 1)[0]
        for phrase in (NAME, "main channel", "real spend or real outreach",
                       "/ paying customers won through it",
                       "Moderate scenario", "Defensive scenario",
                       "never within 24 months", "minimum sample",
                       "founder hours", "alongside the main test",
                       "inside its budget and dates"):
            self.assertIn(phrase, block, phrase)

    def test_line_rule(self):
        block = read(REF + "conventions.md").split("## Channel measure", 1)[1].split("\n## ", 1)[0]
        for phrase in ("Payback cost:", "1 / monthly churn", "one-off cost per new customer",
                       "the transactions a fixed-length offer includes",
                       "Moderate cost at or below the payback cost",
                       "If the Moderate scenario already never breaks even within 24 months",
                       "the fail line is the payback cost",
                       "Moderate cost above the payback cost",
                       "the pass line is at or below the payback cost and the fail line is at or above the Moderate cost",
                       "The pass line is always lower than the fail line; never set them equal",
                       "Defensive scenario's cost to acquire a customer",
                       "Between the lines: change the price or the channel once",
                       "Say which rule set each line"):
            self.assertIn(phrase, block, phrase)

    def test_agents_use_the_line_rule(self):
        for stem in ("byb-sceptical-investor", "byb-validation-test-designer"):
            cover = section(agent(stem), "Must cover")
            self.assertIn("set by the rule in conventions.md", cover, stem)
            self.assertIn("payback cost", cover, stem)
            self.assertIn("lower than the fail line", cover, stem)

    def test_sceptic_question_10_includes_it(self):
        cover = section(agent("byb-sceptical-investor"), "Must cover")
        self.assertIn("For question 10, the test always includes the channel measure", cover)
        self.assertIn(CONVENTION, cover)

    def test_recheck_keeps_it(self):
        text = agent("byb-sceptical-investor")
        recheck = text.split("Re-check", 1)[1]
        self.assertIn("keeps the channel measure", recheck)

    def test_test_designer_covers_it(self):
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        self.assertIn("**Channel measure.**", cover)
        self.assertIn(CONVENTION, cover)
        self.assertIn("even when the riskiest assumption is about the product", cover)
        output = section(agent("byb-validation-test-designer"), "Output")
        self.assertIn("the channel measure has its own row", output)

    def test_report_writer_shows_it(self):
        text = agent("byb-report-writer")
        quick = section(text, "Quick Check")
        self.assertIn("the channel measure", quick)
        self.assertIn("If question 10 has no channel measure", quick)

    def test_templates_have_a_line_for_it(self):
        pack = read(TEMPLATES + "decision_pack.md").split("## The test", 1)[1]
        self.assertRegex(pack, r"(?m)^- Channel measure: ")
        plan = read(TEMPLATES + "test_plan.md")
        self.assertIn("## Channel measure", plan)
        self.assertLess(plan.index("## Channel measure"),
                        plan.index("## Go/no-go date"))
        memo = read(TEMPLATES + "decision_memo.md").split("## The test", 1)[1]
        self.assertRegex(memo, r"(?m)^- Channel measure: ")


if __name__ == "__main__":
    unittest.main()
