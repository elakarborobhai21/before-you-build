import re
import unittest

from tests.helpers import DISCLAIMER, REPO, frontmatter, read

SKILL = "skills/before-you-build/SKILL.md"
TOPICS = ["The idea", "Region and country", "Target customer", "Founders",
          "Money and time", "Existing report", "Mode", "Currency"]
REGIONS = ["South Asia", "Southeast Asia", "East Asia", "Middle East & North Africa",
           "Sub-Saharan Africa", "Europe", "North America", "Latin America"]


def text():
    return read(SKILL)


def section(body, heading):
    """Text under a heading line, up to the next heading of the same or higher level."""
    match = re.search(rf"^(#+) {re.escape(heading)}.*$", body, re.M)
    assert match, heading
    level = len(match.group(1))
    rest = body[match.end():]
    end = re.search(rf"^#{{1,{level}}} ", rest, re.M)
    return rest[: end.start()] if end else rest


def stages(body, heading):
    """Map each '### Stage X' heading under `heading` to its text."""
    part = section(body, heading)
    found = {}
    for match in re.finditer(r"^### Stage (\w+)[^\n]*\n", part, re.M):
        rest = part[match.end():]
        end = re.search(r"^### ", rest, re.M)
        found[match.group(1)] = match.group(0) + (rest[: end.start()] if end else rest)
    return found


