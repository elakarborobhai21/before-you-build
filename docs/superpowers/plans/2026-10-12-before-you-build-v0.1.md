# Before You Build v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v0.1 of Before You Build as an installable Claude Code plugin: a lead skill that runs Quick Check and Full Review, 17 specialist agent files, region packs, templates, a deterministic scorecard, a run checker, a README and one fictional worked example.

**Architecture:** Almost everything is Markdown read by Claude: one lead skill (`skills/before-you-build/SKILL.md`) runs the intake and dispatches subagents (`agents/byb-*.md`) stage by stage, with handoffs through files in a run folder. Two small Python scripts make the judgement rules and stage checks deterministic: `scripts/scorecard.py` (spec §6) and `scripts/check_run.py` (spec §9). A stdlib `unittest` suite checks both scripts and lints every Markdown file for the structure the spec requires.

**Tech Stack:** Claude Code plugin format (`.claude-plugin/plugin.json`, `marketplace.json`, `agents/`, `skills/`), Markdown with YAML frontmatter, Python 3.10+ standard library only (`unittest`, `json`, `csv`, `pathlib`, `argparse`, `re`).

**Spec:** `docs/specs/2026-10-12-before-you-build-design.md`

## Global Constraints

- Python: standard library only, Python ≥ 3.10. Tests run with `python3 -m unittest discover -s tests -v` from the repo root.
- Licence: MIT, copyright line `Copyright (c) 2026 Yaseer Ahsan`.
- Every agent file is `agents/byb-<role>.md`. Frontmatter `name` equals the filename without `.md`.
- Evidence labels, exactly: `[S]` sourced (with link), `[E]` estimated (with method), `[A]` assumed (with reason).
- Verdict words, exactly: `Go to test`, `Pivot`, `Stop`. Never "Go build".
- Scenario names, exactly: `Defensive`, `Moderate`, `Optimistic`.
- Run folder: `~/before-you-build-runs/<idea-slug>-<YYYY-MM-DD>/`.
- Disclaimer text (spec §11), verbatim, in every output template and the README:
  > This report was produced by AI agents using publicly available information and the details you provided. Figures may be incomplete, out of date or wrong; each is marked sourced, estimated or assumed. It is not financial, legal, tax or investment advice. Check important figures yourself and talk to real customers before acting.
- Copy style: plain, direct, no exclamation marks, no hype words ("revolutionary", "game-changing", "guaranteed").
- No names, employers or figures from the author's own earlier case appear anywhere in the repo.
- Credit lines (spec §14) appear in the README.

## Review Focus

1. **Scorecard given bad input** (missing area, rating 4, rating "Strong" as text) → exits with code 2 and a message naming the bad key; never prints a verdict. *Test in Task 2.*
2. **Path B report the agents cannot read** (scanned PDF, image, password-protected file) → lead asks the founder to paste the text instead and does not continue with an empty draft. *Test in Task 8 (SKILL.md must state this).*
3. **Region outside the eight packs or several countries** → lead uses the closest pack, tells the founder which, and research agents treat only the launch country as primary. *Test in Task 8.*
4. **Run folder already exists for the same idea and date** → lead creates `<slug>-<date>-2` (then `-3`), never overwrites. *Test in Task 8 and `check_run.py` unaffected.*
5. **Web search unavailable or blocked** → research agents say so at the top of their brief, label figures `[A]`, and the scorecard confidence comes out Low. *Test in Task 5 (every research agent states this rule).*

---

### Task 1: Plugin scaffold and test harness

**Files:**
- Create: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `LICENSE`, `.gitignore`, `tests/__init__.py`, `tests/helpers.py`, `tests/test_manifest.py`

**Interfaces:**
- Produces: `tests/helpers.py` with `REPO: pathlib.Path` (repo root), `DISCLAIMER: str` (verbatim text above), `read(rel_path: str) -> str`, `frontmatter(text: str) -> dict[str, str]` (parses the `---` block at the top; values as raw strings; raises `ValueError` if absent).

