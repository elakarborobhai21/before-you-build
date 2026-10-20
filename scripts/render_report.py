#!/usr/bin/env python3
"""Build an interactive HTML report from a finished Before You Build run folder.

Usage: python3 scripts/render_report.py <run_dir>
Reads the decision pack (Quick Check) or the decision memo and test plan (Full
Review), the scorecard files and sources.md, and writes
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
from pathlib import Path

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


# ---------- Page ----------

CSS = """
:root{--paper:#f6f6f2;--surface:#fdfdfb;--ink:#13171c;--ink-2:#4b5058;--ink-3:#7d8288;
--line:#dfe0da;--line-2:#c7c9c2;--accent:#0b6e4f;--accent-soft:#e3f0ea;
--go:#0b7a4b;--go-soft:#dff1e8;--pivot:#a86a00;--pivot-soft:#f8ecd3;--stop:#b8323a;--stop-soft:#f6e0e1;
--s:#0b6e4f;--e:#2a6fc4;--a:#a86a00;--adequate:#6f9a3a;--r:10px;
--f-display:"Avenir Next","Segoe UI",system-ui,-apple-system,sans-serif;
--f-body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
--f-mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#111416;--surface:#181c1f;
--ink:#eef0ec;--ink-2:#b9bdb8;--ink-3:#868b88;--line:#2a2f33;--line-2:#3a4045;--accent:#3fbf8f;
--accent-soft:#16302a;--go:#3fbf8f;--go-soft:#16302a;--pivot:#e0a43a;--pivot-soft:#33280f;
--stop:#ef6b6f;--stop-soft:#3a1c1e;--s:#3fbf8f;--e:#6aa5f0;--a:#e0a43a;--adequate:#9cc464;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#111416;--surface:#181c1f;--ink:#eef0ec;--ink-2:#b9bdb8;
--ink-3:#868b88;--line:#2a2f33;--line-2:#3a4045;--accent:#3fbf8f;--accent-soft:#16302a;--go:#3fbf8f;
--go-soft:#16302a;--pivot:#e0a43a;--pivot-soft:#33280f;--stop:#ef6b6f;--stop-soft:#3a1c1e;
--s:#3fbf8f;--e:#6aa5f0;--a:#e0a43a;--adequate:#9cc464;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15.5px/1.6 var(--f-body)}
a{color:var(--accent)}
.shell{display:grid;grid-template-columns:230px minmax(0,1fr);gap:40px;max-width:1180px;margin:0 auto;padding:0 24px 80px}
.rail{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:28px 0}
.rail .brand{font:700 17px/1.25 var(--f-display)}
.rail .brand small{display:block;font:400 11.5px var(--f-body);color:var(--ink-3);letter-spacing:.06em;text-transform:uppercase;margin-top:4px}
.rail ol{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:1px}
.rail a{display:block;padding:5px 8px;border-radius:6px;text-decoration:none;color:var(--ink-2);font-size:13.5px;line-height:1.35}
.rail a:hover,.rail a.on{background:var(--accent-soft);color:var(--ink)}
.mnav{display:none}
main{min-width:0;padding-top:28px}
.hero .eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}
.hero h1{font:700 clamp(30px,4.6vw,48px)/1.06 var(--f-display);letter-spacing:-.02em;margin:10px 0 12px;max-width:22ch;text-wrap:balance}
.meta{display:flex;flex-wrap:wrap;gap:4px 18px;font-size:13px;color:var(--ink-3)}
.meta b{font-weight:500;color:var(--ink-2)}
.intro{color:var(--ink-2);max-width:70ch}
.verdict{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:18px;margin:26px 0 6px}
.vcard{border-radius:var(--r);padding:20px 22px;border:1px solid var(--line);background:var(--surface)}
.vcard .k{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.vword{font:700 clamp(34px,5vw,46px)/1.05 var(--f-display);margin:6px 0 8px}
.vcard.go{background:var(--go-soft);border-color:var(--go)}.vcard.go .vword{color:var(--go)}
.vcard.pivot{background:var(--pivot-soft);border-color:var(--pivot)}.vcard.pivot .vword{color:var(--pivot)}
.vcard.stop{background:var(--stop-soft);border-color:var(--stop)}.vcard.stop .vword{color:var(--stop)}
.vcard ul{margin:8px 0 0;padding-left:18px;font-size:14px}
.score{display:flex;align-items:baseline;gap:10px}
.score .n{font:700 40px/1 var(--f-display)}
.chip{display:inline-block;font-size:12px;padding:2px 10px;border-radius:999px;border:1px solid var(--line-2);color:var(--ink-2)}
svg{display:block;width:100%;height:auto;overflow:visible}
svg text{fill:var(--ink-3);font:11.5px var(--f-body)}
.gauge{margin-top:22px}.gauge text{font-size:15px}.gauge .z-stop{fill:var(--stop-soft)}.gauge .z-pivot{fill:var(--pivot-soft)}.gauge .z-go{fill:var(--go-soft)}
.gauge .mark{stroke:var(--ink);stroke-width:3}.gauge .mark-t{fill:var(--ink);font-weight:700;font-size:16px}
.ratings .grid{stroke:var(--line)}.ratings .an{fill:var(--ink-2);font-size:13px}.ratings .rv{fill:var(--ink-2);font-size:12px}
.ratings .r0{fill:var(--stop)}.ratings .r1{fill:var(--pivot)}.ratings .r2{fill:var(--adequate)}.ratings .r3{fill:var(--go)}
.ratings .before{stroke:var(--ink);stroke-width:2;stroke-dasharray:3 3}
section{padding:40px 0 4px;border-top:1px solid var(--line);margin-top:34px;scroll-margin-top:16px}
h2{font:700 clamp(22px,2.8vw,29px)/1.2 var(--f-display);letter-spacing:-.012em;margin:0 0 12px}
h3{font:600 17px var(--f-display);margin:22px 0 6px}
p,li{max-width:74ch}
.muted{color:var(--ink-3);font-size:13px}
.box{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;margin:12px 0}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;font-size:12.5px;color:var(--ink-2);background:var(--paper)}
tr:last-child td{border-bottom:0}
blockquote{margin:12px 0;padding:10px 16px;border-left:3px solid var(--line-2);color:var(--ink-2)}
code{font:13px var(--f-mono);background:var(--accent-soft);padding:1px 5px;border-radius:4px}
.lab{display:inline-block;font:700 10.5px/1 var(--f-mono);padding:3px 5px;border-radius:4px;margin:0 2px;vertical-align:1px;text-decoration:none;color:#fff}
.lab.s{background:var(--s)}.lab.e{background:var(--e)}.lab.a{background:var(--a)}
a.lab.s:hover{outline:2px solid var(--s);outline-offset:1px}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--ink-2);margin-top:12px}
.mix{margin:14px 0}.mixbar{display:flex;height:12px;border-radius:6px;overflow:hidden;gap:2px}
.mx.s,.mixkey i.s{background:var(--s)}.mx.e,.mixkey i.e{background:var(--e)}.mx.a,.mixkey i.a{background:var(--a)}
.mixkey{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12.5px;color:var(--ink-2);margin-top:8px}
.mixkey i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.sc-bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin:12px 0}
.sc-lbl{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.seg{display:inline-flex;border:1px solid var(--line-2);border-radius:999px;padding:3px;background:var(--surface);gap:2px}
.seg button{font:inherit;font-size:13.5px;border:0;background:transparent;color:var(--ink-2);padding:6px 14px;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.seg button:focus-visible,.rail a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:10px 0 4px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;min-width:0}
.tile .tk{font-size:12.5px;color:var(--ink-3);line-height:1.4}
.sc-val{font:700 19px/1.3 var(--f-display);margin-top:6px;overflow-wrap:anywhere}
.sc-note{font-size:12.5px;color:var(--ink-2);margin-top:8px;border-top:1px dashed var(--line);padding-top:6px}
.sc-note span{color:var(--ink-3)}
details{margin:10px 0}summary{cursor:pointer;color:var(--ink-2);font-size:14px}
dl.test{display:grid;gap:8px;margin:14px 0}
.trow{display:grid;grid-template-columns:170px minmax(0,1fr);gap:16px;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line-2);border-radius:var(--r);padding:12px 16px}
.trow dt{font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3);padding-top:2px}
.trow dd{margin:0}.trow dd ul{margin:6px 0 0;padding-left:18px}
.trow.pass{border-left-color:var(--go)}.trow.fail{border-left-color:var(--stop)}
.trow.channel{border-left-color:var(--e);background:color-mix(in srgb,var(--e) 7%,var(--surface))}
.trow.date{border-left-color:var(--ink)}.trow.wide{grid-template-columns:minmax(0,1fr)}
.disclaimer{margin-top:40px;padding:16px 18px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);color:var(--ink-2);font-size:14px}
.foot{font-size:12.5px;color:var(--ink-3);margin-top:12px}
@media (max-width:900px){.shell{grid-template-columns:minmax(0,1fr);gap:0;padding:0 16px 60px}.rail{display:none}
.mnav{display:block;margin:16px 0 0}.mnav select{font:inherit;width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--line-2);background:var(--surface);color:var(--ink)}
.verdict{grid-template-columns:minmax(0,1fr)}.trow{grid-template-columns:minmax(0,1fr);gap:2px}}
@media print{.rail,.mnav,.sc-bar{display:none}.shell{display:block}.sc-val[hidden]{display:block!important}
.sc-val::before{content:attr(data-sc) ": ";font-weight:400;color:var(--ink-3);font-size:12px}section{break-inside:avoid-page}}
"""

JS = """
(function(){
  var btns=document.querySelectorAll('.sc-btn');
  btns.forEach(function(b){b.addEventListener('click',function(){
    var sc=b.getAttribute('data-sc');
    btns.forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-sc')===sc?'true':'false')});
    document.querySelectorAll('.sc-val').forEach(function(v){v.hidden=v.getAttribute('data-sc')!==sc});
  })});
  var sel=document.getElementById('mnavSel');
  if(sel){sel.addEventListener('change',function(){var t=document.getElementById(sel.value);if(t)t.scrollIntoView()})}
  var links=document.querySelectorAll('.rail a');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)})}})},
      {rootMargin:'-20% 0px -70% 0px'});
    document.querySelectorAll('main section').forEach(function(s){io.observe(s)});
  }
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
            if found:
                tbl = table_html(bl[n][1])
                content = (scenario_html(found) + render_blocks(bl[:n] + bl[n + 1:]) +
                           f"<details><summary>All scenarios side by side</summary>{tbl}</details>")
            else:
                content = render_blocks(bl)
        elif low == "the test":
            content = test_html(md)
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
<script>{JS}</script>
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
