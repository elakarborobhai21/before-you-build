import csv
import io
import re
import unittest

from tests.agentlint import lint_agent, section
from tests.helpers import DISCLAIMER, REPO, frontmatter, read

TEMPLATES = "skills/before-you-build/templates/"
GATE_HEADER = "measure,formula,pass_line,fail_line,measured_value,date_measured,status"
MODEL_HEADER = "scenario,period,line,value,unit,label,assumption_or_source"
FIREWALL = "Never read `20_draft/strategist_notes.md`"
SCENARIOS = ["Defensive", "Moderate", "Optimistic"]
QUICK_CASH_NEED_DEF = ("the lowest point of cumulative monthly results starting from zero "
                       "(not from founder cash) before any money raised, reported as a positive "
                       "amount; when break-even is never within 24 months, give the low point "
                       "within 24 months and say it keeps falling")
CASH_NEED_DEF = ("the lowest point of cumulative operating results starting from zero "
                 "(not from founder cash) before any money raised: the deepest the business "
                 "goes below zero, reported as a positive amount needed")
LEGEND = "Labels: [S] sourced, [E] estimated, [A] assumed."
FULL_RESEARCH = ["market_region", "competition", "customer_demand",
                 "regulation_structure", "founder_fit", "funding_climate"]

# agent stem -> (output paths from spec §5, must-mentions from spec §5 and the brief)
DECISION_AGENTS = {
    "byb-business-model-designer": (
        ["40_plan/business_model.md"],
        ["Revenue and cost streams", "How money moves", "What to drop"],
    ),
    "byb-operations-product-planner": (
        ["40_plan/operations_product.md"],
        ["Product flows", "MVP", "Trust and safety", "Customer service",
         "Org chart", "first hires"],
    ),
    "byb-financial-modeller": (
        ["40_plan/financials.md", "40_plan/model_v2.csv"],
        ["balance sheet", "working capital", "sensitivity", "never"] + SCENARIOS,
    ),
    "byb-validation-test-designer": (
        ["50_decision/test_plan.md", "50_decision/gate_tracker.csv"],
        ["pass", "fail", "formula", "go/no-go", "fallback"],
    ),
    "byb-report-writer": (
        ["50_decision/decision_pack.md", "50_decision/decision_memo.md",
         "50_decision/full_plan.md"],
        ["verdict", "readiness score", "confidence", "top 3 risks", "the test"],
    ),
}
# R22: modellers may run python3 for arithmetic only.
CALCULATOR_AGENTS = ["byb-financial-modeller"]
STAGE4 = ["byb-business-model-designer", "byb-operations-product-planner",
          "byb-financial-modeller"]
STAGE4_OUTPUTS = ["business_model.md", "operations_product.md", "financials.md",
                  "model_v2.csv"]


def agent_path(stem):
    return f"agents/{stem}.md"


def agent(stem):
    return read(agent_path(stem))


class LintTests(unittest.TestCase):
    def test_lint_each_agent(self):
        for stem, (outs, mentions) in DECISION_AGENTS.items():
            with self.subTest(stem=stem):
                self.assertEqual(lint_agent(agent_path(stem), outs, mentions), [])

    def test_run_dir_paths(self):
        for stem, (outs, _) in DECISION_AGENTS.items():
            text = agent(stem)
            inputs = section(text, "Inputs")
            self.assertIn("<RUN_DIR>/00_brief.md", inputs, stem)
            self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/references/conventions.md",
                          inputs, stem)
            output = section(text, "Output")
            for out in outs:
                self.assertIn(f"<RUN_DIR>/{out}", output, f"{stem}: {out}")

    def test_descriptions_are_yaml_safe(self):
        for stem in DECISION_AGENTS:
            description = frontmatter(agent(stem))["description"]
            self.assertNotIn(": ", description, stem)
            self.assertNotIn(" #", description, stem)

    def test_no_web_tools(self):
        # R15: modellers work from the research; the rebuild and decision agents
        # keep evidence in Stage 1 and Stage 3.
        for stem in DECISION_AGENTS:
            tools = frontmatter(agent(stem))["tools"]
            self.assertIn("Read", tools, stem)
            self.assertIn("Write", tools, stem)
            blocked = ("WebSearch", "WebFetch") if stem in CALCULATOR_AGENTS \
                else ("WebSearch", "WebFetch", "Bash")
            for tool in blocked:
                self.assertNotIn(tool, tools, f"{stem}: {tool}")

    def test_no_hype_or_exclamation(self):
        for stem in DECISION_AGENTS:
            text = agent(stem)
            self.assertNotIn("!", text, stem)
            for word in ("revolutionary", "game-changing", "guaranteed"):
                self.assertNotIn(word, text.lower(), f"{stem}: {word}")

    def test_sources_stay_in_own_file(self):
        # Ruling R7: agents never write to the shared sources.md.
        for stem in DECISION_AGENTS:
            text = agent(stem)
            self.assertIn("Do not write to `<RUN_DIR>/sources.md`", text, stem)
            for line in text.splitlines():
                if "sources.md" in line:
                    self.assertIn("Do not write to", line, f"{stem}: {line}")

    def test_label_and_honesty_rules(self):
        for stem in DECISION_AGENTS:
            rules = section(agent(stem), "Rules")
            self.assertIn("Label every figure", rules, stem)
            self.assertIn("Never invent", rules, stem)
            self.assertIn("show the range", rules, stem)

    def test_disclaimer_on_markdown_outputs(self):
        for stem in DECISION_AGENTS:
            self.assertIn("disclaimer from conventions.md, word for word",
                          section(agent(stem), "Output"), stem)