- [ ] **Step 1: Write the failing tests** in `tests/test_manifest.py`:
  - `test_plugin_json_fields`: loads `.claude-plugin/plugin.json`; asserts `name == "before-you-build"`, `version == "0.1.0"`, `license == "MIT"`, `repository == "https://github.com/elakarborobhai21/before-you-build"`, `description` non-empty.
  - `test_marketplace_lists_plugin`: loads `.claude-plugin/marketplace.json`; asserts `name == "before-you-build"`, `owner["name"]` non-empty, `plugins[0]["name"] == "before-you-build"`, `plugins[0]["source"] == "./"`.
  - `test_license_is_mit`: `LICENSE` starts with `MIT License` and contains `Copyright (c) 2026 Yaseer Ahsan`.
  - `test_frontmatter_helper`: `frontmatter("---\nname: x\ndescription: y\n---\nbody") == {"name": "x", "description": "y"}`; `frontmatter("no block")` raises `ValueError`.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_manifest -v` → FAIL (files missing).
- [ ] **Step 3: Create the files.** `plugin.json` also has `author: {"name": "Yaseer Ahsan"}`, `homepage` = repository URL, `keywords: ["startup", "founders", "validation", "investment-committee", "emerging-markets"]`. `.gitignore`: `__pycache__/`, `*.pyc`, `before-you-build-runs/`.
- [ ] **Step 4: Run** the same command → PASS.
- [ ] **Step 5: Commit** `chore: plugin scaffold, licence and test harness`.

---

### Task 2: Scorecard engine (spec §6)

**Files:**
- Create: `scripts/scorecard.py`, `tests/test_scorecard.py`

**Interfaces:**
- Produces:
  - `AREAS: tuple[str, ...] = ("customer_pull", "route_to_customers", "money_per_transaction", "cash_to_proof", "competitive_response", "team_commitment", "rules_operations")`
  - `score(inputs: dict) -> dict` where `inputs` = `{"ratings": {area: int 0–3}, "test_measures_unit_economics": bool, "fulltime_within_6_months": bool, "label_counts": {"S": int, "E": int, "A": int}}` and the result = `{"readiness_score": int, "verdict": str, "confidence": "High"|"Medium"|"Low", "reasons": list[str]}`
  - `class ScorecardError(ValueError)` for bad input.
  - CLI: `python3 scripts/scorecard.py <inputs.json>` prints the result as JSON to stdout, exit 0; on `ScorecardError` prints `error: <message>` to stderr, exit 2.

**Rules (decided here, from spec §6):**
- `readiness_score = floor(sum(ratings) * 100 / 21 + 0.5)`.
- Provisional verdict: score ≥ 65 → `Go to test`; 40–64 → `Pivot`; < 40 → `Stop`.
- Overrides, applied in order: ≥ 2 ratings of 0 → `Stop`. Exactly one 0 and provisional `Go to test` → `Pivot`. `money_per_transaction` ≤ 1 and not `test_measures_unit_economics` and verdict `Go to test` → `Pivot`. Not `fulltime_within_6_months` and verdict `Go to test` → `Pivot`. Each override that fires appends one plain-English sentence to `reasons`.
- Confidence from `label_counts` (figures behind areas 1–4): total 0 → `Low`; `S/total > 0.5` → `High`; `A/total > 0.5` → `Low`; else `Medium`.

- [ ] **Step 1: Write the failing tests** (`all_x` builds ratings with every area = x; defaults `test_measures_unit_economics=True`, `fulltime_within_6_months=True`, `label_counts={"S":6,"E":2,"A":2}`):
  - `test_all_strong`: all 3 → score 100, `Go to test`, `High`.
  - `test_all_adequate`: all 2 → 67, `Go to test`.
  - `test_thresholds`: sum 13 → 62 `Pivot`; sum 9 → 43 `Pivot`; sum 8 → 38 `Stop`.
  - `test_one_fatal_caps_at_pivot`: six 3s and `rules_operations` 0 → 86, `Pivot`, one reason mentioning "Fatal".
  - `test_two_fatal_is_stop`: five 3s and two 0s → 71, `Stop`.
  - `test_weak_unit_economics_not_measured`: all 3 except `money_per_transaction` 1, flag False → `Pivot`; same with flag True → `Go to test`.
  - `test_no_fulltime_founder`: all 3, `fulltime_within_6_months` False → `Pivot`.
  - `test_low_score_stays_stop_with_fatal`: all 1 except one 0 → 29, `Stop`.
  - `test_confidence`: `{"S":0,"E":0,"A":0}` → Low; `{"S":2,"E":2,"A":6}` → Low; `{"S":3,"E":4,"A":3}` → Medium.
  - `test_bad_input` (Review Focus 1): missing `team_commitment`, value 4, value `"Strong"`, unknown area key → each raises `ScorecardError` whose message contains the key.
  - `test_cli`: run via `subprocess` with a temp JSON file → exit 0 and parsed stdout has `verdict`; with a bad file → exit 2, stdout empty, stderr starts `error:`.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_scorecard -v` → FAIL (module missing).
