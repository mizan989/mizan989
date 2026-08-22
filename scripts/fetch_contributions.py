"""
fetch_contributions.py

GitHub serves the contribution calendar as public HTML at
https://github.com/users/<username>/contributions -- the same
fragment the profile page itself uses. No GraphQL, no token.

Usage:
    python scripts/fetch_contributions.py
Writes: data/contributions.json
"""
import json
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "mizan989"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = "data/contributions.json"


def fetch() -> dict:
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day, rect.ContributionCalendar-day"):
        date = cell.get("data-date")
        level = cell.get("data-level")
        count_attr = cell.get("data-count")
        if date is None:
            continue
        days.append({
            "date": date,
            "level": int(level) if level is not None else 0,
            "count": int(count_attr) if count_attr is not None else 0,
        })

    days.sort(key=lambda d: d["date"])

    total = sum(d["count"] for d in days)

    # streaks
    current_streak = 0
    longest_streak = 0
    running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0
    # current streak counted from the most recent day backwards
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    best_day = max(days, key=lambda d: d["count"], default=None)

    return {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days,
    }


if __name__ == "__main__":
    data = fetch()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT}  ({len(data['days'])} days, {data['total']} contributions)")
