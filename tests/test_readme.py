import re
import sys
import unittest

from tests.helpers import DISCLAIMER, REPO, read

sys.path.insert(0, str(REPO / "scripts"))
from check_run import expected_files  # noqa: E402


class ReadmeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = read("README.md")

    def test_tagline_and_version(self):
        self.assertIn("An AI investment committee for founders.", self.readme)
        self.assertIn("v0.1", self.readme)

    def test_install_commands(self):
        self.assertIn("## Install", self.readme)
        self.assertIn("/plugin marketplace add elakarborobhai21/before-you-build", self.readme)
        self.assertIn("/plugin install before-you-build@before-you-build", self.readme)

    def test_required_headings(self):
        for heading in ("## How it works", "## What you get", "## Limits", "## Acknowledgements"):
            self.assertIn(heading, self.readme)

    def test_modes_paths_and_diagrams(self):
        for word in ("Quick Check", "Full Review", "Path A", "Path B"):
            self.assertIn(word, self.readme)
        self.assertGreaterEqual(self.readme.count("```mermaid"), 2)

    def test_full_review_business_model_first(self):
        how = self.readme.split("### Full Review", 1)[1].split("```", 3)[1]
        order = [how.find(word) for word in ("Business Model", "Operations", "Financial")]
        self.assertNotIn(-1, order)
        self.assertEqual(order, sorted(order))
        rebuild = how[order[0]:how.find("re-check")]
        self.assertNotIn("in parallel", rebuild)
        self.assertNotIn("3 rebuild agents", how)

    def test_full_review_rebuild_sentence(self):
        self.assertIn("In the rebuild, the agents work one at a time: the Business Model "
                      "Designer first, then the Operations & Product Planner from its rebuilt "
                      "offer, then the Financial Modeller from both", self.readme)
        self.assertNotIn("then work in parallel from its rebuilt offer", self.readme)

    def test_verdicts_and_labels(self):
        scorecard = self.readme.split("### The Committee Scorecard", 1)[1].split("\n## ", 1)[0]
        self.assertIn("The verdict is one of **Go to test**, **Pivot** or **Stop**.", scorecard)
        for word in ("[S]", "[E]", "[A]"):
            self.assertIn(word, self.readme)
        self.assertNotIn("Go build", self.readme)

    def test_example_links_exist_and_windows_note(self):
        self.assertNotIn("coming in", self.readme)
        for path in set(re.findall(r"\]\((examples/[^)#]+)\)", self.readme)):
            self.assertTrue((REPO / path.rstrip("/")).exists(), path)
        install = self.readme.split("## Install", 1)[1].split("\n## ", 1)[0]
        requirements = install.split("In Claude Code, run", 1)[0]
        self.assertIn("On Windows, python3 may be called python or py.", requirements)

    def test_disclaimer_verbatim(self):
        self.assertIn(DISCLAIMER, self.readme)

    def test_acknowledgements(self):
        for text in ("idea-validation-agents", "Max Kmet", "agency-agents", "msitarzewski",
                     "Built with Claude", "## Licence", "MIT"):
            self.assertIn(text, self.readme)

    def test_no_hype_or_exclamations(self):
        self.assertNotIn("!", self.readme.replace("![", ""))
        for word in ("revolutionary", "game-changing", "guaranteed"):
            self.assertNotIn(word, self.readme.lower())


    def test_file_paths_match_checker(self):
        known = set()
        for mode, paths in (("quick", ("A",)), ("full", ("A", "B"))):
            for path in paths:
                known.update(expected_files(mode, path, 4 if mode == "quick" else 5))
        tokens = set(re.findall(r"\b\d\d_[a-z]+/[A-Za-z0-9_.]+\.[a-z]+", self.readme))
        self.assertTrue(tokens)
        for token in tokens:
            self.assertIn(token, known)


class ClaudeMdTests(unittest.TestCase):
    def test_contributor_notes(self):
        text = read("CLAUDE.md")
        self.assertIn("python3 -m unittest discover -s tests -v", text)
        self.assertIn("Global Constraints", text)
        self.assertIn("Inputs, Must cover, Output, Rules", text.replace("`", "").replace("## ", ""))


if __name__ == "__main__":
    unittest.main()
