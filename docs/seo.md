# SEO & AI Discovery for ZTRAP

This document contains steps and files added to enable search engine & AI discovery for the ZTRAP Streamlit app.

Files added:
- `.streamlit/config.toml` — `enableStaticServing = true` so Streamlit serves `/app/static/` files from `static/`.
- `static/google5c6ccd94a91913a6.html` — Google site verification file.
- `static/sitemap.xml` — Sitemap listing important pages.
- `static/robots.txt` — Crawler rules.

App changes:
- `app.py` page config expanded with page title, icon, and menu items.
- Injected JSON-LD structured data via `components.html(...)` to present `SoftwareApplication` metadata to crawlers.
- Added hidden AI-friendly markup (first 200 chars hook) via `st.markdown(..., unsafe_allow_html=True)`.

Notes & verification:
- Verify ownership in Google Search Console by adding the provided verification file.
- Ensure you set up links from GitHub, LinkedIn, and personal site to increase entity authority.
- Be mindful of privacy/security: avoid publishing sensitive tooling via public static files.
