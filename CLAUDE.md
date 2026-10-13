# Notes for contributors and AI agents

This repository is the Before You Build plugin for Claude Code: a lead skill plus subagents. Read the design spec in `docs/specs/` before changing behaviour.

## Run the tests

From the repository root, Python 3.10 or later, standard library only:

```
python3 -m unittest discover -s tests -v
```

Run the full suite before every commit.

## Global Constraints (short form)

- Python: standard library only.
- Licence: MIT, `Copyright (c) 2026 Yaseer Ahsan`.
- Evidence labels, exactly: `[S]` sourced (with link), `[E]` estimated (with method), `[A]` assumed (with reason).
- Verdict words, exactly: `Go to test`, `Pivot`, `Stop`. Never "Go build".
- Scenario names, exactly: `Defensive`, `Moderate`, `Optimistic`.
- Run folder: `~/before-you-build-runs/<idea-slug>-<YYYY-MM-DD>/`.
- The disclaimer (spec section 11) appears verbatim in every output template and in the README. `tests/helpers.py` holds the exact text.
- Copy style: plain, direct, no exclamation marks, no hype words.
- No real ventures, real founders or real private figures anywhere in the repository. Examples are fictional.
- Credits (spec section 14) stay in the README.

## Agent file conventions

- One file per agent: `agents/byb-<role>.md`.
- Frontmatter has `name` (equal to the filename without `.md`), `description` and `tools`. Grant the fewest tools the agent needs.
- Body sections, in order: `## Inputs`, `## Must cover`, `## Output`, `## Rules`. Extra sections (Lanes, Quick Check, Full Review, Re-check mode) are allowed where a role needs them.
- The lead passes two absolute paths in every dispatch: `RUN_DIR` (the run folder) and `PLUGIN_ROOT` (the plugin root). Agents refer to files as `<RUN_DIR>/...` and `<PLUGIN_ROOT>/skills/before-you-build/...`. Do not rely on variable expansion inside agent bodies.
- Agents that run in parallel never write to the shared `sources.md`. Each lists its links in its own output file under `## Sources`, and the lead compiles `<RUN_DIR>/sources.md`.
- Critics never read the drafter's working notes.

## Keep in sync

- Keep the shared Rules lines identical across the seven research agents (a test checks this). If you change one, change all seven.
- If you change a stage, a file name or a verdict rule, update the skill, the templates, `scripts/check_run.py` and its tests together.
