import re
import unittest

from tests.agentlint import lint_agent, section
from tests.helpers import DISCLAIMER, frontmatter, read

TEMPLATES = "skills/before-you-build/templates/"

# agent stem -> (output path, must-mentions from spec §5 "What each agent must cover")
RESEARCH_AGENTS = {
    "byb-market-competition-scout": (
        "10_research/market_competition.md",
        ["bottom-up", "payment", "logistics", "competitors",
         "pricing", "reviews", "incumbent", "local-language"],
    ),
    "byb-market-region-researcher": (
        "10_research/market_region.md",
        ["bottom-up", "Payment habits", "Cash-on-delivery share", "Logistics cost",
         "failure rates", "Seasonality", "festival calendar", "Internet and device use",
         "Local norms"],
    ),
    "byb-competition-scout": (
        "10_research/competition.md",
        ["Local and global competitors", "pricing", "reviews", "weak spots", "incumbent",
         "Global analogies", "local-language"],
    ),
    "byb-customer-demand-analyst": (
        "10_research/customer_demand.md",
        ["Who buys", "How often", "Current alternative", "Willingness to pay",
         "channels", "Cost to acquire", "range", "Repeat behaviour"],
    ),
    "byb-regulation-structure-mapper": (
        "10_research/regulation_structure.md",
        ["licences", "registrations", "tax", "Consumer", "Data", "Payments",
         "incorporate", "never legal advice"],
    ),
    "byb-founder-fit-reviewer": (
        "10_research/founder_fit.md",
        ["technical", "commercial", "finance", "operations", "full-time", "conflict",
         "competitor", "partner", "regulator", "runway", "What investors will ask"],
    ),
    "byb-funding-climate-scout": (
        "10_research/funding_climate.md",
        ["Recent deals", "cheque sizes", "Active investors", "Non-dilutive",
         "current climate"],
    ),
}
# Agents that read a region pack (Founder Fit reads only the brief, spec §5).
REGION_READERS = [a for a in RESEARCH_AGENTS if a != "byb-founder-fit-reviewer"]

# Opening words of Rules items that must read identically across agents.
SHARED_RULES_ALL = [
    "Label every figure", "Never invent", "When sources disagree", "Give the date",
    "If web search is unavailable", "A figure seen only in a search snippet",
    "Keep the brief under", "Do not write to", "Write in plain",
]
SHARED_RULES_REGION_READERS = ["The launch country is the primary market", "Prefer primary sources"]

INTAKE_HEADINGS = [
    "The idea", "Region and country", "Target customer", "Founders",
    "Money and time", "Existing report", "Mode", "Currency",
]


def agent_path(stem):
    return f"agents/{stem}.md"


class TemplateTests(unittest.TestCase):
    def test_templates(self):
        brief = read(TEMPLATES + "brief.md")
        for heading in INTAKE_HEADINGS:
            self.assertRegex(brief, rf"(?m)^## {re.escape(heading)}\s*$", heading)
        research = read(TEMPLATES + "research_brief.md")
        for heading in ("Key findings", "Evidence", "Gaps and assumptions", "Sources"):
            self.assertRegex(research, rf"(?m)^## {heading}\s*$", heading)
        self.assertIn(DISCLAIMER, research)

    def test_brief_template_founder_block(self):
        founders = section(read(TEMPLATES + "brief.md"), "Founders")
        for field in ("Role", "Experience", "Current job and employer type",
                      "Hours per week", "Full-time from", "Months without salary",
                      "Current-employer conflict"):
            self.assertIn(field, founders)
        self.assertIn("optional", founders.lower())

    def test_brief_template_disclaimer(self):
        self.assertIn(DISCLAIMER, read(TEMPLATES + "brief.md"))

    def test_research_brief_search_status_at_top(self):
        research = read(TEMPLATES + "research_brief.md")
        first_section = research.index("## Key findings")
        self.assertIn("Search status", research[:first_section])
        self.assertIn("partly available: <what failed>", research[:first_section])