- [ ] **Step 3: Implement** `scripts/scorecard.py` per the interface and rules above.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: deterministic committee scorecard`.

---

### Task 3: Shared references (scorecard guide, ten questions, conventions)

**Files:**
- Create: `skills/before-you-build/references/scorecard.md`, `skills/before-you-build/references/questions.md`, `skills/before-you-build/references/conventions.md`, `tests/test_references.py`

**Interfaces:**
- Consumes: `AREAS` from Task 2.
- Produces: the three reference files every agent cites by path.

- [ ] **Step 1: Write the failing tests:**
  - `test_scorecard_md_matches_engine`: every key in `AREAS` appears in `scorecard.md` in backticks; the file contains `Strong (3)`, `Adequate (2)`, `Weak (1)`, `Fatal (0)` and the command `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scorecard.py"`.
  - `test_ten_questions`: `questions.md` has exactly ten lines matching `^\d+\. ` numbered 1–10 in order, and question 9 contains "single assumption".
  - `test_conventions`: `conventions.md` contains `DISCLAIMER`, the three labels `[S]`, `[E]`, `[A]`, the three scenario names, the three verdict words, and the run-folder pattern.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_references -v` → FAIL.
- [ ] **Step 3: Write the files.** `scorecard.md`: spec §6 table, rating meanings with one example each, how to fill the inputs JSON for the engine, and that the engine's verdict is final. `questions.md`: spec §7 verbatim. `conventions.md`: evidence labels with one example each, currency rule (local currency first, USD in brackets at the brief's rate), scenario names, verdict words, copy style from Global Constraints, `sources.md` format (`- [title](url) — accessed YYYY-MM-DD — used in <file>`), and the disclaimer.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `docs: scorecard guide, committee questions and conventions`.

---

### Task 4: Region packs (spec §8)

**Files:**
- Create: `skills/before-you-build/regions/{south-asia,southeast-asia,east-asia,middle-east-north-africa,sub-saharan-africa,europe,north-america,latin-america}.md`, `tests/test_regions.py`

**Interfaces:**
- Produces: `REGION_FILES` naming above; each file has `## Common checks` and `## Region-specific checks` and `## Local-language search terms`.

- [ ] **Step 1: Write the failing tests:**
  - `test_all_regions_exist`: the eight files exist.
  - `test_common_checks`: each `## Common checks` section contains these seven phrases: `payment methods`, `cash-on-delivery`, `logistics`, `festival calendar`, `tax`, `funding climate`, `trust`.
  - `test_region_specific`: each `## Region-specific checks` section has ≥ 3 bullets.
  - `test_no_stored_figures`: no line in any region file matches `\d+(\.\d+)?\s?%` or a currency amount (`(USD|US\$|\$|€|£)\s?\d`), so packs stay checklists.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_regions -v` → FAIL.
- [ ] **Step 3: Write the eight packs.** Region-specific examples from spec §8 (mobile money for Sub-Saharan Africa and South Asia; instalments for Latin America; Sharia-compliant finance and free zones for the Gulf in MENA; super-apps for Southeast Asia); add at least one more per region (e.g. GDPR and VAT OSS for Europe; state-level sales tax for North America; platform dominance and payment super-apps for East Asia). Each item is phrased as a question to answer with a source.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: eight region checklists`.

---

### Task 5: Templates and research agents (Stage 1)

**Files:**
- Create: `skills/before-you-build/templates/{brief,research_brief}.md`; `agents/byb-{market-competition-scout,market-region-researcher,competition-scout,customer-demand-analyst,regulation-structure-mapper,founder-fit-reviewer,funding-climate-scout}.md`; `tests/agentlint.py`; `tests/test_agents_research.py`

