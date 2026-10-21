#!/usr/bin/env python3
"""Build an interactive HTML report from a finished Before You Build run folder.

Usage: python3 scripts/render_report.py <run_dir>
Reads the decision pack (Quick Check) or the decision memo and test plan (Full
Review), the scorecard files, 20_model/model_inputs.json when the run has it
(see scripts/model.py) and sources.md, and writes
<run_dir>/50_decision/report.html. The page is one self-contained file: no
external scripts, fonts or images, so it opens offline and sends nothing
anywhere. It only shows what the run files say. Prints the path and exits 0;
exits 2 with a message on stderr when a required file is missing.
Standard library only.
"""
import csv
import html
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model  # noqa: E402

DISCLAIMER = (
    "This report was produced by AI agents using publicly available information "
    "and the details you provided. Figures may be incomplete, out of date or wrong; "
    "each is marked sourced, estimated or assumed. It is not financial, legal, tax "
    "or investment advice. Check important figures yourself and talk to real "
    "customers before acting."
)
AREAS = [
    ("customer_pull", "Customer pull"),
    ("route_to_customers", "Route to customers"),
    ("money_per_transaction", "Money per transaction"),
    ("cash_to_proof", "Cash to proof"),
    ("competitive_response", "Competitive response"),
    ("team_commitment", "Team and commitment"),
    ("rules_operations", "Rules and operations"),
]
RATING_WORDS = {0: "Fatal", 1: "Weak", 2: "Adequate", 3: "Strong"}
SCENARIOS = ["Defensive", "Moderate", "Optimistic"]
VERDICT_CLASS = {"Go to test": "go", "Pivot": "pivot", "Stop": "stop"}
# Test-section keys that get their own colour.
KEY_CLASS = {"pass line": "pass", "fail line": "fail", "channel measure": "channel",
             "decide by": "date", "go/no-go": "date"}
# Sections taken from test_plan.md into a Full Review report.
TEST_PLAN_SECTIONS = ["Measures, pass and fail lines", "Channel measure", "Fallback pivots"]


class RenderError(Exception):
    pass


# ---------- Markdown subset ----------

INLINE = re.compile(
    r"`(?P<code>[^`]+)`"
    r"|\[(?P<lab>[SEA])\](?:\((?P<laburl>[^)\s]+)\))?"
    r"|\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)\)"
    r"|\*\*(?P<bold>.+?)\*\*"
)


def safe_url(url: str):
    return url if re.match(r"https?://", url, re.I) else None


def inline(raw: str) -> str:
    """Escape text and render code, links, bold and evidence labels."""
    out, pos = [], 0
    for m in INLINE.finditer(raw):
        out.append(html.escape(raw[pos:m.start()]))
        pos = m.end()
        if m.group("code") is not None:
            out.append(f"<code>{html.escape(m.group('code'))}</code>")
        elif m.group("lab") is not None:
            lab = m.group("lab")
            name = {"S": "sourced", "E": "estimated", "A": "assumed"}[lab]
            url = safe_url(m.group("laburl") or "")
            if url:
                out.append(f'<a class="lab {lab.lower()}" href="{html.escape(url)}" '
                           f'title="{name}: open source" target="_blank" rel="noopener">{lab}</a>')
            else:
                out.append(f'<span class="lab {lab.lower()}" title="{name}">{lab}</span>')
                if m.group("laburl"):
                    out.append(html.escape(f"({m.group('laburl')})"))
        elif m.group("url") is not None:
            url = safe_url(m.group("url"))
            text = inline(m.group("text"))
            out.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{text}</a>'
                       if url else text)
        else:
            out.append(f"<strong>{inline(m.group('bold'))}</strong>")
    out.append(html.escape(raw[pos:]))
    return "".join(out)


