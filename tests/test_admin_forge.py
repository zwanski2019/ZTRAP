import os
import importlib
import textwrap
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import admin_forge


def test_get_dynamic_tools_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(admin_forge, "TOOLS_DIR", str(tmp_path))
    os.makedirs(admin_forge.TOOLS_DIR, exist_ok=True)
    assert admin_forge.get_dynamic_tools() == []


def test_get_dynamic_tools_list(tmp_path, monkeypatch):
    monkeypatch.setattr(admin_forge, "TOOLS_DIR", str(tmp_path))
    os.makedirs(admin_forge.TOOLS_DIR, exist_ok=True)
    p = os.path.join(admin_forge.TOOLS_DIR, "sample_tool.py")
    with open(p, "w") as f:
        f.write("def run():\n    print('ok')\n")
    assert admin_forge.get_dynamic_tools() == ["sample_tool"]


def test_run_dynamic_tool_executes(tmp_path, monkeypatch):
    monkeypatch.setattr(admin_forge, "TOOLS_DIR", str(tmp_path))
    os.makedirs(admin_forge.TOOLS_DIR, exist_ok=True)
    out_file = tmp_path / "out.txt"
    code = textwrap.dedent(f"""
    def run():
        with open('{out_file}', 'w') as f:
            f.write('ran')
    """)
    p = os.path.join(admin_forge.TOOLS_DIR, "writer.py")
    with open(p, "w") as f:
        f.write(code)

    admin_forge.run_dynamic_tool("writer")
    assert out_file.exists()
    assert out_file.read_text() == "ran"


def test_validate_and_install_deps_calls_pip(monkeypatch):
    calls = []

    def fake_run(cmd, check=True):
        calls.append(cmd)

    monkeypatch.setattr(admin_forge.subprocess, "run", fake_run)

    content = """
    import requests
    import streamlit
    from bs4 import BeautifulSoup
    """
    admin_forge.validate_and_install_deps(content)

    # Ensure pip install was invoked for requests and bs4
    pkgs = {tuple(c)[-1] for c in calls}
    assert "requests" in pkgs
    assert "bs4" in pkgs or "beautifulsoup4" in pkgs