class RebuildTests(unittest.TestCase):
    def test_stage4_inputs(self):
        for stem in STAGE4:
            inputs = section(agent(stem), "Inputs")
            for name in FULL_RESEARCH:
                self.assertIn(f"<RUN_DIR>/10_research/{name}.md", inputs, f"{stem}: {name}")
            for path in ("<RUN_DIR>/20_draft/strategy_report.md",
                         "<RUN_DIR>/20_draft/model_v1.csv",
                         "<RUN_DIR>/20_draft/uploaded_report.md",
                         "<RUN_DIR>/30_assessment/sceptic.md",
                         "<RUN_DIR>/30_assessment/banker.md"):
                self.assertIn(path, inputs, f"{stem}: {path}")
            self.assertIn("Path B", inputs, stem)

    def test_stage4_firewall(self):
        for stem in STAGE4:
            text = agent(stem)
            self.assertIn(FIREWALL, section(text, "Rules"), stem)
            for line in text.splitlines():
                if "strategist_notes" in line:
                    self.assertIn("Never read", line, f"{stem}: {line}")

    def test_stage4_reads_business_model_not_siblings(self):
        # Ruling R24: the designer runs first; the other two read its file, not each other's.
        designer = agent("byb-business-model-designer")
        self.assertIn("runs first", section(designer, "Inputs"))
        self.assertIn("in one table", designer)
        for word in ("price", "fee", "who pays", "volume"):
            self.assertIn(word, section(designer, "Output"), word)
        for stem in ("byb-operations-product-planner", "byb-financial-modeller"):
            inputs = section(agent(stem), "Inputs")
            self.assertIn("in parallel", inputs, stem)
            self.assertIn("<RUN_DIR>/40_plan/business_model.md", inputs, stem)
            self.assertIn("the offer", inputs, stem)
        for stem in STAGE4:
            inputs = section(agent(stem), "Inputs")
            own = DECISION_AGENTS[stem][0]
            for name in STAGE4_OUTPUTS:
                if f"40_plan/{name}" in own or name == "business_model.md":
                    continue
                for line in inputs.splitlines():
                    if name in line:
                        self.assertIn("Do not read", line, f"{stem}: {line}")

    def test_designer_takes_up_proposed_changes(self):
        cover = section(agent("byb-business-model-designer"), "Must cover")
        self.assertIn("`Proposed for the rebuild`", cover)
        self.assertIn("adopted or rejected", cover)
        self.assertIn("reason", cover)

    def test_designer_findings_table_carries_proposals(self):
        output = section(agent("byb-business-model-designer"), "Output")
        self.assertIn("`strategy_report.md`", output)
        self.assertIn("adopted or rejected", output)
        self.assertIn("for <owner agent>", output)
        template = read(TEMPLATES + "strategy_report.md")
        gaps = template.split("## Known gaps and risks", 1)[1].split("\n## ", 1)[0]
        self.assertRegex(gaps, r"(?m)^### Proposed for the rebuild\s*$")

    def test_financial_modeller_follows_business_model_with_flags(self):
        rules = section(agent("byb-financial-modeller"), "Rules")
        self.assertIn("Follow `business_model.md`", rules)
        self.assertIn("contradicts `sceptic.md`", rules)
        self.assertIn("keep it and flag it", rules)
        self.assertIn("outside research range: <range> in <brief>", rules)

    def test_redispatch_designer_reruns_the_other_two(self):
        from tests.test_skill import stages
        s4 = stages(read("skills/before-you-build/SKILL.md"), "Full Review stages")["4"]
        self.assertIn("If `business_model.md` has to be re-dispatched after the other two have "
                      "run, re-dispatch `byb-operations-product-planner` and "
                      "`byb-financial-modeller` after it", s4)

    def test_spec_stage4_order(self):
        spec = read("docs/specs/2026-10-12-before-you-build-design.md")
        self.assertNotIn("parallel ×3", spec)
        self.assertIn("| 4a | Business Model Designer | alone, first |", spec)
        self.assertIn("| 4 | Operations & Product Planner | parallel ×2, after 4a |", spec)

    def test_financial_model_follows_business_model(self):
        inputs = section(agent("byb-financial-modeller"), "Inputs")
        self.assertIn("prices, fee split and volumes come from `business_model.md`", inputs)
        self.assertIn("where it is silent, use the draft and say so", inputs)

    def test_stage4_answers_every_finding(self):
        for stem in STAGE4:
            cover = section(agent(stem), "Must cover")
            for phrase in ("every finding", "fixed", "answered", "open",
                           "sceptic.md", "banker.md"):
                self.assertIn(phrase, cover, f"{stem}: {phrase}")

    def test_stage4_same_lanes(self):
        # The three planners split the critique the same way, so nothing falls between them.
        lanes = [section(agent(stem), "Lanes") for stem in STAGE4]
        for stem, lane in zip(STAGE4, lanes):
            self.assertIsNotNone(lane, f"{stem}: missing ## Lanes")
        self.assertEqual(lanes[0], lanes[1])
        self.assertEqual(lanes[0], lanes[2])

    def test_financial_modeller_model(self):
        text = agent("byb-financial-modeller")
        output = section(text, "Output")
        self.assertIn(MODEL_HEADER, output)
        self.assertIn("model_v1.csv", output)
        cover = section(text, "Must cover")
        for phrase in ("P&L", "cash flow", "per-transaction waterfall",
                       "60-month horizon",
                       "Draft Modeller", "four assumptions", "down and up",
                       "cash-on-delivery", "payout"):
            self.assertIn(phrase.lower(), cover.lower(), phrase)


    def test_cash_need_definition_matches_draft_modeller(self):
        for stem in ("byb-draft-modeller", "byb-financial-modeller"):
            self.assertIn(CASH_NEED_DEF, section(agent(stem), "Must cover"), stem)

    def test_quick_modeller_uses_full_cash_need_wording(self):
        cover = section(agent("byb-quick-modeller"), "Must cover")
        self.assertIn(QUICK_CASH_NEED_DEF, cover)
        self.assertNotIn("(the lowest point of cumulative cash)", cover)

    def test_banker_recomputes_cash_need_by_the_same_definition(self):
        cover = section(agent("byb-investment-banker"), "Must cover")
        item = next(l for l in cover.splitlines() if "Capital ask and cash need" in l)
        self.assertIn("Recompute the draft's cash need", item)
        self.assertIn(CASH_NEED_DEF, item)
        self.assertIn("keeps falling", item)

    def test_financial_modeller_keeps_v1_lines(self):
        text = agent("byb-financial-modeller")
        output = section(text, "Output")
        self.assertIn("`cumulative_cash_with_working_capital`", output)
        self.assertIn("`cash_need_with_working_capital`", output)
        self.assertIn("meaning it has in `model_v1.csv`", output)
        self.assertNotIn("`cumulative_cash` counts", output)
        self.assertIn("deposits", section(text, "Must cover").split("**Balance sheet.**")[1]
                      .split("6. **")[0])
        self.assertIn("definition changed", section(text, "Must cover"))