class ResearchAgentTests(unittest.TestCase):
    def check(self, stem):
        out, mentions = RESEARCH_AGENTS[stem]
        self.assertEqual(lint_agent(agent_path(stem), [out], mentions), [])
        cover = section(read(agent_path(stem)), "Must cover")
        for phrase in mentions:
            self.assertIn(phrase, cover, f"{stem}: {phrase} not in ## Must cover")

    def test_market_competition_scout(self):
        self.check("byb-market-competition-scout")

    def test_market_region_researcher(self):
        self.check("byb-market-region-researcher")

    def test_competition_scout(self):
        self.check("byb-competition-scout")

    def test_customer_demand_analyst(self):
        self.check("byb-customer-demand-analyst")

    def test_regulation_structure_mapper(self):
        self.check("byb-regulation-structure-mapper")

    def test_founder_fit_reviewer(self):
        self.check("byb-founder-fit-reviewer")

    def test_funding_climate_scout(self):
        self.check("byb-funding-climate-scout")

    def test_research_tools(self):
        for stem in RESEARCH_AGENTS:
            tools = frontmatter(read(agent_path(stem)))["tools"]
            for tool in ("WebSearch", "WebFetch", "Read", "Write"):
                self.assertIn(tool, tools, f"{stem}: {tool}")

    def test_search_unavailable_rule(self):
        for stem in RESEARCH_AGENTS:
            rules = section(read(agent_path(stem)), "Rules")
            self.assertIn("If web search is unavailable", rules, stem)
            self.assertIn("[A]", rules, stem)

    def test_snippet_only_rule(self):
        for stem in RESEARCH_AGENTS:
            rules = section(read(agent_path(stem)), "Rules")
            self.assertIn("snippet only, page not opened", rules, stem)
            self.assertIn("never `[S]`", rules, stem)

    def test_global_analogy_without_pages(self):
        for stem, item in (("byb-market-competition-scout", "One global analogy"),
                           ("byb-competition-scout", "Global analogies")):
            cover = section(read(agent_path(stem)), "Must cover")
            line = next(l for l in cover.splitlines() if item in l)
            for phrase in ("from general knowledge, not checked", "`[A]`",
                           "no fair analogy exists",
                           "web search itself is down",
                           "web search unavailable, not checked live"):
                self.assertIn(phrase, line, f"{stem}: {phrase}")

    def test_shared_rules_identical(self):
        # Shared rules must not drift between agents. Founder Fit rewords the
        # neighbour and source-preference rules, so those are shared by six.
        def rule_lines(stem):
            rules = section(read(agent_path(stem)), "Rules")
            return [re.sub(r"^\d+\. ", "", l) for l in rules.splitlines() if re.match(r"^\d+\. ", l)]

        def find(lines, prefix, stem):
            hits = [l for l in lines if l.startswith(prefix)]
            self.assertEqual(len(hits), 1, f"{stem}: {prefix}")
            return hits[0]

        groups = {
            tuple(RESEARCH_AGENTS): SHARED_RULES_ALL,
            tuple(REGION_READERS): SHARED_RULES_REGION_READERS,
        }
        for stems, prefixes in groups.items():
            for prefix in prefixes:
                texts = {find(rule_lines(stem), prefix, stem) for stem in stems}
                self.assertEqual(len(texts), 1, f"rule drifted: {prefix}")

    def test_run_dir_paths(self):
        for stem in RESEARCH_AGENTS:
            text = read(agent_path(stem))
            inputs = section(text, "Inputs")
            self.assertIn("<RUN_DIR>/00_brief.md", inputs, stem)
            self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/references/conventions.md",
                          inputs, stem)
            out, _ = RESEARCH_AGENTS[stem]
            output = section(text, "Output")
            self.assertIn(f"<RUN_DIR>/{out}", output, stem)
            self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/templates/research_brief.md",
                          output, stem)

    def test_dispatch_may_name_a_sibling_file(self):
        # Ruling R20: in an upgrade the lead may let these agents read market_competition.md.
        for stem in ("byb-market-region-researcher", "byb-competition-scout"):
            inputs = section(read(agent_path(stem)), "Inputs")
            self.assertIn("Do not read other files in `<RUN_DIR>/10_research/` unless the "
                          "lead's dispatch names a file you may read.", inputs, stem)

    def test_region_pack_input(self):
        for stem in REGION_READERS:
            inputs = section(read(agent_path(stem)), "Inputs")
            self.assertIn("<PLUGIN_ROOT>/skills/before-you-build/regions/<region>.md",
                          inputs, stem)

    def test_sources_stay_in_own_file(self):
        # Ruling R7: parallel agents never write to the shared sources.md.
        for stem in RESEARCH_AGENTS:
            text = read(agent_path(stem))
            self.assertIn("## Sources", section(text, "Output"), stem)
            self.assertIn("Do not write to `<RUN_DIR>/sources.md`", text, stem)
            for line in text.splitlines():
                if "sources.md" in line:
                    self.assertIn("Do not write to", line, f"{stem}: {line}")

    def test_honesty_rules(self):
        for stem in RESEARCH_AGENTS:
            rules = section(read(agent_path(stem)), "Rules")
            for phrase in ("launch country", "comparison only", "primary",
                           "local-language", "Never invent", "unknown",
                           "show the range", "1,500 words", "Stay in your lane"):
                self.assertIn(phrase, rules, f"{stem}: {phrase}")

    def test_no_hype_or_exclamation(self):
        for stem in RESEARCH_AGENTS:
            text = read(agent_path(stem))
            self.assertNotIn("!", text, stem)
            for word in ("revolutionary", "game-changing", "guaranteed"):
                self.assertNotIn(word, text.lower(), f"{stem}: {word}")

    def test_founder_fit_modes(self):
        text = read(agent_path("byb-founder-fit-reviewer"))
        cover = section(text, "Must cover")
        self.assertIn("**Quick Check form (short).**", cover)
        self.assertIn("in the team table", cover)
        self.assertIn("**Full Review form.**", cover)
        quick = cover[cover.index("**Quick Check form"):cover.index("**Full Review form")]
        for word in ("role", "full-time", "conflict"):
            self.assertIn(word, quick)
        full = cover[cover.index("**Full Review form"):]
        for phrase in ("personal runway", "hours per week", "non-compete"):
            self.assertIn(phrase, full.lower())
        self.assertIn("mode", section(text, "Inputs"))

    def test_founder_fit_privacy(self):
        rules = section(read(agent_path("byb-founder-fit-reviewer")), "Rules")
        self.assertIn("Never search for private information", rules)
        self.assertIn("written employer clearance", rules)
        self.assertIn("legal opinion", rules)

    def test_market_competition_scout_leaves_willingness_to_pay(self):
        cover = section(read(agent_path("byb-market-competition-scout")), "Must cover")
        self.assertIn("cited sizing input only", cover)
        self.assertIn("willingness to pay stays with the Customer & Demand Analyst", cover)

    def test_market_competition_scout_is_quick_only(self):
        meta = frontmatter(read(agent_path("byb-market-competition-scout")))
        self.assertIn("Quick Check", meta["description"])

    def test_descriptions_are_yaml_safe(self):
        for stem in RESEARCH_AGENTS:
            description = frontmatter(read(agent_path(stem)))["description"]
            self.assertNotIn(": ", description, stem)
            self.assertNotIn(" #", description, stem)


class AgentLintTests(unittest.TestCase):
    def test_reports_missing_file(self):
        self.assertTrue(lint_agent("agents/byb-does-not-exist.md", [], []))

    def test_reports_problems(self):
        # A region pack is not an agent: no frontmatter.
        problems = lint_agent("skills/before-you-build/regions/europe.md", [], [])
        self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
