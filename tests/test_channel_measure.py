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

    def test_fail_line_fallback(self):
        block = read(REF + "conventions.md").split("## Channel measure", 1)[1].split("\n## ", 1)[0]
        for phrase in ("If the Moderate scenario already never breaks even within 24 months",
                       "never pays back what it cost to win them",
                       "1 / monthly churn", "one-off cost per new customer"):
            self.assertIn(phrase, block, phrase)

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