**Interfaces:**
- Consumes: `helpers.frontmatter`, `DISCLAIMER`; references from Tasks 3–4.
- Produces: `tests/agentlint.py` with `lint_agent(rel_path: str, output_paths: list[str], must_mention: list[str]) -> list[str]` returning problems (empty list = clean). It checks: frontmatter `name` = filename stem; `description` non-empty and starts with "Use "; `tools` present; sections `## Inputs`, `## Output`, `## Must cover`, `## Rules` exist; every `output_paths` string appears in `## Output`; every `must_mention` string appears somewhere; the body mentions `references/conventions.md`.
- Agent output paths (relative to the run folder), fixed here for every later task: see the table in spec §5; Quick Check's founder brief is `10_research/founder_fit.md` in both modes.

- [ ] **Step 1: Write the failing tests:**
  - `test_templates`: `brief.md` contains a heading for each of the 8 intake topics in spec §4; `research_brief.md` contains `## Key findings`, `## Evidence`, `## Gaps and assumptions`, `## Sources` and the `DISCLAIMER`.
  - One test per agent calling `lint_agent` with its spec §5 output path and must-mentions taken from spec §5 "What each agent must cover" (e.g. competition scout: `local-language`, `incumbent`, `reviews`; founder fit: `full-time`, `conflict`, `runway`, `technical`).
  - `test_research_tools`: each research agent's `tools` contains `WebSearch`, `WebFetch`, `Read`, `Write`.
  - `test_search_unavailable_rule` (Review Focus 5): each research agent's `## Rules` contains "If web search is unavailable" and `[A]`.
  - `test_founder_fit_modes`: `byb-founder-fit-reviewer.md` describes both the Quick Check short form (role, full-time, conflict) and the Full Review form.
  - `test_market_competition_scout_is_quick_only`: its description says "Quick Check".
- [ ] **Step 2: Run** `python3 -m unittest tests.test_agents_research -v` → FAIL.
- [ ] **Step 3: Write the two templates and seven agents.** Each agent: role in one paragraph, `## Inputs` (`00_brief.md`, the region pack named in the brief), `## Must cover` (spec §5 bullets for that role), `## Output` (its path, built on `templates/research_brief.md`, plus appending used links to `sources.md`), `## Rules` (label every figure; prefer local and primary sources; never invent a source; search-unavailable rule; stay in your lane). Frontmatter `tools: WebSearch, WebFetch, Read, Write`.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: research agents and research templates`.

---

### Task 6: Draft and critique agents (Stages 2–3, Quick Modeller)

**Files:**
- Create: `skills/before-you-build/templates/{strategy_report,assessment}.md`; `agents/byb-{quick-modeller,strategist,draft-modeller,sceptical-investor,investment-banker}.md`; `tests/test_agents_critique.py`

**Interfaces:**
- Consumes: `lint_agent` (Task 5), references (Task 3), `scripts/scorecard.py` CLI (Task 2).
- Produces: the Strategist keeps working notes in `20_draft/strategist_notes.md`; critics write `30_assessment/scorecard_inputs.json` and `30_assessment/scorecard_result.json` (result is the engine's stdout, unedited).

- [ ] **Step 1: Write the failing tests:**
  - `lint_agent` for each of the five with spec §5 paths. Quick Modeller must mention `Defensive`, `Moderate`, `Optimistic`, `break-even`. Draft Modeller writes `20_draft/model_v1.csv`.
  - `test_strategist_ambitious_but_labelled`: Strategist `## Rules` contains "strongest honest case" and writes `20_draft/strategist_notes.md`.
  - `test_firewall`: Sceptical Investor and Investment Banker `## Rules` each contain "Never read `20_draft/strategist_notes.md`" and "recompute".
  - `test_sceptic_uses_engine`: Sceptical Investor mentions `references/questions.md`, `scorecard_inputs.json`, `scripts/scorecard.py` and "pre-mortem" and "risk register"; it has a `## Re-check mode` section for Stage 4b writing `30_assessment/sceptic_recheck.md`.
  - `test_banker_scope`: Investment Banker mentions `valuation`, `dilution`, `option pool`, `use of funds`, `comparable`, `exit`, `due diligence`.
  - `test_assessment_template`: contains `## The ten questions`, `## Missing costs`, `## Pre-mortem`, `## Risk register`, `## Scorecard`, and the `DISCLAIMER`; `strategy_report.md` contains `## Capital ask` and the `DISCLAIMER`.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_agents_critique -v` → FAIL.
- [ ] **Step 3: Write the two templates and five agents.** Critics' tools: `WebSearch, WebFetch, Read, Write, Bash` (Bash only to run the scorecard). In Path B the critics treat `20_draft/uploaded_report.*` as the draft.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: strategist, modellers and critic agents`.