class ModelFileTests(unittest.TestCase):
    BREAK_EVEN_YEARS = ("Y3–Y5 are yearly periods. If the first positive month falls in that "
                        "range, report break-even as the year (for example `Y4`) and say in "
                        "the notes that the month is inside that year.")

    def test_core_lines_and_detail_file(self):
        # Ruling R26: the model CSV holds core lines; helper rows go to a detail file.
        for stem, detail in (("byb-draft-modeller", "model_v1_detail.csv"),
                             ("byb-financial-modeller", "model_v2_detail.csv")):
            output = section(agent(stem), "Output")
            self.assertIn("core lines only", output, stem)
            self.assertIn("under 1,500 rows", output, stem)
            self.assertIn(detail, output, stem)
            self.assertIn("no other agent needs to read", output, stem)
            self.assertIn("every line listed under `line` stays in the core file", output, stem)

    def test_break_even_in_later_years(self):
        for stem in ("byb-draft-modeller", "byb-financial-modeller"):
            self.assertIn(self.BREAK_EVEN_YEARS, section(agent(stem), "Must cover"), stem)


class ValidationTestDesignerTests(unittest.TestCase):
    def test_inputs(self):
        inputs = section(agent("byb-validation-test-designer"), "Inputs")
        for path in ("<RUN_DIR>/10_research/", "<RUN_DIR>/30_assessment/sceptic.md",
                     "<RUN_DIR>/30_assessment/scorecard_inputs.json",
                     "<RUN_DIR>/30_assessment/scorecard_result.json",
                     "<RUN_DIR>/30_assessment/sceptic_recheck.md",
                     "<RUN_DIR>/40_plan/"):
            self.assertIn(path, inputs, path)
        self.assertIn("Full Review",
                      frontmatter(agent("byb-validation-test-designer"))["description"])

    def test_targets_riskiest_assumption(self):
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        for phrase in ("question 9", "Budget", "Duration", "What is built",
                       "what is not", "pass line", "fail line", "go/no-go date",
                       "Fallback pivots"):
            self.assertIn(phrase, cover, phrase)

    def test_starts_from_latest_cheapest_test(self):
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        self.assertIn("updated cheapest test in `sceptic_recheck.md`", cover)
        self.assertIn("question 10 in `sceptic.md`", cover)

    def test_pivot_version_stated(self):
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        self.assertIn("Version tested", cover)
        self.assertIn("`Pivot`", cover)

    def test_test_fits_deadline(self):
        # R28
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        for phrase in ("including the decision, must end on or before the decision deadline",
                       "shortest version that fits", "smaller minimum sample",
                       "the date the deadline would need to move to",
                       "brief's date plus 7 days"):
            self.assertIn(phrase, cover, phrase)
        self.assertNotIn("and before the decision deadline", cover)

    def test_go_next_step_is_not_build(self):
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        self.assertIn("never to build, launch or raise money", cover)

    def test_sample_in_formula(self):
        output = section(agent("byb-validation-test-designer"), "Output")
        self.assertIn("minimum sample", output)
        self.assertIn("(minimum ", output)

    def test_one_duration_limit(self):
        for rel in (agent_path("byb-validation-test-designer"), agent_path("byb-report-writer"),
                    TEMPLATES + "test_plan.md", TEMPLATES + "decision_pack.md",
                    TEMPLATES + "decision_memo.md"):
            text = read(rel)
            self.assertNotIn("13 weeks", text, rel)
            self.assertNotRegex(text, r"no more than 1[0-9] weeks", rel)
        self.assertIn("90 days", section(agent("byb-validation-test-designer"), "Must cover"))

    def test_unit_economics_flag(self):
        # Ruling R11.
        cover = section(agent("byb-validation-test-designer"), "Must cover")
        self.assertIn("test_measures_unit_economics", cover)
        self.assertIn("money per transaction", cover)

    def test_gate_tracker_output(self):
        text = agent("byb-validation-test-designer")
        output = section(text, "Output")
        self.assertIn(GATE_HEADER, output)
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/templates/test_plan.md", output)
        self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/templates/gate_tracker.csv",
                      output)
        self.assertIn("example row", output)


