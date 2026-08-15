#!/usr/bin/env python3
"""Build assets/shots/* — the four project tiles used in the README grid.

Three are real screenshots of the live apps, captured headlessly:

    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      --headless --disable-gpu --hide-scrollbars --virtual-time-budget=9000 \
      --window-size=1280,800 --screenshot=RAW/f1.png https://f1bulletin.pournamiprakash.dev

The fourth is a drawn tile pointing at the case-study repositories, since a
single image can only carry one link and there are three of them.

Every tile is 16:10 so the 2x2 grid stays aligned.
"""

from pathlib import Path
from PIL import Image

RAW = Path("/private/tmp/claude-501/-Users-pournami-Documents-job-search-copilot"
           "/25b310ee-7e74-4588-956d-925caaaf6f96/scratchpad/shots")
OUT = Path(__file__).parent / "assets" / "shots"
TW, TH = 640, 400

BG, FG, MUT, BORDER, BLUE = "#0d1117", "#e6edf3", "#8b949e", "#30363d", "#4493f8"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Consolas,monospace"
UI = "'Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif"

CASE_STUDIES = [
    "retail-decision-engine",
    "criteo-ad-incrementality",
    "meps-healthcare-risk",
]


def cover(im):
    """Crop-to-fill at TWxTH — screenshots are already 16:10."""
    im = im.convert("RGB")
    scale = max(TW / im.width, TH / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - TW) // 2, (im.height - TH) // 2
    return im.crop((left, top, left + TW, top + TH))


def case_studies_tile(path):
    """A tile listing the case-study repos; the whole tile links to the repo list."""
    rows = "".join(
        '<text x="56" y="%d" font-size="21" font-family="%s" fill="%s" '
        'xml:space="preserve">%s</text>' % (208 + i * 42, MONO, FG, name)
        for i, name in enumerate(CASE_STUDIES)
    )
    dots = "".join(
        '<circle cx="40" cy="%d" r="4.5" fill="%s"/>' % (201 + i * 42, BLUE)
        for i in range(len(CASE_STUDIES))
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'role="img" aria-label="Case studies: %s">'
        '<rect x="1" y="1" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="2"/>'
        '<text x="40" y="92" font-size="34" font-weight="700" letter-spacing="1.5" '
        'font-family="%s" fill="%s" xml:space="preserve">Case studies</text>'
        '<text x="40" y="132" font-size="19" font-family="%s" fill="%s" '
        'xml:space="preserve">Written as decision documents</text>'
        '<line x1="40" y1="160" x2="600" y2="160" stroke="%s" stroke-width="1.5"/>'
        '%s%s'
        '<text x="40" y="352" font-size="19" font-family="%s" fill="%s" '
        'xml:space="preserve">View all repositories &#8594;</text>'
        '</svg>'
        % (TW, TH, ", ".join(CASE_STUDIES),
           TW - 2, TH - 2, BG, BORDER,
           UI, FG,
           UI, MUT,
           BORDER,
           dots, rows,
           UI, BLUE)
    )
    Path(path).write_text(svg)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)

    for slug in ("f1", "ipl", "watch"):
        src = RAW / f"{slug}.png"
        if not src.exists():
            print(f"  SKIP {slug}: {src} missing")
            continue
        cover(Image.open(src)).save(OUT / f"{slug}.jpg", quality=82, optimize=True)

    case_studies_tile(OUT / "case-studies.svg")

    total = 0
    for p in sorted(OUT.iterdir()):
        total += p.stat().st_size
        print(f"  {p.name:<20} {p.stat().st_size/1024:6.0f} KB")
    print(f"\n  total {total/1024:.0f} KB across {len(list(OUT.iterdir()))} tiles")
