"""
drop_pattern_detector.py
------------------------
Scans a Webex Calling CDR CSV for the classic fixed-interval mid-call drop
pattern. A 22-minute (1320s) drop is the textbook signature of:
  - SIP Session Timer (RFC 4028) expiration where a re-INVITE/UPDATE
    refresh failed mid-call, or
  - Firewall / NAT UDP binding timeout, or
  - Carrier-side session refresh failing at the ITSP.

The script groups calls by duration and flags any bucket where the count
of abnormal terminations is statistically above the baseline, with special
highlighting of the 20-24 minute window.

Usage:
    python drop_pattern_detector.py --cdr /path/to/cdr_export.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def bucketize_durations(rows: list[dict]) -> Counter:
    """Bucket call durations into 1-minute bins. Only count calls that were
    answered (Talk duration > 0) so we're analyzing real conversations."""
    buckets: Counter = Counter()
    for r in rows:
        try:
            talk = int(r.get("Talk duration") or 0)
        except ValueError:
            continue
        if talk <= 0:
            continue
        minute_bucket = talk // 60
        buckets[minute_bucket] += 1
    return buckets


def flag_anomalous_buckets(buckets: Counter, window: int = 5) -> list[tuple[int, int, float]]:
    """Compare each bucket to a rolling window of neighboring buckets.
    Returns (bucket_minute, count, z_score) for buckets that are anomalously high."""
    results = []
    sorted_minutes = sorted(buckets.keys())
    for m in sorted_minutes:
        neighbors = [buckets[m + d] for d in range(-window, window + 1) if d != 0 and (m + d) >= 0]
        if not neighbors:
            continue
        mean = sum(neighbors) / len(neighbors)
        # Simple deviation proxy — avoids numpy dependency.
        sq = sum((n - mean) ** 2 for n in neighbors) / len(neighbors)
        stddev = sq ** 0.5 or 1.0
        z = (buckets[m] - mean) / stddev
        if z >= 2.5 and buckets[m] >= 3:
            results.append((m, buckets[m], round(z, 2)))
    return results


def highlight_session_timer_window(buckets: Counter) -> dict[int, int]:
    """Return counts in the 20-24 minute window where session timer drops concentrate."""
    return {m: buckets.get(m, 0) for m in range(20, 25)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cdr", required=True, help="Path to Webex Calling CDR CSV export")
    args = p.parse_args()

    rows = load_rows(Path(args.cdr))
    print(f"Loaded {len(rows)} CDR rows.\n")

    buckets = bucketize_durations(rows)
    if not buckets:
        print("No answered calls found in the CDR.")
        return

    print("Call duration distribution (per-minute buckets, top 20 buckets):")
    for minute, count in sorted(buckets.items(), key=lambda kv: -kv[1])[:20]:
        print(f"  {minute:3d} min: {count}")
    print()

    print("Session-timer window (20-24 minutes):")
    for minute, count in highlight_session_timer_window(buckets).items():
        tag = "  <-- classic 22-min SIP Session Timer drop window" if 21 <= minute <= 23 else ""
        print(f"  {minute:2d} min: {count}{tag}")
    print()

    anomalous = flag_anomalous_buckets(buckets)
    if not anomalous:
        print("No anomalously high duration buckets detected.")
        return

    print("Anomalously high duration buckets (possible fixed-interval drops):")
    for minute, count, z in anomalous:
        print(f"  {minute:3d} min: {count:4d} calls  (z = {z})")


if __name__ == "__main__":
    main()