class ReportWriterTests(unittest.TestCase):
    def test_report_writer_two_modes(self):
        text = agent("byb-report-writer")
        quick = section(text, "Quick Check")
        full = section(text, "Full Review")
        self.assertIsNotNone(quick)
        self.assertIsNotNone(full)
        self.assertIn("50_decision/decision_pack.md", quick)
        self.assertIn("decision_memo.md", full)
        self.assertIn("full_plan.md", full)
        self.assertIn("30_assessment/scorecard_result.json", text)
        self.assertIn("unchanged", text)

    def test_verdict_is_copied_not_judged(self):
        rules = section(agent("byb-report-writer"), "Rules")
        self.assertIn("30_assessment/scorecard_result.json", rules)
        self.assertIn("Never change, round, reword or argue with", rules)
        self.assertIn("latest", rules)

    def test_quick_check_test_from_question_10(self):
        quick = section(agent("byb-report-writer"), "Quick Check")
        self.assertIn("question 10", quick)
        self.assertIn("<RUN_DIR>/20_model/quick_model.md", quick)

    def test_full_plan_is_assembled(self):
        full = section(agent("byb-report-writer"), "Full Review")
        self.assertIn("assemble", full)
        for path in ("<RUN_DIR>/40_plan/", "<RUN_DIR>/50_decision/test_plan.md",
                     "<RUN_DIR>/30_assessment/sceptic_recheck.md",
                     "<RUN_DIR>/30_assessment/banker.md"):
            self.assertIn(path, full, path)
        self.assertIn("no new analysis", section(agent("byb-report-writer"), "Rules"))

    def test_memo_length_in_full_review(self):
        full = section(agent("byb-report-writer"), "Full Review")
        self.assertIn("about 1,500 words outside tables", full)
        self.assertIn("detail goes to `full_plan.md`", full)

    def test_pivot_from_reasons_first(self):
        cover = section(agent("byb-report-writer"), "Must cover")
        for phrase in ("`reasons`", "lowest-rated area", "full-time", "fallback pivots",
                       "which finding", "Version tested"):
            self.assertIn(phrase, cover, phrase)

    def test_pivot_is_a_change_to_the_business(self):
        # R27
        cover = section(agent("byb-report-writer"), "Must cover")
        for phrase in ("A pivot is a change to the business (customer, channel, offer, price, "
                       "retention) or, when a committee rule capped the verdict, removing that "
                       "cause (a founder's full-time commitment, or a test that measures money "
                       "per transaction)",
                       "A smaller test is never the pivot",
                       "the test is how the pivot is checked",
                       "comes from the score alone", "Moderate money per transaction is positive",
                       "retention mechanism", "payback is under 1x"):
            self.assertIn(phrase, cover, phrase)

    def test_report_writer_decide_by_fits_deadline(self):
        # R28
        quick = section(agent("byb-report-writer"), "Quick Check")
        for phrase in ("on or before the decision deadline",
                       "states the conflict exactly as the Sceptical Investor gave it"):
            self.assertIn(phrase, quick, phrase)
        # The Test Designer is not dispatched in a Quick Check.
        self.assertNotIn("Test Designer gave it", quick)
        full = section(agent("byb-report-writer"), "Full Review")
        for phrase in ("go/no-go date from `test_plan.md`",
                       "on or before the decision deadline",
                       "states the conflict exactly as the Test Designer gave it"):
            self.assertIn(phrase, full, phrase)

    def test_score_only_pivot_differs_from_question_10(self):
        cover = section(agent("byb-report-writer"), "Must cover")
        for phrase in ("score-only pivot", "name both", "what the test checks",
                       "the change to make after a pass", "never as one pivot",
                       "differs from the version the test checks (question 10 in a Quick "
                       "Check, `test_plan.md` in a Full Review)"):
            self.assertIn(phrase, cover, phrase)
        self.assertNotIn("differs from the version question 10 tests, name both", cover)

    def test_placeholders_removed(self):
        output = section(agent("byb-report-writer"), "Output")
        self.assertIn("placeholder", output)
        self.assertIn("`<PLUGIN_ROOT>`", output)

    def test_templates_named(self):
        text = agent("byb-report-writer")
        for name in ("decision_pack.md", "decision_memo.md", "full_plan.md"):
            self.assertIn(f"<PLUGIN_ROOT>/skills/before-you-build/templates/{name}", text)


