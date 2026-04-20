# WxCC Flow JSON Exports

These are sanitized Webex Contact Center flow exports. All real UUIDs, phone numbers, email addresses, org IDs, and customer brand references have been replaced with generic placeholders per [`docs/SANITIZATION.md`](../../docs/SANITIZATION.md).

| File | Pattern demonstrated |
| --- | --- |
| [`main_contact_center_flow.json`](./main_contact_center_flow.json) | Top-level entry-point flow with welcome, menu, and routing to business-unit queues. |
| [`customer_support_with_callback.json`](./customer_support_with_callback.json) | Customer support entry point with BRE (Business Rules Engine) lookup and courtesy callback offer. Large, feature-rich flow. |
| [`courtesy_callback.json`](./courtesy_callback.json) | Dedicated courtesy callback flow — captures callback number, schedules outbound re-contact, handles retries. |
| [`business_services_queue.json`](./business_services_queue.json) | Business-services vertical queue flow with priority routing and dedicated overflow handling. |
| [`wire_transfer_queue.json`](./wire_transfer_queue.json) | Specialty queue flow for a sensitive transaction type — stricter identity-verification prompts before agent connect. |
| [`core_system_callback.json`](./core_system_callback.json) | Callback flow integrated with a back-office core system lookup for customer context. |

## How to import

In Webex Control Hub:

1. **Contact Center → Flows → Create Flow**.
2. Use the **Import** option and select the target JSON file.
3. Re-point generic entry point / queue / skill names to your tenant's resources.
4. Validate, then Publish.
