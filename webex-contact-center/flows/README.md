# WxCC Flow Exports (`.json`)

This folder will hold sanitized Webex Contact Center flow JSON files.

## Sanitization applied before commit

| Real value (stripped) | Placeholder used |
| --- | --- |
| Tenant / org UUID | `00000000-0000-0000-0000-000000000000` |
| Flow UUID | `11111111-1111-1111-1111-111111111111` |
| Entry point ID / name referencing customer | `EP_Main`, `EP_Sales` |
| Queue names referencing customer | `Queue_Sales`, `Queue_Support` |
| Skill profile names referencing customer | `Skill_English_Tier1`, etc. |
| Published DIDs | `+1-555-0100` range |
| Virtual agent IDs | `00000000-0000-0000-0000-000000000000` |
| Audio file URLs / names | `welcome_prompt`, `menu_options`, etc. |
| Agent / team names | `Team_Sales`, `Team_Support` |
| Business-hours schedule names | `Hours_Default`, `Holidays_Default` |

## Exporting a flow from Webex Control Hub

1. **Control Hub → Contact Center → Flows**.
2. Open the target flow.
3. **⋯ menu → Export**. This downloads a `.json` representation.
4. Run through the sanitizer (see [`docs/SANITIZATION.md`](../../docs/SANITIZATION.md)) before placing it in this folder.
