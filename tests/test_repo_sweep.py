"""Repo-wide sweeps: privacy and copy style across every file a user reads."""
import hashlib
import re
import unittest

from tests.helpers import REPO

HYPE_WORDS = ("revolutionary", "game-changing", "guaranteed")
# SHA-256 digests of lowercase words and phrases that would point to the
# author's real venture (global constraints). Hashes keep the names out of
# the public repo. Phrases are tokens joined with one space.
VENTURE_HASHES = frozenset({
    "8e07df26128d8a78474dc525bf0f0a16afa49344e1ed4229692e13b313de46a8",
    "0fe6a9e7577e05c48dd4771e48779fe231435b53996cf498db15f3e740349c74",
    "525b41e4acf0e6245f5203e1f6a40178975a7530c465d8b3c8417259e76b8904",
    "ed60d7ac6b295cd6865f1219c81c80d5b292737c6f622cfd06359ff8f6d991fa",
    "8d0c55ff709ec2c800179d3d6360034f8f16721cf9b15517e56f9df93de200f7",
    "54e31ac6bab265ef3c18478bf95a821dbe1e5982df358234e488a77a2e22a8d7",
    "0e33fe09060790295ca9626d562c6bd7b328bcb8324b8caf3069c30b1212c662",
    "e3d69273d19322f5c3a4185f306b2788dd953d730f1cc266e08e3640d9b5142c",
})
PHRASE_LENGTHS = (2, 4)
# Case-sensitive: the exact uppercase currency token.
VENTURE_EXACT_HASHES = frozenset({
    "8b9e6c48a28054d0d7e135a850b0cd606269def2dca2af6d24fee770247d59cc",
})
# Ruling R10: the South Asia region pack may name the country.
COUNTRY_HASH = "8e07df26128d8a78474dc525bf0f0a16afa49344e1ed4229692e13b313de46a8"
COUNTRY_ALLOWED = "skills/before-you-build/regions/south-asia.md"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def venture_leaks(text, allow_country=False):
    """Return the hashes of venture words or phrases found in text."""
    tokens = re.findall(r"[^\W\d_]+", text)
    lower = [t.lower() for t in tokens]
    found = {sha(t) for t in tokens} & VENTURE_EXACT_HASHES
    found |= {sha(t) for t in lower} & VENTURE_HASHES
    for n in PHRASE_LENGTHS:
        found |= {sha(" ".join(lower[i:i + n])) for i in range(len(lower) - n + 1)} \
            & VENTURE_HASHES
    if allow_country:
        found.discard(COUNTRY_HASH)
    return found


def files(*roots):
    for root in roots:
        path = REPO / root
        if path.is_file():
            yield path
        else:
            yield from sorted(p for p in path.rglob("*") if p.is_file()
                              and p.suffix in (".md", ".csv"))


def rel(path):
    return path.relative_to(REPO).as_posix()


class PrivacySweepTest(unittest.TestCase):
    def test_no_pointer_to_the_real_venture(self):
        for path in files("docs", "README.md", "CLAUDE.md", "agents", "skills"):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(venture_leaks(text, rel(path) == COUNTRY_ALLOWED), set(),
                             rel(path))

    def test_private_benchmark_reworded(self):
        for doc in ("docs/superpowers/plans/2026-10-12-before-you-build-v0.1.md",
                    "docs/specs/2026-10-12-before-you-build-design.md"):
            text = (REPO / doc).read_text(encoding="utf-8")
            self.assertIn("an optional private comparison against the author's own "
                          "earlier case, never published", text, doc)
            self.assertNotIn("earlier independent assessment", text, doc)


class StyleSweepTest(unittest.TestCase):
    ROOTS = ("agents", "skills", "README.md", "CLAUDE.md")

    def test_no_exclamation_marks_in_prose(self):
        for path in files(*self.ROOTS):
            text = path.read_text(encoding="utf-8").replace("![", "")
            self.assertNotIn("!", text, rel(path))

    def test_no_hype_words(self):
        for path in files(*self.ROOTS):
            # A quoted hype word is the rule naming it, not a use of it.
            text = path.read_text(encoding="utf-8").lower()
            for word in HYPE_WORDS:
                self.assertNotIn(word, text.replace(f'"{word}"', ""), f"{rel(path)}: {word}")

    def test_go_build_only_as_never(self):
        # Ruling R2.
        for path in files(*self.ROOTS):
            text = path.read_text(encoding="utf-8")
            for m in re.finditer(r"go build", text, re.I):
                self.assertTrue(text[:m.start()].lower().endswith('never "'),
                                f"{rel(path)}: {text[max(0, m.start() - 30):m.end()]!r}")


if __name__ == "__main__":
    unittest.main()
