#!/usr/bin/env python3
"""Generate assets/vscode_hero.svg — an animated VS Code window for the GitHub profile README.

Self-contained SVG: no scripts, no external fonts, no network. Renders on GitHub.
Edit CODE / SIDEBAR below and re-run.
"""

from pathlib import Path

OUT = Path(__file__).parent / "assets" / "vscode_hero.svg"

# ---------------------------------------------------------------- geometry
W, H = 920, 560
CHAR_W = 8.1                 # monospace advance at FONT_CODE
FONT_CODE = 13.5
LINE_H = 20.5
FIRST_BASELINE = 93.0
CODE_X = 310                 # left edge of code text
GUTTER_X = 288               # right-aligned line numbers
SEC_PER_CHAR = 0.009         # typing speed
GAP = 0.03                   # pause between lines
BLANK_DUR = 0.09             # pause on an empty line

# VS Code Dark+ palette
BG, TITLEBAR, ACTIVITY, SIDEBAR_BG = "#1e1e1e", "#323233", "#333333", "#252526"
TABBAR, TAB_ACTIVE, STATUS = "#2d2d2d", "#1e1e1e", "#007acc"
FG, MUTED, WHITE = "#cccccc", "#858585", "#ffffff"

# token colors
C_COMMENT, C_KEY, C_TYPE = "#6a9955", "#569cd6", "#4ec9b0"
C_FUNC, C_STR, C_VAR, C_PLAIN = "#dcdcaa", "#ce9178", "#9cdcfe", "#d4d4d4"
C_CONST = "#569cd6"

UI_FONT = "'Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Consolas,monospace"

# ---------------------------------------------------------------- content
# Each line is a list of (text, color) tokens. [] = blank line.
CODE = [
    [("# about.py · whoami()", C_COMMENT)],
    [],
    [("class ", C_KEY), ("Pournami", C_TYPE), ("(", C_PLAIN),
     ("DataScientist", C_TYPE), (", ", C_PLAIN), ("AnalyticsEngineer", C_TYPE),
     ("):", C_PLAIN)],
    [('    """M.S. Data Science, University of Rochester (2025)."""', C_STR)],
    [],
    [("    def ", C_KEY), ("__init__", C_FUNC), ("(", C_PLAIN),
     ("self", C_VAR), ("):", C_PLAIN)],
    [("        self", C_VAR), (".role     = ", C_PLAIN),
     ('"Data Warehouse Analyst I @ U of R IT"', C_STR)],
    [("        self", C_VAR), (".stack    = [", C_PLAIN),
     ('"SQL"', C_STR), (", ", C_PLAIN), ('"Python"', C_STR), (", ", C_PLAIN),
     ('"Snowflake"', C_STR), (", ", C_PLAIN), ('"dbt"', C_STR), (", ", C_PLAIN),
     ('"Airflow"', C_STR), ("]", C_PLAIN)],
    [("        self", C_VAR), (".domains  = [", C_PLAIN),
     ('"retail"', C_STR), (", ", C_PLAIN), ('"advertising"', C_STR), (", ", C_PLAIN),
     ('"healthcare"', C_STR), (",", C_PLAIN)],
    [("                         ", C_PLAIN),
     ('"sports"', C_STR), (", ", C_PLAIN), ('"media"', C_STR), (", ", C_PLAIN),
     ('"higher-ed"', C_STR), ("]", C_PLAIN)],
    [("        self", C_VAR), (".studying = ", C_PLAIN),
     ('"a few certifications, in progress"', C_STR)],
    [],
    [("    def ", C_KEY), ("ship", C_FUNC), ("(", C_PLAIN), ("self", C_VAR),
     (", ", C_PLAIN), ("model", C_VAR), ("):", C_PLAIN)],
    [("        if not ", C_KEY), ("model", C_VAR), (".evidence_holds():", C_PLAIN)],
    [("            return ", C_KEY), ("self", C_VAR), (".say_so(", C_PLAIN),
     ("model", C_VAR), (")", C_PLAIN)],
    [("        return ", C_KEY), ("model", C_VAR), (".decision(", C_PLAIN),
     ("with_limitations", C_VAR), ("=", C_PLAIN), ("True", C_CONST), (")", C_PLAIN)],
    [],
    [("# currently teaching an LLM where our KPIs live", C_COMMENT)],
]

# sidebar: (label, indent_px, dot_color or None, is_active)
BLUE, RLANG, NB, JSON_Y, FOLDER = "#519aba", "#75aadb", "#e37933", "#cbcb41", "#c09553"
SIDEBAR = [
    ("about.py",         80, BLUE,  True),
    ("experience.md",    80, BLUE,  False),
    ("__FOLDER__projects", 0, None, False),
    ("f1_bulletin.py",   94, BLUE,  False),
    ("meps_risk.R",      94, RLANG, False),
    ("criteo_uplift.py", 94, BLUE,  False),
    ("watchscope.ipynb", 94, NB,    False),
    ("skills.json",      80, JSON_Y, False),
    ("contact.json",     80, JSON_Y, False),
]

