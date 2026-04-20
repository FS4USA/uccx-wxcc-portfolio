# Webex Contact Center (WxCC)

Sample Webex Contact Center flow work and supporting documentation.

## Contents

- [`flows/`](./flows) — WxCC flow exports (JSON). Sanitized.
- [`examples/`](./examples) — Documented walk-throughs of flow patterns (entry point → queue, skills-based routing, virtual agent integration, callback, EWT announcements).
- [`docs/`](./docs) — Notes on WxCC Flow Designer behavior and design patterns.

## What each flow demonstrates

| Flow file | Pattern demonstrated | Notes |
| --- | --- | --- |
| `main_entry_point.json` | Entry point → welcome → menu → queue. | Generic 4-option menu. |
| `skills_based_routing.json` | NewPhoneContact → SetVariable → QueueContact with SkillRequirements. | Uses generic skill IDs. |
| `virtual_agent_deflection.json` | VirtualAgentV2 block with fallback to live queue. | Placeholder agent config. |
| `estimated_wait_time_announcement.json` | GetQueueInfo + PlayMessage with EWT announcement loop. | |
| `callback_offer.json` | Courtesy callback offer with CallbackNumber capture and scheduled re-contact. | |
| `business_hours.json` | Business Hours + Holiday block routing with after-hours message. | |

> _Actual `.json` flow exports will land in [`flows/`](./flows) after being sanitized. See [examples](./examples) for flow walk-throughs._

## How to import a WxCC flow

1. Log in to **Webex Control Hub** → Contact Center.
2. Go to **Flows** → Create Flow (or open an existing one).
3. Use **Import** and select the `.json` file from this folder.
4. Review referenced entry points, queues, skill profiles, and virtual agent names — these are generic placeholders in this repo and need re-pointing to your tenant's resources before publishing.
5. **Validate** the flow in Flow Designer.
6. **Publish** the flow once validation passes.
