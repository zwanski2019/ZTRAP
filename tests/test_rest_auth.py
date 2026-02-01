import os
import time
import requests
import subprocess
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nuclei_engine

try:
    import flask  # type: ignore
    FLASK_AVAILABLE = True
except Exception:
    FLASK_AVAILABLE = False


@pytest.mark.skipif(not FLASK_AVAILABLE, reason="Flask not installed in environment")
def test_rest_auth_disabled(monkeypatch):
    # Ensure when no token is set, endpoints are accessible
    monkeypatch.setenv("ZTRAP_ENABLE_REST", "1")
    monkeypatch.setenv("ZTRAP_REST_PORT", "8768")
    # Start rest server in background
    proc = subprocess.Popen(["python3", "-c", "import rest_api; import time; time.sleep(2)"], env=os.environ.copy())
    time.sleep(0.5)
    try:
        r = requests.get("http://127.0.0.1:8768/health", timeout=3)
        assert r.status_code == 200
    finally:
        proc.terminate()
        proc.wait()


@pytest.mark.skipif(not FLASK_AVAILABLE, reason="Flask not installed in environment")
def test_rest_auth_token(monkeypatch):
    token = "secrettoken123"
    monkeypatch.setenv("ZTRAP_ENABLE_REST", "1")
    monkeypatch.setenv("ZTRAP_REST_PORT", "8769")
    monkeypatch.setenv("ZTRAP_REST_TOKEN", token)
    proc = subprocess.Popen(["python3", "-c", "import rest_api; import time; time.sleep(2)"], env=os.environ.copy())
    time.sleep(0.5)
    try:
        r1 = requests.get("http://127.0.0.1:8769/scans", timeout=3)
        assert r1.status_code == 401
        r2 = requests.get("http://127.0.0.1:8769/scans", headers={"Authorization": f"Bearer {token}"}, timeout=3)
        assert r2.status_code == 200
    finally:
        proc.terminate()
        proc.wait()
