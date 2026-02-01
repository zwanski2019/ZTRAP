import os
import json
import tempfile

import security


def test_log_attempt_writes_file(tmp_path):
    tempfile_path = tmp_path / "access_logs.json"
    # Point module to temp file
    security.LOG_FILE = str(tempfile_path)
    # Ensure clean state
    if os.path.exists(security.LOG_FILE):
        os.remove(security.LOG_FILE)

    security.log_attempt("TEST_EVENT", "details here")
    assert os.path.exists(security.LOG_FILE)
    with open(security.LOG_FILE, "r") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[-1]["status"] == "TEST_EVENT"
    assert "timestamp" in data[-1]


def test_log_attempt_appends(tmp_path):
    tempfile_path = tmp_path / "access_logs.json"
    security.LOG_FILE = str(tempfile_path)
    # create base
    security.log_attempt("FIRST", "a")
    security.log_attempt("SECOND", "b")

    with open(security.LOG_FILE, "r") as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["status"] == "FIRST"
    assert data[1]["status"] == "SECOND"
