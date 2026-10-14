import re
import sys
import unittest

from tests.agentlint import lint_agent, section
from tests.helpers import DISCLAIMER, REPO, frontmatter, read

sys.path.insert(0, str(REPO / "scripts"))
from scorecard import AREAS  # noqa: E402

TEMPLATES = "skills/before-you-build/templates/"

# agent stem -> (output paths, must-mentions from spec §5 "What each agent must cover")
DRAFT_AND_CRITIC_AGENTS = {
    "byb-quick-modeller": (
        ["20_model/quick_model.md"],
        ["Defensive", "Moderate", "Optimistic", "break-even", "per transaction",
         "cash"],
    ),
    "byb-strategist": (
        ["20_draft/strategist_notes.md", "20_draft/strategy_report.md"],
        ["Positioning", "each side", "Launch focus", "Revenue streams",
         "Expansion sequence", "Capital ask"],
    ),
    "byb-draft-modeller": (
        ["20_draft/model_v1.csv"],
        ["Volume curve", "per transaction", "Fixed costs", "break-even", "Cash need"],
    ),
    "byb-sceptical-investor": (
        ["30_assessment/sceptic.md", "30_assessment/scorecard_inputs.json",
         "30_assessment/scorecard_result.json"],
        ["ten committee questions", "Recompute every number", "Missing costs",
         "pre-mortem", "risk register", "scorecard"],
    ),
    "byb-investment-banker": (
        ["30_assessment/banker.md"],
        ["valuation", "dilution", "option pool", "use of funds", "comparable",
         "exit", "due diligence"],
    ),
}
CRITICS = ["byb-sceptical-investor", "byb-investment-banker"]
FULL_RESEARCH = ["market_region", "competition", "customer_demand",
                 "regulation_structure", "founder_fit", "funding_climate"]
QUICK_RESEARCH = ["market_competition", "customer_demand", "founder_fit"]
FIREWALL = "Never read `20_draft/strategist_notes.md`"
MODEL_V1_HEADER = "scenario,period,line,value,unit,label,assumption_or_source"


def agent_path(stem):
    return f"agents/{stem}.md"


def agent(stem):
    return read(agent_path(stem))


class TemplateTests(unittest.TestCase):
    def test_assessment_template(self):
        text = read(TEMPLATES + "assessment.md")
        for heading in ("The ten questions", "Missing costs", "Pre-mortem",
                        "Risk register", "Scorecard"):
            self.assertRegex(text, rf"(?m)^## {heading}\s*$", heading)
        self.assertIn(DISCLAIMER, text)

    def test_assessment_template_order(self):
        # The ten questions are answered before anything else (spec §7).
        text = read(TEMPLATES + "assessment.md")
        headings = re.findall(r"(?m)^## (.+?)\s*$", text)
        self.assertEqual(headings[0], "The ten questions")
        for number in range(1, 11):
            self.assertIn(f"### {number}.", section(text, "The ten questions"))
        self.assertIn("Search status", text[:text.index("## The ten questions")])

    def test_assessment_scorecard_section(self):
        scorecard = section(read(TEMPLATES + "assessment.md"), "Scorecard")
        for key in AREAS:
            self.assertIn(key, scorecard)
        self.assertIn("scorecard_result.json", scorecard)

    def test_strategy_report_template(self):
        text = read(TEMPLATES + "strategy_report.md")
        for heading in ("Positioning", "What each side gets", "Launch focus",
                        "Revenue streams", "Expansion sequence", "The numbers",
                        "Capital ask", "Known gaps and risks", "Sources"):
            self.assertRegex(text, rf"(?m)^## {heading}\s*$", heading)
        self.assertIn(DISCLAIMER, text)
        self.assertIn("model_v1.csv", text)


class ScorecardReferenceTests(unittest.TestCase):
    def test_fulltime_flag_source(self):
        text = read("skills/before-you-build/references/scorecard.md")
        line = next(l for l in text.splitlines() if "`fulltime_within_6_months`" in l)
        self.assertIn("10_research/founder_fit.md", line)


