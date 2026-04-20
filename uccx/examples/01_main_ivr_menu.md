# Example: Main IVR Menu

A generic top-level IVR script pattern for UCCX. This walkthrough documents the logical structure of a `main_ivr_menu.aef` script so a reviewer can understand the approach without needing CCX Editor open.

## Goal

Greet the caller, offer a 4-option menu, and route to the appropriate Contact Service Queue (CSQ) based on the caller's digit selection. Handle no-input and invalid-input cases gracefully.

## Variables

| Name | Type | Scope | Purpose |
| --- | --- | --- | --- |
| `callContact` | Contact | In | Implicit inbound contact. |
| `menuSelection` | String | Local | Holds the DTMF digit returned by Get Digit String. |
| `retryCount` | int | Local | Tracks how many times we've re-prompted the caller. Default: 0. |
| `maxRetries` | int | Local | Retry ceiling before sending to operator. Default: 2. |

## Flow summary

```
Start
 └─ Accept
     └─ Play Prompt: welcome.wav
         └─ Get Digit String: "menu_options.wav"  (max digits 1, timeout 5s)
             ├─ Successful → Switch on menuSelection
             │   ├─ "1" → Call Subflow: sales_queue.aef
             │   ├─ "2" → Call Subflow: support_queue.aef
             │   ├─ "3" → Call Subflow: billing_queue.aef
             │   ├─ "4" → Goto: operator_transfer
             │   └─ default → Increment retryCount, loop or fail
             ├─ Timeout  → Increment retryCount, loop or fail
             └─ Unsuccessful → Goto: error_handler
```

## Retry logic

```
If (retryCount < maxRetries):
    retryCount = retryCount + 1
    Play Prompt: invalid_selection.wav
    Loop back to Get Digit String
Else:
    Play Prompt: connecting_operator.wav
    Call Subflow: operator_transfer.aef
```

## Error handling

Any unhandled exception branches to the reusable `error_handler_subflow.aef`, which plays a generic apology prompt and routes the caller to the operator queue. This prevents dead-air / dropped-call customer experience when an unexpected condition (e.g., prompt missing, variable null) occurs.

## Design decisions

- **Single entry point:** All routing happens from one script rather than having the AA route directly to multiple applications, so retry/error behavior is consistent across menu options.
- **Subflows per queue:** Each menu option invokes a subflow rather than inlining queue logic, which keeps the main IVR readable and lets queue-specific logic (skills, priority) be maintained independently.
- **Retry ceiling:** Caps re-prompting at 2 attempts to avoid looping the caller indefinitely if they're on a pulse-dial or rotary phone.
- **Generic prompts:** Prompts are named descriptively (`welcome.wav`, `menu_options.wav`) rather than with customer branding, so the same script can be repurposed.