class SkillTests(unittest.TestCase):
    def test_skill_frontmatter(self):
        fm = frontmatter(text())
        self.assertEqual(fm["name"], "before-you-build")
        self.assertIn("Quick Check", fm["description"])
        self.assertIn("Full Review", fm["description"])

    def test_skill_dispatches_every_agent(self):
        body = text()
        stems = [p.stem for p in (REPO / "agents").glob("byb-*.md")]
        self.assertEqual(len(stems), 17)
        for stem in stems:
            self.assertIn(stem, body, stem)
        self.assertIn("subagent_type", body)

    def test_intake_topics(self):
        intake = section(text(), "Intake")
        positions = [intake.find(f"**{topic}**") for topic in TOPICS]
        self.assertNotIn(-1, positions, dict(zip(TOPICS, positions)))
        self.assertEqual(positions, sorted(positions))
        for region in REGIONS:
            self.assertIn(region, intake, region)
        self.assertIn("one topic at a time", intake)
        self.assertRegex(intake, r"Quick Check.{0,80}only.{0,40}role.{0,60}full-time.{0,80}conflict")

    def test_parallel_and_checks(self):
        body = text()
        full = stages(body, "Full Review stages")
        quick = stages(body, "Quick Check stages")
        self.assertEqual(sorted(quick), ["1", "2", "3", "4"])
        self.assertEqual(sorted(full), ["1", "2", "3", "4", "4b", "5"])
        for name in ("1", "3", "4"):
            self.assertIn("in parallel", full[name], name)
        self.assertIn("in parallel", quick["1"])
        for label, found in (("quick", quick), ("full", full)):
            for name, part in found.items():
                self.assertIn("scripts/check_run.py", part, f"{label} stage {name}")
                number = name.rstrip("b")
                self.assertIn(f"--stage {number}", part, f"{label} stage {name}")
        self.assertIn("one message", body)

    def test_stage_agents_and_modes(self):
        body = text()
        full = stages(body, "Full Review stages")
        quick = stages(body, "Quick Check stages")
        for stem in ("byb-market-competition-scout", "byb-customer-demand-analyst",
                     "byb-founder-fit-reviewer"):
            self.assertIn(stem, quick["1"])
        self.assertIn("byb-quick-modeller", quick["2"])
        self.assertIn("byb-sceptical-investor", quick["3"])
        self.assertIn("byb-report-writer", quick["4"])
        self.assertIn("Quick Check", quick["4"])
        for stem in ("byb-market-region-researcher", "byb-competition-scout",
                     "byb-customer-demand-analyst", "byb-regulation-structure-mapper",
                     "byb-founder-fit-reviewer", "byb-funding-climate-scout"):
            self.assertIn(stem, full["1"])
        s2 = full["2"]
        order = [s2.find("Pass: 1"), s2.find("byb-draft-modeller"), s2.find("Pass: 2")]
        self.assertNotIn(-1, order)
        self.assertEqual(order, sorted(order))
        self.assertIn("Path A only", s2)
        for stem in ("byb-sceptical-investor", "byb-investment-banker"):
            self.assertIn(stem, full["3"])
        for stem in ("byb-business-model-designer", "byb-operations-product-planner",
                     "byb-financial-modeller"):
            self.assertIn(stem, full["4"])
        self.assertIn("re-check", full["4b"])
        s5 = full["5"]
        self.assertLess(s5.find("byb-validation-test-designer"), s5.find("byb-report-writer"))
        self.assertIn("Full Review", s5)

    def test_run_dir_plugin_root(self):
        body = text()
        for phrase in ("RUN_DIR", "PLUGIN_ROOT", "two directories above",
                       "scripts/scorecard.py", "~/before-you-build-runs/",
                       "20_draft/uploaded_report.md", "## Sources", "sources.md"):
            self.assertIn(phrase, body, phrase)

    def test_playback_before_dispatch(self):
        body = text()
        self.assertIn("read the brief back", body)
        self.assertLess(body.index("read the brief back"), body.index("Stage 1"))
        self.assertIn("clear yes", body)

    def test_review_focus_rules(self):
        body = text()
        self.assertIn("paste the text", body)
        self.assertIn("closest pack", body)
        self.assertIn("add `-2`, then `-3`", body)
        self.assertIn("re-dispatch only the agent that owns the file", body)
        self.assertIn("once, with the same prompt", body)

    def test_upgrade_path(self):
        upgrade = section(text(), "Upgrading a Quick Check to a Full Review")
        self.assertIn("10_research/", upgrade)
        self.assertIn("market_competition.md", upgrade)

    def test_final_summary_and_disclaimer(self):
        summary = section(text(), "Final summary")
        for word in ("verdict", "readiness score", "confidence", "200 words"):
            self.assertIn(word, summary)
        self.assertIn(DISCLAIMER, text())

    def test_scorecard_only_through_sceptic(self):
        body = text()
        self.assertIn("scorecard_inputs.json", body)
        self.assertRegex(body, r"(?i)never (write|edit)[^.]*scorecard")

    def test_fix_round_1_edge_cases(self):
        body = text()
        full = stages(body, "Full Review stages")
        self.assertIn("One re-dispatch because `sceptic_recheck.md` is missing or faulty is still "
                      "allowed; this rule only forbids a second revision round.", full["4b"])
        self.assertEqual(full["2"].count("`Stage: 2`"), 3)
        summary = section(body, "Final summary")
        self.assertIn("50_decision/decision_pack.md", summary)
        self.assertIn("50_decision/decision_memo.md", summary)
        self.assertIn("one exception", section(body, "Intake"))
        self.assertIn("Not applicable (Quick Check)", section(body, "Intake"))
        upgrade = section(body, "Upgrading a Quick Check to a Full Review")
        self.assertIn("`used in` paths", upgrade)
        self.assertIn("quick_check/", upgrade)

    def test_stage4_business_model_first(self):
        # Ruling R24: business model first, then operations and financials in parallel.
        s4 = stages(text(), "Full Review stages")["4"]
        designer = s4.find("byb-business-model-designer")
        parallel = s4.find("in parallel", designer)
        self.assertNotIn(-1, (designer, parallel))
        self.assertIn("`Stage: 4a`", s4)
        self.assertIn("alone", s4[designer:parallel])
        self.assertRegex(s4, r"`40_plan/business_model\.md` exists and is not empty")
        for stem in ("byb-operations-product-planner", "byb-financial-modeller"):
            self.assertLess(designer, s4.find(stem), stem)
            self.assertLess(parallel, s4.find(stem), stem)
        self.assertIn("as the offer they plan and model", s4)
        self.assertIn("the only allowed problem is `missing or empty: "
                      "30_assessment/sceptic_recheck.md`", s4)

    def test_length(self):
        self.assertLess(len(text().split()), 3000)


if __name__ == "__main__":
    unittest.main()
