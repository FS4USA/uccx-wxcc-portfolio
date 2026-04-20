# Example: Customer Service Queue with Voicemail Fallback

A UCCX script pattern for a customer service queue that offers queued callers the option to transfer to voicemail rather than keep holding. This is a good example of respecting caller time while still giving the business a recovery path for missed calls.

## Goal

- Queue the caller to the customer service CSQ.
- While queued, periodically offer: "Press 1 to leave a voicemail, or stay on the line."
- On digit "1", transfer to a voicemail pilot.
- On no input, continue queueing.

## Variables

| Name | Type | Purpose |
| --- | --- | --- |
| `maxQueueOfferLoops` | int | Caps how many times we offer the VM option before giving up (default 5). |
| `vmExtension` | String | Generic voicemail pilot extension. |
| `offerInterval` | int | Seconds between offers while queued (default 60). |

## Block sequence

```
Start
 └─ Accept
     └─ Play Prompt: welcome.wav
         └─ Select Resource from CSQ_CustomerService
             ├─ Connected   → Agent handles
             └─ Queued      → Enter offer loop

Offer loop (Looping step with counter):
  ├─ Play Prompt: "press_1_for_vm.wav" (interruptible)
  │     ├─ Caller presses 1  → Call Redirect → vmExtension (success path)
  │     └─ No input          → Play MoH for offerInterval seconds → Loop
  └─ Loop exit (counter == maxQueueOfferLoops) → Stay in queue (no more offers)
```

## Design decisions

- **Interruptible prompts** — the "press 1 for VM" prompt uses Get Digit String with a short timeout so the caller isn't stuck listening if they want to keep holding. Digit buffer collects in the background.
- **Offer ceiling** — after `maxQueueOfferLoops`, the script stops offering the VM option; the caller has clearly chosen to wait and further offers become annoying.
- **Music on hold between offers** — no dead air between offers, caller still hears MoH and position announcements from the queue configuration.
- **Call Redirect to VM pilot** — redirect rather than blind-transfer so the call leaves the queue cleanly and frees up the agent pool.

## Why this pattern is useful

Contact centers that only offer "your call is important to us" music-on-hold give callers no graceful exit. Offering an explicit "leave a voicemail and we'll call you back" option during queue improves both caller experience (they feel in control) and business outcomes (missed calls become trackable voicemails with a callback number, rather than abandoned calls).
