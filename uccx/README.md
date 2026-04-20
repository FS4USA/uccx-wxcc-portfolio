# Cisco UCCX

Sample UCCX (Unified Contact Center Express) script work and supporting documentation.

## Contents

- **[`SCRIPT_CATALOG.md`](./SCRIPT_CATALOG.md)** — Pattern catalog of the 100+ UCCX scripts I've built across customer environments, grouped by pattern type.
- [`examples/`](./examples) — Documented walk-throughs of representative UCCX script patterns (IVR, queue, business-hours, outage toggle, etc.).
- [`docs/`](./docs) — Notes on UCCX behavior, troubleshooting, and design decisions.

> `.aef` binaries are not published in this repo — see [SCRIPT_CATALOG.md](./SCRIPT_CATALOG.md) for the reasoning. The walkthroughs in [`examples/`](./examples) document the logic and design of representative scripts without exposing customer data.

## What each script demonstrates

When a `.aef` is added here, this table will be updated with:

| Script file | Pattern demonstrated | Notes |
| --- | --- | --- |
| `main_ivr_menu.aef` | Top-level IVR with 4-option menu, Get Digit String, Goto, error branch. | Sanitized menu options (Sales / Support / Billing / Operator). |
| `priority_queue_router.aef` | CSQ selection with priority weighting based on dialed number and time of day. | Uses generic CSQ names (`CSQ_TIER1`, `CSQ_TIER2`). |
| `after_hours_routing.aef` | Business-hours check via Holiday List + Day/Time of Day, routes to voicemail outside hours. | Holiday list externalized. |
| `callback_offer.aef` | Queue position estimation + courtesy callback offer with DNIS capture. | |
| `error_handler_subflow.aef` | Reusable subflow for graceful error handling and prompt-playback fallback. | |

> _These are planned example scripts — actual `.aef` files will land in [`scripts/`](./scripts) after being sanitized. See [examples](./examples) for flow logic walk-throughs._

## How to load an `.aef` file

1. Open **Cisco Unified CCX Editor** (matching your UCCX server version).
2. **File → Open** the `.aef` file from this folder.
3. Review referenced prompts, variables, and subflow paths — these are generic in this repo and will need re-pointing to your environment's resources before upload.
4. Upload to the CCX server: **Applications → Script Management → Upload New Scripts**.
5. Associate with an Application under **Applications → Application Management**.
