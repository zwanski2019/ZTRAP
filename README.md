# ZTRAP

[![CI](https://github.com/zwanski2019/ZTRAP/actions/workflows/ci.yml/badge.svg)](https://github.com/zwanski2019/ZTRAP/actions/workflows/ci.yml) [![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

ZTRAP is a Streamlit-based Red Team console demo.

Quick start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

Configuration

- The allowed users can be configured via environment variable `ZTRAP_ALLOWED_USERS`.
  This should be a comma-separated list of usernames (default: current user).

Security notes

- Shell execution is disabled by default in the app. Use the "Enable shell execution" toggle to run commands.
- Background jobs started by the app are registered under `/tmp/ztrap_tasks.json` (for demo purposes).

If you want me to add automated tests or continuous integration, tell me what you'd like covered and I will add them. 🎯

WebSocket & Playwright notes

- To enable optional WebSocket live-tail for Nuclei logs, set `ZTRAP_ENABLE_WS=1` before launching the app. The WebSocket server binds to `127.0.0.1:8765` by default and is intended for local use only.
- To run the UI integration tests with Playwright, install `playwright` and set `PLAYWRIGHT_UI_TESTS=1` in the environment. Playwright also requires running `playwright install` once to fetch browser binaries. The integration tests are skipped by default in CI unless you explicitly enable them.

REST API & WebSocket

- To enable the optional REST API service (automatic, read-only endpoints for scans/logs), set `ZTRAP_ENABLE_REST=1`.
- To enable WebSocket broadcasting of live scan output, set `ZTRAP_ENABLE_WS=1`.
- To run simulated scans (useful for CI/Pipeline/UI tests), set `ZTRAP_FAKE_NUCLEI=1`. This avoids requiring `nuclei` or `go` and produces deterministic logs for testing.
