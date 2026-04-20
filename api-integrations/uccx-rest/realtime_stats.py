"""
realtime_stats.py
-----------------
Polls the UCCX Real-Time Reporting API for a queue snapshot:
calls waiting, longest wait time, agents ready, agents talking, etc.

UCCX exposes both a SOAP interface (older) and an HTTPS REST endpoint via
the Finesse/CUIC stack. This script targets the RTR REST endpoint and falls
back to basic auth with a reporting user.

Usage:
    export UCCX_HOST=uccx01.example.lab
    export UCCX_USER=reporting_user
    export UCCX_PASS=...
    python realtime_stats.py --csq CSQ_Support
"""

import argparse
import os
import sys

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


def fetch_csq_stats(host: str, user: str, password: str, csq_name: str) -> dict:
    # UCCX RTR endpoint — path varies by version; this is the common 12.x path.
    url = f"https://{host}:8443/realtimeservice2/services/RealtimeReportingService"
    headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

    soap = f"""<?xml version="1.0"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
      <soap:Body>
        <getCSQStats xmlns="http://realtimeservice.uccx.cisco.com">
          <csqName>{csq_name}</csqName>
        </getCSQStats>
      </soap:Body>
    </soap:Envelope>"""

    resp = requests.post(
        url,
        data=soap,
        headers=headers,
        auth=HTTPBasicAuth(user, password),
        verify=False,  # self-signed in most labs; in prod, pin the CA bundle
        timeout=30,
    )
    resp.raise_for_status()
    return _parse_csq_response(resp.text)


def _parse_csq_response(xml_body: str) -> dict:
    # Minimal XML parsing using the stdlib. For production, prefer lxml with
    # proper XSD validation of the SOAP response.
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_body)
    ns = {"soap": "http://www.w3.org/2003/05/soap-envelope"}
    body = root.find("soap:Body", ns)
    result: dict[str, str] = {}
    if body is not None:
        for element in body.iter():
            tag = element.tag.split("}")[-1]  # strip namespace
            if element.text and element.text.strip():
                result[tag] = element.text.strip()
    return result


def main() -> None:
    load_dotenv()
    host = os.getenv("UCCX_HOST")
    user = os.getenv("UCCX_USER")
    password = os.getenv("UCCX_PASS")
    if not all([host, user, password]):
        sys.exit("ERROR: UCCX_HOST, UCCX_USER, UCCX_PASS environment variables are required.")

    p = argparse.ArgumentParser()
    p.add_argument("--csq", required=True, help="CSQ name to query")
    args = p.parse_args()

    stats = fetch_csq_stats(host, user, password, args.csq)
    print(f"Real-time stats for CSQ '{args.csq}':")
    for k, v in stats.items():
        print(f"  {k:28s} {v}")


if __name__ == "__main__":
    main()