---

### Task 7: Rebuild and decision agents (Stages 4–5) and output templates

**Files:**
- Create: `skills/before-you-build/templates/{decision_pack,decision_memo,full_plan,test_plan}.md`, `skills/before-you-build/templates/gate_tracker.csv`; `agents/byb-{business-model-designer,operations-product-planner,financial-modeller,validation-test-designer,report-writer}.md`; `tests/test_agents_decision.py`

**Interfaces:**
- Consumes: `lint_agent`, scorecard result file (Task 6).
- Produces: `gate_tracker.csv` header exactly `measure,formula,pass_line,fail_line,measured_value,date_measured,status`.

- [ ] **Step 1: Write the failing tests:**
  - `lint_agent` for each of the five with spec §5 paths. Financial Modeller must mention `balance sheet`, `working capital`, `sensitivity`, `never`, and the three scenario names. Validation Test Designer must mention `pass`, `fail`, `formula`, `go/no-go`, `fallback`.
  - `test_report_writer_two_modes`: Report Writer has `## Quick Check` (writes `50_decision/decision_pack.md`) and `## Full Review` (writes `decision_memo.md`, `full_plan.md`) sections, and states the verdict comes from `30_assessment/scorecard_result.json` unchanged.
  - `test_output_templates`: each of the four Markdown templates contains the `DISCLAIMER`; `decision_pack.md` contains `## Verdict`, `## Readiness score`, `## Top 3 risks`, `## The test`; `decision_memo.md` contains `## Riskiest assumption` and `## Pre-mortem`.
  - `test_gate_tracker_header`: first line of `gate_tracker.csv` equals the header above.
  - `test_no_go_build`: no file under `agents/` or `skills/` contains "Go build" except inside the sentence "never \"Go build\"".
- [ ] **Step 2: Run** `python3 -m unittest tests.test_agents_decision -v` → FAIL.
- [ ] **Step 3: Write templates and agents.**
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** `feat: rebuild, test design and report agents`.

---

### Task 8: Run checker and the lead skill

**Files:**
- Create: `scripts/check_run.py`, `skills/before-you-build/SKILL.md`, `tests/test_check_run.py`, `tests/test_skill.py`

**Interfaces:**
- Consumes: every agent name and output path from Tasks 5–7.
- Produces:
  - `expected_files(mode: str, path: str, stage: int) -> list[str]` — `mode` in `{"quick","full"}`, `path` in `{"A","B"}` (ignored for quick), cumulative list of files required up to and including `stage` (Quick stages 0–4, Full stages 0–5; stage 4b counted inside 4).
  - `check(run_dir: Path, mode: str, path: str, stage: int) -> list[str]` — problems: missing files; any `50_decision/*.md` without the `DISCLAIMER`; `sources.md` missing once stage ≥ 1.
  - CLI: `python3 scripts/check_run.py <run_dir> --mode quick|full [--path A|B] --stage N` → prints `ok` and exits 0, or one problem per line and exits 1.

