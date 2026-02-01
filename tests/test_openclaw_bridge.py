import os
import tempfile
import shutil
import builtins
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import openclaw_bridge as oc


def test_install_instructions_contains_review():
    instr = oc.install_instructions()
    assert "curl" in instr
    assert "review" in instr.lower()


def test_get_status_simulation(monkeypatch):
    monkeypatch.setenv("ZTRAP_OPENCLAW_SIMULATE", "1")
    s = oc.get_status()
    assert s.get("simulate") is True

    ok, path = oc.prepare_install_dry_run()
    assert ok is True
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = f.read()
    assert "SIMULATED" in data
    os.unlink(path)


def test_node_and_moltbot_detection(monkeypatch):
    # Simulate node and moltbot not present
    monkeypatch.setattr(shutil, "which", lambda x: None)
    assert oc.node_installed() is False
    assert oc.openclaw_installed() is False

    # Simulate node present
    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/node" if x == "node" else None)
    assert oc.node_installed() is False  # need both node and npm

    # Simulate both present
    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/node" if x in ("node","npm") else None)
    assert oc.node_installed() is True
