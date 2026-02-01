# REST API

ZTRAP optionally exposes a simple Flask REST API to access Nuclei scan metadata and logs. This service is disabled by default and should only be enabled on trusted hosts or within private networks.

## Enable

Set environment variable:

- `ZTRAP_ENABLE_REST=1` — starts the REST API server on import in a background thread.
- `ZTRAP_REST_HOST` — host to bind (default: `127.0.0.1`).
- `ZTRAP_REST_PORT` — port to bind (default: `8766`).
- `ZTRAP_REST_TOKEN` — optional bearer token to protect endpoints. If set, requests must include `Authorization: Bearer <token>`.

## Endpoints

- `GET /health` — returns `{ "status": "ok" }`.
- `GET /scans` — lists scans from the Nuclei DB (optional `target` query parameter for filtering).
- `GET /scans/<scan_id>/log` — returns the raw log for a scan (returns 404 if not found).
- `GET /scans/<scan_id>/status` — returns parsed JSON status file for the scan or `{ "finished": false }` if missing.

## Security

- Keep the REST API bound to `127.0.0.1` unless you have secure networking in place.
- Use `ZTRAP_REST_TOKEN` to require a bearer token for requests.
