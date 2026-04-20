"""
poor_call_leg_report.py
-----------------------
Rank Webex Calling users by proportion of "poor" call legs. Usage scenario:
you suspect a few users on bad cabling/switch ports are dragging down
overall quality — this surfaces the worst offenders so physical review
can be prioritized.

Note: Detailed Call History CSV does not always include MOS/jitter per call
out of the box; some fields require the org to have Media Quality Feed
enabled. This script handles either case — if jitter/packet-loss columns
are absent it falls back to abnormal-call-ratio as a proxy.

Usage:
    python poor_call_leg_report.py --cdr /path/to/cdr.csv --out poor_users.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def classify_leg(row: dict) -> bool:
    """Return True if this call leg is 'poor' by available signals."""
    # Prefer explicit MOS / jitter / packet-loss if present.
    try:
        jitter = float(row.get("Rx Jitter") or row.get("Jitter") or 0)
        loss = float(row.get("Rx Packet Loss") or row.get("Packet Loss") or 0)
        mos = float(row.get("MOS") or 0)
    except ValueError:
        jitter = loss = mos = 0
    if jitter > 30 or loss > 2 or (0 < mos < 3.5):
        return True
    # Fallback: count abnormal terminations as a poor-quality proxy.
    outcome = (row.get("Call outcome") or "").strip()
    reason = (row.get("Call outcome reason") or "").strip()
    return outcome not in ("Success", "") or reason not in ("Normal", "NoAnswer", "")


def rank(rows: list[dict]) -> list[dict]:
    by_user: dict[str, dict] = defaultdict(lambda: {"total": 0, "poor": 0})
    for r in rows:
        user = r.get("User name") or "(unknown)"
        by_user[user]["total"] += 1
        if classify_leg(r):
            by_user[user]["poor"] += 1
    out = []
    for user, v in by_user.items():
        if v["total"] < 5:
            continue  # ignore sparse data
        pct = v["poor"] / v["total"]
        out.append({"User": user, "Total legs": v["total"], "Poor legs": v["poor"], "Poor %": f"{pct:.1%}", "_pct_sort": pct})
    out.sort(key=lambda r: r["_pct_sort"], reverse=True)
    for r in out:
        r.pop("_pct_sort", None)
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cdr", required=True)
    p.add_argument("--out", default="poor_users.csv")
    args = p.parse_args()

    rows = load_rows(Path(args.cdr))
    ranked = rank(rows)
    if not ranked:
        print("Not enough data to produce a ranking.")
        return

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(ranked[0].keys()))
        w.writeheader()
        w.writerows(ranked)
    print(f"Wrote poor-call-leg ranking for {len(ranked)} user(s) to {args.out}")

    print("\nTop 10 users by poor-leg ratio:")
    for r in ranked[:10]:
        print(f"  {r['User']:30s}  total={r['Total legs']:4d}  poor={r['Poor legs']:4d}  ({r['Poor %']})")


if __name__ == "__main__":
    main()
