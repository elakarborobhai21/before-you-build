import json
import re
import unittest

from scripts.scorecard import AREAS, score
from tests.helpers import DISCLAIMER, read

REF = "skills/before-you-build/references/"


class ReferencesTest(unittest.TestCase):
    def test_scorecard_md_matches_engine(self):
        text = read(REF + "scorecard.md")
        for area in AREAS:
            self.assertIn(f"`{area}`", text)
        for phrase in ("Strong (3)", "Adequate (2)", "Weak (1)", "Fatal (0)"):
            self.assertIn(phrase, text)
        self.assertIn('python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py"', text)
        self.assertIn("scorecard_inputs_v1.json", text)

    def test_scorecard_md_example_validates(self):
        text = read(REF + "scorecard.md")
        example = re.search(r"```json\n(.*?)\n```", text, re.S).group(1)
        result = score(json.loads(example))
        self.assertIn(result["verdict"], ("Go to test", "Pivot", "Stop"))

    def test_ten_questions(self):
        lines = [l for l in read(REF + "questions.md").splitlines() if re.match(r"^\d+\. ", l)]
        self.assertEqual(len(lines), 10)
        for i, line in enumerate(lines, 1):
            self.assertTrue(line.startswith(f"{i}. "), line)
        self.assertIn("single assumption", lines[8])

    def test_conventions(self):
        text = read(REF + "conventions.md")
        self.assertIn("DISCLAIMER", text)
        self.assertIn("> " + DISCLAIMER, text)
        for token in ("[S]", "[E]", "[A]", "Defensive", "Moderate", "Optimistic",
                      "Go to test", "Pivot", "Stop",
                      "~/before-you-build-runs/<idea-slug>-<YYYY-MM-DD>/"):
            self.assertIn(token, text)

    def test_conventions_sources_compiled_by_lead(self):
        text = read(REF + "conventions.md")
        self.assertIn("the lead compiles `sources.md` from those sections after each stage", text)
        self.assertNotIn("whichever agent", text)

    def test_scorecard_md_error_handling(self):
        text = read(REF + "scorecard.md")
        for phrase in ("stdout", "stderr", "exit code 2",
                       "delete any partial `scorecard_result.json`",
                       "Never leave a result file after an error"):
            self.assertIn(phrase, text)

    def test_never_go_build(self):
        for name in ("scorecard.md", "questions.md", "conventions.md"):
            for m in re.finditer(r"go build", read(REF + name), re.I):
                self.assertTrue(read(REF + name)[:m.start()].endswith('never "'), name)


if __name__ == "__main__":
    unittest.main()
