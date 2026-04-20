"""
per_user_quality_summary.py
---------------------------
Summarize a Webex Calling CDR export into per-user quality statistics and
flag users with anomalous patterns. Useful after a complaint like
"some users can't place outbound calls" or "user X keeps dropping calls."

Produces:
  - answered vs unanswered counts per user
  - avg + p95 call duration per user
  - count of abnormal release reasons per user (anything not Normal/Success)
  - ratio of each user's abnormal calls vs their total

Usage:
    python per_user_quality_summary.py --cdr /path/to/cdr_export.csv --out summary.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = (len(values) - 1) * p
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[f]
    return values[f] + (values[c] - values[f]) * (k - f)


def summarize(rows: list[dict]) -> list[dict]:
    by_user: dict[str, dict] = defaultdict(
        lambda: {"total": 0, "answered": 0, "durations": [], "abnormal": 0}
    )
    for r in rows:
        user = r.get("User name") or "(unknown)"
        bucket = by_user[user]
        bucket["total"] += 1
        if (r.get("Answered") or "").upper().startswith("TRUE"):
            bucket["answered"] += 1
        try:
            dur = int(r.get("Duration") or 0)
            if dur > 0:
                bucket["durations"].append(dur)
        except ValueError:
            pass
        outcome = (r.get("Call outcome") or "").strip()
        reason = (r.get("Call outcome reason") or "").strip()
        if outcome not in ("Success", "") or reason not in ("Normal", "NoAnswer", ""):
            bucket["abnormal"] += 1

    rows_out = []
    for user, b in by_user.items():
        durs = b["durations"]
        rows_out.append({
            "User": user,
            "Total calls": b["total"],
            "Answered": b["answered"],
            "Answer rate": f"{b['answered'] / b['total']:.1%}" if b["total"] else "-",
            "Avg duration (s)": f"{mean(durs):.1f}" if durs else "-",
            "p95 duration (s)": f"{percentile(durs, 0.95):.0f}" if durs else "-",
            "Abnormal count": b["abnormal"],
            "Abnormal ratio": f"{b['abnormal'] / b['total']:.1%}" if b["total"] else "-",
        })
    rows_out.sort(key=lambda r: r["Total calls"], reverse=True)
    return rows_out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cdr", required=True)
    p.add_argument("--out", default="per_user_summary.csv")
    args = p.parse_args()

    rows = load_rows(Path(args.cdr))
    summary = summarize(rows)
    if not summary:
        print("No users found in CDR.")
        return

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)

    print(f"Wrote per-user summary for {len(summary)} user(s) to {args.out}")
    # Pretty-print top 10 to stdout
    print("\nTop 10 users by call volume:")
    header = list(summary[0].keys())
    print("  " + " | ".join(h.ljust(18) for h in header))
    for r in summary[:10]:
        print("  " + " | ".join(str(r[h]).ljust(18) for h in header))


if __name__ == "__main__":
    main()
