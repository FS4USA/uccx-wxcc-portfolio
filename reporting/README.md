# Reporting & CDR Analysis

Scripts for parsing Webex Calling CDR exports and doing practical troubleshooting — not just generic "sum calls by day" reports, but the kinds of queries you actually need when a user hands you "calls keep dropping."

## Scripts

- [`cdr-analysis/drop_pattern_detector.py`](./cdr-analysis/drop_pattern_detector.py) — Scans a CDR export for fixed-interval mid-call drops (classic 22-minute SIP Session Timer / firewall NAT-timeout pattern).
- [`cdr-analysis/per_user_quality_summary.py`](./cdr-analysis/per_user_quality_summary.py) — Aggregates a CDR export into per-user summaries (answer rate, avg duration, abnormal releases), flagging users with anomalous patterns.
- [`call-quality/poor_call_leg_report.py`](./call-quality/poor_call_leg_report.py) — Given a CDR export and a jitter/packet-loss threshold, lists users whose call legs exceed the threshold so you know who to prioritize for network/device review.

## Input format

All scripts accept the Webex Control Hub → Analytics → Calling → Detailed Call History CSV export. Column names match the public Webex schema (`Start time`, `Direction`, `Calling number`, `Called number`, `Duration`, `Releasing party`, `Call outcome`, etc.).
