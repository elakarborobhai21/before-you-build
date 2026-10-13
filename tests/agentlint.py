"""Structural checks shared by every agent test (stdlib only)."""
import pathlib
import re

from tests.helpers import REPO, frontmatter, read

REQUIRED_SECTIONS = ("Inputs", "Output", "Must cover", "Rules")


def section(text: str, heading: str) -> str | None:
    """Return the body of a '## heading' section, or None if it is missing."""
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else None


def lint_agent(rel_path: str, output_paths: list[str], must_mention: list[str]) -> list[str]:
    """Return a list of problems with an agent file; an empty list means clean."""
    path = REPO / rel_path
    if not path.is_file():
        return [f"{rel_path}: file not found"]
    text = read(rel_path)
    problems: list[str] = []
    try:
        meta = frontmatter(text)
    except ValueError as exc:
        return [f"{rel_path}: {exc}"]

    stem = pathlib.Path(rel_path).stem
    if meta.get("name") != stem:
        problems.append(f"{rel_path}: name {meta.get('name')!r} does not match {stem!r}")
    description = meta.get("description", "")
    if not description:
        problems.append(f"{rel_path}: description is empty")
    elif not description.startswith("Use "):
        problems.append(f"{rel_path}: description does not start with 'Use '")
    if not meta.get("tools"):
        problems.append(f"{rel_path}: tools missing")

    for heading in REQUIRED_SECTIONS:
        if section(text, heading) is None:
            problems.append(f"{rel_path}: missing section ## {heading}")

    output = section(text, "Output") or ""
    for out in output_paths:
        if out not in output:
            problems.append(f"{rel_path}: output path {out!r} not in ## Output")

    for phrase in must_mention:
        if phrase not in text:
            problems.append(f"{rel_path}: does not mention {phrase!r}")

    if "references/conventions.md" not in text:
        problems.append(f"{rel_path}: does not mention references/conventions.md")
    return problems
