# Example: IT Helpdesk with Emergency / Outage Toggle

A UCCX script pattern for an internal IT helpdesk queue with an admin-controlled "emergency/outage on" announcement toggle. Callers hear a temporary outage message before being queued when an outage is in progress.

## Goal

- Callers hitting the IT helpdesk DID land on a greeting.
- If an active outage flag is set, play a recorded outage announcement before continuing to the agent queue.
- Provide an in-band way for an admin to toggle the outage state (option 1: toggle ON and record prompt, option 2: toggle OFF) without requiring CCX Editor access.
- Queue the caller to the IT helpdesk CSQ with standard error/fallback handling.

## Variables

| Name | Type | Purpose |
| --- | --- | --- |
| `outageActive` | boolean | Read from an external XML document so the state survives script re-deploys. |
| `outagePromptURI` | String | URI of the uploaded outage announcement prompt. |
| `adminPIN` | String | Short PIN verified before allowing toggle-on/off. |
| `menuSelection` | String | DTMF digit from Get Digit String. |

## Block sequence

```
Start
 └─ Accept
     └─ Create XML Document (reads outage_state.xml)
         └─ Get XML Document Data (→ outageActive)
             ├─ outageActive = true
             │   └─ Play Prompt (outagePromptURI)
             │       └─ Continue to Queue
             └─ outageActive = false
                 └─ Play Prompt (standard_greeting.wav)
                     └─ Continue to Queue

Queue:
  Select Resource from CSQ_IT_Helpdesk
    ├─ Connected → Disconnect (agent handles)
    └─ Queued → Play MoH/position prompts

Admin toggle sub-menu (reached via special DTMF/DID):
  Get Digit String "Enter admin PIN"
    ├─ PIN match → Present toggle menu
    │     "1" → Toggle outage ON + Record new announcement → save outage_state.xml
    │     "2" → Toggle outage OFF → save outage_state.xml
    └─ PIN mismatch → Play error, disconnect
```

## Design decisions

- **External XML for state** — keeps outage on/off persistent across script redeploys and visible to anyone with server access, rather than hardcoding booleans in the script.
- **Admin-recorded prompt** — the toggle-on path lets the admin record the actual outage message by phone, so they don't need a studio or CCX Editor access to push a timely announcement during an incident.
- **Short PIN gate** — prevents accidental or malicious toggling if the admin DID/extension is discovered. PIN is configured outside the script.
- **Graceful fallback** — if the XML document is missing or unreadable, the script defaults to `outageActive = false` and continues to the standard greeting, so a missing file never blocks callers from reaching the queue.

## Why this pattern is useful

During active IT incidents, the quickest way to reduce ticket volume is to proactively tell callers "yes, we know, we're working on it." A self-service recorded announcement toggle lets ops teams deploy that message in under two minutes without pulling a contact-center engineer into the incident.
