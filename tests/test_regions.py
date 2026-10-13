import re
import unittest

from tests.helpers import REPO, read

REGIONS = [
    "south-asia", "southeast-asia", "east-asia", "middle-east-north-africa",
    "sub-saharan-africa", "europe", "north-america", "latin-america",
]
REGION_FILES = [f"skills/before-you-build/regions/{r}.md" for r in REGIONS]
COMMON_PHRASES = [
    "payment methods", "cash-on-delivery", "logistics", "festival calendar",
    "tax", "funding climate", "trust",
]
CURRENCY = r"(USD|US\$|\$|€|£|¥|₹|৳|Rs\.?)"
FIGURE = re.compile(
    r"\d+(\.\d+)?\s?%"
    rf"|{CURRENCY}\s?\d"
    rf"|\d\s?{CURRENCY}"
    r"|\d+(\.\d+)?\s?(percent|per cent)\b"
    r"|\d+(\.\d+)?\s?(million|billion)\b",
    re.I,
)


def section(text, heading):
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return match.group(1)


class RegionPackTests(unittest.TestCase):
    def test_all_regions_exist(self):
        for rel in REGION_FILES:
            self.assertTrue((REPO / rel).is_file(), rel)

    def test_common_checks(self):
        for rel in REGION_FILES:
            body = section(read(rel), "Common checks").lower()
            for phrase in COMMON_PHRASES:
                self.assertIn(phrase, body, f"{rel}: {phrase}")

    def test_region_specific(self):
        for rel in REGION_FILES:
            body = section(read(rel), "Region-specific checks")
            bullets = [l for l in body.splitlines() if l.lstrip().startswith("- ")]
            self.assertGreaterEqual(len(bullets), 3, rel)

    def test_local_language_section(self):
        for rel in REGION_FILES:
            self.assertTrue(section(read(rel), "Local-language search terms").strip(), rel)

    def test_no_stored_figures(self):
        for rel in REGION_FILES:
            for n, line in enumerate(read(rel).splitlines(), 1):
                self.assertIsNone(FIGURE.search(line), f"{rel}:{n}: {line}")

    def test_one_funding_window(self):
        for rel in REGION_FILES:
            body = section(read(rel), "Common checks")
            line = next(l for l in body.splitlines() if l.startswith("6. "))
            self.assertIn("the last 12 to 24 months", line, rel)
        scout = read("agents/byb-funding-climate-scout.md")
        self.assertEqual(len(re.findall(r"last 12 to 24 months", scout)), 2)
        self.assertNotIn("roughly the last", scout)

    def test_spelling(self):
        self.assertNotIn("interést", read(REGION_FILES[3]))
        self.assertIn("interest", read(REGION_FILES[3]))
        self.assertIn("Côte d'Ivoire", read(REGION_FILES[4]))
        self.assertNotIn("Cote d'Ivoire", read(REGION_FILES[4]))


if __name__ == "__main__":
    unittest.main()
