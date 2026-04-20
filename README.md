# UCCX & Webex Contact Center Portfolio

A working library of scripts, flows, integrations, and reporting tooling I've built while administering and troubleshooting Cisco UCCX and Webex Contact Center environments. This repo is intended as a portfolio of my hands-on work in the Cisco collaboration / contact center space.

**Author:** Jim Pilgrim ([FS4USA](https://github.com/FS4USA))
**Focus areas:** Cisco UCCX, Webex Contact Center, Webex Calling, call quality troubleshooting, CDR analysis, API automation.

---

## What's in here

| Section | Contents |
| --- | --- |
| [`uccx/`](./uccx) | UCCX script (`.aef`) examples, documented call flow logic, and IVR/queue/error-handling patterns. |
| [`webex-contact-center/`](./webex-contact-center) | Webex Contact Center flow JSON exports, flow documentation, and integration examples. |
| [`api-integrations/`](./api-integrations) | Python examples against the Webex APIs, Control Hub, and UCCX REST/AXL for automation and reporting. |
| [`reporting/`](./reporting) | CDR parsing, call-quality analysis, and fixed-interval drop detection scripts. |
| [`docs/`](./docs) | Sanitization guide, style notes, and reference material. |

## Skills demonstrated

- Cisco UCCX script design (`.aef`): prompts, variables, queue handling, call routing, error branches.
- Webex Contact Center flow design: entry points, queues, virtual agents, business hours, routing strategies.
- Webex Calling administration and troubleshooting: Control Hub analytics, CDR interpretation, session-timer and NAT-related drop diagnosis.
- API automation: Webex APIs, Control Hub Admin APIs, UCCX REST/XML APIs.
- Call-quality analysis: jitter, packet loss, MOS, fixed-interval drop pattern detection (e.g., the classic 22-minute SIP Session Timer teardown).
- Carrier troubleshooting coordination (GRM, Lumen, Peerless, generic ITSP patterns).

## A note on client data

**Every artifact in this repo has been sanitized.** Real customer names, phone numbers, extensions, user names, MAC addresses, IP addresses, UUIDs, hostnames, and any other identifying information have been replaced with generic placeholders (`Customer A`, `+1-555-0100`, `ext. 1001`, `aa:bb:cc:dd:ee:ff`, `10.0.0.0/24`, `00000000-0000-0000-0000-000000000000`, etc.). See [`docs/SANITIZATION.md`](./docs/SANITIZATION.md) for the exact substitution rules I apply.

## License

Released under the MIT License. See [LICENSE](./LICENSE).
