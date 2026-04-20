# UCCX Script Pattern Catalog

I maintain a working library of **100+ UCCX `.aef` scripts** built across real customer environments — internal helpdesks, customer service queues, sales IVRs, skills-based routing, after-hours handling, outage management, and operator-assist flows. Because every `.aef` in that library embeds customer-specific prompts, queue names, PINs, and routing targets, the individual files aren't published here. This catalog instead describes the **patterns** I've implemented repeatedly, with representative walkthroughs in [`examples/`](./examples).

## Pattern coverage

| Pattern | Approx. count in library | Walkthrough |
| --- | --- | --- |
| Main IVR menu (N-option, retry, operator fallback) | 25+ | [01_main_ivr_menu.md](./examples/01_main_ivr_menu.md) |
| Business-hours + holiday-list routing | 15+ | [02_after_hours_routing.md](./examples/02_after_hours_routing.md) |
| Admin-controlled outage / emergency announcement toggle | 10+ | [03_it_helpdesk_with_outage_toggle.md](./examples/03_it_helpdesk_with_outage_toggle.md) |
| Queue with interruptible VM-offer loop | 15+ | [04_customer_service_queue.md](./examples/04_customer_service_queue.md) |
| Skills-based priority queue routing | 10+ | walkthrough planned |
| DID-based branching (multiple numbers, one script) | 10+ | walkthrough planned |
| Courtesy callback offer with DNIS / ANI capture | 5+ | walkthrough planned |
| Operator transfer with call-context attached data | 5+ | walkthrough planned |
| Self-service password reset / account lookup IVR | 5+ | walkthrough planned |
| Conference-bridge pilot with PIN entry | 3+ | walkthrough planned |

## Subflow library

In addition to top-level scripts, I maintain reusable UCCX **subflows** that get called from multiple main scripts to keep logic DRY:

- **`error_handler.aef`** — plays a graceful apology prompt and routes caller to the operator queue on any unhandled exception.
- **`holiday_check.aef`** — reads a central holiday XML list and returns a boolean.
- **`ani_lookup.aef`** — queries a REST endpoint (via HTTP Request step) to resolve the ANI to a customer record, populating call variables for screen-pop.
- **`post_call_survey_offer.aef`** — offers a post-call survey at call end; transfers to a survey collection script on opt-in.
- **`voicemail_transfer.aef`** — standardized Call Redirect to the voicemail pilot with DTMF passthrough for mailbox selection.

## Why a catalog instead of the files

Publishing the individual `.aef` binaries would require opening each in CCX Editor, renaming every customer-specific prompt / queue / variable / PIN / DID, and re-exporting — a process that multiplied across 100+ files is not practical or useful. The representative walkthroughs in [`examples/`](./examples) document the design thinking and logic structure, which is what portfolio reviewers evaluate. On request I can provide a specific sanitized `.aef` tailored to a reviewer's technical interview requirements.
