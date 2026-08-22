"""
make_info_card.py

Hand-authors a neofetch-style SVG panel: a title bar, then colored
key/value rows. Each line fades + slides in on a short stagger so it
looks like it's printing next to the ASCII portrait.

Set STATIC=1 to emit a frozen (no-animation) frame for local previews.

Usage:
    python scripts/make_info_card.py
Writes: info-card.svg
"""
import os

OUT = "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

WIDTH = 490
LINE_H = 30
PAD_TOP = 56
ACCENT = "#39d353"
LABEL_COLOR = "#8b949e"
VALUE_COLOR = "#c9d1d9"
BG = "#0d1117"
BORDER = "#30363d"

ROWS = [
    ("user", "mizan@github", None),
    ("---", "", None),
    ("Now", "Cybersecurity student, full-stack \"vibe coder\"", ACCENT),
    ("Prev", "Building web + security projects since 2023", None),
    ("Stack", "React / Node.js / Flask / MongoDB / Docker", None),
    ("Focus", "Pentesting, network security, web dev", None),
    ("Flagship", "LooseNotion \u00b7 NoVAult \u00b7 CyberSentinel", ACCENT),
    ("Site", "md-mizan.vercel.app", None),
]

STAGGER = 0.12
FADE_DUR = 0.45


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg() -> str:
    height = PAD_TOP + len(ROWS) * LINE_H + 24
    lines = []

    for i, (label, value, color) in enumerate(ROWS):
        y = PAD_TOP + i * LINE_H
        fill = color or VALUE_COLOR
        label_txt = f'<tspan fill="{ACCENT}" font-weight="600">{esc(label)}</tspan>' if label != "---" else ""
        sep = ": " if value and label != "---" else ""
        rule = '<line x1="24" y1="{y}" x2="{w}" y2="{y}" stroke="{b}" stroke-width="1" />'.format(
            y=y - 8, w=WIDTH - 24, b=BORDER
        ) if label == "---" else ""

        if label == "---":
            content = rule
        else:
            content = (
                f'<text x="24" y="{y}" font-family="Consolas, monospace" '
                f'font-size="15" fill="{fill}">{label_txt}{sep}{esc(value)}</text>'
            )

        if STATIC or not content:
            lines.append(f'  {content}')
        else:
            delay = i * STAGGER
            lines.append(f'''  <g opacity="0" transform="translate(-8,0)">
    <animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="{FADE_DUR}s" fill="freeze" />
    <animateTransform attributeName="transform" type="translate" from="-8,0" to="0,0" begin="{delay:.2f}s" dur="{FADE_DUR}s" fill="freeze" />
    {content}
  </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10"
        fill="{BG}" stroke="{BORDER}" />
  <circle cx="22" cy="22" r="6" fill="#ff5f56" />
  <circle cx="42" cy="22" r="6" fill="#ffbd2e" />
  <circle cx="62" cy="22" r="6" fill="#27c93f" />
  <text x="24" y="{PAD_TOP - 18}" font-family="Consolas, monospace" font-size="13"
        fill="{LABEL_COLOR}">mizan989@github ~ %</text>
{chr(10).join(lines)}
</svg>
'''
    return svg


if __name__ == "__main__":
    svg = build_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")