def split_row(line: str) -> list:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_table_rule(line: str) -> bool:
    return bool(re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$", line.strip()))


def table_html(rows: list) -> str:
    head, body = rows[0], rows[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def blocks(md: str) -> list:
    """Split Markdown into blocks: ('p'|'ul'|'ol'|'table'|'quote'|'h3'|'hr', data)."""
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
        elif s.startswith("### ") or s.startswith("#### "):
            out.append(("h3", s.lstrip("#").strip()))
            i += 1
        elif re.match(r"^-{3,}$", s):
            out.append(("hr", None))
            i += 1
        elif s.startswith("|") and i + 1 < len(lines) and is_table_rule(lines[i + 1]):
            rows = [split_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(("table", rows))
        elif s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(("quote", " ".join(quote)))
        elif re.match(r"^(-|\*|\d+\.)\s", s):
            kind = "ol" if re.match(r"^\d+\.", s) else "ul"
            items = []
            while i < len(lines):
                cur = lines[i]
                cs = cur.strip()
                if not cs:
                    break
                indent = len(cur) - len(cur.lstrip())
                m = re.match(r"^(-|\*|\d+\.)\s+(.*)$", cs)
                if m and indent < 2:
                    items.append([m.group(2), []])
                elif m and items:
                    items[-1][1].append(m.group(2))
                elif items:
                    if items[-1][1]:
                        items[-1][1][-1] += " " + cs
                    else:
                        items[-1][0] += " " + cs
                else:
                    break
                i += 1
            out.append((kind, items))
        else:
            para = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(\||>|#|-{3,}$|(-|\*|\d+\.)\s)", lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
            out.append(("p", " ".join(para)))
    return out


def list_html(kind: str, items: list) -> str:
    lis = []
    for text, subs in items:
        sub = ("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in subs) + "</ul>") if subs else ""
        lis.append(f"<li>{inline(text)}{sub}</li>")
    return f"<{kind}>{''.join(lis)}</{kind}>"


def render_blocks(bl: list) -> str:
    parts = []
    for kind, data in bl:
        if kind == "p":
            parts.append(f"<p>{inline(data)}</p>")
        elif kind == "h3":
            parts.append(f"<h3>{inline(data)}</h3>")
        elif kind == "hr":
            continue
        elif kind == "table":
            parts.append(table_html(data))
        elif kind == "quote":
            if " ".join(data.split()) == DISCLAIMER:
                continue  # the footer carries the disclaimer once
            parts.append(f'<blockquote>{inline(data)}</blockquote>')
        else:
            parts.append(list_html(kind, data))
    return "\n".join(parts)


# ---------- Document structure ----------

def parse_doc(text: str) -> dict:
    """Title, header lines and ## sections of one run file."""
    title, header, sections, cur = "", [], [], None
    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            cur = [line[3:].strip(), []]
            sections.append(cur)
        elif cur is None:
            header.append(line)
        else:
            cur[1].append(line)
    return {"title": title, "header": header,
            "sections": [(name, "\n".join(body)) for name, body in sections]}


def header_meta(header: list) -> tuple:
    """Key: value lines become meta; other lines become intro text."""
    meta, intro = [], []
    for line in header:
        m = re.match(r"^([A-Z][A-Za-z ]{1,30}):\s+(.+)$", line.strip())
        if m and m.group(1) not in ("Labels",):
            meta.append((m.group(1), m.group(2)))
        elif line.strip() and not line.strip().startswith("Labels:"):
            intro.append(line)
    return meta, "\n".join(intro)


def slug(name: str, used: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "section"
    s, n = base, 2
    while s in used:
        s, n = f"{base}-{n}", n + 1
    used.add(s)
    return s


def scenario_table(bl: list):
    """The first table block with Defensive, Moderate and Optimistic columns, if any."""
    for n, (kind, data) in enumerate(bl):
        if kind == "table":
            head = [c.replace("*", "") for c in data[0]]
            idx = {}
            for sc in SCENARIOS:
                for j, c in enumerate(head):
                    if c.strip().lower() == sc.lower():
                        idx[sc] = j
            if len(idx) == 3:
                extra = [j for j in range(1, len(head)) if j not in idx.values()]
                return n, (head, data[1:], idx, extra)
    return None, None


def scenario_html(found) -> str:
    head, rows, idx, extra = found
    buttons = "".join(
        f'<button type="button" class="sc-btn" data-sc="{sc}" '
        f'aria-pressed="{"true" if sc == "Moderate" else "false"}">{sc}</button>'
        for sc in SCENARIOS)
    tiles = []
    for r in rows:
        r = r + [""] * (len(head) - len(r))
        vals = "".join(
            f'<div class="sc-val" data-sc="{sc}"{"" if sc == "Moderate" else " hidden"}>'
            f'{inline(r[idx[sc]])}</div>' for sc in SCENARIOS)
        notes = "".join(
            f'<div class="sc-note"><span>{inline(head[j])}:</span> {inline(r[j])}</div>'
            for j in extra if r[j].strip() and r[j].strip().lower() != "same")
        tiles.append(f'<div class="tile"><div class="tk">{inline(r[0])}</div>{vals}{notes}</div>')
    return (f'<div class="sc-bar"><span class="sc-lbl">Scenario</span>'
            f'<div class="seg" role="group" aria-label="Scenario">{buttons}</div></div>'
            f'<div class="tiles">{"".join(tiles)}</div>')


KEYED = re.compile(r"^([A-Z][^:.]{1,90}):\s+(.*)$")


def test_html(md: str) -> str:
    """The test section, with its "Key: value" lists as rows and pass, fail and channel marked."""
    parts = []
    for kind, data in blocks(md):
        keyed = [KEYED.match(t) for t, _ in data] if kind == "ul" else []
        if keyed and sum(1 for m in keyed if m) * 2 >= len(keyed):
            rows = []
            for (text, subs), m in zip(data, keyed):
                sub = ("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in subs) + "</ul>"
                       ) if subs else ""
                if m:
                    key = m.group(1).strip()
                    cls = next((c for k, c in KEY_CLASS.items() if key.lower().startswith(k)), "")
                    rows.append(f'<div class="trow {cls}"><dt>{inline(key)}</dt>'
                                f'<dd>{inline(m.group(2).strip())}{sub}</dd></div>')
                else:
                    rows.append(f'<div class="trow wide"><dd>{inline(text)}{sub}</dd></div>')
            parts.append(f'<dl class="test">{"".join(rows)}</dl>')
        else:
            parts.append(render_blocks([(kind, data)]))
    return "\n".join(parts)


# ---------- Charts (inline SVG) ----------

def gauge_svg(score: int) -> str:
    score = max(0, min(100, int(score)))
    w = 600
    x = lambda v: v * w / 100  # noqa: E731
    return (
        f'<svg class="gauge" viewBox="0 -22 {w} 64" role="img" '
        f'aria-label="Readiness score {score} out of 100">'
        f'<rect x="0" y="0" width="{x(40)}" height="14" class="z-stop"/>'
        f'<rect x="{x(40)}" y="0" width="{x(25)}" height="14" class="z-pivot"/>'
        f'<rect x="{x(65)}" y="0" width="{x(35)}" height="14" class="z-go"/>'
        f'<line x1="{x(score)}" x2="{x(score)}" y1="-6" y2="20" class="mark"/>'
        f'<text x="{x(score)}" y="-11" text-anchor="middle" class="mark-t">{score}</text>'
        f'<text x="{x(20)}" y="36" text-anchor="middle">Stop · under 40</text>'
        f'<text x="{x(52.5)}" y="36" text-anchor="middle">Pivot · 40 to 64</text>'
        f'<text x="{x(82.5)}" y="36" text-anchor="middle">Go to test · 65+</text>'
        f'</svg>')


def ratings_svg(now: dict, before: dict = None) -> str:
    row, lw, bw = 34, 200, 360
    h = row * len(AREAS) + 26
    parts = [f'<svg class="ratings" viewBox="0 0 {lw + bw + 90} {h}" role="img" '
             f'aria-label="Ratings for the seven scorecard areas">']
    for k in range(4):
        gx = lw + k * bw / 3
        parts.append(f'<line x1="{gx}" x2="{gx}" y1="0" y2="{h - 22}" class="grid"/>'
                     f'<text x="{gx}" y="{h - 6}" text-anchor="middle">{RATING_WORDS[k]}</text>')
    for i, (key, name) in enumerate(AREAS):
        y = i * row + 6
        v = int(now.get(key, 0))
        cls = "r" + str(v)
        parts.append(f'<text x="{lw - 10}" y="{y + 15}" text-anchor="end" class="an">'
                     f'{html.escape(name)}</text>')
        width = max(v * bw / 3, 4)
        parts.append(f'<rect x="{lw}" y="{y + 3}" width="{width}" height="16" rx="3" class="{cls}">'
                     f'<title>{html.escape(name)}: {RATING_WORDS[v]} ({v} of 3)</title></rect>')
        parts.append(f'<text x="{lw + width + 8}" y="{y + 15}" class="rv">{RATING_WORDS[v]}</text>')
        if before is not None and key in before and int(before[key]) != v:
            bx = lw + int(before[key]) * bw / 3
            parts.append(f'<line x1="{bx}" x2="{bx}" y1="{y}" y2="{y + 22}" class="before">'
                         f'<title>At Stage 3: {RATING_WORDS[int(before[key])]}</title></line>')
    parts.append("</svg>")
    return "".join(parts)


def mix_html(counts: dict) -> str:
    s, e, a = (int(counts.get(k, 0)) for k in ("S", "E", "A"))
    total = s + e + a
    if not total:
        return ""
    seg = "".join(
        f'<span class="mx {c}" style="flex:{n}" title="{label}: {n}"></span>'
        for n, c, label in ((s, "s", "Sourced"), (e, "e", "Estimated"), (a, "a", "Assumed")) if n)
    return (f'<div class="mix"><div class="mixbar">{seg}</div><div class="mixkey">'
            f'<span><i class="s"></i>Sourced {s}</span><span><i class="e"></i>Estimated {e}</span>'
            f'<span><i class="a"></i>Assumed {a}</span><span class="muted">of {total} figures '
            f'behind areas 1 to 4</span></div></div>')


def figure(title: str, sub: str, inner: str, source: str = "") -> str:
    """A chart in the house style: red tag, bold title, subtitle with units, source line."""
    src = f'<figcaption>{source}</figcaption>' if source else ""
    return (f'<figure class="chart"><div class="ctitle">{html.escape(title)}</div>'
            f'<div class="csub">{sub}</div>{inner}{src}</figure>')


def num(v: float) -> str:
    return f"{v:,.0f}".replace("-", "−")


def waterfall_svg(unit: list, cur: str, tx: str = "transaction") -> str:
    """One transaction from the first revenue line down to the contribution."""
    row, lw, bw, top = 26, 250, 300, 6
    run, spans = 0.0, []
    for line in unit:
        spans.append((line["line"], run, run + line["value"], line["kind"]))
        run += line["value"]
    spans.append((f"Contribution per {tx}", 0.0, run, "total"))
    lo = min(0.0, *(min(a, b) for _, a, b, _ in spans))
    hi = max(0.0, *(max(a, b) for _, a, b, _ in spans))
    x = lambda v: lw + (v - lo) * bw / ((hi - lo) or 1)  # noqa: E731
    h = row * len(spans) + top + 4
    parts = [f'<svg class="wf" viewBox="0 0 {lw + bw + 80} {h}" role="img" '
             f'aria-label="Waterfall from revenue to contribution per transaction, {cur}">',
             f'<line x1="{x(0):.1f}" x2="{x(0):.1f}" y1="0" y2="{h}" class="zero"/>']
    for i, (name, a, b, kind) in enumerate(spans):
        y = top + i * row
        v = b - a
        cls = ("pos" if v >= 0 else "neg") if kind == "total" else ("rev" if v >= 0 else "cost")
        x0, x1 = x(min(a, b)), x(max(a, b))
        parts.append(f'<text x="{lw - 10}" y="{y + 15}" text-anchor="end" class="an'
                     f'{" tot" if kind == "total" else ""}">{html.escape(name)}</text>')
        parts.append(f'<rect x="{x0:.1f}" y="{y + 3}" width="{max(x1 - x0, 1.5):.1f}" height="17" '
                     f'class="{cls}"><title>{html.escape(name)}: {cur} {num(v)}</title></rect>')
        parts.append(f'<text x="{x1 + 6:.1f}" y="{y + 15}" class="wv{" tot" if kind == "total" else ""}">'
                     f'{"+" if v > 0 and kind != "total" else ""}{num(v)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def model_html(inputs: dict) -> str:
    """Three versions of the plan, recalculated in the page when the conversion rate changes."""
    cur = html.escape(str(inputs.get("currency", "")))
    tx = html.escape(str(inputs.get("transaction", "transaction")))
    cust = html.escape(str(inputs.get("customer", "customer")))
    data = json.dumps(inputs).replace("<", "\\u003c")
    buttons = "".join(
        f'<button type="button" class="sc-btn v-{sc.lower()}" data-sc="{sc}" '
        f'aria-pressed="{"true" if sc == "Moderate" else "false"}">{sc}</button>'
        for sc in SCENARIOS)
    keys = [("contribution", f"Each {tx} leaves"), ("breakeven", "Covers its costs"),
            ("test", "Cash for the 90-day test"), ("need", "Cash needed, 24 months"),
            ("runway", "Founder cash runs out"), ("customers", f"Paying {cust}s, month 24")]
    tiles = "".join(f'<div class="kpi"><div class="kk">{k}</div><div class="kv" data-k="{key}">–</div>'
                    f'<div class="ks" data-k="{key}-s"></div></div>' for key, k in keys)
    label = html.escape(str(inputs.get("conversion_label", "")))
    note = inline(str(inputs.get("conversion_note", "")))
    panels = []
    for sc in SCENARIOS:
        s = inputs["scenarios"][sc]
        pct = f'{s["conversion_rate"] * 100:g}'
        panels.append(
            f'<div class="ver" data-sc="{sc}"{"" if sc == "Moderate" else " hidden"}>'
            f'<div class="conv"><div><label for="conv-{sc}">Conversion rate, {sc}</label>'
            f'<p class="muted">{label}</p></div>'
            f'<div class="conv-in"><input id="conv-{sc}" class="conv-input" data-sc="{sc}" type="number" '
            f'min="0.1" max="100" step="0.1" value="{pct}" inputmode="decimal"><span>%</span>'
            f'<button type="button" class="reset" data-sc="{sc}" data-v="{pct}">Reset to {pct}%</button></div>'
            f'<p class="ctw">Cost to win one paying {cust}: <b data-k="ctw"></b> '
            f'<span class="edited" hidden>· your figure, not the run’s</span></p></div>'
            f'<div class="kpis">{tiles}</div>'
            + figure("Profit or loss each month", f"{cur}, months 1 to {inputs.get('months', 24)}. "
                     "Blue is a month that makes money, red a month that loses it.",
                     '<svg class="js-chart" data-chart="bars" role="img" aria-label="Monthly result"></svg>')
            + figure(f"What one {tx} earns", f"{cur} per {tx}, {sc} version. Blue lines add money, "
                     "red lines take it away. The conversion rate does not change this chart.",
                     waterfall_svg(s["unit"], cur, inputs.get("transaction", "transaction")), "Source: <code>20_model/model_inputs.json</code>")
            + '</div>')
    legend = "".join(f'<span><i class="v-{sc.lower()}"></i>{sc}</span>' for sc in SCENARIOS)
    return (
        f'<script type="application/json" id="model-data">{data}</script>'
        f'<p>Three versions of the same plan. <b>Defensive</b> takes the worse end of every range, '
        f'<b>Moderate</b> the honest middle and <b>Optimistic</b> the better end. Change a version’s '
        f'conversion rate and every chart and number in that version is worked out again.</p>'
        f'<p class="muted">Run’s range for the conversion rate: {note}</p>'
        + figure("Cash in the bank, three versions",
                 f"Cumulative result from month 1, {cur}. Below the dashed line the founder cash is gone.",
                 f'<div class="clegend">{legend}<span><i class="ref"></i>Founder cash used up</span></div>'
                 '<svg class="js-chart" data-chart="cash" role="img" aria-label="Cumulative cash, three versions"></svg>')
        + f'<div class="sc-bar"><span class="sc-lbl">Open a version</span>'
          f'<div class="seg" role="group" aria-label="Version">{buttons}</div></div>'
        + "".join(panels)
        + '<noscript><p class="muted">Turn on JavaScript to see the charts. The table below has the '
          'same figures as written.</p></noscript>'
        + '<p class="muted">The charts are worked out in your browser from <code>20_model/model_inputs.json</code> '
          'with the formulas in <code>scripts/model.py</code>. The written sections keep the figures the '
          'agents wrote at the run’s own conversion rates.</p>')


RISK_LEVEL = re.compile(r"Likelihood and impact are both (High|Medium|Low)"
                        r"|Likelihood (High|Medium|Low)\b[^.]*?\bimpact (High|Medium|Low)", re.I)


def risks_html(md: str) -> str:
    """The numbered risks as cards, with likelihood and impact pulled out as chips."""
    parts = []
    for kind, data in blocks(md):
        if kind != "ol":
            parts.append(render_blocks([(kind, data)]))
            continue
        cards = []
        for n, (text, subs) in enumerate(data, 1):
            m = RISK_LEVEL.search(text)
            chips = ""
            if m:
                lik, imp = (m.group(1), m.group(1)) if m.group(1) else (m.group(2), m.group(3))
                chips = "".join(f'<span class="lvl {v.lower()}">{k} {v.capitalize()}</span>'
                                for k, v in (("Likelihood", lik), ("Impact", imp)))
            sub = ("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in subs) + "</ul>") if subs else ""
            cards.append(f'<li class="risk"><div class="nbox">{n}</div><div><div class="chips">{chips}'
                         f'</div><p>{inline(text)}</p>{sub}</div></li>')
        parts.append(f'<ol class="risks">{"".join(cards)}</ol>')
    return "\n".join(parts)


DATED = re.compile(r"([A-Za-z][A-Za-z -]*?)[:\s]+(\d{4}-\d{2}-\d{2})")


def timeline_svg(md: str) -> str:
    """Dates named in the test, on one line. Empty when fewer than two dates are named."""
    seen = {}
    for clause in re.split(r"[,.;()]", md):
        m = DATED.search(clause)
        if not m:
            continue
        try:
            d = date.fromisoformat(m.group(2))
        except ValueError:
            continue
        words = m.group(1).strip(" -").split()[-3:]
        while words and words[-1].lower() in ("of", "on", "from", "the"):
            words.pop()
        if words and d not in seen:
            seen[d] = " ".join(words)[:1].upper() + " ".join(words)[1:]
    if len(seen) < 2:
        return ""
    days = sorted(seen)
    span = (days[-1] - days[0]).days or 1
    w, pad = 640, 70
    x = lambda d: pad + (d - days[0]).days * (w - 2 * pad) / span  # noqa: E731
    parts = [f'<svg class="tl" viewBox="0 0 {w} 120" role="img" aria-label="Test timeline">',
             f'<line x1="{pad}" x2="{w - pad}" y1="60" y2="60" class="axis"/>']
    for i, d in enumerate(days):
        up = i % 2 == 0
        parts.append(f'<circle cx="{x(d):.1f}" cy="60" r="5" class="dot"/>'
                     f'<line x1="{x(d):.1f}" x2="{x(d):.1f}" y1="{48 if up else 66}" y2="{54 if up else 72}" class="tick"/>'
                     f'<text x="{x(d):.1f}" y="{26 if up else 92}" text-anchor="middle" class="tlk">'
                     f'{html.escape(seen[d])}</text>'
                     f'<text x="{x(d):.1f}" y="{40 if up else 106}" text-anchor="middle">'
                     f'{d.day} {d.strftime("%b %Y")}</text>')
    parts.append("</svg>")
    return figure("The test, step by step", "Dates named in the test below.", "".join(parts))


# ---------- Page ----------

CSS = """
:root{--paper:#ffffff;--panel:#e9edf0;--surface:#ffffff;--ink:#0c0c0c;--ink-2:#3f5661;--ink-3:#758d99;
--line:#d9dee2;--line-2:#b7c6cf;--tag:#e3120b;--accent:#006ba2;--accent-soft:#e1edf5;
--go:#2e8577;--go-soft:#e1f1ee;--pivot:#8d6300;--pivot-soft:#fbf0d4;--stop:#c7303c;--stop-soft:#f9e1e1;
--s:#379a8b;--e:#006ba2;--a:#b07c00;--blue:#006ba2;--red:#db444b;--light:#5da4df;--dark:#a81829;
--def:#db444b;--mod:#006ba2;--opt:#3ebcd2;--r:4px;
--f-display:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
--f-chart:"Avenir Next Condensed","Roboto Condensed","Arial Narrow","Helvetica Neue",sans-serif;
--f-body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--f-mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#121518;--panel:#1c2328;--surface:#171c20;
--ink:#f2f4f5;--ink-2:#b7c6cf;--ink-3:#89a2ae;--line:#2b343a;--line-2:#3f4b52;--accent:#5da4df;--accent-soft:#16283a;
--go:#4dad9e;--go-soft:#14302b;--pivot:#ebb434;--pivot-soft:#33290d;--stop:#ff6b6c;--stop-soft:#3a1c1e;
--s:#4dad9e;--e:#5da4df;--a:#ebb434;--blue:#5da4df;--red:#ff6b6c;--light:#98daff;--dark:#ff8785;
--def:#ff6b6c;--mod:#5da4df;--opt:#4ec8de;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#121518;--panel:#1c2328;--surface:#171c20;--ink:#f2f4f5;--ink-2:#b7c6cf;
--ink-3:#89a2ae;--line:#2b343a;--line-2:#3f4b52;--accent:#5da4df;--accent-soft:#16283a;--go:#4dad9e;
--go-soft:#14302b;--pivot:#ebb434;--pivot-soft:#33290d;--stop:#ff6b6c;--stop-soft:#3a1c1e;--s:#4dad9e;
--e:#5da4df;--a:#ebb434;--blue:#5da4df;--red:#ff6b6c;--light:#98daff;--dark:#ff8785;--def:#ff6b6c;
--mod:#5da4df;--opt:#4ec8de;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15.5px/1.6 var(--f-body)}
a{color:var(--accent)}
.shell{display:grid;grid-template-columns:220px minmax(0,1fr);gap:44px;max-width:1180px;margin:0 auto;padding:0 24px 80px}
.rail{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:28px 0}
.rail .brand{font:700 16px/1.25 var(--f-display);border-top:6px solid var(--tag);padding-top:10px}
.rail .brand small{display:block;font:400 11.5px var(--f-body);color:var(--ink-3);letter-spacing:.06em;text-transform:uppercase;margin-top:4px}
.rail ol{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:1px}
.rail a{display:block;padding:5px 8px;border-left:3px solid transparent;text-decoration:none;color:var(--ink-2);font-size:13.5px;line-height:1.35}
.rail a:hover,.rail a.on{background:var(--panel);border-left-color:var(--tag);color:var(--ink)}
.mnav{display:none}
main{min-width:0;padding-top:28px}
.hero .eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--tag);font-weight:700}
.hero h1{font:700 clamp(30px,4.6vw,46px)/1.06 var(--f-display);letter-spacing:-.02em;margin:10px 0 12px;max-width:22ch;text-wrap:balance}
.meta{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:13px;color:var(--ink-3)}
.meta b{font-weight:500;color:var(--ink-2)}
.intro{color:var(--ink-2);max-width:70ch}
.verdict{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:18px;margin:26px 0 6px}
.vcard{border-radius:var(--r);padding:20px 22px;background:var(--panel);border-top:6px solid var(--line-2)}
.vcard .k{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.vword{font:700 clamp(34px,5vw,46px)/1.05 var(--f-display);margin:6px 0 8px}
.vcard.go{background:var(--go-soft);border-top-color:var(--go)}.vcard.go .vword{color:var(--go)}
.vcard.pivot{background:var(--pivot-soft);border-top-color:var(--pivot)}.vcard.pivot .vword{color:var(--pivot)}
.vcard.stop{background:var(--stop-soft);border-top-color:var(--stop)}.vcard.stop .vword{color:var(--stop)}
.vcard ul{margin:8px 0 0;padding-left:18px;font-size:14px}
.score{display:flex;align-items:baseline;gap:10px}
.score .n{font:700 44px/1 var(--f-display)}
.chip{display:inline-block;font-size:12px;padding:2px 10px;border-radius:999px;border:1px solid var(--line-2);color:var(--ink-2)}
svg{display:block;width:100%;height:auto;overflow:visible}
svg text{fill:var(--ink-2);font:13px var(--f-chart)}
.gauge{margin-top:22px}.gauge text{font-size:15px}
.gauge .z-stop{fill:color-mix(in srgb,var(--stop) 22%,transparent)}.gauge .z-pivot{fill:color-mix(in srgb,var(--pivot) 22%,transparent)}.gauge .z-go{fill:color-mix(in srgb,var(--go) 22%,transparent)}
.gauge .mark{stroke:var(--ink);stroke-width:3}.gauge .mark-t{fill:var(--ink);font-weight:700;font-size:17px}
.ratings .grid{stroke:var(--line)}.ratings .an{fill:var(--ink);font-size:14px}.ratings .rv{fill:var(--ink-2);font-size:13px}
.ratings .r0{fill:var(--dark)}.ratings .r1{fill:var(--red)}.ratings .r2{fill:var(--light)}.ratings .r3{fill:var(--blue)}
.ratings .before{stroke:var(--ink);stroke-width:2;stroke-dasharray:3 3}
section{padding:36px 0 4px;margin-top:30px;scroll-margin-top:16px}
h2{font:700 clamp(22px,2.8vw,28px)/1.2 var(--f-display);letter-spacing:-.012em;margin:0 0 12px}
h2::before{content:"";display:block;width:44px;height:7px;background:var(--tag);margin-bottom:12px}
h3{font:700 17px var(--f-display);margin:22px 0 6px}
p,li{max-width:74ch}
.muted{color:var(--ink-3);font-size:13px}
.box{background:var(--surface);border-top:1px solid var(--ink);padding:14px 0;margin:12px 0}
.tw{overflow-x:auto;border-top:1px solid var(--ink);background:var(--surface);margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;font-size:12.5px;color:var(--ink-2)}
tbody tr:nth-child(odd) td{background:color-mix(in srgb,var(--panel) 55%,transparent)}
blockquote{margin:12px 0;padding:10px 16px;border-left:3px solid var(--line-2);color:var(--ink-2)}
code{font:13px var(--f-mono);background:var(--panel);padding:1px 5px;border-radius:3px}
.lab{display:inline-block;font:700 10.5px/1 var(--f-mono);padding:3px 5px;border-radius:3px;margin:0 2px;vertical-align:1px;text-decoration:none;color:#fff}
.lab.s{background:var(--s)}.lab.e{background:var(--e)}.lab.a{background:var(--a)}
a.lab.s:hover{outline:2px solid var(--s);outline-offset:1px}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--ink-2);margin-top:12px}
.mix{margin:14px 0}.mixbar{display:flex;height:12px;overflow:hidden;gap:2px}
.mx.s,.mixkey i.s{background:var(--s)}.mx.e,.mixkey i.e{background:var(--e)}.mx.a,.mixkey i.a{background:var(--a)}
.mixkey{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12.5px;color:var(--ink-2);margin-top:8px}
.mixkey i{display:inline-block;width:10px;height:10px;margin-right:6px;vertical-align:-1px}
.chart{margin:22px 0;padding:0}
.chart::before{content:"";display:block;width:32px;height:6px;background:var(--tag);margin-bottom:8px}
.ctitle{font:700 17px/1.25 var(--f-display)}
.csub{font-size:13.5px;color:var(--ink-2);margin:2px 0 10px}
.chart figcaption{font-size:12px;color:var(--ink-3);margin-top:6px}
.clegend{display:flex;flex-wrap:wrap;gap:4px 16px;font:13px var(--f-chart);color:var(--ink-2);margin-bottom:6px}
.clegend i{display:inline-block;width:14px;height:4px;margin-right:6px;vertical-align:3px}
.clegend i.v-defensive{background:var(--def)}.clegend i.v-moderate{background:var(--mod)}.clegend i.v-optimistic{background:var(--opt)}
.clegend i.ref{background:none;border-top:2px dashed var(--ink-2);height:0}
.js-chart .grid{stroke:var(--line)}.js-chart .zero,.wf .zero{stroke:var(--ink);stroke-width:1.2}
.js-chart .ln{fill:none;stroke-width:2.6;stroke-linejoin:round}
.js-chart .ln.v-defensive{stroke:var(--def)}.js-chart .ln.v-moderate{stroke:var(--mod)}.js-chart .ln.v-optimistic{stroke:var(--opt)}
.js-chart .ln.dim{opacity:.35}
.js-chart .refl{stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:5 4}
.js-chart .pos,.wf .pos,.wf .rev{fill:var(--blue)}.js-chart .neg,.wf .neg,.wf .cost{fill:var(--red)}
.js-chart .endl{font-weight:700}.js-chart .endl.v-defensive{fill:var(--def)}.js-chart .endl.v-moderate{fill:var(--mod)}.js-chart .endl.v-optimistic{fill:var(--opt)}
.wf .an{fill:var(--ink);font-size:13.5px}.wf .tot{font-weight:700}.wf .wv{font-size:13px}
.sc-bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin:18px 0 12px}
.sc-lbl{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.seg{display:inline-flex;border-bottom:2px solid var(--line);gap:4px}
.seg button{font:600 15px var(--f-display);border:0;background:transparent;color:var(--ink-2);padding:8px 14px;cursor:pointer;border-bottom:4px solid transparent;margin-bottom:-2px}
.seg button[aria-pressed="true"]{color:var(--ink)}
.seg button.v-defensive[aria-pressed="true"]{border-bottom-color:var(--def)}.seg button.v-moderate[aria-pressed="true"]{border-bottom-color:var(--mod)}.seg button.v-optimistic[aria-pressed="true"]{border-bottom-color:var(--opt)}
.seg button:not(.v-defensive):not(.v-moderate):not(.v-optimistic)[aria-pressed="true"]{border-bottom-color:var(--ink)}
.seg button:focus-visible,.rail a:focus-visible,.conv input:focus-visible,.reset:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.conv{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 24px;align-items:center;background:var(--panel);padding:16px 18px;border-left:6px solid var(--tag);margin:6px 0 16px}
.conv label{font:700 16px var(--f-display)}.conv p{margin:2px 0 0}
.conv-in{display:flex;align-items:center;gap:8px}
.conv-in input{font:700 28px/1 var(--f-display);width:4.6em;padding:6px 8px;border:2px solid var(--ink-2);border-radius:var(--r);background:var(--surface);color:var(--ink);text-align:right}
.conv-in span{font:700 24px var(--f-display);color:var(--ink-2)}
.reset{font:inherit;font-size:13px;border:1px solid var(--line-2);background:var(--surface);color:var(--ink-2);padding:6px 10px;border-radius:var(--r);cursor:pointer}
.ctw{grid-column:1/-1;font-size:14px;color:var(--ink-2)}.ctw b{color:var(--ink)}
.edited{color:var(--tag)}
.kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border-top:2px solid var(--ink);margin:6px 0 4px}
.kpi{background:var(--surface);padding:14px 14px 12px;min-width:0}
.kk{font-size:13px;color:var(--ink-3);line-height:1.3}
.kv{font:700 28px/1.15 var(--f-display);margin-top:6px;letter-spacing:-.01em;overflow-wrap:anywhere}
.kv.bad{color:var(--red)}.kv.good{color:var(--blue)}
.ks{font-size:12.5px;color:var(--ink-3);margin-top:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:10px 0 4px}
.tile{background:var(--panel);padding:14px 16px;min-width:0}
.tile .tk{font-size:12.5px;color:var(--ink-3);line-height:1.4}
.sc-val{font:700 19px/1.3 var(--f-display);margin-top:6px;overflow-wrap:anywhere}
.sc-note{font-size:12.5px;color:var(--ink-2);margin-top:8px;border-top:1px dashed var(--line-2);padding-top:6px}
.sc-note span{color:var(--ink-3)}
details{margin:10px 0}summary{cursor:pointer;color:var(--ink-2);font-size:14px}
ol.risks{list-style:none;padding:0;margin:14px 0;display:grid;gap:12px}
.risk{display:grid;grid-template-columns:52px minmax(0,1fr);gap:16px;background:var(--panel);padding:16px 18px 6px}
.risk p{margin:6px 0 10px}
.nbox{font:700 30px/52px var(--f-display);text-align:center;background:var(--line-2);color:var(--surface);height:52px}
.risk:first-child .nbox{background:var(--tag);color:#fff}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.lvl{font-size:12px;font-weight:600;padding:2px 9px;border-radius:999px;background:var(--surface);color:var(--ink-2);border:1px solid var(--line-2)}
.lvl.high{background:var(--red);border-color:var(--red);color:#fff}.lvl.medium{background:var(--pivot-soft);border-color:var(--pivot);color:var(--pivot)}
.tl .axis{stroke:var(--ink);stroke-width:2}.tl .dot{fill:var(--tag)}.tl .tick{stroke:var(--ink-2)}.tl .tlk{fill:var(--ink);font-weight:700;font-size:14px}
dl.test{display:grid;gap:8px;margin:14px 0}
.trow{display:grid;grid-template-columns:170px minmax(0,1fr);gap:16px;background:var(--surface);border-bottom:1px solid var(--line);border-left:6px solid var(--line-2);padding:12px 16px}
.trow dt{font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3);padding-top:2px;font-weight:600}
.trow dd{margin:0}.trow dd ul{margin:6px 0 0;padding-left:18px}
.trow.pass{border-left-color:var(--go);background:var(--go-soft)}.trow.fail{border-left-color:var(--stop);background:var(--stop-soft)}
.trow.channel{border-left-color:var(--e);background:var(--accent-soft)}
.trow.date{border-left-color:var(--ink)}.trow.wide{grid-template-columns:minmax(0,1fr)}
.disclaimer{margin-top:40px;padding:16px 18px;background:var(--panel);color:var(--ink-2);font-size:14px}
.foot{font-size:12.5px;color:var(--ink-3);margin-top:12px}
@media (max-width:900px){.shell{grid-template-columns:minmax(0,1fr);gap:0;padding:0 16px 60px}.rail{display:none}
.mnav{display:block;margin:16px 0 0}.mnav select{font:inherit;width:100%;padding:8px 10px;border-radius:var(--r);border:1px solid var(--line-2);background:var(--surface);color:var(--ink)}
.verdict{grid-template-columns:minmax(0,1fr)}.trow{grid-template-columns:minmax(0,1fr);gap:2px}
.conv{grid-template-columns:minmax(0,1fr)}.risk{grid-template-columns:40px minmax(0,1fr);gap:12px}.nbox{font-size:22px;line-height:40px;height:40px}
.kv{font-size:23px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media print{.rail,.mnav,.sc-bar,.reset{display:none}.shell{display:block}.sc-val[hidden],.ver[hidden]{display:block!important}
.sc-val::before{content:attr(data-sc) ": ";font-weight:400;color:var(--ink-3);font-size:12px}section{break-inside:avoid-page}}
"""

# The same formulas as calc() in model.py; tests/test_model.py checks they agree.
MODEL_JS = """
function calc(sc,months,cash,conv){
  if(conv==null)conv=sc.conversion_rate;
  var revenue=0,contribution=0;
  sc.unit.forEach(function(l){contribution+=l.value;if(l.kind==='revenue')revenue+=l.value});
  var active=0,cum=0,rows=[],be=null,out=null;
  for(var t=1;t<=months;t++){
    var leads=sc.leads_month_1*Math.pow(1+sc.lead_growth,t-1),nw=leads*conv,kept=active*(1-sc.churn);
    active=kept+nw;
    var tx=(kept+sc.first_month_share*nw)*sc.transactions_per_customer_month,acq=leads*sc.cost_per_lead,fixed=0,once=0;
    (sc.fixed_costs||[]).forEach(function(l){if((l.from||1)<=t&&t<=(l.to||months))fixed+=l.monthly});
    (sc.scaling_costs||[]).forEach(function(l){fixed+=Math.max(l.min||0,Math.ceil(tx/l.per_transactions))*l.monthly});
    (sc.one_time||[]).forEach(function(l){if((l.month||1)===t)once+=l.amount});
    var margin=tx*contribution,result=margin-acq-fixed-once;
    cum+=result;
    if(be===null&&margin>=acq+fixed)be=t;
    if(out===null&&cum<-cash)out=t;
    rows.push({month:t,new_customers:nw,active_customers:active,transactions:tx,revenue:tx*revenue,
      variable_cost:tx*(revenue-contribution),acquisition:acq,fixed:fixed+once,result:result,cumulative:cum});
  }
  var low=Math.min.apply(null,rows.map(function(r){return r.cumulative}));
  var low3=Math.min.apply(null,rows.slice(0,3).map(function(r){return r.cumulative}));
  return {conversion_rate:conv,cost_to_win_customer:sc.cost_per_lead/conv,revenue_per_transaction:revenue,
    contribution_per_transaction:contribution,break_even_month:be,cash_for_90_day_test:Math.max(0,-low3),
    cash_need:Math.max(0,-low),still_falling:rows[rows.length-1].cumulative<=low,cash_runs_out_month:out,months:rows};
}
"""

JS = """
(function(){
  var vers=document.querySelectorAll('.ver');
  var btns=document.querySelectorAll('.sc-btn');
  function show(sc){
    btns.forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-sc')===sc?'true':'false')});
    document.querySelectorAll('.sc-val,.ver').forEach(function(v){v.hidden=v.getAttribute('data-sc')!==sc});
    if(window.__drawModel)window.__drawModel(sc);
  }
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.getAttribute('data-sc'))})});
  var sel=document.getElementById('mnavSel');
  if(sel){sel.addEventListener('change',function(){var t=document.getElementById(sel.value);if(t)t.scrollIntoView()})}
  var links=document.querySelectorAll('.rail a');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)})}})},
      {rootMargin:'-20% 0px -70% 0px'});
    document.querySelectorAll('main section').forEach(function(s){io.observe(s)});
  }
  var el=document.getElementById('model-data');
  if(!el||!vers.length)return;
  var M=JSON.parse(el.textContent),SC=['Defensive','Moderate','Optimistic'],N=M.months||24,CUR=M.currency||'';
  var conv={},open='Moderate';
  SC.forEach(function(s){conv[s]=M.scenarios[s].conversion_rate});
  var MINUS='\\u2212';
  function unit(a){return a>=1e9?[1e9,'bn']:a>=1e6?[1e6,'m']:a>=1e3?[1e3,'k']:[1,'']}
  function short(v,u){var x=v/u[0],d=Math.abs(x)>=100||u[0]===1?0:1;
    return (x<0?MINUS:'')+Math.abs(x).toFixed(d).replace(/\\.0$/,'')+u[1]}
  function money(v,cur){var u=unit(Math.abs(v));return (v<0?MINUS:'')+(cur||CUR)+' '+short(Math.abs(v),u)}
  function usd(v){return M.usd_rate&&CUR!=='USD'?'USD '+short(v/M.usd_rate,unit(Math.abs(v/M.usd_rate))):''}
  function whole(v){return (v<0?MINUS:'')+Math.round(Math.abs(v)).toLocaleString('en-US')}
  function nice(x){var e=Math.pow(10,Math.floor(Math.log10(x))),f=x/e;return (f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10)*e}
  function frame(svg,vals,bars){
    var W=640,H=260,L=6,R=54,T=12,B=26;
    var lo=Math.min.apply(null,[0].concat(vals)),hi=Math.max.apply(null,[0].concat(vals));
    if(hi===lo)hi=lo+1;
    var st=nice((hi-lo)/5);lo=Math.floor(lo/st)*st;hi=Math.ceil(hi/st)*st;
    var u=unit(Math.max(Math.abs(lo),Math.abs(hi))),p=[];
    var y=function(v){return T+(hi-v)*(H-T-B)/(hi-lo)};
    var x=bars?function(i){return L+(i+0.5)*(W-L-R)/N}:function(i){return L+i*(W-L-R)/(N-1)};
    for(var v=lo;v<=hi+st/2;v+=st){
      p.push('<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y(v)+'" y2="'+y(v)+'" class="'+(Math.abs(v)<st/2?'zero':'grid')+'"/>');
      p.push('<text x="'+(W-R+8)+'" y="'+(y(v)+4)+'">'+short(v,u)+'</text>');
    }
    [1,6,12,18,N].forEach(function(m){if(m<=N)p.push('<text x="'+x(m-1)+'" y="'+(H-6)+'" text-anchor="middle">'+(m===1?'Month 1':m)+'</text>')});
    svg.setAttribute('viewBox','0 0 '+W+' '+H);
    return {p:p,x:x,y:y,W:W,R:R,L:L,u:u};
  }
  function drawCash(svg){
    var res={},vals=[-M.founder_cash];
    SC.forEach(function(s){res[s]=calc(M.scenarios[s],N,M.founder_cash,conv[s]);
      res[s].months.forEach(function(r){vals.push(r.cumulative)})});
    var f=frame(svg,vals,false),p=f.p,ry=f.y(-M.founder_cash),ends=[];
    p.push('<line x1="'+f.L+'" x2="'+(f.W-f.R)+'" y1="'+ry+'" y2="'+ry+'" class="refl"/>');
    p.push('<text x="'+(f.L+4)+'" y="'+(ry+16)+'">Founder cash '+money(M.founder_cash)+' used up</text>');
    SC.forEach(function(s){
      var d=res[s].months.map(function(r,i){return (i?'L':'M')+f.x(i).toFixed(1)+' '+f.y(r.cumulative).toFixed(1)}).join('');
      p.push('<path d="'+d+'" class="ln v-'+s.toLowerCase()+(s===open?'':' dim')+'"><title>'+s+'</title></path>');
      ends.push([f.y(res[s].months[N-1].cumulative),s]);
    });
    ends.sort(function(a,b){return a[0]-b[0]});
    for(var i=1;i<ends.length;i++)if(ends[i][0]-ends[i-1][0]<15)ends[i][0]=ends[i-1][0]+15;
    ends.forEach(function(e){var v=res[e[1]].months[N-1].cumulative;
      p.push('<text x="'+(f.W-f.R-4)+'" y="'+(e[0]-6).toFixed(1)+'" text-anchor="end" class="endl v-'+e[1].toLowerCase()+'">'+
        e[1]+' '+short(v,unit(Math.abs(v)))+'</text>')});
    svg.innerHTML=p.join('');
  }
  function drawBars(svg,r){
    var f=frame(svg,r.months.map(function(m){return m.result}),true),p=f.p,w=(f.W-f.L-f.R)/N*0.72;
    r.months.forEach(function(m,i){
      var y0=f.y(0),y1=f.y(m.result);
      p.push('<rect x="'+(f.x(i)-w/2).toFixed(1)+'" y="'+Math.min(y0,y1).toFixed(1)+'" width="'+w.toFixed(1)+
        '" height="'+Math.max(Math.abs(y1-y0),1).toFixed(1)+'" class="'+(m.result>=0?'pos':'neg')+
        '"><title>Month '+m.month+': '+money(m.result)+'</title></rect>');
    });
    svg.innerHTML=p.join('');
  }
  function put(box,k,v,s,cls){
    var a=box.querySelector('[data-k="'+k+'"]'),b=box.querySelector('[data-k="'+k+'-s"]');
    if(a){a.textContent=v;a.className='kv'+(cls?' '+cls:'')}if(b)b.textContent=s||'';
  }
  function draw(sc){
    if(sc)open=sc;
    var box=document.querySelector('.ver[data-sc="'+open+'"]'),s=M.scenarios[open];
    var r=calc(s,N,M.founder_cash,conv[open]),last=r.months[N-1];
    box.querySelector('[data-k="ctw"]').textContent=money(r.cost_to_win_customer)+(usd(r.cost_to_win_customer)?' ('+usd(r.cost_to_win_customer)+')':'');
    box.querySelector('.edited').hidden=Math.abs(conv[open]-s.conversion_rate)<1e-9;
    var c=r.contribution_per_transaction;
    put(box,'contribution',(c<0?MINUS:'')+CUR+' '+whole(Math.abs(c)),c<0?'a loss on every one':'after its own costs',c<0?'bad':'good');
    put(box,'breakeven',r.break_even_month?'Month '+r.break_even_month:'Not in '+N+' months',
      r.break_even_month?'monthly profit covers fixed costs and marketing':'monthly costs stay above what comes in',r.break_even_month?'good':'bad');
    put(box,'test',money(r.cash_for_90_day_test),usd(r.cash_for_90_day_test));
    put(box,'need',money(r.cash_need),(usd(r.cash_need)?usd(r.cash_need)+', ':'')+(r.still_falling?'and still falling at month '+N:'lowest point'),r.still_falling?'bad':'');
    put(box,'runway',r.cash_runs_out_month?'Month '+r.cash_runs_out_month:'Lasts '+N+' months',
      'founder cash '+money(M.founder_cash),r.cash_runs_out_month?'bad':'good');
    put(box,'customers',whole(last.active_customers),whole(last.transactions)+' '+(M.transaction||'transaction')+'s that month');
    box.querySelectorAll('svg[data-chart="bars"]').forEach(function(g){drawBars(g,r)});
    document.querySelectorAll('svg[data-chart="cash"]').forEach(drawCash);
  }
  window.__drawModel=draw;
  document.querySelectorAll('.conv-input').forEach(function(inp){
    inp.addEventListener('input',function(){
      var v=parseFloat(inp.value);
      if(!(v>0&&v<=100))return;
      conv[inp.getAttribute('data-sc')]=v/100;draw(inp.getAttribute('data-sc'));
    });
  });
  document.querySelectorAll('.reset').forEach(function(b){b.addEventListener('click',function(){
    var sc=b.getAttribute('data-sc'),inp=document.getElementById('conv-'+sc);
    inp.value=b.getAttribute('data-v');conv[sc]=M.scenarios[sc].conversion_rate;draw(sc);
  })});
  draw('Moderate');
})();
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path):
    try:
        return json.loads(read(path))
    except (OSError, ValueError):
        return None


def gate_section(run: Path):
    path = run / "50_decision" / "gate_tracker.csv"
    if not path.is_file():
        return None
    rows = list(csv.reader(io.StringIO(read(path))))
    if len(rows) < 2:
        return None
    head = [c.replace("_", " ").capitalize() for c in rows[0]]
    md_rows = [head] + rows[1:]
    return table_html(md_rows)


def render(run_dir) -> Path:
    run = Path(run_dir)
    dec = run / "50_decision"
    memo, pack = dec / "decision_memo.md", dec / "decision_pack.md"
    full = memo.is_file()
    main_file = memo if full else pack
    if not main_file.is_file():
        raise RenderError(f"missing: 50_decision/{'decision_memo.md' if full else 'decision_pack.md'}")
    result = load_json(run / "30_assessment" / "scorecard_result.json")
    if not isinstance(result, dict) or "verdict" not in result:
        raise RenderError("missing or not valid: 30_assessment/scorecard_result.json")
    inputs = load_json(run / "30_assessment" / "scorecard_inputs.json") or {}
    before = load_json(run / "30_assessment" / "scorecard_inputs_v1.json") if full else None
    model_inputs = load_json(run / "20_model" / "model_inputs.json")
    if model_inputs is not None:
        try:
            model.validate(model_inputs)
        except model.ModelError as exc:
            raise RenderError(f"20_model/model_inputs.json: {exc}")

    doc = parse_doc(read(main_file))
    name = re.sub(r"^(Decision pack|Decision memo):\s*", "", doc["title"]) or "Before You Build"
    meta, intro = header_meta(doc["header"])
    mode = "Full Review" if full else "Quick Check"
    verdict = str(result["verdict"])
    vclass = VERDICT_CLASS.get(verdict, "pivot")
    score = int(result.get("readiness_score", 0))
    conf = html.escape(str(result.get("confidence", "")))
    reasons = result.get("reasons") or []
    reasons_html = ("<ul>" + "".join(f"<li>{html.escape(str(r))}</li>" for r in reasons) + "</ul>"
                    if reasons else '<p class="muted">The score alone set the verdict; no rule overrode it.</p>')

    used, nav, body = set(), [], []

    def add(title, content):
        sid = slug(title, used)
        nav.append((sid, title))
        body.append(f'<section id="{sid}"><h2>{html.escape(title)}</h2>{content}</section>')

    sections = list(doc["sections"])
    if full:
        tp = run / "50_decision" / "test_plan.md"
        if tp.is_file():
            plan = dict(parse_doc(read(tp))["sections"])
            for t in TEST_PLAN_SECTIONS:
                if t in plan and plan[t].strip():
                    sections.append((f"Test plan: {t}", plan[t]))
    for title, md in sections:
        low = title.lower()
        if low == "verdict":
            continue  # shown in the verdict panel
        if low.startswith("readiness score"):
            chart = ratings_svg(inputs.get("ratings", {}), (before or {}).get("ratings"))
            note = ('<p class="muted">Dashed line: the rating at Stage 3, before the rebuild.</p>'
                    if before else "")
            content = (f'<div class="box">{chart}{note}</div>'
                       f'{mix_html(inputs.get("label_counts", {}))}{render_blocks(blocks(md))}')
        elif low in ("what the numbers say", "key numbers"):
            bl = blocks(md)
            n, found = scenario_table(bl)
            if found and model_inputs:
                content = (model_html(model_inputs) + render_blocks(bl[:n] + bl[n + 1:]) +
                           "<details><summary>The figures as written in this file</summary>"
                           f"{table_html(bl[n][1])}</details>")
            elif found:
                tbl = table_html(bl[n][1])
                content = (scenario_html(found) + render_blocks(bl[:n] + bl[n + 1:]) +
                           f"<details><summary>All scenarios side by side</summary>{tbl}</details>")
            else:
                content = render_blocks(bl)
        elif "risk" in low:
            content = risks_html(md)
        elif low == "the test":
            content = timeline_svg(md) + test_html(md)
            gate = gate_section(run) if full else None
            if gate:
                content += ("<h3>Gate tracker</h3><p class=\"muted\">From "
                            "<code>50_decision/gate_tracker.csv</code>. Fill in measured values as the "
                            "test runs.</p>" + gate)
        else:
            content = render_blocks(blocks(md))
        add(title, content)

    src = run / "sources.md"
    if src.is_file():
        src_md = "\n".join(l for l in read(src).splitlines() if not l.startswith("# "))
        n = sum(1 for l in src_md.splitlines() if l.strip().startswith("- ["))
        add("All sources", f"<details><summary>{n} links used in this run</summary>"
                           f"{render_blocks(blocks(src_md))}</details>")

    meta_html = "".join(f"<span><b>{html.escape(k)}:</b> {inline(v)}</span>"
                        for k, v in meta if k not in ("Agent",))
    verdict_md = dict(doc["sections"]).get("Verdict", "")
    verdict_text = render_blocks([b for b in blocks(verdict_md)
                                  if not (b[0] == "p" and b[1].startswith("**"))
                                  and not (b[0] == "p" and b[1].startswith("Why the committee"))
                                  and b[0] != "ul"])
    rail = "".join(f'<li><a href="#{sid}">{html.escape(t)}</a></li>' for sid, t in nav)
    opts = "".join(f'<option value="{sid}">{html.escape(t)}</option>' for sid, t in nav)
    full_plan = ('<p class="foot">The full plan is in <a href="full_plan.md">full_plan.md</a> '
                 'and the test plan in <a href="test_plan.md">test_plan.md</a>, in this folder.</p>'
                 if full else "")

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:">
<title>{html.escape(name)}: Before You Build</title>
<style>{CSS}</style></head><body>
<div class="shell">
<nav class="rail" aria-label="Sections"><div class="brand">{html.escape(name)}<small>Before You Build · {mode}</small></div><ol>{rail}</ol></nav>
<main>
<header class="hero">
<div class="eyebrow">Before You Build · {mode}</div>
<h1>{html.escape(name)}</h1>
<div class="meta">{meta_html}</div>
{render_blocks(blocks(intro))}
<div class="verdict">
<div class="vcard {vclass}"><div class="k">Verdict</div><div class="vword">{html.escape(verdict)}</div>
<div class="k">Why the committee's rules gave this verdict</div>{reasons_html}</div>
<div class="vcard"><div class="k">Readiness score</div>
<div class="score"><span class="n">{score}</span><span class="muted">out of 100</span><span class="chip">Confidence {conf}</span></div>
{gauge_svg(score)}</div>
</div>
<div class="intro">{verdict_text}</div>
<div class="legend"><span><span class="lab s">S</span> sourced, opens the link</span><span><span class="lab e">E</span> estimated, with the method</span><span><span class="lab a">A</span> assumed, with the reason</span></div>
</header>
<div class="mnav"><label class="muted" for="mnavSel">Jump to section</label><select id="mnavSel">{opts}</select></div>
{"".join(body)}
<div class="disclaimer">{html.escape(DISCLAIMER)}</div>
<p class="foot">Verdict, score and confidence are copied from <code>30_assessment/scorecard_result.json</code>; every other figure is shown as its run file gives it.</p>
{full_plan}
</main></div>
<script>{MODEL_JS}{JS}</script>
</body></html>
"""
    out = dec / "report.html"
    out.write_text(page, encoding="utf-8")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: render_report.py <run_dir>", file=sys.stderr)
        return 2
    run = Path(argv[0])
    if not run.is_dir():
        print(f"error: run folder not found: {run}", file=sys.stderr)
        return 2
    try:
        out = render(run)
    except RenderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