class TemplateTests(unittest.TestCase):
    MARKDOWN = ("decision_pack.md", "decision_memo.md", "full_plan.md", "test_plan.md")

    def test_output_templates(self):
        for name in self.MARKDOWN:
            text = read(TEMPLATES + name)
            self.assertIn(DISCLAIMER, text, name)
            self.assertTrue(text.rstrip().endswith(DISCLAIMER), f"{name}: disclaimer not last")
        pack = read(TEMPLATES + "decision_pack.md")
        for heading in ("Verdict", "Readiness score", "Top 3 risks", "The test"):
            self.assertRegex(pack, rf"(?m)^## {heading}\s*$", heading)
        memo = read(TEMPLATES + "decision_memo.md")
        for heading in ("Riskiest assumption", "Pre-mortem"):
            self.assertRegex(memo, rf"(?m)^## {heading}\s*$", heading)

    def test_founder_templates_clean(self):
        # No authoring paths reach a founder; each template carries the label legend.
        for name in self.MARKDOWN:
            text = read(TEMPLATES + name)
            self.assertNotIn("PLUGIN_ROOT", text, name)
            self.assertNotIn("Follow ", text, name)
            self.assertIn(LEGEND, "\n".join(text.splitlines()[:12]), name)

    def test_top_3_risks_heading_in_memo(self):
        self.assertRegex(read(TEMPLATES + "decision_memo.md"), r"(?m)^## Top 3 risks\s*$")

    def test_version_tested_line(self):
        for name in ("decision_pack.md", "decision_memo.md", "test_plan.md"):
            self.assertIn("Version tested:", read(TEMPLATES + name), name)

    def test_decision_first(self):
        for name in ("decision_pack.md", "decision_memo.md"):
            headings = re.findall(r"(?m)^## (.+?)\s*$", read(TEMPLATES + name))
            self.assertEqual(headings[0], "Verdict", name)

    def test_test_plan_template(self):
        text = read(TEMPLATES + "test_plan.md")
        for heading in ("Riskiest assumption", "Budget", "What is built and what is not",
                        "Measures, pass and fail lines", "Go/no-go date", "Fallback pivots"):
            self.assertRegex(text, rf"(?m)^## {heading}\s*$", heading)
        self.assertIn("gate_tracker.csv", text)

    def test_decide_by_placeholders(self):
        # R28: the date fits the deadline, or the conflict is stated.
        placeholder = ("<date, on or before the decision deadline, or the conflict and "
                       "the date the deadline would need to move to>")
        self.assertIn("Decide by: " + placeholder, read(TEMPLATES + "decision_pack.md"))
        go_no_go = read(TEMPLATES + "test_plan.md").split("## Go/no-go date", 1)[1]
        self.assertTrue(go_no_go.lstrip().startswith(placeholder), go_no_go[:120])
        self.assertIn("- Duration: <set-up> plus <live> weeks (<days> days)",
                      read(TEMPLATES + "decision_pack.md"))

    def test_templates_plain(self):
        for name in self.MARKDOWN:
            text = read(TEMPLATES + name)
            self.assertNotIn("!", text, name)
            for word in ("revolutionary", "game-changing", "guaranteed"):
                self.assertNotIn(word, text.lower(), f"{name}: {word}")

    def test_gate_tracker_header(self):
        text = read(TEMPLATES + "gate_tracker.csv")
        self.assertEqual(text.splitlines()[0], GATE_HEADER)

    def test_gate_tracker_example_row(self):
        rows = list(csv.reader(io.StringIO(read(TEMPLATES + "gate_tracker.csv"))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(rows[1]), 7)
        self.assertTrue(rows[1][0].startswith("EXAMPLE"), rows[1][0])


class RecheckTests(unittest.TestCase):
    def test_recheck_tracks_riskiest_assumption_and_contradictions(self):
        recheck = section(agent("byb-sceptical-investor"), "Re-check mode")
        self.assertIn("question 9", recheck)
        self.assertIn("contradictions", recheck)
        for word in ("price", "hires", "timing"):
            self.assertIn(word, recheck, word)


class NoGoBuildTests(unittest.TestCase):
    def test_no_go_build(self):
        # Ruling R2: "Go build" appears only as `never "Go build"`.
        files = [p for folder in ("agents", "skills") for p in (REPO / folder).rglob("*")
                 if p.is_file()]
        self.assertTrue(files)
        for path in files:
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"go build", text, re.I):
                before = text[max(0, match.start() - 7):match.start()]
                self.assertRegex(before, r'(?i)never "$',
                                 f"{path.relative_to(REPO)}: {text[match.start() - 20:match.end()]}")


if __name__ == "__main__":
    unittest.main()
