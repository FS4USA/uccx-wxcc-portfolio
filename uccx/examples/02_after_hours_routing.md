# Example: After-Hours / Business Hours Routing

A UCCX script pattern that checks business hours and holiday lists before routing to a live queue, and falls through to voicemail when outside hours.

## Goal

- During business hours → route to main IVR menu.
- Outside business hours → play closed-hours prompt and route to voicemail.
- On observed holidays → play holiday prompt and route to voicemail.

## Variables

| Name | Type | Purpose |
| --- | --- | --- |
| `isHoliday` | boolean | Set by a check against the Holiday List. |
| `isBusinessHours` | boolean | Set by Day of Week / Time of Day check. |
| `vmExtension` | String | Generic voicemail pilot (`8999` in this example). |

## Flow summary

```
Start
 └─ Accept
     └─ Check Holiday (references holiday_list.xml)
         ├─ isHoliday = true
         │   └─ Play Prompt: holiday_closed.wav
         │       └─ Call Redirect → vmExtension
         │
         └─ isHoliday = false
             └─ Day of Week + Time of Day Check
                 ├─ isBusinessHours = true
                 │   └─ Call Subflow: main_ivr_menu.aef
                 │
                 └─ isBusinessHours = false
                     └─ Play Prompt: after_hours.wav
                         └─ Call Redirect → vmExtension
```

## Holiday list

The Holiday List is maintained outside of the script (in `holiday_list.xml` on the CCX server) so business can update holidays without a script redeploy. The script loads the file at runtime via a Create File Document step.

## Notes

- Business hours in this example are Mon–Fri 08:00–17:00 local time. In a real deployment the Day/Time of Day step is configured via CCX Editor's time ranges.
- The voicemail pilot (`8999`) is a generic internal number; in a real environment this would be the customer's Unity Connection or Webex Calling voicemail retrieval pilot.
