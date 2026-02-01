import os
import json
import time
import threading
import builtins
from unittest import mock
import sys
# Ensure repo root is on sys.path so tests can import module under test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nuclei_engine


def test_is_nuclei_installed(monkeypatch):
    monkeypatch.setattr(nuclei_engine.shutil, "which", lambda name: "/usr/bin/nuclei" if name == "nuclei" else None)
    assert nuclei_engine.is_nuclei_installed()
    monkeypatch.setattr(nuclei_engine.shutil, "which", lambda name: None)
    assert not nuclei_engine.is_nuclei_installed()


def test_install_nuclei_success(monkeypatch, tmp_path):
    # simulate successful subprocess.run
    monkeypatch.setattr(nuclei_engine.subprocess, "run", lambda *args, **kwargs: 0)
    # stub out st to capture messages via monkeypatching streamlit st
    class FakeSt:
        def warning(self, *a, **k): pass
        def success(self, *a, **k): pass
        def error(self, *a, **k): pass
    monkeypatch.setattr(nuclei_engine, "st", FakeSt())
    assert nuclei_engine.install_nuclei() is True


def test_install_nuclei_go_missing(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError("go not found")
    monkeypatch.setattr(nuclei_engine.subprocess, "run", fake_run)

    class FakeSt:
        def warning(self, *a, **k): pass
        def success(self, *a, **k): pass
        def error(self, *a, **k): pass
    monkeypatch.setattr(nuclei_engine, "st", FakeSt())
    assert nuclei_engine.install_nuclei() is False


def test_cooldown_and_record(tmp_path, monkeypatch):
    # Use temp DB file
    dbp = str(tmp_path / "nuclei.db")
    monkeypatch.setattr(nuclei_engine, "NUCLEI_DB_PATH", dbp)
    target = "https://example.com"
    # ensure allowed initially
    ok, reason = nuclei_engine.check_cooldown(target, cooldown_seconds=1, max_per_hour=2, db_path=dbp)
    assert ok
    nuclei_engine.record_scan(target, db_path=dbp)
    # immediate scan should fail due to cooldown
    ok2, reason2 = nuclei_engine.check_cooldown(target, cooldown_seconds=60, max_per_hour=2, db_path=dbp)
    assert not ok2


class DummyProc:
    def __init__(self, out_lines, returncode=0):
        self._lines = out_lines
        self.returncode = returncode
        self.stdout = self
        self._idx = 0
    def readline(self):
        time.sleep(0.01)
        if self._idx >= len(self._lines):
            return ''
        l = self._lines[self._idx]
        self._idx += 1
        return l

    def wait(self):
        return self.returncode


def test_run_scan_worker_writes_log(monkeypatch, tmp_path):
    # Use temp log dir
    monkeypatch.setattr(nuclei_engine, "LOG_DIR", str(tmp_path / "logs"))
    os.makedirs(nuclei_engine.LOG_DIR, exist_ok=True)

    dummy = DummyProc(["line1\n", "line2\n"], returncode=0)
    monkeypatch.setattr(nuclei_engine.subprocess, "Popen", lambda *a, **k: dummy)

    scan_id = "testscan123"
    nuclei_engine._scan_worker(scan_id, "https://example.com", ["critical"])
    logfile = os.path.join(nuclei_engine.LOG_DIR, f"{scan_id}.log")
    assert os.path.exists(logfile)
    with open(logfile, "r") as f:
        content = f.read()
    assert "line1" in content and "line2" in content

    status = nuclei_engine.get_scan_status(scan_id)
    assert status.get("finished") is True


def test_run_scan_async_and_get_log(monkeypatch, tmp_path):
    monkeypatch.setattr(nuclei_engine, "LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setattr(nuclei_engine, "NUCLEI_DB_PATH", str(tmp_path / "nuclei.db"))
    os.makedirs(nuclei_engine.LOG_DIR, exist_ok=True)

    dummy = DummyProc(["a\n", "b\n", "c\n"], returncode=0)
    monkeypatch.setattr(nuclei_engine.subprocess, "Popen", lambda *a, **k: dummy)

    scan_id = nuclei_engine.run_scan_async("https://example.com", ["high"])
    assert scan_id is not None

    # wait for thread to finish and write files
    time.sleep(0.1)

    log = nuclei_engine.get_scan_log(scan_id)
    assert "a" in log
    status = nuclei_engine.get_scan_status(scan_id)
    assert status.get("finished") is True or status.get("returncode") is not None
    # ensure DB recorded the scan
    conn = nuclei_engine._get_conn(nuclei_engine.NUCLEI_DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM scans WHERE target=?", ("https://example.com",))
    assert cur.fetchone()[0] >= 1
    conn.close()