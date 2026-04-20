# UCCX Script Walkthroughs

Documented examples of common UCCX script patterns. Each walkthrough describes the goal, variables, block sequence, and design decisions — enough that a reviewer understands the approach without needing CCX Editor.

| # | Walkthrough | Pattern |
| --- | --- | --- |
| 01 | [Main IVR Menu](./01_main_ivr_menu.md) | Greeting + 4-option menu + retry/error handling. |
| 02 | [After-Hours Routing](./02_after_hours_routing.md) | Business hours + holiday check + VM fallback. |
| 03 | [IT Helpdesk with Outage Toggle](./03_it_helpdesk_with_outage_toggle.md) | Admin-controlled recorded outage announcement. |
| 04 | [Customer Service Queue with VM Fallback](./04_customer_service_queue.md) | Queue + periodic VM-offer loop. |

## Why documentation-only (no `.aef` binaries)

UCCX `.aef` scripts are Java-serialized binaries that cannot be safely text-edited (doing so breaks serialization lengths). Sanitizing a real client `.aef` for public release requires opening it in CCX Editor and renaming every customer-specific prompt / queue / variable manually before re-exporting. These walkthroughs demonstrate the script logic and design thinking, which is typically what portfolio reviewers care about — and they're readable without needing CCX Editor installed.
