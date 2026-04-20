"""
device_inventory.py
-------------------
Pulls a full inventory of calling devices (phones, ATAs, IP DECT, etc.) from
Webex Control Hub via the public Devices API, and outputs firmware + registration
status so you can spot devices running outdated firmware or offline.

Usage:
    export WEBEX_ACCESS_TOKEN=...
    python device_inventory.py --out devices.csv
"""

import argparse
import csv
import os
import sys

import requests
from dotenv import load_dotenv

API_URL = "https://webexapis.com/v1/devices"


def fetch_devices(token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    devices: list[dict] = []
    params = {"max": 100}
    url = API_URL
    while url:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        devices.extend(resp.json().get("items", []))
        # Pagination via Link header
        link = resp.headers.get("Link", "")
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip().lstrip("<").rstrip(">")
        url = next_url
        params = None
    return devices


def main() -> None:
    load_dotenv()
    token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not token:
        sys.exit("ERROR: WEBEX_ACCESS_TOKEN environment variable is required.")

    p = argparse.ArgumentParser()
    p.add_argument("--out", default="devices.csv")
    args = p.parse_args()

    devices = fetch_devices(token)
    if not devices:
        print("No devices returned.")
        return

    fields = ["id", "displayName", "product", "type", "connectionStatus",
              "software", "primarySipUrl", "ip", "mac", "capabilities"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for d in devices:
            w.writerow(d)

    print(f"Wrote {len(devices)} devices to {args.out}")

    # Simple offline summary
    offline = [d for d in devices if d.get("connectionStatus") != "connected"]
    print(f"{len(offline)} device(s) currently NOT connected.")


if __name__ == "__main__":
    main()