class DraftAndCriticAgentTests(unittest.TestCase):
    def check(self, stem):
        outs, mentions = DRAFT_AND_CRITIC_AGENTS[stem]
        self.assertEqual(lint_agent(agent_path(stem), outs, mentions), [])
        cover = section(agent(stem), "Must cover")
        for phrase in mentions:
            self.assertIn(phrase, cover, f"{stem}: {phrase} not in ## Must cover")

    def test_quick_modeller(self):
        self.check("byb-quick-modeller")

    def test_strategist(self):
        self.check("byb-strategist")

    def test_draft_modeller(self):
        self.check("byb-draft-modeller")

    def test_sceptical_investor(self):
        self.check("byb-sceptical-investor")

    def test_investment_banker(self):
        self.check("byb-investment-banker")

    def test_run_dir_paths(self):
        for stem, (outs, _) in DRAFT_AND_CRITIC_AGENTS.items():
            text = agent(stem)
            inputs = section(text, "Inputs")
            self.assertIn("<RUN_DIR>/00_brief.md", inputs, stem)
            self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/references/conventions.md",
                          inputs, stem)
            output = section(text, "Output")
            for out in outs:
                self.assertIn(f"<RUN_DIR>/{out}", output, f"{stem}: {out}")

    def test_descriptions_are_yaml_safe(self):
        for stem in DRAFT_AND_CRITIC_AGENTS:
            description = frontmatter(agent(stem))["description"]
            self.assertNotIn(": ", description, stem)
            self.assertNotIn(" #", description, stem)

    def test_no_hype_or_exclamation(self):
        for stem in DRAFT_AND_CRITIC_AGENTS:
            text = agent(stem)
            self.assertNotIn("!", text, stem)
            self.assertNotIn("go build", text.lower(), stem)
            for word in ("revolutionary", "game-changing", "guaranteed"):
                self.assertNotIn(word, text.lower(), f"{stem}: {word}")

    def test_sources_stay_in_own_file(self):
        # Ruling R7: agents never write to the shared sources.md.
        for stem in DRAFT_AND_CRITIC_AGENTS:
            text = agent(stem)
            self.assertIn("Do not write to `<RUN_DIR>/sources.md`", text, stem)
            for line in text.splitlines():
                if "sources.md" in line:
                    self.assertIn("Do not write to", line, f"{stem}: {line}")

    def test_never_invent_and_label_rules(self):
        for stem in DRAFT_AND_CRITIC_AGENTS:
            rules = section(agent(stem), "Rules")
            self.assertIn("Label every figure", rules, stem)
            self.assertIn("Never invent", rules, stem)
            self.assertIn("show the range", rules, stem)


class InputTests(unittest.TestCase):
    def test_quick_modeller_inputs(self):
        inputs = section(agent("byb-quick-modeller"), "Inputs")
        for name in QUICK_RESEARCH:
            self.assertIn(f"<RUN_DIR>/10_research/{name}.md", inputs, name)
        self.assertIn("Quick Check", frontmatter(agent("byb-quick-modeller"))["description"])

    def test_drafters_read_six_briefs(self):
        for stem in ("byb-strategist", "byb-draft-modeller", "byb-investment-banker"):
            inputs = section(agent(stem), "Inputs")
            for name in FULL_RESEARCH:
                self.assertIn(f"<RUN_DIR>/10_research/{name}.md", inputs, f"{stem}: {name}")

    def test_sceptic_inputs_both_modes(self):
        inputs = section(agent("byb-sceptical-investor"), "Inputs")
        for name in FULL_RESEARCH + QUICK_RESEARCH:
            self.assertIn(f"<RUN_DIR>/10_research/{name}.md", inputs, name)
        self.assertIn("<RUN_DIR>/20_model/quick_model.md", inputs)
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/references/questions.md", inputs)
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/references/scorecard.md", inputs)

    def test_critics_read_draft_for_both_paths(self):
        for stem in CRITICS:
            inputs = section(agent(stem), "Inputs")
            for path in ("<RUN_DIR>/20_draft/strategy_report.md",
                         "<RUN_DIR>/20_draft/model_v1.csv",
                         "<RUN_DIR>/20_draft/uploaded_report.md"):
                self.assertIn(path, inputs, f"{stem}: {path}")
            self.assertIn("Path B", inputs, stem)
            # Ruling R16: one exact readable path, never a glob.
            self.assertNotIn("uploaded_report.*", agent(stem), stem)

    def test_critic_tools(self):
        sceptic_tools = frontmatter(agent("byb-sceptical-investor"))["tools"]
        for tool in ("WebSearch", "WebFetch", "Read", "Write", "Bash"):
            self.assertIn(tool, sceptic_tools, tool)
        banker_tools = frontmatter(agent("byb-investment-banker"))["tools"]
        for tool in ("WebSearch", "WebFetch", "Read", "Write"):
            self.assertIn(tool, banker_tools, tool)
        # The banker does not fill the scorecard, so it has no reason to run Bash.
        self.assertNotIn("Bash", banker_tools)

    def test_modellers_have_calculator_only(self):
        # R22: Bash for python3 arithmetic only, no network, no other commands.
        for stem in ("byb-quick-modeller", "byb-draft-modeller",
                     "byb-financial-modeller"):
            text = agent(stem)
            tools = frontmatter(text)["tools"]
            self.assertIn("Bash", tools, stem)
            for tool in ("WebSearch", "WebFetch"):
                self.assertNotIn(tool, tools, f"{stem}: {tool}")
            rules = section(text, "Rules")
            self.assertIn("except the /tmp scratch scripts the calculator rule allows", rules, stem)
            for phrase in ("Use Bash only to run python3 for arithmetic",
                           "no network calls and no other commands",
                           "Recompute every total with it rather than by hand",
                           "Scratch scripts in /tmp are not outputs; delete them when done."):
                self.assertIn(phrase, rules, f"{stem}: {phrase}")

    def test_sceptic_may_also_run_the_calculator(self):
        # Rule 12: the Sceptic recomputes every number, so it gets the same calculator.
        rules = section(agent("byb-sceptical-investor"), "Rules")
        rule = next(l for l in rules.splitlines() if l.startswith("12. "))
        for phrase in ("to run the scoring engine",
                       "to run python3 for arithmetic, as the modellers' calculator rule allows",
                       "no network calls and no other commands",
                       "Scratch scripts in /tmp are not outputs; delete them when done."):
            self.assertIn(phrase, rule, phrase)
        self.assertIn("except the /tmp scratch scripts the calculator rule allows", rules)

    def test_sceptic_question_10_tests_the_pivot(self):
        # R23
        cover = section(agent("byb-sceptical-investor"), "Must cover")
        for phrase in ("at or below zero in the Moderate scenario",
                       "changed offer", "and it must say which",
                       "pass and fail lines with formulas", "minimum sample",
                       "<set-up> plus <live> weeks",
                       "no changed offer can make", "rather than inventing one",
                       "a changed offer reaches positive contribution",
                       "confirmed non-viable: stop"):
            self.assertIn(phrase, cover, phrase)

    def test_sceptic_question_10_fits_deadline(self):
        # R28
        cover = section(agent("byb-sceptical-investor"), "Must cover")
        for phrase in ("including the decision, must end on or before the decision deadline",
                       "shortest version that fits", "smaller minimum sample",
                       "the date the deadline would need to move to",
                       "brief's date plus 7 days"):
            self.assertIn(phrase, cover, phrase)

    def test_sceptic_length_and_duration_rules(self):
        text = agent("byb-sceptical-investor")
        rules = section(text, "Rules")
        self.assertIn("Keep `sceptic.md` within 5,000 words in total, as `wc -w` counts them", rules)
        self.assertIn("to count words with `wc -w`", rules)
        cover = section(text, "Must cover")
        self.assertIn('"<set-up> plus <live> weeks (<days> days)"', cover)
        self.assertIn("at most 90", cover)

    def test_report_writer_follows_question_10_version(self):
        quick = section(agent("byb-report-writer"), "Quick Check")
        for phrase in ("Version tested", "follows the Sceptical Investor's version in question 10",
                       "Only when question 10 has no pass and fail lines",
                       "consistent with the version question 10 tests",
                       "name both", "checks the question 10 version first",
                       "separate condition", "never as one pivot"):
            self.assertIn(phrase, quick, phrase)


