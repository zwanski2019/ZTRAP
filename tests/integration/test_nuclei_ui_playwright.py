import os
import subprocess
import time
import requests
import pytest

pytestmark = pytest.mark.skipif(os.environ.get("PLAYWRIGHT_UI_TESTS", "0") != "1", reason="Playwright UI tests are disabled by default")

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

pytestmark = pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed in this environment")


def start_streamlit_in_bg(env):
    # start Streamlit in a background process
    cmd = ["streamlit", "run", "app.py", "--server.port", "8501"]
    return subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_nuclei_console_end_to_end(tmp_path):
    env = os.environ.copy()
    env["ZTRAP_FAKE_NUCLEI"] = "1"
    env["ZTRAP_ENABLE_WS"] = "1"
    env["ZTRAP_ENABLE_REST"] = "1"
    env["ZTRAP_REST_PORT"] = "8766"

    proc = start_streamlit_in_bg(env)
    try:
        # give server time to start
        time.sleep(4)
        # ensure REST health
        r = requests.get("http://127.0.0.1:8766/health", timeout=5)
        assert r.status_code == 200

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://127.0.0.1:8501")
            # wait for UI to load and the sidebar to be clickable
            page.wait_for_selector('text=COMMANDS')
            page.click('text=COMMANDS')
            # select NUCLEI-CONSOLE from the sidebar
            page.click('text=NUCLEI-CONSOLE')
            # start a scan
            page.wait_for_selector('text=START SCAN')
            page.click('text=START SCAN')
            # wait a moment for simulated scan to write logs
            time.sleep(1)
            # verify that REST /scans shows an entry
            r = requests.get("http://127.0.0.1:8766/scans", timeout=5)
            assert r.status_code == 200
            data = r.json()
            assert isinstance(data, list) and len(data) >= 1
            # verify log endpoint for the latest scan
            latest = data[0]["scan_id"]
            r2 = requests.get(f"http://127.0.0.1:8766/scans/{latest}/log", timeout=5)
            assert r2.status_code == 200
            assert "[SIM]" in r2.text
            browser.close()
    finally:
        proc.terminate()
        proc.wait(timeout=5)
