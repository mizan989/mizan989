"""
render_heatmap_svg.py

Renders data/contributions.json as the classic 53-week x 7-day
calendar of rounded boxes, GitHub-green ramp. Reveals once with a
diagonal, line-after-line slide-down (plays on load, then freezes).

Usage:
    python scripts/render_heatmap_svg.py
Writes: contrib-heatmap.svg
"""
import json
from datetime import datetime, timedelta

DATA = "data/contributions.json"
OUT = "contrib-heatmap.svg"

CELL = 12
GAP = 3
PAD_LEFT = 30
PAD_TOP = 20
FOOTER_H = 34

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
TEXT_COLOR = "#8b949e"

WEEKS = 53
STAGGER = 0.012
DUR = 0.5


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def build_columns(days):
    """Bucket days into 53 week-columns of 7 (Sun-Sat), most recent last."""
    by_date = {d["date"]: d for d in days}
    if not days:
        return []
    end = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()
    end_sun = end - timedelta(days=(end.weekday() + 1) % 7 - 6 if False else 0)
    # align end to the Saturday of its week, start 52 weeks back on a Sunday
    offset_to_sat = (5 - end.weekday()) % 7  # Python Mon=0..Sun=6; Sat=5
    last_sat = end + timedelta(days=offset_to_sat)
    first_sun = last_sat - timedelta(weeks=WEEKS - 1, days=6)

    columns = []
    cursor = first_sun
    for _w in range(WEEKS):
        col = []
        for _d in range(7):
            key = cursor.strftime("%Y-%m-%d")
            entry = by_date.get(key)
            col.append(entry["level"] if entry else 0)
            cursor += timedelta(days=1)
        columns.append(col)
    return columns


def build_svg(data: dict) -> str:
    columns = build_columns(data["days"])
    width = PAD_LEFT + WEEKS * (CELL + GAP)
    height = PAD_TOP + 7 * (CELL + GAP) + FOOTER_H

    cells = []
    for w, col in enumerate(columns):
        for d, level in enumerate(col):
            x = PAD_LEFT + w * (CELL + GAP)
            y = PAD_TOP + d * (CELL + GAP)
            delay = (w + d * 0.15) * STAGGER
            color = PALETTE[min(level, len(PALETTE) - 1)]
            cells.append(f'''  <rect x="{x}" y="{y - 10}" width="{CELL}" height="{CELL}" rx="2"
        fill="{color}" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="{DUR}s" fill="freeze" />
    <animate attributeName="y" from="{y - 10}" to="{y}" begin="{delay:.3f}s" dur="{DUR}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" />
  </rect>''')

    legend_x = width - 150
    legend_y = height - 12
    legend = [f'  <text x="{legend_x - 40}" y="{legend_y + 4}" font-family="Consolas, monospace" font-size="11" fill="{TEXT_COLOR}">Less</text>']
    for i, c in enumerate(PALETTE):
        legend.append(f'  <rect x="{legend_x + i * 14}" y="{legend_y - 8}" width="10" height="10" rx="2" fill="{c}" />')
    legend.append(f'  <text x="{legend_x + len(PALETTE) * 14 + 6}" y="{legend_y + 4}" font-family="Consolas, monospace" font-size="11" fill="{TEXT_COLOR}">More</text>')

    footer_text = (
        f"{data['total']} contributions in the last year \u00b7 "
        f"current streak {data['current_streak']}d \u00b7 longest {data['longest_streak']}d"
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="transparent" />
{chr(10).join(cells)}
  <text x="{PAD_LEFT}" y="{height - 8}" font-family="Consolas, monospace" font-size="12" fill="{TEXT_COLOR}">{footer_text}</text>
{chr(10).join(legend)}
</svg>
'''
    return svg


if __name__ == "__main__":
    data = load()
    svg = build_svg(data)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}")
