"""
make_ascii_svg.py

Downsamples source-prepped.png to a character grid and maps each
pixel's brightness to a glyph from a density ramp (bright -> sparse,
dark -> dense). Renders it as a monochrome SVG where each row wipes
in left-to-right, staggered top to bottom, then freezes (no loop).

Usage:
    python scripts/make_ascii_svg.py
Writes: mizan-ascii.svg
"""
from PIL import Image

SRC = "source-prepped.png"
OUT = "mizan-ascii.svg"

COLS = 100
ROWS = 53
CHAR_W = 6.2
CHAR_H = 11
FILL = "#8b949e"          # single monochrome fill, no rainbow-per-char
CURSOR_FILL = "#39d353"

# bright (sparse) -> dark (dense); leading space clears background to nothing
RAMP = " .`:-=+*cs#%@"

ROW_DELAY = 0.045          # stagger between rows, seconds
WIPE_DURATION = 0.6        # how long a single row takes to type in


def brightness_to_char(v: int) -> str:
    idx = int((255 - v) / 255 * (len(RAMP) - 1))
    return RAMP[max(0, min(idx, len(RAMP) - 1))]


def build_grid() -> list[str]:
    img = Image.open(SRC).convert("L").resize((COLS, ROWS))
    px = img.load()
    rows = []
    for y in range(ROWS):
        row = "".join(brightness_to_char(px[x, y]) for x in range(COLS))
        rows.append(row)
    return rows


def escape(c: str) -> str:
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(c, c)


def build_svg(rows: list[str]) -> str:
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    total_time = ROWS * ROW_DELAY + WIPE_DURATION

    body = []
    for r, row in enumerate(rows):
        y = (r + 1) * CHAR_H - 2
        delay = r * ROW_DELAY
        clip_id = f"clip{r}"
        text = "".join(escape(c) for c in row)

        body.append(f'''
  <clipPath id="{clip_id}">
    <rect x="0" y="{r * CHAR_H}" width="0" height="{CHAR_H}">
      <animate attributeName="width" from="0" to="{width}"
               begin="{delay:.3f}s" dur="{WIPE_DURATION}s"
               fill="freeze" calcMode="linear" />
    </rect>
  </clipPath>''')

    text_lines = []
    for r, row in enumerate(rows):
        y = (r + 1) * CHAR_H - 2
        clip_id = f"clip{r}"
        text = "".join(escape(c) for c in row)
        text_lines.append(
            f'  <text x="0" y="{y}" clip-path="url(#{clip_id})" '
            f'font-family="Consolas, monospace" font-size="{CHAR_H - 1}" '
            f'fill="{FILL}" xml:space="preserve">{text}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}"
     viewBox="0 0 {width:.0f} {height:.0f}">
  <style>
    text {{ letter-spacing: 0; }}
  </style>
  <defs>{"".join(body)}
  </defs>
  <rect width="100%" height="100%" fill="transparent" />
{chr(10).join(text_lines)}
</svg>
'''
    return svg


if __name__ == "__main__":
    grid = build_grid()
    svg = build_svg(grid)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}  ({COLS}x{ROWS} chars)")
