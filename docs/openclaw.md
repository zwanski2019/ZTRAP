# OpenClaw (Moltbot) Integration — ZTRAP

This document explains the **safe** integration between ZTRAP and OpenClaw (formerly Moltbot).

Key points
- ZTRAP provides a *bridge* that lets operators inspect installation instructions and prepare an installer for local review.
- **ZTRAP will not execute remote installers or start agent gateways for you.** All operational steps must be performed by the human operator on a machine they control.
- A simulation mode is available for development and CI: set `ZTRAP_OPENCLAW_SIMULATE=1` to avoid network access and system changes.

Environment variables
- `ZTRAP_ENABLE_OPENCLAW=1` — enable the OpenClaw UI controls in ZTRAP.
- `ZTRAP_OPENCLAW_SIMULATE=1` — enable simulation mode (safe for CI/test).

Commands provided in the UI
- Safe install instructions (review-first) — contains curl commands but recommends downloading and reviewing prior to execution.
- `Download installer for review (dry-run)` — downloads the installer to `/tmp/openclaw_install.sh` for local inspection (or creates a simulated file when simulation is enabled).
- `nohup moltbot gateway > agent.log 2>&1 &` — suggested command to start the gateway (must be run locally by the operator).

Security Notes
- Do not run the installer on production hosts without review.
- Prefer to run installers in a disposable VM or container.
- ZTRAP refuses to auto-execute remote scripts or start network-exposed agent gateways.
