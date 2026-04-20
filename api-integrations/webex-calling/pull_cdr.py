"""
pull_cdr.py
-----------
Pulls Webex Calling Detailed Call History for a given time window and writes
the result to a sanitized CSV. Useful for call-quality and drop investigations.

Reference: https://developer.webex.com/docs/api/v1/detailed-call-history

Usage:
    export WEBEX_ACCESS_TOKEN=...
    python pull_cdr.py --start 2026-04-01T00:00:00.000Z --end 2026-04-02T00:00:00.000Z --out cdr.csv
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

API_URL = "https://analytics.webexapis.com/v1/cdr_feed"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pull Webex Calling CDRs for a time window.")
    p.add_argument("--start", required=True, help="ISO8601 UTC start (e.g. 2026-04-01T00:00:00.000Z)")
    p.add_argument("--end", required=True, help="ISO8601 UTC end")
    p.add_argument("--out", default="cdr.csv", help="Output CSV path (default: cdr.csv)")
    return p.parse_args()


def fetch_cdrs(token: str, start: str, end: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    params = {"startTime": start, "endTime": end}
    rows: list[dict] = []
    url = API_URL
    while url:
        resp = requests.get(url, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        rows.extend(data.get("items", []))
        url = data.get("next")
        params = None
    return rows


def main() -> None:
    load_dotenv()
    token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not token:
        sys.exit("ERROR: WEBEX_ACCESS_TOKEN environment variable is required.")

    args = parse_args()
    print(f"Fetching CDRs {args.start} → {args.end} ...")
    rows = fetch_cdrs(token, args.start, args.end)
    if not rows:
        print("No records returned for that window.")
        return

    # Write whatever fields came back (schema varies by org licensing)
    fieldnames = sorted({k for r in rows for k in r.keys()})
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