STATUS_LEFT = "⎇ main*"
STATUS_PROBLEMS = "✓ 0   ⚠ 0"
STATUS_POS = "Ln 17, Col 47"


# ---------------------------------------------------------------- helpers
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))


def line_text(tokens):
    return "".join(t for t, _ in tokens)


def build():
    # --- timing pass -------------------------------------------------
    schedule = []          # (idx, begin, dur, width, has_text)
    t = 0.0
    for i, toks in enumerate(CODE):
        txt = line_text(toks)
        if not txt:
            schedule.append((i, round(t, 2), BLANK_DUR, 0.0, False))
            t += BLANK_DUR
            continue
        dur = round(len(txt) * SEC_PER_CHAR, 2)
        width = round(len(txt) * CHAR_W, 0)
        schedule.append((i, round(t, 2), dur, width, True))
        t += dur + GAP
    total = round(t, 2)

    # --- clip paths --------------------------------------------------
    defs = ['<clipPath id="r"><rect x="0" y="0" width="%d" height="%d" rx="10"/></clipPath>' % (W, H)]
    for i, begin, dur, width, has in schedule:
        if not has:
            continue
        y = FIRST_BASELINE + i * LINE_H - 13
        defs.append(
            '<clipPath id="ln%d"><rect x="%d" y="%s" width="0" height="18">'
            '<animate attributeName="width" begin="%.2fs" dur="%.2fs" values="0;%d" fill="freeze"/>'
            '</rect></clipPath>' % (i, CODE_X, y, begin, dur, width))

    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'role="img" aria-label="VS Code window showing about.py for Pournami Prakash">' % (W, H)]
    p.append("<defs>" + "".join(defs) + "</defs>")
    p.append('<g clip-path="url(#r)">')

    # --- chrome ------------------------------------------------------
    p.append('<rect x="0" y="0" width="%d" height="%d" fill="%s"/>' % (W, H, BG))
    p.append('<rect x="0" y="0" width="%d" height="32" fill="%s"/>' % (W, TITLEBAR))
    p.append('<rect x="0" y="32" width="48" height="%d" fill="%s"/>' % (H - 32, ACTIVITY))
    p.append('<rect x="48" y="32" width="210" height="%d" fill="%s"/>' % (H - 32, SIDEBAR_BG))
    p.append('<rect x="258" y="32" width="%d" height="35" fill="%s"/>' % (W - 258, TABBAR))
    for cx, col in ((18, "#ff5f56"), (38, "#ffbd2e"), (58, "#27c93f")):
        p.append('<circle cx="%d" cy="16" r="6" fill="%s"/>' % (cx, col))
    p.append('<text x="%d" y="20.5" text-anchor="middle" font-size="12.5" font-family="%s" '
             'fill="%s" xml:space="preserve">about.py — Pournami Prakash — Visual Studio Code</text>'
             % (W // 2, UI_FONT, MUTED))

    # activity bar icons
    p.append('<rect x="0" y="50" width="2" height="32" fill="%s"/>' % WHITE)
    p.append('<path d="M17 58 h9 l4 4 v12 h-13 z" fill="none" stroke="%s" stroke-width="1.4"/>' % WHITE)
    p.append('<circle cx="22" cy="108" r="6" fill="none" stroke="%s" stroke-width="1.4"/>' % MUTED)
    p.append('<line x1="27" y1="113" x2="32" y2="118" stroke="%s" stroke-width="1.4"/>' % MUTED)
    for cy in (148, 161):
        p.append('<circle cx="19" cy="%d" r="2.5" fill="none" stroke="%s" stroke-width="1.4"/>' % (cy, MUTED))
    p.append('<circle cx="30" cy="153" r="2.5" fill="none" stroke="%s" stroke-width="1.4"/>' % MUTED)
    p.append('<path d="M19 151 v8 M19 155 q0 -2 4 -2 h4" fill="none" stroke="%s" stroke-width="1.4"/>' % MUTED)
    for x in (18, 26):
        for y in (192, 200):
            p.append('<rect x="%d" y="%d" width="5" height="5" fill="none" stroke="%s" stroke-width="1.3"/>'
                     % (x, y, MUTED))

    # --- sidebar -----------------------------------------------------
    p.append('<text x="64" y="56" font-size="11" font-family="%s" fill="%s" '
             'xml:space="preserve">EXPLORER</text>' % (UI_FONT, MUTED))
    p.append('<text x="60" y="86" font-size="11" font-weight="500" font-family="%s" fill="%s" '
             'xml:space="preserve">▾ PORTFOLIO</text>' % (UI_FONT, MUTED))
    y = 108
    for label, indent, dot, active in SIDEBAR:
        if label.startswith("__FOLDER__"):
            name = label.replace("__FOLDER__", "")
            p.append('<text x="74" y="%d" font-size="11" font-family="%s" fill="%s" '
                     'xml:space="preserve">▸</text>' % (y + 4, UI_FONT, MUTED))
            p.append('<text x="86" y="%d" font-size="12" font-family="%s" fill="%s" '
                     'xml:space="preserve">📁</text>' % (y + 4, UI_FONT, FOLDER))
            p.append('<text x="104" y="%d" font-size="12.5" font-family="%s" fill="%s" '
                     'xml:space="preserve">%s</text>' % (y + 4, UI_FONT, FG, esc(name)))
            y += 26
            continue
        if active:
            p.append('<rect x="48" y="%d" width="210" height="20" fill="#37373d"/>' % (y - 10))
        p.append('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (indent, y, dot))
        p.append('<text x="%d" y="%d" font-size="12.5" font-family="%s" fill="%s" '
                 'xml:space="preserve">%s</text>'
                 % (indent + 10, y + 4, UI_FONT, WHITE if active else FG, esc(label)))
        y += 26

    # --- tabs --------------------------------------------------------
    p.append('<rect x="258" y="32" width="150" height="35" fill="%s"/>' % TAB_ACTIVE)
    p.append('<rect x="258" y="32" width="150" height="2" fill="#0a84ff"/>')
    p.append('<circle cx="274" cy="49.5" r="4" fill="%s"/>' % BLUE)
    p.append('<text x="286" y="53.5" font-size="12.5" font-family="%s" fill="%s" '
             'xml:space="preserve">about.py</text>' % (UI_FONT, FG))
    p.append('<text x="386" y="54" font-size="11" font-family="%s" fill="%s" '
             'xml:space="preserve">●</text>' % (UI_FONT, MUTED))
    p.append('<text x="428" y="53.5" font-size="12.5" font-family="%s" fill="%s" '
             'xml:space="preserve">skills.json</text>' % (UI_FONT, MUTED))

    # --- code --------------------------------------------------------
    for i, begin, dur, width, has in schedule:
        base = FIRST_BASELINE + i * LINE_H
        p.append('<text x="%d" y="%s" text-anchor="end" opacity="0" font-size="12.5" '
                 'font-family="%s" fill="%s" xml:space="preserve">%2d'
                 '<set attributeName="opacity" to="1" begin="%.2fs"/></text>'
                 % (GUTTER_X, base, MONO, MUTED, i + 1, begin))
        if not has:
            continue
        spans = "".join('<tspan fill="%s">%s</tspan>' % (c, esc(t)) for t, c in CODE[i])
        p.append('<text x="%d" y="%s" clip-path="url(#ln%d)" font-size="%s" '
                 'font-family="%s" xml:space="preserve">%s</text>'
                 % (CODE_X, base, i, FONT_CODE, MONO, spans))

    # --- cursor ------------------------------------------------------
    cur = ['<rect x="%d" y="%s" width="7" height="15" fill="#aeafad">'
           % (CODE_X, FIRST_BASELINE - 11)]
    for i, begin, dur, width, has in schedule:
        y = FIRST_BASELINE + i * LINE_H - 11
        end_x = CODE_X + (width if has else 0)
        cur.append('<set attributeName="y" to="%s" begin="%.2fs"/>' % (y, begin))
        cur.append('<animate attributeName="x" begin="%.2fs" dur="%.2fs" values="%d;%d" '
                   'fill="freeze"/>' % (begin, dur, CODE_X, end_x))
    cur.append('<animate attributeName="opacity" begin="%.2fs" dur="1.06s" '
               'values="1;1;0;0" repeatCount="indefinite"/>' % total)
    cur.append("</rect>")
    p.append("".join(cur))

    # --- status bar --------------------------------------------------
    p.append('<rect x="0" y="%d" width="%d" height="22" fill="%s"/>' % (H - 22, W, STATUS))
    for x, txt in ((14, STATUS_LEFT), (95, STATUS_PROBLEMS), (590, STATUS_POS),
                   (690, "Spaces: 4"), (770, "UTF-8"), (825, "🐍 Python")):
        p.append('<text x="%d" y="%d" font-size="11.5" font-family="%s" fill="%s" '
                 'xml:space="preserve">%s</text>' % (x, H - 7, UI_FONT, WHITE, esc(txt)))

    p.append("</g></svg>")
    return "".join(p), total, schedule


if __name__ == "__main__":
    svg, total, sched = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    widest = max((w for _, _, _, w, h in sched if h), default=0)
    print(f"wrote {OUT}  ({len(svg):,} bytes)")
    print(f"animation: {total:.2f}s   widest line: {widest:.0f}px "
          f"(pane ends at {W}, code starts at {CODE_X} -> limit {W - CODE_X})")
    if CODE_X + widest > W - 12:
        print("  !! WARNING: a line overflows the editor pane")
