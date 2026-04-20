# API Integrations

Python examples for automating and reporting against Cisco collaboration APIs.

## Subfolders

- [`webex-calling/`](./webex-calling) — Webex Calling user/device lookups, line configuration, CDR pulls.
- [`control-hub/`](./control-hub) — Control Hub admin-level operations (org-wide reports, device inventory).
- [`uccx-rest/`](./uccx-rest) — UCCX REST API examples (real-time stats, historical reporting).

## Running the examples

Each example is a standalone Python script. Dependencies are captured per-script, but a consolidated `requirements.txt` is provided here:

```bash
pip install -r requirements.txt
```

## Authentication

All examples expect credentials via environment variables, **never** hardcoded. Copy `.env.example` to `.env` and populate.

| Variable | Used by | Notes |
| --- | --- | --- |
| `WEBEX_ACCESS_TOKEN` | Webex Calling + Control Hub scripts | Personal access token or bot token. For production, use a service app OAuth token. |
| `WEBEX_ORG_ID` | Control Hub scripts | UUID of your org. |
| `UCCX_HOST` | UCCX REST scripts | FQDN or IP of UCCX server. |
| `UCCX_USER`, `UCCX_PASS` | UCCX REST scripts | Admin/reporting user credentials. Basic Auth. |
