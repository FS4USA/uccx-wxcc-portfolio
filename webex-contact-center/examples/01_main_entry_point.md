# Example: Main Entry Point Flow

A generic Webex Contact Center entry-point flow pattern. Walks through welcome message, menu collection, and queue routing.

## Goal

Greet the caller on a published number, offer a menu, and route to the appropriate queue.

## Variables

| Variable | Type | Purpose |
| --- | --- | --- |
| `Global_MenuSelection` | String | Stores DTMF digit from Menu block. |
| `Global_RetryCount` | Integer | Tracks menu re-prompt attempts. |
| `Global_CustomerANI` | String | Captures the caller's number for later use (screen pop, callback). |

## Block sequence

```
NewPhoneContact
   │
   └─ SetVariable (Global_CustomerANI = {{NewPhoneContact.ANI}})
        │
        └─ PlayMessage (welcome_prompt)
             │
             └─ Menu
                  ├─ "1" Sales   → QueueContact (Queue_Sales)
                  ├─ "2" Support → QueueContact (Queue_Support)
                  ├─ "3" Billing → QueueContact (Queue_Billing)
                  ├─ "0" Operator → QueueContact (Queue_Operator)
                  ├─ No Input   → RetryLogic
                  └─ Invalid   → RetryLogic

RetryLogic
   └─ If (Global_RetryCount < 2):
            Increment Global_RetryCount
            PlayMessage (invalid_selection)
            Loop to Menu
        Else:
            PlayMessage (connecting_operator)
            QueueContact (Queue_Operator)
```

## Design notes

- **Global variables prefixed `Global_`** for readability in Flow Designer.
- **Queue names are descriptive and generic** (`Queue_Sales`, etc.) — in a real tenant they'd be replaced with the customer's actual queue IDs.
- **Retry ceiling of 2** before automatic operator routing, matching the UCCX example's approach.
- **ANI captured early** so downstream blocks (callback offer, CRM screen pop) can reference it without re-prompting.
