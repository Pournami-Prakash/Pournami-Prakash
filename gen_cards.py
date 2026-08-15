#!/usr/bin/env python3
"""Generate assets/cards/*.svg — VS Code-themed project cards.

Each card is a standalone SVG. In the README each one is wrapped in an <a href>,
so the whole card is clickable even though SVG-internal links don't work when
GitHub loads an SVG through <img>.

Re-run after editing PROJECTS.
"""

from pathlib import Path

OUT = Path(__file__).parent / "assets" / "cards"

W, H = 280, 64
BG, BORDER, FG, MUTED = "#252526", "#3d444d", "#cccccc", "#858585"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Consolas,monospace"
UI = "'Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif"

# language dot colors (GitHub linguist-ish)
PY, R, TS, JS = "#3572A5", "#198CE7", "#3178c6", "#f1e05a"

# slug, repo name, language label, dot color
PROJECTS = [
    ("retail",   "retail-decision-engine",   "Python",     PY),
    ("criteo",   "criteo-ad-incrementality", "Python",     PY),
    ("meps",     "meps-healthcare-risk",     "R",          R),
    ("f1",       "f1-bulletin-live",         "TypeScript", TS),
    ("ipl",      "IPL",                      "Python",     PY),
    ("watch",    "Watch-History",            "TypeScript", TS),
    ("printer",  "printer",                  "TypeScript", TS),
    ("blah",     "blah-blah-blah",           "TypeScript", TS),
    ("bigmac",   "bigmac-drifting-burger",   "Python",     PY),
]

CHAR_W = 7.2   # mono advance at 12px
NAME_SIZE = 12


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))


def card(name, lang, dot):
    # shrink the name a touch if it would collide with the language label
    size = NAME_SIZE
    while len(name) * (CHAR_W * size / NAME_SIZE) > 186 and size > 9:
        size -= 0.5

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s — %s">'
        '<rect x="0.5" y="0.5" width="%s" height="%s" rx="6" fill="%s" stroke="%s"/>'
        '<rect x="0" y="0" width="3" height="%d" fill="%s"/>'
        '<circle cx="20" cy="%s" r="4.5" fill="%s"/>'
        '<text x="32" y="%s" font-size="%s" font-family="%s" fill="%s" '
        'xml:space="preserve">%s</text>'
        '<text x="%d" y="%s" text-anchor="end" font-size="10" font-family="%s" fill="%s" '
        'xml:space="preserve">%s</text>'
        '</svg>'
        % (W, H, W, H, esc(name), esc(lang),
           W - 1, H - 1, BG, BORDER,
           H, dot,
           H / 2 - 4, dot,
           H / 2, size, MONO, FG, esc(name),
           W - 16, H / 2 + 16, UI, MUTED, esc(lang))
    )


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, name, lang, dot in PROJECTS:
        p = OUT / f"{slug}.svg"
        p.write_text(card(name, lang, dot))
        print(f"  {p.name:<14} {name}")
    print(f"\n{len(PROJECTS)} cards -> {OUT}")