- [ ] **Step 1: Write the failing tests for `check_run.py`:**
  - `test_quick_stage_lists`: `expected_files("quick","A",1)` equals `["00_brief.md","10_research/market_competition.md","10_research/customer_demand.md","10_research/founder_fit.md","sources.md"]`.
  - `test_full_path_b_skips_draft`: Path B stage 2 list contains no `20_draft/strategy_report.md`; Path A stage 2 contains it and `20_draft/model_v1.csv`.
  - `test_check_reports_missing_and_disclaimer`: temp run dir with stage-4 Quick files where `decision_pack.md` lacks the disclaimer → problems name that file; add it → `[]`.
  - `test_cli_exit_codes`.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_check_run -v` → FAIL; implement `scripts/check_run.py`; run → PASS.
- [ ] **Step 3: Write the failing tests for `SKILL.md`:**
  - `test_skill_frontmatter`: `name: before-you-build`; description mentions "Quick Check" and "Full Review".
  - `test_skill_dispatches_every_agent`: every `agents/byb-*.md` stem appears in `SKILL.md`.
  - `test_intake_topics`: the 8 intake topics and the 8 region names appear; the Quick Check founder short form is stated.
  - `test_parallel_and_checks`: contains "in parallel" for Stage 1, 3 and 4 of Full Review, and `scripts/check_run.py` after every stage.
  - `test_playback_before_dispatch`: the phrase "read the brief back" appears before the first "Stage 1".
  - `test_review_focus_rules`: contains rules for an unreadable uploaded report ("paste the text"), a region outside the eight packs ("closest pack"), and an existing run folder ("-2").
  - `test_upgrade_path`: describes upgrading Quick Check to Full Review reusing `10_research/`.
- [ ] **Step 4: Run** `python3 -m unittest tests.test_skill -v` → FAIL.
- [ ] **Step 5: Write `SKILL.md`:** intake one topic at a time (spec §4); slug and run folder; read the brief back and wait for confirmation; mode-specific stage list with which agents run in parallel (one message with several Agent calls) and which wait; Path A/B; after each stage run `check_run.py` and re-dispatch only the agent whose file is missing (once), else tell the founder what failed; build `scorecard_inputs.json` only through the Sceptical Investor; finish with a short chat summary (verdict, score, confidence, the test, file paths) and the disclaimer.
- [ ] **Step 6: Run** the full suite `python3 -m unittest discover -s tests -v` → all PASS.
- [ ] **Step 7: Commit** `feat: lead skill and run checker`.

---

### Task 9: README and contributor notes

**Files:**
- Modify: `README.md`
- Create: `CLAUDE.md`, `tests/test_readme.py`

- [ ] **Step 1: Write the failing tests:** README contains the tagline, `## Install` with `/plugin marketplace add elakarborobhai21/before-you-build` and `/plugin install before-you-build@before-you-build`, `## How it works` naming both modes and both paths, `## What you get`, `## Limits`, the `DISCLAIMER`, `## Acknowledgements` naming `idea-validation-agents`, `Max Kmet`, `agency-agents`, `msitarzewski`, and "Built with Claude", and `v0.1`. `CLAUDE.md` names the test command and the Global Constraints.
- [ ] **Step 2: Run** `python3 -m unittest tests.test_readme -v` → FAIL.
- [ ] **Step 3: Write both files.** README links the flow diagram as Mermaid (Quick and Full), plain language, no hype.
- [ ] **Step 4: Run** → PASS; run the full suite → PASS.
- [ ] **Step 5: Commit** `docs: README and contributor notes`.

---

### Task 10: Fictional worked example (Lagos)

**Files:**
- Create: `examples/lagos-delivery-quick-check/` (the full run folder), `examples/README.md`

- [ ] **Step 1: Run a real Quick Check** in this session by following `SKILL.md` exactly, with this fictional brief: *a same-day parcel delivery app for small online sellers on Lagos Island and the Lekki axis; two fictional founders (an ex-logistics operations lead, full-time from month 1; a part-time developer with no employer conflict); NGN 18 million founder cash; Sub-Saharan Africa pack.* Write output to `~/before-you-build-runs/` then copy into `examples/lagos-delivery-quick-check/`.
- [ ] **Step 2: Verify the run:** `python3 scripts/check_run.py examples/lagos-delivery-quick-check --mode quick --stage 4` → `ok`.
- [ ] **Step 3: Check every link** in `sources.md` and the Markdown files with a short throwaway script (HTTP status < 400, following redirects). Remove or replace any claim whose link fails. Expected: zero failing links.
- [ ] **Step 4: Read the decision pack end to end** for invented facts, hype words, and anything resembling the author's own earlier case. Fix and re-run the checker.
- [ ] **Step 5: Commit** `docs: fictional Lagos Quick Check example`.

---

### Task 11: Pre-release testing (spec §12), not committed

- [ ] **Step 1:** Run Quick Check on four more fictional ideas (Jakarta B2B SaaS, São Paulo food brand, Riyadh services marketplace, Toronto consumer subscription) and one Full Review Path A (Jakarta). Keep outputs outside the repo.
- [ ] **Step 2:** For each run, record in a scratch log: check_run result, dead links, any invented figures, any verdict that the scorecard rules did not produce. Fix agent or skill text for each class of problem; add a test when the problem is structural. Re-run the suite → PASS.
- [ ] **Step 3: Private comparison:** with the author's permission, an optional private comparison against the author's own earlier case, never published. It runs outside the repo, and nothing from it is committed.
- [ ] **Step 4: Commit** only the fixes from Step 2 (`fix: issues found in pre-release runs`), and tag `v0.1.0`.

Beta testing with 3–5 founders and making the repository public are the author's steps after this plan.
