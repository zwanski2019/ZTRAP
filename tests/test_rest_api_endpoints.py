import os
import sys
import json
import sqlite3
import tempfile
import shutil

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
pytest.importorskip("flask")  # Skip these tests if Flask isn't available in the environment
from rest_api import app
import nuclei_engine


def setup_temp_env(tmp_path):
    # Prepare temp DB and LOG_DIR
    temp_db = str(tmp_path / "test_nuclei.db")
    temp_logdir = str(tmp_path / "logs")
    os.makedirs(temp_logdir, exist_ok=True)

    # Point nuclei_engine to these temp locations
    nuclei_engine.NUCLEI_DB_PATH = temp_db
    nuclei_engine.LOG_DIR = temp_logdir
    # Initialize DB
    nuclei_engine._init_db(temp_db)
    return temp_db, temp_logdir


def test_health_endpoint():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_scans_empty(tmp_path):
    setup_temp_env(tmp_path)
    client = app.test_client()
    r = client.get("/scans")
    assert r.status_code == 200
    assert r.get_json() == []


def test_scans_with_entry(tmp_path):
    db_path, logdir = setup_temp_env(tmp_path)
    # Insert a row
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("INSERT INTO scans (target, ts) VALUES (?, ?)", ("example.com", 123456.0))
    conn.close()

    client = app.test_client()
    r = client.get("/scans")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["target"] == "example.com"
    assert data[0]["scan_id"].startswith("scan_")


def test_log_and_status_endpoints(tmp_path):
    db_path, logdir = setup_temp_env(tmp_path)
    # Create a sample log and status file
    scan_id = "scan_42"
    log_fname = os.path.join(logdir, f"{scan_id}.log")
    status_fname = os.path.join(logdir, f"{scan_id}.status")
    with open(log_fname, "w") as f:
        f.write("line1\nline2\n")
    with open(status_fname, "w") as f:
        json.dump({"finished": True, "returncode": 0}, f)

    client = app.test_client()
    r_log = client.get(f"/scans/{scan_id}/log")
    assert r_log.status_code == 200
    assert b"line1" in r_log.data

    r_status = client.get(f"/scans/{scan_id}/status")
    assert r_status.status_code == 200
    assert r_status.get_json().get("finished") is True


def test_auth_token_enforcement(tmp_path, monkeypatch):
    db_path, logdir = setup_temp_env(tmp_path)
    # Set token
    monkeypatch.setenv("ZTRAP_REST_TOKEN", "sekret")
    client = app.test_client()

    r = client.get("/scans")
    assert r.status_code == 401

    r2 = client.get("/scans", headers={"Authorization": "Bearer sekret"})
    assert r2.status_code == 200
