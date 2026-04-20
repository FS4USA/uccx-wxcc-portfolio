# Sanitization Rules

Every artifact in this repo has been sanitized before commit. The rules below define the substitutions applied. Violations of these rules must never reach `main`.

## What gets stripped

| Real value class | Example (do NOT commit) | Replacement pattern |
| --- | --- | --- |
| Customer / company name | `BankEasy`, `Bank With Choice`, specific bank / credit union name | `Customer A`, `ExampleBank`, `ExampleCorp` |
| Customer email domain | `@bankeasy.com`, `@bankwithchoice.com`, `@marconet.com` | `@example.com` |
| Personal email | `Will.Davidson@bankeasy.com`, `jim.pilgrim@marconet.com` | `user1@example.com`, `user2@example.com`, ... |
| Real phone numbers (E.164) | `+15551234567`, `+17175550100`, or 11-digit `1NXXNXXXXXX` | `+15550100001`, `+15550100002`, ... |
| Real extensions | `4016`, `5448`, `4020` | `1001`, `1002`, `1003` |
| Voicemail pilots | Customer-specific | `8999` (generic) |
| IP addresses | `10.71.101.46`, `96.86.254.700`, `66.86.0.83` | `10.0.0.1` (RFC1918 generic) |
| MAC addresses | `805E0C0320F8` | `aa:bb:cc:dd:ee:ff` |
| UUIDs (tenant / org / flow / user) | any real GUID | deterministic fake UUID per file, stable mapping preserves referential integrity |
| Vendor product names tied to client | `Jack Henry`, `JHA`, `Symitar`, `Episys` | `CoreSystem` |
| Customer-branded flow / queue / app names | `BusinessSolutions`, `CashMgmt`, `Wires` | `BusinessServices`, `AccountServices`, `WireTransfer` |
| Host names / FQDNs | `uccx01.somebank.internal` | `uccx01.example.lab` |
| Holiday lists / schedules with customer dates | specific customer calendar | generic US federal holiday list |
| Recorded prompt file names referencing customer | `SomeBankWelcome.wav` | `welcome.wav` |

## How sanitization is enforced

- **WxCC flow JSON** is run through [`sanitize_flows.py`](../../sanitize_flows.py) (shipped in the repo root for reference), which applies deterministic regex substitutions and validates the output is still parseable JSON.
- **UCCX `.aef`** binaries are **not published**. The `.aef` file format is Java-serialized binary data, which cannot be safely text-edited. Instead, representative script patterns are documented as walkthroughs under [`uccx/examples/`](../uccx/examples). See [`uccx/SCRIPT_CATALOG.md`](../uccx/SCRIPT_CATALOG.md) for the reasoning.
- **Python / integration code** uses environment variables (`.env`) for all credentials. The `.gitignore` blocks `.env`, PEM keys, and any `*_unsanitized.*` or `/raw/` content from ever being tracked.

## Double-check before commit

Before pushing any change, scan for leftover real data:

```bash
# Look for email addresses not ending in example.com
grep -rEn "[A-Za-z0-9._%+-]+@(?!example\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}" .

# Look for phone numbers not in the 555 range
grep -rEn "\+1[2-9]\d{9}" .

# Look for known customer brand tokens
grep -rEin "jack ?henry|jha|symitar|episys|bankeasy|bankwithchoice|marconet|cashmgmt|businesssolutions" .
```

Any hit from those greps is a bug and must be fixed before the commit is allowed to merge.
