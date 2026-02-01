# Deploying ZTRAP to Streamlit Cloud

This document describes how to deploy ZTRAP to Streamlit Cloud for quick demos.

1. Push your branch to GitHub and open a Pull Request.
2. Go to https://streamlit.io/cloud and connect your GitHub account.
3. Create a new app and select this repository and the branch (e.g., `main` or your feature branch).
4. Set the **Entry file** to `app.py`.
5. Set the following **Environment variables** in the Streamlit app settings:
   - `ZTRAP_MASTER_KEY` — set a strong secret; defaults to `zwanski` if not set (for development only).
   - Optional: `ZTRAP_ENABLE_OPENCLAW=1`, `ZTRAP_ENABLE_WS=1` (enable features if desired).
6. Deploy and open the app.

> ⚠️ Security note: Use Streamlit Cloud environment variables or a secret manager; do not store secrets in the repo.
