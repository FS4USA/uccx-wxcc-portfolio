"""
list_users.py
-------------
Lists all Webex Calling-enabled users in the organization and prints a summary
of each user's calling configuration (extension, location, primary number).

Usage:
    export WEBEX_ACCESS_TOKEN=...
    python list_users.py
"""

import os
import sys
from typing import Iterator

import requests
from dotenv import load_dotenv
from tabulate import tabulate

API_BASE = "https://webexapis.com/v1"


def get_token() -> str:
    load_dotenv()
    token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not token:
        sys.exit("ERROR: WEBEX_ACCESS_TOKEN environment variable is required.")
    return token


def paginated_get(url: str, headers: dict, params: dict | None = None) -> Iterator[dict]:
    """Yield items across Webex API pagination (Link: rel=next header)."""
    while url:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        yield from payload.get("items", [])
        # Webex pagination is indicated via the Link header with rel=next
        url = _next_link(resp.headers.get("Link"))
        params = None  # cursor is embedded in the next URL


def _next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        if 'rel="next"' in part:
            return part.split(";")[0].strip().lstrip("<").rstrip(">")
    return None


def list_calling_users(token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    users: list[dict] = []
    for user in paginated_get(f"{API_BASE}/people", headers, params={"max": 100}):
        # Webex Calling users have a 'licenses' entry that maps to a BCS license
        # We fetch the per-user calling details in a follow-up call:
        details = requests.get(
            f"{API_BASE}/telephony/config/people/{user['id']}",
            headers=headers,
            timeout=30,
        )
        if details.status_code == 404:
            continue  # Not a Webex Calling user
        details.raise_for_status()
        d = details.json()
        users.append(
            {
                "Name": user.get("displayName", ""),
                "Email": (user.get("emails") or [""])[0],
                "Extension": d.get("extension", ""),
                "Primary Number": d.get("phoneNumber", ""),
                "Location": d.get("locationName", ""),
            }
        )
    return users


def main() -> None:
    token = get_token()
    users = list_calling_users(token)
    print(f"Found {len(users)} Webex Calling user(s).\n")
    print(tabulate(users, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