class StrategistTests(unittest.TestCase):
    def test_strategist_ambitious_but_labelled(self):
        text = agent("byb-strategist")
        rules = section(text, "Rules")
        self.assertIn("strongest honest case", rules)
        self.assertIn("never grade", rules.lower())
        self.assertIn("20_draft/strategist_notes.md", section(text, "Output"))

    def test_strategist_two_passes(self):
        text = agent("byb-strategist")
        self.assertIn("Pass 1", text)
        self.assertIn("Pass 2", text)
        self.assertIn("## Assumptions for the model", section(text, "Output"))
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/templates/strategy_report.md",
                      section(text, "Output"))
        self.assertIn("<RUN_DIR>/20_draft/model_v1.csv", section(text, "Inputs"))

    def test_strategist_caveats_go_to_known_gaps(self):
        rules = section(agent("byb-strategist"), "Rules")
        self.assertIn("## Known gaps and risks", rules)

    def test_strategist_pass_2_keeps_model_assumptions(self):
        # Ruling R25.
        text = agent("byb-strategist")
        output = section(text, "Output")
        self.assertIn("never changes any assumption the Draft Modeller used", output)
        self.assertIn("Proposed for the rebuild", output)
        self.assertIn("## Known gaps and risks", output)
        self.assertIn("never asks for a model re-run", output)
        self.assertNotIn("tell the lead which assumption", text)

    def test_draft_modeller_reads_notes_and_writes_csv(self):
        text = agent("byb-draft-modeller")
        self.assertIn("<RUN_DIR>/20_draft/strategist_notes.md", section(text, "Inputs"))
        self.assertIn("Assumptions for the model", section(text, "Inputs"))
        self.assertIn(MODEL_V1_HEADER, section(text, "Output"))
        for name in ("Defensive", "Moderate", "Optimistic"):
            self.assertIn(name, text)
        output = section(text, "Output")
        for line in ("`transaction_value`", "`take_rate`", "`break_even_month`", "`cash_need`"):
            self.assertIn(line, output, line)
        cover = section(text, "Must cover")
        self.assertIn("60-month horizon", cover)
        self.assertIn("lowest point of cumulative operating results starting from zero", cover)
        self.assertIn("keeps falling", cover)

    def test_quick_modeller_revenue_base(self):
        cover = section(agent("byb-quick-modeller"), "Must cover")
        self.assertIn("revenue per transaction", cover)
        self.assertIn("seller of record", cover)
        self.assertIn("base it is charged on", cover)


