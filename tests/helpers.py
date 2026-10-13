"""Shared helpers for the Before You Build test suite (stdlib only)."""
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent

DISCLAIMER = (
    "This report was produced by AI agents using publicly available information "
    "and the details you provided. Figures may be incomplete, out of date or wrong; "
    "each is marked sourced, estimated or assumed. It is not financial, legal, tax "
    "or investment advice. Check important figures yourself and talk to real "
    "customers before acting."
)


def read(rel_path: str) -> str:
    """Return the text of a file given a path relative to the repo root."""
    return (REPO / rel_path).read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    """Parse the leading '---' block into a dict of raw string values."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter block")
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.strip()] = value.strip()
    raise ValueError("unterminated frontmatter block")