class FirewallTests(unittest.TestCase):
    def test_firewall(self):
        for stem in CRITICS:
            rules = section(agent(stem), "Rules")
            self.assertIn(FIREWALL, rules, stem)
            self.assertIn("recompute", rules, stem)

    def test_critics_only_mention_notes_to_forbid_them(self):
        for stem in CRITICS:
            for line in agent(stem).splitlines():
                if "strategist_notes" in line:
                    self.assertIn("Never read", line, f"{stem}: {line}")

    def test_quick_modeller_never_reads_drafter_notes(self):
        self.assertNotIn("strategist_notes", agent("byb-quick-modeller"))


class ScepticTests(unittest.TestCase):
    def test_sceptic_uses_engine(self):
        text = agent("byb-sceptical-investor")
        for phrase in ("references/questions.md", "scorecard_inputs.json",
                       "scripts/scorecard.py", "pre-mortem", "risk register"):
            self.assertIn(phrase, text, phrase)
        recheck = section(text, "Re-check mode")
        self.assertIsNotNone(recheck)
        self.assertIn("Stage 4b", recheck)
        self.assertIn("<RUN_DIR>/30_assessment/sceptic_recheck.md", recheck)

    def test_sceptic_engine_command_and_errors(self):
        text = agent("byb-sceptical-investor")
        self.assertIn('python3 "<PLUGIN_ROOT>/scripts/scorecard.py" '
                      '"<RUN_DIR>/30_assessment/scorecard_inputs.json"', text)
        self.assertIn("unedited", text)
        self.assertIn("exit code 2", text)
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/templates/assessment.md",
                      section(text, "Output"))

    def test_sceptic_scorecard_flags(self):
        cover = section(agent("byb-sceptical-investor"), "Must cover")
        for phrase in ("fulltime_within_6_months", "founder_fit.md",
                       "test_measures_unit_economics", "question 10",
                       "money per transaction", "label_counts", "areas 1 to 4"):
            self.assertIn(phrase, cover, phrase)

    def test_sceptic_revenue_checks(self):
        cover = section(agent("byb-sceptical-investor"), "Must cover")
        for phrase in ("take rate", "competitors' range", "willingness to pay",
                       "GMV", "right base", "second side", "working capital", "inventory"):
            self.assertIn(phrase, cover, phrase)

    def test_sceptic_never_writes_verdict(self):
        rules = section(agent("byb-sceptical-investor"), "Rules")
        self.assertIn("Do not write a verdict yourself", rules)

    def test_recheck_rules(self):
        recheck = section(agent("byb-sceptical-investor"), "Re-check mode")
        for phrase in ("<RUN_DIR>/40_plan/", "<RUN_DIR>/40_plan/model_v2.csv",
                       "<RUN_DIR>/30_assessment/sceptic.md",
                       "scorecard_inputs_v1.json", "fixed", "answered", "still open",
                       "once", "Do not loop", "## Gaps and assumptions"):
            self.assertIn(phrase, recheck, phrase)

    def test_recheck_double_failure_restores_stage_3(self):
        recheck = section(agent("byb-sceptical-investor"), "Re-check mode")
        self.assertIn("restore", recheck)
        self.assertIn("could not be computed", recheck)


class BankerTests(unittest.TestCase):
    def test_banker_scope(self):
        text = agent("byb-investment-banker")
        for phrase in ("valuation", "dilution", "option pool", "use of funds",
                       "comparable", "exit", "due diligence"):
            self.assertIn(phrase, text, phrase)

    def test_banker_range_not_point(self):
        rules = section(agent("byb-investment-banker"), "Rules")
        self.assertIn("never a single", rules)
        self.assertIn("Do not rate the scorecard", rules)

    def test_banker_early_stage_valuation(self):
        cover = section(agent("byb-investment-banker"), "Must cover")
        for phrase in ("round sizes", "typical dilution", "No DCF", "projected revenue"):
            self.assertIn(phrase, cover, phrase)

    def test_banker_burn_without_model(self):
        cover = section(agent("byb-investment-banker"), "Must cover")
        self.assertIn("monthly burn", cover)
        self.assertIn("runway", cover)
        self.assertIn("Path B", cover)

    def test_banker_full_only(self):
        self.assertIn("Full Review", frontmatter(agent("byb-investment-banker"))["description"])


if __name__ == "__main__":
    unittest.main()
